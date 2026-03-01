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

## Phase 1b: Branch Archaeology

Branches are the most reliable signal of abandoned work. Each unmerged branch is a frozen snapshot of intent.

```bash
# List all remote branches by recency (most recently touched first)
git branch -r --sort=-committerdate --format='%(committerdate:short) %(refname:short)' | head -30

# For each significant branch, measure divergence from main
git log main..origin/<branch-name> --oneline | wc -l        # commits ahead
git diff main...origin/<branch-name> --stat | tail -1       # files changed

# Get the branch's last commit message (captured intent)
git log origin/<branch-name> -1 --format="%s"

# Show all unmerged remote branches (excluding HEAD/main)
git branch -r --no-merged main | grep -v "HEAD\|main\|master"

# Full branch summary: name, date, last message
git for-each-ref --format='%(committerdate:short)|%(refname:short)|%(subject)' \
  refs/remotes/ --sort=-committerdate | grep -v HEAD | head -20
```

### Per-Branch Analysis

For each branch with >0 commits ahead of main:

| Field | How to Determine |
|-------|-----------------|
| `name` | Branch name without `origin/` prefix |
| `last_commit_date` | `%(committerdate:short)` from for-each-ref |
| `commits_ahead` | `git log main..origin/<branch> --oneline \| wc -l` |
| `description` | Last commit message on branch |
| `significance` | `high` if >5 commits; `medium` if 2–5; `low` if 1 |
| `likely_abandoned` | `true` if last commit >90 days ago |

### Output shape for open_work.branches

```json
[
  {
    "name": "feature/user-auth",
    "last_commit_date": "2024-07-14",
    "commits_ahead": 23,
    "description": "Add OAuth2 login with GitHub",
    "significance": "high",
    "likely_abandoned": true
  },
  {
    "name": "fix/memory-leak",
    "last_commit_date": "2024-08-01",
    "commits_ahead": 3,
    "description": "Fix heap allocation in worker pool",
    "significance": "medium",
    "likely_abandoned": true
  }
]
```

Set `open_work.note` to a one-sentence summary: e.g., `"3 significant branches with 30+ uncommitted changes, largest being user-auth (23 commits)."`

## Phase 1c: Issue / PR Snapshot

Capture the backlog state at the moment of abandonment. GitHub issues and PRs are the highest-fidelity record of what the team intended to build but never finished.

### Availability Check

```bash
# Test GitHub CLI access before attempting any gh commands
gh auth status 2>/dev/null && echo "GITHUB_AVAILABLE" || echo "GITHUB_UNAVAILABLE"
```

If `gh` is unavailable or unauthenticated, set `github_available: false` in both `open_work` and `backlog_at_abandonment` and skip to Phase 2. Do not treat missing GitHub access as an error.

### Open Issues (Backlog at Abandonment)

```bash
# Capture open issues at time of abandonment
gh issue list --state open --limit 100 \
  --json number,title,createdAt,labels,assignees \
  --jq '.[] | {number, title, createdAt, labels: [.labels[].name]}'
```

### Open and Abandoned PRs

```bash
# Open PRs (work in flight)
gh pr list --state open --limit 50 \
  --json number,title,createdAt,headRefName \
  --jq '.[] | {number, title, createdAt, branch: .headRefName}'

# Abandoned PRs = closed without merge
gh pr list --state closed --limit 100 \
  --json number,title,closedAt,mergedAt,headRefName \
  --jq '[.[] | select(.mergedAt == null)] | .[] | {number, title, closedAt, branch: .headRefName}'
```

### Output shape for backlog_at_abandonment

```json
{
  "open_issues": [
    {"number": 42, "title": "Support SSO login", "created_at": "2024-05-01"},
    {"number": 67, "title": "Rate limiting for API", "created_at": "2024-07-03"}
  ],
  "open_prs": [
    {"number": 88, "title": "Add retry logic", "branch": "feature/retry", "created_at": "2024-08-10"}
  ],
  "abandoned_prs": [
    {"number": 71, "title": "Refactor DB layer", "branch": "refactor/db", "closed_at": "2024-06-20"}
  ],
  "total_open_issues": 14,
  "total_open_prs": 1,
  "total_abandoned_prs": 8,
  "github_available": true
}
```

Feed open issues and abandoned PRs directly into the drift analysis (Phase 4) as evidence of scope creep. Feed open PRs into `open_work.branches` cross-reference.

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
    "dormant_days": 157,
    "key_milestones": [
      {"date": "2024-01-15", "event": "Project created", "commit": "abc1234", "significance": "high"},
      {"date": "2024-03-01", "event": "v1.0 released", "tag": "v1.0.0", "significance": "high"},
      {"date": "2024-06-15", "event": "Last feature commit", "significance": "medium"}
    ]
  },
  "open_work": {
    "branches": [
      {
        "name": "feature/user-auth",
        "last_commit_date": "2024-07-14",
        "commits_ahead": 23,
        "description": "Add OAuth2 login with GitHub",
        "significance": "high",
        "likely_abandoned": true
      }
    ],
    "total_branches": 3,
    "note": "3 unmerged branches with 30+ uncommitted changes; largest is user-auth (23 commits).",
    "github_available": true
  },
  "backlog_at_abandonment": {
    "open_issues": [
      {"number": 42, "title": "Support SSO login", "created_at": "2024-05-01"},
      {"number": 67, "title": "Rate limiting for API", "created_at": "2024-07-03"}
    ],
    "open_prs": [
      {"number": 88, "title": "Add retry logic", "branch": "feature/retry", "created_at": "2024-08-10"}
    ],
    "abandoned_prs": [
      {"number": 71, "title": "Refactor DB layer", "branch": "refactor/db", "closed_at": "2024-06-20"}
    ],
    "total_open_issues": 14,
    "total_open_prs": 1,
    "total_abandoned_prs": 8,
    "github_available": true
  },
  "drift": {
    "factors": ["scope_creep", "team_departure"],
    "severity": "moderate",
    "analysis": "Project expanded beyond MVP scope without closing core features; 14 open issues and 3 unmerged branches confirm unfinished work"
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
      "Triage 14 open issues — close stale, promote top 5 to beads",
      "Evaluate feature/user-auth branch (23 commits) for merge or discard",
      "Revise README to reflect current state"
    ]
  },
  "evidence": {
    "files_analyzed": ["README.md", "package.json", "CHANGELOG.md", ".github/"],
    "commits_reviewed": 147,
    "branches_analyzed": 5,
    "issues_reviewed": 22,
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

**Note:** `evidence.branches_analyzed` and `evidence.issues_reviewed` are informational — they track depth of investigation but are not gated. Set `branches_analyzed` to the count of branches examined (including merged); set `issues_reviewed` to 0 if GitHub was unavailable.

## Validation

```bash
python plugins/lisa/hooks/validate.py --stage research
```

## Next Steps

After research completes:
- **REVIVE**: Proceed to Stage 1 (Discover) → `skills/discover/SKILL.md`
- **PIVOT**: Proceed to Stage 1 with adjusted scope
- **ARCHIVE**: Stop pipeline, document archival decision
