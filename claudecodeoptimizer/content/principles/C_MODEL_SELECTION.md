---
name: model-selection-strategy
description: Choose appropriate Claude model (Haiku/Sonnet/Opus) based on task complexity to optimize cost and performance
type: claude
severity: medium
keywords: [model selection, cost optimization, Haiku, Sonnet, Opus, task complexity]
category: [performance, efficiency]
---

# C_MODEL_SELECTION: Model Selection Strategy

**Severity**: Medium

Choose appropriate Claude model (Haiku/Sonnet/Opus) based on task complexity to optimize cost and performance.

---

## Why

Wrong model selection wastes budget or delivers poor quality. Opus for grep is unnecessarily expensive, Haiku for architecture produces poor quality.

---

## Model Capabilities

| Model | Speed | Cost | Use For |
|-------|-------|------|---------|
| **Haiku** | Fastest | Cheapest | Mechanical tasks, data gathering, simple edits |
| **Sonnet** | Balanced | Mid | Features, bugs, code review (default) |
| **Opus** | Slowest | Highest | Architecture, complex algorithms, deep analysis |

### Selection Framework
```
Mechanical/repetitive?
├─ YES → Haiku
└─ NO → Novel thinking required?
   ├─ YES → Opus
   └─ NO → Sonnet (default)
```

---

## Examples

### ✅ Haiku for Simple
```python
Task("Find deprecated function usages", model="haiku")
Task("Run Black formatter", model="haiku")
Task("Read API docs, summarize", model="haiku")
```

### ✅ Sonnet for Development (Default)
```python
Task("Add email validation to signup", model="sonnet")
Task("Fix null pointer in getUserProfile", model="sonnet")
Task("Review PR #123 for security", model="sonnet")
```

### ✅ Opus for Complex
```python
Task("Design microservices architecture", model="opus")
Task("Optimize recommendation engine", model="opus")
Task("Comprehensive security audit", model="opus")
```

---

## Task Complexity Matrix

**Haiku Territory:**
- Search (grep, find files, count)
- Read (docs, extract info)
- Format (linters, formatters)
- Simple edits (typos, renames)

**Sonnet Territory (Default):**
- Features (add validation, implement API)
- Bug fixes (null pointer, race condition)
- Refactoring (extract function, improve naming)
- Code review (PR review, check security)
- Testing (write tests, fix failures)

**Opus Territory (Rare):**
- Architecture (design microservices, patterns)
- Novel algorithms (optimize performance)
- Deep analysis (security audit, system review)
- Complex trade-offs (technology selection)

---

## Cost Optimization

```python
# ❌ EXPENSIVE: All Opus
Task("Find Python files", model="opus")      # Expensive for simple task
Task("Read package.json", model="opus")      # Expensive for simple task
Task("Format code", model="opus")            # Expensive for simple task
Task("Run tests", model="opus")              # Expensive for simple task

# ✅ OPTIMIZED: Right model (significant savings)
Task("Find Python files", model="haiku")     # Cheap, fast
Task("Read package.json", model="haiku")     # Cheap, fast
Task("Format code", model="haiku")           # Cheap, fast
Task("Run tests", model="sonnet")            # Balanced
```

---

## Parallel Strategy

```python
# Option 1: Sequential Opus (slow, expensive)
Task("Analyze all 10 modules", model="opus")  # Slower, higher cost

# Option 2: Parallel Haiku (fast, cheap)
Task("Analyze module1", model="haiku")  # Fast, cheap
# ... 10 in parallel
# Total: Significantly faster with major cost savings
```

---

## Checklist

- [ ] Mechanical/scriptable? → Haiku
- [ ] Typical development? → Sonnet
- [ ] Novel thinking? → Opus
- [ ] Can parallelize? → Multiple Haiku
- [ ] Defaulting to Sonnet without thinking? → Reconsider
