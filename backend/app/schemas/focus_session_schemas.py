from pydantic import BaseModel, Field
from datetime import date, datetime
from uuid import UUID
from typing import Optional


# ============ REQUEST SCHEMAS ============

class FocusSessionStart(BaseModel):
    """Request to start a new focus session"""
    duration_minutes: int = Field(default=25, ge=1, le=120)
    session_type: str = Field(default="focus", pattern="^(focus|break)$")


class FocusSessionComplete(BaseModel):
    """Request to complete the active session"""
    actual_duration: Optional[int] = Field(default=None, ge=0, le=120)


class DistractionLog(BaseModel):
    """Log a distraction during active session"""
    name: str = Field(..., min_length=1, max_length=100)
    duration_seconds: Optional[int] = Field(default=None, ge=0)


# ============ RESPONSE SCHEMAS ============

class DistractionResponse(BaseModel):
    """Distraction response"""
    id: UUID
    name: str
    duration_seconds: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class FocusSessionResponse(BaseModel):
    """Focus session response"""
    id: UUID
    duration_minutes: int
    session_type: str
    completed: bool
    start_time: datetime
    end_time: Optional[datetime]
    actual_duration: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class FocusSessionWithDistractions(FocusSessionResponse):
    """Focus session with distraction list"""
    distractions: list[DistractionResponse] = []


# ============ STATS SCHEMAS ============

class FocusSessionStats(BaseModel):
    """Statistics for focus sessions"""
    total_sessions: int
    completed_sessions: int
    total_focus_minutes: int
    total_distractions: int
    average_session_duration: float
    completion_rate: float
    current_streak: int


class DailyStatsResponse(BaseModel):
    """Daily aggregated stats"""
    date: datetime
    total_focus_minutes: int
    total_break_minutes: int
    sessions_completed: int
    distraction_count: int
    productivity_score: float


class WeeklyStatsResponse(BaseModel):
    """Weekly aggregated stats"""
    total_focus_minutes: int
    total_break_minutes: int
    total_sessions: int
    total_distractions: int
    average_productivity: float
    days_studied: int


class StudySessionCreate(BaseModel):
    """Schema for creating a new study session"""
    session_date: date
    total_focus_minutes: int = 0
    total_break_minutes: int = 0
    sessions_completed: int = 0
    distraction_count: int = 0


class StudySessionUpdate(BaseModel):
    """Schema for updating a study session"""
    total_focus_minutes: Optional[int] = None
    total_break_minutes: Optional[int] = None
    sessions_completed: Optional[int] = None
    distraction_count: Optional[int] = None


class StudySessionResponse(BaseModel):
    """Schema for study session response"""
    id: UUID
    session_date: date
    total_focus_minutes: int
    total_break_minutes: int
    sessions_completed: int
    distraction_count: int
    productivity_score: Optional[float]
    
    class Config:
        from_attributes = True


class AddSessionRequest(BaseModel):
    """Schema for adding a completed pomodoro session"""
    focus_minutes: int
    break_minutes: int = 5
    distractions: int = 0
