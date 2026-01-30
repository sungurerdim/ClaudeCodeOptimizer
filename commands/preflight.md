---
description: Release verification gate - full optimization + review + tests + build
argument-hint: "[--auto] [--preview]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
model: opus
---

# /cco:preflight

**Release Verification Gate** - Comprehensive pre-release checks with parallel orchestration.

> **Implementation Note:** Code blocks use JavaScript-like pseudocode for clarity. Actual execution uses Claude Code tools with appropriate parameters.

Meta command orchestrating /cco:optimize and /cco:align with maximum parallelism.

**Orchestration:**
```
PREFLIGHT
    |
    +-- [Q1: Fix Intensity] ─────────────────┐
    |                                        │
    +-- [Pre-flight Checks] PARALLEL ────────┤
    |       Git state, version sync,         │
    |       markers, semver, dependencies    │
    |                                        │
    +-- [Sub-commands] PARALLEL ─────────────┤
    |       |                                │
    |       +-- /cco:optimize --auto             │
    |       |   (all 10 scopes, 105 checks)  │
    |       |                                │
    |       +-- /cco:align --auto                │
    |           (all 6 scopes, 77 checks)    │
    |                                        │
    +-- [Verification] PARALLEL ─────────────┤
    |       format, lint, type, test, build  │
    |                                        │
    +-- [Changelog] ─────────────────────────┘
            Commit classification, version

    ↓ (Wait for all)

    [Plan Review] (conditional)
        Combined release plan + reasoning

    ↓

    [Q2: Decision]
        Proceed / Fix Issues / Abort
```

**Plan Review is MANDATORY when findings > 0 or blockers detected.**

**Skipped when:** `--auto` mode or 0 findings + 0 blockers

## Context

- Version: !`for f in pyproject.toml package.json setup.py; do test -f "$f" && grep -E "version|__version__|VERSION" "$f"; done | head -1`
- Branch: !`git branch --show-current`
- Changelog: !`test -f CHANGELOG.md && head -20 CHANGELOG.md || echo "No CHANGELOG.md"`
- Git status: !`git status --short`
- Last tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags"`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Profile Requirement [CRITICAL]

CCO profile is auto-loaded from `.claude/rules/cco-profile.md` via Claude Code's auto-context mechanism.

**Check:** Delegate to `/cco:tune --preview` for profile validation:

```javascript
// Delegate profile check to tune command
const tuneResult = await Skill("tune", "--preview")

if (tuneResult.status === "skipped") {
  // User declined setup - exit gracefully
  console.log("CCO setup skipped. Run /cco:tune when ready.")
  return
}

// Profile is now valid - continue with command
```

**After tune completes → continue to Step-0 (Mode Detection)**

---

## Mode Detection [CRITICAL]

```javascript
// --auto mode: unattended, full fix, no questions, minimal output
if (args.includes("--auto")) {
  config = {
    fixMode: "full-fix",          // All severities
    unattended: true
  }
  // Skip Q1, proceed directly to Step-1
}
```

**--auto use cases:** CI/CD pipelines, pre-commit hooks, scheduled cron jobs, IDE integrations (non-interactive)

---

## Architecture

| Phase | Step | Name | Action | Gate |
|-------|------|------|--------|------|
| **SETUP** | 0-1a | Config | Mode + Q1: Settings | Config validated |
| **PRE-CHECK** | 1b | Verify | Git, version, deps (parallel) | Pre-checks done |
| **GATE-1** | - | Checkpoint | No blocking pre-checks | → Sub-commands |
| **OPTIMIZE** | 2a | Fix | /cco:optimize (parallel) | Fixes applied |
| **ALIGN** | 2b | Arch | /cco:align (parallel) | Changes applied |
| **VERIFY** | 3 | Test | test/build/lint (parallel) | Tests pass |
| **GATE-2** | - | Checkpoint | All parallel complete | → Changelog |
| **CHANGELOG** | 4 | Version | Generate + suggest | Entry ready |
| **GATE-3** | - | Checkpoint | Blockers evaluated | → Plan or Release |
| **PLAN** | 4.5 | Review | Combined plan (conditional) | User approval |
| **GATE-4** | - | Checkpoint | Approval received | → Execute |
| **RELEASE** | 5 | Execute | Tag/commit based on mode | Done |

**Execution Flow:** SETUP → PRE-CHECK → GATE-1 → (OPTIMIZE ‖ ALIGN ‖ VERIFY) → GATE-2 → CHANGELOG → GATE-3 → [PLAN if triggered] → GATE-4 → RELEASE

### Phase Gates

```javascript
// GATE-1: Post Pre-checks
function gate1_postPrechecks(prechecks) {
  const blockers = prechecks.filter(p => p.type === "BLOCKER" && !p.resolved)
  if (blockers.length > 0 && !config.unattended) {
    return { pass: false, blockers, reason: "Pre-check blockers" }
  }
  return { pass: true, warnings: prechecks.filter(p => p.type === "WARN") }
}

// GATE-2: Post Parallel Execution
function gate2_postParallel(optimize, align, verify) {
  const allComplete = optimize.done && align.done && verify.done
  if (!allComplete) throw new Error("Parallel execution incomplete")
  return {
    pass: true,
    optimizeApplied: optimize.applied,
    alignApplied: align.applied,
    testsPass: verify.test.exitCode === 0
  }
}

// GATE-3: Blocker Evaluation
function gate3_blockerEval(allBlockers, allWarnings) {
  return {
    pass: allBlockers.length === 0,
    blockers: allBlockers,
    warnings: allWarnings,
    canProceed: allBlockers.length === 0
  }
}

// GATE-4: Post-Plan (or skip)
function gate4_postPlan(planResult, skipPlan) {
  if (skipPlan) return { pass: true, reason: "Plan skipped" }
  if (["Abort", "Fix and Retry"].includes(planResult)) {
    return { pass: false, reason: planResult }
  }
  return { pass: true, mode: planResult }
}
```

**Single question at start** - All settings collected upfront, then uninterrupted flow (unless plan mode).

---

## Everything Mode [CRITICAL]

When `--auto` or user selects "Full Fix":
- Pass to both `/cco:optimize --auto` and `/cco:align --auto`
- **Zero commentary** - No "this is complex", "needs refactor", "minor detail", "consider later"
- **Zero deferrals** - No "future iteration", "lower priority", "recommend manual"
- **Zero skips** - Every finding fixed NOW, no exceptions
- **Only technical failures** - File not found, parse error, permission denied
- Final accounting: `applied + failed = total` (no AI declines allowed)

**See Core Rules:** `No Deferrals Policy` for forbidden responses and valid failure reasons.

---

## Step-1a: Settings Selection [Q1]

**Skip if --auto mode (config already set)**

```javascript
if (!isUnattended) {
  AskUserQuestion([
  {
    question: "Which checks to run?",
    header: "Checks",
    options: [
      { label: "Security (Recommended)", description: "Vulnerabilities, secrets, dependencies" },
      { label: "Code Quality (Recommended)", description: "Types, lint, hygiene" },
      { label: "Architecture", description: "Patterns, structure, maintainability" },
      { label: "Tests + Build", description: "Run test suite and build" }
    ],
    multiSelect: true
  },
  {
    question: "How thorough?",
    header: "Intensity",
    options: [
      { label: "Quick", description: "Fast - high impact only" },
      { label: "Standard (Recommended)", description: "CRITICAL + HIGH + MEDIUM" },
      { label: "Full", description: "All severities" }
    ],
    multiSelect: false
  },
  {
    question: "After checks pass?",
    header: "Release",
    options: [
      { label: "Fix Only (Recommended)", description: "Apply fixes, no tag, no commit" },
      { label: "Fix + Commit + Tag", description: "Apply fixes, commit, create git tag" }
    ],
    multiSelect: false
  }
  ])
}
```

### Settings Mapping

| Selection | Effect |
|-----------|--------|
| **Intensity** | Passed to /cco:optimize and /cco:align |
| **Fix Only** | Apply fixes only, no commit, no tag |
| **Fix + Commit + Tag** | Apply fixes, create commit, create git tag |
| **CHANGELOG** | Generate changelog entry |
| **Skip docs** | No doc updates |

### Validation
```
[x] User completed Q1 (all settings)
→ Store as: config = { fixMode, releaseMode, docs }
→ Proceed to Step-1b
```

---

## Step-1b: Pre-flight Checks [PARALLEL BACKGROUND]

**All checks run in parallel background, no questions:**

### 1.1: Git State [BLOCKER]

```javascript
// Check from context
if (gitStatus.trim().length > 0) {
  blockers.push({
    id: "PRE-01",
    type: "GIT_DIRTY",
    message: "Working directory has uncommitted changes"
  })
}

if (!branch.match(/^(main|master|release\/.*)$/)) {
  warnings.push({
    id: "PRE-02",
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
    id: "PRE-03",
    type: "VERSION_MISMATCH",
    message: `Manifest: ${manifestVersion}, Changelog: ${changelogVersion}`
  })
}
```

### 1.3: Leftover Markers [WARN]

```javascript
// Check for leftover code markers
markersTask = Bash("grep -rn 'TODO\\|FIXME\\|XXX\\|HACK' --exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=vendor --exclude-dir=dist --exclude-dir=build --exclude='*.min.*' . 2>/dev/null | head -20 || true", { run_in_background: true })
```

### 1.4: SemVer Review [WARN]

```javascript
// Analyze commits since last tag
commitsTask = Bash(`git log ${lastTag}..HEAD --oneline 2>/dev/null || git log --oneline -20`, { run_in_background: true })
```

### 1.5: Dependency Audit [BLOCKER if security]

```javascript
depResults = Task("cco-agent-research", `
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
`, { model: "haiku" })  // Synchronous - Task returns results directly
// NOTE: Do NOT use run_in_background for Task (agent) calls
```

**Security advisories are BLOCKERS.** Outdated packages are warnings.

### Validation
```
[x] All pre-flight checks launched
→ Store task IDs for later collection
→ Proceed to Step-2
```

---

## Step-2: Optimize + Review [PARALLEL - BOTH IN ONE MESSAGE]

**CRITICAL:** Launch both Task calls in a SINGLE message for true parallelism:

```javascript
// BOTH calls in same message for parallel execution
// Task tool executes multiple calls in parallel when in same message
// Synchronous - each Task returns results directly
// --auto skips plan review in sub-commands (preflight has its own plan review at Step-4.5)
optimizeResults = Task("general-purpose", `
  Execute /cco:optimize --auto

  CRITICAL: Run ALL 10 scopes (security, hygiene, types, lint, performance, ai-hygiene, robustness, privacy, doc-sync, simplify)
  Fix ALL items. Effort categories are for reporting only, not filtering.

  Return: {
    accounting: { applied, failed, total },
    scopes: { security, hygiene, types, lint, performance, "ai-hygiene", robustness, privacy, "doc-sync", simplify }
  }
`, { model: "opus" })  // Synchronous - no run_in_background for Task

reviewResults = Task("general-purpose", `
  Execute /cco:align --auto

  CRITICAL: Run ALL 6 scopes (architecture, patterns, testing, maintainability, ai-architecture, functional-completeness)
  Fix ALL items. Effort categories are for reporting only, not filtering.

  Return: {
    gaps: { coupling, cohesion, complexity, coverage },
    accounting: { applied, failed, total },
    effortCategories: { quickWin, moderate, complex, major }
  }
`, { model: "opus" })  // Synchronous - no run_in_background for Task
```

### Validation
```
[x] Both tasks launched in parallel
→ Results collected in Step-5
→ Proceed to Step-3
```

---

## Step-3: Verification [BACKGROUND]

> **Pattern:** Quality Gates run external tools. Preflight runs full verification including
> build command (unique to release). Unlike /cco:commit (conditional on changed files),
> preflight runs comprehensive release verification on full project.

**Start all verification in background (full project):**

```javascript
// Commands from profile (detected by /cco:tune) - FULL PROJECT
formatTask = Bash("{format_command} 2>&1", { run_in_background: true })
lintTask = Bash("{lint_command} 2>&1", { run_in_background: true })
typeTask = Bash("{type_command} 2>&1", { run_in_background: true })
testTask = Bash("{test_command} 2>&1", { run_in_background: true })
buildTask = Bash("{build_command} 2>&1", { run_in_background: true })

// Store task IDs
verificationTasks = {
  format: formatTask.id,
  lint: lintTask.id,
  type: typeTask.id,
  test: testTask.id,
  build: buildTask.id
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
→ Check Plan Review triggers → Step-4.5 or Step-5
```

---

## Step-4.5: Plan Review [CONDITIONAL]

**"Think before you release"** - Consolidated view of all changes before release.

### Trigger Conditions

```javascript
// Determine if Plan Review is needed
const totalFixes = optimizeResults.accounting.total + reviewResults.accounting.total
const hasBlockers = allBlockers.length > 0
const hasBreaking = classified.breaking.length > 0

const planMode = (totalFixes > 0) || hasBlockers

// Skip in --auto mode
const skipPlan = isUnattended

if (planMode && !skipPlan) {
  // → Enter Plan Review
} else {
  // → Skip to Step-5
}
```

### Release Plan Display

```markdown
## Release Plan Review

**Version:** {manifestVersion} → {suggestedVersion} ({suggestedBump})
**Branch:** {branch} | **Previous:** {lastTag}

> This is a consolidated view of all changes before release. Review carefully.

### Pre-flight Status

| Check | Status | Detail |
|-------|--------|--------|
| Git State | {gitClean ? "Clean" : "Dirty"} | {gitDetail} |
| Version Sync | {versionMatch ? "Match" : "Mismatch"} | {versionDetail} |
| Dependencies | {depSecure ? "Secure" : "Vulnerabilities"} | {depDetail} |

### Sub-command Results Summary

| Command | Applied | Failed | Key Changes |
|---------|---------|--------|-------------|
| /cco:optimize | {optimizeResults.accounting.applied} | {optimizeResults.accounting.failed} | {optimizeKeyChanges} |
| /cco:align | {reviewResults.accounting.applied} | {reviewResults.accounting.failed} | {alignKeyChanges} |
| **Total** | **{totalApplied}** | **{totalFailed}** | |

### Verification Results

| Gate | Status | Must Pass? |
|------|--------|------------|
| Tests | {testStatus} | Yes |
| Build | {buildStatus} | Yes |
| Types | {typeStatus} | Yes |
| Lint | {lintStatus} | No (warnings OK) |
| Format | {formatStatus} | No (auto-fixed) |

### Breaking Changes

{hasBreaking ? `
**⚠️ Breaking changes detected:**
${classified.breaking.map(c => `- ${c}`).join('\n')}

This will require a MAJOR version bump.
` : "No breaking changes detected."}

### Blockers

{hasBlockers ? `
**🛑 Blockers must be resolved:**
${allBlockers.map((b, i) => `${i+1}. [${b.type}] ${b.message}`).join('\n')}
` : "No blockers - ready to proceed."}

### Changelog Preview

\`\`\`markdown
${changelogEntry}
\`\`\`

### Release Checklist

- [${!hasBlockers ? 'x' : ' '}] No blockers
- [${testResults.exitCode === 0 ? 'x' : ' '}] Tests passing
- [${buildResults.exitCode === 0 ? 'x' : ' '}] Build successful
- [${versionMatch ? 'x' : ' '}] Version synced
- [${!hasBreaking || suggestedBump === 'MAJOR' ? 'x' : ' '}] Breaking changes versioned correctly
```

### User Decision

```javascript
if (hasBlockers) {
  AskUserQuestion([{
    question: "Blockers detected. How to proceed?",
    header: "Decision",
    options: [
      { label: "Fix and Retry", description: "Address blockers, then re-run preflight" },
      { label: "View Details", description: "Show detailed blocker information" },
      { label: "Abort", description: "Cancel release" }
    ],
    multiSelect: false
  }])
} else {
  AskUserQuestion([{
    question: "Release plan review complete. Proceed with release?",
    header: "Decision",
    options: [
      { label: "Proceed (Recommended)", description: `Create tag v${suggestedVersion}` },
      { label: "Review Changes", description: "Show git diff before proceeding" },
      { label: "Abort", description: "Cancel - no tag created" }
    ],
    multiSelect: false
  }])
}

switch (planDecision) {
  case "Proceed":
    config.releaseMode = "tag"
    break
  case "Review Changes":
    Bash("git diff --stat")
    // Re-prompt after review
    break
  case "Fix and Retry":
  case "Abort":
    console.log("Release aborted. Fix issues and re-run /cco:preflight.")
    return
}
```

### Validation
```
[x] Release plan displayed
[x] All results consolidated
[x] User decision captured
→ If Abort/Fix: Exit
→ Proceed to Step-5 with config.releaseMode
```

---

## Step-5: Results + Execute

**Collect Bash background results, then show summary and execute based on Q1 settings:**

```javascript
// Task (agent) results already collected in previous steps (synchronous)
// Only Bash background results need TaskOutput

// Bash background results (TaskOutput works correctly for Bash)
formatResults = await TaskOutput(verificationTasks.format)
lintResults = await TaskOutput(verificationTasks.lint)
typeResults = await TaskOutput(verificationTasks.type)
testResults = await TaskOutput(verificationTasks.test)
buildResults = await TaskOutput(verificationTasks.build)
markersResult = await TaskOutput(markersTask.id)
// Note: commitsTask already processed in Step-4

// NOTE: optimizeResults, reviewResults, depResults already set from synchronous Task calls

// Check if format made changes
formatChanged = formatResults.stdout?.includes("reformatted") || formatResults.stdout?.includes("fixed")

// Aggregate blockers and warnings
allBlockers = [
  ...preflight.blockers,
  ...(testResults.exitCode !== 0 ? [{ id: "VER-01", type: "TESTS", message: "Tests failed" }] : []),
  ...(buildResults.exitCode !== 0 ? [{ id: "VER-02", type: "BUILD", message: "Build failed" }] : []),
  ...(typeResults.exitCode !== 0 ? [{ id: "VER-03", type: "TYPES", message: "Type errors found" }] : []),
  ...(depResults.security || []).map(s => ({ id: "DEP-SEC", type: "SECURITY", message: `${s.package}: ${s.advisory} (${s.cve})` })),
  ...(optimizeResults.accounting?.failed > 0 && optimizeResults.blockers?.filter(b => b.severity === "CRITICAL") || [])
]

allWarnings = [
  ...preflight.warnings,
  ...(lintResults.exitCode !== 0 ? [{ id: "VER-04", type: "LINT", message: "Lint warnings" }] : []),
  ...(formatChanged ? [{ id: "VER-05", type: "FORMAT", message: "Files reformatted - review changes" }] : []),
  ...(markersResult.stdout?.trim() ? [{ id: "PRE-04", type: "MARKERS", message: "TODO/FIXME markers found" }] : []),
  ...(depResults.outdated || []).map(d => ({ id: "DEP-OUT", type: "OUTDATED", message: `${d.package}: ${d.current} → ${d.latest}` }))
]

hasBlockers = allBlockers.length > 0

// Calculate combined accounting
totalApplied = (optimizeResults.accounting?.applied || 0) + (reviewResults.accounting?.applied || 0)
totalFailed = (optimizeResults.accounting?.failed || 0) + (reviewResults.accounting?.failed || 0)
totalFindings = totalApplied + totalFailed
```

### Results Display [MANDATORY]

```markdown
## Release Readiness

| Metric | Value |
|--------|-------|
| Version | {manifestVersion} → {suggestedVersion} ({suggestedBump}) |
| Branch | {branch} |
| Previous | {lastTag} |
| Fix Mode | {config.fixMode} |
| Release Mode | {config.releaseMode} |

### Sub-command Results
| Command | Applied | Failed | Total |
|---------|---------|--------|-------|
| /cco:optimize | {optimizeResults.accounting.applied} | {optimizeResults.accounting.failed} | {optimizeResults.accounting.total} |
| /cco:align | {reviewResults.accounting.applied} | {reviewResults.accounting.failed} | {reviewResults.accounting.total} |
| **Combined** | **{totalApplied}** | **{totalFailed}** | **{totalFindings}** |

### Verification Results
| Check | Status | Detail |
|-------|--------|--------|
| Pre-flight | {preflight.blockers.length === 0 ? "PASS" : "FAIL"} | {detail} |
| Tests | {testResults.exitCode === 0 ? "PASS" : "FAIL"} | {detail} |
| Build | {buildResults.exitCode === 0 ? "PASS" : "FAIL"} | {detail} |
| Types | {typeResults.exitCode === 0 ? "PASS" : "FAIL"} | {detail} |
| Lint | {lintResults.exitCode === 0 ? "PASS" : "WARN"} | {detail} |
| Dependencies | {depResults.summary.security > 0 ? "FAIL" : "PASS"} | {depResults.summary.security} security, {depResults.summary.outdated} outdated |

### Blockers
{allBlockers.length === 0 ? "None - ready to release!" : allBlockers.map((b, i) => `${i+1}. [${b.type}] ${b.message}`).join('\n')}

### Warnings
{allWarnings.length === 0 ? "None" : allWarnings.map((w, i) => `${i+1}. [${w.type}] ${w.message}`).join('\n')}

**Release Ready:** {hasBlockers ? "NO - blockers must be fixed" : "YES"}
```

### Output Schema [STANDARD ENVELOPE]

**All CCO commands use same envelope.**

```json
{
  "status": "OK|WARN|BLOCKED",
  "summary": "Applied 8, Blockers 0, Version v1.2.0",
  "data": {
    "accounting": { "applied": 8, "failed": 0, "total": 8 },
    "optimize": { "applied": 5, "failed": 0 },
    "align": { "applied": 3, "failed": 0 },
    "blockers": [],
    "warnings": ["PRE-04: TODO markers found"],
    "version": { "current": "1.1.0", "suggested": "1.2.0", "bump": "MINOR" }
  },
  "error": null
}
```

**Status rules:**
- `OK`: blockers = 0, tests pass, build pass
- `WARN`: blockers = 0 but warnings > 0
- `BLOCKED`: blockers > 0 OR tests fail OR build fail

**--auto mode:** Prints `summary` field only.
Exit code: 0 (OK), 1 (WARN), 2 (BLOCKED)

### Execute Release Mode (from Q1)

```javascript
// Apply documentation updates (selected in Q1)
if (config.docs.includes("CHANGELOG")) {
  Edit(changelogFile, changelogEntry)
}

// Execute release action based on Q1 selection
if (hasBlockers) {
  console.log(`
## Blocked

${allBlockers.length} blocker(s) must be fixed before release.
Run \`git diff\` to review changes, fix blockers, and re-run preflight.
`)
} else if (config.releaseMode === "Fix Only") {
  console.log(`
## Fixes Applied

All checks passed. Fixes have been applied.

**Next Steps:**
1. Review changes: \`git diff\`
2. Commit: \`git commit -am "chore: apply fixes"\`
3. Push when ready: \`git push\`
`)
} else if (config.releaseMode === "tag" || config.releaseMode === "Create Tag") {
  Bash(`git commit -am "chore: release ${suggestedVersion}" && git tag v${suggestedVersion}`)
  console.log(`
## Tagged

Version ${suggestedVersion} has been tagged.

**Next Steps:**
1. Review: \`git log --oneline -3\`
2. Push when ready: \`git push && git push --tags\`
`)
}
```

### Final Summary

```markdown
## Preflight Complete

Status: {hasBlockers ? "BLOCKED" : (allWarnings.length > 0 ? "WARN" : "OK")} | Applied: {totalApplied} | Failed: {totalFailed} | Total: {totalFindings}

**Invariant:** applied + failed = total

Mode: {config.releaseMode}
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

| Scenario | Questions | Total |
|----------|-----------|-------|
| --auto mode | - | **0** |
| Interactive | Q1 (Intensity + Release Mode + Docs) | **1** |

**Single question at start** - All settings collected upfront, then uninterrupted parallel execution.

### Flags

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode: all scopes, all severities, no questions |
| `--preview` | Run all checks, show results, don't release |

### Release-Specific Checks (14 total)

**BLOCKERS (must fix):**
| ID | Check | Criteria |
|----|-------|----------|
| PRE-01 | Dirty git | Working directory has uncommitted changes |
| PRE-03 | Version mismatch | Manifest version != changelog version |
| VER-01 | Tests fail | Test suite exits non-zero |
| VER-02 | Build fail | Build command exits non-zero |
| VER-03 | Type errors | Type checker finds errors |
| DEP-SEC | Security CVE | Known vulnerability in dependency |
| OPT-CRIT | Optimize critical | Unfixed CRITICAL from /cco:optimize |
| REV-CRIT | Review critical | Unfixed CRITICAL gap from /cco:align |

**WARNINGS (can override):**
| ID | Check | Criteria |
|----|-------|----------|
| PRE-02 | Branch name | Not on main/master or release/* |
| PRE-04 | Markers | TODO/FIXME found in code |
| VER-04 | Lint warnings | Linter has warnings |
| VER-05 | Format changes | Formatter made changes |
| DEP-OUT | Outdated deps | Non-security outdated packages |
| SEM-01 | SemVer mismatch | Commits suggest different bump |

### Go/No-Go Status

| Status | Meaning | Action |
|--------|---------|--------|
| BLOCKED (red) | Has blockers | Cannot release - must fix |
| WARN (yellow) | Has warnings | User decides |
| OK (green) | All clear | Ready to release |

### Model Strategy

**Policy:** Opus + Haiku only (no Sonnet)

| Task | Model | Reason |
|------|-------|--------|
| /cco:optimize | Opus | Code modifications require accuracy |
| /cco:align | Opus | Architectural changes require accuracy |
| Dependency audit | Haiku | Read-only research |
| Verification | Bash | Direct execution |

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Wrong version suggested | Edit version manually before tagging |
| Changelog wrong | Edit CHANGELOG.md before commit |
| Tests failed | Fix tests, re-run preflight |
| Build failed | Fix build issues, re-run |
| Blockers remain | Run with --auto |

---

## Rules

1. **All settings upfront** - Intensity, release mode, and docs selected in single Q1
2. **All parallel background** - Pre-flight, optimize, review, verification all background
3. **Full scope** - Run ALL scopes for both optimize (10) and align (6)
4. **No mid-flow questions** - All decisions made at start, uninterrupted execution
5. **Git safety** - Clean state required, version sync verified
6. **Blockers stop release** - Cannot proceed with blockers regardless of release mode
7. **Security blocks release** - Dependency security advisories are always blockers

---

## Blocker Classification

### Self-Consistency (BLOCKER Decisions)
For blocker classification, validate with multiple perspectives:
```
Path A: "Does this pose risk to users/production?"
Path B: "Is this a development-time concern only?"
Consensus: Both agree risk → BLOCKER. Only dev concern → WARNING
```

**When uncertain → WARNING** (let user decide)

---

## Accounting

**Invariant:** `applied + failed = total` (count findings, not locations)

**No "declined" category:** AI has no option to decline fixes. If it's technically possible and user asked for it, it MUST be done. Only "failed" with specific technical reason is acceptable.

Combined from both sub-commands:
- totalApplied = optimize.applied + review.applied
- totalFailed = optimize.failed + review.failed
- totalFindings = totalApplied + totalFailed
