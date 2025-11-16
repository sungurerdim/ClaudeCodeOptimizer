---
id: C_EFFICIENT_FILE_OPERATIONS
title: Efficient File Operations
category: claude-guidelines
severity: medium
weight: 7
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_EFFICIENT_FILE_OPERATIONS: Efficient File Operations 🟡

**Severity**: Medium

Optimize file operations using grep-first approach: (1) files_with_matches to discover, (2) content with context to preview, (3) targeted Read with offset+limit for precise editing. Minimize token usage through targeted reads and efficient tool usage.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Reading files without searching first wastes massive context:**

- **Blind File Reading** - Reading 10 files to find 1 relevant function wastes 90% of context window
- **Full File Reads** - Reading a 2000-line file to fix a 5-line function wastes 99.75% of context
- **Token Explosion** - Brute-force file reading can consume 10K+ tokens when 100 would suffice
- **Context Pollution** - Irrelevant files clutter context, degrading AI analysis quality
- **Session Limits** - Inefficient searches hit context limits faster, forcing session restarts

### Three-Stage Grep-First Strategy

```
Stage 1: Discovery (files_with_matches)
  ↓
Stage 2: Preview (content with context)
  ↓
Stage 3: Precise Read (Read with offset+limit)
```

**Token savings: 90%+** | **Time savings: 10x faster discovery**

---

## Implementation Patterns

### Stage 1: Discovery with files_with_matches

```python
# Find which files contain the pattern
Grep("JWT.*authenticate", output_mode="files_with_matches")
# Returns: src/auth/jwt.py, src/middleware/auth.py

# Token usage: ~10 (just filenames)
```

### Stage 2: Preview with content and context

```python
# See the pattern in context to verify relevance
Grep("JWT.*authenticate",
     path="src/auth/jwt.py",
     output_mode="content",
     "-C": 5,  # 5 lines before and after
     "-n": true)  # Show line numbers

# Returns:
# 145: def validate_jwt(token: str) -> bool:
# ...
# 149:         return authenticate_user(payload['user_id'])  # ← Match
# ...

# Token usage: ~100 (only matching sections with context)
```

### Stage 3: Precise Read with offset+limit

```python
# Read exact section for editing
Read("src/auth/jwt.py", offset=145, limit=20)  # Lines 145-165

# Token usage: ~50 (only relevant lines)
```

---

## Complete Workflow Example

```python
# Task: Add rate limiting to JWT authentication

# Stage 1: Discovery
files = Grep("def.*authenticate", output_mode="files_with_matches")
# → src/auth/jwt.py, src/api/endpoints.py (10 tokens)

# Stage 2: Preview with context
matches = Grep("def.*authenticate",
               path="src/auth/jwt.py",
               output_mode="content",
               "-C": 3,
               "-n": true)
# → Found at line 149 (50 tokens)

# Stage 3: Precise read
code = Read("src/auth/jwt.py", offset=145, limit=30)
# → Read lines 145-175 for editing (60 tokens)

# Stage 4: Edit (now have precise context)
Edit("src/auth/jwt.py",
     old_string="return authenticate_user(payload['user_id'])",
     new_string="return rate_limit_check() and authenticate_user(payload['user_id'])")

# Total: ~120 tokens vs 5000+ with full file reads (42x better)
```

---

## Anti-Patterns

### ❌ Reading Without Searching

```python
# ❌ BAD: Read all possible files
Read("src/auth/login.py")       # 450 lines = 900 tokens
Read("src/auth/session.py")     # 380 lines = 760 tokens
Read("src/auth/jwt.py")         # 520 lines = 1040 tokens
# Total: 2700 tokens for unknown location!

# ✅ GOOD: Grep first
Grep("class SessionManager", output_mode="files_with_matches")
# → src/auth/session.py (5 tokens)

Grep("class SessionManager", path="src/auth/session.py",
     output_mode="content", "-C": 3, "-n": true)
# → Found at line 45 (30 tokens)

Read("src/auth/session.py", offset=40, limit=50)
# Total: ~85 tokens (97% reduction!)
```

### ❌ Full File Read for Large Files

```python
# ❌ BAD: Read entire 3000-line file
Read("massive_service.py")  # 6000 tokens

# ✅ GOOD: Grep to locate, targeted read
Grep("def specific_function", path="massive_service.py",
     output_mode="content", "-n": true)
# → Found at line 2145

Read("massive_service.py", offset=2140, limit=25)
# 25 lines vs 3000 (99.2% reduction)
```

### ❌ Skipping files_with_matches Stage

```python
# ❌ BAD: Content search everywhere
Grep("authentication", output_mode="content", "-C": 5)
# Returns: 500 matches across 50 files (huge context!)

# ✅ GOOD: Discovery first
Grep("authentication", output_mode="files_with_matches")
# → 12 files, review filenames, pick relevant ones

Grep("authentication", path="src/auth/jwt.py",
     output_mode="content", "-C": 5)
# Focused results from relevant file
```

---

## Advanced Techniques

### head_limit + offset for Pagination

```python
# ❌ BAD: Get all matches (could be thousands)
Grep("TODO", glob="**/*.py", output_mode="content")
# 500 matches * 5 lines each = 2500 lines = 5000 tokens!

# ✅ GOOD: Limit results
Grep("TODO", glob="**/*.py", output_mode="content", head_limit=10)
# First 10 matches only = 50 lines = 100 tokens

# ✅ ADVANCED: Paginate
Grep("TODO", glob="**/*.py", output_mode="content",
     offset=10, head_limit=10)
# Matches 11-20 (for pagination)
```

### Multiline Patterns

```python
# Find multi-line patterns (function signatures)
Grep("def.*\\([^)]*$", multiline=true, "-A": 3)
# Matches function definitions spanning multiple lines
```

### Type Filtering

```python
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

## Implementation Checklist

### Stage 1: Discovery
- [ ] Use files_with_matches first - Always start with file discovery
- [ ] Review filenames - Examine which files contain pattern
- [ ] Filter by relevance - Eliminate obviously irrelevant files
- [ ] Count matches - Use output_mode="count" to identify hotspots

### Stage 2: Preview
- [ ] Add context lines - Always use -C (or -A/-B)
- [ ] Enable line numbers - Use "-n": true
- [ ] Target specific files - Use path parameter from Stage 1
- [ ] Verify relevance - Confirm matches before reading

### Stage 3: Precise Read
- [ ] Use offset+limit - Calculate from grep line numbers
- [ ] Include context - Read 10-20 lines before/after target
- [ ] Batch related reads - If multiple edits, read all sections in parallel
- [ ] Avoid re-reading - Once read, preserve in context

### General
- [ ] Regex mastery - Learn patterns for complex searches
- [ ] Case sensitivity - Use "-i": true when appropriate
- [ ] Glob patterns - Filter file types (glob="*.py")
- [ ] Multiline patterns - Use multiline: true for cross-line patterns

---

## Token Budget Guidelines

**Per-Operation:**
- Grep files_with_matches: 5-10 tokens
- Grep content with -C=5: 50-200 tokens
- Read with offset+limit (50 lines): 100-150 tokens
- Full file read (<500 lines): 1000-1500 tokens
- Full file read (>1000 lines): 2000+ tokens (avoid!)

**Session Budget:**
- Simple task (grep, find): <100 tokens
- Medium task (bug fix): 500-1000 tokens
- Complex task (feature): 2000-5000 tokens
- Architecture (design): 10,000+ tokens (use Opus)

---

## Summary

**Efficient File Operations** means using grep-first approach to minimize token usage: (1) discover with files_with_matches, (2) preview with content+context, (3) read precisely with offset+limit.

**Core Rules:**
- **Grep before Read** - Find location before loading content
- **offset+limit for large files** - Never read >500 lines without limit
- **files_with_matches → content → Read** - Progressive refinement
- **Context is king** - Always use -C/A/B context lines
- **Token awareness** - Track token usage per operation
