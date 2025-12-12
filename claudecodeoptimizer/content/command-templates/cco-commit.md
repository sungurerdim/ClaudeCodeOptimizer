---
name: cco-commit
description: Atomic commits with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*), TodoWrite
---

# /cco-commit

**Smart Commits** - Quality gates → analyze → group atomically → commit.

End-to-end: Runs checks, analyzes changes, creates atomic commits.

**Rules:** User Input | Git Safety | Quick Mode | Task Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`
- Staged files: !`git diff --cached --name-only`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -3`

**Static context (Tools, Type, Maturity, Priority) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
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
| Large file detected ({file}, {size}). Continue? | Yes; No | false |

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
| Include unstaged changes? | Yes (analyze all); No (staged only) | false |

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

## Commit Message Quality [CRITICAL]

### Vague Message Detection

**Do NOT accept generic or vague commit messages.**

| Pattern | Example | Action |
|---------|---------|--------|
| Generic verbs only | "update code", "fix bug", "make changes" | ❌ REJECT |
| No context | "changes", "updates", "stuff" | ❌ REJECT |
| Too short (<10 chars) | "fix", "wip", "done" | ❌ REJECT |
| Non-imperative | "fixed", "adding", "updated" | ⚠️ WARN + fix |
| File names only | "update main.py" | ❌ REJECT |

### Quality Checklist

Before finalizing ANY commit message:
1. **Specificity**: Does it describe WHAT changed specifically?
2. **Context**: Does it explain WHERE the change is (scope)?
3. **Purpose**: Does body explain WHY (if non-obvious)?
4. **Searchability**: Would you find this in `git log --grep`?

### Message Transform Examples

| ❌ Bad | ✅ Good |
|--------|---------|
| "fix bug" | "fix(auth): prevent session timeout on token refresh" |
| "update tests" | "test(api): add edge case coverage for rate limiting" |
| "refactor code" | "refactor(parser): extract validation into separate module" |
| "add feature" | "feat(export): add CSV export option for reports" |

## Change Type Classification [CRITICAL]

### Type Definitions

| Type | Definition | Detection Signals |
|------|------------|-------------------|
| **feat** | New capability for users | New export, new endpoint, new command, new option |
| **fix** | Bug correction | Error handling added, null check, off-by-one, crash fix |
| **refactor** | Structure change, SAME behavior | Rename, extract, inline, move (no new tests needed) |
| **perf** | Performance improvement | Cache added, algorithm optimized, lazy load |
| **test** | Test changes only | Files in test/, spec/, __tests__ ONLY |
| **docs** | Documentation only | .md, docstrings, comments ONLY |
| **style** | Formatting only | Whitespace, semicolons, quotes (no logic change) |
| **build** | Build system/deps | package.json, pyproject.toml, Makefile, Dockerfile |
| **ci** | CI configuration | .github/, .gitlab-ci.yml, .circleci/ |
| **chore** | Maintenance tasks | .gitignore, editor config, tooling |

### Classification Verification [REQUIRED]

**Read the actual diff** before assigning type:
- Behavior changes → NOT refactor (use fix or feat)
- New test for existing code → test (not feat)
- Fixing broken test → fix (not test)
- Security dependency update → fix (not chore)
- New test + implementation → feat (not test)

### Ambiguous Cases

| Change | Looks Like | Actually Is | Why |
|--------|------------|-------------|-----|
| Add validation | feat | fix | Prevents existing bug |
| Rename public API | refactor | feat + BREAKING | Changes user interface |
| Add error message | feat | fix | Improves existing error |
| Update README usage | docs | feat | If new feature documented |

## Atomic Commit Verification [CRITICAL]

### Pre-Commit Atomicity Check

Before finalizing each commit group, verify:

| Check | Question | Fail Action |
|-------|----------|-------------|
| **Self-contained** | Is implementation complete? | Merge remaining work or defer |
| **Independent** | Can this be reverted alone? | Reorder commits |
| **Complete** | Are related tests included? | Add tests or mark as tech debt |
| **Working** | Does codebase work after this commit? | Don't commit broken state |

### Rollback Simulation

For each commit, mentally verify:
```
IF git revert {this-commit}:
  → Codebase still compiles/runs?
  → Other commits still apply cleanly?
  → No orphaned code/imports left?
```

If ANY answer is NO → Commit is not atomic, restructure grouping.

### Dependency Chain Warning

When commits have dependencies:
```
Commit 1: Add interface       ← Base (reverting breaks 2,3)
Commit 2: Implement interface ← Depends on 1
Commit 3: Use implementation  ← Depends on 2

Output:
⚠️ Commit chain detected: 1 → 2 → 3
   Reverting commit 1 will require reverting 2, 3
   Consider: Squash if tightly coupled
```

## Semantic Versioning Impact

### Commit-to-Version Mapping

| Commit Type | Version Impact | Changelog Section |
|-------------|----------------|-------------------|
| feat | MINOR (0.X.0) | Added |
| fix | PATCH (0.0.X) | Fixed |
| perf | PATCH (0.0.X) | Changed |
| refactor | PATCH (0.0.X) | Changed |
| BREAKING CHANGE | MAJOR (X.0.0) | Breaking |
| docs/style/test/ci | None | - |

### Version Impact Summary

After generating commit plan, show:
```
┌─ VERSION IMPACT ─────────────────────────────────────────────┐
│ Highest impact: MINOR (feat detected)                        │
│ Breakdown: 1 feat, 2 fix, 1 refactor, 1 test                │
│ Suggested: v1.3.0 → v1.4.0                                   │
└──────────────────────────────────────────────────────────────┘
```

## Commit History Consistency

### Style Detection

Before generating messages, analyze last 10 commits:
- Scope usage: always / sometimes / never
- Capitalization: lowercase / Sentence case
- Issue references: none / footer (#123) / inline
- Emoji: none / prefix / suffix

### Match Existing Style

```
Detected from history:
- Scope: Always used ✓
- Case: lowercase ✓
- Issues: Footer (Fixes #123)
- Emoji: None

→ Generated messages follow detected style
```

**If no history or inconsistent:** Default to conventional commits standard.

## Title Format

```
<type>(<scope>): <imperative verb> <specific change>
```

**Types:** feat, fix, refactor, perf, test, docs, style, build, ci, chore

## Output

**Follow output formats precisely.**

### Quality Gates
```
┌─ QUALITY GATES ──────────────────────────────────────────────┐
│ Check       │ Status │ Details                               │
├─────────────┼────────┼───────────────────────────────────────┤
│ Secrets     │ {s}    │ {details}                             │
│ Large Files │ {s}    │ {details}                             │
│ Format      │ {s}    │ {details}                             │
│ Lint        │ {s}    │ {details}                             │
│ Types       │ {s}    │ {details}                             │
│ Tests       │ {s}    │ {details}                             │
└─────────────┴────────┴───────────────────────────────────────┘
```

### Commit Plan
```
┌─ COMMIT PLAN ────────────────────────────────────────────────┐
│ # │ Type     │ Scope   │ Description          │ Files        │
├───┼──────────┼─────────┼──────────────────────┼──────────────┤
│ 1 │ {type}   │ {scope} │ {description}        │ {n}          │
│ 2 │ {type}   │ {scope} │ {description}        │ {n}          │
│ ...                                                          │
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
| Add BREAKING CHANGE footer? | Yes; No | false |

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
| Commit plan ready. Action? | Accept; Modify; Merge; Split; Edit message; Cancel | false |

| Option | Behavior |
|--------|----------|
| Accept | Execute plan as shown |
| Modify | Reassign files to different commits |
| Merge | Combine selected commits into one |
| Split | Break a commit into smaller pieces |
| Edit message | Change commit type/scope/description |
| Cancel | Abort without committing |

### Follow-up Questions (multiSelect)

**If Merge selected:**
| Question | Options | multiSelect |
|----------|---------|-------------|
| Which commits to merge? | Commit 1: {desc}; Commit 2: {desc}; ... | true |

**If Modify selected:**
| Question | Options | multiSelect |
|----------|---------|-------------|
| Which commits to modify? | Commit 1: {desc}; Commit 2: {desc}; ... | true |

**If Edit message selected:**
| Question | Options | multiSelect |
|----------|---------|-------------|
| Which messages to edit? | Commit 1: {desc}; Commit 2: {desc}; ... | true |

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show plan without committing |
| `--single` | Force all changes into one commit |
| `--quick` | Single-message execution: stage all, commit, no questions |
| `--skip-checks` | Skip quality gates (emergency use) |
| `--force-large` | Allow files >10MB (use with caution) |
| `--no-verify` | Skip pre-commit hooks (if any) |
| `--amend` | Amend last commit (with safety checks) |

### Quick Mode (`--quick`) [SINGLE-MESSAGE]

**You MUST do all steps in a single message. Do not use any other tools beyond allowed.**

```
[Single message with all tool calls:]
1. Bash: git status
2. Bash: git diff --cached --name-only
3. Bash: git add -A (if nothing staged)
4. Bash: git commit -m "type(scope): message"
5. [Final summary only]
```

No questions, no intermediate text, smart defaults for commit message.

### Amend Safety

Before `--amend`:
1. Check HEAD commit authorship matches current user
2. Verify commit not pushed to remote
3. Show what will be amended
4. Use AskUserQuestion for confirmation

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Amend commit "{hash}: {message}"? | Yes; No | false |

## Usage

```bash
/cco-commit                 # Full flow: checks → analyze → commit
/cco-commit --dry-run       # Preview plan without committing
/cco-commit --single        # Force all changes into one commit
/cco-commit --skip-checks   # Skip quality gates (emergency use)
/cco-commit --amend         # Amend last commit
```

## Related Commands

- `/cco-optimize` - For pre-commit quality checks
- `/cco-preflight` - For release commits

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Git Safety

- **Pre-op**: Check git status before operations
- **No-Force**: Never force push unless explicitly requested
- **Amend-Check**: Verify authorship before amending

### Quick Mode

When `--quick` flag or single-message mode:
- **No-Questions**: Use smart defaults
- **Single-Message**: Complete ALL steps in one message
- **No-Intermediate**: Only tool calls, then final summary

### Task Tracking

- **Create**: TODO list with commit plan
- **Status**: pending → in_progress → completed
- **Accounting**: staged + committed + skipped = total
