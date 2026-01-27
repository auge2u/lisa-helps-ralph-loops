> **DEPRECATION WARNING**
> This command is deprecated and will be removed in v0.4.0.
> Use `/lisa:plan` instead. External orchestrator mode is being phased out.

---
description: "[DEPRECATED] Run ScopeCraft in an iterative loop until LOOP_COMPLETE."
skill: plan
agent: migrator
deprecated: true
replacement: "/lisa:plan"
---

# Roadmap Orchestrated (DEPRECATED)

**This command is deprecated in v0.3.0.**

External orchestrator compatibility (ralph-orchestrator) is being phased out in favor of simpler iterative workflows.

## Migration

Replace:
```bash
/lisa:roadmap-orchestrated
```

With:
```bash
/lisa:plan
```

For iterative refinement:
1. Run `/lisa:plan`
2. Check gates with `/lisa:status`
3. Fix issues and re-run `/lisa:plan`
4. Repeat until all gates pass

## Original Documentation

Execute the **roadmap-scopecraft** skill in iterative mode, compatible with ralph-orchestrator.

### Scratchpad Protocol

Before each iteration, read `.agent/scratchpad.md` to understand:
- Progress from previous iterations
- Quality gate status from last check
- Decisions made and context
- Current blockers
- Remaining work items

### Quality Gates (MUST PASS)

| Gate | Check | Requirement |
|------|-------|-------------|
| all_outputs_exist | File count | 6 files in scopecraft/ |
| phases_in_range | Pattern count | 3-5 `## Phase` headers |
| stories_have_acceptance_criteria | Pattern count | 5+ "Acceptance Criteria" |
| risks_documented | Pattern count | 3+ risk table rows |
| metrics_defined | Pattern exists | "North Star Metric" section |
| no_todo_placeholders | Pattern count | 0 `[TODO]`/`[TBD]`/`[PLACEHOLDER]` |

### Completion Promise

When ALL quality gates pass, print exactly: `LOOP_COMPLETE`
