# Tools Rules
*On-demand loading for CCO commands and agents*

## User Input [CRITICAL]

### Tool Requirement [STRICT]

| Rule | Description |
|------|-------------|
| * Tool | ALL user inputs MUST use AskUserQuestion tool |
| * No-Exceptions | Never use plain text prompts for user decisions |
| * MultiSelect | Use multiSelect: true when multiple selections valid |

### Applies To

| Scenario | Example | MultiSelect |
|----------|---------|-------------|
| Confirmations | "Apply this configuration?" | false |
| Scope selection | "What to audit?" | true |
| Option selection | "Which files to include?" | true |
| Yes/No decisions | "Add BREAKING CHANGE footer?" | false |
| Action selection | "Accept / Modify / Cancel" | false |

### Reference Pattern

Commands MUST explicitly state tool usage:
```markdown
**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| {question}? | {opt1}, {opt2}, ... | true/false |
```

## Command Flow

| Rule | Description |
|------|-------------|
| * Context-Check | Verify CCO_ADAPTIVE, suggest /cco-tune if missing |
| * Read-Context | Parse ./CLAUDE.md markers |
| * Execute | Command-specific logic |
| * Report | Results with accounting |

## Safety

| Rule | Description |
|------|-------------|
| * Pre-op | Git status before modifications |
| * Dirty | Prompt Commit / Stash / Continue |
| * Rollback | Clean state enables git checkout |

### Classification

**Safe (auto-apply):**

| Rule | Description |
|------|-------------|
| * Remove-Imports | Remove unused imports |
| * Parameterize-SQL | Parameterize SQL queries |
| * Move-Secrets | Move secrets to env |
| * Fix-Lint | Fix linting issues |
| * Add-Types | Add type annotations |

**Risky (require approval):**

| Rule | Description |
|------|-------------|
| * Auth-Changes | Auth/CSRF changes |
| * DB-Schema | DB schema changes |
| * API-Contract | API contract changes |
| * Delete-Files | Delete files |
| * Rename-Public | Rename public APIs |

## Fix Workflow

| Rule | Description |
|------|-------------|
| * Flow | Analyze > Report > Approve > Apply > Verify |
| * Output | `Applied: N \| Skipped: N \| Failed: N \| Total: N` |

## Impact Preview

| Rule | Description |
|------|-------------|
| * Direct | Files to modify |
| * Dependents | Files that import/use |
| * Tests | Coverage of affected code |
| * Risk | LOW / MEDIUM / HIGH |
| * Skip | LOW risk, <=2 files, full coverage |

## Priority

| Rule | Description |
|------|-------------|
| * CRITICAL | Security, data exposure |
| * HIGH | High-impact, low-effort |
| * MEDIUM | Balanced impact/effort |
| * LOW | Style, minor optimization |

## Approval Flow

*Inherits User Input [CRITICAL] - all approvals use AskUserQuestion.*

### Configuration [STRICT]

| Rule | Description |
|------|-------------|
| * MultiSelect | true (for batch approvals) |

### Ordering [REQUIRED]

| Rule | Description |
|------|-------------|
| * Priority-Order | CRITICAL -> HIGH -> MEDIUM -> LOW |

### Format [EXACT]

| Rule | Description |
|------|-------------|
| * Item-Format | `{description} [{file:line}] [{safe\|risky}]` |

### Batch Options [REQUIRED]

| Rule | Description |
|------|-------------|
| * All-Option | First option MUST be: "All ({N})" where N = total items |
| * Individual | Remaining options: individual items |

### Pagination [LIMITS]

| Rule | Description |
|------|-------------|
| * Max-Questions | Max 4 questions per AskUserQuestion call |
| * Max-Options | Max 4 options per question |
| * Overflow | If more items: use multiple sequential calls |

## Question Formatting

### Separation Rules [CRITICAL]

| Rule | Description |
|------|-------------|
| * Separate-Categories | Present different categories in SEPARATE batches |

| Category Type | Examples | Batch |
|---------------|----------|-------|
| Settings | strictMode, timeout, format | Batch 1 |
| Permissions | readOnly, allowDelete | Batch 2 |
| Thresholds | coverage%, complexity | Batch 3 |

### Labels [MANDATORY]

| Rule | Description |
|------|-------------|
| * One-Label | Each option receives exactly ONE label |
| * Current | `[current]` - Matches existing config (priority 1) |
| * Detected | `[detected]` - Auto-detected, not in config (priority 2) |
| * Recommended | `[recommended]` - Best practice, max 1/question (priority 3) |
| * Precedence | If detected AND current both apply -> show `[current]` only |

### Ordering [REQUIRED]

| Rule | Description |
|------|-------------|
| * Numeric | Ascending (60 -> 70 -> 80 -> 90) |
| * Severity | Safest -> riskiest |
| * Scope | Narrowest -> widest |

### Verification [PRE-OUTPUT]

| Rule | Description |
|------|-------------|
| * Check-Categories | Categories separated into distinct batches |
| * Check-Labels | Each option has exactly ONE label |
| * Check-Recommended | Maximum ONE `[recommended]` per question |
| * Check-Order | Options ordered per rules above |

## Output Formatting

### Table Characters [STRICT]

| Rule | Description |
|------|-------------|
| * Borders | `─│┌┐└┘├┤┬┴┼` |
| * Headers | `═║╔╗╚╝` |

### Alignment [REQUIRED]

| Rule | Description |
|------|-------------|
| * Numbers | Right-aligned |
| * Text | Left-aligned |
| * Status | Centered |

### Status Indicators [EXACT]

| Rule | Description |
|------|-------------|
| * Values | OK \| WARN \| FAIL \| PASS \| SKIP |

### Progress Bars [FORMULA]

| Rule | Description |
|------|-------------|
| * Formula | `filled = round(percentage / 100 * 8)` -> `████░░░░` |

### Prohibited

| Rule | Description |
|------|-------------|
| * No-Emojis | No emojis in tables |
| * No-Unicode | No unicode decorations beyond specified |
| * No-ASCII-Art | No ASCII art headers |

## Dynamic Context

### Injection Syntax [REQUIRED]

| Rule | Description |
|------|-------------|
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

| Rule | Description |
|------|-------------|
| * Accuracy | Real-time accuracy over stale assumptions |
| * Anti-Hallucination | Reduces hallucination risk |
| * Efficiency | Eliminates redundant file reads |

## Tool Restrictions

### Frontmatter Format [STRICT]

| Rule | Description |
|------|-------------|
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

| Rule | Description |
|------|-------------|
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

| Rule | Description |
|------|-------------|
| * Launch | Launch agents simultaneously |
| * Scope | Each agent handles distinct scope |
| * Merge | Merge results after all complete |

### Benefits

| Rule | Description |
|------|-------------|
| * Speed | Faster execution (N agents = ~1/N time) |
| * Coverage | Better coverage (diverse search strategies) |
| * Context | Reduced context switching |

## Quick Mode

### Single-Message Enforcement [STRICT]

| Rule | Description |
|------|-------------|
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

| Rule | Description |
|------|-------------|
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

| Rule | Description |
|------|-------------|
| * Trust | False positives erode user trust faster than missed issues |
| * Lower | When uncertain between two severities, choose lower |
| * Genuine | Only flag issues that genuinely block users |
| * Evidence | Require explicit evidence, not inference |

### Prohibited Escalations

| Rule | Description |
|------|-------------|
| * Style | Style issues -> never CRITICAL or HIGH |
| * Unverified | Unverified claims -> never above MEDIUM |
| * Single | Single occurrence -> never CRITICAL unless security |

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

| Rule | Description |
|------|-------------|
| * Line | `// cco-ignore` or `# cco-ignore` - skip this line |
| * File | `// cco-ignore-file` or `# cco-ignore-file` - skip entire file |
| * Markdown | `<!-- cco-ignore -->` - skip in markdown |

### Generated File Detection

| Rule | Description |
|------|-------------|
| * Minified | `*.min.js`, `*.min.css` |
| * Generated | `*.generated.*`, `*.auto.*` |
| * Header | Files with `// @generated` or `# Generated by` header |

## Task Tracking

### Pre-Execution Requirement [REQUIRED]

| Rule | Description |
|------|-------------|
| * Create | Create TODO list with ALL items |
| * Status | Mark each as: pending -> in_progress -> completed |
| * No-Skip | Never skip items - update status instead |
| * Single | Exactly ONE item in_progress at a time |

### Accounting Verification

| Rule | Description |
|------|-------------|
| * Total | Final output MUST satisfy: `done + skip + fail = total` |

### Progress Visibility

| Phase | Action |
|-------|--------|
| Start | List all items with pending status |
| Process | Update to in_progress before working |
| Complete | Mark completed immediately after |
| Report | Show final accounting |

## Integration

| Rule | Description |
|------|-------------|
| * Context | Read CCO_ADAPTIVE_START markers |
| * Apply | Guidelines, Thresholds, Applicable |
| * Tools | Parallel independent, sequential dependent |
| * Thinking | 5K standard, 8K medium, 10K complex |
