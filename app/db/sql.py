"""
Learning Portal - SQL Database Module

This module provides SQLAlchemy database connection and session management.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings, logger
import pymysql

# Register PyMySQL as the MySQL driver
pymysql.install_as_MySQLdb()

# Create SQLAlchemy engine and session
try:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    # Create a dummy engine if database connection fails
    # This allows the application to start even if the database is not available
    engine = None
    SessionLocal = None

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Dependency function to get a database session.
    Used in FastAPI endpoints that require database access.
    """
    if SessionLocal is None:
        logger.warning("Database session not available. Database operations will fail.")
        return None
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database by creating all tables.
    Call this function during application startup.
    """
    if engine is None:
        logger.warning("Database engine not available. Skipping table creation.")
        return
        
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise 