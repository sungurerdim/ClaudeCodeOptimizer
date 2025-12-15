---
name: cco-status
description: Project health dashboard
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Task(*), TodoWrite
---

# /cco-status

**Health Dashboard** - Single view of project health with trends via parallel agents.

Read-only metrics collection and visualization.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Last health tag: !`git tag -l "health-*" --sort=-creatordate | head -1 || echo "None"`

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
| 1 | Collect | Run agent for metrics |
| 2 | Process | Calculate scores and trends |
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

```javascript
agentResponse = Task("cco-agent-analyze", `
  scopes: ["scan", "trends"]
  Linters first → Combined scan + trends data
  Return:
  - metrics: { security, tests, debt, cleanliness, docs }
  - trends: { security_delta, tests_delta, ... }
  - details: { issues[], coverage, complexity }
`)
```

**CRITICAL:** ONE analyze agent. Never spawn separate agents.

### Validation
```
[x] Agent returned valid response
[x] response.metrics exists
[x] response.trends exists
→ Proceed to Step-2
```

---

## Step-2: Process Scores

Calculate final scores:
- Apply context multipliers (Data: PII → security ×2)
- Determine status (OK / WARN / FAIL / CRITICAL)
- Calculate trend indicators (↑ ↓ → ⚠)

| Field | Effect |
|-------|--------|
| Scale | <100 → relaxed; 100-10K → moderate; 10K+ → strict |
| Data | PII/Regulated → security ×2 |
| Priority | Speed → blockers only; Quality → all |

### Validation
```
[x] Scores calculated
[x] Status determined
[x] Trends calculated
→ Proceed to Step-3
```

---

## Step-3: Display Dashboard

Display formatted dashboard with:
- Overall health score
- Category scores (Security, Tests, Debt, Cleanliness, Docs)
- Trend indicators
- Top issues (if any)

### Output Formatting

| Element | Format |
|---------|--------|
| Scores | Right-aligned numbers |
| Status | OK / WARN / FAIL / CRITICAL (centered) |
| Trends | ↑ ↓ → ⚠ indicators |
| Progress | `████░░░░` (8 chars, filled = score/100×8) |

**Prohibited:** No emojis │ No ASCII art │ No unicode decorations

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
| `--focus=X` | Detailed: security, tests, debt, clean |
| `--trends` | Historical trend table |
| `--json` | JSON output |
| `--brief` | Summary only |

### Score Thresholds

| Score | Status |
|-------|--------|
| 80-100 | OK |
| 60-79 | WARN |
| 40-59 | FAIL |
| 0-39 | CRITICAL |

---

## Rules

1. **Sequential execution** - Complete each step before proceeding
2. **Validation gates** - Check validation block before next step
3. **ONE analyze agent** - Never spawn multiple agents
4. **Read-only** - Never modify files
5. **Conservative scores** - When uncertain, score lower
6. **Evidence-based** - Every score needs justification
