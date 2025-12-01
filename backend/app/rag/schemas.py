"""Pydantic schemas for RAG API requests and responses."""

from typing import List

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Request model for document search.
    
    Attributes:
        query: The search query string.
        top_k: Number of top results to return (default: 5).
    """

    query: str = Field(..., description="Search query text", min_length=1)
    top_k: int = Field(default=5, description="Number of results to return", ge=1, le=50)


class Source(BaseModel):
    """Source document information for a search result.
    
    Attributes:
        file_title: Title or name of the source file.
        section_title: Title of the section within the document (optional).
        chunk_index: Index of the chunk within the document.
        download_url: URL to download or access the source document.
        document_id: Unique identifier of the document.
        score: Relevance score of the source (optional).
    """

    file_title: str = Field(..., description="Name of the source file")
    section_title: str = Field(default="", description="Section title within the document")
    chunk_index: int = Field(..., description="Chunk index in the document", ge=0)
    download_url: str = Field(..., description="URL to access the source document")
    document_id: str = Field(default="", description="Unique document identifier")
    score: float = Field(default=0.0, description="Relevance score", ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Response model for document search.
    
    Attributes:
        answer: Generated answer based on retrieved documents.
        sources: List of source documents used to generate the answer.
        query: Original query string (echoed back).
    """

    answer: str = Field(..., description="Generated answer text")
    sources: List[Source] = Field(default_factory=list, description="Source documents")
    query: str = Field(..., description="Original search query")


class IndexRequest(BaseModel):
    """Request model for indexing a document.
    
    Attributes:
        document_id: Unique identifier for the document.
        force_reindex: Whether to force re-indexing if document already exists.
    """

    document_id: str = Field(..., description="Document ID to index")
    force_reindex: bool = Field(default=False, description="Force re-indexing")


class IndexResponse(BaseModel):
    """Response model for indexing operation.
    
    Attributes:
        document_id: ID of the indexed document.
        chunks_indexed: Number of chunks indexed.
        status: Status message.
    """

    document_id: str = Field(..., description="Indexed document ID")
    chunks_indexed: int = Field(..., description="Number of chunks indexed", ge=0)
    status: str = Field(..., description="Indexing status message")

