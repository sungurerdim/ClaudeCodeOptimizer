---
description: Release verification gate - full optimization + review + tests + build
argument-hint: "[--auto] [--preview]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, Skill, AskUserQuestion
model: opus
---

# /cco:preflight

**Release Verification Gate** — Comprehensive pre-release checks with parallel orchestration.

Meta command orchestrating `/cco:optimize` and `/cco:align` with maximum parallelism.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | Full fix, no questions, single-line summary. Exit: 0/1/2 |
| `--preview` | Run all checks, show results, don't release |

## Context Detection

At start, detect project context using Claude's native tools:

| Context | Detection Method |
|---------|------------------|
| Version | Glob for `pyproject.toml`, `package.json`, `setup.py` → Read version field |
| Branch | `git branch --show-current` |
| Changelog | Read first 20 lines of `CHANGELOG.md` if exists |
| Git status | `git status --short` |
| Last tag | `git describe --tags --abbrev=0` |

**Use Glob/Read for file detection. Git commands are cross-platform.**

## Execution Flow

Setup → Pre-checks → (Verify ‖ Optimize ‖ Align) → Changelog → [Plan] → Execute

### Phase 1: Setup [SKIP IF --auto]

**Q1:** Two questions:
- Checks (multiselect): Security (Recommended), Code Quality (Recommended), Architecture, Tests + Build
- Release mode: Fix Only (Recommended) / Fix + Commit + Tag

### Phase 2: Pre-flight Checks [PARALLEL]

| Check | Type | Detail |
|-------|------|--------|
| PRE-01 | BLOCKER | Dirty working directory |
| PRE-03 | BLOCKER | Version mismatch (manifest vs changelog) |
| PRE-02 | WARN | Not on main/master/release/* branch |
| PRE-04 | WARN | TODO/FIXME markers in code |
| DEP-SEC | BLOCKER | Security advisories in dependencies |
| DEP-OUT | WARN | Outdated non-security packages |

Dependency audit via cco-agent-research (scope: dependency).

### Phase 3: Verify + Optimize + Align [PARALLEL]

Run concurrently:
- Background Bash: format, lint, type, test, build commands
- Skill calls: `Skill("cco:optimize", "--auto")` and `Skill("cco:align", "--auto")`

Collect ALL background results via TaskOutput before any output.

### Phase 4: Changelog

Classify commits since last tag by conventional commit type. Suggest version bump: breaking → MAJOR, feat → MINOR, else → PATCH. Generate changelog entry.

### Phase 5: Plan Review [CONDITIONAL]

Triggers when: findings > 0 OR blockers detected. Skip in --auto.

Display release plan: pre-flight status, sub-command results, verification results, breaking changes, blockers, changelog preview, release checklist.

If blockers: ask Fix and Retry / View Details / Abort.
If no blockers: standard Action + Severity questions.

### Phase 6: Execute

Based on release mode:
- Fix Only: apply fixes, suggest next steps
- Fix + Commit + Tag: commit and tag with suggested version

### Phase 7: Summary

Combined applied/failed/total accounting from optimize + align. Verification results table.

--auto mode: `cco-preflight: {OK|WARN|BLOCKED} | Applied: N | Failed: N | Version: vX.Y.Z`

Status: OK (blockers=0, tests pass, build pass), WARN (warnings only), BLOCKED (blockers or test/build fail).

## Release Checks (14 total)

**BLOCKERS:** PRE-01 (dirty git), PRE-03 (version mismatch), VER-01 (tests fail), VER-02 (build fail), VER-03 (type errors), DEP-SEC (CVE), OPT-CRIT (optimize critical), REV-CRIT (align critical)

**WARNINGS:** PRE-02 (branch), PRE-04 (markers), VER-04 (lint), VER-05 (format changes), DEP-OUT (outdated), SEM-01 (semver mismatch)

## Recovery

| Situation | Recovery |
|-----------|----------|
| Wrong version | Edit version before tagging |
| Changelog wrong | Edit CHANGELOG.md before commit |
| Tests/build failed | Fix and re-run preflight |
