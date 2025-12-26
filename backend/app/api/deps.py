from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from _collections_abc import AsyncGenerator
from app.db.neondb import AsyncSessionLocal
from app.models import User
from app.core.jwt import decode_access_token



auth_scheme = APIKeyHeader (name = "Authorization")

async def get_db() -> AsyncGenerator [AsyncSession, None]:
    async with AsyncSessionLocal() as session: 
        yield session
        
async def get_current_user(
    token: "str" = Depends(auth_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    
    payload = decode_access_token(token)
    
    if not payload or "sub" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
    user = await db.get(User, payload["sub"])
    if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user





