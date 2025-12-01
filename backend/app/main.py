"""Main FastAPI application module for RAG-SPO backend.

This module initializes and configures the FastAPI application.
"""

from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import rag_routes

# Create FastAPI app instance
app = FastAPI(
    title="RAG-SPO API",
    description="SharePoint Online document RAG backend with Qdrant vector search",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rag_routes.router)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint.
    
    Returns:
        Welcome message.
    """
    return {
        "message": "RAG-SPO API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Health status.
    """
    return {"status": "healthy"}


# Startup event
@app.on_event("startup")
async def startup_event() -> None:
    """Initialize services on application startup.
    
    This function runs when the application starts up.
    """
    print("Starting RAG-SPO API...")
    
    # Ensure Qdrant collection exists
    try:
        from app.qdrant_client import ensure_collection_exists
        ensure_collection_exists()
        print("Qdrant collection verified")
    except Exception as e:
        print(f"Warning: Could not verify Qdrant collection: {e}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Cleanup on application shutdown.
    
    This function runs when the application shuts down.
    """
    print("Shutting down RAG-SPO API...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

