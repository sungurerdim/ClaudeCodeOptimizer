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

## Rules Architecture

CCO rules follow a "behavioral, not procedural" design. Rules define WHAT behavior is expected, not HOW to execute operations. Operational details (accounting formulas, approval flows, execution sequences) live in the commands and agents that use them.

| Layer | Contains | Example |
|-------|----------|---------|
| Rules | Behavioral constraints | "Read before write" |
| Commands | Operational procedures | Needs-approval flow, accounting |
| Agents | Execution details | Confidence scoring, linter detection |

## Agent System

| Agent | Purpose | Model | Pattern |
|-------|---------|-------|---------|
| analyze | Read-only analysis, metrics, findings | Haiku | Conditional linters → Grep → Context reads → JSON |
| apply | Write operations with verification | Opus | Validate input → Read → Apply → Verify → Cascade |
| research | Information gathering with scoring | Haiku | Search → Fetch → Score → Synthesize |

### Agent Contracts

**Input:** All agents receive parameters via the Task tool's prompt. Each agent documents its expected fields in its `## Input` section.

| Agent | Input | Modes | Output |
|-------|-------|-------|--------|
| analyze | `{scopes: string[], mode: "review"\|"auto"\|"audit"}` | review (strategic), auto (tactical), audit (project-level) | `{findings[], scores{}, metrics{}, error?}` |
| apply | `{findings[], fixAll?: boolean}` | — | `{applied, failed, needs_approval, total, error?}` |
| research | `{query, depth: "standard"\|"deep"}` | — | `{sources[], synthesis, reliability_score, error?}` |

**Error contract:** On failure, all agents return `{"error": "message"}` with empty arrays for data fields. Calling commands retry once on malformed output, then report as failed.

### File Manifest Sync

The file lists in `install.sh`, `install.ps1`, and `commands/cco-update.md` must stay synchronized. When adding or removing a command/agent file, update all three locations.

---

## Command Structure

### Standard Section Order

All commands follow this section order: Frontmatter → Description → Args/Flags → Context → Scopes (if applicable) → Execution Flow → Summary format.

- Use `## Args` for commands with positional/named arguments
- Use `## Flags` for commands with only boolean/option flags

### Shared Patterns

Plan Review, Needs-Approval Review, and Accounting are inlined in each command (self-containment principle). This duplication is intentional — each command carries its own operational context without cross-references. When updating these patterns, check all commands that use them:

| Pattern | Used By |
|---------|---------|
| Plan Review | cco-optimize, cco-align, cco-blueprint, cco-docs |
| Needs-Approval | cco-optimize, cco-align, cco-blueprint |
| Accounting | cco-optimize, cco-align, cco-blueprint, cco-commit |

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
  "title": "Hardcoded API key", "location": { "file": "src/config.py", "line": 42 },
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
