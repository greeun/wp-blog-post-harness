# WordPress Blog Post Harness (한국어)

기술 블로그·튜토리얼·트러블슈팅·릴리스 공지 워드프레스 포스트를 **Planner → Generator → Evaluator**
하네스로 작성·검증·게시하는 Claude Code 스킬. Anthropic의
[Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
(Prithvi Rajasekaran, 2026) 원칙을 직역 이식.

Version 1.0.0 · MIT · English: [README.md](README.md)

## 왜 하네스인가

단일 패스 AI는 일반적인 튜토리얼을 만든다 — 플레이스홀더 코드, 템플릿 오프닝
("오늘날 빠르게 변화하는 개발 환경에서..."), 일관성 없는 Gutenberg 블록 마크업,
조용히 누락되는 시각 요소. 이 스킬은 **작성**과 **평가**를 분리(원문의 GAN-영감
핵심 아이디어)하고 엄격한 품질 기준 통과까지 루브릭 기반 반복을 돌린다.

같은 아키텍처가 원문의 프론트엔드 디자인 실험에서 **iteration 10의 창의적 도약**을
만들어냈다 — 단일 패스 생성에서는 나오지 않는 종류의 결과.

## 동작 흐름

```
사용자: "X 주제로 이 세션 정리해서 워드프레스에 올려줘"
         |
    [Planner] ─── spec.md + sprint contract ──→ 사용자 승인
         |
    [Generator, fresh subagent] ── post_vN.md/.html + assets/*.png + handoff.md
         |
    [Evaluator, 별도 subagent] ── critique_vN.md (6 기준 × 1–5)
         |          FAIL → fresh Generator 세션 (critique.md만 읽음, 컨텍스트 리셋)
         |          PASS → 다음 스프린트
         |
     ... R1 Skeleton → R2 Implementation → R3 Visuals → R4 Gutenberg ...
         |
    final_post.html 확정
         |
    ★ 사용자가 제목·카테고리·태그·미리보기 검토 → 명시적 승인 필수 ★
         |
    upload_media.py → publish_post.py (WordPress REST API)
```

## 원문 핵심 원칙 매핑

| 원문 개념 | 블로그 포스트 매핑 |
|---|---|
| GAN식 generator/evaluator 분리 | Draft-writer와 비평가가 별도 `Agent` subagent, 대화 공유 금지 |
| Context anxiety (조기 종결) | "나머지는 비슷"으로 섹션 생략 금지 — 루브릭 통과로만 라운드 종료 |
| Context reset + 구조화 핸드오프 | 라운드마다 `handoff.md`; 다음 Generator는 fresh 세션, critique·handoff만 읽음 |
| Sprint contract 협상 | Planner spec Section 9에 acceptance check; Generator가 불가능 판단 시 `CONTRACT_DISPUTE:` |
| 자기평가 편향 | Generator는 sprint contract 자기 **검증**(PASS/FAIL) 필수, 자기 **채점** 금지 |
| Rubric wording leakage | 레퍼런스 단어 금지("museum quality"); `WORDING_LEAKAGE:` 로그 + 3라운드 리프레이즈 |
| Evaluator 자기설득 차단 | 원문 실패 패턴 직인용: "문제 발견 후 '별일 아니다'로 설득" |
| 전략적 pivot | Generator 매 라운드 결정: REFINE / PIVOT / ESCALATE + `design_memo.md` 정당화 |
| Simplest solution first | 단순 공지는 1라운드 V2 축약; 장문 튜토리얼은 V1 Full (기본 5–8, 최대 15) |
| Every component encodes an assumption | 모델 업그레이드 시 부품을 **한 번에 하나씩** 제거·측정하는 절차 |

원문 인벤토리 — V1 6h/$200 · V2 3h50m/$124.70 비용 앵커 포함 — 는
[`references/source-article-inventory.md`](references/source-article-inventory.md)에 보존.

## 채점 기준 (각 1–5, 통과 조건: 2× floor + 1× floor + 가중평균 4.0)

1. **Content depth & structure** — TL;DR → 배경 → 구현 → 문제해결 → 결과가 한 덩어리
2. **Originality & technical specificity** (★ 2×) — 이 코드베이스, 이 에러, 이 코드. AI slop 감점
3. **Visual fit & completeness** (★ 2×) — quota 아님(표현 적합성): 복잡한 개념마다 맞는 형식(에디토리얼 카드/스크린샷/표/구조도), filler·Mermaid 모노컬처 감점, 산문이 나으면 산문
4. **Gutenberg validity** — wp:group 내부 블록, wp:list-item, heading class, Mermaid 인라인 금지
5. **Metadata fit** — 카테고리 1–2개(기존 우선), 태그 5–10개, 구체 SEO 제목
6. **Craft** — 한글 종결어미 마침표 100%, 코드 블록 언어 태그, 오탈자 0

2× 가중(Originality, Visual fit)은 Claude의 약점 축에 가중을 두라는 원문
지침을 따른다. 18개 few-shot 앵커는 [`references/rubric.md`](references/rubric.md) 참조.

## 환경 설정

### 1. 환경 변수

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
export WP_SITE_URL="https://your-site.com"
export WP_USERNAME="your-username"
export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
```

WordPress Admin → 사용자 → 프로필 → 애플리케이션 비밀번호에서 발급.

### 2. 설치

```bash
git clone https://github.com/greeun/wp-blog-post-harness ~/.claude/skills/wp-blog-post-harness
```

본 스킬은 **형제 스킬 `wp-blog-post`의 스크립트를 그대로 재사용**한다
(`md_to_html.py`, `upload_media.py`, `publish_post.py`). 아직 설치 전이면 같이 설치.

### 3. (선택) Mermaid CLI 설치 — 다이어그램 PNG 렌더용

```bash
npm install -g @mermaid-js/mermaid-cli
```

## 사용

### 트리거 문구

Claude Code에서 다음 중 아무거나:

- "블로그 포스트 하네스 시작"
- "워드프레스 하네스로 이 세션 정리해줘"
- "기술 블로그 하네스"
- "Write a blog post harness about..."

### 산출물

작업 디렉토리 `wp-blog-post/`:

| 파일 | 내용 |
|---|---|
| `spec.md` | Planner의 spec, must-include 콘텐츠, 시각 요소 계획, 메타데이터 |
| `sprint_contract.md` | 라운드별 acceptance check (기계 검증 가능) |
| `existing_categories.txt` | 사전 조회한 WordPress 카테고리 목록 |
| `post_vN.md` / `post_vN.html` | 라운드별 드래프트 |
| `critique_vN.md` | Evaluator 점수 + 라인 단위 blocker |
| `handoff.md` | 라운드 간 노트 + Strategic Decision + Self-Verification |
| `assets/*.png` | Mermaid 렌더 PNG, 이미지 |
| `calibration_log.md` | Evaluator 튜닝 루프 divergence 기록 |
| `final_post.md` / `.html` | 최종 승인본 |
| `publish_log.md` | 게시 후 post ID, URL, 시각 |

## 안전장치

- **필수 Human Gate**: Evaluator PASS만으로 게시 불가. 사용자 명시 승인 필수
- **카테고리 신규 생성**: spec에 사유 필수, 약한 사유는 Evaluator가 감점
- **Mermaid 인라인 금지**: `<pre class="mermaid">`는 WordPress 기본 렌더 불가 → Hard fail
- **플레이스홀더 검출**: `doSomething()`, `...`, `TODO` 코드 블록은 Hard fail
- **라운드 캡 escalation**: 캡 도달 시 사용자 결정(속행·전환·중단). 조용한 종료 금지

## 프로젝트 구조

```
wp-blog-post-harness/
├── SKILL.md                         # 하네스 지침, 오케스트레이션, 모델 가이드
├── README.md                        # 영문 README
├── README.ko.md                     # 본 파일
├── CHANGELOG.md                     # 버전 이력
├── VERSION                          # 1.0.0
└── references/
    ├── planner-prompt.md            # Planner subagent 시스템 프롬프트
    ├── generator-prompt.md          # Generator subagent 시스템 프롬프트
    ├── evaluator-prompt.md          # Evaluator subagent 시스템 프롬프트
    ├── rubric.md                    # 6기준 루브릭 + 18개 캘리브레이션 앵커
    ├── gutenberg-rules.md           # 기계 검증 가능 Gutenberg 규칙
    └── source-article-inventory.md  # 원문 인벤토리 + 비용 앵커
```

이 스킬은 4라운드 품질 게이트 과정을 거쳐 원문 충실도 **약 92%**를 검증.
최종 점수는 `CHANGELOG.md` 참조. 개별 감사 리포트는 릴리스에 포함하지 않음
(빌드 타임 QA 아티팩트, 런타임 데이터 아님).

## 크레딧

- **"Harness Design for Long-Running Application Development"** — Prithvi Rajasekaran, Anthropic (2026)
- **"Building Effective Agents"** — Anthropic ("find the simplest solution possible, and only increase complexity when needed")

WordPress 게시 파이프라인 앞단에 Planner → Generator → Evaluator 품질 게이트를
둔 구성. 게시 스크립트는 이 스킬에 포함돼 있어 별도 설치가 필요 없다.

## 라이선스

MIT
