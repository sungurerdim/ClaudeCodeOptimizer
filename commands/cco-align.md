---
description: Align codebase with ideal architecture - current vs ideal state gap analysis
argument-hint: "[--auto] [--preview]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
model: opus
---

# /cco-align

**Align with Ideal Architecture** — "If I designed from scratch, what would be best?"

**Philosophy:** Evaluate as if no technology choices exist yet. Given only the requirements, what's ideal? Compare current state to that ideal.

**Purpose:** Strategic, architecture-level assessment. For tactical file-level fixes, use `/cco-optimize`.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | All 6 scopes, all severities, no questions, single-line summary |
| `--preview` | Analyze only, show gaps and findings, don't apply |

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`

## Scopes (6 scopes, 77 checks)

| Scope | ID Range | Focus |
|-------|----------|-------|
| architecture | ARC-01 to ARC-15 | Coupling, cohesion, layers, dependencies |
| patterns | PAT-01 to PAT-12 | Design patterns, consistency, SOLID |
| testing | TST-01 to TST-10 | Coverage strategy, test quality, gaps |
| maintainability | MNT-01 to MNT-12 | Complexity, readability, documentation |
| ai-architecture | AIA-01 to AIA-10 | Over-engineering, local solutions, drift |
| functional-completeness | FUN-01 to FUN-18 | API completeness, CRUD, pagination, filtering, edge cases, schema validation, state transitions, data management |

## Execution Flow

Setup → Analyze → Gap Analysis → Recommendations → [Plan] → Apply → Summary

### Phase 1: Setup [SKIP if --auto]

```javascript
AskUserQuestion([{
  question: "Which areas should be reviewed?",
  header: "Scopes",
  options: [
    { label: "Structure (Recommended)", description: "architecture + patterns" },
    { label: "Quality (Recommended)", description: "testing + maintainability" },
    { label: "Completeness & Data", description: "functional-completeness + ai-architecture" }
  ],
  multiSelect: true
}])
```

### Phase 2: Analyze [PARALLEL: 3 calls]

Launch scope groups as parallel Task calls to cco-agent-analyze (mode: review):
- Structure: architecture, patterns
- Quality: testing, maintainability
- Completeness: functional-completeness, ai-architecture

Merge findings and metrics. Filter by user-selected scopes.

On error: Validate agent output (check for `error` field, verify `findings` array exists). If output is missing or malformed → retry once. If retry also fails, log error, continue with remaining groups.

### Phase 3: Gap Analysis [CURRENT vs IDEAL]

**If blueprint profile exists** in CLAUDE.md (between `<!-- cco-blueprint-start/end -->`): use its Ideal Metrics section as targets. Blueprint metrics are calibrated to project type + quality level + data sensitivity.

**Fallback** (no blueprint profile): define ideal metrics by project type:

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |
| Monorepo | <35% | >70% | <12 | 75%+ |
| Mobile | <55% | >65% | <12 | 65%+ |
| Infra/IaC | <45% | >70% | <10 | 60%+ |

Calculate gaps: current vs ideal for coupling, cohesion, complexity, coverage. Display Current vs Ideal table.

Technology assessment: if agent found alternatives, show current vs ideal technology choices with migration cost. Recommend tech changes only with evidence (file:line), migration cost, and team familiarity consideration.

### Phase 4: Recommendations [80/20 PRIORITIZED]

Categorize by effort/impact: Quick Win (high impact, low effort) → Moderate → Complex → Major.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

Display architectural plan before asking.

```javascript
AskUserQuestion([
  {
    question: "What action should be taken?",
    header: "Action",
    options: [
      { label: "Fix All (Recommended)", description: "Apply all recommended changes" },
      { label: "By Severity", description: "Choose which severity levels to fix" },
      { label: "Review Each", description: "Approve each finding individually" },
      { label: "Report Only", description: "Don't change anything" }
    ],
    multiSelect: false
  }
])

// Conditional: only when Action = "By Severity"
AskUserQuestion([{
  question: "Which severity levels should be fixed?",
  header: "Severity",
  options: [
    { label: "CRITICAL", description: "Security, data loss, crash" },
    { label: "HIGH", description: "Broken functionality" },
    { label: "MEDIUM", description: "Suboptimal but works" },
    { label: "LOW", description: "Style only" }
  ],
  multiSelect: true
}])
```

### Phase 6: Apply

Send recommendations to cco-agent-apply. Verify changes don't break functionality.

Count findings, not locations.

On error: If apply fails for a finding, count as failed, continue with next.

### Phase 6.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

After apply, if needs_approval > 0:

1. Display items table (ID, severity, issue, location, reason)
2. Ask: Fix All / Review Each

In --auto mode: fix everything except large architectural changes (module reorganization, framework migration, major API redesign).

### Phase 7: Summary

Accounting: `applied + failed + needs_approval = total`. No declined category. Fix, flag for approval (architectural), or fail with technical reason.

Gap summary (before/after for coupling, cohesion, complexity, coverage), applied/failed/total accounting table, effort category breakdown.

--auto mode (no deferrals — never say "too complex", "might break", or "consider later"):

`cco-align: {OK|WARN|FAIL} | Gaps: N | Applied: N | Failed: N | Needs Approval: N | Total: N`

Status: OK (failed=0, no gap>20%), WARN (failed>0 or gap>20%), FAIL (CRITICAL gap or error).
