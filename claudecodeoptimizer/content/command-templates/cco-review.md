---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(*), Task(*), TodoWrite, AskUserQuestion
model: opus
---

# /cco-review

**Strategic Review** - Parallel analysis with 80/20 prioritization, single question.

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
| 1 | Setup | Q1: Focus + Apply mode (background analysis starts) | Single question |
| 2 | Analysis | Wait for results, show assessment | Progressive |
| 3 | Recommendations | 80/20 prioritized list | Instant |
| 4 | Apply | Apply selected changes | Verified |
| 5 | Summary | Show results | Instant |

---

## Fix-All Mode

When `--fix-all`: Zero skip, zero decline, backlog included. Complex fix (>50 lines) → ask user. Only technical impossibility = fail. Accounting: `notSelected = 0` always.

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Get review settings", status: "in_progress", activeForm: "Getting settings" },
  { content: "Step-2: Run analysis", status: "pending", activeForm: "Running analysis" },
  { content: "Step-3: Show recommendations", status: "pending", activeForm: "Showing recommendations" },
  { content: "Step-4: Apply changes", status: "pending", activeForm: "Applying changes" },
  { content: "Step-5: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Setup [Q1 + BACKGROUND ANALYSIS]

**Start analysis and dependency check in background while asking Q1:**

```javascript
// Dynamic model selection based on flags and context
// --quick → haiku (speed), standard → haiku, large codebase (10K+) → opus (accuracy)
const analyzeModel = args.includes("--quick") ? "haiku"
  : (context.scale === "10K+" || context.scale === "Large") ? "opus"
  : "haiku"

// Start comprehensive analysis - will filter by focus after Q1
analysisTask = Task("cco-agent-analyze", `
  scopes: ["architecture", "quality", "testing", "best-practices"]

  Analyze for each scope:
  - architecture: Dependency graph, coupling metrics, layer violations, pattern consistency
  - quality: Complexity hotspots, code smells, type coverage, error handling
  - testing: Test coverage by module, missing tests, test quality, CI/CD gaps
  - best-practices: Execution patterns, tool selection, code patterns, anti-patterns

  Return: {
    findings: [{ id, scope, severity, title, location, description, recommendation, effort, impact }],
    metrics: { coupling, cohesion, complexity, testCoverage },
    scores: { security, tests, techDebt, cleanliness, overall }
  }
`, { model: analyzeModel, run_in_background: true })

// Dependency version check (parallel with analysis)
depTask = Task("cco-agent-research", `
  scope: dependency

  Check for outdated dependencies:
  1. Read pyproject.toml, package.json, Cargo.toml, go.mod (whichever exist)
  2. For each dependency, fetch latest stable version from registry
  3. Compare current vs latest, classify update risk

  Return: {
    outdated: [{ package, current, latest, updateType, risk, breaking }],
    security: [{ package, advisory, severity }],
    summary: { total, outdated, security, upToDate }
  }
`, { model: "haiku", run_in_background: true })
```

**Ask Q1 with combined settings:**

```javascript
// Determine recommendations based on context
// Greenfield → Architecture; Legacy → Quality; Speed → Best Practices
contextRecommendation = getContextBasedRecommendation()

// Helper: Add (Recommended) suffix if matches context recommendation
function focusLabel(key, displayName) {
  return contextRecommendation === key ? `${displayName} (Recommended)` : displayName
}

AskUserQuestion([
  {
    question: "Focus areas for review?",
    header: "Focus",
    options: [
      { label: focusLabel("architecture", "Architecture"), description: "Dependency graph, coupling, patterns, layers" },
      { label: focusLabel("quality", "Code Quality"), description: "Complexity, code smells, type coverage" },
      { label: focusLabel("testing", "Testing & DX"), description: "Test coverage, developer experience" },
      { label: focusLabel("best-practices", "Best Practices"), description: "Execution patterns, tool usage, efficiency" },
      { label: focusLabel("dependencies", "Dependencies"), description: "Outdated packages, security advisories, version risks" }
    ],
    multiSelect: true
  },
  {
    question: "Apply recommendations?",
    header: "Apply",
    options: [
      { label: "80/20 - Do Now only (Recommended)", description: "High-impact, low-effort items only" },
      { label: "Full - All recommendations", description: "Apply all including high-effort items" },
      { label: "Fix all", description: "Fix EVERYTHING including backlog - no skipping" },
      { label: "Report only", description: "Show findings without applying" }
    ],
    multiSelect: false
  }
])
```

### Validation
```
[x] User completed Q1
→ Store as: config = { focusAreas, applyMode }
→ Proceed to Step-2
```

---

## Step-2: Analysis [WAIT FOR BACKGROUND]

**Collect results and filter by selected focus:**

```javascript
// Wait for background analysis (parallel)
agentResponse = await TaskOutput(analysisTask.id)
depResponse = await TaskOutput(depTask.id)

// Filter by user-selected focus areas
selectedScopes = config.focusAreas.map(f => f.toLowerCase().replace(" & ", "-").replace(" ", "-"))
findings = agentResponse.findings.filter(f => selectedScopes.includes(f.scope))

// Add dependency findings if selected
if (selectedScopes.includes("dependencies")) {
  depFindings = depResponse.outdated.map(d => ({
    id: `DEP-${d.package}`,
    scope: "dependencies",
    severity: d.security ? "P0" : d.breaking ? "P1" : d.updateType === "major" ? "P2" : "P3",
    title: `${d.package}: ${d.current} → ${d.latest}`,
    location: "pyproject.toml|package.json",
    description: d.breaking ? "Breaking changes in update" : "Update available",
    recommendation: `Update to ${d.latest}`,
    effort: d.breaking ? "HIGH" : "LOW",
    impact: d.security ? "HIGH" : "MEDIUM"
  }))
  findings = [...findings, ...depFindings]
}
```

**Display foundation assessment:**

```javascript
// Calculate foundation status using industry-standard thresholds
// See "Threshold Rationale" in Reference section for justification
function getFoundationStatus(metrics) {
  const issues = []
  if (metrics.coupling > 70) issues.push("high coupling")    // >70% = tight deps, hard to change
  if (metrics.cohesion < 50) issues.push("low cohesion")     // <50% = scattered responsibilities
  if (metrics.complexity > 60) issues.push("high complexity") // >60 avg = maintenance burden
  return issues.length === 0 ? "SOUND" : "HAS ISSUES"
}

foundation = getFoundationStatus(agentResponse.metrics)
```

```
## Foundation Assessment

Status: {foundation}

| Metric | Value | Status |
|--------|-------|--------|
| Coupling | {metrics.coupling}% | {coupling > 70 ? "⚠️" : "✓"} |
| Complexity (avg) | {metrics.complexity} | {complexity > 60 ? "⚠️" : "✓"} |
| Test Coverage | {metrics.testCoverage}% | {coverage < 60 ? "⚠️" : "✓"} |
| Circular Deps | {circularCount} | {circularCount > 0 ? "⚠️" : "✓"} |
| Dependencies | {depResponse.summary.outdated}/{depResponse.summary.total} outdated | {depResponse.summary.security > 0 ? "⚠️" : "✓"} |

Verdict: Foundation is {foundation} - {foundation === "SOUND" ? "incremental improvements" : "targeted fixes needed"}.
```

### Validation
```
[x] Analysis results collected
[x] Foundation status determined
→ Proceed to Step-3
```

---

## Step-3: Recommendations [80/20 PRIORITIZED]

**Apply 80/20 prioritization:**

```javascript
// Calculate effort/impact scores and sort into buckets
findings.forEach(f => {
  f.priority = calculatePriority(f.effort, f.impact)
})

doNow = findings.filter(f => f.impact === "HIGH" && f.effort === "LOW")
plan = findings.filter(f => f.impact === "HIGH" && f.effort === "MEDIUM")
consider = findings.filter(f => f.impact === "MEDIUM")
backlog = findings.filter(f => f.impact === "LOW" || f.effort === "HIGH")

// Track total findings for consistent accounting
totalFindings = doNow.length + plan.length + consider.length + backlog.length
```

**Display prioritized recommendations:**

```
## Recommendations (80/20 Prioritized)

### Do Now (High Impact, Low Effort) - {doNow.length} items
{doNow.map((f, i) => `${i+1}. [${f.scope.toUpperCase()}] ${f.title} → ${f.location}`)}

### Plan (High Impact, Medium Effort) - {plan.length} items
{plan.map((f, i) => `${doNow.length + i + 1}. [${f.scope.toUpperCase()}] ${f.title}`)}

### Consider (Medium Impact) - {consider.length} items
{consider.length} items for future consideration...

### Backlog (Low Impact or High Effort) - {backlog.length} items
{backlog.length} items deferred...
```

### Validation
```
[x] Recommendations displayed
[x] Prioritization applied
→ If applyMode = "Report only": Skip to Step-5
→ Proceed to Step-4
```

---

## Step-4: Apply [BASED ON APPLY MODE]

**Apply changes based on user selection in Q1.**

### Pre-Apply Display [MANDATORY]

**Display ALL items in toApply BEFORE execution:**

```javascript
let toApply = []
let notSelected = []

if (config.applyMode.includes("80/20") || config.applyMode.includes("Do Now")) {
  toApply = doNow
  notSelected = [...plan, ...consider, ...backlog]
} else if (config.applyMode === "Fix all") {
  // Fix-all: EVERYTHING including backlog
  toApply = [...doNow, ...plan, ...consider, ...backlog]
  notSelected = []  // Nothing excluded in fix-all mode
} else if (config.applyMode.includes("Full") || config.applyMode.includes("All")) {
  toApply = [...doNow, ...plan, ...consider]
  notSelected = backlog
}

// CRITICAL: Display ALL items in toApply, not just some priorities
if (toApply.length > 0) {
  console.log(formatApplyTable(toApply))  // Must show ALL toApply items
}
```

```markdown
## Applying Recommendations

Mode: {applyMode}

| # | Priority | Issue | Location | Action |
|---|----------|-------|----------|--------|
{toApply.map((item, i) => `| ${i+1} | ${item.priority} | ${item.title} | ${item.location} | ${item.recommendation} |`)}

Selected: {toApply.length} | Not selected: {notSelected.length} | Total: {totalFindings}

Applying {toApply.length} recommendations...
```

if (toApply.length > 0) {
  // Determine if fix-all mode
  const isFixAll = config.applyMode === "Fix all"

  applyResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(toApply)}
    fixAll: ${isFixAll}

    Apply recommendations.
    Verify each change.
    Handle dependencies between fixes.

    ${isFixAll ? `
    CRITICAL - FIX-ALL MODE:
    - Zero agent-initiated skips/declines allowed
    - ALL items including backlog MUST be fixed
    - Only technical impossibilities can be marked as "fail"
    - Every fail must have reason starting with "Technical:"
    - If fix is complex (>50 lines), return needs_confirmation status
    ` : ""}

    CRITICAL - Counting:
    - Count FINDINGS, not locations
    - Each recommendation = 1 finding

    Return accounting at FINDING level:
    { applied: <findings_fixed>, failed: <findings_failed>, total: <findings_attempted> }
  `, { model: "opus" })  // Opus: 50-75% fewer tool errors
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
// COUNTING STANDARD (same as cco-optimize)
// - selected: items user chose to apply (toApply.length)
// - notSelected: items user didn't choose (backlog, or lower priorities in 80/20 mode)
// - applied: agent successfully fixed
// - failed: agent couldn't fix (was selected but failed)
//
// Invariant: applied + notSelected + failed = total

applied = applyResults?.accounting?.applied || 0
failed = applyResults?.accounting?.failed || 0
notSelected = notSelected.length  // From Step-4: items not in toApply

// Verify: selected items = applied + failed
selectedCount = toApply.length
assert(applied + failed === selectedCount,
  `Selected ${selectedCount} but applied ${applied} + failed ${failed}`)

// Verify: total accounting
assert(applied + notSelected + failed === totalFindings,
  "Count mismatch: applied + notSelected + failed must equal totalFindings")

// By priority breakdown (for detailed table)
// Each priority: how many were in toApply vs notSelected, and of those in toApply, how many applied/failed
```

```
## Review Complete

| Metric | Value |
|--------|-------|
| Foundation | {foundation} |
| Mode | {80/20 \| Full} |
| Files modified | {n} |
| **Total findings** | **{totalFindings}** |

Status: {OK\|WARN} | Applied: {applied} | Not Selected: {notSelected} | Failed: {failed} | Total: {totalFindings}

| Priority | Found | Selected | Applied | Failed |
|----------|-------|----------|---------|--------|
| Do Now | {doNow.length} | {selectedDoNow} | {appliedDoNow} | {failedDoNow} |
| Plan | {plan.length} | {selectedPlan} | {appliedPlan} | {failedPlan} |
| Consider | {consider.length} | {selectedConsider} | {appliedConsider} | {failedConsider} |
| Backlog | {backlog.length} | 0 | 0 | 0 |

**Accounting:** selected = applied + failed | applied + notSelected + failed = total

Run `git diff` to review changes.
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

| Scenario | Tabs | Total Questions |
|----------|------|-----------------|
| Any review | 2 (Focus + Apply) | 1 |

**Key optimization:** Focus areas + apply mode combined in single Q1. No follow-up questions.

### Output Schema (when called as sub-command)

```json
{
  "foundation": "SOUND|HAS ISSUES",
  "metrics": {
    "coupling": "{0-100}",
    "cohesion": "{0-100}",
    "complexity": "{0-100}"
  },
  "doNow": [{ "title": "{title}", "location": "{file}:{line}" }],
  "plan": [{ "title": "{title}", "location": "{file}:{line}" }],
  "issues": [{ "severity": "{CRITICAL|HIGH|MEDIUM|LOW}", "title": "{title}", "location": "{file}:{line}" }]
}
```

### Context Application

| Field | Effect |
|-------|--------|
| Maturity | Legacy → safe fixes; Greenfield → restructure OK |
| Breaking | Never → flag structural changes as blockers |
| Priority | Speed → Do Now only; Quality → all priorities |
| Scale | 10K+ → performance focus; <100 → simplicity |
| Data | PII/Regulated → security findings elevated |

### Quick Mode (`--quick`)

When `--quick` flag:
- Auto-select: Architecture + Code Quality
- Report only (no apply phase)
- Single output, no questions

### Flags

| Flag | Effect |
|------|--------|
| `--quick` | Smart defaults, report only, no questions |
| `--focus=X` | architecture, quality, testing, dx, best-practices |
| `--best-practices` | Best practices only |
| `--no-apply` | Report only |
| `--matrix` | Show effort/impact matrix visualization |
| `--do-now-only` | Apply only high-impact, low-effort items |
| `--fix-all` | Fix EVERYTHING including backlog - no skipping allowed |

### Model Strategy

| Agent | Model | Reason |
|-------|-------|--------|
| cco-agent-analyze | Dynamic | --quick/standard → Haiku (fast); 10K+ scale → Opus (accuracy) |
| cco-agent-apply | Opus | 50-75% fewer tool errors, coding SOTA |

### Threshold Rationale

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Coupling | >70% | Dependencies exceed 70% → changes ripple across codebase, refactoring blocked |
| Cohesion | <50% | Module handles too many unrelated concerns → split into focused units |
| Complexity | >60 avg | Average cyclomatic complexity >60 → high bug density, hard to test |
| Test Coverage | <60% | Below 60% → insufficient safety net for refactoring |
| Circular Deps | >0 | Any circular dependency blocks independent deployability |

**Context Adjustments:**
- Legacy projects: thresholds relaxed by 10%
- Greenfield: thresholds tightened by 10%
- Speed priority: only flag CRITICAL threshold violations

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Fix broke something | `git checkout -- {file}` |
| Multiple files affected | `git checkout .` |
| Want to review | `git diff` |
| Wrong focus selected | Re-run with `--focus=X` |

---

## Rules

1. **Background analysis** - Start analysis + dependency check while asking Q1
2. **Single question** - Focus + Apply mode combined in Q1
3. **80/20 filter** - Prioritize high-impact, low-effort items
4. **Upfront decisions** - Apply mode determined in Q1
5. **Evidence required** - Every recommendation needs file:line reference
6. **Progressive display** - Show foundation assessment as it completes
7. **Dependency audit** - Always check for outdated packages and security advisories
8. **Counting consistency** - Count findings, not locations

---

## Accounting

**Invariant:** `applied + notSelected + failed = total` (count findings, not locations)
