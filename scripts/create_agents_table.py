"""
Learning Portal - Agent System Migration Script

This script creates the agents table and updates the questions table
to support the new dynamic agent system.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS

Usage:
    python scripts/create_agents_table.py
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.sql import engine, SessionLocal
from app.core.config import logger

def create_agents_table():
    """Create the agents table if it doesn't exist"""
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS agents (
        id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        system_prompt TEXT NOT NULL,
        icon VARCHAR(10) DEFAULT 'robot',
        qdrant_collection VARCHAR(100),
        is_active BOOLEAN DEFAULT TRUE,
        created_by INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
        INDEX idx_agents_active (is_active),
        INDEX idx_agents_created_by (created_by)
    );
    """
    
    try:
        with engine.connect() as connection:
            connection.execute(text(create_table_sql))
            connection.commit()
            logger.info("✅ Agents table created successfully")
            return True
    except Exception as e:
        logger.error(f"❌ Error creating agents table: {str(e)}")
        return False

def add_agent_id_to_questions():
    """Add agent_id column to questions table"""
    
    # Check if column already exists
    check_column_sql = """
    SELECT COUNT(*) as count
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'questions' 
    AND COLUMN_NAME = 'agent_id';
    """
    
    add_column_sql = """
    ALTER TABLE questions 
    ADD COLUMN agent_id VARCHAR(50),
    ADD INDEX idx_questions_agent_id (agent_id),
    ADD FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE SET NULL;
    """
    
    try:
        with engine.connect() as connection:
            # Check if column exists
            result = connection.execute(text(check_column_sql))
            count = result.fetchone()[0]
            
            if count == 0:
                # Column doesn't exist, add it
                connection.execute(text(add_column_sql))
                connection.commit()
                logger.info("✅ agent_id column added to questions table successfully")
            else:
                logger.info("ℹ️  agent_id column already exists in questions table")
            return True
    except Exception as e:
        logger.error(f"❌ Error adding agent_id column to questions table: {str(e)}")
        return False

def verify_migration():
    """Verify that the migration was successful"""
    
    verify_agents_sql = """
    SELECT COUNT(*) as count
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'agents';
    """
    
    verify_agent_id_sql = """
    SELECT COUNT(*) as count
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'questions' 
    AND COLUMN_NAME = 'agent_id';
    """
    
    try:
        with engine.connect() as connection:
            # Verify agents table
            result = connection.execute(text(verify_agents_sql))
            agents_table_exists = result.fetchone()[0] > 0
            
            # Verify agent_id column
            result = connection.execute(text(verify_agent_id_sql))
            agent_id_column_exists = result.fetchone()[0] > 0
            
            if agents_table_exists and agent_id_column_exists:
                logger.info("✅ Migration verification successful")
                return True
            else:
                logger.error("❌ Migration verification failed")
                return False
    except Exception as e:
        logger.error(f"❌ Error verifying migration: {str(e)}")
        return False

def main():
    """Main migration function"""
    
    logger.info("🚀 Starting agent system database migration...")
    
    if not engine:
        logger.error("❌ Database engine not available. Please check your database configuration.")
        return False
    
    # Step 1: Create agents table
    logger.info("📋 Step 1: Creating agents table...")
    if not create_agents_table():
        return False
    
    # Step 2: Add agent_id to questions table
    logger.info("📋 Step 2: Adding agent_id column to questions table...")
    if not add_agent_id_to_questions():
        return False
    
    # Step 3: Verify migration
    logger.info("📋 Step 3: Verifying migration...")
    if not verify_migration():
        return False
    
    logger.info("🎉 Agent system database migration completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 