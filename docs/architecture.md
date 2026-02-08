# Architecture

How CCO works internally: rules, agents, and command flow.

---

## System Overview

```
                     Claude Code
                          |
              ~/.claude/rules/cco-rules.md
                  (auto-loaded at start)
                          |
                    Rules Active
                          |
              ┌───────────┼───────────┐
              |           |           |
        /cco-optimize  /cco-align  /cco-commit  ...
              |           |           |
              └─────┬─────┴─────┬─────┘
                    |           |
            cco-agent-analyze  cco-agent-apply
```

## Repository Structure

```
ClaudeCodeOptimizer/
├── rules/
│   └── cco-rules.md            # Core rules (single source of truth)
├── commands/                    # Slash commands (8 files)
│   ├── cco-optimize.md
│   ├── cco-align.md
│   ├── cco-commit.md
│   ├── cco-research.md
│   ├── cco-docs.md
│   ├── cco-blueprint.md
│   ├── cco-pr.md
│   └── cco-update.md
├── agents/                      # Subagents (3 files)
│   ├── cco-agent-analyze.md
│   ├── cco-agent-apply.md
│   └── cco-agent-research.md
├── install.sh                   # macOS/Linux installer
├── install.ps1                  # Windows installer
└── version.txt                  # Current version (SSOT, managed by release-please)
```

### Installed Structure

```
~/.claude/
├── rules/
│   └── cco-rules.md            # Auto-loaded by Claude Code
├── commands/
│   ├── cco-optimize.md ... cco-update.md
└── agents/
    ├── cco-agent-analyze.md ... cco-agent-research.md
```

---

## Rule Loading

Rules are loaded automatically at session start via Claude Code's native mechanisms:
- Core rules: `~/.claude/rules/cco-rules.md` (auto-loaded)
- Project rules: `.claude/rules/*.md` (auto-loaded)

---

## Agent System

| Agent | Purpose | Model | Pattern |
|-------|---------|-------|---------|
| analyze | Read-only analysis, metrics, findings | Haiku | Linters → Grep → Context reads → JSON |
| apply | Write operations with verification | Opus | Pre-check → Read → Apply → Verify → Cascade |
| research | Information gathering with scoring | Haiku | Search → Fetch → Score → Synthesize |

---

## Command Flow

### /cco-optimize

```
User: /cco-optimize → Setup → Analyze (parallel) → Plan Review → Apply → Summary
```

---

## Data Flow

### Finding Schema

```json
{
  "id": "SEC-01", "scope": "security", "severity": "CRITICAL",
  "title": "Hardcoded API key", "location": "src/config.py:42",
  "fixable": true, "fix": "Move to environment variable"
}
```

### Accounting Schema

```json
{ "applied": 12, "failed": 1, "needs_approval": 0, "total": 13 }
```

Invariant: `applied + failed + needs_approval = total`

---

## Model Strategy

| Task | Model | Reason |
|------|-------|--------|
| Detection & Analysis | Haiku | Fast, read-only |
| Code fixes & Synthesis | Opus | Fewer errors on edits |
| Research | Haiku + Opus | Haiku search, Opus synthesis |

---

*Back to [README](../README.md)*
