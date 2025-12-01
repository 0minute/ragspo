"""Script to index SharePoint documents into Qdrant.

This script can be run from the command line to index all SharePoint documents
or specific documents by ID.
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Optional

from app.qdrant_client import ensure_collection_exists
from app.rag.indexer import index_all_sharepoint_documents, index_sharepoint_document


def main(document_id: Optional[str] = None) -> None:
    """Run the indexing process.
    
    Args:
        document_id: Optional document ID to index. If None, indexes all documents.
    """
    print("=" * 60)
    print("RAG-SPO Document Indexing Script")
    print("=" * 60)
    
    # Ensure Qdrant collection exists
    print("\nEnsuring Qdrant collection exists...")
    try:
        ensure_collection_exists()
        print("✓ Qdrant collection is ready")
    except Exception as e:
        print(f"✗ Error setting up Qdrant collection: {e}")
        sys.exit(1)
    
    # Index documents
    try:
        if document_id:
            print(f"\nIndexing specific document: {document_id}")
            result = index_sharepoint_document(document_id)
            print(f"✓ Indexed {result['chunks_indexed']} chunks from document {document_id}")
        else:
            print("\nIndexing all SharePoint documents...")
            result = index_all_sharepoint_documents()
            print(f"✓ Indexed {result['total_documents']} documents with {result['total_chunks']} total chunks")
    except Exception as e:
        print(f"✗ Error during indexing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Indexing completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    # Parse command line arguments
    doc_id = None
    if len(sys.argv) > 1:
        doc_id = sys.argv[1]
        print(f"Document ID provided: {doc_id}")
    
    main(document_id=doc_id)

