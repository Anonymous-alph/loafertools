from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime

from .base_model import BaseUUIDModel

if TYPE_CHECKING:
    from .focus_model import FocusSession

class DistractionBase(SQLModel):
    distraction_type: str  # "tab_switch" | "app_switch" | "idle" | "blocked_site"
    source_app: str | None = None  # e.g., "Chrome", "Discord"
    destination_app: str | None = None
    url: str | None = None
    duration_seconds: int | None = None
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

class Distraction(BaseUUIDModel, DistractionBase, table=True):
    __tablename__ = "distractions"

    focus_session_id: UUID = Field(foreign_key="focus_sessions.id", nullable=False, index=True)
    focus_session: "FocusSession" = Relationship(back_populates="distractions")