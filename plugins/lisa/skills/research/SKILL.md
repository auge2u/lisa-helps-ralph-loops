---
name: research
description: Archaeological rescue skill for abandoned projects. Reconstructs lost context through git archaeology, timeline analysis, and mission extraction.
stage: 0
---

# Research Skill (Stage 0)

This skill performs archaeological rescue to reconstruct lost context from abandoned software projects.

## When to Use

Use this skill when:
- Project has been abandoned for 6+ months
- Original developers are unavailable
- Documentation is severely outdated
- "Why was this built?" is unclear
- Need to determine if project should be revived, pivoted, or archived

## Output Structure

```
project/
├── .gt/
│   └── research/
│       ├── timeline.json      # Project evolution timeline
│       └── rescue.json        # Analysis and recommendation
└── [existing project files]
```

## Phase 1: Git Archaeology

### Commit History Analysis

```bash
# View first commits (original vision)
git log --reverse --format="%h %ad %s" --date=short | head -20

# Identify contributors
git shortlog -sn --all

# Find activity patterns
git log --format="%ad" --date=format:"%Y-%m" | sort | uniq -c

# Locate milestones
git tag -l --sort=-creatordate | head -10
```

### Key Questions to Answer

1. **When did work start?** - First commit date
2. **Who contributed?** - Contributor list and commit counts
3. **When did work stop?** - Last commit date
4. **What were the milestones?** - Tags, releases, major commits

## Phase 2: Timeline Construction

Build a timeline from git history:

### Output: timeline.json

```json
{
  "$schema": "timeline-v1",
  "project": {
    "inception": "2024-01-15",
    "last_active": "2024-08-22",
    "dormant_since": "2024-08-22"
  },
  "milestones": [
    {
      "date": "2024-01-15",
      "event": "Project created",
      "commit": "abc1234",
      "significance": "high"
    },
    {
      "date": "2024-03-01",
      "event": "v1.0 released",
      "tag": "v1.0.0",
      "significance": "high"
    }
  ],
  "activity_phases": [
    {
      "period": "2024-01 to 2024-03",
      "level": "high",
      "description": "Initial development sprint"
    },
    {
      "period": "2024-04 to 2024-06",
      "level": "medium",
      "description": "Feature expansion"
    },
    {
      "period": "2024-07 to 2024-08",
      "level": "low",
      "description": "Maintenance only"
    }
  ],
  "contributors": [
    {
      "name": "Developer A",
      "commits": 147,
      "first_commit": "2024-01-15",
      "last_commit": "2024-06-30"
    }
  ]
}
```

## Phase 3: Mission Extraction

### Sources to Analyze

1. **First README version**
   ```bash
   git show $(git rev-list --max-parents=0 HEAD):README.md
   ```

2. **Package description**
   - `package.json` description field
   - `pyproject.toml` description
   - `Cargo.toml` description

3. **Early commit messages**
   ```bash
   git log --reverse --oneline | head -20
   ```

4. **Initial issues/PRs** (if GitHub)
   ```bash
   gh issue list --state all --limit 20 --json number,title,createdAt
   ```

### Mission Statement Format

Extract or infer a mission statement:

```
[Project] helps [target user] to [core action] by [key mechanism].
```

Example: "TaskFlow helps remote teams to track work progress by providing real-time collaborative task boards."

## Phase 4: Drift Analysis

### Drift Factors to Identify

| Factor | Detection Method |
|--------|------------------|
| Scope creep | Unmerged feature branches, expanding deps |
| Technical debt | Increasing fix/feature commit ratio |
| Team changes | Contributor dropout patterns |
| Pivot attempt | Major directory restructuring |
| Dependency rot | Outdated deps, security vulnerabilities |
| Interest waning | Declining commit frequency |

### Drift Severity Assessment

| Severity | Indicators |
|----------|------------|
| Low | Minor scope expansion, team stable |
| Moderate | Significant feature creep, some tech debt |
| High | Major pivot, team departed, severe debt |
| Critical | Abandoned mid-feature, security issues |

## Phase 5: Health Assessment

### Areas to Evaluate

1. **Tests**
   - Do tests exist?
   - Do they pass?
   - What's coverage like?

2. **Dependencies**
   - Are deps up-to-date?
   - Any security vulnerabilities?
   - Any deprecated packages?

3. **Documentation**
   - Does README reflect current state?
   - Are setup instructions valid?
   - Is architecture documented?

4. **Architecture**
   - Clear directory structure?
   - Consistent patterns?
   - Reasonable complexity?

## Phase 6: Rescue Recommendation

### Decision Framework

```
Is the original mission still relevant to users today?
├── No → Is the codebase valuable for a different purpose?
│   ├── No → ARCHIVE
│   └── Yes → PIVOT
└── Yes → Is revival feasible?
    ├── No (too much debt, dead deps) → ARCHIVE
    └── Yes → REVIVE
```

### Recommendation Actions

| Action | When to Recommend | Prerequisites |
|--------|-------------------|---------------|
| **REVIVE** | Mission valid, debt manageable | Update deps, close stale branches |
| **PIVOT** | Good foundation, new direction needed | Define new mission first |
| **ARCHIVE** | Too much debt or obsolete | Document learnings |

### Output: rescue.json

```json
{
  "$schema": "rescue-v1",
  "mission": {
    "statement": "A task management app for distributed teams",
    "confidence": "high",
    "source": "README.md (initial commit)"
  },
  "timeline": {
    "inception": "2024-01-15",
    "last_active": "2024-08-22",
    "dormant_days": 157
  },
  "drift": {
    "factors": ["scope_creep", "team_departure"],
    "severity": "moderate",
    "analysis": "Project expanded beyond MVP scope without closing core features"
  },
  "health": {
    "tests": "partial",
    "dependencies": "outdated",
    "documentation": "stale",
    "architecture": "reasonable"
  },
  "recommendation": {
    "action": "revive",
    "confidence": "medium",
    "rationale": "Core value proposition remains valid, technical debt is manageable",
    "prerequisites": [
      "Update dependencies to address 3 high-severity vulnerabilities",
      "Close or archive 5 abandoned feature branches",
      "Revise README to reflect current state"
    ]
  },
  "evidence": {
    "files_analyzed": ["README.md", "package.json", "CHANGELOG.md", ".github/"],
    "commits_reviewed": 147,
    "analysis_date": "2026-01-27T10:00:00Z"
  }
}
```

## Quality Gates

| Gate | Requirement |
|------|-------------|
| `timeline_constructed` | timeline.json exists with valid structure |
| `mission_clarified` | mission.statement is populated |
| `drift_analyzed` | drift.factors has at least 1 factor |
| `recommendation_made` | recommendation.action is revive/pivot/archive |
| `evidence_gathered` | evidence.files_analyzed has 3+ entries |

## Validation

```bash
python plugins/lisa/hooks/validate.py --stage research
```

## Next Steps

After research completes:
- **REVIVE**: Proceed to Stage 1 (Discover) → `skills/discover/SKILL.md`
- **PIVOT**: Proceed to Stage 1 with adjusted scope
- **ARCHIVE**: Stop pipeline, document archival decision
