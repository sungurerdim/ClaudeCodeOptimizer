---
name: cco-release
description: Pre-release workflow orchestration
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*)
---

# /cco-release

**Release Workflow** - Pre-flight → quality → cleanliness → review → verify → go/no-go.

Meta command that orchestrates other CCO commands for release preparation.

**Standards:** Command Flow | User Input | Output Formatting

## Context

- Context check: !`grep -c "CCO_ADAPTIVE_START" ./CLAUDE.md 2>/dev/null || echo "0"`
- Version: !`grep -E "version|__version__|VERSION" pyproject.toml package.json setup.py 2>/dev/null | head -1`
- Branch: !`git branch --show-current`
- Changelog: !`head -20 CHANGELOG.md 2>/dev/null || echo "No CHANGELOG.md"`
- Git status: !`git status --short`
- Last tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags"`

**Static context (Applicable, Type) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO_ADAPTIVE in ./CLAUDE.md.**

If context check returns "0":
```
CCO_ADAPTIVE not found in ./CLAUDE.md

Run /cco-tune first to configure project context, then restart CLI.
```
**Stop execution immediately.**

**Phase Validation:** Sub-commands (cco-audit, cco-optimize, cco-review) inherit context validation and only run applicable checks.

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
| Install self-test | `cco-setup --dry-run` passes (if CCO project) | YES |
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
│ Git Clean      │ OK     │ No uncommitted changes             │
│ Branch         │ OK     │ main                               │
│ Version        │ OK     │ 1.2.0 (valid semver)              │
│ Version Sync   │ OK     │ All 3 sources match               │
│ Changelog      │ WARN   │ Last entry: 1.1.0                 │
│ Dependencies   │ OK     │ 0 outdated, 0 vulnerabilities     │
│ Breaking       │ OK     │ None detected                      │
│ Markers        │ WARN   │ 2 TODOs in src/utils.py           │
│ Feature Trace  │ OK     │ 5/5 features documented           │
│ Install Test   │ SKIP   │ Not a CCO project                 │
│ Semver         │ OK     │ MINOR appropriate                 │
└────────────────┴────────┴────────────────────────────────────┘
```

### Phase 2: Quality Gate

Orchestrates: `/cco-audit --pre-release --auto-fix`

Includes:
- Security checks (OWASP, secrets, CVEs)
- Test quality and coverage
- Consistency (doc-code mismatch)
- Self-compliance

```
┌─ QUALITY GATE ───────────────────────────────────────────────┐
│ → Running: /cco-audit --pre-release --auto-fix               │
├──────────────────────────────────────────────────────────────┤
│ Security      │ 95%   │ OK                                   │
│ Tests         │ 88%   │ WARN (coverage below 90%)           │
│ Consistency   │ 100%  │ OK                                   │
│ Compliance    │ 92%   │ OK                                   │
├──────────────────────────────────────────────────────────────┤
│ Issues: 2 | Fixed: 1 | Manual: 1                             │
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
│ Orphans       │ 0     │ OK                                   │
│ Stale-Refs    │ 0     │ OK                                   │
│ Duplicates    │ 0     │ OK                                   │
├──────────────────────────────────────────────────────────────┤
│ Cleaned: 0 | Skipped: 0                                      │
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
/cco-release                   # Full release workflow
/cco-release --dry-run         # Check without fixing
/cco-release --strict          # Fail on any warning
/cco-release --tag             # Auto-create git tag
/cco-release --tag --push      # Tag and push
```

## Related Commands

- `/cco-audit` - Quality checks (used in Phase 2)
- `/cco-optimize` - Cleanliness (used in Phase 3)
- `/cco-review` - Architecture (used in Phase 4)
- `/cco-commit` - For committing fixes
