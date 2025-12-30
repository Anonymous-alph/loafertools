from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, date
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.models.focus_model import FocusSession
from app.models.distractions_model import Distraction
from app.models.user_model import User
from app.schemas.focus_session_schemas import (
    FocusSessionStart,
    FocusSessionComplete,
    FocusSessionResponse,
    FocusSessionWithDistractions,
    FocusSessionStats,
    DistractionLog,
    DistractionResponse,
)

router = APIRouter()


# ============ HELPER FUNCTIONS ============

async def get_active_session_or_none(
    db: AsyncSession, 
    user_id: UUID
) -> FocusSession | None:
    """Get user's active session if exists"""
    result = await db.execute(
        select(FocusSession).where(
            FocusSession.user_id == user_id,
            FocusSession.completed == False
        )
    )
    return result.scalar_one_or_none()


# ============ CREATE ENDPOINTS (POST) ============

@router.post("/start", response_model=FocusSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_focus_session(
    session_data: FocusSessionStart,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Start a new focus session
    
    **Input:**
    ```json
    {
      "duration_minutes": 25,
      "session_type": "focus"
    }
    ```
    
    **Output:** Session object with ID, timestamps, completed=false
    
    **Error:** Returns 400 if there's already an active session
    """
    # Check for existing active session
    active = await get_active_session_or_none(db, current_user.id)
    
    if active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Active session already exists",
                "active_session_id": str(active.id),
                "started_at": active.start_time.isoformat(),
                "suggestion": "Complete current session first using PATCH /focus-sessions/complete"
            }
        )
    
    # Create new session
    new_session = FocusSession(
        user_id=current_user.id,
        duration_minutes=session_data.duration_minutes,
        session_type=session_data.session_type,
        start_time=datetime.utcnow(),
        completed=False
    )
    
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return new_session


@router.post("/distractions", response_model=DistractionResponse, status_code=status.HTTP_201_CREATED)
async def log_distraction_to_active_session(
    distraction_data: DistractionLog,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Log a distraction to the currently active session
    
    **Input:**
    ```json
    {
      "name": "Phone notification",
      "duration_seconds": 30
    }
    ```
    
    **Output:** Created distraction object
    
    **Note:** Automatically attaches to active session - no ID needed!
    """
    # Get active session
    session = await get_active_session_or_none(db, current_user.id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active session. Start a focus session before logging distractions."
        )
    
    # Create distraction
    distraction = Distraction(
        focus_session_id=session.id,
        name=distraction_data.name,
        duration_seconds=distraction_data.duration_seconds
    )
    
    db.add(distraction)
    await db.commit()
    await db.refresh(distraction)
    
    return distraction


# ============ UPDATE ENDPOINTS (PATCH) ============

@router.patch("/complete", response_model=FocusSessionResponse)
async def complete_active_session(
    completion_data: FocusSessionComplete,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Complete the currently active session (PATCH - partial update)
    
    **Input:**
    ```json
    {
      "actual_duration": 25
    }
    ```
    
    **Output:** Completed session with end_time set
    
    **Why PATCH?** Only updates specific fields (completed, end_time, actual_duration)
    without requiring full object replacement
    """
    # Get active session
    session = await get_active_session_or_none(db, current_user.id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active focus session found. Start a session first."
        )
    
    # PATCH: Update only these fields
    session.completed = True
    session.end_time = datetime.utcnow()
    
    # Calculate actual duration
    if completion_data.actual_duration is not None:
        session.actual_duration = completion_data.actual_duration
    else:
        # Auto-calculate from timestamps
        elapsed_seconds = (session.end_time - session.start_time).total_seconds()
        session.actual_duration = int(elapsed_seconds / 60)
    
    await db.commit()
    await db.refresh(session)
    
    return session


@router.patch("/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_active_session(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancel and delete the currently active session
    
    **Input:** None
    
    **Output:** 204 No Content
    
    **Why PATCH?** Modifies system state (removes active session)
    
    **Use case:** User accidentally started wrong session type
    """
    session = await get_active_session_or_none(db, current_user.id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active session to cancel"
        )
    
    await db.delete(session)
    await db.commit()


# ============ READ ENDPOINTS (GET) ============

@router.get("/active", response_model=FocusSessionWithDistractions)
async def get_active_session(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the currently active session with its distractions
    
    **Output:** Session object + list of distractions
    
    **Use case:** Resume timer after page refresh
    """
    session = await get_active_session_or_none(db, current_user.id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active session"
        )
    
    # Get distractions
    distraction_result = await db.execute(
        select(Distraction).where(Distraction.focus_session_id == session.id)
    )
    distractions = distraction_result.scalars().all()
    
    response = FocusSessionWithDistractions.model_validate(session)
    response.distractions = [DistractionResponse.model_validate(d) for d in distractions]
    
    return response


@router.get("/history", response_model=list[FocusSessionWithDistractions])
async def get_session_history(
    limit: int = 10,
    skip: int = 0,
    completed_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   
    query = select(FocusSession).where(FocusSession.user_id == current_user.id)
    
    if completed_only:
        query = query.where(FocusSession.completed == True)
    
    query = query.order_by(FocusSession.created_at.desc()).limit(limit).offset(skip)
    
    result = await db.execute(query)
    sessions = result.scalars().all()
    
    # Get distractions for each session
    response_sessions = []
    for session in sessions:
        distraction_result = await db.execute(
            select(Distraction).where(Distraction.focus_session_id == session.id)
        )
        distractions = distraction_result.scalars().all()
        
        session_response = FocusSessionWithDistractions.model_validate(session)
        session_response.distractions = [DistractionResponse.model_validate(d) for d in distractions]
        response_sessions.append(session_response)
    
    return response_sessions


@router.get("/today", response_model=list[FocusSessionWithDistractions])
async def get_today_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all sessions from today (for daily summary)
    
    **Output:** List of today's sessions with distractions
    """
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    
    result = await db.execute(
        select(FocusSession).where(
            and_(
                FocusSession.user_id == current_user.id,
                FocusSession.start_time >= today_start,
                FocusSession.start_time <= today_end
            )
        ).order_by(FocusSession.start_time.asc())
    )
    sessions = result.scalars().all()
    
    # Get distractions for each
    response_sessions = []
    for session in sessions:
        distraction_result = await db.execute(
            select(Distraction).where(Distraction.focus_session_id == session.id)
        )
        distractions = distraction_result.scalars().all()
        
        session_response = FocusSessionWithDistractions.model_validate(session)
        session_response.distractions = [DistractionResponse.model_validate(d) for d in distractions]
        response_sessions.append(session_response)
    
    return response_sessions


@router.get("/stats", response_model=FocusSessionStats)
async def get_focus_statistics(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get productivity statistics
    
    **Query Param:**
    - days: Time range (default: 7)
    
    **Output:** Aggregated stats (total sessions, focus time, etc.)
    """
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Get all sessions in range
    result = await db.execute(
        select(FocusSession).where(
            FocusSession.user_id == current_user.id,
            FocusSession.created_at >= since_date
        )
    )
    sessions = result.scalars().all()
    
    if not sessions:
        return FocusSessionStats(
            total_sessions=0,
            completed_sessions=0,
            total_focus_minutes=0,
            total_distractions=0,
            average_session_duration=0.0,
            completion_rate=0.0,
            current_streak=0
        )
    
    total_sessions = len(sessions)
    completed_sessions = sum(1 for s in sessions if s.completed)
    
    # Only count focus sessions (not breaks)
    focus_sessions = [s for s in sessions if s.session_type == "focus" and s.completed]
    total_focus_minutes = sum(
        s.actual_duration if s.actual_duration else s.duration_minutes
        for s in focus_sessions
    )
    
    # Count total distractions
    distraction_result = await db.execute(
        select(func.count(Distraction.id)).where(
            Distraction.focus_session_id.in_([s.id for s in sessions])
        )
    )
    total_distractions = distraction_result.scalar() or 0
    
    # Calculate averages
    if completed_sessions > 0:
        average_duration = total_focus_minutes / completed_sessions
        completion_rate = (completed_sessions / total_sessions * 100)
    else:
        average_duration = 0.0
        completion_rate = 0.0
    
    # Calculate current streak
    current_streak = await calculate_streak(db, current_user.id)
    
    return FocusSessionStats(
        total_sessions=total_sessions,
        completed_sessions=completed_sessions,
        total_focus_minutes=total_focus_minutes,
        total_distractions=total_distractions,
        average_session_duration=round(average_duration, 2),
        completion_rate=round(completion_rate, 2),
        current_streak=current_streak
    )


async def calculate_streak(db: AsyncSession, user_id: UUID) -> int:
    """Helper: Calculate consecutive days with completed sessions"""
    today = date.today()
    streak = 0
    
    for i in range(365):  # Check up to 1 year back
        check_date = today - timedelta(days=i)
        day_start = datetime.combine(check_date, datetime.min.time())
        day_end = datetime.combine(check_date, datetime.max.time())
        
        result = await db.execute(
            select(FocusSession).where(
                and_(
                    FocusSession.user_id == user_id,
                    FocusSession.completed == True,
                    FocusSession.start_time >= day_start,
                    FocusSession.start_time <= day_end
                )
            ).limit(1)
        )
        
        if result.scalar_one_or_none():
            streak += 1
        else:
            break
    
    return streak