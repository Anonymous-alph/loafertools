from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import date

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User

class StudySessionBase(SQLModel):
    session_date: date = Field(index=True)
    total_focus_minutes: int = Field(default=0)
    total_break_minutes: int = Field(default=0)
    sessions_completed: int = Field(default=0)
    distraction_count: int = Field(default=0)
    productivity_score: float | None = None  # 0-100 calculated score

class StudySession(BaseUUIDModel, StudySessionBase, table=True):
    __tablename__ = "study_sessions"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    user: "User" = Relationship(back_populates="study_sessions")