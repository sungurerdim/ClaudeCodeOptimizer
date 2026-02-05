---
cco_version: 2.0.0
last_update_check: 1970-01-01T00:00:00Z
---

# Foundation Rules
*Enforceable constraints with measurable thresholds*

## Uncertainty Protocol [BLOCKER]

When uncertain, STOP and surface it. Don't guess silently.

- **Stop-When-Unclear**: If task is ambiguous → ask before proceeding
- **Signal-Confidence**: State confidence level: "~90% sure", "uncertain about X"

## Complexity Limits [BLOCKER]

Code exceeding limits = STOP and refactor first.

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

## File Creation [BLOCKER]

**BLOCK**: Creating new files without explicit user request.

Skip: `.git`, `node_modules`, `vendor`, `venv`, `dist`, `build`, `__pycache__`

## Change Scope [BLOCKER]

**Test**: Can every changed line trace directly to user's request?

- NO → Revert that change
- Unrelated issues → mention, don't fix

## Code Volume [CHECK]

- [ ] No single-use abstractions
- [ ] No impossible error handling
- [ ] 100+ lines → could it be 50? Rewrite if yes

## Anti-Overengineering Guard [BLOCKER]

Before flagging ANY finding, all three must be YES:
1. Does this actually break something or pose a risk?
2. Does this cause real problems for developers/users?
3. Is fixing it worth the effort and side effects?

**All NO → not a finding.**

## Validation Boundaries [CHECK]

Public APIs: validate numbers (min/max), strings (max length), arrays (max items), external calls (timeout), resources (cleanup in finally).

## Refactoring Safety [CHECK]

Before modifying shared code:
- [ ] **Delete**: Found ALL callers
- [ ] **Rename**: Will update ALL references
- [ ] **Move**: Will update ALL imports
- [ ] **Signature**: Will update ALL call sites

## Modern Patterns [CHECK]

Prefer modern, idiomatic syntax for each language:
- Union types over Optional (`str | None` not `Optional[str]`)
- Pattern matching over if/elif chains where clearer
- Comprehensions over manual loops for transforms
- Explicit over implicit (named params, type hints on public APIs)
- Standard library over dependencies for simple tasks

## Context Awareness [CHECK]

At project start, quickly assess:

| Signal | Look For | Impact |
|--------|----------|--------|
| Data sensitivity | PII patterns, health/financial terms, encryption usage | Extra caution on logging, errors, exports |
| Priority | "security-first" in docs, performance benchmarks, rapid deployment | Check ordering |
| Team size | CODEOWNERS, contributor count | Review expectations |

If sensitive data detected → never log raw values, mask in errors, audit data flows.

# Safety Rules
*BLOCKER violations*

## Security Violations [BLOCKER]

Finding ANY = STOP. Fix before continuing.

| Pattern | Fix |
|---------|-----|
| Secrets in source | Move to env vars |
| Bare except/catch | Catch specific types |
| Empty catch blocks | Add handling |
| Unsanitized external data | Add validation |
| eval/pickle/yaml.load | Use safe alternatives |

# Workflow Rules
*Execution patterns*

## Read-Before-Edit [BLOCKER]

**BLOCK**: Any edit to file not yet read.

Verify functions/APIs exist before calling.

## Task Completion [BLOCKER]

**BLOCK**: Stopping early due to perceived limits.

Checkpoints: Every 20 steps progress, every 5 steps goal check.

## Incremental Verification [BLOCKER]

After every edit: verify the change has expected effect (lint/test/manual). Do not proceed to next edit until verified.

## Context Staleness [BLOCKER]

File not read in 20+ steps → re-read before editing. Don't rely on stale context.

## Error Recovery [BLOCKER]

Tool error → diagnose first (why?), then change strategy. Never repeat the same failing command twice.

## Partial Output Guard [BLOCKER]

If output contains missing sections, placeholders, or TODOs → it is NOT complete. Finish before reporting done.

## Severity Levels [CHECK]

| Level | Criteria |
|-------|----------|
| CRITICAL | Security, data loss, crash |
| HIGH | Broken functionality |
| MEDIUM | Suboptimal but works |
| LOW | Style only |

**When uncertain → lower severity.**

## Scope Creep Detection [CHECK]

If finding count exceeds 2x initial estimate → stop, inform user, narrow scope.

## Agent Delegation [CHECK]

| Need | Tool |
|------|------|
| Single fact | WebSearch/WebFetch |
| 3+ sources | cco-agent-research |
| Find file/pattern | Glob/Grep/Read |
| Structured audit | cco-agent-analyze |
| 1-2 file edits | Edit/Write |
| 3+ file edits | cco-agent-apply |

## Efficiency

- Independent tool calls → parallel in single message
- Long Bash → `run_in_background: true`, collect via TaskOutput before output
- Multiple agents → parallel Task calls in single message

## No Deferrals [BLOCKER - Auto Mode]

When `--auto` active:

| Never Say | Do Instead |
|-----------|------------|
| "Too complex" | Fix it |
| "Might break" | Fix it, user reviews |
| "Consider later" | Do it NOW |

## Accounting [BLOCKER]

`applied + failed + needs_approval = total`

No declined category. Fix, flag for approval (architectural), or fail with technical reason.

## Skip Patterns [STANDARD]

Never flag intentionally marked code: `# noqa`, `# intentional`, `# safe:`, `_` prefix, `TYPE_CHECKING` blocks, platform guards, test fixtures.

# Tool Rules
*Reusable execution patterns for CCO commands*

## Execution Flow [STANDARD]

All analysis commands: Setup → Analyze → Gate → [Plan] → Apply → Summary.
Skip questions in --auto. Display plan BEFORE asking user. Single-line summary in --auto.

## Plan Review [MANDATORY]

When findings > 0 and not --auto:
1. Display full plan table with rationale BEFORE asking
2. Action: Fix All / By Severity / Review Each / Report Only
3. Severity filter (multiselect): CRITICAL / HIGH / MEDIUM / LOW

## Needs-Approval Flow [STANDARD]

After apply, if needs_approval > 0 and not --auto:
1. Display items table (ID, severity, issue, location, reason)
2. Ask: Fix All / Skip / Review Each

## Confidence Scoring [STANDARD]

| Score | Action |
|-------|--------|
| ≥90 | Auto-fix |
| 80-89 | Auto-fix, visible in diff |
| 70-79 | Recommend in plan |
| 60-69 | Ask approval |
| <60 | Report only |

Threshold: ≥80 for "Apply Safe Only". CRITICAL bypasses confidence.
