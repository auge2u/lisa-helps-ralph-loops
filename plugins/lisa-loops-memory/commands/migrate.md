---
description: Full Gastown migration - analyze project, extract beads, create convoys. One command to structure any project for Gastown.
skill: gastown-migration
agent: gastown-migrator
---

# Migrate — lisa-loops-memory

Complete Gastown migration in one command. Runs analyze, beads, and convoy phases sequentially.

## What This Does

1. **Phase 1: Analyze** — Generate semantic memory from project scan
2. **Phase 2: Beads** — Extract work items from all sources
3. **Phase 3: Convoy** — Bundle beads into work packages

## Execution

1. Follow all phases in `skills/gastown-migration/SKILL.md`
2. Create complete `.gt/` directory structure
3. Validate each phase before proceeding
4. Signal `MIGRATION_COMPLETE` when all gates pass

## Output Structure

```
.gt/
├── memory/
│   ├── semantic.json    # Project facts (Phase 1)
│   ├── episodic.json    # Decisions (optional)
│   └── procedural.json  # Patterns (optional)
├── beads/
│   ├── gt-abc12.json    # Work items (Phase 2)
│   └── ...
└── convoys/
    ├── convoy-001.json  # Work bundles (Phase 3)
    └── ...
```

## Quality Gates (All Must Pass)

### Phase 1: Analyze
- [ ] `semantic.json` is valid JSON
- [ ] `project.name` is populated
- [ ] At least 2 `tech_stack` fields populated

### Phase 2: Beads
- [ ] At least 3 beads extracted
- [ ] All beads have acceptance criteria
- [ ] All beads have evidence

### Phase 3: Convoy
- [ ] At least 1 convoy created
- [ ] All convoys have 3-7 beads
- [ ] All referenced beads exist

## Completion Signal

Issue `MIGRATION_COMPLETE` only after:
1. All three phases complete successfully
2. All quality gates pass
3. `.gt/` directory structure is valid

## Example

```bash
/lisa-loops-memory:migrate
```

This is equivalent to running:
```bash
/lisa-loops-memory:analyze
/lisa-loops-memory:beads
/lisa-loops-memory:convoy
```

## After Migration

Gastown Mayor can now:
1. Read `.gt/memory/semantic.json` for project context
2. Enumerate `.gt/beads/*.json` for available work
3. Assign `.gt/convoys/*.json` to Polecats
