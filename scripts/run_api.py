"""
Learning Portal - API Run Script

This script provides a command-line interface for running the FastAPI application.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

import sys
import os
import uvicorn
import argparse

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    """
    Main entry point for API run script.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run the FastAPI application')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind the server to')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    args = parser.parse_args()

    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == '__main__':
    main() 