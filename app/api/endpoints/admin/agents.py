"""
Learning Portal - Admin Agent Management API Endpoints

This module contains admin-only API endpoints for agent management.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.sql import get_db
from app.models.sql_models import User
from app.models.agent_schema import (
    AgentCreate, AgentUpdate, AdminAgentResponse, AgentTestRequest, 
    AgentTestResponse, BulkAgentOperation, AgentListResponse
)
from app.services.agent_service import AgentService
from app.services.chat_service import ChatService
from app.utils.auth import require_admin_access, require_superadmin_access
from app.core.config import logger
from app.db.qdrant import get_collections_detailed

router = APIRouter(tags=["admin-agents"], prefix="/admin")

@router.get("/agents", response_model=List[AdminAgentResponse])
async def get_all_agents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    include_stats: bool = Query(True, description="Include usage statistics"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Get all agents with complete information (admin only).
    
    Returns:
        List of agents with full admin information including usage statistics
    """
    try:
        agents = AgentService.get_admin_agents(
            db=db, 
            skip=skip, 
            limit=limit, 
            include_stats=include_stats
        )
        return agents
    except Exception as e:
        logger.error(f"Error in get_all_agents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agents"
        )

@router.get("/agents/{agent_id}", response_model=AdminAgentResponse)
async def get_agent_details(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Get detailed information about a specific agent (admin only).
    
    Args:
        agent_id: Unique agent identifier
        
    Returns:
        Complete agent information with statistics
    """
    try:
        # Get agent with admin access (can see inactive agents)
        agent = AgentService.get_agent_by_id(db, agent_id, current_user.role)
        
        # Get usage statistics
        usage_stats = AgentService._get_agent_usage_stats(db, agent_id)
        
        # Prepare admin response
        admin_response = AdminAgentResponse(
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
            usage_stats=usage_stats.dict()
        )
        
        return admin_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent details for {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agent details"
        )

@router.post("/agents", response_model=AdminAgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Create a new agent (admin only).
    
    Args:
        agent_data: Agent creation data
        
    Returns:
        Created agent information
    """
    try:
        agent = AgentService.create_agent(
            db=db,
            agent_data=agent_data,
            creator_id=current_user.id
        )
        
        # Return admin response format
        admin_response = AdminAgentResponse(
            id=agent.id,
            name=agent.name,
            description=agent.description,
            system_prompt=agent.system_prompt,
            icon=agent.icon,
            qdrant_collection=agent.qdrant_collection,
            is_active=agent.is_active,
            created_by=agent.created_by,
            creator_name=f"{current_user.first_name} {current_user.last_name}",
            created_at=agent.created_at,
            updated_at=agent.updated_at,
            usage_stats={}
        )
        
        return admin_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create agent"
        )

@router.put("/agents/{agent_id}", response_model=AdminAgentResponse)
async def update_agent(
    agent_id: str,
    updates: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Update an existing agent (admin only).
    
    Args:
        agent_id: Unique agent identifier
        updates: Agent update data
        
    Returns:
        Updated agent information
    """
    try:
        agent = AgentService.update_agent(
            db=db,
            agent_id=agent_id,
            updates=updates
        )
        
        # Get usage statistics
        usage_stats = AgentService._get_agent_usage_stats(db, agent_id)
        
        # Return admin response format
        admin_response = AdminAgentResponse(
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
            usage_stats=usage_stats.dict()
        )
        
        return admin_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent"
        )

@router.delete("/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    hard_delete: bool = Query(False, description="Perform hard delete instead of soft delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Delete an agent (admin only).
    
    Args:
        agent_id: Unique agent identifier
        hard_delete: Whether to permanently delete the agent
        
    Returns:
        Success confirmation
    """
    try:
        # Only superadmins can perform hard deletes
        if hard_delete and current_user.role.value != "superadmin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only superadmins can perform hard deletes"
            )
        
        success = AgentService.delete_agent(
            db=db,
            agent_id=agent_id,
            soft_delete=not hard_delete
        )
        
        delete_type = "hard deleted" if hard_delete else "deactivated"
        return {
            "message": f"Agent {agent_id} successfully {delete_type}",
            "agent_id": agent_id,
            "hard_delete": hard_delete
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete agent"
        )

@router.post("/agents/{agent_id}/test", response_model=AgentTestResponse)
async def test_agent_configuration(
    agent_id: str,
    test_request: AgentTestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Test an agent configuration with a sample message (admin only).
    
    Args:
        agent_id: Unique agent identifier
        test_request: Test message and optional history
        
    Returns:
        Test results including response and performance metrics
    """
    try:
        test_response = await ChatService.test_agent_configuration(
            db=db,
            agent_id=agent_id,
            test_request=test_request
        )
        
        return test_response
        
    except Exception as e:
        logger.error(f"Error testing agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to test agent configuration"
        )

@router.post("/agents/bulk-operation")
async def bulk_agent_operation(
    operation_request: BulkAgentOperation,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Perform bulk operations on multiple agents (admin only).
    
    Args:
        operation_request: List of agent IDs and operation to perform
        
    Returns:
        Results summary showing success and failed operations
    """
    try:
        # Only superadmins can perform delete operations
        if operation_request.operation == "delete" and current_user.role.value != "superadmin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only superadmins can perform bulk delete operations"
            )
        
        results = AgentService.bulk_update_agents(
            db=db,
            agent_ids=operation_request.agent_ids,
            operation=operation_request.operation
        )
        
        return {
            "operation": operation_request.operation,
            "total_agents": results["total"],
            "successful": len(results["success"]),
            "failed": len(results["failed"]),
            "success_ids": results["success"],
            "failed_operations": results["failed"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk operation {operation_request.operation}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform bulk operation"
        )

@router.get("/collections")
async def get_qdrant_collections(
    current_user: User = Depends(require_admin_access)
):
    """
    Get all Qdrant vector collections with detailed information (admin only).
    
    This endpoint provides comprehensive information about all available
    Qdrant collections including vector counts, configuration, and storage metrics.
    
    Access: Admin and Superadmin only
    
    Returns:
        List of collections with detailed information including:
        - Collection name and status
        - Vector and point counts
        - Configuration details (vector size, distance metric)
        - Storage metrics (disk and RAM usage)
    """
    try:
        collections = get_collections_detailed()
        
        return {
            "total_collections": len(collections),
            "collections": collections,
            "retrieved_at": "now"
        }
        
    except Exception as e:
        logger.error(f"Error retrieving Qdrant collections: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve Qdrant collections"
        ) 