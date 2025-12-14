---
name: cco-status
description: Project health dashboard
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Task(*), TodoWrite
---

# /cco-status

**Health Dashboard** - Single view of project health with trends via parallel agents.

Read-only metrics collection and visualization.

## Dynamic Context (Pre-collected)

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Last health tag: !`git tag -l "health-*" --sort=-creatordate | head -1 || echo "None"`

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Stack, Type, Scale) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Token Efficiency [CRITICAL]

| Rule | Implementation |
|------|----------------|
| **Single agent** | One analyze agent with scan + trends scopes |
| **Linter-first** | Run linters for metrics |
| **Batch calls** | Multiple tool calls in single message |

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each step.

```
TodoWrite([
  { content: "Collect metrics", status: "in_progress", activeForm: "Collecting metrics" },
  { content: "Generate dashboard", status: "pending", activeForm: "Generating dashboard" }
])
```

**Update status:** Mark `completed` immediately after each step finishes, mark next `in_progress`.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Spawn SINGLE analyze agent with scan + trends scopes                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scopes=[scan, trends])                               │
│ → Agent runs linters first for metrics                                       │
│ → Returns combined scan + trend data                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Generate dashboard output                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Use ONE analyze agent. Never spawn separate scan/trends agents.

## Agent Usage

| Agent | Input | Output |
|-------|-------|--------|
| cco-agent-analyze | `scopes: [scan, trends]` | Combined metrics + trends JSON |

### Scope Coverage

| Scope | Returns |
|-------|---------|
| `scan` | Security, tests, debt, cleanliness metrics |
| `trends` | Historical deltas with ↑↓→⚠ indicators |

## Context Application

| Field | Effect |
|-------|--------|
| Scale | <100 → relaxed; 100-10K → moderate; 10K+ → strict thresholds |
| Data | PII/Regulated → security weight ×2 |
| Priority | Speed → blockers only; Quality → all metrics |

## Output

```
┌─ PROJECT HEALTH ─────────────────────────────────────────────┐
│ Project: {name} | Type: {type} | Trend: {icon}               │
├───────────────┬───────┬────────────┬───────┬─────────────────┤
│ Category      │ Score │ Bar        │ Trend │ Status          │
├───────────────┼───────┼────────────┼───────┼─────────────────┤
│ Security      │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Tests         │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Tech Debt     │ {n}   │ {bar}      │ {t}   │ {status}        │
│ Cleanliness   │ {n}   │ {bar}      │ {t}   │ {status}        │
├───────────────┼───────┼────────────┼───────┼─────────────────┤
│ OVERALL       │ {n}   │ {bar}      │ {t}   │ {status}        │
└───────────────┴───────┴────────────┴───────┴─────────────────┘

┌─ FIX FIRST ──────────────────────────────────────────────────┐
│ # │ Issue              │ Location      │ Effort │ Impact     │
├───┼────────────────────┼───────────────┼────────┼────────────┤
│ 1 │ {issue}            │ {file}:{line} │ {eff}  │ {imp}      │
└───┴────────────────────┴───────────────┴────────┴────────────┘
```

## Flags

| Flag | Effect |
|------|--------|
| `--focus=X` | Detailed breakdown: security, tests, debt, clean |
| `--trends` | Show historical trend table |
| `--json` | Output as JSON |
| `--brief` | Summary only |

## Rules

1. **Parallel agents** - Scan + trends agents run simultaneously
2. **Read-only** - No modifications, metrics only
3. **Conservative** - When uncertain, score lower
4. **Evidence** - Require explicit metrics, not inference
