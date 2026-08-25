# Holiday runbook

## What runs with the computer off

Any task already submitted to the Codex cloud environment `gen-dynamics-greenhouse` runs remotely and does not need the desktop app or this computer to remain open.

The next research run does **not** start automatically. This is the usage and drift safety gate: one cloud task may complete at most one bounded run, then it stops at a committed checkpoint.

## Start one session

1. Open `https://chatgpt.com/codex` on any computer or phone.
2. Select environment `gen-dynamics-greenhouse`.
3. Select the durable branch shown in `research/CONTROL.md` (`main` when no run or PR is active).
4. Submit:

   > CONTINUE. Resume from the repository checkpoint. Read AGENTS.md and research/STATE.json first, run `python scripts/research_guard.py recover-check`, execute at most the one authorized bounded run, checkpoint every meaningful step, and do not begin another run.

5. Close the device if desired. The submitted cloud task continues remotely.

## Daily harvest

Later, open the task result and `research/CONTROL.md`. Spend at most 15 minutes.

- If `DECISIONS: none`, start another session only when you want to spend another bounded run.
- If a decision appears, reply only `DEC-### A` or `DEC-### B` as shown.
- If status is `USAGE-PAUSED`, do nothing until usage is available; then start a fresh task with `CONTINUE`.
- If you skip a day, nothing drifts. The repository checkpoint remains authoritative.

## Scheduling

Do not schedule automatic research execution during this holiday experiment. A web scheduled task may be used only as a reminder to inspect `CONTROL.md`; it must not begin runs, choose decisions, add sources, or bypass `usage_paused`.
