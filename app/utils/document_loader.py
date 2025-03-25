"""
Learning Portal - Document Loader Utilities

This module provides utilities for loading documents from various sources
and processing them for vector storage.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from app.core.config import logger
from app.db.qdrant import init_qdrant_client, create_collection, get_collection_name

def load_pdf_directory(directory_path: str = "./data/pdfs", collection_name: str = None):
    """
    Load all PDF documents from a directory, split them into chunks,
    and store them in the Qdrant vector database.
    """
    if collection_name is None:
        collection_name = get_collection_name()
    
    try:
        # Identify PDF files in the data directory
        pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
        
        # Log basic file information
        logger.info(f"Found {len(pdf_files)} PDF files in directory")

        # Load all PDF documents from directory using LangChain's loader
        # Handles PDF parsing and metadata extraction
        loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} document pages total")

        # Count documents by source for monitoring
        doc_count = {}
        for doc in documents:
            source = doc.metadata.get('source', 'Unknown source')
            doc_count[source] = doc_count.get(source, 0) + 1
        
        # Split documents into smaller chunks for better retrieval
        # Uses recursive character splitting with overlap to maintain context
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Each chunk is ~500 characters
            chunk_overlap=50  # 50 character overlap between chunks prevents context loss
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split into {len(chunks)} chunks")

        # Initialize OpenAI embeddings API client
        embeddings = OpenAIEmbeddings()
        
        # Get or create Qdrant client and collection
        client = init_qdrant_client()
        create_collection(client, collection_name, recreate=True)
        
        # Process documents in batches to avoid API rate limits
        # and manage memory usage for large document sets
        batch_size = 100
        total_batches = (len(chunks) - 1) // batch_size + 1
        
        # Process each batch of documents
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [doc.page_content for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            
            # Log OpenAI API call for embeddings in a consistent format
            logger.info(f"OpenAI API Call - Embeddings - Batch {i//batch_size + 1}/{total_batches} - {len(texts)} chunks")
            
            # Generate vector embeddings for the batch using OpenAI's API
            embedding_vectors = embeddings.embed_documents(texts)
            
            # Prepare points for Qdrant with both text and vectors
            # Each point includes the original text, vector, and metadata
            points = []
            for idx, (text, vector, metadata) in enumerate(zip(texts, embedding_vectors, metadatas)):
                if text:  # Only add non-empty texts
                    points.append({
                        "id": idx + i,
                        "vector": vector,
                        "payload": {
                            "page_content": text,
                            "metadata": metadata,
                            "source": metadata.get("source", ""),
                            "page": metadata.get("page", 0)
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

# Add additional document loading functions as needed 