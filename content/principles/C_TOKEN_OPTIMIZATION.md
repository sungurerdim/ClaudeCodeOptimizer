---
id: C_TOKEN_OPTIMIZATION
title: Token Optimization
category: claude-guidelines
severity: medium
weight: 7
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_TOKEN_OPTIMIZATION: Token Optimization 🟡

**Severity**: Medium

Minimize Claude token usage through grep-first approach, targeted reads, and efficient tool usage.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Context overflow** - Reading entire large files wastes tokens
- **Blind file reads** - Reading files without knowing what's needed
- **Inefficient searches** - Full file reads when grep suffices
- **Redundant context** - Re-reading same content multiple times
- **Poor tool usage** - Using Read when Grep is faster

### Business Value
- **50% token reduction** - Grep-first approach vs blind reads
- **Faster execution** - Less token processing = faster responses
- **Lower costs** - Tokens cost money, optimization saves budget
- **Better context utilization** - More room for actual code
- **Improved performance** - Efficient tool usage

### Technical Benefits
- **Targeted context** - Only load what's needed
- **Faster searches** - Grep faster than read+search
- **Scalable workflows** - Works on large codebases
- **Reduced latency** - Less token processing time
- **Better debugging** - Clear what context was used

### Industry Evidence
- **Database optimization** - Index-first approach (similar to grep-first)
- **Search engines** - Inverted index before full content
- **IDE performance** - Incremental parsing, not full reparse
- **Git operations** - `git grep` faster than reading all files

---

## How

### Token Optimization Strategy

**3-Phase Approach:**

1. **Grep Phase**: Find relevant locations
2. **Context Phase**: Get surrounding context
3. **Read Phase**: Targeted reads with offset+limit

### Core Techniques

#### 1. Grep-First Search

✅ **Good: Grep before Read**
```python
# Task: Find where "UserProfile" class is defined

# Phase 1: Find files containing pattern
files = Grep("class UserProfile", output_mode="files_with_matches")
# Result: ["src/models/user.py"]  (1 file identified)

# Phase 2: Get context around match
context = Grep("class UserProfile",
               path="src/models/user.py",
               output_mode="content",
               -B=5, -C=10)
# Result: Shows class definition + 5 lines before + 10 lines context

# Phase 3: If needed, targeted read
Read("src/models/user.py", offset=45, limit=100)
# Only read lines 45-145, not entire 2000-line file
```

❌ **Bad: Read-First (Wasteful)**
```python
# ❌ BAD: Reading entire file without knowing location
Read("src/models/user.py")  # Reads all 2000 lines (wasteful!)
# Then manually search for "UserProfile"

# Token usage: ~4000 tokens
# Grep-first approach: ~200 tokens (20x savings!)
```

#### 2. Targeted Reads with Offset+Limit

✅ **Good: Offset+Limit for Large Files**
```python
# File: large_module.py (5000 lines)

# ❌ BAD: Read entire file
Read("large_module.py")  # 10,000 tokens!

# ✅ GOOD: Grep to find location, then targeted read
matches = Grep("def process_payment", path="large_module.py", output_mode="content", -n=true)
# Found at line 2847

Read("large_module.py", offset=2840, limit=50)
# Only read lines 2840-2890 (100 tokens)
```

#### 3. files_with_matches → content → Read

✅ **Good: Progressive Refinement**
```python
# Task: Find all uses of deprecated API

# Step 1: Identify files (cheap)
files = Grep("deprecated_api()", output_mode="files_with_matches")
# Result: ["api/v1.py", "api/v2.py", "tests/test_api.py"]

# Step 2: Get line numbers and context (medium cost)
for file in files:
    matches = Grep("deprecated_api()", path=file, output_mode="content", -n=true, -C=3)
    # Shows each usage with 3 lines context

# Step 3: Only if needed, targeted full reads
# (Don't read unless absolutely necessary)
```

---

## Implementation Patterns

### Pattern 1: Search Unknown Location

```python
# Goal: Find where "authenticate_user" function is defined

# ✅ GOOD: Grep-first
files = Grep("def authenticate_user", output_mode="files_with_matches")
# Found in: src/auth/handlers.py

context = Grep("def authenticate_user",
               path="src/auth/handlers.py",
               output_mode="content",
               -B=10, -A=50)  # Function definition + body
# Got what I need! No full file read necessary.

# ❌ BAD: Read-first
Read("src/auth/handlers.py")  # 800 lines = 1600 tokens
Read("src/auth/middleware.py")  # 500 lines = 1000 tokens
Read("src/auth/utils.py")  # 300 lines = 600 tokens
# Total: 3200 tokens vs 50 tokens with grep (64x worse!)
```

### Pattern 2: Large File Analysis

```python
# Goal: Understand how "DatabaseConnection" class works
# File: db/connection.py (3000 lines)

# ✅ GOOD: Targeted approach
# Step 1: Find class definition
Grep("class DatabaseConnection", path="db/connection.py", output_mode="content", -A=20)

# Step 2: Find key methods
Grep("def connect|def query|def close", path="db/connection.py", output_mode="content", -C=5)

# Step 3: If specific line range needed
Read("db/connection.py", offset=100, limit=50)

# Total tokens: ~300

# ❌ BAD: Read entire file
Read("db/connection.py")  # 6000 tokens!
```

### Pattern 3: Multi-File Search

```python
# Goal: Find all exception handlers

# ✅ GOOD: Grep-first multi-file
files = Grep("try:|except", output_mode="files_with_matches", glob="**/*.py")
# Found 15 files

# Get context for each
for file in files[:5]:  # Sample first 5
    Grep("try:|except", path=file, output_mode="content", -C=3)

# Total tokens: ~500

# ❌ BAD: Read all files
for file in glob("**/*.py"):  # 50 files
    Read(file)  # 50 files * 500 lines avg = 50,000 tokens!
```

---

## Anti-Patterns

### ❌ Reading Entire Files Blindly

```python
# ❌ BAD: Read everything without knowing what's needed
Read("src/api/users.py")      # 2000 lines
Read("src/api/products.py")   # 1500 lines
Read("src/api/orders.py")     # 1800 lines
Read("src/api/payments.py")   # 2200 lines
# Total: 15,000 tokens

# ✅ GOOD: Grep first to understand structure
Grep("def.*route", glob="src/api/*.py", output_mode="content", -C=2)
# Shows all API routes with minimal context
# Total: 300 tokens (50x better!)
```

### ❌ No Offset+Limit for Large Files

```python
# File: giant_module.py (10,000 lines)

# ❌ BAD: Read entire file
Read("giant_module.py")  # 20,000 tokens!

# ✅ GOOD: Grep location, then targeted read
Grep("class ImportantClass", path="giant_module.py", output_mode="content", -n=true)
# Found at line 7234

Read("giant_module.py", offset=7230, limit=100)
# Only 200 tokens
```

### ❌ Repeated Reads

```python
# ❌ BAD: Reading same file multiple times
Read("config.py")  # First time: 200 tokens
# ... do something ...
Read("config.py")  # Second time: 200 tokens (redundant!)
# ... do something else ...
Read("config.py")  # Third time: 200 tokens (wasteful!)

# ✅ GOOD: Read once, store result
config_content = Read("config.py")  # Once: 200 tokens
# Use config_content multiple times (no additional token cost)
```

---

## Token Cost Comparison

### Scenario: Find specific function in large codebase

**Blind Read Approach (Bad):**
```
Read("module1.py")  # 1000 lines = 2000 tokens
Read("module2.py")  # 800 lines = 1600 tokens
Read("module3.py")  # 1200 lines = 2400 tokens
Read("module4.py")  # 900 lines = 1800 tokens
Total: 7800 tokens
```

**Grep-First Approach (Good):**
```
Grep("function_name", output_mode="files_with_matches")  # 10 tokens
Grep("function_name", path="module2.py", output_mode="content", -C=10)  # 50 tokens
Read("module2.py", offset=450, limit=30)  # 60 tokens
Total: 120 tokens (65x better!)
```

---

## Grep Tool Parameters

### output_mode Options

```python
# 1. files_with_matches: Just list files (cheapest)
Grep("pattern", output_mode="files_with_matches")
# Output: ["file1.py", "file2.py"]
# Tokens: ~5

# 2. count: Show match counts per file
Grep("pattern", output_mode="count")
# Output: file1.py: 15 matches, file2.py: 7 matches
# Tokens: ~10

# 3. content: Show matching lines with context
Grep("pattern", output_mode="content", -C=5)
# Output: Actual code with 5 lines context around each match
# Tokens: ~100 (depends on matches)
```

### Context Parameters

```python
# -B: Lines before match
Grep("pattern", -B=10)  # 10 lines before each match

# -A: Lines after match
Grep("pattern", -A=20)  # 20 lines after each match

# -C: Lines before and after match
Grep("pattern", -C=5)   # 5 lines before and after each match

# -n: Show line numbers
Grep("pattern", -n=true)  # Include line numbers in output
```

---

## Advanced Techniques

### Technique 1: head_limit + offset

```python
# Goal: Sample large search results

# ❌ BAD: Get all matches (could be thousands)
Grep("TODO", glob="**/*.py", output_mode="content")
# 500 matches * 5 lines each = 2500 lines = 5000 tokens!

# ✅ GOOD: Limit results with head_limit
Grep("TODO", glob="**/*.py", output_mode="content", head_limit=10)
# First 10 matches only = 50 lines = 100 tokens

# ✅ ADVANCED: Paginate with offset + head_limit
Grep("TODO", glob="**/*.py", output_mode="content", offset=10, head_limit=10)
# Matches 11-20 (for pagination)
```

### Technique 2: Multiline Patterns

```python
# Goal: Find multi-line patterns (function signatures)

# ✅ GOOD: Use multiline mode
Grep("def.*\\([^)]*$", multiline=true, -A=3)
# Matches function definitions that span multiple lines
```

### Technique 3: Type Filtering

```python
# Goal: Search only in Python files

# ✅ GOOD: Use type parameter (efficient)
Grep("pattern", type="py")
# Only searches .py files

# ❌ LESS EFFICIENT: Use glob
Grep("pattern", glob="**/*.py")
# Also works but type is more efficient
```

---

## Decision Flowchart

```
Need to find code?
├─ Know exact file + line? → Read(file, offset, limit)
└─ Don't know location?
   ├─ Need to search? → Grep("pattern", output_mode="files_with_matches")
   │  ├─ Found 1 file? → Grep(path=file, -C=10) or Read(offset, limit)
   │  └─ Found many files? → Grep each with head_limit
   └─ Need full file? → Validate it's <500 lines, then Read()
```

---

## Optimization Checklist

Before reading files, ask:

- [ ] **Do I know the file location?** If no, Grep first
- [ ] **Is the file >500 lines?** If yes, use offset+limit
- [ ] **Do I need the whole file?** If no, Grep with -C context
- [ ] **Am I searching multiple files?** Use files_with_matches first
- [ ] **Have I already read this file?** Avoid repeated reads
- [ ] **Can I use head_limit?** Limit results for sampling
- [ ] **Is this a multiline pattern?** Use multiline=true

---

## Token Budget Guidelines

**Per-Operation Budget:**
- **Grep files_with_matches**: 5-10 tokens
- **Grep content with -C=5**: 50-200 tokens
- **Read with offset+limit (50 lines)**: 100-150 tokens
- **Full file read (<500 lines)**: 1000-1500 tokens
- **Full file read (>1000 lines)**: 2000+ tokens (avoid!)

**Session Budget:**
- **Simple task** (grep, find): <100 tokens
- **Medium task** (bug fix): 500-1000 tokens
- **Complex task** (feature): 2000-5000 tokens
- **Architecture** (design): 10,000+ tokens (use Opus)

---

## Cross-References

**Related Principles:**
- **C_GREP_FIRST_SEARCH_STRATEGY** - Detailed grep-first methodology
- **C_CONTEXT_WINDOW_MGMT** - Overall context optimization
- **C_MODEL_SELECTION** - Choose right model for token budget
- **C_PARALLEL_AGENTS** - Distribute work to optimize tokens

---

## Summary

**Token Optimization** means minimizing Claude token usage through grep-first approach, targeted reads with offset+limit, and efficient tool usage.

**Core Rules:**
- **Grep before Read** - Find location before loading content
- **offset+limit for large files** - Never read >500 lines without limit
- **files_with_matches → content → Read** - Progressive refinement
- **Avoid repeated reads** - Read once, reuse result

**Remember**: "A grep today saves 1000 tokens tomorrow."

**Impact**: 50% token reduction, faster execution, lower costs, better performance.
