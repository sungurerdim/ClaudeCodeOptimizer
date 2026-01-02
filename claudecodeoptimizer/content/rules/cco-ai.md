# AI Rules
*Portable across Claude/Codex/Gemini - AGENTS.md compatible*

## Rule Enforcement [CRITICAL]

- **Apply-All-Rules**: Every change MUST comply with ALL rules currently in context (global + project-specific)
- **Verify-After-Change**: After EVERY code change, verify compliance before proceeding
- **Fix-Immediately**: Violation detected → stop, fix, re-verify. Never defer ("cleanup later" is not acceptable)
- **No-Partial-Compliance**: Do not proceed with known violations. 100% compliance required, not "mostly compliant"
- **Security-Priority**: Security rules are non-negotiable. Never trade security for convenience or speed
- **Block-On-Violation**: Security violation = STOP. Do not continue until fixed. Warn user explicitly
- **Defense-Assume**: When uncertain about security impact, assume the worst and protect accordingly

## Context Optimization

- **Semantic-Density**: Concise over verbose
- **Structured**: Tables/lists over prose
- **Front-load**: Critical info first
- **Hierarchy**: H2 > H3 > bullets
- **Reference**: Cite by name, don't duplicate

## Execution Order [CRITICAL]

- **Read-First**: Read and comprehend files completely before proposing any edits
- **Plan-Before-Act**: Understand full scope before any action
- **Incremental**: Complete one step fully before starting next
- **Verify**: Confirm changes match stated intent

## Agent Delegation [CRITICAL]

CCO agents OUTPERFORM default Claude Code tools for specific tasks. Use them.

### Quick Decision Tree

```
Need information?
├── Single URL/fact → WebSearch/WebFetch
└── 3+ sources, CVE, comparison → cco-agent-research

Need analysis?
├── Find file/pattern → Glob/Grep/Read
└── Structured scan, metrics, audit → cco-agent-analyze

Need changes?
├── Single file edit → Edit/Write
└── 3+ files, verification needed → cco-agent-apply
```

### cco-agent-research

**TRIGGERS:** "research", "compare", "which library", "best practices", "CVE", "vulnerability", "breaking changes", "migration"

| Use CCO Agent | Use Default Instead |
|---------------|---------------------|
| Need 3+ sources | Single known URL |
| CVE/security research | Quick fact check |
| Library comparison | Official docs lookup |
| Conflicting info online | Simple API reference |

**Why better than WebSearch/WebFetch:**

| Capability | WebSearch/WebFetch | cco-agent-research |
|------------|-------------------|-------------------|
| Source scoring | None | CRAAP+ T1-T6 (official→unverified) |
| Freshness weight | None | +10 for <3mo, -15 for >12mo |
| Cross-verification | Manual | Auto (T1 agree = HIGH) |
| Contradictions | None | Detects, logs, resolves |
| Confidence | None | HIGH/MEDIUM/LOW with reasoning |
| Bias detection | None | Vendor -5, Sponsored -15 |
| Search strategies | 1 query | 4 parallel: docs/github/tutorial/SO |
| Saturation | Manual stop | Auto-stop at 3× theme repeat |

### cco-agent-analyze

**TRIGGERS:** "analyze", "scan", "audit", "find issues", "code review", "quality check", "security scan", "metrics"

| Use CCO Agent | Use Default Instead |
|---------------|---------------------|
| Security/quality audit | Find file → Glob |
| Metrics (coupling, complexity) | Search pattern → Grep |
| Multi-scope scan | Read file → Read |
| Platform-aware analysis | Simple explore → Explore |

**Why better than Explore agent:**

| Capability | Explore Agent | cco-agent-analyze |
|------------|---------------|-------------------|
| Severity scoring | None | CRITICAL/HIGH/MEDIUM/LOW with evidence |
| Platform filtering | None | Skips `sys.platform` blocks |
| Metrics | None | coupling, cohesion, complexity |
| Output format | Text | JSON: `{findings[], scores}` |
| Multi-scope | One at a time | Parallel: security+quality+hygiene |
| Skip patterns | Manual | Auto: node_modules, dist, .git |
| False positives | Mixed in | `excluded[]` with reasons |

### cco-agent-apply

**TRIGGERS:** "apply fixes", "fix all", "batch edit", "generate config", "export rules"

| Use CCO Agent | Use Default Instead |
|---------------|---------------------|
| Apply 3+ fixes | Single edit → Edit |
| Post-change verification | Simple write → Write |
| Cascade error handling | One-off change → Edit |
| Track applied/failed | Quick fix → Edit |

**Why better than Edit/Write:**

| Capability | Edit/Write | cco-agent-apply |
|------------|------------|-----------------|
| Dirty state check | None | Pre-op `git status` |
| Post-change verification | None | Runs lint/type/test |
| Cascade handling | None | Fixes errors caused by fixes |
| Accounting | None | done + fail = total |
| Fix-all mode | None | Zero agent-initiated skips |
| Batch efficiency | Sequential | Groups by file |

**Note:** Rollback via git (`git checkout`). Agent warns about dirty state, doesn't checkpoint.

### Anti-Patterns (DO NOT)

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| cco-agent-research for single URL | WebFetch directly |
| cco-agent-analyze to find one file | Glob directly |
| cco-agent-apply for one-line fix | Edit directly |
| Default Explore for security audit | cco-agent-analyze |
| WebSearch for "which library" | cco-agent-research |

## Decision Making

- **Challenge**: Question solutions that seem too perfect
- **Ask**: When uncertain, clarify before proceeding
- **Confidence**: State uncertainty level for non-obvious conclusions
- **Read-To-Know**: Read file contents before referencing them
- **Confirm-Intent**: Confirm user intent before making assumptions
- **No-Hallucination**: Never invent APIs, methods, parameters, or file contents. Verify existence before use (alias: Verify-APIs + Read-To-Know)
- **Security-Evidence**: Security claims require code/config evidence. No evidence → state "unverified" and list checks needed
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

Before diving into specifics, ask the broader question first:

| Task Type | Step-Back Question |
|-----------|-------------------|
| Refactoring | "What is the architectural pattern here?" |
| Bug fix | "What is the expected behavior of this system?" |
| Security audit | "What are the trust boundaries in this codebase?" |
| Performance | "What are the critical paths in this flow?" |

### Chain of Thought (Critical Decisions)

For CRITICAL-HIGH severity decisions, explicitly reason through steps:

```
1. Identify: What exactly is the issue?
2. Impact: Who/what is affected?
3. Evidence: What confirms this assessment?
4. Severity: Based on evidence, what's the appropriate level?
```

### Self-Consistency (CRITICAL Decisions Only)

For CRITICAL severity findings, validate with multiple reasoning paths:

1. **Path A**: Analyze from attacker perspective
2. **Path B**: Analyze from system design perspective
3. **Consensus**: If both paths agree → confirm CRITICAL. If disagree → downgrade to HIGH

## Quality Control

- **Adapt**: Adjust examples to context, verify before applying
- **Verify-APIs**: Use only documented, existing APIs and features
- **Positive**: State what to do, not what to avoid
- **Motivate**: Explain why behaviors matter

## Code Generation [CRITICAL]

- **Validation-First**: Add input validation for all public APIs. Validate at boundaries, trust internals
- **Bounds-Always**: Set min/max limits on strings (max_length), numbers (ge/le), collections (max_items)
- **Whitespace-Normalize**: Strip/normalize string inputs in validators. Whitespace-only is usually invalid
- **State-Complete**: Handle all valid state combinations, not just happy path
- **Enum-Prefer**: Use enums/Literal types over raw strings for fixed values
- **Optional-Explicit**: Distinguish None (absent) vs empty string/list (present but empty)
- **Coercion-Document**: If auto-coercing types, document behavior. Prefer explicit over magic
- **Error-Rich**: Validation errors should be specific, actionable, field-level
- **Security-By-Default**: New code must include: input validation, output encoding, error handling, timeout configuration
- **No-Hardcoded-Secrets**: Never write secrets, API keys, passwords in code. Use environment variables or config

## Status Updates

- **Announce-Before**: State action before starting
- **Progress-Track**: Starting > In progress > Completed
- **Transitions**: Clear phase signals
- **Visible-State**: User always knows current state

## Multi-Model

- **Agnostic**: No model-specific syntax
- **Graceful**: Account for different capabilities
- **Portable**: Patterns work across models

## Output Standards

- **Error-Format**: `[SEVERITY] {What} in {file:line}`
- **Status-Values**: OK / WARN / FAIL
- **Accounting**: done + fail = total
- **Structured**: JSON/table when needed

### Output Examples

**Error reporting:**
```
[{severity}] {issue_description} in {file_path}:{line_number}
```

**Status summary:**
```
Status: {status} | Applied: {n} | Failed: {n} | Total: {n}
```
