---
description: Fix security, hygiene, types, performance issues in code. Incremental code improvement with parallel analysis.
argument-hint: "[--auto] [--preview] [--scope=<name>]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
---

# /cco-optimize

**Incremental Code Improvement** — Quality gates + parallel analysis + background fixes.

**Philosophy:** "This code works. How can it work better?"

**Purpose:** Tactical, file-level fixes. For strategic architecture assessment, use `/cco-align`.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | All 9 scopes, all severities, no questions, single-line summary. Exit: 0/1/2 |
| `--preview` | Analyze and report findings without applying fixes |
| `--scope=<name>` | Specific scope(s), comma-separated. Valid: security, hygiene, types, performance, ai-hygiene, robustness, privacy, doc-sync, simplify |
| `--loop` | Re-run until clean or max 3 iterations. Combines with `--auto`. |

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`
- Args: $ARGS

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

In --auto mode: all 9 scopes, no stash, no questions.

### Phase 2: Analyze [PARALLEL: 4 calls]

Launch scope groups as parallel Task calls to cco-agent-analyze:
- Security & Privacy: security, robustness, privacy
- Code Quality: hygiene, types, simplify
- Performance: performance
- AI Cleanup: ai-hygiene, doc-sync

Merge all findings. Filter by user-selected scopes. Categorize: autoFixable vs approvalRequired.

Analysis always scans all severities. Filtering happens post-analysis via Plan Review.

Per CCO Rules: Agent Error Handling.

### Phase 3: Plan Review [findings > 0, SKIP if --auto]

Per CCO Rules: Plan Review Protocol.

### Phase 4: Apply [SYNCHRONOUS]

Send findings to cco-agent-apply. Group by file for efficiency.

Count findings, not locations. On failure: retry with alternative fix approach.

On error: If apply fails for a finding, count as failed, continue with next.

### Phase 4.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per CCO Rules: after apply, if needs_approval > 0, display items table and ask Fix All / Review Each.

### Phase 4.6: Loop [CONDITIONAL, --loop flag only]

If `--loop` and applied > 0 in this iteration:
1. Re-run Phase 2 (Analyze) scoped to files modified in previous iteration
2. Re-run Phase 4 (Apply) for new findings
3. Repeat until: applied = 0 (clean), or iteration count reaches 3

Each iteration narrows scope to only changed files. Summary shows per-iteration breakdown.

### Phase 5: Summary

Per CCO Rules: Accounting, Auto Mode, Severity Levels.

--auto mode: `cco-optimize: {OK|WARN} | applied: N | failed: N | needs_approval: N | total: N`

Interactive: table with counts, failed items list, stash reminder if applicable.

Status: OK (failed=0), WARN (failed>0 no CRITICAL), FAIL (CRITICAL unfixed or error).

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
