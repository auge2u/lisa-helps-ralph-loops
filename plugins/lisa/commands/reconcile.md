---
description: Reconcile ecosystem assumptions against project self-reports. Produces alignment report and checkpoint.
skill: reconcile
agent: migrator
stage: 5
---

# Reconcile (Stage 5) - Lisa

Cross-validate ecosystem assumptions against each project's semantic memory. Identify drift, misalignments, and schema divergence.

## When to Use

Use this command when:
- A plugin ships a new version
- A new project joins the ecosystem (e.g. Conductor cloned locally)
- Quality gates or schemas change in any plugin
- Steering questions are resolved
- You suspect ecosystem assumptions have drifted

## Prerequisites

- `~/.lisa/ecosystem.json` exists with project paths
- At least one project has `.gt/memory/semantic.json`
- Run from the ecosystem root (the repo hosting `scopecraft/`)

## What This Does

1. **Loads ecosystem config** - Reads `~/.lisa/ecosystem.json` for project paths
2. **Gathers self-reports** - Reads each project's `.gt/memory/semantic.json` (handles different schemas)
3. **Reads prior state** - Checks existing `scopecraft/ALIGNMENT_REPORT.md` and `.checkpoint.json`
4. **Compares perspectives** - Tech stack drift, constraint violations, capability gaps, schema divergence
5. **Validates gate configs** - Checks for `gates.yaml` conflicts across plugins
6. **Generates outputs** - Writes alignment report, perspectives, and checkpoint

## Execution

1. Follow the instructions in `skills/reconcile/SKILL.md`
2. Expand `~` paths from `ecosystem.json` to absolute paths
3. For missing local projects, try GitHub API as fallback
4. Output all files to `./scopecraft/`

## Output

Creates/updates in `./scopecraft/`:
- `ALIGNMENT_REPORT.md` - Alignments, misalignments, gaps, next actions
- `PERSPECTIVES.md` - Side-by-side self-reports from all projects
- `.checkpoint.json` - Machine-readable reconcile state for context recovery

## Quality Gates (Manual)

- [ ] `ecosystem.json` was loaded and parsed
- [ ] At least 2 projects were reachable
- [ ] `ALIGNMENT_REPORT.md` has Summary, Alignments, and Misalignments sections
- [ ] `PERSPECTIVES.md` has a section per project
- [ ] `.checkpoint.json` is valid JSON with `reconcile-checkpoint-v1` schema
- [ ] If prior checkpoint existed, changes are noted

## Example

```bash
/lisa:reconcile
```

After running, review `scopecraft/ALIGNMENT_REPORT.md` for findings and `scopecraft/.checkpoint.json` for machine-readable state.
