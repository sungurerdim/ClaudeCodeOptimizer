---
name: cco-checkup
description: Regular maintenance routine
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-checkup

**Maintenance Routine** - Health check → smart audit → quick cleanup.

Meta command for regular project maintenance (weekly recommended).

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Last health tag: !`git tag -l "health-*" --sort=-creatordate | head -1 || echo "None"`
- Git status: !`git status --short`
- Recent activity: !`git log --oneline -5`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Architecture

| Step | Name | Action |
|------|------|--------|
| 1 | Phase Select | Ask which phases to run |
| 2 | Health | Run /cco-status --brief |
| 3 | Audit | Run /cco-optimize --fix |
| 4 | Summary | Show results and next checkup |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select phases", status: "in_progress", activeForm: "Selecting phases" },
  { content: "Step-2: Run health dashboard", status: "pending", activeForm: "Running health dashboard" },
  { content: "Step-3: Run quality audit", status: "pending", activeForm: "Running quality audit" },
  { content: "Step-4: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Phase Selection

```javascript
AskUserQuestion([{
  question: "Which phases to run?",
  header: "Phases",
  options: [
    { label: "Health Dashboard", description: "Security, tests, debt, cleanliness scores" },
    { label: "Quality Audit", description: "Security, quality, hygiene, best practices fixes" }
  ],
  multiSelect: true
}])
```

**Dynamic labels:** Add `(Recommended)` based on last run date and context.

**Flags override:** `--health-only`, `--audit-only` skip this question.

### Validation
```
[x] User selected phase(s)
→ Store as: phases = {selections[]}
→ If "Health Dashboard" not in phases: Skip Step-2
→ If "Quality Audit" not in phases: Skip Step-3
→ Proceed to Step-2 or Step-3
```

---

## Step-2: Health Dashboard [SKIP if not selected]

Orchestrates: `/cco-status --brief`

Returns: Security, Tests, Tech Debt, Cleanliness, Documentation scores.

### Validation
```
[x] Health scores collected
→ Store as: healthScores = { security, tests, debt, clean, docs }
→ Proceed to Step-3 (or Step-4 if audit not selected)
```

---

## Step-3: Quality Audit [SKIP if not selected]

Orchestrates: `/cco-optimize --fix`

Runs all scopes: Security, Quality, Hygiene, Best Practices.

### Validation
```
[x] Audit completed
→ Store as: auditResults = { fixed, declined, total }
→ Proceed to Step-4
```

---

## Step-4: Summary

Display:
- Duration: {time}
- Health Scores: {if run}
- Fixed/Declined: {if audit run}
- Changes since last checkup
- Next recommended checkup: {date}

### Validation
```
[x] Summary displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Comparison

| Need | Command |
|------|---------|
| Weekly maintenance | `/cco-checkup` |
| Pre-release | `/cco-preflight` |
| Deep audit | `/cco-optimize` |
| Strategic review | `/cco-review` |

### Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Preview only |
| `--no-fix` | Report only |
| `--deep` | Full audit |
| `--trends` | Trend history |
| `--health-only` | Skip audit |
| `--audit-only` | Skip health |

---

## Rules

1. **Sequential execution** - Complete each step before proceeding
2. **Validation gates** - Check validation block before next step
3. **Delegate to sub-commands** - Don't duplicate /cco-status or /cco-optimize logic
4. **No duplicate work** - Aggregate results from sub-commands
