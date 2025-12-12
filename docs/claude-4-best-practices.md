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

## Implementation Summary

| Practice | CCO Implementation |
|----------|-------------------|
| **Parallel Tool Execution** | Independent operations run simultaneously |
| **Explicit Instructions** | Commands specify exact behaviors, not vague guidance |
| **Context Motivation** | Rules explain "why" not just "what" |
| **Conservative Judgment** | Evidence-based severity, never guesses |
| **Long-horizon State Tracking** | TodoWrite for progress, git for state |
| **Structured Output** | Consistent formats (`Applied: N | Skipped: N | Failed: N`) |
| **Model Self-Knowledge** | Agent descriptions match capabilities |
| **Subagent Orchestration** | Automatic delegation based on task type |

## Implemented Patterns

### Parallel Tool Execution

Commands that spawn multiple agents use explicit XML blocks for context-specific parallelization:

```markdown
<use_parallel_tool_calls>
When calling multiple tools with no dependencies between them, make all independent
calls in a single message. For example:
- Multiple cco-agent-analyze scopes → launch simultaneously
- Multiple file reads → batch in parallel
- Multiple grep searches → parallel calls

Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

**Applied in:** `cco-optimize.md`, `cco-status.md`, `cco-review.md`, `cco-preflight.md`, `cco-optimize.md`, `cco-research.md`

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

These rules apply to ALL CCO commands automatically. Command-specific `<use_parallel_tool_calls>` blocks provide context-specific examples only (no duplication of global rules).

CCO commands also leverage context awareness through:
- Checking git state before operations
- Saving progress with TodoWrite for long tasks
- State tracking via structured files (context.md, settings.json)

### Agent Model Selection

Claude Code 2.0.17+ handles model selection automatically:
- Plan mode → Sonnet (deep reasoning)
- Execution → Haiku (batch implementation)
- `CLAUDE_CODE_SUBAGENT_MODEL` env var overrides all agent models

| Agent | Purpose | Tools |
|-------|---------|-------|
| `cco-agent-analyze` | Read-only analysis | Glob, Read, Grep, Bash |
| `cco-agent-apply` | Write operations with verification | Grep, Read, Glob, Bash, Edit, Write |
| `cco-agent-research` | External research | WebSearch, WebFetch, Read, Grep, Glob |

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

**Applied in:** `cco-optimize.md`, `cco-optimize.md`, `cco-review.md`

### Batch Approval Pattern

Commands with multi-item fixes use consistent approval UX:

- `multiSelect: true` for batch approvals
- First option = "All (N)" for bulk operations
- Priority order: CRITICAL → HIGH → MEDIUM → LOW
- Item format: `{description} [{file:line}] [{safe|risky}]`

**Applied in:** `cco-optimize.md`, `cco-optimize.md`, `cco-optimize.md`

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

## Not Implemented (Claude Code Handles)

These patterns are handled automatically by Claude Code and don't require explicit prompting:

- **Multi-Context Window State Management** - Claude Code has automatic context compaction
- **Subagent Context Isolation** - Each subagent gets isolated context window
- **State Persistence** - TodoWrite and git state are naturally available
