---
id: C_CONTEXT_WINDOW_MGMT
title: Context Window Management
category: claude-guidelines
severity: medium
weight: 6
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_CONTEXT_WINDOW_MGMT: Context Window Management 🟡

**Severity**: Medium

Optimize AI context usage through strategic model selection, targeted file reads, parallel operations, and structured query formats to maximize context efficiency and minimize token waste.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Inefficient context window usage leads to:**

- **Token Waste** - Reading entire 1000-line files when only 20 lines are needed wastes 98% of the context window
- **Slower Responses** - Larger context requires longer processing time, delaying feedback loops
- **Reduced Quality** - Overloaded context dilutes attention from critical information, degrading analysis quality
- **Cost Accumulation** - Wasted tokens directly translate to higher API costs in production environments
- **Session Fragmentation** - Hitting context limits mid-task forces session restarts and context loss
- **Poor Scalability** - Inefficient context usage prevents handling larger codebases or complex multi-file tasks

### Core Techniques

**1. Targeted File Reads**

Instead of reading entire files, use offset and limit parameters to read only relevant sections:

```python
# ❌ BAD: Read entire file
Read("large_module.py")  # 1200 lines → wasted context

# ✅ GOOD: Targeted read
Read("large_module.py", offset=150, limit=30)  # Only 30 lines around the problem
```

**2. Strategic Model Selection**

Match model complexity to task complexity:

```python
# ❌ BAD: Using Sonnet for simple tasks
Task("count files in directory", model="sonnet")  # Overkill

# ✅ GOOD: Haiku for simple, Sonnet for complex
Task("count files", model="haiku")  # Fast, cheap
Task("analyze architecture patterns", model="sonnet")  # Complex analysis needs power
```

**3. Parallel Operations**

Execute independent operations in a single message:

```python
# ❌ BAD: Sequential independent operations
Read("module1.py")
# Wait for response
Read("module2.py")
# Wait for response
Read("module3.py")

# ✅ GOOD: Parallel reads in single message
Read("module1.py")
Read("module2.py")
Read("module3.py")
# All executed together, single response
```

**4. Structured Query Format**

Use `[file:line]` → `[action]` format for clarity:

```markdown
# ❌ BAD: Vague request
"Fix the authentication bug"

# ✅ GOOD: Precise format
"auth.py:127-145 → Add JWT refresh token validation"
"api.py:89 → Extract rate limiting to middleware"
```

**5. Context-Aware Grep/Glob**

Use search tools before reading full files:

```bash
# ❌ BAD: Read all potential files
Read("src/auth/login.py")
Read("src/auth/session.py")
Read("src/auth/tokens.py")
Read("src/auth/middleware.py")

# ✅ GOOD: Grep first, then targeted read
Grep("JWT.*validate", output_mode="files_with_matches")
# Returns: src/auth/tokens.py
Read("src/auth/tokens.py", offset=120, limit=40)
```

---

### Implementation Patterns

#### ✅ Good: Targeted Read with Context

```python
# User reports bug in authentication at line 127

# Step 1: Read targeted section
Read("auth.py", offset=120, limit=30)  # Lines 120-150, gives context

# Step 2: Analyze and fix
Edit("auth.py",
     old_string="if token.expired:",
     new_string="if token.expired or not token.valid:")

# Result: Fixed with minimal context usage
```

**Benefits:**
- Only 30 lines read instead of potentially 800+
- Fast response time
- Preserved context for other operations

---

#### ✅ Good: Model Selection by Complexity

```python
# Complex architecture analysis
Task("Analyze microservices communication patterns and identify bottlenecks",
     model="sonnet",  # Complex task needs powerful model
     subagent_type="Explore")

# Simple file counting
Task("Count TypeScript test files in src/",
     model="haiku",  # Simple task, use fast model
     subagent_type="Explore")
```

**Benefits:**
- Cost optimization: Haiku is 15x cheaper than Sonnet
- Speed optimization: Haiku is 3-5x faster for simple tasks
- Quality optimization: Reserve Sonnet capacity for complex analysis

---

#### ✅ Good: Parallel Operations Pattern

```python
# Analyzing multiple independent modules

# Single message with multiple tool calls:
Read("src/auth/login.py", offset=50, limit=40)
Read("src/api/middleware.py", offset=100, limit=30)
Read("src/db/queries.py", offset=200, limit=50)

# All execute in parallel, single response with all results
```

**Benefits:**
- 3x faster than sequential reads
- Single context window for all data
- Efficient batch processing

---

#### ✅ Good: Structured Query Format

```markdown
**Task**: Implement rate limiting

**Queries**:
1. `api.py:89-120` → Extract rate limiting logic
2. `middleware.py:45` → Create RateLimitMiddleware class
3. `config.py:30` → Add rate_limit_per_minute setting
4. `tests/test_api.py:150` → Add rate limit integration tests

**Expected Outcome**:
- Rate limiting extracted to reusable middleware
- Configurable via environment variables
- Full test coverage
```

**Benefits:**
- Crystal clear intent
- Precise file:line references
- Measurable outcomes
- No ambiguity, no wasted context on clarification

---

#### ❌ Bad: Reading Entire Files Unnecessarily

```python
# User: "Fix login bug at line 127"

# ❌ BAD APPROACH:
Read("auth/login.py")        # 450 lines
Read("auth/session.py")      # 380 lines
Read("auth/tokens.py")       # 520 lines
Read("auth/middleware.py")   # 290 lines
# Total: 1640 lines read for a single line bug!

# ✅ GOOD APPROACH:
Read("auth/login.py", offset=120, limit=20)  # 20 lines, targeted
# Fixed with 1.2% of the context
```

---

#### ❌ Bad: Using Sonnet for Simple Tasks

```python
# ❌ BAD: Expensive overkill
Task("List all Python files in src/",
     model="sonnet")  # Costs 15x more than Haiku

Task("Count lines in config.py",
     model="sonnet")  # Slow and expensive for trivial task

# ✅ GOOD: Right tool for the job
Task("List all Python files in src/",
     model="haiku")  # Fast, cheap, perfect for simple tasks

Task("Analyze complex async race condition in event loop",
     model="sonnet")  # Complex analysis justifies powerful model
```

---

#### ❌ Bad: Sequential Independent Operations

```python
# ❌ BAD: Sequential calls waste time
message_1 = Read("module1.py")
# Wait for response...

message_2 = Read("module2.py")
# Wait for response...

message_3 = Read("module3.py")
# Wait for response...
# Total: 3x round trips

# ✅ GOOD: Parallel execution in single message
Read("module1.py")
Read("module2.py")
Read("module3.py")
# Single round trip, all results together
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Full File Reads by Default

**Problem**: Reading entire files when only specific sections are needed.

```python
# ❌ BAD: Default to full file
Read("large_service.py")  # 1500 lines
# Only needed lines 300-320

# ✅ GOOD: Targeted read
Grep("class UserService", output_mode="content", "-n": true)
# Found at line 305
Read("large_service.py", offset=300, limit=30)
```

**Impact:**
- Wastes 1470 lines of context (98%)
- Slower processing
- Higher costs

---

### ❌ Anti-Pattern 2: Sonnet for Everything

**Problem**: Using expensive, powerful models for simple tasks.

```python
# ❌ BAD: Sonnet for file counting
Task("Count JSON files in data/", model="sonnet")
Task("List directory contents", model="sonnet")
Task("Check if file exists", model="sonnet")

# ✅ GOOD: Model by complexity
Task("Count JSON files", model="haiku")      # Simple: Haiku
Task("List directory", model="haiku")        # Simple: Haiku
Task("Analyze distributed system race conditions", model="sonnet")  # Complex: Sonnet
```

**Impact:**
- 15x higher cost for simple tasks
- 3-5x slower response times
- Wasted Sonnet capacity

---

### ❌ Anti-Pattern 3: Vague Requests

**Problem**: Ambiguous queries waste context on clarification.

```python
# ❌ BAD: Vague
"Fix the bug"
"Improve performance"
"Add error handling"

# ✅ GOOD: Precise
"auth.py:127 → Fix JWT token expiry check (should validate both expired and revoked)"
"db_query.py:89-105 → Add connection pooling (target: 100ms → 10ms query time)"
"api.py:234 → Wrap external API call in try/catch with exponential backoff"
```

**Impact:**
- Wastes tokens on back-and-forth clarification
- Delays task completion
- Introduces ambiguity errors

---

### ❌ Anti-Pattern 4: Read-Then-Grep

**Problem**: Reading files before searching wastes context.

```python
# ❌ BAD: Read first, then search
Read("large_codebase/module1.py")
Read("large_codebase/module2.py")
Read("large_codebase/module3.py")
# Now search in memory... but context is full!

# ✅ GOOD: Grep first, then targeted read
Grep("class DatabaseConnection", output_mode="files_with_matches")
# Returns: module2.py
Read("large_codebase/module2.py", offset=150, limit=50)
```

**Impact:**
- Wastes context on irrelevant files
- May hit context limit before finding target
- Slower and less efficient

---

## Implementation Checklist

### Context Optimization

- [ ] **Targeted reads** - Use offset/limit parameters instead of full file reads
- [ ] **Grep before read** - Search for specific patterns before reading files
- [ ] **Glob for discovery** - Use Glob to find files by pattern before reading
- [ ] **Context budgeting** - Track cumulative context usage, prioritize critical reads

### Model Selection

- [ ] **Haiku for simple** - File counting, directory listing, simple searches use Haiku
- [ ] **Sonnet for complex** - Architecture analysis, complex debugging, code generation use Sonnet
- [ ] **Opus for critical** - Mission-critical analysis, high-stakes decisions use Opus
- [ ] **Model documentation** - Document why each model was chosen in task descriptions

### Query Structure

- [ ] **File:line format** - Use `[file:line]` → `[action]` format for all requests
- [ ] **Specific outcomes** - Define measurable success criteria for each query
- [ ] **Scope limitation** - Explicitly limit scope to prevent context bloat
- [ ] **Priority ordering** - Structure queries from highest to lowest priority

### Parallel Operations

- [ ] **Identify independence** - Determine which operations can run in parallel
- [ ] **Batch tool calls** - Execute all independent operations in single message
- [ ] **Avoid false dependencies** - Don't serialize operations that don't depend on each other
- [ ] **Error handling** - Plan for partial failures in parallel operations

---

## Summary

**Context Window Management** means strategically optimizing how you use the AI's context window through targeted reads, appropriate model selection, parallel operations, and structured queries.

**Core Rules:**

- **Target precisely** - Read only the lines you need (file:offset:limit), not entire files
- **Match model to task** - Haiku for simple, Sonnet for complex, Opus for critical
- **Parallelize when possible** - Execute independent operations in single message
- **Structure queries** - Use `[file:line]` → `[action]` format for clarity
- **Grep before reading** - Search first, then read targeted results
