---
description: Align codebase with ideal architecture — gap analysis and strategic fixes. Use for architecture review, structural improvements, or design pattern evaluation.
argument-hint: "[--auto] [--preview]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
---

# /cco-align

**Align with Ideal Architecture** — Evaluate as if designing from scratch, compare current state to that ideal.

For tactical file-level fixes, use `/cco-optimize`.

**Scope boundary:** Strategic, architecture-level assessment. Questions design decisions, evaluates pattern consistency across the codebase, identifies structural improvements. Does NOT fix individual code issues (unused imports, missing types, etc.) — for tactical fixes, use `/cco-optimize`.

**Do NOT:** Fix individual code issues (unused imports, type errors, formatting), suggest language or framework migration without strong evidence and migration cost analysis, recommend patterns that require >50% codebase rewrite, or apply changes without verifying they don't break existing tests.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | All 7 scopes, all severities, no questions, single-line summary |
| `--preview` | Analyze only, show gaps and findings, don't apply |

## Context

- Git status: !`git status --short 2>/dev/null | cat`

## Scopes (7 scopes, 87 checks)

| Scope | ID Range | Focus |
|-------|----------|-------|
| architecture | ARC-01 to ARC-15 | Coupling, cohesion, layers, dependencies |
| patterns | PAT-01 to PAT-15 | Design patterns, consistency, SOLID, framework-specific anti-patterns |
| testing | TST-01 to TST-10 | Coverage strategy, test quality, gaps |
| maintainability | MNT-01 to MNT-12 | Complexity, readability, documentation |
| ai-architecture | AIA-01 to AIA-10 | Over-engineering, local solutions, drift |
| functional-completeness | FUN-01 to FUN-18 | API completeness, CRUD, pagination, edge cases, schema validation |
| production-readiness | PRD-01 to PRD-07 | Health endpoints, graceful shutdown, config validation, secret management, deployment hygiene, observability hooks, scaling readiness |

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
    { label: "Production Readiness", description: "production-readiness" },
    { label: "Completeness & Data", description: "functional-completeness + ai-architecture" }
  ],
  multiSelect: true
}])
```

### Phase 2: Analyze [PARALLEL: 4 calls]

If blueprint profile exists in CLAUDE.md, read context (projectType, stack, qualityTarget, dataSensitivity, constraints) and pass to agent calls.

Launch scope groups as parallel Task calls to cco-agent-analyze (mode: review, context: from profile if available) in a SINGLE message WITHOUT `run_in_background`:
- Structure: architecture, patterns
- Quality: testing, maintainability
- Production: production-readiness
- Completeness: functional-completeness, ai-architecture

**Agent invocation:** Send ALL 4 Task calls in one message. Do NOT use `run_in_background` for Task calls. Wait for ALL results before proceeding.

Merge findings. Per CCO Rules: Agent Error Handling — validate agent JSON output, retry once on malformed response, on second failure continue with remaining groups, score failed dimensions as N/A.

**Phase gate:** Do NOT proceed to Phase 3 until all 4 agent groups have returned results or failed.

**Gate:** If findings = 0 → skip Phase 5-6, display gap analysis (Phase 3-4) with: `cco-align: OK | No structural issues | Gaps: {metric table}`

### Phase 3: Gap Analysis [CURRENT vs IDEAL]

If blueprint profile exists in CLAUDE.md: use its Ideal Metrics as targets. Otherwise: use project-type defaults per `/cco-blueprint`.

Calculate gaps: current vs ideal for coupling, cohesion, complexity, coverage. Display Current vs Ideal table.

Technology assessment: if alternatives found, show current vs ideal with migration cost. Recommend only with evidence (file:line).

**Evidence verification:** Before including any gap: read the cited file:line to confirm evidence supports the claim. Remove any gap where cited code does not demonstrate the issue.

### Phase 4: Recommendations [80/20 PRIORITIZED]

Categorize by effort/impact: Quick Win → Moderate → Complex → Major.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

Per CCO Rules: Plan Review Protocol — display findings table (ID, severity, title, file:line), then ask with markdown previews showing scope per option:

```javascript
AskUserQuestion([{
  question: "{totalFindings} findings. How would you like to proceed?",
  header: "Action",
  options: [
    { label: "Fix All (Recommended)", description: "Apply all fixable findings",
      markdown: "{full findings table: ID | Severity | Title | Location}" },
    { label: "By Severity", description: "Choose which severity levels to fix",
      markdown: "CRITICAL: {n}\nHIGH:     {n}\nMEDIUM:   {n}\nLOW:      {n}" },
    { label: "Review Each", description: "Decide on each finding individually",
      markdown: "{full findings table}" },
    { label: "Report Only", description: "No fixes, just save the report" }
  ],
  multiSelect: false
}])
```

If "By Severity": severity multiselect (CRITICAL / HIGH / MEDIUM / LOW).

### Phase 6: Apply

Send to cco-agent-apply (scope: fix, findings: [...], fixAll: --auto). Count findings, not locations. On error: count as failed, continue.

### Phase 6.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

**Phase gate:** After Phase 6 completes, count needs_approval items. If needs_approval = 0, skip to Phase 7.

If needs_approval > 0, display items table (ID, severity, issue, location, reason), then ALWAYS use AskUserQuestion:

```javascript
AskUserQuestion([{
  question: "There are items that need your approval. How would you like to proceed?",
  header: "Approval",
  options: [
    { label: "Fix All (Recommended)", description: "Apply all needs-approval items" },
    { label: "Review Each", description: "Review and decide on each item individually" },
    { label: "Skip All", description: "Leave needs-approval items unfixed" }
  ],
  multiSelect: false
}])
```

### Phase 7: Summary

Per CCO Rules: Accounting — applied + failed + needs_approval = total. No "declined" category. Auto Mode — no questions, no deferrals, fix everything except large architectural changes.

Interactive output format:

```
cco-align complete
==================
| Metric     | Current | Ideal | Gap  |
|------------|---------|-------|------|
| Coupling   |   55%   |  50%  | -5%  |
| Cohesion   |   68%   |  70%  | +2%  |
| Complexity |   14    |  12   | -2   |
| Coverage   |   82%   |  80%  |  OK  |

Recommendations by effort:
  Quick Win:  [PAT-05] Inconsistent error handling in services/api/
  Moderate:   [ARC-03] Circular dependency between handlers and debug
  Complex:    [TST-07] Missing integration test coverage for worker

Applied: 4 | Failed: 0 | Needs Approval: 2 | Total: 6
```

--auto: `cco-align: {OK|WARN|FAIL} | Gaps: N | Applied: N | Failed: N | Needs Approval: N | Total: N`

Status: OK (failed=0, no gap>20%), WARN (failed>0 or gap>20%), FAIL (CRITICAL gap or error).

Next: `/cco-optimize` (fix tactical issues) | `/cco-commit` (commit fixes) | `/cco-blueprint` (track progress)
