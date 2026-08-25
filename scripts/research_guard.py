#!/usr/bin/env python3
"""Render, validate, and advance the resumable research greenhouse."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = Path("research/STATE.json")
CONTROL_PATH = Path("research/CONTROL.md")
CLAIMS_PATH = Path("research/CLAIMS.md")

PROGRAMME_STATUSES = {"ready", "running", "waiting_decision", "usage_paused", "complete"}
USAGE_MODES = {"normal", "conserve", "paused"}
CLAIM_STAGES = (
    "asserted",
    "bounded",
    "rivalled",
    "operationalized",
    "preliminarily-tested",
    "retained",
    "revised",
    "rejected",
)
STAGE_RANK = {
    "asserted": 0,
    "bounded": 1,
    "rivalled": 2,
    "operationalized": 3,
    "preliminarily-tested": 4,
    "retained": 5,
    "revised": 5,
    "rejected": 5,
}
PILOT_STATUSES = {"queued", "active", "complete", "unresolved"}
REQUIRED_STATE_KEYS = {
    "schema_version",
    "programme_status",
    "usage_mode",
    "last_completed_run",
    "active_run",
    "active_branch",
    "active_pr",
    "active_pilot",
    "completed_steps",
    "next_atomic_action",
    "next_run",
    "run_queue",
    "claim_states",
    "pilot_states",
    "open_decisions",
    "source_counts",
    "reserve_runs",
    "safe_synthesis_change",
    "harvest",
    "latest_checkpoint_commit",
}
PILOT_HEADINGS = (
    "## Status",
    "## Scope",
    "## Claims under test",
    "## Rival explanations",
    "## Evidence ledger",
    "## Scorecard",
    "## Falsifiers",
    "## Residual uncertainty",
    "## Run log",
)
PROTECTED_SECTIONS = {
    "1": "Hierarchy of commitments",
    "7": "What makes control semantic?",
    "8": "The effective field",
    "15": "Semantic attractors",
    "22": "A finite-ish repertoire, reformulated",
    "32": "Current strongest formulation",
}


class GuardError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_state(root: Path = ROOT) -> dict[str, Any]:
    return json.loads((root / STATE_PATH).read_text(encoding="utf-8"))


def write_state(state: dict[str, Any], root: Path = ROOT) -> None:
    (root / STATE_PATH).write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def status_label(programme_status: str) -> str:
    return {
        "ready": "GREEN",
        "running": "GREEN",
        "waiting_decision": "AMBER",
        "usage_paused": "USAGE-PAUSED",
        "complete": "GREEN",
    }.get(programme_status, "RED")


def render_control(state: dict[str, Any]) -> str:
    decisions = state.get("open_decisions", [])
    decision_ids = ", ".join(item.get("id", "UNKNOWN") for item in decisions) or "none"
    reply = "CONTINUE"
    if decisions:
        first_id = decisions[0].get("id", "DEC-???")
        reply = f"{first_id} A | {first_id} B"

    harvest = state.get("harvest", {})
    active = state.get("active_run")
    active_text = "none"
    if isinstance(active, dict):
        active_text = f"{active.get('id', 'UNKNOWN')} — {active.get('objective', 'No objective')}"

    lines = [
        "# Research Greenhouse Control",
        "",
        f"**STATUS:** {status_label(state.get('programme_status', 'invalid'))}",
        f"**LAST SAFE CHECKPOINT:** {state.get('latest_checkpoint_commit', 'missing')} ({state.get('last_completed_run', 'none')})",
        f"**COMPLETED SINCE LAST CHECK:** {harvest.get('completed_since_last_check', 'Nothing recorded.')}",
        f"**CLAIMS ADVANCED / WEAKENED:** {harvest.get('claims_changed', 'None recorded.')}",
        f"**CURRENT BEST FINDING:** {harvest.get('current_best_finding', 'None recorded.')}",
        f"**NEXT ATOMIC ACTION:** {state.get('next_atomic_action', 'None.')}",
        f"**DECISIONS:** {decision_ids}",
        f"**REPLY:** {reply}",
        "",
        "> This is an exploratory, budget-adaptive programme. Missing a check-in leaves it idle and resumable.",
        "",
        "## Active run",
        "",
        f"- Programme state: `{state.get('programme_status', 'invalid')}`",
        f"- Usage mode: `{state.get('usage_mode', 'invalid')}`",
        f"- Active run: {active_text}",
        f"- Active branch: `{state.get('active_branch') or 'none'}`",
        f"- Active PR: `{state.get('active_pr') or 'none'}`",
        f"- Active pilot: `{state.get('active_pilot') or 'none'}`",
        "",
        "## Pilot budgets",
        "",
        "| Pilot | Status | Sources | Runs without gain |",
        "| --- | --- | ---: | ---: |",
    ]
    for pilot, details in state.get("pilot_states", {}).items():
        count = state.get("source_counts", {}).get(pilot, 0)
        lines.append(
            f"| `{pilot}` | {details.get('status', 'invalid')} | {count}/8 | {details.get('runs_without_gain', 0)}/2 |"
        )

    lines.extend(["", "## Queue", ""])
    queue = state.get("run_queue", [])
    if queue:
        for item in queue:
            pilot = item.get("pilot") or "programme"
            lines.append(f"- `{item.get('id')}` [{pilot}] — {item.get('objective')}")
    else:
        lines.append("- No planned runs remain.")

    lines.extend(["", "## Open decisions", ""])
    if not decisions:
        lines.extend(["None.", ""])
    else:
        for item in decisions:
            lines.extend(
                [
                    f"### {item.get('id')}",
                    "",
                    f"**Question:** {item.get('question')}",
                    "",
                    f"- **A — {item.get('choices', [{}, {}])[0].get('label', 'Missing')}:** {item.get('choices', [{}, {}])[0].get('impact', 'Missing impact')}",
                    f"- **B — {item.get('choices', [{}, {}])[1].get('label', 'Missing')}:** {item.get('choices', [{}, {}])[1].get('impact', 'Missing impact')}",
                    f"- Recommended: **{item.get('recommended')}**",
                    f"- Reversible: **{'yes' if item.get('reversible') else 'no'}**",
                    f"- Safe default: **{item.get('safe_default')}**",
                    f"- Affected lane: `{item.get('lane')}`",
                    "",
                ]
            )

    lines.extend(
        [
            "## Fresh-task recovery",
            "",
            "1. Read `AGENTS.md` and `research/STATE.json` before interpreting the research.",
            "2. Run `python scripts/research_guard.py recover-check` and inspect the PR if active.",
            "3. Treat `active_branch` as the durable source branch; an ephemeral cloud branch such as `work` is not a conflict.",
            "4. Compare committed artifacts with `completed_steps`.",
            "5. Resume `next_atomic_action`; do not repeat completed steps or duplicate sources.",
            "6. Validate and commit after the next atomic step.",
            "",
            "The machine-readable source of truth is `research/STATE.json`; regenerate this dashboard with `python scripts/research_guard.py render`.",
            "",
        ]
    )
    return "\n".join(lines)


def render_to_disk(state: dict[str, Any], root: Path = ROOT) -> None:
    (root / CONTROL_PATH).write_text(render_control(state), encoding="utf-8")


def sync_pilot_statuses(state: dict[str, Any], root: Path = ROOT) -> None:
    for details in state.get("pilot_states", {}).values():
        path = root / details["path"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        status_line = f"{details['status'].capitalize()}. Exploratory and not publication ready."
        updated, count = re.subn(
            r"(## Status\s+)([^\n]+)", rf"\g<1>{status_line}", text, count=1, flags=re.DOTALL
        )
        if count == 1:
            path.write_text(updated, encoding="utf-8")


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8", errors="replace", capture_output=True
    )


def ref_exists(root: Path, ref: str) -> bool:
    return git(root, "rev-parse", "--verify", "--quiet", ref).returncode == 0


def recovery_checkout_report(state: dict[str, Any], root: Path = ROOT) -> tuple[dict[str, Any], list[str]]:
    """Verify a fresh checkout without mistaking a cloud runner branch for a durable branch."""
    errors = validate_repository(root)
    head_result = git(root, "rev-parse", "HEAD")
    head_commit = head_result.stdout.strip() if head_result.returncode == 0 else None
    checkout_branch = current_branch(root)
    source_branch = state.get("active_branch") or "main"
    checkpoint = state.get("latest_checkpoint_commit")
    checkpoint_commit = head_commit if checkpoint == "HEAD" else checkpoint

    if not head_commit:
        errors.append("could not resolve checkout HEAD")
    elif checkpoint_commit and not ref_exists(root, str(checkpoint_commit)):
        errors.append(f"checkpoint commit does not exist: {checkpoint_commit}")
    elif checkpoint_commit and git(root, "merge-base", "--is-ancestor", str(checkpoint_commit), "HEAD").returncode != 0:
        errors.append(f"checkout HEAD does not contain checkpoint commit: {checkpoint_commit}")

    worktree = git(root, "status", "--porcelain=v1")
    if worktree.returncode != 0:
        errors.append("could not inspect checkout worktree")
    elif worktree.stdout.strip():
        errors.append("fresh recovery checkout has uncommitted changes")

    remote_ref = f"refs/remotes/origin/{source_branch}"
    remote_ref_available = ref_exists(root, remote_ref)
    if head_commit and remote_ref_available:
        remote_commit = git(root, "rev-parse", remote_ref).stdout.strip()
        if remote_commit != head_commit:
            errors.append(
                f"checkout HEAD {head_commit} does not match expected source ref origin/{source_branch} at {remote_commit}"
            )

    report = {
        "status": "pass" if not errors else "fail",
        "head_commit": head_commit,
        "checkpoint_commit": checkpoint_commit,
        "checkout_branch": checkout_branch,
        "source_branch": source_branch,
        "ephemeral_checkout_branch": checkout_branch not in {source_branch, "unknown"},
        "remote_ref_verified": remote_ref_available,
        "programme_status": state.get("programme_status"),
        "active_run": state.get("active_run", {}).get("id") if state.get("active_run") else None,
        "active_pr": state.get("active_pr"),
        "next_run": state.get("next_run", {}).get("id") if state.get("next_run") else None,
        "next_atomic_action": state.get("next_atomic_action"),
    }
    return report, errors


def source_ids_from_pilot(text: str) -> set[str]:
    return set(re.findall(r"\|\s*(SRC-[A-Za-z0-9._-]+)\s*\|", text))


def validate_state(state: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_STATE_KEYS - state.keys())
    if missing:
        errors.append(f"STATE.json is missing keys: {', '.join(missing)}")
        return errors

    if state["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if state["programme_status"] not in PROGRAMME_STATUSES:
        errors.append(f"invalid programme_status: {state['programme_status']}")
    if state["usage_mode"] not in USAGE_MODES:
        errors.append(f"invalid usage_mode: {state['usage_mode']}")
    if len(state["open_decisions"]) > 3:
        errors.append("no more than three decision cards may be open")

    pilot_names = set(state["pilot_states"])
    if len(pilot_names) > 3:
        errors.append("a fourth pilot is not allowed")
    if set(state["source_counts"]) != pilot_names:
        errors.append("source_counts keys must match pilot_states keys")
    for pilot, details in state["pilot_states"].items():
        if details.get("status") not in PILOT_STATUSES:
            errors.append(f"{pilot}: invalid pilot status")
        if not isinstance(details.get("runs_without_gain"), int) or details.get("runs_without_gain", 0) < 0:
            errors.append(f"{pilot}: runs_without_gain must be a non-negative integer")
        count = state["source_counts"].get(pilot)
        if not isinstance(count, int) or not 0 <= count <= 8:
            errors.append(f"{pilot}: source count must be between 0 and 8")
        if details.get("status") == "complete" and (not isinstance(count, int) or count < 5):
            errors.append(f"{pilot}: a completed pilot requires at least five sources")

    for claim_id, stage in state["claim_states"].items():
        if not re.fullmatch(r"C-\d{3}", claim_id):
            errors.append(f"invalid claim id: {claim_id}")
        if stage not in STAGE_RANK:
            errors.append(f"{claim_id}: invalid maturity stage {stage}")

    queue = state["run_queue"]
    ids = [item.get("id") for item in queue]
    if len(ids) != len(set(ids)):
        errors.append("run_queue contains duplicate run ids")
    for item in queue:
        if not re.fullmatch(r"RUN-\d{3}", str(item.get("id", ""))):
            errors.append(f"invalid run id: {item.get('id')}")
        if item.get("pilot") is not None and item.get("pilot") not in pilot_names:
            errors.append(f"{item.get('id')}: unknown pilot {item.get('pilot')}")
        if not isinstance(item.get("max_new_sources"), int) or not 0 <= item.get("max_new_sources", -1) <= 4:
            errors.append(f"{item.get('id')}: max_new_sources must be between 0 and 4")

    expected_next = queue[0] if queue else None
    if state["next_run"] != expected_next:
        errors.append("next_run must equal the first run_queue item")
    if state["programme_status"] == "running" and not isinstance(state["active_run"], dict):
        errors.append("running programme requires active_run")
    if state["active_run"] is not None and state["active_run"].get("id") not in ids:
        errors.append("active_run must still be present in run_queue")
    if state["programme_status"] == "complete" and queue:
        errors.append("complete programme cannot retain queued runs")

    reserve = state["reserve_runs"]
    if not isinstance(reserve.get("remaining"), int) or not 0 <= reserve.get("remaining", -1) <= 2:
        errors.append("reserve_runs.remaining must be between 0 and 2")

    for decision in state["open_decisions"]:
        required = {"id", "question", "choices", "recommended", "reversible", "safe_default", "lane"}
        if required - decision.keys():
            errors.append(f"decision {decision.get('id', 'UNKNOWN')} is incomplete")
            continue
        if len(decision["question"].split()) > 20:
            errors.append(f"{decision['id']}: question exceeds 20 words")
        if len(decision["choices"]) != 2:
            errors.append(f"{decision['id']}: exactly two choices are required")
        if decision["recommended"] not in {"A", "B"} or decision["safe_default"] not in {"A", "B", "pause"}:
            errors.append(f"{decision['id']}: invalid recommendation or safe default")
        if not isinstance(decision["reversible"], bool):
            errors.append(f"{decision['id']}: reversible must be boolean")

    checkpoint = state["latest_checkpoint_commit"]
    if checkpoint != "HEAD" and not re.fullmatch(r"[0-9a-f]{40}", str(checkpoint)):
        errors.append("latest_checkpoint_commit must be HEAD or a full commit hash")
    elif checkpoint != "HEAD" and not ref_exists(root, checkpoint):
        errors.append(f"checkpoint commit does not exist: {checkpoint}")

    safe_change = state["safe_synthesis_change"]
    if safe_change is not None:
        required = {"classification", "claim_id", "maturity_from", "maturity_to", "source_ids", "rival_source_id"}
        if required - safe_change.keys():
            errors.append("safe_synthesis_change is incomplete")
        elif safe_change["classification"] != "clarification":
            errors.append("only clarification may be marked as a safe synthesis change")

    return errors


def validate_artifacts(state: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for required_path in (
        "AGENTS.md",
        "research/PUBLISHABILITY_BACKLOG.md",
        "research/CLOUD_TASK.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/research-guard.yml",
    ):
        if not (root / required_path).exists():
            errors.append(f"required greenhouse artifact is missing: {required_path}")
    control = root / CONTROL_PATH
    if not control.exists():
        errors.append("research/CONTROL.md is missing; run the render command")
    elif control.read_text(encoding="utf-8") != render_control(state):
        errors.append("research/CONTROL.md is stale; run the render command")

    claims = root / CLAIMS_PATH
    if not claims.exists():
        errors.append("research/CLAIMS.md is missing")
    else:
        claims_text = claims.read_text(encoding="utf-8")
        for claim_id in state["claim_states"]:
            if claim_id not in claims_text:
                errors.append(f"research/CLAIMS.md is missing {claim_id}")
                continue
            table_row = next(
                (line for line in claims_text.splitlines() if re.match(rf"^\|\s*{re.escape(claim_id)}\s*\|", line)),
                None,
            )
            if table_row:
                cells = [cell.strip() for cell in table_row.strip().strip("|").split("|")]
                if len(cells) < 4 or cells[3] != state["claim_states"][claim_id]:
                    errors.append(f"research/CLAIMS.md maturity for {claim_id} does not match STATE.json")
            else:
                errors.append(f"research/CLAIMS.md has no register row for {claim_id}")

    for pilot, details in state["pilot_states"].items():
        path = root / details["path"]
        if not path.exists():
            errors.append(f"{pilot}: pilot report is missing at {details['path']}")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in PILOT_HEADINGS:
            if heading not in text:
                errors.append(f"{pilot}: missing heading {heading}")
        status_section = re.search(r"## Status\s+(.+?)(?=\n## |\Z)", text, flags=re.DOTALL)
        if status_section and details["status"].lower() not in status_section.group(1).lower():
            errors.append(f"{pilot}: report status does not match STATE.json")
        source_ids = source_ids_from_pilot(text)
        if len(source_ids) != state["source_counts"][pilot]:
            errors.append(
                f"{pilot}: STATE source count is {state['source_counts'][pilot]}, report contains {len(source_ids)} unique source rows"
            )
        if details["status"] == "complete":
            roles = {role: len(re.findall(rf"\[{role}\]", text, flags=re.IGNORECASE)) for role in ("review", "direct", "rival", "methods")}
            if roles["review"] < 1 or roles["direct"] < 2 or roles["rival"] < 1 or roles["methods"] < 1:
                errors.append(f"{pilot}: completed evidence ledger lacks the required role mix")
    return errors


def extract_level_one_section(text: str, section: str | None) -> str:
    lines = text.splitlines()
    if section is None:
        for index, line in enumerate(lines):
            if re.match(r"^#\s+1\.", line):
                return "\n".join(lines[:index]).strip()
        return text.strip()
    start = None
    pattern = re.compile(rf"^#\s+{re.escape(section)}\.")
    for index, line in enumerate(lines):
        if pattern.match(line):
            start = index
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("# "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def read_git_file(root: Path, ref: str, relative_path: str) -> str | None:
    result = git(root, "show", f"{ref}:{relative_path}")
    return result.stdout if result.returncode == 0 else None


def changed_files(root: Path, base: str) -> list[str]:
    result = git(root, "-c", "core.quotepath=false", "diff", "--name-only", f"{base}...HEAD")
    if result.returncode != 0:
        raise GuardError(result.stderr.strip() or f"could not diff {base}...HEAD")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def diff_word_counts(root: Path, base: str, path: str) -> tuple[int, int]:
    result = git(root, "diff", "--unified=0", f"{base}...HEAD", "--", path)
    if result.returncode != 0:
        raise GuardError(result.stderr.strip())
    added = 0
    removed = 0
    for line in result.stdout.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added += len(re.findall(r"\b[\w'-]+\b", line[1:]))
        elif line.startswith("-"):
            removed += len(re.findall(r"\b[\w'-]+\b", line[1:]))
    return added, removed


def validate_synthesis_diff(state: dict[str, Any], root: Path, base: str) -> list[str]:
    errors: list[str] = []
    if not ref_exists(root, base):
        return [f"base ref does not exist: {base}"]
    try:
        files = changed_files(root, base)
    except GuardError as exc:
        return [str(exc)]
    synthesis_paths = [path for path in files if path.startswith("Toward") and path.endswith(".md")]
    if not synthesis_paths:
        return errors
    if len(synthesis_paths) != 1:
        return ["expected exactly one synthesis document"]

    path = synthesis_paths[0]
    old_text = read_git_file(root, base, path)
    if old_text is None:
        return errors  # Initial repository bootstrap.
    new_text = (root / path).read_text(encoding="utf-8")

    if extract_level_one_section(old_text, None) != extract_level_one_section(new_text, None):
        errors.append("protected synthesis preamble changed")
    for number, label in PROTECTED_SECTIONS.items():
        if extract_level_one_section(old_text, number) != extract_level_one_section(new_text, number):
            errors.append(f"protected synthesis section changed: {number}. {label}")

    added, removed = diff_word_counts(root, base, path)
    if added - removed > 300:
        errors.append(f"synthesis adds {added - removed} net words; guarded limit is 300")

    safe = state.get("safe_synthesis_change")
    if safe is None:
        errors.append("synthesis changed without safe_synthesis_change metadata")
        return errors
    if safe.get("classification") != "clarification":
        errors.append("synthesis change is not classified as a clarification")
    source_ids = safe.get("source_ids", [])
    if len(set(source_ids)) < 2:
        errors.append("safe synthesis clarification requires at least two source ids")
    if safe.get("rival_source_id") not in source_ids:
        errors.append("rival_source_id must be included in source_ids")
    recorded_source_ids: set[str] = set()
    for details in state["pilot_states"].values():
        pilot_path = root / details["path"]
        if pilot_path.exists():
            recorded_source_ids.update(source_ids_from_pilot(pilot_path.read_text(encoding="utf-8")))
    missing_sources = sorted(set(source_ids) - recorded_source_ids)
    if missing_sources:
        errors.append(f"safe synthesis clarification references unrecorded sources: {', '.join(missing_sources)}")
    claim_id = safe.get("claim_id")
    if claim_id not in state["claim_states"]:
        errors.append("safe synthesis clarification references an unknown claim")

    old_state_text = read_git_file(root, base, STATE_PATH.as_posix())
    if old_state_text:
        old_state = json.loads(old_state_text)
        old_stage = old_state.get("claim_states", {}).get(claim_id)
        new_stage = state["claim_states"].get(claim_id)
        if old_stage not in STAGE_RANK or new_stage not in STAGE_RANK or STAGE_RANK[new_stage] <= STAGE_RANK[old_stage]:
            errors.append("linked claim did not advance a maturity stage")
        if safe.get("maturity_from") != old_stage or safe.get("maturity_to") != new_stage:
            errors.append("safe synthesis maturity metadata does not match the state transition")
    return errors


def validate_repository(root: Path = ROOT, base: str | None = None) -> list[str]:
    try:
        state = load_state(root)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"could not load research/STATE.json: {exc}"]
    errors = validate_state(state, root)
    if not errors:
        errors.extend(validate_artifacts(state, root))
    if base:
        errors.extend(validate_synthesis_diff(state, root, base))
    return errors


def save_and_render(state: dict[str, Any], root: Path = ROOT) -> None:
    state["latest_checkpoint_commit"] = "HEAD"
    write_state(state, root)
    sync_pilot_statuses(state, root)
    render_to_disk(state, root)


def save_transactionally(state: dict[str, Any], root: Path = ROOT) -> None:
    state_path = root / STATE_PATH
    control_path = root / CONTROL_PATH
    old_state = state_path.read_bytes()
    old_control = control_path.read_bytes() if control_path.exists() else None
    pilot_backups = {
        root / details["path"]: (root / details["path"]).read_bytes()
        for details in state.get("pilot_states", {}).values()
        if (root / details["path"]).exists()
    }
    save_and_render(state, root)
    errors = validate_repository(root)
    if errors:
        state_path.write_bytes(old_state)
        if old_control is None:
            control_path.unlink(missing_ok=True)
        else:
            control_path.write_bytes(old_control)
        for path, content in pilot_backups.items():
            path.write_bytes(content)
        raise GuardError("update would leave invalid repository state: " + "; ".join(errors))


def current_branch(root: Path = ROOT) -> str:
    result = git(root, "branch", "--show-current")
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else "unknown"


def begin_run(state: dict[str, Any], branch: str | None = None) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if state["programme_status"] != "ready":
        raise GuardError(f"cannot begin while programme_status is {state['programme_status']}")
    if state.get("active_pr"):
        raise GuardError("inspect and clear the previous active PR before beginning another run")
    if not state["run_queue"]:
        raise GuardError("no queued run remains")
    run = copy.deepcopy(state["run_queue"][0])
    run.update({"started_at": utc_now(), "research_passes_completed": 0, "new_sources_this_run": 0})
    state["active_run"] = run
    state["active_pilot"] = run.get("pilot")
    state["active_branch"] = branch or current_branch()
    state["active_pr"] = None
    state["completed_steps"] = []
    state["programme_status"] = "running"
    state["usage_mode"] = "normal"
    state["next_atomic_action"] = f"Execute the first bounded pass for {run['id']}: {run['objective']}"
    if run.get("pilot"):
        state["pilot_states"][run["pilot"]]["status"] = "active"
    state["harvest"]["completed_since_last_check"] = f"Started {run['id']}."
    state["harvest"]["next_recommendation"] = state["next_atomic_action"]
    return state


def checkpoint_run(
    state: dict[str, Any], step: str, next_action: str, research_pass: bool = False, new_sources: int = 0
) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if state["programme_status"] != "running" or not state["active_run"]:
        raise GuardError("checkpoint requires an active running run")
    active = state["active_run"]
    if research_pass:
        active["research_passes_completed"] += 1
        if active["research_passes_completed"] > 2:
            raise GuardError("a run may contain at most two research passes")
    if new_sources < 0:
        raise GuardError("new source count cannot be negative")
    active["new_sources_this_run"] += new_sources
    if active["new_sources_this_run"] > active["max_new_sources"]:
        raise GuardError("run source budget exceeded")
    pilot = active.get("pilot")
    if new_sources and not pilot:
        raise GuardError("programme-level runs cannot add pilot sources")
    if pilot:
        state["source_counts"][pilot] += new_sources
        if state["source_counts"][pilot] > 8:
            raise GuardError("pilot source budget exceeded")
    if step not in state["completed_steps"]:
        state["completed_steps"].append(step)
    state["next_atomic_action"] = next_action
    state["harvest"]["completed_since_last_check"] = step
    state["harvest"]["next_recommendation"] = next_action
    return state


def advance_claim(state: dict[str, Any], claim_id: str, target: str) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if state["programme_status"] != "running":
        raise GuardError("claim advancement requires an active run")
    if claim_id not in state["claim_states"]:
        raise GuardError(f"unknown claim: {claim_id}")
    if target not in STAGE_RANK:
        raise GuardError(f"invalid maturity stage: {target}")
    current = state["claim_states"][claim_id]
    if STAGE_RANK[target] <= STAGE_RANK[current]:
        raise GuardError(f"claim must advance beyond {current}")
    state["claim_states"][claim_id] = target
    state["harvest"]["claims_changed"] = f"{claim_id}: {current} → {target}"
    return state


def pause_programme(state: dict[str, Any], reason: str) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if state["programme_status"] not in {"ready", "running", "waiting_decision"}:
        raise GuardError(f"cannot pause while programme_status is {state['programme_status']}")
    state["programme_status"] = "usage_paused"
    state["usage_mode"] = "paused"
    state["next_atomic_action"] = f"Resume from the last checkpoint. Pause reason: {reason}"
    state["harvest"]["completed_since_last_check"] = f"Paused safely: {reason}"
    state["harvest"]["next_recommendation"] = "Resume only when usage is available."
    return state


def conserve_programme(state: dict[str, Any], reason: str) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if state["programme_status"] != "running" or not state["active_run"]:
        raise GuardError("conserve requires an active running run")
    state["usage_mode"] = "conserve"
    state["next_atomic_action"] = (
        f"Finish only the current atomic step, add no optional sources, then checkpoint and pause. Reason: {reason}"
    )
    state["harvest"]["next_recommendation"] = state["next_atomic_action"]
    return state


def resume_programme(state: dict[str, Any]) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if state["programme_status"] != "usage_paused":
        raise GuardError("resume requires programme_status usage_paused")
    state["programme_status"] = "running" if state["active_run"] else "ready"
    state["usage_mode"] = "normal"
    state["harvest"]["completed_since_last_check"] = "Resumed from the last safe checkpoint."
    state["harvest"]["next_recommendation"] = state["next_atomic_action"]
    return state


def complete_run(state: dict[str, Any], finding: str, claim_change: str) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if state["programme_status"] != "running" or not state["active_run"]:
        raise GuardError("complete requires an active running run")
    active = state["active_run"]
    if not state["run_queue"] or state["run_queue"][0]["id"] != active["id"]:
        raise GuardError("active run does not match the queue head")
    pilot = active.get("pilot")
    state["run_queue"].pop(0)
    state["last_completed_run"] = active["id"]
    if pilot:
        future_for_pilot = any(item.get("pilot") == pilot for item in state["run_queue"])
        if future_for_pilot:
            state["pilot_states"][pilot]["status"] = "active"
        elif 5 <= state["source_counts"][pilot] <= 8:
            state["pilot_states"][pilot]["status"] = "complete"
        else:
            raise GuardError(f"final run for {pilot} requires five to eight sources")
    state["active_run"] = None
    state["active_pilot"] = None
    state["completed_steps"] = [f"Completed {active['id']}: {active['objective']}"]
    state["next_run"] = state["run_queue"][0] if state["run_queue"] else None
    if state["next_run"]:
        state["programme_status"] = "ready"
        state["next_atomic_action"] = f"Begin {state['next_run']['id']}: {state['next_run']['objective']}"
    else:
        state["programme_status"] = "complete"
        state["next_atomic_action"] = "No planned run remains; review the final harvest."
    state["harvest"] = {
        "completed_since_last_check": f"Completed {active['id']}.",
        "claims_changed": claim_change,
        "current_best_finding": finding,
        "next_recommendation": state["next_atomic_action"],
    }
    return state


def set_active_pr(state: dict[str, Any], pr: str | None) -> dict[str, Any]:
    state = copy.deepcopy(state)
    state["active_pr"] = pr
    if pr:
        state["harvest"]["completed_since_last_check"] = f"Recorded active PR {pr}."
    else:
        state["harvest"]["completed_since_last_check"] = "Verified and cleared the previous active PR."
    return state


def mark_safe_change(
    state: dict[str, Any], claim_id: str, maturity_from: str, maturity_to: str, sources: str, rival: str
) -> dict[str, Any]:
    state = copy.deepcopy(state)
    source_ids = [item.strip() for item in sources.split(",") if item.strip()]
    if claim_id not in state["claim_states"]:
        raise GuardError(f"unknown claim: {claim_id}")
    if maturity_from not in STAGE_RANK or maturity_to not in STAGE_RANK:
        raise GuardError("invalid maturity stage")
    if STAGE_RANK[maturity_to] <= STAGE_RANK[maturity_from]:
        raise GuardError("safe clarification requires a maturity advance")
    if len(set(source_ids)) < 2 or rival not in source_ids:
        raise GuardError("safe clarification requires at least two sources including the rival source")
    if state["claim_states"][claim_id] != maturity_to:
        raise GuardError("current claim state must equal maturity_to")
    state["safe_synthesis_change"] = {
        "classification": "clarification",
        "claim_id": claim_id,
        "maturity_from": maturity_from,
        "maturity_to": maturity_to,
        "source_ids": source_ids,
        "rival_source_id": rival,
    }
    return state


def add_decision(state: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    state = copy.deepcopy(state)
    if len(state["open_decisions"]) >= 3:
        raise GuardError("no more than three decision cards may be open")
    if any(item["id"] == args.id for item in state["open_decisions"]):
        raise GuardError(f"duplicate decision id: {args.id}")
    if len(args.question.split()) > 20:
        raise GuardError("decision question exceeds 20 words")
    decision = {
        "id": args.id,
        "question": args.question,
        "choices": [
            {"label": args.option_a, "impact": args.impact_a},
            {"label": args.option_b, "impact": args.impact_b},
        ],
        "recommended": args.recommended,
        "reversible": args.reversible,
        "safe_default": args.safe_default,
        "lane": args.lane,
    }
    state["open_decisions"].append(decision)
    state["programme_status"] = "waiting_decision"
    state["harvest"]["next_recommendation"] = f"Resolve {args.id}."
    return state


def resolve_decision(state: dict[str, Any], decision_id: str, choice: str) -> dict[str, Any]:
    state = copy.deepcopy(state)
    match = next((item for item in state["open_decisions"] if item["id"] == decision_id), None)
    if not match:
        raise GuardError(f"unknown decision: {decision_id}")
    state["open_decisions"] = [item for item in state["open_decisions"] if item["id"] != decision_id]
    state["harvest"]["completed_since_last_check"] = f"Resolved {decision_id} with option {choice}."
    if not state["open_decisions"] and state["programme_status"] == "waiting_decision":
        state["programme_status"] = "running" if state["active_run"] else "ready"
    return state


def configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate state, artifacts, and optional synthesis diff")
    validate.add_argument("--base", help="Git base ref for guarded synthesis-diff validation")
    sub.add_parser("recover-check", help="validate a fresh checkout and resolve cloud branch indirection")
    sub.add_parser("render", help="regenerate research/CONTROL.md")
    begin = sub.add_parser("begin", help="begin the next queued run")
    begin.add_argument("--branch", help="active branch; defaults to the checked-out branch")
    checkpoint = sub.add_parser("checkpoint", help="record an atomic checkpoint")
    checkpoint.add_argument("--step", required=True)
    checkpoint.add_argument("--next-action", required=True)
    checkpoint.add_argument("--research-pass", action="store_true")
    checkpoint.add_argument("--new-sources", type=int, default=0)
    advance = sub.add_parser("advance-claim", help="advance one claim maturity stage")
    advance.add_argument("--claim", required=True)
    advance.add_argument("--to", required=True, choices=CLAIM_STAGES)
    complete = sub.add_parser("complete", help="complete the active run")
    complete.add_argument("--finding", required=True)
    complete.add_argument("--claim-change", default="No claim transition recorded.")
    pause = sub.add_parser("pause", help="pause safely at the current checkpoint")
    pause.add_argument("--reason", required=True)
    conserve = sub.add_parser("conserve", help="finish only the active atomic step, then pause")
    conserve.add_argument("--reason", required=True)
    sub.add_parser("resume", help="resume from usage_paused")
    set_pr = sub.add_parser("set-pr", help="record the active PR URL or number")
    set_pr.add_argument("--pr", required=True)
    sub.add_parser("clear-pr", help="clear a verified merged or closed active PR")
    safe = sub.add_parser("mark-safe-change", help="record evidence for a guarded synthesis clarification")
    safe.add_argument("--claim", required=True)
    safe.add_argument("--from-stage", required=True, choices=CLAIM_STAGES)
    safe.add_argument("--to-stage", required=True, choices=CLAIM_STAGES)
    safe.add_argument("--sources", required=True, help="comma-separated source ids")
    safe.add_argument("--rival", required=True, help="rival source id")
    sub.add_parser("clear-safe-change", help="clear synthesis-clarification metadata after integration")
    decision = sub.add_parser("add-decision", help="add a bounded decision card")
    decision.add_argument("--id", required=True)
    decision.add_argument("--question", required=True)
    decision.add_argument("--option-a", required=True)
    decision.add_argument("--impact-a", required=True)
    decision.add_argument("--option-b", required=True)
    decision.add_argument("--impact-b", required=True)
    decision.add_argument("--recommended", choices=("A", "B"), required=True)
    decision.add_argument("--reversible", action="store_true")
    decision.add_argument("--safe-default", choices=("A", "B", "pause"), required=True)
    decision.add_argument("--lane", required=True)
    resolve = sub.add_parser("resolve-decision", help="resolve a decision card")
    resolve.add_argument("--id", required=True)
    resolve.add_argument("--choice", choices=("A", "B"), required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = configure_parser().parse_args(argv)
    try:
        if args.command == "validate":
            errors = validate_repository(ROOT, args.base)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}")
                return 1
            print("Research greenhouse validation passed.")
            return 0

        if args.command == "recover-check":
            state = load_state(ROOT)
            report, errors = recovery_checkout_report(state, ROOT)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            return 0

        state = load_state(ROOT)
        if args.command == "render":
            render_to_disk(state, ROOT)
            print("Rendered research/CONTROL.md.")
            return 0
        if args.command == "begin":
            state = begin_run(state, args.branch)
        elif args.command == "checkpoint":
            state = checkpoint_run(state, args.step, args.next_action, args.research_pass, args.new_sources)
        elif args.command == "advance-claim":
            state = advance_claim(state, args.claim, args.to)
        elif args.command == "complete":
            state = complete_run(state, args.finding, args.claim_change)
        elif args.command == "pause":
            state = pause_programme(state, args.reason)
        elif args.command == "conserve":
            state = conserve_programme(state, args.reason)
        elif args.command == "resume":
            state = resume_programme(state)
        elif args.command == "set-pr":
            state = set_active_pr(state, args.pr)
        elif args.command == "clear-pr":
            state = set_active_pr(state, None)
        elif args.command == "mark-safe-change":
            state = mark_safe_change(
                state, args.claim, args.from_stage, args.to_stage, args.sources, args.rival
            )
        elif args.command == "clear-safe-change":
            state = copy.deepcopy(state)
            state["safe_synthesis_change"] = None
        elif args.command == "add-decision":
            state = add_decision(state, args)
        elif args.command == "resolve-decision":
            state = resolve_decision(state, args.id, args.choice)
        else:
            raise GuardError(f"unknown command: {args.command}")

        state_errors = validate_state(state, ROOT)
        if state_errors:
            raise GuardError("; ".join(state_errors))
        save_transactionally(state, ROOT)
        print(f"Updated greenhouse state via {args.command}.")
        return 0
    except (GuardError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
