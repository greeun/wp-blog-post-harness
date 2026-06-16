---
name: wp-blog-post-harness
description: |
  워드프레스 블로그 포스트를 Planner → Generator → Evaluator 하네스로 작성·게시.
  Anthropic "Harness Design for Long-Running Application Development" (Prithvi Rajasekaran, 2026)의
  원칙(역할 분리·컨텍스트 리셋·스프린트 계약·루브릭 평가·컨텍스트 불안 방지·자기평가 편향 방지)을
  기술 블로그/튜토리얼 도메인에 이식. Gutenberg 블록 유효성·시각 요소·카테고리/태그 메타데이터를
  루브릭으로 검증하고, 승인 후 WordPress REST API로 실제 게시.

  트리거 — EN: "WordPress post harness", "blog post harness", "publish with evaluator",
  "multi-agent blog post", "wp-blog-post harness", "write and evaluate blog post",
  "rigorous tech blog", "harness blog publish".
  KO: "워드프레스 하네스", "블로그 하네스", "블로그 포스트 하네스", "워드프레스 블로그 하네스",
  "평가기 블로그", "평가기 블로그 포스트", "하네스로 블로그", "하네스로 워드프레스",
  "블로그 품질 검증", "블로그 자율 작성", "블로그 멀티에이전트", "기술 블로그 하네스",
  "튜토리얼 하네스", "세션 정리 하네스".
---

# WordPress Blog Post Harness

기술 블로그/튜토리얼 포스트를 3-역할 하네스(Planner → Generator → Evaluator)로 생성하고,
Evaluator 통과 **AND** 사용자 명시 승인 후에만 WordPress REST API로 게시한다.

방법론은 Anthropic의 "Harness Design for Long-Running Application Development"
(Prithvi Rajasekaran, 2026) 원문 원칙의 직역 이식이다. 기존 단일 패스 `wp-blog-post`
스킬과 동일한 publish 파이프라인을 재사용하되, 품질 보증 루프를 구조적으로 앞단에 추가한다.

---

## 이 하네스가 막는 두 가지 실패

1. **자기평가 편향.** 단일 세션이 글쓰기와 평가를 동시에 하면 "이만하면 괜찮다"는
   방향으로 스스로 설득한다. 결과: 얕은 TL;DR, 클리셰 오프닝, 템플릿만 채운 빈약한
   구현 섹션, 빠진 시각 요소에 대한 관대함. → Generator와 Evaluator를 **별도 subagent**로
   분리하고, 파일로만 소통한다.
2. **컨텍스트 불안 (조기 종결).** 세션이 길어질수록 모델은 "충분히 썼다"는 이유로
   마무리를 서두른다. 결과: Gutenberg 블록 규칙 위반(특히 wp:group 내부 raw HTML),
   시각 요소 1개 이하, 태그 5개 미만, 종결어미 마침표 누락. → 라운드 말미마다 **컨텍스트
   리셋**과 구조화된 `handoff.md`를 강제한다.

---

## Input

사용자가 주지 않았다면 이것만 묻는다:

> **주제(Topic):** 한 단락 분량의 포스트 주제·목적(기록/튜토리얼/트러블슈팅/릴리스 공지)·
> 청중(수준 및 관심)·반드시 포함할 기술 스택이나 코드 변경·길이 목표(단문 1,500–3,000자 /
> 중문 3,000–6,000자 / 장문 6,000자+)·언어(한국어/영어)·참고할 세션 내용 혹은 자료.

답변을 `{{WP_TOPIC}}`로 저장한다.

---

## Non-negotiable Principles (원문 직역 이식)

| 원문 개념 | 블로그 포스트 하네스 매핑 |
|---|---|
| GAN식 generator/evaluator 분리 | Draft-writer와 비평가 역할 별도 subagent, 대화 공유 금지 |
| Context anxiety (조기 종결) | "충분히 길다"는 이유로 시각 요소·실제 코드를 생략 금지. 루브릭 통과로만 종료 |
| Context reset + 구조화 핸드오프 | 라운드 말미 `handoff.md` 작성, 다음 라운드는 새 컨텍스트에서 그 파일만 읽고 시작 |
| Compaction과의 구분 | 조용한 요약 금지 — 반드시 명시적 handoff 파일 작성 |
| Sprint contract negotiation | Planner가 정한 "done 기준"을 Generator가 실행 전에 `sprint_contract.md`로 확정 |
| Design quality | Content coherence — 배경·구현·문제해결·결과가 한 덩어리로 읽히는가 |
| Originality | Non-obvious insight — 이 작업만의 구체 상황·실제 코드·실패 사례. 클리셰 TL;DR 배제 |
| Craft | 한글 종결어미 마침표, 코드 블록 언어 태그, Mermaid→PNG 변환, Gutenberg 블록 유효성 |
| Functionality | 독자가 이 글만으로 같은 문제를 재현하거나 같은 기능을 구현할 수 있는가 |
| Adversarial probing | Evaluator가 실제로 Gutenberg 블록을 검사(wp:group inner block 주석, wp:list-item, heading class), 코드 실행 가능성 검증 |
| 5–15 iteration | 기본 5–8라운드, 장문 튜토리얼은 최대 15. 단순 공지는 1–2라운드 축약(Planner가 축약 여부 결정) |
| 자기평가 편향 | Generator는 자기 **채점**(루브릭 점수·최종 품질 판정) 금지, 자기 **검증**(sprint contract PASS/FAIL 체크리스트) 필수. 최종 평가는 오직 Evaluator |
| Generator 전략적 pivot | 매 평가 후 REFINE / PIVOT / ESCALATE 중 택1 (`handoff.md` 최상단에 명시). 점수 상승이면 REFINE, 정체/하락이면 PIVOT(관점·구조 전면 전환), spec 모순·반복 blocker면 ESCALATE |
| 후반 창의적 도약 | 원문 Dutch Museum: 9라운드 대비 10라운드가 근본 전환. 라운드 캡(기본 5–8, 최대 15) 도달 시 자동 종료가 아니라 사용자에게 escalate |
| Evaluator 자기설득 차단 | 원문 실패 패턴 — "합법적 문제 발견 후 '별일 아니다'로 설득" — 이 감지되면 루브릭 하드 스레숄드 강화 |
| 비선형 반복 발견 | 중간 라운드가 최종보다 나을 수 있음 — `handoff.md`에 "지금까지 가장 좋았던 버전 번호" 기록 |
| V1/V2 tier | **기본은 V1 Full** (기술 블로그는 다중 독립 섹션 포함 — 원문 Full 기준 충족). V2(sprint 제거·최종 평가)는 단순 공지에서 Planner가 명시적으로 `HARNESS_MODE: V2` 선언 시에만 |
| 급진적 단순화 실패 | 모델 업그레이드 시 하네스 부품을 **한 번에 하나씩** 제거해 load-bearing 식별 |
| 하네스 공간은 이동 | 비하중 부품은 제거하되 더 큰 역량(예: 이미지 비전 검증, 링크 fetch)을 새로 추가 |

원문 핵심 인용 및 전체 매핑 인벤토리는
[references/source-article-inventory.md](references/source-article-inventory.md)에 보존.

---

## Roles

### Planner (1회, 드래프트 전)

- Input: `{{WP_TOPIC}}`, 사용자 제약, 기존 WordPress 카테고리 목록(스킬이 사전 조회).
- Output: `spec.md` — 목표·청중·핵심 메시지(1문장)·포맷(기술 블로그/튜토리얼/트러블슈팅)·
  구조 개요(섹션 순서와 각 섹션 의도)·**반드시 포함할 실제 내용**(사용자 세션에서 추출한
  코드 스니펫/변경점/에러 메시지/해결책)·시각 요소 계획(최소 2개: 어떤 종류/어디에)·
  카테고리 후보(기존 재사용 우선, 신규 생성 사유)·태그 후보 5–10개·SEO 제목 후보 2–3개·
  한글/영문 여부와 그에 따른 스타일 규칙·**Sprint Contract**(Generator가 검증할 acceptance checks).
- 이 글에만 고유한 "insight angle"을 1개 명시(원문의 "weave AI features"에 해당).
- 모호한 부분은 `spec.md`에 명시적으로 해소하고 가정은 `ASSUMPTION:` 라벨로 표시.
- 전문 프롬프트: [references/planner-prompt.md](references/planner-prompt.md)

### Generator (라운드마다)

- Input: `spec.md` + `sprint_contract.md` + (있다면) 직전 `critique.md` + 직전 `handoff.md`.
- Output: `post_vN.html`(Gutenberg 유효 HTML, `md_to_html.py` 또는 직접 작성) +
  `post_vN.md`(원본 Markdown) + `handoff.md`(무엇을 썼고, 어떤 가정·외부 인용을 했고,
  시각 요소를 어떻게 생성했고, 지금까지 가장 좋았던 버전 번호).
- 시각 자산(Mermaid→PNG)은 `assets/`에 저장. WordPress 업로드는 Evaluator 통과 후 진행
  (드래프트 검증 단계에서는 경로만 기록).
- **자기 채점 금지, 자기 검증 필수**: 자기 드래프트에 점수·최종 품질 판정 금지(Evaluator 권한).
  그러나 `sprint_contract.md`의 각 acceptance check를 PASS/FAIL로 `handoff.md`에 기록 필수.
  자기 검증 FAIL이 있으면 Evaluator에 제출하지 말고 재작업.
- **전략적 결정 (N>1 라운드)**: REFINE | PIVOT | ESCALATE 중 택1, `handoff.md` 최상단 명시.
  점수 상승 → REFINE. 정체/하락 → PIVOT(관점·구조 전면 전환, `design_memo_vN.md` 작성).
  spec 모순·3라운드 연속 blocker → ESCALATE(드래프트 중단, 사용자 개입 요청).
- 파일로만 소통.
- 전문 프롬프트: [references/generator-prompt.md](references/generator-prompt.md)

### Evaluator (라운드마다)

- Input: `spec.md`, `sprint_contract.md`, `post_vN.html` (+ `.md`), `assets/`.
- Output: `critique_vN.md` — 각 루브릭 기준 1–5 점수(근거+증거) + 라인 단위 지적 +
  구체 수정 지시 + Verdict: PASS/FAIL.
- 적극적 프로빙 (증거 필수):
  - Gutenberg 규칙 기계 검증: wp:group 내부 raw HTML 금지, `<h2> class="wp-block-heading"`,
    `wp:list-item` 래핑, `wp:heading` level 속성. 위반 라인 번호를 모두 기록.
  - 시각 요소 카운트 및 적합성: 최소 2개, 복잡 개념 다이어그램, 비교 표 여부.
  - 코드 스니펫 실행 가능성 검사(문법·import·변수 참조). 가짜 코드·플레이스홀더는 즉시 FAIL.
  - 외부 인용·수치는 WebFetch 등으로 실제 검증.
  - 한글 포스트: 종결어미(~다/했다/된다/있다/없다) 뒤 마침표 누락 전수조사.
  - 카테고리/태그: 기존 WordPress 카테고리 목록 대비 신규 생성 사유 타당성.
- **자기 설득 금지.** 원문의 구체 실패 패턴("합법적 문제 발견 후 '별일 아니다'로 설득,
  엣지 케이스 대신 피상적 테스트")이 감지되면 루브릭 하드 스레숄드 강화.
- 캘리브레이션: 첫 라운드 전 few-shot 점수 분석을 내부적으로 구성. 예:
  "Originality 2 — '오늘날 빠르게 변화하는…' 류 오프닝, 이 작업만의 구체 상황 부재."
- 통과 기준: 모든 기준 ≥4 AND Hard fail triggers 없음.
- 전문 프롬프트: [references/evaluator-prompt.md](references/evaluator-prompt.md)

---

## Grading Rubric (1–5, 매 라운드)

상세: [references/rubric.md](references/rubric.md)

1. **Content depth & structure** — TL;DR·배경·구현·문제해결·결과의 논리 일관성과 깊이.
2. **Originality & technical specificity** (★ weight 2×) — 이 작업·이 코드베이스·이 에러에만
   고유한 세부사항. 템플릿/클리셰 감점.
3. **Visual completeness** (★ weight 2×) — **Infographic-first**. The post structure and every
   explanation must be **graspable at a glance**; visuals are the primary delivery vehicle, not
   decoration. Aim for one visual per major section (minimum 2 per post). **Type diversity is
   mandatory**: mind map (topic decomposition), diagram/schematic, flowchart, architecture,
   chart/graph (metrics), timeline, sequence, webtoon/illustration (problem→solution narrative),
   and other creative visualizations beyond these types — the list is not exhaustive (journey
   strip, quadrant, labeled map, cards, custom infographic, …). Repeating the
   same type is penalized. Complex concepts must be diagrammed; Mermaid→PNG must render; alt text
   required. **Plugin-independent only**: every infographic ships as a static image file embedded
   via the core `wp:image` block — no inline Mermaid, shortcodes, or JS chart libraries.
   Pass criterion: "Can the post be understood by skimming the images alone?"
4. **Gutenberg validity** — wp:group inner block 규칙, heading class, list-item 래핑.
   하나라도 위반 시 hard fail.
5. **Metadata fit** — 카테고리(기존 재사용 우선) 1–2개, 태그 5–10개, SEO 제목 구체성.
6. **Craft** — 한글 종결어미 마침표, 코드 블록 언어 태그, 오탈자, 어조 일관성.

**Weighting**: Originality와 Visual completeness가 Claude의 약점(템플릿 기본값으로
회귀) 축이라 2× 가중. 통과: 가중 평균 ≥4 AND 모든 기준 ≥3 AND Hard fail 없음.

**Hard fail triggers** (즉시 반려):
- Gutenberg 블록 규칙 위반 1건 이상.
- 시각 요소 2개 미만.
- Plugin-dependent visual: inline Mermaid, chart/diagram shortcode, plugin-specific block, or
  JS-injected chart in the body. Visuals must be plugin-independent static images via `wp:image`.
- 가짜 코드·플레이스홀더(`TODO`, `...` 이상), 실행 불가능한 스니펫.
- 한글 포스트에서 종결어미 마침표 누락.
- 외부 수치 인용에서 확인 불가능한 숫자.
- 태그 5개 미만 또는 10개 초과.

---

## Default Round Sequence (Planner가 조정 가능)

1. **R1 Skeleton & Hook** — 제목·TL;DR·섹션 구조 + 훅·배경 확정.
2. **R2 Implementation & Problems** — 실제 코드·에러·해결 세부 채움. 시각 요소 1차 생성.
3. **R3 Visuals & Metadata** — Infographic-first design: target one visual per section, diversify
   types (mind map, flowchart, architecture, chart/graph, timeline, sequence, webtoon/illustration,
   creative schematic). Render Mermaid→PNG (`mmdc` renders mindmap, xychart-beta, pie, timeline,
   quadrantChart in addition to flowcharts); webtoon/custom infographics are generated as images
   then uploaded via `upload_media.py`. All visuals are **plugin-independent static images** embedded
   via core `wp:image` (no inline Mermaid/shortcodes/JS). Finalize categories/tags and SEO title.
4. **R4 Gutenberg Compliance** — 블록 규칙 전수검사, 오탈자·종결어미 점검.
5. **(옵션) R5 Revision** — 잔여 blocker 수정.

단순 공지·짧은 패치 노트는 Planner가 1라운드로 축약(원문 Opus 4.6 단순화 대응).

---

## Orchestration / Execution Protocol

### Orchestration Mechanics (필독)

**본 하네스의 핵심 전제**: Planner·Generator·Evaluator는 **반드시 별도의 subagent**로
디스패치해야 한다. 같은 세션이 다중 역할을 하면 자기평가 편향(원문: "confidently praise
mediocre work")으로 구조가 무너진다. Claude Code에서는 **`Agent` 툴**을 사용한다.

각 역할 디스패치 계약:

| 단계 | Agent 툴 호출 | 시스템 프롬프트 | 주요 입력 파일 | 콘솔 반환 신호 |
|---|---|---|---|---|
| Planner | `Agent(subagent_type: "general-purpose", prompt: <planner-prompt.md 전문> + "{{WP_TOPIC}}" + existing_categories.txt)` | `references/planner-prompt.md` | `{{WP_TOPIC}}`, `existing_categories.txt` | `SPEC_READY: wp-blog-post/spec.md` |
| Generator | `Agent(subagent_type: "general-purpose", prompt: <generator-prompt.md 전문>)` | `references/generator-prompt.md` | `spec.md`, `sprint_contract.md`, (N>1) `critique_v{N-1}.md`, `handoff.md` | `READY_FOR_QA: wp-blog-post/post_vN.html` |
| Evaluator | `Agent(subagent_type: "general-purpose", prompt: <evaluator-prompt.md 전문>)` | `references/evaluator-prompt.md` | `spec.md`, `sprint_contract.md`, `post_vN.md/.html`, `assets/`, `handoff.md` | `CRITIQUE_READY: wp-blog-post/critique_vN.md` |

**오케스트레이터(이 skill을 읽는 Claude)의 금지 행동**:
- Planner/Generator/Evaluator 역할을 직접 수행하지 말 것 — 반드시 `Agent` 툴로 디스패치.
- subagent에게 이전 subagent의 대화·추론을 전달하지 말 것 — 오직 파일로만.
- subagent의 콘솔 산출물을 요약해 다음 subagent에 inline으로 넘기지 말 것 — 파일 경로만 전달.

**Fallback**: `Agent` 툴이 사용 불가한 환경이라면, 오케스트레이터는 먼저 사용자에게 "본 하네스는
subagent 디스패치 전제로 설계되었으며, 단일 세션 실행은 자기평가 편향 리스크가 있다"고 알린 후
각 역할 프롬프트를 **하드 역할 전환**으로 순차 실행한다. 각 역할 프롬프트 파일을 읽고 그 내용만을
시스템 프롬프트로 간주해 작업한다.

### Execution Flow

사용자가 주제를 제공하면:

1. `{{WP_TOPIC}}` 한 문장 재확인.
2. 작업 디렉토리 `wp-blog-post/` 를 현재 경로(또는 사용자 지정)에 생성.
   하위 구조: `spec.md`, `sprint_contract.md`, `post_vN.md/.html`, `critique_vN.md`,
   `handoff.md`, `assets/`, `calibration_log.md`, `publish_log.md`.
3. 기존 WordPress 카테고리 사전 조회 (API 가능 시):
   ```bash
   curl -s "${WP_SITE_URL}/wp-json/wp/v2/categories?per_page=100" \
     | python3 -c "import sys,json; cats=json.load(sys.stdin); [print(f\"{c['id']}: {c['name']} ({c['count']})\") for c in cats]"
   ```
   결과를 `wp-blog-post/existing_categories.txt`에 저장. 실패 시 spec에 `ASSUMPTION:` 기재.
4. **Planner**를 `Agent` 툴로 디스패치 → `spec.md` + `sprint_contract.md` 작성 후 `SPEC_READY:`
   반환. **사용자에게 spec 요약을 보여주고 명시적 go 대기** (spec이 잘못 잡히면 이후 전부 낭비).
5. 각 라운드:
   a. **Generator**를 `Agent` 툴로 **fresh subagent 세션**으로 디스패치 → `post_vN.md` +
      `post_vN.html` + 필요 assets + `handoff.md` → `READY_FOR_QA:` 반환.
   b. **Evaluator**를 `Agent` 툴로 **별도 fresh subagent 세션**으로 디스패치 → `critique_vN.md`
      (PASS/FAIL + 증거) → `CRITIQUE_READY:` 반환.
   c. FAIL → 다음 라운드는 **새 Generator subagent 세션** (컨텍스트 리셋, Agent 툴 재호출). 입력은
      `spec.md`, `sprint_contract.md`, 최신 `critique_vN.md`, `handoff.md`만. 이전 drafts 참조 금지.
   d. PASS → `final_post.html`, `final_post.md` 확정.
6. 라운드 캡 도달 후에도 FAIL → **사용자에게 escalate**. 침묵 종료 금지.
   사용자가 "그대로 진행(추가 라운드)", "방향 전환", "중단" 중 선택.

   **라운드 캡 범위**: 기본 5–8. 장문 튜토리얼/대형 분석은 최대 **15**까지 허용.
   단순 공지·짧은 패치 노트는 1–2. 고정값 5는 원문의 Dutch Art Museum iteration-10 도약을
   구조적으로 차단하므로 장문 포스트에서는 반드시 8 이상으로 설정.

   **Wall-clock 허용성**: 5-라운드 하네스가 6,000자+ 튜토리얼에 대해 **30–90분** 소요는 정상.
   시간이 길다는 이유로 라운드를 임의 축소하지 말 것.
7. **[MANDATORY HUMAN GATE]** PASS 후, 사용자에게 다음을 그대로 출력하고 명시적 승인
   ("게시", "publish", "OK" 등)을 기다린다:
   - 최종 제목·카테고리·태그·SEO 제목.
   - 시각 자산 파일 경로 목록.
   - 본문 길이와 첫 300자 미리보기.
   - `status=draft` 또는 `status=publish` 중 사용자 선택.
   - WordPress 환경 변수 존재 여부 확인 결과.
   **승인 없이 `publish_post.py` 호출 금지.**
8. 승인 후 publish 파이프라인:
   a. `assets/` 내 이미지를 `upload_media.py`로 업로드 → 각 이미지의 MEDIA_ID, URL 획득.
   b. 본문 HTML의 이미지 placeholder를 업로드된 URL로 치환.
   c. `publish_post.py --title ... --content-file final_post.html --status <선택>
      --categories ... --tags ...` 실행.
   d. 반환된 post URL을 사용자에게 제공하고 `publish_log.md`에 append.

### Safeguards

- **컨텍스트 불안 감지**: Generator가 섹션을 건너뛰거나 "나머지는 비슷하게"로 마무리하면
  그 자체가 FAIL 신호. Evaluator는 이를 라인 단위로 지적.
- **라운드 캡 escalation**: 캡 도달 시 자동 게시 절대 금지. 사용자 결정 필수.
- **Publish gate**: Evaluator PASS는 게시 조건이 **아니다**. 오직 사용자 승인만.
- **카테고리 신규 생성**: Planner가 spec에 사유 명시. 사유가 약하면 Evaluator가 감점.
- **Mermaid 렌더 실패**: PNG가 없으면 Visual completeness 자동 FAIL — 인라인 `<pre class="mermaid">`
  금지(wp-blog-post 원문 규칙).

### Tuning the Evaluator across runs

원문 경고: LLM Evaluator는 기본값으로 관대하다. "confidently praises mediocre work."
이를 상쇄하기 위해 매 실행 후 다음 루프를 수행한다.

1. **기록**: 각 라운드의 `critique_vN.md`에서 점수·verdict·blocker 건수를
   `wp-blog-post/calibration_log.md`에 append. 형식:
   ```
   {YYYY-MM-DD HH:MM} R{N} — weighted_avg={X.XX} verdict={PASS|FAIL}
   blockers={n} top_issue="{한 줄 요약}"
   user_judgment_divergence="{사용자가 Evaluator와 다르게 판단한 부분, 있으면 기록}"
   ```
2. **발견 (divergence)**: 사용자가 최종 산출물을 검토한 후, Evaluator가 놓친 문제를 한 번
   보고받는다. 예: "Evaluator는 PASS했지만 실제 독자 입장에서 Implementation 섹션이 얕다고
   느꼈다." 이 관찰을 `calibration_log.md`에 기록.
3. **업데이트**: divergence가 2회 이상 동일 패턴이면 `references/rubric.md`의 해당 기준에
   새 캘리브레이션 앵커(해당 패턴의 점수 예시)를 append. Evaluator 프롬프트의 캘리브레이션
   지침이 자동으로 다음 실행에 반영된다.
4. **재실행**: 다음 호출 시 업데이트된 rubric 기준으로 동작. 동일 패턴이 해소되는지 확인.

**루프 중단 기준**: 같은 블로그 유형에서 3회 연속 divergence 없음 → 현 캘리브레이션 안정화로 간주.

---

## Environment Variables (Publishing 단계)

기존 `wp-blog-post` 스킬과 동일:

```bash
export WP_SITE_URL="https://your-site.com"
export WP_USERNAME="your-username"
export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
```

환경 변수 누락 시, Evaluator 통과 이후 사용자에게 알리고 draft 파일만 보존(`final_post.html`).

---

## Scripts (기존 `wp-blog-post` 재사용)

게시 파이프라인은 기존 스킬 스크립트를 그대로 호출한다. 중복 구현하지 않는다.

| 스크립트 | 역할 | 호출 시점 |
|---|---|---|
| `~/.claude/skills/wp-blog-post/scripts/md_to_html.py` | Markdown → Gutenberg 블록 HTML | Generator가 드래프트 생성 시 |
| `~/.claude/skills/wp-blog-post/scripts/upload_media.py` | 이미지 업로드 (PNG/JPG) | 사용자 승인 후 publish 단계 |
| `~/.claude/skills/wp-blog-post/scripts/publish_post.py` | 포스트 게시 (draft/publish) | 사용자 승인 후 publish 단계 |

Mermaid 렌더: `mmdc -i diagram.mmd -o diagram.png -w 900 --backgroundColor white`
(Generator 단계, `assets/`에 저장).

---

## File Handoff Contract

단일 진실 원천(Single source of truth). 모든 역할은 파일로만 소통한다.

```
wp-blog-post/
├── spec.md                   Planner → Generator, Evaluator
├── sprint_contract.md        Planner가 작성, Generator 참조, Evaluator가 체크리스트로 사용
├── existing_categories.txt   사전 조회 결과 (Planner, Evaluator 참조)
├── post_v1.md / post_v1.html Generator → Evaluator
├── post_vN.md / post_vN.html (이후 라운드)
├── critique_v1.md            Evaluator → (다음 라운드) Generator
├── critique_vN.md
├── handoff.md                라운드 말미 Generator가 작성, 다음 라운드 fresh Generator가 읽음
├── assets/                   이미지·다이어그램 PNG
├── final_post.md / .html     모든 라운드 통과 후 확정
└── publish_log.md            게시 후 append: post_id, URL, 시각
```

---

## Gutenberg Block Rules

전문: [references/gutenberg-rules.md](references/gutenberg-rules.md)

하드 룰 요약(Evaluator가 기계 검사):

1. `<!-- wp:group -->` 내부 모든 HTML 요소는 개별 블록 주석 필수 (`wp:heading`, `wp:paragraph`,
   `wp:list`, `wp:list-item`).
2. 리스트 아이템은 `<!-- wp:list-item --><li>...</li><!-- /wp:list-item -->` 래핑 필수.
3. 헤딩은 `class="wp-block-heading"` 필수, level 속성 명시(`<!-- wp:heading {"level":2} -->`).
4. `wp:group` 안에 raw `<h4>`, `<ul>`, `<p>` 직접 배치 금지 — "unexpected content" 오류.
5. Mermaid 인라인(`<pre class="mermaid">`) 금지 — 반드시 PNG 렌더 후 `wp:image` 블록.

---

## Harness Tier & Model-Specific Guidance

### Tier 결정

이 스킬의 **기본 tier는 V1 (Full harness)** 이다. 근거: 기술 블로그 포스트는 독립 섹션
(TL;DR / 배경 / 구현 / 문제해결 / 결과 / 메타데이터 / 시각 자산 / Gutenberg 컴플라이언스)이
5개 이상이라 원문 article의 "Complex, multi-feature output" 기준에 부합. Planner 1회 +
라운드별 Generator/Evaluator + 라운드별 sprint_contract 체크를 유지.

**V2 (Simplified harness) 모드로 축약**하는 경우:
- 단순 릴리스 공지·패치 노트·1–2 문단 공유글.
- Opus 4.6 이상 모델에서 실행하며 사용자가 속도를 우선시하는 경우.
- 이 때 Planner가 spec에 `HARNESS_MODE: V2` 기재 → R1–R4 sprint 분해를 삭제하고 Generator
  1회 연속 실행 + Evaluator 1회 최종 패스로 축약.

**"Find the simplest solution possible, and only increase complexity when needed."**
— Anthropic, *Building Effective Agents*. V2로 시작해 Evaluator가 2라운드 연속 "섹션 간
논리 단절"이나 "단일 패스 내 일관성 부족" blocker를 제기하면 V1로 승격한다.

### Model-Specific Guidance

모든 하네스 부품은 "모델이 혼자 못 하는 것"에 대한 가정이다. 모델이 개선되면 부품을
**한 번에 하나씩** 제거해 가정을 재검증한다(일괄 단순화는 원문에서 재현 실패).

| 모델 | 컨텍스트 불안 | 권장 tier | Sprint 세분화 | Evaluator 빈도 | 컨텍스트 리셋 |
|---|---|---|---|---|---|
| **Sonnet 4.5** 이하 | 강함 — 조기 종결 | V1 Full | 세분화 필수 (R1–R4) | 라운드당 1회 | 라운드마다 강제 |
| **Opus 4.5** | 크게 감소 | V1 Full 또는 V2 | 선택적 | 라운드당 1회 | FAIL 시에만 |
| **Opus 4.6** | 제거됨 (원문 검증) | V2 Simplified | 제거 가능 | 최종 1회 또는 마일스톤 | 컨텍스트 압박 시에만 |
| **Opus 4.7+** | 원문 미언급 (운영 가정)※ | V2 또는 단일 패스 | 제거 | 최종 1회 | 필요 시에만 |

※ 원문은 Opus 4.5/4.6 실험 데이터만 보고하며 4.7 컨텍스트 안정성은 직접 측정하지 않았다.
이 행은 "4.6 추세의 연속"이라는 **운영 가정**이며, 4.7로 실제 실행 시 **Sonnet 4.5 기준선 대비
품질 측정을 1회 수행**하여 가정을 검증할 것. 품질 저하 발견 시 V1 Full로 즉시 회귀.

**부품 제거 실험 절차**:
1. 현재 설정으로 1회 실행하여 산출물을 베이스라인으로 저장.
2. 부품 1개만 제거(예: 라운드별 sprint_contract 체크 삭제).
3. 같은 주제로 1회 재실행.
4. 루브릭 점수가 베이스라인 대비 하락하지 않으면 제거 유지. 하락하면 복원.
5. 다음 부품으로 이동. 한 번에 여러 개 제거하지 말 것.

실패 시 원복할 수 있도록 각 실험은 git 또는 디렉토리 스냅샷으로 보존.

---

## Iteration Wisdom (원문 교훈)

- **후반 창의적 도약 가능.** 원문에서 iteration 10이 1–9와 근본적으로 다른 결과를
  낳았다. 라운드 캡 도달 시 자동 종료하지 말고 사용자 escalate.
- **중간 라운드가 최종보다 나을 수 있다.** `handoff.md`에 "best version so far" 번호 기록.
  최종 확정 전 비교 판단.
- **Pivot은 정당화 필요.** 후반 방향 전환은 Evaluator의 명시적 REDIRECT 혹은 Generator의
  `design_memo.md`로 사유 기록. 컨텍스트 리셋으로 인한 망각 ≠ 통찰.
- **모델 업그레이드 시 부품 제거는 하나씩.** 일괄 단순화는 원문에서 실패. 제거 후 1라운드
  측정, 품질 저하 없으면 유지.

---

## Red Flags — 멈춰야 할 징후

| 징후 | 의미 | 대응 |
|---|---|---|
| Generator가 자기 드래프트를 "잘 쓰여졌다" 요약 | 자기평가 편향 진입 | 즉시 컷, 요약 문장 삭제하고 계약 이행만 |
| 섹션 생략·"..."·"유사하게 처리" | 컨텍스트 불안 | FAIL, 새 세션에서 해당 섹션부터 재개 |
| 코드에 실제 함수명 없이 `doSomething()` 등 플레이스홀더 | 가짜 구현 | Hard fail |
| 시각 요소 계획만 있고 PNG 미생성 | 컨텍스트 불안 마무리 | Hard fail |
| Evaluator가 "전체적으로 무난하다"로 PASS | 자기 설득 | 루브릭 재적용, 라인 단위 증거 요구 |
| 기존 카테고리 무시하고 전부 신규 생성 | Planner 스코프 미확인 | Planner 재실행 |
| 사용자 승인 전 `publish_post.py` 호출 시도 | 게이트 위반 | 즉시 중단, 사용자 승인 필수 |

---

## References

- 원문 전체 인벤토리와 매핑: [references/source-article-inventory.md](references/source-article-inventory.md)
- Planner 프롬프트: [references/planner-prompt.md](references/planner-prompt.md)
- Generator 프롬프트: [references/generator-prompt.md](references/generator-prompt.md)
- Evaluator 프롬프트: [references/evaluator-prompt.md](references/evaluator-prompt.md)
- 루브릭 상세: [references/rubric.md](references/rubric.md)
- Gutenberg 블록 규칙: [references/gutenberg-rules.md](references/gutenberg-rules.md)
- 기존 단일 패스 스킬 (publish 파이프라인 소스): `~/.claude/skills/wp-blog-post/`
