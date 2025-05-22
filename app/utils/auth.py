"""
Learning Portal - Authentication Utilities

This module provides utilities for JWT token creation, verification,
and role-based access control.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: PracPad
"""

from datetime import datetime, timedelta
from typing import Optional, Union, List
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.sql import get_db
from app.core.config import settings
from app.models.sql_models import User, UserRole
from app.models.user_schema import TokenData
from app.utils.password import verify_password

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
        
    Returns:
        User object if authentication succeeds, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Create JWT token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token.
    
    Args:
        token: JWT token
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(
            email=email,
            user_id=payload.get("user_id"),
            role=payload.get("role")
        )
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Check if current user is active.
    
    Args:
        current_user: Current user from token
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

def role_required(allowed_roles: List[UserRole]):
    """
    Dependency factory for role-based access control.
    
    Args:
        allowed_roles: List of roles allowed to access the endpoint
        
    Returns:
        Dependency function to check if user has required role
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return role_checker

# Role-based dependencies for convenience
get_admin_user = role_required([UserRole.ADMIN, UserRole.SUPERADMIN])
get_superadmin_user = role_required([UserRole.SUPERADMIN]) 