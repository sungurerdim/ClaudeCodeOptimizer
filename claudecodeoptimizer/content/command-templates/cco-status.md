---
name: cco-status
description: Project health dashboard
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Task(*), TodoWrite
---

# /cco-status

**Health Dashboard** - Single view of project health with trends via parallel agents.

Read-only metrics collection and visualization.

## Context Requirement

```
test -f ./.claude/rules/cco/context.md && echo "OK" || echo "Run /cco-config first"
```

If not found: Stop immediately with message to run /cco-config.

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each step.

```
TodoWrite([
  { content: "Spawn parallel agents", status: "in_progress", activeForm: "Spawning parallel agents" },
  { content: "Merge metrics", status: "pending", activeForm: "Merging metrics" },
  { content: "Generate dashboard", status: "pending", activeForm: "Generating dashboard" }
])
```

**Update status:** Mark `completed` immediately after each step finishes, mark next `in_progress`.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Spawn parallel agents (single message with 2 Task calls)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scope=scan)   ──┬──→ Both run simultaneously        │
│ Task(cco-agent-analyze, scope=trends) ──┘                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Merge metrics + trend data                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Generate dashboard output                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Parallel agents MUST be spawned in a single message with multiple Task tool calls.

## Agent Scopes

| Agent | Scope | Returns |
|-------|-------|---------|
| cco-agent-analyze | `scan` | Security, tests, debt, cleanliness metrics |
| cco-agent-analyze | `trends` | Historical deltas with ↑↓→⚠ indicators |

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
