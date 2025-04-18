"""
Learning Portal - User Schemas

This module defines Pydantic models for user data validation.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.sql_models import UserRole

class UserBase(BaseModel):
    """Base user model with shared attributes"""
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)

class UserCreate(UserBase):
    """User creation model with password"""
    password: str = Field(..., min_length=8)
    role: Optional[UserRole] = UserRole.REGULAR

class UserResponse(UserBase):
    """User response model for API outputs"""
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        """Pydantic config for ORM mode"""
        from_attributes = True

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token data model for JWT payload"""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None 