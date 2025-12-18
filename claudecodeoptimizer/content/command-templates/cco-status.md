---
name: cco-status
description: Project health dashboard
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Task(*), TodoWrite
---

# /cco-status

**Health Dashboard** - Snapshot metrics via cco-agent-analyze.

Read-only metrics. No historical tracking, no file generation.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Architecture

| Step | Name | Action |
|------|------|--------|
| 1 | Collect | cco-agent-analyze with scan scope |
| 2 | Process | Apply context multipliers |
| 3 | Display | Show dashboard |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Collect metrics", status: "in_progress", activeForm: "Collecting metrics" },
  { content: "Step-2: Process scores", status: "pending", activeForm: "Processing scores" },
  { content: "Step-3: Display dashboard", status: "pending", activeForm: "Displaying dashboard" }
])
```

---

## Step-1: Collect Metrics

**Use cco-agent-analyze with scan scope:**

```javascript
agentResponse = Task("cco-agent-analyze", `
  scopes: ["scan"]

  Collect metrics for all categories:
  - Security: OWASP, secrets, CVEs, input validation
  - Tests: Coverage %, branch coverage, quality
  - Tech Debt: Complexity, dead code, TODO count
  - Cleanliness: Orphans, duplicates, stale refs

  Return: {
    scores: { security, tests, techDebt, cleanliness, overall },
    status: "OK|WARN|FAIL|CRITICAL",
    topIssues: [{ category, title, location }]
  }
`)
```

**Agent handles parallelization internally** (parallel grep patterns, parallel linters).

### Validation
```
[x] Agent returned valid response
[x] response.scores exists
[x] response.status exists
→ Proceed to Step-2
```

---

## Step-2: Process Scores

Merge parallel results and calculate:

```javascript
// Aggregate from 5 parallel responses
metrics = {
  security: securityAgent.score,
  tests: testsAgent.score,
  debt: debtAgent.score,
  cleanliness: cleanlinessAgent.score,
  docs: docsAgent.score
}

// Apply context multipliers
if (context.data === "PII" || context.data === "Regulated") {
  metrics.security *= 2  // Weight security higher
}

// Calculate overall
overall = weightedAverage(metrics, weights)
status = getStatus(overall)  // OK/WARN/FAIL/CRITICAL
```

| Field | Effect |
|-------|--------|
| Scale | <100 → relaxed; 100-10K → moderate; 10K+ → strict |
| Data | PII/Regulated → security ×2 |
| Priority | Speed → blockers only; Quality → all |

### Validation
```
[x] All metrics merged
[x] Multipliers applied
[x] Status determined
→ Proceed to Step-3
```

---

## Step-3: Display Dashboard

```
┌─────────────────────────────────────────────┐
│  PROJECT HEALTH                   [{status}]│
├─────────────────────────────────────────────┤
│  Security    {progress}  {score}  {status}  │
│  Tests       {progress}  {score}  {status}  │
│  Tech Debt   {progress}  {score}  {status}  │
│  Cleanliness {progress}  {score}  {status}  │
├─────────────────────────────────────────────┤
│  Overall     {progress}  {score}  {status}  │
└─────────────────────────────────────────────┘

Top Issues ({n}):
1. [{CATEGORY}] {title} in {file}:{line}
2. [{CATEGORY}] {title} in {file}:{line}
3. [{CATEGORY}] {title} in {file}:{line}
```

### Output Formatting

| Element | Format |
|---------|--------|
| Scores | Right-aligned numbers |
| Status | OK / WARN / FAIL / CRITICAL |
| Progress | `████░░░░` (8 chars, filled = score/100×8) |

**Prohibited:** No emojis │ No ASCII art │ No unicode decorations │ No trend indicators

### Validation
```
[x] Dashboard displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Flags

| Flag | Effect |
|------|--------|
| `--focus=X` | Detailed view: security, tests, debt, clean |
| `--json` | JSON output |
| `--brief` | Summary only (overall score + status) |

### Score Thresholds

| Score | Status |
|-------|--------|
| 80-100 | OK |
| 60-79 | WARN |
| 40-59 | FAIL |
| 0-39 | CRITICAL |

---

## Rules

1. **Use cco-agent-analyze** - Agent handles parallelization internally
2. **Snapshot only** - No historical tracking, no trend indicators
3. **Read-only** - Never modify files, never create files
4. **Conservative scores** - When uncertain, score lower
5. **Evidence-based** - Every score needs file:line reference
