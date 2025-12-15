---
name: cco-preflight
description: Pre-release checks and workflow
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-preflight

**Release Workflow** - Pre-flight → quality → cleanliness → review → verify → go/no-go.

Meta command that orchestrates other CCO commands for release preparation.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Version: !`for f in pyproject.toml package.json setup.py; do test -f "$f" && grep -E "version|__version__|VERSION" "$f"; done | head -1`
- Branch: !`git branch --show-current`
- Changelog: !`test -f CHANGELOG.md && head -20 CHANGELOG.md || echo "No CHANGELOG.md"`
- Git status: !`git status --short`
- Last tag: !`git describe --tags --abbrev=0 || echo "No tags"`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Architecture

| Step | Name | Action |
|------|------|--------|
| 1 | Phase Select | Ask which phases to run |
| 2 | Pre-flight | Release-specific checks |
| 3 | Quality | Run /cco-optimize --pre-release |
| 4 | Architecture | Run /cco-review --quick |
| 5 | Verification | Full test/build/lint |
| 6 | Changelog | Update changelog & docs |
| 7 | Decision | Go/No-go summary |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select phases", status: "in_progress", activeForm: "Selecting phases" },
  { content: "Step-2: Run pre-flight checks", status: "pending", activeForm: "Running pre-flight checks" },
  { content: "Step-3: Run quality gate", status: "pending", activeForm: "Running quality gate" },
  { content: "Step-4: Review architecture", status: "pending", activeForm: "Reviewing architecture" },
  { content: "Step-5: Run verification", status: "pending", activeForm: "Running verification" },
  { content: "Step-6: Update changelog", status: "pending", activeForm: "Updating changelog" },
  { content: "Step-7: Show go/no-go", status: "pending", activeForm: "Showing go/no-go decision" }
])
```

---

## Step-1: Phase Selection

```javascript
AskUserQuestion([{
  question: "Which phases to run?",
  header: "Phases",
  options: [
    { label: "Verification", description: "Pre-flight + final verification (Steps 2, 5)" },
    { label: "Quality", description: "Full quality gate (Step 3)" },
    { label: "Architecture", description: "Architecture review (Step 4)" },
    { label: "Changelog & Docs", description: "Release notes + docs sync (Step 6)" }
  ],
  multiSelect: true
}])
```

**Dynamic labels:** Add `(Recommended)` based on project priority and recent changes.

**Default:** All phases selected.

### Validation
```
[x] User selected phase(s)
→ Store as: phases = {selections[]}
→ Map phases to steps to skip
→ Proceed to Step-2
```

---

## Step-2: Pre-flight Checks [SKIP if "Verification" not selected]

### Step-2.1: Git State [BLOCKER]

| Check | Action |
|-------|--------|
| Clean working directory | BLOCK if dirty |
| On `{main_branch}` or release branch | WARN if not |

### Step-2.2: Version Sync [BLOCKER]

```bash
grep "{version_pattern}" {version_file}   # e.g., __version__, version
grep "version" {manifest_file}            # e.g., pyproject.toml, package.json
grep "^\[" {changelog_file} | head -1     # e.g., CHANGELOG.md
```

All must match. BLOCK if mismatch.

### Step-2.3: Leftover Markers [WARN]

```bash
grep -rn "TODO\|FIXME\|WIP\|HACK\|XXX" {src_dir}/ --include="*.{ext}"
grep -rn "Experimental\|DRAFT\|PLACEHOLDER" {docs_dir}/
```

WARN if found.

### Step-2.4: SemVer Review [WARN]

| Bump | Allowed Changes |
|------|-----------------|
| PATCH (x.x.1) | Fixes only |
| MINOR (x.1.0) | New features |
| MAJOR (1.0.0) | Breaking changes |

WARN if changes don't match version bump.

### Validation
```
[x] Git state clean (or user acknowledged)
[x] Version synced
[x] Markers checked
[x] SemVer reviewed
→ Store as: preflight = { blockers: [], warnings: [] }
→ Proceed to Step-3
```

---

## Step-3: Quality Gate [SKIP if "Quality" not selected]

Orchestrates: `/cco-optimize --pre-release --fix`

Runs all scopes with strict settings.

### Validation
```
[x] Quality gate completed
→ Store as: qualityResults = { fixed, declined, total }
→ Proceed to Step-4
```

---

## Step-4: Architecture Review [SKIP if "Architecture" not selected]

Orchestrates: `/cco-review --quick`

Gap analysis, DX review, what's working.

### Validation
```
[x] Architecture review completed
→ Store as: archResults = { issues, recommendations }
→ Proceed to Step-5
```

---

## Step-5: Final Verification [SKIP if "Verification" not selected]

| Check | Command | Blocker? |
|-------|---------|----------|
| Full test suite | `{test_command}` | YES |
| Build | `{build_command}` | YES |
| Lint | `{lint_command}` | YES |
| Type check | `{type_command}` | YES |

*Commands from context.md Operational section.*

### Validation
```
[x] All verification checks passed
→ Store as: verification = { passed: true/false, failures: [] }
→ Proceed to Step-6
```

---

## Step-6: Changelog & Docs [SKIP if "Changelog & Docs" not selected]

### Step-6.1: Generate Changelog

```bash
git log {last_tag}..HEAD --oneline
```

Classify commits:
| Type | Detection | Section |
|------|-----------|---------|
| Breaking | `BREAKING:`, API removal | Breaking |
| Added | `feat:`, new files | Added |
| Changed | `refactor:`, `perf:` | Changed |
| Fixed | `fix:` | Fixed |
| Removed | Deleted files | Removed |
| Security | `security:`, CVE | Security |

### Step-6.2: Version Suggestion

```
1. Check current version
2. Scan commits since last tag:
   - BREAKING: → MAJOR
   - feat: → MINOR
   - fix: only → PATCH
3. Suggest: {current} → {suggested} ({reason})
```

### Step-6.3: Docs Sync Check

| Feature | Check |
|---------|-------|
| New features | `{readme_file}` coverage |
| API changes | API docs updated |
| Config changes | Config docs updated |
| Breaking | Migration guide exists |

### Step-6.4: Apply Updates

```javascript
AskUserQuestion([{
  question: "Apply documentation updates?",
  header: "Docs",
  options: [
    { label: "Apply all", description: "Update CHANGELOG and docs" },
    { label: "Review each", description: "Show each change for approval" },
    { label: "Skip", description: "Don't update documentation" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Changelog generated
[x] Version suggestion made
[x] Docs sync checked
[x] Updates applied (or skipped)
→ Proceed to Step-7
```

---

## Step-7: Go/No-Go Decision

Display summary:
- Version: {current} → {suggested}
- Branch: {branch}
- Previous: {last_tag}
- Blockers: {count} (red)
- Warnings: {count} (yellow)
- Ready: YES/NO

```javascript
AskUserQuestion([{
  question: "Release decision?",
  header: "Decision",
  options: [
    { label: "Proceed", description: "Create tag and continue release" },
    { label: "Fix warnings", description: "Address warnings before release" },
    { label: "Abort", description: "Cancel release process" }
  ],
  multiSelect: false
}])
```

### If Proceed with Warnings

```javascript
AskUserQuestion([{
  question: "Release has {n} warnings. Confirm proceed?",
  header: "Confirm",
  options: [
    { label: "Yes, proceed anyway", description: "Release despite warnings" },
    { label: "No, fix first", description: "Go back and fix warnings" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Decision displayed
[x] User made decision
→ If Proceed: Show next steps (git tag, git push --tags, publish)
→ Done
```

---

## Reference

### Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Check without fixing |
| `--strict` | Treat warnings as blockers |
| `--skip-tests` | Skip test suite |
| `--tag` | Create git tag |
| `--push` | Push to remote |
| `--changelog` | CHANGELOG only |
| `--docs` | Documentation only |
| `--skip-docs` | Skip changelog & docs |

### Go/No-Go Status

| Status | Action |
|--------|--------|
| Blocker (red) | Cannot release |
| Warning (yellow) | Can override |
| Pass (green) | Ready |

---

## Rules

1. **Sequential execution** - Complete each step before proceeding
2. **Validation gates** - Check validation block before next step
3. **Git safety** - Clean state, version sync, no force push
4. **Delegate to sub-commands** - Don't duplicate /cco-optimize or /cco-review logic
5. **User decision required** - No release without explicit approval
