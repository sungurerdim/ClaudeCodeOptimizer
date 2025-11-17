# C_EFFICIENT_FILE_OPERATIONS: Efficient File Operations

**Severity**: Medium

Optimize file operations via grep-first: (1) files_with_matches to discover, (2) content with context to preview, (3) targeted Read with offset+limit for precise editing.

---

## Why

Reading without searching wastes 90%+ context. Grep-first delivers 90%+ token savings and 10x faster discovery.

**Problems:**
- Reading 10 files to find 1 function wastes 90% context
- Reading 2000-line file for 5-line fix wastes 99.75% tokens
- Brute-force can consume 10K+ tokens when 100 would suffice

**Strategy:**
```
Stage 1: Discovery (files_with_matches) → Find which files
Stage 2: Preview (content + context)     → Verify relevance
Stage 3: Precise Read (offset+limit)     → Read exact section
```

---

## Implementation

### Stage 1: Discovery
```python
Grep("JWT.*authenticate", output_mode="files_with_matches")
# → src/auth/jwt.py, src/middleware/auth.py (~10 tokens)
```

### Stage 2: Preview with Context
```python
Grep("JWT.*authenticate", path="src/auth/jwt.py",
     output_mode="content", "-C": 5, "-n": true)
# → Line 149 with context (~100 tokens)
```

### Stage 3: Precise Read
```python
Read("src/auth/jwt.py", offset=145, limit=20)
# → Lines 145-165 (~50 tokens)
```

---

## Complete Example

```python
# Task: Add rate limiting to JWT auth

# Stage 1: Discovery
Grep("def.*authenticate", output_mode="files_with_matches")
# → src/auth/jwt.py (10 tokens)

# Stage 2: Preview
Grep("def.*authenticate", path="src/auth/jwt.py",
     output_mode="content", "-C": 3, "-n": true)
# → Line 149 (50 tokens)

# Stage 3: Precise read
Read("src/auth/jwt.py", offset=145, limit=30)
# → Lines 145-175 (60 tokens)

# Total: ~120 tokens vs 5000+ with full reads (42x better)
```

---

## Anti-Patterns

### ❌ Reading Without Searching
```python
# ❌ BAD: Read all (2700 tokens)
Read("src/auth/login.py")    # 450 lines
Read("src/auth/session.py")  # 380 lines
Read("src/auth/jwt.py")      # 520 lines

# ✅ GOOD: Grep first (85 tokens, 97% reduction)
Grep("SessionManager", output_mode="files_with_matches")
Grep("SessionManager", path="src/auth/session.py", "-C": 3)
Read("src/auth/session.py", offset=40, limit=50)
```

### ❌ Skipping Discovery
```python
# ❌ BAD: Content everywhere (huge)
Grep("authentication", output_mode="content", "-C": 5)
# 500 matches across 50 files

# ✅ GOOD: Discovery first
Grep("authentication", output_mode="files_with_matches")
# → 12 files, pick relevant
Grep("authentication", path="src/auth/jwt.py", "-C": 5)
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
