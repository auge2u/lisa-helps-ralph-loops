> **DEPRECATION WARNING**
> This command is deprecated and will be removed in v0.4.0.
> Use `/lisa:discover` instead.

---
description: "[DEPRECATED] Analyze project and generate Gastown semantic memory."
skill: discover
agent: migrator
deprecated: true
replacement: "/lisa:discover"
---

# Analyze (DEPRECATED)

**This command has been renamed to `/lisa:discover` in v0.3.0.**

The functionality is identical - only the name has changed to better reflect the staged architecture (research -> discover -> plan -> structure).

## Migration

Replace:
```bash
/lisa:analyze
```

With:
```bash
/lisa:discover
```

## Original Documentation

Scan the current project and generate Gastown-compatible semantic memory.

### What This Does

1. **Scans package files** - Detects runtime, framework, dependencies
2. **Reads configuration** - Identifies database, auth, deployment targets
3. **Analyzes documentation** - Extracts constraints, personas, non-goals
4. **Generates memory** - Outputs `.gt/memory/semantic.json`

### Output

Creates/updates `.gt/memory/semantic.json` with:
- Project identity (name, type, language)
- Tech stack (runtime, framework, database, auth, etc.)
- User personas if documented
- Constraints and non-goals
- Evidence of what was analyzed
