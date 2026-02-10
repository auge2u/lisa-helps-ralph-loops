# Metrics and PMF

## North Star Metric
**Metric:** External users who complete at least one pipeline stage (discover, plan, or structure)
**Target:** 10 users by end of Phase 5
**Why:** Proves Lisa delivers standalone value -- a user who completes a stage has extracted meaningful structure from their project. This is the minimum signal that Lisa is useful beyond its creator.

### Long-term North Star (Phase 6)
**Metric:** Successful end-to-end ecosystem runs (Lisa structure -> Conductor assign -> Agent complete -> Carlos validate)
**Target:** 1 successful run by end of Phase 6
**Why:** Proves the three-plugin architecture delivers value beyond what any single plugin provides alone.

## Supporting Metrics

| Metric | Current | Phase 4 Target | Phase 5 Target | Phase 6 Target | Rationale |
|--------|---------|----------------|----------------|----------------|-----------|
| Marketplace installs | 0 | 50+ | 100+ | 200+ | Adoption signal |
| External stage completions | 0 | 5+ | 10+ | 50+ | Usage depth |
| Pipeline success rate (diverse repos) | unknown | measured | 90%+ | 95%+ | Reliability |
| Semantic.json files populated (ecosystem) | 3/3 | 3/3 | 3/3 | 3/3 | Foundation |
| Reconcile checkpoint valid | Yes (v4.0.0) | Yes | Yes | Yes | Ecosystem memory |
| Quality gate duplication | 0 | 0 | 0 | 0 | Single source of truth |
| Cost per roadmap run | ~$2 (Carlos) | ~$2 | ~$2 | <$1 | Model routing savings |
| Context rollover success | N/A | N/A | N/A | >90% | Agents survive exhaustion |
| Beads assigned via Conductor | 0 | 0 | 0 | 10+ | Conductor distributes work |

## PMF Signals

### Phase 4 (Ship) -- Awareness

| Signal | Measurement | Threshold |
|--------|-------------|-----------|
| Marketplace installs | Plugin install count | 50+ |
| GitHub stars | Repository engagement | 25+ |
| Getting started completions | Users who finish guide | 10+ |
| Issue reports | Bug reports and feature requests filed | 3+ |

### Phase 5 (Harden) -- Engagement

| Signal | Measurement | Threshold |
|--------|-------------|-----------|
| Repeat usage | Users running pipeline 2+ times | 20%+ of installers |
| Stage completion depth | Average stages completed per user | 2+ stages |
| Diverse project types | Language ecosystems with successful runs | 4+ (Python, TS, Go, Rust) |
| Community contributions | External PRs or issues | 3+ |

### Phase 6 (Ecosystem) -- Retention

| Signal | Measurement | Threshold |
|--------|-------------|-----------|
| Multi-plugin users | Users with 2+ ecosystem plugins | 20%+ of Lisa users |
| Reconcile frequency | Reconcile runs per user per month | 2+ |
| Context recovery usage | Checkpoint reads after context loss | Positive signal |
| Ecosystem referrals | Users who install Carlos/Conductor after Lisa | 10%+ |

## Instrumentation Plan

| Event | Trigger | Properties | Priority |
|-------|---------|------------|----------|
| `discover_complete` | Lisa Stage 1 finishes | project_name, tech_stack_count, duration | P0 |
| `plan_complete` | Lisa Stage 2 finishes | project_name, story_count, duration | P0 |
| `structure_complete` | Lisa Stage 3 finishes | bead_count, convoy_count, duration | P0 |
| `reconcile_complete` | `/lisa:reconcile` finishes | project_count, aligned_count, drifted_count | P0 |
| `quality_gate_result` | validate.py runs | stage, pass_count, fail_count, fallback_mode | P0 |
| `pipeline_error` | Any stage fails | stage_name, error_type, project_language | P0 |
| `standalone_mode` | Ecosystem partners absent | missing_plugins, stages_available | P1 |
| `marketplace_install` | Plugin installed | version, platform | P1 |
| `context_recovery` | Checkpoint read for context restore | checkpoint_age_hours, recovery_success | P2 |

Note: Instrumentation is local-only (no telemetry). Events logged to `.gt/` artifacts for reconcile consumption. External metrics (marketplace installs, GitHub stars) tracked via platform dashboards.
