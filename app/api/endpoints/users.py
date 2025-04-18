"""
Learning Portal - User API Endpoints

This module contains FastAPI endpoints for user management.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.sql import get_db
from app.models.sql_models import User, UserRole
from app.models.user_schema import UserCreate, UserResponse
from app.utils.password import hash_password
from app.utils.auth import get_current_active_user, get_admin_user, get_superadmin_user
from app.core.config import logger

router = APIRouter(tags=["users"])

@router.get("/users", response_model=List[UserResponse])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Get all users with pagination.
    Admin access only.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new user.
    
    Regular users can only create regular users.
    Admin users can create regular and admin users.
    Superadmin users can create any type of user.
    """
    # Check if user with this email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Role-based permission checks
    if user.role == UserRole.SUPERADMIN and current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmins can create superadmin users"
        )
    
    if user.role == UserRole.ADMIN and current_user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins or superadmins can create admin users"
        )
    
    # Create new user with properly hashed password
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        role=user.role
    )
    
    # Add and commit to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User created: {user.email} with role {user.role}")
    return db_user

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific user by ID.
    
    Users can view their own profile.
    Admins and superadmins can view any profile.
    """
    # Check if user is requesting their own profile or has admin access
    if user_id != current_user.id and current_user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user profile"
        )
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user 