# Changelog

## [1.2.0] — 2026-06-18

Visualization criterion reworked from **infographic-first quota** to **representation-fit**. The
1.1.0 directive made every post produce the same shape: one auto-generated visual per section, all
rendered through Mermaid (`mmdc`), so posts looked uniform within and across each other. 1.2.0 makes
the content decide the form, adds an editorial render path, and penalizes both under- and
over-visualization.

### Changed
- **Criterion 3 renamed** `Visual completeness` → **`Visual fit & completeness`**. No per-section
  quota; a visual earns its place only when it makes a concept graspable that prose can't carry.
  Choosing prose/table/code over a diagram is now scored as good craft, not a gap.
- **Open, non-diagram-only form menu**: editorial card-news / poster cards (preferred for conceptual
  content), annotated screenshots, comparison tables, code diffs, illustration/webtoon, and
  structural diagrams (flowchart / mind map / architecture / sequence / timeline / chart) **only when
  the content is genuinely a process / hierarchy / flow / metric**.
- **Mermaid demoted** to genuine node-graphs only — never the default, never to hit a count.
- **Two-directional Hard fails**: under-visualization (a complex concept left as a text wall) AND
  filler/quota visuals AND render monoculture (all-`mmdc` set). Replaces the old "fewer than 2 PNGs"
  count floor.

### Added
- **`scripts/render_html.py`** — headless-Chromium (Playwright) HTML/CSS → PNG renderer for editorial
  cards/posters/schematics. Card-news default 1080×1350 @2x; `--selector` element capture; `--full-page`.
- Render-origin diversity (mix card + screenshot + structural diagram) now weighed alongside type
  diversity; an all-Mermaid set is a monoculture deduction.
- Propagated through `SKILL.md` (rubric 3, Hard fail triggers, R2/R3 round sequence, scripts table,
  red flags) and `references/`: `planner-prompt.md` (Visuals Plan + R2/R3 contract),
  `generator-prompt.md` (visual assets + anti-patterns + handoff template), `evaluator-prompt.md`
  (visual fit check + Hard fail + calibration), `rubric.md` (criterion 3 + score anchors),
  `gutenberg-rules.md` (Rule 5 broadened to all pre-rendered images).

## [1.1.0] — 2026-06-17

Infographic-first visualization directive added across the harness. Visuals become the primary
delivery vehicle so the post structure and every explanation are graspable at a glance, and every
infographic must ship as a plugin-independent static image.

### Added
- **Visual completeness (criterion 3)** reworked to infographic-first: one visual per major
  section, mandatory type diversity (mind map, flowchart, architecture, chart/graph, timeline,
  sequence, webtoon/illustration, plus other creative visualizations — the type list is not
  exhaustive). Pass test: "Can the post be understood by skimming the images alone?"
- **Plugin independence** enforced end-to-end: every infographic is a self-contained static image
  embedded via core `wp:image`. Inline Mermaid, chart/diagram shortcodes, plugin-specific blocks,
  and JS chart libraries are Hard fails.
- Propagated through `references/`: `planner-prompt.md` (Visuals Plan), `generator-prompt.md`
  (visual assets), `evaluator-prompt.md` (visual checks + plugin scan Hard fail), `rubric.md`
  (score anchors, diversity floor, plugin-dependency floor).
- R3 round and Hard fail triggers updated; `mmdc` multi-type rendering and webtoon/custom-image
  upload path documented.

## [1.0.0] — 2026-04-17

Initial release. WordPress blog post authoring and publishing using the
**Planner → Generator → Evaluator** harness pattern from Anthropic's
[Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
(Prithvi Rajasekaran, 2026).

### Included
- 3-role harness with `Agent` tool dispatch, file-based handoffs, context resets
- V1 Full tier default (tech blog posts have 5+ independent sections); V2 Simplified opt-in via `HARNESS_MODE: V2`
- 6-criterion rubric with 2× weighting on Originality and Visual completeness (Claude's weak-by-default axes)
- Few-shot calibration anchors: 6 criteria × score 1/3/5 = 18 anchors
- Rubric wording leakage guard (`WORDING_LEAKAGE:` log + 3-round rephrase rule)
- Generator Strategic Decision block: REFINE / PIVOT / ESCALATE / CONTRACT_DISPUTE
- `EVALUATOR_NECESSITY` conditional per article V2 insight
- Gutenberg block machine validation (wp:group / wp:list-item / wp:heading class / Mermaid→PNG)
- Korean 종결어미 마침표 전수검사
- Mandatory human gate before WordPress publishing
- Reuses existing [`wp-blog-post`](../wp-blog-post/) scripts for md→HTML, media upload, post publish
- Model-specific tier guidance (Sonnet 4.5 / Opus 4.5 / 4.6 / 4.7+)
- Evaluator tuning loop with divergence logging

### Article fidelity
Verified ~92% against the source article across 32 audit rows
(FULL 27 / PARTIAL 3 / MISSING 1 / DIVERGED-justified 1). Rubric self-score
converged R1 3.375 → R2 3.875 → R3 4.000 → R4 4.125 (PASS) over a 4-round
quality-gate process. Individual audit reports are build-time QA artifacts
and are not shipped with the release.
