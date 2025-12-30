# Claude 4 Best Practices Reference

This document details how CCO implements official Claude 4 best practices and Opus 4.5 optimizations.

## Official Documentation

| Resource | Description |
|----------|-------------|
| [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices) | Prompt engineering patterns |
| [Sub-agents](https://code.claude.com/docs/en/sub-agents) | Agent architecture |
| [Slash Commands](https://code.claude.com/docs/en/slash-commands) | Command syntax and frontmatter |
| [Memory & Rules](https://code.claude.com/docs/en/memory) | Rules directory structure |
| [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | Feature history |
| [Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5) | Model capabilities |
| [Google Prompt Engineering Whitepaper](https://www.kaggle.com/whitepaper-prompt-engineering) | Instruction-First, Few-Shot, CoT, Self-Consistency patterns |

## Implementation Summary

| Practice | CCO Implementation |
|----------|-------------------|
| **Parallel Tool Execution** | `[PARALLEL]` markers, background tasks, multi-agent launches |
| **Explicit Instructions** | Commands specify exact behaviors, not vague guidance |
| **Context Motivation** | Rules explain "why" not just "what" |
| **Conservative Judgment** | Evidence-based severity, never guesses |
| **Long-horizon State Tracking** | TodoWrite + git state + structured findings JSON |
| **Structured Output** | Consistent formats (`Status: X | Applied: N | Skipped: N | Failed: N | Total: N`) |
| **Model Self-Knowledge** | Agent descriptions match capabilities |
| **Subagent Orchestration** | Automatic delegation based on task type |
| **Over-engineering Prevention** | YAGNI + KISS + Scope rules in Core |

## Implemented Patterns

### Parallel Tool Execution

Official Claude 4 documentation recommends the `<use_parallel_tool_calls>` XML block pattern. CCO achieves the same goal through alternative patterns:

**CCO Patterns (Alternative Implementation):**
- `[PARALLEL]` step markers for simultaneous operations
- `run_in_background: true` for non-blocking analysis
- Multiple Task launches in single message for agent parallelism

**Applied in:**
- `cco-checkup.md`: Parallel health + audit execution
- `cco-commit.md`: Parallel quality gates (secrets, format, lint, types)
- `cco-optimize.md`: Background analysis during user questions
- `cco-preflight.md`: Parallel phase execution

> **Note:** CCO does not use the official `<use_parallel_tool_calls>` XML block. Instead, it relies on step markers and background execution patterns that achieve equivalent parallel behavior.

### Efficiency (Global AI Rules)

Efficiency patterns are **global AI rules** in `~/.claude/rules/cco/ai.md`:

```markdown
## Efficiency

- **Parallel-Independent**: Run unrelated operations simultaneously
- **Sequential-Dependent**: Chain operations that depend on prior results
- **Batch-Reads**: Multiple file reads in single call when possible
- **No-Bash-Loops**: Avoid `for f in *; do..done` - use single commands or parallel tool calls
- **Background-Long**: Long-running commands (servers, tails) → background, continue working
- **Complete-Fully**: Never stop early due to context concerns - auto-compaction handles limits
```

These rules apply to ALL CCO commands automatically.

### Long-horizon State Tracking

Official Claude 4 documentation emphasizes state tracking for extended tasks. CCO implements this through:

**Structured State (JSON):**
- `context.md`: Project configuration and detection results
- Findings arrays with `{ id, scope, severity, location, fix }` schema

**Progress Tracking:**
- TodoWrite for step-by-step progress visibility
- Git status checks before/after operations
- Accounting format: `Status: {OK|WARN} | Applied: N | {Declined|Not Selected}: N | Failed: N | Total: N`
  - Use "Declined" when user actively rejects items (approval flow)
  - Use "Not Selected" when items excluded by mode choice (Essential/Thorough)

**State Persistence (from official docs):**
```text
Use git for state tracking: Git provides a log of what's been done and
checkpoints that can be restored. Claude 4.5 models perform especially
well in using git to track state across multiple sessions.
```

**Applied in:** All CCO commands use TodoWrite + git state checks

### Model Selection Architecture

CCO uses a tiered model strategy based on Opus 4.5 performance data:

**Commands:**
| Command | Model | Rationale |
|---------|-------|-----------|
| `cco-optimize` | opus | Deep security/quality analysis |
| `cco-research` | opus | Complex synthesis and reasoning |
| `cco-review` | opus | Architecture analysis |
| `cco-commit` | opus | Quality gates, 50-75% fewer lint errors |
| Others | inherit | Orchestration only |

**Sub-agents:**
| Agent | Model | Rationale |
|-------|-------|-----------|
| `cco-agent-analyze` | haiku | Read-only, fast scanning |
| `cco-agent-apply` | opus | Coding SOTA, 50-75% fewer tool errors |
| `cco-agent-research` | haiku | Fast web fetches |

**Architecture:**
```
Opus Commands (analysis + coding)
    └── cco-optimize, cco-research, cco-review, cco-commit

Inherit Commands (orchestration)
    └── cco-config, cco-status, cco-checkup, cco-preflight

Sub-agents
    └── analyze: haiku (read-only)
    └── apply: opus (writes)
    └── research: haiku (web)
```

**Opus 4.5 Performance Advantages (from announcement):**
- SWE-bench Verified: State-of-the-art
- Aider Polyglot: +10.6% improvement
- Tool calling errors: 50-75% reduction
- Vending-Bench (autonomous): +29% improvement

**Model Strategy:** Opus + Haiku only (no Sonnet). Opus for intelligence, Haiku for speed.

### Instruction-First Approach

CCO rules use positive instructions instead of negative constraints:

| Negative (Avoided) | Positive (Used) |
|--------------------|-----------------|
| "Never guess file contents" | "Read files before referencing them" |
| "No hallucination" | "Use only documented, existing APIs" |
| "Don't swallow exceptions" | "Log all exceptions with context" |

**Why:** Positive instructions are clearer. The model performs better when told what TO do.

**Applied in:** `cco-core.md`, `cco-ai.md`

### Reasoning Strategies

For critical decisions, CCO implements structured reasoning:

| Strategy | When | Pattern |
|----------|------|---------|
| **Step-Back** | Complex tasks | Ask broader question first |
| **Chain of Thought** | P0-P1 severity | Explicit 4-step reasoning |
| **Self-Consistency** | CRITICAL only | Multiple paths + consensus |

**Example (Self-Consistency for P0):**
```
Path A: Analyze from attacker perspective
Path B: Analyze from system design perspective
Consensus: Both agree → confirm P0. Disagree → downgrade to P1
```

**Applied in:** `cco-ai.md` Reasoning Strategies section

### Placeholder Standards

All examples use `{placeholder}` format, never hardcoded values:

| Type | Format |
|------|--------|
| Simple | `{name}` |
| Enumerated | `{opt1\|opt2}` |
| Numeric | `{n}` |
| Location | `{file}:{line}` |

**Why:** Hardcoded examples can be misinterpreted as commands.

**Applied in:** All command templates, agent templates

### Conservative Judgment

Commands that report findings embed severity rules:

| Keyword | Severity | Confidence Required |
|---------|----------|---------------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

**Rules:**
- When uncertain between severities, choose lower
- Require explicit evidence, not inference
- Style issues never escalate to CRITICAL or HIGH

**Applied in:** `cco-optimize.md`, `cco-review.md`

### Batch Approval Pattern

Commands with multi-item fixes use consistent approval UX:

- `multiSelect: true` for batch approvals
- First option = "All (N)" for bulk operations
- Priority order: CRITICAL → HIGH → MEDIUM → LOW
- Item format: `{description} [{file:line}] [{safe|risky}]`

**Applied in:** `cco-optimize.md`, `cco-review.md`, `cco-preflight.md`

### Output Formatting

Agents use consistent table formatting:

| Element | Characters |
|---------|------------|
| Borders | `─│┌┐└┘├┤┬┴┼` |
| Headers | `═║╔╗╚╝` |
| Numbers | Right-aligned |
| Text | Left-aligned |
| Status | `OK` `WARN` `FAIL` `PASS` `SKIP` |

**Applied in:** `cco-agent-analyze.md`, `cco-agent-apply.md`

### YAML Frontmatter

Commands use Claude Code's frontmatter options:

```yaml
---
name: cco-optimize
description: Security and code quality analysis
allowed-tools: Read(*), Grep(*), Glob(*), Task(*)
---
```

## Opus 4.5 Optimizations

Built for [Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5):

| Opus 4.5 Feature | CCO Alignment |
|------------------|---------------|
| Multi-agent coordination | Parallel agent spawning in commands |
| Context management | `<context_awareness>` prompt |
| Plan Mode precision | Commands structured for planning |
| Self-improving iterations | TodoWrite tracking supports iteration |
| Tool use improvements | Explicit tool lists in allowed-tools |

Additional optimizations:
- Precise instruction following without over-prompting
- Reduced verbosity with XML format indicators
- Parallel tool calling for maximum efficiency
- Context-aware token budget management

### Over-engineering Prevention

Official Claude 4 documentation warns about overeagerness. CCO addresses this through YAGNI rule:

**Official Pattern (from Claude 4 Best Practices):**
```text
Avoid over-engineering. Only make changes that are directly requested or
clearly necessary. Keep solutions simple and focused.

Don't add features, refactor code, or make "improvements" beyond what was
asked. Don't create helpers, utilities, or abstractions for one-time
operations. Don't design for hypothetical future requirements.
```

**CCO Implementation (Core Rules):**
- **YAGNI**: Don't add features beyond request. DO add robustness (validation, edge cases, error handling) - robustness is NOT a feature
- **KISS**: Simplest solution that works correctly for all valid inputs
- **Scope**: Only requested changes, general solutions

---

## Not Implemented (Claude Code Handles)

These patterns are handled automatically by Claude Code and don't require explicit prompting:

- **Multi-Context Window State Management** - Claude Code has automatic context compaction
- **Subagent Context Isolation** - Each subagent gets isolated context window
- **State Persistence** - TodoWrite and git state are naturally available
