# CCO Agent Standards - Built-in Behaviors

**Purpose:** Define standard behaviors that ALL CCO agents inherit automatically.

**DRY Principle:** Define once, reference everywhere. Agents simply reference this file instead of duplicating content.

---

## How to Use in Agent Files

```markdown
---
name: {agent-name}
description: {One-line description}
tools: {tool-list}
model: {haiku|sonnet|opus}
---

# {Agent Name}

**Purpose:** {One sentence}

**Built-in Behaviors:** See [AGENT_STANDARDS.md](../AGENT_STANDARDS.md) for:
- File Discovery & Exclusion (Stage 0)
- Three-Stage File Discovery
- Model Selection Guidelines
- Parallel Execution Patterns
- Evidence-Based Verification
- Cross-Platform Compatibility

---

{Agent-specific content here}
```

---

## Built-in Behavior 1: File Discovery & Exclusion

**Principle:** C_EFFICIENT_FILE_OPERATIONS (Stage 0)

**What:** Apply exclusions BEFORE processing any files to avoid wasted effort.

### Standard Exclusion Lists

```python
# Directories to ALWAYS exclude
EXCLUDED_DIRS = [
    ".git",           # Version control
    "node_modules",   # Node.js dependencies
    "venv", ".venv",  # Python virtual environments
    "__pycache__",    # Python cache
    ".pytest_cache",  # Test cache
    "dist", "build",  # Build artifacts
    ".next", ".nuxt", # Framework build dirs
    "target",         # Rust/Java build
    "bin", "obj",     # .NET build
    ".egg-info",      # Python package metadata
    "coverage",       # Test coverage reports
    ".tox", ".nox",   # Python testing
]

# Files to ALWAYS exclude
EXCLUDED_FILES = [
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",  # Node.js locks
    "poetry.lock", "Pipfile.lock", "Gemfile.lock",       # Other locks
    "*.min.js", "*.min.css",  # Minified assets
    "*.map",                   # Source maps
    "*.pyc", "*.pyo",         # Python bytecode
    "*.so", "*.dll", "*.dylib", # Compiled binaries
    "*.exe", "*.bin",         # Executables
    "*.log",                  # Log files
]
```

### Implementation Pattern

```python
def discover_files(root_dir: str) -> Tuple[List[str], List[str]]:
    """
    Discover files with exclusions applied FIRST.

    Returns:
        (included_files, excluded_files)
    """
    all_files = Glob("**/*", path=root_dir)
    included = []
    excluded = []

    for file in all_files:
        if should_exclude_path(file):
            excluded.append(file)
        else:
            included.append(file)

    return included, excluded

def should_exclude_path(path: str) -> bool:
    """Check if path should be excluded."""
    path_parts = Path(path).parts

    # Check directory exclusions
    for excluded_dir in EXCLUDED_DIRS:
        if excluded_dir in path_parts:
            return True

    # Check file exclusions
    filename = Path(path).name
    for pattern in EXCLUDED_FILES:
        if fnmatch.fnmatch(filename, pattern):
            return True

    return False
```

### Reporting Pattern

```markdown
Files discovered: {total_found}
Files included: {len(included)} ({percentage_included}%)
Files excluded: {len(excluded)} ({percentage_excluded}%)
```

---

## Built-in Behavior 2: Three-Stage File Discovery

**Principle:** C_EFFICIENT_FILE_OPERATIONS

**What:** Progressive refinement to minimize token usage.

### Three Stages

```python
# Stage 1: Discovery - Which files contain the pattern?
files_with_pattern = Grep(
    "pattern",
    output_mode="files_with_matches"
)
# Token cost: ~10 tokens per 100 files

# Stage 2: Preview - Is this file relevant?
for file in files_with_pattern:
    preview = Grep(
        "pattern",
        path=file,
        output_mode="content",
        "-C": 3,  # 3 lines context
        "-n": True  # Line numbers
    )
    # Token cost: ~50-100 tokens per file

    if is_relevant(preview):
        relevant_files.append(file)

# Stage 3: Precise Read - Get exact section
for file in relevant_files:
    # Extract line number from preview
    start_line = extract_line_number(preview)

    content = Read(
        file,
        offset=start_line - 5,  # 5 lines before
        limit=20  # 20 lines total
    )
    # Token cost: ~40-80 tokens per section
```

### Token Savings

```
Traditional (read all files): ~5000 tokens
Three-stage discovery: ~120 tokens
Savings: 42x reduction (98% less tokens)
```

---

## Built-in Behavior 3: Model Selection Guidelines

**Principle:** C_AGENT_ORCHESTRATION_PATTERNS, C_MODEL_SELECTION

**What:** Choose the right model for each task type.

### Model Decision Matrix

| Task Type | Model | Why | Cost |
|-----------|-------|-----|------|
| **Mechanical Tasks** | Haiku | Fast, cheap, sufficient | $0.25/M tokens |
| - File enumeration | Haiku | Pattern matching | Lowest |
| - Grep operations | Haiku | String search | Lowest |
| - Count/stats | Haiku | Simple arithmetic | Lowest |
| - Format/lint | Haiku | Rules-based | Lowest |
| **Balanced Tasks** | Sonnet | Quality/cost balance | $3/M tokens |
| - Code analysis | Sonnet | Semantic understanding | Medium |
| - Bug fixes | Sonnet | Logic reasoning | Medium |
| - Code generation | Sonnet | Pattern application | Medium |
| - Test writing | Sonnet | Coverage reasoning | Medium |
| **Complex Tasks** | Opus | Highest capability | $15/M tokens |
| - Architecture | Opus | Novel design | Highest |
| - Complex algorithms | Opus | Deep reasoning | Highest |
| - Security audits | Opus | Threat modeling | Highest |

### Selection Algorithm

```python
def select_model(task_type: str, complexity: str) -> str:
    """Select appropriate model for task."""

    # Mechanical/repetitive → always Haiku
    if task_type in ["grep", "find", "count", "list", "format"]:
        return "haiku"

    # Novel/architectural → Opus if complex
    if task_type in ["design", "architecture", "algorithm"]:
        return "opus" if complexity == "high" else "sonnet"

    # Default → Sonnet (balanced)
    return "sonnet"
```

---

## Built-in Behavior 4: Parallel Execution Patterns

**Principle:** C_AGENT_ORCHESTRATION_PATTERNS

**What:** Execute independent tasks in parallel for maximum speed.

### Fan-Out Pattern (Independent Tasks)

```python
# ✅ GOOD: Parallel execution (single message, multiple Task calls)
Task("Analyze security", model="sonnet")
Task("Analyze tests", model="sonnet")
Task("Analyze database", model="sonnet")
# Executes in parallel → 3x faster

# ❌ BAD: Sequential execution
Task("Analyze security", model="sonnet")  # Wait for completion
# Then...
Task("Analyze tests", model="sonnet")  # Wait for completion
# Then...
Task("Analyze database", model="sonnet")  # Wait for completion
# Total time: 3x slower
```

### Pipeline Pattern (Dependent Tasks)

```python
# When tasks depend on previous results → sequential
result1 = Task("Discover issues", model="haiku")
# MUST wait for result1...
result2 = Task(f"Fix issues: {result1}", model="sonnet")
# MUST wait for result2...
result3 = Task(f"Verify fixes: {result2}", model="haiku")
```

### Scatter-Gather Pattern

```python
# Scatter: Parallel analysis
security = Task("Security review", model="sonnet")
performance = Task("Performance review", model="sonnet")
quality = Task("Quality review", model="sonnet")

# Gather: Synthesize results
synthesis = Task(
    f"Synthesize reviews: {security}, {performance}, {quality}",
    model="sonnet"
)
```

---

## Built-in Behavior 5: Evidence-Based Verification

**Principle:** U_EVIDENCE_BASED_ANALYSIS

**What:** Never claim completion without verified proof.

### Verification Protocol

```python
class VerificationState:
    """Track all operations with complete accounting."""

    total_items: int = 0
    completed: List[Item] = []
    skipped: List[Tuple[Item, str]] = []  # (item, reason)
    failed: List[Tuple[Item, str]] = []   # (item, reason)

    def verify_accounting(self) -> bool:
        """
        Verify accounting formula.

        Formula: total = len(completed) + len(skipped) + len(failed)
        """
        accounted = len(self.completed) + len(self.skipped) + len(self.failed)
        return accounted == self.total_items

    def get_report(self) -> str:
        """Generate accounting report."""
        return f"""
Total: {self.total_items}
Completed: {len(self.completed)}
Skipped: {len(self.skipped)}
Failed: {len(self.failed)}
Verification: {self.total_items} = {len(self.completed)} + {len(self.skipped)} + {len(self.failed)} ✓
"""
```

### Never Trust Blindly

```python
# ❌ BAD: Trust agent output without verification
agent_result = Task("Fix authentication bug")
# No verification!

# ✅ GOOD: Always verify
agent_result = Task("Fix authentication bug")

# Verify file changed
content = Read("auth.py", offset=145, limit=20)
assert "session['user_id']" in content  # Verify fix applied

# Verify accounting
assert agent_result.total == agent_result.completed + agent_result.skipped

# Run tests
test_result = Bash("pytest tests/test_auth.py -v")
assert "PASSED" in test_result
```

### Outcome Categories

```python
OUTCOMES = {
    # Truly completed
    "fixed": "Change applied AND verified in file",
    "generated": "File created AND exists on disk",
    "completed": "Action performed AND result confirmed",

    # Requires human action
    "needs_decision": "Multiple valid approaches - user must choose",
    "needs_review": "Complex change - requires human verification",

    # Outside tool scope
    "impossible_external": "Issue in third-party code",
    "impossible_design": "Requires architectural redesign",
}
```

---

## Built-in Behavior 6: Cross-Platform Compatibility

**Principle:** U_CROSS_PLATFORM_COMPATIBILITY

**What:** Ensure commands work on Windows, Linux, and macOS.

### Always Use Forward Slashes

```python
# ❌ BAD: Backslashes (Windows-only)
cd C:\Users\Developer\project

# ✅ GOOD: Forward slashes (cross-platform)
cd C:/Users/Developer/project
```

### Use Git Bash Commands

```bash
# ✅ Available via Git Bash (cross-platform)
ls -la
grep "pattern" file.txt
cat config.json
find . -name "*.py"

# ❌ BAD: CMD-specific
dir /s /b
type file.txt

# ❌ BAD: PowerShell-specific
Get-ChildItem -Recurse
```

### Quote Paths with Spaces

```bash
# ❌ BAD: Unquoted
cd C:/Program Files/MyApp  # Fails!

# ✅ GOOD: Quoted
cd "C:/Program Files/MyApp"
```

### Never CD to Current Directory

```bash
# Working directory: D:/GitHub/MyProject

# ❌ BAD: Redundant cd
cd "D:/GitHub/MyProject" && ruff check .
cd "D:/GitHub/MyProject" && pytest tests/

# ✅ GOOD: Direct execution
ruff check .
pytest tests/
```

---

## Agent-Specific Built-in Behaviors

### For Audit Agent (cco-agent-audit)

**Additional behaviors:**
- Real-time progress streaming
- Per-category progress bars
- Explicit phase transitions (START → COMPLETE)
- Score calculation (0-100 per category)

### For Fix Agent (cco-agent-fix)

**Additional behaviors:**
- ALWAYS verify fix applied (Read or git diff)
- Report: fixed/skipped/failed with reasons
- TDD verification (write test before fix)

### For Generate Agent (cco-agent-generate)

**Additional behaviors:**
- Pattern following (U_FOLLOW_PATTERNS)
- Match existing naming, structure, style
- NEVER overwrite existing files without approval

### For Slim Agent (cco-agent-slim)

**Additional behaviors:**
- Quality preservation (semantic meaning MUST be preserved)
- Rollback on degradation
- Syntax validation before acceptance

---

## Verification Checklist

Before claiming ANY agent execution is complete:

- [ ] File exclusions applied (Stage 0)
- [ ] Three-stage discovery used (when reading files)
- [ ] Right model selected (haiku/sonnet/opus)
- [ ] Parallel execution used (when tasks independent)
- [ ] Accounting formula verified (total = completed + skipped + failed)
- [ ] Cross-platform commands used (forward slashes, Git Bash)
- [ ] No cd to current working directory
- [ ] All claims verified with command execution

---

## References

- **Quality Standards:** `COMMAND_QUALITY_STANDARDS.md`
- **Command Patterns:** `COMMAND_PATTERNS.md`
- **Principle Files:** `~/.claude/principles/*.md`

---

**Last Updated:** 2025-01-23
**Version:** 1.0.0
**Status:** Active - All agents MUST comply
