---
name: cco-commit
description: Atomic commits with quality gates
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(npm:*), Bash(pytest:*), Read(*), Grep(*), Edit(*), TodoWrite, AskUserQuestion
---

# /cco-commit

**Smart Commits** - Parallel quality gates + atomic grouping.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`
- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Stash list: !`git stash list --oneline | head -3`
- Line counts: !`git diff --shortstat`
- Staged lines: !`git diff --cached --shortstat`

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
| 1 | Pre-checks | Conflicts, stash, large | Instant |
| 2 | Unstaged | Ask about unstaged | Skip if none |
| 3 | Quality | Parallel: format+lint+types, background: tests | 3x faster |
| 4 | Analyze | Group atomically | While tests run |
| 5 | Plan | Show plan, ask approval | Instant |
| 6 | Execute | Create commits | Sequential |
| 7 | Summary | Show results | Instant |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Run pre-checks", status: "in_progress", activeForm: "Running pre-checks" },
  { content: "Step-2: Handle unstaged", status: "pending", activeForm: "Handling unstaged changes" },
  { content: "Step-3: Run quality gates", status: "pending", activeForm: "Running quality gates" },
  { content: "Step-4: Analyze changes", status: "pending", activeForm: "Analyzing changes" },
  { content: "Step-5: Get plan approval", status: "pending", activeForm: "Getting plan approval" },
  { content: "Step-6: Execute commits", status: "pending", activeForm: "Executing commits" },
  { content: "Step-7: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Pre-checks

### Step-1.1: Conflict Check [BLOCKER]

If `UU`/`AA`/`DD` in git status:
```
Cannot commit: {n} conflict(s) detected. Resolve first.
```
**Stop immediately.**

### Step-1.2: Stash Check

If stash list not empty:

```javascript
AskUserQuestion([{
  question: "You have stashed changes. What to do?",
  header: "Stash",
  options: [
    { label: "Keep stashed", description: "Continue without stash (stash remains)" },
    { label: "Apply and include", description: "Apply to working tree, include in commit (stash kept)" },
    { label: "Pop and include", description: "Pop to working tree, include in commit (stash removed)" }
  ],
  multiSelect: false
}])
```

### Step-1.3: Large Changes Check

If 500+ lines changed:

```javascript
AskUserQuestion([{
  question: "Large changeset (500+ lines). How to proceed?",
  header: "Size",
  options: [
    { label: "Continue", description: "Proceed with large commit" },
    { label: "Split", description: "Help me split into smaller commits" },
    { label: "Cancel", description: "Abort and review manually" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] No conflicts (or stopped)
[x] Stash handled (if exists)
[x] Large changes handled (if applicable)
→ Proceed to Step-2
```

---

## Step-2: Unstaged Changes

If unstaged changes exist:

```javascript
AskUserQuestion([{
  question: "Include unstaged changes?",
  header: "Unstaged",
  options: [
    { label: "Yes, include all", description: "Stage and include all changes" },
    { label: "No, staged only", description: "Commit only staged changes" },
    { label: "Select files", description: "Choose which files to include" }
  ],
  multiSelect: false
}])
```

If "Select files" → show file picker with multiSelect.

### Validation
```
[x] Unstaged changes decision made
[x] Files staged as needed
→ Proceed to Step-3
```

---

## Step-3: Quality Gates [PARALLEL + BACKGROUND]

**Phase 1: Blocking checks (instant)**
```javascript
// These must pass before proceeding - run in parallel
Bash("grep -rn '{secret_patterns}' --include='*.{extensions}' || true")  // Secrets
Bash("find . -size +{max_size} -not -path './.git/*' 2>/dev/null || true")  // Large files
```

**Phase 2: Code quality (parallel)**
```javascript
// Run format, lint, types in PARALLEL - all in ONE message
// Commands from context.md Operational section
Bash("{format_command} 2>&1")    // Format - auto-fix
Bash("{lint_command} 2>&1")      // Lint
Bash("{type_command} 2>&1")      // Types
```

**Phase 3: Tests (background while continuing)**
```javascript
// Start tests in background - don't block
testTask = Bash("{test_command} 2>&1", { run_in_background: true })

// Continue to Step-4 while tests run
// Check testTask.id before Step-6 (Execute)
```

| Gate | Execution | Action |
|------|-----------|--------|
| Secrets | Parallel Phase 1 | BLOCK if found |
| Large Files | Parallel Phase 1 | BLOCK if >10MB |
| Format | Parallel Phase 2 | Auto-fix, re-stage |
| Lint | Parallel Phase 2 | STOP on unfixable |
| Types | Parallel Phase 2 | STOP on failure |
| Tests | Background Phase 3 | Check before commit |

**Commands from context.md Operational section.**

### On Failure

```javascript
AskUserQuestion([{
  question: "{gate} failed: {error}. How to proceed?",
  header: "Gate Failed",
  options: [
    { label: "Fix and retry", description: "I'll fix the issue, then retry" },
    { label: "Skip gate", description: "Continue without this check" },
    { label: "Cancel", description: "Abort commit" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] Phase 1 blocking checks passed
[x] Phase 2 code quality passed (or skipped)
[x] Phase 3 tests started in background
→ Proceed to Step-4 (don't wait for tests)
```

---

## Step-4: Analyze Changes

Group changes atomically:
- **Keep together:** Implementation + tests, renames, single logical change
- **Split apart:** Different features, unrelated files, config vs code
- **Order:** Types → Core → Dependent → Tests → Docs

Generate commit plan with messages.

### Validation
```
[x] Changes grouped atomically
[x] Commit messages generated
→ Store as: commitPlan = { commits: [...] }
→ Proceed to Step-5
```

---

## Step-5: Plan Approval

Display commit plan, then ask:

```javascript
AskUserQuestion([{
  question: "Commit plan ready. How to proceed?",
  header: "Plan",
  options: [
    { label: "Accept", description: "Execute commits as planned" },
    { label: "Modify", description: "Change grouping or order" },
    { label: "Edit messages", description: "Modify commit messages" },
    { label: "Cancel", description: "Abort without committing" }
  ],
  multiSelect: false
}])
```

**Dynamic labels:** Add `(Recommended)` if clean history.

### If Modify

```javascript
AskUserQuestion([{
  question: "How to modify?",
  header: "Modify",
  options: [
    { label: "Merge commits", description: "Combine multiple into one" },
    { label: "Split commit", description: "Break one into multiple" },
    { label: "Reorder", description: "Change commit sequence" },
    { label: "Edit files", description: "Change file grouping" }
  ],
  multiSelect: false
}])
```

### If Edit Messages

Show each message for editing, then return to approval.

### Breaking Change Detection

If API removal/signature change detected:

```javascript
AskUserQuestion([{
  question: "Breaking change detected. Add BREAKING CHANGE footer?",
  header: "Breaking",
  options: [
    { label: "Yes", description: "Add BREAKING CHANGE: footer to commit" },
    { label: "No", description: "Not a breaking change" }
  ],
  multiSelect: false
}])
```

### Validation
```
[x] User approved plan (or modified and re-approved)
[x] Breaking changes handled
→ If Cancel: Exit
→ Proceed to Step-6
```

---

## Step-6: Execute Commits

**First: Check background tests**
```javascript
// Wait for tests that started in Step-3
testResults = await TaskOutput(testTask.id)

if (testResults.failed) {
  AskUserQuestion([{
    question: "Tests failed. Proceed anyway?",
    header: "Tests",
    options: [
      { label: "Fix first", description: "Cancel and fix failing tests" },
      { label: "Commit anyway", description: "Proceed despite test failures" }
    ],
    multiSelect: false
  }])
}
```

**Then: Execute commits sequentially**

**Message Format:**
```
{type}({scope}): {title}

{description}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

| Rule | Requirement |
|------|-------------|
| Title | ≤50 chars, action verb, no period |
| Description | What changed and why (1-3 lines) |
| Scope | From affected module/feature |
| Types | feat, fix, refactor, perf, test, docs, build, ci, chore |

### Validation
```
[x] Background tests checked
[x] All commits created successfully
→ Proceed to Step-7
```

---

## Step-7: Summary

Display:
- Commits created: {n}
- Files changed: {n}
- Lines: +{n} -{n}
- Branch: {branch}

### Validation
```
[x] Summary displayed
[x] All todos marked completed
→ Done
```

---

## Reference

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

### Context Application

| Field | Effect |
|-------|--------|
| Tools | format/lint/test from Operational |
| Maturity | Legacy → smaller commits; Greenfield → batch |
| Type | Library → careful with API; API → note contracts |

---

## Recovery

If something goes wrong during the commit process:

| Situation | Recovery |
|-----------|----------|
| Commit failed mid-way | `git status` to see state, unstaged files remain safe |
| Wrong files committed | `git reset --soft HEAD~1` to undo last commit (keeps changes staged) |
| Bad commit message | `git commit --amend` to edit message (only if not pushed) |
| Quality gate broke something | `git checkout -- {file}` to restore, or `git stash` to save work |
| Need to abort completely | `git reset HEAD` to unstage all, working tree unchanged |

**Safe rule:** Local commits can always be amended/reset. Once pushed, create a new commit instead.

---

## Rules

1. **Parallel quality gates** - Format+lint+types in single message
2. **Background tests** - Start tests early, check before commit
3. **Analyze while waiting** - Group changes while tests run
4. **No vague messages** - Reject "fix bug", "update code", "changes"
5. **Git safety** - Never force push, always verify
6. **Skip flags** - `--skip-checks` bypasses quality gates
