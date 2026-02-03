# CCO Rules

Core rules injected via SessionStart hook. Every session, automatically.

---

## How It Works

```
Session Start
     │
     ▼
SessionStart hook fires
     │
     ▼
hooks/core-rules.json read
     │
     ▼
Rules injected into context via additionalContext
     │
     ▼
Rules active for entire session
```

**Source:** `hooks/core-rules.json` — single source of truth for all CCO rules.

---

## Foundation Rules [BLOCKER]

Enforceable constraints with measurable thresholds.

### Uncertainty Protocol

When uncertain, STOP and surface it.

- **Stop-When-Unclear**: Ambiguous task → ask before proceeding
- **Signal-Confidence**: State confidence: "~90% sure", "uncertain about X"

### Complexity Limits

Code exceeding limits = STOP and refactor first.

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

### File Creation

**BLOCK**: Creating new files without explicit user request.

### Change Scope

**Test**: Can every changed line trace directly to user's request?

- NO → Revert that change
- Unrelated issues → mention, don't fix

### Code Volume

- [ ] No single-use abstractions
- [ ] No impossible error handling
- [ ] 100+ lines → could it be 50? Rewrite if yes

### Anti-Overengineering Guard

Before flagging ANY finding, all three must be YES:
1. Does this actually break something or pose a risk?
2. Does this cause real problems for developers/users?
3. Is fixing it worth the effort and side effects?

**All NO → not a finding.**

### Validation Boundaries

| Input Type | Required |
|------------|----------|
| Numbers | min/max bounds |
| Strings | max length |
| Arrays | max items |
| External calls | timeout |
| Resources | cleanup in finally |

### Refactoring Safety

Before modifying shared code:
- [ ] **Delete**: Found ALL callers
- [ ] **Rename**: Will update ALL references
- [ ] **Move**: Will update ALL imports
- [ ] **Signature**: Will update ALL call sites

### Modern Patterns

Prefer modern, idiomatic syntax:
- Union types over Optional (`str | None` not `Optional[str]`)
- Pattern matching over if/elif chains where clearer
- Comprehensions over manual loops for transforms
- Explicit over implicit (named params, type hints on public APIs)
- Standard library over dependencies for simple tasks

### Context Awareness

At project start, quickly assess:

| Signal | Look For | Impact |
|--------|----------|--------|
| Data sensitivity | PII patterns, health/financial terms, encryption | Extra caution on logging, errors, exports |
| Priority | "security-first" in docs, performance benchmarks | Check ordering |
| Team size | CODEOWNERS, contributor count | Review expectations |

If sensitive data detected → never log raw values, mask in errors, audit data flows.

---

## Safety Rules [BLOCKER]

Finding ANY = STOP. Fix before continuing.

| Pattern | Fix |
|---------|-----|
| Secrets in source | Move to env vars |
| Bare except/catch | Catch specific types |
| Empty catch blocks | Add handling |
| Unsanitized external data | Add validation |
| eval/pickle/yaml.load | Use safe alternatives |

**Safe vs Unsafe:**

| Safe | Unsafe |
|------|--------|
| `json.loads()` | `pickle.load()`, `eval()` |
| bcrypt, argon2 | MD5, SHA1, plaintext |
| TLS 1.2+ | HTTP, TLS 1.0/1.1 |

---

## Workflow Rules [BLOCKER]

### Read-Before-Edit

**BLOCK**: Any edit to file not yet read.

Verify functions/APIs exist before calling.

### Task Completion

**BLOCK**: Stopping early due to perceived limits.

Checkpoints: Every 20 steps progress, every 5 steps goal check.

### Incremental Verification

After every edit: verify the change has expected effect. Do not proceed until verified.

### Context Staleness

File not read in 20+ steps → re-read before editing.

### Error Recovery

Tool error → diagnose first (why?), then change strategy. Never repeat the same failing command twice.

### Partial Output Guard

If output contains missing sections, placeholders, or TODOs → NOT complete. Finish before reporting done.

### Severity Levels

| Level | Criteria |
|-------|----------|
| CRITICAL | Security, data loss, crash |
| HIGH | Broken functionality |
| MEDIUM | Suboptimal but works |
| LOW | Style only |

**When uncertain → lower severity.**

### Scope Creep Detection

If finding count exceeds 2x initial estimate → stop, inform user, narrow scope.

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

- Independent tool calls → parallel in single message
- Long Bash → `run_in_background: true`, collect via TaskOutput before output
- Multiple agents → parallel Task calls in single message

### No Deferrals [Auto Mode]

When `--auto` active:

| Never Say | Do Instead |
|-----------|------------|
| "Too complex" | Fix it |
| "Might break" | Fix it, user reviews |
| "Consider later" | Do it NOW |

### Accounting

`applied + failed + needs_approval = total`

No declined category. Fix, flag for approval (architectural), or fail with technical reason.

### Skip Patterns

Never flag: `# noqa`, `# intentional`, `# safe:`, `_` prefix, `TYPE_CHECKING` blocks, platform guards, test fixtures.

---

## Tool Rules

### Execution Flow

All analysis commands: Setup → Analyze → Gate → [Plan] → Apply → Summary.

Skip questions in --auto. Display plan BEFORE asking user. Single-line summary in --auto.

### Plan Review [MANDATORY]

When findings > 0 and not --auto:
1. Display full plan table with rationale BEFORE asking
2. Action: Fix All / By Severity / Review Each / Report Only
3. Severity filter (multiselect): CRITICAL / HIGH / MEDIUM / LOW

### Confidence Scoring

| Score | Action |
|-------|--------|
| ≥90 | Auto-fix |
| 80-89 | Auto-fix, visible in diff |
| 70-79 | Recommend in plan |
| 60-69 | Ask approval |
| <60 | Report only |

Threshold: ≥80 for "Apply Safe Only". CRITICAL bypasses confidence.

---

*Back to [README](../README.md)*
