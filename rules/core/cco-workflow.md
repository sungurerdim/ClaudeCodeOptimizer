# Workflow Rules
*Execution patterns and enforcement*

## Read-Before-Edit [BLOCKER]

**BLOCK**: Any edit to a file not yet read in this session.

```
Edit request?
├── File read? → OK to edit
└── Not read? → Read first, then edit
```

Before calling any function/API, verify it exists with expected signature.

## Task Completion [BLOCKER]

**BLOCK**: Stopping early due to perceived limits.

- Task needs 50 files? Process all 50.
- Context getting long? Continue anyway.
- Format: `"Task incomplete, {n} items remaining"` (if must pause)

**Checkpoints**: Every 20 steps, brief progress summary. Every 5 steps, verify goal alignment.

## Severity Levels [CHECK]

| Level | Criteria | Examples |
|-------|----------|----------|
| CRITICAL | Security, data loss, crash | SQL injection, secrets exposed |
| HIGH | Broken functionality | Missing validation, API mismatch |
| MEDIUM | Suboptimal but works | Code smell, missing edge case |
| LOW | Style only | Formatting, naming |

**When uncertain → choose lower severity.**

## Reasoning [CHECK]

### For CRITICAL/HIGH findings:

1. **Identify**: What exactly is the issue?
2. **Evidence**: What confirms this?
3. **Counter-check**: Could this be intentional? If uncertain → downgrade

### For complex logic:

- Pick 2-3 inputs (normal, edge, error)
- Trace execution mentally
- If unclear: `"Logic uncertain at [point]"`

## Agent Delegation [CHECK]

```
Information needed?
├── Single fact → WebSearch/WebFetch
└── 3+ sources → cco-agent-research

Analysis needed?
├── Find file/pattern → Glob/Grep/Read
└── Structured audit → cco-agent-analyze

Changes needed?
├── 1-2 files → Edit/Write
└── 3+ files → cco-agent-apply
```

## Efficiency

- **Parallel calls**: Independent tool calls in single message
- **Background**: Long commands → `run_in_background: true`

## No Deferrals [BLOCKER - Auto Mode]

When `--auto` active, AI MUST attempt every fix.

**Forbidden reasons:**
| Never Say | Do Instead |
|-----------|------------|
| "Too complex" | Fix it |
| "Needs refactoring" | Do the refactor |
| "Might break something" | Fix it, user reviews via git diff |
| "Consider later" | Do it NOW |

**Valid failures (technical only):**
- File not found
- Parse error
- Permission denied

## Accounting [BLOCKER]

```
applied + failed = total
```

No "declined" category. Every finding = FIXED or FAILED (with technical reason).

## Output Standards

| Display | Meaning |
|---------|---------|
| OK | Score ≥ 80 |
| WARN | Score 60-79 |
| FAIL | Score < 60 |

Error format: `[SEVERITY] {what} in {file}:{line}`
