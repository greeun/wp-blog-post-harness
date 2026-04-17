# WordPress Blog Post Harness

A Claude Code skill that writes, validates, and publishes WordPress blog posts
(tech tutorials, troubleshooting writeups, release notes) using a **Planner →
Generator → Evaluator** harness, directly adapted from Anthropic's
[Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
(Prithvi Rajasekaran, 2026).

Version 1.0.0 · MIT · Korean docs: [README.ko.md](README.ko.md)

## Why a Harness for Tech Blog Posts?

Single-pass AI writing produces generic tutorials with placeholder code,
template openings ("In today's fast-paced world..."), inconsistent Gutenberg
block markup, and silently-dropped visuals. This skill separates **drafting**
from **judging** (the GAN-inspired core idea from Anthropic's article) and
iterates through rubric-graded rounds until a strict quality bar is met.

The same architecture produced iteration-10 "creative leaps" in Anthropic's
frontend design experiments that single-pass generation never achieved.

## How It Works

```
You: "Write a blog post about X from my session"
         |
    [Planner] ─── spec.md + sprint contract ──→ You approve
         |
    [Generator, fresh subagent] ── post_vN.md/.html + assets/*.png + handoff.md
         |
    [Evaluator, separate subagent] ── critique_vN.md (6 criteria, each 1-5)
         |          fail → fresh Generator session with critique only (context reset)
         |          pass → next sprint
         |
     ... R1 Skeleton → R2 Implementation → R3 Visuals → R4 Gutenberg ...
         |
    final_post.html confirmed
         |
    ★ You review title/categories/tags/preview → explicit approval required ★
         |
    upload_media.py → publish_post.py (WordPress REST API)
```

## Key Principles (from the article)

| Article Concept | Blog Post Mapping |
|---|---|
| GAN-style generator/evaluator split | Draft-writer and critic are separate `Agent` subagents; they never share conversation |
| Context anxiety (premature wrap-up) | Never skip sections with "rest is similar" — only rubric pass ends a round |
| Context resets + structured handoff | `handoff.md` at each round; next Generator starts fresh, reads only critique + handoff |
| Sprint contract negotiation | Planner's spec Section 9 lists acceptance checks; Generator can `CONTRACT_DISPUTE:` if infeasible |
| Self-evaluation bias | Generator self-**verifies** sprint contract (PASS/FAIL), but self-**scoring** is forbidden |
| Rubric wording leakage | Avoid reference words ("museum quality"); `WORDING_LEAKAGE:` log + 3-round rephrase rule |
| Evaluator self-convincing guard | Quotes article failure pattern verbatim: "finds issue → talks itself into ignoring it" |
| Strategic pivot | Generator decides each round: REFINE / PIVOT / ESCALATE with `design_memo.md` justification |
| Simplest solution first | Simple announcements collapse to 1-round V2; long tutorials use V1 Full (5-8 rounds default, max 15) |
| Every component encodes an assumption | Model-upgrade stress-test procedure (remove one component at a time, measure) |

Full article inventory — including V1 6h/$200 / V2 3h50m/$124.70 cost anchors — preserved in [`references/source-article-inventory.md`](references/source-article-inventory.md).

## Grading Criteria (each 1-5, pass = 2× floor + 1× floor + weighted avg 4.0)

1. **Content depth & structure** — TL;DR → background → implementation → problems → results read as one
2. **Originality & technical specificity** (★ 2×) — This codebase, this error, this code. Penalizes AI slop
3. **Visual completeness** (★ 2×) — ≥2 visuals, Mermaid→PNG rendered, alt text complete
4. **Gutenberg validity** — wp:group inner blocks, wp:list-item, heading class, no inline Mermaid
5. **Metadata fit** — 1-2 categories (prefer existing), 5-10 tags, specific SEO title
6. **Craft** — Korean 종결어미 마침표 100%, code language tags, typo-free

2× floor on Originality and Visual completeness matches the article's guidance
to weight Claude's weak-by-default axes. See [`references/rubric.md`](references/rubric.md)
for all 18 few-shot calibration anchors (6 criteria × scores 1/3/5).

## Setup

### 1. Environment Variables

```bash
# Add to ~/.zshrc or ~/.bashrc
export WP_SITE_URL="https://your-site.com"
export WP_USERNAME="your-username"
export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
```

Create the Application Password in WordPress Admin → Users → Profile → Application Passwords.

### 2. Install

Clone into `~/.claude/skills/` (or symlink from this repo):

```bash
git clone https://github.com/greeun/wp-blog-post-harness ~/.claude/skills/wp-blog-post-harness
```

This skill **reuses the publishing scripts from the sibling `wp-blog-post` skill**
(`md_to_html.py`, `upload_media.py`, `publish_post.py`). Install that skill too
if you don't have it yet.

### 3. Optional: Mermaid CLI for diagram rendering

```bash
npm install -g @mermaid-js/mermaid-cli
# or use npx mmdc -i ... -o ...
```

## Usage

### Trigger Phrases

Just say any of these in Claude Code:

- "Write a blog post harness about..."
- "워드프레스 하네스로 이 세션 정리해줘"
- "블로그 포스트 하네스 시작"

### Output Files

All artifacts are written to a `wp-blog-post/` working directory:

| File | Contents |
|---|---|
| `spec.md` | Planner's spec with must-include content, visuals plan, metadata |
| `sprint_contract.md` | Acceptance checks per round (mechanically verifiable) |
| `existing_categories.txt` | Pre-fetched WordPress category list |
| `post_vN.md` / `post_vN.html` | Drafts per round |
| `critique_vN.md` | Evaluator scores + line-level blockers |
| `handoff.md` | Round-to-round notes + Strategic Decision + Self-Verification |
| `assets/*.png` | Rendered Mermaid diagrams, images |
| `calibration_log.md` | Evaluator tuning loop divergence records |
| `final_post.md` / `.html` | Approved final |
| `publish_log.md` | Post ID, URL, timestamp (after publish) |

## Safety

- **Mandatory human gate**: Evaluator PASS is NOT sufficient for publishing. Explicit user approval required.
- **Category creation**: New categories require justification in spec; weak reasons are penalized by Evaluator.
- **Mermaid inline prohibition**: WordPress doesn't render `<pre class="mermaid">` without plugins; Hard fail.
- **Placeholder detection**: `doSomething()`, `...`, `TODO` in code blocks are Hard fail.
- **Round cap escalation**: Cap reached without PASS → user decides (continue, pivot, abort). No silent stop.

## Project Structure

```
wp-blog-post-harness/
├── SKILL.md                         # Harness instructions, orchestration, model guidance
├── README.md                        # This file
├── README.ko.md                     # Korean README
├── CHANGELOG.md                     # Version history
├── VERSION                          # 1.0.0
└── references/
    ├── planner-prompt.md            # Planner subagent system prompt
    ├── generator-prompt.md          # Generator subagent system prompt
    ├── evaluator-prompt.md          # Evaluator subagent system prompt
    ├── rubric.md                    # 6-criterion rubric + 18 calibration anchors
    ├── gutenberg-rules.md           # Machine-verifiable Gutenberg rules
    └── source-article-inventory.md  # Full article inventory + cost anchors
```

This skill was built using a 4-round quality-gate process that verified ~92%
article fidelity against the source article. See `CHANGELOG.md` for the final
scores; the individual audit reports are not published with the release
(they're build-time QA artifacts, not runtime data).

## Credits

Methodology from:
- **"Harness Design for Long-Running Application Development"** — Prithvi Rajasekaran, Anthropic (2026)
- **"Building Effective Agents"** — Anthropic ("find the simplest solution possible, and only increase complexity when needed")

Extends the sibling [`wp-blog-post`](../wp-blog-post/) skill by adding the
Planner → Generator → Evaluator quality-gate loop before publish.

## License

MIT
