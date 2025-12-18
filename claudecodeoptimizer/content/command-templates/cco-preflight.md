---
name: cco-preflight
description: Pre-release checks and workflow
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-preflight

**Release Workflow** - Parallel pre-flight checks with background verification.

Meta command orchestrating CCO commands with maximum parallelism.

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

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Phase Select | Ask which phases | Skip with flags |
| 2 | Pre-flight | Release-specific checks | Parallel checks |
| 3 | Quality + Review | Parallel: optimize + review | 2x faster |
| 4 | Verification | Background: test/build/lint | Non-blocking |
| 5 | Changelog | Generate + suggest version | While tests run |
| 6 | Decision | Go/No-go with all results | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select phases", status: "in_progress", activeForm: "Selecting phases" },
  { content: "Step-2: Run pre-flight checks", status: "pending", activeForm: "Running pre-flight checks" },
  { content: "Step-3: Quality + review (parallel)", status: "pending", activeForm: "Running quality and review" },
  { content: "Step-4: Verification (background)", status: "pending", activeForm: "Running verification" },
  { content: "Step-5: Changelog & docs", status: "pending", activeForm: "Updating changelog" },
  { content: "Step-6: Go/no-go decision", status: "pending", activeForm: "Showing go/no-go decision" }
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
grep "{version_pattern}" {version_file}     # e.g., __version__, version
grep "version" {manifest_file}              # e.g., pyproject.toml, package.json
grep "^\[" {changelog_file} | head -1       # e.g., CHANGELOG.md
```

All must match. BLOCK if mismatch.

### Step-2.3: Leftover Markers [WARN]

```bash
grep -rn "{marker_patterns}" {src_dir}/ --include="*.{extensions}"
grep -rn "{doc_markers}" {docs_dir}/
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

## Step-3: Quality + Review [PARALLEL]

**Launch optimize and review in a SINGLE message:**

```javascript
// CRITICAL: Both Task calls in ONE message for true parallelism

if (phases.includes("Quality")) {
  qualityTask = Task("general-purpose", `
    Execute /cco-optimize --pre-release --fix
    Return: { fixed, declined, total, blockers }
  `, { model: "sonnet", run_in_background: true })
}

if (phases.includes("Architecture")) {
  reviewTask = Task("general-purpose", `
    Execute /cco-review --quick --no-apply
    Return: { foundation, doNow, plan, issues }
  `, { model: "haiku", run_in_background: true })
}
```

**Parallel Execution:**
- Quality uses Sonnet (code modifications)
- Review uses Haiku (read-only analysis)
- Both complete while verification starts

### Validation
```
[x] Both tasks launched in parallel
[x] Results collected before Step-6
→ Start Step-4 immediately (don't wait)
```

---

## Step-4: Verification [BACKGROUND]

**Start all verification in background while changelog work proceeds:**

```javascript
// Launch all verifications in parallel background
// Commands from context.md Operational section
testTask = Bash("{test_command} 2>&1", { run_in_background: true })
buildTask = Bash("{build_command} 2>&1", { run_in_background: true })
lintTask = Bash("{lint_command} 2>&1", { run_in_background: true })

// Store task IDs for Step-6
verificationTasks = { test: testTask.id, build: buildTask.id, lint: lintTask.id }
```

**Background Pattern:**
- All verification runs while user reviews changelog
- Results collected before go/no-go decision
- Failed verification = blocker

### Validation
```
[x] Background tasks launched
[x] Task IDs stored for Step-6
→ Proceed to Step-5 immediately (don't wait)
```

---

## Step-5: Changelog & Docs [WHILE VERIFICATION RUNS]

**Generate changelog while tests run in background:**

### 5.1: Generate Changelog

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
| Security | `security:`, CVE | Security |

### 5.2: Version Suggestion

```
Scan commits since last tag:
- BREAKING: → MAJOR bump
- feat: → MINOR bump
- fix: only → PATCH bump
Suggest: {current} → {suggested} ({reason})
```

### 5.3: Apply Updates

```javascript
AskUserQuestion([{
  question: "Apply documentation updates?",
  header: "Docs",
  options: [
    { label: "Apply all (Recommended)", description: "Update CHANGELOG and docs" },
    { label: "Review each", description: "Show each change for approval" },
    { label: "Skip", description: "Don't update documentation" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Changelog generated
[x] Version suggested
[x] Updates applied (or skipped)
→ Proceed to Step-6
```

---

## Step-6: Go/No-Go Decision

**First: Collect all background results**

```javascript
// Wait for all background tasks
qualityResults = await TaskOutput(qualityTask.id)
reviewResults = await TaskOutput(reviewTask.id)
testResults = await TaskOutput(verificationTasks.test)
buildResults = await TaskOutput(verificationTasks.build)
lintResults = await TaskOutput(verificationTasks.lint)

// Aggregate blockers and warnings
blockers = [
  ...qualityResults.blockers,
  ...(testResults.failed ? ["Tests failed"] : []),
  ...(buildResults.failed ? ["Build failed"] : []),
  ...(lintResults.failed ? ["Lint failed"] : [])
]
warnings = [
  ...preflightResults.warnings,
  ...reviewResults.issues
]
```

**Display summary:**

```
## Release Readiness

Version: {current_version} → {suggested_version}
Branch: {branch}
Previous: {last_tag}

### Results
| Check | Status |
|-------|--------|
| Pre-flight | {status} |
| Quality | Fixed {n}, Declined {n} |
| Architecture | {foundation_status} |
| Tests | {status} |
| Build | {status} |
| Lint | {status} |

Blockers: {n} (must fix)
Warnings: {n} (can override)

Ready: {YES|NO}
```

```javascript
AskUserQuestion([{
  question: "Release decision?",
  header: "Decision",
  options: [
    { label: "Proceed", description: "Create tag and continue release" },
    { label: "Fix issues", description: "Address blockers/warnings first" },
    { label: "Abort", description: "Cancel release process" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] All background results collected
[x] Summary displayed
[x] User made decision
→ If Proceed: Show next steps (git tag, git push --tags)
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

1. **Parallel sub-commands** - Launch quality + review in single message
2. **Background verification** - Tests/build/lint run while user works
3. **Collect before decision** - Wait for all results at Step-6
4. **Git safety** - Clean state, version sync, no force push
5. **User decision required** - No release without explicit approval
