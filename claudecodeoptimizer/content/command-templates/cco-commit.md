---
name: cco-commit
description: Atomic commits with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-commit

**Smart Commits** - Quality gates → analyze → group atomically → commit.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`
- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Stash list: !`git stash list --oneline 2>/dev/null | head -3`
- Line counts: !`git diff --shortstat 2>/dev/null`
- Staged lines: !`git diff --cached --shortstat 2>/dev/null`

**Static context (Tools, Conventions) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Pre-collected Git Info

**Git status, branch, recent commits, stash list, and line counts are already available above via dynamic context.**

Use this pre-collected info instead of running git commands again in Step 1.

## Pre-commit Awareness

**Check dynamic context above for these conditions before proceeding:**

| Condition | Detection | Action |
|-----------|-----------|--------|
| **Stash exists** | Stash list is not empty | Ask user via AskUserQuestion |
| **Conflicts** | `UU` or `AA` in git status | BLOCK - must resolve first |
| **Large changes** | Line counts show 500+ lines | WARN - consider splitting |

### Stash Handling

If stash list shows entries, present **AskUserQuestion**:

```
Question: "You have stashed changes. What would you like to do?"
Header: "Stash"
Options:
  - label: "Keep stashed"
    description: "Continue without stashed changes (stash remains for later)"
  - label: "Apply and include"
    description: "Apply stash to working tree, include in this commit (stash kept)"
  - label: "Pop and include"
    description: "Pop stash to working tree, include in this commit (stash removed)"
MultiSelect: false
```

**Show stash contents summary before asking:**
```
Stashed changes found:
  stash@{0}: WIP on main: abc123 feat: add login
    → 3 files changed (src/auth.ts, src/login.tsx, tests/auth.test.ts)
  stash@{1}: WIP on main: def456 refactor: cleanup
    → 1 file changed (src/utils.ts)
```

### Conflict Handling

If conflicts detected in git status (`UU`, `AA`, `DD` markers):
```
Cannot commit: {n} unresolved conflict(s) detected.

Conflicting files:
  • {file1}
  • {file2}

Resolve conflicts first, then run /cco-commit again.
```
**Stop execution immediately.**

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each step.

```
TodoWrite([
  { content: "Collect git info", status: "in_progress", activeForm: "Collecting git info" },
  { content: "Run quality gates", status: "pending", activeForm: "Running quality gates" },
  { content: "Analyze changes", status: "pending", activeForm: "Analyzing changes" },
  { content: "Get plan approval", status: "pending", activeForm: "Getting plan approval" },
  { content: "Execute commits", status: "pending", activeForm: "Executing commits" }
])
```

**Update status:** Mark `completed` immediately after each step finishes, mark next `in_progress`.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Collect git info (single message with 4 Bash calls)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Bash(git status --short)        ──┐                                         │
│ Bash(git diff --cached --stat)  ──┼──→ All run simultaneously               │
│ Bash(git branch --show-current) ──┤                                         │
│ Bash(git log --oneline -5)      ──┘                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Quality gates (sequential - stop on failure)                                 │
│ Secrets → Large files → Format → Lint → Types → Tests                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Analyze + Group changes atomically                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Show plan, get approval                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Execute commits                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Git info MUST be collected in a single message with multiple Bash tool calls.

## Context Application

| Field | Effect |
|-------|--------|
| Tools | Use format/lint/test from context Operational section |
| Maturity | Legacy → smaller commits; Greenfield → batch related |
| Type | Library → careful with public API; API → note contract impacts |

## Quality Gates [CRITICAL]

**Read tools from context.md Operational section:**
```
Tools: {format_cmd} (format), {lint_cmd} (lint), {test_cmd} (test)
```

**Run sequentially, stop on failure:**

| Gate | Command Source | Action |
|------|----------------|--------|
| Secrets | `grep -rn "sk-\|ghp_\|password=" --include="*.py"` | BLOCK if found |
| Large Files | `find . -size +1M -type f` | WARN >1MB, BLOCK >10MB |
| Format | `{format_cmd}` from context | Auto-fix, stage changes |
| Lint | `{lint_cmd}` from context | STOP on unfixable |
| Types | `{type_cmd}` from context (if configured) | STOP on failure |
| Tests | `{test_cmd}` from context | STOP on failure |

**Execution order:**
```
Step 2 runs:
  1. Secrets check (grep for patterns)
  2. {format_cmd} from context        # Format (auto-fix)
  3. {lint_cmd} from context          # Lint + Types
  4. {test_cmd} from context          # Tests
```

**If any gate fails:** Stop immediately, show error, do NOT proceed to Step 3.

## Atomic Grouping

**Keep together:** Implementation + tests, renames, single logical change
**Split apart:** Different features, unrelated files, config vs code, docs vs impl

## Commit Order

1. Types/interfaces → 2. Core impl → 3. Dependent code → 4. Tests → 5. Docs

## Message Quality

| Rule | Requirement |
|------|-------------|
| Length | Title ≤50 chars (hard limit: 72) |
| Format | `{type}({scope}): {description}` |
| Scope | From affected module/feature |
| Description | Action verb, no period |

| ❌ Reject | ✅ Accept |
|-----------|-----------|
| "fix bug" | "fix({scope}): {specific_fix}" |
| "update code" | "refactor({scope}): {what_changed}" |
| "changes" | "feat({scope}): {new_capability}" |
| "{type}({scope}): {very_long_description_exceeding_50_chars}" | "{type}({scope}): {short}" |

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

┌─ CHANGE SUMMARY ─────────────────────────────────────────────┐
│ Files: {n} changed │ Lines: +{added} / -{removed}            │
└──────────────────────────────────────────────────────────────┘

┌─ COMMIT PLAN ────────────────────────────────────────────────┐
│ # │ Type     │ Scope   │ Description          │ Files │ +/-  │
├───┼──────────┼─────────┼──────────────────────┼───────┼──────┤
│ 1 │ {type}   │ {scope} │ {description}        │ {n}   │ +{a} │
└───┴──────────┴─────────┴──────────────────────┴───────┴──────┘

┌─ VERSION IMPACT ─────────────────────────────────────────────┐
│ Highest: {MAJOR|MINOR|PATCH} | Suggested: v{x} → v{y}        │
└──────────────────────────────────────────────────────────────┘
```

**Line counts per commit** help assess change magnitude and review effort.

## User Decisions

### Primary Decisions

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Include unstaged? | Yes (Recommended); No | false |
| Commit plan action? | Accept (Recommended); Modify; Edit message; Cancel | false |
| Large file ({file})? | Include; Exclude | false |
| Add BREAKING CHANGE? | Yes; No | false |

### Follow-up: Modify Options

*Only shown if "Modify" selected:*

| Question | Options | MultiSelect |
|----------|---------|-------------|
| How to modify? | Merge commits; Split commit; Reorder; Edit files | false |

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
