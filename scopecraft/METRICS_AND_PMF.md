# Metrics and PMF

## North Star Metric
**Metric:** Successful end-to-end ecosystem runs (Lisa structure -> Conductor assign -> Agent complete -> Carlos validate)
**Target:** 1 successful run by end of Phase 6
**Why:** Proves the three-plugin architecture delivers value beyond what any single plugin provides alone.

### Interim North Star (Phase 4-5)
**Metric:** External users who complete at least one pipeline stage
**Target:** 10 users by end of Phase 5
**Why:** Validates that Lisa is useful standalone before measuring ecosystem integration.

## Supporting Metrics

| Metric | Current | Phase 4 Target | Phase 6 Target | Rationale |
|--------|---------|----------------|----------------|-----------|
| Plugins with populated semantic.json | 3/3 | 3/3 | 3/3 | Foundation for reconcile |
| Reconcile produces valid checkpoint | Yes (v4.0.0) | Yes | Yes | Ecosystem memory exists |
| Marketplace installs | 0 | 50+ | 200+ | Adoption |
| External users completing pipeline stage | 0 | 10+ | 50+ | Usage depth |
| Pipeline success rate on diverse repos | ~80% (estimated) | 90%+ | 95%+ | Reliability |
| Quality gate definition duplication | 0 | 0 | 0 | Single source of truth |
| Cost per roadmap run | ~$2 (Carlos solo) | ~$2 | <$1 | Model routing reduces costs |
| Context rollover success rate | N/A | N/A | >90% | CLI agents survive exhaustion |
| Beads assigned via Conductor | 0 | 0 | 10+ | Conductor distributes work |

## PMF Signals

### Phase 4 (Publish) — Awareness

| Signal | Measurement | Threshold |
|--------|-------------|-----------|
| Marketplace installs | Plugin installs | 50+ |
| GitHub stars | Repository engagement | 50+ |
| Documentation completions | Users who finish getting started | 10+ |

### Phase 5 (Standalone) — Engagement

| Signal | Measurement | Threshold |
|--------|-------------|-----------|
| Repeat usage | Users running pipeline 2+ times | 20%+ |
| Stage completion depth | Average stages completed per user | 2+ |
| Issue reports | Bug reports and feature requests | 5+ |

### Phase 6 (Ecosystem) — Retention

| Signal | Measurement | Threshold |
|--------|-------------|-----------|
| Multi-plugin users | Users with 2+ ecosystem plugins | 20%+ of Lisa users |
| Reconcile frequency | Reconcile runs per user per month | 2+ |
| Context recovery usage | Checkpoint reads after context loss | Positive signal |

## Instrumentation Plan

| Event | Trigger | Properties | Priority |
|-------|---------|------------|----------|
| `discover_complete` | Lisa Stage 1 finishes | project_name, tech_stack_count, duration | P0 |
| `reconcile_complete` | `/lisa:reconcile` finishes | project_count, aligned_count, drifted_count | P0 |
| `pipeline_stage_complete` | Any stage finishes | stage_name, project_name, duration | P0 |
| `quality_gate_result` | validate.py runs | stage, pass_count, fail_count | P0 |
| `marketplace_install` | Plugin installed | version, platform | P1 |
| `standalone_mode` | Ecosystem partners absent | missing_plugins | P1 |
| `context_recovery` | Checkpoint read | checkpoint_age, recovery_success | P2 |

Note: Instrumentation is local-only (no telemetry). Events logged to `.gt/` artifacts for reconcile consumption.
