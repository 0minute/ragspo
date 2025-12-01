# 🎨 RAG-SPO 프론트엔드

간단한 웹 인터페이스로 RAG-SPO 시스템을 사용할 수 있습니다.

## 🚀 빠른 시작

### 1단계: 백엔드 서버 실행

```bash
cd backend
python -m app.main
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 2단계: 프론트엔드 열기

#### 방법 1: 파일로 직접 열기

```bash
# 브라우저에서 파일 열기
open frontend/index.html

# 또는 Windows
start frontend/index.html
```

#### 방법 2: HTTP 서버 사용 (권장)

```bash
# Python 3
cd frontend
python -m http.server 8080

# 브라우저에서 접속
# http://localhost:8080
```

#### 방법 3: VS Code Live Server

1. VS Code에서 `index.html` 열기
2. 우클릭 → "Open with Live Server"
3. 자동으로 브라우저 열림

---

## 📋 기능

### 1. 문서 검색
- 자연어로 질문 입력
- 결과 개수 조절 (1-20개)
- Enter 키로 빠른 검색

### 2. AI 답변
- LLM이 생성한 답변 표시
- 관련 문서 기반 답변

### 3. 관련 문서 목록
- 관련도 점수 표시
- 문서 제목 및 정보
- 청크 인덱스 표시

### 4. 다운로드
- 클릭 한 번으로 파일 다운로드
- 자동 파일명 설정
- SharePoint 링크 제공

---

## 🎯 사용 방법

### 검색하기

1. 검색창에 질문 입력:
   ```
   프로젝트 일정은?
   시스템 아키텍처를 설명해주세요
   회의록 내용은?
   ```

2. "검색" 버튼 클릭 또는 Enter

3. 결과 확인:
   - 상단: AI 답변
   - 하단: 관련 문서 목록

### 문서 다운로드

1. 관련 문서 목록에서 "📥 다운로드" 버튼 클릭
2. 파일 자동 다운로드

### SharePoint에서 보기

1. "🔗 SharePoint에서 보기" 링크 클릭
2. 새 탭에서 원본 문서 열림

---

## ⚙️ 설정

### API 서버 주소 변경

`index.html` 파일의 상단 스크립트 섹션에서:

```javascript
const API_BASE_URL = 'http://localhost:8000';  // 여기 수정
```

다른 서버 주소로 변경:
```javascript
const API_BASE_URL = 'http://your-server:8000';
```

### 결과 개수 기본값

HTML에서 기본값 변경:
```html
<input type="number" id="topK" value="5" min="1" max="20">
                                    ↑ 여기 수정
```

---

## 🎨 커스터마이징

### 색상 테마 변경

CSS 상단의 그라데이션 색상 수정:

```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 다른 테마 예시 */

/* 블루 테마 */
background: linear-gradient(135deg, #667eea 0%, #4facfe 100%);

/* 그린 테마 */
background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);

/* 핑크 테마 */
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
```

### 레이아웃 변경

`.container`의 `max-width` 수정:

```css
.container {
    max-width: 1200px;  /* 원하는 크기로 변경 */
}
```

---

## 🔧 문제 해결

### 문제 1: "API 서버에 연결할 수 없습니다"

**원인:** 백엔드 서버가 실행되지 않음

**해결:**
```bash
cd backend
python -m app.main
```

서버가 `http://localhost:8000`에서 실행 중인지 확인

### 문제 2: CORS 에러

**원인:** 파일로 직접 열면 CORS 문제 발생 가능

**해결:** HTTP 서버 사용
```bash
cd frontend
python -m http.server 8080
```

### 문제 3: 다운로드가 안 됨

**원인:** 
- 데모 모드 실행 중
- document_id가 없음

**해결:**
1. `.env`에서 `DEMO_MODE=False` 확인
2. SharePoint 연동 확인

### 문제 4: 검색 결과가 없음

**원인:** 문서가 인덱싱되지 않음

**해결:**
```bash
cd backend
python scripts/run_indexing.py
```

---

## 📱 모바일 지원

프론트엔드는 반응형으로 제작되어 모바일에서도 사용 가능합니다:

- ✅ 자동 레이아웃 조정
- ✅ 터치 최적화
- ✅ 작은 화면 지원

---

## 🚀 배포

### GitHub Pages

1. `frontend/` 폴더를 GitHub 리포지토리에 푸시
2. Settings → Pages → Source: main branch, /frontend
3. 저장 후 URL 확인

**주의:** API 서버 주소를 배포된 백엔드 주소로 변경 필요

### Netlify

1. Netlify에 `frontend/` 폴더 드래그 앤 드롭
2. 자동 배포
3. API 서버 주소 변경

### Vercel

```bash
cd frontend
vercel
```

---

## 🎯 다음 단계

기본 기능이 작동하면:

1. ✅ 로딩 애니메이션 개선
2. ✅ 검색 히스토리 추가
3. ✅ 북마크 기능
4. ✅ 다크 모드
5. ✅ 검색 필터
6. ✅ 사용자 인증

---

## 📚 기술 스택

- HTML5
- CSS3 (순수 CSS, 프레임워크 없음)
- Vanilla JavaScript (라이브러리 없음)
- Fetch API (AJAX)

**빌드 과정 없음** - 바로 실행 가능! 🎉

---

## 💡 팁

### 개발자 도구 활용

브라우저에서 F12를 누르면:
- 네트워크 탭: API 요청/응답 확인
- 콘솔: 로그 및 에러 확인

### 로컬 개발

Live Server 사용 시 코드 수정하면 자동 새로고침됩니다.

---

## 📞 지원

문제가 있으면:
1. 브라우저 콘솔 확인 (F12)
2. 백엔드 로그 확인
3. 이슈 제기

즐거운 사용 되세요! 🚀

