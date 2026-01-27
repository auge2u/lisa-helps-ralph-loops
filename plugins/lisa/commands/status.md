---
description: Show migration progress and quality gate results across all stages.
---

# Status - Lisa

Display current migration status and quality gate results.

## When to Use

Use this command when:
- Want to check progress of an ongoing migration
- Need to see which quality gates are passing/failing
- Reviewing migration readiness before next stage

## What This Does

1. **Detects completed stages** - Checks for stage output directories
2. **Runs validation** - Executes quality gates for detected stages
3. **Shows progress** - Displays pass/fail status for each gate
4. **Suggests next steps** - Recommends what to run next

## Output

```
LISA MIGRATION STATUS
=====================

Stages Detected:
  [x] research  - .gt/research/ exists
  [x] discover  - .gt/memory/semantic.json exists
  [ ] plan      - scopecraft/ not found
  [ ] structure - .gt/beads/ not found

Quality Gates:
  research:
    [PASS] timeline_constructed
    [PASS] mission_clarified
    [WARN] drift_analyzed
    [PASS] recommendation_made

  discover:
    [PASS] semantic_valid
    [PASS] project_identified
    [FAIL] tech_stack_detected - Expected >= 2, found 1
    [PASS] evidence_recorded

Summary: 6 passed, 1 failed, 1 warning

Next Step: Run /lisa:discover to fix tech_stack detection
```

## Execution

```bash
/lisa:status
```

Or use the Python validator directly:

```bash
# Check all stages
python plugins/lisa/hooks/validate.py --stage all

# Check specific stage
python plugins/lisa/hooks/validate.py --stage discover

# Check workflow
python plugins/lisa/hooks/validate.py --workflow migrate

# Output as JSON
python plugins/lisa/hooks/validate.py --format json

# Output as markdown
python plugins/lisa/hooks/validate.py --format markdown
```

## Stage Detection

| Stage | Indicator |
|-------|-----------|
| research | `.gt/research/rescue.json` exists |
| discover | `.gt/memory/semantic.json` exists |
| plan | `scopecraft/ROADMAP.md` exists |
| structure | `.gt/beads/gt-*.json` exists |

## Gate Severity

| Severity | Meaning |
|----------|---------|
| blocker | Must pass before proceeding |
| warning | Should fix but non-blocking |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All gates passed |
| 1 | Blocker gates failed |
| 2 | Only warning gates failed |
| 3 | Security error |
