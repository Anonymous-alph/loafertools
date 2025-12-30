from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .focus_model import FocusSession

class DistractionBase(SQLModel):
    name: str = Field(max_length=100)
    duration_seconds: int | None = None

class Distraction(BaseUUIDModel, DistractionBase, table=True):
    __tablename__ = "distractions"

    focus_session_id: UUID = Field(foreign_key="focus_sessions.id", nullable=False, index=True)
    focus_session: "FocusSession" = Relationship(back_populates="distractions")