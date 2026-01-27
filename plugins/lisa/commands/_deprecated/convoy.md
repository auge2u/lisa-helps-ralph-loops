> **DEPRECATION WARNING**
> This command is deprecated and will be removed in v0.4.0.
> Use `/lisa:structure` instead (combines beads + convoy).

---
description: "[DEPRECATED] Bundle Beads into Convoys for Gastown assignment."
skill: structure
agent: migrator
deprecated: true
replacement: "/lisa:structure"
---

# Convoy (DEPRECATED)

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

Bundle existing Beads into Convoys for efficient Gastown assignment.

### Prerequisites

Run `/lisa:beads` first to generate beads in `.gt/beads/`.

### What This Does

1. **Reads existing beads** - Loads all `.gt/beads/*.json`
2. **Analyzes relationships** - Groups by epic, dependencies, skill
3. **Creates bundles** - 3-7 beads per convoy (optimal size)
4. **Generates convoys** - Outputs to `.gt/convoys/`

### Output

Creates `.gt/convoys/convoy-*.json` files with:
- Sequential ID (convoy-001, convoy-002, etc.)
- Descriptive name and purpose
- List of 3-7 bead IDs
- Status (pending by default)
