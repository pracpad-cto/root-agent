"""
Learning Portal - Document Loader Utilities

This module provides utilities for loading documents from various sources
and processing them for vector storage. Includes OCR capabilities for
handling scanned image-based PDFs.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

import os
import pytesseract
from pdf2image import convert_from_path
import pypdf
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document as LangchainDocument
from app.core.config import logger, settings
from app.db.qdrant import init_qdrant_client, create_collection, get_collection_name
from typing import List, Dict, Any, Optional

# Default poppler path - should be configured in settings or env variable
POPPLER_PATH = os.getenv("POPPLER_PATH", "")

def load_pdf_directory(directory_path: str = "./data/pdfs", collection_name: str = None, use_ocr: bool = True, poppler_path: str = POPPLER_PATH, recreate: bool = False):
    """
    Load all PDF documents from a directory, split them into chunks,
    and store them in the Qdrant vector database.
    
    Args:
        directory_path: Path to directory containing PDF files
        collection_name: Name of the Qdrant collection to store embeddings
        use_ocr: Whether to use OCR for scanned PDFs
        poppler_path: Path to poppler binaries for PDF to image conversion
        recreate: Whether to recreate the collection if it exists
    """
    if collection_name is None:
        collection_name = get_collection_name()
    
    try:
        # Identify PDF files in the data directory
        pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
        
        # Log basic file information
        logger.info(f"Found {len(pdf_files)} PDF files in directory")

        # Process documents with both text extraction methods
        all_documents = []
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory_path, pdf_file)
            logger.info(f"Processing PDF: {pdf_path}")
            
            # First try with standard PyPDF extraction
            regular_documents = extract_text_with_pypdf(pdf_path)
            
            # Check if regular extraction produced sufficient text
            if regular_documents and has_sufficient_text(regular_documents):
                logger.info(f"Using standard PyPDF extraction for {pdf_file}")
                all_documents.extend(regular_documents)
            else:
                # If standard extraction fails, use OCR if enabled
                if use_ocr:
                    logger.info(f"Standard extraction insufficient, using OCR for {pdf_file}")
                    ocr_documents = extract_text_with_ocr(pdf_path, poppler_path)
                    all_documents.extend(ocr_documents)
                    logger.info(f"Extracted {len(ocr_documents)} pages with OCR from {pdf_file}")
                else:
                    logger.warning(f"Standard extraction failed and OCR is disabled. Skipping {pdf_file}")
        
        logger.info(f"Loaded {len(all_documents)} document pages total")

        # Split documents into smaller chunks for better retrieval
        # Uses recursive character splitting with overlap to maintain context
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Each chunk is ~500 characters
            chunk_overlap=50  # 50 character overlap between chunks prevents context loss
        )
        chunks = text_splitter.split_documents(all_documents)
        logger.info(f"Split into {len(chunks)} chunks")

        # Initialize OpenAI embeddings API client
        embeddings = OpenAIEmbeddings()
        
        # Get or create Qdrant client and collection
        client = init_qdrant_client()
        create_collection(client, collection_name, recreate=recreate)
        
        # Process documents in batches to avoid API rate limits
        # and manage memory usage for large document sets
        batch_size = 100
        total_batches = (len(chunks) - 1) // batch_size + 1
        
        # Process each batch of documents
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [doc.page_content for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            
            # Skip empty texts
            valid_indices = [idx for idx, text in enumerate(texts) if text and text.strip()]
            valid_texts = [texts[idx] for idx in valid_indices]
            valid_metadatas = [metadatas[idx] for idx in valid_indices]
            
            if not valid_texts:
                logger.warning(f"Batch {i//batch_size + 1} contains no valid texts. Skipping.")
                continue
            
            # Log OpenAI API call for embeddings in a consistent format
            logger.info(f"OpenAI API Call - Embeddings - Batch {i//batch_size + 1}/{total_batches} - {len(valid_texts)} chunks")
            
            # Generate vector embeddings for the batch using OpenAI's API
            embedding_vectors = embeddings.embed_documents(valid_texts)
            
            # Prepare points for Qdrant with both text and vectors
            # Each point includes the original text, vector, and metadata
            points = []
            for idx, (text, vector, metadata) in enumerate(zip(valid_texts, embedding_vectors, valid_metadatas)):
                if text:  # Double-check for non-empty texts
                    points.append({
                        "id": idx + i,
                        "vector": vector,
                        "payload": {
                            "page_content": text,
                            "metadata": metadata,
                            "source": metadata.get("source", ""),
                            "page": metadata.get("page", 0),
                            "extraction_method": metadata.get("extraction_method", "standard")
                        }
                    })
            
            # Add vectors and metadata to Qdrant
            client.upsert(
                collection_name=collection_name,
                points=points
            )
            logger.info(f"Processed batch {i//batch_size + 1} of {total_batches}")

        # Log successful completion
        logger.info(f"Successfully loaded {len(chunks)} chunks into Qdrant!")
        logger.info(f"Collection name: {collection_name}")

    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        raise

def extract_text_with_pypdf(pdf_path: str) -> List[LangchainDocument]:
    """
    Extract text from PDF using PyPDF
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of LangChain documents
    """
    documents = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text or len(text) < 50:  # Skip pages with little or no text
                    continue
                    
                documents.append(
                    LangchainDocument(
                        page_content=text,
                        metadata={
                            "page": i+1,
                            "source": os.path.basename(pdf_path),
                            "extraction_method": "standard"
                        }
                    )
                )
        
        return documents
    except Exception as e:
        logger.error(f"Error extracting text with PyPDF from {pdf_path}: {str(e)}")
        return []

def extract_text_with_ocr(pdf_path: str, poppler_path: str = "") -> List[LangchainDocument]:
    """
    Extract text from PDF using OCR
    
    Args:
        pdf_path: Path to PDF file
        poppler_path: Path to poppler binaries
        
    Returns:
        List of LangChain documents
    """
    documents = []
    page_num = 0
    
    try:
        conversion_kwargs = {}
        if poppler_path:
            conversion_kwargs["poppler_path"] = poppler_path
            
        # Determine total pages for logging
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            total_pages = len(reader.pages)
            
        logger.info(f"Starting OCR processing for {pdf_path} with {total_pages} pages")
            
        while True:
            page_num += 1
            
            if page_num > total_pages:
                break
                
            try:
                logger.info(f"Processing page {page_num}/{total_pages} with OCR")
                
                # Convert PDF page to image
                images = convert_from_path(
                    pdf_path,
                    first_page=page_num,
                    last_page=page_num,
                    **conversion_kwargs
                )
                
                if not images:
                    logger.warning(f"No images extracted for page {page_num}. Skipping.")
                    continue
                    
                image = images[0]
                
                # Extract text using OCR
                text = pytesseract.image_to_string(image)
                
                if not text or len(text) < 50:  # Skip pages with little or no text
                    logger.warning(f"Page {page_num} has insufficient text. Skipping.")
                    continue
                
                # Create document with extracted text
                documents.append(
                    LangchainDocument(
                        page_content=text,
                        metadata={
                            "page": page_num,
                            "source": os.path.basename(pdf_path),
                            "extraction_method": "ocr"
                        }
                    )
                )
                    
            except Exception as e:
                logger.error(f"Error processing page {page_num} with OCR: {str(e)}")
                if page_num > 100:  # Safety limit
                    logger.warning("Reached safety limit of 100 pages. Stopping OCR processing.")
                    break
                continue
        
        return documents
    except Exception as e:
        logger.error(f"Error extracting text with OCR from {pdf_path}: {str(e)}")
        return []

def has_sufficient_text(documents: List[LangchainDocument]) -> bool:
    """
    Check if the extracted documents have sufficient text
    
    Args:
        documents: List of documents
        
    Returns:
        Boolean indicating if documents have sufficient text
    """
    if not documents:
        return False
        
    # Check if at least 25% of pages have reasonable text content
    total_pages = len(documents)
    pages_with_text = sum(1 for doc in documents if len(doc.page_content) > 100)
    
    return pages_with_text >= max(1, total_pages * 0.25)

# Add additional document loading functions as needed 