# Cloud Task Prompt

The planned greenhouse is complete through `RUN-010`. Use this prompt to review
it in a fresh Codex cloud task:

> Review the completed research greenhouse from the repository checkpoint. Read `AGENTS.md`, `research/STATE.json`, `research/CONTROL.md`, and `research/HARVEST.md` before interpreting the research, then run `python scripts/research_guard.py recover-check`. Treat the machine-readable state as authoritative: `RUN-001` through `RUN-010` and all three pilots are complete, no run is active or queued, and historical bootstrap fixtures and preflight text are not current progress. Summarize the harvest and its limitations without presenting it as systematic or publication ready. Do not begin or invent `RUN-011`, add sources, or modify the protected synthesis. New research requires an explicit user choice of a backlog opportunity and a deliberately bounded new or replacement programme. Follow the branch and PR lifecycle in `AGENTS.md` for any changes.

The ordinary daily responses are:

- `CONTINUE` — valid only after a user has explicitly authorized and defined a new programme in repository state.
- `DEC-### A` or `DEC-### B` — resolve the displayed decision, then continue only if repository state permits.
- `REVIEW` — no planned run remains; inspect the harvest before authorizing any new programme.

No conversational history is required. If the prompt and repository disagree, the repository wins.
