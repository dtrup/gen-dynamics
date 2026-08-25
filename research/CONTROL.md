# Research Greenhouse Control

**STATUS:** GREEN
**LAST SAFE CHECKPOINT:** HEAD (RUN-001)
**COMPLETED SINCE LAST CHECK:** Compared instruction, incentive, observation, expectancy, and pairing evidence; bounded semantic control against broader component rivals and specified a carrier-by-content test.
**CLAIMS ADVANCED / WEAKENED:** C-002: asserted → bounded
**CURRENT BEST FINDING:** All eight claims now have explicit maturity, boundaries, principal rivals, falsifiers, and candidate measurements; no empirical evidence was added.
**NEXT ATOMIC ACTION:** Create the RUN-002 pull request, record it in state, and then complete the run.
**DECISIONS:** none
**REPLY:** CONTINUE

> This is an exploratory, budget-adaptive programme. Missing a check-in leaves it idle and resumable.

## Active run

- Programme state: `running`
- Usage mode: `normal`
- Active run: RUN-002 — Compare semantic intervention with conditioned-response rivals in threat and avoidance.
- Active branch: `research/run-002`
- Active PR: `none`
- Active pilot: `threat-avoidance`

## Pilot budgets

| Pilot | Status | Sources | Runs without gain |
| --- | --- | ---: | ---: |
| `threat-avoidance` | active | 4/8 | 0/2 |
| `fear-conditioning` | queued | 0/8 | 0/2 |
| `fiat-money` | queued | 0/8 | 0/2 |

## Queue

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
