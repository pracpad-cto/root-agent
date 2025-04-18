"""
Learning Portal - Superadmin Creation Script

This script creates a superadmin user in the database.
Run this script to initialize the first superadmin user.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

import sys
import os
from sqlalchemy.orm import Session

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import logger
from app.db.sql import init_db, get_db
from app.models.sql_models import User, UserRole
from app.utils.password import hash_password

def create_superadmin(
    email: str = "admin@example.com", 
    password: str = "SuperAdmin@123", 
    first_name: str = "Super", 
    last_name: str = "Admin"
):
    """
    Create a superadmin user if it doesn't exist.
    
    Args:
        email: Superadmin email
        password: Superadmin password
        first_name: Superadmin first name
        last_name: Superadmin last name
    """
    # Initialize database
    init_db()
    
    # Get database session
    db = next(get_db())
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        logger.info(f"User with email {email} already exists.")
        return
    
    # Create superadmin user
    hashed_password = hash_password(password)
    superadmin = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=UserRole.SUPERADMIN,
        hashed_password=hashed_password
    )
    
    # Add to database
    db.add(superadmin)
    db.commit()
    db.refresh(superadmin)
    
    logger.info(f"Superadmin user created with email: {email}")

if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create a superadmin user")
    parser.add_argument("--email", type=str, default="admin@example.com", help="Superadmin email")
    parser.add_argument("--password", type=str, default="SuperAdmin@123", help="Superadmin password")
    parser.add_argument("--first-name", type=str, default="Super", help="Superadmin first name")
    parser.add_argument("--last-name", type=str, default="Admin", help="Superadmin last name")
    
    args = parser.parse_args()
    
    # Create superadmin
    create_superadmin(
        email=args.email,
        password=args.password,
        first_name=args.first_name,
        last_name=args.last_name
    ) 