---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Edit(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-review

**Strategic Review** - Fresh perspective diagnosis + pragmatic optimization via parallel agents.

## Context Requirement

```
test -f ./.claude/rules/cco/context.md && echo "OK" || echo "Run /cco-config first"
```

If not found: Stop immediately with message to run /cco-config.

## User Input

When called without flags:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Focus areas? | Architecture (Recommended); Code Quality (Recommended); Testing & DX; Best Practices | true |

*MultiSelect: Kullanıcı birden fazla alan seçebilir. Tümü seçilirse = Full review.*

## Step Announcements [CRITICAL]

**Before starting each step, announce:** `▶ Step X/5: Step Name`

| Step | Name |
|------|------|
| 1 | Spawn Parallel Agents |
| 2 | Merge Results |
| 3 | Foundation Assessment |
| 4 | Generate Recommendations |
| 5 | Apply Changes |

### Option Mapping

| Option | Covers | Agent Scope |
|--------|--------|-------------|
| Architecture | Foundation, Dependencies, Structure, Layers | architecture |
| Code Quality | Issues, Complexity, Patterns, Consistency | scan (focus=quality) |
| Testing & DX | Test coverage, Test quality, Developer experience, Errors | scan (focus=testing,dx) |
| Best Practices | Tool usage, Parallel execution, Efficiency, Code patterns | best-practices |

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Spawn parallel agents (single message with 3 Task calls)            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scope=architecture)   ──┐                           │
│ Task(cco-agent-analyze, scope=scan)           ──┼──→ All run simultaneously │
│ Task(cco-agent-analyze, scope=best-practices) ──┘                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Merge agent results                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Foundation assessment (SOUND vs HAS ISSUES)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Generate 80/20 recommendations                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 5: Apply via Task(cco-agent-apply) or show report                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Step 1 MUST be a single message with multiple Task tool calls.

## Agent Scopes

| Agent | Scope | Returns |
|-------|-------|---------|
| cco-agent-analyze | `architecture` | Dependency graph, coupling metrics, patterns, layers |
| cco-agent-analyze | `scan` | Issues with file:line, complexity violations |
| cco-agent-analyze | `best-practices` | Tool usage, execution patterns, efficiency opportunities |
| cco-agent-apply | `fix` | Implement approved recommendations |

## Best Practices Scope

Reviews optimal patterns for both code and AI tool usage:

| Category | Reviews |
|----------|---------|
| **Execution Efficiency** | Parallel vs sequential, batching, background tasks |
| **Tool Selection** | Right tool for task, subagent usage, single-message multi-tool |
| **Code Patterns** | Async handling, error boundaries, state management |
| **Architecture** | Layer separation, dependency direction, abstraction levels |

**Recommends:**
- Converting sequential tool calls to parallel where independent
- Using Task tool for complex multi-step searches
- Extracting repeated patterns into shared utilities
- Optimizing hot paths and removing unnecessary operations

## Context Application

| Field | Effect |
|-------|--------|
| Maturity | Legacy → safe incremental; Greenfield → allow restructuring |
| Breaking | Never → flag interface changes as blockers |
| Priority | Speed → quick wins only; Quality → comprehensive |
| Scale | 10K+ → performance focus; <100 → simplicity focus |
| Data | PII/Regulated → security review mandatory |

## Review Rigor

| Requirement | Rule |
|-------------|------|
| Evidence | Every recommendation cites `file:line` |
| Pattern Discovery | 3+ examples before concluding pattern |
| No Speculation | Never recommend changes to unread code |

## Foundation Assessment

From agent results, classify:

| Status | Criteria | Action |
|--------|----------|--------|
| SOUND | Architecture fits purpose, patterns appropriate | Optimize within structure |
| HAS ISSUES | Wrong pattern, missing abstraction, inverted deps | Targeted fixes (not rewrites) |

## Prioritization (80/20)

| Priority | Criteria |
|----------|----------|
| Do Now | High impact, low effort, low risk |
| Plan | High impact, medium effort |
| Consider | Medium impact, needs discussion |
| Backlog | Low impact or high effort |

**Reject:** Recommendations where effort > impact.

## Output

```
┌─ REVIEW SUMMARY ─────────────────────────────────────────────┐
│ Project: {name} | Type: {type} | Foundation: {SOUND|ISSUES}  │
├──────────────────────────────────────────────────────────────┤
│ Coupling: {n} avg | Circular Deps: {n} | Cohesion: {n}%      │
├──────────────────────────────────────────────────────────────┤
│ RECOMMENDATIONS (80/20 filtered)                             │
├───┬──────────────────────────┬────────┬────────┬─────────────┤
│ # │ Recommendation           │ Impact │ Effort │ Priority    │
├───┼──────────────────────────┼────────┼────────┼─────────────┤
│ 1 │ {recommendation}         │ {imp}  │ {eff}  │ {priority}  │
└───┴──────────────────────────┴────────┴────────┴─────────────┘

Applied: {n} | Skipped: {n} | Manual: {n}
```

## Apply Phase

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply recommendations? | All ({N}); Select individual; Skip | false |

## Flags

| Flag | Effect |
|------|--------|
| `--quick` | Single-message analysis, smart defaults |
| `--focus=X` | Focus: architecture, quality, testing, dx, best-practices |
| `--best-practices` | Best practices focus only |
| `--no-apply` | Report only |
| `--matrix` | Show effort/impact matrix |

## Rules

1. **Parallel agents** - Architecture + scan agents run simultaneously
2. **Evidence required** - No recommendations without file:line proof
3. **80/20 filter** - High impact / low effort prioritized
4. **Git safety** - Check status before apply phase
