## Greenhouse run

- Run ID: `RUN-___`
- Claim family:
- Pilot or programme lane:
- Latest checkpoint: `HEAD`

## Classification

- [ ] Research artifacts or control infrastructure only
- [ ] Validated synthesis clarification
- [ ] Protected thesis-level change — do not auto-merge

## Evidence and validation

- [ ] `research/STATE.json` and `research/CONTROL.md` agree
- [ ] Source and run budgets remain within limits
- [ ] Rivals, falsifiers, and residual uncertainty are recorded
- [ ] `python scripts/research_guard.py validate --base origin/main` passes
- [ ] Unit tests pass

Apply `safe-auto-merge` only when the first or second classification is selected and the guard passes. Never apply it to a protected thesis-level change.
