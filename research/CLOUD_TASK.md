# Cloud Task Prompt

Use this prompt to start or resume the greenhouse in a fresh Codex cloud task:

> Resume the budget-adaptive research greenhouse from the repository checkpoint. Read `AGENTS.md` and `research/STATE.json` before interpreting the research, then run `python scripts/research_guard.py recover-check`. Treat `active_branch` as the durable source branch; Codex cloud's ephemeral local branch name (for example `work`) is not itself a conflict. Inspect the active PR if present. If a run is active, resume `next_atomic_action` without repeating committed steps or sources. If the programme is ready, begin only `next_run`. Complete at most one bounded run, keep within its source and pass budgets, checkpoint after every meaningful step, run the validator and tests, and open or update one PR. Do not begin the following run. If usage becomes constrained, checkpoint and pause. If a protected decision is required, create one compact decision card and pause only that lane.

The ordinary daily responses are:

- `CONTINUE` — run only the next authorized bounded run.
- `DEC-### A` or `DEC-### B` — resolve the displayed decision, then continue only if repository state permits.

No conversational history is required. If the prompt and repository disagree, the repository wins.
