---
description: Align codebase with ideal architecture - current vs ideal state gap analysis
argument-hint: "[--auto] [--preview]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, Skill, AskUserQuestion
model: opus
---

# /cco:align

**Align with Ideal Architecture** - "If I designed from scratch, what would be best?"

> **Implementation Note:** Code blocks use JavaScript-like pseudocode for clarity. Actual execution uses Claude Code tools with appropriate parameters.

> **Standard Flow:** This command follows the standard CCO execution pattern:
> Setup → Analyze → Gate → Assess → Plan → Apply → Summary (see docs/philosophy.md for rationale)

**Philosophy:** Evaluate as if no technology choices exist yet. Given only the requirements, what's ideal? Then compare current state to that ideal.

**Purpose:** Strategic, architecture-level assessment. For tactical file-level fixes, use `/cco:optimize`.

**Unique Value:**
- "Would FastAPI be better than Flask here?"
- "Should this be microservices or monolith?"
- "Is Repository pattern missing?"
- "Is this over-engineered by AI?"

## Skip Patterns [CONSTRAINT]

| Pattern | Reason |
|---------|--------|
| Simple CRUD for project scale | Appropriate complexity |
| Single-implementation interfaces | Prototyping phase |
| Framework-mandated patterns | Required by framework |
| ADR/comment-documented trade-offs | Intentional decisions |
| Legacy code in maintenance mode | Mention, don't prioritize |

## Scopes

| Scope | ID Range | Focus | Checks |
|-------|----------|-------|--------|
| `architecture` | ARC-01 to ARC-15 | Coupling, cohesion, layers, dependencies | 15 |
| `patterns` | PAT-01 to PAT-12 | Design patterns, consistency, SOLID | 12 |
| `testing` | TST-01 to TST-10 | Coverage strategy, test quality, gaps | 10 |
| `maintainability` | MNT-01 to MNT-12 | Complexity, readability, documentation | 12 |
| `ai-architecture` | AIA-01 to AIA-10 | Over-engineering, local solutions, drift | 10 |
| `functional-completeness` | FUN-01 to FUN-18 | API completeness: CRUD, pagination, filtering, edge cases, schema validation, state transitions, soft delete, locking, timeout/retry, caching, consistency, indexing, bulk ops | 18 |

**Total: 77 checks**

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Profile Requirement [CRITICAL]

<!-- Standard profile validation pattern (shared across optimize, align, docs, preflight) -->

CCO profile is auto-loaded from `.claude/rules/cco-profile.md` via Claude Code's auto-context mechanism.

**Check:** Delegate to `/cco:tune --preview` for profile validation:

```javascript
// Standard profile validation: delegate to tune, handle skip/error/success
const tuneResult = await Skill("cco:tune", "--preview")

if (tuneResult.status === "skipped") {
  console.log("CCO setup skipped. Run /cco:tune when ready.")
  return
} else if (tuneResult.status === "error") {
  console.error("Profile validation failed:", tuneResult.reason)
  return
}

// Profile is now valid - continue with command
```

**After tune completes → continue to Step-0 (Mode Detection)**

---

## Mode Detection [CRITICAL]

<!-- Config shape: { fixMode: string, scopes: string[], applyMode: string, unattended: boolean } -->

```javascript
// --auto mode: unattended, full scope, no questions, minimal output
if (args.includes("--auto")) {
  config = {
    fixMode: "full-fix",          // All severities
    scopes: ["architecture", "patterns", "testing", "maintainability", "ai-architecture", "functional-completeness"],
    applyMode: "apply-all",       // Apply everything
    unattended: true
  }
  // Skip Q1 entirely, proceed directly to Step-1b
}
```

**--auto use cases:** CI/CD pipelines, pre-commit hooks, scheduled cron jobs, IDE integrations (non-interactive)

---

## Architecture

| Phase | Step | Name | Action | Gate |
|-------|------|------|--------|------|
| **SETUP** | 0-1a | Config | Mode + Q1: Areas | Config validated |
| **ANALYZE** | 1b | Scan | Parallel scope analysis | Findings collected |
| **GATE-1** | - | Checkpoint | Validate findings, metrics | → Gap Analysis |
| **ASSESS** | 2-3 | Gap | Current vs Ideal + Prioritize | Gaps quantified |
| **GATE-2** | - | Checkpoint | Recommendations ready | → Plan or Apply |
| **PLAN** | 3.5 | Review | Architectural plan + Q2 (Action/Severity) | User approval |
| **GATE-3** | - | Checkpoint | Approval received or skipped | → Apply |
| **APPLY** | 4 | Fix | Apply recommendations | Changes verified |
| **GATE-4** | - | Checkpoint | applied + failed + needs_approval = total | → Summary |
| **SUMMARY** | 5 | Report | Show gap changes | Done |

**Execution Flow:** SETUP → ANALYZE → GATE-1 → ASSESS → GATE-2 → [PLAN if triggered] → GATE-3 → APPLY → GATE-4 → SUMMARY

### Phase Gates

| Gate | Pass | Fail |
|------|------|------|
| GATE-1 (Post-Analysis) | Findings + metrics valid | Analysis error or missing metrics |
| GATE-2 (Post-Assessment) | coupling + cohesion gaps present | Incomplete gap analysis |
| GATE-3 (Post-Plan) | Approval received or plan skipped | User aborted |
| GATE-4 (Post-Apply) | `applied + failed + needs_approval = total` | Accounting mismatch |

**Plan Review is MANDATORY when findings > 0.**

**Skipped when:** `--auto` mode or 0 findings

---

## Policies

**See Core Rules:** `CCO Operation Standards` for No Deferrals Policy, Intensity Levels, Quality Thresholds, and Accounting invariant.

---

## Step-1a: Scope Selection [Q1]

**Skip if --auto mode (config already set)**

```javascript
AskUserQuestion([
  {
    question: "Which areas to review?",
    header: "Areas",
    options: [
      { label: "Structure (Recommended)", description: "Architecture, design patterns (ARC + PAT)" },
      { label: "Quality (Recommended)", description: "Testing, maintainability (TST + MNT)" },
      { label: "Completeness & Data", description: "API gaps, data management, AI over-engineering (FUN + AIA)" }
    ],
    multiSelect: true
  }
])
```

### Validation
```
[x] User completed Q1 (Areas)
→ Store as: config = { scopes }
→ Proceed to Step-1b (analysis runs all severities)
```

---

## Step-1b: Analyze [PARALLEL SCOPES]

**Run analysis with parallel scope groups - multiple Task calls in same message execute concurrently:**

```javascript
// Map user-selected scopes to agent scopes
const scopeMapping = {
  "Architecture": "architecture",
  "Patterns": "patterns",
  "Testing": "testing",
  "Maintainability": "maintainability",
  "AI-Architecture": "ai-architecture",
  "Functional Completeness": "functional-completeness"
}
const selectedScopes = config.scopes.map(s => scopeMapping[s] || s.toLowerCase())

// PARALLEL EXECUTION: Launch scope groups in single message
// Each Task returns results directly (synchronous)
// Multiple Task calls in same message run in parallel automatically

// Structure group (ARC + PAT)
structureResults = Task("cco-agent-analyze", `
  scopes: ["architecture", "patterns"]
  mode: review

  Analyze architecture and design patterns:
  - ARC-01-15: Coupling score, cohesion score, circular deps, layer violations,
    god classes, feature envy, shotgun surgery, module size, dependency direction,
    missing DI, hardcoded deps, monolith hotspots
  - PAT-01-12: Error handling consistency, logging patterns, async consistency,
    SOLID violations, DRY violations, framework idioms, missing factory/strategy,
    primitive obsession, data clumps, switch smell

  For each finding report: id, scope, severity, title, location (file:line),
  description, recommendation, fixable, effort (LOW/MEDIUM/HIGH),
  impact (LOW/MEDIUM/HIGH), confidence (0-100).

  Also calculate metrics: coupling %, cohesion %, complexity avg.
  Also include techAssessment if technology alternatives found.

  Return: { findings: [...], metrics: {...}, techAssessment: {...} }
`, { model: "haiku", timeout: 120000 })

// Quality group (TST + MNT)
qualityResults = Task("cco-agent-analyze", `
  scopes: ["testing", "maintainability"]
  mode: review

  Analyze testing strategy and maintainability:
  - TST-01-10: Coverage by module, critical path coverage, test-to-code ratio,
    missing edge cases, flaky tests, isolation issues, mock overuse,
    integration gaps, e2e coverage, naming violations
  - MNT-01-12: Complexity hotspots (>15), cognitive complexity, long methods (>50),
    long params (>5), deep nesting (>4), magic numbers in logic,
    missing docs on complex logic, naming inconsistency, missing error context,
    missing cleanup, hardcoded config, missing boundary validation

  For each finding report: id, scope, severity, title, location (file:line),
  description, recommendation, fixable, effort (LOW/MEDIUM/HIGH),
  impact (LOW/MEDIUM/HIGH), confidence (0-100).

  Also calculate metrics: testCoverage %, complexity avg.

  Return: { findings: [...], metrics: {...} }
`, { model: "haiku", timeout: 120000 })

// Completeness group (FUN + AIA)
completenessResults = Task("cco-agent-analyze", `
  scopes: ["functional-completeness", "ai-architecture"]
  mode: review

  Analyze functional completeness and AI architecture drift:
  - FUN-01-18: Missing CRUD, missing pagination, missing filters,
    missing edge cases, incomplete error handling, missing schema validation,
    state transition gaps, missing soft delete, concurrent data access,
    missing timeout config, missing retry strategy, incomplete API surface,
    missing data validation layer, missing caching strategy,
    inefficient data retrieval, missing data consistency,
    missing data indexing, missing bulk operations
  - AIA-01-10: Over-engineering (interface with 1 impl), local solutions,
    architectural drift, pattern inconsistency, premature abstraction,
    framework antipatterns, coupling hotspots, interface bloat,
    god modules, missing abstractions

  For each finding report: id, scope, severity, title, location (file:line),
  description, recommendation, fixable, effort (LOW/MEDIUM/HIGH),
  impact (LOW/MEDIUM/HIGH), confidence (0-100).

  Return: { findings: [...], metrics: {...} }
`, { model: "haiku", timeout: 120000 })

// Merge all parallel results
analysisTask = {
  findings: [
    ...structureResults.findings,
    ...qualityResults.findings,
    ...completenessResults.findings
  ],
  metrics: mergeMetrics([structureResults, qualityResults, completenessResults]),
  techAssessment: structureResults.techAssessment
}

// Filter by user-selected scopes
analysisTask.findings = analysisTask.findings.filter(f => selectedScopes.includes(f.scope))

// IDs: ARC-01-15, PAT-01-12, TST-01-10, MNT-01-12, AIA-01-10, FUN-01-18 (77 checks total)
```

---

## Step-2: Gap Analysis [CURRENT vs IDEAL]

**Results from synchronous analysis:**

```javascript
// agentResponse is already set from Step-1 (synchronous Task call)
agentResponse = analysisTask  // Task returns results directly when synchronous

// Filter by selected scopes
findings = agentResponse.findings.filter(f => selectedScopes.includes(f.scope))
metrics = agentResponse.metrics
techAssessment = agentResponse.techAssessment
```

### Define Ideal State (Based on Project Type)

```javascript
// Read context to determine project type
const projectType = context.type  // CLI, Library, API, Web
const scale = context.scale        // Small, Medium, Large
const maturity = context.maturity  // Prototype, Stable, Legacy

// Define ideal metrics based on project type
const idealMetrics = {
  CLI:     { coupling: 40, cohesion: 75, complexity: 10, coverage: 70 },
  Library: { coupling: 30, cohesion: 80, complexity: 8,  coverage: 85 },
  API:     { coupling: 50, cohesion: 70, complexity: 12, coverage: 80 },
  Web:     { coupling: 60, cohesion: 65, complexity: 15, coverage: 70 }
}

const ideal = idealMetrics[projectType] || idealMetrics.API

// Calculate gaps
const gaps = {
  coupling:   { current: metrics.coupling,   ideal: ideal.coupling,   gap: metrics.coupling - ideal.coupling },
  cohesion:   { current: metrics.cohesion,   ideal: ideal.cohesion,   gap: ideal.cohesion - metrics.cohesion },
  complexity: { current: metrics.complexity, ideal: ideal.complexity, gap: metrics.complexity - ideal.complexity },
  coverage:   { current: metrics.testCoverage, ideal: ideal.coverage, gap: ideal.coverage - metrics.testCoverage }
}

// Determine gap severity (for reporting, not filtering)
function getGapSeverity(gap, threshold) {
  if (gap > threshold * 2) return "HIGH"
  if (gap > threshold) return "MEDIUM"
  if (gap > 0) return "LOW"
  return "OK"
}
```

### Display Current vs Ideal

```markdown
## Current State vs Ideal State

Project Type: {projectType} | Scale: {scale} | Maturity: {maturity}

| Dimension | Current | Ideal | Gap | Severity |
|-----------|---------|-------|-----|----------|
| Coupling | {metrics.coupling}% | <{ideal.coupling}% | {gaps.coupling.gap > 0 ? "HIGH" : "OK"} | {getGapSeverity(gaps.coupling.gap, 10)} |
| Cohesion | {metrics.cohesion}% | >{ideal.cohesion}% | {gaps.cohesion.gap > 0 ? "HIGH" : "OK"} | {getGapSeverity(gaps.cohesion.gap, 10)} |
| Complexity | {metrics.complexity} | <{ideal.complexity} | {gaps.complexity.gap > 0 ? "MEDIUM" : "OK"} | {getGapSeverity(gaps.complexity.gap, 5)} |
| Coverage | {metrics.testCoverage}% | {ideal.coverage}%+ | {gaps.coverage.gap > 0 ? "MEDIUM" : "OK"} | {getGapSeverity(gaps.coverage.gap, 10)} |
```

### Technology Assessment (Ideal vs Chosen)

```javascript
// Only show if agent found alternatives
if (techAssessment && techAssessment.alternatives.length > 0) {
  console.log(`
## Technology Assessment

> "If I were designing from scratch, would I make the same choices?"

| Current Choice | Ideal Alternative | Reason | Effort to Change |
|----------------|-------------------|--------|------------------|
${techAssessment.alternatives.map(a =>
  `| ${a.current} | ${a.alternative} | ${a.reason} | ${a.effort} |`
).join('\n')}

**Recommendation:** ${techAssessment.recommendation}
`)
}
```

### Validation
```
[x] Gap analysis complete
[x] Ideal state defined
→ Proceed to Step-3
```

---

## Step-3: Recommendations [80/20 PRIORITIZED]

**Apply 80/20 prioritization:**

```javascript
// No pre-filtering by severity — all findings kept for post-analysis Q2
filteredFindings = [...findings]

// Categorize by effort level (for REPORTING only, not for filtering what to fix)
filteredFindings.forEach(f => {
  f.effortCategory = calculateEffortCategory(f.effort, f.impact)
})

quickWin = filteredFindings.filter(f => f.impact === "HIGH" && f.effort === "LOW")
moderate = filteredFindings.filter(f => f.impact === "HIGH" && f.effort === "MEDIUM")
complex = filteredFindings.filter(f => f.impact === "MEDIUM")
major = filteredFindings.filter(f => f.impact === "LOW" || f.effort === "HIGH")

// For Quick Wins mode, only keep quickWin
if (config.fixMode === "quick-wins") {
  moderate = []
  complex = []
  major = []
}

totalFindings = quickWin.length + moderate.length + complex.length + major.length
```

**Display findings by effort category (for reporting):**

```markdown
## Findings by Effort Category

Intensity: {config.fixMode} | Scopes: {config.scopes.join(", ")}

### Quick Win (High Impact, Low Effort) - {quickWin.length} items

| # | Severity | ID | Issue | Location | Recommendation |
|---|----------|-----|-------|----------|----------------|
{quickWin.map((f, i) => `| ${i+1} | ${f.severity} | ${f.id} | ${f.title} | ${f.location} | ${f.recommendation} |`)}

### Moderate Effort (High Impact, Medium Effort) - {moderate.length} items

{moderate.map((f, i) => `${i+1}. [${f.severity}] ${f.id}: ${f.title} in ${f.location}`)}

### Complex (Medium Impact) - {complex.length} items
{complex.map((f, i) => `${i+1}. [${f.severity}] ${f.id}: ${f.title} in ${f.location}`)}

### Major (Low Impact or High Effort) - {major.length} items
{major.map((f, i) => `${i+1}. [${f.severity}] ${f.id}: ${f.title} in ${f.location}`)}
```

### Validation
```
[x] Recommendations displayed
[x] Prioritization applied
→ If fixMode = "report-only": Skip to Step-5
→ If findings > 0: Step-3.5 (Plan Review)
→ If findings = 0: Skip to Step-5
```

---

## Step-3.5: Plan Review [MANDATORY]

**"Think before you act"** - For architectural changes, reasoning matters more.

### Trigger Conditions

```javascript
// Plan Review runs whenever there are findings
const planMode = filteredFindings.length > 0

// Skip in --auto mode
const skipPlan = isUnattended

if (planMode && !skipPlan) {
  // → Enter Plan Review
} else {
  // → Skip to Step-4
}
```

### Architectural Plan Generation

**For each recommendation, generate strategic plan:**

```javascript
const architecturalPlans = filteredFindings.map(finding => ({
  id: finding.id,
  title: finding.title,
  scope: finding.scope,  // architecture, patterns, testing, etc.
  severity: finding.severity,

  // STRATEGIC PLAN (architectural reasoning)
  plan: {
    what: finding.recommendation,
    why: generateArchitecturalRationale(finding),    // "Reduces coupling from 72% to ~50%"
    approach: selectArchitecturalApproach(finding),  // "Extract interface + dependency injection"
    alternatives: [
      { approach: "Keep as-is", tradeoff: "Technical debt accumulates" },
      { approach: "Full rewrite", tradeoff: "High effort, risk of regression" },
      { approach: "Incremental refactor", tradeoff: "Recommended - balanced risk/reward" }
    ],
    risks: assessArchitecturalRisks(finding),        // ["May affect 5 dependent modules"]
    affectedModules: findAffectedModules(finding),   // ["auth", "user", "api"]
    estimatedFiles: countAffectedFiles(finding),     // ~12 files
    breakingChanges: detectBreakingChanges(finding)  // true/false
  }
}))
```

### Architectural Plan Display [MANDATORY - DISPLAY BEFORE ASKING]

**[CRITICAL] You MUST display the following table to the user BEFORE asking for approval. NEVER skip this display. NEVER ask "How to proceed?" without first showing the full plan.**

```markdown
## Architectural Plan Review

**Intensity:** {config.fixMode} | **Gaps:** {gapCount} | **Modules Affected:** {uniqueModules.length}

> Architectural changes have wider impact. Review reasoning before proceeding.

### Current vs Ideal State

| Dimension | Current | Target | Gap | Approach |
|-----------|---------|--------|-----|----------|
| Coupling | {metrics.coupling}% | <{ideal.coupling}% | {gaps.coupling.gap}% | {couplingApproach} |
| Cohesion | {metrics.cohesion}% | >{ideal.cohesion}% | {gaps.cohesion.gap}% | {cohesionApproach} |
| Complexity | {metrics.complexity} | <{ideal.complexity} | {gaps.complexity.gap} | {complexityApproach} |

### Planned Changes by Module

#### auth/ (3 changes)
| ID | What | Why | Risk | Conf |
|----|------|-----|------|------|
| ARC-05 | Extract `UserService` from god class | 847 lines → ~200 lines each | Medium - test coverage needed | 85 |
| PAT-01 | Standardize error handling | Inconsistent patterns confuse maintainers | Low | 92 |

#### api/ (2 changes)
| ID | What | Why | Risk | Conf |
|----|------|-----|------|------|
| ARC-04 | Add repository layer | Direct DB access in handlers | Medium - migration needed | 78 |

### Alternatives Considered

For each major change, why this approach:

**ARC-05 (God Class):**
- - Keep as-is: Technical debt grows, 847 lines unmaintainable
- - Full rewrite: 2-week effort, high regression risk
- > **Extract services incrementally**: 3-day effort, testable steps, low risk

**ARC-04 (Missing Layer):**
- - Keep direct access: Coupling increases, testing harder
- > **Repository pattern**: Industry standard, testable, flexible

### Summary

| Metric | Value |
|--------|-------|
| Total recommendations | {filteredFindings.length} |
| Modules affected | {uniqueModules.length} |
| Estimated files | ~{totalEstimatedFiles} |
| Breaking changes | {breakingCount} |
| High confidence (≥80) | {highConfidenceCount} ({highConfidencePercent}%) |
| Medium confidence (60-79) | {mediumConfidenceCount} |
```

### User Decision

```javascript
// Standard Post-Analysis Q2: Action + Severity (same pattern in optimize, align, preflight)
const counts = {
  critical: filteredFindings.filter(f => f.severity === "CRITICAL").length,
  high: filteredFindings.filter(f => f.severity === "HIGH").length,
  medium: filteredFindings.filter(f => f.severity === "MEDIUM").length,
  low: filteredFindings.filter(f => f.severity === "LOW").length
}

AskUserQuestion([
  {
    question: `${filteredFindings.length} finding across ${uniqueModules.length} modules. How to proceed?`,
    header: "Action",
    options: [
      { label: "Fix All (Recommended)", description: `Apply all ${filteredFindings.length} fixes` },
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
      { label: `CRITICAL (${counts.critical})`, description: "Security, data loss, crash" },
      { label: `HIGH (${counts.high})`, description: "Broken functionality" },
      { label: `MEDIUM (${counts.medium})`, description: "Suboptimal but works" },
      { label: `LOW (${counts.low})`, description: "Style, minor improvements" }
    ],
    multiSelect: true
  }
])

switch (actionDecision) {
  case "Fix All":
    config.reviewMode = "apply-all"
    break
  case "By Severity":
    config.reviewMode = "apply-all"
    const selectedSeverities = severityDecision
    filteredFindings = filteredFindings.filter(f => selectedSeverities.some(s => s.startsWith(f.severity)))
    break
  case "Review Each":
    config.reviewMode = "interactive"
    if (severityDecision?.length > 0) {
      filteredFindings = filteredFindings.filter(f => severityDecision.some(s => s.startsWith(f.severity)))
    }
    break
  case "Report Only":
    config.reviewMode = "report-only"
    // Skip to summary
    break
}
```

### Validation
```
[x] Architectural plan generated
[x] Alternatives documented
[x] User decision captured
→ If Abort: Exit
→ Proceed to Step-4 with config.reviewMode
```

---

## Step-4: Apply [BASED ON INTENSITY]

**Determine what to apply:**

```javascript
// filteredFindings already filtered by Q2 severity selection (or all if "Fix All")
let toApply = []
let skipped = []

if (config.reviewMode === "report-only") {
  toApply = []
  skipped = [...quickWin, ...moderate, ...complex, ...major]
} else if (isUnattended) {
  toApply = [...quickWin, ...moderate, ...complex, ...major]
  skipped = []
} else {
  // Q2 already filtered filteredFindings by severity — recategorize
  toApply = [...quickWin, ...moderate, ...complex, ...major]
  skipped = []
}
```

### Pre-Apply Display [MANDATORY]

```markdown
## Applying Recommendations

Intensity: {config.fixMode}

| # | ID | Effort | Issue | Location | Action |
|---|-----|--------|-------|----------|--------|
{toApply.map((item, i) => `| ${i+1} | ${item.id} | ${item.effortCategory} | ${item.title} | ${item.location} | ${item.recommendation} |`)}

Applying: {toApply.length} | Total: {totalFindings}
```

```javascript
if (toApply.length > 0) {
  const isFixAll = config.fixMode === "full-fix"

  applyResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(toApply)}
    fixAll: ${isFixAll}

    Apply architectural recommendations.
    Verify each change doesn't break existing functionality.
    Handle dependencies between fixes.

    ${isFixAll ? `
    FIX-ALL MODE: Fix ALL items. No Deferrals Policy applies (see Core Rules).
    Every item = applied, failed (Technical: reason), or needs_approval (Needs-Approval: reason).
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each recommendation = 1 finding

    Return accounting at FINDING level:
    { applied: <findings_fixed>, failed: <findings_failed>, needs_approval: <findings_needs_approval>, total: <findings_attempted> }
  `, { model: "opus", timeout: 120000 })
}
```

### Validation
```
[x] Selected changes applied
[x] No cascading errors
→ Proceed to Step-4.5 (Approval) or Step-5 (Summary)
```

---

## Step-4.5: Needs-Approval Review [CONDITIONAL]

**Presents needs_approval items to user for decision. Skipped in --auto mode (all items attempted).**

```javascript
if (applyResults.needs_approval > 0 && !isUnattended) {
  const needsApprovalItems = applyResults.details.filter(d => d.status === "needs_approval")

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
    applyResults.applied += approvalResults.applied
    applyResults.failed += approvalResults.failed
    applyResults.needs_approval = 0
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
    }
  }
}
```

### Validation
```
[x] Needs-approval items reviewed (or skipped in --auto)
→ Proceed to Step-5 (Summary)
```

---

## Step-5: Summary

### Calculate Final Counts [CRITICAL]

```javascript
// COUNTING STANDARD
// - total: all findings in selected fixMode scope
// - applied: successfully fixed
// - failed: couldn't fix (technical reason required)
//
// Invariant: applied + failed + needs_approval = total
// NOTE: No "declined" category - AI has no option to decline. Fix, defer (architectural), or fail with reason.

applied = applyResults?.accounting?.applied || 0
failed = applyResults?.accounting?.failed || 0
needs_approval = applyResults?.accounting?.needs_approval || 0

// Verify invariant
assert(applied + failed + needs_approval === toApply.length,
  "Count mismatch: applied + failed + needs_approval must equal toApply.length")
```

### Interactive Mode Output

```markdown
## Align Complete

### Gap Summary
| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Coupling | {before.coupling}% | {after.coupling}% | {delta.coupling} |
| Cohesion | {before.cohesion}% | {after.cohesion}% | {delta.cohesion} |
| Complexity | {before.complexity} | {after.complexity} | {delta.complexity} |
| Coverage | {before.coverage}% | {after.coverage}% | {delta.coverage} |

### Accounting
| Metric | Value |
|--------|-------|
| Fix Mode | {config.fixMode} |
| Scopes | {config.scopes.join(", ")} |
| Files modified | {n} |
| **Total findings** | **{totalFindings}** |

Status: {OK|WARN} | Applied: {applied} | Failed: {failed} | Needs Approval: {needs_approval} | Total: {toApply.length}

${failed > 0 ? `### Failed Items\n${applyResults.details.filter(d => d.status === "failed").map(d => `[${d.severity}] ${d.id}: ${d.title} in ${d.location}`).join('\n')}` : ''}

| Effort Category | Count | Applied | Failed | Needs Approval |
|-----------------|-------|---------|--------|----------|
| Quick Win | {quickWin.length} | {appliedQuickWin} | {failedQuickWin} | {needsApprovalQuickWin} |
| Moderate | {moderate.length} | {appliedModerate} | {failedModerate} | {needsApprovalModerate} |
| Complex | {complex.length} | {appliedComplex} | {failedComplex} | {needsApprovalComplex} |
| Major | {major.length} | {appliedMajor} | {failedMajor} | {needsApprovalMajor} |

**Invariant:** applied + failed + needs_approval = total (effort categories are for reporting only)

Run \`git diff\` to review changes.
```

### Unattended Mode Output (--auto)

```
cco-align: {OK|WARN|FAIL} | Gaps: {gapCount} | Applied: {applied} | Failed: {failed} | Needs Approval: {needs_approval} | Total: {totalFindings}
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

| Scenario | Questions | Total |
|----------|-----------|-------|
| --auto mode | 0 | 0 |
| Interactive, 0 findings | Q1 (Areas) | 1 |
| Interactive, findings | Q1 (Areas) + Q2 (Action/Severity) | 2 |

### Output Schema [STANDARD ENVELOPE]

**All CCO commands use same envelope.**

```json
{
  "status": "OK|WARN|FAIL",
  "summary": "Applied 3, Failed 0, Needs Approval 0, Gaps: coupling 22%, cohesion 15%",
  "data": {
    "accounting": { "applied": 3, "failed": 0, "needs_approval": 0, "total": 3 },
    "gaps": {
      "coupling": { "current": 72, "ideal": 50, "gap": 22 },
      "cohesion": { "current": 55, "ideal": 70, "gap": 15 },
      "complexity": { "current": 12, "ideal": 10, "gap": 2 },
      "coverage": { "current": 65, "ideal": 80, "gap": 15 }
    },
    "effortCategories": { "quickWin": 2, "moderate": 1, "complex": 0, "major": 0 }
  },
  "error": null
}
```

**Status rules:**
- `OK`: failed = 0 AND no gap > 20%
- `WARN`: failed > 0 OR any gap > 20%
- `FAIL`: any CRITICAL gap OR error != null

**--auto mode:** Prints `summary` field only.

### Context Application

| Field | Effect |
|-------|--------|
| Type | CLI → stricter coupling; API → relax coupling |
| Maturity | Legacy → conservative; Greenfield → restructure OK |
| Breaking | Never → flag structural changes as blockers |
| Priority | Speed → Quick wins only; Quality → all findings |
| Scale | 10K+ → performance focus; <100 → simplicity |

### Flags

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode: all scopes, all severities, no questions |
| `--preview` | Analyze only, show gaps and findings, don't apply changes |

### Scope Groups

**Note:** These groupings align with `/cco:optimize` groups to provide consistent mental model.
Both commands group related concerns together: structure (architecture+patterns), quality (testing+maintainability), etc.

| Group | Scopes Included | Checks |
|-------|-----------------|--------|
| **Structure** | architecture + patterns | ARC-01-15, PAT-01-12 (27 checks) |
| **Quality** | testing + maintainability | TST-01-10, MNT-01-12 (22 checks) |
| **Completeness & Data** | functional + ai-architecture | FUN-01-18, AIA-01-10 (28 checks) |

### Model Strategy

**See Core Rules:** `Model Strategy` for Opus/Haiku policy.

### Ideal Metrics by Project Type

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |

### Metric Rationale

**See Core Rules:** `cco-thresholds.md` for detailed metric rationale, sources, and override protocol.

**NEVER recommend changes without evidence (file:line) and rationale.**

### Technology Assessment Rules [CRITICAL]

**NEVER recommend technology changes without:**
1. **Evidence from codebase** - Specific pain points with file:line references
2. **Migration cost** - File count, breaking changes
3. **Team familiarity** - Don't recommend unknown tech

### Gap Severity Calculation

| Gap vs Threshold | Severity |
|------------------|----------|
| >2x threshold | HIGH |
| >1x threshold | MEDIUM |
| >0 | LOW |
| At/better | OK |

Default thresholds: coupling 10%, cohesion 10%, complexity 20%, coverage 10%.

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Fix broke something | `git checkout -- {file}` |
| Multiple files affected | `git checkout .` |
| Want to review | `git diff` |
| Wrong fix mode selected | Re-run and select different option |

---

## Rules

1. **Ideal-first** - Define ideal state before evaluating current
2. **Gap analysis** - Quantify current vs ideal differences
3. **Technology assessment** - Question stack/framework choices
4. **Parallel analysis** - Start analysis immediately
5. **Scope question first** - Q1 collects areas, Q2 post-analysis collects action + severity
6. **80/20 filter** - Prioritize high-impact, low-effort items
7. **Evidence required** - Every recommendation needs file:line reference
8. **Counting consistency** - Count findings, not locations

---

## Reasoning & Guards

**See Core Rules:** `Reasoning`, `Anti-Overengineering Guard`, `Severity Levels` for shared patterns.

**See Core Rules:** `Confidence Scoring` in `cco-thresholds.md` for score calculation, interpretation, and ≥80 threshold.

**Align-specific Step-Back questions:**

| Scope | Step-Back Question |
|-------|-------------------|
| Architecture | "What is the intended system design here?" |
| Patterns | "What patterns does this codebase follow?" |
| Testing | "What is the testing strategy?" |
| Maintainability | "How easy is this code to change?" |
| AI-Architecture | "Has AI introduced inconsistent patterns?" |

---

## Accounting

**Invariant:** `applied + failed + needs_approval = total` (count findings, not locations)

**See Core Rules:** `Accounting` for status definitions and no-declined policy.
