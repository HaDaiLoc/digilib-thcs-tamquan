"""initial schema with seed data

Revision ID: 20260314_0001
Revises:
Create Date: 2026-03-14 10:00:00.000000

"""

from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa

from app.security import hash_password


# revision identifiers, used by Alembic.
revision = '20260314_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('student_id', sa.String(length=64), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=32), nullable=False),
        sa.Column('grade', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_student_id', 'users', ['student_id'], unique=True)

    op.create_table(
        'documents',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=100), nullable=False),
        sa.Column('grade', sa.String(length=32), nullable=False),
        sa.Column('section', sa.String(length=32), nullable=False),
        sa.Column('resource_type', sa.String(length=64), nullable=False),
        sa.Column('image', sa.Text(), nullable=False),
        sa.Column('pdf_url', sa.Text(), nullable=False),
        sa.Column('owner_role', sa.String(length=32), nullable=False),
        sa.Column('created_by_id', sa.String(length=64), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_by_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_documents_created_by_id', 'documents', ['created_by_id'], unique=False)
    op.create_index('ix_documents_grade', 'documents', ['grade'], unique=False)
    op.create_index('ix_documents_section', 'documents', ['section'], unique=False)
    op.create_index('ix_documents_subject', 'documents', ['subject'], unique=False)

    op.create_table(
        'donations',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('book_name', sa.String(length=255), nullable=False),
        sa.Column('grade', sa.String(length=32), nullable=False),
        sa.Column('condition', sa.String(length=64), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('submitted_by_id', sa.String(length=64), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('submitted_by_role', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_donations_submitted_by_id', 'donations', ['submitted_by_id'], unique=False)

    users_table = sa.table(
        'users',
        sa.column('id', sa.String),
        sa.column('full_name', sa.String),
        sa.column('email', sa.String),
        sa.column('student_id', sa.String),
        sa.column('password_hash', sa.String),
        sa.column('role', sa.String),
        sa.column('grade', sa.String),
        sa.column('created_at', sa.DateTime(timezone=True)),
    )
    documents_table = sa.table(
        'documents',
        sa.column('id', sa.String),
        sa.column('title', sa.String),
        sa.column('description', sa.Text),
        sa.column('author', sa.String),
        sa.column('subject', sa.String),
        sa.column('grade', sa.String),
        sa.column('section', sa.String),
        sa.column('resource_type', sa.String),
        sa.column('image', sa.Text),
        sa.column('pdf_url', sa.Text),
        sa.column('owner_role', sa.String),
        sa.column('created_by_id', sa.String),
        sa.column('created_by_name', sa.String),
        sa.column('created_at', sa.DateTime(timezone=True)),
        sa.column('updated_at', sa.DateTime(timezone=True)),
    )
    donations_table = sa.table(
        'donations',
        sa.column('id', sa.String),
        sa.column('full_name', sa.String),
        sa.column('book_name', sa.String),
        sa.column('grade', sa.String),
        sa.column('condition', sa.String),
        sa.column('message', sa.Text),
        sa.column('submitted_by_id', sa.String),
        sa.column('submitted_by_role', sa.String),
        sa.column('created_at', sa.DateTime(timezone=True)),
    )

    now = datetime(2026, 3, 14, 0, 0, tzinfo=timezone.utc)
    op.bulk_insert(
        users_table,
        [
            {
                'id': 'u-school',
                'full_name': 'Ban quản trị thư viện số',
                'email': 'school@tamquan.edu.vn',
                'student_id': 'SCH-001',
                'password_hash': hash_password('123456'),
                'role': 'school',
                'grade': 'Khối 9',
                'created_at': now,
            },
            {
                'id': 'u-teacher',
                'full_name': 'Cô Nguyễn Thị Hoa',
                'email': 'teacher@tamquan.edu.vn',
                'student_id': 'GV-001',
                'password_hash': hash_password('123456'),
                'role': 'teacher',
                'grade': 'Khối 9',
                'created_at': now,
            },
            {
                'id': 'u-student',
                'full_name': 'Trần Minh Khoa',
                'email': 'student@tamquan.edu.vn',
                'student_id': 'HS-001',
                'password_hash': hash_password('123456'),
                'role': 'student',
                'grade': 'Khối 8',
                'created_at': now,
            },
        ],
    )

    op.bulk_insert(
        documents_table,
        [
            {
                'id': 'doc-1',
                'title': 'Ebook Toán 9 - Ôn thi vào 10',
                'description': 'Tài liệu tổng hợp kiến thức trọng tâm và bài tập ôn thi dành cho học sinh khối 9.',
                'author': 'Nhà trường THCS Tam Quan',
                'subject': 'Toán',
                'grade': 'Khối 9',
                'section': 'library',
                'resource_type': 'Ebook',
                'image': 'https://www.superprof.co.in/blog/wp-content/uploads/2021/09/image3-2.png',
                'pdf_url': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
                'owner_role': 'school',
                'created_by_id': 'u-school',
                'created_by_name': 'Ban quản trị thư viện số',
                'created_at': datetime(2026, 3, 1, 8, 0, tzinfo=timezone.utc),
                'updated_at': datetime(2026, 3, 1, 8, 0, tzinfo=timezone.utc),
            },
            {
                'id': 'doc-2',
                'title': 'Ngữ văn 9 - Tuyển tập bài văn mẫu',
                'description': 'Bộ sưu tập bài văn mẫu và hướng dẫn lập dàn ý cho học sinh cuối cấp.',
                'author': 'Cô Nguyễn Thị Hoa',
                'subject': 'Văn',
                'grade': 'Khối 9',
                'section': 'library',
                'resource_type': 'Tài liệu',
                'image': 'https://cbqqo.edu.vn/storage/app/public/photos/7/8xprovn_hieunh_170304100311images.jpg',
                'pdf_url': 'https://www.orimi.com/pdf-test.pdf',
                'owner_role': 'teacher',
                'created_by_id': 'u-teacher',
                'created_by_name': 'Cô Nguyễn Thị Hoa',
                'created_at': datetime(2026, 3, 2, 8, 0, tzinfo=timezone.utc),
                'updated_at': datetime(2026, 3, 2, 8, 0, tzinfo=timezone.utc),
            },
            {
                'id': 'doc-3',
                'title': 'Đề cương ôn tập Toán 9 - Học kỳ 1',
                'description': 'Đề cương theo chuyên đề với phần trắc nghiệm và tự luận để học sinh luyện tập.',
                'author': 'Tổ Toán',
                'subject': 'Toán',
                'grade': 'Khối 9',
                'section': 'exams',
                'resource_type': 'Đề cương',
                'image': 'https://img.freepik.com/free-vector/math-concept-illustration_114360-3916.jpg',
                'pdf_url': 'https://www.africau.edu/images/default/sample.pdf',
                'owner_role': 'teacher',
                'created_by_id': 'u-teacher',
                'created_by_name': 'Cô Nguyễn Thị Hoa',
                'created_at': datetime(2026, 3, 3, 8, 0, tzinfo=timezone.utc),
                'updated_at': datetime(2026, 3, 3, 8, 0, tzinfo=timezone.utc),
            },
            {
                'id': 'doc-4',
                'title': 'Đề thi thử Ngữ văn vào 10 - Năm 2024',
                'description': 'Đề thi thử bám sát cấu trúc tuyển sinh, có đáp án tham khảo.',
                'author': 'Nhà trường THCS Tam Quan',
                'subject': 'Văn',
                'grade': 'Khối 9',
                'section': 'exams',
                'resource_type': 'Đề thi',
                'image': 'https://img.freepik.com/free-vector/history-concept-illustration_114360-1123.jpg',
                'pdf_url': 'https://www.clickdimensions.com/links/TestPDFfile.pdf',
                'owner_role': 'school',
                'created_by_id': 'u-school',
                'created_by_name': 'Ban quản trị thư viện số',
                'created_at': datetime(2026, 3, 4, 8, 0, tzinfo=timezone.utc),
                'updated_at': datetime(2026, 3, 4, 8, 0, tzinfo=timezone.utc),
            },
            {
                'id': 'doc-5',
                'title': 'Slide Bài giảng: Hệ thức lượng trong tam giác',
                'description': 'Slide minh họa ngắn gọn, trực quan cho tiết học ôn tập hình học 9.',
                'author': 'Thầy Tùng',
                'subject': 'Toán',
                'grade': 'Khối 9',
                'section': 'slides',
                'resource_type': 'Slide',
                'image': 'https://img.freepik.com/free-vector/presentation-concept-illustration_114360-155.jpg',
                'pdf_url': 'https://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf',
                'owner_role': 'teacher',
                'created_by_id': 'u-teacher',
                'created_by_name': 'Cô Nguyễn Thị Hoa',
                'created_at': datetime(2026, 3, 5, 8, 0, tzinfo=timezone.utc),
                'updated_at': datetime(2026, 3, 5, 8, 0, tzinfo=timezone.utc),
            },
            {
                'id': 'doc-6',
                'title': 'Thông báo hướng dẫn sử dụng thư viện số',
                'description': 'Tài liệu hướng dẫn sử dụng, nội quy và cách tra cứu trên thư viện số của trường.',
                'author': 'Nhà trường THCS Tam Quan',
                'subject': 'Hướng dẫn',
                'grade': 'Tất cả',
                'section': 'library',
                'resource_type': 'Tài liệu',
                'image': 'https://img.freepik.com/free-vector/online-library-concept-illustration_114360-4940.jpg',
                'pdf_url': 'https://www.learningcontainer.com/wp-content/uploads/2019/09/sample-pdf-file.pdf',
                'owner_role': 'school',
                'created_by_id': 'u-school',
                'created_by_name': 'Ban quản trị thư viện số',
                'created_at': datetime(2026, 3, 6, 8, 0, tzinfo=timezone.utc),
                'updated_at': datetime(2026, 3, 6, 8, 0, tzinfo=timezone.utc),
            },
        ],
    )

    op.bulk_insert(
        donations_table,
        [
            {
                'id': 'don-1',
                'full_name': 'Trần Minh Khoa',
                'book_name': 'Bộ sách tham khảo Toán 8',
                'grade': 'Khối 8',
                'condition': 'Còn mới',
                'message': 'Em mong các bạn khóa sau sử dụng tốt.',
                'submitted_by_id': 'u-student',
                'submitted_by_role': 'student',
                'created_at': datetime(2026, 3, 7, 8, 0, tzinfo=timezone.utc),
            },
        ],
    )


def downgrade() -> None:
    op.drop_index('ix_donations_submitted_by_id', table_name='donations')
    op.drop_table('donations')
    op.drop_index('ix_documents_subject', table_name='documents')
    op.drop_index('ix_documents_section', table_name='documents')
    op.drop_index('ix_documents_grade', table_name='documents')
    op.drop_index('ix_documents_created_by_id', table_name='documents')
    op.drop_table('documents')
    op.drop_index('ix_users_student_id', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
