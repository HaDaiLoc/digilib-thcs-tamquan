#!/usr/bin/env python3
"""Seed fake data into the Digital Library database.

Usage (from workspace root):
  python backend/scripts/seed_fake_data.py --users 20 --documents 200 --donations 50

Requires: pip install Faker
Run from project root so the `app` package (backend/app) is importable.
"""
import argparse
import os
import sys
import uuid
import random
from datetime import datetime, timezone

# Make sure `backend` is on sys.path so `import app` works when running from repo root
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, BACKEND_DIR)

from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models import User, Document, Donation
from app.security import hash_password


def create_users(session, faker, count: int, password_plain: str) -> list[User]:
    created = []
    attempts = 0
    while len(created) < count and attempts < count * 5:
        attempts += 1
        uid = str(uuid.uuid4())
        full_name = faker.name()
        email = faker.unique.email()
        student_id = f'HS-{faker.random_number(digits=6)}'
        password_hash = hash_password(password_plain)
        role = random.choices(['student', 'teacher', 'school'], weights=[85, 14, 1])[0]
        grade = random.choice(['Khối 6', 'Khối 7', 'Khối 8', 'Khối 9', 'Tất cả'])
        created_at = datetime.now(timezone.utc)

        user = User(
            id=uid,
            full_name=full_name,
            email=email,
            student_id=student_id,
            password_hash=password_hash,
            role=role,
            grade=grade,
            created_at=created_at,
        )

        try:
            session.add(user)
            session.commit()
            created.append(user)
        except IntegrityError:
            session.rollback()
            faker.unique.clear()
            continue

    return created


def create_documents(session, faker, count: int, user_objs: list[User]) -> list[Document]:
    subjects = ['Toán', 'Văn', 'Lý', 'Hóa', 'Sinh', 'Sử', 'Địa', 'Anh', 'Tin học', 'Hướng dẫn']
    resource_types = ['Ebook', 'Tài liệu', 'Slide', 'Đề thi', 'Đề cương', 'Bài giảng']
    sections = ['library', 'exams', 'slides', 'library', 'exams']

    created = []
    for _ in range(count):
        uid = str(uuid.uuid4())
        title = faker.sentence(nb_words=6)
        description = faker.paragraph(nb_sentences=4)
        author = faker.name()
        subject = random.choice(subjects)
        grade = random.choice(['Khối 6', 'Khối 7', 'Khối 8', 'Khối 9', 'Tất cả'])
        section = random.choice(sections)
        resource_type = random.choice(resource_types)
        image = f'https://picsum.photos/seed/{uid[:8]}/600/400'
        pdf_url = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
        owner_role = random.choice(['school', 'teacher', 'student'])
        created_by = random.choice(user_objs)
        now = datetime.now(timezone.utc)

        doc = Document(
            id=uid,
            title=title,
            description=description,
            author=author,
            subject=subject,
            grade=grade,
            section=section,
            resource_type=resource_type,
            image=image,
            pdf_url=pdf_url,
            owner_role=owner_role,
            created_by_id=created_by.id,
            created_by_name=created_by.full_name,
            created_at=now,
            updated_at=now,
        )

        created.append(doc)

    session.add_all(created)
    session.commit()
    return created


def create_donations(session, faker, count: int, user_objs: list[User]) -> list[Donation]:
    conditions = ['Mới', 'Còn mới', 'Tốt', 'Hư hỏng nhẹ', 'Cũ']
    created = []
    for _ in range(count):
        uid = str(uuid.uuid4())
        full_name = faker.name()
        book_name = faker.sentence(nb_words=4)
        grade = random.choice(['Khối 6', 'Khối 7', 'Khối 8', 'Khối 9'])
        condition = random.choice(conditions)
        message = faker.sentence(nb_words=10)
        submitted_by = random.choice(user_objs)
        submitted_by_role = submitted_by.role
        now = datetime.now(timezone.utc)

        don = Donation(
            id=uid,
            full_name=full_name,
            book_name=book_name,
            grade=grade,
            condition=condition,
            message=message,
            submitted_by_id=submitted_by.id,
            submitted_by_role=submitted_by_role,
            created_at=now,
        )
        created.append(don)

    session.add_all(created)
    session.commit()
    return created


def main():
    parser = argparse.ArgumentParser(description='Seed fake data into Digital Library DB')
    parser.add_argument('--users', type=int, default=10, help='Number of users to create')
    parser.add_argument('--documents', type=int, default=50, help='Number of documents to create')
    parser.add_argument('--donations', type=int, default=20, help='Number of donations to create')
    parser.add_argument('--password', type=str, default='password123', help='Plain password for all generated users')
    args = parser.parse_args()

    faker = Faker('vi_VN')
    faker.seed_instance(42)

    session = SessionLocal()
    try:
        # load existing users (including migration-seeded ones)
        existing_users = session.scalars(select(User)).all()

        new_users = []
        if args.users > 0:
            print(f'Creating {args.users} users...')
            new_users = create_users(session, faker, args.users, args.password)
            print(f'  -> created {len(new_users)} users')

        # refresh users list
        users = session.scalars(select(User)).all()

        if args.documents > 0:
            print(f'Creating {args.documents} documents...')
            docs = create_documents(session, faker, args.documents, users)
            print(f'  -> created {len(docs)} documents')

        if args.donations > 0:
            print(f'Creating {args.donations} donations...')
            dons = create_donations(session, faker, args.donations, users)
            print(f'  -> created {len(dons)} donations')

        print('Seeding finished.')
    finally:
        session.close()


if __name__ == '__main__':
    main()
