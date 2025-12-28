---
name: cco-commit
description: Atomic commits with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*), TodoWrite, AskUserQuestion
model: opus
---

# /cco-commit

**Smart Commits** - Parallel quality gates + atomic grouping with minimal questions.

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
| 1 | Pre-checks | Conflicts check + parallel quality gates | Background |
| 2 | Analyze | Group changes atomically | While gates run |
| 3 | Approval | Q1: Combined commit settings | Single question |
| 4 | Execute | Create commits | Sequential |
| 5 | Summary | Show results | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Run pre-checks and quality gates", status: "in_progress", activeForm: "Running checks" },
  { content: "Step-2: Analyze and group changes", status: "pending", activeForm: "Analyzing changes" },
  { content: "Step-3: Get commit approval", status: "pending", activeForm: "Getting approval" },
  { content: "Step-4: Execute commits", status: "pending", activeForm: "Executing commits" },
  { content: "Step-5: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Pre-checks + Quality Gates [PARALLEL]

### 1.1: Conflict Check [BLOCKER]

If `UU`/`AA`/`DD` in git status:
```
Cannot commit: {n} conflict(s) detected. Resolve first.
```
**Stop immediately.**

### 1.2: Quality Gates [PARALLEL + BACKGROUND]

**Smart Default:** Stage all unstaged changes automatically. Use `--staged-only` to commit only staged.

**Targeted Execution:** Run quality checks on **changed files only** for speed. Use `--full-project` flag to check entire project when cross-file issues are suspected.

```javascript
// Get changed files (language-agnostic)
changedFiles = Bash("git diff --name-only HEAD").split('\n').filter(f => f.trim())

// Phase 1: Blocking checks (instant, parallel) - on changed files only
Bash(`grep -n 'api_key\\|password\\|secret\\|token\\|credential' ${changedFiles.join(' ')} 2>/dev/null || true`)
Bash(`find ${changedFiles.join(' ')} -size +10M 2>/dev/null || true`)

// Phase 2: Code quality (parallel) - Commands from context.md Operational.Tools
// TARGETED: Replace "." with changed files list for ~85% token reduction
// Example: "ruff format ." → "ruff format file1.py file2.py"
targetFiles = args.includes('--full-project') ? '.' : changedFiles.join(' ')

formatTask = Bash(`{format_command} ${targetFiles} 2>&1`, { run_in_background: true })
lintTask = Bash(`{lint_command} ${targetFiles} 2>&1`, { run_in_background: true })
typeTask = Bash(`{type_command} ${targetFiles} 2>&1`, { run_in_background: true })

// Phase 3: Tests - smart selection based on changed files
// Use test framework's built-in file targeting when available
testTask = Bash("{test_command} 2>&1", { run_in_background: true })
```

**Why targeted?** Commits typically touch 2-5 files. Checking only those files reduces output by ~85% while catching relevant issues. Use `--full-project` when refactoring imports or types.

| Gate | Execution | Action |
|------|-----------|--------|
| Secrets | Parallel Phase 1 | BLOCK if found |
| Large Files | Parallel Phase 1 | BLOCK if >10MB |
| Format | Parallel Phase 2 | Auto-fix, re-stage |
| Lint | Parallel Phase 2 | Collect errors |
| Types | Parallel Phase 2 | Collect errors |
| Tests | Background Phase 3 | Check before commit |

### 1.3: Collect Gate Results

```javascript
// Wait for Phase 2 results
formatResult = await TaskOutput(formatTask.id)
lintResult = await TaskOutput(lintTask.id)
typeResult = await TaskOutput(typeTask.id)

// Determine gate status
gateFailures = []
if (lintResult.exitCode !== 0) gateFailures.push({ gate: "Lint", error: lintResult.stderr })
if (typeResult.exitCode !== 0) gateFailures.push({ gate: "Types", error: typeResult.stderr })

// Detect breaking changes
breakingChanges = detectBreakingChanges(gitDiff)
```

### Validation
```
[x] No conflicts
[x] Phase 1 passed (no secrets, no large files)
[x] Phase 2 results collected
[x] Tests running in background
→ Proceed to Step-2
```

---

## Step-2: Analyze Changes [WHILE TESTS RUN]

**Analyze and group while tests run in background.**

### 2.1: Collect ALL Uncommitted Changes [CRITICAL]

```javascript
// CRITICAL: Include ALL uncommitted changes, not just session changes
// This means: modified, added, deleted, renamed, untracked - EVERYTHING

// Get complete list of all uncommitted files
allChanges = {
  staged: Bash("git diff --cached --name-only").split('\n'),      // Already staged
  unstaged: Bash("git diff --name-only").split('\n'),             // Modified but not staged
  untracked: Bash("git ls-files --others --exclude-standard").split('\n')  // New files
}

// Combine all - these are the files to commit
filesToCommit = [...new Set([
  ...allChanges.staged,
  ...allChanges.unstaged,
  ...allChanges.untracked
])].filter(f => f.trim())

// If --staged-only flag, only use staged files
if (args.includes('--staged-only')) {
  filesToCommit = allChanges.staged.filter(f => f.trim())
}
```

### 2.2: Group Changes Atomically

```javascript
// Group changes atomically
// - Keep together: Implementation + tests, renames, single logical change
// - Split apart: Different features, unrelated files, config vs code
// - Order: Types → Core → Dependent → Tests → Docs

// Get full diff content for analysis
gitDiff = Bash("git diff HEAD")  // All changes vs HEAD
gitDiffUntracked = filesToCommit
  .filter(f => allChanges.untracked.includes(f))
  .map(f => Bash(`cat "${f}"`))  // Content of new files

commitPlan = analyzeChanges(filesToCommit, gitDiff, gitDiffUntracked)
// Returns: { commits: [{ files: [], message: { type, scope, title, body }, breaking: boolean }] }
```

### Validation
```
[x] All uncommitted changes collected (staged + unstaged + untracked)
[x] Changes grouped atomically
[x] Commit messages generated
→ Proceed to Step-3
```

---

## Step-3: Approval [Q1 - DYNAMIC TABS]

**Display commit table BEFORE asking approval question:**

### Pre-Confirmation Display [MANDATORY]

```markdown
## Changes to Commit

**Source:** All uncommitted changes (staged: {n}, unstaged: {n}, untracked: {n})

| # | Type | Title | Files |
|---|------|-------|-------|
| 1 | {type} | {title} | {n} files |
| 2 | {type} | {title} | {n} files |
...

Total: {n} commit(s), {n} file(s), +{added} -{removed} lines
```

**Build Q1 with only relevant tabs based on context:**

```javascript
// Check conditions
hasStash = stashList.trim().length > 0
hasGateFailures = gateFailures.length > 0
hasBreakingChanges = breakingChanges.length > 0

// Wait for test results now
testResult = await TaskOutput(testTask.id)
hasTestFailures = testResult.exitCode !== 0

// Display commit table BEFORE question
console.log(formatCommitTable(commitPlan.commits))

// Build questions dynamically
questions = []

// Tab 1: Stash handling (only if stash exists)
if (hasStash) {
  questions.push({
    question: "You have stashed changes. What to do?",
    header: "Stash",
    options: [
      { label: "Keep stashed (Recommended)", description: "Continue without stash" },
      { label: "Apply and include", description: "Apply to working tree, include in commit" },
      { label: "Pop and include", description: "Pop to working tree, include in commit" }
    ],
    multiSelect: false
  })
}

// Tab 2: Commit plan (always)
questions.push({
  question: `Commit plan: ${commitPlan.commits.length} commit(s). How to proceed?`,
  header: "Plan",
  options: [
    { label: "Accept (Recommended)", description: "Execute commits as planned" },
    { label: "Single commit", description: "Combine all into one commit" },
    { label: "Edit messages", description: "Modify commit messages first" },
    { label: "Cancel", description: "Abort without committing" }
  ],
  multiSelect: false
})

// Tab 3: Breaking changes (only if detected)
if (hasBreakingChanges) {
  questions.push({
    question: `Breaking change detected: ${breakingChanges[0].description}. Add footer?`,
    header: "Breaking",
    options: [
      { label: "Add BREAKING CHANGE (Recommended)", description: "Add footer to commit message" },
      { label: "Not breaking", description: "This is not a breaking change" }
    ],
    multiSelect: false
  })
}

// Tab 4: Gate/Test failures (only if failures exist)
if (hasGateFailures || hasTestFailures) {
  const failureType = hasTestFailures ? "Tests" : gateFailures[0].gate
  const failureMsg = hasTestFailures ? testResult.stderr : gateFailures[0].error

  questions.push({
    question: `${failureType} failed. How to proceed?`,
    header: "Failure",
    options: [
      { label: "Fix first (Recommended)", description: "Cancel and fix the issue" },
      { label: "Skip check", description: "Continue without this check" },
      { label: "Commit anyway", description: "Proceed despite failure" }
    ],
    multiSelect: false
  })
}

AskUserQuestion(questions)
```

### Question Flow Summary

| Condition | Tabs Shown |
|-----------|------------|
| Clean, no stash, no breaking | Plan only (1 tab) |
| Has stash | Stash + Plan (2 tabs) |
| Breaking change detected | Plan + Breaking (2 tabs) |
| Test/gate failure | Plan + Failure (2 tabs) |
| All conditions | Stash + Plan + Breaking + Failure (4 tabs) |

### Validation
```
[x] User completed Q1
→ If Plan = "Cancel" or Failure = "Fix first": Exit
→ If Plan = "Edit messages": Show message editor, return to Q1
→ If Plan = "Single commit": Merge commitPlan into single
→ Proceed to Step-4
```

---

## Step-4: Execute Commits

**Create commits sequentially:**

```javascript
for (const commit of commitPlan.commits) {
  // Stage files
  Bash(`git add ${commit.files.join(' ')}`)

  // Build message with footer if breaking
  let message = `${commit.message.type}(${commit.message.scope}): ${commit.message.title}\n\n${commit.message.body}`

  if (commit.breaking && userApprovedBreaking) {
    message += `\n\nBREAKING CHANGE: ${commit.breakingDescription}`
  }

  // Append Claude Code signature with current model name
  message += `\n\nGenerated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: ${currentModelName} <noreply@anthropic.com>`

  // Create commit using HEREDOC
  Bash(`git commit -m "$(cat <<'EOF'\n${message}\nEOF\n)"`)
}
```

**Message Format:**
```
{type}({scope}): {title}

{description}

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Note:** Use the current active model name (e.g., Claude Opus 4.5, Claude Sonnet 4, Claude Haiku 3.5).

### Title Rules [CRITICAL]

**MUST be ≤50 characters total** (including `type(scope): ` prefix)

```javascript
// VALIDATE before commit - this is BLOCKING
const fullTitle = `${type}(${scope}): ${title}`
if (fullTitle.length > 50) {
  // SHORTEN the title, not optional
  // Remove adjectives, use shorter words, abbreviate
}
```

| Component | Max Length | Example |
|-----------|------------|---------|
| type | 8 | `feat`, `fix`, `refactor` |
| scope | 10 | `{module}`, `{feature}`, `{area}` |
| title | ~30 | `{concise action description}` |
| **TOTAL** | **≤50** | `{type}({scope}): {short title}` (≤50 chars ✓) |

**Good:** `{type}({scope}): {short title}` (≤50 chars)
**Bad:** `{type}({scope}): {title}, {extra detail}, and {more info}` (>50 chars ❌)

| Rule | Requirement |
|------|-------------|
| Title | **≤50 chars total**, action verb, no period |
| Description | What changed and why (1-3 lines) |
| Scope | From affected module/feature |
| Types | feat, fix, refactor, perf, test, docs, build, ci, chore |

### Validation
```
[x] All commits created successfully
→ Proceed to Step-5
```

---

## Step-5: Summary

```javascript
// Build summary with conditional stash reminder
let summary = `
## Commit Complete

| Metric | Value |
|--------|-------|
| Commits created | {n} |
| Files changed | {n} |
| Lines | +{added} -{removed} |
| Branch | {branch} |

Status: OK | Applied: {n} | Declined: 0 | Failed: 0

### Commits Created
| # | Type | Title |
|---|------|-------|
| 1 | {type}({scope}) | {title} |
| 2 | {type}({scope}) | {title} |
...

Next: git push origin {branch}`

// Stash reminder if user chose "Keep stashed"
if (hasStash && stashChoice === "Keep stashed") {
  summary += `

**Reminder:** You have stashed changes. Run \`git stash pop\` to restore them.`
}

console.log(summary)
```

### Validation
```
[x] Summary displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Question Flow Summary

| Scenario | Tabs | Total Questions |
|----------|------|-----------------|
| Clean state, simple commit | 1 (Plan) | 1 |
| Has stash | 2 (Stash + Plan) | 1 |
| Breaking change | 2 (Plan + Breaking) | 1 |
| Test failure | 2 (Plan + Failure) | 1 |
| Maximum complexity | 4 (all tabs) | 1 |

**Key optimization:** All conditional situations handled in single Q1 with dynamic tabs.

### Quick Mode (`--quick`)

When `--quick` flag:
- No questions - use smart defaults
- Stage all changes
- Single commit with auto-generated message
- Complete in single message

### Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Show plan only |
| `--single` | Force one commit |
| `--quick` | Single-message, smart defaults |
| `--skip-checks` | Skip quality gates |
| `--amend` | Amend last (with safety) |
| `--staged-only` | Commit only staged changes |
| `--split` | Auto-split large changesets |
| `--full-project` | Run quality gates on entire project (not just changed files) |

### Context Application

| Field | Effect |
|-------|--------|
| Tools | format/lint/test from Operational |
| Maturity | Legacy → smaller commits; Greenfield → batch |
| Type | Library → careful with API; API → note contracts |

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Commit failed mid-way | `git status` to see state |
| Wrong files committed | `git reset --soft HEAD~1` |
| Bad commit message | `git commit --amend` (if not pushed) |
| Quality gate broke something | `git checkout -- {file}` |
| Need to abort | `git reset HEAD` |

**Safe rule:** Local commits can always be amended/reset. Once pushed, create new commit.

---

## Rules

1. **Title ≤50 chars** - BLOCKING: `type(scope): title` must be ≤50 total
2. **Parallel quality gates** - Format+lint+types in background
3. **Background tests** - Start tests early, check before commit
4. **Single question** - All conditional tabs in one Q1
5. **Dynamic tabs** - Only show relevant tabs
6. **Specific messages** - Use descriptive action verbs: "add", "fix", "refactor", "update"
7. **Git safety** - Verify before push, prefer safe operations
8. **Targeted checks** - Run format/lint/type on changed files only (~85% faster). Use `--full-project` for cross-file refactoring
