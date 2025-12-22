from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .task_model import Task

class SubtaskBase(SQLModel):
    title: str = Field(max_length=255)
    is_completed: bool = Field(default=False)
    order: int = Field(default=0)

class Subtask(BaseUUIDModel, SubtaskBase, table=True):
    __tablename__ = "subtasks"

    task_id: UUID = Field(foreign_key="tasks.id", nullable=False, index=True)
    task: "Task" = Relationship(back_populates="subtasks")