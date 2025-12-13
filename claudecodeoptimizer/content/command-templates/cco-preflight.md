---
name: cco-preflight
description: Pre-release checks and workflow
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*), TodoWrite
---

# /cco-preflight

**Release Workflow** - Pre-flight → quality → cleanliness → review → verify → go/no-go.

Meta command that orchestrates other CCO commands for release preparation.

**Rules:** User Input | Git Safety | Go/No-Go Decision | Progress Tracking

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
| Which phases to run? | Verification (Recommended); Quality & Cleanup; Architecture; Changelog & Docs | true |

*MultiSelect: Kullanıcı birden fazla faz seçebilir. Tümü seçilirse = Full preflight.*

### Option Mapping

| Option | Covers | Phases |
|--------|--------|--------|
| Verification | Pre-flight checks + Final verification | 1, 5 |
| Quality & Cleanup | Quality audit + Cleanliness check | 2, 3 |
| Architecture | Architecture review | 4 |
| Changelog & Docs | Release notes + Documentation sync | 6 (NEW) |

**Default:** All phases if user doesn't specify

## Execution Optimization

<use_parallel_tool_calls>
When calling multiple tools with no dependencies between them, make all independent
calls in a single message. For example:
- Multiple cco-agent-analyze scopes → launch simultaneously
- Multiple file reads → batch in parallel
- Multiple grep searches → parallel calls

Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each phase.

```
TodoWrite([
  { content: "Run pre-flight checks", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Run quality gate", status: "pending", activeForm: "Running quality gate" },
  { content: "Check cleanliness", status: "pending", activeForm: "Checking cleanliness" },
  { content: "Review architecture", status: "pending", activeForm: "Reviewing architecture" },
  { content: "Run final verification", status: "pending", activeForm: "Running final verification" },
  { content: "Update changelog & docs", status: "pending", activeForm: "Updating changelog & docs" },
  { content: "Show go/no-go summary", status: "pending", activeForm: "Showing go/no-go summary" }
])
```

**Update status:** Mark `completed` immediately after each phase finishes, mark next `in_progress`.

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
│ Issues: {n} | Fixed: {n} | Declined: {n}                     │
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
│ Tests       │ {test_cmd}           │ {s}    │ {details}      │
│ Build       │ {build_cmd}          │ {s}    │ {details}      │
│ Lint        │ {lint_cmd}           │ {s}    │ {details}      │
│ Types       │ {type_cmd}           │ {s}    │ {details}      │
└─────────────┴──────────────────────┴────────┴────────────────┘
```

*Commands from context.md Operational section*

### Phase 6: Changelog & Docs Update (Release-Specific)

Analyzes all changes since last release tag and updates documentation:

| Step | Action | Output |
|------|--------|--------|
| 1. Diff Analysis | `git log {last_tag}..HEAD --oneline` | Commit list |
| 2. Change Classification | Categorize: Added, Changed, Fixed, Removed, Breaking | Grouped changes |
| 3. Version Suggestion | Analyze changes → suggest SemVer bump | Recommended version |
| 4. CHANGELOG Update | Generate/update entries for new version | CHANGELOG.md |
| 5. Docs Sync | Check README, docs/ for feature coverage | Missing docs list |
| 6. Apply Updates | Write changes (if auto-fix enabled) | Updated files |

**Change Classification:**

| Type | Detection | CHANGELOG Section |
|------|-----------|-------------------|
| Breaking | `BREAKING:`, API removal, signature change | ⚠️ Breaking Changes |
| Added | `feat:`, new files, new exports | Added |
| Changed | `refactor:`, `perf:`, modified behavior | Changed |
| Fixed | `fix:`, bug corrections | Fixed |
| Removed | Deleted files, removed exports | Removed |
| Security | `security:`, CVE fixes | Security |

**Version Suggestion (SemVer):**

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking changes | MAJOR (X.0.0) | 1.2.3 → 2.0.0 |
| New features (no breaking) | MINOR (x.Y.0) | 1.2.3 → 1.3.0 |
| Bug fixes only | PATCH (x.y.Z) | 1.2.3 → 1.2.4 |
| Pre-release | Keep suffix | 1.0.0-alpha → 1.0.0-beta |

**Version Analysis Logic:**
```
1. Check current version: pyproject.toml / package.json / __version__
2. Scan commits since last tag:
   - Any BREAKING: or removed exports? → MAJOR
   - Any feat: or new exports? → MINOR
   - Only fix: or refactor:? → PATCH
3. Cross-check with existing CHANGELOG entries
4. Suggest: {current} → {suggested} ({reason})
```

**Beginner-Friendly Explanation:**
```
┌─ VERSION SUGGESTION ─────────────────────────────────────────┐
│ Current: {current_version}                                   │
│ Suggested: {suggested_version} ({bump_type} bump)            │
├──────────────────────────────────────────────────────────────┤
│ Why {bump_type}?                                             │
│   {analysis_points}                                          │
├──────────────────────────────────────────────────────────────┤
│ SemVer Guide:                                                │
│   MAJOR (X.0.0): Breaking changes, removed features          │
│   MINOR (x.Y.0): New features, backward compatible           │
│   PATCH (x.y.Z): Bug fixes, no new features                  │
└──────────────────────────────────────────────────────────────┘
```

**Docs Sync Check:**

| Check | Source | Target |
|-------|--------|--------|
| New features | CHANGELOG Added | README.md, docs/ |
| API changes | Changed exports | API docs |
| Config changes | New options | Configuration docs |
| Breaking changes | BREAKING section | Migration guide |

```
┌─ CHANGELOG & DOCS ───────────────────────────────────────────┐
│ Analyzing changes since {last_tag}...                        │
├──────────────────────────────────────────────────────────────┤
│ Commits: {n} │ Files: {n} │ Breaking: {n} │ Features: {n}    │
├──────────────────────────────────────────────────────────────┤
│ VERSION SUGGESTION                                           │
│   Current: {current} → Suggested: {suggested} ({bump_type})  │
│   Reason: {reason}                                           │
├──────────────────────────────────────────────────────────────┤
│ CHANGELOG entries generated:                                 │
│   {entries_list}                                             │
├──────────────────────────────────────────────────────────────┤
│ Docs requiring update:                                       │
│   {docs_status_list}                                         │
├──────────────────────────────────────────────────────────────┤
│ Action: {Applied {n} updates | Review required | Up to date} │
└──────────────────────────────────────────────────────────────┘
```

**→ AskUserQuestion** (if updates needed):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply documentation updates? | Apply all; Review each; Skip | false |

### Phase 7: Go/No-Go Summary

```
┌─ RELEASE SUMMARY ────────────────────────────────────────────┐
│ Version: {version}                                           │
│ Branch: {branch}                                             │
│ Previous: {prev_version} ({n} commits ago)                   │
├──────────────────────────────────────────────────────────────┤
│ BLOCKERS (must fix before release):                          │
│   {blockers_list}                                            │
├──────────────────────────────────────────────────────────────┤
│ WARNINGS (should fix):                                       │
│   {warnings_list}                                            │
├──────────────────────────────────────────────────────────────┤
│ READY TO RELEASE: {YES|NO} {(with warnings)}                 │
├──────────────────────────────────────────────────────────────┤
│ Next Steps:                                                  │
│   1. {pending_actions}                                       │
│   2. git tag v{version}                                      │
│   3. git push origin {branch} --tags                         │
│   4. {publish_cmd}                                           │
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
| `--changelog` | Generate/update CHANGELOG entries only |
| `--docs` | Check and update documentation only |
| `--skip-docs` | Skip changelog & docs phase |

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

### Progress Tracking

*See Progress Tracking section above. Use TodoWrite for all phases.*
