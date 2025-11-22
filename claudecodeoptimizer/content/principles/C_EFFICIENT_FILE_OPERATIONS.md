---
name: efficient-file-operations
description: Optimize file operations via grep-first discovery, content preview, and targeted reads with offset/limit
type: claude
severity: medium
keywords: [file operations, grep-first, token efficiency, search strategy, three-stage discovery]
category: [efficiency, performance]
---

# C_EFFICIENT_FILE_OPERATIONS: Efficient File Operations

**Severity**: Medium

Optimize file operations via grep-first: (1) files_with_matches to discover, (2) content with context to preview, (3) targeted Read with offset+limit for precise editing.

---

## Why

Reading without searching wastes most context. Grep-first delivers significant token savings and faster discovery.

**Problems:**
- Reading many files to find 1 function wastes most context
- Reading full files for small fixes wastes most tokens
- Brute-force can consume excessive tokens when few would suffice

**Strategy:**
```
Stage 0: File Exclusion              → Filter out unnecessary files FIRST
Stage 1: Discovery (files_with_matches) → Find which files
Stage 2: Preview (content + context)     → Verify relevance
Stage 3: Precise Read (offset+limit)     → Read exact section
```

---

## Stage 0: File Exclusion (Apply FIRST)

**CRITICAL**: Filter files BEFORE any processing to avoid wasted effort.

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
    "poetry.lock", "Pipfile.lock", "Gemfile.lock",        # Other locks
    "*.min.js", "*.min.css",  # Minified assets
    "*.map",                   # Source maps
    "*.pyc", "*.pyo",         # Python bytecode
    "*.so", "*.dll", "*.dylib", # Compiled binaries
    "*.exe", "*.bin",         # Executables
    "*.log",                  # Log files
]
```

### Implementation

```python
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

def discover_files(root_dir: str) -> List[str]:
    """Discover files with exclusions applied FIRST."""

    all_files = Glob("**/*", path=root_dir)
    included = []
    excluded = []

    for file in all_files:
        if should_exclude_path(file):
            excluded.append(file)
        else:
            included.append(file)

    # Report counts
    print(f"Included: {len(included)} files")
    print(f"Excluded: {len(excluded)} files")

    return included
```

### Checklist

- [ ] Apply exclusions BEFORE any processing (not during/after)
- [ ] Report included/excluded counts
- [ ] Use standard lists (extend if project-specific)
- [ ] Never process excluded files

---

## Three-Stage File Discovery

### Stage 1: Discovery
```python
Grep("JWT.*authenticate", output_mode="files_with_matches")
# → <auth_module>/<jwt_file>.py, <middleware_module>/<auth_file>.py (~10 tokens)
```

### Stage 2: Preview with Context
```python
Grep("JWT.*authenticate", path="<auth_module>/<jwt_file>.py",
     output_mode="content", "-C": 5, "-n": true)
# → Line 149 with context (~100 tokens)
```

### Stage 3: Precise Read
```python
Read("<auth_module>/<jwt_file>.py", offset=145, limit=20)
# → Lines 145-165 (~50 tokens)
```

---

## Complete Example

```python
# Task: Add rate limiting to JWT auth

# Stage 1: Discovery
Grep("def.*authenticate", output_mode="files_with_matches")
# → <auth_module>/<jwt_file>.py (10 tokens)

# Stage 2: Preview
Grep("def.*authenticate", path="<auth_module>/<jwt_file>.py",
     output_mode="content", "-C": 3, "-n": true)
# → Line 149 (50 tokens)

# Stage 3: Precise read
Read("<auth_module>/<jwt_file>.py", offset=145, limit=30)
# → Lines 145-175 (60 tokens)

# Total: ~120 tokens vs 5000+ with full reads (42x better)
```

---

## Tool Selection for File Modifications

**Choose the right tool based on modification type and risk.**

### Decision Tree

```
File modification?
├─ Simple pattern? → sed/awk (atomic, no locking)
├─ Complex semantic?
│  ├─ <5 files? → Edit tool (verify)
│  └─ 5+ files? → Agent + sed
└─ Agent-driven? → MUST verify output
```

### Tool Comparison

| Tool | Use Case | Pros | Cons |
|------|----------|------|------|
| **sed** | Pattern replacement, line deletion, simple edits | Atomic, no file locking issues, reliable, scriptable | Limited to line-based operations |
| **awk** | Column-based edits, complex patterns | Powerful pattern matching, field processing | Steeper learning curve |
| **Edit tool** | Semantic changes, small edits | Preserves formatting, line number tracking | File locking issues, "unexpectedly modified" errors |
| **Write tool** | Complete file rewrites | Full control | Must Read first, overwrites entire file |
| **Agent + sed** | Bulk modifications | Parallelizable, scalable | Agent output must be verified |

### sed Best Practices

```bash
# ✅ GOOD: In-place edit with backup
```bash
# ✅ In-place with backup
sed -i.bak 's/old/new/g' file.txt

# ✅ Delete lines by pattern
sed -i '/^[[:space:]]*#/d' file.py

# ✅ Multi-line deletion
sed -i '/start/,/end/d' file.txt

# ✅ Test first
sed 's/old/new/g' file.txt  # Preview
sed -i 's/old/new/g' file.txt  # Apply
```

1. **Agent generates sed commands** (not direct edits)
2. **Review commands** before execution
3. **Execute sed commands** with Bash tool
4. **Verify changes** with git diff or Read
5. **Rollback if needed** (git restore or .bak files)

```python
# ❌ BAD: Blindly trust agent edits
**When using agents for file modifications:**

1. Agent generates sed commands (not direct edits)
2. Review commands before execution
3. Execute with Bash tool
4. Verify with git diff
5. Rollback if needed (git restore or .bak)

```python
# ❌ BAD: Blind trust
agent_result = Task("Optimize file.py")

# ✅ GOOD: Verify
agent_result = Task("Generate sed commands for file.py")
Bash("sed -i.bak '/^#/d' file.py")  # Execute
Bash("git diff file.py")  # Verify
```
2. **Commit changes** and retry
3. **Close file watchers** (disable linters temporarily)
4. **Use agent with sed** (generate commands, execute via Bash)

### Checklist

- [ ] Simple pattern? → Use sed
- [ ] Complex semantic change? → Use Edit (if <5 files) or Agent + sed (if 5+ files)
- [ ] Agent modifications? → Verify output before accepting
- [ ] Edit tool fails? → Switch to sed immediately
- [ ] Bulk changes? → Parallelize with multiple agents

---

## Anti-Patterns

### ❌ Reading Without Searching
```python
# ❌ BAD: Read all (2700 tokens)
Read("<auth_module>/login.py")    # 450 lines
Read("<auth_module>/session.py")  # 380 lines
Read("<auth_module>/<jwt_file>.py")      # 520 lines

# ✅ GOOD: Grep first (significant reduction)
Grep("SessionManager", output_mode="files_with_matches")
Grep("SessionManager", path="<auth_module>/session.py", "-C": 3)
Read("<auth_module>/session.py", offset=40, limit=50)
```

### ❌ Skipping Discovery
```python
# ❌ BAD: Content everywhere (huge)
Grep("authentication", output_mode="content", "-C": 5)
# {MATCH_COUNT} matches across {FILE_COUNT} files

# ✅ GOOD: Discovery first
Grep("authentication", output_mode="files_with_matches")
# → 12 files, pick relevant
Grep("authentication", path="<auth_module>/<jwt_file>.py", "-C": 5)
```

---

## Token Budget Guidelines

**Per-Operation:**
- Grep files_with_matches: 5-10 tokens
- Grep content (-C=5): 50-200 tokens
- Read (offset+limit, 50 lines): 100-150 tokens
- Full file (<500 lines): 1000-1500 tokens
- Full file (>1000 lines): 2000+ tokens (avoid!)

---

## Checklist

- [ ] Grep before Read
- [ ] Use offset+limit for large files (>500 lines)
- [ ] Progressive refinement: files_with_matches → content → Read
- [ ] Always use context (-C/A/B)
- [ ] Track token usage per-operation
