# 🔐 Microsoft 365 Developer Program 및 Azure AD 설정 가이드

Azure AD 앱 등록 권한이 없는 경우 무료 개발자 테넌트를 사용할 수 있습니다!

## 🎯 Microsoft 365 Developer Program (추천!)

**완전 무료**로 실제 SharePoint Online과 Graph API를 사용할 수 있습니다.

### 장점
- ✅ 90일 무료 (활동 시 자동 연장)
- ✅ 25개 사용자 라이선스
- ✅ SharePoint Online 포함
- ✅ 샘플 데이터 자동 생성
- ✅ 완전한 관리자 권한
- ✅ 실제 프로덕션과 동일한 환경

---

## 📝 단계별 설정 가이드

### Step 1: Developer Program 가입

1. **웹사이트 접속**
   ```
   https://developer.microsoft.com/en-us/microsoft-365/dev-program
   ```

2. **"Join now" 클릭**

3. **Microsoft 계정으로 로그인**
   - 개인 계정 사용 (Outlook.com, Hotmail.com 등)
   - 회사 계정이 아닌 개인 계정 권장

4. **프로필 정보 입력**
   - Country/Region: South Korea
   - Company: 개인 또는 회사명
   - 사용 목적: Learning / Development

### Step 2: 샌드박스 환경 생성

1. **"Set up E5 subscription" 선택**

2. **관리자 계정 생성**
   ```
   Username: admin (또는 원하는 이름)
   Domain: yourname.onmicrosoft.com (고유한 이름 선택)
   Password: 강력한 비밀번호 설정
   ```
   
   예시: `admin@myragspo.onmicrosoft.com`

3. **✅ "Add sample data packs" 옵션 체크**
   - SharePoint 사이트와 문서가 자동 생성됩니다!
   - 메일, 팀즈, 사용자 등 테스트 데이터 포함

4. **생성 대기** (약 5-10분)

5. **완료!** 
   - 테넌트 정보 확인
   - 관리자 포털 링크 저장

### Step 3: Azure Portal 접속

1. **Azure Portal 열기**
   ```
   https://portal.azure.com/
   ```

2. **위에서 만든 관리자 계정으로 로그인**
   ```
   admin@yourname.onmicrosoft.com
   ```

### Step 4: Azure AD 앱 등록

1. **Azure Active Directory로 이동**
   - 왼쪽 메뉴에서 "Azure Active Directory" 클릭
   - 또는 검색창에 "Azure Active Directory" 입력

2. **앱 등록 메뉴**
   - 왼쪽 메뉴에서 "앱 등록(App registrations)" 클릭
   - "새 등록(New registration)" 클릭

3. **앱 정보 입력**
   ```
   이름: RAG-SPO-Backend
   지원되는 계정 유형: 이 조직 디렉터리의 계정만
   리디렉션 URI: (비워둠)
   ```

4. **"등록" 클릭**

### Step 5: 앱 ID 확인

앱이 생성되면 "개요(Overview)" 페이지에서:

```
애플리케이션(클라이언트) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
디렉터리(테넌트) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

📋 **메모장에 복사해두세요!**

### Step 6: 클라이언트 시크릿 생성

1. **왼쪽 메뉴에서 "인증서 및 비밀" 클릭**

2. **"클라이언트 비밀" 탭 선택**

3. **"+ 새 클라이언트 암호" 클릭**

4. **정보 입력**
   ```
   설명: RAG-SPO Backend Secret
   만료: 24개월 (권장)
   ```

5. **"추가" 클릭**

6. **⚠️ 중요! 즉시 "값(Value)" 복사**
   ```
   값: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   - **지금 복사하지 않으면 다시 볼 수 없습니다!**
   - 메모장에 안전하게 저장

### Step 7: API 권한 부여 ⭐

1. **왼쪽 메뉴에서 "API 권한" 클릭**

2. **"+ 권한 추가" 클릭**

3. **"Microsoft Graph" 선택**

4. **"애플리케이션 권한(Application permissions)" 선택**
   - ❌ "위임된 권한" 아님!

5. **필요한 권한 검색 및 체크**
   
   검색: `Sites`
   - ✅ `Sites.Read.All` 체크
   
   검색: `Files`
   - ✅ `Files.Read.All` 체크

6. **"권한 추가" 클릭**

7. **⭐ 관리자 동의 허용**
   - "... 에 대한 관리자 동의 허용" 버튼 클릭
   - "예" 클릭
   - 상태가 녹색 체크 표시로 변경되는지 확인

### Step 8: .env 파일 설정

`backend/.env` 파일 생성 및 입력:

```env
# 데모 모드 비활성화 (실제 SharePoint 사용)
DEMO_MODE=False

# Step 5에서 복사한 값들
TENANT_ID=복사한-테넌트-ID
CLIENT_ID=복사한-클라이언트-ID
CLIENT_SECRET=복사한-클라이언트-시크릿

# SharePoint Site ID (아래에서 확인)
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

---

## 🔍 SharePoint Site ID 찾기

### ⚡ 자동 생성되는 것들

Microsoft 365 Developer Program에서 **"샘플 데이터 포함"** 선택 시:

| 항목 | 자동 생성? | 조회 방법 |
|------|-----------|----------|
| SharePoint 사이트 | ✅ 자동 생성 | 브라우저로 접속 가능 |
| 샘플 문서 | ✅ 자동 생성 | 사이트에서 확인 가능 |
| **Site ID** | ❌ 수동 조회 필요 | 아래 방법 사용 |

### 방법 1: Python 스크립트 사용 (가장 쉬움! ⭐)

**우리가 만든 도구 사용:**

```bash
cd backend

# 1. .env 파일에 Azure AD 정보 입력 (DEMO_MODE=False)
# 2. 스크립트 실행
python scripts/get_site_id.py
```

**출력 예시:**
```
🔍 SharePoint Site ID 조회 도구
================================================

✅ 총 2개의 사이트를 찾았습니다.

사이트 #1: Communication site
🔑 Site ID: yourname.sharepoint.com,abc123...,def456...
🌐 URL: https://yourname.sharepoint.com/sites/contoso
📝 설명: Sample communication site

💡 추천
첫 번째 사이트를 사용하는 것을 추천합니다:

.env 파일에 다음과 같이 추가하세요:
SHAREPOINT_SITE_ID=yourname.sharepoint.com,abc123...,def456...
```

**특정 사이트만 조회:**
```bash
python scripts/get_site_id.py /sites/contoso
```

### 방법 2: Graph Explorer 사용 (웹 브라우저)

1. **Graph Explorer 열기**
   ```
   https://developer.microsoft.com/en-us/graph/graph-explorer
   ```

2. **개발자 계정으로 로그인**
   ```
   admin@yourname.onmicrosoft.com
   ```

3. **권한 동의**
   - "Modify permissions" 클릭
   - `Sites.Read.All` 체크 후 동의

4. **사이트 목록 조회**
   ```
   GET https://graph.microsoft.com/v1.0/sites?search=*
   ```

5. **"Run query" 클릭**

6. **응답에서 `id` 복사**
   ```json
   {
     "value": [
       {
         "id": "yourname.sharepoint.com,12345678-1234...",
         "displayName": "Communication site",
         "webUrl": "https://yourname.sharepoint.com/sites/contoso"
       }
     ]
   }
   ```

### 방법 3: PowerShell 사용 (Windows)

```powershell
# 1. 토큰 발급
$tenantId = "your-tenant-id"
$clientId = "your-client-id"
$clientSecret = "your-client-secret"

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

# 2. 사이트 목록 조회
$headers = @{
    Authorization = "Bearer $token"
}

$sites = Invoke-RestMethod -Method Get `
    -Uri "https://graph.microsoft.com/v1.0/sites?search=*" `
    -Headers $headers

# 3. 사이트 정보 출력
$sites.value | ForEach-Object {
    Write-Host "사이트: $($_.displayName)"
    Write-Host "Site ID: $($_.id)"
    Write-Host "URL: $($_.webUrl)"
    Write-Host ""
}
```

---

## ✅ 설정 확인

### 1. 토큰 발급 테스트

PowerShell에서:

```powershell
$tenantId = "your-tenant-id"
$clientId = "your-client-id"
$clientSecret = "your-client-secret"

$body = @{
    client_id     = $clientId
    scope         = "https://graph.microsoft.com/.default"
    client_secret = $clientSecret
    grant_type    = "client_credentials"
}

$response = Invoke-RestMethod -Method Post -Uri "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" -Body $body

$response.access_token
```

성공하면 긴 토큰 문자열이 출력됩니다!

### 2. Graph API 호출 테스트

```powershell
$token = $response.access_token
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Method Get -Uri "https://graph.microsoft.com/v1.0/sites" -Headers $headers
```

사이트 목록이 출력되면 성공! 🎉

---

## 🎓 다음 단계

설정이 완료되면:

1. ✅ `backend/.env` 파일 확인
2. ✅ Qdrant 실행
3. ✅ 앱 실행: `python -m app.main`
4. ✅ 인덱싱: `python scripts/run_indexing.py`
5. ✅ 검색 테스트: `python scripts/test_search.py`

---

## ❓ FAQ

### Q1: Developer Program 계정이 만료되나요?
A: 90일 후 자동 만료되지만, **활동이 있으면 자동 연장**됩니다!
- API 호출
- 로그인
- 테넌트 사용

### Q2: 실제 프로덕션에 사용할 수 있나요?
A: Developer Program은 **개발 및 테스트 전용**입니다.
- 프로덕션: 회사 계정 또는 유료 Microsoft 365 사용

### Q3: 샘플 데이터는 어디에 있나요?
A: SharePoint 사이트는 자동 생성됩니다:
```
https://yourname.sharepoint.com/sites/contoso
```

### Q4: 권한이 거부되었습니다
A: 다음을 확인하세요:
1. API 권한에서 "관리자 동의" 허용했는지
2. 애플리케이션 권한 (위임된 권한 아님)
3. 토큰 재발급

### Q5: 회사 계정으로 가입했는데 권한이 없어요
A: 개인 Microsoft 계정(Outlook.com)으로 새로 가입하세요!

---

## 📚 참고 자료

- [Microsoft 365 Developer Program](https://developer.microsoft.com/microsoft-365/dev-program)
- [Graph API 인증 문서](https://learn.microsoft.com/en-us/graph/auth-v2-service)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Azure AD 앱 등록](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

---

## 🆘 도움이 필요하신가요?

문제가 발생하면:
1. DEMO_GUIDE.md의 데모 모드로 먼저 테스트
2. GitHub Issues에 질문 남기기
3. Microsoft Learn Q&A 커뮤니티 활용

즐거운 개발 되세요! 🚀

