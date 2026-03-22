---
description: Review codebase quality and architecture — tactical fixes and strategic alignment in one skill. Use for code review, security audit, architecture assessment, or cleanup.
argument-hint: "[--quality] [--architecture] [--auto] [--preview] [--force-approve]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Bash
  - Task
  - AskUserQuestion
---

# /cco-review

**Code Review** — Quality fixes and architecture alignment in a single skill.

Two modes: `--quality` for file-level fixes, `--architecture` for strategic assessment.

**Default:** `--quality` when no mode specified.

## Args

| Flag | Effect |
|------|--------|
| `--quality` | File-level fixes: security, hygiene, types, performance, privacy (default) |
| `--architecture` | Architecture-level: patterns, coupling, testing, production readiness |
| `--auto` | All scopes, all severities, no questions, single-line summary |
| `--preview` | Analyze and report findings without applying fixes |
| `--scope=<name>` | Specific scope(s), comma-separated |
| `--loop` | Re-run until clean or max 3 iterations (quality mode only) |
| `--force-approve` | Auto-apply needs_approval items. Combines with `--auto`. |

## State Management

Per CCO Rules: State Management. This skill uses task prefix `[REV]`.

| Task | Created | Completed |
|------|---------|-----------|
| `[REV] Analyze Batch 1` | Phase 2 Batch 1 launch | Batch 1 done |
| `[REV] Analyze Batch 2` | Phase 2 Batch 2 launch | Batch 2 done |
| `[REV] Plan Review` | Phase 3 start | Phase 3 end |
| `[REV] Apply` | Phase 4 start | Phase 4 end |
| `[REV] Summary` | Phase 5 start | Phase 5 end |

**Recovery:** At Phase 1 start, run TaskList. If `[REV]` tasks exist with incomplete status → per State Management recovery protocol.

## Context

- Git status: !`git status --short --branch`
- Args: $ARGUMENTS

## Scopes

### Quality Scopes (--quality)

Per cco-agent-analyze: Optimize Scopes — security, hygiene, types, performance, ai-hygiene, robustness, privacy, doc-sync, simplify.

9 scopes, 97 checks.

| Group | Scopes |
|-------|--------|
| Security & Privacy | security, robustness, privacy |
| Code Quality | hygiene, types, simplify |
| Performance | performance |
| AI Cleanup | ai-hygiene, doc-sync |

**Scope boundary:** Tactical, file-level fixes within current architecture. Finds repeated code blocks, unnecessary abstractions, missing types — does NOT question architectural decisions. If an issue requires architectural change, report as `needs_approval`.

### Architecture Scopes (--architecture)

Per cco-agent-analyze: Review Scopes — architecture, patterns, testing, maintainability, ai-architecture, functional-completeness, production-readiness, cross-cutting.

8 scopes, 92 checks.

| Group | Scopes |
|-------|--------|
| Structure | architecture, patterns, cross-cutting |
| Quality | testing, maintainability |
| Production Readiness | production-readiness |
| Completeness | functional-completeness, ai-architecture |

**Scope boundary:** Strategic, architecture-level assessment. Questions design decisions, evaluates pattern consistency. Does NOT fix individual code issues.

## Execution Flow

Setup → Analyze → [Gap Analysis] → [Plan] → Apply → Summary

### Phase 1: Setup [SKIP if --auto]

**Pre-flight:** Verify git repo: `git rev-parse --git-dir 2>/dev/null` → not a repo: warn and continue.

**Recovery check:** TaskList → filter `[REV]` prefix. If incomplete tasks found → per State Management recovery protocol.

**Quality mode:**
```javascript
AskUserQuestion([
  {
    question: "Which areas should be checked?",
    header: "Scopes",
    options: [
      { label: "Security & Privacy (Recommended)", description: "SEC + ROB + PRV" },
      { label: "Code Quality (Recommended)", description: "HYG + TYP + SIM" },
      { label: "Performance", description: "PRF" },
      { label: "AI Cleanup", description: "AIH + DOC" }
    ],
    multiSelect: true
  }
])
```

**Architecture mode:**
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

If blueprint profile exists in CLAUDE.md, read context and pass to agent calls.

Per CCO Rules: Parallel Execution, Agent Contract, Model Routing.

**Quality mode:**

| Batch | Tracks | Model |
|-------|--------|-------|
| 1 | Security & Privacy + Code Quality — mode: auto | haiku |
| 2 | Performance + AI Cleanup — mode: auto | haiku |

**Architecture mode:**

| Batch | Tracks | Model |
|-------|--------|-------|
| 1 | Structure + Quality — mode: review | sonnet |
| 2 | Production + Completeness — mode: review | sonnet |

Wait for ALL batches. Phase gate: do not proceed until all tracks return or fail.

**State update:** After each batch, TaskCreate + TaskUpdate `[REV] Analyze Batch N` → completed, write findings to description in compact format.

Merge findings. Per CCO Rules: CRITICAL Escalation — if any CRITICAL findings, run single opus validation call before proceeding.

**Gate:** If findings = 0 → skip to summary.

### Phase 3: Gap Analysis [ARCHITECTURE MODE ONLY]

TaskCreate `[REV] Gap+Recs` (status: in_progress).

If blueprint profile exists in CLAUDE.md: use its Ideal Metrics as targets. Otherwise: use project-type defaults per `/cco-blueprint`.

Calculate gaps: current vs ideal for coupling, cohesion, complexity, coverage. Display Current vs Ideal table.

Technology assessment: if alternatives found, show current vs ideal with migration cost. Recommend only with evidence (file:line).

**Evidence verification:** Before including any gap: read the cited file:line to confirm.

**Decision quality check:** For key technology decisions, evaluate as OK / Questionable / Problematic. Include only Questionable/Problematic.

Categorize recommendations by effort/impact: Quick Win → Moderate → Complex → Major.

### Phase 4: Plan Review [findings > 0, SKIP if --auto]

TaskCreate `[REV] Plan Review` (status: in_progress).

Per CCO Rules: Plan Review Protocol — display findings table (ID, severity, title, file:line). Options: Fix All (recommended) / By Severity / Review Each / Report Only.

TaskUpdate `[REV] Plan Review` → completed.

### Phase 5: Apply [SKIP if --preview]

TaskCreate `[REV] Apply` (status: in_progress).

**Recovery-aware read:** If findings not in conversation context (compaction occurred), reconstruct from TaskGet on `[REV] Analyze Batch 1/2` task descriptions.

Send findings to cco-agent-apply. Group by file. Count findings, not locations. On failure: retry with alternative, then count as failed.

### Phase 5.1: Needs-Approval Review [CONDITIONAL, SKIP if --auto, AUTO-APPLY if --force-approve]

Per CCO Rules: Needs-Approval Protocol.

### Phase 5.2: Loop [--loop flag, quality mode only]

If applied > 0:
1. **Cascade check** — verify dependent files don't need updates
2. **Re-analyze** — re-run Phase 2 scoped to modified + cascade-affected files
3. **Re-apply** — re-run Phase 5 for new findings

Max 3 iterations. Summary shows per-iteration breakdown.

### Phase 6: Summary

**State cleanup:** TaskUpdate all `[REV]` tasks → completed. TaskCreate `[REV] Summary` with final accounting in description.

Per CCO Rules: Accounting, Auto Mode.

**Quality mode output:**

```
cco-review complete (quality)
=============================
| Scope          | Findings | Fixed | Failed |
|----------------|----------|-------|--------|
| security       |     3    |   3   |   0    |
| hygiene        |     5    |   4   |   1    |
| types          |     2    |   2   |   0    |
| Total          |    10    |   9   |   1    |

Applied: 9 | Failed: 1 | Needs Approval: 0 | Total: 10
```

**Architecture mode output:**

```
cco-review complete (architecture)
==================================
| Metric     | Current | Ideal | Gap  |
|------------|---------|-------|------|
| Coupling   |   55%   |  50%  | -5%  |
| Cohesion   |   68%   |  70%  | +2%  |
| Complexity |   14    |  12   | -2   |
| Coverage   |   82%   |  80%  |  OK  |

Recommendations by effort:
  Quick Win:  [PAT-05] Inconsistent error handling
  Moderate:   [ARC-03] Circular dependency
  Complex:    [TST-07] Missing integration tests

Applied: 4 | Failed: 0 | Needs Approval: 2 | Total: 6
```

--auto: `cco-review: {OK|WARN|FAIL} | Applied: N | Failed: N | Needs Approval: N | Total: N`

Status: OK (failed=0), WARN (failed>0 no CRITICAL), FAIL (CRITICAL unfixed or error).

Next: `/cco-commit` (commit fixes) | `/cco-blueprint` (track progress)
