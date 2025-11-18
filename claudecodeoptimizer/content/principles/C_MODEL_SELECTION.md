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

Wrong model selection wastes budget or delivers poor quality. Opus for grep costs 10x more, Haiku for architecture produces poor quality.

---

## Model Capabilities

| Model | Speed | Cost | Use For |
|-------|-------|------|---------|
| **Haiku** | 3x faster | 10x cheaper | Mechanical tasks, data gathering, simple edits |
| **Sonnet** | Balanced | Mid | Features, bugs, code review (default) |
| **Opus** | Slower | 10x cost | Architecture, complex algorithms, deep analysis |

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
# ❌ EXPENSIVE: All Opus ($1.80)
Task("Find Python files", model="opus")      # $0.50
Task("Read package.json", model="opus")      # $0.30
Task("Format code", model="opus")            # $0.40
Task("Run tests", model="opus")              # $0.60

# ✅ OPTIMIZED: Right model ($0.27, 85% savings)
Task("Find Python files", model="haiku")     # $0.05
Task("Read package.json", model="haiku")     # $0.03
Task("Format code", model="haiku")           # $0.04
Task("Run tests", model="sonnet")            # $0.15
```

---

## Parallel Strategy

```python
# Option 1: Sequential Opus (slow, expensive)
Task("Analyze all 10 modules", model="opus")  # $2.00, 5 min

# Option 2: Parallel Haiku (fast, cheap)
Task("Analyze module1", model="haiku")  # $0.05, 30s
# ... 10 in parallel
# Total: $0.50, 30 seconds (75% savings, 10x faster)
```

---

## Checklist

- [ ] Mechanical/scriptable? → Haiku
- [ ] Typical development? → Sonnet
- [ ] Novel thinking? → Opus
- [ ] Can parallelize? → Multiple Haiku
- [ ] Defaulting to Sonnet without thinking? → Reconsider
