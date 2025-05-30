"""
Learning Portal - Qdrant Database Connection

This module handles the connection to the Qdrant vector database
and provides functions for interacting with it.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: PracPad
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from app.core.config import settings, logger

# Helper function to generate collection name based on module
def get_collection_name(module: str = "module1") -> str:
    """Generate collection name based on module"""
    return f"{module}_docs"

def init_qdrant_client():
    """Initialize the Qdrant client with proper error handling"""
    try:
        # Create client with increased timeout for large document processing
        client = QdrantClient(
            url=settings.normalized_qdrant_url,
            api_key=settings.QDRANT_API_KEY,
            timeout=120,  # Increased timeout for large operations
            prefer_grpc=False  # Force HTTP protocol for compatibility
        )
        
        # Test connection by retrieving collections list
        collections = client.get_collections()
        logger.info(f"Successfully connected to Qdrant cloud! {collections}")
        
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {str(e)}")
        raise

def create_collection(client: QdrantClient, collection_name: str, recreate: bool = False):
    """Create a new collection or recreate an existing one"""
    try:
        # Check if collection exists and delete if needed
        if recreate and client.collection_exists(collection_name):
            logger.info(f"Deleting existing collection: {collection_name}")
            client.delete_collection(collection_name)
        
        # Only create if it doesn't exist or we're recreating
        if not client.collection_exists(collection_name) or recreate:
            # Create new collection with appropriate vector dimensions
            # OpenAI embeddings use 1536-dimensional vectors
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
            logger.info(f"Created Qdrant collection: {collection_name}")
    except Exception as e:
        logger.error(f"Error creating/recreating collection {collection_name}: {str(e)}")
        raise

def init_vector_store(collection_name: str = None):
    """Initialize the Qdrant vector store with the given collection name"""
    if collection_name is None:
        collection_name = get_collection_name(settings.DEFAULT_MODULE)
    
    client = init_qdrant_client()
    
    # Initialize embeddings client
    embeddings = OpenAIEmbeddings()
    
    # Create Qdrant vector store
    vector_store = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )
    
    return vector_store, client 

def get_collections():
    """
    Get all collections from Qdrant and transform them into module information.
    
    Returns:
        List of dictionaries with module information extracted from collection names
    """
    try:
        client = init_qdrant_client()
        collections_info = client.get_collections()
        
        # Extract module names from collection names (removing the "_docs" suffix)
        modules = []
        for collection in collections_info.collections:
            name = collection.name
            if name.endswith("_docs"):
                module_name = name[:-5]  # Remove "_docs" suffix
                modules.append({
                    "id": module_name,
                    "name": module_name.title(),  # Capitalize first letter for display
                    "collection": name
                })
        
        logger.info(f"Retrieved {len(modules)} modules from Qdrant collections")
        return modules
    except Exception as e:
        logger.error(f"Error retrieving collections from Qdrant: {str(e)}")
        return []

def get_collections_detailed():
    """
    Get detailed information about all collections from Qdrant.
    
    Returns:
        List of dictionaries with detailed collection information
    """
    try:
        client = init_qdrant_client()
        collections_info = client.get_collections()
        
        detailed_collections = []
        for collection in collections_info.collections:
            try:
                # Get collection info including vector count and configuration
                collection_info = client.get_collection(collection.name)
                
                detailed_collection = {
                    "name": collection.name,
                    "status": collection_info.status,
                    "vectors_count": collection_info.vectors_count if collection_info.vectors_count else 0,
                    "points_count": collection_info.points_count if collection_info.points_count else 0,
                    "segments_count": len(collection_info.segments) if collection_info.segments else 0,
                    "config": {
                        "vector_size": collection_info.config.params.vectors.size if collection_info.config.params.vectors else None,
                        "distance": collection_info.config.params.vectors.distance.value if collection_info.config.params.vectors else None,
                        "indexed": collection_info.config.params.vectors.hnsw_config is not None if collection_info.config.params.vectors else False
                    } if collection_info.config else {},
                    "disk_data_size": getattr(collection_info, 'disk_data_size', 0),
                    "ram_data_size": getattr(collection_info, 'ram_data_size', 0)
                }
                detailed_collections.append(detailed_collection)
                
            except Exception as collection_error:
                logger.warning(f"Error getting details for collection {collection.name}: {str(collection_error)}")
                # Add basic info even if detailed info fails
                detailed_collections.append({
                    "name": collection.name,
                    "status": "unknown",
                    "vectors_count": 0,
                    "points_count": 0,
                    "segments_count": 0,
                    "config": {},
                    "disk_data_size": 0,
                    "ram_data_size": 0,
                    "error": str(collection_error)
                })
        
        logger.info(f"Retrieved detailed information for {len(detailed_collections)} collections")
        return detailed_collections
        
    except Exception as e:
        logger.error(f"Error retrieving detailed collections from Qdrant: {str(e)}")
        return [] 