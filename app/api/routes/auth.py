"""
Opti-Scholar: Authentication Routes
Login, registration, and token management
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.core.config import settings
from app.api.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
)
from app.core.csv_db import csv_db

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    # Check if email exists
    existing = await csv_db.get_user_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # For Hackathon CSV version: we won't implement full user creation as it requires writing to users.csv
    # and maintaining IDs. We'll default to error or dummy success.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration disabled for CSV mode. Please use demo accounts."
    )


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Authenticate user and return access token."""
    user = await csv_db.get_user_by_email(login_data.email)
    
    # In CSV we stored plain text or just assume success if password matches demo123 for simplicity in hackathon
    # or proper check if we stored hash. 
    # For now, simplistic check:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if login_data.password != user["password"] and login_data.password != "demo123":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": str(user["id"]),
            "email": user["email"],
            "role": user["role"]
        },
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            is_active=True,
            created_at="2024-01-01T00:00:00" # Dummy
        )
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
async def demo_login(login_data: LoginRequest):
    """Demo login - accepts any password for demo accounts (hackathon mode)."""
    # Find user by email
    user = await csv_db.get_user_by_email(login_data.email)
    
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
    
    if user["role"] == "student":
        # Mock profile data for CSV mode
         profile_data = {
            "registration_number": "2023101103",
            "school_id": "1",
            "department": "SCIS",
            "program": "M.Tech",
            "semester": 1
        }
    
    elif user["role"] == "teacher":
         profile_data = {
            "employee_id": "T101",
            "school_id": "1",
            "department": "SCIS",
            "designation": "Professor"
        }
    
    return {
        "success": True,
        "user": {
            "id": str(user["id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "is_active": True,
            **profile_data
        },
        "message": f"Welcome, {user['full_name']}!"
    }

