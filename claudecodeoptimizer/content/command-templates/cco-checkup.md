---
name: cco-checkup
description: Regular maintenance routine
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-checkup

**Maintenance Routine** - Health check → smart audit → quick cleanup.

Meta command for regular project maintenance (weekly recommended).

**Rules:** User Input | Orchestration | Progress Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Last health tag: !`git tag -l "health-*" --sort=-creatordate | head -1 || echo "None"`
- Git status: !`git status --short`
- Recent activity: !`git log --oneline -5`

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Applicable) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Phase Selection

When called without flags → **AskUserQuestion**:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Which phases to run? | Health Dashboard (Recommended); Quality Audit (Recommended) | true |

Flags `--health-only`, `--audit-only` skip this question.

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Run health dashboard", status: "in_progress", activeForm: "Running health dashboard" },
  { content: "Run quality audit", status: "pending", activeForm: "Running quality audit" },
  { content: "Show summary", status: "pending", activeForm: "Showing summary" }
])
```

## Flow

### Phase 1: Health Dashboard
Orchestrates: `/cco-status --brief` (Security, Tests, Tech Debt, Cleanliness, Documentation scores)

### Phase 2: Quality Audit
Orchestrates: `/cco-optimize --fix` (Security, Quality, Hygiene, Best Practices)

### Summary
Shows: Duration, Changes since last, Fixed/Declined counts, Next recommended checkup

## Comparison

| Need | Command |
|------|---------|
| Weekly maintenance | `/cco-checkup` |
| Pre-release | `/cco-preflight` |
| Deep audit | `/cco-optimize` |
| Strategic review | `/cco-review` |

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Preview only |
| `--no-fix` | Report only |
| `--deep` | Full audit |
| `--trends` | Trend history |

## Strategy Evolution

| Pattern | Action |
|---------|--------|
| Recurring issue | Add to `Systemic` |
| Score degraded | Add to `Avoid` |
| Score improved | Add to `Prefer` |

## Rules

Delegate to sub-commands │ Aggregate results │ No duplicate work │ Use TodoWrite │ Safety via /cco-optimize
