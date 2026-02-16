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

- Git status: !`git status --short 2>/dev/null || echo ""`
- Args: $ARGUMENTS

## Execution Flow

Setup → Analyze → Gate → [Plan] → Apply → Summary

### Phase 1: Setup [SKIP if --auto]

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

### Phase 2: Analyze [PARALLEL: 4 calls]

Launch scope groups as parallel Task calls to cco-agent-analyze (mode: auto):
- Security & Privacy: security, robustness, privacy
- Code Quality: hygiene, types, simplify
- Performance: performance
- AI Cleanup: ai-hygiene, doc-sync

Merge findings. Filter by user-selected scopes. Categorize: autoFixable vs approvalRequired. Per CCO Rules: Agent Error Handling — validate agent JSON output, retry once on malformed response, on second failure continue with remaining groups, score failed dimensions as N/A.

**Gate:** If findings = 0 after analysis → skip Phase 3-4, go directly to Phase 5 with: `cco-optimize: OK | No issues found | Scopes: {scoped list}`

### Phase 3: Plan Review [findings > 0, SKIP if --auto]

Per CCO Rules: Plan Review Protocol — display findings table (ID, severity, title, file:line), then ask: Fix All / By Severity / Review Each / Report Only. If "By Severity": severity multiselect (CRITICAL / HIGH / MEDIUM / LOW).

### Phase 4: Apply [SYNCHRONOUS]

Send findings to cco-agent-apply (scope: fix, findings: [...], fixAll: --auto). Group by file. Count findings, not locations. On failure: retry with alternative, then count as failed.

### Phase 4.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

**Phase gate:** After Phase 4 completes, ALWAYS evaluate needs_approval count before proceeding. Do not skip to Summary.

Per CCO Rules: if needs_approval > 0, display items table (ID, severity, issue, location, reason) and ask Fix All / Review Each.

### Phase 4.6: Loop [--loop flag only]

If applied > 0: re-run Phase 2 scoped to modified files → re-run Phase 4. Max 3 iterations. Summary shows per-iteration breakdown.

### Phase 5: Summary

Per CCO Rules: Accounting — applied + failed + needs_approval = total. No "declined" category. Auto Mode — no questions, no deferrals, fix everything except large architectural changes.

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

--auto: `cco-optimize: {OK|WARN} | applied: N | failed: N | needs_approval: N | total: N`

Status: OK (failed=0), WARN (failed>0 no CRITICAL), FAIL (CRITICAL unfixed or error).

Next: `/cco-commit` (commit fixes) | `/cco-align` (check architecture) | `/cco-blueprint` (track progress)

## Scopes (9 scopes, 97 checks)

| Scope | ID Range | Checks |
|-------|----------|--------|
| security | SEC-01-12 | Secrets, injection, deserialization, eval, debug, crypto |
| hygiene | HYG-01-20 | Unused code, dead code, duplicates, stale TODOs, comment quality |
| types | TYP-01-10 | Type errors, missing annotations, type:ignore, Any in API |
| performance | PRF-01-10 | N+1, blocking async, missing cache/pagination/pool |
| ai-hygiene | AIH-01-08 | Hallucinated APIs, orphan abstractions, over-documented, stale mocks |
| robustness | ROB-01-10 | Missing timeout/retry, unbounded collections, resource cleanup |
| privacy | PRV-01-08 | PII exposure, missing masking/consent/retention |
| doc-sync | DOC-01-08 | README drift, API mismatch, broken links, changelog gaps |
| simplify | SIM-01-11 | Deep nesting, duplicates, unnecessary abstractions, test bloat |
