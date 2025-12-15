---
name: cco-commit
description: Atomic commits with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*), TodoWrite, AskUserQuestion
---

# /cco-commit

**Smart Commits** - Quality gates → analyze → group atomically → commit.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`
- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Stash list: !`git stash list --oneline | head -3`
- Line counts: !`git diff --shortstat`
- Staged lines: !`git diff --cached --shortstat`

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Tools, Conventions) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Pre-commit Awareness

| Condition | Detection | Action |
|-----------|-----------|--------|
| Stash exists | Stash list not empty | Ask via AskUserQuestion |
| Conflicts | `UU`/`AA`/`DD` in status | BLOCK - must resolve first |
| Large changes | 500+ lines | WARN - consider splitting |

### Stash Handling

If stash exists → **AskUserQuestion**:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| You have stashed changes. What to do? | Keep stashed; Apply and include; Pop and include | false |

- **Keep stashed**: Continue without stash (stash remains)
- **Apply and include**: Apply to working tree, include in commit (stash kept)
- **Pop and include**: Pop to working tree, include in commit (stash removed)

### Conflict Handling

If conflicts detected: `Cannot commit: {n} conflict(s). Resolve first.` **Stop immediately.**

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Collect git info", status: "in_progress", activeForm: "Collecting git info" },
  { content: "Run quality gates", status: "pending", activeForm: "Running quality gates" },
  { content: "Analyze changes", status: "pending", activeForm: "Analyzing changes" },
  { content: "Get plan approval", status: "pending", activeForm: "Getting plan approval" },
  { content: "Execute commits", status: "pending", activeForm: "Executing commits" }
])
```

## Execution Flow

| Step | Action |
|------|--------|
| 1. Git info | Single message: `status`, `diff --cached`, `branch`, `log` (parallel) |
| 2. Quality gates | Sequential: Secrets → Large files → Format → Lint → Types → Tests |
| 3. Analyze | Group changes atomically |
| 4. Approval | Show plan, get user approval |
| 5. Commit | Execute commits |

## Context Application

| Field | Effect |
|-------|--------|
| Tools | format/lint/test from context Operational |
| Maturity | Legacy → smaller commits; Greenfield → batch |
| Type | Library → careful with API; API → note contracts |

## Quality Gates [CRITICAL]

| Gate | Command | Action |
|------|---------|--------|
| Secrets | `grep -rn "sk-\|ghp_\|password="` | BLOCK if found |
| Large Files | `find . -size +1M` | WARN >1MB, BLOCK >10MB |
| Format | `{format_cmd}` from context | Auto-fix, stage |
| Lint | `{lint_cmd}` from context | STOP on unfixable |
| Types | `{type_cmd}` from context | STOP on failure |
| Tests | `{test_cmd}` from context | STOP on failure |

**Sequential, stop on failure.** Commands from context.md Operational section.

## Atomic Grouping

**Keep together:** Implementation + tests, renames, single logical change
**Split apart:** Different features, unrelated files, config vs code, docs vs impl
**Order:** Types/interfaces → Core impl → Dependent code → Tests → Docs

## Message Format

```
{type}({scope}): {title}

{description}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

| Rule | Requirement |
|------|-------------|
| Title | ≤50 chars (hard: 72), action verb, no period |
| Description | What changed and why (1-3 lines) |
| Scope | From affected module/feature |
| Trailer | Always include Generated + Co-Authored-By |
| Types | feat, fix, refactor, perf, test, docs, build, ci, chore |

**Reject:** "fix bug", "update code", "changes" → Use specific descriptions

**Breaking:** API removal/signature change → WARN + ask for BREAKING CHANGE footer

## User Decisions

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Include unstaged? | Yes (Recommended); No | false |
| Commit plan action? | Accept (Recommended); Modify; Edit message; Cancel | false |
| Large file? | Include; Exclude | false |
| Add BREAKING CHANGE? | Yes; No | false |

**Modify options:** Merge commits; Split commit; Reorder; Edit files

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show plan only |
| `--single` | Force one commit |
| `--quick` | Single-message, smart defaults |
| `--skip-checks` | Skip quality gates |
| `--amend` | Amend last (with safety) |

## Default Behavior (No Flags)

Interactive mode with full control:
1. Run all quality gates (format, lint, types, tests)
2. Analyze changes and suggest atomic grouping
3. Ask about unstaged changes
4. Show commit plan for approval
5. Execute approved commits

**User controls every decision via AskUserQuestion.**

## Quick Mode (`--quick`)

When `--quick` flag is used:
- No questions - use smart defaults
- Stage all changes
- Single commit with auto-generated message
- Complete in single message

## Rules

Parallel git info │ Sequential gates │ Atomic commits │ No vague messages │ Git safety
