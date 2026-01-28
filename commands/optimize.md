---
description: Incremental code improvement - fix security, hygiene, types, lint, performance issues
argument-hint: "[--auto] [--preview] [--score] [--report] [--fix] [--fix-all] [--plan] [--intensity=<level>] [--security] [--hygiene] [--types] [--lint] [--performance] [--ai-hygiene] [--robustness] [--doc-sync]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
model: opus
---

# /cco:optimize

**Incremental Code Improvement** - Quality gates + parallel analysis + background fixes with Fix Intensity selection.

> **Implementation Note:** Code blocks use JavaScript-like pseudocode for clarity. Actual execution uses Claude Code tools with appropriate parameters.

**Philosophy:** "This code works. How can it work better?"

**Purpose:** Tactical, file-level fixes. For strategic architecture assessment, use `/cco:align`.

## Args

- `--auto` or `--unattended`: Fully unattended mode for CI/CD, pre-commit, cron jobs
  - **No questions asked** - all 8 scopes, Full Fix intensity
  - **No progress output** - silent execution
  - **Only final summary** - single status line (machine-readable)
  - Exit codes: 0 (success), 1 (warnings), 2 (failures)
- `--security`: Security scope only (SEC-01 to SEC-12)
- `--hygiene`: Hygiene scope only (HYG-01 to HYG-15)
- `--types`: Types scope only (TYP-01 to TYP-10)
- `--lint`: Lint scope only (LNT-01 to LNT-08)
- `--performance`: Performance scope only (PRF-01 to PRF-10)
- `--ai-hygiene`: AI hygiene scope only (AIH-01 to AIH-08)
- `--robustness`: Robustness scope only (ROB-01 to ROB-10)
- `--doc-sync`: Doc-code sync scope only (DOC-01 to DOC-08)
- `--simplify`: Simplify scope only (SIM-01 to SIM-10)
- `--report`: Report only, no fixes
- `--fix`: Auto-fix safe items (default)
- `--fix-all`: Full Fix intensity without approval
- `--score`: Quality score only (0-100), skip all questions
- `--intensity=<level>`: Set fix intensity (quick-wins, standard, full-fix, report-only)
- `--plan`: Enable Plan Review phase - show detailed fix plan before applying
  - Shows: what will change, why this approach, alternatives considered, risks
  - Requires explicit approval before any changes
  - Auto-enabled when: >10 findings OR any CRITICAL severity OR --fix-all
  - Skipped in --auto mode (use --auto --plan to force)

**Usage:**
- `/cco:optimize --auto` - Silent full optimization (all scopes, full fix)
- `/cco:optimize --security --fix-all` - Security only, fix all
- `/cco:optimize --ai-hygiene` - Find AI-generated code issues
- `/cco:optimize --doc-sync` - Find doc↔code inconsistencies
- `/cco:optimize --score` - Quick quality score

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

## Skip Patterns [CONSTRAINT]

Do NOT flag or fix:
- `# noqa`, `# intentional`, `# safe:` marked code
- `_` prefixed variables (intentional unused)
- `TYPE_CHECKING` blocks (type-only imports)
- Platform guards (`sys.platform`, `msvcrt`, `fcntl`)
- Test fixtures in `fixtures/`, `testdata/`, `__snapshots__/`

## Policies

**See Core Rules:** `CCO Operation Standards` for No Deferrals Policy, Intensity Levels, and Quality Thresholds.

### No Deferrals in Auto/Fix-All [CRITICAL]

When `--auto` or `--fix-all` is active:
- **Zero commentary** - No "this is complex", "needs refactor", "minor detail"
- **Zero deferrals** - No "consider later", "recommend manual", "outside scope"
- **Zero skips** - Every finding = FIXED or TECHNICAL FAILURE
- **Only technical failures** - File not found, parse error, permission denied

## Context

- Git status: !`git status --short`
- Args: $ARGS

**DO NOT re-run these commands. Use the pre-collected values above.**

## Profile Requirement [CRITICAL]

CCO profile is auto-loaded from `.claude/rules/cco-profile.md` via Claude Code's auto-context mechanism.

**Check:** Delegate to `/cco:tune --check` for profile validation:

```javascript
// Delegate profile check to tune command
const tuneResult = await Skill("tune", "--check")

if (tuneResult.status === "skipped") {
  // User declined setup - exit gracefully
  console.log("CCO setup skipped. Run /cco:tune when ready.")
  return
}

// Profile is now valid - continue with command
```

**After tune completes → continue to Mode Detection**

## Mode Detection

```javascript
// Parse arguments
const args = "$ARGS"
const isUnattended = args.includes("--auto") || args.includes("--unattended")

// Parse intensity from args
const intensityArg = args.match(/--intensity=(\w+)/)?.[1]

if (isUnattended) {
  // UNATTENDED MODE: CI/CD, pre-commit hooks, cron jobs
  // No progress output, no intermediate messages
  // Skip Q1, Q2, Q3 - proceed directly with full scope and full fix

  config = {
    intensity: "full-fix",  // All severities
    scopes: ["security", "hygiene", "types", "lint", "performance", "ai-hygiene", "robustness", "doc-sync", "simplify"],  // ALL 9 scopes
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
| quick-wins | High impact + low effort only | 80/20 fast improvement |
| standard | CRITICAL + HIGH + MEDIUM | Normal operation (default) |
| full-fix | ALL severities, ALL effort levels | Comprehensive cleanup |
| report-only | ALL (analysis only) | Review without changes |

## Architecture

| Phase | Step | Name | Action | Gate |
|-------|------|------|--------|------|
| **SETUP** | 1 | Config | Q1: Combined settings | Config validated |
| **ANALYZE** | 2 | Scan | Parallel scope analysis | Findings collected |
| **GATE-1** | - | Checkpoint | Validate findings ≥0, no errors | → Plan or Apply |
| **PLAN** | 2.5 | Review | Show fix plan (conditional) | User approval |
| **GATE-2** | - | Checkpoint | Approval received or skipped | → Apply |
| **APPLY** | 3 | Fix | Apply fixes based on intensity | Fixes verified |
| **GATE-3** | - | Checkpoint | applied + failed = total | → Summary |
| **SUMMARY** | 4 | Report | Show counts | Done |

**Execution Flow:** SETUP → ANALYZE → GATE-1 → [PLAN if triggered] → GATE-2 → APPLY → GATE-3 → SUMMARY

### Phase Gates

```javascript
// GATE-1: Post-Analysis
function gate1_postAnalysis(findings) {
  if (findings.error) throw new Error("Analysis failed: " + findings.error)
  if (!Array.isArray(findings.findings)) throw new Error("Invalid findings structure")
  return { pass: true, count: findings.findings.length }
}

// GATE-2: Post-Plan (or skip)
function gate2_postPlan(planResult, skipPlan) {
  if (skipPlan) return { pass: true, reason: "Plan skipped" }
  if (planResult === "Abort") return { pass: false, reason: "User aborted" }
  return { pass: true, mode: planResult }
}

// GATE-3: Post-Apply
function gate3_postApply(results) {
  const valid = results.applied + results.failed === results.total
  if (!valid) throw new Error("Accounting mismatch: applied + failed != total")
  return { pass: true, applied: results.applied, failed: results.failed }
}
```

> **Note:** Quality Gates (format, lint, type, test) removed from optimize.
> LNT and TYP scopes already analyze lint/type issues. Use `/cco:commit` for pre-commit gates.

**Plan Review triggers automatically when:**
- `--plan` flag is passed
- >10 findings detected
- Any CRITICAL severity finding
- `--fix-all` intensity selected

**Skipped when:** `--auto` mode (unless `--auto --plan`)

**Intensity determines what gets fixed:**
- Quick Wins → High impact, low effort only
- Standard → CRITICAL + HIGH + MEDIUM
- Full Fix → Everything
- Report Only → No changes

---

## Step-1: Setup [Q1: Intensity + Q2: Scopes] [SKIP IF --auto]

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
      { label: "Security (Recommended)", description: "Secrets, injection, defensive patterns (SEC + ROB)" },
      { label: "Code Quality (Recommended)", description: "Unused code, types, style (HYG + TYP + LNT)" },
      { label: "Performance", description: "N+1, caching, blocking I/O (PRF)" },
      { label: "AI Cleanup", description: "Hallucinations, doc drift (AIH + DOC)" },
      { label: "Simplify", description: "Reduce complexity, flatten nesting (SIM)" }
    ],
    multiSelect: true
  }
```

**Q2: Fix Intensity:**

```javascript
  intensityQuestion = {
    question: "How much to fix?",
    header: "Intensity",
    options: [
      { label: "Quick Wins", description: "High impact, low effort only" },
      { label: "Standard (Recommended)", description: "CRITICAL + HIGH + MEDIUM" },
      { label: "Full", description: "All severities including LOW" }
    ],
    multiSelect: false
  }
```

**Q3: Git State (conditional, only if dirty):**

```javascript
  questions = [scopeQuestion, intensityQuestion]

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

## Step-2: Analyze [PARALLEL SCOPES]

**Run analysis with parallel scope groups - multiple Task calls in same message execute concurrently:**

```javascript
// PARALLEL EXECUTION: Launch scope groups in single message
// Each Task returns results directly (synchronous)
// Multiple Task calls in same message run in parallel automatically

// Security group (SEC + ROB)
securityResults = Task("cco-agent-analyze", `
  scopes: ["security", "robustness"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku" })

// Code Quality group (HYG + TYP + LNT)
qualityResults = Task("cco-agent-analyze", `
  scopes: ["hygiene", "types", "lint"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku" })

// Performance group (PRF)
perfResults = Task("cco-agent-analyze", `
  scopes: ["performance"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku" })

// AI Cleanup group (AIH + DOC)
aiResults = Task("cco-agent-analyze", `
  scopes: ["ai-hygiene", "doc-sync"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku" })

// Simplify group (SIM)
simplifyResults = Task("cco-agent-analyze", `
  scopes: ["simplify"]
  Find all issues with severity, fix info, effort/impact scores, and confidence.
  Return: { findings: [...], summary: {...} }
`, { model: "haiku" })

// Merge all parallel results
allFindings = {
  findings: [
    ...securityResults.findings,
    ...qualityResults.findings,
    ...perfResults.findings,
    ...aiResults.findings,
    ...simplifyResults.findings
  ],
  summary: mergeScoreSummaries([securityResults, qualityResults, perfResults, aiResults, simplifyResults])
}

// Confidence calculation (0-100) included in each agent call:
// - Pattern match (40%): How well does issue match known patterns?
// - Context clarity (30%): Is surrounding code clear?
// - Fix determinism (20%): Is there one correct fix?
// - Test coverage (10%): Are there validating tests?
```

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
| Robustness | ROB-01-10 | {n} | {n} | {n} | {n} | {n} |
| Doc Sync | DOC-01-08 | {n} | {n} | {n} | {n} | {n} |
| Simplify | SIM-01-10 | {n} | {n} | {n} | {n} | {n} |
| **Total** | **91 checks** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

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
→ If action = "Report only": Skip to Step-4
→ If --auto (without --plan): Skip to Step-3
→ Check Plan Review triggers → Step-2.5 or Step-3
```

---

## Step-2.5: Plan Review [CONDITIONAL]

**"Think before you act"** - Reduces errors and low-quality decisions (Karpathy insight).

> **Pattern:** Plan Review is used in /cco:optimize, /cco:align, and /cco:preflight with command-specific
> triggers and content. Each command has different thresholds (optimize: >10 findings,
> align: >5 recommendations, preflight: any blockers). The structure is consistent:
> 1. Trigger Conditions → 2. Plan Generation → 3. Plan Display → 4. User Decision

### Trigger Conditions

```javascript
// Determine if Plan Review is needed
const planMode = args.includes("--plan") ||
  (findings.length > 10) ||
  (findings.some(f => f.severity === "CRITICAL")) ||
  (config.intensity === "full-fix")

// Skip in pure --auto mode (unless --auto --plan)
const skipPlan = isUnattended && !args.includes("--plan")

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

### Plan Display

```markdown
## Fix Plan Review

**Mode:** {config.intensity} | **Findings:** {findings.length} | **Files:** {uniqueFiles.length}

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
AskUserQuestion([{
  question: "Review complete. How to proceed?",
  header: "Plan",
  options: [
    { label: "Apply All (Recommended)", description: `Apply all ${findings.length} fixes as planned` },
    { label: "Apply Safe Only", description: `Apply only ${highConfidenceCount} high-confidence fixes (>80%)` },
    { label: "Review Each", description: "Ask before each fix (slower but more control)" },
    { label: "Abort", description: "Cancel and make no changes" }
  ],
  multiSelect: false
}])

// Handle response
switch (planDecision) {
  case "Apply All":
    config.reviewMode = "apply-all"
    break
  case "Apply Safe Only":
    config.reviewMode = "safe-only"
    findings = findings.filter(f => f.plan.confidence >= 80)
    break
  case "Review Each":
    config.reviewMode = "interactive"
    break
  case "Abort":
    console.log("Aborted. No changes made.")
    return
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
let fixResults = { applied: 0, failed: 0, total: 0 }

if (config.action !== "Report only" && autoFixable.length > 0) {
  // Determine if fix-all mode
  const isFixAll = config.action.includes("Everything") || isUnattended

  // NOTE: Synchronous execution - results returned directly
  // Do NOT use run_in_background: true - output file stays empty
  fixResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(autoFixable)}
    fixAll: ${isFixAll}

    Apply all auto-fixable items. Verify each fix.
    Group by file for efficiency.

    ${isFixAll ? `
    FIX-ALL MODE [MANDATORY]:
    Fix ALL items. Effort categories are for reporting only, not filtering.

    Rules:
    - ALL findings must be fixed regardless of effort level
    - Zero agent-initiated skips
    - Every item = FIXED or TECHNICAL FAILURE (with "Technical: [reason]")
    - If unsure → fix it anyway, user reviews with git diff

    FORBIDDEN RESPONSES (never use these as skip reasons):
    - "This is too complex" → Fix it
    - "This requires refactoring" → Do the refactor
    - "This is a minor detail" → Fix it anyway
    - "Consider doing this later" → Do it NOW
    - "This might break something" → Fix it, user reviews
    - "Recommend manual review" → Apply the fix

    ONLY VALID FAILURES: File not found, parse error, permission denied
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each finding = 1 item, regardless of how many locations it has
    - Example: "Type ignore comments" with 3 locations = 1 finding

    Return accounting at FINDING level:
    { applied: <findings_fixed>, failed: <findings_failed>, total: <findings_attempted> }
  `, { model: "opus" })  // No run_in_background - synchronous execution
}
```

### Validation
```
[x] All fixes applied based on intensity
→ Proceed to Step-4 (Summary)
```

---

## Step-4: Summary

### Calculate Final Counts [CRITICAL]

```javascript
// COUNTING STANDARD
// - total: all findings in selected intensity scope
// - applied: successfully fixed
// - failed: couldn't fix (technical reason required)
//
// Invariant: applied + failed = total
// NOTE: No "declined" category - AI has no option to decline. Fix or fail with reason.

// fixResults already set in Step-3 (synchronous execution)
// Default: { applied: 0, failed: 0, total: 0 } if no fixes needed

// Final accounting - use fixResults directly (set in Step-3)
finalCounts = {
  applied: fixResults.applied || 0,
  failed: fixResults.failed || 0,
  total: fixResults.total || 0
}

// Final verification - these MUST balance
assert(finalCounts.applied + finalCounts.failed === finalCounts.total,
  "Count mismatch: applied + failed must equal total")
```

### Unattended Mode Output [--auto]

**Single line summary only:**

```javascript
if (isUnattended) {
  const status = finalCounts.failed > 0 ? "WARN" : "OK"
  console.log(`cco-optimize: ${status} | Fixed: ${finalCounts.applied} | Failed: ${finalCounts.failed} | Scopes: all`)
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
| **Total** | **${finalCounts.total}** |

Status: ${finalCounts.failed > 0 ? "WARN" : "OK"}

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

| Scenario | Questions | Total |
|----------|-----------|-------|
| **--auto mode** | - | **0** |
| Clean git | Intensity + Scopes (2-3 tabs) | **1** |
| Dirty git | Intensity + Scopes + Git State (3-4 tabs) | **1** |

**No approval questions** - Intensity selection determines what gets fixed automatically.

### Output Schema [STANDARD ENVELOPE]

**All CCO commands use same envelope. Counts are at FINDING level.**

```json
{
  "status": "OK|WARN|FAIL",
  "summary": "Applied 5, Failed 0, Total 5",
  "data": {
    "accounting": { "applied": 5, "failed": 0, "total": 5 },
    "intensity": "standard",
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

**Accounting invariant:** `applied + failed = total`

**--auto mode:** Prints `summary` field only.

### Scope Coverage (9 Scopes, 91 Checks)

| Scope | ID Range | Checks |
|-------|----------|--------|
| `security` | SEC-01-12 | Hardcoded secrets, SQL/command injection, path traversal, unsafe deserialization, input validation, cleartext logging, insecure temp files, missing HTTPS, eval/exec, debug endpoints, weak crypto |
| `hygiene` | HYG-01-15 | Unused imports/vars/functions, dead code, orphan files, duplicate blocks, stale TODOs, empty files, commented code, line endings, whitespace, indentation, missing __init__.py, circular imports, bare except |
| `types` | TYP-01-10 | Type errors (mypy/pyright), missing return types, untyped args, type:ignore without reason, Any in APIs, missing generics, union vs literal, optional handling, narrowing opportunities, override signatures |
| `lint` | LNT-01-08 | Format violations, import order, line length, naming conventions, docstring format, magic numbers, string literals, quote style |
| `performance` | PRF-01-10 | N+1 patterns, list on iterator, missing cache, blocking in async, large file reads, missing pagination, string concat loops, unnecessary copies, missing pooling, sync in hot paths |
| `ai-hygiene` | AIH-01-08 | Hallucinated APIs, orphan abstractions, phantom imports, dead feature flags, stale mocks, incomplete implementations, copy-paste artifacts, dangling references |
| `robustness` | ROB-01-10 | Code-level defensive patterns: missing timeouts, retries, endpoint guards, unbounded collections, implicit coercion, null checks, graceful degradation, circuit breakers, resource cleanup, concurrent safety |
| `doc-sync` | DOC-01-08 | README outdated, API signature mismatch, deprecated references in docs, missing new feature docs, outdated examples, broken internal links, changelog not updated, comment-code drift |
| `simplify` | SIM-01-10 | Deeply nested conditionals (>3 levels), duplicate/similar code blocks, unnecessary abstractions, single-use wrappers, over-engineered patterns, complex boolean expressions, long parameter lists, god functions (>50 lines), premature optimization, redundant null checks |

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
| `--auto` | Unattended mode: all areas, full intensity, no questions |
| `--preview` | Analyze only, show findings, don't apply fixes |
| `--score` | Quality score only (0-100), skip questions |

### Model Strategy

**Policy:** Opus + Haiku only (no Sonnet)

| Task | Model | Reason |
|------|-------|--------|
| Analysis (parallel scopes) | Haiku | Fast, cost-effective scanning |
| Apply fixes | Opus | 50-75% fewer tool errors |
| Score calculation | Haiku | Simple aggregation |

### Scope Groups

| Group | Scopes Included | Checks |
|-------|-----------------|--------|
| **Security** | security + robustness | SEC-01-12, ROB-01-10 (22 checks) |
| **Code Quality** | hygiene + types + lint | HYG-01-15, TYP-01-10, LNT-01-08 (33 checks) |
| **Performance** | performance | PRF-01-10 (10 checks) |
| **AI Cleanup** | ai-hygiene + doc-sync | AIH-01-08, DOC-01-08 (16 checks) |
| **Simplify** | simplify | SIM-01-10 (10 checks) |

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

1. **Single question** - All settings in Q1, no approval questions
2. **Background analysis** - Start analysis while asking Q1
3. **Dynamic tabs** - Git State tab only if dirty
4. **Intensity-driven** - Selected intensity determines what gets fixed automatically
5. **Single Recommended** - Each tab has one recommended option
6. **Counting consistency** - Count findings, not locations

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

## Confidence Scoring

Each finding includes a confidence score (0-100) indicating fix reliability.

### Score Calculation

| Factor | Weight | Criteria |
|--------|--------|----------|
| Pattern Match | 40% | How well does the issue match known patterns? |
| Context Clarity | 30% | Is the surrounding code clear and unambiguous? |
| Fix Determinism | 20% | Is there exactly one correct fix? |
| Test Coverage | 10% | Are there tests that validate the fix? |

```javascript
confidence = (patternMatch * 0.4) + (contextClarity * 0.3) +
             (fixDeterminism * 0.2) + (testCoverage * 0.1)
```

### Score Interpretation

| Score | Level | Action |
|-------|-------|--------|
| 90-100 | Very High | Auto-fix without review |
| 80-89 | High | Auto-fix, visible in diff |
| 70-79 | Medium | Show in plan, recommend fix |
| 60-69 | Low | Show in plan, ask approval |
| <60 | Very Low | Report only, no auto-fix |

### Threshold: ≥80

- **"Apply Safe Only"** filters to confidence ≥80
- Findings below 80 require explicit approval
- CRITICAL severity bypasses confidence (always shown)

---

## Accounting

**Invariant:** `applied + failed = total` (count findings, not locations)

**No "declined" category:** AI has no option to decline fixes. If it's technically possible and user asked for it, it MUST be done. Only "failed" with specific technical reason is acceptable.
