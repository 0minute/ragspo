"""LLM 모델 초기화 및 관련 유틸리티"""

import os
import threading
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings


# 환경 변수 로드
load_dotenv()

# 모델 캐시 및 스레드 안전성
_model_cache = {}
_cache_lock = threading.Lock()
_MAX_CACHE_SIZE = 10  # 최대 캐시 크기

def _get_cache_key(model_type: str, **kwargs) -> str:
    """캐시 키 생성"""
    key_parts = [model_type]
    for key, value in sorted(kwargs.items()):
        key_parts.append(f"{key}={value}")
    return "_".join(key_parts)


def _manage_cache_size():
    """캐시 크기 관리 (LRU 방식)"""
    if len(_model_cache) >= _MAX_CACHE_SIZE:
        # 가장 오래된 항목 하나 제거
        oldest_key = next(iter(_model_cache))
        del _model_cache[oldest_key]


def clear_model_cache():
    """모델 캐시 초기화 (선택적 사용)"""
    with _cache_lock:
        _model_cache.clear()


def load_llm_model(max_tokens=8096, temperature=0.3, top_p=0.8, llm_model_name='vertex_ai.gemini-2.5-pro'):
    """PwC GenAI Shared Service LLM 모델을 초기화합니다.

    Args:
        max_tokens: 최대 토큰 수
        temperature: 온도 파라미터
        top_p: 상위 확률 파라미터

    Returns:
        ChatOpenAI: 초기화된 LLM 모델
    """
    # PwC GenAI Shared Service 설정
    base_url = os.getenv("PWC_GENAI_BASE_URL", "https://genai-sharedservice-americas.pwcinternal.com/v1")
    api_key = os.getenv("OPENAI_API_KEY")
    if llm_model_name:
        model_name = llm_model_name
    else:
        model_name = os.getenv("LLM_MODEL")

    if not api_key:
        raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

    # 캐시 키 생성
    cache_key = _get_cache_key("llm", model_name=model_name, base_url=base_url, max_tokens=max_tokens, temperature=temperature, top_p=top_p)

    # 캐시에서 모델 확인
    with _cache_lock:
        if cache_key in _model_cache:
            return _model_cache[cache_key]

        # 캐시 크기 관리
        _manage_cache_size()

        # LLM 모델 초기화 (PwC GenAI 클라우드)
        llm = ChatOpenAI(model=model_name, openai_api_base=base_url, openai_api_key=api_key, max_tokens=max_tokens, temperature=temperature, top_p=top_p)

        # 캐시에 저장
        _model_cache[cache_key] = llm
        return llm


def load_ocr_model(max_tokens=8096, temperature=0.3, top_p=0.8, model=None):
    """PwC GenAI Shared Service OCR 모델을 초기화합니다.

    Args:
        max_tokens: 최대 토큰 수
        temperature: 온도 파라미터
        top_p: 상위 확률 파라미터
        model: 사용할 모델명 (None일 경우 환경변수에서 가져옴)

    Returns:
        ChatOpenAI: 초기화된 LLM 모델
    """
    # PwC GenAI Shared Service 설정
    base_url = os.getenv("PWC_GENAI_BASE_URL", "https://genai-sharedservice-americas.pwcinternal.com/v1")
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = model or os.getenv("OCR_MODEL", "bedrock.anthropic.claude-3-5-sonnet-v2")

    if not api_key:
        raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

    # 캐시 키 생성
    cache_key = _get_cache_key("ocr", model_name=model_name, base_url=base_url, max_tokens=max_tokens, temperature=temperature, top_p=top_p)

    # 캐시에서 모델 확인
    with _cache_lock:
        if cache_key in _model_cache:
            return _model_cache[cache_key]

        # 캐시 크기 관리
        _manage_cache_size()

        # LLM 모델 초기화 (PwC GenAI 클라우드)
        llm = ChatOpenAI(model=model_name, openai_api_base=base_url, openai_api_key=api_key, max_tokens=max_tokens, temperature=temperature, top_p=top_p)

        # 캐시에 저장
        _model_cache[cache_key] = llm
        return llm


def load_embed_model(model_name: str = None):
    """
    BGE-M3 또는 OpenAI를 선택하여 임베딩 모델을 로드.
    GPU(CUDA) 자동 사용 지원.
    """

    provider = os.getenv("EMBED_PROVIDER", "openai").lower()

    print("[load_embed_model] Using OpenAI embedding")
    base_url = os.getenv("PWC_GENAI_BASE_URL", "https://genai-sharedservice-americas.pwcinternal.com/v1")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 없습니다.")
    model_name = model_name or os.getenv("EMBEDDING_MODEL", "azure.text-embedding-3-large")
    return OpenAIEmbeddings(model=model_name, openai_api_base=base_url, openai_api_key=api_key)

