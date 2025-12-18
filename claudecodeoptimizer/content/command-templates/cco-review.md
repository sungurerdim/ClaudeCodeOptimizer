---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Edit(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-review

**Strategic Review** - Parallel analysis with 80/20 prioritization.

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
| 1 | Focus | Ask focus areas | Skip with flags |
| 2 | Analyze | cco-agent-analyze (parallel internally) | Fast |
| 3 | Assessment | Show foundation status | Progressive |
| 4 | Recommendations | 80/20 prioritized list | Instant |
| 5 | Approval | Ask which to apply | Batched |
| 6 | Apply | cco-agent-apply | Verified |
| 7 | Summary | Show results | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select focus areas", status: "in_progress", activeForm: "Selecting focus areas" },
  { content: "Step-2: Run parallel analysis", status: "pending", activeForm: "Running parallel analysis" },
  { content: "Step-3: Show assessment", status: "pending", activeForm: "Showing assessment" },
  { content: "Step-4: Show recommendations", status: "pending", activeForm: "Showing recommendations" },
  { content: "Step-5: Get approval", status: "pending", activeForm: "Getting approval" },
  { content: "Step-6: Apply changes", status: "pending", activeForm: "Applying changes" },
  { content: "Step-7: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Focus Areas

```javascript
AskUserQuestion([{
  question: "Focus areas?",
  header: "Focus",
  options: [
    { label: "Architecture", description: "Dependency graph, coupling, patterns, layers" },
    { label: "Code Quality", description: "Issues with file:line, complexity" },
    { label: "Testing & DX", description: "Test coverage, developer experience" },
    { label: "Best Practices", description: "Tool usage, execution patterns, efficiency" }
  ],
  multiSelect: true
}])
```

**Flags override:** `--focus=X`, `--quick`, `--best-practices` skip this question.

**Dynamic labels based on context:**
- Greenfield maturity → Architecture recommended
- Legacy maturity → Code Quality recommended
- Speed priority → Best Practices recommended

### Validation
```
[x] User selected focus area(s)
→ Store as: focusAreas = {selections[]}
→ Proceed to Step-2
```

---

## Step-2: Analysis [PARALLEL]

**Launch cco-agent-analyze with architecture scope + selected focus areas:**

```javascript
// CRITICAL: All focus areas in ONE cco-agent-analyze call
// Agent handles parallelization internally

Task("cco-agent-analyze", `
  scopes: ["architecture", ...focusAreas.map(f => f.toLowerCase().replace(" & ", "-").replace(" ", "-"))]

  Analyze for each scope:
  - architecture: Dependency graph, coupling metrics, layer violations, pattern consistency
  - quality: Complexity hotspots, code smells, type coverage, error handling
  - testing-dx: Test coverage by module, missing tests, DX friction, CI/CD gaps
  - best-practices: Execution patterns, tool selection, code patterns, anti-patterns

  Return: {
    findings: [{ id: "{SCOPE}-{NNN}", scope, severity: "{P0-P3}", title, location: "{file}:{line}", description, recommendation, effort: "{LOW|MEDIUM|HIGH}", impact: "{LOW|MEDIUM|HIGH}" }],
    metrics: { coupling: "{0-100}", cohesion: "{0-100}", complexity: "{0-100}" },
    scores: { security, tests, techDebt, cleanliness, overall }
  }
`, { model: "haiku" })
```

**Parallel Execution:**
- cco-agent-analyze handles parallelization internally
- Returns combined findings with metrics
- Deduplication handled by agent

### Validation
```
[x] All focus area agents launched in parallel
[x] Results merged
[x] Foundation status determined
→ Proceed to Step-3
```

---

## Step-3: Foundation Assessment [PROGRESSIVE]

Display foundation status as architecture agent completes:

```
## Foundation Assessment

Status: {SOUND|HAS ISSUES}

| Metric | Value | Status |
|--------|-------|--------|
| Coupling | {value} | {status} |
| Complexity (avg) | {value} | {status} |
| Test Coverage | {value}% | {status} |
| Circular Deps | {n} | {status} |
| Layer Violations | {n} | {status} |

Verdict: Foundation is {status} - {recommendation}.
```

| Status | Meaning | Approach |
|--------|---------|----------|
| SOUND | Good base | Incremental improvements |
| HAS ISSUES | Structural problems | Targeted fixes, not rewrites |

### Validation
```
[x] Assessment displayed
→ Proceed to Step-4
```

---

## Step-4: Recommendations [80/20]

Merge all findings and apply 80/20 prioritization:

```javascript
// Calculate effort/impact scores
findings.forEach(f => {
  f.priority = calculatePriority(f.effort, f.impact)
})

// Sort into buckets
doNow = findings.filter(f => f.impact === "HIGH" && f.effort === "LOW")
plan = findings.filter(f => f.impact === "HIGH" && f.effort === "MEDIUM")
consider = findings.filter(f => f.impact === "MEDIUM")
backlog = findings.filter(f => f.impact === "LOW" || f.effort === "HIGH")
```

Display prioritized recommendations:

```
## Recommendations (80/20 Prioritized)

### Do Now (High Impact, Low Effort) - {n} items
1. [{SCOPE}] {title} → {location}
...

### Plan (High Impact, Medium Effort) - {n} items
{n}. [{SCOPE}] {title}
...

### Consider (Medium Impact) - {n} items
{range}. [Various findings...]

### Backlog (Low Impact or High Effort) - {n} items
{range}. [Defer for later...]
```

### Validation
```
[x] Recommendations displayed
[x] Prioritization applied
→ If --no-apply or --quick: Skip to Step-7
→ Proceed to Step-5
```

---

## Step-5: Approval [SKIP if --no-apply or --quick]

```javascript
AskUserQuestion([{
  question: "Apply recommendations?",
  header: "Apply",
  options: [
    { label: `All (${totalCount})`, description: "Apply all - review git diff after" },
    { label: "Do Now only", description: `Apply ${doNow.length} high-impact, low-effort items` },
    { label: "Select individual", description: "Choose specific items" },
    { label: "Skip", description: "Report only, no changes" }
  ],
  multiSelect: false
}])
```

### If Select Individual

**Batched by priority group:**

```javascript
// Do Now items first (most valuable)
if (doNow.length > 0) {
  AskUserQuestion([{
    question: `Apply 'Do Now' items? (${doNow.length} high-impact, low-effort)`,
    header: "Do Now",
    options: [
      ...(doNow.length > 4 ? [{
        label: `All Do Now (${doNow.length})`,
        description: "Apply all high-priority items"
      }] : []),
      ...doNow.slice(0, doNow.length > 4 ? 3 : 4).map(item => ({
        label: `[${item.category}] ${item.title}`,
        description: `${item.file}:${item.line}`
      }))
    ],
    multiSelect: true
  }])
}

// Then Plan items if user wants more
// Skip Consider/Backlog unless explicitly requested
```

### Validation
```
[x] User made selection
→ Store as: approved = {selections[]}, declined = {unselected[]}
→ If Skip: Skip to Step-7
→ Proceed to Step-6
```

---

## Step-6: Apply [SKIP if nothing approved]

```javascript
Task("cco-agent-apply", `
  fixes: ${JSON.stringify(approved)}
  Apply approved recommendations.
  Verify each change.
  Handle dependencies between fixes.
`, { model: "sonnet" })
```

### Validation
```
[x] Approved changes applied
[x] No cascading errors
→ Store as: applied = {count}
→ Proceed to Step-7
```

---

## Step-7: Summary

```
## Review Complete

Foundation: {status}

| Priority | Found | Applied | Declined |
|----------|-------|---------|----------|
| Do Now | {n} | {n} | {n} |
| Plan | {n} | {n} | {n} |
| Consider | {n} | {n} | {n} |
| Backlog | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** |

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

### Context Application

| Field | Effect |
|-------|--------|
| Maturity | Legacy → safe fixes; Greenfield → restructure OK |
| Breaking | Never → flag structural changes as blockers |
| Priority | Speed → Do Now only; Quality → all priorities |
| Scale | 10K+ → performance focus; <100 → simplicity |
| Data | PII/Regulated → security findings elevated |

### Model Strategy

| Agent | Model | Reason |
|-------|-------|--------|
| cco-agent-analyze | Haiku | Fast, read-only analysis |
| cco-agent-apply | Sonnet | Accurate code modifications |

### Quick Mode (`--quick`)

When `--quick` flag:
- Auto-select: Architecture + Code Quality
- Report only (no apply phase)
- Single output, no questions

### Flags

| Flag | Effect |
|------|--------|
| `--quick` | Smart defaults, report only |
| `--focus=X` | architecture, quality, testing, dx, best-practices |
| `--best-practices` | Best practices only |
| `--no-apply` | Report only |
| `--matrix` | Show effort/impact matrix visualization |
| `--do-now-only` | Apply only high-impact, low-effort items |
| `--sequential` | Disable parallel (debug mode) |

---

## Rules

1. **Use cco-agent-analyze** - Agent handles scope parallelization internally
2. **Use cco-agent-apply** - Agent handles verification and cascading
3. **Progressive display** - Show foundation assessment as it completes
4. **80/20 filter** - Prioritize high-impact, low-effort items
5. **Evidence required** - Every recommendation needs file:line reference
