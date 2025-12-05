# ClaudeCodeOptimizer

A process and standards layer for Claude Code in the Opus 4.5 era.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/claudecodeoptimizer.svg)](https://pypi.org/project/claudecodeoptimizer/)
[![Claude 4 Best Practices](https://img.shields.io/badge/Claude_4-Best_Practices-blueviolet.svg)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

> Claude already knows how to code. **CCO adds safety, approval, and consistency.**

> **~110 standards active** per project (not 206 - only relevant ones load)

![CCO Environment](docs/screenshots/environment.png)
*CCO lives directly inside Claude Code, no extra UI.*

---

## Quickstart

```bash
pip install claudecodeoptimizer && cco-setup
```

Inside Claude Code:
```
/cco-tune      # Auto-detect your project, confirm once
/cco-health    # See your scores
```

**That's it.** Start coding with safety nets in place.

---

## Why CCO vs Plain Rules?

| Plain Rules (.cursorrules, CLAUDE.md) | CCO |
|---------------------------------------|-----|
| Static text files | Dynamic project detection |
| Load everything always | Only relevant standards load |
| No verification | `Applied: N \| Skipped: N \| Failed: N` |
| Trust the AI completely | Git safety + approval flow + rollback |
| Manual copy-paste setup | `pip install && cco-setup` |
| Tool-specific | Export to AGENTS.md for any AI tool |

---

## Design Principles

- **Transparency** - Announce before action, progress signals, no silent operations
- **User Control** - Approval required, priority levels (CRITICAL→LOW), safe vs risky classification
- **Context-Aware** - Project detection drives thresholds and standards
- **Token Efficient** - Semantic density, bounded context, conditional loading

*[Full principles documentation](docs/design-principles.md)*

---

## What CCO Does

| Layer | What It Adds | Example |
|-------|--------------|---------|
| **Pre-** | Safety checks before action | Git status, impact preview |
| **Process** | Standardized workflows | Approval flow, AI-pattern detection |
| **Post-** | Verification and reporting | Session stats, accounting |
| **Context** | Project-aware behavior | Production readiness, adjusted thresholds |

## What CCO Does NOT Do

| Anti-Pattern | Why Not |
|--------------|---------|
| Teach Claude to code | Opus 4.5 already knows - CCO adds process, not knowledge |
| Replace your judgment | Every change requires your approval |
| Add overhead to simple tasks | Standards are guidance, not blockers |
| Lock you into Claude Code | Export to AGENTS.md anytime |
| Require configuration | Works with sensible defaults after `/cco-tune` |

---

## Requirements

- **Python 3.10+** (tested on 3.10–3.14)
- **Claude Code** CLI or IDE extension
- **Zero Python dependencies** - uses only standard library

---

## Standards Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  ALWAYS ACTIVE (98)           │  PROJECT-SPECIFIC (~10-25)    │
├───────────────────────────────┼────────────────────────────────┤
│  Universal (48)               │  Selected by /cco-tune based   │
│  AI-Specific (31)             │  on what's detected in YOUR    │
│  CCO-Workflow (19)            │  project (9 categories)        │
├───────────────────────────────┴────────────────────────────────┤
│  TYPICAL TOTAL: ~110-125 standards active                      │
│  (from 206 pool - you never load all of them)                  │
└────────────────────────────────────────────────────────────────┘
```

### Base Standards (Always Active)

| Category | Count | Examples |
|----------|-------|----------|
| **Universal** | 48 | DRY, Fail-Fast, Clean Code, Security, Testing |
| **AI-Specific** | 31 | Semantic Density, No Hallucination, Read First |
| **CCO-Workflow** | 19 | Git Safety, Approval Flow, Verification |

### Project-Specific Standards (Conditional)

| Category | Trigger | Standards |
|----------|---------|-----------|
| Security & Compliance | PII/Regulated data OR 10K+ scale | 12 |
| Scale & Architecture | 10K+ OR microservices | 12 |
| Backend Services | API + DB + CI/CD detected | 18 |
| Frontend | React/Vue/Angular/Svelte/etc. | 10 |
| Apps | Mobile + Desktop + CLI | 15 |
| Library | Package/library project | 5 |
| Infrastructure | Containers + Serverless + Monorepo | 13 |
| Specialized | ML/AI + Game Dev | 10 |
| Collaboration | Team 2+ OR i18n | 13 |

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
| `/cco-audit` | Quality gates with AI-pattern detection |
| `/cco-review` | Architecture analysis + production readiness |
| `/cco-optimize` | AI context, docs, code efficiency |
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
{selected from 9 categories based on detection}
<!-- CCO_CONTEXT_END -->
```

---

## Audit Categories

| Flag | What It Checks |
|------|----------------|
| `--security` | OWASP, secrets, CVEs, supply chain |
| `--tech-debt` | Dead code, complexity, duplication |
| `--ai-patterns` | Almost-right logic, hallucinated APIs, over-engineering |
| `--self-compliance` | Code vs project's stated standards |
| `--consistency` | Doc-code mismatches |
| `--tests` | Coverage, isolation, flaky tests |
| `--performance` | Caching, N+1, async issues |
| `--docs` | README, docstrings, API docs |

**Meta-flags:** `--smart` (auto-detect), `--critical`, `--weekly`, `--all`

---

## Safety Features

| Feature | What It Does |
|---------|--------------|
| **Git Safety** | Checks status before changes, enables rollback |
| **Impact Preview** | Shows affected files, dependents, test coverage before apply |
| **Approval Flow** | Priority-based (CRITICAL→LOW), safe vs risky classification |
| **Verification** | `Applied: N \| Skipped: N \| Failed: N` accounting |

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

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
