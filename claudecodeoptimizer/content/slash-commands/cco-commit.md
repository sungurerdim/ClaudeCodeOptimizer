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

1. **Secrets Scan** - Detect accidentally staged secrets (blocks commit)
2. **Large Files** - Warn on files >1MB or binaries (requires confirmation)
3. **Format** - Auto-fix style issues (modifies files)
4. **Lint** - Static analysis (may auto-fix)
5. **Test** - Verify behavior (read-only)

### Secrets Detection

Scan staged files for potential secrets before commit:

| Pattern | Examples |
|---------|----------|
| API keys | `sk-`, `api_key=`, `apiKey:` |
| Tokens | `ghp_`, `gho_`, `Bearer ` |
| Passwords | `password=`, `passwd:`, `secret=` |
| Private keys | `-----BEGIN.*PRIVATE KEY-----` |
| Connection strings | `mongodb://`, `postgres://`, `mysql://` |

**On detection:** Block commit, show file:line, suggest `.gitignore` or env var.

### Large File Warning

| Condition | Action |
|-----------|--------|
| File > 1MB | Warn, ask confirmation |
| Binary file (non-text) | Warn, suggest Git LFS |
| File > 10MB | Block, require `--force-large` |

### Behavior

- Run checks in order, stop on blocking failure
- If format modifies files, include in commit
- If lint fails with unfixable errors, stop and report
- If tests fail, stop and report - never commit broken code
- Show summary: `Secrets: {status} | Format: {status} | Lint: {status} | Tests: {count} passed`

### Skip Option

Use `--skip-checks` to bypass (use with caution).

## Staged vs Unstaged Handling

| State | Behavior |
|-------|----------|
| Nothing staged, has unstaged | Analyze all unstaged, propose grouping |
| Has staged, has unstaged | Ask: "Include unstaged?" → Yes: analyze all, No: commit staged only |
| Has staged, no unstaged | Commit staged as-is (user already decided) |
| Nothing staged, nothing unstaged | Show "No changes to commit" and exit |

**Respect user intent:** If user explicitly staged files, don't second-guess unless asked.

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
1. **Quality Gates** - Check | Status | Details (Secrets, Large Files, Format, Lint, Test)
2. **Changes Detected** - File | + | - (with total in header)
3. **Commit Plan** - # | Type | Scope | Description | Files
4. **Breaking Changes** - File | Change | Impact (only if detected)

## Breaking Change Detection

Detect breaking changes and prompt for proper documentation:

| Signal | Detection |
|--------|-----------|
| Public API removal | Function/method deleted from exports |
| Signature change | Parameters added/removed/reordered |
| Return type change | Different return type in typed code |
| Renamed export | Public symbol renamed |
| Config schema change | Required field added, field removed |

**On detection:**
1. Warn user: "Breaking change detected in {file}"
2. Ask: "Add BREAKING CHANGE footer?" → Yes/No
3. If Yes, append to commit body:
   ```
   BREAKING CHANGE: {description of what breaks and migration path}
   ```

## Flow

Per Command Flow standard, then:
1. **Quality Gates** - Run secrets → large files → format → lint → test (stop on failure)
2. **Analyze** - `git status`, `git diff`, detect change types + breaking changes
3. **Group** - Apply atomic grouping rules
4. **Plan** - Show commit plan with files per commit
5. **Confirm** - AskUserQuestion (see options below)
6. **Execute** - Stage and commit each group in order
7. **Verify** - `git log` count = planned count

### Confirm Options

| Option | Behavior |
|--------|----------|
| Accept | Execute plan as shown |
| Modify | Show file list, let user reassign files to different commits |
| Merge | Combine selected commits into one |
| Split | Break a commit into smaller pieces |
| Edit message | Change commit type/scope/description |
| Cancel | Abort without committing |

**Modify flow:**
```
Current plan: 3 commits
[1] feat(auth): add login endpoint — auth.ts, auth.test.ts
[2] fix(ui): correct button alignment — button.css
[3] docs: update README — README.md

Move files between commits or type 'done':
> move auth.test.ts to 3
> done
```

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show plan without committing |
| `--single` | Force all changes into one commit |
| `--skip-checks` | Skip quality gates (emergency use) |
| `--force-large` | Allow files >10MB (use with caution) |
| `--no-verify` | Skip pre-commit hooks (if any) |

## Usage

```bash
/cco-commit                 # Full flow: checks → analyze → commit
/cco-commit --dry-run       # Preview plan without committing
/cco-commit --single        # Force all changes into one commit
/cco-commit --skip-checks   # Skip quality gates (emergency use)
/cco-commit --force-large   # Allow large files (>10MB)
```
