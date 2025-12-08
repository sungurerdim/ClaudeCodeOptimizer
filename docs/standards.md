# CCO Standards

Complete reference of all CCO standards organized by category.

---

## Standards Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  ALWAYS ACTIVE (Base Standards)                                 │
├─────────────────────────────────────────────────────────────────┤
│  Universal      - All projects, AI/human agnostic               │
│  AI-Specific    - All AI assistants, model agnostic             │
│  CCO-Specific   - CCO workflow mechanisms                       │
├─────────────────────────────────────────────────────────────────┤
│  DYNAMICALLY LOADED (Project-Specific)                          │
├─────────────────────────────────────────────────────────────────┤
│  Selected by /cco-tune based on project detection               │
│  Only relevant standards are loaded per project                 │
└─────────────────────────────────────────────────────────────────┘

Counts are dynamically calculated. Run /cco-tune to see current totals.
```

---

## Universal Standards

*Applies to ALL software projects regardless of language, framework, or team size.*

### Code Quality
| Standard | Description |
|----------|-------------|
| Fail-Fast | Immediate visible failure, no silent fallbacks |
| DRY | Single source of truth, zero duplicates |
| No Orphans | Every function called, every import used |
| Type Safety | Annotations where language supports |
| Complexity | Cyclomatic <10 per function |
| Clean Code | Meaningful names, single responsibility, consistent style |
| Immutability | Prefer immutable, mutate only when necessary |
| No Overengineering | Only requested changes, minimum complexity |
| General Solutions | Correct algorithms for all inputs, not just test cases |
| Explicit Over Implicit | Clear intent, no magic values |
| Separation of Concerns | Distinct responsibilities per module |

### File & Resource Management
| Standard | Description |
|----------|-------------|
| Minimal Touch | Only files required for task |
| Paths | Forward slash (/), relative paths, quote spaces |
| No Unsolicited Files | Never create unless requested |
| Resource Management | Cleanup temp files, close handles, release connections |
| Exclusions | Skip .git, node_modules, __pycache__, venv, dist, build |

### Security Fundamentals
| Standard | Description |
|----------|-------------|
| Secrets | Never hardcode, use env vars or vault |
| Input Boundaries | Validate at system entry points |
| Least Privilege | Minimum necessary access/permissions |
| Dependencies | Keep updated, review before adding |
| Defense in Depth | Multiple layers, don't trust single control |
| Secure Defaults | Opt-in to less secure, not opt-out |

### Testing Fundamentals
| Standard | Description |
|----------|-------------|
| Coverage | Meaningful coverage (context-adjusted: 60-90%) |
| Isolation | No dependencies between tests |
| Test Integrity | Never edit tests to make code pass |
| Critical Paths | E2E for critical workflows |
| Reproducible | Same input → same result, no flaky tests |

### Error Handling
| Standard | Description |
|----------|-------------|
| Fail Gracefully | Catch, log context, recover or propagate |
| No Silent Failures | Never swallow exceptions without logging |
| User-Friendly | Technical details in logs, clarity for users |
| Rollback on Failure | Leave system in consistent state |
| Actionable Errors | Include what went wrong and how to fix |

### Documentation
| Standard | Description |
|----------|-------------|
| README | Description, setup, usage |
| CHANGELOG | Version history with breaking changes |
| Comments | Explain why, not what |
| Examples | Working examples for common use cases |

### Workflow
| Standard | Description |
|----------|-------------|
| Review Conventions | Match existing patterns |
| Reference Integrity | Find ALL refs → update in order → verify |
| Decompose | Break complex tasks into smaller steps |
| Version | SemVer (MAJOR.MINOR.PATCH) |

### UX/DX
| Standard | Description |
|----------|-------------|
| Minimum Friction | Fewest steps to goal |
| Maximum Clarity | Unambiguous output, clear next actions |
| Predictability | Consistent behavior across sessions |

---

## AI-Specific Standards

*Applies to ALL AI coding assistants regardless of provider or model.*

### Context Optimization
| Standard | Description |
|----------|-------------|
| Semantic Density | Max meaning per token, concise over verbose |
| Structured Format | Tables/lists over prose for clarity |
| Front-load Critical | Important info first (Purpose → Details → Edge cases) |
| Scannable Hierarchy | Clear H2 → H3 → bullets |
| Reference Over Repeat | Cite by name instead of duplicating |
| Bounded Context | Provide relevant scope, not entire codebase |

### AI Behavior
| Standard | Description |
|----------|-------------|
| Read First | Always read files before proposing edits |
| Plan Before Act | Understand scope before making changes |
| Work Incrementally | Complete one step fully before next |
| Verify Changes | Confirm changes match intent |
| Challenge Assumptions | Question "perfect-looking" solutions |
| Ask When Uncertain | Clarify ambiguous requirements before proceeding |
| State Confidence | Indicate certainty level for non-obvious suggestions |

### Quality Control
| Standard | Description |
|----------|-------------|
| No Vibe Coding | Avoid unfamiliar frameworks without understanding |
| No Example Fixation | Adapt examples to context, don't copy blindly |
| No Hallucination | Don't invent APIs, methods, or features that don't exist |
| Positive Framing | Tell what to do, not what to avoid |
| Contextual Motivation | Explain WHY behaviors matter |

### Status Updates
| Standard | Description |
|----------|-------------|
| Announce Before Action | State what will be done before starting |
| Progress Signals | "Starting...", "In progress...", "Completed" |
| Timing Accuracy | Announce at the right moment (not after completion) |
| Phase Transitions | Clear signals when moving between workflow phases |
| No Silent Operations | User should always know what's happening |

### Multi-Model Compatibility
| Standard | Description |
|----------|-------------|
| Model-Agnostic Instructions | No model-specific syntax in shared rules |
| Capability Awareness | Account for different model strengths |
| Graceful Degradation | Work with models that lack certain features |
| Tool-Agnostic Patterns | Patterns that work across Claude/Codex/Gemini/etc. |

### Output Standards
| Standard | Description |
|----------|-------------|
| Error Format | [SEVERITY] {What} in {file:line} |
| Status Values | OK/WARN/FAIL (consistent terminology) |
| Accounting | done + skip + fail = total (always verify) |
| Structured Results | JSON/table for machine-parseable output |

---

## CCO-Specific Standards

*CCO workflow mechanisms - only for CCO users.*

| Standard | Description |
|----------|-------------|
| Command Flow | Context Check → Read Context → Execute → Report |
| Pre-Operation Safety | Git status check, dirty state handling, rollback support |
| Safety Classification | Safe (auto-apply) vs Risky (require approval) |
| Fix Workflow | Analyze → Report → Approve → Apply → Verify |
| Impact Preview | Show direct changes, dependents, test coverage, risk score |
| Priority Levels | CRITICAL/HIGH/MEDIUM/LOW based on security and impact |
| Approval Flow | AskUserQuestion, multiSelect, priority tabs, pagination |
| Output Formatting | ASCII tables, column alignment, status indicators |
| Context Integration | Read CCO_CONTEXT, apply thresholds and guidelines |
| Claude Code Integration | Parallel tools, subagent delegation, resource scaling |
| Option Labels | [current], [detected], [recommended] markers |

---

## Project-Specific Standards (167 pool)

*Dynamically selected by /cco-tune based on project detection.*

### Categories

| Category | Trigger | Standards |
|----------|---------|-----------|
| Security & Compliance | PII/Regulated data, 10K+ scale, Compliance set | 12 |
| Scale & Architecture | 10K+ scale, Microservices, 100+ | 12 |
| Backend Services | API, DB, or CI/CD detected | 17 |
| Frontend | React/Vue/Angular/Svelte detected | 10 |
| Apps | Mobile, Desktop, or CLI detected | 15 |
| Library | Type: library | 4 |
| Infrastructure | Container/K8s, Serverless, Monorepo | 13 |
| Specialized | ML/AI or Game Dev detected | 10 |
| Collaboration | Team 2+, i18n detected | 17 |
| Real-time | WebSocket/SSE detected | 14 |
| Testing | Testing strategy selected | 20 |
| Observability | SLA level selected | 23 |

**Total pool:** 167 standards (only triggered ones are loaded per project)

### Full list

See [cco-standards-conditional.md](../claudecodeoptimizer/content/standards/cco-standards-conditional.md) for complete standard definitions.

---

## Export Behavior

| Format | Universal | AI-Specific | CCO-Specific | Project-Specific |
|--------|-----------|-------------|--------------|------------------|
| **AGENTS.md** | ✓ | ✓ | ✗ | ✓ (triggered) |
| **CLAUDE.md** | ✓ | ✓ | ✓ | ✓ (triggered) |

CCO-Specific standards are excluded from AGENTS.md export because they depend on CCO's approval flow and tools.

---

*Back to [README](../README.md)*
