from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User
    from .distractions_model import Distraction

class FocusSessionBase(SQLModel):
    duration_minutes: int = Field(default=25)  # Pomodoro default
    break_duration_minutes: int = Field(default=5)
    session_type: str = Field(default="focus")  # "focus" | "break" | "long_break"
    started_at: datetime | None = None
    ended_at: datetime | None = None
    is_completed: bool = Field(default=False)

class FocusSession(BaseUUIDModel, FocusSessionBase, table=True):
    __tablename__ = "focus_sessions"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    user: "User" = Relationship(back_populates="focus_sessions")
    distractions: list["Distraction"] = Relationship(back_populates="focus_session", sa_relationship_kwargs={"cascade": "all, delete"})