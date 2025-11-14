---
id: C_GREP_FIRST_SEARCH_STRATEGY
title: Grep-First Search Strategy
category: claude-guidelines
severity: medium
weight: 6
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_GREP_FIRST_SEARCH_STRATEGY: Grep-First Search Strategy 🟡

**Severity**: Medium

Optimize file operations using a three-stage grep-first approach: (1) files_with_matches to discover, (2) content with context to preview, (3) targeted Read with offset+limit for precise editing.

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
- **Slow Discovery** - Reading files sequentially to find patterns takes 10-50x longer than grep
- **Context Pollution** - Irrelevant files clutter context, degrading AI analysis quality
- **Session Limits** - Inefficient searches hit context limits faster, forcing session restarts

### Business Value

- **90-95% token reduction** - Grep-first approach reduces token usage by 90-95% on search tasks
- **10-50x faster discovery** - Finding patterns via grep is 10-50x faster than reading files
- **5-10x more operations** - Efficient searching allows 5-10x more operations per session
- **Better quality** - Focused context improves AI analysis accuracy and relevance
- **Cost savings** - Dramatic token reduction directly translates to lower API costs

### Technical Benefits

- **Three-stage efficiency** - files_with_matches → content preview → targeted read optimizes each step
- **Precision targeting** - Grep identifies exact locations (file:line) before reading
- **Context preservation** - Minimal token usage preserves context for actual work
- **Parallel discovery** - Grep can search entire codebase in seconds
- **Pattern matching** - Regex patterns find complex relationships across files efficiently
- **Scalability** - Grep-first scales to codebases of any size without context issues

### Industry Evidence

- **Anthropic Guidelines** - Official Claude Code documentation emphasizes grep-before-read strategy
- **ripgrep Performance** - ripgrep (underlying tool) searches millions of lines in milliseconds
- **Developer Workflows** - Professional developers universally use grep/ag/rg before file reads
- **Token Economics** - Production data shows 90%+ token savings with search-first approach
- **Performance Benchmarks** - Grep-first is 10-100x faster than read-and-search approaches

---

## How

### Core Techniques

**The Three-Stage Grep-First Strategy**

```
Stage 1: Discovery (files_with_matches)
  ↓
Stage 2: Preview (content with context)
  ↓
Stage 3: Precise Read (Read with offset+limit)
```

---

### Stage 1: Discovery with files_with_matches

**Goal**: Find which files contain the pattern

```python
# Discover files containing "JWT authentication"
Grep("JWT.*authenticate", output_mode="files_with_matches")

# Returns:
# src/auth/jwt.py
# src/middleware/auth.py
# tests/test_auth.py
```

**When to use:**
- Don't know which files contain the pattern
- Need to survey entire codebase
- Want to identify all occurrences

**Token usage:** Minimal (only filenames)

---

### Stage 2: Preview with content and context

**Goal**: See the pattern in context to verify relevance

```python
# Preview the matches with surrounding context
Grep("JWT.*authenticate",
     path="src/auth/jwt.py",
     output_mode="content",
     "-C": 5,  # 5 lines before and after
     "-n": true)  # Show line numbers

# Returns:
# 145: def validate_jwt(token: str) -> bool:
# 146:     """Validate JWT token signature and expiry"""
# 147:     try:
# 148:         payload = jwt.decode(token, SECRET_KEY)
# 149:         return authenticate_user(payload['user_id'])  # ← Match here
# 150:     except jwt.ExpiredSignatureError:
# 151:         return False
```

**When to use:**
- Need to verify which match is relevant
- Want to understand context before reading
- Deciding where to make changes

**Token usage:** Low (only matching sections with context)

---

### Stage 3: Precise Read with offset+limit

**Goal**: Read exact section for editing

```python
# Now read precisely for editing
Read("src/auth/jwt.py", offset=145, limit=20)  # Lines 145-165

# Returns targeted section ready for editing
```

**When to use:**
- Identified exact location from grep
- Ready to make changes
- Need full file syntax for Edit tool

**Token usage:** Minimal (only relevant lines)

---

### Complete Example: Three-Stage Workflow

```python
# Task: Add rate limiting to JWT authentication

# Stage 1: Discovery
files = Grep("def.*authenticate", output_mode="files_with_matches")
# → src/auth/jwt.py, src/api/endpoints.py

# Stage 2: Preview with context
matches = Grep("def.*authenticate",
               path="src/auth/jwt.py",
               output_mode="content",
               "-C": 3,
               "-n": true)
# → Found at line 149: authenticate_user()

# Stage 3: Precise read
code = Read("src/auth/jwt.py", offset=145, limit=30)
# → Read lines 145-175 for editing

# Stage 4: Edit (now have precise context)
Edit("src/auth/jwt.py",
     old_string="return authenticate_user(payload['user_id'])",
     new_string="return rate_limit_check() and authenticate_user(payload['user_id'])")

# Total tokens: ~500 (vs 5000+ with full file reads)
```

**Token savings:** 90%
**Time savings:** 10x faster discovery
**Context preserved:** For additional operations

---

### Implementation Patterns

#### ✅ Good: Grep-First Discovery

```python
# Unknown location, need to find function

# ❌ BAD: Read all possible files
Read("src/auth/login.py")       # 450 lines
Read("src/auth/session.py")     # 380 lines
Read("src/auth/jwt.py")         # 520 lines
Read("src/auth/middleware.py")  # 290 lines
# Total: 1640 lines for unknown location!

# ✅ GOOD: Grep first
Grep("class SessionManager", output_mode="files_with_matches")
# → src/auth/session.py

Grep("class SessionManager",
     path="src/auth/session.py",
     output_mode="content",
     "-C": 3,
     "-n": true)
# → Found at line 45

Read("src/auth/session.py", offset=40, limit=50)
# Total: ~50 lines (97% reduction!)
```

---

#### ✅ Good: Pattern Discovery Across Codebase

```python
# Find all SQL query locations for optimization

# Stage 1: Find all files with SQL
sql_files = Grep("SELECT.*FROM", output_mode="files_with_matches")
# → db/queries.py, api/users.py, reports/analytics.py

# Stage 2: Preview each to identify slow queries
for file in sql_files:
    Grep("SELECT.*FROM.*JOIN",
         path=file,
         output_mode="content",
         "-C": 2,
         "-n": true)
# → Identify 3 complex queries at specific lines

# Stage 3: Read only problematic queries
Read("db/queries.py", offset=127, limit=15)
Read("api/users.py", offset=234, limit=20)
# Total: 35 lines vs thousands if reading all files
```

---

#### ✅ Good: Multi-File Pattern Analysis

```python
# Analyze error handling patterns across codebase

# Stage 1: Find all error handling
Grep("except.*Exception", output_mode="files_with_matches")
# → Returns 15 files

# Stage 2: Count occurrences per file
Grep("except.*Exception", output_mode="count")
# → service.py: 12, api.py: 8, utils.py: 5

# Stage 3: Focus on highest count
Grep("except.*Exception",
     path="service.py",
     output_mode="content",
     "-C": 2,
     "-n": true)
# → See all 12 instances with context

# Stage 4: Read problematic sections only
Read("service.py", offset=145, limit=25)  # First problematic pattern
Read("service.py", offset=290, limit=30)  # Second problematic pattern
```

---

#### ❌ Bad: Read-First Approach

```python
# ❌ BAD: Read files hoping to find pattern
Read("src/services/user_service.py")     # 800 lines
Read("src/services/auth_service.py")     # 650 lines
Read("src/services/payment_service.py")  # 920 lines
# Searching in memory... not found in any of these!
Read("src/services/admin_service.py")    # 540 lines
# Found it! But wasted 2970 lines of context first

# ✅ GOOD: Grep first
Grep("class PaymentProcessor", output_mode="files_with_matches")
# → src/services/admin_service.py
Read("src/services/admin_service.py", offset=200, limit=40)
# Found immediately with minimal context
```

---

#### ❌ Bad: Full File Read for Small Change

```python
# ❌ BAD: Read entire large file
Read("large_module.py")  # 2000 lines
# Need to change one function at line 1234
# Wasted 1999 lines of context!

# ✅ GOOD: Grep to locate, then targeted read
Grep("def process_payment", output_mode="content", "-n": true)
# → Found at line 1234
Read("large_module.py", offset=1230, limit=30)
# Only 30 lines, precise context
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Reading Without Searching

**Problem**: Reading files blindly hoping to find what you need.

```python
# ❌ BAD: Blind reading
Read("module1.py")  # Hope it's here
Read("module2.py")  # Maybe here?
Read("module3.py")  # Or here?
# Wasting context on irrelevant files

# ✅ GOOD: Grep first
Grep("target_function", output_mode="files_with_matches")
# → module2.py (found instantly)
Read("module2.py", offset=from_grep, limit=30)
```

**Impact:**
- Wastes 90% of context on irrelevant files
- 10-50x slower discovery
- Context pollution degrades analysis

---

### ❌ Anti-Pattern 2: Full File Reads for Large Files

**Problem**: Reading 1000+ line files to find small sections.

```python
# ❌ BAD: Read entire 3000-line file
Read("massive_service.py")  # 3000 lines
# Looking for 10-line function somewhere in there

# ✅ GOOD: Grep to locate, targeted read
Grep("def specific_function",
     path="massive_service.py",
     output_mode="content",
     "-n": true)
# → Found at line 2145
Read("massive_service.py", offset=2140, limit=25)
# 25 lines vs 3000 (99.2% reduction)
```

**Impact:**
- Wastes 99%+ of context window
- Slower processing
- May hit context limits

---

### ❌ Anti-Pattern 3: No Context in Grep

**Problem**: Using grep without context lines, can't verify relevance.

```python
# ❌ BAD: No context
Grep("user_id", output_mode="content")
# Returns: Hundreds of isolated matches, no context

# ✅ GOOD: Context lines
Grep("user_id", output_mode="content", "-C": 3)
# Returns: Each match with 3 lines before/after
# Can verify which matches are relevant
```

**Impact:**
- Can't determine relevance without context
- May need multiple grep iterations
- Wastes time on false positives

---

### ❌ Anti-Pattern 4: Skipping files_with_matches Stage

**Problem**: Jumping straight to content search across entire codebase.

```python
# ❌ BAD: Content search everywhere
Grep("authentication", output_mode="content", "-C": 5)
# Returns: 500 matches across 50 files (huge context usage!)

# ✅ GOOD: Discovery first, then targeted content
Grep("authentication", output_mode="files_with_matches")
# → 12 files
# Review filenames, pick relevant ones
Grep("authentication",
     path="src/auth/jwt.py",
     output_mode="content",
     "-C": 5)
# Focused results from relevant file
```

**Impact:**
- Overwhelms with irrelevant results
- High token usage
- Difficult to identify relevant matches

---

## Implementation Checklist

### Stage 1: Discovery

- [ ] **Use files_with_matches first** - Always start with file discovery
- [ ] **Review filenames** - Examine which files contain pattern before diving deeper
- [ ] **Filter by relevance** - Eliminate obviously irrelevant files from filename review
- [ ] **Count matches** - Use output_mode="count" to identify hotspots

### Stage 2: Preview

- [ ] **Add context lines** - Always use -C (or -A/-B) to see surrounding code
- [ ] **Enable line numbers** - Use "-n": true to get precise line numbers
- [ ] **Target specific files** - Use path parameter to focus on relevant files from Stage 1
- [ ] **Verify relevance** - Confirm matches are what you need before reading

### Stage 3: Precise Read

- [ ] **Use offset+limit** - Calculate offset from grep line numbers, read minimal lines
- [ ] **Include context** - Read 10-20 lines before/after target for editing context
- [ ] **Batch related reads** - If multiple edits needed, read all sections in parallel
- [ ] **Avoid re-reading** - Once read, preserve in context for edits

### General Best Practices

- [ ] **Regex mastery** - Learn regex patterns for complex searches (e.g., "class.*Service")
- [ ] **Case sensitivity** - Use "-i": true for case-insensitive when appropriate
- [ ] **Glob patterns** - Combine with glob parameter to filter file types (e.g., glob="*.py")
- [ ] **Multiline patterns** - Use multiline: true for patterns spanning multiple lines

---

## Cross-References

**Related Principles:**

- **C_CONTEXT_WINDOW_MGMT** - Grep-first is a core context optimization technique
- **C_TOKEN_OPTIMIZATION** - Grep-first dramatically reduces token usage
- **C_MODEL_SELECTION** - Use Haiku for grep tasks, reserve Sonnet for analysis
- **C_PARALLEL_AGENTS** - Parallel grep operations for multi-pattern searches
- **U_MINIMAL_TOUCH** - Find exact locations to minimize changes

**Workflow Integration:**
- Use **Grep** tool for all searches before **Read** tool
- Combine with **Glob** for file pattern discovery
- Use with **Task/Explore agents** for codebase analysis

---

## Summary

**Grep-First Search Strategy** means always searching with grep before reading files, using a three-stage approach: (1) discover files with files_with_matches, (2) preview matches with content+context, (3) read precisely with offset+limit.

**Core Rules:**

- **Stage 1: Discover** - Use files_with_matches to find which files contain pattern
- **Stage 2: Preview** - Use content with -C context and -n line numbers to verify relevance
- **Stage 3: Precise Read** - Use Read(offset, limit) for exact sections only
- **Never read blindly** - Always grep first unless you have exact file:line reference
- **Context is king** - Always use -C/A/B context lines in content mode

**Remember**: "Grep first, read precisely, edit confidently. Never read files blindly when grep can find your target in milliseconds."

**Impact**: 90-95% token reduction, 10-50x faster discovery, 5-10x more operations per session, preserved context for real work.

---

**Three-Stage Workflow:**
```
files_with_matches → content with context → Read with offset+limit → Edit
    (discover)           (preview)              (precise)           (action)
```

**Token Efficiency:**
- Blind reading: 5000+ tokens for unknown location
- Grep-first: 200-500 tokens for same task
- Savings: 90-95% reduction
