"""RAG API routes for document search and indexing.

This module defines the FastAPI routes for RAG operations.
"""

from typing import Dict
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
import io

from app.rag.indexer import index_sharepoint_document, index_all_sharepoint_documents
from app.rag.schemas import (
    IndexRequest,
    IndexResponse,
    SearchRequest,
    SearchResponse,
    IndexAllRequest,
    IndexAllResponse,
)
from app.rag.search import build_answer_with_sources
from app.sharepoint_client import get_document_metadata, get_access_token
from app.config import get_settings
import requests

router = APIRouter(prefix="/api/rag", tags=["RAG"])


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest) -> SearchResponse:
    """Search for relevant documents and generate an answer.
    
    Args:
        request: SearchRequest containing the query and parameters.
        
    Returns:
        SearchResponse with generated answer and source citations.
        
    Raises:
        HTTPException: If search fails.
    """
    try:
        response = build_answer_with_sources(
            query=request.query,
            top_k=request.top_k,
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )


@router.post("/index", response_model=IndexResponse)
async def index_document(request: IndexRequest) -> IndexResponse:
    """Index a SharePoint document into the vector database.
    
    Args:
        request: IndexRequest containing the document ID to index.
        
    Returns:
        IndexResponse with indexing statistics.
        
    Raises:
        HTTPException: If indexing fails.
    """
    try:
        result = index_sharepoint_document(request.document_id)
        
        return IndexResponse(
            document_id=result["document_id"],
            chunks_indexed=result["chunks_indexed"],
            status="success",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Indexing failed: {str(e)}",
        )


@router.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint for the RAG service.
    
    Returns:
        Dictionary with status message.
    """
    return {"status": "healthy", "service": "rag"}


@router.post("/index-all", response_model=IndexAllResponse)
async def index_all_documents(request: IndexAllRequest) -> IndexAllResponse:
    """Index all SharePoint documents into the vector database.

    This endpoint can optionally override the SharePoint site ID used
    for indexing. If ``site_id`` is provided in the request, it will be
    used for this indexing run; otherwise the backend configuration
    (``SHAREPOINT_SITE_ID``) is used.

    Args:
        request: IndexAllRequest containing an optional site ID.

    Returns:
        IndexAllResponse with aggregated indexing statistics.

    Raises:
        HTTPException: If indexing fails.
    """
    from app.qdrant_client import ensure_collection_exists
    import os

    settings = get_settings()

    try:
        # Ensure Qdrant collection exists
        ensure_collection_exists()

        effective_site_id = request.site_id or settings.sharepoint_site_id

        # If site_id is provided, update environment so subsequent calls
        # use the same site without requiring a restart.
        if request.site_id:
            os.environ["SHAREPOINT_SITE_ID"] = request.site_id
            print(f"[IndexAll] Using custom SHAREPOINT_SITE_ID: {request.site_id}")

        result = index_all_sharepoint_documents(site_id=effective_site_id)

        return IndexAllResponse(
            total_documents=result["total_documents"],
            total_chunks=result["total_chunks"],
            site_id=effective_site_id,
            status="success",
        )
    except Exception as e:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Index-all failed: {str(e)}",
        )


@router.get("/download/{document_id}")
async def download_document(document_id: str):
    """Download a SharePoint document.
    
    Args:
        document_id: The unique identifier of the document to download.
        
    Returns:
        StreamingResponse: The file content as a streaming response.
        
    Raises:
        HTTPException: If download fails.
        
    Examples:
        GET /api/rag/download/doc_demo_1
    """
    settings = get_settings()
    
    try:
        # Demo mode: return demo message
        if settings.demo_mode:
            demo_content = f"[데모 모드]\n\n이것은 '{document_id}' 문서의 데모 다운로드입니다.\n\n실제 다운로드를 위해서는:\n1. DEMO_MODE=False\n2. SharePoint 연동 필요"
            demo_filename = f"demo_{document_id}.txt"
            
            # UTF-8 인코딩된 파일명 (RFC 5987)
            encoded_filename = quote(demo_filename, safe='')
            
            return StreamingResponse(
                io.BytesIO(demo_content.encode('utf-8')),
                media_type="text/plain; charset=utf-8",
                headers={
                    "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
                }
            )
        
        # Get document metadata
        metadata = get_document_metadata(document_id)
        download_url = metadata.get("download_url")
        file_name = metadata.get("name", f"{document_id}.bin")
        
        if not download_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Download URL not found for document {document_id}"
            )
        
        # Download file from SharePoint
        print(f"[Download] Downloading {file_name} from SharePoint...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Determine content type
        content_type = response.headers.get('content-type', 'application/octet-stream')
        
        # UTF-8 인코딩된 파일명 (RFC 5987)
        # 한글 파일명 지원을 위해 URL 인코딩
        encoded_filename = quote(file_name, safe='')
        
        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(response.content),
            media_type=content_type,
            headers={
                # RFC 5987: UTF-8 파일명 인코딩
                # filename*=UTF-8''encoded_filename 형식
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
                # 레거시 브라우저를 위한 ASCII 파일명 (선택적)
                # "Content-Disposition": f"attachment; filename=\"{file_name}\"; filename*=UTF-8''{encoded_filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Download failed: {str(e)}"
        )


@router.get("/document/{document_id}/info")
async def get_document_info(document_id: str) -> Dict:
    """Get metadata information for a SharePoint document.
    
    Args:
        document_id: The unique identifier of the document.
        
    Returns:
        Dictionary containing document metadata.
        
    Raises:
        HTTPException: If retrieval fails.
        
    Examples:
        GET /api/rag/document/doc_demo_1/info
    """
    settings = get_settings()
    
    try:
        # Demo mode: return demo metadata
        if settings.demo_mode:
            return {
                "id": document_id,
                "name": f"demo_{document_id}.txt",
                "size": 1234,
                "web_url": f"https://demo.sharepoint.com/{document_id}",
                "download_url": f"/api/rag/download/{document_id}",
                "modified_date": "2025-11-30T00:00:00Z",
                "author": "Demo User",
                "mode": "demo"
            }
        
        # Get real metadata
        metadata = get_document_metadata(document_id)
        
        # Add internal download endpoint
        metadata["internal_download_url"] = f"/api/rag/download/{document_id}"
        
        return metadata
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get document info: {str(e)}"
        )

