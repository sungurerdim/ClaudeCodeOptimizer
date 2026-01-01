---
name: cco-review
description: |
  Architecture review with 80/20 prioritization.
  TRIGGERS: "review", "architecture", "coupling", "dependencies", "refactor plan"
  USE WHEN: Need strategic view of codebase health
  FLAGS: --quick, --focus=X, --fix-all, --matrix
  OUTPUTS: Foundation assessment, Do Now/Plan/Consider/Backlog prioritization
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

## Everything Mode [CRITICAL]

When `--fix-all` or user selects "Everything":
- **Zero deferrals** - no "future iteration", no "later pass", no "lower priority"
- **Zero skips** - every finding must be addressed NOW
- **Backlog included** - architectural refactoring happens in this pass
- **Complex fixes** - implement them, don't defer them
- **Only exit** - FIXED or TECHNICAL FAILURE (with specific blocker)
- Accounting: `notSelected = 0` always

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
      { label: "Essential (Recommended)", description: "High-impact, low-effort only (Do Now)" },
      { label: "Thorough", description: "Do Now + Plan + Consider (skip backlog)" },
      { label: "Everything", description: "All findings including backlog" },
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
    severity: d.security ? "CRITICAL" : d.breaking ? "HIGH" : d.updateType === "major" ? "MEDIUM" : "LOW",
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

if (config.applyMode.includes("Essential")) {
  toApply = doNow
  notSelected = [...plan, ...consider, ...backlog]
} else if (config.applyMode.includes("Thorough")) {
  toApply = [...doNow, ...plan, ...consider]
  notSelected = backlog
} else if (config.applyMode.includes("Everything")) {
  // Everything: ALL findings including backlog
  toApply = [...doNow, ...plan, ...consider, ...backlog]
  notSelected = []  // Nothing excluded
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
  const isFixAll = config.applyMode.includes("Everything")

  applyResults = Task("cco-agent-apply", `
    fixes: ${JSON.stringify(toApply)}
    fixAll: ${isFixAll}

    Apply recommendations.
    Verify each change.
    Handle dependencies between fixes.

    ${isFixAll ? `
    CRITICAL - EVERYTHING MODE [MANDATORY]:
    You MUST fix every single item. No exceptions. No deferrals.

    FORBIDDEN responses:
    - "recommended for future iteration" - NO, fix it NOW
    - "lower priority" - NO, user chose Everything, priority is NOW
    - "would benefit from dedicated pass" - NO, this IS that pass
    - "architectural refactoring" - YES, do the refactoring NOW
    - Any suggestion to skip or defer - FORBIDDEN

    Rules:
    - Zero agent-initiated skips/declines
    - Every item = either FIXED or TECHNICAL FAILURE
    - Technical failure requires specific reason: "Technical: [exact blocker]"
    - Complex fix (>50 lines) → implement it, don't defer it
    - If unsure how to fix → ask user, don't skip

    User explicitly chose "Everything". Respect that choice.
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
| Mode | {Essential \| Thorough \| Everything} |
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
| `--do-now-only` | Essential mode - apply only high-impact, low-effort items |
| `--fix-all` | Everything mode - apply all findings including backlog |

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

## Reasoning Strategies

### Step-Back (Before Analysis)
Ask broader questions before diving into specifics:

| Focus Area | Step-Back Question |
|------------|-------------------|
| Architecture | "What is the intended system design here?" |
| Quality | "What are the quality standards for this codebase?" |
| Testing | "What is the testing strategy?" |
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
- Missing type hints in internal helpers
- Unconventional but working patterns

---

## Severity Definitions

| Severity | Criteria |
|----------|----------|
| CRITICAL | Security risk, data loss, broken core functionality |
| HIGH | Significant bug, architectural violation, doc mismatch |
| MEDIUM | Suboptimal but functional, minor DX issue |
| LOW | Style, minor improvement, nice-to-have |

**When uncertain → choose lower severity.**

---

## Accounting

**Invariant:** `applied + notSelected + failed = total` (count findings, not locations)
