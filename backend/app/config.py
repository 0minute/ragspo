"""Configuration module for RAG-SPO application.

This module provides configuration management using Pydantic BaseSettings.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        tenant_id: Azure AD tenant ID for Microsoft Graph API authentication.
        client_id: Application (client) ID for Microsoft Graph API.
        client_secret: Client secret for Microsoft Graph API authentication.
        sharepoint_site_id: SharePoint site identifier.
        qdrant_host: Qdrant vector database host address.
        qdrant_port: Qdrant vector database port number.
        qdrant_collection_name: Name of the Qdrant collection for SPO documents.
        embedding_model: Name or identifier of the embedding model to use.
        chunk_size: Maximum size of text chunks in characters.
        chunk_overlap: Overlap size between consecutive chunks.
    """

    # Demo mode (set to True to use dummy data without real SharePoint)
    demo_mode: bool = False

    # SharePoint / Microsoft Graph API settings
    tenant_id: str = "demo-tenant-id"
    client_id: str = "demo-client-id"
    client_secret: str = "demo-client-secret"
    sharepoint_site_id: Optional[str] = None

    # Qdrant settings
    qdrant_mode: str = "local"  # "local" or "server"
    qdrant_path: str = "./qdrant_data"  # Local storage path (used when mode=local)
    qdrant_host: str = "localhost"  # Server host (used when mode=server)
    qdrant_port: int = 6333  # Server port (used when mode=server)
    qdrant_collection_name: str = "spo_docs"

    # Embedding settings
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536

    # Chunking settings
    chunk_size: int = 1000
    chunk_overlap: int = 200

    openai_api_key: str = "demo_openai_api_key"
    llm_model: str = "demo_llm_model"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="allow"  # .env의 모든 필드 허용
    )


def get_settings() -> Settings:
    """Get application settings instance.
    
    Returns:
        Settings: Application settings loaded from environment variables.
    """
    return Settings()

