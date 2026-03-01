#!/usr/bin/env python3
"""
Tests for plugins/lisa/hooks/validate.py (UnifiedValidator)

Run with: pytest tests/test_validate_quality_gates.py -v
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Target the active validator
sys.path.insert(0, str(Path(__file__).parent.parent / "plugins" / "lisa" / "hooks"))

from validate import (
    GateResult,
    GatesConfig,
    HAS_YAML,
    UnifiedValidator,
    generate_markdown_report,
    load_gates_config,
)


def make_config(*gates):
    """Build a minimal GatesConfig with the given gates under a 'test' stage."""
    return GatesConfig(
        version="test",
        stages={"test": {"gates": list(gates)}},
        workflows={},
        exit_codes={},
    )


def run(tmp_path, gate):
    """Run a single gate definition and return the GateResult."""
    return UnifiedValidator(tmp_path, make_config(gate)).validate_stage("test")[0]


# ---------------------------------------------------------------------------
# GateResult dataclass
# ---------------------------------------------------------------------------

class TestGateResult:
    def test_create_passing_result(self):
        result = GateResult(
            gate_id="test_gate",
            name="Test Gate",
            passed=True,
            severity="blocker",
            message="All good",
            stage="test",
        )
        assert result.gate_id == "test_gate"
        assert result.passed is True
        assert result.actual is None
        assert result.expected is None

    def test_create_failing_result_with_counts(self):
        result = GateResult(
            gate_id="file_count",
            name="File Count Check",
            passed=False,
            severity="blocker",
            message="Expected 6, found 4",
            stage="test",
            actual=4,
            expected="6",
        )
        assert result.passed is False
        assert result.actual == 4
        assert result.expected == "6"


# ---------------------------------------------------------------------------
# file_count gate
# ---------------------------------------------------------------------------

class TestFileCountGate:
    def test_pass_when_min_met(self, tmp_path):
        sc = tmp_path / "scopecraft"
        sc.mkdir()
        for name in ["A.md", "B.md", "C.md", "D.md", "E.md", "F.md"]:
            (sc / name).write_text("# Content", encoding="utf-8")

        result = run(tmp_path, {
            "id": "file_count", "name": "File count check",
            "check": "file_count", "path": "scopecraft/*.md",
            "min": 6, "severity": "blocker",
        })
        assert result.passed is True
        assert result.actual == 6

    def test_fail_when_below_min(self, tmp_path):
        sc = tmp_path / "scopecraft"
        sc.mkdir()
        for name in ["A.md", "B.md", "C.md"]:
            (sc / name).write_text("# Content", encoding="utf-8")

        result = run(tmp_path, {
            "id": "file_count", "name": "File count check",
            "check": "file_count", "path": "scopecraft/*.md",
            "min": 6, "severity": "blocker",
        })
        assert result.passed is False
        assert result.actual == 3

    def test_exact_expect(self, tmp_path):
        (tmp_path / "a.json").write_text("{}", encoding="utf-8")
        (tmp_path / "b.json").write_text("{}", encoding="utf-8")

        result = run(tmp_path, {
            "id": "exact", "name": "Exact count",
            "check": "file_count", "path": "*.json",
            "expect": 2, "severity": "blocker",
        })
        assert result.passed is True


# ---------------------------------------------------------------------------
# pattern_count gate
# ---------------------------------------------------------------------------

class TestPatternCountGate:
    def test_within_range(self, tmp_path):
        (tmp_path / "ROADMAP.md").write_text(
            "## Phase 1\n## Phase 2\n## Phase 3\n", encoding="utf-8"
        )
        result = run(tmp_path, {
            "id": "phases", "name": "Phase count",
            "check": "pattern_count", "path": "ROADMAP.md",
            "pattern": r"^## Phase \d", "min": 3, "max": 5, "severity": "blocker",
        })
        assert result.passed is True
        assert result.actual == 3

    def test_below_min_fails(self, tmp_path):
        (tmp_path / "ROADMAP.md").write_text("## Phase 1\n## Phase 2\n", encoding="utf-8")
        result = run(tmp_path, {
            "id": "phases", "name": "Phase count",
            "check": "pattern_count", "path": "ROADMAP.md",
            "pattern": r"^## Phase \d", "min": 3, "max": 5, "severity": "blocker",
        })
        assert result.passed is False

    def test_above_max_fails(self, tmp_path):
        (tmp_path / "ROADMAP.md").write_text(
            "\n".join(f"## Phase {i}" for i in range(1, 7)), encoding="utf-8"
        )
        result = run(tmp_path, {
            "id": "phases", "name": "Phase count",
            "check": "pattern_count", "path": "ROADMAP.md",
            "pattern": r"^## Phase \d", "min": 3, "max": 5, "severity": "blocker",
        })
        assert result.passed is False
        assert result.actual == 6

    def test_max_zero_passes_when_no_matches(self, tmp_path):
        (tmp_path / "doc.md").write_text("Clean content", encoding="utf-8")
        result = run(tmp_path, {
            "id": "no_todos", "name": "No TODO placeholders",
            "check": "pattern_count", "path": "doc.md",
            "pattern": r"\[TODO\]|\[TBD\]", "max": 0, "severity": "blocker",
        })
        assert result.passed is True
        assert result.actual == 0

    def test_max_zero_fails_when_matches_found(self, tmp_path):
        (tmp_path / "doc.md").write_text(
            "[TODO] fill this in\n[TBD] timeline", encoding="utf-8"
        )
        result = run(tmp_path, {
            "id": "no_todos", "name": "No TODO placeholders",
            "check": "pattern_count", "path": "doc.md",
            "pattern": r"\[TODO\]|\[TBD\]", "max": 0, "severity": "blocker",
        })
        assert result.passed is False
        assert result.actual == 2

    def test_no_bounds_is_config_error(self, tmp_path):
        """A pattern_count gate with neither min nor max should fail as a config error."""
        (tmp_path / "doc.md").write_text("content", encoding="utf-8")
        result = run(tmp_path, {
            "id": "bad_gate", "name": "Gate with no bounds",
            "check": "pattern_count", "path": "doc.md",
            "pattern": r"content", "severity": "blocker",
        })
        assert result.passed is False
        assert "configuration error" in result.message.lower()

    def test_invalid_regex_returns_failure(self, tmp_path):
        (tmp_path / "doc.md").write_text("content", encoding="utf-8")
        result = run(tmp_path, {
            "id": "bad_regex", "name": "Invalid regex gate",
            "check": "pattern_count", "path": "doc.md",
            "pattern": r"(?P<invalid>", "min": 1, "severity": "blocker",
        })
        assert result.passed is False
        assert "invalid regex" in result.message.lower()


# ---------------------------------------------------------------------------
# pattern_exists gate
# ---------------------------------------------------------------------------

class TestPatternExistsGate:
    def test_pattern_found(self, tmp_path):
        (tmp_path / "metrics.md").write_text(
            "## North Star Metric\nMAU", encoding="utf-8"
        )
        result = run(tmp_path, {
            "id": "north_star", "name": "North Star defined",
            "check": "pattern_exists", "path": "metrics.md",
            "pattern": r"North Star Metric", "severity": "blocker",
        })
        assert result.passed is True

    def test_pattern_not_found(self, tmp_path):
        (tmp_path / "metrics.md").write_text("## KPIs\nSome metrics", encoding="utf-8")
        result = run(tmp_path, {
            "id": "north_star", "name": "North Star defined",
            "check": "pattern_exists", "path": "metrics.md",
            "pattern": r"North Star Metric", "severity": "blocker",
        })
        assert result.passed is False

    def test_invalid_regex_returns_failure(self, tmp_path):
        (tmp_path / "doc.md").write_text("content", encoding="utf-8")
        result = run(tmp_path, {
            "id": "bad_regex", "name": "Invalid regex",
            "check": "pattern_exists", "path": "doc.md",
            "pattern": r"(?P<invalid>", "severity": "blocker",
        })
        assert result.passed is False
        assert "invalid regex" in result.message.lower()

    def test_file_not_found(self, tmp_path):
        result = run(tmp_path, {
            "id": "missing", "name": "Missing file",
            "check": "pattern_exists", "path": "nonexistent.md",
            "pattern": r"anything", "severity": "blocker",
        })
        assert result.passed is False
        assert "no files found" in result.message.lower()


# ---------------------------------------------------------------------------
# json gates
# ---------------------------------------------------------------------------

class TestJsonGates:
    def test_json_valid_pass(self, tmp_path):
        (tmp_path / "data.json").write_text('{"key": "value"}', encoding="utf-8")
        result = run(tmp_path, {
            "id": "json_check", "name": "Valid JSON",
            "check": "json_valid", "path": "data.json", "severity": "blocker",
        })
        assert result.passed is True

    def test_json_valid_fail(self, tmp_path):
        (tmp_path / "data.json").write_text('{"broken": }', encoding="utf-8")
        result = run(tmp_path, {
            "id": "json_check", "name": "Valid JSON",
            "check": "json_valid", "path": "data.json", "severity": "blocker",
        })
        assert result.passed is False

    def test_json_field_present_pass(self, tmp_path):
        (tmp_path / "data.json").write_text(
            '{"project": {"name": "my-app"}}', encoding="utf-8"
        )
        result = run(tmp_path, {
            "id": "name_check", "name": "Project name present",
            "check": "json_field_present", "path": "data.json",
            "field": "project.name", "severity": "blocker",
        })
        assert result.passed is True

    def test_json_field_present_fail(self, tmp_path):
        (tmp_path / "data.json").write_text('{"project": {}}', encoding="utf-8")
        result = run(tmp_path, {
            "id": "name_check", "name": "Project name present",
            "check": "json_field_present", "path": "data.json",
            "field": "project.name", "severity": "blocker",
        })
        assert result.passed is False

    def test_json_field_count_pass(self, tmp_path):
        (tmp_path / "data.json").write_text(
            '{"tech_stack": {"runtime": "Node", "db": "Postgres", "auth": "Firebase"}}',
            encoding="utf-8",
        )
        result = run(tmp_path, {
            "id": "stack_check", "name": "Tech stack detected",
            "check": "json_field_count", "path": "data.json",
            "field": "tech_stack", "min": 2, "severity": "blocker",
        })
        assert result.passed is True

    def test_json_field_count_fail(self, tmp_path):
        (tmp_path / "data.json").write_text(
            '{"tech_stack": {"runtime": "Node"}}', encoding="utf-8"
        )
        result = run(tmp_path, {
            "id": "stack_check", "name": "Tech stack detected",
            "check": "json_field_count", "path": "data.json",
            "field": "tech_stack", "min": 2, "severity": "blocker",
        })
        assert result.passed is False


# ---------------------------------------------------------------------------
# cross_reference gate
# ---------------------------------------------------------------------------

class TestCrossReferenceGate:
    def _setup_convoy(self, tmp_path, bead_ids, convoy_beads):
        beads_dir = tmp_path / ".gt" / "beads"
        convoys_dir = tmp_path / ".gt" / "convoys"
        beads_dir.mkdir(parents=True)
        convoys_dir.mkdir(parents=True)
        for bead_id in bead_ids:
            (beads_dir / f"{bead_id}.json").write_text(
                json.dumps({"id": bead_id}), encoding="utf-8"
            )
        convoy = {"id": "convoy-001", "beads": convoy_beads}
        (convoys_dir / "convoy-001.json").write_text(json.dumps(convoy), encoding="utf-8")

    def _gate(self):
        return {
            "id": "convoy_beads_exist", "name": "All convoy beads exist",
            "check": "cross_reference",
            "source_path": ".gt/convoys/*.json",
            "source_field": "beads",
            "target_dir": ".gt/beads",
            "target_pattern": "{id}.json",
            "severity": "blocker",
        }

    def test_all_refs_exist(self, tmp_path):
        self._setup_convoy(tmp_path, ["gt-abc12", "gt-def34"], ["gt-abc12", "gt-def34"])
        result = run(tmp_path, self._gate())
        assert result.passed is True

    def test_missing_ref_fails(self, tmp_path):
        self._setup_convoy(tmp_path, ["gt-abc12"], ["gt-abc12", "gt-missing"])
        result = run(tmp_path, self._gate())
        assert result.passed is False
        assert "gt-missing" in result.message

    def test_many_missing_refs_shows_overflow(self, tmp_path):
        """When more than 5 refs are missing, the message should mention 'more'."""
        beads_dir = tmp_path / ".gt" / "beads"
        convoys_dir = tmp_path / ".gt" / "convoys"
        beads_dir.mkdir(parents=True)
        convoys_dir.mkdir(parents=True)
        missing = [f"gt-{i:05d}" for i in range(10)]
        convoy = {"id": "convoy-001", "beads": missing}
        (convoys_dir / "convoy-001.json").write_text(json.dumps(convoy), encoding="utf-8")
        result = run(tmp_path, self._gate())
        assert result.passed is False
        assert "more" in result.message

    def test_malformed_source_file_fails(self, tmp_path):
        """A malformed convoy JSON should cause the gate to fail, not silently pass."""
        convoys_dir = tmp_path / ".gt" / "convoys"
        convoys_dir.mkdir(parents=True)
        (convoys_dir / "convoy-001.json").write_text("not json {{{", encoding="utf-8")
        result = run(tmp_path, self._gate())
        assert result.passed is False
        assert "malformed" in result.message.lower()


# ---------------------------------------------------------------------------
# unknown check type
# ---------------------------------------------------------------------------

class TestUnknownCheckType:
    def test_unknown_check_fails(self, tmp_path):
        result = run(tmp_path, {
            "id": "unknown", "name": "Unknown check",
            "check": "invalid_check_type", "severity": "warning",
        })
        assert result.passed is False
        assert "unknown check type" in result.message.lower()


# ---------------------------------------------------------------------------
# markdown report
# ---------------------------------------------------------------------------

class TestMarkdownReport:
    def test_all_pass(self):
        results = [
            GateResult("g1", "Gate 1", True, "blocker", "OK", stage="discover"),
            GateResult("g2", "Gate 2", True, "warning", "OK", stage="plan"),
        ]
        report = generate_markdown_report(results)
        assert "## Quality Gate Status" in report
        assert "Blockers: 0" in report
        assert "Ready to proceed" in report

    def test_with_blockers(self):
        results = [
            GateResult("g1", "Gate 1", False, "blocker", "Failed", stage="discover"),
            GateResult("g2", "Gate 2", True, "warning", "OK", stage="plan"),
        ]
        report = generate_markdown_report(results)
        assert "Blockers: 1" in report

    def test_warnings_only_still_ready(self):
        results = [
            GateResult("g1", "Gate 1", True, "blocker", "OK", stage="discover"),
            GateResult("g2", "Gate 2", False, "warning", "Minor issue", stage="plan"),
        ]
        report = generate_markdown_report(results)
        assert "Blockers: 0" in report
        assert "Ready to proceed" in report


# ---------------------------------------------------------------------------
# Integration: validate against real gates.yaml
# ---------------------------------------------------------------------------

class TestIntegration:
    @pytest.fixture
    def full_scopecraft(self, tmp_path):
        sc = tmp_path / "scopecraft"
        sc.mkdir()
        (sc / "VISION_AND_STAGE_DEFINITION.md").write_text(
            "# Vision\n## Product Vision\nBuild the best thing ever.\n",
            encoding="utf-8",
        )
        (sc / "ROADMAP.md").write_text(
            "# Roadmap\n## Phase 1\nFoundation\n## Phase 2\nCore\n## Phase 3\nPolish\n",
            encoding="utf-8",
        )
        (sc / "EPICS_AND_STORIES.md").write_text(
            "# Epics\n"
            + "\n".join(
                f"### Story {i}\n#### Acceptance Criteria\n- Criterion {i}"
                for i in range(1, 6)
            ),
            encoding="utf-8",
        )
        (sc / "RISKS_AND_DEPENDENCIES.md").write_text(
            "# Risks\n| Risk | Type | Mitigation |\n|------|------|------------|\n"
            "| DB scaling | Technical | Replicas |\n"
            "| Market timing | Product | Fast iteration |\n"
            "| Competition | GTM | Differentiation |\n",
            encoding="utf-8",
        )
        (sc / "METRICS_AND_PMF.md").write_text(
            "# Metrics\n## North Star Metric\nMAU\n", encoding="utf-8"
        )
        (sc / "OPEN_QUESTIONS.md").write_text(
            "# Open Questions\n1. What's the pricing model?\n", encoding="utf-8"
        )
        return tmp_path

    @pytest.mark.skipif(not HAS_YAML, reason="requires PyYAML")
    def test_plan_stage_passes_with_valid_scopecraft(self, full_scopecraft):
        gates_yaml = (
            Path(__file__).parent.parent / "plugins" / "lisa" / "gates.yaml"
        )
        config = load_gates_config(gates_yaml)
        assert config is not None, "Failed to load gates.yaml"
        validator = UnifiedValidator(full_scopecraft, config)
        results = validator.validate_stage("plan")
        failed = [r for r in results if not r.passed]
        assert failed == [], f"Failed gates: {[(r.gate_id, r.message) for r in failed]}"
