# ClaudeCodeOptimizer

A process and standards layer for Claude Code in the Opus 4.5 era.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/claudecodeoptimizer.svg)](https://pypi.org/project/claudecodeoptimizer/)
[![Claude 4 Best Practices](https://img.shields.io/badge/Claude_4-Best_Practices-blueviolet.svg)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

> Claude already knows how to code. **CCO adds safety, approval, and consistency.**

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

## What CCO Does

| Layer | What It Adds | Example |
|-------|--------------|---------|
| **Pre-** | Safety checks before action | Git status, dirty state handling |
| **Process** | Standardized workflows | Approval flow, priority classification |
| **Post-** | Verification and reporting | `Applied: N \| Skipped: N \| Failed: N` |
| **Context** | Project-aware behavior | Scale-adjusted thresholds, stack-specific checks |

## What CCO Does NOT Do

- **Teach Claude to code** - Opus 4.5 already knows
- **Replace your judgment** - Every change requires approval
- **Add overhead** - Standards are guidance, not blockers
- **Lock you in** - Export to AGENTS.md anytime

---

## Standards

CCO uses a 4-category standards system:

| Category | Count | Scope | Export |
|----------|-------|-------|--------|
| **Universal** | 47 | All projects, AI/human agnostic | Both |
| **AI-Specific** | 31 | All AI assistants, model agnostic | Both |
| **CCO-Specific** | 23 | CCO workflow mechanisms | CLAUDE.md only |
| **Project-Specific** | ~15-35 | Selected by /cco-tune from 108 pool | Both |

**Typical active: ~116-136 standards** (only relevant ones load)

### Categories Explained

- **Universal** - Core software principles: DRY, Fail-Fast, Clean Code, Security, Testing
- **AI-Specific** - AI behavior patterns: Read First, No Hallucination, Semantic Density
- **CCO-Specific** - CCO workflow: Approval Flow, Fix Workflow, Safety Classification
- **Project-Specific** - Stack-based: Frontend accessibility, API standards, Container security

*[Full standards documentation](docs/standards.md)*

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-tune` | Project tuning: detection + configuration + export |
| `/cco-health` | Metrics dashboard with actionable next steps |
| `/cco-audit` | Quality gates with prioritized fixes |
| `/cco-review` | Architecture analysis with recommendations |
| `/cco-optimize` | Efficiency improvements (context, docs, code) |
| `/cco-generate` | Convention-following generation |
| `/cco-refactor` | Safe structural changes with rollback |
| `/cco-commit` | Quality-gated atomic commits |

*[Full commands documentation](docs/commands.md)*

---

## Agents

| Agent | Purpose | Mode |
|-------|---------|------|
| **cco-agent-analyze** | Project detection and issue scanning | Read-only |
| **cco-agent-apply** | Execute changes with verification | Write |

*[Full agents documentation](docs/agents.md)*

---

## Project Tuning

`/cco-tune` is the central configuration command:

1. **Detects** your project: stack, type, scale, team size
2. **Selects** relevant Project-Specific standards
3. **Writes** context to `./CLAUDE.md`
4. **Configures** AI settings (thinking tokens, MCP limits)

### Export

```bash
/cco-tune --export
```

- **AGENTS.md** - For other AI tools (Universal + AI-Specific + Project-Specific)
- **CLAUDE.md** - For Claude Code (includes CCO-Specific)

---

## Safety Features

| Feature | What It Does |
|---------|--------------|
| **Git Safety** | Checks status before changes, enables rollback |
| **Approval Flow** | Priority-based (CRITICAL→LOW), safe vs risky classification |
| **Verification** | `Applied: N \| Skipped: N \| Failed: N` accounting |

---

## Requirements

- **Python 3.10+** (tested on 3.10–3.14)
- **Claude Code** CLI or IDE extension
- **Zero Python dependencies** - stdlib only

---

## Installation

```bash
# pip (recommended)
pip install claudecodeoptimizer && cco-setup

# pipx (isolated)
pipx install claudecodeoptimizer && cco-setup

# Development
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git && cco-setup

# Upgrade
pip install -U claudecodeoptimizer && cco-setup
```

## Uninstallation

```bash
cco-remove  # Complete removal with confirmation
```

---

## Design Principles

- **Transparency** - Announce before action, progress signals, no silent operations
- **User Control** - Approval required, priority levels, safe vs risky classification
- **Context-Aware** - Project detection drives thresholds and standards
- **Token Efficient** - Semantic density, conditional loading, bounded context

*[Full principles documentation](docs/design-principles.md)*

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
