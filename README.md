# Lisa

**Give Claude Code a memory before it touches your code.**

Lisa is a Claude Code plugin that reads your project before acting on it — extracting tech stack, constraints, prior decisions, and open work into structured files that every future Claude session can instantly use. No more re-explaining what the project is. No more "wait, why was this built this way?" No more lost context.

---

## The best way to try it

You know that project you started six months ago and never quite finished? The one with the half-written README, the TODOs in the code, the Slack thread where you worked out the architecture? Open it in Claude Code and run:

```
/lisa:rescue
```

Lisa will read your git history like an archaeologist, reconstruct what you were building and why you stopped, understand your tech stack and constraints, generate a fresh roadmap, and create structured work items ready to pick up. In one command, a dormant project becomes a living, organized one — with a memory file that any future Claude session can load in seconds.

---

## What it actually does

Lisa runs a staged pipeline. Each stage produces files that the next stage (and future Claude sessions) can read:

| Stage | Command | What you get |
|-------|---------|--------------|
| **0 — Research** | `/lisa:research` | Git archaeology report: original mission, timeline, why it stalled, rescue recommendation |
| **1 — Discover** | `/lisa:discover` | `.gt/memory/semantic.json` — tech stack, constraints, personas, non-goals |
| **2 — Plan** | `/lisa:plan` | `scopecraft/` — vision, phased roadmap, epics + user stories, risks, metrics, open questions |
| **3 — Structure** | `/lisa:structure` | `.gt/beads/` + `.gt/convoys/` — individual work items and bundled assignments |
| **5 — Reconcile** | `/lisa:reconcile` | Cross-project alignment report — checks multiple repos stay consistent |

Two composite shortcuts:

```
/lisa:migrate    # Stages 1–3: discover + plan + structure (for active projects)
/lisa:rescue     # Stages 0–3: full rescue pipeline (for abandoned projects)
```

---

## Install

```
/install-plugin auge2u/lisa-helps-ralph-loops
```

That's it. No API keys, no database, no cloud. All outputs are local files.

---

## What you get in your repo

After `/lisa:migrate` or `/lisa:rescue`, your project has:

```
your-project/
├── .gt/
│   ├── memory/
│   │   └── semantic.json      ← everything Claude needs to understand the project
│   ├── beads/
│   │   └── gt-abc12.json      ← individual work items with acceptance criteria
│   └── convoys/
│       └── convoy-001.json    ← beads grouped for assignment
└── scopecraft/
    ├── VISION_AND_STAGE_DEFINITION.md
    ├── ROADMAP.md
    ├── EPICS_AND_STORIES.md
    ├── RISKS_AND_DEPENDENCIES.md
    ├── METRICS_AND_PMF.md
    └── OPEN_QUESTIONS.md
```

The `semantic.json` is the key file. Point any future Claude session at it and you skip the 20 minutes of re-orientation. It's a structured summary of what the project is, what it's built with, what constraints exist, and what's been decided — all in a format Claude reads natively.

---

## Quality gates

Every stage validates its own output against 31 declarative gates before you move on. If something is missing or wrong, you know before the next agent touches it.

```bash
python3 plugins/lisa/hooks/validate.py --stage discover
python3 plugins/lisa/hooks/validate.py --stage all
```

No PyYAML? It runs in fallback mode (file and JSON checks). Install PyYAML for full pattern validation.

---

## Part of a larger ecosystem

Lisa is the foundation layer of a three-plugin ecosystem:

| Plugin | What it adds | Status |
|--------|-------------|--------|
| **Lisa** (this) | Pipeline, memory, work structure | Alpha v0.3.0 |
| **[Carlos](https://github.com/auge2u/carlos)** | Specialist analysis: market fit, tech debt, roadmap depth | Beta v1.2.0 |
| **[Conductor](https://github.com/habitusnet/conductor)** | Multi-agent orchestration and task tracking | GA v1.0.0 |

Each plugin works completely standalone. Install one, or all three — the ecosystem is additive. Lisa's outputs (`.gt/` files and `scopecraft/`) are the shared language between them.

---

## Why this exists

Claude Code is powerful, but every new session starts cold. You re-explain the project, re-establish context, re-decide things that were already decided. Lisa solves the cold-start problem by giving Claude a structured memory of the project that persists across sessions.

It's especially useful for:

- **Abandoned projects** — reconstruct context and get a clear path to resume
- **Onboarding** — new contributors (human or AI) get up to speed immediately
- **Multi-agent workflows** — structured work items that agents can pick up without ambiguity
- **Long-running projects** — semantic memory keeps Claude oriented as the project grows

---

## License

MIT
