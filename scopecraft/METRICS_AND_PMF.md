# Metrics and PMF

## North Star Metric
**Metric:** Successful end-to-end ecosystem runs (Lisa structure -> Conductor assign -> Agent complete -> Carlos validate)
**Target:** 1 successful run by end of Phase 3
**Why:** Proves the three-plugin architecture delivers value beyond what any single plugin provides alone.

## Supporting Metrics

| Metric | Current | Target | Rationale |
|--------|---------|--------|-----------|
| Plugins with populated semantic.json | 1/3 (Carlos) | 3/3 | Foundation for reconcile |
| Reconcile produces valid checkpoint | 0 | 1 | Ecosystem memory exists |
| Carlos skip-discovery rate (on Lisa projects) | 0% | >80% | Integration eliminates redundant work |
| Quality gate definition duplication | ~6 duplicated | 0 | Single source of truth in gates.yaml |
| Cost per roadmap run | ~$2 (Carlos solo) | <$1 | Model routing reduces costs |
| Context rollover success rate | N/A | >90% | CLI agents survive context exhaustion |
| Beads assigned via Conductor | 0 | 10+ | Conductor can distribute work |

## PMF Signals

### Activation Funnel
1. Install any one plugin -> 100% (standalone works)
2. Install second plugin -> detect ecosystem benefits -> TBD%
3. Run reconcile across projects -> get alignment report -> TBD%
4. Use ecosystem for multi-agent work -> sustained usage -> TBD%

### Retention
- **Per-session:** Plugin used at least once per development session
- **Per-version:** Reconcile run on every version ship
- **Per-break:** Context recovery via checkpoint after >7 day gap

### Usage Depth
- Number of stages completed per project (research through structure)
- Number of beads created and assigned
- Frequency of reconcile runs
- Cost savings from model routing

## Instrumentation Plan

| Event | Trigger | Properties | Priority |
|-------|---------|------------|----------|
| `discover_complete` | Lisa Stage 1 finishes | project_name, tech_stack_count, duration | P0 |
| `reconcile_complete` | `/lisa:reconcile` finishes | project_count, aligned_count, drifted_count | P0 |
| `carlos_skip_discovery` | Carlos uses existing semantic.json | semantic_json_age_hours, project_name | P1 |
| `conductor_assign_bead` | Conductor assigns work | bead_id, agent_type, model_tier | P1 |
| `context_rollover` | Conductor detects exhaustion | agent_id, checkpoint_size, resume_success | P1 |
| `quality_gate_result` | Carlos/Lisa validates output | stage, pass_count, fail_count, duration | P0 |
| `model_route_decision` | Model router selects tier | task_type, selected_tier, estimated_cost | P2 |

Note: Instrumentation is local-only (no telemetry). Events are logged to `.gt/` artifacts for reconcile consumption.
