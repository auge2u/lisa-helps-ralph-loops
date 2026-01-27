#!/usr/bin/env python3
"""
Tests for validate_quality_gates.py

Run with: pytest tests/test_validate_quality_gates.py -v
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Add the hooks directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "plugins" / "lisa-loops-memory" / "hooks"))

from validate_quality_gates import (
    ALLOWED_OUTPUT_DIRS,
    ALLOWED_SCRATCHPAD_PATTERNS,
    GateResult,
    QualityGateValidator,
    generate_markdown_report,
    validate_path_security,
)


class TestGateResult:
    """Tests for GateResult dataclass."""

    def test_create_passing_result(self):
        result = GateResult(
            gate_id="test_gate",
            name="Test Gate",
            passed=True,
            severity="blocker",
            message="All good"
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
            actual=4,
            expected="6"
        )
        assert result.passed is False
        assert result.actual == 4
        assert result.expected == "6"


class TestPathSecurity:
    """Tests for path security validation."""

    def test_valid_scopecraft_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            os.makedirs("scopecraft", exist_ok=True)
            result = validate_path_security("scopecraft", ALLOWED_OUTPUT_DIRS, "--output-dir")
            assert result.name == "scopecraft"

    def test_valid_dot_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = validate_path_security(".", ALLOWED_OUTPUT_DIRS, "--output-dir")
            assert result == Path(tmpdir).resolve()

    def test_path_traversal_blocked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            with pytest.raises(SystemExit) as exc_info:
                validate_path_security("../../../etc", ALLOWED_OUTPUT_DIRS, "--output-dir")
            assert exc_info.value.code == 3

    def test_absolute_path_outside_cwd_blocked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            with pytest.raises(SystemExit) as exc_info:
                validate_path_security("/tmp/malicious", ALLOWED_OUTPUT_DIRS, "--output-dir")
            assert exc_info.value.code == 3

    def test_gt_directory_allowed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            os.makedirs(".gt", exist_ok=True)
            result = validate_path_security(".gt", ALLOWED_OUTPUT_DIRS, "--output-dir")
            assert ".gt" in str(result)


class TestQualityGateValidator:
    """Tests for QualityGateValidator class."""

    @pytest.fixture
    def temp_scopecraft(self):
        """Create a temporary scopecraft directory with test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scopecraft = Path(tmpdir) / "scopecraft"
            scopecraft.mkdir()
            yield tmpdir, scopecraft

    def test_file_count_pass(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        # Create 6 markdown files
        for name in ["VISION.md", "ROADMAP.md", "EPICS.md", "RISKS.md", "METRICS.md", "QUESTIONS.md"]:
            (scopecraft / name).write_text("# Content", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "file_count",
                "name": "File count check",
                "check": "file_count",
                "path": "scopecraft/*.md",
                "expect": 6,
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert len(results) == 1
        assert results[0].passed is True
        assert results[0].actual == 6

    def test_file_count_fail(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        # Create only 3 files
        for name in ["VISION.md", "ROADMAP.md", "EPICS.md"]:
            (scopecraft / name).write_text("# Content", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "file_count",
                "name": "File count check",
                "check": "file_count",
                "path": "scopecraft/*.md",
                "expect": 6,
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is False
        assert results[0].actual == 3

    def test_pattern_count_min_pass(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        roadmap = scopecraft / "ROADMAP.md"
        roadmap.write_text("""# Roadmap
## Phase 1
Content
## Phase 2
Content
## Phase 3
Content
""", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "phases",
                "name": "Phase count",
                "check": "pattern_count",
                "path": "scopecraft/ROADMAP.md",
                "pattern": r"^## Phase \d",
                "min": 3,
                "max": 5,
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is True
        assert results[0].actual == 3

    def test_pattern_count_max_exceeded(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        roadmap = scopecraft / "ROADMAP.md"
        roadmap.write_text("""# Roadmap
## Phase 1
## Phase 2
## Phase 3
## Phase 4
## Phase 5
## Phase 6
""", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "phases",
                "name": "Phase count",
                "check": "pattern_count",
                "path": "scopecraft/ROADMAP.md",
                "pattern": r"^## Phase \d",
                "min": 3,
                "max": 5,
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is False
        assert results[0].actual == 6

    def test_pattern_exists_pass(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        metrics = scopecraft / "METRICS.md"
        metrics.write_text("""# Metrics
## North Star Metric
User engagement rate
""", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "north_star",
                "name": "North Star defined",
                "check": "pattern_exists",
                "path": "scopecraft/METRICS.md",
                "pattern": r"North Star Metric",
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is True

    def test_pattern_exists_fail(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        metrics = scopecraft / "METRICS.md"
        metrics.write_text("""# Metrics
## Key Performance Indicators
Some metrics
""", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "north_star",
                "name": "North Star defined",
                "check": "pattern_exists",
                "path": "scopecraft/METRICS.md",
                "pattern": r"North Star Metric",
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is False

    def test_min_lines_pass(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        doc = scopecraft / "DOC.md"
        doc.write_text("\n".join([f"Line {i}" for i in range(100)]), encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "min_lines",
                "name": "Minimum lines",
                "check": "min_lines",
                "path": "scopecraft/DOC.md",
                "min": 50,
                "severity": "warning"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is True
        assert results[0].actual == 100

    def test_min_lines_fail(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        doc = scopecraft / "DOC.md"
        doc.write_text("Just a few lines\nNot enough\n", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "min_lines",
                "name": "Minimum lines",
                "check": "min_lines",
                "path": "scopecraft/DOC.md",
                "min": 50,
                "severity": "warning"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is False
        assert results[0].actual == 2

    def test_file_not_found(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "missing_file",
                "name": "Missing file check",
                "check": "pattern_exists",
                "path": "scopecraft/NONEXISTENT.md",
                "pattern": r"anything",
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is False
        assert "not found" in results[0].message.lower()

    def test_unknown_check_type(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "unknown",
                "name": "Unknown check",
                "check": "invalid_check_type",
                "severity": "warning"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is False
        assert "unknown check type" in results[0].message.lower()

    def test_no_todo_placeholders_pass(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        for name in ["VISION.md", "ROADMAP.md"]:
            (scopecraft / name).write_text("# Clean content\nNo placeholders here.", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "no_todos",
                "name": "No TODO placeholders",
                "check": "pattern_count",
                "path": "scopecraft/*.md",
                "pattern": r"\[TODO\]|\[TBD\]|\[PLACEHOLDER\]",
                "max": 0,
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is True
        assert results[0].actual == 0

    def test_no_todo_placeholders_fail(self, temp_scopecraft):
        tmpdir, scopecraft = temp_scopecraft
        (scopecraft / "VISION.md").write_text("# Vision\n[TODO] Fill this in", encoding="utf-8")
        (scopecraft / "ROADMAP.md").write_text("# Roadmap\n[TBD] Timeline", encoding="utf-8")

        validator = QualityGateValidator(
            Path(tmpdir),
            gates=[{
                "id": "no_todos",
                "name": "No TODO placeholders",
                "check": "pattern_count",
                "path": "scopecraft/*.md",
                "pattern": r"\[TODO\]|\[TBD\]|\[PLACEHOLDER\]",
                "max": 0,
                "severity": "blocker"
            }]
        )
        results = validator.validate_all()
        assert results[0].passed is False
        assert results[0].actual == 2


class TestMarkdownReport:
    """Tests for markdown report generation."""

    def test_generate_report_all_pass(self):
        results = [
            GateResult("g1", "Gate 1", True, "blocker", "OK"),
            GateResult("g2", "Gate 2", True, "warning", "OK"),
        ]
        report = generate_markdown_report(results)
        assert "## Quality Gate Status" in report
        assert "Blockers remaining: 0" in report
        assert "Ready to issue LOOP_COMPLETE" in report

    def test_generate_report_with_blockers(self):
        results = [
            GateResult("g1", "Gate 1", False, "blocker", "Failed"),
            GateResult("g2", "Gate 2", True, "warning", "OK"),
        ]
        report = generate_markdown_report(results)
        assert "Blockers remaining: 1" in report
        assert "Cannot issue LOOP_COMPLETE" in report

    def test_generate_report_warnings_only(self):
        results = [
            GateResult("g1", "Gate 1", True, "blocker", "OK"),
            GateResult("g2", "Gate 2", False, "warning", "Minor issue"),
        ]
        report = generate_markdown_report(results)
        assert "Blockers remaining: 0" in report
        assert "Ready to issue LOOP_COMPLETE" in report


class TestDefaultGates:
    """Tests using the default gate configuration."""

    def test_default_gates_defined(self):
        validator = QualityGateValidator(Path("."))
        assert len(validator.gates) == 6
        gate_ids = [g["id"] for g in validator.gates]
        assert "all_outputs_exist" in gate_ids
        assert "phases_in_range" in gate_ids
        assert "stories_have_acceptance_criteria" in gate_ids
        assert "risks_documented" in gate_ids
        assert "no_todo_placeholders" in gate_ids
        assert "metrics_defined" in gate_ids

    def test_all_default_gates_are_blockers(self):
        validator = QualityGateValidator(Path("."))
        for gate in validator.gates:
            assert gate.get("severity") == "blocker"


class TestIntegration:
    """Integration tests with full scopecraft directory."""

    @pytest.fixture
    def full_scopecraft(self):
        """Create a complete valid scopecraft directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scopecraft = Path(tmpdir) / "scopecraft"
            scopecraft.mkdir()

            # VISION_AND_STAGE_DEFINITION.md
            (scopecraft / "VISION_AND_STAGE_DEFINITION.md").write_text("""# Vision and Stage Definition
## Product Vision
Build the best thing ever.
## Current Stage
MVP
""", encoding="utf-8")

            # ROADMAP.md with 3 phases
            (scopecraft / "ROADMAP.md").write_text("""# Roadmap
## Phase 1
Foundation
## Phase 2
Core Features
## Phase 3
Polish
""", encoding="utf-8")

            # EPICS_AND_STORIES.md with acceptance criteria
            (scopecraft / "EPICS_AND_STORIES.md").write_text("""# Epics and Stories
## Epic 1
### Story 1.1
#### Acceptance Criteria
- Criterion 1
### Story 1.2
#### Acceptance Criteria
- Criterion 2
## Epic 2
### Story 2.1
#### Acceptance Criteria
- Criterion 3
### Story 2.2
#### Acceptance Criteria
- Criterion 4
### Story 2.3
#### Acceptance Criteria
- Criterion 5
""", encoding="utf-8")

            # RISKS_AND_DEPENDENCIES.md with risk table
            (scopecraft / "RISKS_AND_DEPENDENCIES.md").write_text("""# Risks and Dependencies
| Risk | Type | Mitigation |
|------|------|------------|
| Database scaling | Technical | Use read replicas |
| Market timing | Product | Fast iteration |
| Competition | GTM | Differentiation |
""", encoding="utf-8")

            # METRICS_AND_PMF.md with North Star
            (scopecraft / "METRICS_AND_PMF.md").write_text("""# Metrics and PMF
## North Star Metric
Monthly Active Users (MAU)
## Supporting Metrics
- DAU/MAU ratio
- Retention rate
""", encoding="utf-8")

            # OPEN_QUESTIONS.md
            (scopecraft / "OPEN_QUESTIONS.md").write_text("""# Open Questions
1. What's the pricing model?
2. Which markets first?
""", encoding="utf-8")

            yield tmpdir

    def test_full_validation_pass(self, full_scopecraft):
        validator = QualityGateValidator(Path(full_scopecraft))
        results = validator.validate_all()

        passed = [r for r in results if r.passed]
        failed = [r for r in results if not r.passed]

        assert len(failed) == 0, f"Failed gates: {[(r.gate_id, r.message) for r in failed]}"
        assert len(passed) == 6
