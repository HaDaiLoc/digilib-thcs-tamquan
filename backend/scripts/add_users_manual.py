#!/usr/bin/env python3
"""Add or update three specific users (school, teacher, student).

Run from workspace root:
  python backend/scripts/add_users_manual.py

This script imports the app package and uses `hash_password` to compute the stored password hash.
"""
import os
import sys
from datetime import datetime, timezone

# Ensure backend package is importable when running from repo root
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.db import SessionLocal
from app.models import User
from app.security import hash_password


USERS = [
    {
        'id': 'u-school',
        'full_name': 'Ban quản trị thư viện số',
        'email': 'school@tamquan.edu.vn',
        'student_id': 'SCH-001',
        'role': 'school',
        'grade': 'Khối 9',
    },
    {
        'id': 'u-teacher',
        'full_name': 'Trần Thị Kim Chi',
        'email': 'teacher@tamquan.edu.vn',
        'student_id': 'GV-001',
        'role': 'teacher',
        'grade': 'Khối 9',
    },
    {
        'id': 'u-student',
        'full_name': 'Hà Đại Lộc',
        'email': 'student@tamquan.edu.vn',
        'student_id': 'HS-001',
        'role': 'student',
        'grade': 'Khối 8',
    },
]


def main(password_plain: str = '123456') -> None:
    now = datetime.now(timezone.utc)
    session = SessionLocal()
    try:
        for u in USERS:
            existing = session.query(User).filter(User.email == u['email']).one_or_none()
            hashed = hash_password(password_plain)
            if existing:
                existing.full_name = u['full_name']
                existing.student_id = u['student_id']
                existing.password_hash = hashed
                existing.role = u['role']
                existing.grade = u['grade']
                session.add(existing)
                print(f"Updated user: {u['email']}")
            else:
                new = User(
                    id=u['id'],
                    full_name=u['full_name'],
                    email=u['email'],
                    student_id=u['student_id'],
                    password_hash=hashed,
                    role=u['role'],
                    grade=u['grade'],
                    created_at=now,
                )
                session.add(new)
                print(f"Inserted user: {u['email']}")

        session.commit()
        print('Done.')
    finally:
        session.close()


if __name__ == '__main__':
    main()
