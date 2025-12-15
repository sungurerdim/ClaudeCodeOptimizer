---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Edit(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-review

**Strategic Review** - Fresh perspective diagnosis + pragmatic optimization via parallel agents.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`

**DO NOT re-run these commands. Use the pre-collected values above.**
**Static context (Maturity, Breaking, Priority, Scale) from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## User Input

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Focus areas? | Architecture (Recommended); Code Quality (Recommended); Testing & DX; Best Practices | true |

| Option | Agent Scope |
|--------|-------------|
| Architecture | architecture |
| Code Quality | scan (focus=quality) |
| Testing & DX | scan (focus=testing,dx) |
| Best Practices | best-practices |

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Analyze codebase", status: "in_progress", activeForm: "Analyzing codebase" },
  { content: "Generate recommendations", status: "pending", activeForm: "Generating recommendations" },
  { content: "Apply changes", status: "pending", activeForm: "Applying changes" }
])
```

## Token Efficiency [CRITICAL]

Single analyze agent │ Single apply agent │ Linter-first │ Batch calls

## Execution Flow

| Step | Action |
|------|--------|
| 1. Analyze | `Task(cco-agent-analyze, scopes=[...])` → Combined findings |
| 2. Foundation | Assess SOUND vs HAS ISSUES |
| 3. Recommendations | Generate 80/20 filtered list |
| 4. Apply | `Task(cco-agent-apply)` or report only |

**CRITICAL:** ONE analyze agent, ONE apply agent. Never per-scope.

## Scope Coverage

| Scope | Returns |
|-------|---------|
| `architecture` | Dependency graph, coupling, patterns, layers |
| `scan` | Issues with file:line, complexity |
| `best-practices` | Tool usage, execution patterns, efficiency |

## Best Practices Scope

| Category | Reviews |
|----------|---------|
| Execution | Parallel vs sequential, batching |
| Tool Selection | Right tool, subagent usage |
| Code Patterns | Async, error boundaries, state |
| Architecture | Layer separation, dependencies |

## Context Application

| Field | Effect |
|-------|--------|
| Maturity | Legacy → safe; Greenfield → restructure |
| Breaking | Never → flag as blockers |
| Priority | Speed → quick wins; Quality → comprehensive |
| Scale | 10K+ → performance; <100 → simplicity |
| Data | PII/Regulated → security mandatory |

## Foundation Assessment

| Status | Action |
|--------|--------|
| SOUND | Optimize within structure |
| HAS ISSUES | Targeted fixes (not rewrites) |

## Prioritization (80/20)

| Priority | Criteria |
|----------|----------|
| Do Now | High impact, low effort |
| Plan | High impact, medium effort |
| Consider | Medium impact |
| Backlog | Low impact or high effort |

## Apply Phase

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply recommendations? | All ({N}); Select individual; Skip | false |

## Flags

| Flag | Effect |
|------|--------|
| `--quick` | Smart defaults |
| `--focus=X` | architecture, quality, testing, dx, best-practices |
| `--best-practices` | Best practices only |
| `--no-apply` | Report only |
| `--matrix` | Effort/impact matrix |

## Strategy Evolution

| Pattern | Action |
|---------|--------|
| Architectural anti-pattern | Add to `Systemic` |
| High-impact accepted | Add to `Prefer` |
| Rejected (wrong context) | Add to `Avoid` |

## Rules

Parallel agents │ Evidence required │ 80/20 filter │ Git safety
