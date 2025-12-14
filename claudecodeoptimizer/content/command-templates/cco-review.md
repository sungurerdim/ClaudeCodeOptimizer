---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Edit(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-review

**Strategic Review** - Fresh perspective diagnosis + pragmatic optimization via parallel agents.

## Dynamic Context (Pre-collected)

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Maturity, Breaking, Priority, Scale) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## User Input

When called without flags:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Focus areas? | Architecture (Recommended); Code Quality (Recommended); Testing & DX; Best Practices | true |

*MultiSelect: Kullanıcı birden fazla alan seçebilir. Tümü seçilirse = Full review.*

## Progress Tracking [CRITICAL]

**Use TodoWrite to track progress.** Create todo list at start, update status for each step.

```
TodoWrite([
  { content: "Analyze codebase", status: "in_progress", activeForm: "Analyzing codebase" },
  { content: "Generate recommendations", status: "pending", activeForm: "Generating recommendations" },
  { content: "Apply changes", status: "pending", activeForm: "Applying changes" }
])
```

**Update status:** Mark `completed` immediately after each step finishes, mark next `in_progress`.

### Option Mapping

| Option | Covers | Agent Scope |
|--------|--------|-------------|
| Architecture | Foundation, Dependencies, Structure, Layers | architecture |
| Code Quality | Issues, Complexity, Patterns, Consistency | scan (focus=quality) |
| Testing & DX | Test coverage, Test quality, Developer experience, Errors | scan (focus=testing,dx) |
| Best Practices | Tool usage, Parallel execution, Efficiency, Code patterns | best-practices |

## Token Efficiency [CRITICAL]

| Rule | Implementation |
|------|----------------|
| **Single agent** | One analyze agent with all scopes, one apply agent with all fixes |
| **Linter-first** | Run linters before manual analysis |
| **Batch calls** | Multiple tool calls in single message |

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Spawn SINGLE analyze agent with ALL selected scopes                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task(cco-agent-analyze, scopes=[architecture, scan, best-practices])         │
│ → Agent runs linters first, then targeted analysis per scope                 │
│ → Returns combined findings with scope tags                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Foundation assessment (SOUND vs HAS ISSUES)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Generate 80/20 recommendations                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Apply via Task(cco-agent-apply) or show report                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** Use ONE analyze agent and ONE apply agent. Never spawn per-scope agents.

## Agent Usage

| Agent | Input | Output |
|-------|-------|--------|
| cco-agent-analyze | `scopes: [architecture, scan, ...]` | Combined findings JSON |
| cco-agent-apply | `fixes: [finding1, ...]` | Results + verification |

### Scope Coverage

| Scope | Returns |
|-------|---------|
| `architecture` | Dependency graph, coupling metrics, patterns, layers |
| `scan` | Issues with file:line, complexity violations |
| `best-practices` | Tool usage, execution patterns, efficiency opportunities |

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

Applied: {n} | Declined: {n}
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

## Strategy Evolution

After review, update `.claude/rules/cco/context.md` Learnings section:

| Pattern | Action |
|---------|--------|
| Architectural anti-pattern | Add to `Systemic`: pattern + root cause + fix |
| High-impact recommendation accepted | Add to `Prefer`: pattern + impact |
| Recommendation rejected (wrong context) | Add to `Avoid`: pattern + why it failed |

**Max items:** 5 per category (remove oldest when full)

## Rules

1. **Parallel agents** - Architecture + scan agents run simultaneously
2. **Evidence required** - No recommendations without file:line proof
3. **80/20 filter** - High impact / low effort prioritized
4. **Git safety** - Check status before apply phase
