---
description: Align codebase with ideal architecture - current vs ideal state gap analysis and strategic fixes.
argument-hint: "[--auto] [--preview]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
---

# /cco-align

**Align with Ideal Architecture** — Evaluate as if designing from scratch, compare current state to that ideal.

For tactical file-level fixes, use `/cco-optimize`.

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
| functional-completeness | FUN-01 to FUN-18 | API completeness, CRUD, pagination, edge cases, schema validation |

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

Merge findings. Per CCO Rules: Agent Error Handling.

### Phase 3: Gap Analysis [CURRENT vs IDEAL]

If blueprint profile exists in CLAUDE.md: use its Ideal Metrics as targets. Otherwise: use project-type defaults per `/cco-blueprint`.

Calculate gaps: current vs ideal for coupling, cohesion, complexity, coverage. Display Current vs Ideal table.

Technology assessment: if alternatives found, show current vs ideal with migration cost. Recommend only with evidence (file:line).

**Evidence verification:** Before including any gap: read the cited file:line to confirm evidence supports the claim. Remove any gap where cited code does not demonstrate the issue.

### Phase 4: Recommendations [80/20 PRIORITIZED]

Categorize by effort/impact: Quick Win → Moderate → Complex → Major.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

Per CCO Rules: Plan Review Protocol.

### Phase 6: Apply

Send to cco-agent-apply. Count findings, not locations. On error: count as failed, continue.

### Phase 6.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per CCO Rules: if needs_approval > 0, display items table and ask Fix All / Review Each.

### Phase 7: Summary

Per CCO Rules: Accounting, Auto Mode, Severity Levels.

Gap summary (before/after), applied/failed/total, effort category breakdown.

--auto: `cco-align: {OK|WARN|FAIL} | Gaps: N | Applied: N | Failed: N | Needs Approval: N | Total: N`

Status: OK (failed=0, no gap>20%), WARN (failed>0 or gap>20%), FAIL (CRITICAL gap or error).
