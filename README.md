# RAG-SPO

SharePoint Online (SPO) 문서 기반 RAG (Retrieval-Augmented Generation) 백엔드

## 📋 개요

이 프로젝트는 SharePoint Online의 문서를 크롤링하여 벡터 데이터베이스에 인덱싱하고, 자연어 질문에 대해 관련 문서를 검색하여 답변을 생성하는 RAG 시스템입니다.

### 주요 기능

- ✅ SharePoint Online 문서 크롤링 (Microsoft Graph API)
- ✅ 문서 청크 분할 및 임베딩
- ✅ Qdrant 벡터 데이터베이스 인덱싱
- ✅ 자연어 기반 문서 검색
- ✅ 소스 문서 다운로드 URL 제공
- 🚧 LLM 기반 답변 생성 (TODO)

## 🏗️ 프로젝트 구조

```
rag-spo/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI 앱 진입점
│   │   ├── config.py               # 설정 관리
│   │   ├── embeddings.py           # 임베딩 생성
│   │   ├── qdrant_client.py        # Qdrant 클라이언트
│   │   ├── sharepoint_client.py    # SharePoint/Graph API 클라이언트
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── rag_routes.py       # RAG API 라우트
│   │   └── rag/
│   │       ├── __init__.py
│   │       ├── chunking.py         # 텍스트 청킹
│   │       ├── indexer.py          # 문서 인덱싱
│   │       ├── search.py           # 검색 및 답변 생성
│   │       └── schemas.py          # Pydantic 스키마
│   ├── scripts/
│   │   ├── run_indexing.py         # 인덱싱 스크립트
│   │   └── test_search.py          # 검색 테스트 스크립트
│   └── requirements.txt
├── .env                            # 환경 변수 (gitignore)
└── README.md
```

## 🎨 프론트엔드 (새로 추가!)

간단한 웹 UI로 검색, 답변 확인, 다운로드를 바로 사용할 수 있습니다!

```bash
# 1. 백엔드 서버 실행
cd backend
python -m app.main

# 2. 프론트엔드 열기 (새 터미널)
cd frontend
python -m http.server 8080

# 3. 브라우저 접속
# http://localhost:8080
```

👉 **상세 가이드: [frontend/README.md](frontend/README.md)**

**주요 기능:**
- 🔍 자연어 검색
- 💬 AI 답변 표시
- 📥 원클릭 다운로드
- 🎨 깔끔한 UI
- 📱 모바일 지원

---

## 🚀 시작하기

### ⚡ 빠른 시작 (Azure 없이 테스트!)

Azure AD 앱 등록 권한이 없나요? **데모 모드**로 즉시 시작하세요!

👉 **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - 5분 안에 시작하기

### 1. 사전 요구사항

#### 데모 모드 (추천!)
- ✅ Python 3.10+
- ✅ Qdrant (로컬 Docker)
- ✅ Azure 계정 불필요!

#### 실제 SharePoint 연동
- Python 3.10+
- Qdrant (로컬 또는 클라우드)
- Microsoft Azure AD 앱 등록 (Graph API 액세스용)
  - 권한 없으면? 👉 **[AZURE_SETUP.md](AZURE_SETUP.md)** - 무료 개발자 계정 만들기

### 2. Qdrant 설치 및 실행

#### 옵션 A: Local 모드 (Docker 불필요! ⭐ 추천)

**가장 간단한 방법 - 설정만으로 완료:**

```bash
# .env 파일에서 다음 설정:
QDRANT_MODE=local
QDRANT_PATH=./qdrant_data
```

데이터는 `backend/qdrant_data/` 폴더에 자동 저장됩니다!

👉 **상세 가이드: [NO_DOCKER_GUIDE.md](NO_DOCKER_GUIDE.md)**

#### 옵션 B: Server 모드 (Docker)

Docker를 사용한 서버 실행:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

```bash
# .env 파일에서:
QDRANT_MODE=server
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

#### 옵션 C: Qdrant Cloud

https://cloud.qdrant.io/ 사용

### 3. 환경 설정

#### 옵션 A: 데모 모드 (추천!)

```bash
cd backend
cp env.example .env
```

`.env` 파일에서 **DEMO_MODE=True**로 설정:

```env
# 데모 모드 활성화!
DEMO_MODE=True

# 아래 값들은 데모 모드에서 무시됨
TENANT_ID=demo-tenant-id
CLIENT_ID=demo-client-id
CLIENT_SECRET=demo-client-secret
# ... 나머지 설정은 그대로
```

#### 옵션 B: 실제 SharePoint 연동

1. Azure AD 앱 등록: **[AZURE_SETUP.md](AZURE_SETUP.md)** 참고
2. `.env` 파일 설정:

```env
# 데모 모드 비활성화
DEMO_MODE=False

# Azure AD에서 받은 실제 값
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
SHAREPOINT_SITE_ID=your-site-id

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=spo_docs

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 4. 의존성 설치

```bash
cd backend
pip install -r requirements.txt
```

또는 uv 사용:

```bash
cd backend
uv pip install -r requirements.txt
```

### 5. 서버 실행

```bash
cd backend
python -m app.main
```

또는 uvicorn 직접 실행:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 다음 URL에서 확인할 수 있습니다:

- API 문서: http://localhost:8000/docs
- 대체 API 문서: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📝 사용 방법

### 문서 인덱싱

모든 SharePoint 문서 인덱싱:

```bash
cd backend
python scripts/run_indexing.py
```

특정 문서만 인덱싱:

```bash
cd backend
python scripts/run_indexing.py <document_id>
```

### 검색 테스트

대화형 검색 모드:

```bash
cd backend
python scripts/test_search.py
```

단일 쿼리 실행:

```bash
cd backend
python scripts/test_search.py "프로젝트 일정은 어떻게 되나요?"
```

### API 사용

#### 1. 문서 검색

```bash
curl -X POST "http://localhost:8000/api/rag/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "프로젝트 타임라인은?",
    "top_k": 5
  }'
```

응답 예시:

```json
{
  "answer": "관련 문서를 찾았습니다...",
  "sources": [
    {
      "file_title": "project_plan.docx",
      "section_title": "",
      "chunk_index": 0,
      "download_url": "https://sharepoint.com/...",
      "score": 0.92
    }
  ],
  "query": "프로젝트 타임라인은?"
}
```

#### 2. 문서 인덱싱

```bash
curl -X POST "http://localhost:8000/api/rag/index" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc_123",
    "force_reindex": false
  }'
```

## 🔧 TODO 및 개선 사항

### 핵심 기능

- [ ] **임베딩 구현**: OpenAI embeddings 또는 sentence-transformers 통합
- [ ] **Graph API 구현**: 실제 SharePoint 문서 크롤링 로직
- [ ] **LLM 통합**: GPT-4, Claude 등을 사용한 답변 생성
- [ ] **문서 파싱**: DOCX, PDF, TXT 등 다양한 포맷 지원

### 인프라 및 성능

- [ ] **캐싱**: 임베딩 및 검색 결과 캐싱
- [ ] **배치 처리**: 대량 문서 인덱싱 최적화
- [ ] **비동기 처리**: 백그라운드 작업 큐 (Celery, Redis)
- [ ] **로깅**: 구조화된 로깅 (structlog)
- [ ] **모니터링**: 메트릭 수집 및 알림

### 보안 및 인증

- [ ] **API 인증**: JWT 토큰 기반 인증
- [ ] **권한 관리**: 사용자별 문서 접근 제어
- [ ] **비밀 관리**: Azure Key Vault 또는 AWS Secrets Manager

### 테스트 및 품질

- [ ] **단위 테스트**: pytest 기반 테스트 작성
- [ ] **통합 테스트**: API 엔드포인트 테스트
- [ ] **CI/CD**: GitHub Actions 또는 GitLab CI

## 🔑 Microsoft Graph API 설정

### Azure AD 앱 등록

1. Azure Portal에서 앱 등록: https://portal.azure.com/
2. API 권한 설정:
   - `Sites.Read.All`
   - `Files.Read.All`
3. 클라이언트 시크릿 생성
4. 테넌트 ID, 클라이언트 ID, 시크릿을 `.env`에 추가

👉 **자세한 설명: [AZURE_SETUP.md](AZURE_SETUP.md)**

### SharePoint Site ID 찾기

**자동 생성 여부:**
- ✅ SharePoint 사이트: 자동 생성 (샘플 데이터 포함 시)
- ❌ Site ID: 수동 조회 필요

**가장 쉬운 방법:**
```bash
cd backend
python scripts/get_site_id.py
```

Site ID가 자동으로 출력되어 `.env`에 복사-붙여넣기만 하면 됩니다!

👉 **자세한 방법: [AZURE_SETUP.md](AZURE_SETUP.md) 의 "SharePoint Site ID 찾기" 섹션**

## 📚 참고 자료

- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Qdrant 문서](https://qdrant.tech/documentation/)
- [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/)
- [Pydantic 문서](https://docs.pydantic.dev/)

## 📄 라이선스

이 프로젝트는 개발 중인 샘플 프로젝트입니다.

