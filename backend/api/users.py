"""
API router for user-related endpoints (registration, login)
"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from passlib.context import CryptContext

from database.session import get_async_session
from models.user import User, UserCreate, UserPublic
from core.security import create_access_token
from core.config import settings


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash for the given password."""
    return pwd_context.hash(password)


@router.post("/register", response_model=UserPublic)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Register a new user
    """
    # Check if user already exists
    result_email = await session.execute(select(User).where(User.email == user_data.email))
    existing_user_by_email = result_email.scalar_one_or_none()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    result_username = await session.execute(select(User).where(User.username == user_data.username))
    existing_user_by_username = result_username.scalar_one_or_none()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create new user with hashed password
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    # Add user to database
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return UserPublic(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at
    )


@router.post("/login")
async def login_user(email: str, password: str, session: AsyncSession = Depends(get_async_session)):
    """
    Authenticate user and return access token
    """
    # Find user by email
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserPublic(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at
        )
    }