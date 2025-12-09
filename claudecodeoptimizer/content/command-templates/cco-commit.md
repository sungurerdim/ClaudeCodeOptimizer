---
name: cco-commit
description: Atomic traceable change management with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*)
---

# /cco-commit

**Smart Commits** - Quality gates → analyze → group atomically → commit.

End-to-end: Runs checks, analyzes changes, creates atomic commits.

**Standards:** Command Flow | Pre-Operation Safety | User Input | Approval Flow | Output Formatting

## Context

- Context check: !`grep -c "CCO_ADAPTIVE_START" ./CLAUDE.md 2>/dev/null || echo "0"`
- Git status: !`git status --short`
- Staged files: !`git diff --cached --name-only`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -3`

**Static context (Tools, Type, Maturity, Priority) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO_ADAPTIVE in ./CLAUDE.md.**

If context check returns "0":
```
CCO_ADAPTIVE not found in ./CLAUDE.md

Run /cco-tune first to configure project context, then restart CLI.
```
**Stop execution immediately.**

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
5. **Type Check** - Verify type consistency (if typed language)
6. **Test** - Verify behavior (read-only)

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
| File > 1MB | Warn, use AskUserQuestion for confirmation |
| Binary file (non-text) | Warn, suggest Git LFS |
| File > 10MB | Block, require `--force-large` |

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Large file detected ({file}, {size}). Continue? | Yes, No | false |

### Behavior

- Run checks in order, stop on blocking failure
- If format modifies files, include in commit
- If lint fails with unfixable errors, stop and report
- If type check fails, stop and report
- If tests fail, stop and report - never commit broken code
- Show summary: `Secrets: {status} | Format: {status} | Lint: {status} | Types: {status} | Tests: {count} passed`

### Skip Option

Use `--skip-checks` to bypass (use with caution).

## Dependency Impact Analysis

For changes that modify interfaces or exports:

| Change Type | Analysis |
|-------------|----------|
| Function signature | Find all callers, verify compatibility |
| Export removal | Find all importers, warn if external |
| Type change | Check downstream type compatibility |
| Config change | Verify dependent configs |

Report: `[IMPACT] {change} affects {N} files: {file1}, {file2}...`

## Staged vs Unstaged Handling

| State | Behavior |
|-------|----------|
| Nothing staged, has unstaged | Analyze all unstaged, propose grouping |
| Has staged, has unstaged | Use AskUserQuestion (see below) |
| Has staged, no unstaged | Commit staged as-is (user already decided) |
| Nothing staged, nothing unstaged | Show "No changes to commit" and exit |

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Include unstaged changes? | Yes (analyze all), No (staged only) | false |

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

### Quality Gates
```
┌─ QUALITY GATES ──────────────────────────────────────────────┐
│ Check       │ Status │ Details                               │
├─────────────┼────────┼───────────────────────────────────────┤
│ Secrets     │ OK     │ No secrets detected                   │
│ Large Files │ OK     │ No large files                        │
│ Format      │ OK     │ 2 files formatted                     │
│ Lint        │ OK     │ Clean                                 │
│ Types       │ OK     │ No type errors                        │
│ Tests       │ OK     │ 42 passed                             │
└─────────────┴────────┴───────────────────────────────────────┘
```

### Commit Plan
```
┌─ COMMIT PLAN ────────────────────────────────────────────────┐
│ # │ Type     │ Scope   │ Description          │ Files        │
├───┼──────────┼─────────┼──────────────────────┼──────────────┤
│ 1 │ feat     │ auth    │ add login endpoint   │ 3            │
│ 2 │ fix      │ ui      │ correct alignment    │ 1            │
│ 3 │ docs     │ -       │ update README        │ 1            │
└───┴──────────┴─────────┴──────────────────────┴──────────────┘
```

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
2. Use AskUserQuestion (see below)
3. If Yes, append to commit body:
   ```
   BREAKING CHANGE: {description of what breaks and migration path}
   ```

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Add BREAKING CHANGE footer? | Yes, No | false |

## Flow

1. **Quality Gates** - Run secrets → large files → format → lint → types → test (stop on failure)
2. **Analyze** - `git status`, `git diff`, detect change types + breaking changes + impacts
3. **Group** - Apply atomic grouping rules
4. **Plan** - Show commit plan with files per commit
5. **Confirm** - User approval
6. **Execute** - Stage and commit each group in order
7. **Verify** - `git log` count = planned count

### Confirm Options

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Commit plan ready. Action? | Accept, Modify, Merge, Split, Edit message, Cancel | false |

| Option | Behavior |
|--------|----------|
| Accept | Execute plan as shown |
| Modify | Reassign files to different commits |
| Merge | Combine selected commits into one |
| Split | Break a commit into smaller pieces |
| Edit message | Change commit type/scope/description |
| Cancel | Abort without committing |

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show plan without committing |
| `--single` | Force all changes into one commit |
| `--skip-checks` | Skip quality gates (emergency use) |
| `--force-large` | Allow files >10MB (use with caution) |
| `--no-verify` | Skip pre-commit hooks (if any) |
| `--amend` | Amend last commit (with safety checks) |

### Amend Safety

Before `--amend`:
1. Check HEAD commit authorship matches current user
2. Verify commit not pushed to remote
3. Show what will be amended
4. Use AskUserQuestion for confirmation

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Amend commit "{hash}: {message}"? | Yes, No | false |

## Usage

```bash
/cco-commit                 # Full flow: checks → analyze → commit
/cco-commit --dry-run       # Preview plan without committing
/cco-commit --single        # Force all changes into one commit
/cco-commit --skip-checks   # Skip quality gates (emergency use)
/cco-commit --amend         # Amend last commit
```

## Related Commands

- `/cco-audit` - For pre-commit quality checks
- `/cco-release` - For release commits
