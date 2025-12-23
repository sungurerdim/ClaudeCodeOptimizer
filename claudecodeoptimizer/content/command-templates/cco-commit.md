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
- Line counts: !`git diff --shortstat`
- Staged lines: !`git diff --cached --shortstat`

**DO NOT re-run these commands. Use the pre-collected values above.**

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

**CRITICAL:** Run ALL quality commands from **project root** for the **entire project**, not just changed files/directories.

```javascript
// Phase 1: Blocking checks (instant, parallel)
Bash("grep -rn '{secret_patterns}' --include='*.{extensions}' || true")  // Secrets
Bash("find . -size +{max_size} -not -path './.git/*' 2>/dev/null || true")  // Large files

// Phase 2: Code quality (parallel) - Commands from context.md Operational.Tools
// IMPORTANT: Use exact commands from context.md, run from project root
// Example for Python: ruff format . && ruff check . && mypy src/
formatTask = Bash("{format_command} 2>&1", { run_in_background: true })  // e.g., "ruff format ."
lintTask = Bash("{lint_command} 2>&1", { run_in_background: true })      // e.g., "ruff check ."
typeTask = Bash("{type_command} 2>&1", { run_in_background: true })      // e.g., "mypy src/"

// Phase 3: Tests (background - check before commit)
testTask = Bash("{test_command} 2>&1", { run_in_background: true })      // e.g., "pytest tests/"
```

**Why entire project?** A change in one file can break imports, types, or tests in other files. Running checks only on changed files misses these cross-file issues.

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

**Analyze and group while tests run in background:**

```javascript
// Group changes atomically
// - Keep together: Implementation + tests, renames, single logical change
// - Split apart: Different features, unrelated files, config vs code
// - Order: Types → Core → Dependent → Tests → Docs

commitPlan = analyzeChanges(gitDiff, gitStatus)
// Returns: { commits: [{ files: [], message: { type, scope, title, body }, breaking: boolean }] }
```

### Validation
```
[x] Changes grouped atomically
[x] Commit messages generated
→ Proceed to Step-3
```

---

## Step-3: Approval [Q1 - DYNAMIC TABS]

**Build Q1 with only relevant tabs based on context:**

```javascript
// Check conditions
hasStash = stashList.trim().length > 0
hasGateFailures = gateFailures.length > 0
hasBreakingChanges = breakingChanges.length > 0

// Wait for test results now
testResult = await TaskOutput(testTask.id)
hasTestFailures = testResult.exitCode !== 0

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

  message += `\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>`

  // Create commit using HEREDOC
  Bash(`git commit -m "$(cat <<'EOF'\n${message}\nEOF\n)"`)
}
```

**Message Format:**
```
{type}({scope}): {title}

{description}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

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

```
## Commit Complete

Commits created: {n}
Files changed: {n}
Lines: +{added} -{removed}
Branch: {branch}

Commits:
{commitPlan.commits.map(c => `- ${c.message.type}(${c.message.scope}): ${c.message.title}`)}

Next: git push origin {branch}
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
6. **No vague messages** - Reject "fix bug", "update code"
7. **Git safety** - Never force push, always verify
8. **Full project checks** - Run format/lint/test on entire project from root, not just changed files
