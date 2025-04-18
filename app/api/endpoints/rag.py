"""
Learning Portal - RAG API Endpoints

This module contains the FastAPI endpoints for the RAG functionality.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Dict, Optional, List
import logging

from app.models.schema import Question, AnswerAnalysis, AnalysisResponse, ChatbotInfo
from app.core.agent.rag_agent import get_qdrant_response_stream, get_streaming_analysis
from app.core.config import logger
from app.models.sql_models import User
from app.utils.auth import get_current_active_user
from app.db.qdrant import get_collections

router = APIRouter(tags=["rag"])

@router.get("/chatbots", response_model=List[ChatbotInfo])
async def get_chatbots(current_user: User = Depends(get_current_active_user)):
    """
    Get a list of available chatbots based on Qdrant collections.
    Each collection (module_docs) becomes a chatbot with the module name.
    Requires authentication.
    """
    try:
        # Get modules from Qdrant collections
        modules = get_collections()
        
        # Transform to chatbot format with icons and descriptions
        chatbots = []
        for module in modules:
            chatbot = ChatbotInfo(
                id=module["id"],
                name=module["name"],
                description=f"AI assistant for {module['name']} knowledge base",
                icon="🤖"  # Default icon, could be customized based on module name
            )
            chatbots.append(chatbot)
            
        return chatbots
    except Exception as e:
        logger.error(f"Error retrieving chatbots: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chatbots")

@router.post("/ask_bot")
async def ask_bot(
    question: Question,
    current_user: User = Depends(get_current_active_user)
):
    """
    Ask a question to the bot with streaming response.
    Requires authentication.
    """
    try:
        # Return a streaming response that sends chunks as they become available
        return StreamingResponse(
            get_qdrant_response_stream(
                question.text, 
                module=question.module,
                history=question.history
            ),
            media_type='text/event-stream'
        )
    except Exception as e:
        logger.error(f"Error in ask_bot endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze_answer")
async def analyze_answer(
    request: AnswerAnalysis,
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze user's answer using guidelines and knowledge base context.
    Requires authentication.
    """
    try:
        return StreamingResponse(
            get_streaming_analysis(
                request.question,
                request.user_answer,
                request.guide,
                module=request.module
            ),
            media_type='text/event-stream'
        )
    except Exception as e:
        logger.error(f"Error in analyze_answer endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 