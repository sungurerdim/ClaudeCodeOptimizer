---
name: cco-commit
description: Atomic commits with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-commit

**Smart Commits** - Quality gates → analyze → group atomically → commit.

## Context Requirement

```
test -f ./.claude/rules/cco/context.md && echo "OK" || echo "Run /cco-config first"
```

If not found: Stop immediately with message to run /cco-config.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Parallel git info (single message with 4 Bash calls)                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Bash(git status --short)        ──┐                                         │
│ Bash(git diff --cached --stat)  ──┼──→ All run simultaneously               │
│ Bash(git branch --show-current) ──┤                                         │
│ Bash(git log --oneline -5)      ──┘                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Quality gates (sequential - stop on failure)                        │
│         Secrets → Large files → Format → Lint → Types → Tests               │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Analyze + Group changes atomically                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Show plan, get approval                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 5: Execute commits                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Step 1 MUST be a single message with multiple Bash tool calls.

## Context Application

| Field | Effect |
|-------|--------|
| Tools | Use format/lint/test from context Operational section |
| Maturity | Legacy → smaller commits; Greenfield → batch related |
| Type | Library → careful with public API; API → note contract impacts |

## Quality Gates

Run sequentially, stop on failure:

| Gate | Detection | Action |
|------|-----------|--------|
| Secrets | `sk-`, `ghp_`, `password=`, private keys | BLOCK |
| Large Files | >1MB warn, >10MB block | ASK |
| Format | Auto-fix style | MODIFY |
| Lint | Static analysis | STOP on unfixable |
| Types | Type consistency | STOP on failure |
| Tests | Behavior verification | STOP on failure |

## Atomic Grouping

**Keep together:** Implementation + tests, renames, single logical change
**Split apart:** Different features, unrelated files, config vs code, docs vs impl

## Commit Order

1. Types/interfaces → 2. Core impl → 3. Dependent code → 4. Tests → 5. Docs

## Message Quality

| ❌ Reject | ✅ Accept |
|-----------|-----------|
| "fix bug" | "fix(auth): prevent session timeout on refresh" |
| "update code" | "refactor(parser): extract validation module" |
| "changes" | "feat(export): add CSV export for reports" |

## Type Classification

| Type | Definition |
|------|------------|
| feat | New capability |
| fix | Bug correction |
| refactor | Structure change, same behavior |
| perf | Performance improvement |
| test | Test changes only |
| docs | Documentation only |
| build | Build/deps |
| ci | CI config |
| chore | Maintenance |

## Breaking Change Detection

| Signal | Action |
|--------|--------|
| API removal, signature change, renamed export | WARN + ask for BREAKING CHANGE footer |

## Output

```
┌─ QUALITY GATES ──────────────────────────────────────────────┐
│ Secrets: {s} │ Format: {s} │ Lint: {s} │ Tests: {s}          │
└──────────────────────────────────────────────────────────────┘

┌─ COMMIT PLAN ────────────────────────────────────────────────┐
│ # │ Type     │ Scope   │ Description          │ Files        │
├───┼──────────┼─────────┼──────────────────────┼──────────────┤
│ 1 │ {type}   │ {scope} │ {description}        │ {n}          │
└───┴──────────┴─────────┴──────────────────────┴──────────────┘

┌─ VERSION IMPACT ─────────────────────────────────────────────┐
│ Highest: {MAJOR|MINOR|PATCH} | Suggested: v{x} → v{y}        │
└──────────────────────────────────────────────────────────────┘
```

## User Decisions

| Question | Options |
|----------|---------|
| Include unstaged? | Yes; No |
| Commit plan action? | Accept; Modify; Merge; Split; Edit message; Cancel |
| Large file ({file})? | Yes; No |
| Add BREAKING CHANGE? | Yes; No |

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show plan only |
| `--single` | Force one commit |
| `--quick` | Single-message, smart defaults |
| `--skip-checks` | Skip quality gates |
| `--amend` | Amend last (with safety checks) |

## Quick Mode

Single message: `git status` → `git add -A` → `git commit -m "..."` → summary

## Rules

1. **Parallel git info** - Status/diff/branch/log run simultaneously
2. **Sequential gates** - Quality checks stop on failure
3. **Atomic commits** - Each commit independently revertible
4. **No vague messages** - Reject generic descriptions
5. **Git safety** - No force push, verify before amend
