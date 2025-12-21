---
name: cco-optimize
description: Security and code quality analysis with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(ruff:*), Bash(mypy:*), Bash(pip:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-optimize

**Full-Stack Optimization** - Parallel analysis + background fixes.

## Core Principle [CRITICAL]

**Fix everything that can be fixed.** All issues fall into:
1. **Auto-fix**: Safe to apply without asking (background)
2. **Approval Required**: Ask user, then fix if approved

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

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Safety | Check git state | Instant |
| 2 | Scope | Ask what to optimize | Skip with flags |
| 3 | Action | Ask report/auto-fix | Skip with flags |
| 4 | Analyze | cco-agent-analyze (parallel internally) | Fast |
| 5 | Show | Progressive display | Real-time |
| 6 | Auto-fix | cco-agent-apply (background) | Non-blocking |
| 7 | Approval | Ask while fixes run | Parallel UX |
| 8 | Apply | cco-agent-apply | Batched |
| 9 | Summary | Show counts | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Check safety", status: "in_progress", activeForm: "Checking git safety" },
  { content: "Step-2: Ask scope", status: "pending", activeForm: "Asking scope" },
  { content: "Step-3: Ask action", status: "pending", activeForm: "Asking action type" },
  { content: "Step-4: Run parallel analysis", status: "pending", activeForm: "Running parallel analysis" },
  { content: "Step-5: Show findings", status: "pending", activeForm: "Showing findings" },
  { content: "Step-6: Apply auto-fixes (background)", status: "pending", activeForm: "Applying auto-fixes" },
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
    { label: "Continue anyway (Recommended)", description: "Proceed, changes will be visible in git diff" },
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
→ If --score flag: Jump to Step-Score
→ Proceed to Step-2
```

---

## Step-Score: Quality Score [OPTIONAL]

**When `--score` flag is used, skip Steps 2-8 and show quality score only:**

```javascript
agentResponse = Task("cco-agent-analyze", `
  scopes: ["scan"]

  Calculate overall quality score (0-100).
  Scoring: Start at 100, deduct for issues (critical: -10, high: -5, medium: -2, low: -1)
`, { model: "haiku" })

// Agent returns (matches cco-agent-analyze scan output schema):
// agentResponse = {
//   scores: { security, quality, architecture, bestPractices, overall },
//   status: "OK|WARN|FAIL|CRITICAL",
//   topIssues: [{ category, title, location }],
//   summary: "{assessment}"
// }
```

**Output:**
```
## Quality Score: {agentResponse.scores.overall}/100

| Category | Score |
|----------|-------|
| Security | {agentResponse.scores.security}/100 |
| Quality | {agentResponse.scores.quality}/100 |
| Architecture | {agentResponse.scores.architecture}/100 |
| Best Practices | {agentResponse.scores.bestPractices}/100 |

{agentResponse.summary}

Top Issues:
{agentResponse.topIssues.map(i => `- ${i.title} (${i.location})`)}
```

→ Exit after showing score

---

## Step-2: Scope

```javascript
AskUserQuestion([{
  question: "What to optimize?",
  header: "Scope",
  options: [
    { label: "Security", description: "OWASP, secrets, CVEs, input validation" },
    { label: "Quality", description: "Tech debt, type errors, test gaps, error handling" },
    { label: "Architecture", description: "SOLID violations, god classes, circular deps" },
    { label: "Best Practices", description: "Resource management, patterns, consistency" }
  ],
  multiSelect: true
}])
```

**Flags override:** `--security`, `--quality`, `--architecture`, `--best-practices` skip this question.

**Dynamic labels:** Add `(Recommended)` based on Data/Priority context:
- PII/Regulated data → Security recommended
- Legacy maturity → Quality recommended
- Speed priority → Security + Quality recommended

### Validation
```
[x] User selected scope(s)
→ Store as: scopes = {selections[]}
→ Proceed to Step-3
```

---

## Step-3: Action

**Smart Default:** Auto-fix safe issues, ask for risky ones. No question needed.

```javascript
// Default: Auto-fix - no question needed
action = "Auto-fix"

// Flags override:
// --report → action = "Report Only" (skip Steps 6-8)
// --fix → action = "Auto-fix" (default)
// --fix-all → action = "Fix All" (no approval needed)
// --interactive → action = "Interactive" (ask before each)
```

### Validation
```
[x] Action determined (default: Auto-fix)
→ Store as: action = {selection}
→ If Report Only: Skip Step-6, Step-7, Step-8
→ Proceed to Step-4
```

---

## Step-4: Analyze [PARALLEL]

**Launch cco-agent-analyze in a SINGLE message with selected scopes:**

```javascript
// CRITICAL: All selected scopes in ONE cco-agent-analyze call
// Agent handles parallelization internally

Task("cco-agent-analyze", `
  scopes: ${JSON.stringify(scopes.map(s => s.toLowerCase().replace(" ", "-")))}

  For each scope, find issues with:
  - security: Hardcoded secrets, OWASP vulnerabilities (SQL/command injection, XSS, path traversal), CVE patterns, input validation gaps, unsafe deserialization
  - quality: Type errors, missing type hints, tech debt markers, missing tests, test isolation issues, complexity >10, bare excepts, silent failures, missing exception chaining (raise from), dead code, unused imports, missing docstrings on public APIs, magic values/literals, poor naming
  - architecture: SOLID violations, god classes (>300 LOC), circular imports, tight coupling, orphan files, poor separation of concerns, missing abstractions, over-engineering, deep nesting
  - best-practices: Anti-patterns, inefficient algorithms, inconsistent styles, missing context managers, resource leaks, connection cleanup, memory leaks, missing error handling, duplicates, stale refs, hardcoded paths/config, missing logging, N+1 queries, missing caching opportunities

  Return: {
    findings: [{ id: "{SCOPE}-{NNN}", severity: "{P0-P3}", title, location: "{file}:{line}", fixable, approvalRequired, fix }],
    summary: { "{scope}": { count, p0, p1, p2, p3 } }
  }
`, { model: "haiku" })
```

**Parallel Execution:**
- cco-agent-analyze handles parallelization internally
- Returns combined findings for all scopes
- Deduplication handled by agent

### Validation
```
[x] All scope agents launched in parallel
[x] Results merged and deduplicated
[x] Findings sorted by severity
→ Proceed to Step-5
```

---

## Step-5: Show Findings [PROGRESSIVE]

Display findings as analysis completes:

```
## Analysis Results

| Scope | Critical | High | Medium | Low | Auto-fix |
|-------|----------|------|--------|-----|----------|
| Security | {n} | {n} | {n} | {n} | {n} |
| Quality | {n} | {n} | {n} | {n} | {n} |
| Architecture | {n} | {n} | {n} | {n} | {n} |
| Best Practices | {n} | {n} | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

Summary:
- Auto-fixable (LOW risk): {n} items
- Approval required (MEDIUM/HIGH risk): {n} items
```

### Validation
```
[x] Summary displayed to user
→ If action = "Report Only": Skip to Step-9
→ Proceed to Step-6
```

---

## Step-6: Apply Auto-fixes [BACKGROUND]

**Start auto-fix in background while preparing approval questions:**

```javascript
autoFixable = allFindings.filter(f => f.auto_fixable && f.risk === "LOW")

// Launch in background - non-blocking
autoFixTask = Task("cco-agent-apply", `
  fixes: ${JSON.stringify(autoFixable)}
  Apply all auto-fixable items. Verify each fix.
  Group by file for efficiency.
`, { model: "sonnet", run_in_background: true })

// Don't wait - proceed to Step-7 immediately
// Will check autoFixTask.id later for results
```

**Background Pattern:**
- Auto-fixes run while user reviews approval items
- Better UX - no waiting
- Check results before summary

### Validation
```
[x] Background task launched
[x] Task ID saved for later
→ Proceed to Step-7 immediately (don't wait)
```

---

## Step-7: Approval [PARALLEL with Step-6]

**Ask approval while auto-fixes run in background:**

```javascript
approvalRequired = allFindings.filter(f => !f.auto_fixable || f.risk !== "LOW")

// Sort by severity: CRITICAL → HIGH → MEDIUM → LOW
approvalRequired.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity])
```

**Option Batching (max 4 per page):**

| Total Items | Strategy |
|-------------|----------|
| 1-4 | Single page, no "All" option |
| 5-8 | "All" + 3 items, then remaining |
| 9+ | "All" + 3 items per page |

```javascript
// Page 1 (with All option if many items)
AskUserQuestion([{
  question: `Approve fixes? (${approvalRequired.length} items need review)`,
  header: "Approve",
  options: [
    ...(approvalRequired.length > 4 ? [{
      label: `All (${approvalRequired.length})`,
      description: "Apply all - review git diff after"
    }] : []),
    ...approvalRequired.slice(0, approvalRequired.length > 4 ? 3 : 4).map(f => ({
      label: `[${f.severity}] ${f.title}`,
      description: `${f.file}:${f.line} - ${f.fix_description}`
    }))
  ],
  multiSelect: true
}])

// Continue for additional pages if needed
```

### Validation
```
[x] All pages presented
[x] User selections collected
→ Store as: approved = {selections[]}, declined = {unselected[]}
→ Proceed to Step-8
```

---

## Step-8: Apply Approved

```javascript
// First, check background auto-fix status
autoFixResults = await TaskOutput(autoFixTask.id)

// Then apply user-approved items
if (approved.length > 0) {
  Task("cco-agent-apply", `
    fixes: ${JSON.stringify(approved)}
    Apply user-approved items. Verify each fix.
    Handle cascading errors.
  `, { model: "sonnet" })
}
```

### Validation
```
[x] Background auto-fixes completed
[x] Approved fixes applied
[x] Cascading errors handled
→ Proceed to Step-9
```

---

## Step-9: Summary

```
## Optimization Complete

| Category | Count |
|----------|-------|
| Auto-fixed | {n} |
| User-approved | {n} |
| Declined | {n} |
| **Total fixed** | **{n}** |

Files modified: {n}
Run `git diff` to review changes.
Run `git checkout .` to revert all.
```

### Validation
```
[x] Summary displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Output Schema (when called as sub-command)

When called via `/cco-optimize --fix` (e.g., from cco-checkup, cco-preflight):

```json
{
  "accounting": {
    "done": "{n}",
    "declined": "{n}",
    "fail": "{n}",
    "total": "{n}"
  },
  "by_scope": {
    "security": "{n}",
    "quality": "{n}",
    "architecture": "{n}",
    "bestPractices": "{n}"
  },
  "blockers": [{ "severity": "{P0-P1}", "title": "{title}", "location": "{file}:{line}" }]
}
```

**Mapping from agent responses:**
- `accounting` ← `cco-agent-apply.accounting`
- `by_scope` ← grouped count from `cco-agent-analyze.findings`
- `blockers` ← `findings.filter(f => f.severity === "P0" || f.severity === "P1")`

### Scope Coverage

| Scope | Checks |
|-------|--------|
| `security` | Secrets, OWASP (SQL/command injection, XSS, path traversal), CVEs, input validation, unsafe deserialization |
| `quality` | Type errors/hints, tech debt, test gaps/isolation, complexity, bare excepts, silent failures, exception chaining, dead code, unused imports, docstrings, magic values, naming |
| `architecture` | SOLID violations, god classes, circular imports, coupling, orphan files, separation of concerns, abstractions, over-engineering, nesting depth |
| `best-practices` | Anti-patterns, inefficient algorithms, inconsistent styles, context managers, resource/connection leaks, memory leaks, error handling, duplicates, stale refs, hardcoded config, logging, N+1 queries, caching |

### Context Application

| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security scope auto-selected |
| Scale | 10K+ → stricter thresholds |
| Maturity | Legacy → auto-fix only LOW risk |
| Priority | Speed → critical only; Quality → all |

### Model Strategy

| Agent | Model | Reason |
|-------|-------|--------|
| cco-agent-analyze | Haiku | Fast, read-only scanning |
| cco-agent-apply | Sonnet | Accurate code modifications |

### Flags

| Flag | Effect |
|------|--------|
| `--security` | Security scope only |
| `--quality` | Quality scope only |
| `--architecture` | Architecture scope only |
| `--best-practices` | Best practices scope only |
| `--report` | Report only (no fixes) |
| `--fix` | Auto-fix safe (default) |
| `--fix-all` | Fix all with approval |
| `--score` | Quality score only (0-100), no fixes |
| `--critical` | Security + critical severity only |
| `--pre-release` | All scopes, strict thresholds |
| `--sequential` | Disable parallel (debug mode) |

---

## Recovery

If something goes wrong during optimization:

| Situation | Recovery |
|-----------|----------|
| Fix broke something | `git checkout -- {file}` to restore |
| Multiple files affected | `git checkout .` to restore all |
| Want to review | `git diff` to see all changes |
| Stashed at start | `git stash pop` to restore |
| Analysis hung | Re-run - analysis is stateless |
| Partial apply | `git diff` to see progress |

---

## Rules

1. **Use cco-agent-analyze** - Agent handles scope parallelization internally
2. **Use cco-agent-apply** - Agent handles verification and cascading
3. **Background apply** - Auto-fix runs while user reviews
4. **Progressive display** - Show results as analysis completes
5. **Paginated approval** - Max 4 items per AskUserQuestion
