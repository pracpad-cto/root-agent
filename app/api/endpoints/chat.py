"""
Learning Portal - Chat API Endpoints

This module contains the FastAPI endpoints for the dynamic agent chat system.
Chat functionality is restricted to admin and superadmin users only.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.db.sql import get_db
from app.models.sql_models import User
from app.models.agent_schema import ChatRequest, PublicChatbotInfo
from app.services.agent_service import AgentService
from app.services.chat_service import ChatService
from app.utils.auth import require_admin_access
from app.core.config import logger

router = APIRouter(tags=["chat"])

@router.get("/chatbots", response_model=List[PublicChatbotInfo])
async def get_available_chatbots(
    current_user: User = Depends(require_admin_access)
):
    """
    Get available chatbots for admin users.
    Only shows active agents with limited public information.
    
    Access: Admin and Superadmin only
    
    Returns:
        List of available chatbots with public information only
    """
    try:
        db = next(get_db())
        agents = AgentService.get_public_agents(db)
        return agents
    except Exception as e:
        logger.error(f"Error retrieving available chatbots: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve available chatbots"
        )

@router.post("/chat")
async def chat_with_agent(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Chat with a specific agent using streaming response.
    Admin users can interact with active agents.
    
    Access: Admin and Superadmin only
    
    Args:
        chat_request: Chat request containing agent_id, message, and optional history
        
    Returns:
        Streaming response with agent's reply
    """
    try:
        # Validate chat request
        ChatService.validate_chat_request(chat_request)
        
        # Return streaming response
        return StreamingResponse(
            ChatService.chat_with_agent(
                db=db,
                chat_request=chat_request,
                user=current_user
            ),
            media_type='text/event-stream',
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request"
        )

@router.get("/agents/{agent_id}/info", response_model=PublicChatbotInfo)
async def get_agent_public_info(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_access)
):
    """
    Get public information about a specific agent.
    Only returns basic information available to admin users.
    
    Access: Admin and Superadmin only
    
    Args:
        agent_id: Unique agent identifier
        
    Returns:
        Public agent information
    """
    try:
        # Validate agent access (admin user permissions)
        agent = AgentService.validate_agent_access(
            db=db,
            agent_id=agent_id,
            user_role=current_user.role
        )
        
        # Return only public information
        public_info = PublicChatbotInfo(
            id=agent.id,
            name=agent.name,
            description=agent.description,
            icon=agent.icon
        )
        
        return public_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting public info for agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agent information"
        ) 