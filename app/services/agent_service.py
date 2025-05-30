"""
Learning Portal - Agent Service

This module provides business logic for agent management operations.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from fastapi import HTTPException, status
import re
from datetime import datetime

from app.models.sql_models import Agent, User, UserRole, Question
from app.models.agent_schema import (
    AgentCreate, AgentUpdate, AdminAgentResponse, 
    PublicChatbotInfo, AgentUsageStats
)
from app.core.config import logger

class AgentService:
    """Service class for agent management operations"""
    
    @staticmethod
    def get_public_agents(db: Session) -> List[PublicChatbotInfo]:
        """
        Get active agents with public information only (for regular users).
        
        Args:
            db: Database session
            
        Returns:
            List of public chatbot info
        """
        try:
            agents = db.query(Agent).filter(Agent.is_active == True).all()
            
            public_agents = []
            for agent in agents:
                public_agent = PublicChatbotInfo(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    icon=agent.icon
                )
                public_agents.append(public_agent)
            
            logger.info(f"Retrieved {len(public_agents)} active agents for public access")
            return public_agents
            
        except Exception as e:
            logger.error(f"Error retrieving public agents: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve agents"
            )
    
    @staticmethod
    def get_admin_agents(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        include_stats: bool = True
    ) -> List[AdminAgentResponse]:
        """
        Get all agents with complete information (for admin users).
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_stats: Whether to include usage statistics
            
        Returns:
            List of admin agent responses
        """
        try:
            # Query agents with creator information
            query = db.query(Agent).options(joinedload(Agent.creator))
            agents = query.offset(skip).limit(limit).all()
            
            admin_agents = []
            for agent in agents:
                # Get usage stats if requested
                usage_stats = None
                if include_stats:
                    usage_stats = AgentService._get_agent_usage_stats(db, agent.id)
                
                admin_agent = AdminAgentResponse(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    system_prompt=agent.system_prompt,
                    icon=agent.icon,
                    qdrant_collection=agent.qdrant_collection,
                    is_active=agent.is_active,
                    created_by=agent.created_by,
                    creator_name=f"{agent.creator.first_name} {agent.creator.last_name}" if agent.creator else None,
                    created_at=agent.created_at,
                    updated_at=agent.updated_at,
                    usage_stats=usage_stats.dict() if usage_stats else None
                )
                admin_agents.append(admin_agent)
            
            logger.info(f"Retrieved {len(admin_agents)} agents for admin access")
            return admin_agents
            
        except Exception as e:
            logger.error(f"Error retrieving admin agents: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve agents"
            )
    
    @staticmethod
    def get_agent_by_id(db: Session, agent_id: str, user_role: UserRole = UserRole.REGULAR) -> Agent:
        """
        Get a specific agent by ID with appropriate access control.
        
        Args:
            db: Database session
            agent_id: Agent identifier
            user_role: Role of the requesting user
            
        Returns:
            Agent object
            
        Raises:
            HTTPException: If agent not found or access denied
        """
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Agent not found"
                )
            
            # Regular users can only access active agents
            if user_role not in [UserRole.ADMIN, UserRole.SUPERADMIN] and not agent.is_active:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Agent not found"
                )
            
            return agent
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving agent {agent_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve agent"
            )
    
    @staticmethod
    def create_agent(db: Session, agent_data: AgentCreate, creator_id: int) -> Agent:
        """
        Create a new agent.
        
        Args:
            db: Database session
            agent_data: Agent creation data
            creator_id: ID of the user creating the agent
            
        Returns:
            Created agent object
            
        Raises:
            HTTPException: If agent creation fails
        """
        try:
            # Validate agent ID format
            if not re.match(r'^[a-zA-Z0-9_-]+$', agent_data.id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Agent ID must contain only alphanumeric characters, underscores, and dashes"
                )
            
            # Check if agent with this ID already exists
            existing_agent = db.query(Agent).filter(Agent.id == agent_data.id).first()
            if existing_agent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Agent with this ID already exists"
                )
            
            # Create new agent
            agent = Agent(
                id=agent_data.id,
                name=agent_data.name,
                description=agent_data.description,
                system_prompt=agent_data.system_prompt,
                icon=agent_data.icon,
                qdrant_collection=agent_data.qdrant_collection,
                is_active=agent_data.is_active,
                created_by=creator_id
            )
            
            db.add(agent)
            db.commit()
            db.refresh(agent)
            
            logger.info(f"Agent created successfully: {agent.id} by user {creator_id}")
            return agent
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating agent: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create agent"
            )
    
    @staticmethod
    def update_agent(db: Session, agent_id: str, updates: AgentUpdate) -> Agent:
        """
        Update an existing agent.
        
        Args:
            db: Database session
            agent_id: Agent identifier
            updates: Update data
            
        Returns:
            Updated agent object
            
        Raises:
            HTTPException: If agent not found or update fails
        """
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Agent not found"
                )
            
            # Update only provided fields
            update_data = updates.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(agent, field, value)
            
            agent.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(agent)
            
            logger.info(f"Agent updated successfully: {agent.id}")
            return agent
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating agent {agent_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update agent"
            )
    
    @staticmethod
    def delete_agent(db: Session, agent_id: str, soft_delete: bool = True) -> bool:
        """
        Delete an agent (soft delete by default).
        
        Args:
            db: Database session
            agent_id: Agent identifier
            soft_delete: Whether to soft delete (deactivate) or hard delete
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If agent not found or deletion fails
        """
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Agent not found"
                )
            
            if soft_delete:
                # Soft delete - just deactivate
                agent.is_active = False
                agent.updated_at = datetime.utcnow()
                db.commit()
                logger.info(f"Agent soft deleted (deactivated): {agent.id}")
            else:
                # Hard delete - remove from database
                # Note: This will fail if there are foreign key constraints
                db.delete(agent)
                db.commit()
                logger.info(f"Agent hard deleted: {agent.id}")
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting agent {agent_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete agent"
            )
    
    @staticmethod
    def bulk_update_agents(db: Session, agent_ids: List[str], operation: str) -> Dict[str, Any]:
        """
        Perform bulk operations on multiple agents.
        
        Args:
            db: Database session
            agent_ids: List of agent IDs
            operation: Operation to perform ('activate', 'deactivate', 'delete')
            
        Returns:
            Results summary
        """
        try:
            results = {
                'success': [],
                'failed': [],
                'total': len(agent_ids)
            }
            
            for agent_id in agent_ids:
                try:
                    if operation == 'activate':
                        agent = db.query(Agent).filter(Agent.id == agent_id).first()
                        if agent:
                            agent.is_active = True
                            agent.updated_at = datetime.utcnow()
                            results['success'].append(agent_id)
                        else:
                            results['failed'].append({'id': agent_id, 'error': 'Not found'})
                    
                    elif operation == 'deactivate':
                        agent = db.query(Agent).filter(Agent.id == agent_id).first()
                        if agent:
                            agent.is_active = False
                            agent.updated_at = datetime.utcnow()
                            results['success'].append(agent_id)
                        else:
                            results['failed'].append({'id': agent_id, 'error': 'Not found'})
                    
                    elif operation == 'delete':
                        AgentService.delete_agent(db, agent_id, soft_delete=True)
                        results['success'].append(agent_id)
                    
                except Exception as e:
                    results['failed'].append({'id': agent_id, 'error': str(e)})
            
            db.commit()
            logger.info(f"Bulk operation {operation} completed: {len(results['success'])} success, {len(results['failed'])} failed")
            return results
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error in bulk operation {operation}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to perform bulk operation"
            )
    
    @staticmethod
    def _get_agent_usage_stats(db: Session, agent_id: str) -> AgentUsageStats:
        """
        Get usage statistics for an agent.
        
        Args:
            db: Database session
            agent_id: Agent identifier
            
        Returns:
            Agent usage statistics
        """
        try:
            # Count total conversations (questions) for this agent
            total_conversations = db.query(func.count(Question.id)).filter(
                Question.agent_id == agent_id
            ).scalar() or 0
            
            # Get last used date
            last_question = db.query(Question).filter(
                Question.agent_id == agent_id
            ).order_by(Question.created_at.desc()).first()
            
            last_used = last_question.created_at if last_question else None
            
            return AgentUsageStats(
                total_conversations=total_conversations,
                total_messages=total_conversations,  # For now, assuming 1:1 mapping
                last_used=last_used,
                avg_response_time_ms=None,  # TODO: Implement response time tracking
                user_satisfaction_score=None  # TODO: Implement satisfaction tracking
            )
            
        except Exception as e:
            logger.error(f"Error getting usage stats for agent {agent_id}: {str(e)}")
            return AgentUsageStats()
    
    @staticmethod
    def validate_agent_access(db: Session, agent_id: str, user_role: UserRole = UserRole.REGULAR) -> Agent:
        """
        Validate agent access and return agent if accessible.
        
        Args:
            db: Database session
            agent_id: Agent identifier
            user_role: Role of the requesting user
            
        Returns:
            Agent object if accessible
            
        Raises:
            HTTPException: If agent not found or access denied
        """
        return AgentService.get_agent_by_id(db, agent_id, user_role) 