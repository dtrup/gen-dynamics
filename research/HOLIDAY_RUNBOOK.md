# Holiday runbook (programme complete)

## Current disposition

The planned programme completed `RUN-001` through `RUN-010`. No research run is
active or queued. The ordinary action is now `REVIEW`: inspect
`research/HARVEST.md` and confirm the terminal state in `research/CONTROL.md`.
The run-start instructions below are retained only for a future programme that
a user explicitly authorizes and defines; they must not be used to infer that
only an early run is complete or to create `RUN-011` automatically.

## What runs with the computer off

Any task already submitted to the Codex cloud environment `gen-dynamics-greenhouse` runs remotely and does not need the desktop app or this computer to remain open.

The next research run does **not** start automatically. This is the usage and drift safety gate: one cloud task may complete at most one bounded run, then it stops at a committed checkpoint.

## Review the completed programme

1. Open `https://chatgpt.com/codex` on any computer or phone.
2. Select environment `gen-dynamics-greenhouse`.
3. Select the durable branch shown in `research/CONTROL.md`.
4. Submit:

   > REVIEW. Read AGENTS.md, research/STATE.json, research/CONTROL.md, and research/HARVEST.md first, then run `python scripts/research_guard.py recover-check`. Confirm that RUN-001 through RUN-010 are complete and summarize the bounded findings and limitations. Do not begin or invent another run.

5. Close the device if desired. The submitted cloud task continues remotely.

## Daily harvest

Later, open the task result and `research/CONTROL.md`. Spend at most 15 minutes.

- If status is `complete` and `DECISIONS: none`, leave the programme idle unless you explicitly authorize and define new work.
- If a decision appears, reply only `DEC-### A` or `DEC-### B` as shown.
- If a future authorized programme is `USAGE-PAUSED`, do nothing until usage is available; then resume from its recorded checkpoint.
- If you skip a day, nothing drifts. The repository checkpoint remains authoritative.

## Scheduling

Do not schedule automatic research execution during this holiday experiment. A web scheduled task may be used only as a reminder to inspect `CONTROL.md`; it must not begin runs, choose decisions, add sources, or bypass `usage_paused`.
