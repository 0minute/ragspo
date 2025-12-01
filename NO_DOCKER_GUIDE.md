# 🚀 Docker 없이 RAG-SPO 실행하기

Docker가 설치되어 있지 않아도 괜찮습니다! Qdrant를 **로컬 파일 시스템**에 저장하여 실행할 수 있습니다.

---

## ⚡ 빠른 시작 (Docker 불필요!)

### 1단계: 환경 설정

`backend/.env` 파일 생성:

```bash
cd backend
cp env.example .env
```

### 2단계: .env 파일 편집

```env
# 데모 모드 (SharePoint 없이 테스트)
DEMO_MODE=True

# ⭐ Qdrant 로컬 모드 (Docker 불필요!)
QDRANT_MODE=local
QDRANT_PATH=./qdrant_data

# 아래 설정들은 기본값 사용
TENANT_ID=demo-tenant-id
CLIENT_ID=demo-client-id
CLIENT_SECRET=demo-client-secret
SHAREPOINT_SITE_ID=

QDRANT_COLLECTION_NAME=spo_docs
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 3단계: 의존성 설치

```bash
cd backend
pip install -r requirements.txt
```

### 4단계: 바로 실행!

#### 옵션 A: 서버 실행

```bash
python -m app.main
```

서버가 시작되고 Qdrant 데이터는 `backend/qdrant_data/` 폴더에 자동 저장됩니다!

#### 옵션 B: 샘플 문서 인덱싱

```bash
python scripts/run_indexing.py
```

#### 옵션 C: 검색 테스트

```bash
python scripts/test_search.py
```

---

## 🎯 Qdrant 모드 비교

| 항목 | Local 모드 | Server 모드 |
|------|-----------|------------|
| **Docker 필요** | ❌ 불필요 | ✅ 필요 |
| **설치 복잡도** | 낮음 | 높음 |
| **성능** | 개발/테스트 충분 | 프로덕션급 |
| **데이터 저장** | 로컬 파일 | 서버 메모리/디스크 |
| **추천 환경** | 개발, 테스트, 학습 | 프로덕션, 고성능 |
| **설정** | `QDRANT_MODE=local` | `QDRANT_MODE=server` |

---

## 📁 데이터 저장 위치

### Local 모드
```
backend/
├── qdrant_data/          ← 여기에 벡터 데이터 저장!
│   ├── collection/
│   ├── meta.json
│   └── ...
├── app/
├── scripts/
└── .env
```

**데이터는 `backend/qdrant_data/` 폴더에 자동으로 저장됩니다.**

### 데이터 초기화 (필요시)

```bash
# Qdrant 데이터 삭제 (새로 시작하고 싶을 때)
cd backend
rm -rf qdrant_data
# Windows: rmdir /s qdrant_data
```

---

## 🔧 모드 전환하기

### Local → Server (나중에 Docker 설치 후)

`.env` 파일 수정:

```env
# Server 모드로 전환
QDRANT_MODE=server
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

Docker 실행:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Server → Local (Docker 제거 후)

`.env` 파일 수정:

```env
# Local 모드로 전환
QDRANT_MODE=local
QDRANT_PATH=./qdrant_data
```

---

## 🧪 전체 테스트 예제

### 1. 환경 준비

```bash
# 1. 프로젝트 디렉토리로 이동
cd backend

# 2. .env 파일 생성 및 편집
cp env.example .env

# .env 파일 내용:
# DEMO_MODE=True
# QDRANT_MODE=local
# QDRANT_PATH=./qdrant_data

# 3. 의존성 설치
pip install -r requirements.txt
```

### 2. 샘플 데이터 인덱싱

```bash
python scripts/run_indexing.py
```

**출력 예시:**
```
==================================================
RAG-SPO Document Indexing Script
==================================================

Ensuring Qdrant collection exists...
[Qdrant] Using LOCAL mode: ./qdrant_data
✓ Qdrant collection is ready

Indexing all SharePoint documents...
[DEMO MODE] Returning sample documents
Retrieving document doc_demo_1 from SharePoint...
[DEMO MODE] Using dummy access token
[DEMO MODE] Returning sample content for doc_demo_1
Splitting document into chunks...
Generating embeddings for 5 chunks...
Uploading 5 chunks to Qdrant...
Successfully indexed 5 chunks for document doc_demo_1

✓ Indexed 3 documents with 15 total chunks

==================================================
Indexing completed successfully!
==================================================
```

### 3. 검색 테스트

```bash
python scripts/test_search.py
```

```
==================================================
RAG-SPO Document Search Test
==================================================

Type your query (or 'quit' to exit)
--------------------------------------------------------------

Query: 프로젝트 일정은?

Searching...
[Qdrant] Using LOCAL mode: ./qdrant_data

==================================================
ANSWER:
--------------------------------------------------------------
[TODO: LLM 통합 필요] '프로젝트 일정은?' 질문에 대해 3개의 관련 문서를 찾았습니다.

==================================================
SOURCES:
--------------------------------------------------------------

1. 프로젝트_계획서.docx (chunk 0)
   Score: 0.9234
   URL: https://demo.sharepoint.com/sites/demo/프로젝트_계획서.docx

2. 회의록_2025.txt (chunk 1)
   Score: 0.8567
   URL: https://demo.sharepoint.com/sites/demo/회의록_2025.txt
```

### 4. FastAPI 서버 실행

```bash
python -m app.main
```

**브라우저에서 확인:**
- API 문서: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**API 테스트:**
```bash
curl -X POST "http://localhost:8000/api/rag/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "프로젝트 일정은?", "top_k": 3}'
```

---

## 💾 데이터 백업

Local 모드는 파일로 저장되므로 백업이 쉽습니다!

```bash
# 백업
cd backend
zip -r qdrant_backup.zip qdrant_data/

# 복원
unzip qdrant_backup.zip
```

---

## 🔍 문제 해결

### Q1: "qdrant_data 폴더에 권한이 없습니다"

**해결:**
```bash
# 폴더 수동 생성
mkdir -p backend/qdrant_data

# 권한 확인 (Linux/Mac)
chmod 755 backend/qdrant_data
```

### Q2: "Collection not found" 에러

**원인:** Qdrant 데이터가 초기화되지 않음

**해결:**
1. 서버를 한 번 실행하면 자동으로 컬렉션 생성됨
2. 또는 수동으로:
```python
python -c "from app.qdrant_client import ensure_collection_exists; ensure_collection_exists()"
```

### Q3: 데이터가 계속 쌓여서 공간이 부족해요

**해결:**
```bash
# 데이터 삭제
rm -rf backend/qdrant_data
# 또는 Windows: rmdir /s backend\qdrant_data

# 다시 인덱싱
python scripts/run_indexing.py
```

### Q4: Local 모드와 Server 모드 데이터 호환되나요?

**답변:** 아니요, 데이터 형식이 다릅니다.

**전환 시 재인덱싱 필요:**
```bash
# 1. 모드 변경 (.env 수정)
# 2. 기존 데이터 삭제
# 3. 재인덱싱
python scripts/run_indexing.py
```

---

## 📊 성능 비교

### Local 모드 (Docker 없음)
- ✅ 설치 간편
- ✅ 메모리 효율적
- ✅ 개발/테스트 충분
- ⚠️ 대량 데이터에는 느릴 수 있음 (수만 개 이상)

### Server 모드 (Docker)
- ✅ 프로덕션급 성능
- ✅ 확장성 좋음
- ✅ 대량 데이터 처리
- ⚠️ Docker 설치 필요
- ⚠️ 메모리 사용량 많음

---

## 🎓 추천 사용 시나리오

| 시나리오 | 추천 모드 |
|---------|----------|
| 처음 시작 / 학습 | **Local** ⭐ |
| 개발 / 테스트 | **Local** ⭐ |
| 소규모 프로젝트 (< 10,000 문서) | **Local** |
| 대규모 프로젝트 (> 10,000 문서) | Server |
| 프로덕션 배포 | Server |
| Docker 사용 불가 환경 | **Local** ⭐ |

---

## ✨ 요약

### Docker 없이 실행하는 완전한 단계:

```bash
# 1. 설정
cd backend
cp env.example .env
# .env에서 DEMO_MODE=True, QDRANT_MODE=local 확인

# 2. 설치
pip install -r requirements.txt

# 3. 실행 (이게 전부!)
python scripts/run_indexing.py
python scripts/test_search.py
python -m app.main
```

**Qdrant 데이터는 `backend/qdrant_data/`에 자동 저장됩니다!**

---

## 🚀 다음 단계

1. ✅ Docker 없이 로컬에서 테스트 완료
2. ✅ 데모 모드로 전체 흐름 이해
3. ⬜ 실제 SharePoint 연동 (AZURE_SETUP.md 참고)
4. ⬜ 임베딩 모델 추가 (OpenAI 또는 sentence-transformers)
5. ⬜ LLM 통합 (GPT-4, Claude)

---

**이제 Docker 걱정 없이 바로 시작할 수 있습니다!** 🎉

궁금한 점이 있으면 언제든 물어보세요!

