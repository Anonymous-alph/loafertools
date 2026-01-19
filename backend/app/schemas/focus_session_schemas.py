from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


# ============ FOCUS SESSION SCHEMAS ============

class FocusSessionStart(BaseModel):
    """Request to start a new focus session"""
    duration_minutes: int = Field(default=25, ge=1, le=180)
    break_duration_minutes: int = Field(default=5, ge=1, le=60)
    session_type: str = Field(default="focus")  # "focus" | "break" | "long_break"


class FocusSessionResponse(BaseModel):
    """Response for focus session data"""
    id: UUID
    user_id: UUID
    duration_minutes: int
    break_duration_minutes: int
    session_type: str
    started_at: datetime | None
    ended_at: datetime | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ============ DISTRACTION SCHEMAS ============

class DistractionCreate(BaseModel):
    """Request to log a distraction"""
    distraction_type: str  # "tab_switch" | "app_switch" | "idle" | "blocked_site"
    source_app: str | None = None
    destination_app: str | None = None
    url: str | None = None
    duration_seconds: int | None = None


class DistractionResponse(BaseModel):
    """Response for distraction data"""
    id: UUID
    focus_session_id: UUID
    distraction_type: str
    source_app: str | None
    destination_app: str | None
    url: str | None
    duration_seconds: int | None
    occured_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}