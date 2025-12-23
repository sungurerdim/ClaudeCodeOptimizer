---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Edit(*), Task(*), TodoWrite, AskUserQuestion
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

**Start analysis in background while asking Q1:**

```javascript
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
      { label: focusLabel("best-practices", "Best Practices"), description: "Execution patterns, tool usage, efficiency" }
    ],
    multiSelect: true
  },
  {
    question: "Apply recommendations?",
    header: "Apply",
    options: [
      { label: "Do Now only (Recommended)", description: "Apply high-impact, low-effort items" },
      { label: "All recommendations", description: "Apply all - review git diff after" },
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
// Wait for background analysis
agentResponse = await TaskOutput(analysisTask.id)

// Filter by user-selected focus areas
selectedScopes = config.focusAreas.map(f => f.toLowerCase().replace(" & ", "-").replace(" ", "-"))
findings = agentResponse.findings.filter(f => selectedScopes.includes(f.scope))
```

**Display foundation assessment:**

```javascript
// Calculate foundation status
function getFoundationStatus(metrics) {
  const issues = []
  if (metrics.coupling > 70) issues.push("high coupling")
  if (metrics.cohesion < 50) issues.push("low cohesion")
  if (metrics.complexity > 60) issues.push("high complexity")
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

**Apply changes based on user selection in Q1:**

```javascript
let toApply = []

if (config.applyMode === "Do Now only") {
  toApply = doNow
} else if (config.applyMode === "All recommendations") {
  toApply = [...doNow, ...plan, ...consider]
}

if (toApply.length > 0) {
  Task("cco-agent-apply", `
    fixes: ${JSON.stringify(toApply)}
    Apply recommendations.
    Verify each change.
    Handle dependencies between fixes.
  `)
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

```
## Review Complete

Foundation: {foundation}

| Priority | Found | Applied | Skipped |
|----------|-------|---------|---------|
| Do Now | {doNow.length} | {appliedDoNow} | {skippedDoNow} |
| Plan | {plan.length} | {appliedPlan} | {skippedPlan} |
| Consider | {consider.length} | {appliedConsider} | {skippedConsider} |
| Backlog | {backlog.length} | 0 | {backlog.length} |
| **Total** | **{total}** | **{applied}** | **{skipped}** |

Files modified: {n}
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
  "issues": [{ "severity": "{P0-P3}", "title": "{title}", "location": "{file}:{line}" }]
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

### Model Strategy

| Agent | Model | Reason |
|-------|-------|--------|
| cco-agent-analyze | Haiku | Fast, read-only analysis |
| cco-agent-apply | Sonnet | Accurate code modifications |

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

1. **Background analysis** - Start analysis while asking Q1
2. **Single question** - Focus + Apply mode combined in Q1
3. **80/20 filter** - Prioritize high-impact, low-effort items
4. **No follow-up questions** - Apply mode determined upfront
5. **Evidence required** - Every recommendation needs file:line reference
6. **Progressive display** - Show foundation assessment as it completes
