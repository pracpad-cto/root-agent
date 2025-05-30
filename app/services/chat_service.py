"""
Learning Portal - Chat Service

This module provides business logic for chat operations with dynamic agent configurations.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from typing import Dict, List, Optional, Any, AsyncGenerator
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import time

from app.models.sql_models import Agent, User
from app.models.agent_schema import ChatRequest, AgentTestRequest, AgentTestResponse
from app.services.agent_service import AgentService
from app.core.config import logger

class ChatService:
    """Service class for chat operations with dynamic agent configurations"""
    
    @staticmethod
    def prepare_agent_config(agent: Agent) -> Dict[str, Any]:
        """
        Prepare agent configuration for RAG processing.
        
        Args:
            agent: Agent object from database
            
        Returns:
            Agent configuration dictionary
        """
        return {
            'agent_id': agent.id,
            'agent_name': agent.name,
            'system_prompt': agent.system_prompt,
            'qdrant_collection': agent.qdrant_collection,
            'description': agent.description,
            'icon': agent.icon
        }
    
    @staticmethod
    async def chat_with_agent(
        db: Session,
        chat_request: ChatRequest,
        user: User
    ) -> AsyncGenerator[str, None]:
        """
        Process chat request with specified agent using streaming response.
        Note: Chat history is not saved to database per requirements.
        
        Args:
            db: Database session
            chat_request: Chat request with agent_id and message
            user: Current user
            
        Yields:
            Streaming response chunks
            
        Raises:
            HTTPException: If agent not found or chat fails
        """
        try:
            # Validate agent access
            agent = AgentService.validate_agent_access(
                db, 
                chat_request.agent_id, 
                user.role
            )
            
            # Prepare agent configuration
            agent_config = ChatService.prepare_agent_config(agent)
            
            # Import RAG function here to avoid circular imports
            from app.core.agent.rag_agent import get_agent_response_stream
            
            # Get streaming response from RAG agent with dynamic configuration
            async for chunk in get_agent_response_stream(
                question=chat_request.message,
                agent_config=agent_config,
                history=chat_request.history or []
            ):
                yield chunk
            
            logger.info(f"Chat completed for user {user.id} with agent {agent.id}")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in chat with agent {chat_request.agent_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process chat request"
            )
    
    @staticmethod
    async def test_agent_configuration(
        db: Session,
        agent_id: str,
        test_request: AgentTestRequest
    ) -> AgentTestResponse:
        """
        Test an agent configuration with a sample message.
        
        Args:
            db: Database session
            agent_id: Agent identifier
            test_request: Test request with message
            
        Returns:
            Test response with results
        """
        start_time = time.time()
        
        try:
            # Get agent (admin access assumed)
            agent = AgentService.get_agent_by_id(db, agent_id, user_role=None)
            
            # Prepare agent configuration
            agent_config = ChatService.prepare_agent_config(agent)
            
            # Import RAG function
            from app.core.agent.rag_agent import get_agent_response_stream
            
            # Get response from RAG agent
            response_chunks = []
            async for chunk in get_agent_response_stream(
                question=test_request.test_message,
                agent_config=agent_config,
                history=test_request.test_history or []
            ):
                response_chunks.append(chunk)
            
            complete_response = ''.join(response_chunks)
            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)
            
            return AgentTestResponse(
                agent_id=agent_id,
                test_message=test_request.test_message,
                response=complete_response,
                response_time_ms=response_time_ms,
                success=True
            )
            
        except Exception as e:
            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)
            
            logger.error(f"Error testing agent {agent_id}: {str(e)}")
            return AgentTestResponse(
                agent_id=agent_id,
                test_message=test_request.test_message,
                response="",
                response_time_ms=response_time_ms,
                success=False,
                error=str(e)
            )
    
    @staticmethod
    def validate_chat_request(chat_request: ChatRequest) -> None:
        """
        Validate chat request parameters.
        
        Args:
            chat_request: Chat request to validate
            
        Raises:
            HTTPException: If validation fails
        """
        if not chat_request.agent_id or not chat_request.agent_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent ID is required"
            )
        
        if not chat_request.message or not chat_request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is required"
            )
        
        if len(chat_request.message) > 10000:  # 10KB limit
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message too long (max 10,000 characters)"
            ) 