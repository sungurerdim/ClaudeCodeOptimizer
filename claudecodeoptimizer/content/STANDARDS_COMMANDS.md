# CCO Command Standards

**All CCO commands MUST follow these standards for consistency, UX/DX optimization, and maintainability.**

---

## 1. Execution Guarantee

**Every command that performs work MUST include this section after the description:**

```markdown
## Execution Guarantee

This command executes the FULL operation as planned.
No scope reduction due to time constraints or "workload concerns".

**Estimated time: Provided for transparency, NOT to reduce scope.**
```

**Purpose:** Sets user expectation that commands complete fully, time estimates are informational only.

**Applies to:** audit, fix, generate, slim, optimize, implement

**Does NOT apply to:** status, help, remove, commit (utility commands)

---

## 2. Introduction and Confirmation (Step 0)

**Every command MUST start with user-facing introduction and confirmation:**

```markdown
## Execution Protocol

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# [Command Name] Command

**What I do:**
[1-2 sentence description of command purpose]

**How it works:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]
5. [Step 5]

**What you'll get:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]
- [Benefit 4]

**Time estimate:** [X]-[Y] minutes depending on [factor]

**[Warning if applicable]:** Changes WILL be made / New files WILL be created / etc.
```

**Then ask for confirmation using AskUserQuestion:**

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start [command action]?",
    header: "Start [Command]",
    multiSelect: false,
    options: [
      {
        label: "Yes, start [action]",
        description: "[What will happen]"
      },
      {
        label: "No, cancel",
        description: "Exit without [doing anything]"
      }
    ]
  }]
})
```

**CRITICAL:**
- If user selects "No, cancel" → EXIT immediately, do NOT proceed
- If user selects "Yes, start [action]" → Continue to Step 0.5 or Step 1
```

**Purpose:** Transparency, user control, no surprises.

**Applies to:** ALL commands except status, help

---

## 2.5. Native UI Tools for ALL User Interactions

**CRITICAL RULE: Every user interaction MUST use AskUserQuestion tool.**

**This applies to:**
- ✅ Step 0 Introduction confirmation
- ✅ Mode/category selection
- ✅ Pre-flight confirmation
- ✅ Error recovery decisions
- ✅ Mid-execution choices
- ✅ ANY question asked to user

**NEVER use text-based prompts:**

```python
# ❌ FORBIDDEN: Text-based prompts
print("Ready to proceed with context optimization?")
print("Do you want to continue? (y/n)")
print("Select option (1/2/3):")
print("""
Choose mode:
- Conservative
- Balanced
- Aggressive
""")

# ✅ REQUIRED: AskUserQuestion
AskUserQuestion({
  questions: [{
    question: "Ready to proceed with context optimization?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {label: "Yes", description: "Start optimization process"},
      {label: "No", description: "Cancel operation"}
    ]
  }]
})
```

**Why this matters:**
- Text-based prompts break UX flow
- No validation, accessibility, or consistency
- Manual parsing required
- Not cross-platform compatible
- Poor user experience

**Enforcement:**
- Grep check: No patterns like "Ready to", "Do you want", "Select option", "(y/n)", "Choose"
- All user decisions via AskUserQuestion with proper options
- MultiSelect questions MUST include "All" option

**See also:** C_NATIVE_TOOL_INTERACTIONS principle in ~/.claude/principles/

---


## 3. File Discovery Protocol

**Every command that processes files MUST apply filters BEFORE any analysis:**

```markdown
## File Discovery Protocol

**CRITICAL: Apply file filters BEFORE any analysis/processing begins.**

### Excluded Directories (Never process):
```python
EXCLUDED_DIRS = [
    # Version Control
    ".git", ".github/workflows", ".hg", ".svn",

    # Dependencies
    "node_modules", "venv", ".venv", "env", ".env",
    "__pycache__", "site-packages",

    # Tool Caches
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
    ".coverage", ".hypothesis", ".benchmarks",

    # Build Artifacts
    "build", "dist", "*.egg-info", ".eggs",
    "out", "target", "bin", "obj",

    # Temporary Files
    "cache", "tmp", "temp", ".temp", ".cache",

    # IDE/Editor
    ".vscode", ".idea", ".vs", "*.swp", "*.swo",

    # OS Files
    ".DS_Store", "Thumbs.db", "desktop.ini",
]
```

### Excluded Files (Never read):
```python
EXCLUDED_FILES = [
    # Secrets
    ".env*", "credentials*", "secrets*", "*.key", "*.pem", "*.p12",
    "*.pfx", "*.jks", "*.keystore",

    # Compiled
    "*.pyc", "*.pyo", "*.so", "*.dll", "*.dylib", "*.exe",
    "*.o", "*.a", "*.lib", "*.class", "*.jar",

    # Minified/Bundled
    "*.min.js", "*.min.css", "bundle.js", "*.bundle.*",

    # Logs/Backups
    "*.log", "*.bak", "*.swp", "*.swo", "*.tmp",

    # Lock Files
    "package-lock.json", "yarn.lock", "poetry.lock", "Pipfile.lock",
]
```

### Implementation Template:
```python
import os
from pathlib import Path

def discover_files(root_dir: str, include_patterns: list[str]) -> list[Path]:
    """
    Discover files with exclusion BEFORE processing.

    Args:
        root_dir: Root directory to search
        include_patterns: File patterns to include (e.g., ["*.py", "*.js"])

    Returns:
        List of Path objects for files to process
    """
    files_to_process = []
    total_found = 0
    excluded_count = 0

    for root, dirs, files in os.walk(root_dir):
        # Exclude directories IN-PLACE (prevents os.walk from entering them)
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith('.')]

        for file in files:
            total_found += 1
            file_path = Path(root) / file

            # Skip excluded files
            if any(file.endswith(pattern) or file.startswith(pattern.rstrip('*'))
                   for pattern in EXCLUDED_FILES):
                excluded_count += 1
                continue

            # Include only matching patterns
            if any(file_path.match(pattern) for pattern in include_patterns):
                files_to_process.append(file_path)
            else:
                excluded_count += 1

    # Report counts
    print(f"**Total files found:** {total_found}")
    print(f"**Files to process:** {len(files_to_process)}")
    print(f"**Files excluded:** {excluded_count} ({excluded_count/total_found*100:.1f}%)")

    return files_to_process
```

### Included File Types (Process these):
[Command-specific: e.g., `*.py`, `*.js`, `*.ts`, `*.go`, `*.java`, `*.md`, etc.]

### File Count Verification:
After filtering, report:
- **Total files found:** {COUNT}
- **Files to process:** {COUNT}
- **Files excluded:** {COUNT} ({PERCENTAGE}%)
```

**Purpose:** Performance, security, avoid processing unnecessary files.

**Applies to:** audit, fix, generate, slim, optimize

---

## 4. Project Context Discovery (Step 0.5 - Optional)

**Commands that benefit from project context SHOULD offer this:**

```markdown
### Step 0.5: Project Context Discovery (Optional)

**Ask user if they want project documentation analyzed for better [command goal] alignment.**

```python
AskUserQuestion({
  questions: [{
    question: "Extract context from project documentation?",
    header: "Project Context",
    multiSelect: false,
    options: [
      {
        label: "Yes (recommended)",
        description: "Extract [relevant context] from README/CONTRIBUTING, [benefit]"
      },
      {
        label: "No",
        description: "[Command action] only (faster)"
      }
    ]
  }]
})
```

**If "Yes" selected:**

```python
# Extract project context via Haiku sub-agent
context_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Extract project context summary (MAX 200 tokens).
    Focus on: [command-specific context needs]

    Files to check: README.md, CONTRIBUTING.md, ARCHITECTURE.md, docs/ADR/*.md

    Return: [Command-specific summary format]
    """
})

# Use context in [command execution]
project_context = context_result
```

**Benefits:** [Command-specific benefits]
```

**Purpose:** Context-aware operations, respect existing conventions.

**Applies to:** audit, fix, generate, implement (recommended), optimize (optional)

---

## 5. Concise Reporting

**All reports MUST be concise and user-friendly:**

### Summary Format (Always show):
```markdown
## [Phase/Section] Summary

**[Metric 1]:** {VALUE}
**[Metric 2]:** {VALUE}
**[Metric 3]:** {VALUE}

[2-3 sentences of interpretation]
```

### Detailed Format (On request only):
- Use collapsible sections (where supported)
- Paginate long lists
- Provide "Show more" options

### Progress Updates:
- Show milestones, not every step
- Use percentage/progress bars
- Keep to 1 line per update

**Anti-pattern:** Verbose phase announcements, unnecessary details, redundant information

---

## 6. No Unnecessary `cd` in Root Directory

**NEVER cd to project root directory when already there:**

```bash
# ❌ BAD: Redundant cd (already in working directory)
cd /path/to/project && ruff check .

# ✅ GOOD: Direct execution
ruff check .
```

**Purpose:** Cleaner commands, follows cross-platform compatibility principles.

---

## 7. Maximum Parallelization

**Use parallel Task() calls whenever possible:**

```python
# ❌ BAD: Sequential (slow)
Task("Analyze module A", model="haiku")
# Wait for result
Task("Analyze module B", model="haiku")
# Wait for result
Task("Analyze module C", model="haiku")

# ✅ GOOD: Parallel (single message, all run simultaneously)
Task("Analyze module A", model="haiku")
Task("Analyze module B", model="haiku")
Task("Analyze module C", model="haiku")
# All run in parallel, significantly faster
```

**Purpose:** Performance, cost-efficiency, better UX.

---

## 8. Agent Permissions

**All agents used in commands are pre-approved:**

```markdown
### Agents Used

- **audit-agent** (subagent_type: "Explore", model: "haiku") - Fast scanning
- **fix-agent** (subagent_type: "general-purpose", model: "sonnet") - Accurate fixes
- **generate-agent** (subagent_type: "general-purpose", model: "sonnet") - Quality generation
- **optimize-context-usage-agent** (subagent_type: "general-purpose", model: "haiku") - Token optimization

All agents use existing global/project permissions (no additional approval needed).
```

**Purpose:** Smooth UX, no unexpected permission prompts.

---

## 9. TodoWrite Usage

**Use TodoWrite for progress tracking in multi-step commands:**

```python
# At command start
TodoWrite([
    {"content": "Phase 1: [Description]", "status": "in_progress", "activeForm": "[Doing...]"},
    {"content": "Phase 2: [Description]", "status": "pending", "activeForm": "[Doing...]"},
    {"content": "Phase 3: [Description]", "status": "pending", "activeForm": "[Doing...]"}
])

# Mark complete IMMEDIATELY after each phase
TodoWrite([...update Phase 1 to "completed", Phase 2 to "in_progress"...])
```

**Purpose:** User visibility, progress tracking, professionalism.

**Applies to:** All multi-phase commands (audit, fix, generate, slim, optimize, implement)

---

## 10. No Hardcoded Examples

**NEVER use hardcoded file paths, function names, or data in examples:**

```python
# ❌ BAD: Hardcoded (AI interprets as real)
"file": "src/auth/login.py"
"line": 45
"function": "authenticate()"

# ✅ GOOD: Placeholders
"file": "{FILE_PATH}"
"line": "{LINE_NUMBER}"
"function": "{FUNCTION_NAME}"
```

**Purpose:** Prevents AI from using fake data as real findings.

---

## 11. Dynamic Option Generation

**Generate AskUserQuestion options from REAL project analysis:**

```python
# ❌ BAD: Hardcoded options
options: [
  {label: "Fix auth.py SQL injection", description: "..."}
]

# ✅ GOOD: Generated from actual findings
for finding in actual_findings:
    options.append({
        label: f"Fix {finding.file} {finding.issue}",
        description: f"({finding.severity}) {finding.description}"
    })
```

**Purpose:** Accuracy, relevance, user trust.

---

## 12. Complete Accounting

**Every command MUST account for ALL items:**

```python
Formula: total = completed + skipped + failed + cannot_do

# Report MUST balance
assert len(completed) + len(skipped) + len(failed) + len(cannot_do) == total_items
```

**Purpose:** Honesty, no lost work, complete transparency.

---

## 13. Token Optimization

**Optimize context usage via targeted reads, strategic model selection, and three-stage discovery:**

### Three-Stage File Discovery

**Stage 1: Discovery** (files_with_matches) → Find which files
```python
Grep("JWT.*authenticate", output_mode="files_with_matches")
# → auth/jwt.py, middleware/auth.py (~10 tokens)
```

**Stage 2: Preview** (content with context) → Verify relevance
```python
Grep("JWT.*authenticate", path="auth/jwt.py",
     output_mode="content", "-C": 5, "-n": true)
# → Line 149 with context (~100 tokens)
```

**Stage 3: Precise Read** (offset+limit) → Read exact section
```python
Read("auth/jwt.py", offset=145, limit=20)
# → Lines 145-165 (~50 tokens)
# Total: ~160 tokens vs 5000+ with full reads (31x better)
```

### Agent Prompt Optimization

```python
# ❌ BAD: Vague, verbose prompt (wastes tokens)
Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Please analyze the authentication module and find all the places
    where JWT tokens are validated. Look through all the files and
    give me a comprehensive report about what you find...
    """ # 200+ tokens
})

# ✅ GOOD: Precise, structured prompt (minimal tokens)
Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Find JWT validation in auth/ module.
    Return: file:line format only.
    """ # 15 tokens
})
```

### Targeted File Reads

```python
# ❌ BAD: Read entire file
Read("large_module.py")  # 1200 lines = 3000+ tokens

# ✅ GOOD: Targeted read
Read("large_module.py", offset=150, limit=30)  # 30 lines = 75 tokens
```

### Model Selection for Cost

```python
# ❌ EXPENSIVE: Sonnet for simple tasks
Task("Count Python files", model="sonnet")  # $$$

# ✅ OPTIMIZED: Haiku for simple tasks
Task("Count Python files", model="haiku")  # $
```

### Parallel Operations

```python
# ❌ SLOW: Sequential (3x time, 3x messages)
Read("module1.py")  # Wait
Read("module2.py")  # Wait
Read("module3.py")  # Wait

# ✅ FAST: Parallel (single message)
Read("module1.py")
Read("module2.py")
Read("module3.py")
# All execute simultaneously
```

**Purpose:** Maximum efficiency with minimal context consumption.

**Applies to:** All commands

---

## 14. Cross-Platform Compatibility

**Ensure commands work on Windows, Linux, and macOS:**

### Path Handling

```bash
# ❌ BAD: Backslashes (Windows-only)
cd C:\Users\Developer\project

# ✅ GOOD: Forward slashes (cross-platform)
cd C:/Users/Developer/project
```

### Quote Paths with Spaces

```bash
# ❌ BAD: Unquoted
cd C:/Program Files/MyApp  # Fails!

# ✅ GOOD: Quoted
cd "C:/Program Files/MyApp"
```

### No Redundant cd to Working Directory

```bash
# Working directory: D:/GitHub/MyProject

# ❌ BAD: Redundant cd (already there!)
cd "D:/GitHub/MyProject" && ruff check .
cd "D:/GitHub/MyProject" && pytest tests/

# ✅ GOOD: Direct execution
ruff check .
pytest tests/
```

### Use Git Bash Commands

```bash
# ✅ Available via Git Bash (cross-platform)
ls -la
grep "pattern" file.txt
cat config.json
find . -name "*.py"

# ❌ Avoid CMD-specific
dir /s /b
copy src\*.py dest\

# ❌ Avoid PowerShell-specific
Get-ChildItem -Recurse
```

### Absolute Paths for Other Directories

```bash
# ❌ BAD: cd to different directory from working dir
cd ../OtherProject && pytest tests/

# ✅ GOOD: Absolute path (no cd needed)
pytest D:/GitHub/OtherProject/tests/
```

**Purpose:** Consistent behavior across all platforms.

**Applies to:** All commands

---

## 15. Error Handling

**Standardized error handling templates for common scenarios:**

### Agent Error Template

```python
try:
    result = Task({
        subagent_type: "Explore",
        model: "haiku",
        prompt: "..."
    })
except Exception as e:
    # Ask user how to proceed
    AskUserQuestion({
        questions: [{
            question: "Agent task failed. How to proceed?",
            header: "Error Recovery",
            multiSelect: false,
            options: [
                {
                    label: "Retry",
                    description: "Run agent task again"
                },
                {
                    label: "Skip",
                    description: "Continue without this task"
                },
                {
                    label: "Abort",
                    description: "Stop entire operation"
                }
            ]
        }]
    })
```

### Git Error Template

```python
# Before git operations
git_status = Bash("git status --porcelain")

if git_status.exit_code != 0:
    print("**Warning:** Not a git repository or git not available.")
    AskUserQuestion({
        questions: [{
            question: "Git not available. Continue without version control?",
            header: "Git Warning",
            multiSelect: false,
            options: [
                {label: "Yes", description: "Proceed without git"},
                {label: "No", description: "Abort operation"}
            ]
        }]
    })
```

### File Operation Error Template

```python
try:
    Read(file_path)
except FileNotFoundError:
    print(f"**Skipped:** {file_path} (not found)")
    skipped.append((file_path, "File not found"))
    # Continue to next file
except PermissionError:
    print(f"**Failed:** {file_path} (permission denied)")
    failed.append((file_path, "Permission denied"))
    # Continue to next file
```

**Purpose:** Graceful degradation, user control over error recovery.

**Applies to:** All commands

---

## 16. Model Selection Guide

**Choose appropriate Claude model based on task complexity:**

### Decision Matrix

| Task Type | Complexity | Model | Reason |
|-----------|-----------|-------|--------|
| File search, grep, ls | Mechanical | **Haiku** | Fast, cheap, no reasoning needed |
| Format, lint, count | Mechanical | **Haiku** | Simple transformations |
| Read docs, summarize | Low | **Haiku** | Information extraction |
| Add feature, fix bug | Medium | **Sonnet** | Requires understanding + changes |
| Code review, refactor | Medium | **Sonnet** | Requires judgment |
| Architecture design | High | **Auto** | Let Claude decide |
| Complex algorithms | High | **Auto** | Let Claude decide |

### Cost Optimization Pattern

```python
# ❌ BAD: Specifying model for non-mechanical tasks
Task("Find Python files", model="haiku")     # Fast, cheap
Task("Add validation logic")                  # Let Claude decide
Task("Design microservices")                  # Let Claude decide

# ✅ OPTIMIZED: Right model for task
Task("Find Python files", model="haiku")     # Cheap, fast
Task("Add validation logic", model="sonnet") # Balanced
Task("Design microservices")                  # Let Claude decide
```

### Parallel Execution with Model Selection

```python
# Analyze 10 modules in parallel (fast + cheap)
Task("Analyze module 1", model="haiku")
Task("Analyze module 2", model="haiku")
Task("Analyze module 3", model="haiku")
# ... 10 tasks in single message
# Significantly faster with parallel execution
```

**Purpose:** Optimize cost/performance ratio.

**Applies to:** All commands using Task()

---

## 17. Anti-Patterns

**Common mistakes to AVOID:**

### 1. Processing Excluded Files

```python
# ❌ BAD: Filter AFTER reading
all_files = glob("**/*.py")
for file in all_files:
    content = Read(file)
    if "node_modules" not in file:  # Too late!
        analyze(content)

# ✅ GOOD: Filter BEFORE reading
files = discover_files(".", ["*.py"])  # Excludes node_modules
for file in files:
    content = Read(file)
    analyze(content)
```

### 2. Verbose Output

```python
# ❌ BAD: Pages of intermediate info
print("=" * 80)
print("STARTING PHASE 1: DISCOVERY")
print("=" * 80)
print("Now searching for Python files...")
print("Found file: module1.py")
print("Found file: module2.py")
# ... 100 more lines

# ✅ GOOD: Concise summary
print("**Phase 1:** Discovery - Found 102 Python files")
```

### 3. Sequential Execution

```python
# ❌ BAD: Sequential (slow)
Task("Analyze module A", model="haiku")  # Wait
Task("Analyze module B", model="haiku")  # Wait

# ✅ GOOD: Parallel (fast)
Task("Analyze module A", model="haiku")
Task("Analyze module B", model="haiku")
# Single message, both run simultaneously
```

### 4. Hardcoded Examples in Templates

```python
# ❌ BAD: AI interprets as real data
"file": "src/auth/login.py"  # AI thinks this file exists!
"line": 45

# ✅ GOOD: Placeholders
"file": "{FILE_PATH}"
"line": "{LINE_NUMBER}"
```

### 5. Inconsistent Counts

```python
# ❌ BAD: Different calculations
print(f"Found {len(critical_issues)} critical")  # One calculation
print(f"Total: {security + testing}")            # Different calculation

# ✅ GOOD: Single source of truth
total = len(all_issues)
print(f"Found {len(critical_issues)} critical")
print(f"Total: {total}")
```

### 6. No Error Handling

```python
# ❌ BAD: Unhandled errors crash command
result = Task("Analyze codebase", model="haiku")
# If Task fails, command crashes

# ✅ GOOD: Graceful degradation
try:
    result = Task("Analyze codebase", model="haiku")
except Exception as e:
    # Ask user how to proceed
    AskUserQuestion({...})
```

**Purpose:** Learn from common mistakes, maintain quality.

**Applies to:** All commands

---

## 18. Command Discovery Protocol

**How Skills Expose Commands:**

Skills declare which commands are relevant via frontmatter metadata:

```yaml
# Example: cco-skill-security-owasp-xss-sqli-csrf.md
---
name: security-owasp-xss-sqli-csrf
description: Prevent OWASP Top 10 vulnerabilities...
keywords: [security, OWASP, XSS, SQL injection, CSRF, auth]
category: security
related_commands:
  action_types: [audit, fix, generate]
  categories: [security]
  pain_points: [1, 2, 3]
---
```

**Discovery Mechanism:**

When a skill is active, CCO automatically discovers relevant commands:

1. **Keyword Matching**: Grep command files for `keywords:` in frontmatter
   ```bash
   grep -l "keywords:.*security" ~/.claude/commands/*.md
   ```

2. **Category Matching**: Filter by `category:` and `action_types:`
   ```python
   if skill.category in command.categories and
      any(action in command.action_types for action in skill.related_commands.action_types):
       commands.append(command)
   ```

3. **Pain Point Alignment**: Match `pain_points:` (1=AI Tech Debt, 2=AI Quality, 3=Security, etc.)

4. **Present to User**: Show matching commands with their parameters and descriptions

**Benefits:**

- Commands are always current (no hardcoded lists)
- Skills and commands loosely coupled via metadata
- New commands automatically discovered if metadata matches
- Commands can be renamed/moved without breaking skills

**Implementation:**

Commands and skills use frontmatter metadata, not hardcoded references. CCO runtime handles discovery dynamically.

**Applies to:** All skills and commands

---

## Compliance Checklist

Before finalizing any command, verify compliance across these categories:

### 1. User Experience & Flow
- [ ] Execution Guarantee section (if applicable)
- [ ] Introduction and Confirmation (Step 0)
- [ ] Project Context Discovery offered (if applicable)
- [ ] Concise reporting (summary format, not verbose)
- [ ] TodoWrite for multi-phase progress tracking

### 2. File & Resource Management
- [ ] File Discovery Protocol with EXCLUDED_DIRS/EXCLUDED_FILES
- [ ] Exclusion filters applied BEFORE processing
- [ ] File count verification (total/process/excluded)
- [ ] No unnecessary file creation

### 3. Performance & Efficiency
- [ ] Token Optimization (three-stage discovery)
- [ ] Maximum parallelization (Task calls in single message)
- [ ] Appropriate model selection (Haiku for mechanical, omit for complex)
- [ ] Agent prompt optimization (concise, structured)

### 4. Cross-Platform & Compatibility
- [ ] Forward slashes in paths (not backslashes)
- [ ] No redundant `cd` to working directory
- [ ] Git Bash compatible commands
- [ ] Quoted paths with spaces

### 5. Data Quality & Accuracy
- [ ] No hardcoded examples (use {PLACEHOLDERS})
- [ ] Dynamic option generation from real data
- [ ] Complete accounting formula verified (total = completed + skipped + failed + cannot_do)
- [ ] Single source of truth for counts

### 6. Robustness & Error Handling
- [ ] Agent permissions documented
- [ ] Error handling templates used
- [ ] Graceful degradation on failures
- [ ] User control over error recovery

---

**These standards ensure consistency, excellent UX/DX, and maintainability across all CCO commands.**
