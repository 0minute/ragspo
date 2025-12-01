"""SharePoint client module for Microsoft Graph API integration.

This module provides functions to interact with SharePoint Online via Microsoft Graph API.
"""

from typing import Any, Dict, List, Optional

import requests

from app.config import get_settings


def get_access_token() -> str:
    """Obtain an access token for Microsoft Graph API.
    
    Returns:
        str: Access token for authenticating Microsoft Graph API requests.
        
    Raises:
        Exception: If authentication fails.
        
    Note:
        Uses OAuth2 client credentials flow for app-only authentication.
        Token should be cached for better performance (TODO: implement caching).
    """
    settings = get_settings()
    
    # Demo mode: return dummy token
    if settings.demo_mode:
        print("[DEMO MODE] Using dummy access token")
        return "dummy_access_token"
    
    # Real implementation: OAuth2 client credentials flow
    token_url = f"https://login.microsoftonline.com/{settings.tenant_id}/oauth2/v2.0/token"
    
    data = {
        "client_id": settings.client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": settings.client_secret,
        "grant_type": "client_credentials",
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token = response.json()["access_token"]
        print("[Graph API] Access token obtained successfully")
        return token
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get access token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"[ERROR] Response: {e.response.text}")
        raise Exception(f"Authentication failed: {e}")


def list_sharepoint_documents(site_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all documents from a SharePoint site.
    
    Args:
        site_id: SharePoint site identifier. If None, uses default from settings.
        
    Returns:
        List of document metadata dictionaries containing file information.
        
    TODO:
        - Implement Microsoft Graph API call to list documents
        - Handle pagination for large document libraries
        - Add filtering options (by date, file type, etc.)
        - Include document metadata (title, author, modified date, etc.)
    """
    settings = get_settings()
    token = get_access_token()
    
    if site_id is None:
        site_id = settings.sharepoint_site_id
    
    # Demo mode: return rich dummy data
    if settings.demo_mode:
        print("[DEMO MODE] Returning sample documents")
        return [
            {
                "id": "doc_demo_1",
                "name": "프로젝트_계획서.docx",
                "web_url": "https://demo.sharepoint.com/sites/demo/프로젝트_계획서.docx",
                "size": 45678,
            },
            {
                "id": "doc_demo_2",
                "name": "기술_문서.pdf",
                "web_url": "https://demo.sharepoint.com/sites/demo/기술_문서.pdf",
                "size": 123456,
            },
            {
                "id": "doc_demo_3",
                "name": "회의록_2025.txt",
                "web_url": "https://demo.sharepoint.com/sites/demo/회의록_2025.txt",
                "size": 8901,
            },
        ]
    
    # Real implementation: Graph API call to list documents
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    
    try:
        # Get the default document library (drive) for the site
        drive_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive"
        drive_response = requests.get(drive_url, headers=headers)
        drive_response.raise_for_status()
        drive_id = drive_response.json()["id"]
        
        print(f"[Graph API] Found drive: {drive_id}")
        
        # List all items in the root of the document library
        items_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
        items_response = requests.get(items_url, headers=headers)
        items_response.raise_for_status()
        
        items = items_response.json().get("value", [])
        
        # Filter only files (not folders)
        documents = []
        for item in items:
            if "file" in item:  # It's a file, not a folder
                documents.append({
                    "id": item["id"],
                    "name": item["name"],
                    "web_url": item.get("webUrl", ""),
                    "size": item.get("size", 0),
                    "download_url": item.get("@microsoft.graph.downloadUrl", ""),
                })
        
        print(f"[Graph API] Found {len(documents)} documents")
        return documents
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to list documents: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"[ERROR] Response: {e.response.text}")
        raise Exception(f"Failed to list SharePoint documents: {e}")


def get_document_content(document_id: str) -> str:
    """Retrieve the text content of a SharePoint document.
    
    Args:
        document_id: Unique identifier of the document.
        
    Returns:
        str: Text content extracted from the document.
        
    TODO:
        - Implement Graph API call to download document
        - Add support for different file formats (docx, pdf, txt, etc.)
        - Implement text extraction logic for binary formats
        - Handle large documents efficiently
        - Add error handling for inaccessible documents
    """
    settings = get_settings()
    token = get_access_token()
    
    # Demo mode: return realistic sample content
    if settings.demo_mode:
        print(f"[DEMO MODE] Returning sample content for {document_id}")
        demo_contents = {
            "doc_demo_1": """
프로젝트 계획서

1. 프로젝트 개요
본 프로젝트는 SharePoint Online 문서를 기반으로 한 RAG(Retrieval-Augmented Generation) 시스템을 구축하는 것을 목표로 합니다.

2. 프로젝트 일정
- 2025년 1월: 요구사항 분석 및 설계
- 2025년 2월: 개발 및 테스트
- 2025년 3월: 배포 및 운영

3. 주요 기능
- 문서 자동 인덱싱
- 자연어 기반 검색
- AI 기반 답변 생성

4. 기대 효과
직원들이 필요한 정보를 빠르게 찾을 수 있어 업무 효율성이 30% 향상될 것으로 예상됩니다.
            """,
            "doc_demo_2": """
기술 문서

시스템 아키텍처

1. 백엔드 구조
- FastAPI를 사용한 RESTful API
- Qdrant 벡터 데이터베이스
- Microsoft Graph API 연동

2. 데이터 파이프라인
문서 수집 → 전처리 → 청킹 → 임베딩 → 벡터 DB 저장

3. 검색 프로세스
사용자 질의 → 임베딩 변환 → 벡터 유사도 검색 → LLM 답변 생성

4. 보안 고려사항
- OAuth 2.0 인증
- 역할 기반 접근 제어(RBAC)
- 데이터 암호화
            """,
            "doc_demo_3": """
회의록 2025-01-15

참석자: 김철수, 이영희, 박민수

안건:
1. RAG 시스템 개발 현황 공유
   - 백엔드 스캐폴딩 완료
   - 벡터 DB 설정 완료
   - Graph API 연동 준비 중

2. 다음 주 목표
   - 임베딩 모델 선정 및 구현
   - SharePoint 크롤러 개발
   - 초기 테스트 데이터 수집

3. 이슈 및 해결 방안
   - Azure AD 앱 등록 권한 문제 → Developer Program 활용
   - 토큰 만료 처리 → 캐싱 및 자동 갱신 로직 추가

다음 회의: 2025-01-22
            """,
        }
        
        return demo_contents.get(document_id, f"[DEMO] 샘플 콘텐츠 for {document_id}")
    
    # Real implementation: Download and extract text from document
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    try:
        # Get document metadata including download URL
        metadata_url = f"https://graph.microsoft.com/v1.0/sites/{settings.sharepoint_site_id}/drive/items/{document_id}"
        metadata_response = requests.get(metadata_url, headers=headers)
        metadata_response.raise_for_status()
        
        download_url = metadata_response.json().get("@microsoft.graph.downloadUrl")
        
        if not download_url:
            raise Exception(f"No download URL available for document {document_id}")
        
        # Download the file content
        print(f"[Graph API] Downloading document {document_id}...")
        file_response = requests.get(download_url)
        file_response.raise_for_status()
        
        # TODO: Implement proper text extraction based on file type
        # For now, return raw content as text (works for .txt files)
        # For production, add support for .docx, .pdf, etc. using libraries like:
        # - python-docx for Word documents
        # - PyPDF2 or pdfplumber for PDFs
        # - beautifulsoup4 for HTML
        
        content = file_response.text
        print(f"[Graph API] Downloaded {len(content)} characters")
        return content
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get document content: {e}")
        raise Exception(f"Failed to download document {document_id}: {e}")


def get_document_metadata(document_id: str) -> Dict[str, Any]:
    """Retrieve metadata for a SharePoint document.
    
    Args:
        document_id: Unique identifier of the document.
        
    Returns:
        Dict containing document metadata (name, url, modified date, author, etc.).
        
    TODO:
        - Implement Graph API call to get document metadata
        - Include all relevant metadata fields
    """
    settings = get_settings()
    token = get_access_token()
    
    # Demo mode: return realistic metadata
    if settings.demo_mode:
        demo_metadata = {
            "doc_demo_1": {
                "id": "doc_demo_1",
                "name": "프로젝트_계획서.docx",
                "web_url": "https://demo.sharepoint.com/sites/demo/프로젝트_계획서.docx",
                "download_url": "https://demo.sharepoint.com/download/doc_demo_1",
                "modified_date": "2025-01-15T09:30:00Z",
                "author": "김철수",
            },
            "doc_demo_2": {
                "id": "doc_demo_2",
                "name": "기술_문서.pdf",
                "web_url": "https://demo.sharepoint.com/sites/demo/기술_문서.pdf",
                "download_url": "https://demo.sharepoint.com/download/doc_demo_2",
                "modified_date": "2025-01-20T14:15:00Z",
                "author": "이영희",
            },
            "doc_demo_3": {
                "id": "doc_demo_3",
                "name": "회의록_2025.txt",
                "web_url": "https://demo.sharepoint.com/sites/demo/회의록_2025.txt",
                "download_url": "https://demo.sharepoint.com/download/doc_demo_3",
                "modified_date": "2025-01-15T16:00:00Z",
                "author": "박민수",
            },
        }
        
        return demo_metadata.get(document_id, {
            "id": document_id,
            "name": f"demo_{document_id}.docx",
            "web_url": f"https://demo.sharepoint.com/sites/demo/{document_id}",
            "download_url": f"https://demo.sharepoint.com/download/{document_id}",
            "modified_date": "2025-11-30T00:00:00Z",
            "author": "Demo User",
        })
    
    # Real implementation: Get document metadata from Graph API
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    
    try:
        metadata_url = f"https://graph.microsoft.com/v1.0/sites/{settings.sharepoint_site_id}/drive/items/{document_id}"
        response = requests.get(metadata_url, headers=headers)
        response.raise_for_status()
        
        item = response.json()
        
        return {
            "id": item["id"],
            "name": item["name"],
            "web_url": item.get("webUrl", ""),
            "download_url": item.get("@microsoft.graph.downloadUrl", ""),
            "modified_date": item.get("lastModifiedDateTime", ""),
            "author": item.get("createdBy", {}).get("user", {}).get("displayName", "Unknown"),
            "size": item.get("size", 0),
        }
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get document metadata: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"[ERROR] Response: {e.response.text}")
        raise Exception(f"Failed to get metadata for document {document_id}: {e}")

