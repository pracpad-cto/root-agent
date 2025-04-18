"""
Learning Portal - Document Loading Script

This script provides a command-line interface for loading documents
into the Qdrant vector database.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

import sys
import os
import argparse

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.document_loader import load_pdf_directory
from app.db.qdrant import get_collection_name
from app.core.config import logger

def main():
    """
    Main entry point for document loading script.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Load documents into Qdrant vector database')
    parser.add_argument('--dir', type=str, default='./data/pdfs', help='Directory containing PDF files')
    parser.add_argument('--module', type=str, default='module1', help='Module identifier for collection name')
    parser.add_argument('--recreate', action='store_true', help='Recreate collection if it exists')
    parser.add_argument('--no-ocr', action='store_true', help='Disable OCR processing for scanned documents')
    parser.add_argument('--poppler-path', type=str, default=os.getenv('POPPLER_PATH', ''), 
                        help='Path to poppler binaries for PDF to image conversion')
    args = parser.parse_args()

    # Generate collection name based on module
    collection_name = get_collection_name(args.module)

    logger.info(f"Loading documents from {args.dir} into collection {collection_name}")
    logger.info(f"OCR processing: {'Disabled' if args.no_ocr else 'Enabled'}")
    
    try:
        # Load documents
        load_pdf_directory(
            directory_path=args.dir, 
            collection_name=collection_name,
            use_ocr=not args.no_ocr,
            poppler_path=args.poppler_path
        )
        logger.info("Documents loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 