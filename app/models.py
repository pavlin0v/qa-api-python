import uuid
from datetime import datetime

from sqlalchemy import Text, Integer, DateTime, UUID, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
    )

class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    question = relationship(
        "Question",
        back_populates="answers",
    )