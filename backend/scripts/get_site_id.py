"""Script to retrieve SharePoint Site ID using Microsoft Graph API.

This script helps you find the Site ID for your SharePoint site,
which is required for the RAG-SPO application.
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from typing import Optional

from app.config import get_settings


def get_access_token_real() -> str:
    """Get real access token from Microsoft Graph API.
    
    Returns:
        str: Access token for Graph API.
        
    Raises:
        Exception: If authentication fails.
    """
    settings = get_settings()
    
    token_url = f"https://login.microsoftonline.com/{settings.tenant_id}/oauth2/v2.0/token"
    
    data = {
        "client_id": settings.client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": settings.client_secret,
        "grant_type": "client_credentials",
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting access token: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        sys.exit(1)


def list_all_sites(token: str) -> None:
    """List all SharePoint sites in the tenant.
    
    Args:
        token: Access token for Graph API.
    """
    print("\n" + "=" * 70)
    print("📋 모든 SharePoint 사이트 목록")
    print("=" * 70)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    try:
        # Method 1: Search for all sites
        url = "https://graph.microsoft.com/v1.0/sites?search=*"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        sites = response.json().get("value", [])
        
        if not sites:
            print("\n⚠️  사이트를 찾을 수 없습니다.")
            print("샌드박스 생성 시 '샘플 데이터 포함' 옵션을 선택했는지 확인하세요.")
            return
        
        print(f"\n✅ 총 {len(sites)}개의 사이트를 찾았습니다.\n")
        
        for idx, site in enumerate(sites, 1):
            print(f"{'─' * 70}")
            print(f"사이트 #{idx}: {site.get('displayName', 'N/A')}")
            print(f"{'─' * 70}")
            print(f"🔑 Site ID: {site.get('id', 'N/A')}")
            print(f"🌐 URL: {site.get('webUrl', 'N/A')}")
            print(f"📝 설명: {site.get('description', 'N/A')}")
            print()
        
        # Provide recommendation
        print("=" * 70)
        print("💡 추천")
        print("=" * 70)
        if sites:
            recommended_site = sites[0]
            print(f"\n첫 번째 사이트를 사용하는 것을 추천합니다:")
            print(f"\n사이트 이름: {recommended_site.get('displayName')}")
            print(f"Site ID: {recommended_site.get('id')}")
            print(f"\n.env 파일에 다음과 같이 추가하세요:")
            print(f"\nSHAREPOINT_SITE_ID={recommended_site.get('id')}")
            print()
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error listing sites: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        sys.exit(1)


def get_site_by_url(token: str, site_url: str) -> None:
    """Get specific site information by URL.
    
    Args:
        token: Access token for Graph API.
        site_url: SharePoint site URL (e.g., /sites/contoso).
    """
    print("\n" + "=" * 70)
    print(f"🔍 특정 사이트 조회: {site_url}")
    print("=" * 70)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    try:
        # Extract hostname and path
        # Example: https://yourname.sharepoint.com/sites/contoso
        # → hostname: yourname.sharepoint.com
        # → path: /sites/contoso
        
        settings = get_settings()
        
        # Construct the Graph API URL
        # Format: /sites/{hostname}:{path}
        url = f"https://graph.microsoft.com/v1.0/sites/{settings.tenant_id.split('.')[0]}.sharepoint.com:{site_url}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        site = response.json()
        
        print(f"\n✅ 사이트를 찾았습니다!\n")
        print(f"{'─' * 70}")
        print(f"사이트 이름: {site.get('displayName', 'N/A')}")
        print(f"{'─' * 70}")
        print(f"🔑 Site ID: {site.get('id', 'N/A')}")
        print(f"🌐 URL: {site.get('webUrl', 'N/A')}")
        print(f"📝 설명: {site.get('description', 'N/A')}")
        print()
        
        print("=" * 70)
        print(".env 파일에 추가:")
        print("=" * 70)
        print(f"\nSHAREPOINT_SITE_ID={site.get('id')}")
        print()
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting site: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        print("\n💡 Tip: URL 형식을 확인하세요 (예: /sites/contoso)")
        sys.exit(1)


def main() -> None:
    """Main function to retrieve SharePoint Site ID.
    
    This function authenticates with Microsoft Graph API and retrieves
    SharePoint site information.
    """
    print("=" * 70)
    print("🔍 SharePoint Site ID 조회 도구")
    print("=" * 70)
    
    settings = get_settings()
    
    # Check if demo mode
    if settings.demo_mode:
        print("\n⚠️  데모 모드가 활성화되어 있습니다.")
        print("실제 SharePoint Site ID를 조회하려면 .env 파일에서:")
        print("DEMO_MODE=False")
        print("로 변경하고 실제 Azure AD 정보를 입력하세요.\n")
        sys.exit(1)
    
    # Validate settings
    if settings.tenant_id == "demo-tenant-id":
        print("\n⚠️  .env 파일에 실제 Azure AD 정보를 입력해주세요.")
        print("\nTENANT_ID=your-actual-tenant-id")
        print("CLIENT_ID=your-actual-client-id")
        print("CLIENT_SECRET=your-actual-client-secret")
        print("\n자세한 설명: AZURE_SETUP.md 참고\n")
        sys.exit(1)
    
    print("\n1️⃣  Microsoft Graph API 인증 중...")
    try:
        token = get_access_token_real()
        print("✅ 인증 성공!\n")
    except Exception as e:
        print(f"❌ 인증 실패: {e}")
        print("\n.env 파일의 TENANT_ID, CLIENT_ID, CLIENT_SECRET을 확인하세요.")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        site_url = sys.argv[1]
        get_site_by_url(token, site_url)
    else:
        print("2️⃣  SharePoint 사이트 목록 조회 중...")
        list_all_sites(token)
    
    print("=" * 70)
    print("✅ 완료!")
    print("=" * 70)
    print("\n다음 단계:")
    print("1. 위에서 출력된 Site ID를 복사")
    print("2. backend/.env 파일 열기")
    print("3. SHAREPOINT_SITE_ID=<복사한-ID> 입력")
    print("4. 저장 후 앱 재시작\n")


if __name__ == "__main__":
    main()

