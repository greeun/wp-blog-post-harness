#!/usr/bin/env python3
"""
워드프레스 REST API를 사용하여 미디어 파일을 업로드합니다.

환경변수 필요:
  - WP_SITE_URL: 워드프레스 사이트 URL (https://your-site.com)
  - WP_USERNAME: 워드프레스 사용자명
  - WP_APP_PASSWORD: 애플리케이션 비밀번호
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_credentials():
    """환경변수에서 워드프레스 인증 정보를 가져옵니다."""
    site_url = os.environ.get("WP_SITE_URL", "").rstrip("/")
    username = os.environ.get("WP_USERNAME", "")
    app_password = os.environ.get("WP_APP_PASSWORD", "")

    if not all([site_url, username, app_password]):
        missing = []
        if not site_url:
            missing.append("WP_SITE_URL")
        if not username:
            missing.append("WP_USERNAME")
        if not app_password:
            missing.append("WP_APP_PASSWORD")
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return site_url, username, app_password


def make_auth_header(username: str, app_password: str) -> str:
    """Basic 인증 헤더를 생성합니다."""
    credentials = f"{username}:{app_password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def upload_media(file_path: str, alt_text: str = None, caption: str = None) -> dict:
    """워드프레스에 미디어 파일을 업로드합니다."""
    site_url, username, app_password = get_credentials()
    auth_header = make_auth_header(username, app_password)

    file_path = Path(file_path)
    if not file_path.exists():
        return {
            "success": False,
            "error": f"File not found: {file_path}",
        }

    # MIME 타입 추정
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        mime_type = "application/octet-stream"

    # 파일 읽기
    file_data = file_path.read_bytes()
    filename = file_path.name

    # API 요청
    api_url = f"{site_url}/wp-json/wp/v2/media"

    req = Request(
        api_url,
        data=file_data,
        headers={
            "Authorization": auth_header,
            "Content-Type": mime_type,
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
        method="POST",
    )

    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode())
            media_id = result["id"]

            # alt_text나 caption 업데이트가 필요하면 추가 요청
            if alt_text or caption:
                update_data = {}
                if alt_text:
                    update_data["alt_text"] = alt_text
                if caption:
                    update_data["caption"] = caption

                update_url = f"{site_url}/wp-json/wp/v2/media/{media_id}"
                update_req = Request(
                    update_url,
                    data=json.dumps(update_data).encode(),
                    headers={
                        "Authorization": auth_header,
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
                with urlopen(update_req) as update_response:
                    result = json.loads(update_response.read().decode())

            return {
                "success": True,
                "id": result["id"],
                "url": result["source_url"],
                "link": result["link"],
                "mime_type": result["mime_type"],
            }

    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        return {
            "success": False,
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_body,
        }
    except URLError as e:
        return {
            "success": False,
            "error": str(e.reason),
        }


def main():
    parser = argparse.ArgumentParser(description="워드프레스 미디어 업로드")
    parser.add_argument("--file", required=True, help="업로드할 파일 경로")
    parser.add_argument("--alt-text", help="이미지 대체 텍스트")
    parser.add_argument("--caption", help="미디어 캡션")

    args = parser.parse_args()

    result = upload_media(
        file_path=args.file,
        alt_text=args.alt_text,
        caption=args.caption,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
