"""Embeddings module for text vectorization.

This module provides functions to convert text into vector embeddings.

It is wired to use the shared ``llm_utils.load_embed_model`` utility, which
handles provider selection and model caching based on environment variables.
"""

from typing import List

from llm_utils import load_embed_model


_EMBEDDING_MODEL = None


def _get_embedding_model():
    """Get or initialize the shared embedding model instance.

    The underlying ``load_embed_model`` function already implements
    its own caching, but we keep a local reference to avoid repeated
    lookups and to make call sites simpler.

    Returns:
        Embedding model instance with ``embed_documents`` and ``embed_query`` methods.
    """
    global _EMBEDDING_MODEL

    if _EMBEDDING_MODEL is None:
        print("[Embeddings] Initializing embedding model via llm_utils.load_embed_model()")
        _EMBEDDING_MODEL = load_embed_model()

    return _EMBEDDING_MODEL


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Convert a list of text strings into vector embeddings.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors, where each vector is a list of floats.
    """
    if not texts:
        return []

    model = _get_embedding_model()

    try:
        embeddings = model.embed_documents(texts)
        print(f"[Embeddings] Generated embeddings for {len(texts)} texts")
        return embeddings
    except Exception as exc:  # pragma: no cover - defensive
        print(f"[ERROR] Failed to generate embeddings: {exc}")
        raise


def embed_query(query: str) -> List[float]:
    """Convert a single query string into a vector embedding.

    Args:
        query: Query text string to embed.

    Returns:
        Embedding vector as a list of floats.
    """
    model = _get_embedding_model()

    try:
        embedding = model.embed_query(query)
        print("[Embeddings] Generated embedding for query")
        return embedding
    except Exception as exc:  # pragma: no cover - defensive
        print(f"[ERROR] Failed to generate query embedding: {exc}")
        raise

