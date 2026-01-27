---
description: Incremental code improvement - fix security, hygiene, types, lint, performance issues
argument-hint: [--auto] [--security] [--hygiene] [--types] [--lint] [--performance] [--ai-hygiene] [--fix-all] [--score]
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(*), Task(*), AskUserQuestion
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

## Good Targets vs Bad Targets

**Good optimization targets (fix these):**
- Hardcoded secrets in config files → move to env vars
- Unused imports in production code → remove
- Type errors caught by mypy → fix types
- Missing input validation at API boundaries → add validation
- Empty catch blocks → add proper handling
- Console.log/print debugging statements → remove

**Bad optimization targets (skip these):**
- Type ignores with explanatory comments → intentional
- Platform-specific imports (msvcrt, fcntl) → cross-platform code
- Unused variables prefixed with `_` → intentional unused
- Code inside `if TYPE_CHECKING:` blocks → type-only
- Test fixtures and mock data → test infrastructure
- Code marked with `# noqa`, `# intentional`, `# safe:` → explicitly silenced

## Maintain Balance [CRITICAL]

**Avoid over-optimization that:**
- Creates more complex code than before (clever > readable)
- Removes helpful abstractions that improve organization
- Prioritizes "fewer issues" over correctness
- Combines too many concerns into single functions
- Replaces clear if/else with nested ternaries

**Preserve:**
- Existing code structure unless explicitly broken
- Developer intent expressed in comments
- Platform-specific guards and conditionals
- Test infrastructure patterns

## Policies

**See Core Rules:** `CCO Operation Standards` for No Deferrals Policy, Intensity Levels, and Quality Thresholds.

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
    scopes: ["security", "hygiene", "types", "lint", "performance", "ai-hygiene", "robustness", "doc-sync"],  // ALL 8 scopes
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

| Step | Name | Action | Optimization | Dependency |
|------|------|--------|--------------|------------|
| 1 | Setup | Q1: Combined settings (background analysis starts) | Single question | - |
| 2 | Analyze | Wait for analysis, show findings | Progressive | [SEQUENTIAL] after 1 |
| 2.5 | Plan Review | Show fix plan, get approval (conditional) | User decision | [SEQUENTIAL] after 2 |
| 3 | Apply | Apply fixes based on intensity | Batched | [SEQUENTIAL] after 2.5 |
| 4 | Summary | Show counts | Instant | [SEQUENTIAL] after 3 |

**Execution Flow:** 1 → 2 → [2.5 if plan mode] → 3 → 4

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

## Step-1: Setup [Q1: Intensity + Q2: Scopes + BACKGROUND ANALYSIS] [SKIP IF --auto]

**Start analysis in background while asking questions (or immediately if --auto):**

```javascript
// Determine if git is dirty from context
gitDirty = gitStatus.trim().length > 0

// Start analysis with ALL 8 scopes - will filter after Q1/Q2 (or use all if --auto)
// Scopes: security (SEC-01-12), hygiene (HYG-01-15), types (TYP-01-10),
//         lint (LNT-01-08), performance (PRF-01-10), ai-hygiene (AIH-01-08), robustness (ROB-01-10)
analysisTask = Task("cco-agent-analyze", `
  scopes: ["security", "hygiene", "types", "lint", "performance", "ai-hygiene", "robustness"]

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
      { label: "Quick Wins (80/20)", description: "High impact, low effort only" },
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

**Q3: Scope Selection - Advanced (4 scopes):**

```javascript
  scopeQuestion2 = {
    question: "Advanced scopes to analyze?",
    header: "Scopes 2/2",
    options: [
      { label: "Performance (10)", description: "PRF-01-10: N+1, blocking I/O, caching" },
      { label: "AI Hygiene (8)", description: "AIH-01-08: hallucinations, orphan abstractions" },
      { label: "Robustness (10)", description: "ROB-01-10: timeouts, retries, validation, null safety" },
      { label: "Doc Sync (8)", description: "DOC-01-08: README outdated, API mismatch, broken links" }
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
| Robustness | ROB-01-10 | {n} | {n} | {n} | {n} | {n} |
| **Total** | **73 checks** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

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

| # | ID | What | Why | Risk | Confidence |
|---|-----|------|-----|------|------------|
| 1 | SEC-01 | Remove hardcoded API key | Security vulnerability, key exposed in repo | None - will use env var | 95% |
| 2 | SEC-03 | Sanitize SQL input | SQL injection possible via user input | Low - parameterized approach | 90% |

### HIGH Priority ({highCount})

| # | ID | What | Why | Risk | Confidence |
|---|-----|------|-----|------|------------|
| 1 | HYG-01 | Remove 12 unused imports | Dead code, slower load times | None | 100% |
| 2 | TYP-01 | Add return type to `process_data()` | Type safety, IDE support | None | 95% |

### MEDIUM Priority ({mediumCount})

{...similar table...}

### Summary

| Metric | Value |
|--------|-------|
| Total changes | {findings.length} findings across {uniqueFiles.length} files |
| Estimated lines | ~{totalEstimatedLines} lines modified |
| High confidence (>80%) | {highConfidenceCount} ({highConfidencePercent}%) |
| Risky changes | {riskyCount} (will ask before each) |

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
    FULL FIX MODE [MANDATORY]:
    Fix ALL items. Effort categories are for reporting only, not filtering.

    Rules:
    - ALL findings must be fixed regardless of effort level
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

// Get results from Step-3
fixResults = autoFixResults?.accounting || { applied: 0, failed: 0, total: 0 }

// Final accounting
finalCounts = {
  applied: fixResults.applied,
  failed: fixResults.failed,
  total: fixResults.total
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
    "ai-hygiene": "{n}",
    "robustness": "{n}"
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

### Scope Coverage (8 Scopes, 81 Checks)

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
| `--auto` | **Unattended mode:** all 8 scopes, full-fix intensity, no questions, silent execution, single-line summary |
| `--security` | Security scope only (SEC-01-12) |
| `--hygiene` | Hygiene scope only (HYG-01-15) |
| `--types` | Types scope only (TYP-01-10) |
| `--lint` | Lint scope only (LNT-01-08) |
| `--performance` | Performance scope only (PRF-01-10) |
| `--ai-hygiene` | AI hygiene scope only (AIH-01-08) |
| `--robustness` | Robustness scope only (ROB-01-10) |
| `--doc-sync` | Doc-code sync scope only (DOC-01-08) |
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

## Accounting

**Invariant:** `applied + failed = total` (count findings, not locations)

**No "declined" category:** AI has no option to decline fixes. If it's technically possible and user asked for it, it MUST be done. Only "failed" with specific technical reason is acceptable.
