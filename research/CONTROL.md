# Research Greenhouse Control

**STATUS:** GREEN
**LAST SAFE CHECKPOINT:** HEAD (RUN-010)
**COMPLETED SINCE LAST CHECK:** Completed the full planned programme, RUN-001 through RUN-010.
**CLAIMS ADVANCED / WEAKENED:** No final claim maturity changed; all outcomes remain provisional, the synthesis is unchanged, and the programme closes without an open decision.
**CURRENT BEST FINDING:** The programme did not validate a substantive cross-domain architecture; it delivered a semantic-causal test, cross-scale typing discipline, explicit rivals, and bounded requirements for future advancement.
**NEXT ATOMIC ACTION:** No planned run remains; review the final harvest.
**DECISIONS:** none
**REPLY:** REVIEW

> This is an exploratory, budget-adaptive programme. Missing a check-in leaves it idle and resumable.

## Active run

- Programme state: `complete`
- Usage mode: `normal`
- Active run: none
- Active branch: `work`
- Active PR: `none`
- Active pilot: `none`

## Pilot budgets

| Pilot | Status | Sources | Runs without gain |
| --- | --- | ---: | ---: |
| `threat-avoidance` | complete | 8/8 | 0/2 |
| `fear-conditioning` | complete | 8/8 | 0/2 |
| `fiat-money` | complete | 8/8 | 0/2 |

## Queue

- No planned runs remain.

## Open decisions

None.

## Fresh-task recovery

1. Read `AGENTS.md` and `research/STATE.json` before interpreting the research.
2. Run `python scripts/research_guard.py recover-check` and inspect any recorded PR.
3. Treat `active_branch` as the durable source branch; an ephemeral cloud branch such as `work` is not a conflict.
4. Compare committed artifacts with `completed_steps`.
5. Resume `next_atomic_action`; do not repeat completed steps or duplicate sources.
6. Validate and commit after the next atomic step.

The machine-readable source of truth is `research/STATE.json`; regenerate this dashboard with `python scripts/research_guard.py render`.
