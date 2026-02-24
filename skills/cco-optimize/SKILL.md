---
description: Fix security, hygiene, types, performance issues in code. Use when code needs quality review, security audit, or cleanup.
argument-hint: "[--auto] [--preview] [--scope=<name>]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
---

# /cco-optimize

**Incremental Code Improvement** — Quality gates + parallel analysis + background fixes.

For strategic architecture assessment, use `/cco-align`.

**Scope boundary:** Tactical, file-level fixes within current architecture. Finds repeated code blocks, unnecessary abstractions, missing types — but does NOT question architectural decisions or suggest pattern changes. For architectural assessment, use `/cco-align`.

**Do NOT:** Suggest architectural changes, question technology choices, add new abstractions, refactor working code outside the target scopes, or create new files. If an issue requires architectural change, report as `needs_approval` with reason.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | All 9 scopes, all severities, no questions, single-line summary. Exit: 0/1/2 |
| `--preview` | Analyze and report findings without applying fixes |
| `--scope=<name>` | Specific scope(s), comma-separated. Valid: security, hygiene, types, performance, ai-hygiene, robustness, privacy, doc-sync, simplify |
| `--loop` | Re-run until clean or max 3 iterations. Combines with `--auto`. |

## Context

- Git status: !`git status --short --branch`
- Args: $ARGUMENTS

## Execution Flow

Setup → Analyze → Gate → [Plan] → Apply → Summary

### Phase 1: Setup [SKIP if --auto]

**Pre-flight:** Verify git repo: `git rev-parse --git-dir 2>/dev/null` → not a repo: warn "Not a git repo — git context unavailable" and continue (git optional for optimize).

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

// Conditional: only if git dirty
AskUserQuestion([{
  question: "Uncommitted changes detected. Proceed?",
  header: "Git status",
  options: [
    { label: "Continue (Recommended)", description: "Analyze with current changes" },
    { label: "Stash first", description: "Stash changes, analyze clean tree" },
    { label: "Cancel", description: "Stop and let me handle it" }
  ],
  multiSelect: false
}])
```

### Phase 2: Analyze [BATCHED: 2+2]

Per CCO Rules: Parallel Execution, Agent Contract, Model Routing.

| Batch | Tracks | Model |
|-------|--------|-------|
| 1 | Security & Privacy (security, robustness, privacy) + Code Quality (hygiene, types, simplify) — mode: auto | haiku |
| 2 | Performance (performance) + AI Cleanup (ai-hygiene, doc-sync) — mode: auto | haiku |

Wait for ALL batches. Phase gate: do not proceed until all tracks return or fail.

Merge findings. Filter by user-selected scopes. Categorize: autoFixable vs approvalRequired. Per CCO Rules: CRITICAL Escalation — if any CRITICAL findings, run single opus validation call before proceeding.

**Gate:** If findings = 0 after analysis → skip Phase 3-4, go directly to Phase 5 with: `cco-optimize: OK | No issues found | Scopes: {scoped list}`

### Phase 3: Plan Review [findings > 0, SKIP if --auto]

Per CCO Rules: Plan Review Protocol — display findings table (ID, severity, title, file:line), then ask with markdown previews. Options: Fix All (recommended) / By Severity / Review Each / Report Only.

### Phase 4: Apply [SYNCHRONOUS, SKIP if --preview]

Send findings to cco-agent-apply (scope: fix, findings: [...], fixAll: --auto). Group by file. Count findings, not locations. On failure: retry with alternative, then count as failed.

### Phase 4.1: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per CCO Rules: Needs-Approval Protocol.

### Phase 4.2: Loop [--loop flag only]

If applied > 0:
1. **Cascade check** — for each modified file, verify dependent files don't need updates (exports, versions, config references). Report cascade items as new findings.
2. **Re-analyze** — re-run Phase 2 scoped to modified files + cascade-affected files
3. **Re-apply** — re-run Phase 4 for new findings

Max 3 iterations. Summary shows per-iteration breakdown.

### Phase 5: Summary

Per CCO Rules: Accounting, Auto Mode.

Interactive output format:

```
cco-optimize complete
=====================
| Scope          | Findings | Fixed | Failed |
|----------------|----------|-------|--------|
| security       |     3    |   3   |   0    |
| hygiene        |     5    |   4   |   1    |
| types          |     2    |   2   |   0    |
| Total          |    10    |   9   |   1    |

Failed:
  [MEDIUM] HYG-12: Unused import in services/api/handlers.py:15
    Reason: Import used by test mock path

Applied: 9 | Failed: 1 | Needs Approval: 0 | Total: 10
```

--auto: `cco-optimize: {OK|WARN} | Applied: N | Failed: N | Needs Approval: N | Total: N`

Status: OK (failed=0), WARN (failed>0 no CRITICAL), FAIL (CRITICAL unfixed or error).

Next: `/cco-commit` (commit fixes) | `/cco-align` (check architecture) | `/cco-blueprint` (track progress)

## Scopes (9 scopes, 97 checks)

Per cco-agent-analyze: Optimize Scopes — security, hygiene, types, performance, ai-hygiene, robustness, privacy, doc-sync, simplify.
