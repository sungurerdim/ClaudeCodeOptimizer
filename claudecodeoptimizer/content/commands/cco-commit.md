---
name: cco-commit
description: Atomic traceable change management
---

# /cco-commit

**Change management** - Quality gates → analyze → group atomically → commit with traceability.

## Pre-Commit Quality Gates

Before committing, automatically run quality checks:

### Tool Resolution

**Priority order:**

1. **CCO Context** (preferred) - Read from `CLAUDE.md`:
   ```markdown
   <!-- CCO_CONTEXT_START -->
   ## Operational
   Tools: ruff (format+lint), mypy (types), pytest --cov (test)
   ```
   Parse the Tools line to extract format, lint, and test commands.

2. **Fallback: Auto-detect** - If no CCO context, run `cco-agent-detect` with `scope: tools`

   The detect agent checks: pyproject.toml, package.json, Cargo.toml, go.mod, Makefile, .pre-commit-config.yaml

### Check Order

1. **Format** - Auto-fix style issues (modifies files)
2. **Lint** - Static analysis (may auto-fix)
3. **Test** - Verify behavior (read-only)

### Behavior

- Run detected tools in order
- If format modifies files, include in commit
- If lint fails with unfixable errors, stop and report
- If tests fail, stop and report - never commit broken code
- Show summary: `Format: OK | Lint: OK | Tests: 47 passed`

### Skip Option

Use `--skip-checks` to bypass (use with caution):
```bash
/cco-commit --skip-checks  # Skip quality gates
```

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

1. **Resolve Tools** - Read CCO context from CLAUDE.md, fallback to auto-detect
2. **Quality Gates** - Run format → lint → test (stop on failure)
3. **Analyze** - `git status`, `git diff`, detect change types
4. **Group** - Apply atomic grouping rules, detect dependencies
5. **Plan** - Show commit plan with files per commit
6. **Confirm** - AskUserQuestion: Accept / Modify / Custom
7. **Execute** - Stage and commit each group in order
8. **Verify** - `git log` count = planned count

## Flags

- `--dry-run` - Show plan without committing
- `--single` - Force all changes into one commit
- `--skip-checks` - Skip format/lint/test gates (use with caution)

## Usage

```bash
/cco-commit                 # Full flow: checks → analyze → commit
/cco-commit --dry-run       # Preview only (still runs checks)
/cco-commit --skip-checks   # Skip quality gates (emergency use)
```
