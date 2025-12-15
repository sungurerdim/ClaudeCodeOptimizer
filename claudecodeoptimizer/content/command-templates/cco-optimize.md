---
name: cco-optimize
description: Security and code quality analysis with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(ruff:*), Bash(mypy:*), Bash(pip:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-optimize

**Full-Stack Optimization** - Detect and fix ALL issues, leave nothing behind.

## Core Principle [CRITICAL]

**Fix everything that can be fixed.** All issues fall into:
1. **Auto-fix**: Safe to apply without asking
2. **Approval Required**: Ask user, then fix if approved

If an issue can be fixed by editing code, it MUST be fixed (with approval if needed).

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`

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
| 1 | Safety | Check git state, warn if dirty |
| 2 | Scope | Ask what to optimize |
| 3 | Action | Ask report/auto-fix/interactive |
| 4 | Analyze | Run agent, get findings JSON |
| 5 | Show | Display findings summary |
| 6 | Auto-fix | Apply safe fixes (if action != report) |
| 7 | Approval | Ask for approval-required items |
| 8 | Apply | Apply user-approved fixes |
| 9 | Summary | Show applied/declined counts |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Check safety", status: "in_progress", activeForm: "Checking git safety" },
  { content: "Step-2: Ask scope", status: "pending", activeForm: "Asking scope" },
  { content: "Step-3: Ask action", status: "pending", activeForm: "Asking action type" },
  { content: "Step-4: Run analysis", status: "pending", activeForm: "Running analysis" },
  { content: "Step-5: Show findings", status: "pending", activeForm: "Showing findings" },
  { content: "Step-6: Apply auto-fixes", status: "pending", activeForm: "Applying auto-fixes" },
  { content: "Step-7: Get approval", status: "pending", activeForm: "Getting approval" },
  { content: "Step-8: Apply approved", status: "pending", activeForm: "Applying approved fixes" },
  { content: "Step-9: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Safety

Check git working tree state.

| Condition | Action |
|-----------|--------|
| Clean | Proceed |
| Dirty | AskUserQuestion below |

```javascript
AskUserQuestion([{
  question: "Working tree has uncommitted changes. How to proceed?",
  header: "Git State",
  options: [
    { label: "Continue anyway", description: "Proceed with dirty working tree" },
    { label: "Stash first", description: "Stash changes, continue, remind to pop" },
    { label: "Cancel", description: "Abort optimization" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Git state checked
[x] If dirty: user decision collected
→ If Cancel: Exit
→ Proceed to Step-2
```

---

## Step-2: Scope

```javascript
AskUserQuestion([{
  question: "What to optimize?",
  header: "Scope",
  options: [
    { label: "Security", description: "OWASP, secrets, CVEs, input validation" },
    { label: "Quality", description: "Tech debt, type errors, test gaps" },
    { label: "Hygiene", description: "Orphans, stale refs, duplicates" },
    { label: "Best Practices", description: "Patterns, efficiency, consistency" }
  ],
  multiSelect: true
}])
```

**Dynamic labels:** Add `(Recommended)` based on Data/Priority context.

### Validation
```
[x] User selected scope(s)
→ Store as: scopes = {selections[]}
→ Proceed to Step-3
```

---

## Step-3: Action

```javascript
AskUserQuestion([{
  question: "How to handle findings?",
  header: "Action",
  options: [
    { label: "Report Only", description: "Show issues without fixing" },
    { label: "Auto-fix", description: "Apply safe fixes automatically" },
    { label: "Interactive", description: "Ask before each fix" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] User selected action
→ Store as: action = {selection}
→ If Report Only: Skip Step-6, Step-7, Step-8
→ Proceed to Step-4
```

---

## Step-4: Analyze

```javascript
agentResponse = Task("cco-agent-analyze", `
  scopes: ${JSON.stringify(scopes)}
  Return findings JSON with:
  - findings[]: { id, scope, severity, title, file, line, fix_description, auto_fixable, risk }
  - summary: { total, by_scope, by_severity, auto_fixable_count }
`)
```

### Validation
```
[x] Agent returned valid response
[x] response.findings exists
[x] response.summary exists
→ Proceed to Step-5
```

---

## Step-5: Show Findings

Display findings summary to user:
- Counts by scope (Security: N, Quality: N, ...)
- Counts by severity (Critical: N, High: N, ...)
- Auto-fixable vs Approval-required counts

### Validation
```
[x] Summary displayed to user
→ If action = "Report Only": Skip to Step-9
→ Proceed to Step-6
```

---

## Step-6: Apply Auto-fixes [SKIP if action = "Report Only"]

```javascript
autoFixable = findings.filter(f => f.auto_fixable && f.risk === "LOW")

Task("cco-agent-apply", `
  fixes: ${JSON.stringify(autoFixable)}
  Apply all auto-fixable items. Verify each fix.
`)
```

### Validation
```
[x] Auto-fixes applied
[x] No cascading errors introduced
→ Store as: autoFixed = {count}
→ If no approval-required items: Skip to Step-9
→ Proceed to Step-7
```

---

## Step-7: Approval [SKIP if action = "Report Only" OR no approval-required items]

**Paginated format (max 4 per page):**

```javascript
approvalRequired = findings.filter(f => !f.auto_fixable || f.risk !== "LOW")

// Page 1
AskUserQuestion([{
  question: `Fix these issues? (Page 1/${totalPages})`,
  header: "Approve",
  options: approvalRequired.slice(0, 4).map(f => ({
    label: `${f.id}: ${f.title}`,
    description: `${f.file}:${f.line} - ${f.fix_description}`
  })),
  multiSelect: true
}])

// Continue for additional pages...
```

### Validation
```
[x] All pages presented
[x] User selections collected
→ Store as: approved = {selections[]}, declined = {unselected[]}
→ Proceed to Step-8
```

---

## Step-8: Apply Approved [SKIP if nothing approved]

```javascript
Task("cco-agent-apply", `
  fixes: ${JSON.stringify(approved)}
  Apply user-approved items. Verify each fix. Cascade if needed.
`)
```

### Validation
```
[x] Approved fixes applied
[x] Cascading errors handled
→ Store as: appliedApproved = {count}
→ Proceed to Step-9
```

---

## Step-9: Summary

Display final summary:
- Auto-fixed: {autoFixed} items
- User-approved: {appliedApproved} items
- Declined: {declined.length} items
- Verification status

### Validation
```
[x] Summary displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Scope Coverage

| Scope | Checks |
|-------|--------|
| `security` | OWASP, secrets, CVEs, input validation |
| `quality` | Tech debt, type errors, test gaps |
| `hygiene` | Orphans, stale refs, duplicates |
| `best-practices` | Patterns, efficiency, consistency |

### Context Application

| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security ×2 |
| Scale | 10K+ → stricter |
| Maturity | Legacy → safe only |
| Priority | Speed → critical; Quality → all |

### Impact Preview

For each fix, show:
- **Direct**: Files to modify
- **Dependents**: Files that import/use
- **Tests**: Coverage of affected code
- **Risk**: LOW (auto-fix) / MEDIUM / HIGH (approval required)

### Flags

| Flag | Effect |
|------|--------|
| `--security` | Security scope only |
| `--quality` | Quality scope only |
| `--hygiene` | Hygiene scope only |
| `--best-practices` | Best practices scope only |
| `--report` | Report only (no fixes) |
| `--fix` | Auto-fix safe (default) |
| `--fix-all` | Fix all with approval |
| `--critical` | Security + tests only |
| `--pre-release` | All scopes, strict |

---

## Rules

1. **Sequential execution** - Complete each step before proceeding
2. **Validation gates** - Check validation block before next step
3. **ONE analyze agent** - Never spawn multiple analyze agents
4. **ONE apply agent** - Never spawn multiple apply agents
5. **Paginated approval** - Max 4 items per AskUserQuestion
