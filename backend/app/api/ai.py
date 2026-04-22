from __future__ import annotations

import re
import unicodedata
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai_service import (
    generate_advisor_answer,
    infer_exam_goal_from_question,
    infer_grade_from_question,
    infer_resource_type_from_question,
    infer_section_from_question,
    infer_subject_from_question,
    infer_subjects_from_question,
    rank_candidate_documents,
    select_recommended_documents,
    strip_recommended_ids_json,
    suggest_sections_for_exam_goal,
    to_advisor_document,
)
from app.config import get_settings
from app.db import get_db
from app.dependencies import get_current_user
from app.models import Document, User
from app.schemas import AiAdvisorDocument, AiAdvisorRequest, AiAdvisorResponse, AiAdvisorSubjectPlan


router = APIRouter(prefix='/ai', tags=['ai'])


def normalize_text(value: str | None) -> str:
    if not value:
        return ''
    normalized = unicodedata.normalize('NFD', value)
    normalized = ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')
    return normalized.lower().replace('đ', 'd').strip()


def tokenize_question(question: str) -> list[str]:
    normalized = normalize_text(question)
    normalized = re.sub(r'[^\w\s]', ' ', normalized, flags=re.UNICODE)
    return [token for token in normalized.split() if len(token) >= 2]


def has_meaningful_relevance(
    question: str,
    advisor_documents: list[AiAdvisorDocument],
    subjects: list[str] | None,
) -> bool:
    if not advisor_documents:
        return False

    tokens = tokenize_question(question)
    normalized_subjects = {normalize_text(subject) for subject in (subjects or []) if subject}
    best_score = 0

    for document in advisor_documents:
        haystack = normalize_text(
            f'{document.title} {document.description} {document.subject} {document.resource_type} {document.grade}'
        )
        score = sum(1 for token in tokens if token in haystack)
        if normalized_subjects and normalize_text(document.subject) in normalized_subjects:
            score += 3
        if score > best_score:
            best_score = score

    if normalized_subjects:
        return best_score >= 2
    return best_score >= 3


def normalize_subjects(subjects: list[str] | None) -> list[str] | None:
    if not subjects:
        return None
    deduped = [subject.strip() for subject in subjects if subject and subject.strip() and subject.strip() != 'Tất cả']
    if not deduped:
        return None
    return list(dict.fromkeys(deduped))


def build_study_plan_by_subject(subjects: list[str], advisor_documents: list[AiAdvisorDocument]) -> list[AiAdvisorSubjectPlan]:
    plans: list[AiAdvisorSubjectPlan] = []
    for index, subject in enumerate(subjects, start=1):
        docs = [document for document in advisor_documents if document.subject == subject][:3]
        recommendation = (
            f'Ưu tiên học {subject} theo thứ tự: tài liệu tổng hợp trước, sau đó đề cương, cuối cùng luyện đề để kiểm tra tiến độ.'
        )
        plans.append(
            AiAdvisorSubjectPlan(
                subject=subject,
                priority=index,
                recommendation=recommendation,
                documents=docs,
            )
        )
    return plans


@router.post('/advisor', response_model=AiAdvisorResponse)
def advisor(
    payload: AiAdvisorRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> AiAdvisorResponse:
    settings = get_settings()
    question = payload.question.strip()

    if len(question) > settings.ai_max_question_length:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cau hoi qua dai cho che do tu van hien tai.')

    inferred_grade = infer_grade_from_question(question)
    inferred_subjects = infer_subjects_from_question(question)
    if not inferred_subjects:
        inferred_subject = infer_subject_from_question(question)
        inferred_subjects = [inferred_subject] if inferred_subject else []
    inferred_section = infer_section_from_question(question)
    inferred_resource_type = infer_resource_type_from_question(question)
    inferred_exam_goal = infer_exam_goal_from_question(question)

    applied_grade = payload.grade or inferred_grade or (current_user.grade if current_user.role == 'student' else None)
    payload_subjects = payload.subjects or ([payload.subject] if payload.subject else None)
    applied_subjects = normalize_subjects(payload_subjects) or normalize_subjects(inferred_subjects)
    applied_subject = applied_subjects[0] if applied_subjects else None
    applied_exam_goal = payload.exam_goal or inferred_exam_goal
    suggested_sections = suggest_sections_for_exam_goal(applied_exam_goal)
    applied_section = payload.section or inferred_section
    applied_resource_type = payload.resource_type or inferred_resource_type

    query = select(Document)
    if applied_grade and applied_grade != 'Tất cả':
        query = query.where(Document.grade.in_([applied_grade, 'Tất cả']))

    documents = db.scalars(query.order_by(Document.created_at.desc()).limit(max(settings.ai_candidate_limit * 10, 50))).all()

    candidate_documents = rank_candidate_documents(
        documents,
        question,
        subjects=applied_subjects,
        exam_goal=applied_exam_goal,
        section=applied_section,
        suggested_sections=suggested_sections,
        resource_type=applied_resource_type,
        grade=applied_grade,
        limit=settings.ai_candidate_limit,
    )
    advisor_documents = [to_advisor_document(document) for document in candidate_documents]

    llm_documents = advisor_documents
    if not has_meaningful_relevance(question, advisor_documents, applied_subjects):
        llm_documents = []

    plan_by_subject = build_study_plan_by_subject(applied_subjects or [], llm_documents)

    try:
        answer = generate_advisor_answer(
            settings=settings,
            current_user=current_user,
            question=question,
            documents=llm_documents,
            grade=applied_grade,
            subjects=applied_subjects,
            section=applied_section,
            resource_type=applied_resource_type,
            exam_goal=applied_exam_goal,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Khong the ket noi tro ly AI luc nay. Vui long thu lai sau.',
        ) from exc

    recommended = select_recommended_documents(answer, llm_documents) if llm_documents else []
    cleaned_answer = strip_recommended_ids_json(answer)

    return AiAdvisorResponse(
        answer=cleaned_answer,
        recommended_documents=recommended,
        applied_grade=applied_grade,
        applied_subject=applied_subject,
        applied_subjects=applied_subjects,
        applied_section=applied_section,
        applied_resource_type=applied_resource_type,
        applied_exam_goal=applied_exam_goal,
        plan_by_subject=plan_by_subject,
    )
