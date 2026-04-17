# Changelog

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
