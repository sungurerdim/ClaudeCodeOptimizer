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
- Version: !`for f in pyproject.toml package.json setup.py; do test -f "$f" && grep -E "version|__version__|VERSION" "$f"; done | head -1`
- Branch: !`git branch --show-current`
- Changelog: !`test -f CHANGELOG.md && head -20 CHANGELOG.md || echo "No CHANGELOG.md"`
- Git status: !`git status --short`
- Last tag: !`git describe --tags --abbrev=0 || echo "No tags"`

**Static context (Applicable, Type) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0": `CCO context not found. Run /cco-config first.` **Stop immediately.**

Sub-commands inherit context validation.

## Phase Selection

When called without flags → **AskUserQuestion** (mandatory):

| Question | Options | multiSelect |
|----------|---------|-------------|
| Which phases to run? | Verification (Recommended); Quality (Recommended); Architecture; Changelog & Docs | true |

| Option | Covers | Phases |
|--------|--------|--------|
| Verification | Pre-flight + Final verification | 1, 4 |
| Quality | Full quality gate | 2 |
| Architecture | Architecture review | 3 |
| Changelog & Docs | Release notes + docs sync | 5 |

**Default:** All phases. **Parallel:** Independent operations in single message.

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Run pre-flight checks", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Run quality gate", status: "pending", activeForm: "Running quality gate" },
  { content: "Review architecture", status: "pending", activeForm: "Reviewing architecture" },
  { content: "Run final verification", status: "pending", activeForm: "Running final verification" },
  { content: "Update changelog & docs", status: "pending", activeForm: "Updating changelog & docs" },
  { content: "Show go/no-go summary", status: "pending", activeForm: "Showing go/no-go summary" }
])
```

## Flow

### Phase 1: Pre-flight Checks (Release-Specific)

| Check | Verification | Blocker? |
|-------|--------------|----------|
| Git state | Clean working directory | YES |
| Branch | On main/master or release | WARN |
| Version | Valid semver in manifest | YES |
| Version sync | `__version__` = CHANGELOG = pyproject.toml | YES |
| Changelog | Updated for this version | WARN |
| Dependencies | No outdated with vulnerabilities | WARN |
| Breaking changes | Documented in changelog | WARN |
| Leftover markers | No TODO/WIP/FIXME in src | WARN |
| Feature trace | CHANGELOG items in README/docs | WARN |
| Install self-test | `cco-install --dry-run` (if CCO) | YES |
| Semver review | Changes match version bump | WARN |

**Version Sync:**
```bash
grep "__version__" src/__init__.py
grep "version" pyproject.toml
grep "^\[" CHANGELOG.md | head -1
```

**Leftover Markers:**
```bash
grep -rn "TODO\|FIXME\|WIP\|HACK\|XXX" src/ --include="*.py"
grep -rn "Experimental\|DRAFT\|PLACEHOLDER" docs/
```

**Feature Trace:** For each Added in CHANGELOG: 1. README.md? 2. docs/? 3. Implementation?

**Semver:** PATCH (x.x.1) = fixes only │ MINOR (x.1.0) = new features │ MAJOR (1.0.0) = breaking

### Phase 2: Quality Gate

Orchestrates: `/cco-optimize --pre-release --fix` (Security, Quality, Hygiene, Best Practices)

### Phase 3: Architecture Review

Orchestrates: `/cco-review --quick` (Gap analysis, DX review, What's working)

### Phase 4: Final Verification (Release-Specific)

| Check | Command | Blocker? |
|-------|---------|----------|
| Full test suite | `{test_command}` | YES |
| Build | `{build_command}` | YES |
| Lint | `{lint_command}` | YES |
| Type check | `{type_command}` | YES |

*Commands from context.md Operational section*

### Phase 5: Changelog & Docs Update (Release-Specific)

| Step | Action | Output |
|------|--------|--------|
| 1. Diff | `git log {last_tag}..HEAD --oneline` | Commits |
| 2. Classify | Added, Changed, Fixed, Removed, Breaking | Groups |
| 3. Version | Analyze → suggest SemVer bump | Recommended |
| 4. CHANGELOG | Generate/update entries | CHANGELOG.md |
| 5. Docs Sync | Check README, docs/ coverage | Missing docs |
| 6. Apply | Write changes (if enabled) | Updated files |

**Change Classification:**

| Type | Detection | Section |
|------|-----------|---------|
| Breaking | `BREAKING:`, API removal | ⚠️ Breaking |
| Added | `feat:`, new files/exports | Added |
| Changed | `refactor:`, `perf:` | Changed |
| Fixed | `fix:`, corrections | Fixed |
| Removed | Deleted files/exports | Removed |
| Security | `security:`, CVE fixes | Security |

**Version Analysis Logic:**
```
1. Check current: pyproject.toml / package.json / __version__
2. Scan commits since last tag:
   - BREAKING: or removed exports? → MAJOR
   - feat: or new exports? → MINOR
   - Only fix: or refactor:? → PATCH
3. Cross-check CHANGELOG entries
4. Suggest: {current} → {suggested} ({reason})
```

**SemVer:** MAJOR = breaking │ MINOR = features │ PATCH = fixes │ Pre-release = keep suffix

**Docs Sync:** Features → README/docs │ API changes → API docs │ Config → Config docs │ Breaking → Migration guide

**→ AskUserQuestion** (if updates needed):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply documentation updates? | Apply all; Review each; Skip | false |

### Phase 6: Go/No-Go Summary

Shows: Version, Branch, Previous, Blockers, Warnings, Ready status, Next steps (`git tag`, `git push --tags`, publish)

**→ AskUserQuestion** (mandatory):

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Release decision? | Proceed (create tag); Fix warnings first; Abort | false |

If warnings + "Proceed" → confirm: `Yes, proceed anyway; No, fix first`

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Check without fixing |
| `--strict` | Treat warnings as blockers |
| `--skip-tests` | Skip test suite |
| `--tag` | Create git tag |
| `--push` | Push to remote |
| `--changelog` | CHANGELOG entries only |
| `--docs` | Documentation only |
| `--skip-docs` | Skip changelog & docs |

## Go/No-Go Decision

| Status | Action |
|--------|--------|
| Blocker (red) | Cannot release |
| Warning (yellow) | Can override |
| Pass (green) | Ready |

## Rules

Git Safety: Clean state │ Version sync │ No force push │ Use TodoWrite for phases
