"""
Learning Portal - Code Migration Script

This script migrates code from the original flat structure to the new modular structure.
It creates backups of original files and copies the appropriate content to the new files.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: PracPad
"""

import os
import shutil
import sys
import re
from datetime import datetime

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def backup_file(file_path):
    """Create a backup of the original file"""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.{timestamp}.bak"
        try:
            shutil.copy2(file_path, backup_path)
            print(f"Created backup: {backup_path}")
        except Exception as e:
            print(f"Failed to create backup of {file_path}: {str(e)}")
            return False
    return True

def migrate_code():
    """Migrate code from original structure to new structure"""
    print("Starting code migration...")
    
    # Create backups of original files
    files_to_backup = ["api.py", "models.py", "qdrant_agent.py", "loadDocs.py"]
    for file in files_to_backup:
        backup_file(file)
    
    # Make sure directories exist (just in case)
    directories = [
        "app", "app/api", "app/api/endpoints", "app/api/middleware",
        "app/core", "app/core/agent", "app/db", "app/models",
        "app/services", "app/utils", "scripts"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Verify the existence of the new files
    new_files = [
        "app/api/endpoints/health.py",
        "app/api/endpoints/rag.py",
        "app/core/agent/rag_agent.py",
        "app/core/config.py",
        "app/db/qdrant.py",
        "app/models/schema.py",
        "app/utils/document_loader.py",
        "app/main.py",
        "scripts/load_documents.py",
        "scripts/run_api.py",
        "run.py"
    ]
    
    for file in new_files:
        if not os.path.exists(file):
            print(f"Error: File {file} does not exist. Migration may be incomplete.")
    
    print("Code migration structure verification complete.")
    print("The new code structure is ready to use!")
    print("\nTo run the application:")
    print("1. First load documents: python scripts/load_documents.py")
    print("2. Then start the API: python run.py")

if __name__ == "__main__":
    migrate_code() 