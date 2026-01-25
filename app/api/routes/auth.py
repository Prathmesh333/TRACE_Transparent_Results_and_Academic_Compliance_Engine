"""
Opti-Scholar: Authentication Routes
Login, registration, and token management
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.core.config import settings
from app.models import User
from app.api.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if email exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
        phone=user_data.phone,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token."""
    # Find user
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        },
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current authenticated user."""
    # TODO: Implement dependency for current user from token
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint under development"
    )


@router.post("/demo-login")
async def demo_login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Demo login - accepts any password for demo accounts (hackathon mode)."""
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    # For demo, accept password "demo123" for all demo accounts
    if login_data.password != "demo123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password (hint: use 'demo123' for demo accounts)",
        )
    
    # Get additional profile info based on role
    profile_data = {}
    
    if user.role == "student":
        from app.models.models import Student
        student_result = await db.execute(
            select(Student).where(Student.user_id == user.id)
        )
        student = student_result.scalar_one_or_none()
        if student:
            profile_data = {
                "registration_number": student.registration_number,
                "school_id": student.school_id,
                "department": student.department,
                "program": student.program,
                "semester": student.current_semester
            }
    
    elif user.role == "teacher":
        from app.models.models import Teacher
        teacher_result = await db.execute(
            select(Teacher).where(Teacher.user_id == user.id)
        )
        teacher = teacher_result.scalar_one_or_none()
        if teacher:
            profile_data = {
                "employee_id": teacher.employee_id,
                "school_id": teacher.school_id,
                "department": teacher.department,
                "designation": teacher.designation
            }
    
    return {
        "success": True,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            **profile_data
        },
        "message": f"Welcome, {user.full_name}!"
    }

