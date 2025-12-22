from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User
    from .subtask_model import Subtask

class TaskBase(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5)  # 1-5 scale
    due_date: datetime | None = None
    is_completed: bool = Field(default=False)
    estimated_pomodoros: int | None = None
    completed_pomodoros: int = Field(default=0)

class Task(BaseUUIDModel, TaskBase, table=True):
    __tablename__ = "tasks"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    user: "User" = Relationship(back_populates="tasks")
    subtasks: list["Subtask"] = Relationship(back_populates="task", sa_relationship_kwargs={"cascade": "all, delete"})