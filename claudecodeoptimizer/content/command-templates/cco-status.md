---
name: cco-status
description: Project health dashboard
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Task(*), TodoWrite
---

# /cco-status

**Health Dashboard** - Single view of project health with trends via parallel agents.

Read-only metrics collection and visualization.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Last health tag: !`git tag -l "health-*" --sort=-creatordate | head -1 || echo "None"`

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Stack, Type, Scale) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Token Efficiency [CRITICAL]

Single analyze agent (scan + trends) │ Linter-first │ Batch calls

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Collect metrics", status: "in_progress", activeForm: "Collecting metrics" },
  { content: "Generate dashboard", status: "pending", activeForm: "Generating dashboard" }
])
```

## Execution Flow

```
Task(cco-agent-analyze, scopes=[scan, trends])
→ Linters first → Combined scan + trends data → Dashboard output
```

**CRITICAL:** Use ONE analyze agent. Never spawn separate agents.

| Scope | Returns |
|-------|---------|
| `scan` | Security, tests, debt, cleanliness metrics |
| `trends` | Historical deltas (↑↓→⚠) |

## Context Application

| Field | Effect |
|-------|--------|
| Scale | <100 → relaxed; 100-10K → moderate; 10K+ → strict |
| Data | PII/Regulated → security ×2 |
| Priority | Speed → blockers only; Quality → all |

## Flags

| Flag | Effect |
|------|--------|
| `--focus=X` | Detailed: security, tests, debt, clean |
| `--trends` | Historical trend table |
| `--json` | JSON output |
| `--brief` | Summary only |

## Output Formatting

| Element | Format |
|---------|--------|
| Scores | Right-aligned numbers |
| Status | OK / WARN / FAIL / CRITICAL (centered) |
| Trends | ↑ ↓ → ⚠ indicators |
| Progress | `████░░░░` (8 chars, filled = score/100×8) |

**Prohibited:** No emojis │ No ASCII art │ No unicode decorations

## Rules

Single agent │ Read-only │ Conservative scores │ Evidence-based
