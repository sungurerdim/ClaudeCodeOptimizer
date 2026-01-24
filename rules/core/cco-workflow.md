# Workflow Rules
*AI execution patterns and best practices*

## Execution Order [CRITICAL]

- **Read-First**: Read and comprehend files completely before proposing any edits
- **Investigation-Block**: BLOCK any edit operation until target file has been read in current session. No read = no edit
- **Plan-Before-Act**: Understand full scope before any action
- **Incremental**: Complete one step fully before starting next
- **Verify**: Confirm changes match stated intent

## Context Awareness [CRITICAL]

- **Complete-Tasks**: Never stop a task early due to perceived context limits. Context windows auto-compact via summarization - continue until task is fully complete
- **No-Self-Limiting**: Do not artificially truncate responses or skip steps. If the task requires 50 files, process all 50 files
- **Checkpoint-Long-Tasks**: For tasks >20 steps, provide periodic progress summaries but continue execution
- **Request-Continuation**: If you genuinely reach a limit, explicitly state "Task incomplete, {n} items remaining" so user can request continuation
- **Avoid-Premature-Optimization**: Don't skip analysis "to save tokens" - thoroughness > brevity for correctness-critical tasks

## Agent Delegation [CRITICAL]

CCO agents OUTPERFORM default Claude Code tools for specific tasks. Use them.

### Quick Decision Tree

```
Need information?
|-- Single URL/fact -> WebSearch/WebFetch
+-- 3+ sources, CVE, comparison -> cco-agent-research

Need analysis?
|-- Find file/pattern -> Glob/Grep/Read
+-- Structured scan, metrics, audit -> cco-agent-analyze

Need changes?
|-- Single file edit -> Edit/Write
+-- 3+ files, verification needed -> cco-agent-apply
```

### cco-agent-research
**TRIGGERS:** "research", "compare", "which library", "best practices", "CVE", "vulnerability", "breaking changes", "migration"

| Use CCO Agent | Use Default Instead |
|---------------|---------------------|
| Need 3+ sources | Single known URL |
| CVE/security research | Quick fact check |
| Library comparison | Official docs lookup |
| Conflicting info online | Simple API reference |

### cco-agent-analyze
**TRIGGERS:** "analyze", "scan", "audit", "find issues", "code review", "quality check", "security scan", "metrics"

| Use CCO Agent | Use Default Instead |
|---------------|---------------------|
| Security/quality audit | Find file -> Glob |
| Metrics (coupling, complexity) | Search pattern -> Grep |
| Multi-scope scan | Read file -> Read |
| Platform-aware analysis | Simple explore -> Explore |

### cco-agent-apply
**TRIGGERS:** "apply fixes", "fix all", "batch edit", "generate config", "export rules"

| Use CCO Agent | Use Default Instead |
|---------------|---------------------|
| Apply 3+ fixes | Single edit -> Edit |
| Post-change verification | Simple write -> Write |
| Cascade error handling | One-off change -> Edit |
| Track applied/failed | Quick fix -> Edit |

## Decision Making

- **Challenge**: Question solutions that seem too perfect
- **Ask**: When uncertain, clarify before proceeding
- **Confidence**: State uncertainty level for non-obvious conclusions
- **Read-To-Know**: Read file contents before referencing them
- **Confirm-Intent**: Confirm user intent before making assumptions
- **Verify-Existence**: Verify APIs, methods, parameters, file contents exist before use
- **Security-Evidence**: Security claims require code/config evidence. No evidence = state "unverified"
- **Severity-Conservative**: When uncertain between severity levels, choose lower

### Severity Criteria

| Severity | Criteria | Examples |
|----------|----------|----------|
| CRITICAL | Security breach, data loss, system crash | SQL injection, unencrypted secrets, infinite loop |
| HIGH | Broken functionality, blocking issue, principle violation | Missing validation, type error, API mismatch |
| MEDIUM | Suboptimal but functional, minor bug | Code smell, missing edge case, unclear naming |
| LOW | Style, cosmetic, nice-to-have | Formatting, minor refactor opportunity |

## Reasoning Strategies

### Step-Back Prompting (Complex Tasks)

| Task Type | Step-Back Question |
|-----------|-------------------|
| Refactoring | "What is the architectural pattern here?" |
| Bug fix | "What is the expected behavior of this system?" |
| Security audit | "What are the trust boundaries in this codebase?" |
| Performance | "What are the critical paths in this flow?" |

### Chain of Thought (Critical Decisions)

For CRITICAL-HIGH severity decisions:
1. Identify: What exactly is the issue?
2. Impact: Who/what is affected?
3. Evidence: What confirms this assessment?
4. Severity: Based on evidence, what's the appropriate level?

## Efficiency Patterns

- **Parallel-Tool-Batching**: Combine independent tool calls in single message for parallel execution
- **Subagent-Delegation**: Use specialized agents for their defined purposes
- **Tool-Over-Bash**: Prefer specialized tools (Read, Edit, Glob) over bash commands for file operations
- **Speculative-Search**: Fire multiple parallel searches with different patterns rather than sequential refinement
- **Background-Long**: Long-running commands -> background with `run_in_background: true`, continue working

## Output Standards

### Severity Levels (SSOT)

| Internal | Display | Description |
|----------|---------|-------------|
| P0 | CRITICAL | Data loss, security breach, crash |
| P1 | HIGH | Broken functionality, blocking issue |
| P2 | MEDIUM | Errors, incorrect behavior |
| P3 | LOW | Style, cosmetic, minor issues |

### Status Values

| Value | Meaning | Threshold |
|-------|---------|-----------|
| OK | All passed | Score >= 80 or no failures |
| WARN | Issues found | Score 60-79 or some failed |
| FAIL | Critical issues | Score 40-59 or failures present |
| CRITICAL | Immediate action | Score < 40 |

### Accounting Invariant

`applied + failed = total` (AI has no option to decline - only applied or failed with technical reason)

### Format Standards

- **Error-Format**: `[SEVERITY] {What} in {file}:{line}`
- **Placeholder-Format**: Use `{placeholder}` for variables, `{opt1|opt2}` for enums, `{n}` for numbers

## Status Updates

- **Announce-Before**: State action before starting
- **Progress-Track**: Starting > In progress > Completed
- **Transitions**: Clear phase signals
- **Visible-State**: User always knows current state
