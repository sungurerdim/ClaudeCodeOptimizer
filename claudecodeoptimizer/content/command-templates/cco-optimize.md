---
name: cco-optimize
description: |
  Incremental code improvement - tactical fixes for security, hygiene, types, lint, performance, and AI-generated code issues.
  QUESTION: "This code works. How can it work better?"
  TRIGGERS: "optimize", "fix issues", "security scan", "clean up", "fix all", "improve code"
  USE WHEN: Want to find AND fix code-level issues in one pass
  FLAGS: --auto (unattended), --security, --hygiene, --types, --lint, --performance, --ai-hygiene, --fix-all, --score
  SCOPES: 6 scopes, 63 checks total (SEC-01 to AIH-08)
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(*), Task(*), TodoWrite, AskUserQuestion
model: opus
---

# /cco-optimize

**Incremental Code Improvement** - Quality gates + parallel analysis + background fixes with Fix Intensity selection.

**Philosophy:** "This code works. How can it work better?"

**Purpose:** Tactical, file-level fixes. For strategic architecture assessment, use `/cco-review`.

## Args

- `--auto` or `--unattended`: Fully unattended mode for CI/CD, pre-commit, cron jobs
  - **No questions asked** - all 6 scopes, Full Fix intensity
  - **No progress output** - silent execution
  - **Only final summary** - single status line (machine-readable)
  - Exit codes: 0 (success), 1 (warnings), 2 (failures)
- `--security`: Security scope only (SEC-01 to SEC-12)
- `--hygiene`: Hygiene scope only (HYG-01 to HYG-15)
- `--types`: Types scope only (TYP-01 to TYP-10)
- `--lint`: Lint scope only (LNT-01 to LNT-08)
- `--performance`: Performance scope only (PRF-01 to PRF-10)
- `--ai-hygiene`: AI hygiene scope only (AIH-01 to AIH-08)
- `--report`: Report only, no fixes
- `--fix`: Auto-fix safe items (default)
- `--fix-all`: Full Fix intensity without approval
- `--score`: Quality score only (0-100), skip all questions
- `--intensity=<level>`: Set fix intensity (quick-wins, standard, full-fix, report-only)

**Usage:**
- `/cco-optimize --auto` - Silent full optimization (all scopes, full fix)
- `/cco-optimize --security --fix-all` - Security only, fix all
- `/cco-optimize --ai-hygiene` - Find AI-generated code issues
- `/cco-optimize --score` - Quick quality score

## Core Principle [CRITICAL]

**Fix everything that can be fixed.** Auto-fix safe items, ask approval for risky ones.

## Everything Mode [CRITICAL]

When `--fix-all` or user selects "Everything":
- **Zero deferrals** - no "future iteration", no "later pass", no "lower priority"
- **Zero skips** - every finding must be addressed NOW
- **Complex fixes** - implement them, don't defer them
- **Only exit** - FIXED or TECHNICAL FAILURE (with specific blocker)
- Accounting: `applied + failed = total` (no AI declines allowed)

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`
- Args: $ARGS

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Mode Detection

```javascript
// Parse arguments
const args = "$ARGS"
const isUnattended = args.includes("--auto") || args.includes("--unattended")

// Parse intensity from args
const intensityArg = args.match(/--intensity=(\w+)/)?.[1]

if (isUnattended) {
  // UNATTENDED MODE: CI/CD, pre-commit hooks, cron jobs
  // No TodoWrite, no progress output, no intermediate messages
  // Skip Q1, Q2, Q3 - proceed directly with full scope and full fix

  config = {
    intensity: "full-fix",  // All severities
    scopes: ["security", "hygiene", "types", "lint", "performance", "ai-hygiene"],  // ALL 6 scopes
    action: "Everything",   // No approval needed
    gitState: "Continue anyway"  // Don't stash
  }

  // Execute silently:
  // 1. Run analysis (no output)
  // 2. Apply ALL fixes (no output)
  // 3. Show ONLY final summary line (machine-readable)

  // → Jump directly to Step-2 analysis, skip Q1
}
```

**Severity Thresholds by Intensity:**

| Intensity | Severities Included | Use Case |
|-----------|---------------------|----------|
| quick-wins | "Do Now" bucket (high impact, low effort) | 80/20 fast improvement |
| standard | CRITICAL + HIGH + MEDIUM | Normal operation (default) |
| full-fix | ALL (including LOW) | Comprehensive cleanup |
| report-only | ALL (analysis only) | Review without changes |

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 0 | Quality Gates | Format + Lint + Type + Test (full project) | Parallel background |
| 1 | Setup | Q1: Combined settings (background analysis starts) | Single question |
| 2 | Analyze | Wait for analysis, show findings | Progressive |
| 3 | Auto-fix | Apply safe fixes (background) | Non-blocking |
| 4 | Approval | Q2: Approve remaining (conditional) | Only if needed |
| 5 | Apply | Apply approved fixes | Batched |
| 6 | Summary | Show counts | Instant |

---

## Progress Tracking [SKIP IF --auto]

**If `--auto` flag: Skip TodoWrite entirely. Silent execution.**

```javascript
if (!isUnattended) {
  TodoWrite([
    { content: "Step-0: Run quality gates", status: "in_progress", activeForm: "Running quality gates" },
    { content: "Step-1: Get optimization settings", status: "pending", activeForm: "Getting settings" },
    { content: "Step-2: Run analysis", status: "pending", activeForm: "Running analysis" },
    { content: "Step-3: Apply auto-fixes", status: "pending", activeForm: "Applying auto-fixes" },
    { content: "Step-4: Get approval", status: "pending", activeForm: "Getting approval" },
    { content: "Step-5: Apply approved", status: "pending", activeForm: "Applying approved fixes" },
    { content: "Step-6: Show summary", status: "pending", activeForm: "Showing summary" }
  ])
}
```

---

## Step-0: Quality Gates [PARALLEL BACKGROUND]

**Run format, lint, type check, and tests on FULL PROJECT in parallel:**

```javascript
// Commands from context.md Operational section - FULL PROJECT
formatTask = Bash("{format_command} 2>&1", { run_in_background: true })
lintTask = Bash("{lint_command} 2>&1", { run_in_background: true })
typeTask = Bash("{type_command} 2>&1", { run_in_background: true })
testTask = Bash("{test_command} 2>&1", { run_in_background: true })

// Store task IDs for collection in Step-6
qualityGateTasks = {
  format: formatTask.id,
  lint: lintTask.id,
  type: typeTask.id,
  test: testTask.id
}

// Continue immediately - results collected in Step-6
```

**Key points:**
- Format auto-fixes code style issues
- Lint catches code quality issues
- Type check catches type errors
- Tests verify functionality
- All run in parallel for speed
- Results shown in final summary

### Validation
```
[x] Background tasks launched
→ Proceed to Step-1 immediately
```

---

## Step-1: Setup [Q1: Intensity + Q2: Scopes + BACKGROUND ANALYSIS] [SKIP IF --auto]

**Start analysis in background while asking questions (or immediately if --auto):**

```javascript
// Determine if git is dirty from context
gitDirty = gitStatus.trim().length > 0

// Start analysis with ALL 6 scopes - will filter after Q1/Q2 (or use all if --auto)
// Scopes: security (SEC-01-12), hygiene (HYG-01-15), types (TYP-01-10),
//         lint (LNT-01-08), performance (PRF-01-10), ai-hygiene (AIH-01-08)
analysisTask = Task("cco-agent-analyze", `
  scopes: ["security", "hygiene", "types", "lint", "performance", "ai-hygiene"]

  Find all issues with severity, fix info, and effort/impact scores.
  Return: {
    findings: [{ id, scope, severity, title, location, fixable, approvalRequired, fix, effort, impact }],
    summary: { scope: { count, critical, high, medium, low } }
  }
`, { model: "haiku", run_in_background: true })
```

**UNATTENDED MODE: Skip all questions, use defaults from Mode Detection**

```javascript
if (isUnattended) {
  // config already set in Mode Detection
  // → Proceed directly to Step-2 (no questions)
} else {
  // Interactive mode - ask Q1 (Intensity) + Q2 (Scopes)
```

**Q1: Fix Intensity (first question):**

```javascript
  intensityQuestion = {
    question: "How much to fix?",
    header: "Intensity",
    options: [
      { label: "Quick Wins (80/20)", description: "High impact, low effort only (Do Now bucket)" },
      { label: "Standard (Recommended)", description: "CRITICAL + HIGH + MEDIUM severity" },
      { label: "Full Fix", description: "All severities including LOW (complete cleanup)" },
      { label: "Report Only", description: "Analyze without making any changes" }
    ],
    multiSelect: false
  }
```

**Q2: Scope Selection - Code Quality (4 scopes):**

```javascript
  scopeQuestion1 = {
    question: "Code quality scopes to analyze?",
    header: "Scopes 1/2",
    options: [
      { label: "Security (12)", description: "SEC-01-12: secrets, injection, path traversal" },
      { label: "Hygiene (15)", description: "HYG-01-15: unused code, dead imports, orphans" },
      { label: "Types (10)", description: "TYP-01-10: type errors, annotations, Any usage" },
      { label: "Lint (8)", description: "LNT-01-08: formatting, naming, style" }
    ],
    multiSelect: true
  }
```

**Q3: Scope Selection - Advanced (2 scopes):**

```javascript
  scopeQuestion2 = {
    question: "Advanced scopes to analyze?",
    header: "Scopes 2/2",
    options: [
      { label: "Performance (10)", description: "PRF-01-10: N+1, blocking I/O, caching" },
      { label: "AI Hygiene (8)", description: "AIH-01-08: hallucinations, orphan abstractions" },
      { label: "Skip advanced", description: "Only run code quality scopes selected above" }
    ],
    multiSelect: true
  }
```

**Q4: Git State (conditional, only if dirty):**

```javascript
  questions = [intensityQuestion, scopeQuestion1, scopeQuestion2]

  // Add git state question only if dirty (max 4 questions per AskUserQuestion)
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

  AskUserQuestion(questions)  // Max 4 questions: Intensity + Scopes1 + Scopes2 + GitState
}
```

### Validation
```
[x] User completed Q1 (or skipped if --auto)
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

**Collect results, filter by intensity and scopes:**

```javascript
// Wait for background analysis
allFindings = await TaskOutput(analysisTask.id)

// Map intensity to severity thresholds
const intensityThresholds = {
  "quick-wins": null,  // Special: filter by effort/impact, not severity
  "standard": ["CRITICAL", "HIGH", "MEDIUM"],
  "full-fix": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
  "report-only": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]  // Show all, apply none
}

// Filter by user-selected scopes
selectedScopes = config.scopes.map(s => s.toLowerCase().replace(" ", "-"))
let findings = allFindings.findings.filter(f => selectedScopes.includes(f.scope))

// Filter by intensity
const allowedSeverities = intensityThresholds[config.intensity]
if (config.intensity === "quick-wins") {
  // 80/20 mode: high impact, low effort only
  findings = findings.filter(f => f.impact === "HIGH" && f.effort === "LOW")
} else if (allowedSeverities) {
  findings = findings.filter(f => allowedSeverities.includes(f.severity))
}

// Categorize for fix flow
autoFixable = findings.filter(f => f.fixable && !f.approvalRequired)
approvalRequired = findings.filter(f => f.approvalRequired || !f.fixable)

// In --auto mode: ALL findings are auto-fixable (no approval needed)
if (isUnattended) {
  autoFixable = findings.filter(f => f.fixable)
  approvalRequired = []  // No approval in unattended mode
}

// Report-only mode: nothing to fix
if (config.intensity === "report-only") {
  autoFixable = []
  approvalRequired = []
}

// Track counts at FINDING level (not location level)
counts = {
  total: findings.length,
  autoFixable: autoFixable.length,
  approvalRequired: approvalRequired.length,
  byScope: Object.fromEntries(
    selectedScopes.map(s => [s, findings.filter(f => f.scope === s).length])
  ),
  bySeverity: {
    critical: findings.filter(f => f.severity === "CRITICAL").length,
    high: findings.filter(f => f.severity === "HIGH").length,
    medium: findings.filter(f => f.severity === "MEDIUM").length,
    low: findings.filter(f => f.severity === "LOW").length
  }
}
```

**Display findings progressively (Interactive only):**

```javascript
if (!isUnattended) {
  // Show comprehensive analysis table
```

```
## Analysis Results

**Intensity:** {config.intensity} | **Scopes:** {selectedScopes.length}/6

| Scope | ID Range | Critical | High | Medium | Low | Auto-fix |
|-------|----------|----------|------|--------|-----|----------|
| Security | SEC-01-12 | {n} | {n} | {n} | {n} | {n} |
| Hygiene | HYG-01-15 | {n} | {n} | {n} | {n} | {n} |
| Types | TYP-01-10 | {n} | {n} | {n} | {n} | {n} |
| Lint | LNT-01-08 | {n} | {n} | {n} | {n} | {n} |
| Performance | PRF-01-10 | {n} | {n} | {n} | {n} | {n} |
| AI Hygiene | AIH-01-08 | {n} | {n} | {n} | {n} | {n} |
| **Total** | **63 checks** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

**Severity Distribution:**
- CRITICAL: {counts.bySeverity.critical}
- HIGH: {counts.bySeverity.high}
- MEDIUM: {counts.bySeverity.medium}
- LOW: {counts.bySeverity.low}

**Fix Plan:**
- Auto-fixable (safe): {autoFixable.length} items
- Approval required (risky): {approvalRequired.length} items
- Excluded by intensity: {allFindings.findings.length - findings.length} items
```

```javascript
}
// In --auto mode: No output, proceed silently
```

### Validation
```
[x] Analysis results collected
[x] Findings categorized
→ If action = "Report only": Skip to Step-6
→ If --auto: Skip Q2 (Step-4), apply all fixable
→ Proceed to Step-3
```

---

## Step-3: Auto-fix [BACKGROUND]

**Start auto-fixes in background while preparing approval:**

```javascript
if (config.action !== "Report only" && autoFixable.length > 0) {
  // Determine if fix-all mode
  const isFixAll = config.action.includes("Everything") || isUnattended

  autoFixTask = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(autoFixable)}
    fixAll: ${isFixAll}

    Apply all auto-fixable items. Verify each fix.
    Group by file for efficiency.

    ${isFixAll ? `
    EVERYTHING MODE [MANDATORY]:
    Fix ALL items. Planning metadata (effort/impact/bucket) is for reporting only - ignored here.

    Rules:
    - Zero agent-initiated skips
    - Every item = FIXED or TECHNICAL FAILURE (with "Technical: [reason]")
    - If unsure → ask user, don't skip
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each finding = 1 item, regardless of how many locations it has
    - Example: "Type ignore comments" with 3 locations = 1 finding

    Return accounting at FINDING level:
    { applied: <findings_fixed>, failed: <findings_failed>, total: <findings_attempted> }
  `, { model: "opus", run_in_background: true })
}

// Proceed to Step-4 immediately (auto-fix runs in background)
```

### Validation
```
[x] Background auto-fix launched
→ Proceed to Step-4 immediately
```

---

## Step-4: Approval [Q2 - CONDITIONAL] [SKIP IF --auto]

**Skip entirely if `--auto` flag - all fixable items already being applied.**

**Only ask if there are approval-required items AND action is not "Everything":**

### Pre-Confirmation Display [MANDATORY - Interactive only]

**Display ALL items in approvalRequired BEFORE asking approval question:**

```javascript
// CRITICAL: Display ALL items, not just some severities
console.log(formatApprovalTable(approvalRequired))  // Must show ALL items
```

```markdown
## Issues Requiring Approval

| # | Severity | Issue | Location | Fix |
|---|----------|-------|----------|-----|
{approvalRequired.map((item, i) => `| ${i+1} | [${item.severity}] | ${item.title} | ${item.location} | ${item.fix} |`)}

Total: {approvalRequired.length} issues requiring approval
```

```javascript
// UNATTENDED MODE: Skip approval entirely
if (isUnattended) {
  approved = []  // All fixable items handled in Step-3
  // → Proceed directly to Step-5
} else if (config.action.includes("Everything")) {
  // No approval needed - apply all
  approved = approvalRequired
} else if (approvalRequired.length === 0) {
  // Nothing to approve
  approved = []
} else {
  // Sort by severity: CRITICAL → HIGH → MEDIUM → LOW
  const severityOrder = { "CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3 }
  approvalRequired.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity])

  // Display issues table BEFORE question
  console.log(formatIssuesTable(approvalRequired))

  // Build approval question with pagination
  const PAGE_SIZE = 4
  let currentPage = 0
  let allApproved = []

  while (currentPage * PAGE_SIZE < approvalRequired.length) {
    const startIdx = currentPage * PAGE_SIZE
    const pageItems = approvalRequired.slice(startIdx, startIdx + PAGE_SIZE)
    const remaining = approvalRequired.length - startIdx - pageItems.length

    options = []

    // "All" option only on first page if more than PAGE_SIZE items
    if (currentPage === 0 && approvalRequired.length > PAGE_SIZE) {
      options.push({
        label: `All (${approvalRequired.length})`,
        description: "Apply all - review git diff after"
      })
    }

    // Add page items
    pageItems.forEach(f => {
      options.push({
        label: `[${f.severity}] ${f.title}`,
        description: `${f.location} - ${f.fix?.substring(0, 50)}...`
      })
    })

    const pageInfo = approvalRequired.length > PAGE_SIZE
      ? ` (page ${currentPage + 1}/${Math.ceil(approvalRequired.length / PAGE_SIZE)})`
      : ""

    const response = AskUserQuestion([{
      question: `Approve fixes${pageInfo}?`,
      header: "Approve",
      options: options,
      multiSelect: true
    }])

    // Handle response
    if (response.includes("All")) {
      allApproved = approvalRequired
      break  // Exit pagination loop
    }

    // Add selected to approved (unselected are simply not processed)
    pageItems.forEach(item => {
      if (response.includes(item.title)) {
        allApproved.push(item)
      }
      // Unselected items are not tracked - they're simply not processed
    })

    // If no more pages or user selected nothing (implicit "done"), exit
    if (remaining === 0) break
    currentPage++
  }

  approved = allApproved
}
```

### Validation
```
[x] Approval collected (or skipped)
→ Store as: approved = {selections[]}
→ Unselected items are not processed (no "declined" category)
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
  // In fix-all mode, all approval-required items are also auto-approved
  const isFixAll = config.action.includes("Everything") || isUnattended

  approvedResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(approved)}
    fixAll: ${isFixAll}

    Apply user-approved items. Verify each fix.
    Handle cascading errors.

    ${isFixAll ? `
    EVERYTHING MODE [MANDATORY]:
    Fix ALL items. Planning metadata (effort/impact/bucket) is for reporting only - ignored here.

    Rules:
    - Zero agent-initiated skips
    - Every item = FIXED or TECHNICAL FAILURE (with "Technical: [reason]")
    - If unsure → ask user, don't skip
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each finding = 1 item, regardless of how many locations it has

    Return accounting at FINDING level:
    { applied: <findings_fixed>, failed: <findings_failed>, total: <findings_attempted> }
  `, { model: "opus" })
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

### Collect Quality Gate Results

```javascript
// Collect quality gate results from Step-0
formatResults = await TaskOutput(qualityGateTasks.format)
lintResults = await TaskOutput(qualityGateTasks.lint)
typeResults = await TaskOutput(qualityGateTasks.type)
testResults = await TaskOutput(qualityGateTasks.test)

qualityGateStatus = {
  format: formatResults.exitCode === 0 ? "OK" : "FIXED",
  lint: lintResults.exitCode === 0 ? "OK" : "WARN",
  type: typeResults.exitCode === 0 ? "OK" : "FAIL",
  test: testResults.exitCode === 0 ? "OK" : "FAIL"
}
```

### Calculate Final Counts [CRITICAL]

```javascript
// COUNTING STANDARD
// - total: all findings in selected intensity scope
// - applied: successfully fixed
// - failed: couldn't fix (technical reason required)
//
// Invariant: applied + failed = total
// NOTE: No "declined" category - AI has no option to decline. Fix or fail with reason.

// Auto-fixed findings (from Step-3)
autoFixedCount = autoFixResults?.accounting?.applied || 0
autoFixFailedCount = autoFixResults?.accounting?.failed || 0

// Verify: auto-fix accounting
assert(autoFixedCount + autoFixFailedCount === autoFixable.length,
  `Auto-fix mismatch: ${autoFixedCount} + ${autoFixFailedCount} != ${autoFixable.length}`)

// User-approved findings (from Step-5)
approvedFixedCount = approvedResults?.accounting?.applied || 0
approvedFailedCount = approvedResults?.accounting?.failed || 0

// Verify: approved accounting (if approval was requested)
if (approved.length > 0) {
  assert(approvedFixedCount + approvedFailedCount === approved.length,
    `Approved mismatch: ${approvedFixedCount} + ${approvedFailedCount} != ${approved.length}`)
}

// Final accounting
finalCounts = {
  applied: autoFixedCount + approvedFixedCount,
  failed: autoFixFailedCount + approvedFailedCount,
  total: autoFixable.length + approved.length  // Only items attempted
}

// Final verification - these MUST balance
assert(finalCounts.applied + finalCounts.failed === finalCounts.total,
  "Count mismatch: applied + failed must equal total")
```

### Unattended Mode Output [--auto]

**Single line summary only:**

```javascript
if (isUnattended) {
  // Quality gates status
  const gateStatus = Object.values(qualityGateStatus).includes("FAIL") ? "FAIL" : "OK"

  // ONLY output - single status line
  const status = (finalCounts.failed > 0 || gateStatus === "FAIL") ? "WARN" : "OK"
  console.log(`cco-optimize: ${status} | Fixed: ${finalCounts.applied} | Failed: ${finalCounts.failed} | Gates: ${gateStatus} | Scopes: all`)
  // No tables, no details, no stash reminder
  return
}
```

### Interactive Mode Output

```javascript
// Build summary with quality gates and conditional stash reminder
let summary = `
## Optimization Complete

### Quality Gates (Full Project)

| Gate | Status |
|------|--------|
| Format | ${qualityGateStatus.format} |
| Lint | ${qualityGateStatus.lint} |
| Type Check | ${qualityGateStatus.type} |
| Tests | ${qualityGateStatus.test} |

### Code Analysis

| Metric | Value |
|--------|-------|
| Auto-fixed | ${autoFixedCount} |
| User-approved | ${approvedFixedCount} |
| Failed | ${finalCounts.failed} |
| **Total** | **${finalCounts.total}** |

Status: ${finalCounts.failed > 0 ? "WARN" : "OK"} | Applied: ${finalCounts.applied} | Failed: ${finalCounts.failed} | Total: ${finalCounts.total}

Run \`git diff\` to review changes.`

// Stash reminder if user chose "Stash first"
if (config.gitState === "Stash first") {
  summary += `

**Reminder:** Changes were stashed before optimization. Run \`git stash pop\` to restore them.`
}

console.log(summary)
```

### Validation
```
[x] Summary displayed (single line if --auto, full if interactive)
[x] All todos marked completed (skipped if --auto)
→ Done
```

---

## Reference

### Question Flow Summary

| Scenario | Q1 | Q2 | Total |
|----------|----|----|-------|
| **--auto mode** | - | - | **0 questions** |
| Clean git, has approval items | 2 tabs | 1 tab | 2 questions |
| Dirty git, has approval items | 3 tabs | 1 tab | 2 questions |
| Clean git, no approval items | 2 tabs | - | 1 question |
| Report only mode | 2-3 tabs | - | 1 question |
| Everything mode | 2-3 tabs | - | 1 question |

### Output Schema (when called as sub-command)

**All counts are at FINDING level (not location level).**

```json
{
  "accounting": {
    "applied": "{n}",
    "failed": "{n}",
    "total": "{n}"
  },
  "intensity": "{quick-wins|standard|full-fix|report-only}",
  "by_scope": {
    "security": "{n}",
    "hygiene": "{n}",
    "types": "{n}",
    "lint": "{n}",
    "performance": "{n}",
    "ai-hygiene": "{n}"
  },
  "by_severity": {
    "critical": "{n}",
    "high": "{n}",
    "medium": "{n}",
    "low": "{n}"
  },
  "blockers": [{ "id": "{SEC-01|...}", "severity": "{CRITICAL|HIGH}", "title": "{title}", "location": "{file}:{line}" }]
}
```

**Accounting invariant:** `applied + failed = total`

### Scope Coverage (6 Scopes, 63 Checks)

| Scope | ID Range | Checks |
|-------|----------|--------|
| `security` | SEC-01-12 | Hardcoded secrets, SQL/command injection, path traversal, unsafe deserialization, input validation, cleartext logging, insecure temp files, missing HTTPS, eval/exec, debug endpoints, weak crypto |
| `hygiene` | HYG-01-15 | Unused imports/vars/functions, dead code, orphan files, duplicate blocks, stale TODOs, empty files, commented code, line endings, whitespace, indentation, missing __init__.py, circular imports, bare except |
| `types` | TYP-01-10 | Type errors (mypy/pyright), missing return types, untyped args, type:ignore without reason, Any in APIs, missing generics, union vs literal, optional handling, narrowing opportunities, override signatures |
| `lint` | LNT-01-08 | Format violations, import order, line length, naming conventions, docstring format, magic numbers, string literals, quote style |
| `performance` | PRF-01-10 | N+1 patterns, list on iterator, missing cache, blocking in async, large file reads, missing pagination, string concat loops, unnecessary copies, missing pooling, sync in hot paths |
| `ai-hygiene` | AIH-01-08 | Hallucinated APIs, orphan abstractions, phantom imports, dead feature flags, stale mocks, incomplete implementations, copy-paste artifacts, dangling references |

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
| `--auto` | **Unattended mode:** all 6 scopes, full-fix intensity, no questions, silent execution, single-line summary |
| `--security` | Security scope only (SEC-01-12) |
| `--hygiene` | Hygiene scope only (HYG-01-15) |
| `--types` | Types scope only (TYP-01-10) |
| `--lint` | Lint scope only (LNT-01-08) |
| `--performance` | Performance scope only (PRF-01-10) |
| `--ai-hygiene` | AI hygiene scope only (AIH-01-08) |
| `--report` | Report only, analyze without fixing |
| `--fix` | Standard intensity (default) |
| `--fix-all` | Full-fix intensity, no approval needed |
| `--score` | Quality score only (0-100), skip all questions |
| `--intensity=<level>` | Set fix intensity: quick-wins, standard, full-fix, report-only |
| `--pre-release` | All scopes, standard intensity, strict thresholds |

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
7. **Counting consistency** - Count findings, not locations

---

## Reasoning Strategies

### Step-Back (Before Analysis)
Ask broader question before diving into code:

| Scope | Step-Back Question |
|-------|-------------------|
| Security | "What are the trust boundaries in this codebase?" |
| Quality | "What are the quality standards for this project?" |
| Hygiene | "What is considered 'dead' in this context?" |
| Best Practices | "What patterns does this project follow?" |

### Chain of Thought (Each Finding)
```
1. Identify: What exactly is the issue?
2. Impact: Who/what is affected?
3. Evidence: What confirms this assessment?
4. Severity: Based on evidence, what level?
```

### Self-Consistency (CRITICAL Only)
For CRITICAL severity findings, validate with multiple reasoning paths:
```
Path A: Analyze as if this is a real security/quality issue
Path B: Analyze as if this might be intentional or acceptable
Consensus: Both agree → confirm CRITICAL. Disagree → downgrade to HIGH
```

---

## Anti-Overengineering Guard

Before flagging ANY finding:
1. Does this actually break something or pose a risk?
2. Does this cause real problems for developers/users?
3. Is fixing it worth the effort and potential side effects?

**All NO → not a finding.**

NON-findings:
- Unused import in a file being actively developed
- Missing type hint on internal helper
- Code style preference that doesn't affect functionality

---

## Severity Definitions

| Severity | Criteria |
|----------|----------|
| CRITICAL | Security vulnerability, data loss risk, broken functionality |
| HIGH | Significant bug, type error, missing validation |
| MEDIUM | Code smell, minor type issue, suboptimal pattern |
| LOW | Style, naming, nice-to-have improvement |

**When uncertain → choose lower severity.**

---

## Accounting

**Invariant:** `applied + failed = total` (count findings, not locations)

**No "declined" category:** AI has no option to decline fixes. If it's technically possible and user asked for it, it MUST be done. Only "failed" with specific technical reason is acceptable.
