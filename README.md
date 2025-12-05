# ClaudeCodeOptimizer

A process and standards layer for Claude Code in the Opus 4.5 era.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/claudecodeoptimizer.svg)](https://pypi.org/project/claudecodeoptimizer/)
[![Claude 4 Best Practices](https://img.shields.io/badge/Claude_4-Best_Practices-blueviolet.svg)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

> **Fully aligned with [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)** - Agentic coding, extended thinking, parallel tools, context management.

> Claude already knows how to code. CCO adds safety, approval, and consistency.

> **Claude Code exclusive.** CCO runs only inside Claude Code (CLI or IDE extension). Standards can be exported to AGENTS.md for use with other AI tools, but CCO itself requires Claude Code.

![CCO Environment](docs/screenshots/environment.png)
*CCO lives directly inside Claude Code, no extra UI.*

---

## Design Principles

CCO is built on these core principles that guide all development and usage:

### Transparency
- **Announce Before Action**: Always state what will be done before starting
- **Progress Signals**: Clear "Starting...", "In progress...", "Completed" messages
- **No Silent Operations**: User should always know what's happening
- **Phase Transitions**: Clear signals when moving between workflow phases

### Single Source of Truth (SSOT)
- **No Hardcoded Values**: Use placeholders like `{value}` instead of fixed examples
- **Reference Over Repeat**: Standards are defined once, referenced by name
- **Context-Driven**: All thresholds and behaviors come from project context

### DRY (Don't Repeat Yourself)
- **Standards Reference**: Commands reference `**Standards:** X | Y | Z` instead of duplicating
- **Shared Agents**: Three agents (detect, scan, action) serve all commands
- **Conditional Loading**: Project-specific standards loaded only when relevant

### User Control
- **Approval Required**: No silent changes to codebase
- **Priority Classification**: CRITICAL > HIGH > MEDIUM > LOW
- **Safety Classification**: Safe (auto-apply) vs Risky (require approval)
- **Rollback Support**: Clean git state enables safe recovery

### AI Efficiency
- **Semantic Density**: Maximum meaning per token
- **Structured Format**: Tables/lists over prose for clarity
- **Front-load Critical**: Important info first (Purpose → Details → Edge cases)
- **Bounded Context**: Relevant scope only, not entire codebase

---

## What CCO Does (and Does NOT Do)

**CCO is NOT teaching Claude how to code.** Opus 4.5 already knows:
- How to write clean, maintainable code
- Security best practices
- Testing patterns
- Refactoring techniques

**CCO adds process layers** around what Claude already does well:

| Layer | What It Adds | Example |
|-------|--------------|---------|
| **Pre-** | Safety checks before action | Git status check, dirty state handling |
| **Process** | Standardized workflows | Approval flow, priority levels |
| **Post-** | Verification and reporting | `done + skip + fail = total` |
| **Context** | Project-aware behavior | Scale, team size → adjusted thresholds |

---

## Quickstart

```bash
# Install + setup (one-time, copies to ~/.claude/)
pip install claudecodeoptimizer && cco-setup

# Inside Claude Code, tune for your project (auto-detect, one confirmation)
/cco-tune --quick

# Start using
/cco-audit --smart
```

**That's it.** The `--quick` flag auto-detects your project and applies sensible defaults with a single confirmation. Use `/cco-tune` (without flag) for full interactive configuration.

---

## Requirements

- **Python 3.10+** (tested on 3.10–3.14)
- **Claude Code** CLI or IDE extension
- **Zero Python dependencies** - uses only standard library

---

## Standards Architecture

CCO uses a **four-category standards system** designed for clarity and portability:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STANDARDS ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. UNIVERSAL (48 standards)                        [Always Active]  │   │
│  │    • Applies to ALL projects, AI or human                           │   │
│  │    • Fundamental principles: DRY, Fail-Fast, Clean Code             │   │
│  │    • Location: ~/.claude/CLAUDE.md                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. AI-SPECIFIC (31 standards)                      [Always Active]  │   │
│  │    • Standards that help AI assistants work more effectively        │   │
│  │    • AI efficiency: Semantic Density, Read First, No Hallucination  │   │
│  │    • Location: ~/.claude/CLAUDE.md                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. CCO-WORKFLOW (19 standards)                     [Always Active]  │   │
│  │    • CCO-specific mechanisms: Git safety, Approval flow             │   │
│  │    • Location: ~/.claude/CLAUDE.md                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. PROJECT-SPECIFIC (108 standards pool)           [Selective]      │   │
│  │    • /cco-tune selects ~10-25 based on YOUR project                 │   │
│  │    • 17 categories: Frontend, Mobile, API, ML/AI, Game, etc.        │   │
│  │    • Location: ./CLAUDE.md (per-project)                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  BASE: 98 standards (always active)                                         │
│  TYPICAL: ~110-125 standards (base + project-specific selections)           │
│  POOL: 206 standards (full library, never all active at once)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key insight:** You never have 206 standards active. The base 98 are always on, then /cco-tune adds only the ~10-25 that match your project type.

### Category Details

#### Universal Standards
*Applies to ALL software projects regardless of language, framework, or team size.*

| Section | Standards | Examples |
|---------|-----------|----------|
| Code Quality | 12 | Fail-Fast, DRY, No Orphans, Type Safety, Complexity <10 |
| File & Resource | 6 | Minimal Touch, Cleanup, Resource Disposal |
| Security | 6 | Secrets, Input Boundaries, Least Privilege |
| Testing | 5 | Coverage, Isolation, Reproducible |
| Error Handling | 5 | Fail Gracefully, No Silent Failures, Actionable Errors |
| Documentation | 4 | README, CHANGELOG, Comments |
| Workflow | 4 | Reference Integrity, Decompose, SemVer |
| UX/DX | 6 | Minimum Friction, Fast Feedback, Transparency |

#### AI-Specific Standards
*Applies to ALL AI coding assistants for better quality and efficiency. AGENTS.md compatible.*

| Section | Standards | Examples |
|---------|-----------|----------|
| Context Optimization | 6 | Semantic Density, Front-load Critical, Bounded Context |
| AI Behavior | 7 | Read First, Plan Before Act, Ask When Uncertain |
| Quality Control | 5 | No Vibe Coding, No Hallucination, Positive Framing |
| Status Updates | 5 | Announce Before Action, Progress Signals, Timing Accuracy |
| Multi-Model | 4 | Model-Agnostic, Tool-Agnostic Patterns |
| Output | 4 | Error Format, Status Values, Accounting |

#### Project-Specific Standards
*Selected by /cco-tune based on detection. Only relevant standards load.*

| Category | Trigger | Standards |
|----------|---------|-----------|
| Security Enhanced | PII/Regulated OR 10K+ | 8 |
| Architecture | 10K+ OR microservices | 6 |
| Operations | CI/CD detected | 7 |
| Performance | Scale 100+ | 6 |
| Data | DB detected | 5 |
| API | REST/GraphQL/gRPC | 6 |
| Frontend | React/Vue/Angular/etc. | 10 |
| Mobile | iOS/Android/RN/Flutter | 6 |
| Desktop | Electron/Tauri/native | 4 |
| CLI | CLI tool | 5 |
| Library | Package/library | 5 |
| ML/AI Projects | PyTorch/TF/sklearn | 6 |
| Game Dev | Unity/Unreal/Godot | 4 |
| Serverless | Lambda/Functions | 4 |
| Monorepo | nx/turborepo/lerna | 4 |
| Container/K8s | Docker/K8s | 5 |
| Team Collaboration | Team 2+ | 8 |
| Compliance | SOC2/HIPAA/PCI/GDPR | 4 |
| i18n | Multi-language | 5 |

#### CCO-Workflow
*CCO-specific mechanisms for safety and approval.*

| Section | Purpose |
|---------|---------|
| Pre-Operation Safety | Git status check, dirty state handling |
| Safety Classification | Safe vs risky changes |
| Fix Workflow | Analyze → Report → Approve → Apply → Verify |
| Priority & Approval | CRITICAL/HIGH/MEDIUM/LOW, pagination |
| Claude Code Integration | Parallel tools, subagents, resource scaling |

### Export Standards

**Take your standards with you.** Export your curated standards for use with other AI tools or share with other Claude Code users:

```bash
/cco-tune --export
```

Choose export format:
- **AGENTS.md** - Prose format for other AI tools (Cursor, Windsurf, Copilot, etc.)
- **CLAUDE.md** - Minimal format for sharing with other Claude Code projects

**What exports:** Universal + AI-Specific + your selected Project-Specific standards
**What stays:** CCO-Workflow - requires Claude Code's approval flow

---

## Commands

![CCO Commands](docs/screenshots/commands-list.png)

| Command | Purpose |
|---------|---------|
| `/cco-tune` | Project tuning: context + AI settings + configuration |
| `/cco-health` | Metrics dashboard with actionable next steps |
| `/cco-audit` | Quality gates with prioritized fixes |
| `/cco-optimize` | AI context, docs, code efficiency |
| `/cco-review` | Strategic architecture analysis |
| `/cco-generate` | Convention-following generation |
| `/cco-refactor` | Safe structural changes with rollback |
| `/cco-commit` | Quality-gated atomic commits |

---

## Project Tuning

`/cco-tune` is the central configuration command:

![cco-tune](docs/screenshots/tune-flow.png)

### What It Does

1. **Detects** your project: stack, type, scale, team size
2. **Selects** relevant Project-Specific standards
3. **Writes** context to `./CLAUDE.md`
4. **Configures** AI settings (thinking tokens, MCP limits)

### Context Format

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {description}
Team: Solo | Scale: <100 | Data: Public | Compliance: None
Stack: Python 3.10+, pytest | Type: CLI | DB: None

## AI Performance
Thinking: 8K | MCP: 25K | Caching: on

## Guidelines
- Self-review sufficient
- Simple solutions, optimize for clarity

## Operational
Tools: ruff format, pytest
Applicable: security, tech-debt, tests, docs

## Project-Specific Standards
{selected from 17 categories based on detection}
<!-- CCO_CONTEXT_END -->
```

---

## Audit Categories

| Flag | What It Checks |
|------|----------------|
| `--security` | OWASP, secrets, CVEs, supply chain |
| `--tech-debt` | Dead code, complexity, duplication |
| `--self-compliance` | Code vs project's stated standards |
| `--consistency` | Doc-code mismatches |
| `--tests` | Coverage, isolation, flaky tests |
| `--performance` | Caching, N+1, async issues |
| `--docs` | README, docstrings, API docs |

**Meta-flags:** `--smart` (auto-detect), `--critical`, `--weekly`, `--all`

---

## Safety Features

### Git Safety
- Checks `git status` before changes
- Offers: Commit / Stash / Continue
- Enables rollback on failure

### Approval Flow
- No silent changes
- Risk classification: safe vs risky
- Priority levels: CRITICAL → HIGH → MEDIUM → LOW
- Verification: `Applied: N | Skipped: N | Failed: N`

---

## Installation

**pip (recommended):**
```bash
pip install claudecodeoptimizer && cco-setup
```

**pipx (isolated):**
```bash
pipx install claudecodeoptimizer && cco-setup
```

**Development:**
```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git && cco-setup
```

**Upgrade:**
```bash
pip install -U claudecodeoptimizer && cco-setup
```

## Uninstallation

```bash
cco-remove  # Complete removal with confirmation
```

---

## How CCO Differs

| Aspect | Typical AI Rules | CCO Approach |
|--------|------------------|--------------|
| Scope | Static rule files | Context-aware, project-detected |
| Safety | Trust the AI | Git checks, approval flow, rollback |
| Standards | Generic guidelines | Base + selective project-specific |
| Workflow | Rules only | Full process: Analyze → Approve → Apply → Verify |
| Portability | Tool-specific | AGENTS.md export for other tools |

**CCO adds process layers** (safety, approval, verification) on top of what AI already does well.

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
