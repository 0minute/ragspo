"""Qdrant client module for vector database operations.

This module provides functions to interact with Qdrant vector database.
"""

from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import get_settings


def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client instance.
    
    Returns:
        QdrantClient: Configured Qdrant client (local file or server mode).
        
    Note:
        Supports two modes:
        - "local": Stores data in local filesystem (no Docker required)
        - "server": Connects to Qdrant server (requires Docker or remote server)
    """
    settings = get_settings()
    
    # if settings.qdrant_mode == "local":
    # Local mode: stores data in filesystem (no Docker needed!)
    print(f"[Qdrant] Using LOCAL mode: {settings.qdrant_path}")
    client = QdrantClient(path=settings.qdrant_path)
    # else:
    #     # Server mode: connects to Qdrant server
    #     print(f"[Qdrant] Using SERVER mode: {settings.qdrant_host}:{settings.qdrant_port}")
    #     client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
    
    return client


def create_collection(
    collection_name: Optional[str] = None,
    vector_size: Optional[int] = None,
    distance: Distance = Distance.COSINE,
) -> None:
    """Create a new collection in Qdrant if it doesn't exist.
    
    Args:
        collection_name: Name of the collection to create. If None, uses default from settings.
        vector_size: Size of the embedding vectors. If None, uses default from settings.
        distance: Distance metric for vector similarity (COSINE, EUCLID, DOT).
        
    Note:
        If the collection already exists, this function will not raise an error.
    """
    settings = get_settings()
    client = get_qdrant_client()
    
    if collection_name is None:
        collection_name = settings.qdrant_collection_name
    
    if vector_size is None:
        vector_size = settings.embedding_dimension
    
    # Check if collection exists
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if collection_name not in collection_names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )
        print(f"Created collection: {collection_name}")
    else:
        print(f"Collection {collection_name} already exists")


def ensure_collection_exists() -> None:
    """Ensure the default SPO documents collection exists in Qdrant.
    
    This is a convenience function that creates the collection with default settings.
    """
    create_collection()

