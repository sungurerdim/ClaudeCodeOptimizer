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
  - Security: Secrets, OWASP, CVEs, input validation
  - Quality: Type errors, tech debt, test gaps, complexity
  - Architecture: SOLID violations, coupling, circular deps
  - Best Practices: Resource management, patterns, consistency

  Scoring: Start at 100, deduct for issues (critical: -10, high: -5, medium: -2, low: -1)
`)

// Agent returns (matches cco-agent-analyze scan output schema):
// agentResponse = {
//   scores: { security, quality, architecture, bestPractices, overall },
//   status: "OK|WARN|FAIL|CRITICAL",
//   topIssues: [{ category, title, location }],
//   summary: "{assessment}"
// }
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

Apply context multipliers:

```javascript
metrics = {
  security: response.scores.security,
  quality: response.scores.quality,
  architecture: response.scores.architecture,
  bestPractices: response.scores.bestPractices
}

// Apply context multipliers from context.md
if (context.data === "PII" || context.data === "Regulated") {
  metrics.security = Math.max(0, metrics.security * 0.8)  // Stricter for sensitive data
}

if (context.scale === "10K+") {
  metrics.architecture = Math.max(0, metrics.architecture * 0.9)  // Stricter for large scale
}

// Calculate overall (equal weights)
overall = (metrics.security + metrics.quality + metrics.architecture + metrics.bestPractices) / 4
status = getStatus(overall)  // OK/WARN/FAIL/CRITICAL
```

| Context | Effect |
|---------|--------|
| Scale 10K+ | Architecture score stricter |
| PII/Regulated | Security score stricter |
| Speed priority | Show critical issues only |

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
## Quality Score: {overall}/100  [{status}]

| Category       | Score | Status |
|----------------|-------|--------|
| Security       | {n}   | {OK/WARN/FAIL} |
| Quality        | {n}   | {OK/WARN/FAIL} |
| Architecture   | {n}   | {OK/WARN/FAIL} |
| Best Practices | {n}   | {OK/WARN/FAIL} |

Top Issues ({n}):
- [{CATEGORY}] {title} ({file}:{line})
- [{CATEGORY}] {title} ({file}:{line})
- [{CATEGORY}] {title} ({file}:{line})

Run `/cco-optimize` to fix issues.
```

### Output Formatting

| Element | Format |
|---------|--------|
| Scores | 0-100 integers |
| Status | OK (80+) / WARN (60-79) / FAIL (40-59) / CRITICAL (<40) |
| Issues | Max 5 shown, most critical first |

**Output style:** Plain text tables, numerical scores, text status values only

### Validation
```
[x] Dashboard displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Output Schema (when called as sub-command)

When called via `/cco-status --brief` (e.g., from cco-checkup):

```json
{
  "scores": {
    "security": "{0-100}",
    "quality": "{0-100}",
    "architecture": "{0-100}",
    "bestPractices": "{0-100}",
    "overall": "{0-100}"
  },
  "status": "OK|WARN|FAIL|CRITICAL"
}
```

**Mapping from agent response:**
- `scores` ← `cco-agent-analyze.scores` (with context multipliers applied)
- `status` ← calculated from `overall` score

### Flags

| Flag | Effect |
|------|--------|
| `--focus=X` | Detailed view: security, quality, architecture, best-practices |
| `--json` | JSON output |
| `--brief` | Overall score + status only |

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
2. **Snapshot only** - Current state only, fresh metrics each run
3. **Read-only** - Analysis and reporting only, preserve file state
4. **Conservative scores** - When uncertain, score lower
5. **Evidence-based** - Every score needs file:line reference
