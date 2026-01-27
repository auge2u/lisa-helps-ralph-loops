---
description: Extract work items as Beads and bundle them into Convoys. Creates Gastown-compatible work structure.
skill: structure
agent: migrator
stage: 3
---

# Structure (Stage 3) - Lisa

Extract work items from the project and structure them as Gastown Beads and Convoys.

## When to Use

Use this command when:
- Have completed `discover` and optionally `plan` stages
- Ready to create actionable work items
- Want to structure work for Gastown multi-agent execution
- Need to bundle related tasks for efficient assignment

## What This Does

### Beads (Work Items)
1. **Scans TODO comments** - Finds `TODO:`, `FIXME:`, `HACK:` in code
2. **Reads GitHub issues** - Imports open issues (if git repo)
3. **Parses PRD documents** - Extracts user stories with criteria
4. **Checks existing roadmaps** - Imports from `scopecraft/` if present
5. **Generates beads** - Outputs to `.gt/beads/`

### Convoys (Work Bundles)
1. **Analyzes dependencies** - Groups related beads
2. **Applies sizing rules** - 3-7 beads per convoy
3. **Bundles by theme** - Epic, skill, or dependency chain
4. **Generates convoys** - Outputs to `.gt/convoys/`

## Execution

1. Follow the instructions in `skills/structure/SKILL.md`
2. Create `.gt/beads/` and `.gt/convoys/` directories
3. Generate beads with unique IDs (`gt-xxxxx` format)
4. Bundle beads into convoys (`convoy-XXX` format)

## Output

Creates `.gt/beads/gt-*.json` files with:
- Unique ID in Gastown format
- Clear title and type (feature/bug/chore/docs/spike)
- Acceptance criteria (at least 1)
- Complexity estimate (XS/S/M/L/XL)
- Evidence linking to source

Creates `.gt/convoys/convoy-*.json` files with:
- Convoy ID and name
- List of 3-7 bead IDs
- Theme description
- Status tracking

## Quality Gates

### Beads
- [ ] At least 1 bead extracted
- [ ] All beads have acceptance criteria
- [ ] All beads have evidence.source
- [ ] All IDs match `gt-[a-z0-9]{5}` pattern

### Convoys
- [ ] At least 1 convoy created
- [ ] All convoys have 3-7 beads
- [ ] All referenced beads exist

## Example

```bash
/lisa:structure
```

After running, list beads with: `ls .gt/beads/`

## Migration Note

This command replaces the deprecated `/lisa:beads` and `/lisa:convoy` commands, combining both steps into a single coherent operation.
