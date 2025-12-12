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

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Spawn parallel agents (single message with 2 Task calls)            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scope=scan)   ──┬──→ Both run simultaneously        │
│ Task(cco-agent-analyze, scope=trends) ──┘                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Merge metrics + trend data                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Generate dashboard output                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Step 1 MUST be a single message with multiple Task tool calls.

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

## Score Categories

| Category | Metrics |
|----------|---------|
| Security | OWASP, secrets, CVEs, input validation |
| Tests | Coverage %, branch coverage, quality |
| Tech Debt | Complexity, dead code, TODO count |
| Cleanliness | Orphans, duplicates, stale refs |
| Documentation | README, docstrings, examples |

## Status Thresholds

| Score | Status |
|-------|--------|
| 90-100 | OK |
| 70-89 | WARN |
| 50-69 | FAIL |
| 0-49 | CRITICAL |

## Trend Indicators

| Symbol | Meaning |
|--------|---------|
| ↑ | Improved (>5% better) |
| → | Stable (±5%) |
| ↓ | Degraded (>5% worse) |
| ⚠ | Rapid decline (>15% worse) |

## Output

```
┌─ PROJECT HEALTH ─────────────────────────────────────────────┐
│ Project: {name} | Type: {type} | Trend: {icon}               │
├───────────────┬───────┬────────────┬───────┬─────────────────┤
│ Category      │ Score │ Bar        │ Trend │ Status          │
├───────────────┼───────┼────────────┼───────┼─────────────────┤
│ Security      │ {n}   │ ████░░░░   │ {t}   │ {status}        │
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
