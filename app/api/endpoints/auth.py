"""
Learning Portal - Authentication API Endpoints

This module contains the FastAPI endpoints for authentication and user management.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.sql import get_db
from app.models.sql_models import User, UserRole
from app.models.user_schema import Token, UserResponse, UserCreate
from app.utils.auth import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user,
    get_admin_user,
    get_superadmin_user
)
from app.core.config import settings, logger
from app.utils.password import hash_password

router = APIRouter(tags=["authentication"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT token.
    
    Args:
        form_data: OAuth2 password request form
        db: Database session
        
    Returns:
        JWT token
        
    Raises:
        HTTPException: If authentication fails
    """
    # Authenticate user
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role
        }, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    This endpoint is public and does not require authentication.
    New users are created with regular user role by default.
    
    Args:
        user: User creation model
        db: Database session
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If email already exists
    """
    # Check if user with this email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Force role to be regular for self-registration
    user_role = UserRole.REGULAR
    
    # Create new user with properly hashed password
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        role=user_role
    )
    
    # Add and commit to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User registered: {user.email}")
    return db_user

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return current_user

@router.get("/admin", response_model=UserResponse)
async def admin_only(current_user: User = Depends(get_admin_user)):
    """
    Admin only endpoint.
    
    Args:
        current_user: Current authenticated admin user
        
    Returns:
        Admin user information
    """
    return current_user

@router.get("/superadmin", response_model=UserResponse)
async def superadmin_only(current_user: User = Depends(get_superadmin_user)):
    """
    Superadmin only endpoint.
    
    Args:
        current_user: Current authenticated superadmin user
        
    Returns:
        Superadmin user information
    """
    return current_user 