"""
Learning Portal - Main Application

This module initializes and configures the FastAPI application.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import api_router
from app.core.config import settings, logger

# Lifecycle management for FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.
    Handles initialization and cleanup tasks.
    """
    # Initialization code here
    logger.info("API initialized")
    yield
    # Cleanup code here
    logger.info("API shutdown")

# Create and configure FastAPI application
def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    # Initialize FastAPI application with metadata and lifecycle manager
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        contact={
            "name": "AI Agent Support",
            "email": "support@example.com",
        },
        lifespan=lifespan
    )

    # Configure CORS to allow cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Include API router
    app.include_router(api_router)

    return app

# Create application instance
app = create_application() 