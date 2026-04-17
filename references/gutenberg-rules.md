# Gutenberg Block Rules (Reference)

기존 `wp-blog-post` 스킬의 규칙을 Evaluator가 기계 검사하기 위해 정규화한 문서.
위반 시 "unexpected content" 또는 "invalid block content" 오류가 블록 에디터에서 발생.

---

## Rule 1: `wp:group` 내부 모든 HTML 요소는 개별 블록 주석 필수

| 요소 | 필수 블록 주석 |
|---|---|
| `<h1>`–`<h6>` | `<!-- wp:heading {"level":N} -->` |
| `<p>` | `<!-- wp:paragraph -->` |
| `<ul>` | `<!-- wp:list -->` |
| `<ol>` | `<!-- wp:list {"ordered":true} -->` |
| `<img>` (wrapper `<figure>` 포함) | `<!-- wp:image -->` |
| `<pre>` 코드 | `<!-- wp:code -->` 또는 `<!-- wp:preformatted -->` |

## Rule 2: 리스트 아이템은 `wp:list-item` 래핑 (WordPress 6.0+)

```html
<!-- wp:list -->
<ul class="wp-block-list">
  <!-- wp:list-item -->
  <li>Item</li>
  <!-- /wp:list-item -->
  <!-- wp:list-item -->
  <li>Item</li>
  <!-- /wp:list-item -->
</ul>
<!-- /wp:list -->
```

`<li>`가 wp:list-item 래핑 없이 등장하면 오류.

## Rule 3: 헤딩은 class 필수, level 속성 필수

```html
<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Title</h2>
<!-- /wp:heading -->
```

- `class="wp-block-heading"` 빠지면 오류.
- 블록 주석 JSON에 `"level": N` 빠지면 기본 h2로 렌더되어 문서 구조 오염.

## Rule 4: `wp:group` 안에 raw HTML 직접 배치 금지

```html
<!-- WRONG -->
<!-- wp:group -->
<div class="wp-block-group">
  <h4>Title</h4>
  <ul><li>item</li></ul>
</div>
<!-- /wp:group -->

<!-- CORRECT -->
<!-- wp:group -->
<div class="wp-block-group">
  <!-- wp:heading {"level":4} -->
  <h4 class="wp-block-heading">Title</h4>
  <!-- /wp:heading -->
  <!-- wp:list -->
  <ul class="wp-block-list">
    <!-- wp:list-item -->
    <li>item</li>
    <!-- /wp:list-item -->
  </ul>
  <!-- /wp:list -->
</div>
<!-- /wp:group -->
```

## Rule 5: Mermaid 인라인 절대 금지

```html
<!-- ABSOLUTELY WRONG — does not render -->
<pre class="mermaid">
flowchart LR
  A --> B
</pre>
```

반드시 `.mmd` 파일 작성 → `mmdc`로 PNG 렌더 → `wp:image` 블록:

```html
<!-- wp:image {"id":MEDIA_ID,"sizeSlug":"full"} -->
<figure class="wp-block-image size-full">
  <img src="MEDIA_URL" alt="diagram description" class="wp-image-MEDIA_ID"/>
  <figcaption class="wp-element-caption">Caption</figcaption>
</figure>
<!-- /wp:image -->
```

드래프트 단계에서 MEDIA_ID/URL 미정이면 플레이스홀더 사용:

```html
<!-- wp:image -->
<figure class="wp-block-image size-full">
  <img src="{{ASSET:diagram_1.png}}" alt="..."/>
</figure>
<!-- /wp:image -->
```

사용자 승인 후 `upload_media.py` 실행 결과로 치환.

## Rule 6: 코드 블록 언어 태그

```html
<!-- wp:code {"language":"python"} -->
<pre class="wp-block-code"><code class="language-python">
def example():
    pass
</code></pre>
<!-- /wp:code -->
```

언어 태그 빠지면 syntax highlighting 작동 안 함 → Craft 감점.

## Rule 7: 표 블록

```html
<!-- wp:table -->
<figure class="wp-block-table">
  <table>
    <thead>
      <tr><th>A</th><th>B</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>2</td></tr>
    </tbody>
  </table>
  <figcaption>Caption</figcaption>
</figure>
<!-- /wp:table -->
```

---

## Evaluator Detection Patterns (의사코드)

```python
# 1. wp:group 내부 raw HTML 검출
content = open("post_vN.html").read()
violations = []
# 간단한 스캔: wp:group 블록 스코프를 추적하며 내부에서 wp:heading/wp:paragraph 주석 없이 등장한 태그 기록
# (실제 구현은 HTML 파서 기반)

# 2. heading class 검증
import re
for m in re.finditer(r'<h([1-6])([^>]*)>', content):
    if 'class="wp-block-heading"' not in m.group(0):
        violations.append(("heading class missing", m.start()))

# 3. li 래핑 검증
lis = list(re.finditer(r'<li[^>]*>', content))
list_items = list(re.finditer(r'<!-- wp:list-item -->', content))
if len(lis) > len(list_items):
    violations.append(("li without wp:list-item wrapping", None))

# 4. 인라인 Mermaid 검출
if re.search(r'<pre[^>]*class="mermaid"', content):
    violations.append(("inline mermaid", ...))  # Hard fail
```

Evaluator는 이러한 검출을 실행하고 위반 라인을 `critique.md`에 전수 기록한다.

---

## KO 종결어미 검출 (Craft 기준)

```python
# 종결어미 뒤 마침표 누락 검출
pattern = r'(다|했다|된다|있다|없다|한다|이다|봤다|됐다|쳤다|왔다|갔다)(?=[\s\n])(?!\.)'
# 매칭된 각 위치가 문장 끝인지 확인(다음 토큰이 공백/개행이고 바로 다음이 소문자 영문이 아닌 경우)
```

KO 포스트에서 이 패턴 매치가 1건이라도 있으면 Craft Hard fail.
