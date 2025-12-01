# 🤖 LLM 통합 가이드

RAG-SPO에 LLM(Large Language Model)을 통합하여 실제 답변을 생성하는 방법을 설명합니다.

---

## ✅ 이미 완료된 것

```
✅ llm_utils.py를 사용한 LLM 통합 완료
✅ PwC GenAI Shared Service 지원
✅ 캐싱 기능 포함
✅ 데모 모드 / 실제 모드 구분
✅ 에러 처리 및 Fallback
```

---

## 🚀 LLM 사용 설정

### 1단계: 의존성 설치

```bash
cd backend
pip install langchain langchain-core langchain-openai
```

### 2단계: `.env` 파일 설정

`backend/.env` 파일에 다음 내용 추가:

```env
# 데모 모드 끄기 (LLM 사용)
DEMO_MODE=False

# LLM 설정
LLM_MODEL=gpt-4o

# API Key (필수!)
OPENAI_API_KEY=your-api-key-here

# PwC GenAI Shared Service URL
PWC_GENAI_BASE_URL=https://genai-sharedservice-americas.pwcinternal.com/v1

# Embedding 설정
EMBED_PROVIDER=openai
EMBEDDING_MODEL=azure.text-embedding-3-large

# 나머지 SharePoint 설정
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
SHAREPOINT_SITE_ID=your-site-id

# Qdrant 설정
QDRANT_MODE=local
QDRANT_PATH=./qdrant_data
QDRANT_COLLECTION_NAME=spo_docs
```

---

## 🧪 테스트하기

### 1. 검색 테스트 (CLI)

```bash
cd backend
python scripts/test_search.py
```

**대화형 모드:**
```
Query: 프로젝트 일정은?
```

**LLM이 정상 작동하면:**
```
[LLM] Loading LLM model...
[LLM] Generating answer...
[LLM] Generated answer (234 characters)

==================================================
ANSWER:
--------------------------------------------------
프로젝트는 2025년 1월부터 3월까지 진행됩니다.
주요 일정은 다음과 같습니다:
- 1월: 요구사항 분석 및 설계
- 2월: 개발 및 테스트
- 3월: 배포 및 운영
...
```

### 2. FastAPI 서버 테스트

```bash
cd backend
python -m app.main
```

**브라우저:**
```
http://localhost:8000/docs
```

**API 테스트:**
```bash
curl -X POST "http://localhost:8000/api/rag/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "프로젝트 일정은?",
    "top_k": 3
  }'
```

---

## 🎛️ LLM 파라미터 조정

`llm_utils.py`의 `load_llm_model` 함수는 다음 파라미터를 지원합니다:

```python
llm = load_llm_model(
    max_tokens=2000,      # 최대 토큰 수
    temperature=0.3,      # 창의성 (0.0-1.0)
    top_p=0.8,           # 샘플링 확률
    llm_model_name=None  # 모델명 (None이면 환경변수 사용)
)
```

### 파라미터 설명

| 파라미터 | 설명 | 추천값 |
|---------|------|--------|
| `max_tokens` | 생성할 최대 토큰 수 | 2000-4000 |
| `temperature` | 답변의 창의성/무작위성 | 0.3 (정확한 답변)<br>0.7 (창의적 답변) |
| `top_p` | 상위 확률 샘플링 | 0.8-0.95 |

---

## 🔧 문제 해결

### 문제 1: "OPENAI_API_KEY 환경변수가 설정되지 않았습니다"

**원인:** API 키가 `.env`에 없음

**해결:**
```bash
# .env 파일에 추가
OPENAI_API_KEY=your-actual-api-key
```

### 문제 2: "LLM 답변 생성 중 오류가 발생했습니다"

**원인:** API 호출 실패 또는 네트워크 문제

**해결:**
1. API 키 확인
2. 네트워크 연결 확인
3. PwC GenAI URL 확인
4. 로그 확인:
```bash
python scripts/test_search.py
# [ERROR] 메시지 확인
```

### 문제 3: "llm_utils not available"

**원인:** `llm_utils.py` 파일을 찾을 수 없음

**해결:**
```bash
# backend/ 디렉토리에 llm_utils.py가 있는지 확인
ls backend/llm_utils.py

# 없다면 프로젝트 루트에서 복사
cp llm_utils.py backend/
```

### 문제 4: 답변이 데모 모드로 나옴

**원인:** `.env`에서 `DEMO_MODE=True`로 설정됨

**해결:**
```env
DEMO_MODE=False  # 실제 모드로 변경
```

---

## 📊 모드 비교

| 모드 | DEMO_MODE | LLM 사용 | 답변 형태 |
|------|-----------|----------|----------|
| 데모 | True | ❌ | 템플릿 답변 |
| 실제 | False | ✅ | LLM 생성 답변 |

---

## 🎨 프롬프트 커스터마이징

`backend/app/rag/search.py`의 프롬프트를 수정하여 답변 스타일을 변경할 수 있습니다:

```python
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
```

**커스터마이징 예시:**

```python
# 더 간결한 답변
답변 가이드:
1. 핵심만 간결하게 답변하세요
2. 불릿 포인트를 사용하세요
3. 3-5문장으로 요약하세요

# 더 상세한 답변
답변 가이드:
1. 상세하게 설명하세요
2. 관련 배경 정보도 포함하세요
3. 예시를 들어 설명하세요
4. 단계별로 설명하세요
```

---

## 🔄 다른 LLM 모델 사용

### OpenAI GPT-4

```env
LLM_MODEL=gpt-4
OPENAI_API_KEY=sk-...
PWC_GENAI_BASE_URL=https://api.openai.com/v1
```

### OpenAI GPT-3.5-turbo (저렴함)

```env
LLM_MODEL=gpt-3.5-turbo
```

### PwC GenAI Bedrock Claude

```env
LLM_MODEL=bedrock.anthropic.claude-3-5-sonnet-v2
PWC_GENAI_BASE_URL=https://genai-sharedservice-americas.pwcinternal.com/v1
```

---

## 📈 성능 최적화

### 1. 캐싱 활용

`llm_utils.py`는 이미 모델 캐싱을 지원합니다. 같은 설정의 모델은 재사용됩니다.

### 2. 컨텍스트 길이 조정

```python
# search.py에서 top_k 값 조정
build_answer_with_sources(query, top_k=3)  # 적은 컨텍스트
build_answer_with_sources(query, top_k=10) # 많은 컨텍스트
```

**트레이드오프:**
- `top_k` 작음: 빠름, 정보 부족 가능
- `top_k` 큼: 느림, 정보 풍부

### 3. 배치 처리

여러 질문을 한 번에 처리할 때는 모델을 재사용하세요:

```python
from llm_utils import load_llm_model

# 한 번만 로드
llm = load_llm_model()

# 여러 질문 처리
for query in queries:
    response = llm.invoke(prompt)
```

---

## 🎯 전체 흐름

```
1. 사용자 질문 입력
   ↓
2. Qdrant 벡터 검색 (top_k개 문서 찾기)
   ↓
3. 검색된 문서들을 컨텍스트로 구성
   ↓
4. llm_utils.load_llm_model() 호출
   ↓
5. 프롬프트 + 컨텍스트를 LLM에 전달
   ↓
6. LLM이 답변 생성
   ↓
7. 답변 + 출처 반환
```

---

## ✨ 다음 단계

LLM이 정상 작동하면:

1. ✅ **실제 SharePoint 연동** (AZURE_SETUP.md 참고)
2. ✅ **임베딩 모델 실제 구현** (llm_utils.py의 load_embed_model 사용)
3. ✅ **프롬프트 최적화** (더 나은 답변을 위해)
4. ⬜ **스트리밍 응답** (실시간 답변 생성)
5. ⬜ **답변 품질 평가** (자동 평가 시스템)

---

## 📞 지원

문제가 있으면:
1. 로그 확인: `python scripts/test_search.py`
2. `.env` 파일 확인
3. API 키 유효성 확인
4. 이슈 제기 또는 문의

즐거운 개발 되세요! 🚀

