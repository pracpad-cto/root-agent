"""
Learning Portal - Default Agents Creation Script

This script creates default agents based on existing Qdrant collections
and sets up initial agent configurations for the dynamic agent system.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS

Usage:
    python scripts/create_default_agents.py
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.sql import SessionLocal, engine
from app.db.qdrant import get_collections
from app.models.sql_models import Agent, User, UserRole
from app.core.config import logger

# Default system prompt template
DEFAULT_SYSTEM_PROMPT = """You are an AI assistant specializing in {module_name}. 

Your role is to:
- Provide accurate, helpful information based on the knowledge base
- Answer questions clearly and concisely
- Ask for clarification when questions are ambiguous
- Admit when you don't know something rather than guessing
- Maintain a professional, friendly tone

When responding:
- Use the retrieved context to provide accurate answers
- Cite specific information when possible
- If the context doesn't contain relevant information, say so clearly
- Focus on being helpful while staying within your knowledge domain

Knowledge Domain: {module_name}
Context: Use the provided knowledge base to answer questions related to {module_name}."""

def get_system_admin_user(db: Session) -> User:
    """Get or create a system admin user for creating default agents"""
    
    # Try to find an existing superadmin
    admin_user = db.query(User).filter(User.role == UserRole.SUPERADMIN).first()
    
    if admin_user:
        logger.info(f"Using existing admin user: {admin_user.email}")
        return admin_user
    
    # Try to find an admin user
    admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
    
    if admin_user:
        logger.info(f"Using existing admin user: {admin_user.email}")
        return admin_user
    
    # If no admin users exist, use the first user and upgrade them temporarily
    first_user = db.query(User).first()
    if first_user:
        logger.warning(f"No admin users found. Using first user {first_user.email} for agent creation")
        return first_user
    
    logger.error("No users found in the database. Cannot create default agents.")
    return None

def create_agent_from_collection(db: Session, collection_info: dict, admin_user: User) -> bool:
    """Create an agent from Qdrant collection information"""
    
    module_name = collection_info.get("name", "Unknown Module")
    collection_id = collection_info.get("id", "unknown")
    
    # Create agent ID from collection ID
    agent_id = f"agent_{collection_id}".lower().replace(" ", "_").replace("-", "_")
    
    # Check if agent already exists
    existing_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if existing_agent:
        logger.info(f"Agent {agent_id} already exists, skipping...")
        return True
    
    # Create system prompt specific to this module
    system_prompt = DEFAULT_SYSTEM_PROMPT.format(module_name=module_name)
    
    # Determine appropriate icon based on module name
    icon = get_module_icon(module_name)
    
    # Create the agent
    agent = Agent(
        id=agent_id,
        name=f"{module_name} Assistant",
        description=f"AI assistant specialized in {module_name} knowledge and Q&A",
        system_prompt=system_prompt,
        icon=icon,
        qdrant_collection=collection_id,
        is_active=True,
        created_by=admin_user.id
    )
    
    try:
        db.add(agent)
        db.commit()
        logger.info(f"✅ Created agent: {agent_id} ({module_name})")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating agent {agent_id}: {str(e)}")
        db.rollback()
        return False

def get_module_icon(module_name: str) -> str:
    """Get an appropriate icon for the module based on its name"""
    
    module_name_lower = module_name.lower()
    
    # Icon mapping based on common module types - using text instead of emojis
    icon_mapping = {
        'math': 'math',
        'science': 'science',
        'physics': 'physics',
        'chemistry': 'chemistry',
        'biology': 'biology',
        'computer': 'computer',
        'programming': 'code',
        'history': 'history',
        'geography': 'geography',
        'language': 'language',
        'english': 'english',
        'literature': 'book',
        'art': 'art',
        'music': 'music',
        'business': 'business',
        'finance': 'finance',
        'marketing': 'marketing',
        'legal': 'legal',
        'medical': 'medical',
        'engineering': 'engineer',
        'ai': 'ai',
        'machine learning': 'ml',
        'data': 'data',
        'security': 'security',
        'network': 'network',
        'database': 'database',
    }
    
    # Check for keyword matches
    for keyword, icon in icon_mapping.items():
        if keyword in module_name_lower:
            return icon
    
    # Default icon
    return 'robot'

def create_general_assistant_agent(db: Session, admin_user: User) -> bool:
    """Create a general-purpose AI assistant agent"""
    
    agent_id = "general_assistant"
    
    # Check if agent already exists
    existing_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if existing_agent:
        logger.info(f"General assistant agent already exists, skipping...")
        return True
    
    general_system_prompt = """You are a helpful AI assistant with access to a comprehensive knowledge base.

Your role is to:
- Provide accurate, helpful information across various topics
- Answer questions clearly and concisely
- Ask for clarification when questions are ambiguous
- Admit when you don't know something rather than guessing
- Maintain a professional, friendly, and approachable tone

When responding:
- Use the retrieved context to provide accurate answers
- Be conversational while remaining informative
- If the context doesn't contain relevant information, provide general knowledge while noting the limitation
- Encourage follow-up questions for clarification

You have access to diverse knowledge domains and can help with a wide range of topics."""
    
    agent = Agent(
        id=agent_id,
        name="General AI Assistant",
        description="A versatile AI assistant capable of helping with a wide range of topics and questions",
        system_prompt=general_system_prompt,
        icon="robot",
        qdrant_collection=None,  # Uses default collection
        is_active=True,
        created_by=admin_user.id
    )
    
    try:
        db.add(agent)
        db.commit()
        logger.info(f"✅ Created general assistant agent")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating general assistant agent: {str(e)}")
        db.rollback()
        return False

def main():
    """Main function to create default agents"""
    
    logger.info("🚀 Starting default agents creation...")
    
    if not engine:
        logger.error("❌ Database engine not available. Please check your database configuration.")
        return False
    
    db = SessionLocal()
    try:
        # Get admin user for creating agents
        admin_user = get_system_admin_user(db)
        if not admin_user:
            return False
        
        # Create general assistant agent
        logger.info("📋 Creating general assistant agent...")
        if not create_general_assistant_agent(db, admin_user):
            return False
        
        # Get Qdrant collections and create agents
        logger.info("📋 Fetching Qdrant collections...")
        try:
            collections = get_collections()
            logger.info(f"Found {len(collections)} collections in Qdrant")
            
            # Create agents from collections
            success_count = 0
            for collection in collections:
                if create_agent_from_collection(db, collection, admin_user):
                    success_count += 1
            
            logger.info(f"✅ Successfully created {success_count} agents from Qdrant collections")
            
        except Exception as e:
            logger.warning(f"Could not fetch Qdrant collections: {str(e)}")
            logger.info("Continuing with general assistant agent only...")
        
        logger.info("🎉 Default agents creation completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during default agents creation: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 