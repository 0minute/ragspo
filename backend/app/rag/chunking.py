"""Text chunking module for splitting documents into smaller pieces.

This module provides functions to split text documents into overlapping chunks
for better embedding and retrieval performance.
"""

from typing import List


def split_into_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[str]:
    """Split text into overlapping chunks.
    
    Args:
        text: The text content to split into chunks.
        chunk_size: Maximum size of each chunk in characters.
        chunk_overlap: Number of overlapping characters between consecutive chunks.
        
    Returns:
        List of text chunks.
        
    Note:
        This is a simple character-based chunking implementation.
        Consider using more sophisticated chunking strategies for production:
        - Sentence-aware chunking
        - Paragraph-aware chunking
        - Semantic chunking using embeddings
        
    Examples:
        >>> text = "This is a long document that needs to be split..."
        >>> chunks = split_into_chunks(text, chunk_size=100, chunk_overlap=20)
        >>> len(chunks)
        5
    """
    if not text or chunk_size <= 0:
        return []
    
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Define the end of the current chunk
        end = start + chunk_size
        
        # Extract the chunk
        chunk = text[start:end]
        
        # Add non-empty chunks
        if chunk.strip():
            chunks.append(chunk)
        
        # Move to the next chunk with overlap
        start = end - chunk_overlap
        
        # Prevent infinite loop if we're at the end
        if end >= len(text):
            break
    
    return chunks


def split_document_with_metadata(
    text: str,
    document_id: str,
    document_name: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[dict]:
    """Split document into chunks with metadata.
    
    Args:
        text: The text content to split.
        document_id: Unique identifier for the document.
        document_name: Name of the document.
        chunk_size: Maximum size of each chunk in characters.
        chunk_overlap: Number of overlapping characters between consecutive chunks.
        
    Returns:
        List of dictionaries containing chunk text and metadata.
        Each dictionary has keys: 'text', 'document_id', 'document_name', 'chunk_index'.
        
    Examples:
        >>> chunks = split_document_with_metadata(
        ...     text="Long document...",
        ...     document_id="doc_123",
        ...     document_name="example.docx",
        ... )
        >>> chunks[0]['chunk_index']
        0
    """
    text_chunks = split_into_chunks(text, chunk_size, chunk_overlap)
    
    chunks_with_metadata = []
    for idx, chunk_text in enumerate(text_chunks):
        chunks_with_metadata.append({
            "text": chunk_text,
            "document_id": document_id,
            "document_name": document_name,
            "chunk_index": idx,
        })
    
    return chunks_with_metadata

