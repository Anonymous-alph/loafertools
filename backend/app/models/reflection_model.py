from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User

class ReflectionBase(SQLModel):
    mood: int = Field(ge=1, le=5)  # 1-5 scale
    energy_level: int = Field(ge=1, le=5)
    accomplishments: str | None = None
    challenges: str | None = None
    

class Reflection(BaseUUIDModel, ReflectionBase, table=True):
    __tablename__ = "reflections"

    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    user: "User" = Relationship(back_populates="reflections")