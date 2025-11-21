---
name: cco-commit
description: AI-assisted semantic commit workflow with atomic commit recommendations and conventional commits format
action_type: commit
keywords: [commit, git, semantic, atomic, conventional, version control, changelog]
category: productivity
pain_points: [5]
---

# cco-commit

**AI-assisted semantic commit workflow with atomic commit recommendations.**

---

## Purpose

Generate high-quality semantic commit messages, recommend atomic commit splits, and improve git workflow quality (Pain #5: Git quality).

---

## Skills Used

- `cco-skill-git-branching-pr-review`
- `cco-skill-versioning-semver-changelog-compat`

---

## Execution Protocol

### Step 1: Analyze Staged Changes

```bash
git status
git diff --cached --stat
git diff --cached
```

Analyze:
- Files changed and line counts
- Types of changes (feature, fix, refactor, docs)
- Related vs unrelated changes
- Breaking changes

### Step 2: Recommend Atomic Commits

If multiple change types detected:
```markdown
Analyzing staged changes...

Files changed: 8
Lines added: 234
Lines removed: 89

Detected changes:
- [CHANGE_TYPE_1] ([ACTUAL_FILES])
- [CHANGE_TYPE_2] ([ACTUAL_FILES])
- [CHANGE_TYPE_3] ([ACTUAL_FILES])

Recommendation: Split into [N] atomic commits

[For each detected change type:]
Commit [N]: [CHANGE_TYPE]
Files: [ACTUAL_FILES from analysis]
Type: [type]([scope])

AskUserQuestion({
  questions: [{
    question: "Proceed with atomic commit split?",
    header: "Commit Split",
    multiSelect: false,
    options: [
      {label: "Yes", description: "Create atomic commits as suggested"},
      {label: "No", description: "Cancel split"},
      {label: "Customize", description: "Modify commit grouping"}
    ]
  }]
})
```

### Step 3: Generate Semantic Commit Messages

For each commit, generate message following Conventional Commits:

```
<type>(<scope>): <summary>

<body>

BREAKING CHANGE: <description if applicable>
Refs: #<issue-number>
```

**Example template (generate from ACTUAL changes):**
```markdown
Commit [N] Message:

[type]([scope]): [summary from actual changes]

- [Specific change 1 from analysis]
- [Specific change 2 from analysis]
- [Impact description based on actual changes]

Skill used: [skill used if applicable]

BREAKING CHANGE: [None or description]
Refs: #[issue-number if applicable]
```

### Step 4: Create Commits

```bash
# Stage files for commit [N]
git reset
git add [ACTUAL_FILES for this commit]

# Create commit [N]
git commit -m "$(cat <<'EOF'
[type]([scope]): [summary from actual changes]

- [Specific change 1]
- [Specific change 2]
- [Impact description]

Refs: #[issue-number if applicable]
EOF
)"

# Repeat for each atomic commit
```

**Error Handling:**

If commit fails:
```bash
# Check for pre-commit hooks
git commit --no-verify  # Only if user approves

# Check for uncommitted changes
git status
git diff --cached

# Verify git config
git config user.name
git config user.email
```

Common failures:
- Pre-commit hook rejection: Review hook output, fix issues, retry
- Empty commit: Verify files staged with `git diff --cached`
- Author not configured: Run `git config user.name/email`
- Merge conflicts: Resolve conflicts first with `git status`

### Step 5: Summary

**IMPORTANT - Dynamic Summary Generation:**
Generate summary from ACTUAL commits created. Use this template:

```markdown
Created [N] atomic commits:

[For each commit created:]
✓ [type]([scope]): [summary]
  Files: [ACTUAL_FILES]
  Lines: +[ADDED] / -[REMOVED]

Impact:
- Git workflow score: [BEFORE] → [AFTER]
- Addresses Pain #5 (better git practices)
- Benefits: Easier review, better history, simpler rollbacks

Next:
- Push: git push origin [ACTUAL_BRANCH]
- Create PR: gh pr create
```

---

## Conventional Commits Format

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring (no feature/fix)
- `perf`: Performance improvement
- `test`: Add/update tests
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

**Scopes:** Module/component affected (api, auth, database, etc.)

**Breaking Changes:** Always document with `BREAKING CHANGE:`

---

## Success Criteria

- [OK] Staged changes analyzed
- [OK] Change types detected
- [OK] Atomic split recommended if needed
- [OK] Semantic messages generated
- [OK] Commits created with proper format
- [OK] Summary presented
- [OK] Pain-point impact communicated

---

## Example Usage

```bash
# Analyze staged changes and create commits
/cco-commit

# If no staged changes, stage all and analyze
git add .
/cco-commit
```

---

## Optional Prompt Support

Any text after the command is treated as additional context for commit generation.

**Examples:**
```bash
/cco-commit "Include co-authored commit"
/cco-commit "Use conventional commits with BREAKING CHANGE keyword"
/cco-commit "Focus on security-related changes"
/cco-commit "Atomic commits only - split unrelated changes"
```

**How it works:**
The AI will incorporate your guidance when:
- Analyzing changes for commit granularity
- Generating commit messages
- Determining atomic commit boundaries
- Applying conventional commit formats
- Adding co-authors or special metadata

**Use cases:**
- Specify commit message style preferences
- Request inclusion of specific metadata (co-authors, issue refs, breaking changes)
- Provide context about the changes (why, not just what)
- Request specific commit splitting strategies

---

### Step 4.5: Git Error Handling

**If commit fails (pre-commit hook, git config, merge conflict):**

AskUserQuestion({
  questions: [{
    question: "Git commit failed: {error_type} - {error_message}. How to proceed?",
    header: "Git Error",
    multiSelect: false,
    options: [
      {label: "Fix and retry", description: "Fix the issue and retry commit"},
      {label: "Skip hooks", description: "Commit with --no-verify (use cautiously)"},
      {label: "Amend previous", description: "Amend previous commit instead"},
      {label: "Cancel", description: "Stop commit operation"}
    ]
  }]
})

**If too many changes detected (>5 logical changes):**

AskUserQuestion({
  questions: [{
    question: "Too many changes detected ({COUNT} logical changes). Split into atomic commits?",
    header: "Commit Split",
    multiSelect: false,
    options: [
      {label: "Yes - atomic commits", description: "Create separate commit for each logical change (recommended)"},
      {label: "No - single commit", description: "Keep all changes in one commit"},
      {label: "Custom split", description: "Manually select which changes to group"}
    ]
  }]
})
