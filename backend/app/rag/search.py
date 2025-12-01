"""Document search module for querying indexed SPO documents.

This module provides functions to search the vector database and generate
answers based on retrieved documents.
"""

import sys
from pathlib import Path
from typing import List

# Add backend directory to path for llm_utils import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.config import get_settings
from app.embeddings import embed_query
from app.qdrant_client import get_qdrant_client
from app.rag.schemas import SearchResponse, Source

try:
    from llm_utils import load_llm_model
    LLM_AVAILABLE = True
except ImportError:
    print("[Warning] llm_utils not available. LLM features will be disabled.")
    LLM_AVAILABLE = False


def search_spo_docs(query: str, top_k: int = 5) -> List[dict]:
    """Search for relevant document chunks in Qdrant.
    
    Args:
        query: The search query string.
        top_k: Number of top results to return.
        
    Returns:
        List of dictionaries containing search results with scores and payloads.
        Each result contains:
        - 'id': Unique ID of the chunk
        - 'score': Similarity score
        - 'payload': Document metadata and text
        
    Examples:
        >>> results = search_spo_docs("What is the project timeline?", top_k=3)
        >>> len(results)
        3
        >>> results[0]['payload']['text']
        'The project timeline spans 6 months...'
    """
    settings = get_settings()
    client = get_qdrant_client()
    
    # Generate embedding for the query
    print(f"Embedding query: {query}")
    query_vector = embed_query(query)
    
    # Search in Qdrant
    print(f"Searching in collection: {settings.qdrant_collection_name}")
    query_response = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=top_k,
    )
    search_results = query_response.points
    
    # Convert search results to list of dicts
    results = []
    for result in search_results:
        results.append({
            "id": result.id,
            "score": result.score,
            "payload": result.payload,
        })
    
    return results


def build_answer_with_sources(query: str, top_k: int = 5) -> SearchResponse:
    """Build an answer with source citations based on search results.
    
    This function:
    1. Searches for relevant document chunks
    2. Generates an answer using retrieved context (TODO: LLM integration)
    3. Extracts source information from search results
    
    Args:
        query: The search query string.
        top_k: Number of top results to retrieve.
        
    Returns:
        SearchResponse containing the answer and source citations.
        
    TODO:
        - Implement LLM integration for answer generation (OpenAI, Anthropic, etc.)
        - Add context window management for LLM
        - Implement prompt engineering for better answers
        - Add answer quality validation
        - Consider streaming responses for better UX
    """
    # Step 1: Search for relevant chunks
    search_results = search_spo_docs(query, top_k)
    
    # Step 2: Extract sources from search results
    sources: List[Source] = []
    context_chunks: List[str] = []
    
    for result in search_results:
        payload = result["payload"]
        
        # Extract source information
        document_id = payload.get("document_id", "")
        source = Source(
            file_title=payload.get("document_name", "Unknown"),
            section_title="",  # Could be enhanced with section detection
            chunk_index=payload.get("chunk_index", 0),
            download_url=payload.get("sharepoint", {}).get("web_url", ""),
            document_id=document_id,
            score=result["score"],
        )
        sources.append(source)
        
        # Collect context for answer generation
        context_chunks.append(payload.get("text", ""))
    
    # Step 3: Generate answer using LLM
    settings = get_settings()
    
    if not search_results:
        answer = "관련된 문서를 찾을 수 없습니다. 다른 키워드로 검색해보세요."
    elif settings.demo_mode:
        # Demo mode: return template answer
        answer = (
            f"[데모 모드] '{query}' 질문에 대해 {len(search_results)}개의 관련 문서를 찾았습니다.\n\n"
            f"가장 관련성 높은 문서: '{sources[0].file_title}'\n\n"
            f"실제 LLM 답변을 받으려면:\n"
            f"1. .env에서 DEMO_MODE=False 설정\n"
            f"2. OPENAI_API_KEY 입력\n"
            f"3. PWC_GENAI_BASE_URL 설정 (PwC GenAI 사용 시)"
        )
    elif not LLM_AVAILABLE:
        answer = (
            f"LLM 기능을 사용할 수 없습니다. llm_utils.py를 확인해주세요.\n\n"
            f"{len(search_results)}개의 관련 문서를 찾았습니다."
        )
    else:
        # Real mode: use LLM to generate answer
        # try:
        if True:
            print("[LLM] Loading LLM model...")
            llm = load_llm_model(
            )
            
            # Build context from chunks
            context = "\n\n".join([
                f"[문서 {i+1}: {sources[i].file_title}]\n{chunk}" 
                for i, chunk in enumerate(context_chunks)
            ])
            
            # Create prompt
            prompt = f"""당신은 SharePoint 문서를 기반으로 질문에 답변하는 AI 어시스턴트입니다.

아래 문서들을 참고하여 사용자의 질문에 정확하고 자세하게 답변해주세요.
문서에 없는 내용은 추측하지 말고, 문서 기반으로만 답변하세요.

<문서 내용>
{context}
</문서 내용>

<질문>
{query}
</질문>

<답변 가이드>
1. 문서의 내용을 기반으로 답변하세요
2. 가능한 구체적으로 답변하세요
3. 문서에 정보가 부족하면 그렇게 말씀하세요
4. 한국어로 답변하세요

답변:"""

            print("[LLM] Generating answer...")
            response = llm.invoke(prompt)
            answer = response.content
            print(f"[LLM] Generated answer ({len(answer)} characters)")
            
        # except Exception as e:
        else:
            print(f"[ERROR] LLM generation failed: {e}")
            # Fallback to simple answer
            answer = (
                f"LLM 답변 생성 중 오류가 발생했습니다: {str(e)}\n\n"
                f"'{query}' 질문에 대해 {len(search_results)}개의 관련 문서를 찾았습니다.\n"
                f"관련 문서를 확인해주세요."
            )
    
    return SearchResponse(
        answer=answer,
        sources=sources,
        query=query,
    )

