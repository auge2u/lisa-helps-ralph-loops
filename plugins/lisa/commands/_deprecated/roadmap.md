> **DEPRECATION WARNING**
> This command is deprecated and will be removed in v0.4.0.
> Use `/lisa:plan` instead.

---
description: "[DEPRECATED] Generate a full scope roadmap."
skill: plan
agent: migrator
deprecated: true
replacement: "/lisa:plan"
---

# Roadmap (DEPRECATED)

**This command has been renamed to `/lisa:plan` in v0.3.0.**

The functionality is identical - only the name has changed to better reflect the staged architecture (research -> discover -> plan -> structure).

## Migration

Replace:
```bash
/lisa:roadmap
```

With:
```bash
/lisa:plan
```

## Original Documentation

Execute the **roadmap-scopecraft** skill to generate a complete product roadmap.

### Execution

1. Follow all instructions in `skills/plan/SKILL.md`
2. Use templates from `skills/plan/templates/`
3. Output all files to `./scopecraft/`

### Style Constraints

- Be explicit, practical, and senior-engineer-friendly
- Optimize for outcomes (PMF) and delivery feasibility
- Keep roadmap to 3-5 phases max

### Output

Creates 6 files in `./scopecraft/`:
1. VISION_AND_STAGE_DEFINITION.md
2. ROADMAP.md
3. EPICS_AND_STORIES.md
4. RISKS_AND_DEPENDENCIES.md
5. METRICS_AND_PMF.md
6. OPEN_QUESTIONS.md
