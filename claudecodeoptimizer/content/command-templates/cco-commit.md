---
name: cco-commit
description: Atomic commits with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*), TodoWrite, AskUserQuestion
---

# /cco-commit

**Smart Commits** - Quality gates + atomic grouping + conventional messages.

## Dynamic Context (Pre-collected)

- Context: !`test -f ./.claude/rules/cco/context.md && echo "OK" || echo "MISSING"`
- Status: !`git status --short`
- Staged: !`git diff --cached --name-only`
- Branch: !`git branch --show-current`
- Recent: !`git log --oneline -5`
- Stash: !`git stash list --oneline 2>/dev/null | head -2`
- Unstaged stats: !`git diff --shortstat 2>/dev/null`
- Staged stats: !`git diff --cached --shortstat 2>/dev/null`

## Context Requirement

If Context shows "MISSING": Stop with "Run /cco-config first".

## Pre-commit Checks (from dynamic context)

| Condition | Detection | Action |
|-----------|-----------|--------|
| Conflicts | `UU`, `AA`, `DD` in Status | BLOCK - resolve first |
| Stash exists | Stash not empty | Ask: keep / apply / pop |
| Large changes | 500+ lines in stats | WARN - consider splitting |

## Execution Flow [Speed Optimized]

**Use pre-collected dynamic context. DO NOT re-run git commands.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. CHECK: Context OK? Conflicts? Stash? (from dynamic context above)        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. GATES: Single Bash call with combined commands                           │
│    {lint_cmd} && {test_cmd}                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. ANALYZE: Group changes atomically, generate commit plan                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. APPROVE: Show plan, get user approval                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. COMMIT: git add && git commit (single Bash call per commit)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quality Gates

**Single combined command** (from context.md Tools):
```bash
{format_cmd} && {lint_cmd} && {test_cmd}
```

Format auto-fixes code style, lint checks errors, tests verify behavior.

**Secrets check:** Only if changed files contain `.env`, `credentials`, `secret`, `password`.

## Atomic Grouping

**Keep together:**
- Implementation + its tests
- Renames across files
- Single logical change
- Related config changes

**Split apart:**
- Different features
- Unrelated files
- Config vs code
- Docs vs implementation

## Commit Order

When multiple commits needed:
1. Types/interfaces first
2. Core implementation
3. Dependent code
4. Tests
5. Documentation

## Message Format

```
{type}({scope}): {title}

{description}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

| Rule | Requirement |
|------|-------------|
| Title | ≤50 chars (hard limit: 72), action verb, no period |
| Description | What changed and why (1-3 lines) |
| Scope | From affected module/feature |
| Trailer | Always include Generated + Co-Authored-By |

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

**Message Quality:**

| Reject | Accept |
|--------|--------|
| "fix bug" | "fix({scope}): {specific_fix}" |
| "update code" | "refactor({scope}): {what_changed}" |
| "changes" | "feat({scope}): {new_capability}" |

## Breaking Change Detection

| Signal | Action |
|--------|--------|
| API removal | Add `BREAKING CHANGE:` footer |
| Signature change | Add `BREAKING CHANGE:` footer |
| Renamed export | Add `BREAKING CHANGE:` footer |

## Output

```
┌─ QUALITY GATES ──────────────────────────────────────────────┐
│ Lint: ✓ │ Tests: ✓ ({n} passed)                              │
└──────────────────────────────────────────────────────────────┘

┌─ COMMIT PLAN ────────────────────────────────────────────────┐
│ # │ Type     │ Scope      │ Description          │ Files │+/-│
├───┼──────────┼────────────┼──────────────────────┼───────┼───┤
│ 1 │ {type}   │ {scope}    │ {description}        │ {n}   │{±}│
│ 2 │ {type}   │ {scope}    │ {description}        │ {n}   │{±}│
└───┴──────────┴────────────┴──────────────────────┴───────┴───┘

┌─ VERSION IMPACT ─────────────────────────────────────────────┐
│ Highest: {MAJOR|MINOR|PATCH} │ Suggested: v{x} → v{y}        │
└──────────────────────────────────────────────────────────────┘
```

## User Decisions

| Situation | Question | Options |
|-----------|----------|---------|
| Unstaged changes exist | Include unstaged? | Yes (Recommended); No |
| Plan ready | Commit? | Accept (Recommended); Edit message; Cancel |
| Breaking change detected | Add BREAKING CHANGE footer? | Yes; No |

## Rules

1. **Use dynamic context** - Never re-run git status/diff/branch/log
2. **Single Bash for gates** - Combine lint + test in one call
3. **Atomic commits** - Each commit independently revertible
4. **Conventional messages** - Reject vague descriptions
5. **Git safety** - No force push, verify before amend
