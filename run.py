"""
Learning Portal - Main Application Runner

This module provides a convenient entry point for running the application.
Execute with `python run.py` to start the API server.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

import sys
import uvicorn

if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload for development
    ) 