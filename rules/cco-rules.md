---
cco_version: 2.0.0 # x-release-please-version
last_update_check: 1970-01-01T00:00:00Z
---

# CCO Rules

## Focus and Discipline

### Decision Commitment

Pick one approach and follow through. When multiple solutions seem viable, choose the simplest one that meets the requirements. Only reassess if it fails.

### Exploration Restraint

Read only what you need before acting:

| Task | Files to Read |
|------|---------------|
| Small fix (1-2 files) | 1-3 files |
| Feature (3-5 files) | 5-10 files |
| Architecture scan | Structure first, then deepen |

### Change Scope

Every changed line should trace directly to the user's request. Unrelated issues: mention, don't fix.

### File Discipline

Create new files only when the user explicitly requests them. Skip: `.git`, `node_modules`, `vendor`, `venv`, `dist`, `build`, `__pycache__`

## Code Quality

### Complexity Limits

Refactor before proceeding when code exceeds these limits:

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

### Code Volume

Avoid single-use abstractions, impossible error handling, and unnecessary bulk. If 100+ lines could be 50, prefer the shorter version.

### Anti-Overengineering Guard

Before flagging any finding, all three must be YES:
1. Does this actually break something or pose a risk?
2. Does this cause real problems for developers/users?
3. Is fixing it worth the effort and side effects?

All NO = not a finding.

## Security

### Security Patterns

Address these patterns before continuing:

| Pattern | Fix |
|---------|-----|
| Secrets in source | Move to env vars |
| Bare except/catch | Catch specific types |
| Empty catch blocks | Add handling |
| Unsanitized external data | Add validation |
| eval/pickle/yaml.load | Use safe alternatives |

## Workflow

### Uncertainty

When uncertain, surface it. State confidence level ("~90% sure", "uncertain about X") and ask before proceeding on ambiguous tasks.

### Error Recovery

On tool error: diagnose why, then use a different approach on the second attempt.

### Severity Levels

| Level | Criteria |
|-------|----------|
| CRITICAL | Security, data loss, crash |
| HIGH | Broken functionality |
| MEDIUM | Suboptimal but works |
| LOW | Style only |

When uncertain, choose lower severity.

### Scope Creep Detection

If finding count exceeds 2x initial estimate, stop and ask the user before continuing.

## CCO Operations

### Version Awareness

If `last_update_check` is >24 hours old, run `/cco-update --check` at the start of any CCO command (skip silently in --auto mode).

### Agent Delegation

| Need | Tool |
|------|------|
| Single fact | WebSearch/WebFetch |
| 3+ sources | cco-agent-research |
| Find file/pattern | Glob/Grep/Read |
| Structured audit | cco-agent-analyze |
| 1-2 file edits | Edit/Write |
| 3+ file edits | cco-agent-apply |

### Efficiency

- Independent tool calls: parallel in single message
- Long Bash: `run_in_background: true`, collect via TaskOutput before output
- Multiple agents: parallel Task calls in single message

### No Deferrals (Auto Mode)

When `--auto` active:

| Never Say | Do Instead |
|-----------|------------|
| "Too complex" | Fix it |
| "Might break" | Fix it, user reviews |
| "Consider later" | Do it now |

### Accounting

`applied + failed + needs_approval = total`

No declined category. Fix, flag for approval (architectural), or fail with technical reason.

### Skip Patterns

Never flag intentionally marked code: `# noqa`, `# intentional`, `# safe:`, `_` prefix, `TYPE_CHECKING` blocks, platform guards, test fixtures.

### Execution Flow

All analysis commands: Setup → Analyze → Gate → [Plan] → Apply → Summary. Skip questions in --auto. Display plan before asking user. Single-line summary in --auto.

### Plan Review

When findings > 0 and not --auto:
1. Display full plan table with rationale before asking
2. Action: Fix All / By Severity / Review Each / Report Only
3. Severity filter (multiselect): CRITICAL / HIGH / MEDIUM / LOW

### Needs-Approval Flow

After apply, if needs_approval > 0 and not --auto:
1. Display items table (ID, severity, issue, location, reason)
2. Ask: Fix All / Skip / Review Each

### Confidence Scoring

| Score | Action |
|-------|--------|
| ≥90 | Auto-fix |
| 80-89 | Auto-fix, visible in diff |
| 70-79 | Recommend in plan |
| 60-69 | Ask approval |
| <60 | Report only |

Threshold: ≥80 for "Apply Safe Only". CRITICAL bypasses confidence.
