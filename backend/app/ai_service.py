import json
import re
import unicodedata
from urllib import error, request

from app.config import Settings
from app.models import Document, User
from app.schemas import AiAdvisorDocument


def normalize_text(text: str | None) -> str:
    if not text:
        return ''
    value = unicodedata.normalize('NFD', text)
    value = ''.join(ch for ch in value if unicodedata.category(ch) != 'Mn')
    return value.lower().replace('đ', 'd').strip()


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def equals_normalized(a: str | None, b: str | None) -> bool:
    return normalize_text(a) == normalize_text(b)


GRADE_KEYWORDS = {
    'Khối 6': ['khoi 6', 'lop 6', 'toan 6', 'van 6', 'anh 6'],
    'Khối 7': ['khoi 7', 'lop 7', 'toan 7', 'van 7', 'anh 7'],
    'Khối 8': ['khoi 8', 'lop 8', 'toan 8', 'van 8', 'anh 8'],
    'Khối 9': ['khoi 9', 'lop 9', 'toan 9', 'van 9', 'anh 9', 'vao 10'],
}

SUBJECT_KEYWORDS = {
    'Toán': ['toan'],
    'Văn': ['ngu van', 'van hoc', 'bai tho', 'tho', 'van'],
    'Tiếng Anh': ['tieng anh', 'anh van'],
    'Vật lý': ['vat ly', 'mon ly'],
    'Hóa học': ['hoa hoc', 'mon hoa'],
    'Sinh học': ['sinh hoc'],
    'Lịch sử': ['lich su'],
    'Địa lý': ['dia ly'],
}

SECTION_KEYWORDS = {
    'library': ['ebook', 'sach', 'tai lieu', 'thu vien'],
    'exams': ['de thi', 'de cuong', 'on thi'],
    'slides': ['slide', 'bai giang'],
}

RESOURCE_TYPE_KEYWORDS = {
    'Ebook': ['ebook', 'sach'],
    'Tài liệu': ['tai lieu'],
    'Đề thi': ['de thi'],
    'Đề cương': ['de cuong'],
    'Slide': ['slide', 'bai giang'],
}

EXAM_GOAL_KEYWORDS = {
    'entrance_10': ['thi vao 10', 'luyen thi vao 10', 'on thi vao 10'],
    'midterm': ['giua ky', 'kiem tra giua ky'],
    'final': ['cuoi ky', 'kiem tra cuoi ky'],
}


def tokenize_question(question: str) -> list[str]:
    normalized = normalize_text(question)
    normalized = re.sub(r'[^\w\s]', ' ', normalized, flags=re.UNICODE)
    return [token for token in normalized.split() if len(token) >= 2]


def infer_value_from_keywords(question: str, keyword_map: dict[str, list[str]]) -> str | None:
    normalized = normalize_text(question)
    for value, keywords in keyword_map.items():
        if contains_any(normalized, keywords):
            return value
    return None


def infer_grade_from_question(question: str) -> str | None:
    return infer_value_from_keywords(question, GRADE_KEYWORDS)


def infer_subject_from_question(question: str) -> str | None:
    subjects = infer_subjects_from_question(question)
    return subjects[0] if subjects else None


def infer_subjects_from_question(question: str) -> list[str]:
    normalized = normalize_text(question)
    detected: list[str] = []
    for subject, keywords in SUBJECT_KEYWORDS.items():
        if contains_any(normalized, keywords):
            detected.append(subject)
    return detected


def infer_section_from_question(question: str) -> str | None:
    return infer_value_from_keywords(question, SECTION_KEYWORDS)


def infer_resource_type_from_question(question: str) -> str | None:
    return infer_value_from_keywords(question, RESOURCE_TYPE_KEYWORDS)


def infer_exam_goal_from_question(question: str) -> str | None:
    return infer_value_from_keywords(question, EXAM_GOAL_KEYWORDS)


def suggest_sections_for_exam_goal(exam_goal: str | None) -> list[str] | None:
    if exam_goal == 'entrance_10':
        return ['exams', 'slides', 'library']
    if exam_goal in {'midterm', 'final'}:
        return ['exams', 'slides']
    return None


def score_document(
    document: Document,
    tokens: list[str],
    *,
    subjects: list[str] | None,
    exam_goal: str | None,
    section: str | None = None,
    suggested_sections: list[str] | None = None,
    resource_type: str | None = None,
    grade: str | None = None,
) -> int:
    score = 0

    doc_title = normalize_text(document.title)
    doc_desc = normalize_text(document.description)
    doc_subject = normalize_text(document.subject)
    doc_grade = normalize_text(document.grade)
    doc_resource_type = normalize_text(document.resource_type)
    doc_author = normalize_text(document.author)

    haystack = ' '.join([doc_title, doc_desc, doc_author, doc_subject, doc_grade, doc_resource_type])

    for token in tokens:
        if token in haystack:
            score += 1
        if token in doc_subject:
            score += 2
        if token in doc_title:
            score += 3
        if token in doc_desc:
            score += 1

    if subjects and any(equals_normalized(document.subject, subject) for subject in subjects):
        score += 10

    if grade and not equals_normalized(grade, 'Tất cả'):
        if equals_normalized(document.grade, grade):
            score += 5
        elif equals_normalized(document.grade, 'Tất cả'):
            score += 2

    if section and not equals_normalized(section, 'Tất cả') and equals_normalized(document.section, section):
        score += 4
    elif suggested_sections and document.section in suggested_sections:
        idx = suggested_sections.index(document.section)
        score += max(3 - idx, 1)

    if resource_type and not equals_normalized(resource_type, 'Tất cả') and equals_normalized(document.resource_type, resource_type):
        score += 4

    if exam_goal == 'entrance_10':
        if document.section == 'exams':
            score += 5
        if any(equals_normalized(document.resource_type, value) for value in ('Đề thi', 'Đề cương')):
            score += 6
        if equals_normalized(document.grade, 'Khối 9'):
            score += 3
    elif exam_goal in {'midterm', 'final'}:
        if document.section == 'exams':
            score += 3
        if any(equals_normalized(document.resource_type, value) for value in ('Đề thi', 'Đề cương')):
            score += 3

    return score


def rank_candidate_documents(
    documents: list[Document],
    question: str,
    *,
    subjects: list[str] | None,
    exam_goal: str | None,
    section: str | None = None,
    suggested_sections: list[str] | None = None,
    resource_type: str | None = None,
    grade: str | None = None,
    limit: int,
) -> list[Document]:
    tokens = tokenize_question(question)
    ranked = [
        (
            score_document(
                document,
                tokens,
                subjects=subjects,
                exam_goal=exam_goal,
                section=section,
                suggested_sections=suggested_sections,
                resource_type=resource_type,
                grade=grade,
            ),
            document,
        )
        for document in documents
    ]
    ranked.sort(key=lambda item: (item[0], item[1].created_at), reverse=True)
    return [document for _, document in ranked[:limit]]


def to_advisor_document(document: Document) -> AiAdvisorDocument:
    return AiAdvisorDocument(
        id=document.id,
        title=document.title,
        description=document.description,
        subject=document.subject,
        grade=document.grade,
        section=document.section,
        resource_type=document.resource_type,
        author=document.author,
        pdf_url=document.pdf_url,
    )


def build_messages(
    *,
    current_user: User,
    question: str,
    documents: list[AiAdvisorDocument],
    grade: str | None,
    subjects: list[str] | None,
    section: str | None,
    resource_type: str | None,
    exam_goal: str | None,
) -> list[dict[str, str]]:
    has_document_context = bool(documents)

    document_context = '\n\n'.join(
        (
            f"Tai lieu {index}:\n"
            f"- ID: {document.id}\n"
            f"- Tieu de: {document.title}\n"
            f"- Mo ta: {document.description}\n"
            f"- Mon hoc: {document.subject}\n"
            f"- Khoi: {document.grade}\n"
            f"- Khu vuc: {document.section}\n"
            f"- Loai: {document.resource_type}\n"
            f"- Tac gia: {document.author}\n"
            f"- Link PDF: {document.pdf_url}"
        )
        for index, document in enumerate(documents, start=1)
    )

    learner_context = (
        f"Vai tro nguoi dung: {current_user.role}\n"
        f"Khoi mac dinh cua nguoi dung: {current_user.grade}\n"
        f"Bo loc dang ap dung: grade={grade or 'khong co'}, subjects={', '.join(subjects or []) or 'khong co'}, "
        f"section={section or 'khong co'}, resource_type={resource_type or 'khong co'}, exam_goal={exam_goal or 'khong co'}"
    )

    if has_document_context:
        system_content = (
            'Ban la tro ly hoc tap cho thu vien so THCS Tam Quan. '
            'Ban vua tra loi kien thuc mon hoc, vua goi y hoc lieu khi danh sach tai lieu da duoc cung cap. '
            'Quy tac: '
            '- Uu tien dua tren danh sach tai lieu duoc cung cap de goi y hoc lieu. '
            '- Co the bo sung giai thich kien thuc tong quan cho hoc sinh bang ngon ngu de hieu. '
            '- Khong duoc bịa them tai lieu ngoai danh sach. '
            '- Ket thuc bang 1 dong JSON: {"recommended_ids": [...]} (toi da 5 ID, neu khong co thi []). '
            '- Tra loi bang tieng Viet than thien voi hoc sinh THCS.'
        )
        user_content = (
            f"{learner_context}\n\n"
            f"Cau hoi cua hoc sinh: {question}\n\n"
            f"Danh sach tai lieu ung vien (moi tai lieu co mot ID duy nhat):\n{document_context}\n\n"
            'Hay tra loi cau hoi theo cach de hieu, va neu phu hop thi de xuat tai lieu trong danh sach. '
            'Ket thuc bang JSON: {"recommended_ids": [...]}.'
        )
    else:
        system_content = (
            'Ban la tro ly hoc tap cho hoc sinh THCS Tam Quan. '
            'Nhiem vu: tra loi cac cau hoi kien thuc mon hoc, dinh huong cach hoc, va de xuat huong on tap thuc te. '
            'Hien tai khong co tai lieu nao trong CSDL phu hop de de xuat truc tiep, '
            'vi vay khong duoc bịa tai lieu cu the hoac ID tai lieu. '
            'Ket thuc bang 1 dong JSON: {"recommended_ids": []}. '
            '- Tra loi bang tieng Viet ro rang, ngan gon, de hoc sinh de hieu.'
        )
        user_content = (
            f"{learner_context}\n\n"
            f"Cau hoi cua hoc sinh: {question}\n\n"
            'Hay tra loi kien thuc mon hoc hoac dinh huong cach hoc phu hop voi cau hoi. '
            'Vi khong co tai lieu ung vien, hay ket thuc bang JSON: {"recommended_ids": []}.'
        )

    return [
        {
            'role': 'system',
            'content': system_content,
        },
        {
            'role': 'user',
            'content': user_content,
        },
    ]



def _iter_api_keys(settings: Settings) -> list[str]:
    candidates = list(settings.ai_api_keys or [])
    if settings.nvidia_api_key:
        candidates.append(settings.nvidia_api_key)

    deduped: list[str] = []
    seen: set[str] = set()
    for token in candidates:
        token = token.strip()
        if not token or token in seen:
            continue
        seen.add(token)
        deduped.append(token)
    return deduped


def _should_try_next_token(status_code: int) -> bool:
    return status_code in {401, 403, 408, 409, 425, 429} or status_code >= 500
def generate_advisor_answer(
    *,
    settings: Settings,
    current_user: User,
    question: str,
    documents: list[AiAdvisorDocument],
    grade: str | None,
    subjects: list[str] | None,
    section: str | None,
    resource_type: str | None,
    exam_goal: str | None,
) -> str:
    api_keys = _iter_api_keys(settings)
    if not api_keys:
        raise RuntimeError('AI_API_KEY is missing.')

    messages = build_messages(
        current_user=current_user,
        question=question,
        documents=documents,
        grade=grade,
        subjects=subjects,
        section=section,
        resource_type=resource_type,
        exam_goal=exam_goal,
    )
    payload = {
        'model': settings.nvidia_model,
        'messages': messages,
        'temperature': 0.2,
        'top_p': 0.7,
        'max_tokens': settings.ai_max_response_tokens,
        'stream': False,
    }

    last_error: Exception | None = None

    for index, api_key in enumerate(api_keys, start=1):
        http_request = request.Request(
            url=f"{settings.nvidia_api_base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            method='POST',
        )

        try:
            with request.urlopen(http_request, timeout=settings.ai_request_timeout_seconds) as response:
                response_payload = json.loads(response.read().decode('utf-8'))

            choices = response_payload.get('choices') or []
            if not choices:
                raise RuntimeError('AI service returned an empty response.')

            content = choices[0].get('message', {}).get('content', '').strip()
            if not content:
                raise RuntimeError('AI service returned no answer content.')

            return content
        except error.HTTPError as exc:
            last_error = exc
            if index < len(api_keys) and _should_try_next_token(exc.code):
                continue
            raise RuntimeError(f'AI request failed with status {exc.code}.') from exc
        except error.URLError as exc:
            last_error = exc
            if index < len(api_keys):
                continue
            raise RuntimeError('Unable to reach AI service.') from exc

    if last_error is not None:
        raise RuntimeError('AI request failed after trying all configured API keys.') from last_error

    raise RuntimeError('AI request failed before sending request.')


def parse_recommended_ids(answer: str) -> list[str]:
    array_match = re.search(
        r'recommended_ids\s*"?\s*:\s*\[([^\]]*)\]',
        answer,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not array_match:
        return []

    array_text = array_match.group(1)
    token_matches = re.findall(r'[A-Za-z0-9][A-Za-z0-9_-]*', array_text)
    if token_matches:
        return list(dict.fromkeys(token_matches))

    patterns = [
        r'```(?:json)?\s*(\{[^`]*"recommended_ids"\s*:\s*\[[^\]]*\][^`]*\})\s*```',
        r'(\{"recommended_ids"\s*:\s*\[[^\]]*\]\s*\})',
    ]
    for pattern in patterns:
        match = re.search(pattern, answer, re.DOTALL | re.IGNORECASE)
        if not match:
            continue
        try:
            data = json.loads(match.group(1))
            ids = data.get('recommended_ids', [])
            normalized = [str(i).strip() for i in ids if str(i).strip()]
            if normalized:
                return list(dict.fromkeys(normalized))
        except json.JSONDecodeError:
            continue

    return []


def strip_recommended_ids_json(answer: str) -> str:
    patterns = [
        r'\n*```(?:json)?\s*\{[^`]*"recommended_ids"\s*:\s*\[[^\]]*\][^`]*\}\s*```\s*$',
        r'\n*\{\s*"recommended_ids"\s*:\s*\[[^\]]*\]\s*\}\s*$',
    ]
    cleaned = answer
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'\n*\s*(ket\s*thuc\s*bang\s*json\s*:?)\s*$', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def select_recommended_documents(
    answer: str,
    advisor_documents: list[AiAdvisorDocument],
    fallback_limit: int = 5,
) -> list[AiAdvisorDocument]:
    recommended_ids = parse_recommended_ids(answer)
    if recommended_ids:
        doc_map = {doc.id: doc for doc in advisor_documents}
        selected = [doc_map[doc_id] for doc_id in recommended_ids if doc_id in doc_map]
        if selected:
            return selected
    return advisor_documents[:fallback_limit]
