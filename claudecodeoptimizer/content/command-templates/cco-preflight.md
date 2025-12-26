---
name: cco-preflight
description: Pre-release checks and workflow
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-preflight

**Release Workflow** - Parallel pre-flight checks with single decision question.

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
| 1 | Pre-flight | Release checks (parallel) | Background |
| 2 | Quality + Review | Parallel: optimize + review | Background |
| 3 | Verification | Background: test/build/lint | Background |
| 4 | Changelog | Generate + suggest version | While tests run |
| 5 | Decision | Q1: Docs + Release decision | Single question |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Run pre-flight checks", status: "in_progress", activeForm: "Running pre-flight" },
  { content: "Step-2: Run quality + review", status: "pending", activeForm: "Running quality and review" },
  { content: "Step-3: Run verification", status: "pending", activeForm: "Running verification" },
  { content: "Step-4: Generate changelog", status: "pending", activeForm: "Generating changelog" },
  { content: "Step-5: Get release decision", status: "pending", activeForm: "Getting decision" }
])
```

---

## Step-1: Pre-flight Checks [PARALLEL]

**All checks run in parallel, no questions:**

### 1.1: Git State [BLOCKER]

```javascript
// Check from context
if (gitStatus.trim().length > 0) {
  blockers.push({
    type: "GIT_DIRTY",
    message: "Working directory has uncommitted changes"
  })
}

if (!branch.match(/^(main|master|release\/.*)$/)) {
  warnings.push({
    type: "BRANCH",
    message: `On branch '${branch}' - expected main/master or release/*`
  })
}
```

### 1.2: Version Sync [BLOCKER]

```javascript
// Extract versions from context
manifestVersion = extractVersion(versionContext)
changelogVersion = extractChangelogVersion(changelog)

if (manifestVersion !== changelogVersion) {
  blockers.push({
    type: "VERSION_MISMATCH",
    message: `Manifest: ${manifestVersion}, Changelog: ${changelogVersion}`
  })
}
```

### 1.3: Leftover Markers [WARN]

```javascript
// Check for leftover code markers (TODO, FIXME, XXX, HACK)
// Language-agnostic: search all text files, exclude binaries and generated
markersTask = Bash("grep -rn 'TODO\\|FIXME\\|XXX\\|HACK' --exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=vendor --exclude-dir=dist --exclude-dir=build --exclude='*.min.*' . 2>/dev/null || true")
```

### 1.4: SemVer Review [WARN]

```javascript
// Analyze commits since last tag
commitsTask = Bash(`git log ${lastTag}..HEAD --oneline`)

// Determine expected bump
// BREAKING: in commits → MAJOR
// feat: in commits → MINOR
// fix: only → PATCH
```

### 1.5: Dependency Audit [BLOCKER if security]

```javascript
// Check for outdated dependencies and security advisories
depTask = Task("cco-agent-research", `
  scope: dependency

  Pre-release dependency audit:
  1. Read manifest files (pyproject.toml, package.json, Cargo.toml, go.mod)
  2. Check each dependency for latest stable version
  3. Check for known security advisories (CVEs)

  Return: {
    outdated: [{ package, current, latest, updateType, breaking }],
    security: [{ package, advisory, severity, cve }],
    summary: { total, outdated, security }
  }
`, { model: "haiku", run_in_background: true })
```

**Security advisories are BLOCKERS.** Outdated packages are warnings (can release but noted).

### Validation
```
[x] All pre-flight checks completed
→ Store as: preflight = { blockers, warnings }
→ Proceed to Step-2
```

---

## Step-2: Quality + Review [PARALLEL - BOTH IN ONE MESSAGE]

**CRITICAL:** Launch both Task calls in a SINGLE message for true parallelism:

```javascript
// Both calls MUST be in same message block

qualityTask = Task("general-purpose", `
  Execute /cco-optimize --pre-release --fix
  Return: {
    accounting: { done, declined, fail, total },
    blockers: [{ severity, title, location }]
  }
`, { run_in_background: true })

reviewTask = Task("general-purpose", `
  Execute /cco-review --quick --no-apply
  Return: {
    foundation: "SOUND|HAS ISSUES",
    metrics: { coupling, cohesion, complexity },
    doNow: [{ title, location }],
    issues: [{ severity, title, location }]
  }
`, { model: "haiku", run_in_background: true })
```

### Validation
```
[x] Both tasks launched in parallel
→ Results collected in Step-5
→ Proceed to Step-3
```

---

## Step-3: Verification [BACKGROUND]

**Start all verification in background:**

```javascript
// Commands from context.md Operational section
testTask = Bash("{test_command} 2>&1", { run_in_background: true })
buildTask = Bash("{build_command} 2>&1", { run_in_background: true })
lintTask = Bash("{lint_command} 2>&1", { run_in_background: true })

// Store task IDs
verificationTasks = {
  test: testTask.id,
  build: buildTask.id,
  lint: lintTask.id
}
```

### Validation
```
[x] Background tasks launched
→ Results collected in Step-5
→ Proceed to Step-4
```

---

## Step-4: Changelog [WHILE BACKGROUND RUNS]

**Generate changelog while tests run:**

### 4.1: Classify Commits

```javascript
commits = await TaskOutput(commitsTask.id)

classified = {
  breaking: commits.filter(c => c.match(/BREAKING/i)),
  added: commits.filter(c => c.match(/^feat:/)),
  changed: commits.filter(c => c.match(/^(refactor|perf):/)),
  fixed: commits.filter(c => c.match(/^fix:/)),
  security: commits.filter(c => c.match(/^security:/i))
}
```

### 4.2: Suggest Version

```javascript
if (classified.breaking.length > 0) {
  suggestedBump = "MAJOR"
} else if (classified.added.length > 0) {
  suggestedBump = "MINOR"
} else {
  suggestedBump = "PATCH"
}

suggestedVersion = calculateNextVersion(manifestVersion, suggestedBump)
```

### 4.3: Generate Changelog Entry

```javascript
changelogEntry = generateChangelogEntry(classified, suggestedVersion)
```

### Validation
```
[x] Commits classified
[x] Version suggested
[x] Changelog entry generated
→ Proceed to Step-5
```

---

## Step-5: Decision [Q1 - ALL RESULTS]

**Wait for all background tasks, then ask single decision question:**

```javascript
// Collect all background results
qualityResults = await TaskOutput(qualityTask.id)
reviewResults = await TaskOutput(reviewTask.id)
testResults = await TaskOutput(verificationTasks.test)
buildResults = await TaskOutput(verificationTasks.build)
lintResults = await TaskOutput(verificationTasks.lint)
depResults = await TaskOutput(depTask.id)

// Aggregate blockers and warnings
allBlockers = [
  ...preflight.blockers,
  ...(qualityResults.blockers || []),
  ...(testResults.exitCode !== 0 ? [{ type: "TESTS", message: "Tests failed" }] : []),
  ...(buildResults.exitCode !== 0 ? [{ type: "BUILD", message: "Build failed" }] : []),
  // Security advisories are blockers
  ...(depResults.security || []).map(s => ({ type: "SECURITY", message: `${s.package}: ${s.advisory} (${s.cve})` }))
]

allWarnings = [
  ...preflight.warnings,
  ...(lintResults.exitCode !== 0 ? [{ type: "LINT", message: "Lint warnings" }] : []),
  ...(reviewResults.issues || []),
  // Outdated packages are warnings
  ...(depResults.outdated || []).map(d => ({ type: "OUTDATED", message: `${d.package}: ${d.current} → ${d.latest}` }))
]

hasBlockers = allBlockers.length > 0
```

**Display summary with blockers/warnings detail BEFORE decision:**

### Pre-Decision Display [MANDATORY]

```
## Release Readiness

| Metric | Value |
|--------|-------|
| Version | {manifestVersion} → {suggestedVersion} ({suggestedBump}) |
| Branch | {branch} |
| Previous | {lastTag} |

### Check Results
| Check | Status | Detail |
|-------|--------|--------|
| Pre-flight | {✓\|✗} | {detail or "OK"} |
| Quality | {✓\|✗} | Done {n}, Declined {n} |
| Architecture | {✓\|⚠️} | {foundation} |
| Tests | {✓\|✗} | {PASS\|FAIL: reason} |
| Build | {✓\|✗} | {PASS\|FAIL: reason} |
| Lint | {✓\|⚠️} | {PASS\|WARN: count} |
| Dependencies | {✓\|⚠️\|✗} | {depResults.summary.security > 0 ? "SECURITY" : depResults.summary.outdated > 0 ? `${depResults.summary.outdated} outdated` : "Up to date"} |

### Blockers (must fix)
| # | Type | Issue |
|---|------|-------|
| 1 | {type} | {message} |
...

### Warnings (can override)
| # | Type | Issue |
|---|------|-------|
| 1 | {type} | {message} |
...

Ready: {hasBlockers ? "NO" : "YES"}
```

**Ask combined decision question:**

```javascript
AskUserQuestion([
  {
    question: "Documentation updates to apply?",
    header: "Docs",
    options: [
      { label: "CHANGELOG (Recommended)", description: "Update CHANGELOG.md with new entry" },
      { label: "README", description: "Update README if needed" },
      { label: "API docs", description: "Regenerate API documentation" }
    ],
    multiSelect: true
  },
  {
    question: hasBlockers
      ? `Release has ${allBlockers.length} blocker(s). Decision?`
      : "All checks passed. Proceed with release?",
    header: "Decision",
    options: hasBlockers
      ? [
          { label: "Fix issues first (Recommended)", description: "Address blockers before release" },
          { label: "Abort release", description: "Cancel release process" }
        ]
      : [
          { label: "Proceed (Recommended)", description: "Create tag and continue release" },
          { label: "Fix issues first", description: "Address warnings before release" },
          { label: "Abort release", description: "Cancel release process" }
        ],
    multiSelect: false
  }
])
```

### If Proceed

```javascript
// Apply selected documentation updates
if (docsSelection.includes("CHANGELOG")) {
  Edit(changelogFile, changelogEntry)
}

// Show next steps
console.log(`
## Next Steps

1. Review changes: git diff
2. Commit: git commit -am "chore: prepare release ${suggestedVersion}"
3. Tag: git tag v${suggestedVersion}
4. Push: git push && git push --tags
`)
```

### Validation
```
[x] All background results collected
[x] Summary displayed
[x] User made decision
→ Done
```

---

## Reference

### Question Flow Summary

| Scenario | Questions |
|----------|-----------|
| Any preflight run | 1 (Docs + Decision combined) |

**Key optimization:** All pre-flight, quality, review, and verification run in parallel background. Single question at the end with all results.

### Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Check without fixing |
| `--strict` | Treat warnings as blockers |
| `--skip-tests` | Skip test suite |
| `--tag` | Create git tag after success |
| `--push` | Push to remote after success |
| `--changelog-only` | Only generate changelog |
| `--skip-docs` | Skip documentation updates |

### Go/No-Go Status

| Status | Meaning | Action |
|--------|---------|--------|
| Blocker (red) | Must fix | Cannot release |
| Warning (yellow) | Can override | User decides |
| Pass (green) | All clear | Ready to release |

### Model Strategy

| Task | Model | Reason |
|------|-------|--------|
| Quality (/cco-optimize) | Sonnet | Code modifications |
| Review (/cco-review) | Haiku | Read-only analysis |
| Verification | Bash | Direct execution |

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Wrong version suggested | Edit version manually before tagging |
| Changelog wrong | Edit CHANGELOG.md before commit |
| Tests failed | Fix tests, re-run preflight |
| Build failed | Fix build issues, re-run |

---

## Rules

1. **All parallel background** - Pre-flight, quality, review, verification, dependency audit all background
2. **Single question at end** - Docs + Decision combined after all results
3. **Collect before decision** - Wait for all background tasks before Q1
4. **Git safety** - Clean state required, version sync verified
5. **User decision required** - No release without explicit approval
6. **Security blocks release** - Dependency security advisories are blockers, not warnings
