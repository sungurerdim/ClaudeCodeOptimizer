# ClaudeCodeOptimizer (CCO)

[![PyPI](https://img.shields.io/pypi/v/claudecodeoptimizer.svg)](https://pypi.org/project/claudecodeoptimizer/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code 2.0+](https://img.shields.io/badge/Claude_Code-2.0+-00A67E.svg)](https://github.com/anthropics/claude-code)

**Safety, quality, and decision layer for Claude Code.**

Same prompts, better outcomes. Fewer errors, fewer rollbacks, more consistent results.

---

## What CCO Does

| Without CCO | With CCO |
|-------------|----------|
| Claude applies generic patterns | Domain-specific best practices for your stack |
| Changes happen without pre-checks | Git status verified, clean state for rollback |
| Silent operations | Full accounting: `Applied: 5 | Failed: 0 | Total: 5` |
| "Add caching somewhere" | "Use TTL + invalidation for this data fetch" |

**CCO is a process layer, not a teaching layer.** Opus 4.5 already knows how to code. CCO adds safety between intent and action.

---

## Install

```bash
pip install claudecodeoptimizer && cco-install
```

**Restart Claude Code** to load the new commands.

<details>
<summary>Alternative installation methods</summary>

```bash
# Isolated (pipx)
pipx install claudecodeoptimizer && cco-install

# Upgrade
pip install -U claudecodeoptimizer && cco-install

# Uninstall
cco-uninstall

# Preview changes before installing
cco-install --dry-run
```

</details>

---

## What Gets Installed

| Component | Location | Purpose |
|-----------|----------|---------|
| 8 commands | `~/.claude/commands/` | `/cco-config`, `/cco-status`, etc. |
| 3 agents | `~/.claude/agents/` | Analyze, Apply, Research |
| 148 rules | `~/.claude/rules/cco/` | Core (87) + AI (61) patterns |
| Statusline | `~/.claude/settings.json` | Project info in Claude Code |

**Your project files are not modified.** CCO only touches `~/.claude/` (global) and `.claude/rules/cco/` (per-project, after `/cco-config`).

---

## Quick Start

### 1. Configure Your Project

```
/cco-config
```

Auto-detects your stack and generates project-specific rules.

### 2. Check Health

```
/cco-status
```

See security, quality, and hygiene scores.

### 3. Fix Issues

```
/cco-optimize
```

Security + quality + hygiene fixes with approval flow.

---

## Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/cco-config` | Project configuration | First time, or when stack changes |
| `/cco-status` | Health dashboard | Start of session |
| `/cco-optimize` | Fix issues | Before PR, after major changes |
| `/cco-review` | Architecture analysis | Before refactoring |
| `/cco-commit` | Quality-gated commit | Every commit |
| `/cco-research` | Multi-source research | "Which library?", "Best practice?" |
| `/cco-preflight` | Pre-release workflow | Before release |
| `/cco-checkup` | Regular maintenance | Weekly or before PR |

See [Commands documentation](docs/commands.md) for flags and examples.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  Your Prompt                                                │
└─────────────────┬───────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  CCO Layer                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Pre-check   │→ │ Analyze     │→ │ Approve (if risky)  │  │
│  │ Git status  │  │ Find issues │  │ Safe = auto-apply   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                           ▼                                 │
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │ Verify      │← │ Apply                               │   │
│  │ Accounting  │  │ Execute with full tracking          │   │
│  └─────────────┘  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Every operation:** Pre-check → Analyze → Approve → Apply → Verify

---

## Safety Model

### Auto-Apply (Safe)

- Remove unused imports
- Parameterize SQL queries
- Move hardcoded secrets to env vars
- Fix lint/format issues
- Add missing type hints

### Require Approval (Risky)

- Auth/CSRF changes
- Database schema changes
- API contract changes
- Delete files
- Rename public APIs

**Rollback:** All changes are made with clean git state. Use `git checkout` to revert.

---

## Rules System

| Category | Count | Location | Loaded |
|----------|-------|----------|--------|
| Core | 87 | `~/.claude/rules/cco/core.md` | Always |
| AI | 61 | `~/.claude/rules/cco/ai.md` | Always |
| Adaptive | 1563 | `.claude/rules/cco/` | Per-project |

**Core rules:** SSOT, DRY, YAGNI, KISS, Fail-Fast, Type-Safe
**AI rules:** Read-First, No-Hallucination, Evidence-Required
**Adaptive:** Stack-specific (Python, TypeScript, React, Docker, etc.)

See [Rules documentation](docs/rules.md) for full reference.

---

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `cco-agent-analyze` | Haiku | Fast read-only analysis |
| `cco-agent-apply` | Opus | Code changes with verification |
| `cco-agent-research` | Haiku | Multi-source research with reliability scoring |

**Why dual models?** Haiku for speed (reads), Opus for accuracy (writes).

See [Agents documentation](docs/agents.md) for details.

---

## Requirements

- Python 3.10+
- Claude Code CLI or IDE extension
- Zero runtime dependencies

---

## Documentation

| Document | Content |
|----------|---------|
| [Getting Started](docs/getting-started.md) | Installation, first 10 minutes, troubleshooting |
| [Commands](docs/commands.md) | All 8 commands with flags and examples |
| [Agents](docs/agents.md) | 3 agents, scopes, when to use |
| [Rules](docs/rules.md) | Full 1711-rule reference |
| [Workflow](docs/workflow.md) | Daily, pre-PR, pre-release workflows |
| [Philosophy](docs/philosophy.md) | Design principles and decisions |

---

## License

MIT — see [LICENSE](LICENSE)

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**
