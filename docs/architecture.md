# Architecture

How CCO works internally: rules, agents, and skill flow.

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
├── skills/                     # Skills (8 directories)
│   ├── cco-optimize/SKILL.md
│   ├── cco-align/SKILL.md
│   ├── cco-commit/SKILL.md
│   ├── cco-research/SKILL.md
│   ├── cco-docs/SKILL.md
│   ├── cco-blueprint/SKILL.md
│   ├── cco-pr/SKILL.md
│   └── cco-update/SKILL.md
├── agents/                     # Subagents (3 files)
│   ├── cco-agent-analyze.md
│   ├── cco-agent-apply.md
│   └── cco-agent-research.md
├── extras/
│   ├── installer/              # Go binary installer
│   └── statusline/             # Optional statusline add-on
└── version.txt                 # Current version (SSOT, managed by release-please)
```

### Installed Structure

```
~/.claude/
├── rules/
│   └── cco-rules.md            # Auto-loaded by Claude Code
├── skills/
│   ├── cco-optimize/SKILL.md ... cco-update/SKILL.md
└── agents/
    ├── cco-agent-analyze.md ... cco-agent-research.md
```

---

## Rule Loading

Rules are loaded automatically at session start via Claude Code's native mechanisms:
- Core rules: `~/.claude/rules/cco-rules.md` (auto-loaded)
- Project rules: `.claude/rules/*.md` (auto-loaded)

---

## Skill System

Skills use Claude Code's native skill mechanism with `SKILL.md` files in `~/.claude/skills/{name}/`. Frontmatter fields (`allowed-tools`, `description`) are enforced by Claude Code, unlike the legacy `commands/` directory.

6 skills have auto-invoke enabled (triggered by natural language), 2 require explicit invocation (`/cco-blueprint`, `/cco-update`).

### Shared Patterns

Common patterns (severity levels, accounting, skip patterns, confidence scoring, auto mode) are defined once in `rules/cco-rules.md` under CCO Operations. Skills reference them with `Per CCO Rules.`

When updating these patterns, update the rules file — all skills and agents inherit automatically.

---

## Agent System

| Agent | Purpose | Model | Pattern |
|-------|---------|-------|---------|
| analyze | Read-only analysis, metrics, findings | Haiku | Linters → Grep → Context reads → JSON |
| apply | Write operations with verification | Opus | Pre-check → Read → Apply → Verify → Cascade |
| research | Information gathering with scoring | Haiku | Search → Fetch → Score → Synthesize |

### Agent Contracts

| Agent | Input | Output |
|-------|-------|--------|
| analyze | `{scopes: string[], mode: "review"\|"auto"\|"audit"}` | `{findings[], scores{}, metrics{}, error?}` |
| apply | `{findings[], fixAll?: boolean}` | `{applied, failed, needs_approval, total, error?}` |
| research | `{query, depth: "standard"\|"deep"}` | `{sources[], synthesis, reliability_score, error?}` |

**Error contract:** On failure, all agents return `{"error": "message"}`. Per CCO Rules: Agent Output.

### File Manifest Sync

The file lists in `extras/installer/main.go` and `skills/cco-update/SKILL.md` must stay synchronized. When adding or removing a skill/agent file, update both locations.

---

## Skill Flow

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

Agent model selection is specified in agent frontmatter (`model: haiku` / `model: opus`). Skills inherit the session model — no model lock-in.

| Task | Model | Reason |
|------|-------|--------|
| Detection & Analysis | Haiku | Fast, read-only |
| Code fixes & Synthesis | Opus | Fewer errors on edits |
| Research | Haiku + Opus | Haiku search, Opus synthesis |

---

*Back to [README](../README.md)*
