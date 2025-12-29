---
name: cco-optimize
description: Security and code quality analysis with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(*), Task(*), TodoWrite, AskUserQuestion
model: opus
---

# /cco-optimize

**Full-Stack Optimization** - Quality gates + parallel analysis + background fixes with minimal questions.

## Args

- `--auto` or `--unattended`: Fully unattended mode for CI/CD and benchmarks
  - **No questions asked** - full scope, fix all
  - **No progress output** - silent execution
  - **Only final summary** - single status line at end
  - Defaults:
    - Scopes: ALL (security, quality, hygiene, best-practices)
    - Action: Fix all (no approval needed)
    - Git state: Continue anyway
- `--security`: Security scope only
- `--quality`: Quality scope only
- `--report`: Report only, no fixes
- `--fix`: Auto-fix safe items (default)
- `--fix-all`: Fix all without approval
- `--score`: Quality score only (0-100), skip all questions
- `--pre-release`: All scopes, strict thresholds

**Usage:**
- `/cco-optimize --auto` - Silent full optimization, fix everything
- `/cco-optimize --security --fix-all` - Security only, fix all
- `/cco-optimize --score` - Quick quality score

## Core Principle [CRITICAL]

**Fix everything that can be fixed.** All issues fall into:
1. **Auto-fix**: Safe to apply without asking (background)
2. **Approval Required**: Ask user, then fix if approved

## Fix-All Behavior [CRITICAL]

When `--fix-all` flag OR "Fix all" action is selected:

**MANDATORY:**
1. **Zero Skipping**: Agent MUST NOT skip, decline, or defer ANY finding
2. **No Self-Declining**: Agent cannot decide a fix is "too complex" - that's user's decision
3. **Ask for Complex**: If fix requires significant refactoring (>50 lines changed), ASK user:
   ```javascript
   AskUserQuestion([{
     question: `Fix "${finding.title}" requires significant changes (~${estimatedLines} lines). Proceed?`,
     header: "Complex Fix",
     options: [
       { label: "Yes, apply fix (Recommended)", description: "Agent will implement the fix" },
       { label: "Skip this one", description: "Move to next finding" }
     ],
     multiSelect: false
   }])
   ```
4. **Only Technical Impossibility**: Only skip if technically impossible (e.g., missing dependency, file locked)
5. **Report All Skips**: Any skipped item MUST appear in failed count with clear reason

**Accounting in Fix-All Mode:**
```javascript
// In fix-all mode: declined should always be 0
// User explicitly chose "fix all" - no agent-initiated declines
if (config.action === "Fix all") {
  assert(declined.length === 0, "Fix-all mode: agent should not decline items")
}
```

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

if (isUnattended) {
  // SILENT MODE: No TodoWrite, no progress output, no intermediate messages
  // Skip Q1, Q2 - proceed directly with full scope and fix all

  config = {
    scopes: ["security", "quality", "hygiene", "best-practices"],  // ALL scopes
    action: "Fix all",                                              // No approval needed
    gitState: "Continue anyway"                                     // Don't stash
  }

  // Execute silently:
  // 1. Run analysis (no output)
  // 2. Apply ALL fixes (no output)
  // 3. Show ONLY final summary line

  // → Jump directly to Step-2 analysis, skip Q1
}
```

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

## Step-1: Setup [Q1 + BACKGROUND ANALYSIS] [SKIP Q1 IF --auto]

**Start analysis in background while asking Q1 (or immediately if --auto):**

```javascript
// Determine if git is dirty from context
gitDirty = gitStatus.trim().length > 0

// Start analysis with all scopes - will filter after Q1 (or use all if --auto)
// Scopes: security (OWASP, secrets), quality (complexity, types), hygiene (dead code, orphans), best-practices (patterns)
analysisTask = Task("cco-agent-analyze", `
  scopes: ["security", "quality", "hygiene", "best-practices"]

  Find all issues with severity and fix information.
  Return: {
    findings: [{ id, scope, severity, title, location, fixable, approvalRequired, fix }],
    summary: { scope: { count, p0, p1, p2, p3 } }
  }
`, { model: "haiku", run_in_background: true })
```

**UNATTENDED MODE: Skip Q1, use defaults from Mode Detection**

```javascript
if (isUnattended) {
  // config already set in Mode Detection
  // → Proceed directly to Step-2 (no Q1)
} else {
  // Interactive mode - ask Q1
```

**Build Q1 dynamically based on git state (Interactive only):**

```javascript
  questions = [
    {
      question: "What to optimize?",
      header: "Scope",
      options: [
        { label: "Security (Recommended)", description: "OWASP, secrets, CVEs, input validation" },
        { label: "Quality", description: "Complexity, type errors, code smells" },
        { label: "Hygiene", description: "Dead code, unused imports, orphan files" },
        { label: "Best Practices", description: "Error handling, naming, patterns" }
      ],
      multiSelect: true
    },
    {
      question: "Action mode?",
      header: "Action",
      options: [
        { label: "Auto-fix safe (Recommended)", description: "Fix LOW risk, ask for others" },
        { label: "Fix all", description: "Fix everything, no approval needed" },
        { label: "Report only", description: "Show findings without fixing" }
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

**Collect results and filter by selected scopes:**

```javascript
// Wait for background analysis
allFindings = await TaskOutput(analysisTask.id)

// Filter by user-selected scopes (all scopes if --auto)
selectedScopes = config.scopes.map(s => s.toLowerCase().replace(" ", "-"))
findings = allFindings.findings.filter(f => selectedScopes.includes(f.scope))

// Categorize
autoFixable = findings.filter(f => f.fixable && !f.approvalRequired)
approvalRequired = findings.filter(f => f.approvalRequired || !f.fixable)

// In --auto mode: ALL findings are auto-fixable (no approval needed)
if (isUnattended) {
  autoFixable = findings.filter(f => f.fixable)
  approvalRequired = []  // No approval in unattended mode
}

// Track counts at FINDING level (not location level)
// These counts MUST be used consistently through summary
counts = {
  total: findings.length,
  autoFixable: autoFixable.length,
  approvalRequired: approvalRequired.length
}
```

**Display findings progressively (Interactive only):**

```javascript
if (!isUnattended) {
  // Show analysis table only in interactive mode
```

```
## Analysis Results

| Scope | Critical | High | Medium | Low | Auto-fix |
|-------|----------|------|--------|-----|----------|
| Security | {n} | {n} | {n} | {n} | {n} |
| Quality | {n} | {n} | {n} | {n} | {n} |
| Hygiene | {n} | {n} | {n} | {n} | {n} |
| Best Practices | {n} | {n} | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

Summary:
- Auto-fixable (LOW risk): {autoFixable.length} items
- Approval required: {approvalRequired.length} items
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
  const isFixAll = config.action === "Fix all" || isUnattended

  autoFixTask = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(autoFixable)}
    fixAll: ${isFixAll}

    Apply all auto-fixable items. Verify each fix.
    Group by file for efficiency.

    ${isFixAll ? `
    CRITICAL - FIX-ALL MODE:
    - Zero agent-initiated skips/declines allowed
    - Only technical impossibilities can be marked as "fail"
    - Every fail must have reason starting with "Technical:"
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

**Only ask if there are approval-required items AND action is not "Fix all":**

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
  declined = []
  // → Proceed directly to Step-5
} else if (config.action === "Fix all") {
  // No approval needed - apply all
  approved = approvalRequired
} else if (approvalRequired.length === 0) {
  // Nothing to approve
  approved = []
} else {
  // Sort by severity: P0 → P1 → P2 → P3
  approvalRequired.sort((a, b) => a.severity.localeCompare(b.severity))

  // Display issues table BEFORE question
  console.log(formatIssuesTable(approvalRequired))

  // Build approval question with pagination
  const PAGE_SIZE = 4
  let currentPage = 0
  let allApproved = []
  let allDeclined = []

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
      allDeclined = []
      break  // Exit pagination loop
    }

    // Add selected to approved, rest to declined
    pageItems.forEach(item => {
      if (response.includes(item.title)) {
        allApproved.push(item)
      } else {
        allDeclined.push(item)
      }
    })

    // If no more pages or user selected nothing (implicit "done"), exit
    if (remaining === 0) break
    currentPage++
  }

  approved = allApproved
  declined = allDeclined
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
  // In fix-all mode, all approval-required items are also auto-approved
  const isFixAll = config.action === "Fix all" || isUnattended

  approvedResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(approved)}
    fixAll: ${isFixAll}

    Apply user-approved items. Verify each fix.
    Handle cascading errors.

    ${isFixAll ? `
    CRITICAL - FIX-ALL MODE:
    - Zero agent-initiated skips/declines allowed
    - Only technical impossibilities can be marked as "fail"
    - Every fail must have reason starting with "Technical:"
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
// - total: all findings from analysis (autoFixable + approvalRequired)
// - applied: successfully fixed (autoFixed + approvedFixed)
// - declined: user explicitly declined in Q2 approval
// - failed: couldn't fix (autoFailed + approvedFailed)
//
// Invariants:
// 1. autoFixable.length = autoFixedCount + autoFixFailedCount
// 2. approved.length = approvedFixedCount + approvedFailedCount
// 3. approvalRequired.length = approved.length + declined.length
// 4. applied + declined + failed = total

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
  declined: declined.length,
  failed: autoFixFailedCount + approvedFailedCount,
  total: counts.total  // From Step-2, MUST match Analysis Results total
}

// Final verification - these MUST balance
assert(finalCounts.applied + finalCounts.declined + finalCounts.failed === finalCounts.total,
  "Count mismatch: applied + declined + failed must equal total from analysis")
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
| Declined | ${finalCounts.declined} |
| Failed | ${finalCounts.failed} |
| **Total findings** | **${finalCounts.total}** |

Status: ${finalCounts.failed > 0 ? "WARN" : "OK"} | Applied: ${finalCounts.applied} | Declined: ${finalCounts.declined} | Failed: ${finalCounts.failed} | Total: ${finalCounts.total}

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
| Fix all mode | 2-3 tabs | - | 1 question |

### Output Schema (when called as sub-command)

**All counts are at FINDING level (not location level).**

```json
{
  "accounting": {
    "applied": "{n}",
    "declined": "{n}",
    "failed": "{n}",
    "total": "{n}"
  },
  "by_scope": {
    "security": "{n}",
    "quality": "{n}",
    "hygiene": "{n}",
    "bestPractices": "{n}"
  },
  "blockers": [{ "severity": "{CRITICAL|HIGH}", "title": "{title}", "location": "{file}:{line}" }]
}
```

**Accounting invariant:** `applied + declined + failed = total`

### Scope Coverage

| Scope | Checks |
|-------|--------|
| `security` | Secrets, OWASP, CVEs, input validation, unsafe deserialization |
| `quality` | Type errors, tech debt, test gaps, complexity, dead code |
| `hygiene` | Orphans, stale refs, duplicates, unused imports, dead code |
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
| `--auto` | **Unattended mode:** all scopes, fix all, no questions, silent execution, single-line summary |
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
7. **Counting consistency** - See Counting Principle in cco-tools.md

---

## Counting Principle

**Reference:** See `cco-tools.md` → Counting Principle for full rules.

**This command uses:** `applied + declined + failed = total`

```javascript
// Optimize-specific accounting:
findingsApplied = autoFixable.length + approved.length  // Fixed findings
findingsDeclined = declined.length                      // User declined
findingsFailed = failedFindings.length                  // Could not fix

// Invariant: applied + declined + failed = total
assert(findingsApplied + findingsDeclined + findingsFailed === findingsTotal)
```
