"""
Learning Portal - SQL Database Models

This module defines SQLAlchemy models for database tables.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.sql import Base

class UserRole(str, enum.Enum):
    """Enum for user roles"""
    REGULAR = "regular"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class User(Base):
    """User model for authentication and user management"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(20))
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.REGULAR, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    questions = relationship("Question", back_populates="user")
    responses = relationship("Response", back_populates="user")
    created_agents = relationship("Agent", back_populates="creator")

class Agent(Base):
    """Agent model for storing chat agent configurations"""
    __tablename__ = "agents"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    system_prompt = Column(Text, nullable=False)
    icon = Column(String(10), default="robot")
    qdrant_collection = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_agents")
    questions = relationship("Question", back_populates="agent")

class Question(Base):
    """Question model for storing user questions"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(String(50), ForeignKey("agents.id"))
    text = Column(Text, nullable=False)
    module = Column(String(50), nullable=False, default="module1")
    unit = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="questions")
    agent = relationship("Agent", back_populates="questions")
    responses = relationship("Response", back_populates="question")

class Response(Base):
    """Response model for storing AI responses to questions"""
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    question = relationship("Question", back_populates="responses")
    user = relationship("User", back_populates="responses")

class Assessment(Base):
    """Assessment model for storing user answer assessments"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_text = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=False)
    guide = Column(Text, nullable=False)
    analysis = Column(Text, nullable=False)
    score = Column(Integer)
    module = Column(String(50), nullable=False, default="module1")
    unit = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 