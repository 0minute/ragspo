# 📥 다운로드 기능 가이드

RAG-SPO에서 검색된 SharePoint 문서를 다운로드하는 방법을 설명합니다.

---

## ✅ 제공되는 다운로드 기능

```
✅ API를 통한 파일 다운로드
✅ 문서 메타데이터 조회
✅ 데모 모드 지원
✅ 스트리밍 다운로드 (대용량 파일)
```

---

## 🚀 다운로드 API 사용법

### 1️⃣ 검색 후 다운로드

#### Step 1: 문서 검색

```bash
curl -X POST "http://localhost:8000/api/rag/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "프로젝트 계획서",
    "top_k": 5
  }'
```

**응답 예시:**
```json
{
  "answer": "프로젝트 계획서에 대한 답변...",
  "sources": [
    {
      "file_title": "프로젝트_계획서.docx",
      "chunk_index": 0,
      "download_url": "https://sharepoint.com/sites/demo/프로젝트_계획서.docx",
      "document_id": "doc_demo_1",
      "score": 0.95
    }
  ],
  "query": "프로젝트 계획서"
}
```

#### Step 2: 문서 다운로드

검색 결과에서 `document_id`를 사용:

```bash
# API를 통한 다운로드
curl -X GET "http://localhost:8000/api/rag/download/doc_demo_1" \
  --output "다운로드_파일.docx"
```

**또는 브라우저에서:**
```
http://localhost:8000/api/rag/download/doc_demo_1
```

---

## 📋 API 엔드포인트

### 1. 파일 다운로드

```
GET /api/rag/download/{document_id}
```

**파라미터:**
- `document_id`: 문서 고유 ID (검색 결과에서 얻음)

**응답:**
- 파일 스트림 (실제 파일 다운로드)
- Content-Type: 파일 형식에 따라 자동 설정
- Content-Disposition: attachment (다운로드 트리거)

**예시:**
```bash
# 명령줄
curl -X GET "http://localhost:8000/api/rag/download/abc123" \
  -o "downloaded_file.docx"

# Python
import requests
response = requests.get("http://localhost:8000/api/rag/download/abc123")
with open("file.docx", "wb") as f:
    f.write(response.content)
```

### 2. 문서 정보 조회

```
GET /api/rag/document/{document_id}/info
```

**파라미터:**
- `document_id`: 문서 고유 ID

**응답:**
```json
{
  "id": "doc_demo_1",
  "name": "프로젝트_계획서.docx",
  "size": 45678,
  "web_url": "https://sharepoint.com/sites/demo/프로젝트_계획서.docx",
  "download_url": "https://sharepoint.com/download/doc_demo_1",
  "internal_download_url": "/api/rag/download/doc_demo_1",
  "modified_date": "2025-01-15T09:30:00Z",
  "author": "김철수"
}
```

**예시:**
```bash
curl -X GET "http://localhost:8000/api/rag/document/doc_demo_1/info"
```

---

## 💻 프론트엔드 통합 예시

### JavaScript / React

```javascript
// 1. 검색
async function searchDocuments(query) {
  const response = await fetch('http://localhost:8000/api/rag/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: 5 })
  });
  return await response.json();
}

// 2. 다운로드
async function downloadDocument(documentId, fileName) {
  const response = await fetch(`http://localhost:8000/api/rag/download/${documentId}`);
  const blob = await response.blob();
  
  // 브라우저에서 자동 다운로드
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}

// 사용 예시
const results = await searchDocuments('프로젝트 계획');
const firstDoc = results.sources[0];
await downloadDocument(firstDoc.document_id, firstDoc.file_title);
```

### Python

```python
import requests

# 1. 검색
def search_documents(query: str):
    response = requests.post(
        "http://localhost:8000/api/rag/search",
        json={"query": query, "top_k": 5}
    )
    return response.json()

# 2. 다운로드
def download_document(document_id: str, save_path: str):
    response = requests.get(
        f"http://localhost:8000/api/rag/download/{document_id}",
        stream=True
    )
    response.raise_for_status()
    
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Downloaded to {save_path}")

# 사용 예시
results = search_documents("프로젝트 계획")
first_doc = results["sources"][0]
download_document(first_doc["document_id"], first_doc["file_title"])
```

---

## 🎨 React 컴포넌트 예시

```jsx
import React, { useState } from 'react';

function DocumentSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/rag/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 5 })
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (documentId, fileName) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/rag/download/${documentId}`
      );
      const blob = await response.blob();
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  return (
    <div>
      <h1>SharePoint 문서 검색</h1>
      
      <div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="검색어를 입력하세요..."
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? '검색 중...' : '검색'}
        </button>
      </div>

      {results && (
        <div>
          <h2>답변</h2>
          <p>{results.answer}</p>

          <h3>관련 문서</h3>
          <ul>
            {results.sources.map((source, idx) => (
              <li key={idx}>
                <strong>{source.file_title}</strong>
                <span> (점수: {source.score.toFixed(2)})</span>
                <button
                  onClick={() => handleDownload(
                    source.document_id,
                    source.file_title
                  )}
                >
                  📥 다운로드
                </button>
                <a
                  href={source.download_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  🔗 SharePoint에서 보기
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default DocumentSearch;
```

---

## 🧪 테스트 시나리오

### 시나리오 1: 데모 모드 테스트

```bash
# 1. 서버 실행
cd backend
python -m app.main

# 2. 새 터미널에서 테스트
# 검색
curl -X POST "http://localhost:8000/api/rag/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "프로젝트", "top_k": 3}'

# 다운로드 (데모 파일)
curl -X GET "http://localhost:8000/api/rag/download/doc_demo_1" \
  -o "demo_file.txt"

# 파일 확인
cat demo_file.txt
```

### 시나리오 2: 실제 SharePoint 다운로드

```bash
# .env 설정
DEMO_MODE=False
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
SHAREPOINT_SITE_ID=your-site-id

# 검색
curl -X POST "http://localhost:8000/api/rag/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "실제 문서", "top_k": 5}'

# 다운로드 (실제 파일)
curl -X GET "http://localhost:8000/api/rag/download/{actual-doc-id}" \
  -o "real_file.docx"
```

---

## 🔧 고급 기능

### 1. 대용량 파일 스트리밍

API는 자동으로 스트리밍 다운로드를 지원합니다:

```python
import requests

def download_large_file(document_id: str, save_path: str):
    """대용량 파일 다운로드 (메모리 효율적)"""
    url = f"http://localhost:8000/api/rag/download/{document_id}"
    
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        
        # 청크 단위로 저장
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
```

### 2. 진행률 표시

```python
import requests
from tqdm import tqdm

def download_with_progress(document_id: str, save_path: str):
    """진행률 표시와 함께 다운로드"""
    url = f"http://localhost:8000/api/rag/download/{document_id}"
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(save_path, 'wb') as f, tqdm(
        total=total_size,
        unit='B',
        unit_scale=True
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))
```

### 3. 배치 다운로드

```python
def download_all_sources(search_results: dict, output_dir: str):
    """검색 결과의 모든 문서 다운로드"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    for source in search_results['sources']:
        file_path = os.path.join(output_dir, source['file_title'])
        print(f"Downloading {source['file_title']}...")
        
        download_document(source['document_id'], file_path)
```

---

## ⚠️ 주의사항

### 1. 파일 크기 제한

현재는 제한이 없지만, 프로덕션에서는 설정 권장:

```python
# main.py에서
app = FastAPI(
    max_request_size=100 * 1024 * 1024  # 100MB
)
```

### 2. 권한 관리

실제 환경에서는 다운로드 권한 확인 필요:

```python
@router.get("/download/{document_id}")
async def download_document(
    document_id: str,
    current_user: User = Depends(get_current_user)  # 인증 추가
):
    # 권한 확인
    if not has_download_permission(current_user, document_id):
        raise HTTPException(status_code=403, detail="권한 없음")
    
    # ... 다운로드 로직
```

### 3. CORS 설정

프론트엔드에서 사용 시 CORS 설정 확인:

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프론트엔드 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 API 응답 형식

### 검색 응답 (추가된 필드)

```json
{
  "answer": "답변 텍스트",
  "sources": [
    {
      "file_title": "문서명.docx",
      "section_title": "",
      "chunk_index": 0,
      "download_url": "https://sharepoint.com/...",
      "document_id": "doc_123",  ← 추가됨!
      "score": 0.95
    }
  ],
  "query": "검색어"
}
```

### 다운로드 응답

```
HTTP/1.1 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="프로젝트_계획서.docx"
Content-Length: 45678

[파일 바이너리 데이터]
```

---

## 🎯 완전한 워크플로우

```python
import requests

# 1. 검색
search_response = requests.post(
    "http://localhost:8000/api/rag/search",
    json={"query": "프로젝트 계획서", "top_k": 5}
)
results = search_response.json()

print("답변:", results['answer'])
print("\n관련 문서:")

# 2. 각 문서 정보 및 다운로드
for idx, source in enumerate(results['sources'], 1):
    print(f"\n{idx}. {source['file_title']} (점수: {source['score']:.2f})")
    
    # 문서 상세 정보
    info_response = requests.get(
        f"http://localhost:8000/api/rag/document/{source['document_id']}/info"
    )
    info = info_response.json()
    print(f"   크기: {info['size']} bytes")
    print(f"   수정일: {info['modified_date']}")
    print(f"   작성자: {info['author']}")
    
    # 다운로드
    download_response = requests.get(
        f"http://localhost:8000/api/rag/download/{source['document_id']}"
    )
    
    with open(f"downloaded_{idx}_{source['file_title']}", 'wb') as f:
        f.write(download_response.content)
    
    print(f"   ✅ 다운로드 완료!")
```

---

## 📚 요약

| 기능 | 엔드포인트 | 설명 |
|------|-----------|------|
| **검색** | `POST /api/rag/search` | 문서 검색 + `document_id` 반환 |
| **다운로드** | `GET /api/rag/download/{id}` | 파일 다운로드 |
| **문서 정보** | `GET /api/rag/document/{id}/info` | 메타데이터 조회 |

**핵심 흐름:**
```
검색 → document_id 획득 → 다운로드/정보 조회
```

---

이제 검색한 문서를 바로 다운로드할 수 있습니다! 🎉

추가 질문이나 커스터마이징이 필요하면 말씀해주세요!

