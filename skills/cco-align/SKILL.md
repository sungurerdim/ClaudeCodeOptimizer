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
| `--auto` | All 8 scopes, all severities, no questions, single-line summary |
| `--preview` | Analyze only, show gaps and findings, don't apply |

## Context

- Git status: !`git status --short --branch`

## Scopes (8 scopes, 92 checks)

Per cco-agent-analyze: Review Scopes — architecture, patterns, testing, maintainability, ai-architecture, functional-completeness, production-readiness, cross-cutting.

## Execution Flow

Setup → Analyze → Gap Analysis → Recommendations → [Plan] → Apply → Summary

### Phase 1: Setup [SKIP if --auto]

**Pre-flight:** Verify git repo: `git rev-parse --git-dir 2>/dev/null` → not a repo: warn "Not a git repo — git context unavailable" and continue (git optional for align).

```javascript
AskUserQuestion([{
  question: "Which areas should be reviewed?",
  header: "Scopes",
  options: [
    { label: "Structure (Recommended)", description: "architecture + patterns + cross-cutting" },
    { label: "Quality (Recommended)", description: "testing + maintainability" },
    { label: "Production Readiness", description: "production-readiness" },
    { label: "Completeness & Data", description: "functional-completeness + ai-architecture" }
  ],
  multiSelect: true
}])
```

### Phase 2: Analyze [BATCHED: 2+2]

If blueprint profile exists in CLAUDE.md, read context (projectType, stack, qualityTarget, dataSensitivity, constraints) and pass to agent calls.

Per CCO Rules: Parallel Execution, Agent Contract, Model Routing.

| Batch | Tracks | Model |
|-------|--------|-------|
| 1 | Structure (architecture, patterns, cross-cutting) + Quality (testing, maintainability) — mode: review | sonnet |
| 2 | Production (production-readiness) + Completeness (functional-completeness, ai-architecture) — mode: review | sonnet |

Wait for ALL batches. Phase gate: do not proceed until all tracks return or fail.

Merge findings. Per CCO Rules: CRITICAL Escalation — if any CRITICAL findings, run single opus validation call before proceeding.

**Gate:** If findings = 0 → skip Phase 5-6, display gap analysis (Phase 3-4) with: `cco-align: OK | No structural issues | Gaps: {metric table}`

### Phase 3: Gap Analysis [CURRENT vs IDEAL]

If blueprint profile exists in CLAUDE.md: use its Ideal Metrics as targets. Otherwise: use project-type defaults per `/cco-blueprint`.

Calculate gaps: current vs ideal for coupling, cohesion, complexity, coverage. Display Current vs Ideal table.

Technology assessment: if alternatives found, show current vs ideal with migration cost. Recommend only with evidence (file:line).

**Evidence verification:** Before including any gap: read the cited file:line to confirm evidence supports the claim. Remove any gap where cited code does not demonstrate the issue.

**Decision quality check:** For key technology decisions detected in the codebase (stack, framework, data model, auth, deployment), evaluate:

| Decision | Current | Rationale | Alternative | Trade-off | Assessment |
|----------|---------|-----------|-------------|-----------|------------|

- **OK** — fits context, no clearly superior alternative
- **Questionable** — concrete alternative may be better (show evidence)
- **Problematic** — actively causing issues (show evidence at file:line)

Include only Questionable/Problematic. OK decisions go in summary strengths.

**Strategic gap check (human-judgment issues not caught by pattern analysis):**

| Area | Question | Evidence Source |
|------|----------|----------------|
| Tech debt trajectory | Accumulating or decreasing? Where concentrated? | TODO/FIXME density, complex regions |
| Evolution capacity | Next major change — what breaks first? | Coupling hotspots, hardcoded values |
| Scale ceiling | At what point does architecture fail? Realistic? | Data structures, I/O patterns |

Include only areas where concrete risk is identified with evidence. Speculative gaps excluded.

### Phase 4: Recommendations [80/20 PRIORITIZED]

Categorize by effort/impact: Quick Win → Moderate → Complex → Major.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

Per CCO Rules: Plan Review Protocol — display findings table (ID, severity, title, file:line), then ask with markdown previews. Options: Fix All (recommended) / By Severity / Review Each / Report Only.

### Phase 6: Apply [SKIP if --preview]

Send to cco-agent-apply (scope: fix, findings: [...], fixAll: --auto). Count findings, not locations. On error: count as failed, continue.

### Phase 6.1: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per CCO Rules: Needs-Approval Protocol.

### Phase 7: Summary

Per CCO Rules: Accounting, Auto Mode.

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
