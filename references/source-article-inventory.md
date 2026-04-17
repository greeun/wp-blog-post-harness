# Source Article Inventory

원문: Prithvi Rajasekaran, *Harness Design for Long-Running Application Development*,
Anthropic Engineering Blog, 2026.

이 스킬이 차용한 원문의 핵심 개념·실험·수치를 보존한다. Planner·Generator·Evaluator가
필요 시 이 문서를 참조해 개념의 원본 의도를 확인한다.

---

## 1. 핵심 문제 진술

> "장시간 실행 코딩 에이전트는 생성과 평가를 같은 세션에서 하면 자기평가 편향으로 인해
> 평범한 작업을 당당히 칭찬한다."

이 스킬의 매핑: 블로그 포스트에서도 같은 문제가 더 빈번. "이 정도면 훌륭한 튜토리얼"
같은 자기평가가 한글 문체·Gutenberg 규칙·시각 요소 부재를 덮는다.

## 2. 여섯 가지 원칙

| 원문 | 본 스킬 적용 |
|---|---|
| Structural role separation (GAN식) | Planner / Generator / Evaluator 별도 subagent |
| File-based handoffs | `spec.md`, `sprint_contract.md`, `post_vN.md/.html`, `critique_vN.md`, `handoff.md` |
| Sprint contracts | Planner가 `spec.md` Section 9에 라운드별 acceptance checks 명시 |
| Context resets | 라운드마다 fresh Generator 세션, `handoff.md`만 읽고 시작 |
| Rubric-based evaluation with evidence | 6개 기준 1–5 채점 + 라인 번호·실제 값 증거 |
| Every component encodes an assumption | 모델 업그레이드 시 하네스 부품을 1개씩 제거하며 load-bearing 식별 |

## 3. V1 → V2 진화

- **V1 (Sonnet 시대)**: 작은 스프린트, 매 라운드 Evaluator, 공격적 컨텍스트 리셋.
- **V2 (Opus 4.5+)**: 스프린트 분해 제거, Generator 연속 실행, Evaluator는 최종 혹은
  단계적 통과만 판정. Planner는 유지(spec 부재 시 under-scoping 재현).

이 스킬은 **기본 V1 Full** (기술 블로그는 다중 독립 섹션 — TL;DR/배경/구현/문제해결/
결과/메타데이터/시각/Gutenberg — 으로 원문 "Complex, multi-feature output" 기준 충족).
단순 공지·짧은 패치 노트만 Planner가 `HARNESS_MODE: V2`로 선언하여 축약.

## 4. Dutch Art Museum 사례 (창의적 후반 도약)

- 원문 실험: 디지털 미술관 페이지 생성. 9라운드까지 어두운 랜딩 페이지 수준.
- 10라운드에서 Generator가 기존 접근을 전면 폐기하고 공간적 3D 경험으로 재구상.
- 단일 패스 모델에서는 절대 나오지 않는 종류의 도약.

이 스킬 적용: 라운드 캡(기본 5–8, 최대 15) 도달 시 자동 종료 금지. 사용자에게 escalate. Generator는
정체/하락 시 **관점·구조 전면 전환** 옵션을 쓰도록 지시됨.

## 5. Evaluator self-persuasion 실패 패턴

원문 인용: "Evaluators find legitimate problems, then talk themselves into approving —
'this is fine' — and run shallow tests instead of edge cases."

이 스킬의 방어:
- Evaluator 프롬프트에 명시적으로 이 패턴 경고.
- 증거(라인 번호, 실제 값) 없는 PASS 금지.
- few-shot 캘리브레이션 기준선 내부 구성.
- 전 기준 ≥4일 때 깐깐한 편집자가 잡을 1가지를 더 찾도록 강제.

## 6. Planner 부재 시 under-scoping

원문: Planner를 건너뛰면 Generator가 스코프를 축소하여 빈약한 결과물 생성.

이 스킬 적용: Planner가 `spec.md` Section 5 "Must-Include Concrete Content"에
세션 실제 코드·에러·수치를 고정. 누락 시 Originality Hard fail.

## 7. 비선형 반복 발견

> "중간 라운드가 최종보다 나을 수 있다. 라운드가 갈수록 복잡도가 불필요하게 늘어나는
> 경향이 있다."

이 스킬 적용:
- `handoff.md`에 "Best version so far" 번호 기록.
- Evaluator의 "Iteration Quality Note"에서 직전 라운드 대비 상승/정체/하락 판정.
- 최종 확정 전 중간 라운드 드래프트와 비교 판단.

## 8. 급진적 단순화 실패 교훈

원문: 하네스 부품을 한꺼번에 제거하면 성능 재현 불가.

이 스킬 적용: 모델 업그레이드 시 **한 번에 하나씩** 제거하며 측정.
SKILL.md "Iteration Wisdom" 섹션에 명시.

## 9. 하네스 공간은 축소가 아닌 이동

> "모델이 개선되어도 하네스 조합 공간은 줄지 않는다. 이동한다. 비하중 부품은 제거하되
> 더 큰 역량을 위한 새 부품을 추가하라."

이 스킬의 미래 확장 예시:
- 이미지 비전 Evaluator (렌더된 PNG의 가독성 자동 판정).
- 코드 실행 샌드박스 (스니펫 실제 실행 확인).
- 검색엔진 스니펫 시뮬레이터 (SEO 제목·메타 description 실제 Google 미리보기 재현).

---

## 원문 실험 규모 수치 (보존)

하네스 비용·복잡도 직관을 전달하기 위해 원문에 등장한 구체 수치를 보존.

| 실험 | Tier | Wall-clock | 비용 (API) | 구조 규모 |
|---|---|---|---|---|
| V1 game maker | Full (sprint 기반) | ~6시간 | ~$200 | 16 features / 10 sprints, sprint3의 Evaluator가 27개 acceptance criteria 검증 |
| V2 Digital Audio Workstation (DAW) | Simplified (sprint 제거) | 3시간 50분 | $124.70 | 단일 연속 Generator 실행, 최종 Evaluator 1회 |
| Dutch Art Museum page | V1 | (미공개) | (미공개) | 10 iterations — iter 1–9 vs iter 10 근본 전환 |

**수치가 전달하는 것**:
- Full 하네스는 시간·비용 모두 **Simplified 대비 약 1.5–1.6배**. 단순 작업에 Full을 쓰면 낭비.
- V2 DAW가 V1 game보다 복잡도 낮아서가 아니라, **모델(Opus 4.5→4.6) 개선으로 sprint·reset이
  load-bearing이 아니게 되어** 제거된 것. 같은 규모에서 하네스만 경량화한 비교.
- sprint3 27 criteria는 **단일 sprint 내 검증 밀도**의 최대치 참고점. 스킬의 Sprint Contract
  체크박스는 라운드당 10–20개 범위가 현실적.

이 숫자들은 사용자가 "내 블로그에 하네스가 과잉인가 적정인가"를 가늠하는 앵커다.

---

## 원문 키워드 Quick Reference

- **Context anxiety** — 세션이 길어질수록 조기 종결하려는 편향. Compaction으로 해결 불가.
- **Strategic role separation** — Generator ≠ Evaluator. 같은 세션이 아니라 다른 subagent.
- **Sprint contract** — 구현 전 관찰 가능한 acceptance criteria 합의.
- **Handoff file** — 컨텍스트 리셋 시 다음 세션이 읽는 단일 진실 원천.
- **Rubric calibration** — LLM 평가자는 out-of-the-box로 너무 관대. few-shot으로 교정.
- **Strategic pivot** — 정체 시 관점·구조 전면 전환. 단일 패스 모델에는 없는 도약.
- **Load-bearing component** — 하네스 각 부품은 "모델이 혼자 못 하는 것"을 가정. 검증 필수.
