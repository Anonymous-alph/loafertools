from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.user_model import User
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.schemas.auth_schemas import UserLoginRequest, UserRegisterRequest, TokenResponse, UserResponse

router = APIRouter()



@router.post("/register", response_model=UserResponse, tags=["auth"])
async def register(
    user_data: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    # 1. Check if user already exists
    existing_user = await db.execute(
        select(User).where(
            (User.email == user_data.email) | (User.username == user_data.username)
        )
    )
    existing = existing_user.scalar_one_or_none()
    
    if existing:
        if existing.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # 2. Hash the password
    hashed_pwd = hash_password(user_data.password)
    
    # 3. Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pwd
    )
    
    # 4. Save to database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # 5. Return success response
    return UserResponse(
        id=str(new_user.id),
        username=new_user.username,
        email=new_user.email,
        message="User registered successfully"
    )


@router.post("/login", response_model=TokenResponse, tags=["auth"])
async def login(
    user_data: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    # 1. Find user by username
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    user = result.scalar_one_or_none()
    
    # 2. Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # 3. Verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # 4. Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 5. Return token
    return TokenResponse(access_token=access_token)


@router.get("/me", tags=["auth"])
async def get_me(
    token: str = Depends(get_db),  # This should use get_current_user
):
    """Get current user info - implement after auth is working"""
    pass


