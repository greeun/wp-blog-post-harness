#!/usr/bin/env python3
"""
마크다운을 워드프레스 호환 HTML로 변환합니다.
외부 라이브러리 없이 기본적인 변환만 수행합니다.
"""

import argparse
import re
import sys
from pathlib import Path


def convert_code_blocks(text: str) -> str:
    """코드 블록을 Gutenberg 형식으로 변환"""
    # ```language 형식의 코드 블록
    pattern = r'```(\w+)?\n(.*?)```'

    def replace_code(match):
        lang = match.group(1) or ""
        code = match.group(2).rstrip()
        # HTML 이스케이프
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if lang:
            return f'<!-- wp:code {{"language":"{lang}"}} -->\n<pre class="wp-block-code"><code>{code}</code></pre>\n<!-- /wp:code -->'
        else:
            return f'<!-- wp:code -->\n<pre class="wp-block-code"><code>{code}</code></pre>\n<!-- /wp:code -->'

    return re.sub(pattern, replace_code, text, flags=re.DOTALL)


def convert_inline_code(text: str) -> str:
    """인라인 코드 변환"""
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', text)


def convert_headers(text: str) -> str:
    """헤더 변환"""
    # H1-H6
    for i in range(6, 0, -1):
        pattern = r'^' + '#' * i + r' (.+)$'
        replacement = f'<h{i}>\\1</h{i}>'
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text


def convert_bold_italic(text: str) -> str:
    """굵은 글씨와 이탤릭 변환"""
    # Bold + Italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def convert_links(text: str) -> str:
    """링크 변환"""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)


def convert_images(text: str) -> str:
    """이미지 변환"""
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def replace_image(match):
        alt = match.group(1)
        src = match.group(2)
        return f'''<!-- wp:image -->
<figure class="wp-block-image"><img src="{src}" alt="{alt}"/></figure>
<!-- /wp:image -->'''

    return re.sub(pattern, replace_image, text)


def convert_lists(text: str) -> str:
    """리스트 변환 (단순 버전)"""
    lines = text.split('\n')
    result = []
    in_ul = False
    in_ol = False

    for line in lines:
        # 비순서 리스트
        if re.match(r'^[-*] ', line):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            content = re.sub(r'^[-*] ', '', line)
            result.append(f'  <li>{content}</li>')
        # 순서 리스트
        elif re.match(r'^\d+\. ', line):
            if not in_ol:
                result.append('<ol>')
                in_ol = True
            content = re.sub(r'^\d+\. ', '', line)
            result.append(f'  <li>{content}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)

    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')

    return '\n'.join(result)


def convert_paragraphs(text: str) -> str:
    """단락 변환"""
    # 이미 변환된 wp:code 블록은 본문에 빈 줄이 있을 수 있으므로
    # 플레이스홀더로 보호한 뒤 '\n\n' 기준 단락 분리를 하고 마지막에 복원한다.
    # (보호하지 않으면 코드 블록 내부의 빈 줄에서 블록이 쪼개져 뒷조각이
    #  <p>로 감싸지고 Gutenberg 오류를 유발한다.)
    placeholders = {}

    def protect(match):
        key = f"\x00CODEBLOCK{len(placeholders)}\x00"
        placeholders[key] = match.group(0)
        return key

    code_pattern = (
        r'<!-- wp:code(?: \{[^}]*\})? -->\n'
        r'<pre class="wp-block-code"><code>.*?</code></pre>\n'
        r'<!-- /wp:code -->'
    )
    text = re.sub(code_pattern, protect, text, flags=re.DOTALL)

    lines = text.split('\n\n')
    result = []

    for block in lines:
        block = block.strip()
        if not block:
            continue
        # 보호된 코드 블록 플레이스홀더는 그대로 복원
        if block in placeholders:
            result.append(placeholders[block])
            continue
        # 이미 HTML 태그로 시작하면 건너뜀
        if re.match(r'^<[a-z]', block) or re.match(r'^<!--', block):
            result.append(block)
        else:
            # 여러 줄 블록은 <br>로 연결
            block = block.replace('\n', '<br>\n')
            result.append(f'<p>{block}</p>')

    return '\n\n'.join(result)


def markdown_to_html(markdown: str) -> str:
    """마크다운을 HTML로 변환"""
    html = markdown

    # 변환 순서가 중요
    html = convert_code_blocks(html)
    html = convert_images(html)
    html = convert_links(html)
    html = convert_headers(html)
    html = convert_bold_italic(html)
    html = convert_inline_code(html)
    html = convert_lists(html)
    html = convert_paragraphs(html)

    return html


def main():
    parser = argparse.ArgumentParser(description="마크다운을 워드프레스 HTML로 변환")
    parser.add_argument("--input", "-i", required=True, help="입력 마크다운 파일")
    parser.add_argument("--output", "-o", help="출력 HTML 파일 (기본: stdout)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    markdown = input_path.read_text(encoding="utf-8")
    html = markdown_to_html(markdown)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(html, encoding="utf-8")
        print(f"Converted: {args.input} -> {args.output}")
    else:
        print(html)


if __name__ == "__main__":
    main()
