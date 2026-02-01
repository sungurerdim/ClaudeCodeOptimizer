---
description: Incremental code improvement - fix security, hygiene, types, lint, performance issues
argument-hint: "[--auto] [--preview] [--scope=<name>]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, Skill, AskUserQuestion
model: opus
---

# /cco:optimize

**Incremental Code Improvement** - Quality gates + parallel analysis + background fixes with Fix Intensity selection.

> **Implementation Note:** Code blocks use JavaScript-like pseudocode for clarity. Actual execution uses Claude Code tools with appropriate parameters.

> **Standard Flow:** This command follows the standard CCO execution pattern:
> Setup → Analyze → Gate → Plan → Apply → Summary (see docs/philosophy.md for rationale)

**Philosophy:** "This code works. How can it work better?"

**Purpose:** Tactical, file-level fixes. For strategic architecture assessment, use `/cco:align`.

## Args

- `--auto`: Fully unattended mode for CI/CD, pre-commit, cron jobs
  - **No questions asked** - all 10 scopes, all severities
  - **No progress output** - silent execution
  - **Only final summary** - single status line (machine-readable)
  - Exit codes: 0 (success), 1 (warnings), 2 (failures)
- `--preview`: Analyze and report findings without applying fixes (includes quality score)
- `--scope=<name>`: Run specific scope only. Valid names: security, hygiene, types, lint, performance, ai-hygiene, robustness, privacy, doc-sync, simplify

**Usage:**
- `/cco:optimize --auto` - Silent full optimization (all scopes, full fix)
- `/cco:optimize --scope=security --auto` - Security only, fix all
- `/cco:optimize --scope=ai-hygiene` - Find AI-generated code issues
- `/cco:optimize --preview` - Report findings without fixing (includes quality score)

## Core Principle [CRITICAL]

**Fix everything that can be fixed.** Auto-fix safe items, ask approval for risky ones.

## Fixable Definition [CRITICAL]

A finding is **FIXABLE** if ALL conditions are met:
1. **Single file change** - No cross-file refactoring required
2. **No API contract change** - No breaking changes to public interfaces
3. **No new dependencies** - No npm install/pip install required
4. **Deterministic fix** - Not subjective (clear right answer exists)

### Examples

| Finding | Fixable? | Reason |
|---------|----------|--------|
| Remove unused import | YES | Single file, deterministic |
| Add missing type annotation | YES | Single file, deterministic |
| Replace print() with logger | YES | Single file, deterministic |
| Fix SQL injection | YES | Single file, deterministic pattern |
| Refactor god class | NO | Multiple files, subjective structure |
| Change API response format | NO | Breaking change |
| Add input validation | YES | Single file, deterministic (schema exists) |
| Switch from sync to async | NO | Cross-file changes, architecture decision |

### Auto-fix vs Approval Required

| Category | Auto-fix? | Why |
|----------|-----------|-----|
| Unused imports/vars | Yes | Zero risk, deterministic |
| Type annotations | Yes | Zero risk, tooling validates |
| Formatting | Yes | Zero risk, deterministic |
| Missing validation | Approval | Logic change, needs review |
| Security fixes | Approval | High impact, needs review |
| Refactoring | Approval | Subjective, needs context |

> **Note:** In `--auto` and `full-fix` modes, the `fixable` flag is ignored.
> ALL findings are sent to the apply agent. Items that truly cannot be fixed
> are reported as `failed` with a technical reason — not silently skipped.

## Skip Patterns [CONSTRAINT]

**See Tool Rules: Skip Patterns.** Additionally for optimize: `sys.platform`, `msvcrt`, `fcntl` (platform-specific guards).

## Policies

**See Tool Rules:** No Deferrals, Accounting, Mode Detection, Execution Flow.

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`
- Args: $ARGS

**DO NOT re-run these commands. Use the pre-collected values above.**

## Profile Requirement [CRITICAL]

**See Tool Rules: Profile Validation.** Delegate to `/cco:tune --preview`, handle skip/error/success.

## Mode Detection

<!-- Config shape: { fixMode: string, scopes: string[], action: string, gitState: string } -->

```javascript
// Parse arguments
const args = "$ARGS"
const isUnattended = args.includes("--auto")
const isPreview = args.includes("--preview")

// Parse scope filter (--scope=security or --scope=hygiene,types)
const scopeArg = args.match(/--scope=([\w,-]+)/)?.[1]
const validScopes = ["security", "hygiene", "types", "lint", "performance", "ai-hygiene", "robustness", "privacy", "doc-sync", "simplify"]
const scopeFilter = scopeArg ? scopeArg.split(",").filter(s => validScopes.includes(s)) : null

if (isUnattended) {
  // UNATTENDED MODE: CI/CD, pre-commit hooks, cron jobs
  // No progress output, no intermediate messages
  // Skip Q1, Q2, Q3 - proceed directly with full scope and full fix

  config = {
    fixMode: "full-fix",  // All severities
    scopes: ["security", "hygiene", "types", "lint", "performance", "ai-hygiene", "robustness", "privacy", "doc-sync", "simplify"],  // ALL 10 scopes
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

**Analysis always scans ALL severities.** Severity filtering happens post-analysis via Q2.

## Architecture

| Phase | Step | Name | Action | Gate |
|-------|------|------|--------|------|
| **SETUP** | 1 | Config | Q1: Scopes (+ git state) | Config validated |
| **ANALYZE** | 2 | Scan | Parallel scope analysis | Findings collected |
| **GATE-1** | - | Checkpoint | Validate findings ≥0, no errors | → Plan or Apply |
| **PLAN** | 2.5 | Review | Show fix plan + Q2 (Action/Severity) | User approval |
| **GATE-2** | - | Checkpoint | Approval received or skipped | → Apply |
| **APPLY** | 3 | Fix | Apply fixes based on fix mode | Fixes verified |
| **GATE-3** | - | Checkpoint | applied + failed + needs_approval = total | → Summary |
| **SUMMARY** | 4 | Report | Show counts | Done |

**Execution Flow:** SETUP → ANALYZE → GATE-1 → [PLAN if triggered] → GATE-2 → APPLY → GATE-3 → SUMMARY

### Phase Gates

| Gate | Pass | Fail |
|------|------|------|
| GATE-1 (Post-Analysis) | findings is valid array | Analysis error or invalid structure |
| GATE-2 (Post-Plan) | Approval received or plan skipped | User aborted |
| GATE-3 (Post-Apply) | `applied + failed + needs_approval = total` | Accounting mismatch |

> **Note:** Quality Gates (format, lint, type, test) removed from optimize.
> LNT and TYP scopes already analyze lint/type issues. Use `/cco:commit` for pre-commit gates.

**Plan Review is MANDATORY when findings > 0.**

**Skipped when:** `--auto` mode or 0 findings

**Post-analysis Q2 determines what gets fixed:**
- Fix All → Everything
- By Severity → User-selected severity levels
- Review Each → Individual approval per fix
- Report Only → No changes

---

## Step-1: Setup [Q1: Scopes] [SKIP IF --auto]

**Execution Pattern:** Questions first, then synchronous analysis. This ensures reliable result handling.

```javascript
// Determine if git is dirty from context
gitDirty = gitStatus.trim().length > 0
```

**UNATTENDED MODE: Skip all questions, use defaults from Mode Detection**

```javascript
if (isUnattended) {
  // config already set in Mode Detection
  // → Proceed directly to Step-2 (no questions)
} else {
  // Interactive mode - ask Q1 (Intensity) + Q2 (Scopes)
```

**Q1: Scope Groups (multiselect):**

```javascript
  scopeQuestion = {
    question: "Which areas to check?",
    header: "Areas",
    options: [
      { label: "Security & Privacy (Recommended)", description: "Secrets, injection, defensive patterns, PII protection (SEC + ROB + PRV)" },
      { label: "Code Quality (Recommended)", description: "Unused code, types, style, complexity, test cleanup (HYG + TYP + LNT + SIM)" },
      { label: "Performance", description: "N+1, caching, blocking I/O (PRF)" },
      { label: "AI Cleanup", description: "Hallucinations, doc drift (AIH + DOC)" }
    ],
    multiSelect: true
  }
```

**Q2: Git State (conditional, only if dirty):**

```javascript
  questions = [scopeQuestion]

  if (gitDirty) {
    questions.push({
      question: "Uncommitted changes detected. Proceed?",
      header: "Git",
      options: [
        { label: "Continue (Recommended)", description: "Changes visible in git diff" },
        { label: "Stash first", description: "Stash, continue, remind to pop" },
        { label: "Cancel", description: "Abort" }
      ],
      multiSelect: false
    })
  }

  AskUserQuestion(questions)  // Max 3 questions
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

---

## Step-2: Analyze [PARALLEL SCOPES]

**Run analysis with parallel scope groups - multiple Task calls in same message execute concurrently:**

```javascript
// PARALLEL EXECUTION: Launch scope groups in single message
// Each Task returns results directly (synchronous)
// Multiple Task calls in same message run in parallel automatically

// Security & Privacy group (SEC + ROB + PRV)
securityResults = Task("cco-agent-analyze", `
  scopes: ["security", "robustness", "privacy"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku", timeout: 120000 })

// Code Quality group (HYG + TYP + LNT + SIM)
qualityResults = Task("cco-agent-analyze", `
  scopes: ["hygiene", "types", "lint", "simplify"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku", timeout: 120000 })

// Performance group (PRF)
perfResults = Task("cco-agent-analyze", `
  scopes: ["performance"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku", timeout: 120000 })

// AI Cleanup group (AIH + DOC)
aiResults = Task("cco-agent-analyze", `
  scopes: ["ai-hygiene", "doc-sync"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku", timeout: 120000 })

// Merge all parallel results
allFindings = {
  findings: [
    ...securityResults.findings,
    ...qualityResults.findings,
    ...perfResults.findings,
    ...aiResults.findings
  ],
  summary: mergeScoreSummaries([securityResults, qualityResults, perfResults, aiResults])
}

// Confidence calculation (0-100) included in each agent call:
// - Pattern match (40%): How well does issue match known patterns?
// - Context clarity (30%): Is surrounding code clear?
// - Fix determinism (20%): Is there one correct fix?
// - Test coverage (10%): Are there validating tests?
```

// Filter by user-selected scopes
selectedScopes = config.scopes.map(s => s.toLowerCase().replace(" ", "-"))
let findings = allFindings.findings.filter(f => selectedScopes.includes(f.scope))

// No pre-filtering by severity — all findings kept for post-analysis Q2
// Categorize for fix flow
if (isUnattended) {
  // AUTO MODE: ALL findings attempted, none skipped
  autoFixable = [...findings]
  approvalRequired = []
} else {
  autoFixable = findings.filter(f => f.fixable && !f.approvalRequired)
  approvalRequired = findings.filter(f => f.approvalRequired || !f.fixable)
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

**Scopes:** {selectedScopes.length}/6

| Scope | ID Range | Critical | High | Medium | Low | Auto-fix |
|-------|----------|----------|------|--------|-----|----------|
| Security | SEC-01-12 | {n} | {n} | {n} | {n} | {n} |
| Hygiene | HYG-01-20 | {n} | {n} | {n} | {n} | {n} |
| Types | TYP-01-10 | {n} | {n} | {n} | {n} | {n} |
| Lint | LNT-01-08 | {n} | {n} | {n} | {n} | {n} |
| Performance | PRF-01-10 | {n} | {n} | {n} | {n} | {n} |
| AI Hygiene | AIH-01-08 | {n} | {n} | {n} | {n} | {n} |
| Robustness | ROB-01-10 | {n} | {n} | {n} | {n} | {n} |
| Privacy | PRV-01-08 | {n} | {n} | {n} | {n} | {n} |
| Doc Sync | DOC-01-08 | {n} | {n} | {n} | {n} | {n} |
| Simplify | SIM-01-11 | {n} | {n} | {n} | {n} | {n} |
| **Total** | **105 checks** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

**Severity Distribution:**
- [CRITICAL] {counts.bySeverity.critical} items
- [HIGH] {counts.bySeverity.high} items
- [MEDIUM] {counts.bySeverity.medium} items
- [LOW] {counts.bySeverity.low} items

**Fix Plan:**
- Auto-fixable (safe): {autoFixable.length} items
- Approval required (risky): {approvalRequired.length} items
- Excluded by scope: {allFindings.findings.length - findings.length} items
```

```javascript
}
// In --auto mode: No output, proceed silently
```

### Validation
```
[x] Analysis results collected
[x] Findings categorized
→ If action = "Report only": Skip to Step-4
→ If --auto: Skip to Step-3
→ If findings > 0: Step-2.5 (Plan Review)
→ If findings = 0: Skip to Step-4
```

---

## Step-2.5: Plan Review [MANDATORY]

**"Think before you act"** - Reduces errors and low-quality decisions (Karpathy insight).

> **Pattern:** Plan Review is used in /cco:optimize, /cco:align, and /cco:preflight with command-specific
> triggers and content. The structure is consistent:
> 1. Check findings > 0 → 2. Plan Generation → 3. Plan Display → 4. User Decision

### Trigger Conditions

```javascript
// Plan Review runs whenever there are findings
const planMode = findings.length > 0

// Skip in --auto mode
const skipPlan = isUnattended

if (planMode && !skipPlan) {
  // → Enter Plan Review
} else {
  // → Skip to Step-3
}
```

### Plan Generation

**For each finding, generate fix plan with rationale:**

```javascript
const fixPlans = findings.map(finding => ({
  id: finding.id,
  title: finding.title,
  location: finding.location,
  severity: finding.severity,

  // THE PLAN (what Karpathy wants)
  plan: {
    what: generateFixDescription(finding),      // "Remove unused import 'os'"
    why: generateRationale(finding),            // "Reduces bundle size, cleaner code"
    approach: selectApproach(finding),          // "Direct deletion" vs "Replace with..."
    alternatives: listAlternatives(finding),    // ["Keep if used elsewhere", "Move to __all__"]
    risks: assessRisks(finding),                // ["None - unused code"] or ["May break X"]
    confidence: calculateConfidence(finding),   // 0-100 based on evidence
    affectedFiles: [finding.location.file],     // Files that will change
    estimatedLines: estimateChanges(finding)    // ~5 lines
  }
}))
```

### Plan Display [MANDATORY - DISPLAY BEFORE ASKING]

**[CRITICAL] You MUST display the following table to the user BEFORE asking for approval. NEVER skip this display. NEVER ask "How to proceed?" without first showing the full plan.**

```markdown
## Fix Plan Review

**Mode:** {config.fixMode} | **Findings:** {findings.length} | **Files:** {uniqueFiles.length}

> This plan shows what will change and why. Review before approving.

### CRITICAL Fixes ({criticalCount})

| # | ID | What | Why | Risk | Conf |
|---|-----|------|-----|------|------|
| 1 | SEC-01 | Remove hardcoded API key | Security vulnerability, key exposed in repo | None - will use env var | 95 |
| 2 | SEC-03 | Sanitize SQL input | SQL injection possible via user input | Low - parameterized approach | 90 |

### HIGH Priority ({highCount})

| # | ID | What | Why | Risk | Conf |
|---|-----|------|-----|------|------|
| 1 | HYG-01 | Remove 12 unused imports | Dead code, slower load times | None | 100 |
| 2 | TYP-01 | Add return type to `process_data()` | Type safety, IDE support | None | 95 |

### MEDIUM Priority ({mediumCount})

{...similar table...}

### Summary

| Metric | Value |
|--------|-------|
| Total changes | {findings.length} findings across {uniqueFiles.length} files |
| Estimated lines | ~{totalEstimatedLines} lines modified |
| High confidence (≥80) | {highConfidenceCount} ({highConfidencePercent}%) |
| Medium confidence (60-79) | {mediumConfidenceCount} |
| Low confidence (<60) | {lowConfidenceCount} (report only) |

**Alternatives Considered:**
{findings.filter(f => f.plan.alternatives.length > 1).map(f =>
  `- ${f.id}: Chose "${f.plan.approach}" over "${f.plan.alternatives[0]}" because ${f.plan.why}`
)}
```

### User Decision

```javascript
// Standard Post-Analysis Q2: Action + Severity (same pattern in optimize, align, preflight)
AskUserQuestion([
  {
    question: `${findings.length} finding across ${uniqueFiles.length} files. How to proceed?`,
    header: "Action",
    options: [
      { label: "Fix All (Recommended)", description: `Apply all ${findings.length} fixes` },
      { label: "By Severity", description: "Choose which severity levels to fix" },
      { label: "Review Each", description: "Approve each fix individually" },
      { label: "Report Only", description: "No changes, just report" }
    ],
    multiSelect: false
  },
  {
    question: "Which severity levels to include?",
    header: "Severity",
    options: [
      { label: `CRITICAL (${counts.bySeverity.critical})`, description: "Security, data loss, crash" },
      { label: `HIGH (${counts.bySeverity.high})`, description: "Broken functionality" },
      { label: `MEDIUM (${counts.bySeverity.medium})`, description: "Suboptimal but works" },
      { label: `LOW (${counts.bySeverity.low})`, description: "Style, minor improvements" }
    ],
    multiSelect: true
  }
])

// Handle response
// Q2 (Severity) only used when Action = "By Severity"
switch (actionDecision) {
  case "Fix All":
    config.reviewMode = "apply-all"
    // All findings, ignore severity selection
    break
  case "By Severity":
    config.reviewMode = "apply-all"
    const selectedSeverities = severityDecision  // Array of selected severity labels
    findings = findings.filter(f => selectedSeverities.some(s => s.startsWith(f.severity)))
    break
  case "Review Each":
    config.reviewMode = "interactive"
    // If severity selected, filter first
    if (severityDecision?.length > 0) {
      findings = findings.filter(f => severityDecision.some(s => s.startsWith(f.severity)))
    }
    break
  case "Report Only":
    config.reviewMode = "report-only"
    autoFixable = []
    approvalRequired = []
    // Skip to summary
    break
}
```

### Validation
```
[x] Plan generated for all findings
[x] Plan displayed to user
[x] User decision captured
→ If Abort: Exit
→ If Apply Safe Only: Filter to confidence >= 80%
→ Proceed to Step-3 with config.reviewMode
```

---

## Step-3: Apply Fixes [SYNCHRONOUS]

**Run fixes synchronously - Task tool returns results directly:**

```javascript
let fixResults = { applied: 0, failed: 0, needs_approval: 0, total: 0 }

if (config.action !== "Report only" && autoFixable.length > 0) {
  // Determine if unattended mode
  const isUnattendedMode = config.action.includes("Everything") || isUnattended

  // NOTE: Synchronous execution - results returned directly
  // Task agents must be synchronous -- TaskOutput doesn't work for background Task agents, results arrive via task-notification
  fixResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(autoFixable)}
    fixAll: ${isUnattendedMode}

    Apply all items. Verify each fix.
    Group by file for efficiency.

    ${isUnattendedMode ? `
    UNATTENDED MODE: Fix ALL items. No Deferrals Policy applies (see Core Rules).
    Every item = applied, failed (Technical: reason), or needs_approval (Needs-Approval: reason).
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each finding = 1 item, regardless of how many locations it has
    - Example: "Type ignore comments" with 3 locations = 1 finding

    Return accounting at FINDING level:
    { applied: <findings_fixed>, failed: <findings_failed>, needs_approval: <findings_needs_approval>, total: <findings_attempted> }
  `, { model: "opus", timeout: 120000 })  // No run_in_background - synchronous execution

  // Retry guidance: On failure, retry with alternative fix approach
  if (fixResults.error) {
    console.log(`Fix agent failed: ${fixResults.error}. Retrying with alternative approach...`)
    fixResults = Task("cco-agent-apply", `
      fixes: ${JSON.stringify(autoFixable)}
      fixAll: ${isUnattendedMode}
      retryMode: true
      Use alternative fix approaches for items that failed in previous attempt.
      Return accounting at FINDING level.
    `, { model: "opus", timeout: 180000 })
  }
}
```

### Validation
```
[x] All fixes applied based on fix mode
→ Proceed to Step-3.5 (Approval) or Step-4 (Summary)
```

---

## Step-3.5: Needs-Approval Review [CONDITIONAL]

**Presents needs_approval items to user for decision. Skipped in --auto mode (all items attempted).**

```javascript
if (fixResults.needs_approval > 0 && !isUnattended) {
  const needsApprovalItems = fixResults.details.filter(d => d.status === "needs_approval")

  // [MANDATORY] Display needs-approval items BEFORE asking. NEVER skip this display.
  // Output the following table to the user:
  //
  // ## Items Needing Approval
  //
  // | # | ID | Severity | Issue | Location | Reason |
  // |---|-----|----------|-------|----------|--------|
  // {needsApprovalItems.map((item, i) => `| ${i+1} | ${item.id} | ${item.severity} | ${item.title} | ${item.location} | ${item.reason} |`)}

  AskUserQuestion([{
    question: `${needsApprovalItems.length} items need approval (architectural changes). See list above.`,
    header: "Approval",
    options: [
      { label: "Fix All (Recommended)", description: "Apply all architectural changes" },
      { label: "Skip", description: "Leave as-is" },
      { label: "Review Each", description: "Approve individually" }
    ],
    multiSelect: false
  }])

  if (approvalDecision === "Fix All") {
    approvalResults = Task("cco-agent-apply", `
      fixes: ${JSON.stringify(needsApprovalItems)}
      fixAll: true
      Apply approved architectural changes.
    `, { model: "opus" })
    fixResults.applied += approvalResults.applied
    fixResults.failed += approvalResults.failed
    fixResults.needs_approval = 0
  } else if (approvalDecision === "Review Each") {
    for (const item of needsApprovalItems) {
      AskUserQuestion([{
        question: `[${item.id}] ${item.title}\nReason: ${item.reason}`,
        header: "Fix?",
        options: [
          { label: "Apply", description: "Fix this item" },
          { label: "Skip", description: "Leave as-is" }
        ],
        multiSelect: false
      }])
      // Apply or skip based on answer
    }
  }
  // "Skip" → no action, needs_approval count stays
}
```

### Validation
```
[x] Needs-approval items reviewed (or skipped in --auto)
→ Proceed to Step-4 (Summary)
```

---

## Step-4: Summary

### Calculate Final Counts [CRITICAL]

```javascript
// COUNTING STANDARD
// - total: all findings in selected fix mode scope
// - applied: successfully fixed
// - failed: couldn't fix (technical reason required)
//
// Invariant: applied + failed + needs_approval = total
// NOTE: No "declined" category - AI has no option to decline. Fix, defer (architectural), or fail with reason.

// fixResults already set in Step-3 (synchronous execution)
// Default: { applied: 0, failed: 0, total: 0 } if no fixes needed

// Final accounting - use fixResults directly (set in Step-3)
finalCounts = {
  applied: fixResults.applied || 0,
  failed: fixResults.failed || 0,
  needs_approval: fixResults.needs_approval || 0,
  total: fixResults.total || 0
}

// Final verification - these MUST balance
assert(finalCounts.applied + finalCounts.failed + finalCounts.needs_approval === finalCounts.total,
  "Count mismatch: applied + failed + needs_approval must equal total")
```

### Unattended Mode Output [--auto]

**Single line summary only:**

```javascript
if (isUnattended) {
  const status = finalCounts.failed > 0 ? "WARN" : "OK"
  console.log(`cco-optimize: ${status} | Applied: ${finalCounts.applied} | Failed: ${finalCounts.failed} | Needs Approval: ${finalCounts.needs_approval} | Total: ${finalCounts.total}`)
  return
}
```

### Interactive Mode Output

```javascript
let summary = `
## Optimization Complete

| Metric | Value |
|--------|-------|
| Applied | ${finalCounts.applied} |
| Failed | ${finalCounts.failed} |
| Needs Approval | ${finalCounts.needs_approval} |
| **Total** | **${finalCounts.total}** |

Status: ${finalCounts.failed > 0 ? "WARN" : "OK"}

Run \`git diff\` to review changes.`

// Failed items list
if (finalCounts.failed > 0) {
  summary += `\n### Failed Items\n`
  summary += fixResults.details
    .filter(d => d.status === "failed")
    .map(d => `[${d.severity}] ${d.id}: ${d.title} in ${d.location}`)
    .join('\n')
}

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

| Scenario | Questions | Total |
|----------|-----------|-------|
| **--auto mode** | - | **0** |
| Clean git, 0 findings | Scopes (Q1) | **1** |
| Clean git, findings | Scopes (Q1) + Action/Severity (Q2) | **2** |
| Dirty git, findings | Scopes + Git (Q1) + Action/Severity (Q2) | **2** |

**Post-analysis Q2** - User sees real finding counts before deciding action and severity filter.

### Output Schema [STANDARD ENVELOPE]

**All CCO commands use same envelope. Counts are at FINDING level.**

```json
{
  "status": "OK|WARN|FAIL",
  "summary": "Applied 5, Failed 0, Needs Approval 0, Total 5",
  "data": {
    "accounting": { "applied": 5, "failed": 0, "needs_approval": 0, "total": 5 },
    "by_scope": { "security": 2, "hygiene": 3, "types": 0 },
    "by_severity": { "critical": 0, "high": 2, "medium": 3, "low": 0 },
    "blockers": []
  },
  "error": null
}
```

**Status rules:**
- `OK`: failed = 0
- `WARN`: failed > 0 but no CRITICAL
- `FAIL`: any CRITICAL unfixed OR error != null

**Accounting invariant:** `applied + failed + needs_approval = total`

**--auto mode:** Prints `summary` field only.

### Scope Coverage (10 Scopes, 105 Checks)

| Scope | ID Range | Checks |
|-------|----------|--------|
| `security` | SEC-01-12 | Secrets, injection, path traversal, deserialization, input validation, logging, temp files, HTTPS, eval, debug endpoints, crypto |
| `hygiene` | HYG-01-20 | Unused imports/vars/functions, dead code, orphan files, duplicates, stale TODOs, empty files, commented code, formatting, circular imports, bare except, comment quality |
| `types` | TYP-01-10 | Type errors, missing return types, untyped args, type:ignore without reason, Any in APIs, generics, union vs literal, optional handling, narrowing, override signatures |
| `lint` | LNT-01-08 | Format violations, import order, line length, naming, docstrings, magic numbers, string literals, quote style |
| `performance` | PRF-01-10 | N+1 patterns, list on iterator, missing cache, blocking in async, large file reads, pagination, string concat loops, copies, pooling, sync in hot paths |
| `ai-hygiene` | AIH-01-08 | Hallucinated APIs, orphan abstractions, over-documented functions, dead flags, stale mocks, incomplete impls, copy-paste artifacts, dangling refs |
| `robustness` | ROB-01-10 | Missing timeouts, retries, endpoint guards, unbounded collections, implicit coercion, null checks, graceful degradation, circuit breakers, cleanup, concurrency |
| `privacy` | PRV-01-08 | PII in logs/responses, missing masking, excessive collection, consent checks, retention policy, cross-border transfer, audit trails, insecure PII storage |
| `doc-sync` | DOC-01-08 | README outdated, API mismatch, deprecated refs in docs, missing feature docs, outdated examples, broken links, changelog not updated, comment-code drift |
| `simplify` | SIM-01-11 | Deep nesting (>3), duplicate blocks, unnecessary abstractions, single-use wrappers, over-engineering, complex booleans, long param lists, god functions (>50 lines), premature optimization, redundant null checks |

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
| `--auto` | Unattended mode: all scopes, all severities, no questions |
| `--preview` | Analyze only, show findings and quality score, don't apply fixes |
| `--scope=<name>` | Run specific scope(s) only, comma-separated |

### Model Strategy

Opus for orchestration/apply, Haiku for analysis agents.

### Scope Groups

**Note:** These groupings align with `/cco:align` groups to provide consistent mental model.
Both commands use similar grouping strategy: security/privacy together, quality/testing together, etc.

| Group | Scopes Included | Checks |
|-------|-----------------|--------|
| **Security & Privacy** | security + robustness + privacy | SEC-01-12, ROB-01-10, PRV-01-08 (30 checks) |
| **Code Quality** | hygiene + types + lint + simplify | HYG-01-20, TYP-01-10, LNT-01-08, SIM-01-11 (49 checks) |
| **Performance** | performance | PRF-01-10 (10 checks) |
| **AI Cleanup** | ai-hygiene + doc-sync | AIH-01-08, DOC-01-08 (16 checks) |

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

1. **Scope question first** - Q1 collects scopes (+ git state if dirty)
2. **Post-analysis decision** - Q2 shows real counts, user picks action + severity
3. **Parallel analysis** - Start analysis after Q1
4. **Dynamic tabs** - Git State tab only if dirty
5. **Single Recommended** - Each question has one recommended option
6. **Counting consistency** - Count findings, not locations

---

## Reasoning & Guards

**See Tool Rules:** Severity Levels, Plan Review, Confidence Scoring.

**Optimize-specific Step-Back questions:**

| Scope | Step-Back Question |
|-------|-------------------|
| Security | "What are the trust boundaries in this codebase?" |
| Quality | "What are the quality standards for this project?" |
| Hygiene | "What is considered 'dead' in this context?" |
| Best Practices | "What patterns does this project follow?" |

---

## Confidence Scoring

**See Tool Rules: Confidence Scoring.** Threshold ≥80 for safe-only mode. CRITICAL bypasses confidence.

---

## Accounting

**See Tool Rules: Accounting.** Invariant: `applied + failed + needs_approval = total` (count findings, not locations).
