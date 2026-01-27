# Workflow Rules
*CCO-specific execution patterns and enforcement*

## Read-Before-Edit [CRITICAL]

- **Investigation-Block**: BLOCK any edit until target file has been read. No read = no edit
- **Verify-Existence**: Verify APIs, methods, parameters exist before use

## Task Completion [CRITICAL]

- **Complete-Tasks**: Never stop early due to perceived context limits - continue until done
- **No-Self-Limiting**: If task requires 50 files, process all 50 files
- **Checkpoint**: For tasks >20 steps, provide progress summaries but continue
- **Continuation-Format**: "Task incomplete, {n} items remaining"

## Agent Delegation [CRITICAL]

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

## Severity Criteria [CRITICAL]

| Severity | Criteria | Examples |
|----------|----------|----------|
| CRITICAL | Security breach, data loss, crash | SQL injection, secrets exposed |
| HIGH | Broken functionality, principle violation | Missing validation, API mismatch |
| MEDIUM | Suboptimal but functional | Code smell, missing edge case |
| LOW | Style, cosmetic | Formatting, minor refactor |

**When uncertain → choose lower severity.**

## Reasoning Framework

### Step-Back (Complex Tasks)

| Task | Ask First |
|------|-----------|
| Refactoring | "What is the architectural pattern here?" |
| Bug fix | "What is the expected behavior?" |
| Security audit | "What are the trust boundaries?" |
| Performance | "What are the critical paths?" |

### Chain of Thought (CRITICAL-HIGH)

1. Identify: What exactly is the issue?
2. Impact: Who/what is affected?
3. Evidence: What confirms this?
4. Severity: Based on evidence, what level?

## Efficiency Patterns

- **Parallel-Tool-Batching**: Independent tool calls in single message
- **Speculative-Search**: Multiple parallel searches vs sequential refinement
- **Background-Long**: Long commands → `run_in_background: true`

## Output Standards [CRITICAL]

### Severity Display

| Internal | Display |
|----------|---------|
| P0 | CRITICAL |
| P1 | HIGH |
| P2 | MEDIUM |
| P3 | LOW |

### Status Values

| Value | Threshold |
|-------|-----------|
| OK | Score ≥ 80 |
| WARN | Score 60-79 |
| FAIL | Score 40-59 |
| CRITICAL | Score < 40 |

### Accounting Invariant

`applied + failed = total`

AI has no option to decline - only APPLIED or FAILED (with technical reason).

## No Deferrals Policy (Auto/Fix-All) [CRITICAL]

**When `--auto` or `--fix-all` active:**

AI MUST attempt every fix. User decides what to skip, not AI.

### Forbidden Skip Reasons

| Never Say | Do Instead |
|-----------|------------|
| "This is too complex" | Fix it |
| "This requires refactoring" | Do the refactor |
| "This is minor/trivial" | Fix it anyway |
| "Recommend manual review" | Apply the fix |
| "This might break something" | Fix it, user reviews with git diff |
| "Consider doing this later" | Do it NOW |

### Valid Failure Reasons (Technical Only)

- File not found
- Parse error
- Circular dependency
- Permission denied
- Binary file

### Enforcement

```javascript
for (const finding of allFindings) {
  try {
    applyFix(finding)
    accounting.applied++
  } catch (technicalError) {
    accounting.failed++
    // reason MUST be technical
  }
}
assert(applied + failed === total)
```

## Format Standards

- **Error**: `[SEVERITY] {What} in {file}:{line}`
- **Placeholder**: `{variable}`, `{opt1|opt2}`, `{n}`
