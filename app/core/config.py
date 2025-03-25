"""
Learning Portal - Configuration Settings

This module centralizes configuration settings and environment variables
for the application.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import logging

# Load environment variables from .env file
load_dotenv(override=True)

# Make sure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/openai_api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "AI Agent API"
    API_DESCRIPTION: str = "An API for interacting with an AI agent that can answer questions based on PDF knowledge"
    API_VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Default collection settings
    DEFAULT_MODULE: str = "module1"
    
    # Get normalized Qdrant URL
    @property
    def normalized_qdrant_url(self) -> str:
        """Normalize and sanitize the Qdrant URL."""
        if not self.QDRANT_URL:
            raise ValueError("QDRANT_URL environment variable is not set")
            
        qdrant_url = self.QDRANT_URL.strip().rstrip('/')
        if ':6333' in qdrant_url:  # Remove port if present
            qdrant_url = qdrant_url.replace(':6333', '')
        if not qdrant_url.startswith(('http://', 'https://')):
            qdrant_url = f"https://{qdrant_url}"
        
        return qdrant_url

# Create instance of settings
settings = Settings()

# Log configuration on startup
logger.info(f"Environment: {settings.ENVIRONMENT}")
logger.info(f"Qdrant URL: {settings.normalized_qdrant_url}") 