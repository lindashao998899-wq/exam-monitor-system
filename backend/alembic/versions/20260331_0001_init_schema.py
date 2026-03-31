"""init schema

Revision ID: 20260331_0001
Revises:
Create Date: 2026-03-31 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260331_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_no", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("class_name", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_students_student_no", "students", ["student_no"], unique=True)

    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("device_code", sa.String(length=80), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
    )
    op.create_index("ix_devices_device_code", "devices", ["device_code"], unique=True)

    op.create_table(
        "exams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("question_no", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("correct_answer", sa.String(length=200), nullable=False),
        sa.Column("knowledge_point", sa.String(length=120), nullable=True),
        sa.Column("score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"]),
    )
    op.create_index("ix_questions_exam_id", "questions", ["exam_id"], unique=False)

    op.create_table(
        "exam_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=True),
        sa.Column("current_question_no", sa.Integer(), nullable=False),
        sa.Column("is_online", sa.Boolean(), nullable=False),
        sa.Column("abnormal_flag", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
    )
    op.create_index("ix_exam_sessions_exam_id", "exam_sessions", ["exam_id"], unique=False)
    op.create_index("ix_exam_sessions_student_id", "exam_sessions", ["student_id"], unique=False)

    op.create_table(
        "answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["exam_sessions.id"]),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
    )
    op.create_index("ix_answers_session_id", "answers", ["session_id"], unique=False)
    op.create_index("ix_answers_question_id", "answers", ["question_id"], unique=False)

    op.create_table(
        "answer_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=True),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["exam_sessions.id"]),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
    )
    op.create_index("ix_answer_events_session_id", "answer_events", ["session_id"], unique=False)

    op.create_table(
        "proctor_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("level", sa.String(length=20), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["exam_sessions.id"]),
    )
    op.create_index("ix_proctor_events_session_id", "proctor_events", ["session_id"], unique=False)

    op.create_table(
        "question_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.Column("elapsed_seconds", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["exam_sessions.id"]),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
    )
    op.create_index("ix_question_snapshots_session_id", "question_snapshots", ["session_id"], unique=False)

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("report_type", sa.String(length=20), nullable=False),
        sa.Column("file_url", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"]),
    )
    op.create_index("ix_reports_exam_id", "reports", ["exam_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_reports_exam_id", table_name="reports")
    op.drop_table("reports")
    op.drop_index("ix_question_snapshots_session_id", table_name="question_snapshots")
    op.drop_table("question_snapshots")
    op.drop_index("ix_proctor_events_session_id", table_name="proctor_events")
    op.drop_table("proctor_events")
    op.drop_index("ix_answer_events_session_id", table_name="answer_events")
    op.drop_table("answer_events")
    op.drop_index("ix_answers_question_id", table_name="answers")
    op.drop_index("ix_answers_session_id", table_name="answers")
    op.drop_table("answers")
    op.drop_index("ix_exam_sessions_student_id", table_name="exam_sessions")
    op.drop_index("ix_exam_sessions_exam_id", table_name="exam_sessions")
    op.drop_table("exam_sessions")
    op.drop_index("ix_questions_exam_id", table_name="questions")
    op.drop_table("questions")
    op.drop_table("exams")
    op.drop_index("ix_devices_device_code", table_name="devices")
    op.drop_table("devices")
    op.drop_index("ix_students_student_no", table_name="students")
    op.drop_table("students")
