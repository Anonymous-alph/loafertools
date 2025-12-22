from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import date

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User

class StreakBase(SQLModel):
    current_streak: int = Field(default=0)
    longest_streak: int = Field(default=0)
    last_activity_date: date | None = None
    total_focus_minutes: int = Field(default=0)
    total_sessions_completed: int = Field(default=0)

class Streak(BaseUUIDModel, StreakBase, table=True):
    __tablename__ = "streaks"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, unique=True, index=True)
    user: "User" = Relationship(back_populates="streak")