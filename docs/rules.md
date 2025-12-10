# CCO Rules

Complete reference of all CCO rules organized by category.

For rule counts, see [README](../README.md#rules).

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
│  Selected by /cco-tune based on project detection               │
│  Only relevant rules are loaded per project                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Rules

*AI/human agnostic - fundamental principles for all software projects.*

### Code Quality
| Rule | Description |
|------|-------------|
| * Fail-Fast | No silent fallbacks, immediate visible failure |
| * DRY | Single source of truth, no duplicates |
| * No-Orphans | Every function called, every import used |
| * Type-Safe | Annotations where supported, prefer immutable |
| * Complexity | Cyclomatic <10 per function |
| * Clean | Meaningful names, single responsibility, consistent style |
| * Explicit | No magic values, clear intent |
| * Scope | Only requested changes, general solutions |

### File & Resource
| Rule | Description |
|------|-------------|
| * Minimal-Touch | Only files required for task |
| * No-Unsolicited | Never create files unless requested |
| * Paths | Forward slash, relative, quote spaces |
| * Cleanup | Temp files, handles, connections |
| * Skip | .git, node_modules, __pycache__, venv, dist, build |

### Security
| Rule | Description |
|------|-------------|
| * Secrets | Env vars or vault only |
| * Input | Validate at system boundaries |
| * Access | Least privilege, secure defaults |
| * Deps | Review before adding, keep updated |
| * Defense | Multiple layers, don't trust single control |

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
| * Catch | Log context, recover or propagate |
| * No-Silent | Never swallow exceptions |
| * User-Facing | Clarity + actionable |
| * Logs | Technical details only |
| * Rollback | Consistent state on failure |

### Documentation
| Rule | Description |
|------|-------------|
| * README | Description, setup, usage |
| * CHANGELOG | Versions with breaking changes |
| * Comments | Why not what |
| * Examples | Working, common use cases |

### Workflow
| Rule | Description |
|------|-------------|
| * Conventions | Match existing patterns |
| * Reference-Integrity | Find ALL refs, update, verify |
| * Decompose | Break complex tasks into steps |
| * Version | SemVer (MAJOR.MINOR.PATCH) |

### UX/DX
| Rule | Description |
|------|-------------|
| * Minimum-Friction | Fewest steps to goal |
| * Maximum-Clarity | Unambiguous output |
| * Predictable | Consistent behavior |

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
| * Scope | Bounded, reference over repeat |

### AI Behavior
| Rule | Description |
|------|-------------|
| * Read-First | NEVER propose edits to unread files |
| * Plan-Before-Act | Understand full scope before any action |
| * Incremental | Complete one step fully before starting next |
| * Verify | Confirm changes match stated intent |
| * Challenge | Question solutions that seem too perfect |
| * Ask | When uncertain, clarify before proceeding |
| * Confidence | Explicitly state uncertainty level |

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
| * Announce | Before action, not after |
| * Progress | Starting > In progress > Completed |
| * Transitions | Clear phase signals |
| * No-Silent | User always knows state |

### Multi-Model
| Rule | Description |
|------|-------------|
| * Agnostic | No model-specific syntax |
| * Graceful | Account for different capabilities |
| * Portable | Patterns work across models |

### Output Rules
| Rule | Description |
|------|-------------|
| * Error | `[SEVERITY] {What} in {file:line}` |
| * Status | OK / WARN / FAIL |
| * Accounting | done + skip + fail = total |
| * Structured | JSON/table when needed |

---

## Tool Rules

*CCO workflow mechanisms - excluded from AGENTS.md export. Loaded on-demand by commands/agents.*

### Core Workflow
| Rule | Description |
|------|-------------|
| * Command-Flow | Context Check > Read > Execute > Report |
| * Safety | Git status check, dirty handling, rollback |
| * Classification | Safe (auto) vs Risky (approval) |
| * Fix-Workflow | Analyze > Report > Approve > Apply > Verify |
| * Impact-Preview | Direct, dependents, tests, risk |
| * Priority | CRITICAL > HIGH > MEDIUM > LOW |

### Approval & Output
| Rule | Description |
|------|-------------|
| * Approval-Flow | AskUserQuestion, multiSelect, pagination |
| * Output-Formatting | ASCII tables, alignment, status |
| * Question-Formatting | Labels, precedence, ordering |

### Workflow Enhancements (v1.1.0+)
| Rule | Description |
|------|-------------|
| * Dynamic-Context | `!` backtick syntax for real-time context injection |
| * Tool-Restrictions | `allowed-tools` frontmatter for command security |
| * Parallel-Execution | Launch multiple agents simultaneously |
| * Quick-Mode | Single-message execution with `--quick` flag |
| * Conservative-Judgment | Prefer lower severity when uncertain |
| * Skip-Criteria | Standard paths/patterns to always skip |
| * Task-Tracking | TodoWrite with accounting verification |

### Integration
| Rule | Description |
|------|-------------|
| * Context-Integration | Read markers, apply thresholds |
| * Tool-Integration | Parallel/sequential, subagents |

---

## Adaptive Rules

*Dynamically selected by /cco-tune based on project detection.*

### Tier System

**Cumulative tiers:** Higher tiers include all rules from lower tiers.

| Category | Tiers | Behavior |
|----------|-------|----------|
| Scale | Small → Medium → Large | Large includes Medium + Small |
| Testing | Basics → Standard → Full | Full includes Standard + Basics |
| Observability | Basics → Standard → HA → Critical | Each includes lower tiers |
| Team | Small → Large | Large includes Small |
| Real-time | Basic → Standard → Low-latency | Higher includes lower |

### Categories

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

### Full list

See [cco-adaptive.md](../claudecodeoptimizer/content/rules/cco-adaptive.md) for complete rule definitions.

---

## Export Behavior

| Format | Core | AI | Tool | Adaptive |
|--------|------|-----|------|----------|
| **AGENTS.md** | Yes | Yes | No | Yes (triggered) |
| **CLAUDE.md** | Yes | Yes | Yes | Yes (triggered) |

Tool rules are excluded from AGENTS.md export because they depend on CCO's approval flow and tools.

---

*Back to [README](../README.md)*
