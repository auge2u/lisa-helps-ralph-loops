---
description: Extract semantic memory from project analysis. Scans codebase, docs, and configs to understand tech stack, constraints, and goals.
skill: discover
agent: migrator
stage: 1
---

# Discover (Stage 1) - Lisa

Scan the current project and generate Gastown-compatible semantic memory.

## When to Use

Use this command when:
- Starting migration of an existing project
- Need to understand a codebase's tech stack
- Want to document project constraints and goals
- Preparing for roadmap generation

## What This Does

1. **Scans package files** - Detects runtime, framework, dependencies
2. **Reads configuration** - Identifies database, auth, deployment targets
3. **Analyzes documentation** - Extracts constraints, personas, non-goals
4. **Generates memory** - Outputs `.gt/memory/semantic.json`

## Execution

1. Follow the instructions in `skills/discover/SKILL.md`
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
/lisa:discover
```

After running, check `.gt/memory/semantic.json` for results.

## Migration Note

This command replaces the deprecated `/lisa:analyze` command. The functionality is identical, but the naming better reflects the staged architecture.
