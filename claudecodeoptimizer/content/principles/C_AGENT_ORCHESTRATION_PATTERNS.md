---
name: agent-orchestration-patterns
description: Orchestrate multiple agents via parallel execution, pipelines, and appropriate model selection for optimal cost/performance
type: claude
severity: high
keywords: [orchestration, parallel execution, agent management, cost optimization, workflow]
category: [workflow, performance]
---

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
# 5 modules in parallel (significantly faster than sequential)
Task("Analyze auth module", model="haiku")
Task("Analyze payment module", model="haiku")
Task("Analyze user module", model="haiku")
Task("Analyze product module", model="haiku")
Task("Analyze order module", model="haiku")
# Cost-efficient parallel execution
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
Task("Identify top 5 critical modules", model="opus")  # Planning phase
# Then parallel:
Task("Audit auth module", model="sonnet")  # Execution phase
Task("Audit payment module", model="sonnet")
Task("Audit user module", model="sonnet")
# Faster execution with optimized cost
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
| **Haiku** | Fastest | Cheapest | Grep, format, read, simple edits |
| **Sonnet** | Balanced | Mid | Features, bugs, code review (default) |
| **Opus** | Slowest | Highest | Architecture, complex algorithms |

---

## Cost Optimization

```python
# ❌ EXPENSIVE: All Opus
Task("Find Python files", model="opus")    # Expensive for simple task
Task("Read configs", model="opus")         # Expensive for simple task
Task("Analyze architecture", model="opus") # Appropriate complexity
Task("List dependencies", model="opus")    # Expensive for simple task

# ✅ OPTIMIZED: Right model (significant savings)
Task("Find Python files", model="haiku")   # Cheap, fast
Task("Read configs", model="haiku")        # Cheap, fast
Task("Analyze architecture", model="opus") # Appropriate complexity
Task("List dependencies", model="haiku")   # Cheap, fast
```

---

## Context Efficiency Through Sub-Agent Delegation**Principle**: Prefer sub-agents over direct tool calls to keep main session context clean and efficient.### Why Sub-Agents for Context EfficiencyMain session context is expensive and accumulates. Sub-agents:- Use separate context windows (don't pollute main session)- Can be parallelized (faster + cleaner)- Isolate complex operations (grep loops, file analysis)- Enable better token management (results summarized back)### Decision Framework```Task requires multiple operations?├─ Independent data gathering? → Sub-agent (Explore)├─ Sequential analysis? → Sub-agent (general-purpose)├─ Simple single operation? → Direct tool call└─ Complex multi-step? → Sub-agent```### Examples```python# ❌ BAD: Direct tool calls pollute main contextfiles = Glob("**/*.{FILE_EXT}")  # {FILE_COUNT} files in main contextfor file in files:    content = Read(file)  # {FILE_COUNT} reads in main context    if "{SEARCH_PATTERN}" in content:        results.append(extract_data(content))# Main context now has {FILE_COUNT}+ file reads!# ✅ GOOD: Sub-agent isolates operationsTask({    subagent_type: "Explore",    model: "haiku",    prompt: "Find all {SEARCH_PATTERN} in {FILE_TYPE} files. Return summary: file paths and {RESULT_TYPE} only."})# Main context receives only summary (clean!)# ❌ BAD: Complex grep loop in main sessionfor pattern in {PATTERN_LIST}:    results = Grep(pattern, output_mode="content")    analyze_results(results)# Main context accumulates all grep results# ✅ GOOD: Delegate to sub-agentTask({    subagent_type: "general-purpose",    model: "sonnet",    prompt: "Search for {CATEGORY} patterns: {PATTERN_LIST}. Return findings with file:line references."})# Main context gets only findings summary```### When Direct Tools Are OK```python# ✅ Single targeted readRead("{CONFIG_FILE}")# ✅ Single specific grepGrep("{SEARCH_PATTERN}", output_mode="files_with_matches")# ✅ Simple editEdit("{FILE_PATH}", old="{OLD_VALUE}", new="{NEW_VALUE}")# ✅ Single bash commandBash("{TEST_COMMAND}")```### Sub-Agent Benefits Quantified| Operation | Direct Tools (Main Context) | Sub-Agent | Savings ||-----------|----------------------------|-----------|---------| | Analyze {FILE_COUNT} files | {FILE_COUNT} Read calls (~{TOKEN_COUNT_LARGE}K tokens) | 1 Task call (~{TOKEN_COUNT_SMALL}K tokens) | {SAVINGS_PERCENT}% || Complex search | {ITERATION_COUNT}+ Grep iterations (~{TOKEN_COUNT_MED}K tokens) | 1 Explore agent (~{TOKEN_COUNT_TINY}K tokens) | {SAVINGS_PERCENT}% || Multi-step analysis | All intermediate results (~{TOKEN_COUNT_LARGE}K tokens) | Final summary only (~{TOKEN_COUNT_SMALL}K tokens) | {SAVINGS_PERCENT}% |---
## Checklist

- [ ] Pattern identified? (Fan-out/Pipeline/Hierarchical/Scatter-Gather)
- [ ] Dependencies mapped?
- [ ] Parallelization opportunities?
- [ ] Right model per agent?
- [ ] Cost estimated?
- [ ] Error handling planned?
- [ ] Could use sub-agent for context efficiency? (multi-file operations, complex searches, iterative analysis)
- [ ] Direct tools only for simple single operations?
