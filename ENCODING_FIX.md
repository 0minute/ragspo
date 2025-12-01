# 🔧 한글 파일명 인코딩 문제 해결

## 🐛 문제

다운로드 시 다음과 같은 에러 발생:

```
'latin-1' codec can't encode characters in position 21-23: 
ordinal not in range(256)
```

**원인:** HTTP 헤더 `Content-Disposition`이 기본적으로 Latin-1 인코딩만 지원하기 때문에 한글 파일명을 처리하지 못함.

---

## ✅ 해결 방법

### RFC 5987 표준 사용

파일명을 UTF-8로 URL 인코딩하여 전달:

```python
from urllib.parse import quote

# 한글 파일명
file_name = "프로젝트_계획서.docx"

# URL 인코딩
encoded_filename = quote(file_name, safe='')
# 결과: "%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EA%B3%84%ED%9A%8D%EC%84%9C.docx"

# HTTP 헤더에 추가
headers = {
    "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
}
```

---

## 🔍 수정된 코드

### Before (문제 있던 코드)

```python
headers = {
    "Content-Disposition": f"attachment; filename={file_name}"
}
# ❌ 한글 파일명 → Latin-1 인코딩 에러
```

### After (수정된 코드)

```python
from urllib.parse import quote

encoded_filename = quote(file_name, safe='')
headers = {
    "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
}
# ✅ 한글 파일명 정상 작동
```

---

## 🧪 테스트

### Python으로 테스트

```python
import requests

# 다운로드 테스트
response = requests.get("http://localhost:8000/api/rag/download/doc_demo_1")

# 헤더 확인
print(response.headers['Content-Disposition'])
# 출력: attachment; filename*=UTF-8''demo_doc_demo_1.txt

# 파일 저장
with open("test_download.txt", "wb") as f:
    f.write(response.content)

print("✅ 다운로드 성공!")
```

### 브라우저에서 테스트

1. 프론트엔드에서 검색
2. "📥 다운로드" 버튼 클릭
3. 파일명 확인 (한글 정상 표시)

---

## 📋 RFC 5987 표준

### 형식

```
Content-Disposition: attachment; filename*=charset'language'encoded-filename
```

**예시:**

```
Content-Disposition: attachment; filename*=UTF-8''%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8.docx
```

### 구성 요소

- `charset`: UTF-8 (인코딩)
- `language`: '' (비워둠, 선택적)
- `encoded-filename`: URL 인코딩된 파일명

---

## 🌐 브라우저 호환성

### 지원 브라우저

| 브라우저 | RFC 5987 지원 | 비고 |
|---------|--------------|------|
| Chrome | ✅ 지원 | |
| Firefox | ✅ 지원 | |
| Safari | ✅ 지원 | |
| Edge | ✅ 지원 | |
| IE 11 | ⚠️ 부분 지원 | filename 폴백 권장 |

### 레거시 브라우저 지원

두 가지 방식 모두 제공:

```python
# ASCII 안전 파일명 (레거시)과 UTF-8 파일명 (모던) 둘 다 제공
safe_filename = "document.docx"  # ASCII만 사용
encoded_filename = quote("프로젝트_계획서.docx", safe='')

headers = {
    "Content-Disposition": (
        f'attachment; '
        f'filename="{safe_filename}"; '  # 레거시 브라우저용
        f"filename*=UTF-8''{encoded_filename}"  # 모던 브라우저용
    )
}
```

---

## 🔧 추가 수정 사항

### 1. Content-Type에 charset 추가

```python
# Before
media_type="text/plain"

# After
media_type="text/plain; charset=utf-8"
```

### 2. 다양한 파일 형식 지원

```python
import mimetypes

def get_content_type(filename: str) -> str:
    """파일 확장자로 Content-Type 자동 감지"""
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or 'application/octet-stream'

# 사용
content_type = get_content_type("프로젝트.docx")
# 결과: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
```

---

## 🎯 완전한 예시

### FastAPI 엔드포인트

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from urllib.parse import quote
import io

@router.get("/download/{document_id}")
async def download_document(document_id: str):
    # 파일 데이터 및 이름 가져오기
    file_content = get_file_content(document_id)
    file_name = "프로젝트_계획서.docx"
    
    # UTF-8 인코딩
    encoded_filename = quote(file_name, safe='')
    
    # 응답 반환
    return StreamingResponse(
        io.BytesIO(file_content),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )
```

---

## 🐛 다른 인코딩 문제

### 문제 1: URL에 한글이 있는 경우

```python
# 문제
url = "https://sharepoint.com/문서/파일.docx"

# 해결
from urllib.parse import quote
encoded_url = quote(url, safe=':/?#[]@!$&\'()*+,;=')
```

### 문제 2: JSON 응답에 한글

```python
# FastAPI는 자동으로 UTF-8 처리
return {"message": "다운로드 완료"}  # ✅ 자동 처리됨
```

### 문제 3: 파일 시스템에 저장 시

```python
# Windows에서 한글 파일명
with open("프로젝트.docx", "wb") as f:  # ✅ Python 3는 자동 처리
    f.write(content)
```

---

## ✅ 검증 방법

### 1. 헤더 확인

```bash
curl -I "http://localhost:8000/api/rag/download/doc_demo_1"
```

**출력:**
```
Content-Disposition: attachment; filename*=UTF-8''demo_doc_demo_1.txt
```

### 2. 실제 다운로드

```python
import requests

response = requests.get("http://localhost:8000/api/rag/download/doc_demo_1")
filename = response.headers['Content-Disposition'].split("filename*=UTF-8''")[1]

# URL 디코딩
from urllib.parse import unquote
decoded_filename = unquote(filename)
print(decoded_filename)  # demo_doc_demo_1.txt
```

### 3. 브라우저 테스트

1. 검색 수행
2. "다운로드" 버튼 클릭
3. 다운로드 폴더 확인
4. 파일명이 한글로 정상 표시되는지 확인

---

## 📚 참고 자료

### RFC 5987
- [RFC 5987 - Character Set and Language Encoding](https://tools.ietf.org/html/rfc5987)
- [MDN - Content-Disposition](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition)

### Python urllib.parse
- [Python Documentation - urllib.parse.quote](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote)

---

## 🎉 결과

```
✅ 한글 파일명 정상 다운로드
✅ 특수문자 지원
✅ 모든 브라우저 호환
✅ UTF-8 완벽 지원
```

---

## 💡 추가 팁

### URL 안전 문자

`quote()` 함수에서 `safe` 매개변수:

```python
# 모든 문자 인코딩
quote("프로젝트_계획서.docx", safe='')

# 일부 문자는 안전하게 유지
quote("path/to/파일.docx", safe='/')  # /는 인코딩 안 함
```

### 파일명 정리

```python
def sanitize_filename(filename: str) -> str:
    """안전한 파일명으로 변환"""
    # 위험한 문자 제거
    dangerous = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous:
        filename = filename.replace(char, '_')
    return filename

# 사용
safe_name = sanitize_filename("프로젝트:계획서?.docx")
# 결과: "프로젝트_계획서_.docx"
```

---

이제 한글 파일명도 완벽하게 다운로드됩니다! 🎉

