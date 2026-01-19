from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.models.focus_model import FocusSession
from app.models.distractions_model import Distraction
from app.models.user_model import User
from app.schemas.focus_session_schemas import (
    FocusSessionStart,
    FocusSessionResponse,
    DistractionCreate,
    DistractionResponse,
)

router = APIRouter(prefix="/focus-sessions", tags=["Focus Sessions"])


# ============ HELPER ============

async def get_active_session(db: AsyncSession, user_id: UUID) -> FocusSession | None:
    result = await db.execute(
        select(FocusSession).where(
            FocusSession.user_id == user_id,
            FocusSession.is_completed == False
        )
    )
    return result.scalar_one_or_none()


# ============ SESSION ENDPOINTS ============

@router.post("/start", response_model=FocusSessionResponse, status_code=201)
async def start_session(
    data: FocusSessionStart,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if await get_active_session(db, user.id):
        raise HTTPException(400, "Session already active")

    session = FocusSession(
        user_id=user.id,
        started_at=datetime.now(timezone.utc),
        **data.model_dump()
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


@router.patch("/complete", response_model=FocusSessionResponse)
async def complete_session(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    session = await get_active_session(db, user.id)
    if not session:
        raise HTTPException(404, "No active session")

    session.is_completed = True
    session.ended_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(session)
    return session

@router.delete("/cancel", status_code=204)
async def cancel_session(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    session = await get_active_session(db, user.id)
    if not session:
        raise HTTPException(404, "No Active Session")
    
    await db.delete(session)
    await db.commit()
    
    
@router.get("/active", response_model=FocusSessionResponse)
async def get_current_session(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    session = await get_active_session(db, user.id)
    if not session:
        raise HTTPException(404, "No active Session")
    return session

@router.get("/history", response_model=list[FocusSessionResponse])
async def get_history(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(FocusSession)
        .where(FocusSession.user_id == user.id, FocusSession.is_completed == True )
        .order_by(FocusSession.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()

#Distractions Tracking/logging Endpoints

@router.post("/distractions", response_model=DistractionResponse, status_code=status.HTTP_201_CREATED)
async def log_distraction(
    data: DistractionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    session = await get_active_session(db, user.id)
    if not session:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No active session")
    
    distraction = Distraction(
        focus_session_id = session.id,
        occured_at = datetime.now(timezone.utc),
        **data.model_dump()
    )
    db.add(distraction)
    await db.commit()
    await db.refresh(distraction)
    return distraction

@router.get("/distractions", response_model = list[DistractionResponse])
async def get_distractions(
    session_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if session_id:
        result = await db.execute(
            select(FocusSession).where(
                FocusSession.id == session_id,
                FocusSession.user_id == user.id
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
        query = select(Distraction).where(Distraction.focus_session_id == session_id)
    else:
        session = await get_active_session(db, user.id)
        if not session:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No active session")
        query = select(Distraction).where(Distraction.focus_session_id == session.id)
        
    result = await db.execute(query.order_by(Distraction.occured_at))
    return result.scalars().all()



