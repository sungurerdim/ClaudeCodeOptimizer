---
name: cco-preflight
description: Pre-release checks and workflow
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*), TodoWrite
---

# /cco-preflight

**Release Workflow** - Pre-flight → quality → cleanliness → review → verify → go/no-go.

Meta command that orchestrates other CCO commands for release preparation.

**Rules:** User Input | Git Safety | Go/No-Go Decision | Task Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Version: !`grep -E "version|__version__|VERSION" pyproject.toml package.json setup.py 2>/dev/null | head -1`
- Branch: !`git branch --show-current`
- Changelog: !`head -20 CHANGELOG.md 2>/dev/null || echo "No CHANGELOG.md"`
- Git status: !`git status --short`
- Last tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags"`

**Static context (Applicable, Type) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

**Phase Validation:** Sub-commands (cco-optimize, cco-review) inherit context validation and only run applicable checks.

## Phase Selection

When called without flags → **AskUserQuestion** (mandatory):

| Question | Options | multiSelect |
|----------|---------|-------------|
| Which phases to run? | Pre-flight Checks; Quality Audit; Cleanliness Check; Architecture Review; Final Verification; All (Recommended) | true |

**Default:** All (if user doesn't specify)

## Execution Optimization

<use_parallel_tool_calls>
When calling multiple tools with no dependencies between them, make all independent
calls in a single message. For example:
- Multiple cco-agent-analyze scopes → launch simultaneously
- Multiple file reads → batch in parallel
- Multiple grep searches → parallel calls

Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>

## Flow

### Phase 1: Pre-flight Checks (Release-Specific)

| Check | Verification | Blocker? |
|-------|--------------|----------|
| Git state | Clean working directory | YES |
| Branch | On main/master or release branch | WARN |
| Version | Valid semver in manifest | YES |
| Version sync | `__version__` = CHANGELOG = pyproject.toml | YES |
| Changelog | Updated for this version | WARN |
| Dependencies | No outdated with vulnerabilities | WARN |
| Breaking changes | Documented in changelog | WARN |
| Leftover markers | No TODO/WIP/FIXME/Experimental in src | WARN |
| Feature trace | New CHANGELOG items exist in README/docs | WARN |
| Install self-test | `cco-install --dry-run` passes (if CCO project) | YES |
| Semver review | Changes appropriate for version bump type | WARN |

**Version Sync:** Cross-file version matching
```bash
# Must all match
grep "__version__" src/__init__.py
grep "version" pyproject.toml
grep "^\[" CHANGELOG.md | head -1
```

**Leftover Markers:** Scan for incomplete work
```bash
grep -rn "TODO\|FIXME\|WIP\|HACK\|XXX" src/ --include="*.py"
grep -rn "Experimental\|DRAFT\|PLACEHOLDER" docs/
```

**Feature Trace:** For each Added item in CHANGELOG:
1. Mentioned in README.md?
2. Documented in docs/?
3. Implementation exists?

**Semver Review:**
| Version Bump | Appropriate Changes |
|--------------|---------------------|
| PATCH (x.x.1) | Bug fixes only, no new features |
| MINOR (x.1.0) | New features, backward compatible |
| MAJOR (1.0.0) | Breaking changes, API removals |

```
┌─ PRE-FLIGHT ─────────────────────────────────────────────────┐
│ Check          │ Status │ Details                            │
├────────────────┼────────┼────────────────────────────────────┤
│ Git Clean      │ {s}    │ {details}                          │
│ Branch         │ {s}    │ {branch}                           │
│ Version        │ {s}    │ {version} ({validation})           │
│ Version Sync   │ {s}    │ {sync_details}                     │
│ Changelog      │ {s}    │ {changelog_details}                │
│ Dependencies   │ {s}    │ {dep_details}                      │
│ Breaking       │ {s}    │ {breaking_details}                 │
│ Markers        │ {s}    │ {marker_details}                   │
│ Feature Trace  │ {s}    │ {trace_details}                    │
│ Install Test   │ {s}    │ {install_details}                  │
│ Semver         │ {s}    │ {semver_details}                   │
└────────────────┴────────┴────────────────────────────────────┘
```

### Phase 2: Quality Gate

Orchestrates: `/cco-optimize --pre-release --auto-fix`

Includes:
- Security checks (OWASP, secrets, CVEs)
- Test quality and coverage
- Consistency (doc-code mismatch)
- Self-compliance

```
┌─ QUALITY GATE ───────────────────────────────────────────────┐
│ → Running: /cco-optimize --pre-release --auto-fix            │
├──────────────────────────────────────────────────────────────┤
│ Security      │ {n}%  │ {status}                             │
│ Tests         │ {n}%  │ {status}                             │
│ Consistency   │ {n}%  │ {status}                             │
│ Compliance    │ {n}%  │ {status}                             │
├──────────────────────────────────────────────────────────────┤
│ Issues: {n} | Fixed: {n} | Manual: {n}                       │
└──────────────────────────────────────────────────────────────┘
```

### Phase 3: Cleanliness

Orchestrates: `/cco-optimize --hygiene --auto-fix`

Includes:
- Orphan removal
- Stale reference cleanup
- Duplicate consolidation

```
┌─ CLEANLINESS ────────────────────────────────────────────────┐
│ → Running: /cco-optimize --hygiene --auto-fix                │
├──────────────────────────────────────────────────────────────┤
│ Orphans       │ {n}   │ {status}                             │
│ Stale-Refs    │ {n}   │ {status}                             │
│ Duplicates    │ {n}   │ {status}                             │
├──────────────────────────────────────────────────────────────┤
│ Cleaned: {n} | Skipped: {n}                                  │
└──────────────────────────────────────────────────────────────┘
```

### Phase 4: Architecture Review

Orchestrates: `/cco-review --quick`

Includes:
- Gap analysis (quick)
- DX review
- What's working well

```
┌─ ARCHITECTURE ───────────────────────────────────────────────┐
│ → Running: /cco-review --quick                               │
├──────────────────────────────────────────────────────────────┤
│ Gaps Found    │ 1     │ Minor: undocumented export          │
│ DX Score      │ Good  │ Clear CLI, good errors              │
│ Working Well  │ 5     │ Clean separation, good tests        │
└──────────────────────────────────────────────────────────────┘
```

### Phase 5: Final Verification (Release-Specific)

| Check | Command | Blocker? |
|-------|---------|----------|
| Full test suite | `{test_command}` | YES |
| Build | `{build_command}` | YES |
| Lint | `{lint_command}` | YES |
| Type check | `{type_command}` | YES |

```
┌─ FINAL VERIFICATION ─────────────────────────────────────────┐
│ Check       │ Command              │ Status │ Details        │
├─────────────┼──────────────────────┼────────┼────────────────┤
│ Tests       │ pytest tests/        │ PASS   │ 142 passed     │
│ Build       │ python -m build      │ PASS   │ dist/ created  │
│ Lint        │ ruff check .         │ PASS   │ Clean          │
│ Types       │ mypy src/            │ PASS   │ No errors      │
└─────────────┴──────────────────────┴────────┴────────────────┘
```

### Phase 6: Go/No-Go Summary

```
┌─ RELEASE SUMMARY ────────────────────────────────────────────┐
│ Version: 1.2.0                                               │
│ Branch: main                                                 │
│ Previous: 1.1.0 (15 commits ago)                            │
├──────────────────────────────────────────────────────────────┤
│ BLOCKERS (must fix before release):                          │
│   (none)                                                     │
├──────────────────────────────────────────────────────────────┤
│ WARNINGS (should fix):                                       │
│   • Test coverage 88% (target: 90%)                         │
│   • Changelog not updated for 1.2.0                         │
├──────────────────────────────────────────────────────────────┤
│ READY TO RELEASE: YES (with warnings)                       │
├──────────────────────────────────────────────────────────────┤
│ Next Steps:                                                  │
│   1. Update CHANGELOG.md                                    │
│   2. git tag v1.2.0                                         │
│   3. git push origin main --tags                            │
│   4. Publish: python -m twine upload dist/*                 │
└──────────────────────────────────────────────────────────────┘
```

**→ AskUserQuestion** (mandatory):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Release decision? | Proceed (create tag); Fix warnings first; Abort | false |

If warnings exist and "Proceed" selected **→ AskUserQuestion** (mandatory):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Confirm release with {N} warnings? | Yes, proceed anyway; No, fix first | false |

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Run all checks without fixing |
| `--strict` | Treat warnings as blockers |
| `--skip-tests` | Skip test suite (not recommended) |
| `--tag` | Create git tag after success |
| `--push` | Push to remote after success |

## Usage

```bash
/cco-preflight                   # Full release workflow
/cco-preflight --dry-run         # Check without fixing
/cco-preflight --strict          # Fail on any warning
/cco-preflight --tag             # Auto-create git tag
/cco-preflight --tag --push      # Tag and push
```

## Related Commands

- `/cco-optimize` - Quality checks (used in Phase 2)
- `/cco-optimize` - Cleanliness (used in Phase 3)
- `/cco-review` - Architecture (used in Phase 4)
- `/cco-commit` - For committing fixes

---

## Behavior Rules

*Inherits: User Input rules from cco-tools.md*

### Git Safety

- **Clean-State**: Require clean git state before release
- **Version-Sync**: Verify version in all files matches
- **No-Force**: Never force push release branches

### Go/No-Go Decision

| Status | Meaning | Action |
|--------|---------|--------|
| Blocker (red) | Must fix | Cannot release |
| Warning (yellow) | Should fix | Can override |
| Pass (green) | All clear | Ready to release |

### Task Tracking

- **Create**: TODO list with release phases
- **Status**: pending → in_progress → completed
- **Accounting**: passed + fixed + blocked = total
