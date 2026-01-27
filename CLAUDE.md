# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lisa-helps-ralph-loops** extends the Ralph Loop pattern with **memory persistence** for multi-agent autonomous coding workflows. It transforms stateless iterations into cumulative, learning systems.

**Current version:** 0.1.0 (see `.claude-plugin/marketplace.json`)

**Forked from:** [ralph-it-up v1.2.0](https://github.com/auge2u/ralph-it-up)

**Inspired by:** [multi-agent-ralph-loop](https://github.com/alfredolopez80/multi-agent-ralph-loop)

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace registry (version, plugins list)
plugins/
  lisa-loops-memory/
    .claude-plugin/plugin.json     # Plugin manifest (name, version, license)
    commands/
      roadmap.md                   # One-shot slash command
      roadmap-native.md            # Native Claude Code loop with memory
      roadmap-orchestrated.md      # Loop mode (ralph-orchestrator compatible)
    agents/
      product-owner.md             # Agent persona for one-shot mode
      roadmap-orchestrator.md      # Native loop orchestrator agent
    skills/
      roadmap-scopecraft/
        SKILL.md                   # Core skill logic, quality gates, discovery
        templates/                 # Output format templates
    templates/                     # ralph-orchestrator v2 templates
    hooks/
      validate_quality_gates.py    # Quality gate validation (Python 3)
      validate-gates-handler.sh    # Native bash validation
    examples/
      scopecraft/                  # Sample outputs for reference
```

## Memory Architecture

The core differentiator from ralph-it-up is the **three-tier memory system**:

```
.agent/
├── memory/
│   ├── semantic.json      # Permanent facts (project, tech stack, personas)
│   ├── episodic.json      # Decisions with timestamps and expiry (~30 days)
│   └── procedural.json    # Learned patterns and heuristics
├── scratchpad.md          # Cross-iteration working memory
└── validation-results.json
```

### Semantic Memory (Facts)

Permanent knowledge about the project that persists forever:
- Project identity (name, type, language)
- Tech stack (database, auth, deployment)
- User personas and priorities
- Architectural constraints

### Episodic Memory (Decisions)

Decisions and rationale with timestamps and expiry:
- What was decided
- Why it was decided (rationale)
- Context (session, iteration)
- Expiry date (~30 days default)

### Procedural Memory (Patterns)

Learned heuristics that evolve over time:
- Complexity patterns (e.g., "auth stories are L/XL")
- Success patterns (e.g., "stories with acceptance criteria ship faster")
- Failure patterns (e.g., "dependencies on X team often block")

## Commands

Users invoke plugins via:
- `/lisa-loops-memory:roadmap` — One-shot roadmap generation
- `/lisa-loops-memory:roadmap-native` — Native Claude Code loop with memory
- `/lisa-loops-memory:roadmap-orchestrated` — External orchestrator mode

## Quality Gates

Inherited from ralph-it-up, must pass before `LOOP_COMPLETE`:

| Gate | Requirement |
|------|-------------|
| `all_outputs_exist` | 6 `.md` files in scopecraft/ |
| `phases_in_range` | 3-5 `## Phase \d` headers in ROADMAP.md |
| `stories_have_acceptance_criteria` | 5+ "Acceptance Criteria" sections |
| `risks_documented` | 3+ risk table rows with Technical/Product/GTM types |
| `metrics_defined` | "North Star Metric" section exists |
| `no_todo_placeholders` | Zero `[TODO]`/`[TBD]`/`[PLACEHOLDER]` markers |

### Validation

```bash
# Native bash validator
./plugins/lisa-loops-memory/hooks/validate-gates-handler.sh

# JSON output
./plugins/lisa-loops-memory/hooks/validate-gates-handler.sh --json

# Python validator
python plugins/lisa-loops-memory/hooks/validate_quality_gates.py
```

## How Memory Enhances the Loop

### Without Memory (ralph-it-up)

```
Iteration 1 → Discover project → Generate roadmap
Iteration 2 → Discover project (again) → Generate roadmap
Iteration 3 → Discover project (again) → Generate roadmap
```

### With Memory (lisa-helps-ralph-loops)

```
Iteration 1 → Discover project → Store facts → Generate roadmap → Store decisions
Iteration 2 → Load facts + decisions → Refine roadmap → Update decisions
Iteration 3 → Load facts + decisions → Learn patterns → Finalize roadmap
```

## Memory Protocol

### On Iteration Start

1. Load `.agent/memory/semantic.json` for project facts
2. Load `.agent/memory/episodic.json` for recent decisions (filter expired)
3. Load `.agent/memory/procedural.json` for learned patterns
4. Read `.agent/scratchpad.md` for working context

### On Iteration End

1. Extract new facts → Update `semantic.json`
2. Record decisions made → Append to `episodic.json`
3. Observe patterns → Update confidence in `procedural.json`
4. Update scratchpad with progress

## Roadmap

- [x] Fork from ralph-it-up v1.2.0
- [ ] Implement semantic memory store
- [ ] Implement episodic memory with TTL
- [ ] Implement procedural memory learning
- [ ] Add memory-aware agents
- [ ] Multi-model consensus (future)

## Quality Standards

- Memory files must be valid JSON
- Semantic facts require evidence (file paths, commit SHAs)
- Episodic decisions require rationale
- Procedural patterns require confidence scores
- Quality gates must pass before `LOOP_COMPLETE`
- Scratchpad must track memory state between iterations
