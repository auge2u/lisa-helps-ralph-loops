---
description: Generate a roadmap using native Claude Code orchestration with memory persistence.
skill: roadmap-scopecraft
agent: roadmap-orchestrator
---

# Roadmap — Native Claude Code Orchestration with Memory

Execute the **roadmap-scopecraft** skill using the native **roadmap-orchestrator** agent. This mode includes memory persistence across iterations.

## Features

- **Zero dependencies** — No Python packages or external tools required
- **Built-in loop control** — Iterates until quality gates pass (max 15 iterations)
- **Memory persistence** — Semantic, episodic, and procedural memory
- **Native validation** — Uses `hooks/validate-gates-handler.sh` for gate checks
- **Scratchpad memory** — Cross-iteration context via `.agent/scratchpad.md`

## Memory Architecture

```
.agent/
├── memory/
│   ├── semantic.json      # Permanent facts (project, tech stack)
│   ├── episodic.json      # Decisions with TTL (~30 days)
│   └── procedural.json    # Learned patterns
├── scratchpad.md          # Working memory
└── validation-results.json
```

## Execution

The orchestrator will:

1. **Load Memory** — Read semantic facts, recent decisions, learned patterns
2. **Initialize** — Check for existing scratchpad context
3. **Execute** — Run roadmap-scopecraft skill, output to `./scopecraft/`
4. **Validate** — Check all 6 quality gates
5. **Store Memory** — Update facts, record decisions, observe patterns
6. **Iterate** — If gates fail, update scratchpad and repeat
7. **Complete** — Output `LOOP_COMPLETE` when all gates pass

## Quality Gates

All must pass before completion:

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 `.md` files in scopecraft/ |
| `phases_in_range` | 3-5 `## Phase` headers in ROADMAP.md |
| `stories_have_acceptance_criteria` | 5+ "Acceptance Criteria" sections |
| `risks_documented` | 3+ risk table rows |
| `metrics_defined` | "North Star Metric" section exists |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers |

## Manual Validation

```bash
# Human-readable output
./plugins/lisa-loops-memory/hooks/validate-gates-handler.sh

# JSON output (for scripts)
./plugins/lisa-loops-memory/hooks/validate-gates-handler.sh --json

# Quiet mode (exit code only)
./plugins/lisa-loops-memory/hooks/validate-gates-handler.sh --quiet
```

## Output Files

```
scopecraft/
├── VISION_AND_STAGE_DEFINITION.md
├── ROADMAP.md
├── EPICS_AND_STORIES.md
├── RISKS_AND_DEPENDENCIES.md
├── METRICS_AND_PMF.md
└── OPEN_QUESTIONS.md

.agent/
├── memory/
│   ├── semantic.json
│   ├── episodic.json
│   └── procedural.json
├── scratchpad.md
└── validation-results.json
```

## Comparison with Other Commands

| Command | Orchestration | Memory | Dependencies |
|---------|---------------|--------|--------------|
| `/roadmap` | One-shot | No | None |
| `/roadmap-native` | Native loop | Yes | None |
| `/roadmap-orchestrated` | External | Scratchpad only | ralph-orchestrator |
