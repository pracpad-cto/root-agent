"""
Learning Portal - Health Check Endpoint

This module contains the health check endpoint for the API.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter
from typing import Dict

router = APIRouter(tags=["health"])

@router.get("/")
async def root() -> Dict[str, str]:
    """
    Health check endpoint to verify the API is running
    """
    return {"message": "AI Agent API is running"} 