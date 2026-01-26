---
description: Align codebase with ideal architecture - current vs ideal state gap analysis
argument-hint: [--auto] [--intensity=X] [--focus=X] [--report] [--dry-run] [--quick]
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(*), Task(*), AskUserQuestion
model: opus
---

# /align

**Align with Ideal Architecture** - "If I designed from scratch, what would be best?"

> **Implementation Note:** Code blocks use JavaScript-like pseudocode for clarity. Actual execution uses Claude Code tools with appropriate parameters.

**Philosophy:** Evaluate as if no technology choices exist yet. Given only the requirements, what's ideal? Then compare current state to that ideal.

**Purpose:** Strategic, architecture-level assessment. For tactical file-level fixes, use `/optimize`.

**Unique Value:**
- "Would FastAPI be better than Flask here?"
- "Should this be microservices or monolith?"
- "Is Repository pattern missing?"
- "Is this over-engineered by AI?"

## Good Targets vs Bad Targets

**Good align targets (flag these):**
- God classes with >500 lines or >20 methods
- Circular dependencies between modules
- Missing abstraction layers (UI calling DB directly)
- Inconsistent error handling patterns across modules
- Test files with >5 mocks per test (integration candidate)
- Over-engineered AI code (factory for single type)

**Bad align targets (skip these):**
- Simple CRUD with minimal abstraction (appropriate for scale)
- Single-implementation interfaces during prototyping
- Framework-mandated patterns (even if not "ideal")
- Legacy code in maintenance mode (flag but don't prioritize)
- Deliberate trade-offs documented in ADRs

## Align Balance [CRITICAL]

**Avoid over-critical alignment that:**
- Recommends rewrites for working, stable code
- Ignores team context (solo dev vs large team)
- Proposes ideal patterns that add complexity without benefit
- Treats all code as if it's greenfield
- Ignores explicit trade-off decisions in docs/comments

**Consider:**
- Project maturity (prototype → production)
- Team size and skill distribution
- Time-to-market constraints
- Existing technical debt backlog priority

## Scopes

| Scope | ID Range | Focus | Checks |
|-------|----------|-------|--------|
| `architecture` | ARC-01 to ARC-15 | Coupling, cohesion, layers, dependencies | 15 |
| `patterns` | PAT-01 to PAT-12 | Design patterns, consistency, SOLID | 12 |
| `testing` | TST-01 to TST-10 | Coverage strategy, test quality, gaps | 10 |
| `maintainability` | MNT-01 to MNT-12 | Complexity, readability, documentation | 12 |
| `ai-architecture` | AIA-01 to AIA-10 | Over-engineering, local solutions, drift | 10 |
| `functional-completeness` | FUN-01 to FUN-12 | CRUD coverage, edge cases, error handling | 12 |

**Total: 71 checks**

## Context

- Git status: !`git status --short`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

CCO context is auto-loaded from `.claude/rules/cco-context.md` via Claude Code's auto-context mechanism.

**Check:** If auto-context does NOT contain `cco: true` marker:

```javascript
// Fallback: Trigger auto-setup inline (same as SessionStart hook)
// Step 1: Analyze + Questions (parallel)
const configData = await Task("cco-agent-analyze", `
  scope: config

  CCO is not configured for this project.

  Offer setup options first:
  - [Auto-setup] Detect stack and create rules automatically
  - [Interactive] Ask questions to customize setup
  - [Skip] Don't configure CCO for this project

  If Skip → return { skip: true }
  If Auto-setup → detect without questions, return { detected, answers: defaults }
  If Interactive → ask questions while detecting, return { detected, answers }
`, { model: "haiku" })

if (configData.skip) {
  // Exit command gracefully
  return
}

// Step 2: Write files (uses analyze output)
await Task("cco-agent-apply", `
  scope: config
  input: ${JSON.stringify(configData)}

  Write config files and output context for immediate use.
`, { model: "opus" })
```

**After config complete → continue to Step-0 (Mode Detection)**

---

## Mode Detection [CRITICAL]

```javascript
// --auto mode: unattended, full scope, no questions, minimal output
if (args.includes("--auto")) {
  config = {
    intensity: "full-fix",        // All severities
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

| Step | Name | Action | Optimization | Dependency |
|------|------|--------|--------------|------------|
| 0 | Mode | Detect --auto or interactive | Instant | - |
| 1a | Q1 | Fix Intensity + Scope selection | Single question | [PARALLEL] with 1b |
| 1b | Analysis | Start background analysis | Parallel | [PARALLEL] with 1a |
| 2 | Gap Analysis | Current vs Ideal comparison | Progressive | [SEQUENTIAL] after 1b |
| 3 | Recommendations | 80/20 prioritized roadmap | Instant | [SEQUENTIAL] after 2 |
| 4 | Apply | Apply based on intensity | Verified | [SEQUENTIAL] after 3 |
| 5 | Summary | Show results | Instant | [SEQUENTIAL] after 4 |

**Execution Flow:** Step-0 → (1a ‖ 1b) → 2 → 3 → 4 → 5

---

## No Deferrals Policy [CRITICAL]

**AI never decides to skip or defer. User decides.**

### Interactive Mode (default)
When a finding requires complex/architectural changes:
1. **Show the finding** with effort estimate and impact
2. **Ask user**: "This requires architectural changes (~{n} files, {effort}). Fix now? [Yes] [Skip]"
3. **User decides** - AI implements user's choice

### Unattended Mode (--auto)
- **ALL findings fixed** - no questions, no deferrals
- **Architectural changes included** - implement them regardless of complexity
- **Only exit states**: FIXED or TECHNICAL FAILURE (with specific blocker)

### Everything Mode (--intensity=full-fix)
When `--intensity=full-fix` or user selects "Full Fix":
- **ALL findings fixed** - effort categories are for reporting only, not filtering
- **Zero skips** - every finding must be addressed NOW
- **No deferrals** - no "future iteration", no "later pass", no "lower priority"
- **Only exit** - FIXED or TECHNICAL FAILURE (with specific blocker)
- Accounting: `applied + failed = total` (no AI declines allowed)

**Rule:** Exclusion decision belongs to USER, not AI. AI must attempt or ask.

---

## Step-1a: Fix Intensity + Scope Selection [Q1]

**Skip if --auto mode (config already set)**

```javascript
AskUserQuestion([
  {
    question: "What level of changes should be made?",
    header: "Intensity",
    options: [
      { label: "Quick Wins (80/20)", description: "High impact, low effort only" },
      { label: "Standard (Recommended)", description: "CRITICAL + HIGH + MEDIUM severity" },
      { label: "Full Fix", description: "All severities including LOW (complete overhaul)" },
      { label: "Report Only", description: "Analysis only, no changes applied" }
    ],
    multiSelect: false
  },
  {
    question: "Structure scopes to review?",
    header: "Scopes 1/2",
    options: [
      { label: "Architecture (15)", description: "ARC-01-15: coupling, cohesion, layers, dependencies" },
      { label: "Patterns (12)", description: "PAT-01-12: design patterns, SOLID, consistency" },
      { label: "Testing (10)", description: "TST-01-10: coverage, test quality, gaps" }
    ],
    multiSelect: true
  },
  {
    question: "Additional scopes to review?",
    header: "Scopes 2/2",
    options: [
      { label: "Maintainability (12)", description: "MNT-01-12: complexity, readability, docs" },
      { label: "AI-Architecture (10)", description: "AIA-01-10: over-engineering, drift, premature abstraction" },
      { label: "Functional Completeness (12)", description: "FUN-01-12: CRUD coverage, edge cases, error handling" }
    ],
    multiSelect: true
  }
])
```

### Intensity Mapping

| Selection | Severity Filter | Apply Mode |
|-----------|-----------------|------------|
| Quick Wins (80/20) | High impact + low effort only | Apply quick wins |
| Standard | CRITICAL + HIGH + MEDIUM | Apply filtered |
| Full Fix | ALL severities, ALL effort levels | Apply ALL |
| Report Only | ALL (for analysis) | No apply |

### Validation
```
[x] User completed Q1
→ Store as: config = { intensity, scopes, applyMode }
→ Proceed to Step-1b
```

---

## Step-1b: Start Background Analysis

```javascript
// Dynamic model selection
const analyzeModel = args.includes("--quick") ? "haiku"
  : (context.scale === "10K+" || context.scale === "Large") ? "opus"
  : "haiku"

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

// Start comprehensive analysis
analysisTask = Task("cco-agent-analyze", `
  scopes: ${JSON.stringify(selectedScopes)}
  mode: review  // Strategic, architecture-level

  For each scope, analyze and return findings with check IDs:

  ## architecture (ARC-01 to ARC-15)
  - ARC-01: Coupling score (target: <50%)
  - ARC-02: Cohesion score (target: >70%)
  - ARC-03: Circular dependencies
  - ARC-04: Layer violations (UI → DB direct)
  - ARC-05: God classes (>500 lines, >20 methods)
  - ARC-06: Feature envy
  - ARC-07: Shotgun surgery indicators
  - ARC-08: Divergent change indicators
  - ARC-09: Missing abstraction layers
  - ARC-10: Over-abstraction
  - ARC-11: Package/module organization
  - ARC-12: Dependency direction violations
  - ARC-13: Missing dependency injection
  - ARC-14: Hardcoded dependencies
  - ARC-15: Monolith coupling hotspots

  ## patterns (PAT-01 to PAT-12)
  - PAT-01: Inconsistent error handling
  - PAT-02: Inconsistent logging
  - PAT-03: Inconsistent async/await
  - PAT-04: SOLID principle violations
  - PAT-05: DRY violations at codebase level
  - PAT-06: Framework pattern violations
  - PAT-07: Missing factory patterns
  - PAT-08: Missing strategy patterns
  - PAT-09: Primitive obsession
  - PAT-10: Data clumps
  - PAT-11: Switch statement smell
  - PAT-12: Parallel inheritance hierarchies

  ## testing (TST-01 to TST-10)
  - TST-01: Test coverage by module (target: 80%+)
  - TST-02: Critical path coverage
  - TST-03: Test-to-code ratio
  - TST-04: Missing edge case tests
  - TST-05: Flaky test detection
  - TST-06: Test isolation issues
  - TST-07: Mock overuse indicators
  - TST-08: Integration test gaps
  - TST-09: E2E test coverage
  - TST-10: Test naming convention violations

  ## maintainability (MNT-01 to MNT-12)
  - MNT-01: Cyclomatic complexity hotspots (>15)
  - MNT-02: Cognitive complexity issues
  - MNT-03: Long methods (>50 lines)
  - MNT-04: Long parameter lists (>5 params)
  - MNT-05: Deeply nested code (>4 levels)
  - MNT-06: Magic numbers in business logic
  - MNT-07: Missing inline documentation
  - MNT-08: Inconsistent naming
  - MNT-09: Missing error context
  - MNT-10: Resource cleanup patterns missing
  - MNT-11: Hardcoded configuration
  - MNT-12: Missing validation at boundaries

  ## ai-architecture (AIA-01 to AIA-10)
  - AIA-01: Over-engineering (unnecessary layers)
  - AIA-02: Local solution warning (breaks global pattern)
  - AIA-03: Architectural drift (from original design)
  - AIA-04: Pattern inconsistency across modules
  - AIA-05: Premature abstraction (single-use generics)
  - AIA-06: Framework anti-patterns
  - AIA-07: Coupling hotspots (AI-generated tight coupling)
  - AIA-08: Interface bloat (too many methods)
  - AIA-09: God module detection (too many responsibilities)
  - AIA-10: Missing abstraction (should exist but doesn't)

  ## functional-completeness (FUN-01 to FUN-12)
  - FUN-01: Missing CRUD operations (entity without create/read/update/delete)
  - FUN-02: Missing list pagination (collection endpoints without limit/offset)
  - FUN-03: Missing filter support (list endpoints without query params)
  - FUN-04: Missing edge case handling (empty input, null, boundary values)
  - FUN-05: Incomplete error handling (generic errors, missing specific types)
  - FUN-06: Missing validation at boundaries (public APIs without input validation)
  - FUN-07: State transition gaps (undocumented or unvalidated state changes)
  - FUN-08: Missing soft delete (hard delete without audit trail)
  - FUN-09: Concurrent access issues (race conditions, missing locks)
  - FUN-10: Missing timeout configuration (external calls without timeout)
  - FUN-11: Missing retry logic (transient errors without retry)
  - FUN-12: Incomplete API surface (missing endpoints for common operations)

  Return: {
    findings: [{ id, scope, severity, title, location, description, recommendation, effort, impact }],
    metrics: { coupling, cohesion, complexity, testCoverage },
    techAssessment: { stack, alternatives, recommendation }
  }
`, { model: analyzeModel, run_in_background: true })
```

---

## Step-2: Gap Analysis [CURRENT vs IDEAL]

**Wait for analysis and calculate gaps:**

```javascript
agentResponse = await TaskOutput(analysisTask.id)

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
// Filter by intensity FIRST
function matchesIntensity(finding) {
  switch(config.intensity) {
    case "critical-only": return finding.severity === "CRITICAL"
    case "high-priority": return ["CRITICAL", "HIGH"].includes(finding.severity)
    case "quick-wins": return finding.effort === "LOW" && finding.impact === "HIGH"
    case "standard": return ["CRITICAL", "HIGH", "MEDIUM"].includes(finding.severity)
    case "full-fix": return true  // ALL findings, no filtering
    case "report-only": return true  // Show all but don't apply
  }
}

filteredFindings = findings.filter(matchesIntensity)

// Categorize by effort level (for REPORTING only, not for filtering what to fix)
// In Full Fix mode, ALL categories are applied
filteredFindings.forEach(f => {
  f.effortCategory = calculateEffortCategory(f.effort, f.impact)
})

quickWin = filteredFindings.filter(f => f.impact === "HIGH" && f.effort === "LOW")
moderate = filteredFindings.filter(f => f.impact === "HIGH" && f.effort === "MEDIUM")
complex = filteredFindings.filter(f => f.impact === "MEDIUM")
major = filteredFindings.filter(f => f.impact === "LOW" || f.effort === "HIGH")

// For Quick Wins mode, only keep quickWin
if (config.intensity === "quick-wins") {
  moderate = []
  complex = []
  major = []
}

totalFindings = quickWin.length + moderate.length + complex.length + major.length
```

**Display findings by effort category (for reporting):**

```markdown
## Findings by Effort Category

Intensity: {config.intensity} | Scopes: {config.scopes.join(", ")}

### Quick Win (High Impact, Low Effort) - {quickWin.length} items

| # | ID | Issue | Location | Recommendation |
|---|-----|-------|----------|----------------|
{quickWin.map((f, i) => `| ${i+1} | ${f.id} | ${f.title} | ${f.location} | ${f.recommendation} |`)}

### Moderate Effort (High Impact, Medium Effort) - {moderate.length} items

{moderate.map((f, i) => `${i+1}. [${f.id}] ${f.title} in ${f.location}`)}

### Complex (Medium Impact) - {complex.length} items
{complex.map((f, i) => `${i+1}. [${f.id}] ${f.title} in ${f.location}`)}

### Major (Low Impact or High Effort) - {major.length} items
{major.map((f, i) => `${i+1}. [${f.id}] ${f.title} in ${f.location}`)}
```

### Validation
```
[x] Recommendations displayed
[x] Prioritization applied
→ If intensity = "report-only": Skip to Step-5
→ Proceed to Step-4
```

---

## Step-4: Apply [BASED ON INTENSITY]

**Determine what to apply:**

```javascript
let toApply = []
let skipped = []  // Items excluded by intensity filter (not AI declining)

// NOTE: Effort categories (quickWin/moderate/complex/major) are for REPORTING only
// In full-fix mode, ALL items are applied regardless of effort category
switch(config.intensity) {
  case "critical-only":
    toApply = quickWin.filter(f => f.severity === "CRITICAL")
    skipped = [...quickWin.filter(f => f.severity !== "CRITICAL"), ...moderate, ...complex, ...major]
    break
  case "high-priority":
    toApply = [...quickWin, ...moderate].filter(f => ["CRITICAL", "HIGH"].includes(f.severity))
    skipped = [...complex, ...major]
    break
  case "quick-wins":
    toApply = quickWin
    skipped = [...moderate, ...complex, ...major]
    break
  case "standard":
    toApply = [...quickWin, ...moderate, ...complex]
    skipped = major
    break
  case "full-fix":
    // ALL findings applied - effort category is irrelevant
    toApply = [...quickWin, ...moderate, ...complex, ...major]
    skipped = []  // Nothing excluded
    break
  case "report-only":
    toApply = []
    skipped = [...quickWin, ...moderate, ...complex, ...major]
    break
}
```

### Pre-Apply Display [MANDATORY]

```markdown
## Applying Recommendations

Intensity: {config.intensity}

| # | ID | Effort | Issue | Location | Action |
|---|-----|--------|-------|----------|--------|
{toApply.map((item, i) => `| ${i+1} | ${item.id} | ${item.effortCategory} | ${item.title} | ${item.location} | ${item.recommendation} |`)}

Applying: {toApply.length} | Total: {totalFindings}
```

```javascript
if (toApply.length > 0) {
  const isFixAll = config.intensity === "full-fix"

  applyResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(toApply)}
    fixAll: ${isFixAll}

    Apply architectural recommendations.
    Verify each change doesn't break existing functionality.
    Handle dependencies between fixes.

    ${isFixAll ? `
    FULL FIX MODE [MANDATORY]:
    Fix ALL items. Planning metadata (effort/impact/bucket) is for reporting only - ignored here.

    Rules:
    - Zero agent-initiated skips
    - Every item = FIXED or TECHNICAL FAILURE (with "Technical: [reason]")
    - If unsure → ask user, don't skip
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each recommendation = 1 finding

    Return accounting at FINDING level:
    { applied: <findings_fixed>, failed: <findings_failed>, total: <findings_attempted> }
  `, { model: "opus" })
}
```

### Validation
```
[x] Selected changes applied
[x] No cascading errors
→ Proceed to Step-5
```

---

## Step-5: Summary

### Calculate Final Counts [CRITICAL]

```javascript
// COUNTING STANDARD
// - total: all findings in selected intensity scope
// - applied: successfully fixed
// - failed: couldn't fix (technical reason required)
//
// Invariant: applied + failed = total
// NOTE: No "declined" category - AI has no option to decline. Fix or fail with reason.

applied = applyResults?.accounting?.applied || 0
failed = applyResults?.accounting?.failed || 0

// Verify invariant
assert(applied + failed === toApply.length,
  "Count mismatch: applied + failed must equal toApply.length")
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
| Intensity | {config.intensity} |
| Scopes | {config.scopes.join(", ")} |
| Files modified | {n} |
| **Total findings** | **{totalFindings}** |

Status: {OK|WARN} | Applied: {applied} | Failed: {failed} | Total: {toApply.length}

| Effort Category | Count | Applied | Failed |
|-----------------|-------|---------|--------|
| Quick Win | {quickWin.length} | {appliedQuickWin} | {failedQuickWin} |
| Moderate | {moderate.length} | {appliedModerate} | {failedModerate} |
| Complex | {complex.length} | {appliedComplex} | {failedComplex} |
| Major | {major.length} | {appliedMajor} | {failedMajor} |

**Invariant:** applied + failed = total (effort categories are for reporting only)

Run \`git diff\` to review changes.
```

### Unattended Mode Output (--auto)

```
cco-align: {OK|WARN|FAIL} | Gaps: {gapCount} | Applied: {applied} | Failed: {failed} | Total: {totalFindings}
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
| Interactive | Q1 (Intensity + Scopes) | 1 |

### Output Schema (when called as sub-command)

```json
{
  "status": "OK|WARN|FAIL",
  "gaps": {
    "coupling": { "current": 72, "ideal": 50, "gap": 22 },
    "cohesion": { "current": 55, "ideal": 70, "gap": 15 },
    "complexity": { "current": 12, "ideal": 10, "gap": 2 },
    "coverage": { "current": 65, "ideal": 80, "gap": 15 }
  },
  "techAssessment": {
    "alternatives": [{ "current": "Flask", "alternative": "FastAPI", "reason": "async support" }]
  },
  "effortCategories": {
    "quickWin": [{ "id": "ARC-01", "title": "...", "location": "file:line" }],
    "moderate": [],
    "complex": [],
    "major": []
  },
  "accounting": {
    "applied": "{applied_count}",
    "failed": "{failed_count}",
    "total": "{total_count}"
  }
}
```

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
| `--auto` | Unattended mode, all 6 scopes, full-fix intensity, no questions |
| `--intensity=X` | quick-wins, standard, full-fix, report-only |
| `--focus=X` | architecture, patterns, testing, maintainability, ai-architecture, functional-completeness |
| `--quick` | Haiku model, report-only, no questions |
| `--report` | Alias for --intensity=report-only |
| `--dry-run` | Same as --report (show plan, no changes) |

### Model Strategy

| Agent | Model | Reason |
|-------|-------|--------|
| cco-agent-analyze | Dynamic | --quick → Haiku; 10K+ scale → Opus |
| cco-agent-apply | Opus | 50-75% fewer tool errors, architectural changes |

### Ideal Metrics by Project Type

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |

### Metric Rationale [CRITICAL]

**NEVER recommend changes without evidence and rationale.**

| Metric | Target | Why | Source |
|--------|--------|-----|--------|
| Coupling <50% | Industry standard | Martin Fowler's "Refactoring", studies show >50% correlation leads to 2x bug rates | Fowler (1999), IEEE SE studies |
| Cohesion >70% | High cohesion = easier testing | LCOM (Lack of Cohesion) metric, classes <70% harder to unit test | Chidamber & Kemerer metrics |
| God Class <500 lines | Maintenance nightmare | Studies show classes >500 LOC have 3x defect density | NASA/JPL coding standards |
| Complexity <15 | Human working memory | Cognitive complexity limit ~7±2 items, 15 CC maps to ~7 decision points | Miller's Law, McCabe (1976) |
| Coverage 80% | Diminishing returns | 80% catches 90% of bugs, beyond 80% has 3x effort/bug ratio | Google Testing Blog |

### Technology Assessment Rules [CRITICAL]

**NEVER recommend technology changes without:**

1. **Evidence from current codebase** - Specific pain points with file:line references
2. **Migration cost estimate** - File count, breaking changes, estimated effort
3. **Team familiarity consideration** - Don't recommend if team doesn't know it

**Example of BAD recommendation:**
> "Consider switching from Flask to FastAPI for better async support."

**Example of GOOD recommendation:**
> "Flask limitation found in `src/api/users.py:45` - sync endpoint blocking event loop.
> FastAPI alternative: 15 files affected, 2-3 day migration, team has FastAPI experience.
> Evidence: 3 endpoints doing sync DB calls in async context."

### Gap Severity Calculation

```javascript
// Gap severity is calculated, not arbitrary
function getGapSeverity(current, ideal, threshold) {
  const gap = Math.abs(current - ideal)
  const percentGap = gap / ideal * 100

  // Severity based on % deviation from ideal
  if (percentGap > threshold * 2) return "HIGH"      // >2x threshold = HIGH
  if (percentGap > threshold) return "MEDIUM"        // >1x threshold = MEDIUM
  if (percentGap > 0) return "LOW"                   // Any gap = LOW
  return "OK"                                        // At or better than ideal
}

// Default thresholds (can be overridden by project type)
const thresholds = {
  coupling: 10,     // 10% deviation
  cohesion: 10,     // 10% deviation
  complexity: 20,   // 20% deviation (more tolerance)
  coverage: 10      // 10% deviation
}
```

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Fix broke something | `git checkout -- {file}` |
| Multiple files affected | `git checkout .` |
| Want to review | `git diff` |
| Wrong intensity selected | Re-run with `--intensity=X` |

---

## Rules

1. **Ideal-first** - Define ideal state before evaluating current
2. **Gap analysis** - Quantify current vs ideal differences
3. **Technology assessment** - Question stack/framework choices
4. **Background analysis** - Start analysis immediately
5. **Single question** - Intensity + Scopes combined in Q1
6. **80/20 filter** - Prioritize high-impact, low-effort items
7. **Evidence required** - Every recommendation needs file:line reference
8. **Counting consistency** - Count findings, not locations

---

## Reasoning Strategies

### Step-Back (Before Analysis)
Ask broader questions before diving into specifics:

| Scope | Step-Back Question |
|-------|-------------------|
| Architecture | "What is the intended system design here?" |
| Patterns | "What patterns does this codebase follow?" |
| Testing | "What is the testing strategy?" |
| Maintainability | "How easy is this code to change?" |
| AI-Architecture | "Has AI introduced inconsistent patterns?" |

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
Path A: Analyze from "this is a real problem" perspective
Path B: Analyze from "this might be intentional" perspective
Consensus: Both agree → confirm CRITICAL. Disagree → downgrade to HIGH
```

---

## Anti-Overengineering Guard

Before flagging ANY finding:
1. Does this actually break something?
2. Does this confuse users or developers?
3. Is fixing it worth the complexity cost?

**All NO → not a finding.**

NON-findings:
- Small module without full test coverage (if not critical path)
- Missing abstraction that only has one implementation
- Unconventional but working patterns

---

## Severity Definitions

| Severity | Criteria |
|----------|----------|
| CRITICAL | Security risk, data loss, broken core functionality |
| HIGH | Significant architectural violation, blocking refactoring |
| MEDIUM | Suboptimal but functional, minor maintainability issue |
| LOW | Style, minor improvement, nice-to-have |

**When uncertain → choose lower severity.**

---

## Accounting

**Invariant:** `applied + failed = total` (count findings, not locations)

**No "declined" category:** AI has no option to decline fixes. If it's technically possible and user asked for it, it MUST be done. Only "failed" with specific technical reason is acceptable.
