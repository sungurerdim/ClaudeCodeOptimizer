---
name: cco-checkup
description: Regular maintenance routine
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-checkup

**Maintenance Routine** - Parallel health + audit for fast weekly checkups.

Meta command running /cco-status and /cco-optimize in parallel.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
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

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Phase Select | Ask which phases | Skip with flags |
| 2 | Execute | Parallel: health + audit | 2x faster |
| 3 | Summary | Merge and display | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select phases", status: "in_progress", activeForm: "Selecting phases" },
  { content: "Step-2: Run health + audit (parallel)", status: "pending", activeForm: "Running health and audit" },
  { content: "Step-3: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Phase Selection

**Smart Default:** Run both phases (health + audit) without asking.

```javascript
// Default: Both phases - no question needed
phases = "Both"

// Flags override:
// --health-only → phases = "Health Dashboard"
// --audit-only → phases = "Quality Audit"
```

### Validation
```
[x] Phases determined (default: Both)
→ Store as: phases = {selection}
→ Proceed to Step-2
```

---

## Step-2: Execute [PARALLEL]

**Launch both sub-commands in a SINGLE message if both selected:**

```javascript
// CRITICAL: Both Task calls in ONE message for true parallelism

if (phases === "Both" || phases === "Health Dashboard") {
  healthTask = Task("general-purpose", `
    Execute /cco-status --brief
    Return: {
      scores: { security, quality, architecture, bestPractices, overall },
      status: "OK|WARN|FAIL|CRITICAL"
    }
  `, { model: "haiku", run_in_background: phases === "Both" })
}

if (phases === "Both" || phases === "Quality Audit") {
  auditTask = Task("general-purpose", `
    Execute /cco-optimize --fix --security --quality
    Return: {
      accounting: { done, declined, fail, total },
      by_scope: { security: {n}, quality: {n} }
    }
  `, { model: "sonnet", run_in_background: phases === "Both" })
}

// If both running, collect results
if (phases === "Both") {
  healthResults = await TaskOutput(healthTask.id)
  auditResults = await TaskOutput(auditTask.id)
}
```

**Parallel Execution:**
- Health (read-only) uses Haiku for speed
- Audit (writes) uses Sonnet for accuracy
- Both complete in ~same time as single command

### Validation
```
[x] Selected tasks launched in parallel
[x] Results collected
→ Proceed to Step-3
```

---

## Step-3: Summary

```
## Checkup Complete

### Health Dashboard
| Category | Score | Status |
|----------|-------|--------|
| Security | {scores.security} | {getStatus(scores.security)} |
| Quality | {scores.quality} | {getStatus(scores.quality)} |
| Architecture | {scores.architecture} | {getStatus(scores.architecture)} |
| Best Practices | {scores.bestPractices} | {getStatus(scores.bestPractices)} |
| **Overall** | **{scores.overall}** | **{status}** |

### Quality Audit
| Scope | Done | Declined | Failed |
|-------|------|----------|--------|
| Security | {by_scope.security} | - | - |
| Quality | {by_scope.quality} | - | - |
| **Total** | **{accounting.done}** | **{accounting.declined}** | **{accounting.fail}** |

Duration: {n}s
```

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
| `--no-fix` | Report only (health + audit report) |
| `--deep` | Full deep audit |
| `--health-only` | Skip audit |
| `--audit-only` | Skip health |
| `--sequential` | Disable parallel (debug) |

---

## Rules

1. **Parallel-first** - Launch health + audit in single message
2. **Model strategy** - Haiku for health, Sonnet for audit
3. **Delegate to sub-commands** - Don't duplicate logic
4. **Aggregate results** - Merge outputs for summary
