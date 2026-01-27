---
description: Bundle Beads into Convoys for Gastown assignment. Groups related work items into optimal work packages.
skill: gastown-migration
agent: gastown-migrator
---

# Convoy — lisa-loops-memory

Bundle existing Beads into Convoys for efficient Gastown assignment.

## Prerequisites

Run `/lisa-loops-memory:beads` first to generate beads in `.gt/beads/`.

## What This Does

1. **Reads existing beads** — Loads all `.gt/beads/*.json`
2. **Analyzes relationships** — Groups by epic, dependencies, skill
3. **Creates bundles** — 3-7 beads per convoy (optimal size)
4. **Generates convoys** — Outputs to `.gt/convoys/`

## Execution

1. Follow the "Phase 3: Convoy" section in `skills/gastown-migration/SKILL.md`
2. Create `.gt/convoys/` directory if it doesn't exist
3. Group beads using bundling strategies
4. Write convoy JSON files: `.gt/convoys/convoy-*.json`

## Bundling Strategies

| Strategy | Description |
|----------|-------------|
| By Epic | Group beads from same epic/feature area |
| By Dependency | Chain dependent beads sequentially |
| By Skill | Group beads requiring similar expertise |
| By Size | Combine small beads, isolate large ones |

## Output

Creates `.gt/convoys/convoy-*.json` files with:
- Sequential ID (convoy-001, convoy-002, etc.)
- Descriptive name and purpose
- List of 3-7 bead IDs
- Status (pending by default)

## Quality Gates

- [ ] At least 1 convoy created
- [ ] All convoys have 3-7 beads
- [ ] All referenced bead IDs exist in `.gt/beads/`
- [ ] Convoy JSON is valid

## Example

```bash
/lisa-loops-memory:convoy
```

After running, list convoys with: `ls .gt/convoys/`
