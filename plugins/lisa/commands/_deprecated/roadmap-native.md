> **DEPRECATION WARNING**
> This command is deprecated and will be removed in v0.4.0.
> Use `/lisa:plan` instead. Native loop orchestration is being simplified.

---
description: "[DEPRECATED] Generate a roadmap using native Claude Code orchestration."
skill: plan
agent: migrator
deprecated: true
replacement: "/lisa:plan"
---

# Roadmap Native (DEPRECATED)

**This command is deprecated in v0.3.0.**

The native orchestration loop has been simplified. Use `/lisa:plan` for one-shot roadmap generation.

## Migration

Replace:
```bash
/lisa:roadmap-native
```

With:
```bash
/lisa:plan
```

For iterative refinement, run `/lisa:plan` multiple times and use `/lisa:status` to check quality gates.

## Original Documentation

Execute the **roadmap-scopecraft** skill using native orchestration with memory persistence.

### Features

- **Zero dependencies** - No Python packages or external tools required
- **Built-in loop control** - Iterates until quality gates pass (max 15 iterations)
- **Memory persistence** - Semantic, episodic, and procedural memory
- **Native validation** - Uses hooks for gate checks
- **Scratchpad memory** - Cross-iteration context

### Quality Gates

All must pass before completion:

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 `.md` files in scopecraft/ |
| `phases_in_range` | 3-5 `## Phase` headers in ROADMAP.md |
| `stories_have_acceptance_criteria` | 5+ "Acceptance Criteria" sections |
| `risks_documented` | 3+ risk table rows |
| `metrics_defined` | "North Star Metric" section exists |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers |
