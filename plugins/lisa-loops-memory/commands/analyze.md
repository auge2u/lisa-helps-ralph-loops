---
description: Analyze project and generate Gastown semantic memory. Scans codebase, docs, and configs to understand tech stack, constraints, and goals.
skill: gastown-migration
agent: gastown-migrator
---

# Analyze — lisa-loops-memory

Scan the current project and generate Gastown-compatible semantic memory.

## What This Does

1. **Scans package files** — Detects runtime, framework, dependencies
2. **Reads configuration** — Identifies database, auth, deployment targets
3. **Analyzes documentation** — Extracts constraints, personas, non-goals
4. **Generates memory** — Outputs `.gt/memory/semantic.json`

## Execution

1. Follow the "Phase 1: Analyze" section in `skills/gastown-migration/SKILL.md`
2. Create `.gt/memory/` directory if it doesn't exist
3. Write `semantic.json` with discovered facts
4. Record all analyzed files in `evidence.files_analyzed`

## Output

Creates/updates `.gt/memory/semantic.json` with:
- Project identity (name, type, language)
- Tech stack (runtime, framework, database, auth, etc.)
- User personas if documented
- Constraints and non-goals
- Evidence of what was analyzed

## Quality Gates

- [ ] `semantic.json` is valid JSON
- [ ] `project.name` is populated
- [ ] At least 2 `tech_stack` fields are populated
- [ ] `evidence.files_analyzed` has at least 1 entry

## Example

```bash
/lisa-loops-memory:analyze
```

After running, check `.gt/memory/semantic.json` for results.
