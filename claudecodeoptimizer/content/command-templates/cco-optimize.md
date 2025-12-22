---
name: cco-optimize
description: Security and code quality analysis with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(ruff:*), Bash(mypy:*), Bash(pip:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-optimize

**Full-Stack Optimization** - Parallel analysis + background fixes with minimal questions.

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
| 1 | Setup | Q1: Combined settings (background analysis starts) | Single question |
| 2 | Analyze | Wait for analysis, show findings | Progressive |
| 3 | Auto-fix | Apply safe fixes (background) | Non-blocking |
| 4 | Approval | Q2: Approve remaining (conditional) | Only if needed |
| 5 | Apply | Apply approved fixes | Batched |
| 6 | Summary | Show counts | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Get optimization settings", status: "in_progress", activeForm: "Getting settings" },
  { content: "Step-2: Run analysis", status: "pending", activeForm: "Running analysis" },
  { content: "Step-3: Apply auto-fixes", status: "pending", activeForm: "Applying auto-fixes" },
  { content: "Step-4: Get approval", status: "pending", activeForm: "Getting approval" },
  { content: "Step-5: Apply approved", status: "pending", activeForm: "Applying approved fixes" },
  { content: "Step-6: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Setup [Q1 + BACKGROUND ANALYSIS]

**Start analysis in background while asking Q1:**

```javascript
// Determine if git is dirty from context
gitDirty = gitStatus.trim().length > 0

// Start analysis with all scopes - will filter after Q1
analysisTask = Task("cco-agent-analyze", `
  scopes: ["security", "quality", "architecture", "best-practices"]

  Find all issues with severity and fix information.
  Return: {
    findings: [{ id, scope, severity, title, location, fixable, approvalRequired, fix }],
    summary: { scope: { count, p0, p1, p2, p3 } }
  }
`, { model: "haiku", run_in_background: true })
```

**Build Q1 dynamically based on git state:**

```javascript
questions = [
  {
    question: "What to optimize?",
    header: "Scope",
    options: [
      { label: "Security (Recommended)", description: "OWASP, secrets, CVEs, input validation" },
      { label: "Quality", description: "Tech debt, type errors, test gaps" },
      { label: "Architecture", description: "SOLID violations, coupling, patterns" },
      { label: "Best Practices", description: "Resource management, consistency" }
    ],
    multiSelect: true
  },
  {
    question: "Action mode?",
    header: "Action",
    options: [
      { label: "Auto-fix safe (Recommended)", description: "Fix LOW risk, ask for others" },
      { label: "Report only", description: "Show findings without fixing" },
      { label: "Fix all", description: "Fix everything, no approval needed" }
    ],
    multiSelect: false
  }
]

// Add git state tab only if dirty
if (gitDirty) {
  questions.push({
    question: "Working tree has uncommitted changes. How to proceed?",
    header: "Git State",
    options: [
      { label: "Continue anyway (Recommended)", description: "Proceed, changes visible in git diff" },
      { label: "Stash first", description: "Stash changes, continue, remind to pop" },
      { label: "Cancel", description: "Abort optimization" }
    ],
    multiSelect: false
  })
}

AskUserQuestion(questions)
```

### Validation
```
[x] User completed Q1
→ Store as: config = { scopes, action, gitState? }
→ If gitState = "Cancel": Exit
→ If gitState = "Stash first": Run git stash
→ If action = "Report only": Skip Steps 3-5
→ Proceed to Step-2
```

---

## Step-Score: Quality Score [OPTIONAL]

**When `--score` flag is used, skip all steps and show score only:**

```javascript
agentResponse = Task("cco-agent-analyze", `
  scopes: ["scan"]
  Calculate overall quality score (0-100).
`, { model: "haiku" })

// Output score and exit
console.log(`## Quality Score: ${agentResponse.scores.overall}/100`)
```

→ Exit after showing score

---

## Step-2: Analyze [WAIT FOR BACKGROUND]

**Collect results and filter by selected scopes:**

```javascript
// Wait for background analysis
allFindings = await TaskOutput(analysisTask.id)

// Filter by user-selected scopes
selectedScopes = config.scopes.map(s => s.toLowerCase().replace(" ", "-"))
findings = allFindings.findings.filter(f => selectedScopes.includes(f.scope))

// Categorize
autoFixable = findings.filter(f => f.fixable && !f.approvalRequired)
approvalRequired = findings.filter(f => f.approvalRequired || !f.fixable)
```

**Display findings progressively:**

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
- Auto-fixable (LOW risk): {autoFixable.length} items
- Approval required: {approvalRequired.length} items
```

### Validation
```
[x] Analysis results collected
[x] Findings categorized
→ If action = "Report only": Skip to Step-6
→ Proceed to Step-3
```

---

## Step-3: Auto-fix [BACKGROUND]

**Start auto-fixes in background while preparing approval:**

```javascript
if (config.action !== "Report only" && autoFixable.length > 0) {
  autoFixTask = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(autoFixable)}
    Apply all auto-fixable items. Verify each fix.
    Group by file for efficiency.
  `, { model: "sonnet", run_in_background: true })
}

// Don't wait - proceed to Step-4 immediately
```

### Validation
```
[x] Background auto-fix launched
→ Proceed to Step-4 immediately
```

---

## Step-4: Approval [Q2 - CONDITIONAL]

**Only ask if there are approval-required items AND action is not "Fix all":**

```javascript
if (config.action === "Fix all") {
  // No approval needed - apply all
  approved = approvalRequired
} else if (approvalRequired.length === 0) {
  // Nothing to approve
  approved = []
} else {
  // Sort by severity: P0 → P1 → P2 → P3
  approvalRequired.sort((a, b) => a.severity.localeCompare(b.severity))

  // Build approval question with batching
  options = []

  if (approvalRequired.length > 3) {
    options.push({
      label: `All (${approvalRequired.length})`,
      description: "Apply all - review git diff after"
    })
  }

  // Add individual items (max 3 if "All" shown, max 4 otherwise)
  const maxItems = approvalRequired.length > 3 ? 3 : 4
  approvalRequired.slice(0, maxItems).forEach(f => {
    options.push({
      label: `[${f.severity}] ${f.title}`,
      description: `${f.location} - ${f.fix?.substring(0, 50)}...`
    })
  })

  AskUserQuestion([{
    question: `Approve fixes? (${approvalRequired.length} items need review)`,
    header: "Approve",
    options: options,
    multiSelect: true
  }])

  // If more than 4 items and not "All" selected, continue with more pages
  // (handled by batching logic in execution)
}
```

### Validation
```
[x] Approval collected (or skipped)
→ Store as: approved = {selections[]}, declined = {unselected[]}
→ Proceed to Step-5
```

---

## Step-5: Apply Approved

**Wait for auto-fix and apply approved items:**

```javascript
// First, check background auto-fix status
if (autoFixTask) {
  autoFixResults = await TaskOutput(autoFixTask.id)
}

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
→ Proceed to Step-6
```

---

## Step-6: Summary

```
## Optimization Complete

| Category | Count |
|----------|-------|
| Auto-fixed | {autoFixResults?.accounting?.done || 0} |
| User-approved | {approved.length} |
| Declined | {declined.length} |
| **Total fixed** | **{totalFixed}** |

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

### Question Flow Summary

| Scenario | Q1 | Q2 | Total |
|----------|----|----|-------|
| Clean git, has approval items | 2 tabs | 1 tab | 2 questions |
| Dirty git, has approval items | 3 tabs | 1 tab | 2 questions |
| Clean git, no approval items | 2 tabs | - | 1 question |
| Report only mode | 2-3 tabs | - | 1 question |
| Fix all mode | 2-3 tabs | - | 1 question |

### Output Schema (when called as sub-command)

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

### Scope Coverage

| Scope | Checks |
|-------|--------|
| `security` | Secrets, OWASP, CVEs, input validation, unsafe deserialization |
| `quality` | Type errors, tech debt, test gaps, complexity, dead code |
| `architecture` | SOLID violations, god classes, circular imports, coupling |
| `best-practices` | Anti-patterns, resource leaks, inconsistent styles |

### Context Application

| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security scope recommended |
| Scale | 10K+ → stricter thresholds |
| Maturity | Legacy → auto-fix only LOW risk |
| Priority | Speed → critical only; Quality → all |

### Flags

| Flag | Effect |
|------|--------|
| `--security` | Security scope only, skip Q1 scope tab |
| `--quality` | Quality scope only, skip Q1 scope tab |
| `--report` | Report only, skip Q1 action tab |
| `--fix` | Auto-fix safe (default) |
| `--fix-all` | Fix all without approval |
| `--score` | Quality score only (0-100), skip all questions |
| `--pre-release` | All scopes, strict thresholds |

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Fix broke something | `git checkout -- {file}` |
| Multiple files affected | `git checkout .` |
| Want to review | `git diff` |
| Stashed at start | `git stash pop` |

---

## Rules

1. **Background analysis** - Start analysis while asking Q1
2. **Max 2 questions** - Q1 settings, Q2 approval (if needed)
3. **Dynamic tabs** - Git State tab only if dirty
4. **Background auto-fix** - Run while user reviews approval
5. **Single Recommended** - Each tab has one recommended option
6. **Paginated approval** - Max 4 items per question
