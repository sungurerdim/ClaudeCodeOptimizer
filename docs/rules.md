# CCO Rules

**Single Source of Truth** for all CCO rules organized by category.

**Counting:** `grep -c "| \* " <file>` - each rule row starts with `| * `

---

## Rules Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  ALWAYS ACTIVE (Core + AI Rules)                                │
├─────────────────────────────────────────────────────────────────┤
│  Core         - All projects, AI/human agnostic                 │
│  AI           - All AI assistants, model agnostic               │
├─────────────────────────────────────────────────────────────────┤
│  ON-DEMAND (Tool Rules)                                         │
├─────────────────────────────────────────────────────────────────┤
│  Tools        - CCO command/agent workflow mechanisms           │
│  Loaded via: !`cat ~/.claude/rules/cco-tools.md 2>/dev/null`    │
├─────────────────────────────────────────────────────────────────┤
│  DYNAMICALLY LOADED (Adaptive Rules)                            │
├─────────────────────────────────────────────────────────────────┤
│  Selected by /cco-config based on project detection             │
│  Only relevant rules are loaded per project                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Rules

*AI/human agnostic - fundamental principles for all software projects.*

### Design Principles
| Rule | Description |
|------|-------------|
| * SSOT | Single source of truth for every piece of data/logic |
| * DRY | Don't repeat yourself, extract common patterns |
| * YAGNI | Only build what's needed now, not hypotheticals |
| * KISS | Simplest solution that works |
| * Separation-of-Concerns | Distinct responsibilities per module |
| * Composition | Prefer composition over inheritance |
| * Idempotent | Same operation, same result, safe to retry |
| * Least-Astonishment | Behavior matches user expectations |

### Code Quality
| Rule | Description |
|------|-------------|
| * Fail-Fast | Immediate visible failure, no silent fallbacks |
| * No-Orphans | Every function called, every import used |
| * Type-Safe | Annotations where supported |
| * Immutable | Prefer immutable, mutate only when necessary |
| * Complexity | Cyclomatic <10 per function |
| * Clean | Meaningful names, single responsibility |
| * Explicit | No magic values, clear intent |
| * Scope | Only requested changes, general solutions |
| * Defensive | Validate assumptions, handle edge cases |

### File & Resource
| Rule | Description |
|------|-------------|
| * Minimal-Touch | Only files required for task |
| * No-Unsolicited | Never create files unless requested |
| * Paths | Forward slash, relative, quote spaces |
| * Cleanup | Temp files, handles, connections |
| * Skip | VCS, deps, build, IDE, generated |

### Efficiency
| Rule | Description |
|------|-------------|
| * Parallel-Independent | Run unrelated operations simultaneously |
| * Sequential-Dependent | Chain dependent operations |
| * Lazy-Evaluation | Defer work until needed |
| * Cache-Reuse | Don't recompute, cache results |
| * Batch-Operations | Group similar operations |

### Security
| Rule | Description |
|------|-------------|
| * Secrets | Env vars or vault only |
| * Input-Boundary | Validate at system entry points |
| * Least-Privilege | Minimum necessary access |
| * Deps-Audit | Review before adding, keep updated |
| * Defense-in-Depth | Multiple layers, don't trust single control |

### Testing
| Rule | Description |
|------|-------------|
| * Coverage | 60-90% context-adjusted |
| * Isolation | No inter-test deps, reproducible |
| * Integrity | Never edit tests to pass code |
| * Critical-Paths | E2E for critical workflows |

### Error Handling
| Rule | Description |
|------|-------------|
| * Catch-Context | Log context, recover or propagate |
| * No-Swallow | Never swallow exceptions silently |
| * User-Actionable | Clarity + next steps for users |
| * Logs-Technical | Technical details only in logs |
| * Rollback-State | Consistent state on failure |

### Analysis
| Rule | Description |
|------|-------------|
| * Architecture-First | Before fixing symptoms, understand system design |
| * Dependency-Mapping | Trace impact through component relationships |
| * Root-Cause-Hunt | Ask "why does this pattern exist?" |
| * Cross-Cutting-Concerns | Check for issues spanning modules |
| * Systemic-Patterns | Identify recurring problems indicating design flaws |

### Documentation
| Rule | Description |
|------|-------------|
| * README | Description, setup, usage |
| * CHANGELOG | Versions with breaking changes |
| * Comments-Why | Explain why, not what |
| * Examples | Working, common use cases |

### Workflow
| Rule | Description |
|------|-------------|
| * Match-Conventions | Follow existing patterns |
| * Reference-Integrity | Find ALL refs, update, verify |
| * Decompose | Break complex tasks into steps |
| * SemVer | MAJOR.MINOR.PATCH |

### UX/DX
| Rule | Description |
|------|-------------|
| * Minimum-Friction | Fewest steps to goal |
| * Maximum-Clarity | Unambiguous output |
| * Predictable | Consistent behavior |
| * Fast-Feedback | Progress indicators, incremental results |

---

## AI Rules

*Portable across Claude/Codex/Gemini - AGENTS.md compatible.*

### Context Optimization
| Rule | Description |
|------|-------------|
| * Semantic-Density | Concise over verbose |
| * Structured | Tables/lists over prose |
| * Front-load | Critical info first |
| * Hierarchy | H2 > H3 > bullets |
| * Reference | Cite by name, don't duplicate |

### Execution Order [CRITICAL]
| Rule | Description |
|------|-------------|
| * Read-First | NEVER propose edits to unread files |
| * Plan-Before-Act | Understand full scope before any action |
| * Incremental | Complete one step fully before starting next |
| * Verify | Confirm changes match stated intent |

### Decision Making
| Rule | Description |
|------|-------------|
| * Challenge | Question solutions that seem too perfect |
| * Ask | When uncertain, clarify before proceeding |
| * Confidence | State uncertainty level for non-obvious |
| * No-Guessing | Never guess file contents without reading |
| * No-Assume | Never assume user intent without confirmation |

### Quality Control
| Rule | Description |
|------|-------------|
| * Understand-First | No vibe coding |
| * Adapt | Examples to context, don't copy blind |
| * No-Hallucination | Only existing APIs/features |
| * Positive | What to do, not what to avoid |
| * Motivate | Explain why behaviors matter |

### Status Updates
| Rule | Description |
|------|-------------|
| * Announce-Before | State action before starting |
| * Progress-Track | Starting > In progress > Completed |
| * Transitions | Clear phase signals |
| * Visible-State | User always knows current state |

### Multi-Model
| Rule | Description |
|------|-------------|
| * Agnostic | No model-specific syntax |
| * Graceful | Account for different capabilities |
| * Portable | Patterns work across models |

### Output Standards
| Rule | Description |
|------|-------------|
| * Error-Format | `[SEVERITY] {What} in {file:line}` |
| * Status-Values | OK / WARN / FAIL |
| * Accounting | done + skip + fail = total |
| * Structured | JSON/table when needed |

---

## Tool Rules

*CCO workflow mechanisms - excluded from AGENTS.md export. Loaded on-demand by commands/agents.*

### User Input [MANDATORY]
| Rule | Description |
|------|-------------|
| * AskUserQuestion-Required | ALL questions/confirmations → AskUserQuestion tool |
| * No-Plain-Text-Questions | Plain text questions = VIOLATION, stop command |
| * No-Workarounds | Cannot skip by rephrasing as statement |
| * All-Stages | Start, middle, end, follow-up → all use tool |
| * MultiSelect-When-Valid | Use `multiSelect: true` when multiple selections valid |
| * Semicolon-Separator | Use `;` to separate options, never comma |
| * Self-Check | Before `?` or choices → must use AskUserQuestion |

### Command Flow
| Rule | Description |
|------|-------------|
| * Context-Check | Verify context.md exists, suggest /cco-config if missing |
| * Read-Context | Load `.claude/rules/cco/context.md` |
| * Execute | Command-specific logic |
| * Report | Results with accounting |

### Safety
| Rule | Description |
|------|-------------|
| * Pre-op | Git status before modifications |
| * Dirty-Handling | Prompt Commit / Stash / Continue |
| * Rollback | Clean state enables git checkout |
| * Safe-Auto | Remove imports, parameterize SQL, move secrets, fix lint, add types |
| * Risky-Approval | Auth changes, DB schema, API contract, delete files, rename public |

### Fix Workflow
| Rule | Description |
|------|-------------|
| * Flow | Analyze > Report > Approve > Apply > Verify |
| * Output-Accounting | `Applied: N \| Skipped: N \| Failed: N \| Total: N` |

### Impact Preview
| Rule | Description |
|------|-------------|
| * Direct | Files to modify |
| * Dependents | Files that import/use |
| * Tests | Coverage of affected code |
| * Risk | LOW / MEDIUM / HIGH |
| * Skip-Preview | LOW risk, <=2 files, full coverage |

### Priority
| Rule | Description |
|------|-------------|
| * CRITICAL | Security, data exposure |
| * HIGH | High-impact, low-effort |
| * MEDIUM | Balanced impact/effort |
| * LOW | Style, minor optimization |

### Question Patterns
| Rule | Description |
|------|-------------|
| * Max-Questions | 4 per AskUserQuestion call |
| * Max-Options | 4 per question |
| * Overflow | Use multiple sequential calls |
| * MultiSelect-Batch | true for batch approvals |
| * All-Option | First option = "All ({N})" for bulk |
| * Priority-Order | CRITICAL → HIGH → MEDIUM → LOW |
| * Item-Format | `{description} [{file:line}] [{safe\|risky}]` |

### Labels
| Rule | Description |
|------|-------------|
| * One-Label | Each option has exactly ONE label |
| * Current | `[current]` - matches existing config (priority 1) |
| * Detected | `[detected]` - auto-detected (priority 2) |
| * Recommended | `(Recommended)` - max 1/question (priority 3) |
| * Precedence | detected AND current → show `[current]` only |

### Ordering
| Rule | Description |
|------|-------------|
| * Numeric | Ascending (60 → 70 → 80 → 90) |
| * Severity | Safest → riskiest |
| * Scope | Narrowest → widest |

### Output Formatting
| Rule | Description |
|------|-------------|
| * Table-Borders | `─│┌┐└┘├┤┬┴┼` |
| * Table-Headers | `═║╔╗╚╝` |
| * Numbers-Right | Right-aligned |
| * Text-Left | Left-aligned |
| * Status-Center | Centered |
| * Status-Values | OK \| WARN \| FAIL \| PASS \| SKIP |
| * Progress-Bar | `filled = round(percentage / 100 * 8)` → `████░░░░` |
| * No-Emojis | No emojis in tables |
| * No-Extra-Unicode | No unicode decorations beyond specified |

### Dynamic Context
| Rule | Description |
|------|-------------|
| * Backtick-Syntax | Use `!` backtick for real-time context |
| * Git-Status | `` `git status --short` `` |
| * Branch | `` `git branch --show-current` `` |
| * CCO-Context | `` `head -30 .claude/rules/cco/context.md` `` |
| * Accuracy | Real-time accuracy over stale assumptions |
| * Anti-Hallucination | Reduces hallucination risk |

### Parallel Execution
| Rule | Description |
|------|-------------|
| * Independent-Parallel | Launch parallel agents for independent scans |
| * Batch-Reads | Multiple file reads in single call |
| * Unrelated-Simultaneous | Run unrelated checks simultaneously |
| * Dependent-Sequential | Run dependent operations sequentially |
| * Agent-Launch | Launch agents simultaneously in single message |
| * Agent-Scope | Each agent handles distinct scope |
| * Agent-Diverse | Use varied search strategies per agent |
| * Agent-Merge | Merge results after all complete |

### Agent Propagation
| Rule | Description |
|------|-------------|
| * Context-Pass | Pass context.md summary to all agents |
| * Rules-Pass | Include applicable rules from context |
| * Format-Pass | Specify exact output format expected |
| * Todo-Pass | Tell agents: "Make a todo list first" |

### Quick Mode
| Rule | Description |
|------|-------------|
| * No-Questions | Do not ask questions |
| * Defaults | Use smart defaults for all options |
| * No-Intermediate | Do not output intermediate text |
| * Summary-Only | Only tool calls, then final summary |
| * Single-Message | Complete ALL steps in a single message |

### Conservative Judgment
| Rule | Description |
|------|-------------|
| * Severity-Keywords | crash/data loss → CRITICAL, broken → HIGH, error → MEDIUM, style → LOW |
| * False-Positive-Prevention | False positives erode trust faster than missed issues |
| * Lower-When-Uncertain | When uncertain between severities, choose lower |
| * Genuine-Issues | Only flag issues that genuinely block users |
| * Evidence-Required | Require explicit evidence, not inference |
| * Style-Never-High | Style issues → never CRITICAL or HIGH |
| * Single-Never-Critical | Single occurrence → never CRITICAL unless security |

### Skip Criteria
| Rule | Description |
|------|-------------|
| * Line-Ignore | `// cco-ignore` or `# cco-ignore` - skip line |
| * File-Ignore | `// cco-ignore-file` or `# cco-ignore-file` - skip file |
| * Markdown-Ignore | `<!-- cco-ignore -->` - skip in markdown |
| * Test-Fixtures | Skip `fixtures/`, `testdata/`, `__snapshots__/` |
| * Examples | Skip `examples/`, `samples/`, `demo/`, `benchmarks/` |

### Progress Tracking (TodoWrite)
| Rule | Description |
|------|-------------|
| * Start-With-Todo | Create todo list with ALL steps at command start |
| * Track-In-Progress | Mark `in_progress` before starting each step |
| * Update-Completed | Mark `completed` immediately after each step |
| * Single-Active | Exactly ONE item `in_progress` at a time |
| * Immediate-Update | Update status immediately, not batched |
| * No-Skip-Items | Never skip items - update status instead |
| * ActiveForm-Continuous | Use present continuous (-ing form) |
| * Content-Imperative | Use imperative form |

### Artifact Handling
| Rule | Description |
|------|-------------|
| * Reference-Large | Reference large outputs by path/ID, not inline |
| * Tokenize-Efficiently | Use `[artifact:path]` notation for files >500 lines |
| * Summarize-First | Provide digest before full artifact access |
| * Chunk-Processing | Process large data in manageable segments |
| * Cache-Artifacts | Reuse analyzed artifacts within session |

### Strategy Evolution
| Rule | Description |
|------|-------------|
| * Learnings-Location | `.claude/rules/cco/context.md` → `## Learnings` section |
| * Avoid-Section | Pattern + why it failed + what works instead |
| * Prefer-Section | Pattern + why it works + impact level |
| * Systemic-Section | Issue + root cause + recommendation |
| * Session-Start | Read context.md, note Learnings section |
| * Check-Avoid | Check Avoid patterns before recommending |
| * Max-Items | 5 per category (remove oldest when full) |
| * Update-Existing | Update existing instead of adding duplicate |

---

## Adaptive Rules

*Dynamically selected by /cco-config based on project detection.*

### Tier System

**Cumulative tiers:** Higher tiers include all rules from lower tiers.

| Category | Tiers | Behavior |
|----------|-------|----------|
| Scale | Small → Medium → Large | Large includes Medium + Small |
| Testing | Basics → Standard → Full | Full includes Standard + Basics |
| Observability | Basics → Standard → HA → Critical | Each includes lower tiers |
| Team | Small → Large | Large includes Small |
| Real-time | Basic → Standard → Low-latency | Higher includes lower |

### Categories & Triggers

| Category | Trigger |
|----------|---------|
| * Security & Compliance | PII/Regulated data, 10K+ scale, Compliance set |
| * Scale | 100+ users (cumulative tiers) |
| * Backend > API | REST/GraphQL/gRPC detected |
| * Backend > Data | DB != None |
| * Backend > Operations | CI/CD AND NOT CLI/Library |
| * Backend > CI Only | CI/CD AND (CLI OR Library) |
| * Frontend | React/Vue/Angular/Svelte/Next/Nuxt detected |
| * Apps > Mobile | iOS/Android/RN/Flutter |
| * Apps > Desktop | Electron/Tauri/native |
| * Apps > CLI | Type: CLI |
| * Library | Type: Library |
| * Infra > Container | Docker detected (not in examples/) |
| * Infra > Kubernetes | K8s/Helm detected |
| * Infra > Serverless | Lambda/Functions/Vercel/Netlify |
| * Infra > Monorepo | nx/turbo/lerna/pnpm-workspace |
| * ML/AI | torch/tensorflow/sklearn/transformers/langchain |
| * Game | Unity/Unreal/Godot |
| * Team | Team 2+ (cumulative tiers) |
| * i18n | locales/i18n/messages/ detected |
| * Real-time | WebSocket/SSE detected (cumulative tiers) |
| * Testing | User-selected (cumulative tiers) |
| * Observability | SLA-based (cumulative tiers) |

### Full Adaptive Rules List

For complete rule definitions per category, see [cco-adaptive.md](../claudecodeoptimizer/content/rules/cco-adaptive.md).

---

## Export Behavior

### Format Comparison

| Format | Target | Core | AI | Tool | Adaptive |
|--------|--------|------|-----|------|----------|
| **AGENTS.md** | Universal (Codex, Cursor, Copilot, Cline, etc.) | Yes | Yes | No | Yes (triggered) |
| **CLAUDE.md** | Claude Code only | Yes | Yes | Yes | Yes (triggered) |

### Why AGENTS.md Excludes Tool Rules

Tool rules depend on Claude Code specific features:
- `AskUserQuestion`, `TodoWrite`, `Task` tool references
- `.claude/` directory structure
- CCO command integration (`/cco-*`)

### Content Filtering (AGENTS.md)

AGENTS.md export filters Claude-specific content for cross-tool compatibility:

| Category | Filtered | Reason |
|----------|----------|--------|
| Tool names | `Read`, `Write`, `Edit`, `Bash`, `Task`, etc. | Claude Code specific |
| Paths | `~/.claude/`, `.claude/` | Claude directory structure |
| Product refs | "Claude Code", "Claude" | Vendor-specific |
| CCO refs | `cco-*`, `/cco-*` | CCO-specific features |

Model-agnostic principles (DRY, Fail-Fast, Read-First) are preserved.

---

*Back to [README](../README.md)*
