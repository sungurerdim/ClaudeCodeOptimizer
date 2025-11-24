---
name: cco-commit
description: AI-assisted semantic commit workflow with atomic commit recommendations and conventional commits format

keywords: [commit, git, semantic, atomic, conventional, version control, changelog]
category: productivity
pain_points: [5]
---

# cco-commit

**AI-assisted semantic commit workflow with atomic commit recommendations.**
---

## Built-in References

**This command inherits standard behaviors from:**

- **[STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md)** - Standard structure, execution protocol, file discovery
- **[STANDARDS_QUALITY.md](../STANDARDS_QUALITY.md)** - UX/DX, efficiency, simplicity, performance standards
- **[LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md)** - Reusable patterns (Step 0, Selection, Accounting, Progress, Error Handling)
- **[STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md)** - File discovery, model selection, parallel execution

**See these files for detailed patterns. Only command-specific content is documented below.**

---

## Execution Guarantee

**This command WILL execute fully without requiring user presence during processing.**

**What Happens:**
1. **Step 0**: Introduction and confirmation (user input required)
2. **Step 1**: Analyze ALL uncommitted changes (staged, unstaged, untracked), detect change types (automated)
3. **Step 2**: Recommend atomic commit splits if needed (user confirmation required)
4. **Step 3**: Generate semantic commit messages following skill guidelines (automated)
5. **Step 4**: Create commits with proper format (automated)
6. **Step 5**: Display summary with accounting (automated)

**User Interaction Points:**
- Initial confirmation (optional prompt context)
- Atomic commit split confirmation (if multiple change types detected)
- Git error handling (if commit failures occur)

**Automation:**
- Git diff analysis runs without interruption
- Commit messages generated automatically from actual changes
- All commits created with conventional commits format
- Complete accounting enforced (total commits created = planned commits)

**Time Estimate:**
- Single commit: 1-2 minutes
- Multiple atomic commits (2-5): 3-5 minutes
- Complex split (6+): 5-10 minutes

**Verification:**
- All commits verified with git log
- Accounting enforced: created commits = planned commits
- Conventional commits format validated

---

## Purpose

Generate high-quality semantic commit messages, recommend atomic commit splits, and improve git workflow quality (Pain #5: Git quality).

---

## CRITICAL: No Hardcoded Examples

**AI models interpret hardcoded examples as real data. Use placeholders and generate from actual changes.**

```python
# ❌ BAD: Hardcoded example commit message
message = "feat(auth): add JWT authentication"

# ✅ GOOD: Generated from actual changes
message = f"{commit_type}({scope}): {summary_from_actual_changes}"
```

**All commit messages, file lists, and summaries must be generated from actual git diff output.**

**Template:**
```
{commit_type}({scope_from_actual_files}): {summary_from_actual_changes}

- {change_1_from_diff}
- {change_2_from_diff}
- {impact_from_analysis}

Refs: #{issue_number_if_provided}
```

---

## Skills Used

- `cco-skill-git-branching-pr-review`
- `cco-skill-versioning-semver-changelog-compat`

---

## Step 0: Introduction and Confirmation

**Pattern:** Pattern 1 (Step 0 Introduction)

**Command-Specific Details:**

**What I do:**
Help you create high-quality git commits following Conventional Commits format per `cco-skill-git-branching-pr-review`.

**Process:**
1. Analyze ALL uncommitted changes (staged, unstaged, untracked files)
2. Detect change types and recommend atomic splits
3. Generate semantic commit messages following skill guidelines (title max 50 chars)
4. Create commits with Conventional Commits format

**Output:**
- Semantic messages following Conventional Commits format
- Proper type/scope classification
- Clear summary and detailed body
- Issue references and co-authors (if provided)

**Time:** 1-5 minutes depending on changes

```python
AskUserQuestion({
  questions: [{
    question: "Ready to create semantic commits from all uncommitted changes?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {
        label: "Start Commit",
        description: "Analyze ALL uncommitted changes (staged/unstaged/untracked) and create commits (recommended)"
      },
      {
        label: "Add Context",
        description: "Provide additional context before analysis (e.g., co-authors, issue refs)"
      },
      {
        label: "Cancel",
        description: "Exit cco-commit"
      }
    ]
  }]
})
```

---

## Design Principles

**See:** STANDARDS_QUALITY.md
- UX/DX principles (transparency, progressive disclosure, zero surprises)
- Honesty & accurate reporting (no false positives/negatives)
- No hardcoded examples (use placeholders: `{FILE_PATH}`, `{LINE_NUMBER}`)

---

## Execution Protocol

### Step 1: Analyze All Uncommitted Changes

**Pattern:** Pattern 7 (File Discovery)

**File Discovery with Exclusion Protocol:**

```bash
# Get ALL uncommitted files (staged, unstaged, untracked)
all_changes=$(git status --short)

# Separate file types:
# - Modified (staged/unstaged): M, MM, AM
# - Deleted: D
# - Untracked: ??
# - Renamed: R

# Define exclusion patterns (match STANDARDS_COMMANDS.md)
EXCLUDED_FILES=(
    "*.pyc" "*.pyo" "*.so" "*.dll" "*.class" "*.o"
    "*.min.js" "*.min.css" "*.bundle.js"
    "package-lock.json" "yarn.lock" "poetry.lock"
    ".env" ".env.*" "*secret*" "*credential*" "*.pem"
)

# Filter excluded files
# Analyze ALL changes (staged + unstaged + untracked):
git diff HEAD --stat -- $filtered_files  # Staged + unstaged
git ls-files --others --exclude-standard  # Untracked
git diff HEAD -- $filtered_files  # Detailed diff
```

**Analysis (on filtered files only):**
- Files changed and line counts
- Types of changes (feature, fix, refactor, docs)
- Related vs unrelated changes
- Breaking changes

**Display Included/Excluded:**
```markdown
════════════════════════════════════════════════════════════════
         ALL UNCOMMITTED CHANGES ANALYSIS
════════════════════════════════════════════════════════════════

## Files Included (Staged + Unstaged + Untracked)
{for file in included_files}
✅ {file} ({status}) (+{added} -{removed})
   Status: M=modified, ??=untracked, D=deleted, R=renamed

Total: {included_count} files

## Files Excluded (Not Committed)
{for file in excluded_files}
❌ {file} (excluded by pattern: {pattern})

Total: {excluded_count} files
════════════════════════════════════════════════════════════════
```

### Step 2: Recommend Atomic Commits

If multiple change types detected:
```markdown
Analyzing uncommitted changes (staged + unstaged + untracked)...

Files changed: {COUNT}
Lines added: {COUNT}
Lines removed: {COUNT}

Detected changes:
- {CHANGE_TYPE_1} ({ACTUAL_FILES})
- {CHANGE_TYPE_2} ({ACTUAL_FILES})
- {CHANGE_TYPE_3} ({ACTUAL_FILES})

Recommendation: Split into {N} atomic commits

{For each detected change type:}
Commit {N}: {CHANGE_TYPE}
Files: {ACTUAL_FILES from analysis}
Type: {type}({scope})

AskUserQuestion({
  questions: [{
    question: "Proceed with atomic commit split?",
    header: "Commit Split",
    multiSelect: false,
    options: [
      {label: "Yes", description: "Create atomic commits as suggested"},
      {label: "No", description: "Single commit for all changes"},
      {label: "Customize", description: "Modify commit grouping"}
    ]
  }]
})
```

### Step 3: Generate Semantic Commit Messages

**See:**
- **[LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md#pattern-8-dynamic-results-generation)** for template
- **`cco-skill-git-branching-pr-review`** for commit message format rules

For each commit, generate message following Conventional Commits **and skill guidelines**:

```
<type>(<scope>): <subject>  ← MAX 50 CHARS (see skill)

<body wrapped at 72 chars>
Explain WHAT and WHY, not HOW.

BREAKING CHANGE: <description if applicable>
Refs: #<issue-number>
```

**CRITICAL:** Title must be ≤50 chars (ideal) or ≤72 (hard limit) per `cco-skill-git-branching-pr-review`.

### Step 4: Create Commits

```bash
# Stage files for commit {N}
git reset
git add {ACTUAL_FILES for this commit}

# Create commit {N}
git commit -m "$(cat <<'EOF'
{type}({scope}): {summary from actual changes}

- {Specific change 1}
- {Specific change 2}
- {Impact description}

Refs: #{issue-number if applicable}
EOF
)"
```

### Multi-Commit Tracking with TodoWrite

**Pattern:** Pattern 3 (Progress Reporting)

```python
# When creating multiple atomic commits
if commit_count > 1:
    todos = []
    for i, commit_plan in enumerate(commit_plans, 1):
        todos.append({
            "content": f"Create commit {i}/{commit_count}: {commit_plan.type}({commit_plan.scope})",
            "status": "pending",
            "activeForm": f"Creating commit {i}/{commit_count}"
        })
    TodoWrite(todos)
```

### Step 5: Summary with Complete Accounting

**Pattern:** Pattern 4 (Complete Accounting)

**Command-Specific Details:**

**Accounting formula enforced:** `total_commits = planned_commits`

**Real metrics (no placeholders):**

```markdown
Created {total_commits} atomic commits:

{for commit in created_commits}
✓ {commit.type}({commit.scope}): {commit.summary}
  Files: {commit.files}
  Lines: +{commit.added} / -{commit.removed}

**Accounting Verification:**
- Planned commits: {planned_commits}
- Created commits: {created_commits}
- **Verification**: {created_commits} = {planned_commits} ✓

Impact:
- Git workflow score: {BEFORE} → {AFTER}
- Addresses Pain #5 (better git practices)
- Benefits: Easier review, better history, simpler rollbacks

Next:
- Push: git push origin {ACTUAL_BRANCH}
- Create PR: gh pr create
```

---

## Agent Error Handling

**Pattern:** Pattern 5 (Error Handling)

**Command-Specific Handling:**

**Git Error Handling:**

If commit fails:

```python
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
```

**If too many changes detected:**

```python
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

- [ ] Step 0: Introduction and confirmation completed
- [ ] ALL uncommitted changes analyzed (staged/unstaged/untracked, excluded files filtered)
- [ ] Change types detected
- [ ] Atomic split recommended if needed (dynamic based on analysis)
- [ ] Semantic messages generated following `cco-skill-git-branching-pr-review` (title ≤50 chars, no hardcoded examples)
- [ ] TodoWrite tracking for multi-commit operations
- [ ] Commits created with proper format per skill guidelines
- [ ] Complete accounting verified (created = planned)
- [ ] Summary presented with impact metrics
- [ ] Pain-point impact communicated

---

## Example Usage

```bash
# Analyze ALL uncommitted changes (staged/unstaged/untracked) and create commits
/cco-commit

# The command automatically detects all uncommitted changes:
# - Staged files (git add)
# - Unstaged modified files
# - Untracked new files
# No need to stage beforehand - cco-commit handles everything
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
