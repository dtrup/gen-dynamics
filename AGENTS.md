# Research Greenhouse Constitution

## Mission

Improve the empirical discrimination of the architecture in the root synthesis through bounded, resumable research runs. Progress means that claims become better bounded, rivalled, operationalized, tested, retained, revised, or rejected. More words are not progress by themselves.

The programme is exploratory. Never represent its outputs as exhaustive, systematic, original, peer reviewed, or publication ready.

## Mandatory startup and recovery

Every fresh task must do these steps before interpreting the research:

1. Fetch `main` and the branch named in `research/STATE.json`, when a remote is available.
2. Read this file, then `research/STATE.json`, then `research/CONTROL.md`, `research/CLAIMS.md`, and the active pilot report.
3. Inspect the active PR and the commit referenced by `latest_checkpoint_commit`. `HEAD` means the commit containing the checked-out state file.
4. If `programme_status` is `running`, compare committed artifacts with `completed_steps`; resume `next_atomic_action` without repeating completed steps.
5. Deduplicate evidence by DOI, stable URL, or source identifier.
6. Run `python scripts/research_guard.py validate` before changing state.

Never restart a pilot because a prior chat is unavailable. Repository state, not conversational memory, is authoritative.

If branch, PR, artifacts, and state disagree, set `programme_status` to `waiting_decision`, add one decision card, avoid editing the synthesis, and continue only unrelated reversible work.

## Run lifecycle

Only one research run and one claim family may be active.

```text
python scripts/research_guard.py begin
python scripts/research_guard.py checkpoint --step "..." --next-action "..."
python scripts/research_guard.py conserve --reason "Usage warning surfaced"
python scripts/research_guard.py pause --reason "Usage unavailable"
python scripts/research_guard.py resume
python scripts/research_guard.py set-pr --pr "<PR URL or number>"
python scripts/research_guard.py complete --finding "..." --claim-change "..."
python scripts/research_guard.py render
python scripts/research_guard.py validate
```

Commit immediately after `begin`, after each source-selection or analytical pass, and after `complete`. A run may contain at most two research passes, four new sources, and one PR. Do not start the next run automatically.

Create the run PR before `complete`, record it with `set-pr`, and retain it in state until a fresh task has verified that it merged or closed. Then use `clear-pr`. A new run cannot begin while an earlier PR remains unresolved.

When usage appears low, finish the current atomic step, add no optional sources, checkpoint, and pause. Never buy credits, upgrade a plan, add an API key, or change billing.

## Evidence standard

Each pilot may use five to eight sources in total and must eventually include:

- at least one review or authoritative overview;
- at least two directly relevant empirical or theoretical sources;
- at least one serious rival treatment;
- at least one methods or measurement source.

For each source record a stable identifier, full citation, evidence type, role, relevant finding, limitation, affected claim, and access URL. Distinguish full-text review from abstract-only inspection. Preserve negative and unresolved results.

Do not perform systematic reviews, meta-analysis, publication formatting, exhaustive historical reconstruction, formal-model estimation, data collection, or novelty searches. Put publication-scale opportunities in `research/PUBLISHABILITY_BACKLOG.md` and stop.

## Rabbit-hole gate

A new path may use one reserve run only if all are true:

1. it could materially change a core claim;
2. it has two independent preliminary signals or one strong direct contradiction;
3. it can deliver discriminating evidence in one run;
4. it replaces a lower-priority run.

Otherwise record it in the backlog. Close a pilot as unresolved after two runs without claim advancement or score improvement. Never add a fourth pilot automatically.

## Claim scorecard

Score each pilot from 0 to 4 on:

1. semantic necessity over lower-level explanation;
2. operational measurability;
3. rival discrimination;
4. perturbation or intervention specificity;
5. evidence quality and independence.

A synthesis clarification is validated only when a linked claim advances at least one maturity stage, at least two sources support the change including a rival source, falsifiers and residual uncertainty are explicit, and no score regresses without explanation.

## Protected commitments

The following synthesis regions require a user decision and must never receive guarded auto-merge:

- the preamble and central claims;
- hierarchy of commitments;
- definitions of semantic control and effective field;
- definition of semantic attractor;
- compression hypothesis;
- current strongest formulation.

Also protect new primitives, operators, universals, cross-scale generalizations, deletion or reframing of central claims, and synthesis changes above 300 net new words.

Safe research infrastructure, checkpoints, pilot reports, bibliography corrections, and small validated clarifications may use the `safe-auto-merge` PR label. Protected changes remain in an open PR with a decision card.

## Decision cards

Keep at most three open. Each card must contain:

- one question of at most 20 words;
- exactly two choices where possible;
- the recommended choice first;
- one-line consequences;
- reversibility and safe default;
- the affected lane.

Use an unanswered recommended default only when reversible. Otherwise pause only the affected lane. Missing check-ins must leave the programme idle and resumable.

## Completion

Every finished run must leave:

- valid `research/STATE.json`;
- regenerated `research/CONTROL.md`;
- updated claim and pilot records;
- an exact `next_atomic_action`;
- no completed work that exists only in chat;
- a passing `python scripts/research_guard.py validate` result.
