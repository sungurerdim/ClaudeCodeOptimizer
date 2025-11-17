# C_AGENT_ORCHESTRATION_PATTERNS: Agent Orchestration Patterns

**Severity**: High

Orchestrate multiple agents via parallel execution, pipelines, and appropriate model selection for optimal cost/performance.

---

## Why

Poor orchestration wastes resources through sequential bottlenecks, wrong model choices (Opus for grep, Haiku for architecture), and lack of parallelization strategy.

---

## Patterns

### 1. Parallel Fan-Out
**When**: Independent tasks
```python
# 5 modules in parallel (2 min vs 10 min sequential)
Task("Analyze auth module", model="haiku")
Task("Analyze payment module", model="haiku")
Task("Analyze user module", model="haiku")
Task("Analyze product module", model="haiku")
Task("Analyze order module", model="haiku")
# Cost: 5 * $0.10 = $0.50
```

### 2. Sequential Pipeline
**When**: Dependencies exist
```python
# Build → Test → Deploy
Task("Build application", model="sonnet")  # Wait
Task("Run test suite", model="sonnet")     # Wait
Task("Deploy to staging", model="haiku")
```

### 3. Hierarchical Decomposition
**When**: Complex task breaks into subtasks
```python
# Strategy (Opus) → Parallel execution (Sonnet)
Task("Identify top 5 critical modules", model="opus")  # 3 min
# Then parallel:
Task("Audit auth module", model="sonnet")  # 5 min parallel
Task("Audit payment module", model="sonnet")
Task("Audit user module", model="sonnet")
# Time: 8 min (3 + 5), Cost: $2.50
```

### 4. Scatter-Gather
**When**: Parallel work needs synthesis
```python
# Scatter: Parallel reviews
Task("Security review", model="sonnet")
Task("Performance review", model="sonnet")
Task("Quality review", model="sonnet")
# Gather: Synthesize
Task("Create action plan from reviews", model="sonnet")
```

---

## Model Selection

| Model | Speed | Cost | Use For |
|-------|-------|------|---------|
| **Haiku** | 3x faster | 10x cheaper | Grep, format, read, simple edits |
| **Sonnet** | Balanced | Mid | Features, bugs, code review (default) |
| **Opus** | Slower | 10x cost | Architecture, complex algorithms |

---

## Cost Optimization

```python
# ❌ EXPENSIVE: All Opus ($3.90)
Task("Find Python files", model="opus")    # $1.00
Task("Read configs", model="opus")         # $0.80
Task("Analyze architecture", model="opus") # $1.50
Task("List dependencies", model="opus")    # $0.60

# ✅ OPTIMIZED: Right model ($1.60, 59% savings)
Task("Find Python files", model="haiku")   # $0.05
Task("Read configs", model="haiku")        # $0.03
Task("Analyze architecture", model="opus") # $1.50
Task("List dependencies", model="haiku")   # $0.02
```

---

## Checklist

- [ ] Pattern identified? (Fan-out/Pipeline/Hierarchical/Scatter-Gather)
- [ ] Dependencies mapped?
- [ ] Parallelization opportunities?
- [ ] Right model per agent?
- [ ] Cost estimated?
- [ ] Error handling planned?
