---
description: Extract work items from project as Gastown Beads. Scans TODOs, issues, PRDs, and backlogs to create actionable work items.
skill: gastown-migration
agent: gastown-migrator
---

# Beads — lisa-loops-memory

Extract work items from the project and structure them as Gastown Beads.

## What This Does

1. **Scans TODO comments** — Finds `TODO:`, `FIXME:`, `HACK:` in code
2. **Reads GitHub issues** — Imports open issues (if git repo)
3. **Parses PRD documents** — Extracts user stories with criteria
4. **Checks existing roadmaps** — Imports from `scopecraft/` if present
5. **Generates beads** — Outputs to `.gt/beads/`

## Execution

1. Follow the "Phase 2: Beads" section in `skills/gastown-migration/SKILL.md`
2. Create `.gt/beads/` directory if it doesn't exist
3. Generate unique IDs for each bead (`gt-xxxxx` format)
4. Write one JSON file per bead: `.gt/beads/gt-xxxxx.json`

## Bead Sources (Priority Order)

1. GitHub Issues (most authoritative)
2. PRD documents in `/docs`
3. TODO/FIXME comments in source code
4. `scopecraft/EPICS_AND_STORIES.md` if exists
5. `BACKLOG.md`, `TODO.md` files

## Output

Creates `.gt/beads/gt-*.json` files with:
- Unique ID in Gastown format
- Clear title and type (feature/bug/chore/docs/spike)
- Acceptance criteria (at least 2)
- Complexity estimate (XS/S/M/L/XL)
- Evidence linking to source

## Quality Gates

- [ ] At least 1 bead extracted
- [ ] All beads have acceptance criteria
- [ ] All beads have evidence.source
- [ ] All IDs match `gt-[a-z0-9]{5}` pattern

## Example

```bash
/lisa-loops-memory:beads
```

After running, list beads with: `ls .gt/beads/`
