"""
Learning Portal - RAG API Endpoints

This module contains the FastAPI endpoints for the RAG functionality.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, Optional, List
import logging

from app.models.schema import Question, AnswerAnalysis, AnalysisResponse
from app.core.agent.rag_agent import get_qdrant_response_stream, get_streaming_analysis
from app.core.config import logger

router = APIRouter(tags=["rag"])

@router.post("/ask_bot")
async def ask_bot(question: Question):
    """
    Ask a question to the bot with streaming response
    """
    try:
        # Return a streaming response that sends chunks as they become available
        return StreamingResponse(
            get_qdrant_response_stream(
                question.text, 
                module=question.module,
                unit=question.unit,
                history=question.history
            ),
            media_type='text/event-stream'
        )
    except Exception as e:
        logger.error(f"Error in ask_bot endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze_answer")
async def analyze_answer(request: AnswerAnalysis):
    """
    Analyze user's answer using guidelines and knowledge base context
    """
    try:
        return StreamingResponse(
            get_streaming_analysis(
                request.question,
                request.user_answer,
                request.guide,
                module=request.module,
                unit=request.unit
            ),
            media_type='text/event-stream'
        )
    except Exception as e:
        logger.error(f"Error in analyze_answer endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 