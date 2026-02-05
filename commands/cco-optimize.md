---
description: Incremental code improvement - fix security, hygiene, types, lint, performance issues
argument-hint: "[--auto] [--preview] [--scope=<name>]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
model: opus
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

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`
- Args: $ARGS

**DO NOT re-run these commands. Use the pre-collected values above.**

## Update Check

1. Read `cco_version` and `last_update_check` from context (cco-rules.md frontmatter, already loaded)
2. If last check >24 hours ago → `/cco-update --check`
3. New version available → display: `CCO vX.Y.Z available. Run /cco-update to upgrade.`
4. In --auto mode: skip silently

## Core Principle [CRITICAL]

**Fix everything that can be fixed.** Auto-fix safe items, ask approval for risky ones.

## Fixable Definition

A finding is fixable if ALL: single file change, no API contract change, no new dependencies, deterministic fix.

| Category | Auto-fix? |
|----------|-----------|
| Unused imports/vars, formatting | Yes — zero risk |
| Type annotations | Yes — tooling validates |
| Missing validation, security fixes | Approval — logic change |
| Refactoring | Approval — subjective |

In `--auto` and full-fix modes, the fixable flag is ignored — ALL findings sent to apply agent. Truly unfixable items reported as `failed`.

## Execution Flow

Setup → Analyze → Gate → [Plan] → Apply → Summary

### Step 1: Setup [SKIP IF --auto]

**Q1 (multiselect):** "Which areas to check?"
- Security & Privacy (Recommended): SEC + ROB + PRV
- Code Quality (Recommended): HYG + TYP + SIM
- Performance: PRF
- AI Cleanup: AIH + DOC

**Q2 (conditional, only if git dirty):** "Uncommitted changes detected. Proceed?"
- Continue (Recommended) / Stash first / Cancel

In --auto mode: all 9 scopes, no stash, no questions.

### Phase 2: Analyze [PARALLEL SCOPES]

Launch scope groups as parallel Task calls to cco-agent-analyze:
- Security & Privacy: security, robustness, privacy
- Code Quality: hygiene, types, simplify
- Performance: performance
- AI Cleanup: ai-hygiene, doc-sync

Merge all findings. Filter by user-selected scopes. Categorize: autoFixable vs approvalRequired.

Analysis always scans ALL severities. Filtering happens post-analysis via Plan Review.

### Phase 3: Plan Review [MANDATORY when findings > 0, SKIP if --auto]

Per Core Rules: Plan Review. Display plan table BEFORE asking.

**Post-analysis Q2:**
- Action: Fix All (Recommended) / By Severity / Review Each / Report Only
- Severity filter (multiselect): CRITICAL / HIGH / MEDIUM / LOW

Severity question only applies when Action = "By Severity".

### Phase 4: Apply [SYNCHRONOUS]

Send findings to cco-agent-apply. Group by file for efficiency.

Per Core Rules: No Deferrals, Accounting.

Count FINDINGS, not locations. On failure: retry with alternative fix approach.

### Phase 4.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per Core Rules: Needs-Approval Flow.

### Validation [x]

- [x] All findings accounted for (per accounting rule in Core Rules)
- [x] No CRITICAL findings left unfixed

### Step 5: Summary

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

## Recovery

| Situation | Recovery |
|-----------|----------|
| Fix broke something | `git checkout -- {file}` |
| Multiple files | `git checkout .` |
| Want to review | `git diff` |
| Stashed at start | `git stash pop` |
