---
name: cco-commit
description: Atomic traceable change management
---

# /cco-commit

**Change management** - Quality gates → analyze → group atomically → commit with traceability.

## Agent Delegation

| Phase | Agent | Purpose |
|-------|-------|---------|
| Detect | `cco-agent-detect` | Find project tools (format, lint, test) |

### MANDATORY Agent Rules

1. **ALWAYS use `cco-agent-detect`** for tool detection
2. Do NOT hardcode tool names - detect from config files
3. Git commands (add, commit) can be direct Bash

### Error Recovery

On tool detection errors:
1. Delegate to `cco-agent-detect` for fresh scan
2. Report detected tools to user

## Pre-Commit Quality Gates

Before committing, automatically run quality checks:

### Tool Detection

Detect project tools from config files (no hardcoded tool names):
- `pyproject.toml` → extract [tool.*] sections
- `package.json` → extract scripts and devDependencies
- `Cargo.toml` → Rust toolchain
- `go.mod` → Go toolchain
- `Makefile` → check for lint/test/format targets
- `.pre-commit-config.yaml` → use pre-commit if configured

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

1. **Detect Tools** - Find formatters, linters, test runners from config
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
