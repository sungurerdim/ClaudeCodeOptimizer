# Tools Rules
*On-demand loading for CCO commands and agents*

## User Input [MANDATORY - NO ALTERNATIVES]

### AskUserQuestion Tool Requirement [ABSOLUTE]

**RULE:** Every user interaction MUST use `AskUserQuestion` native tool. No exceptions. No alternatives.

| Requirement | Enforcement |
|-------------|-------------|
| **Mandatory** | ALL questions, confirmations, selections → AskUserQuestion |
| **No Alternatives** | Plain text questions = VIOLATION, stop command |
| **No Workarounds** | Cannot skip by rephrasing as statement |
| **All Stages** | Start, middle, end, follow-up → all use tool |
| **MultiSelect** | Use `multiSelect: true` when multiple selections valid |

### Applies To (ALL of these)

| Scenario | Example | MultiSelect |
|----------|---------|-------------|
| Confirmations | "Apply this configuration?" | false |
| Scope selection | "What to audit?" | true |
| Option selection | "Which files to include?" | true |
| Yes/No decisions | "Add BREAKING CHANGE footer?" | false |
| Action selection | "Accept / Modify / Cancel" | false |
| Follow-up actions | "Apply recommendations?" | true |
| Final decisions | "Proceed with release?" | false |
| Clarifications | "Which module do you mean?" | false |
| Error recovery | "How to proceed?" | false |

### Prohibited Patterns [VIOLATION = STOP]

| Pattern | Why Prohibited | Action |
|---------|----------------|--------|
| "Would you like me to...?" | Plain text question | STOP |
| "Do you want to...?" | Plain text question | STOP |
| "Should I...?" | Plain text question | STOP |
| "Let me know if..." | Implicit question | STOP |
| "Feel free to..." | Passive request | STOP |
| Any `?` without AskUserQuestion | Bypassing tool | STOP |
| Statements expecting response | Disguised question | STOP |

### Option Separator [STRICT]

- **Separator**: Use semicolon (`;`) to separate options
- **No-Comma**: Never use comma - ambiguous with multi-word options
- **Consistent**: Same format across all commands

**Examples:**
- ✓ `Accept; Modify; Cancel`
- ✓ `Yes, proceed anyway; No, fix first` (comma OK within single option)
- ✗ `Accept, Modify, Cancel` (ambiguous)
- ✗ `Yes, proceed anyway, No, fix first` (very ambiguous)

### Command Template Standard [REQUIRED]

All command templates MUST define interactions as tables:

```markdown
## User Input

| Question | Options | MultiSelect |
|----------|---------|-------------|
| {question}? | {opt1}; {opt2}; ... | true/false |
```

**Execution:** When command reaches this table → call `AskUserQuestion` with exact parameters.

### Self-Check Before Response

Before ANY response that expects user input:
1. Does it contain `?` → Must use AskUserQuestion
2. Does it offer choices → Must use AskUserQuestion
3. Does it need confirmation → Must use AskUserQuestion
4. Is it a statement but waits for reply → Must use AskUserQuestion

## Command Flow

- **Context-Check**: Verify context.md exists, suggest /cco-config if missing
- **Read-Context**: Load `.claude/rules/cco/context.md`
- **Execute**: Command-specific logic
- **Report**: Results with accounting

## Context Requirement [CRITICAL]

All commands (except `/cco-config`) require CCO context. Check at command start:

```
If context check returns "0":
  CCO context not found.
  Run /cco-config first to configure project context, then restart CLI.
  **Stop immediately.**
```

**Enforcement:** No partial execution. No fallback. Stop and instruct user.

## Token Efficiency [CRITICAL]

Minimize token usage at every step:

| Principle | Implementation |
|-----------|----------------|
| **Single-Agent** | ONE analyze agent, ONE apply agent per command |
| **Linter-First** | Run linters before grep patterns (avoid duplication) |
| **Batch-Calls** | Group multiple tool calls in single message |
| **Targeted-Reads** | Read only matched files, use offset/limit |
| **Early-Exit** | Stop when saturation reached (3× repeated themes) |

**Anti-patterns:** Per-file agents │ Per-scope agents │ Full file reads │ Redundant searches

## Safety

- **Pre-op**: Git status before modifications
- **Dirty**: Prompt Commit / Stash / Continue
- **Rollback**: Clean state enables git checkout

### Classification

**Safe (auto-apply):**

- **Remove-Imports**: Remove unused imports
- **Parameterize-SQL**: Parameterize SQL queries
- **Move-Secrets**: Move secrets to env
- **Fix-Lint**: Fix linting issues
- **Add-Types**: Add type annotations

**Risky (require approval):**

- **Auth-Changes**: Auth/CSRF changes
- **DB-Schema**: DB schema changes
- **API-Contract**: API contract changes
- **Delete-Files**: Delete files
- **Rename-Public**: Rename public APIs

## Fix Workflow

- **Flow**: Analyze > Report > Approve > Apply > Verify
- **Output**: `Applied: N | Declined: N | Failed: N | Total: N`

## Impact Preview

- **Direct**: Files to modify
- **Dependents**: Files that import/use
- **Tests**: Coverage of affected code
- **Risk**: LOW / MEDIUM / HIGH
- **Skip**: LOW risk, <=2 files, full coverage

## Priority

- **CRITICAL**: Security, data exposure
- **HIGH**: High-impact, low-effort
- **MEDIUM**: Balanced impact/effort
- **LOW**: Style, minor optimization

## Question Patterns

*All questions inherit User Input [MANDATORY] rules above.*

### Pagination [LIMITS]

- **Max-Questions**: 4 per AskUserQuestion call
- **Max-Options**: 4 per question
- **Overflow**: Use multiple sequential calls

### Batch Approval (for fix operations)

- **MultiSelect**: true for batch approvals
- **All-Option**: First option = "All ({N})" for bulk
- **Priority-Order**: CRITICAL → HIGH → MEDIUM → LOW
- **Item-Format**: `{description} [{file:line}] [{safe|risky}]`

### Labels [MANDATORY]

- **One-Label**: Each option has exactly ONE label
- **Current**: `[current]` - matches existing config (priority 1)
- **Detected**: `[detected]` - auto-detected (priority 2)
- **Recommended**: `(Recommended)` - max 1/question (priority 3)
- **Precedence**: detected AND current → show `[current]` only

### Ordering

- **Numeric**: Ascending (60 → 70 → 80 → 90)
- **Severity**: Safest → riskiest
- **Scope**: Narrowest → widest

### Category Separation

Present different categories in SEPARATE batches:

| Type | Examples |
|------|----------|
| Settings | strictMode, timeout |
| Permissions | readOnly, allowDelete |
| Thresholds | coverage%, complexity |

## Output Formatting

**Follow output formats precisely. Exact formatting ensures consistency and parseability.**

### Table Characters [STRICT]

- **Borders**: `─│┌┐└┘├┤┬┴┼`
- **Headers**: `═║╔╗╚╝`

### Alignment [REQUIRED]

- **Numbers**: Right-aligned
- **Text**: Left-aligned
- **Status**: Centered

### Status Indicators [EXACT]

- **Values**: OK | WARN | FAIL | PASS | SKIP

### Progress Bars [FORMULA]

- **Formula**: `filled = round(percentage / 100 * 8)` -> `████░░░░`

### Prohibited

- **No-Emojis**: No emojis in tables
- **No-Unicode**: No unicode decorations beyond specified
- **No-ASCII-Art**: No ASCII art headers

## Dynamic Context

### Injection Syntax [REQUIRED]

- **Syntax**: Use `!` backtick for real-time context
- **Git-Status**: `` `git status --short` ``
- **Branch**: `` `git branch --show-current` ``
- **CCO-Context**: `` `test -f .claude/rules/cco/context.md && head -30 .claude/rules/cco/context.md` ``

### When to Use

| Context Type | Command | Example |
|--------------|---------|---------|
| Git state | commit, refactor | `` `git status` `` |
| File content | audit, review | `` `head -50 .claude/rules/cco/context.md` `` |
| Dependencies | audit, health | `` `cat package.json \| jq .dependencies` `` |
| Recent changes | commit, review | `` `git log --oneline -5` `` |

### Benefits

- **Accuracy**: Real-time accuracy over stale assumptions
- **Anti-Hallucination**: Reduces hallucination risk
- **Efficiency**: Eliminates redundant file reads

## Parallel Execution

### When to Parallelize [REQUIRED]

| Scenario | Action |
|----------|--------|
| Independent scans | Launch parallel agents |
| Multiple file reads | Batch in single call |
| Unrelated checks | Run simultaneously |
| Dependent operations | Run sequentially |

### Agent Parallelization Pattern

- **Launch**: Launch agents simultaneously in single message
- **Scope**: Each agent handles distinct scope
- **Diverse**: Use varied search strategies per agent
- **Merge**: Merge results after all complete

### Agent Propagation [REQUIRED]

- **Context-Pass**: Pass context.md summary to all agents
- **Rules-Pass**: Include applicable rules from context
- **Format-Pass**: Specify exact output format expected
- **Todo-Pass**: Tell agents: "Make a todo list first"

**Template for agent instructions:**
```
Context: {relevant context.md fields}
Rules: {applicable rules from this file}
Output: {expected format - follow precisely}
Note: Make a todo list first, then process systematically
```

### Benefits

- **Speed**: Faster execution (N agents = ~1/N time)
- **Coverage**: Better coverage (diverse search strategies)
- **Context**: Reduced context switching

## Quick Mode

### Single-Message Enforcement [STRICT]

- **No-Questions**: Do not ask questions
- **Defaults**: Use smart defaults for all options
- **No-Intermediate**: Do not output intermediate text
- **Summary**: Only tool calls, then final summary
- **MUST-Single**: You MUST do all steps in a single message

### Applicable Commands

| Command | Quick Behavior |
|---------|----------------|
| `/cco-commit` | Stage all, single commit, smart defaults |
| `/cco-research` | T1-T2 only, brief output, no questions |
| `/cco-review` | Smart defaults, report only |
| `/cco-preflight` | (Not applicable - requires explicit decisions) |

### Output Restriction

- **Single-Message**: Complete ALL steps in a single message
- **No-Extra-Tools**: Do not use any other tools beyond allowed
- **No-Extra-Text**: Do not send any text besides tool calls and final summary

## Conservative Judgment

### Severity Assignment [CRITICAL]

| Keyword | Severity | Confidence Required |
|---------|----------|---------------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

### False Positive Prevention

- **Trust**: False positives erode user trust faster than missed issues
- **Lower**: When uncertain between two severities, choose lower
- **Genuine**: Only flag issues that genuinely block users
- **Evidence**: Require explicit evidence, not inference

### Prohibited Escalations

- **Style**: Style issues -> never CRITICAL or HIGH
- **Unverified**: Unverified claims -> never above MEDIUM
- **Single**: Single occurrence -> never CRITICAL unless security

## Skip Criteria

*Base skip paths defined in Core Rules (Skip).*

### CCO Skip Markers

- **Line**: `// cco-ignore` or `# cco-ignore` - skip this line
- **File**: `// cco-ignore-file` or `# cco-ignore-file` - skip entire file
- **Markdown**: `<!-- cco-ignore -->` - skip in markdown

### Additional CCO Exclusions

- **Test Fixtures**: `fixtures/`, `testdata/`, `__snapshots__/`
- **Examples**: `examples/`, `samples/`, `demo/`, `benchmarks/`

## Progress Tracking (TodoWrite)

**All CCO commands use TodoWrite for progress visibility.** No custom step announcements.

### Requirement [CRITICAL]

1. **Start**: Create todo list with ALL steps/phases at command start
2. **Track**: Mark `in_progress` before starting each step
3. **Update**: Mark `completed` immediately after each step finishes
4. **Single**: Exactly ONE item `in_progress` at a time

### Format

```
TodoWrite([
  { content: "{step_name}", status: "in_progress", activeForm: "{step_name_ing}" },
  { content: "{step_name}", status: "pending", activeForm: "{step_name_ing}" },
  ...
])
```

### Rules

| Rule | Description |
|------|-------------|
| **Immediate** | Update status immediately, not batched |
| **No-Skip** | Never skip items - update status instead |
| **activeForm** | Use present continuous (-ing form) |
| **content** | Use imperative form |

## Artifact Handling

- **Reference-Large**: Reference large outputs by path/ID, not inline
- **Tokenize-Efficiently**: Use `[artifact:path]` notation for files >500 lines
- **Summarize-First**: Provide digest before full artifact access
- **Chunk-Processing**: Process large data in manageable segments
- **Cache-Artifacts**: Reuse analyzed artifacts within session

## Strategy Evolution

### Learnings Section [REQUIRED]

**Location:** `.claude/rules/cco/context.md` → `## Learnings` section

**Format:**
```markdown
## Learnings

### Avoid
- {pattern}: {why it failed} → {what works instead}

### Prefer
- {pattern}: {why it works} [{impact: high|medium|low}]

### Systemic
- {issue}: {root cause} → {recommendation}
```

### Usage Flow

| Phase | Action |
|-------|--------|
| Session Start | Read context.md, note Learnings section |
| Analysis | Check Avoid patterns before recommending |
| Failure | Add to Avoid with root cause |
| Success | Add to Prefer with context |
| Systemic | Add architectural findings to Systemic |

### Rules

- **Max Items**: 5 per category (remove oldest when full)
- **Duplicates**: Update existing instead of adding new
- **Format**: Single line per learning, concise
