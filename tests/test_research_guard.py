import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import research_guard as guard  # noqa: E402


class ResearchGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            "AGENTS.md",
            "research/STATE.json",
            "research/CLAIMS.md",
            "research/PILOTS/threat-avoidance.md",
            "research/PILOTS/fear-conditioning.md",
            "research/PILOTS/fiat-money.md",
            "research/PUBLISHABILITY_BACKLOG.md",
            "research/CLOUD_TASK.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/workflows/research-guard.yml",
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text((REPO_ROOT / relative).read_text(encoding="utf-8"), encoding="utf-8")
        synthesis = next(REPO_ROOT.glob("Toward*.md"))
        (self.root / synthesis.name).write_text(synthesis.read_text(encoding="utf-8"), encoding="utf-8")
        guard.render_to_disk(guard.load_state(self.root), self.root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_bootstrap_repository_is_valid(self):
        self.assertEqual([], guard.validate_repository(self.root))

    def test_dashboard_is_deterministic_and_stale_copy_is_rejected(self):
        state = guard.load_state(self.root)
        expected = guard.render_control(state)
        guard.render_to_disk(state, self.root)
        self.assertEqual(expected, (self.root / guard.CONTROL_PATH).read_text(encoding="utf-8"))
        (self.root / guard.CONTROL_PATH).write_text("stale\n", encoding="utf-8")
        self.assertIn("research/CONTROL.md is stale; run the render command", guard.validate_repository(self.root))

    def test_claim_register_maturity_must_match_state(self):
        claims_path = self.root / guard.CLAIMS_PATH
        claims_path.write_text(
            claims_path.read_text(encoding="utf-8").replace(
                "| C-001 | Meaning-sensitive constructions", "| C-001 | Meaning-sensitive constructions"
            ).replace("| Core | bounded | threat-avoidance, fiat-money |", "| Core | asserted | threat-avoidance, fiat-money |", 1),
            encoding="utf-8",
        )
        self.assertTrue(
            any("maturity for C-001" in error for error in guard.validate_repository(self.root))
        )

    def test_run_can_pause_and_resume_without_losing_checkpoint(self):
        state = guard.begin_run(guard.load_state(self.root), "codex/holiday/run-001")
        state = guard.checkpoint_run(state, "Baseline table inspected.", "Score C-001 through C-008.", True, 0)
        paused = guard.pause_programme(state, "Plus usage unavailable")
        self.assertEqual("usage_paused", paused["programme_status"])
        self.assertEqual(state["completed_steps"], paused["completed_steps"])
        resumed = guard.resume_programme(paused)
        self.assertEqual("running", resumed["programme_status"])
        self.assertEqual("RUN-001", resumed["active_run"]["id"])
        self.assertEqual(state["completed_steps"], resumed["completed_steps"])

    def test_cloud_ephemeral_branch_is_not_a_recovery_conflict(self):
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Research Guard",
                "-c",
                "user.email=guard@example.invalid",
                "commit",
                "-m",
                "checkpoint",
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        subprocess.run(["git", "switch", "-c", "work"], cwd=self.root, check=True, capture_output=True)
        report, errors = guard.recovery_checkout_report(guard.load_state(self.root), self.root)
        self.assertEqual([], errors)
        self.assertEqual("main", report["source_branch"])
        self.assertEqual("work", report["checkout_branch"])
        self.assertTrue(report["ephemeral_checkout_branch"])

    def test_conserve_mode_and_pr_gate_are_explicit(self):
        state = guard.begin_run(guard.load_state(self.root), "codex/holiday/run-001")
        state = guard.conserve_programme(state, "usage warning")
        self.assertEqual("conserve", state["usage_mode"])
        self.assertIn("add no optional sources", state["next_atomic_action"])
        state = guard.set_active_pr(state, "https://github.example/pr/1")
        state = guard.complete_run(state, "Baseline recorded.", "No transitions.")
        self.assertEqual("https://github.example/pr/1", state["active_pr"])
        with self.assertRaises(guard.GuardError):
            guard.begin_run(state, "codex/holiday/run-002")
        state = guard.set_active_pr(state, None)
        state = guard.begin_run(state, "codex/holiday/run-002")
        self.assertEqual("RUN-002", state["active_run"]["id"])

    def test_transactional_lifecycle_reaches_first_pilot(self):
        state = guard.begin_run(guard.load_state(self.root), "codex/holiday/run-001")
        guard.save_transactionally(state, self.root)
        state = guard.complete_run(guard.load_state(self.root), "Baseline recorded.", "No transitions.")
        guard.save_transactionally(state, self.root)
        state = guard.begin_run(guard.load_state(self.root), "codex/holiday/run-002")
        guard.save_transactionally(state, self.root)
        self.assertEqual([], guard.validate_repository(self.root))
        report = (self.root / "research/PILOTS/threat-avoidance.md").read_text(encoding="utf-8")
        self.assertIn("Active. Exploratory and not publication ready.", report)

    def test_per_run_source_budget_is_enforced(self):
        state = guard.load_state(self.root)
        state["run_queue"] = state["run_queue"][1:]
        state["next_run"] = state["run_queue"][0]
        state = guard.begin_run(state, "codex/holiday/run-002")
        state = guard.checkpoint_run(state, "Selected four sources.", "Analyze sources.", True, 4)
        with self.assertRaises(guard.GuardError):
            guard.checkpoint_run(state, "Selected another source.", "Continue.", False, 1)

    def test_invalid_lifecycle_update_rolls_back(self):
        original_state = (self.root / guard.STATE_PATH).read_bytes()
        state = guard.load_state(self.root)
        state["source_counts"]["threat-avoidance"] = 1
        with self.assertRaises(guard.GuardError):
            guard.save_transactionally(state, self.root)
        self.assertEqual(original_state, (self.root / guard.STATE_PATH).read_bytes())

    def test_claims_must_advance(self):
        state = guard.begin_run(guard.load_state(self.root), "codex/holiday/run-001")
        advanced = guard.advance_claim(state, "C-002", "rivalled")
        self.assertEqual("rivalled", advanced["claim_states"]["C-002"])
        with self.assertRaises(guard.GuardError):
            guard.advance_claim(advanced, "C-002", "bounded")

    def test_decision_cards_are_bounded(self):
        args = type(
            "Args",
            (),
            {
                "id": "DEC-001",
                "question": "Should this reversible clarification enter the synthesis?",
                "option_a": "Apply clarification",
                "impact_a": "Improves precision.",
                "option_b": "Keep in pilot",
                "impact_b": "Defers integration.",
                "recommended": "A",
                "reversible": True,
                "safe_default": "A",
                "lane": "synthesis",
            },
        )()
        state = guard.add_decision(guard.load_state(self.root), args)
        self.assertEqual("waiting_decision", state["programme_status"])
        resolved = guard.resolve_decision(state, "DEC-001", "A")
        self.assertEqual("ready", resolved["programme_status"])
        self.assertEqual([], resolved["open_decisions"])

    def test_protected_synthesis_change_is_rejected(self):
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Research Guard",
                "-c",
                "user.email=guard@example.invalid",
                "commit",
                "-m",
                "baseline",
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        base = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, check=True, text=True, capture_output=True
        ).stdout.strip()
        synthesis = next(self.root.glob("Toward*.md"))
        text = synthesis.read_text(encoding="utf-8")
        synthesis.write_text(
            text.replace("# 1. Hierarchy of commitments", "# 1. Hierarchy of commitments\n\nProtected mutation."),
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Research Guard",
                "-c",
                "user.email=guard@example.invalid",
                "commit",
                "-m",
                "protected change",
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        errors = guard.validate_synthesis_diff(guard.load_state(self.root), self.root, base)
        self.assertTrue(any("protected synthesis section changed" in error for error in errors))

    def test_validated_unprotected_clarification_is_allowed(self):
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            ["git", "-c", "user.name=Research Guard", "-c", "user.email=guard@example.invalid", "commit", "-m", "baseline"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        base = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, check=True, text=True, capture_output=True
        ).stdout.strip()

        state = guard.load_state(self.root)
        state["claim_states"]["C-001"] = "rivalled"
        state["source_counts"]["threat-avoidance"] = 2
        state["safe_synthesis_change"] = {
            "classification": "clarification",
            "claim_id": "C-001",
            "maturity_from": "bounded",
            "maturity_to": "rivalled",
            "source_ids": ["SRC-A", "SRC-B"],
            "rival_source_id": "SRC-B",
        }
        claims = self.root / guard.CLAIMS_PATH
        claims.write_text(
            claims.read_text(encoding="utf-8").replace(
                "| Core | bounded | threat-avoidance, fiat-money |",
                "| Core | rivalled | threat-avoidance, fiat-money |",
                1,
            ),
            encoding="utf-8",
        )
        pilot = self.root / "research/PILOTS/threat-avoidance.md"
        pilot.write_text(
            pilot.read_text(encoding="utf-8").replace(
                "| --- | --- | --- | --- | --- | --- | --- |",
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                "| SRC-A | [direct] | Direct source | Study | Finding | Limitation | C-001 |\n"
                "| SRC-B | [rival] | Rival source | Theory | Finding | Limitation | C-001 |",
                1,
            ),
            encoding="utf-8",
        )
        synthesis = next(self.root.glob("Toward*.md"))
        synthesis.write_text(
            synthesis.read_text(encoding="utf-8").replace(
                "# 28. Worked minimal testbed: threat interpretation and avoidance",
                "# 28. Worked minimal testbed: threat interpretation and avoidance\n\nThis testbed is provisional.",
            ),
            encoding="utf-8",
        )
        guard.write_state(state, self.root)
        guard.render_to_disk(state, self.root)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            ["git", "-c", "user.name=Research Guard", "-c", "user.email=guard@example.invalid", "commit", "-m", "safe clarification"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        self.assertEqual([], guard.validate_repository(self.root, base))


if __name__ == "__main__":
    unittest.main()
