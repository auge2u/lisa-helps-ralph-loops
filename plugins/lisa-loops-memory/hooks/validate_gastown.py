#!/usr/bin/env python3
"""
Gastown Migration Validator for lisa-loops-memory

Validates .gt/ structure and contents against Gastown requirements.
Can validate individual phases or the complete migration.

Usage:
    python validate_gastown.py [--phase analyze|beads|convoy|all]

Exit codes:
    0 - All gates passed
    1 - Required gates failed
    2 - Warnings (non-blocking)
    3 - Security error
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class GateResult:
    """Result of a quality gate check."""
    gate_id: str
    name: str
    passed: bool
    severity: str
    message: str
    phase: str


class GastownValidator:
    """Validates Gastown migration outputs."""

    BEAD_ID_PATTERN = re.compile(r'^gt-[a-z0-9]{5}$')
    CONVOY_ID_PATTERN = re.compile(r'^convoy-\d{3}$')

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.gt_dir = self.base_dir / ".gt"

    def validate_all(self) -> list[GateResult]:
        """Run all validation checks."""
        results = []
        results.extend(self.validate_analyze())
        results.extend(self.validate_beads())
        results.extend(self.validate_convoy())
        return results

    def validate_analyze(self) -> list[GateResult]:
        """Validate Phase 1: Analyze (semantic memory)."""
        results = []
        semantic_path = self.gt_dir / "memory" / "semantic.json"

        # Gate: semantic.json exists
        if not semantic_path.exists():
            results.append(GateResult(
                gate_id="semantic_exists",
                name="Semantic memory file exists",
                passed=False,
                severity="blocker",
                message=f"File not found: {semantic_path}",
                phase="analyze"
            ))
            return results

        # Gate: valid JSON
        try:
            with open(semantic_path, "r", encoding="utf-8") as f:
                semantic = json.load(f)
        except json.JSONDecodeError as e:
            results.append(GateResult(
                gate_id="semantic_valid_json",
                name="Semantic memory is valid JSON",
                passed=False,
                severity="blocker",
                message=f"Invalid JSON: {e}",
                phase="analyze"
            ))
            return results

        results.append(GateResult(
            gate_id="semantic_valid_json",
            name="Semantic memory is valid JSON",
            passed=True,
            severity="blocker",
            message="Valid JSON",
            phase="analyze"
        ))

        # Gate: project.name populated
        project_name = semantic.get("project", {}).get("name")
        results.append(GateResult(
            gate_id="project_identified",
            name="Project name identified",
            passed=project_name is not None and project_name != "",
            severity="blocker",
            message=f"project.name = {project_name}" if project_name else "project.name is null or empty",
            phase="analyze"
        ))

        # Gate: tech_stack has entries
        tech_stack = semantic.get("tech_stack", {})
        populated = sum(1 for v in tech_stack.values() if v is not None)
        results.append(GateResult(
            gate_id="tech_stack_detected",
            name="Tech stack detected (2+ fields)",
            passed=populated >= 2,
            severity="blocker",
            message=f"{populated} tech_stack fields populated",
            phase="analyze"
        ))

        # Gate: evidence recorded
        evidence = semantic.get("evidence", {})
        files_analyzed = evidence.get("files_analyzed", [])
        results.append(GateResult(
            gate_id="evidence_recorded",
            name="Evidence files recorded",
            passed=len(files_analyzed) > 0,
            severity="warning",
            message=f"{len(files_analyzed)} files in evidence",
            phase="analyze"
        ))

        return results

    def validate_beads(self) -> list[GateResult]:
        """Validate Phase 2: Beads (work items)."""
        results = []
        beads_dir = self.gt_dir / "beads"

        # Gate: beads directory exists
        if not beads_dir.exists():
            results.append(GateResult(
                gate_id="beads_dir_exists",
                name="Beads directory exists",
                passed=False,
                severity="blocker",
                message=f"Directory not found: {beads_dir}",
                phase="beads"
            ))
            return results

        # Find bead files
        bead_files = list(beads_dir.glob("gt-*.json"))

        # Gate: at least 1 bead
        results.append(GateResult(
            gate_id="beads_extracted",
            name="Beads extracted (1+ required)",
            passed=len(bead_files) >= 1,
            severity="blocker",
            message=f"{len(bead_files)} beads found",
            phase="beads"
        ))

        if not bead_files:
            return results

        # Validate each bead
        beads_with_criteria = 0
        beads_with_evidence = 0
        invalid_ids = []

        for bead_file in bead_files:
            try:
                with open(bead_file, "r", encoding="utf-8") as f:
                    bead = json.load(f)

                # Check ID format
                bead_id = bead.get("id", "")
                if not self.BEAD_ID_PATTERN.match(bead_id):
                    invalid_ids.append(bead_id)

                # Check acceptance criteria
                criteria = bead.get("acceptance_criteria", [])
                if len(criteria) >= 1:
                    beads_with_criteria += 1

                # Check evidence
                evidence = bead.get("evidence", {})
                if evidence.get("source"):
                    beads_with_evidence += 1

            except (json.JSONDecodeError, KeyError):
                pass

        # Gate: beads have acceptance criteria
        results.append(GateResult(
            gate_id="beads_have_criteria",
            name="Beads have acceptance criteria",
            passed=beads_with_criteria == len(bead_files),
            severity="blocker",
            message=f"{beads_with_criteria}/{len(bead_files)} beads have criteria",
            phase="beads"
        ))

        # Gate: beads have evidence
        results.append(GateResult(
            gate_id="beads_have_evidence",
            name="Beads have evidence source",
            passed=beads_with_evidence == len(bead_files),
            severity="warning",
            message=f"{beads_with_evidence}/{len(bead_files)} beads have evidence",
            phase="beads"
        ))

        # Gate: valid IDs
        results.append(GateResult(
            gate_id="beads_valid_ids",
            name="Bead IDs match gt-xxxxx pattern",
            passed=len(invalid_ids) == 0,
            severity="warning",
            message="All IDs valid" if not invalid_ids else f"Invalid IDs: {invalid_ids}",
            phase="beads"
        ))

        return results

    def validate_convoy(self) -> list[GateResult]:
        """Validate Phase 3: Convoy (work bundles)."""
        results = []
        convoys_dir = self.gt_dir / "convoys"
        beads_dir = self.gt_dir / "beads"

        # Gate: convoys directory exists
        if not convoys_dir.exists():
            results.append(GateResult(
                gate_id="convoy_dir_exists",
                name="Convoys directory exists",
                passed=False,
                severity="blocker",
                message=f"Directory not found: {convoys_dir}",
                phase="convoy"
            ))
            return results

        # Find convoy files
        convoy_files = list(convoys_dir.glob("convoy-*.json"))

        # Gate: at least 1 convoy
        results.append(GateResult(
            gate_id="convoy_created",
            name="Convoy created (1+ required)",
            passed=len(convoy_files) >= 1,
            severity="blocker",
            message=f"{len(convoy_files)} convoys found",
            phase="convoy"
        ))

        if not convoy_files:
            return results

        # Get existing bead IDs
        existing_beads = set()
        if beads_dir.exists():
            for bead_file in beads_dir.glob("gt-*.json"):
                try:
                    with open(bead_file, "r", encoding="utf-8") as f:
                        bead = json.load(f)
                        existing_beads.add(bead.get("id", ""))
                except (json.JSONDecodeError, KeyError):
                    pass

        # Validate each convoy
        valid_size_count = 0
        missing_beads = []

        for convoy_file in convoy_files:
            try:
                with open(convoy_file, "r", encoding="utf-8") as f:
                    convoy = json.load(f)

                beads = convoy.get("beads", [])

                # Check size (3-7 beads)
                if 3 <= len(beads) <= 7:
                    valid_size_count += 1

                # Check bead references exist
                for bead_id in beads:
                    if bead_id not in existing_beads:
                        missing_beads.append(bead_id)

            except (json.JSONDecodeError, KeyError):
                pass

        # Gate: convoy size valid
        results.append(GateResult(
            gate_id="convoy_size_valid",
            name="Convoys have 3-7 beads",
            passed=valid_size_count == len(convoy_files),
            severity="warning",
            message=f"{valid_size_count}/{len(convoy_files)} convoys have valid size",
            phase="convoy"
        ))

        # Gate: all beads exist
        results.append(GateResult(
            gate_id="convoy_beads_exist",
            name="All convoy beads exist",
            passed=len(missing_beads) == 0,
            severity="blocker",
            message="All beads exist" if not missing_beads else f"Missing beads: {missing_beads[:5]}",
            phase="convoy"
        ))

        return results


def print_results(results: list[GateResult], phase_filter: Optional[str] = None) -> tuple[int, int]:
    """Print validation results and return counts."""
    if phase_filter and phase_filter != "all":
        results = [r for r in results if r.phase == phase_filter]

    blockers_failed = 0
    warnings_failed = 0

    print("\n" + "=" * 60)
    print("GASTOWN MIGRATION VALIDATION RESULTS")
    if phase_filter and phase_filter != "all":
        print(f"Phase: {phase_filter}")
    print("=" * 60 + "\n")

    current_phase = None
    for result in results:
        if result.phase != current_phase:
            current_phase = result.phase
            print(f"\n--- Phase: {current_phase.upper()} ---\n")

        if result.passed:
            status = "✓ PASS"
            color = "\033[92m"
        elif result.severity == "blocker":
            status = "✗ FAIL"
            color = "\033[91m"
            blockers_failed += 1
        else:
            status = "⚠ WARN"
            color = "\033[93m"
            warnings_failed += 1

        reset = "\033[0m"
        print(f"{color}{status}{reset} [{result.gate_id}] {result.name}")
        print(f"       {result.message}")
        print()

    # Summary
    total = len(results)
    passed = total - blockers_failed - warnings_failed

    print("-" * 60)
    print(f"Total: {total} | Passed: {passed} | Blockers: {blockers_failed} | Warnings: {warnings_failed}")
    print("-" * 60)

    if blockers_failed > 0:
        print("\n❌ MIGRATION VALIDATION FAILED")
    elif warnings_failed > 0:
        print("\n⚠️  MIGRATION COMPLETE WITH WARNINGS")
    else:
        print("\n✅ MIGRATION VALIDATION PASSED - Ready for Gastown")

    return blockers_failed, warnings_failed


def main():
    parser = argparse.ArgumentParser(description="Validate Gastown migration")
    parser.add_argument("--phase", "-p", choices=["analyze", "beads", "convoy", "all"],
                        default="all", help="Phase to validate")
    parser.add_argument("--base-dir", "-d", default=".", help="Base directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    validator = GastownValidator(Path(args.base_dir))

    if args.phase == "all":
        results = validator.validate_all()
    elif args.phase == "analyze":
        results = validator.validate_analyze()
    elif args.phase == "beads":
        results = validator.validate_beads()
    elif args.phase == "convoy":
        results = validator.validate_convoy()

    if args.json:
        output = [
            {
                "gate_id": r.gate_id,
                "name": r.name,
                "passed": r.passed,
                "severity": r.severity,
                "message": r.message,
                "phase": r.phase
            }
            for r in results
        ]
        print(json.dumps(output, indent=2))
        blockers = sum(1 for r in results if not r.passed and r.severity == "blocker")
        sys.exit(1 if blockers > 0 else 0)
    else:
        blockers, warnings = print_results(results, args.phase)
        if blockers > 0:
            sys.exit(1)
        elif warnings > 0:
            sys.exit(2)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
