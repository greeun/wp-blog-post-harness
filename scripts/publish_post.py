#!/usr/bin/env python3
"""
워드프레스 REST API를 사용하여 블로그 포스트를 발행합니다.

환경변수 필요:
  - WP_SITE_URL: 워드프레스 사이트 URL (https://your-site.com)
  - WP_USERNAME: 워드프레스 사용자명
  - WP_APP_PASSWORD: 애플리케이션 비밀번호
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote


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


def get_or_create_category(site_url: str, auth_header: str, category_name: str) -> int:
    """카테고리 ID를 가져오거나 새로 생성합니다."""
    # 기존 카테고리 검색
    search_url = f"{site_url}/wp-json/wp/v2/categories?search={quote(category_name)}"
    req = Request(search_url, headers={"Authorization": auth_header})

    try:
        with urlopen(req) as response:
            categories = json.loads(response.read().decode())
            for cat in categories:
                if cat["name"].lower() == category_name.lower():
                    return cat["id"]
    except HTTPError:
        pass

    # 새 카테고리 생성
    create_url = f"{site_url}/wp-json/wp/v2/categories"
    data = json.dumps({"name": category_name}, ensure_ascii=False).encode("utf-8")
    req = Request(
        create_url,
        data=data,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result["id"]
    except HTTPError as e:
        print(f"Warning: Could not create category '{category_name}': {e}", file=sys.stderr)
        return None


def get_or_create_tag(site_url: str, auth_header: str, tag_name: str) -> int:
    """태그 ID를 가져오거나 새로 생성합니다."""
    # 기존 태그 검색
    search_url = f"{site_url}/wp-json/wp/v2/tags?search={quote(tag_name)}"
    req = Request(search_url, headers={"Authorization": auth_header})

    try:
        with urlopen(req) as response:
            tags = json.loads(response.read().decode())
            for tag in tags:
                if tag["name"].lower() == tag_name.lower():
                    return tag["id"]
    except HTTPError:
        pass

    # 새 태그 생성
    create_url = f"{site_url}/wp-json/wp/v2/tags"
    data = json.dumps({"name": tag_name}, ensure_ascii=False).encode("utf-8")
    req = Request(
        create_url,
        data=data,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result["id"]
    except HTTPError as e:
        print(f"Warning: Could not create tag '{tag_name}': {e}", file=sys.stderr)
        return None


def publish_post(
    title: str,
    content: str,
    status: str = "draft",
    categories: list = None,
    tags: list = None,
    featured_media: int = None,
) -> dict:
    """워드프레스에 포스트를 발행합니다."""
    site_url, username, app_password = get_credentials()
    auth_header = make_auth_header(username, app_password)

    # 카테고리 ID 변환
    category_ids = []
    if categories:
        for cat_name in categories:
            cat_id = get_or_create_category(site_url, auth_header, cat_name.strip())
            if cat_id:
                category_ids.append(cat_id)

    # 태그 ID 변환
    tag_ids = []
    if tags:
        for tag_name in tags:
            tag_id = get_or_create_tag(site_url, auth_header, tag_name.strip())
            if tag_id:
                tag_ids.append(tag_id)

    # 포스트 데이터 구성
    post_data = {
        "title": title,
        "content": content,
        "status": status,
    }

    if category_ids:
        post_data["categories"] = category_ids
    if tag_ids:
        post_data["tags"] = tag_ids
    if featured_media:
        post_data["featured_media"] = featured_media

    # API 요청
    api_url = f"{site_url}/wp-json/wp/v2/posts"
    data = json.dumps(post_data, ensure_ascii=False).encode("utf-8")

    req = Request(
        api_url,
        data=data,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode())
            return {
                "success": True,
                "id": result["id"],
                "link": result["link"],
                "status": result["status"],
                "edit_link": f"{site_url}/wp-admin/post.php?post={result['id']}&action=edit",
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
    parser = argparse.ArgumentParser(description="워드프레스 블로그 포스트 발행")
    parser.add_argument("--title", required=True, help="포스트 제목")
    parser.add_argument("--content", help="포스트 내용 (HTML)")
    parser.add_argument("--content-file", help="포스트 내용이 담긴 파일 경로")
    parser.add_argument(
        "--status",
        choices=["draft", "publish", "pending", "private"],
        default="draft",
        help="발행 상태 (기본: draft)",
    )
    parser.add_argument("--categories", help="카테고리 (쉼표 구분)")
    parser.add_argument("--tags", help="태그 (쉼표 구분)")
    parser.add_argument("--featured-media", type=int, help="대표 이미지 미디어 ID")

    args = parser.parse_args()

    # 콘텐츠 가져오기
    if args.content_file:
        content_path = Path(args.content_file)
        if not content_path.exists():
            print(f"Error: Content file not found: {args.content_file}", file=sys.stderr)
            sys.exit(1)
        content = content_path.read_text(encoding="utf-8")
    elif args.content:
        content = args.content
    else:
        print("Error: Either --content or --content-file is required", file=sys.stderr)
        sys.exit(1)

    # 카테고리/태그 파싱
    categories = args.categories.split(",") if args.categories else None
    tags = args.tags.split(",") if args.tags else None

    # 포스트 발행
    result = publish_post(
        title=args.title,
        content=content,
        status=args.status,
        categories=categories,
        tags=tags,
        featured_media=args.featured_media,
    )

    # 결과 출력
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
