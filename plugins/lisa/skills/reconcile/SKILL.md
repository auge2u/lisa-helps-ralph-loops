---
name: reconcile
description: Cross-validates ecosystem assumptions against project semantic memory. Identifies drift, schema divergence, and misalignments across multiple codebases.
stage: 5
---

# Reconcile Skill (Stage 5)

This skill compares what each project says about itself (via `.gt/memory/semantic.json`) against what the ecosystem assumes, producing an alignment report and checkpoint.

## When to Use

Use this skill when:
- A plugin ships a new version
- A new project is added to the ecosystem
- Quality gates or schemas change across plugins
- Steering questions are resolved and decisions recorded
- Prior reconcile is stale (check `.checkpoint.json` timestamp)

## Output Structure

```
project/
└── scopecraft/
    ├── ALIGNMENT_REPORT.md   # Human-readable findings
    ├── PERSPECTIVES.md        # Side-by-side project self-reports
    └── .checkpoint.json       # Machine-readable state for recovery
```

Output templates: [`templates/`](templates/) | Checkpoint schema: [`checkpoint-schema.json`](checkpoint-schema.json)

## Ecosystem Configuration

The reconcile skill reads project locations from `~/.lisa/ecosystem.json`.

### Schema: ecosystem-config-v1

```json
{
  "$schema": "ecosystem-config-v1",
  "name": "ecosystem-name",
  "projects": [
    {
      "name": "project-name",
      "path": "~/github/org/repo",
      "role": "role-description",
      "active": true,
      "notes": "optional context"
    }
  ],
  "updated": "YYYY-MM-DD"
}
```

**Path handling:** All paths use `~/` for portability. Expand tildes to absolute paths before file access. Example: `~/github/auge2u/lisa3` becomes `/Users/<user>/github/auge2u/lisa3`.

## Reconciliation Procedure

### Step 1: Load Ecosystem Config

1. Read `~/.lisa/ecosystem.json`
2. Validate it has `projects` array with at least 1 entry
3. Expand all `~` paths to absolute paths
4. Note which projects are `active: true`

**If `~/.lisa/ecosystem.json` is missing:** Stop and instruct user to create it. Provide the schema above.

### Step 2: Gather Semantic Memory

For each active project:

1. Check if `<project.path>` exists locally
2. If local: read `<project.path>/.gt/memory/semantic.json`
3. If not local: try GitHub API as fallback (e.g. `gh api repos/<org>/<repo>/contents/.gt/memory/semantic.json`)
4. If neither works: record project as `status: "not-found"` and continue

**Handle different schemas gracefully:**
- Lisa and Carlos use `semantic-memory-v1` schema with `ecosystem_role`, `integration_points`, `non_goals`
- Conductor (and other gastown projects) may use `https://gastown.dev/schemas/semantic-memory.json` without ecosystem fields
- Extract common fields regardless of schema: `project.name`, `project.type`, `project.primary_language`, `tech_stack`
- Flag schema differences as a finding (not an error)

### Step 3: Read Existing Ecosystem State

If running from ecosystem root:
1. Read `scopecraft/ALIGNMENT_REPORT.md` if it exists (prior findings)
2. Read `scopecraft/.checkpoint.json` if it exists (prior state)
3. Note the prior reconcile version and timestamp for change tracking

### Step 4: Compare Perspectives

For each pair of projects, check:

| Check | What to compare |
|-------|----------------|
| **Role conflicts** | Do any two projects claim the same role or write to the same outputs? |
| **Interface agreements** | Does what project A says it writes match what project B says it reads? |
| **Tech stack drift** | Are shared dependencies on compatible versions? |
| **Constraint violations** | Does any project violate another's stated constraints or non-goals? |
| **Capability gaps** | Are expected capabilities (from design docs) missing from self-reports? |
| **Schema divergence** | Do projects use different semantic.json schemas? What fields are missing? |
| **Stale assumptions** | Are any assumptions from prior reconcile now outdated? |

Classify each finding as:
- **Alignment** — Both projects agree
- **Misalignment** — Projects contradict each other (assign severity: HIGH/MEDIUM/LOW)
- **Gap** — Expected information is missing

### Step 5: Validate Gate Configs

For each project that has quality gates:
1. Check if `gates.yaml` exists (declarative) or gates are hardcoded
2. Compare gate definitions across plugins — look for:
   - Same gate name, different criteria
   - Missing gates that another plugin expects
   - Format inconsistencies (declarative vs hardcoded)
3. Record gate config misalignments

### Step 6: Generate Outputs

#### ALIGNMENT_REPORT.md

```markdown
# Ecosystem Alignment Report

**Generated:** YYYY-MM-DD (reconcile vX.Y.Z)
**Previous reconcile:** YYYY-MM-DD vX.Y.Z (or "none")
**Ecosystem root:** <repo name>
**Projects:** <list with status>

---

## Summary

| Status | Count | Change from previous |
|--------|-------|----------------------|
| Aligned | N | +/- N |
| Misaligned | N | +/- N |
| Gaps | N | +/- N |

**Overall assessment:** <2-3 sentence summary>

---

## Changes Since vX.Y.Z
<!-- Only if prior checkpoint exists -->

| Item | Previous | Current | Impact |
|------|----------|---------|--------|

---

## Alignments (What's Working)

### A1: <title>
<description of what both projects agree on>

<!-- Repeat for each alignment -->

---

## Misalignments (Need Resolution)

### M1: <title> (PRIORITY: HIGH/MEDIUM/LOW)
**<Project A>'s view:** ...
**<Project B>'s view:** ...

**Impact:** ...
**Resolution:** ...
**Status:** new/unchanged/worsened

<!-- Repeat for each misalignment -->

---

## Gaps (Missing Information)

### G1: <title>
<what's missing and why it matters>

---

## Steering Questions

| # | Question | Decision or Options |
|---|----------|---------------------|

---

## Next Actions

| Priority | Action | Owner | Blocks |
|----------|--------|-------|--------|
```

#### PERSPECTIVES.md

```markdown
# Ecosystem Perspectives

**Generated:** YYYY-MM-DD (reconcile vX.Y.Z)
**Projects scanned:** N attempted, N found

---

## Project Status Matrix

| Field | Project A | Project B | ... |
|-------|-----------|-----------|-----|
| Status | found/not-found | ... | |
| Version | X.Y.Z | ... | |
| Schema | semantic-memory-v1 | ... | |
<!-- Key fields from each semantic.json -->

---

## <Project Name> Self-Report

**Source:** <path to semantic.json>

| Attribute | Value |
|-----------|-------|
<!-- Extracted fields -->

**Reads from:** ...
**Writes to:** ...
**Does not own:** ...

<!-- Repeat for each project -->

---

## Ecosystem Role Comparison

| Responsibility | Project A | Project B | Conflict? |
|----------------|-----------|-----------|-----------|

---

## Interface Agreement Check

| Interface | Project A says | Project B says | Match? |
|-----------|---------------|----------------|--------|

---

## Schema Divergence Note
<!-- Only if schemas differ across projects -->
```

#### .checkpoint.json

Formal JSON Schema: [`checkpoint-schema.json`](checkpoint-schema.json)

```json
{
  "$schema": "reconcile-checkpoint-v1",
  "reconcile": {
    "timestamp": "ISO-8601",
    "version": "X.Y.Z",
    "previous_version": "X.Y.Z or null",
    "ecosystem_root": "repo-name",
    "method": "lisa reconcile skill (Stage 5)"
  },
  "projects": {
    "<name>": {
      "path": "~/...",
      "status": "found|not-found",
      "source": "local filesystem|GitHub API",
      "semantic_json": {
        "exists": true,
        "version": "X.Y.Z",
        "schema": "schema-identifier",
        "last_scan": "ISO-8601",
        "project_name": "name",
        "role": "role"
      },
      "scopecraft": {
        "exists": true,
        "files": ["..."],
        "level": "project|ecosystem"
      },
      "alignment": "aligned|mostly-aligned|divergent|not-found"
    }
  },
  "alignment_summary": {
    "total_projects": 0,
    "found": 0,
    "missing": 0,
    "aligned": 0,
    "mostly_aligned": 0,
    "divergent": 0,
    "alignments": 0,
    "misalignments": 0,
    "gaps": 0
  },
  "misalignments": [
    {
      "id": "M1",
      "severity": "high|medium|low",
      "description": "...",
      "affects": ["project-names"],
      "resolution": "...",
      "status": "new|unchanged|worsened|resolved"
    }
  ],
  "resolved": [],
  "decisions": {
    "resolved_date": "YYYY-MM-DD",
    "steering_questions": [],
    "open_questions": []
  },
  "next_reconcile_triggers": []
}
```

## Schema Tolerance

External projects (e.g., Conductor) may produce their own reconcile checkpoints with different field names. When reading external checkpoints during reconcile, extract common fields regardless of schema:
- `misalignments` / `remaining_misalignments` — treat as equivalent
- `steering_questions` / `steering_questions_resolved` + `open_queries` — extract both
- Different severity scales or status enums — normalize to Lisa's convention

The `reconcile-checkpoint-v1` schema (see [`checkpoint-schema.json`](checkpoint-schema.json)) is canonical for Lisa's own checkpoints. External formats are tolerated as input, not required to conform.

## Error Handling

| Error | Response |
|-------|----------|
| `~/.lisa/ecosystem.json` missing | Stop. Print schema and ask user to create it. |
| Project path doesn't exist locally | Warn, try GitHub API, record as `"source": "GitHub API"` or `"not-found"` |
| `semantic.json` missing for a project | Record `semantic_json.exists: false`, continue with other projects |
| `semantic.json` malformed | Record error in checkpoint, skip project's comparison |
| Different schema than expected | Extract common fields, flag divergence as a finding |
| No prior checkpoint | First reconcile — skip "Changes Since" section |
| Fewer than 2 projects reachable | Warn but still produce report (limited comparison) |

## Quality Gates

Reconcile quality gates are defined in `gates.yaml` (9 gates, automated via `validate.py --stage reconcile`):

| Gate | Check | Severity |
|------|-------|----------|
| `config_loaded` | Checkpoint confirms ecosystem config was loaded | blocker |
| `projects_found` | 2+ projects found in checkpoint | blocker |
| `alignment_report_exists` | ALIGNMENT_REPORT.md generated | blocker |
| `perspectives_exists` | PERSPECTIVES.md generated | blocker |
| `checkpoint_valid` | .checkpoint.json is valid JSON | blocker |
| `checkpoint_schema` | Checkpoint has reconcile-checkpoint-v1 schema | blocker |
| `report_has_summary` | Report has Summary section | blocker |
| `report_has_misalignments` | Report has Misalignments section | warning |
| `changes_tracked` | Prior version tracked in checkpoint | warning |

## Next Steps

After reconcile completes:
- Run `validate.py --stage reconcile` to verify outputs
- Review `ALIGNMENT_REPORT.md` for action items
- Address HIGH priority misalignments first
- Re-run reconcile after significant changes (see `next_reconcile_triggers` in checkpoint)
