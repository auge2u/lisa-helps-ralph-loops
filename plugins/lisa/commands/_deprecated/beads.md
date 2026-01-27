> **DEPRECATION WARNING**
> This command is deprecated and will be removed in v0.4.0.
> Use `/lisa:structure` instead (combines beads + convoy).

---
description: "[DEPRECATED] Extract work items from project as Gastown Beads."
skill: structure
agent: migrator
deprecated: true
replacement: "/lisa:structure"
---

# Beads (DEPRECATED)

**This command has been merged into `/lisa:structure` in v0.3.0.**

The new `structure` command combines both bead extraction and convoy bundling into a single coherent operation.

## Migration

Replace:
```bash
/lisa:beads
/lisa:convoy
```

With:
```bash
/lisa:structure
```

## Original Documentation

Extract work items from the project and structure them as Gastown Beads.

### What This Does

1. **Scans TODO comments** - Finds `TODO:`, `FIXME:`, `HACK:` in code
2. **Reads GitHub issues** - Imports open issues (if git repo)
3. **Parses PRD documents** - Extracts user stories with criteria
4. **Checks existing roadmaps** - Imports from `scopecraft/` if present
5. **Generates beads** - Outputs to `.gt/beads/`

### Output

Creates `.gt/beads/gt-*.json` files with:
- Unique ID in Gastown format
- Clear title and type (feature/bug/chore/docs/spike)
- Acceptance criteria (at least 2)
- Complexity estimate (XS/S/M/L/XL)
- Evidence linking to source
