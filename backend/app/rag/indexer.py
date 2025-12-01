"""Document indexing module for processing and storing SPO documents in Qdrant.

This module handles the full indexing pipeline: document retrieval, chunking,
embedding, and storage in the vector database.
"""

from typing import Dict, List
from uuid import uuid4

from app.config import get_settings
from app.embeddings import embed_texts
from app.qdrant_client import get_qdrant_client
from app.rag.chunking import split_document_with_metadata
from app.sharepoint_client import get_document_content, get_document_metadata
from qdrant_client.models import PointStruct


def index_sharepoint_document(document_id: str) -> Dict[str, int]:
    """Index a SharePoint document into Qdrant vector database.
    
    This function:
    1. Retrieves document content and metadata from SharePoint
    2. Splits the document into chunks
    3. Generates embeddings for each chunk
    4. Stores chunks and embeddings in Qdrant
    
    Args:
        document_id: Unique identifier of the SharePoint document.
        
    Returns:
        Dictionary containing indexing statistics:
        - 'chunks_indexed': Number of chunks successfully indexed
        - 'document_id': The document ID that was indexed
        
    Raises:
        Exception: If document retrieval or indexing fails.
        
    TODO:
        - Add error handling for failed document retrieval
        - Implement incremental indexing (check if document already exists)
        - Add document versioning support
        - Handle large documents with batch processing
    """
    settings = get_settings()
    
    # Step 1: Get document content and metadata from SharePoint
    print(f"Retrieving document {document_id} from SharePoint...")
    document_content = get_document_content(document_id)
    document_metadata = get_document_metadata(document_id)
    
    # Step 2: Split document into chunks
    print(f"Splitting document into chunks...")
    chunks_with_metadata = split_document_with_metadata(
        text=document_content,
        document_id=document_id,
        document_name=document_metadata.get("name", "Unknown"),
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    
    if not chunks_with_metadata:
        print(f"No chunks created for document {document_id}")
        return {"chunks_indexed": 0, "document_id": document_id}
    
    # Step 3: Generate embeddings for all chunks
    print(f"Generating embeddings for {len(chunks_with_metadata)} chunks...")
    chunk_texts = [chunk["text"] for chunk in chunks_with_metadata]
    embeddings = embed_texts(chunk_texts)
    
    # Step 4: Prepare points for Qdrant
    points = []
    for chunk, embedding in zip(chunks_with_metadata, embeddings):
        point = PointStruct(
            id=str(uuid4()),  # Generate unique ID for each chunk
            vector=embedding,
            payload={
                "document_id": document_id,
                "document_name": document_metadata.get("name", "Unknown"),
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "sharepoint": {
                    "web_url": document_metadata.get("web_url", ""),
                    "download_url": document_metadata.get("download_url", ""),
                    "modified_date": document_metadata.get("modified_date", ""),
                    "author": document_metadata.get("author", ""),
                },
            },
        )
        points.append(point)
    
    # Step 5: Upload to Qdrant
    print(f"Uploading {len(points)} chunks to Qdrant...")
    client = get_qdrant_client()
    client.upsert(
        collection_name=settings.qdrant_collection_name,
        points=points,
    )
    
    print(f"Successfully indexed {len(points)} chunks for document {document_id}")
    return {"chunks_indexed": len(points), "document_id": document_id}


def index_all_sharepoint_documents() -> Dict[str, int]:
    """Index all documents from SharePoint into Qdrant.
    
    Returns:
        Dictionary containing indexing statistics:
        - 'total_documents': Total number of documents processed
        - 'total_chunks': Total number of chunks indexed
        
    TODO:
        - Implement parallel processing for multiple documents
        - Add progress tracking
        - Handle failures gracefully (continue with other documents)
    """
    from app.sharepoint_client import list_sharepoint_documents
    
    print("Listing all SharePoint documents...")
    documents = list_sharepoint_documents()
    
    total_chunks = 0
    successful_documents = 0
    
    for doc in documents:
        try:
            result = index_sharepoint_document(doc["id"])
            total_chunks += result["chunks_indexed"]
            successful_documents += 1
        except Exception as e:
            print(f"Error indexing document {doc['id']}: {e}")
            continue
    
    print(f"Indexing complete: {successful_documents}/{len(documents)} documents, {total_chunks} total chunks")
    
    return {
        "total_documents": successful_documents,
        "total_chunks": total_chunks,
    }

