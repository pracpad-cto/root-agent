"""
Learning Portal - API Router

This module combines all API endpoints into a single router.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import APIRouter
from app.api.endpoints import health, users, auth, chat
from app.api.endpoints.admin import agents as admin_agents

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="")
api_router.include_router(users.router, prefix="")
api_router.include_router(auth.router, prefix="")

# Include new dynamic agent system endpoints
api_router.include_router(chat.router, prefix="")  # Public chat endpoints
api_router.include_router(admin_agents.router, prefix="")  # Admin agent management
