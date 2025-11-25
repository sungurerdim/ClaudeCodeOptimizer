---
name: context-window-management
description: Optimize context via targeted reads, strategic model selection, parallel operations, and structured queries
type: claude
severity: medium
keywords: [context optimization, token efficiency, targeted reads, model selection, file operations]
category: [performance, efficiency]
---

# C_CONTEXT_WINDOW_MGMT: Context Window Management

**Severity**: Medium

Optimize context via targeted reads, strategic model selection, parallel operations, and structured queries to maximize efficiency and minimize token waste.

---

## Why

Inefficient context usage wastes most tokens (reading full files when few lines needed), slows responses, reduces quality, increases costs.

---

## Techniques

### 1. Targeted File Reads
```python
# ❌ BAD: Read entire file (1200 lines wasted)
Read("large_module.py")

# ✅ GOOD: Targeted read (only needed lines)
Read("large_module.py", offset=150, limit=30)
```

### 2. Strategic Model Selection
```python
# ❌ BAD: Sonnet for simple tasks
Task("count files", model="sonnet")

# ✅ GOOD: Match complexity
Task("count files", model="haiku")  # Fast, cheap
Task("analyze architecture", model="sonnet")  # Complex
```

### 3. Parallel Operations
```python
# ❌ BAD: Sequential (3x time)
Read("module1.py")  # Wait
Read("module2.py")  # Wait

# ✅ GOOD: Parallel (single response)
Read("module1.py")
Read("module2.py")
Read("module3.py")
```

### 4. Structured Query Format
```markdown
# ❌ BAD: Vague
"Fix the authentication bug"

# ✅ GOOD: Precise
"auth.py:<line>-145 → Add JWT refresh token validation"
"api.py:89 → Extract rate limiting to middleware"
```

### 5. Grep Before Read
```bash
# ❌ BAD: Read all potential files
Read("src/auth/login.py")
Read("src/auth/session.py")
Read("src/auth/tokens.py")

# ✅ GOOD: Grep first
Grep("JWT.*validate", output_mode="files_with_matches")
# → src/auth/tokens.py
Read("src/auth/tokens.py", offset=120, limit=40)
```

---

## Three-Stage Strategy

```
Stage 1: Discovery (files_with_matches) → Which files?
Stage 2: Preview (content + context)     → Verify relevance
Stage 3: Precise Read (offset+limit)     → Exact section
```

**Example:**
```python
# Stage 1: Discovery
Grep("authenticate", output_mode="files_with_matches")
# → auth.py, middleware.py (10 tokens)

# Stage 2: Preview
Grep("authenticate", path="auth.py", output_mode="content", "-C": 5)
# → Line 149 (100 tokens)

# Stage 3: Precise read
Read("auth.py", offset=145, limit=20)
# → Lines 145-165 (50 tokens)
# Total: 160 tokens vs 5000+ with full reads
```

---

## Checklist

- [ ] Use offset+limit for targeted reads
- [ ] Grep before Read to locate targets
- [ ] Match model to task (Haiku for mechanical, omit for complex)
- [ ] Parallelize independent operations
- [ ] Use `file:line → action` format
