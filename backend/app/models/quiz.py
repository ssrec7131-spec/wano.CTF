"""Round 1 Quiz — questions, options, and per-user attempt records.

SECURITY: The ``correct_option`` column is **never** serialised in any public
schema.  Only the backend validates answers and updates attempt records.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.models.base import Base, TimestampMixin, uuid_pk


class QuizQuestion(Base, TimestampMixin):
    """A single Round-1 quiz question.

    ``correct_option`` is a single character ('A', 'B', 'C', or 'D') and is
    **never** included in any public response schema.
    """

    __tablename__ = "quiz_questions"

    id: Mapped[uuid.UUID] = uuid_pk()
    question_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(Text, nullable=False)
    option_b: Mapped[str] = mapped_column(Text, nullable=False)
    option_c: Mapped[str] = mapped_column(Text, nullable=False)
    option_d: Mapped[str] = mapped_column(Text, nullable=False)
    # NEVER serialised in public schemas
    correct_option: Mapped[str] = mapped_column(String(1), nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(80))
    points: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), default="extreme", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint("correct_option IN ('A','B','C','D')", name="valid_correct_option"),
        CheckConstraint("points >= 0", name="quiz_points_non_negative"),
    )


class QuizAttempt(Base):
    """Records a user's answer to a single question within a quiz session.

    One row per (user, question).  ``is_correct`` is set at submit time.
    """

    __tablename__ = "quiz_attempts"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False
    )
    chosen_option: Mapped[str] = mapped_column(String(1), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    points_awarded: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="uq_quiz_attempts_user_question"),
        Index("ix_quiz_attempts_user", "user_id"),
        CheckConstraint("chosen_option IN ('A','B','C','D')", name="valid_chosen_option"),
    )


class QuizResult(Base):
    """Aggregated pass/fail result for a user's Round-1 attempt.

    One row per user — created/updated when the user submits all answers.
    ``passed`` is true when score >= pass_threshold (set at record time).
    """

    __tablename__ = "quiz_results"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    pass_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
