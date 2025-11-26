---
name: cco-commit
description: Atomic traceable change management
---

# /cco-commit

**Change management** - Analyze → group atomically → commit with traceability.

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

Good: `fix(auth): handle expired token in refresh flow`
Bad: `fix: fixed bug`

**Types:** feat, fix, refactor, perf, test, docs, style, build, ci, chore

## Flow

1. **Analyze** - `git status`, `git diff`, detect change types
2. **Group** - Apply atomic grouping rules, detect dependencies
3. **Plan** - Show commit plan with files per commit
4. **Confirm** - AskUserQuestion: Accept / Modify / Custom
5. **Execute** - Stage and commit each group in order
6. **Verify** - `git log` count = planned count

## Flags

- `--dry-run` - Show plan without committing
- `--single` - Force all changes into one commit

## Usage

```bash
/cco-commit              # Analyze and suggest atomic commits
/cco-commit --dry-run    # Preview only
```
