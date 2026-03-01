#!/usr/bin/env python3
"""
Unified Validator for Lisa Plugin

Validates outputs against quality gates defined in gates.yaml.
Supports all 5 stages: research, discover, plan, structure, reconcile.

Usage:
    python validate.py [--stage research|discover|plan|structure|reconcile|all]
    python validate.py --stage discover --format json
    python validate.py --workflow migrate --format markdown

Exit codes:
    0 - All gates passed
    1 - Blocker gates failed
    2 - Warning gates failed (but no blockers)
    3 - Security error

PyYAML fallback:
    When PyYAML is not installed, the validator runs in fallback mode using
    a built-in subset of gates (file_exists, file_count, json_valid,
    json_field_present, json_field_count). Pattern-based checks are skipped
    with a warning. Install PyYAML for full validation: pip install pyyaml
"""

import argparse
import glob
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class GateResult:
    """Result of a quality gate check."""
    gate_id: str
    name: str
    passed: bool
    severity: str
    message: str
    stage: str
    actual: Optional[Any] = None
    expected: Optional[str] = None

@dataclass
class GatesConfig:
    """Loaded gates configuration."""
    version: str
    stages: dict
    workflows: dict
    exit_codes: dict

class UnifiedValidator:
    """Validates outputs against gates.yaml definitions."""

    def __init__(self, base_dir: Path, gates_config: GatesConfig):
        self.base_dir = Path(base_dir)
        self.config = gates_config

    def validate_stage(self, stage_name: str) -> list[GateResult]:
        """Validate all gates for a specific stage."""
        if stage_name not in self.config.stages:
            return [GateResult(
                gate_id="invalid_stage",
                name="Stage validation",
                passed=False,
                severity="blocker",
                message=f"Unknown stage: {stage_name}",
                stage=stage_name
            )]

        stage = self.config.stages[stage_name]
        results = []

        for gate in stage.get("gates", []):
            result = self._check_gate(gate, stage_name)
            results.append(result)

        return results

    def validate_all(self) -> list[GateResult]:
        """Validate all stages."""
        results = []
        for stage_name in self.config.stages:
            results.extend(self.validate_stage(stage_name))
        return results

    def validate_workflow(self, workflow_name: str) -> list[GateResult]:
        """Validate stages in a workflow."""
        if workflow_name not in self.config.workflows:
            return [GateResult(
                gate_id="invalid_workflow",
                name="Workflow validation",
                passed=False,
                severity="blocker",
                message=f"Unknown workflow: {workflow_name}",
                stage="workflow"
            )]

        workflow = self.config.workflows[workflow_name]
        results = []

        for stage_name in workflow.get("stages", []):
            results.extend(self.validate_stage(stage_name))

        return results

    def _check_gate(self, gate: dict, stage_name: str) -> GateResult:
        """Check a single gate."""
        check_type = gate.get("check")
        gate_id = gate.get("id", "unknown")
        name = gate.get("name", "Unknown gate")
        severity = gate.get("severity", "warning")

        try:
            if check_type == "file_exists":
                return self._check_file_exists(gate, stage_name)
            elif check_type == "file_count":
                return self._check_file_count(gate, stage_name)
            elif check_type == "json_valid":
                return self._check_json_valid(gate, stage_name)
            elif check_type == "json_field_present":
                return self._check_json_field_present(gate, stage_name)
            elif check_type == "json_field_count":
                return self._check_json_field_count(gate, stage_name)
            elif check_type == "pattern_exists":
                return self._check_pattern_exists(gate, stage_name)
            elif check_type == "pattern_count":
                return self._check_pattern_count(gate, stage_name)
            elif check_type == "cross_reference":
                return self._check_cross_reference(gate, stage_name)
            else:
                return GateResult(
                    gate_id=gate_id,
                    name=name,
                    passed=False,
                    severity=severity,
                    message=f"Unknown check type: {check_type}",
                    stage=stage_name
                )
        except Exception as e:
            return GateResult(
                gate_id=gate_id,
                name=name,
                passed=False,
                severity=severity,
                message=f"Check error: {e}",
                stage=stage_name
            )

    def _check_file_exists(self, gate: dict, stage: str) -> GateResult:
        """Check if file exists."""
        # gates.yaml is developer-controlled (checked into the plugin directory),
        # so paths in it are trusted. No traversal risk for this CLI tool.
        file_path = self.base_dir / gate["path"]
        exists = file_path.exists()

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=exists,
            severity=gate.get("severity", "blocker"),
            message="File exists" if exists else f"File not found: {gate['path']}",
            stage=stage
        )

    def _check_file_count(self, gate: dict, stage: str) -> GateResult:
        """Check file count matches expectation."""
        pattern = self.base_dir / gate["path"]
        files = glob.glob(str(pattern))
        count = len(files)

        expected = gate.get("expect")
        min_count = gate.get("min", 0)
        max_count = gate.get("max")

        if expected is not None:
            passed = count == expected
            expected_str = str(expected)
        else:
            passed = count >= min_count
            if max_count is not None:
                passed = passed and count <= max_count
                expected_str = f"{min_count}-{max_count}"
            else:
                expected_str = f">= {min_count}"

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=f"Found {count} files" if passed else f"Expected {expected_str} files, found {count}",
            stage=stage,
            actual=count,
            expected=expected_str
        )

    def _check_json_valid(self, gate: dict, stage: str) -> GateResult:
        """Check if file is valid JSON."""
        file_path = self.base_dir / gate["path"]

        if not file_path.exists():
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"File not found: {gate['path']}",
                stage=stage
            )

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json.load(f)
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=True,
                severity=gate.get("severity", "blocker"),
                message="Valid JSON",
                stage=stage
            )
        except json.JSONDecodeError as e:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"Invalid JSON: {e}",
                stage=stage
            )

    def _check_json_field_present(self, gate: dict, stage: str) -> GateResult:
        """Check if JSON field is present and not empty."""
        path_pattern = gate["path"]
        field_path = gate["field"]
        all_files = gate.get("all_files", False)

        files = glob.glob(str(self.base_dir / path_pattern))

        if not files:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"No files found matching: {path_pattern}",
                stage=stage
            )

        files_with_field = 0
        total_files = len(files)

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                value = self._get_nested_field(data, field_path)
                if value is not None and value != "" and value != []:
                    files_with_field += 1
            except (json.JSONDecodeError, KeyError):
                pass

        if all_files:
            passed = files_with_field == total_files
            message = f"{files_with_field}/{total_files} files have '{field_path}'"
        else:
            passed = files_with_field > 0
            message = f"Field '{field_path}' present" if passed else f"Field '{field_path}' not found or empty"

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=message,
            stage=stage,
            actual=files_with_field
        )

    def _check_json_field_count(self, gate: dict, stage: str) -> GateResult:
        """Check JSON field item count against min/max."""
        file_path = self.base_dir / gate["path"]
        field_path = gate["field"]

        if not file_path.exists():
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"File not found: {gate['path']}",
                stage=stage
            )

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message="Invalid JSON",
                stage=stage
            )

        value = self._get_nested_field(data, field_path)

        if value is None:
            count = 0
        elif isinstance(value, dict):
            if gate.get("count_non_null", False):
                count = sum(1 for v in value.values() if v is not None)
            else:
                count = len(value)
        elif isinstance(value, list):
            count = len(value)
        else:
            count = 1 if value else 0

        min_count = gate.get("min", 0)
        max_count = gate.get("max")

        passed = count >= min_count
        expected_parts = [f">= {min_count}"]

        if max_count is not None:
            passed = passed and count <= max_count
            expected_parts.append(f"<= {max_count}")

        expected = " and ".join(expected_parts)

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=f"Found {count} items" if passed else f"Expected {expected}, found {count}",
            stage=stage,
            actual=count,
            expected=expected
        )

    def _check_pattern_exists(self, gate: dict, stage: str) -> GateResult:
        """Check if regex pattern exists in file(s)."""
        path_pattern = gate["path"]
        regex_pattern = gate["pattern"]
        all_files = gate.get("all_files", False)
        json_field = gate.get("json_field")

        files = glob.glob(str(self.base_dir / path_pattern))

        if not files:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"No files found matching: {path_pattern}",
                stage=stage
            )

        try:
            regex = re.compile(regex_pattern, re.MULTILINE)
        except re.error as e:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"Invalid regex pattern: {e}",
                stage=stage
            )
        files_with_pattern = 0

        for file_path in files:
            try:
                if json_field:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    content = str(self._get_nested_field(data, json_field) or "")
                else:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                if regex.search(content):
                    files_with_pattern += 1
            except (json.JSONDecodeError, IOError):
                pass

        if all_files:
            passed = files_with_pattern == len(files)
            message = f"{files_with_pattern}/{len(files)} files match pattern"
        else:
            passed = files_with_pattern > 0
            message = "Pattern found" if passed else f"Pattern not found: {regex_pattern}"

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=message,
            stage=stage,
            actual=files_with_pattern
        )

    def _check_pattern_count(self, gate: dict, stage: str) -> GateResult:
        """Check regex pattern occurrence count."""
        path_pattern = gate["path"]
        regex_pattern = gate["pattern"]

        files = glob.glob(str(self.base_dir / path_pattern))

        if not files:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"No files found matching: {path_pattern}",
                stage=stage
            )

        try:
            regex = re.compile(regex_pattern, re.MULTILINE)
        except re.error as e:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"Invalid regex pattern: {e}",
                stage=stage
            )
        total_count = 0

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                matches = regex.findall(content)
                total_count += len(matches)
            except IOError:
                pass

        min_count = gate.get("min")
        max_count = gate.get("max")

        if min_count is None and max_count is None:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message="Gate configuration error: pattern_count requires min or max",
                stage=stage
            )

        passed = True
        expected_parts = []

        if min_count is not None:
            if total_count < min_count:
                passed = False
            expected_parts.append(f">= {min_count}")

        if max_count is not None:
            if total_count > max_count:
                passed = False
            expected_parts.append(f"<= {max_count}")

        expected = " and ".join(expected_parts)

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=f"Found {total_count} matches" if passed else f"Expected {expected}, found {total_count}",
            stage=stage,
            actual=total_count,
            expected=expected
        )

    def _check_cross_reference(self, gate: dict, stage: str) -> GateResult:
        """Check that references between files exist."""
        source_pattern = gate["source_path"]
        source_field = gate["source_field"]
        target_dir = gate["target_dir"]
        target_pattern = gate.get("target_pattern", "{id}.json")

        source_files = glob.glob(str(self.base_dir / source_pattern))

        if not source_files:
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=f"No source files found: {source_pattern}",
                stage=stage
            )

        missing_refs = []
        malformed_files = []
        total_refs = 0

        for source_file in source_files:
            try:
                with open(source_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                refs = self._get_nested_field(data, source_field)
                if refs is None:
                    continue

                if not isinstance(refs, list):
                    refs = [refs]

                for ref in refs:
                    total_refs += 1
                    target_file = target_pattern.replace("{id}", str(ref))
                    target_path = self.base_dir / target_dir / target_file

                    if not target_path.exists():
                        missing_refs.append(ref)
            except (json.JSONDecodeError, IOError):
                malformed_files.append(Path(source_file).name)

        if malformed_files:
            detail = f"Malformed source files: {malformed_files}"
            if missing_refs:
                detail += f"; missing references: {missing_refs}"
            return GateResult(
                gate_id=gate["id"],
                name=gate["name"],
                passed=False,
                severity=gate.get("severity", "blocker"),
                message=detail,
                stage=stage
            )

        passed = len(missing_refs) == 0
        if passed:
            message = f"All {total_refs} references exist"
        else:
            shown = missing_refs[:5]
            extra = len(missing_refs) - len(shown)
            message = f"Missing references: {shown}"
            if extra:
                message += f" and {extra} more"

        return GateResult(
            gate_id=gate["id"],
            name=gate["name"],
            passed=passed,
            severity=gate.get("severity", "blocker"),
            message=message,
            stage=stage,
            actual=total_refs - len(missing_refs),
            expected=f"{total_refs}"
        )

    def _get_nested_field(self, data: dict, field_path: str) -> Any:
        """Get nested field value using dot notation."""
        parts = field_path.split(".")
        value = data

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None

        return value

def _build_fallback_config() -> GatesConfig:
    """Build a fallback gates config for when PyYAML is not available.

    Covers JSON-based and file-based checks only. Pattern-based checks
    (pattern_exists, pattern_count) require PyYAML to load gates.yaml.
    """
    return GatesConfig(
        version="fallback",
        stages={
            "discover": {
                "description": "Generate semantic memory (fallback mode)",
                "output_dir": ".gt/memory",
                "gates": [
                    {"id": "semantic_valid", "name": "Semantic memory is valid JSON",
                     "check": "json_valid", "path": ".gt/memory/semantic.json", "severity": "blocker"},
                    {"id": "project_identified", "name": "Project name identified",
                     "check": "json_field_present", "path": ".gt/memory/semantic.json",
                     "field": "project.name", "severity": "blocker"},
                    {"id": "tech_stack_detected", "name": "Tech stack detected (2+ fields)",
                     "check": "json_field_count", "path": ".gt/memory/semantic.json",
                     "field": "tech_stack", "min": 2, "count_non_null": True, "severity": "blocker"},
                    {"id": "evidence_recorded", "name": "Evidence files recorded",
                     "check": "json_field_count", "path": ".gt/memory/semantic.json",
                     "field": "evidence.files_analyzed", "min": 1, "severity": "warning"},
                ],
            },
            "plan": {
                "description": "Generate roadmap (fallback mode)",
                "output_dir": "scopecraft",
                "gates": [
                    {"id": "outputs_exist", "name": "All required plan outputs exist (6+ files)",
                     "check": "file_count", "path": "scopecraft/*.md", "min": 6, "severity": "blocker"},
                ],
            },
            "structure": {
                "description": "Create beads and convoys (fallback mode)",
                "output_dir": ".gt",
                "gates": [
                    {"id": "beads_extracted", "name": "Beads extracted (1+ required)",
                     "check": "file_count", "path": ".gt/beads/gt-*.json", "min": 1, "severity": "blocker"},
                    {"id": "convoy_created", "name": "Convoy created (1+ required)",
                     "check": "file_count", "path": ".gt/convoys/*convoy-*.json", "min": 1, "severity": "blocker"},
                ],
            },
            "reconcile": {
                "description": "Ecosystem reconciliation (fallback mode)",
                "output_dir": "scopecraft",
                "gates": [
                    {"id": "checkpoint_valid", "name": "Checkpoint is valid JSON",
                     "check": "json_valid", "path": "scopecraft/.checkpoint.json", "severity": "blocker"},
                    {"id": "checkpoint_schema", "name": "Checkpoint has reconcile-checkpoint-v1 schema",
                     "check": "json_field_present", "path": "scopecraft/.checkpoint.json",
                     "field": "$schema", "severity": "blocker"},
                    {"id": "config_loaded", "name": "Checkpoint confirms ecosystem config was loaded",
                     "check": "json_field_present", "path": "scopecraft/.checkpoint.json",
                     "field": "reconcile.ecosystem_root", "severity": "blocker"},
                    {"id": "projects_found", "name": "2+ projects found in checkpoint",
                     "check": "json_field_count", "path": "scopecraft/.checkpoint.json",
                     "field": "projects", "min": 2, "severity": "blocker"},
                    {"id": "alignment_report_exists", "name": "Alignment report generated",
                     "check": "file_exists", "path": "scopecraft/ALIGNMENT_REPORT.md", "severity": "blocker"},
                    {"id": "perspectives_exists", "name": "Perspectives generated",
                     "check": "file_exists", "path": "scopecraft/PERSPECTIVES.md", "severity": "blocker"},
                ],
            },
        },
        workflows={
            "migrate": {"description": "Standard migration (fallback)", "stages": ["discover", "plan", "structure"]},
            "ecosystem": {"description": "Ecosystem reconciliation (fallback)", "stages": ["reconcile"]},
        },
        exit_codes={"pass": 0, "blocker_failed": 1, "warning_failed": 2, "security_error": 3},
    )

def load_gates_config(config_path: Path) -> Optional[GatesConfig]:
    """Load gates configuration from YAML file.

    Falls back to built-in config when PyYAML is not available.
    """
    if not HAS_YAML:
        print("Warning: PyYAML not installed. Running in fallback mode (JSON/file checks only).",
              file=sys.stderr)
        print("         Pattern-based checks skipped. Install PyYAML for full validation:",
              file=sys.stderr)
        print("         pip install pyyaml", file=sys.stderr)
        print(file=sys.stderr)
        return _build_fallback_config()

    if not config_path.exists():
        print(f"Error: Gates config not found: {config_path}", file=sys.stderr)
        return None

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        print(f"Error: gates.yaml is empty or invalid: {config_path}", file=sys.stderr)
        return None

    if not data.get("stages"):
        print(f"Error: gates.yaml missing required 'stages' section: {config_path}", file=sys.stderr)
        return None

    return GatesConfig(
        version=data.get("version", "1.0"),
        stages=data.get("stages", {}),
        workflows=data.get("workflows", {}),
        exit_codes=data.get("exit_codes", {})
    )

def print_results(results: list[GateResult], verbose: bool = False) -> tuple[int, int]:
    """Print validation results and return counts."""
    blockers_failed = 0
    warnings_failed = 0

    print("\n" + "=" * 60)
    print("LISA VALIDATION RESULTS")
    print("=" * 60 + "\n")

    current_stage = None
    for result in results:
        if result.stage != current_stage:
            current_stage = result.stage
            print(f"\n--- Stage: {current_stage.upper()} ---\n")

        if result.passed:
            status = "\033[92m\u2713 PASS\033[0m"
        elif result.severity == "blocker":
            status = "\033[91m\u2717 FAIL\033[0m"
            blockers_failed += 1
        else:
            status = "\033[93m\u26a0 WARN\033[0m"
            warnings_failed += 1

        print(f"{status} [{result.gate_id}] {result.name}")
        if verbose or not result.passed:
            print(f"       {result.message}")
        print()

    # Summary
    total = len(results)
    passed = total - blockers_failed - warnings_failed

    print("-" * 60)
    print(f"Total: {total} | Passed: {passed} | Blockers: {blockers_failed} | Warnings: {warnings_failed}")
    print("-" * 60)

    if blockers_failed > 0:
        print("\n\u274c VALIDATION FAILED")
    elif warnings_failed > 0:
        print("\n\u26a0\ufe0f  PASSED WITH WARNINGS")
    else:
        print("\n\u2705 ALL GATES PASSED")

    return blockers_failed, warnings_failed

def generate_json_output(results: list[GateResult]) -> str:
    """Generate JSON output."""
    output = [
        {
            "gate_id": r.gate_id,
            "name": r.name,
            "passed": r.passed,
            "severity": r.severity,
            "message": r.message,
            "stage": r.stage,
            "actual": r.actual,
            "expected": r.expected
        }
        for r in results
    ]
    return json.dumps(output, indent=2)

def generate_markdown_report(results: list[GateResult]) -> str:
    """Generate markdown report."""
    lines = [
        "## Quality Gate Status",
        "",
        "| Status | Stage | Gate | Message |",
        "|--------|-------|------|---------|"
    ]

    for result in results:
        if result.passed:
            status = "\u2705"
        elif result.severity == "blocker":
            status = "\u274c"
        else:
            status = "\u26a0\ufe0f"

        lines.append(f"| {status} | {result.stage} | {result.name} | {result.message} |")

    blockers = sum(1 for r in results if not r.passed and r.severity == "blocker")
    warnings = sum(1 for r in results if not r.passed and r.severity == "warning")

    lines.extend([
        "",
        f"**Blockers: {blockers} | Warnings: {warnings}**",
        ""
    ])

    if blockers > 0:
        lines.append("\u26d4 Cannot proceed until all blockers pass.")
    else:
        lines.append("\u2705 Ready to proceed.")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Validate Lisa plugin outputs")
    parser.add_argument("--stage", "-s",
                        choices=["research", "discover", "plan", "structure", "reconcile", "all"],
                        default="all", help="Stage to validate")
    parser.add_argument("--workflow", "-w",
                        choices=["migrate", "rescue", "ecosystem"],
                        help="Validate workflow stages")
    parser.add_argument("--base-dir", "-d", default=".", help="Base directory")
    parser.add_argument("--config", "-c", help="Path to gates.yaml (default: auto-detect)")
    parser.add_argument("--format", "-f", choices=["text", "json", "markdown"],
                        default="text", help="Output format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all gate details")
    args = parser.parse_args()

    # Find gates.yaml
    if args.config:
        config_path = Path(args.config)
    else:
        # Try common locations
        candidates = [
            Path(__file__).parent.parent / "gates.yaml",
            Path("plugins/lisa/gates.yaml"),
            Path("gates.yaml")
        ]
        config_path = None
        for candidate in candidates:
            if candidate.exists():
                config_path = candidate
                break

        if config_path is None and HAS_YAML:
            print("Error: Could not find gates.yaml. Specify with --config", file=sys.stderr)
            sys.exit(1)

    # Load configuration (falls back to built-in config if PyYAML unavailable)
    config = load_gates_config(config_path or Path("gates.yaml"))
    if config is None:
        sys.exit(1)

    # Create validator
    validator = UnifiedValidator(Path(args.base_dir), config)

    # Run validation
    if args.workflow:
        results = validator.validate_workflow(args.workflow)
    elif args.stage == "all":
        results = validator.validate_all()
    else:
        results = validator.validate_stage(args.stage)

    # Output results
    if args.format == "json":
        print(generate_json_output(results))
    elif args.format == "markdown":
        print(generate_markdown_report(results))
    else:
        print_results(results, args.verbose)

    # Determine exit code
    blockers = sum(1 for r in results if not r.passed and r.severity == "blocker")
    warnings = sum(1 for r in results if not r.passed and r.severity == "warning")

    if blockers > 0:
        sys.exit(1)
    elif warnings > 0:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
