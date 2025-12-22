from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .focus_model import FocusSession
    from .task_model import Task
    from .streak_model import Streak
    from .session_model import StudySession
    from .reflection_model import Reflection
    from .feedback_model import Feedback
    from .resource_model import Resource

class UserBase(SQLModel):
    username: str
    email: EmailStr = Field()

class User(BaseUUIDModel, UserBase, table=True):
    __tablename__ = "users"

    hashed_password: str | None = Field(default=None, nullable=False, index=True)
    
    # Relationships
    focus_sessions: list["FocusSession"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
    tasks: list["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
    streak: "Streak" = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete", "uselist": False})
    study_sessions: list["StudySession"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
    reflections: list["Reflection"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
    feedbacks: list["Feedback"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
    resources: list["Resource"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})

