---
description: Smart git commits with quality gates and atomic grouping
argument-hint: [--staged-only] [--no-verify] [--amend]
allowed-tools: Read(*), Grep(*), Edit(*), Bash(*), AskUserQuestion
model: opus
---

# /cco-commit

**Smart Commits** - Fast quality gates + atomic grouping, no unnecessary questions.

## Context

- Git status: !`git status --short`
- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Stash list: !`git stash list --oneline | head -3`
- All changes (staged+unstaged): !`git diff HEAD --shortstat`
- Staged only: !`git diff --cached --shortstat`
- Untracked files: !`git ls-files --others --exclude-standard | wc -l`

**DO NOT re-run these commands. Use the pre-collected values above.**

**[CRITICAL] Scope: ALL uncommitted changes are included by default:**
- Staged files (already in index)
- Unstaged modifications (tracked files with changes)
- Untracked files (new files not yet added)
- Use `--staged-only` flag to commit only staged changes

## Architecture

| Step | Name | Action | Optimization |
|------|------|--------|--------------|
| 1 | Pre-checks | Conflicts + quality gates | Parallel, conditional tests |
| 2 | Analyze | Group changes, show table | Smart grouping |
| 3 | Execute | Create commits | Direct (no question) |
| 4 | Verify | Confirm commits created | git log check |
| 5 | Summary | Show results | Instant |

**No TodoWrite** - Fast operation, output is self-explanatory.

---

## Step-1: Pre-checks + Quality Gates [PARALLEL]

### 1.1: Conflict Check [BLOCKER]

If `UU`/`AA`/`DD` in git status:
```
Cannot commit: {n} conflict(s) detected. Resolve first.
```
**Stop immediately.**

### 1.2: Detect File Types

```javascript
// Get changed files
changedFiles = Bash("git diff --name-only HEAD").split('\n').filter(f => f.trim())

// Categorize files
codeFiles = changedFiles.filter(f => f.match(/\.(py|js|ts|go|rs|java|rb|php|c|cpp|h)$/))
testFiles = changedFiles.filter(f => f.match(/test[_.]|_test\.|\.test\.|spec\./i))
docFiles = changedFiles.filter(f => f.match(/\.(md|txt|rst|adoc)$/))
configFiles = changedFiles.filter(f => f.match(/\.(json|yaml|yml|toml|ini|cfg)$/))

hasCodeChanges = codeFiles.length > 0
hasTestChanges = testFiles.length > 0
```

### 1.3: Quality Gates [PARALLEL + CONDITIONAL]

```javascript
// Phase 1: Blocking checks (always, instant)
Bash(`grep -rn 'api_key\\|password\\|secret\\|token\\|credential' ${changedFiles.join(' ')} 2>/dev/null | grep -v '.md:' || true`)
Bash(`find ${changedFiles.join(' ')} -size +10M 2>/dev/null || true`)

// Phase 2: Code quality (only if code files changed)
if (hasCodeChanges) {
  targetFiles = changedFiles.filter(f => codeFiles.includes(f)).join(' ')

  formatTask = Bash(`{format_command} ${targetFiles} 2>&1`, { run_in_background: true })
  lintTask = Bash(`{lint_command} ${targetFiles} 2>&1`, { run_in_background: true })
  typeTask = Bash(`{type_command} ${targetFiles} 2>&1`, { run_in_background: true })
}

// Phase 3: Tests (CONDITIONAL - skip if only docs/config changed)
if (hasCodeChanges || hasTestChanges) {
  testTask = Bash("{test_command} 2>&1", { run_in_background: true })
} else {
  // Skip tests for doc-only or config-only changes
  testTask = null
}
```

**Conditional Test Logic:**
| Changed Files | Run Tests? |
|---------------|------------|
| Code (.py, .js, etc.) | Yes |
| Tests (test_*, *_test.*) | Yes |
| Docs only (.md) | No |
| Config only (.json, .yaml) | No |
| Mixed | Yes |

### 1.4: Collect Gate Results

```javascript
gateFailures = []

if (hasCodeChanges) {
  formatResult = await TaskOutput(formatTask.id)
  lintResult = await TaskOutput(lintTask.id)
  typeResult = await TaskOutput(typeTask.id)

  if (lintResult.exitCode !== 0) gateFailures.push({ gate: "Lint", error: lintResult.stderr })
  if (typeResult.exitCode !== 0) gateFailures.push({ gate: "Types", error: typeResult.stderr })
}

if (testTask) {
  testResult = await TaskOutput(testTask.id)
  if (testResult.exitCode !== 0) gateFailures.push({ gate: "Tests", error: testResult.stderr })
}
```

### Gate Failure Handling

```javascript
if (gateFailures.length > 0) {
  // Ask only if there are failures
  AskUserQuestion([{
    question: `${gateFailures[0].gate} failed. How to proceed?`,
    header: "Failure",
    options: [
      { label: "Fix first (Recommended)", description: "Cancel and fix the issue" },
      { label: "Commit anyway", description: "Proceed despite failure" }
    ],
    multiSelect: false
  }])

  if (response === "Fix first") {
    // Show error details and exit
    console.log(`\n**${gateFailures[0].gate} Error:**\n${gateFailures[0].error}`)
    return
  }
}
```

---

## Step-2: Analyze Changes

### 2.1: Collect ALL Uncommitted Changes

```javascript
allChanges = {
  staged: Bash("git diff --cached --name-only").split('\n').filter(f => f.trim()),
  unstaged: Bash("git diff --name-only").split('\n').filter(f => f.trim()),
  untracked: Bash("git ls-files --others --exclude-standard").split('\n').filter(f => f.trim())
}

filesToCommit = [...new Set([
  ...allChanges.staged,
  ...allChanges.unstaged,
  ...allChanges.untracked
])]

if (args.includes('--staged-only')) {
  filesToCommit = allChanges.staged
}
```

### 2.2: Smart Grouping

```javascript
// Get diff for analysis
gitDiff = Bash("git diff HEAD")

// Smart grouping rules:
// - ≤5 files OR single logical change → single commit
// - Different features/scopes → split commits
// - Default: single commit (simpler, user can always split manually)

if (args.includes('--split')) {
  commitPlan = splitByScope(filesToCommit, gitDiff)
} else {
  // Default: single commit
  commitPlan = { commits: [{ files: filesToCommit, message: generateMessage(gitDiff) }] }
}

// [CRITICAL] Message generation rules:
// 1. ONLY analyze gitDiff content
// 2. NEVER use session memory
// 3. Describe WHAT changed, not WHY
```

### 2.3: Display Commit Plan

```javascript
console.log(`
## Changes to Commit

| # | Type | Title | Files |
|---|------|-------|-------|
${commitPlan.commits.map((c, i) =>
  `| ${i+1} | ${c.message.type} | ${c.message.title} | ${c.files.length} |`
).join('\n')}

Total: ${commitPlan.commits.length} commit(s), ${filesToCommit.length} file(s)
${testTask === null ? '\n*Tests skipped (no code changes)*' : ''}
`)
```

---

## Step-3: Execute Commits [DIRECT]

**No approval question** - table was shown, user sees what will happen.

```javascript
for (const commit of commitPlan.commits) {
  // Stage files
  Bash(`git add ${commit.files.map(f => `"${f}"`).join(' ')}`)

  // Build message
  let message = `${commit.message.type}(${commit.message.scope}): ${commit.message.title}`

  if (commit.message.body) {
    message += `\n\n${commit.message.body}`
  }

  // Append signature
  message += `\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: ${currentModelName} <noreply@anthropic.com>`

  // Create commit
  Bash(`git commit -m "$(cat <<'EOF'
${message}
EOF
)"`)
}
```

### Title Rules [CRITICAL]

**MUST be ≤50 characters total** (including `type(scope): ` prefix)

| Component | Max | Example |
|-----------|-----|---------|
| type | 8 | `feat`, `fix`, `refactor` |
| scope | 10 | `benchmark`, `templates` |
| title | ~30 | concise action |
| **TOTAL** | **≤50** | `fix(api): handle null response` |

---

## Step-4: Verify

```javascript
// Verify commits were created successfully
verifyResult = Bash("git log --oneline -" + commitPlan.commits.length)
gitStatus = Bash("git status --short")

// Check working tree is clean (all changes committed)
if (gitStatus.trim() && !args.includes('--staged-only')) {
  console.log("⚠️ Warning: Working tree not clean after commit")
}

// Verify commit count matches plan
actualCommits = verifyResult.split('\n').filter(l => l.trim()).length
if (actualCommits < commitPlan.commits.length) {
  console.log(`⚠️ Warning: Expected ${commitPlan.commits.length} commits, found ${actualCommits}`)
}
```

---

## Step-5: Summary

```javascript
console.log(`
## Commit Complete

| Metric | Value |
|--------|-------|
| Commits | ${commitPlan.commits.length} |
| Files | ${filesToCommit.length} |
| Branch | ${branch} |
| Status | ${gitStatus.trim() ? 'WARN' : 'OK'} |

${commitPlan.commits.map((c, i) =>
  `- ${c.message.type}(${c.message.scope}): ${c.message.title}`
).join('\n')}

Next: \`git push origin ${branch}\`
`)

if (stashList.trim()) {
  console.log(`\n**Note:** You have stashed changes. Run \`git stash pop\` if needed.`)
}
```

---

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show plan only, don't commit |
| `--single` | Force single commit |
| `--split` | Auto-split by scope |
| `--skip-tests` | Skip test gate |
| `--amend` | Amend last commit (safety checks apply) |
| `--staged-only` | Commit only staged changes |
| `--full-project` | Run gates on entire project |
| `--confirm` | Ask approval before commit (old behavior) |

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Wrong files | `git reset --soft HEAD~1` |
| Bad message | `git commit --amend` (if not pushed) |
| Gate broke something | `git checkout -- {file}` |

---

## Rules

1. **Title ≤50 chars** - BLOCKING requirement
2. **Diff-only messages** - Generate from `git diff HEAD` only, never session memory
3. **Conditional tests** - Skip tests if only docs/config changed
4. **No approval by default** - Table shown, commit direct, use `--confirm` if needed
5. **Smart defaults** - Single commit unless `--split`
6. **Parallel gates** - Format+lint+types run together
7. **Fast path** - No TodoWrite, minimal questions
