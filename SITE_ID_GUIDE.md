# 🆔 SharePoint Site ID 찾기 완벽 가이드

## ❓ SharePoint Site ID가 뭔가요?

SharePoint Site ID는 SharePoint 사이트를 식별하는 **고유 번호**입니다.

```
형식: yourname.sharepoint.com,12345678-1234-5678-abcd-123456789012,87654321-4321-8765-dcba-210987654321
```

RAG-SPO 앱이 **어느 SharePoint 사이트**에서 문서를 가져올지 알려주는 데 필요합니다.

---

## 🎯 자동 생성 여부 요약

### Microsoft 365 Developer Program 사용 시

| 항목 | 자동 생성? | 비고 |
|------|-----------|------|
| SharePoint 사이트 | ✅ **자동** | "샘플 데이터 포함" 선택 시 |
| 문서 및 폴더 | ✅ **자동** | 샘플 데이터 함께 생성 |
| Tenant ID | ✅ **자동** | Azure Portal에서 확인 |
| Client ID | ✅ **자동** | 앱 등록 시 발급 |
| Client Secret | ✅ **자동** | 생성 시 발급 (즉시 복사 필수!) |
| **Site ID** | ❌ **수동 조회** | 아래 방법으로 찾기 |

### 결론

**SharePoint 사이트는 자동으로 만들어지지만, Site ID는 만들어진 후에 조회해야 합니다!**

---

## 🚀 Site ID 찾는 3가지 방법

### ⭐ 방법 1: Python 스크립트 (가장 쉬움!)

**장점:**
- ✅ 명령어 한 줄로 완료
- ✅ 모든 사이트 자동 출력
- ✅ 복사-붙여넣기만 하면 됨

**사용법:**

```bash
# 1. 백엔드 디렉토리로 이동
cd backend

# 2. .env 파일 확인 (DEMO_MODE=False, 실제 Azure AD 정보 입력)
# DEMO_MODE=False
# TENANT_ID=your-actual-tenant-id
# CLIENT_ID=your-actual-client-id
# CLIENT_SECRET=your-actual-client-secret

# 3. 스크립트 실행
python scripts/get_site_id.py
```

**출력 예시:**

```
🔍 SharePoint Site ID 조회 도구
==================================================

1️⃣  Microsoft Graph API 인증 중...
✅ 인증 성공!

2️⃣  SharePoint 사이트 목록 조회 중...

==================================================
📋 모든 SharePoint 사이트 목록
==================================================

✅ 총 3개의 사이트를 찾았습니다.

──────────────────────────────────────────────────
사이트 #1: Communication site
──────────────────────────────────────────────────
🔑 Site ID: contoso.sharepoint.com,12345678-abcd-...,87654321-dcba-...
🌐 URL: https://contoso.sharepoint.com/sites/contoso
📝 설명: Sample communication site with news and events

──────────────────────────────────────────────────
사이트 #2: Team site
──────────────────────────────────────────────────
🔑 Site ID: contoso.sharepoint.com,aaaaaaaa-bbbb-...,cccccccc-dddd-...
🌐 URL: https://contoso.sharepoint.com/sites/team
📝 설명: Collaboration site for team

==================================================
💡 추천
==================================================

첫 번째 사이트를 사용하는 것을 추천합니다:

사이트 이름: Communication site
Site ID: contoso.sharepoint.com,12345678-abcd-...,87654321-dcba-...

.env 파일에 다음과 같이 추가하세요:

SHAREPOINT_SITE_ID=contoso.sharepoint.com,12345678-abcd-...,87654321-dcba-...
```

**특정 사이트만 조회:**

```bash
# /sites/contoso 사이트의 ID만 조회
python scripts/get_site_id.py /sites/contoso
```

---

### 🌐 방법 2: Graph Explorer (웹 브라우저)

**장점:**
- ✅ 브라우저에서 바로 실행
- ✅ 코드 실행 불필요
- ✅ 시각적으로 확인 가능

**단계:**

#### Step 1: Graph Explorer 접속

```
https://developer.microsoft.com/en-us/graph/graph-explorer
```

#### Step 2: 로그인

- 우측 상단 "Sign in" 클릭
- 개발자 계정으로 로그인: `admin@yourname.onmicrosoft.com`

#### Step 3: 권한 동의

1. 좌측 하단 "Modify permissions" 클릭
2. `Sites.Read.All` 찾기
3. "Consent" 버튼 클릭
4. 권한 승인

#### Step 4: 쿼리 실행

1. 상단 쿼리 입력창에:
   ```
   https://graph.microsoft.com/v1.0/sites?search=*
   ```

2. "Run query" 버튼 클릭

#### Step 5: 결과 확인

응답 JSON에서 `id` 필드 복사:

```json
{
  "@odata.context": "...",
  "value": [
    {
      "id": "contoso.sharepoint.com,12345678-1234-5678-abcd-123456789012,87654321-4321-8765-dcba-210987654321",
      "displayName": "Communication site",
      "name": "contoso",
      "webUrl": "https://contoso.sharepoint.com/sites/contoso",
      "description": "Sample communication site"
    }
  ]
}
```

📋 `id` 값을 복사하여 `.env`에 추가

---

### 💻 방법 3: PowerShell / Bash

#### Windows (PowerShell)

```powershell
# 변수 설정
$tenantId = "your-tenant-id"
$clientId = "your-client-id"
$clientSecret = "your-client-secret"

# 토큰 발급
$body = @{
    client_id     = $clientId
    scope         = "https://graph.microsoft.com/.default"
    client_secret = $clientSecret
    grant_type    = "client_credentials"
}

$tokenResponse = Invoke-RestMethod -Method Post `
    -Uri "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" `
    -Body $body

$token = $tokenResponse.access_token

# 사이트 목록 조회
$headers = @{
    Authorization = "Bearer $token"
}

$sites = Invoke-RestMethod -Method Get `
    -Uri "https://graph.microsoft.com/v1.0/sites?search=*" `
    -Headers $headers

# 결과 출력
$sites.value | ForEach-Object {
    Write-Host "===================="
    Write-Host "사이트: $($_.displayName)"
    Write-Host "Site ID: $($_.id)"
    Write-Host "URL: $($_.webUrl)"
    Write-Host ""
}
```

#### Linux / macOS (Bash + curl)

```bash
#!/bin/bash

TENANT_ID="your-tenant-id"
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"

# 토큰 발급
TOKEN_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -d "client_id=$CLIENT_ID" \
  -d "scope=https://graph.microsoft.com/.default" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "grant_type=client_credentials")

TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

# 사이트 조회
curl -s -X GET \
  "https://graph.microsoft.com/v1.0/sites?search=*" \
  -H "Authorization: Bearer $TOKEN" | jq '.value[] | {displayName, id, webUrl}'
```

---

## 🔧 .env 파일 설정

Site ID를 찾았다면 `.env` 파일에 추가:

```env
# Microsoft Graph API
DEMO_MODE=False
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret

# ⭐ 여기에 복사한 Site ID 추가
SHAREPOINT_SITE_ID=contoso.sharepoint.com,12345678-1234-5678-abcd-123456789012,87654321-4321-8765-dcba-210987654321

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=spo_docs

# 나머지 설정...
```

---

## ✅ 설정 확인

Site ID가 제대로 설정되었는지 확인:

```bash
cd backend

# 인덱싱 테스트
python scripts/run_indexing.py

# 또는 서버 실행
python -m app.main
```

에러 없이 실행되면 성공! 🎉

---

## ❓ FAQ

### Q1: Site ID를 찾을 수 없어요

**원인:**
- SharePoint 사이트가 아직 생성되지 않음
- API 권한이 부여되지 않음

**해결:**
1. Microsoft 365 Admin Center에서 SharePoint 사이트 확인
   ```
   https://admin.microsoft.com/
   ```
2. Azure Portal에서 API 권한 확인 (`Sites.Read.All` 동의 필요)

### Q2: 여러 사이트가 있는데 어떤 걸 써야 하나요?

**추천 순서:**
1. 샘플 데이터가 포함된 사이트 (Communication site 등)
2. 가장 많이 사용하는 사이트
3. 테스트용으로 만든 사이트

**모든 사이트 사용:**
- Site ID를 생략하면 모든 사이트에서 검색 가능 (일부 API에서)

### Q3: Site ID를 입력 안 하면 어떻게 되나요?

**데모 모드:**
- 문제 없음! Site ID 불필요

**실제 모드:**
- 특정 사이트 지정 필요
- 입력 안 하면 에러 발생 가능

### Q4: Site ID 형식이 이상해요

**정상적인 형식:**
```
hostname,guid1,guid2
예: contoso.sharepoint.com,12345678-1234-...,87654321-4321-...
```

**비정상:**
- GUID 하나만 있음
- .sharepoint.com이 없음
- 쉼표가 없음

→ Graph API로 다시 조회 필요

---

## 📚 참고 자료

- [Microsoft Graph Sites API](https://learn.microsoft.com/en-us/graph/api/resources/site)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [SharePoint Site ID 구조](https://learn.microsoft.com/en-us/graph/api/site-get)

---

## 🎯 요약

| 항목 | 설명 |
|------|------|
| **자동 생성?** | ❌ 수동 조회 필요 |
| **가장 쉬운 방법** | `python scripts/get_site_id.py` |
| **브라우저 방법** | Graph Explorer 사용 |
| **설정 위치** | `backend/.env` → `SHAREPOINT_SITE_ID` |
| **데모 모드** | Site ID 불필요 |

---

문제가 있으면 언제든 질문하세요! 🚀

