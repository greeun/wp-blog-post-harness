# Grading Rubric

각 기준은 1–5점. **2× 가중 기준은 Claude의 기본값이 약한 축**을 의미한다.
통과: 가중 평균 ≥ 4.0 AND 모든 기준 ≥ 3 AND Hard fail 0.

## 1. Content depth & structure (weight 1×)

| 점수 | 기준 |
|---|---|
| 5 | TL;DR → 배경 → 구현 → 문제해결 → 결과가 한 덩어리로 읽히고, 각 섹션이 이전을 전제로 다음을 심화. 한 번 읽으면 독자가 같은 문제를 재현할 수 있음. |
| 4 | 논리 연결 명확, 주요 섹션 모두 충실. 1–2곳에서 전개가 평평. |
| 3 | 섹션 순서는 맞으나 한 섹션이 얕거나 타 섹션 반복. |
| 2 | 구조 혼재, TL;DR이 본문과 괴리. |
| 1 | 단락 모음. 논리 흐름 없음. |

## 2. Originality & technical specificity (weight 2×) ★

Claude가 기본값에서 약한 영역. 2× 가중.

| 점수 | 기준 |
|---|---|
| 5 | 이 작업·이 코드베이스·이 에러에만 고유한 디테일. 다른 블로그에서 볼 수 없는 관점. Insight angle이 본문을 관통. |
| 4 | 구체적 세부사항 다수. 제시된 주장이 일반론이 아님. |
| 3 | 대부분 구체적이나 1–2개 섹션은 일반 튜토리얼처럼 들림. |
| 2 | 주장은 있으나 증거가 가짜 코드 또는 범용 예제. |
| 1 | "AI가 세상을 바꾼다" 수준. 검색 리플리카. |

**Hard floor**: "바야흐로", "오늘날 빠르게 변화하는", "In today's fast-paced world",
"이번 포스트에서는 ~에 대해 알아보겠습니다" 형태의 오프닝이 있으면 최대 3점.

## 3. Visual completeness (weight 2×) ★

Area where Claude is weak by default (tends to replace visuals with text). Weighted 2×.
**Infographic-first**: visuals are the primary delivery vehicle so the post structure and every
explanation are graspable at a glance. Top-score criterion: "Can the post be understood by
skimming the images alone?" All visuals must be **plugin-independent static images** (PNG/JPG/SVG)
embedded via core `wp:image` — no inline Mermaid, shortcodes, or JS chart libraries.

| Score | Criterion |
|---|---|
| 5 | Most major sections carry their own visual (≥3 total). **Diverse types** (e.g. mind map + flowchart + chart/graph + table, or webtoon/illustration, timeline, quadrant). Each compresses/replaces a body paragraph; the type list is not exhaustive — fitting open-ended creative visuals also count. |
| 4 | ≥2 visuals, complex concepts properly diagrammed, ≥2 distinct types mixed, alt text complete. |
| 3 | 2 visuals but monotone in type (same diagram/table repeated) or one is decorative (table just re-states body text). |
| 2 | Only 1 visual. |
| 1 | None. Or inline `<pre class="mermaid">` used (plugin-dependent). |

**Hard floor**: fewer than 2 PNGs in `assets/` → auto score 1 + Hard fail.
**Diversity floor**: if all visuals are the same type (e.g. 3 tables) → max score 3; ≥2 distinct
types (mind map / flowchart / chart / architecture / timeline / sequence / webtoon-illustration)
required for score 4+.
**Plugin-dependency floor**: any inline Mermaid, chart/diagram shortcode, plugin-specific block,
or JS-injected chart in the post body → auto score 1 + Hard fail.

## 4. Gutenberg validity (weight 1×)

| 점수 | 기준 |
|---|---|
| 5 | 모든 블록 주석 정확, wp:group 내부 전부 블록 래핑, heading class 전부 존재, list-item 전부 래핑. |
| 4 | 1–2곳 사소한 누락(class 빠짐 등), 블록 오류 없음. |
| 3 | 블록 오류는 없으나 다수 헤딩 class 누락 등. |
| 2 | 블록 구조 1건 위반 — "unexpected content" 잠재. |
| 1 | 다수 블록 규칙 위반. |

**Hard floor**: 블록 규칙 위반 1건이라도 있으면 1점 + Hard fail.

## 5. Metadata fit (weight 1×)

| 점수 | 기준 |
|---|---|
| 5 | 카테고리 1–2개(전부 기존 재사용), 태그 7–10개(모두 본문에 실제 등장한 기술), SEO 제목 구체·50–65자. |
| 4 | 카테고리·태그 적절. SEO 제목 일부 일반어. |
| 3 | 카테고리가 신규 생성인데 사유가 충분. 태그 5–6개. |
| 2 | 카테고리 신규 생성 사유 없음, 또는 태그 3–4개. |
| 1 | 카테고리·태그 미작성, 또는 태그 10개 초과. |

**Hard floor**: 태그 5개 미만 또는 10개 초과 → 1점 + Hard fail.

## 6. Craft (weight 1×)

| 점수 | 기준 |
|---|---|
| 5 | 모든 코드 블록 언어 태그, KO 종결어미 마침표 100%, 오탈자 0, 어조 일관, 모바일 가독성(단락 3–4줄) 준수. |
| 4 | 1–2곳 마침표 누락 또는 언어 태그 누락. |
| 3 | 다수 마침표 누락 또는 오탈자 2–3개. |
| 2 | 스타일 불일치 반복. |
| 1 | 교정 없이 토해낸 초안. |

**Hard floor**: KO 종결어미 마침표 누락 1건 이상 → 1점 + Hard fail.

---

## 가중 평균 계산식

```
weighted_avg = (c1 + 2×c2 + 2×c3 + c4 + c5 + c6) / 8
```

- c1: Content depth & structure (1×)
- c2: Originality & tech specificity (2×) ★
- c3: Visual completeness (2×) ★
- c4: Gutenberg validity (1×)
- c5: Metadata fit (1×)
- c6: Craft (1×)

### 통과 조건 (3단계 floor + 가중 평균, 모두 만족해야 PASS)

1. **2× floor**: `c2 ≥ 4` AND `c3 ≥ 4`
   Claude의 약점 축(Originality, Visual completeness)은 타 기준의 평균으로 상쇄 불가.
   이 둘 중 하나라도 3 이하면 타 기준 점수와 무관하게 **즉시 FAIL**.
2. **1× floor**: `min(c1, c4, c5, c6) ≥ 3`
   단일 기준이 2 이하면 가중 평균이 4.0을 넘더라도 **즉시 FAIL**.
3. **가중 평균 floor**: `weighted_avg ≥ 4.0`
4. **Hard fail trigger 0건** (각 기준 하단 Hard floor 참조).

위 네 조건 중 하나라도 어기면 Evaluator는 PASS를 선언할 수 없다. 가중 평균 4.0이
넘더라도 Originality 3점이면 무조건 반려된다.

---

## Rubric Wording Leakage 경고 (원문 V1 교훈)

원문의 **핵심 메타 교훈**: 루브릭 문구 자체가 Generator의 출력을 그 문구 쪽으로 수렴시킨다.
원문 Dutch Art Museum 실험에서 "museum quality"라는 루브릭 단어가 모든 iteration을 실제
미술관 랜딩 페이지처럼 만들었고, 이것이 10라운드의 전면 재구상을 필요하게 만든 원인 중 하나였다.

**이 스킬의 방어**:
- 루브릭 기준은 **reference 단어가 아닌 quality 단어로** 작성됨 (e.g., "originality",
  "specificity", "coherence"). "Medium.com 수준", "Pulitzer 기사처럼" 같은 레퍼런스 금지.
- **동일 루브릭 문구가 3라운드 연속** 사용되면서 Generator 출력이 동일 패턴으로 수렴한다고
  Evaluator가 판단하면, `calibration_log.md`에 `WORDING_LEAKAGE: <기준명> <수렴 패턴>` 기록.
  다음 라운드 전 해당 기준 문구를 **동의어로 리프레이즈**(의미 보존 + 표현 변경).
  예: "고유한 기술적 세부" → "비자명한 관찰" → "이 코드베이스만의 디테일".
- Evaluator few-shot anchor에 특정 문장을 직접 쓰지 말 것(예시로 고정되어 수렴 유도).
  대신 **패턴 기술**(예: "이 작업만의 구체 상황 부재") 사용.

이 경고는 루브릭을 읽는 모든 Evaluator에게 적용. 자기 글이 루브릭 문구에 수렴하는지
iter 3 이후 매번 점검.

---

## Evaluator Calibration — Few-shot Anchors (6 기준 × 점수 1/3/5)

Evaluator는 첫 라운드 전 내부적으로 아래 앵커를 기준선으로 삼는다. 점수 1은 "이렇게 쓰면
즉시 반려", 3은 "통과 턱걸이 — 다음 라운드에서 개선 필요", 5는 "더 이상 손볼 곳 없음"이다.
라운드가 진행되며 채점이 관대하다고 판단되면 기준선을 한 단계 상향한다. 새 패턴이 관찰되면
이 섹션에 append (`SKILL.md`의 Tuning the Evaluator 루프 참조).

### 1. Content depth & structure

- **Score 1** — "TL;DR 2줄, 배경 2줄, 구현 5줄로 끝. Problems & Solutions 섹션 부재.
  제목만 보고 읽은 것과 차이가 없는 개요 수준."
- **Score 3** — "전 섹션 존재하나 Implementation이 설정 명령 나열에 그침. 실제 코드 변경
  diff가 없어 독자가 재현 불가. Problems & Solutions에 에러 메시지 없이 '몇 가지 이슈가
  있었다' 수준."
- **Score 5** — "TL;DR → 배경 → Implementation의 각 단계가 실제 에러 로그·코드 diff·수정
  후 결과로 이어짐. Problems & Solutions에 구체 에러 3건과 각각의 원인·해결책·검증 명령.
  독자가 이 한 글만으로 같은 환경에서 재현 가능."

### 2. Originality & technical specificity (★ 2×)

- **Score 1** — "오프닝 '오늘날 빠르게 변화하는 개발 환경에서, 효율적인 워크플로우 구축은
  필수적입니다.' 전체 본문이 특정 라이브러리 튜토리얼 웹의 요약본. 이 작업만의 고유 맥락
  부재."
- **Score 3** — "대부분 구체적이나 Problems 섹션이 'Stack Overflow에서 자주 언급되는 패턴'
  수준. 이 프로젝트만의 특수한 조합(예: 내부 모노레포 설정과 라이브러리 버전 충돌) 언급 부족."
- **Score 5** — "Insight angle이 본문 전체를 관통. 예: '기본 캐시 TTL이 문서화된 값과 달리
  내부적으로 600초로 강제되어 프로덕션 메모리 스파이크 원인이 됨.' 실제 commit SHA·라인
  번호·에러 스택 트레이스가 증거로 제시."

### 3. Visual completeness (★ 2×)

- **Score 1** — "0 PNGs in `assets/`. Body has one table and just re-lists the Implementation
  steps as text. No diagrams. Hard fail." (Also score 1 if any inline `<pre class=\"mermaid\">`
  or chart shortcode is used — plugin-dependent.)
- **Score 3** — "2 PNGs exist but the second is a decorative table repeating body text. Complex
  architecture (data flow between components) is not diagrammed. All alt text present."
- **Score 5** — "3 PNGs — mind map (post scope), flowchart (Implementation §), and a metrics
  chart (xychart-beta, before/after p95). Diverse types, each compresses a body paragraph and
  is graspable on its own. All alt text specific. Source `.mmd` files preserved in assets/.
  Every visual is a plugin-independent static image embedded via core `wp:image`."

### 4. Gutenberg validity

- **Score 1** — "line 47: `<h4>Key Points</h4>`가 wp:group 내부에 블록 주석 없이. 블록
  에디터에서 'unexpected content' 오류 재현됨. line 52–55: `<ul><li>Item1</li>...`
  wp:list / wp:list-item 주석 모두 누락. Hard fail."
- **Score 3** — "블록 구조 위반은 없으나 다수 heading에 `class='wp-block-heading'` 누락.
  에디터 로딩은 가능하나 테마 CSS 적용이 일관되지 않음."
- **Score 5** — "모든 wp:group 내부 요소 개별 블록 주석 처리. 모든 heading class 포함.
  모든 `<li>` wp:list-item 래핑. Mermaid 인라인 0건, 모두 wp:image로 변환. 블록 에디터
  로드 후 수정 없이 게시 가능."

### 5. Metadata fit

- **Score 1** — "카테고리 0개 또는 4개 이상. 태그 2개 또는 15개. SEO 제목 '~에 대하여' 수준."
- **Score 3** — "기존 카테고리 1개 선택하나 신규 카테고리 1개를 충분치 않은 사유로 생성.
  태그 6개. SEO 제목 구체적이나 65자 초과."
- **Score 5** — "카테고리 1–2개 모두 기존에서 재사용 (existing_categories.txt에 존재 확인).
  태그 8개 모두 본문에 실제 등장한 기술. SEO 제목 58자, 핵심 키워드와 구체 문제를 포함."

### 6. Craft

- **Score 1** — "KO 종결어미 마침표 12건 누락. 코드 블록 언어 태그 4건 누락. 오탈자 3건."
- **Score 3** — "종결어미 마침표 누락 2건(허용치 0 위반, Hard floor). 오탈자 1건. 어조는
  일관되나 1인칭/3인칭 혼재."
- **Score 5** — "종결어미 마침표 100% 준수. 모든 코드 블록 언어 태그 존재. 오탈자 0.
  모바일 가독성(단락 3–4줄) 전 섹션 일관."
