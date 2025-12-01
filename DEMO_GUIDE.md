# 🎮 데모 모드 사용 가이드

Azure AD 앱 등록 권한이 없어도 RAG-SPO 시스템을 테스트할 수 있습니다!

## 🚀 빠른 시작 (5분 안에!)

### 1. 환경 설정

`backend/.env` 파일 생성:

```bash
cd backend
cp env.example .env
```

`.env` 파일을 열고 **DEMO_MODE=True**로 설정:

```env
# 데모 모드 활성화! (이것만 True로 설정하면 됩니다)
DEMO_MODE=True

# 아래 값들은 데모 모드에서는 무시됨 (그대로 두세요)
TENANT_ID=demo-tenant-id
CLIENT_ID=demo-client-id
CLIENT_SECRET=demo-client-secret
SHAREPOINT_SITE_ID=

# Qdrant 설정
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=spo_docs

# Embedding 설정
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# Chunking 설정
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 2. Qdrant 설정

#### 옵션 A: Local 모드 (Docker 불필요! ⭐ 추천)

`.env` 파일에서 다음 설정만 확인:

```env
QDRANT_MODE=local
QDRANT_PATH=./qdrant_data
```

**끝!** 별도 실행 불필요, 데이터는 자동으로 `backend/qdrant_data/`에 저장됩니다.

#### 옵션 B: Server 모드 (Docker)

Docker로 로컬 Qdrant 실행:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

`.env` 파일:
```env
QDRANT_MODE=server
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

또는 Docker Desktop에서 실행:
- Images 탭 → `qdrant/qdrant` 검색 → Pull → Run
- Port: `6333:6333` 설정

👉 **Docker 없이 실행: [NO_DOCKER_GUIDE.md](NO_DOCKER_GUIDE.md)**

### 3. 의존성 설치

```bash
cd backend
pip install -r requirements.txt
```

### 4. 데모 실행! 🎉

#### 방법 A: FastAPI 서버 실행

```bash
cd backend
python -m app.main
```

브라우저에서 확인:
- API 문서: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

#### 방법 B: 인덱싱 스크립트 실행

```bash
cd backend
python scripts/run_indexing.py
```

샘플 문서 3개가 자동으로 인덱싱됩니다:
- ✅ 프로젝트_계획서.docx
- ✅ 기술_문서.pdf
- ✅ 회의록_2025.txt

#### 방법 C: 검색 테스트

```bash
cd backend
python scripts/test_search.py
```

대화형 모드에서 질문 입력:
```
Query: 프로젝트 일정은?
Query: RAG 시스템 아키텍처는?
Query: 회의에서 논의된 내용은?
```

## 📚 데모 모드에서 제공되는 샘플 데이터

### 문서 1: 프로젝트_계획서.docx
```
내용:
- 프로젝트 개요
- 일정: 2025년 1~3월
- 주요 기능: 문서 인덱싱, 검색, AI 답변
- 기대 효과: 업무 효율 30% 향상
```

### 문서 2: 기술_문서.pdf
```
내용:
- 시스템 아키텍처 (FastAPI, Qdrant, Graph API)
- 데이터 파이프라인
- 검색 프로세스
- 보안 고려사항
```

### 문서 3: 회의록_2025.txt
```
내용:
- 개발 현황 공유
- 다음 주 목표
- 이슈: Azure AD 권한 문제 해결
- 다음 회의 일정
```

## 🧪 API 테스트 예제

### 1. 문서 검색

```bash
curl -X POST "http://localhost:8000/api/rag/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "프로젝트 일정은 언제인가요?",
    "top_k": 3
  }'
```

### 2. 특정 문서 인덱싱

```bash
curl -X POST "http://localhost:8000/api/rag/index" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc_demo_1",
    "force_reindex": false
  }'
```

## 🎯 테스트할 수 있는 질문 예시

- ✅ "프로젝트 일정은 어떻게 되나요?"
- ✅ "RAG 시스템의 아키텍처를 설명해주세요"
- ✅ "회의에서 어떤 이슈가 논의되었나요?"
- ✅ "보안은 어떻게 처리하나요?"
- ✅ "데이터 파이프라인은 어떻게 작동하나요?"

## 🔄 실제 SharePoint로 전환하기

데모 테스트가 끝나고 실제 SharePoint를 연결하려면:

### 옵션 1: Microsoft 365 Developer Program

1. https://developer.microsoft.com/microsoft-365/dev-program 가입
2. 무료 E5 샌드박스 생성 (90일, 자동 연장)
3. Azure Portal에서 앱 등록
4. `.env`에서 `DEMO_MODE=False`로 변경
5. 실제 `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET` 입력

### 옵션 2: 회사 IT 관리자에게 요청

회사 IT 부서에 다음을 요청:
1. Azure AD 앱 등록 권한 또는
2. 앱 등록 대행 요청 (필요한 권한: Sites.Read.All, Files.Read.All)

## ⚠️ 데모 모드 제한사항

데모 모드는 **학습 및 테스트 목적**으로 제공됩니다:

- ✅ 전체 API 흐름 테스트 가능
- ✅ 검색 및 인덱싱 로직 확인 가능
- ✅ UI/UX 개발 가능
- ❌ 실제 임베딩 생성 안 함 (더미 벡터 사용)
- ❌ 실제 LLM 답변 생성 안 함 (템플릿 응답)
- ❌ 샘플 문서 3개만 제공

## 🎓 다음 단계

데모가 마음에 들었다면:

1. **임베딩 구현**: OpenAI API 또는 sentence-transformers 추가
2. **LLM 통합**: GPT-4 또는 Claude로 실제 답변 생성
3. **실제 SharePoint 연동**: Developer Program 또는 회사 계정 사용
4. **문서 파싱**: DOCX, PDF 파일 텍스트 추출 구현

## 📞 도움이 필요하신가요?

- 데모 모드 오류 발생 시: 이슈 제기 또는 문의
- 실제 배포 관련 질문: README.md 참고
- Azure 설정 도움: AZURE_SETUP.md 참고

즐거운 개발 되세요! 🚀

