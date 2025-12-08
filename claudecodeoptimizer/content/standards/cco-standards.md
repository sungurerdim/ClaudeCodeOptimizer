<!-- CCO_STANDARDS_START -->
# Universal Standards
*AI/human agnostic - fundamental principles for all software projects*

## Code Quality

| Standard | Rule |
|----------|------|
| * Fail-Fast | No silent fallbacks, immediate visible failure |
| * DRY | Single source of truth, no duplicates |
| * No-Orphans | Every function called, every import used |
| * Type-Safe | Annotations where supported, prefer immutable |
| * Complexity | Cyclomatic <10 per function |
| * Clean | Meaningful names, single responsibility, consistent style |
| * Explicit | No magic values, clear intent |
| * Scope | Only requested changes, general solutions |

## File & Resource

| Standard | Rule |
|----------|------|
| * Minimal-Touch | Only files required for task |
| * No-Unsolicited | Never create files unless requested |
| * Paths | Forward slash, relative, quote spaces |
| * Cleanup | Temp files, handles, connections |
| * Skip | .git, node_modules, __pycache__, venv, dist, build |

## Security

| Standard | Rule |
|----------|------|
| * Secrets | Env vars or vault only |
| * Input | Validate at system boundaries |
| * Access | Least privilege, secure defaults |
| * Deps | Review before adding, keep updated |
| * Defense | Multiple layers, don't trust single control |

## Testing

| Standard | Rule |
|----------|------|
| * Coverage | 60-90% context-adjusted |
| * Isolation | No inter-test deps, reproducible |
| * Integrity | Never edit tests to pass code |
| * Critical-Paths | E2E for critical workflows |

## Error Handling

| Standard | Rule |
|----------|------|
| * Catch | Log context, recover or propagate |
| * No-Silent | Never swallow exceptions |
| * User-Facing | Clarity + actionable |
| * Logs | Technical details only |
| * Rollback | Consistent state on failure |

## Documentation

| Standard | Rule |
|----------|------|
| * README | Description, setup, usage |
| * CHANGELOG | Versions with breaking changes |
| * Comments | Why not what |
| * Examples | Working, common use cases |

## Workflow

| Standard | Rule |
|----------|------|
| * Conventions | Match existing patterns |
| * Reference-Integrity | Find ALL refs, update, verify |
| * Decompose | Break complex tasks into steps |
| * Version | SemVer (MAJOR.MINOR.PATCH) |

## UX/DX

| Standard | Rule |
|----------|------|
| * Minimum-Friction | Fewest steps to goal |
| * Maximum-Clarity | Unambiguous output |
| * Predictable | Consistent behavior |

---

# AI-Specific Standards
*Portable across Claude/Codex/Gemini - AGENTS.md compatible*

## Context Optimization

| Standard | Rule |
|----------|------|
| * Semantic-Density | Concise over verbose |
| * Structured | Tables/lists over prose |
| * Front-load | Critical info first |
| * Hierarchy | H2 > H3 > bullets |
| * Scope | Bounded, reference over repeat |

## AI Behavior

### Execution Order [CRITICAL]

| Standard | Rule |
|----------|------|
| * Read-First | NEVER propose edits to unread files |
| * Plan-Before-Act | Understand full scope before any action |
| * Incremental | Complete one step fully before starting next |
| * Verify | Confirm changes match stated intent |

### Decision Making

| Standard | Rule |
|----------|------|
| * Challenge | Question solutions that seem too perfect |
| * Ask | When uncertain, clarify before proceeding |
| * Confidence | Explicitly state uncertainty level for non-obvious conclusions |

### Prohibited Patterns

| Pattern | Rule |
|---------|------|
| * No-Guessing | Never guess file contents without reading |
| * No-Premature | Never start implementation before understanding scope |
| * No-Skip | Never skip verification steps |
| * No-Assume | Never assume user intent without confirmation |

## Quality Control

| Standard | Rule |
|----------|------|
| * Understand-First | No vibe coding |
| * Adapt | Examples to context, don't copy blind |
| * No-Hallucination | Only existing APIs/features |
| * Positive | What to do, not what to avoid |
| * Motivate | Explain why behaviors matter |

## Status Updates

| Standard | Rule |
|----------|------|
| * Announce | Before action, not after |
| * Progress | Starting > In progress > Completed |
| * Transitions | Clear phase signals |
| * No-Silent | User always knows state |

## Multi-Model

| Standard | Rule |
|----------|------|
| * Agnostic | No model-specific syntax |
| * Graceful | Account for different capabilities |
| * Portable | Patterns work across models |

## Output Standards

| Standard | Rule |
|----------|------|
| * Error | `[SEVERITY] {What} in {file:line}` |
| * Status | OK / WARN / FAIL |
| * Accounting | done + skip + fail = total |
| * Structured | JSON/table when needed |

---

# CCO-Specific Standards
*CCO workflow mechanisms - excluded from AGENTS.md export*

## Command Flow

| Standard | Rule |
|----------|------|
| * Context-Check | Verify CCO_CONTEXT, suggest /cco-tune if missing |
| * Read-Context | Parse ./CLAUDE.md markers |
| * Execute | Command-specific logic |
| * Report | Results with accounting |

## Safety

| Standard | Rule |
|----------|------|
| * Pre-op | Git status before modifications |
| * Dirty | Prompt Commit / Stash / Continue |
| * Rollback | Clean state enables git checkout |

### Classification

**Safe (auto-apply):**

| Standard | Rule |
|----------|------|
| * Remove-Imports | Remove unused imports |
| * Parameterize-SQL | Parameterize SQL queries |
| * Move-Secrets | Move secrets to env |
| * Fix-Lint | Fix linting issues |
| * Add-Types | Add type annotations |

**Risky (require approval):**

| Standard | Rule |
|----------|------|
| * Auth-Changes | Auth/CSRF changes |
| * DB-Schema | DB schema changes |
| * API-Contract | API contract changes |
| * Delete-Files | Delete files |
| * Rename-Public | Rename public APIs |

## Fix Workflow

| Standard | Rule |
|----------|------|
| * Flow | Analyze > Report > Approve > Apply > Verify |
| * Output | `Applied: N \| Skipped: N \| Failed: N \| Total: N` |

## Impact Preview

| Standard | Rule |
|----------|------|
| * Direct | Files to modify |
| * Dependents | Files that import/use |
| * Tests | Coverage of affected code |
| * Risk | LOW / MEDIUM / HIGH |
| * Skip | LOW risk, <=2 files, full coverage |

## Priority

| Standard | Rule |
|----------|------|
| * CRITICAL | Security, data exposure |
| * HIGH | High-impact, low-effort |
| * MEDIUM | Balanced impact/effort |
| * LOW | Style, minor optimization |

## Approval Flow

### Tool Configuration [STRICT]

| Standard | Rule |
|----------|------|
| * Tool | AskUserQuestion |
| * MultiSelect | true (always) |

### Ordering [REQUIRED]

| Standard | Rule |
|----------|------|
| * Priority-Order | CRITICAL → HIGH → MEDIUM → LOW |

### Format [EXACT]

| Standard | Rule |
|----------|------|
| * Item-Format | `{description} [{file:line}] [{safe\|risky}]` |

### Batch Options [REQUIRED]

| Standard | Rule |
|----------|------|
| * All-Option | First option MUST be: "All ({N})" where N = total items |
| * Individual | Remaining options: individual items |

### Pagination [LIMITS]

| Standard | Rule |
|----------|------|
| * Max-Questions | Max 4 questions per AskUserQuestion call |
| * Max-Options | Max 4 options per question |
| * Overflow | If more items: use multiple sequential calls |

## Question Formatting

### Separation Rules [CRITICAL]

| Standard | Rule |
|----------|------|
| * Separate-Categories | Present different categories in SEPARATE batches |

| Category Type | Examples | Batch |
|---------------|----------|-------|
| Settings | strictMode, timeout, format | Batch 1 |
| Permissions | readOnly, allowDelete | Batch 2 |
| Thresholds | coverage%, complexity | Batch 3 |

### Labels [MANDATORY]

| Standard | Rule |
|----------|------|
| * One-Label | Each option receives exactly ONE label |
| * Current | `[current]` - Matches existing config (priority 1) |
| * Detected | `[detected]` - Auto-detected, not in config (priority 2) |
| * Recommended | `[recommended]` - Best practice, max 1/question (priority 3) |
| * Precedence | If detected AND current both apply → show `[current]` only |

### Ordering [REQUIRED]

| Standard | Rule |
|----------|------|
| * Numeric | Ascending (60 → 70 → 80 → 90) |
| * Severity | Safest → riskiest |
| * Scope | Narrowest → widest |

### Verification [PRE-OUTPUT]

| Standard | Rule |
|----------|------|
| * Check-Categories | Categories separated into distinct batches |
| * Check-Labels | Each option has exactly ONE label |
| * Check-Recommended | Maximum ONE `[recommended]` per question |
| * Check-Order | Options ordered per rules above |

### Examples

<example type="correct">
**Batch 1 - Settings:**
Q: "Select output format"
- JSON [current]
- YAML
- XML [recommended]

**Batch 2 - Permissions:**
Q: "Select access level"
- Read-only [detected]
- Full access
</example>

<example type="incorrect" reason="Mixed categories">
Q: "Configure options"
- JSON output [current]
- Full access [detected]
- Strict mode
</example>

<example type="incorrect" reason="Multiple labels">
- JSON [current] [recommended]
</example>

<example type="incorrect" reason="Missing label on detected item">
- JSON (detected but no label shown)
</example>

## Output Formatting

### Table Characters [STRICT]

| Standard | Rule |
|----------|------|
| * Borders | `─│┌┐└┘├┤┬┴┼` |
| * Headers | `═║╔╗╚╝` |

### Alignment [REQUIRED]

| Standard | Rule |
|----------|------|
| * Numbers | Right-aligned |
| * Text | Left-aligned |
| * Status | Centered |

### Status Indicators [EXACT]

| Standard | Rule |
|----------|------|
| * Values | OK \| WARN \| FAIL \| PASS \| SKIP |

### Progress Bars [FORMULA]

| Standard | Rule |
|----------|------|
| * Formula | `filled = round(percentage / 100 * 8)` → `████░░░░` |

### Prohibited

| Standard | Rule |
|----------|------|
| * No-Emojis | No emojis in tables |
| * No-Unicode | No unicode decorations beyond specified |
| * No-ASCII-Art | No ASCII art headers |

## Dynamic Context

### Injection Syntax [REQUIRED]

| Standard | Rule |
|----------|------|
| * Syntax | Use `!` backtick for real-time context |
| * Git-Status | `!`git status --short`` |
| * Branch | `!`git branch --show-current`` |
| * CCO-Context | `!`head -30 ./CLAUDE.md 2>/dev/null`` |

### When to Use

| Context Type | Command | Example |
|--------------|---------|---------|
| Git state | commit, refactor | `!`git status`` |
| File content | audit, review | `!`head -50 ./CLAUDE.md`` |
| Dependencies | audit, health | `!`cat package.json \| jq .dependencies`` |
| Recent changes | commit, review | `!`git log --oneline -5`` |

### Benefits

| Standard | Rule |
|----------|------|
| * Accuracy | Real-time accuracy over stale assumptions |
| * Anti-Hallucination | Reduces hallucination risk |
| * Efficiency | Eliminates redundant file reads |

## Tool Restrictions

### Frontmatter Format [STRICT]

| Standard | Rule |
|----------|------|
| * Name | `name: command-name` |
| * Description | `description: Brief description` |
| * Tools | `allowed-tools: Tool1(*), Tool2(pattern:*)` |

### Pattern Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `Tool(*)` | All uses of tool | `Read(*)` |
| `Tool(path/*)` | Path prefix | `Edit(src/*)` |
| `Bash(cmd:*)` | Specific command | `Bash(git:*)` |
| `Bash(cmd1:*, cmd2:*)` | Multiple commands | `Bash(git:*, npm:*)` |

### Security Benefit

| Standard | Rule |
|----------|------|
| * Scope | Commands can only use declared tools |
| * Prevention | Prevents accidental destructive operations |
| * Explicit | Explicit scope = predictable behavior |

## Parallel Execution

### When to Parallelize [REQUIRED]

| Scenario | Action |
|----------|--------|
| Independent scans | Launch parallel agents |
| Multiple file reads | Batch in single call |
| Unrelated checks | Run simultaneously |
| Dependent operations | Run sequentially |

### Agent Parallelization Pattern

| Standard | Rule |
|----------|------|
| * Launch | Launch agents simultaneously |
| * Scope | Each agent handles distinct scope |
| * Merge | Merge results after all complete |

### Benefits

| Standard | Rule |
|----------|------|
| * Speed | Faster execution (N agents = ~1/N time) |
| * Coverage | Better coverage (diverse search strategies) |
| * Context | Reduced context switching |

## Quick Mode

### Single-Message Enforcement [STRICT]

| Standard | Rule |
|----------|------|
| * No-Questions | Do not ask questions |
| * Defaults | Use smart defaults for all options |
| * No-Intermediate | Do not output intermediate text |
| * Summary | Only tool calls, then final summary |

### Applicable Commands

| Command | Quick Behavior |
|---------|----------------|
| commit | Stage all, single commit, push |
| generate | Use detected conventions |
| audit | Smart scope, auto-fix safe |
| optimize | Balanced mode, all categories |

### Output Restriction

| Standard | Rule |
|----------|------|
| * Single-Message | Complete ALL steps in a single message |
| * No-Extra-Tools | Do not use any other tools |
| * No-Extra-Text | Do not send any other text besides tool calls and final summary |

## Conservative Judgment

### Severity Assignment [CRITICAL]

| Keyword | Severity | Confidence Required |
|---------|----------|---------------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

### False Positive Prevention

| Standard | Rule |
|----------|------|
| * Trust | False positives erode user trust faster than missed issues |
| * Lower | When uncertain between two severities, choose lower |
| * Genuine | Only flag issues that genuinely block users |
| * Evidence | Require explicit evidence, not inference |

### Prohibited Escalations

| Standard | Rule |
|----------|------|
| * Style | Style issues → never CRITICAL or HIGH |
| * Unverified | Unverified claims → never above MEDIUM |
| * Single | Single occurrence → never CRITICAL unless security |

## Skip Criteria

### Always Skip [STRICT]

| Category | Paths/Patterns |
|----------|----------------|
| Version Control | `.git/`, `.svn/`, `.hg/` |
| Dependencies | `node_modules/`, `vendor/`, `.venv/`, `venv/` |
| Build Output | `dist/`, `build/`, `out/`, `target/`, `.next/` |
| Cache | `__pycache__/`, `.cache/`, `.tmp/` |
| IDE | `.idea/`, `.vscode/`, `.vs/` |
| Test Fixtures | `fixtures/`, `testdata/`, `__snapshots__/` |
| Examples | `examples/`, `samples/`, `demo/`, `benchmarks/` |

### Inline Skip Markers

| Standard | Rule |
|----------|------|
| * Line | `// cco-ignore` or `# cco-ignore` - skip this line |
| * File | `// cco-ignore-file` or `# cco-ignore-file` - skip entire file |
| * Markdown | `<!-- cco-ignore -->` - skip in markdown |

### Generated File Detection

| Standard | Rule |
|----------|------|
| * Minified | `*.min.js`, `*.min.css` |
| * Generated | `*.generated.*`, `*.auto.*` |
| * Header | Files with `// @generated` or `# Generated by` header |

## Task Tracking

### Pre-Execution Requirement [REQUIRED]

| Standard | Rule |
|----------|------|
| * Create | Create TODO list with ALL items |
| * Status | Mark each as: pending → in_progress → completed |
| * No-Skip | Never skip items - update status instead |
| * Single | Exactly ONE item in_progress at a time |

### Accounting Verification

| Standard | Rule |
|----------|------|
| * Total | Final output MUST satisfy: `done + skip + fail = total` |

### Progress Visibility

| Phase | Action |
|-------|--------|
| Start | List all items with pending status |
| Process | Update to in_progress before working |
| Complete | Mark completed immediately after |
| Report | Show final accounting |

## Integration

| Standard | Rule |
|----------|------|
| * Context | Read CCO_CONTEXT_START markers |
| * Apply | Guidelines, Thresholds, Applicable |
| * Tools | Parallel independent, sequential dependent |
| * Thinking | 5K standard, 8K medium, 10K complex |
<!-- CCO_STANDARDS_END -->
