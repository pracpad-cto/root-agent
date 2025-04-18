"""
Learning Portal - API Router

This module combines all API endpoints into a single router.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter
from app.api.endpoints import rag, health, users, auth

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="")
api_router.include_router(rag.router, prefix="")
api_router.include_router(users.router, prefix="")
api_router.include_router(auth.router, prefix="")
