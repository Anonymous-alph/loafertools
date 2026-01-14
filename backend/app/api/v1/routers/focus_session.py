from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, date, timezone
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
    DistractionCreate,
    DistractionResponse,   
)

router = APIRouter(prefix="/focus-sessions", tags=["Focus Sessions"])