# Generative Dynamics Research Greenhouse

This repository contains an exploratory research programme on generative-dynamical architectures of meaningful worlds.

## Programme complete

The planned greenhouse programme is **complete**. All ten runs (`RUN-001` through
`RUN-010`) are accounted for, all three pilots are complete at eight sources
each, and there is no active or queued run. Start with the
[`final harvest`](research/HARVEST.md) for the findings and limitations, then use
[`research/CONTROL.md`](research/CONTROL.md) or
[`research/STATE.json`](research/STATE.json) to verify the terminal checkpoint.

Do not interpret historical bootstrap fixtures, preflight records, or run-log
entries as current progress. They intentionally preserve earlier lifecycle
states for testing and provenance. New research requires explicit authorization
and a deliberately defined programme; it must not silently append `RUN-011`.

- Read [`research/CONTROL.md`](research/CONTROL.md) for the current checkpoint and the exact next action.
- Use [`research/HOLIDAY_RUNBOOK.md`](research/HOLIDAY_RUNBOOK.md) for the completion-review and optional restart routine.
- Read [`AGENTS.md`](AGENTS.md) before changing research state.
- Treat [`research/STATE.json`](research/STATE.json) as the authoritative machine-readable state.
- Run `python scripts/research_guard.py validate` before committing.

The programme is explicitly exploratory. It is not a systematic review or a publication-ready academic manuscript.
