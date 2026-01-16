---
description: Weekly maintenance - health check + optimization in one pass
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(*), Task(*)
---

# /checkup

**Maintenance Routine** - Parallel health + audit for fast weekly checkups.

Meta command: runs /status and /optimize in parallel. No TodoWrite - delegates to sub-commands.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /config first to configure project context, then restart CLI.
```
**Stop immediately.**

---

## Execution

### 1. Launch Parallel Tasks

```javascript
// Determine phases from flags
phases = args.includes('--health-only') ? 'health'
       : args.includes('--audit-only') ? 'audit'
       : 'both'

// Launch in parallel (SINGLE message with multiple Task calls)
if (phases === 'both' || phases === 'health') {
  healthTask = Task("general-purpose", `
    Execute /status --brief
    Return: { scores: {...}, status: "OK|WARN|FAIL|CRITICAL" }
  `, { model: "haiku", run_in_background: phases === 'both' })
}

if (phases === 'both' || phases === 'audit') {
  auditTask = Task("general-purpose", `
    Execute /optimize --fix --security --quality
    Return: { accounting: { applied, failed, total } }
  `, { model: "opus", run_in_background: phases === 'both' })
}
```

### 2. Collect Results

```javascript
if (phases === 'both') {
  healthResults = await TaskOutput(healthTask.id)
  auditResults = await TaskOutput(auditTask.id)
}
```

### 3. Display Summary

```
## Checkup Complete

### Health Dashboard
| Category       | Score | Status |
|----------------|-------|--------|
| Security       | {n}   | {status} |
| Quality        | {n}   | {status} |
| Architecture   | {n}   | {status} |
| Best Practices | {n}   | {status} |
| **Overall**    | **{n}** | **{status}** |

### Quality Audit
Applied: {n} | Failed: {n}

Status: {status}
```

---

## Flags

| Flag | Effect |
|------|--------|
| `--health-only` | Skip audit |
| `--audit-only` | Skip health |
| `--dry-run` | Preview only |
| `--no-fix` | Report only |

## Rules

1. **Parallel-first** - Launch both in single message
2. **Model strategy** - Haiku for health, Opus for audit
3. **Delegate** - Sub-commands handle their own logic
4. **Fast** - No TodoWrite, sub-commands show progress
