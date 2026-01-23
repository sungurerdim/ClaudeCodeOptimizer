---
description: Release verification gate - full optimization + review + tests + build
argument-hint: [--auto] [--intensity=X] [--dry-run] [--strict] [--tag] [--push]
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(*), Task(*), AskUserQuestion
model: opus
---

# /preflight

**Release Verification Gate** - Comprehensive pre-release checks with parallel orchestration.

Meta command orchestrating /optimize and /review with maximum parallelism.

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
    |       +-- /optimize --intensity=X  │
    |       |   (all 6 scopes)               │
    |       |                                │
    |       +-- /review --intensity=X    │
    |           (all 5 scopes)               │
    |                                        │
    +-- [Verification] PARALLEL ─────────────┤
    |       format, lint, type, test, build  │
    |                                        │
    +-- [Changelog] ─────────────────────────┘
            Commit classification, version

    ↓ (Wait for all)

    [Q2: Decision]
        Proceed / Fix Issues / Abort
```

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Version: !`for f in pyproject.toml package.json setup.py; do test -f "$f" && grep -E "version|__version__|VERSION" "$f"; done | head -1`
- Branch: !`git branch --show-current`
- Changelog: !`test -f CHANGELOG.md && head -20 CHANGELOG.md || echo "No CHANGELOG.md"`
- Git status: !`git status --short`
- Last tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags"`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /config first to configure project context, then restart CLI.
```
**Stop immediately.**

---

## Mode Detection [CRITICAL]

```javascript
// --auto mode: unattended, full fix, no questions, minimal output
if (args.includes("--auto")) {
  config = {
    intensity: "full-fix",        // All severities
    unattended: true
  }
  // Skip Q1, proceed directly to Step-1
}
```

**--auto use cases:** CI/CD pipelines, pre-commit hooks, scheduled cron jobs, IDE integrations (non-interactive)

---

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 0 | Mode | Detect --auto or interactive | Instant |
| 1a | Q1 | Fix Intensity selection | Single question |
| 1b | Pre-flight | Release checks (parallel background) | Background |
| 2 | Sub-commands | /optimize + /review (parallel) | Background |
| 3 | Verification | test/build/lint (parallel background) | Background |
| 4 | Changelog | Generate + suggest version | While tests run |
| 5 | Decision | Q2: Docs + Release decision | Single question |

---

## Everything Mode [CRITICAL]

When `--intensity=full-fix` or user selects "Full Fix":
- Pass to both `/optimize --intensity=full-fix` and `/review --intensity=full-fix`
- **Zero deferrals** - no "future iteration", no "lower priority"
- **Zero skips** - every finding fixed NOW
- Final accounting: `applied + failed = total` (no AI declines allowed)

---

## Step-1a: Fix Intensity Selection [Q1]

**Skip if --auto mode (config already set)**

```javascript
AskUserQuestion([
  {
    question: "What level of fixes for this release?",
    header: "Intensity",
    options: [
      { label: "Quick Wins (80/20)", description: "High impact, low effort only (fast release)" },
      { label: "Standard (Recommended)", description: "CRITICAL + HIGH + MEDIUM (comprehensive)" },
      { label: "Full Fix", description: "All severities including LOW (complete cleanup)" },
      { label: "Dry Run", description: "Check only, no fixes applied" }
    ],
    multiSelect: false
  }
])
```

### Intensity Mapping for Sub-commands

| Selection | Optimize Args | Review Args |
|-----------|---------------|-------------|
| Quick Wins (80/20) | `--intensity=quick-wins` | `--intensity=quick-wins` |
| Standard | `--intensity=standard` | `--intensity=standard` |
| Full Fix | `--intensity=full-fix` | `--intensity=full-fix` |
| Dry Run | `--intensity=report-only` | `--intensity=report-only` |

### Validation
```
[x] User completed Q1
→ Store as: config = { intensity }
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
// Map intensity to command args
const intensityFlag = `--intensity=${config.intensity}`

// BOTH calls MUST be in same message block for parallelism
optimizeTask = Task("general-purpose", `
  Execute /optimize ${intensityFlag}

  CRITICAL: Run ALL 6 scopes (security, hygiene, types, lint, performance, ai-hygiene)
  Apply fixes based on intensity selection.

  ${config.intensity === "full-fix" ? `
  FULL FIX MODE: Fix ALL items. Effort categories are for reporting only, not filtering.
  ` : ""}

  Return: {
    accounting: { applied, failed, total },
    scopes: { security, hygiene, types, lint, performance, "ai-hygiene" }
  }
`, { model: "opus", run_in_background: true })

reviewTask = Task("general-purpose", `
  Execute /review ${intensityFlag}

  CRITICAL: Run ALL 5 scopes (architecture, patterns, testing, maintainability, ai-architecture)
  Apply recommendations based on intensity selection.

  ${config.intensity === "full-fix" ? `
  FULL FIX MODE: Fix ALL items. Effort categories are for reporting only, not filtering.
  ` : ""}

  Return: {
    gaps: { coupling, cohesion, complexity, coverage },
    accounting: { applied, failed, total },
    effortCategories: { quickWin, moderate, complex, major }
  }
`, { model: "opus", run_in_background: true })
```

### Validation
```
[x] Both tasks launched in parallel
→ Results collected in Step-5
→ Proceed to Step-3
```

---

## Step-3: Verification [BACKGROUND]

**Start all verification in background (full project):**

```javascript
// Commands from context.md Operational section - FULL PROJECT
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
→ Proceed to Step-5
```

---

## Step-5: Decision [Q2 - ALL RESULTS]

**Wait for all background tasks, then show summary and ask decision:**

```javascript
// Collect all background results
optimizeResults = await TaskOutput(optimizeTask.id)
reviewResults = await TaskOutput(reviewTask.id)
formatResults = await TaskOutput(verificationTasks.format)
lintResults = await TaskOutput(verificationTasks.lint)
typeResults = await TaskOutput(verificationTasks.type)
testResults = await TaskOutput(verificationTasks.test)
buildResults = await TaskOutput(verificationTasks.build)
depResults = await TaskOutput(depTask.id)
markersResult = await TaskOutput(markersTask.id)

// Check if format made changes
formatChanged = formatResults.stdout?.includes("reformatted") || formatResults.stdout?.includes("fixed")

// Aggregate blockers and warnings
allBlockers = [
  ...preflight.blockers,
  ...(testResults.exitCode !== 0 ? [{ id: "VER-01", type: "TESTS", message: "Tests failed" }] : []),
  ...(buildResults.exitCode !== 0 ? [{ id: "VER-02", type: "BUILD", message: "Build failed" }] : []),
  ...(typeResults.exitCode !== 0 ? [{ id: "VER-03", type: "TYPES", message: "Type errors found" }] : []),
  // Security advisories are blockers
  ...(depResults.security || []).map(s => ({ id: "DEP-SEC", type: "SECURITY", message: `${s.package}: ${s.advisory} (${s.cve})` })),
  // CRITICAL findings from optimize that weren't fixed
  ...(optimizeResults.accounting?.failed > 0 && optimizeResults.blockers?.filter(b => b.severity === "CRITICAL") || [])
]

allWarnings = [
  ...preflight.warnings,
  ...(lintResults.exitCode !== 0 ? [{ id: "VER-04", type: "LINT", message: "Lint warnings" }] : []),
  ...(formatChanged ? [{ id: "VER-05", type: "FORMAT", message: "Files reformatted - review changes" }] : []),
  ...(markersResult.stdout?.trim() ? [{ id: "PRE-04", type: "MARKERS", message: "TODO/FIXME markers found" }] : []),
  // Outdated packages are warnings
  ...(depResults.outdated || []).map(d => ({ id: "DEP-OUT", type: "OUTDATED", message: `${d.package}: ${d.current} → ${d.latest}` }))
]

hasBlockers = allBlockers.length > 0

// Calculate combined accounting
// NOTE: No "declined" - AI has no option to decline. Fix or fail with reason.
totalApplied = (optimizeResults.accounting?.applied || 0) + (reviewResults.accounting?.applied || 0)
totalFailed = (optimizeResults.accounting?.failed || 0) + (reviewResults.accounting?.failed || 0)
totalFindings = totalApplied + totalFailed
```

### Pre-Decision Display [MANDATORY]

```markdown
## Release Readiness

| Metric | Value |
|--------|-------|
| Version | {manifestVersion} → {suggestedVersion} ({suggestedBump}) |
| Branch | {branch} |
| Previous | {lastTag} |
| Intensity | {config.intensity} |

### Sub-command Results
| Command | Applied | Failed | Total |
|---------|---------|--------|-------|
| /optimize | {optimizeResults.accounting.applied} | {optimizeResults.accounting.failed} | {optimizeResults.accounting.total} |
| /review | {reviewResults.accounting.applied} | {reviewResults.accounting.failed} | {reviewResults.accounting.total} |
| **Combined** | **{totalApplied}** | **{totalFailed}** | **{totalFindings}** |

### Gap Analysis (from /review)
| Dimension | Current | Ideal | Status |
|-----------|---------|-------|--------|
| Coupling | {reviewResults.gaps.coupling.current}% | <{reviewResults.gaps.coupling.ideal}% | {status} |
| Cohesion | {reviewResults.gaps.cohesion.current}% | >{reviewResults.gaps.cohesion.ideal}% | {status} |
| Complexity | {reviewResults.gaps.complexity.current} | <{reviewResults.gaps.complexity.ideal} | {status} |
| Coverage | {reviewResults.gaps.coverage.current}% | {reviewResults.gaps.coverage.ideal}%+ | {status} |

### Verification Results
| Check | Status | Detail |
|-------|--------|--------|
| Pre-flight | {preflight.blockers.length === 0 ? "PASS" : "FAIL"} | {detail} |
| Optimize | {optimizeResults.accounting.failed === 0 ? "PASS" : "WARN"} | Applied {optimizeResults.accounting.applied}/{optimizeResults.accounting.total} |
| Review | {reviewResults.accounting.failed === 0 ? "PASS" : "WARN"} | Applied {reviewResults.accounting.applied}/{reviewResults.accounting.total} |
| Tests | {testResults.exitCode === 0 ? "PASS" : "FAIL"} | {detail} |
| Build | {buildResults.exitCode === 0 ? "PASS" : "FAIL"} | {detail} |
| Types | {typeResults.exitCode === 0 ? "PASS" : "FAIL"} | {detail} |
| Lint | {lintResults.exitCode === 0 ? "PASS" : "WARN"} | {detail} |
| Dependencies | {depResults.summary.security > 0 ? "FAIL" : "PASS"} | {depResults.summary.security} security, {depResults.summary.outdated} outdated |

### Blockers (must fix before release)
{allBlockers.length === 0 ? "None - ready to release!" : allBlockers.map((b, i) => `${i+1}. [${b.type}] ${b.message}`).join('\n')}

### Warnings (can override)
{allWarnings.length === 0 ? "None" : allWarnings.map((w, i) => `${i+1}. [${w.type}] ${w.message}`).join('\n')}

**Release Ready:** {hasBlockers ? "NO - blockers must be fixed" : "YES"}
```

### Unattended Mode (--auto)

If --auto, skip Q2 and output single line:

```
cco-preflight: {hasBlockers ? "BLOCKED" : "READY"} | Blockers: {allBlockers.length} | Warnings: {allWarnings.length} | Applied: {totalApplied} | Version: {suggestedVersion}
```

Exit code: 0 (ready), 1 (warnings only), 2 (blockers)

### Interactive Mode - Ask Q2

```javascript
AskUserQuestion([
  {
    question: "Documentation updates?",
    header: "Docs",
    options: [
      { label: "CHANGELOG (Recommended)", description: "Update CHANGELOG.md with new entry" },
      { label: "README", description: "Update README if needed" },
      { label: "Skip docs", description: "No documentation updates" }
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

console.log(`
## Next Steps

1. Review changes: git diff
2. Commit: git commit -am "chore: prepare release ${suggestedVersion}"
3. Tag: git tag v${suggestedVersion}
4. Push: git push && git push --tags
`)
```

### Final Summary

```markdown
## Preflight Complete

Status: {hasBlockers ? "BLOCKED" : (allWarnings.length > 0 ? "WARN" : "OK")} | Applied: {totalApplied} | Failed: {totalFailed} | Total: {totalFindings}

**Invariant:** applied + failed = total

Decision: {userDecision}
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
| --auto mode | 0 | 0 |
| Interactive | Q1 (Intensity) + Q2 (Docs + Decision) | 2 |

**Key optimization:** All pre-flight, optimize, review, and verification run in parallel background. Only intensity upfront, then decision at the end.

### Flags

| Flag | Effect |
|------|--------|
| `--auto` | Unattended mode, full-fix intensity, no questions |
| `--intensity=X` | quick-wins, standard, full-fix, dry-run |
| `--dry-run` | Alias for --intensity=dry-run |
| `--strict` | Treat warnings as blockers |
| `--skip-tests` | Skip test suite |
| `--tag` | Create git tag after success |
| `--push` | Push to remote after success |
| `--changelog-only` | Only generate changelog |
| `--skip-docs` | Skip documentation updates |

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
| OPT-CRIT | Optimize critical | Unfixed CRITICAL from /optimize |
| REV-CRIT | Review critical | Unfixed CRITICAL gap from /review |

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

| Task | Model | Reason |
|------|-------|--------|
| /optimize | Opus | Code modifications require accuracy |
| /review | Opus | Architectural changes require accuracy |
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
| Blockers remain | Run with --intensity=full-fix |

---

## Rules

1. **Intensity first** - Select fix level before any work starts
2. **All parallel background** - Pre-flight, optimize, review, verification all background
3. **Full scope** - Run ALL scopes for both optimize (6) and review (5)
4. **Single question at end** - Docs + Decision combined after all results
5. **Collect before decision** - Wait for all background tasks before Q2
6. **Git safety** - Clean state required, version sync verified
7. **User decision required** - No release without explicit approval (unless --auto)
8. **Security blocks release** - Dependency security advisories are always blockers

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
