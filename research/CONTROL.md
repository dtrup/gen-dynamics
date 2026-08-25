# Research Greenhouse Control

**STATUS:** GREEN
**LAST SAFE CHECKPOINT:** HEAD (RUN-000)
**COMPLETED SINCE LAST CHECK:** Greenhouse control system prepared locally.
**CLAIMS ADVANCED / WEAKENED:** None; baseline is the next run.
**CURRENT BEST FINDING:** No empirical finding yet.
**NEXT ATOMIC ACTION:** Begin RUN-001 and baseline the core claims without adding sources.
**DECISIONS:** none
**REPLY:** CONTINUE

> This is an exploratory, budget-adaptive programme. Missing a check-in leaves it idle and resumable.

## Active run

- Programme state: `ready`
- Usage mode: `normal`
- Active run: none
- Active branch: `main`
- Active PR: `none`
- Active pilot: `none`

## Pilot budgets

| Pilot | Status | Sources | Runs without gain |
| --- | --- | ---: | ---: |
| `threat-avoidance` | queued | 0/8 | 0/2 |
| `fear-conditioning` | queued | 0/8 | 0/2 |
| `fiat-money` | queued | 0/8 | 0/2 |

## Queue

- `RUN-001` [programme] — Baseline the core claims and scorecard.
- `RUN-002` [threat-avoidance] — Compare semantic intervention with conditioned-response rivals in threat and avoidance.
- `RUN-003` [threat-avoidance] — Test effective-field, feedback, perturbation, and hysteresis claims in threat and avoidance.
- `RUN-004` [fear-conditioning] — Construct the strongest lower-level account of Pavlovian fear conditioning.
- `RUN-005` [fear-conditioning] — Determine the semantic boundary and required revisions from fear conditioning.
- `RUN-006` [fiat-money] — Test carrier variation and meaning-sensitive consequences in fiat money.
- `RUN-007` [fiat-money] — Separate representation, coordination, infrastructure, enforcement, and power in fiat money.
- `RUN-008` [programme] — Compare all pilots using the common case protocol.
- `RUN-009` [programme] — Run a subtraction pass and propose validated synthesis clarifications.
- `RUN-010` [programme] — Produce the final or partial harvest and leave a clean resume point.

## Open decisions

None.

## Fresh-task recovery

1. Read `AGENTS.md` and `research/STATE.json` before interpreting the research.
2. Run `python scripts/research_guard.py recover-check` and inspect the PR if active.
3. Treat `active_branch` as the durable source branch; an ephemeral cloud branch such as `work` is not a conflict.
4. Compare committed artifacts with `completed_steps`.
5. Resume `next_atomic_action`; do not repeat completed steps or duplicate sources.
6. Validate and commit after the next atomic step.

The machine-readable source of truth is `research/STATE.json`; regenerate this dashboard with `python scripts/research_guard.py render`.
