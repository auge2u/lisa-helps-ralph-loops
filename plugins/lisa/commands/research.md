---
description: Archaeological rescue for lost projects. Reconstructs context from abandoned codebases, dead documentation, and git archaeology.
skill: research
agent: archaeologist
stage: 0
---

# Research (Stage 0) - Lisa

Perform archaeological rescue to reconstruct lost project context.

## When to Use

Use this command when:
- Project has been abandoned for 6+ months
- Original developers are unavailable
- Documentation is outdated or missing
- "Why was this built?" is unclear
- Scope drift has obscured original mission

## What This Does

1. **Git archaeology** - Analyze commit history, contributors, activity patterns
2. **Timeline reconstruction** - Build project evolution timeline
3. **Mission extraction** - Infer original goals from early commits and docs
4. **Drift analysis** - Identify where project diverged from original vision
5. **Rescue recommendation** - Propose path forward (revive, archive, or pivot)

## Execution

1. Follow the instructions in `skills/research/SKILL.md`
2. Create `.gt/research/` directory if it doesn't exist
3. Generate `timeline.json` with project history
4. Generate `rescue.json` with analysis and recommendations
5. Record all evidence in `evidence.files_analyzed`

## Output

Creates `.gt/research/` with:
- `timeline.json` - Project evolution timeline
- `rescue.json` - Mission analysis and recommendation

## Quality Gates

- [ ] `timeline.json` exists with valid structure
- [ ] `mission.statement` is populated
- [ ] `recommendation.action` is one of: revive, archive, pivot
- [ ] Evidence includes 3+ analyzed files

## Example

```bash
/lisa:research
```

After running, review `.gt/research/rescue.json` for recommendations.
