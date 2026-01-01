---
name: cco-status
description: |
  Project health dashboard with quality scores.
  TRIGGERS: "status", "health", "score", "metrics", "dashboard"
  USE WHEN: Quick snapshot of project quality
  FLAGS: --focus=X, --json, --brief
  OUTPUTS: Security/Quality/Architecture/Best-Practices scores (0-100)
allowed-tools: Read(*), Grep(*), Glob(*), Bash(*), Task(*)
---

# /cco-status

**Health Dashboard** - Quick snapshot via cco-agent-analyze.

Read-only. No TodoWrite - single agent call + display.

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

---

## Execution

### 1. Collect Metrics

```javascript
response = Task("cco-agent-analyze", `
  scopes: ["scan"]

  Collect metrics for all categories:
  - Security: Secrets, OWASP, CVEs, input validation
  - Quality: Type errors, tech debt, test gaps, complexity
  - Architecture: SOLID violations, coupling, circular deps
  - Best Practices: Resource management, patterns, consistency

  Scoring: Start at 100, deduct per issue (critical: -10, high: -5, medium: -2, low: -1)
`, { model: "haiku" })
```

### 2. Apply Context Multipliers

```javascript
metrics = response.scores

// Stricter for sensitive data
if (context.data === "PII" || context.data === "Regulated") {
  metrics.security *= 0.8
}

// Stricter for large scale
if (context.scale === "10K+") {
  metrics.architecture *= 0.9
}

overall = (metrics.security + metrics.quality + metrics.architecture + metrics.bestPractices) / 4
status = overall >= 80 ? "OK" : overall >= 60 ? "WARN" : overall >= 40 ? "FAIL" : "CRITICAL"
```

### 3. Display Dashboard

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

Run `/cco-optimize` to fix issues.
```

---

## Flags

| Flag | Effect |
|------|--------|
| `--focus=X` | Detailed view: security, quality, architecture, best-practices |
| `--json` | JSON output |
| `--brief` | Overall score + status only |

## Score Thresholds

| Score | Status | Meaning |
|-------|--------|---------|
| 80-100 | OK | Production-ready |
| 60-79 | WARN | Address before release |
| 40-59 | FAIL | Requires attention |
| 0-39 | CRITICAL | Fix immediately |

---

## Rules

1. **Single agent call** - cco-agent-analyze handles all collection
2. **Read-only** - No file modifications
3. **Fast** - No TodoWrite, minimal overhead
