---
name: cco-commit
description: Atomic traceable change management
---

# /cco-commit

**Change management** - Quality gates → analyze → group atomically → commit.

**Standards:** Command Flow | Pre-Operation Safety | Approval Flow | Output Formatting

## Context Application

| Field | Effect |
|-------|--------|
| Tools | Use format, lint, test commands from Operational section |
| Maturity | Legacy → conservative grouping, smaller commits; Greenfield → batch related changes |
| Scale | 10K+ → smaller atomic commits, detailed messages; <100 → can batch more |
| Type | Library → extra care with public API changes; API → note contract impacts |
| Priority | Speed → minimal commit message; Quality → detailed why + impact |

## Pre-Commit Quality Gates

Before committing, automatically run quality checks.

### Stale Lock Recovery

Before any git operation: if `.git/index.lock` exists but no git process running → remove it.

### Tool Resolution

**Priority order:**

1. **CCO Context** (preferred) - Read from `./CLAUDE.md`:
   - Parse `Tools:` line from Operational section
   - Extract: `{format_command}`, `{lint_command}`, `{test_command}`

2. **Fallback: Auto-detect** - If no CCO context, run `cco-agent-analyze` with `scope: detect`

### Check Order

1. **Format** - Auto-fix style issues (modifies files)
2. **Lint** - Static analysis (may auto-fix)
3. **Test** - Verify behavior (read-only)

### Behavior

- Run detected tools in order
- If format modifies files, include in commit
- If lint fails with unfixable errors, stop and report
- If tests fail, stop and report - never commit broken code
- Show summary: `Format: {status} | Lint: {status} | Tests: {count} passed`

### Skip Option

Use `--skip-checks` to bypass (use with caution).

## Atomic Grouping Rules

**Keep together (one commit):**
- Implementation + its tests
- Implementation + its types/interfaces
- Rename across multiple files
- Single logical change across related files

**Split apart (separate commits):**
- Different features/fixes
- Unrelated files
- Config vs code changes
- Docs vs implementation

## Commit Order

If changes have dependencies, commit in order:
1. Types/interfaces first
2. Core implementations
3. Dependent code
4. Tests
5. Docs/config

## Quality Thresholds

- Max 10 files per commit (split if more)
- Title: max 50 chars, imperative verb, no period
- Body: wrap at 72 chars, explain WHY not just WHAT
- Scope: derive from directory/module name

## Title Format

```
<type>(<scope>): <imperative verb> <specific change>
```

**Types:** feat, fix, refactor, perf, test, docs, style, build, ci, chore

## Output

**Standards:** Output Formatting

Tables:
1. **Quality Gates** - Check | Status | Details (Format, Lint, Test)
2. **Changes Detected** - File | + | - (with total in header)
3. **Commit Plan** - # | Type | Scope | Description | Files

## Flow

Per Command Flow standard, then:
1. **Quality Gates** - Run format → lint → test (stop on failure)
2. **Analyze** - `git status`, `git diff`, detect change types
3. **Group** - Apply atomic grouping rules
4. **Plan** - Show commit plan with files per commit
5. **Confirm** - AskUserQuestion: Accept / Modify / Custom
6. **Execute** - Stage and commit each group in order
7. **Verify** - `git log` count = planned count

## Flags

- `--dry-run` - Show plan without committing
- `--single` - Force all changes into one commit
- `--skip-checks` - Skip format/lint/test gates (use with caution)

## Usage

```bash
/cco-commit                 # Full flow: checks → analyze → commit
/cco-commit --dry-run       # Preview only (still runs checks)
/cco-commit --single        # Force all changes into one commit
/cco-commit --skip-checks   # Skip quality gates (emergency use)
```
