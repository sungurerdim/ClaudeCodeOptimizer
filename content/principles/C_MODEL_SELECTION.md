---
id: C_MODEL_SELECTION
title: Model Selection Strategy
category: claude-guidelines
severity: medium
weight: 7
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_MODEL_SELECTION: Model Selection Strategy 🟡

**Severity**: Medium

Choose appropriate Claude model (Haiku/Sonnet/Opus) based on task complexity. Optimize for cost and performance.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Over-specification** - Using Opus for simple grep operations (10x cost)
- **Under-specification** - Using Haiku for complex architectural decisions (poor quality)
- **Cost inefficiency** - Wrong model selection wastes budget
- **Performance issues** - Slower models when fast ones suffice
- **Quality problems** - Insufficient reasoning capacity for complex tasks

### Model Capabilities

#### Haiku (Fast, Cost-Effective)
- **Speed**: 3x faster than Sonnet
- **Cost**: 10x cheaper than Opus
- **Context**: Up to 200K tokens
- **Reasoning**: Basic pattern matching and simple logic
- **Best for**: Mechanical tasks, data gathering, simple edits

#### Sonnet (Balanced, Default)
- **Speed**: Balanced performance
- **Cost**: Mid-tier pricing
- **Context**: Up to 200K tokens
- **Reasoning**: Strong reasoning, complex problem solving
- **Best for**: Feature development, bug fixes, code review

#### Opus (Advanced Reasoning)
- **Speed**: Slower, thorough
- **Cost**: 10x more than Haiku
- **Context**: Up to 200K tokens
- **Reasoning**: Deep analysis, novel problem solving
- **Best for**: Architecture, complex algorithms, rare use cases

### Selection Framework

**Decision Tree:**
```
Is it mechanical/repetitive?
├─ YES → Haiku
└─ NO → Does it require novel thinking?
   ├─ YES → Opus
   └─ NO → Sonnet (default)
```

---

## Implementation Patterns

### ✅ Good: Haiku for Simple Tasks

```python
# Task: Search codebase for pattern
Task("Find all usages of deprecated function",
     model="haiku",  # ✅ Fast, cost-effective for grep-like tasks
     subagent_type="Explore")

# Task: Format code with linter
Task("Run Black formatter on all Python files",
     model="haiku",  # ✅ Mechanical task, no reasoning needed
     subagent_type="general-purpose")

# Task: Read documentation
Task("Read API documentation and summarize endpoints",
     model="haiku",  # ✅ Simple information extraction
     subagent_type="general-purpose")
```

### ✅ Good: Sonnet for Development (Default)

```python
# Task: Implement feature
Task("Add email validation to signup form",
     model="sonnet",  # ✅ Default for feature work
     subagent_type="general-purpose")

# Task: Fix bug
Task("Fix null pointer exception in getUserProfile",
     model="sonnet",  # ✅ Requires debugging logic
     subagent_type="Fix")

# Task: Code review
Task("Review PR #123 for security issues",
     model="sonnet",  # ✅ Requires judgment and reasoning
     subagent_type="Audit")
```

### ✅ Good: Opus for Complex Reasoning

```python
# Task: Architecture decision
Task("Design microservices architecture for payment system",
     model="opus",  # ✅ Complex architectural reasoning
     subagent_type="Plan")

# Task: Novel algorithm
Task("Optimize recommendation engine algorithm for cold start",
     model="opus",  # ✅ Requires creative problem solving
     subagent_type="general-purpose")

# Task: Deep system analysis
Task("Analyze entire codebase for security vulnerabilities",
     model="opus",  # ✅ Comprehensive deep analysis
     subagent_type="Audit")
```

### ❌ Bad: Wrong Model Selection

```python
# ❌ BAD: Opus for simple grep
Task("Find all TODO comments",
     model="opus",  # ❌ Wasteful! Use Haiku
     subagent_type="Explore")

# ❌ BAD: Haiku for complex architecture
Task("Design distributed transaction system with saga pattern",
     model="haiku",  # ❌ Insufficient reasoning! Use Opus
     subagent_type="Plan")

# ❌ BAD: Always using default (never optimizing)
Task("Format all files", model="sonnet")  # ❌ Should use Haiku
Task("Simple grep", model="sonnet")       # ❌ Should use Haiku
Task("Refactor", model="sonnet")          # ✅ OK (appropriate)
```

---

## Task Complexity Matrix

### Haiku Territory (Mechanical, Simple)

| Task Type | Examples | Why Haiku |
|-----------|----------|-----------|
| **Search** | Grep, find files, count occurrences | Pattern matching |
| **Read** | Read docs, extract info, summarize | Information retrieval |
| **Format** | Run linters, apply formatters | Mechanical transformation |
| **Simple Edits** | Fix typos, rename variables | Straightforward changes |
| **Data Gathering** | List dependencies, check versions | Data collection |

**Haiku Rule**: If task can be scripted, use Haiku.

### Sonnet Territory (Development, Default)

| Task Type | Examples | Why Sonnet |
|-----------|----------|-----------|
| **Features** | Add validation, implement API endpoint | Business logic |
| **Bug Fixes** | Fix null pointer, resolve race condition | Debugging reasoning |
| **Refactoring** | Extract function, improve naming | Code understanding |
| **Code Review** | Review PR, check security | Judgment required |
| **Testing** | Write tests, fix test failures | Test logic |

**Sonnet Rule**: If it's typical development work, use Sonnet.

### Opus Territory (Complex, Rare)

| Task Type | Examples | Why Opus |
|-----------|----------|-----------|
| **Architecture** | Design microservices, choose patterns | Strategic thinking |
| **Novel Algorithms** | Optimize performance, new approach | Creative problem solving |
| **Deep Analysis** | Security audit, full system review | Comprehensive reasoning |
| **Complex Trade-offs** | Technology selection, risk analysis | Multi-factor decisions |

**Opus Rule**: If it requires novel thinking or deep analysis, use Opus.

---

## Anti-Patterns

### ❌ Always Using Opus (Cost Explosion)

```python
# ❌ BAD: Using Opus for everything
Task("Find all Python files", model="opus")       # Cost: $0.50
Task("Read package.json", model="opus")           # Cost: $0.30
Task("Format code", model="opus")                 # Cost: $0.40
Task("Run tests", model="opus")                   # Cost: $0.60
# Total: $1.80

# ✅ GOOD: Right model for each task
Task("Find all Python files", model="haiku")      # Cost: $0.05
Task("Read package.json", model="haiku")          # Cost: $0.03
Task("Format code", model="haiku")                # Cost: $0.04
Task("Run tests", model="sonnet")                 # Cost: $0.15
# Total: $0.27 (85% savings!)
```

### ❌ Never Using Opus (Quality Problems)

```python
# ❌ BAD: Using Haiku for complex architecture
Task("""Design a distributed transaction system handling:
- Multi-region consistency
- Saga pattern compensation
- Event sourcing
- CQRS
- CAP theorem trade-offs
""", model="haiku")  # ❌ Insufficient reasoning capacity

# Result: Poor architecture, missing edge cases, incorrect trade-offs

# ✅ GOOD: Use Opus for complex decisions
Task("""Design a distributed transaction system...""",
     model="opus")  # ✅ Appropriate for complexity
```

### ❌ Default to Sonnet Always (Missed Optimization)

```python
# ❌ BAD: Never optimizing model selection
Task("Find files", model="sonnet")           # Should be Haiku
Task("Read docs", model="sonnet")            # Should be Haiku
Task("Implement feature", model="sonnet")    # ✅ Correct
Task("Design architecture", model="sonnet")  # Should be Opus

# Result: Higher costs, slower execution for simple tasks
```

---

## Parallel Agent Strategy

### Haiku Parallelism (Cost-Effective)

```python
# ✅ GOOD: Parallel Haiku agents instead of one Opus
# Task: Analyze 10 modules for unused imports

# Option 1: Sequential Opus (slow, expensive)
Task("Analyze all 10 modules", model="opus")  # $2.00, 5 minutes

# Option 2: Parallel Haiku (fast, cheap)
Task("Analyze module1", model="haiku")  # $0.05, 30 seconds
Task("Analyze module2", model="haiku")  # $0.05, 30 seconds
# ... (all 10 in parallel)
# Total: $0.50, 30 seconds (75% cost saving, 10x faster!)
```

**Parallelization Rule**: If task can be split, use multiple Haiku agents.

---

## Decision Checklist

Before selecting model, ask:

- [ ] **Is this mechanical?** (Grep, format, read) → Haiku
- [ ] **Can it be scripted?** → Haiku
- [ ] **Is it typical development?** (Features, bugs, tests) → Sonnet
- [ ] **Does it require novel thinking?** → Opus
- [ ] **Is it complex architecture?** → Opus
- [ ] **Can it be parallelized?** → Multiple Haiku agents
- [ ] **Am I defaulting to Sonnet without thinking?** → Reconsider

---

## Cost Analysis Examples

### Example 1: Refactoring Project

**Bad Approach (Always Opus):**
```
1. Search for pattern: Opus ($0.50)
2. Read files: Opus ($1.20)
3. Refactor code: Opus ($2.00)
4. Run tests: Opus ($0.80)
5. Format code: Opus ($0.30)
Total: $4.80
```

**Good Approach (Right Models):**
```
1. Search for pattern: Haiku ($0.05)
2. Read files: Haiku ($0.12)
3. Refactor code: Sonnet ($0.50)
4. Run tests: Sonnet ($0.20)
5. Format code: Haiku ($0.03)
Total: $0.90 (81% savings!)
```

### Example 2: Architecture Design

**Bad Approach (Always Haiku):**
```
Design microservices architecture: Haiku ($0.10)
Result: Poor quality, missing considerations
Rework needed: Sonnet ($2.00)
Total: $2.10 + wasted time
```

**Good Approach (Opus First):**
```
Design microservices architecture: Opus ($1.50)
Result: High quality, comprehensive analysis
Total: $1.50 (correct the first time)
```

---

## Model Selection by Programming Language

All models work with all languages, but complexity drives selection:

| Language | Simple Tasks | Typical Work | Complex Design |
|----------|-------------|--------------|----------------|
| Python | Haiku | Sonnet | Opus |
| JavaScript | Haiku | Sonnet | Opus |
| Go | Haiku | Sonnet | Opus |
| Rust | Haiku | Sonnet | Opus (ownership complexity) |
| Java | Haiku | Sonnet | Opus (enterprise patterns) |

**Note**: Language doesn't change model selection strategy.

---

## Summary

**Model Selection Strategy** means choosing the appropriate Claude model (Haiku/Sonnet/Opus) based on task complexity to optimize cost and performance.

**Core Rules:**
- **Haiku**: Mechanical, simple, scriptable tasks (fast, cheap)
- **Sonnet**: Typical development work (default, balanced)
- **Opus**: Complex reasoning, architecture, novel problems (rare, expensive)
