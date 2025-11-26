# ClaudeCodeOptimizer

**Commands, agents, and rules for Claude Code.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## What is CCO?

CCO extends Claude Code with:
- **7 Commands** - Audit, fix, generate, optimize, commit, status, help
- **2 Agents** - Scan (read-only) and Action (write operations)
- **Rules** - Minimal guidelines (~80 tokens) added to CLAUDE.md

All content is installed globally to `~/.claude/` - zero project pollution.

---

## Installation

```bash
# Install package
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git

# Setup global files
cco-setup
```

**Alternative methods:**

```bash
# With pipx (isolated)
pipx install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup

# With uv (fast)
uv tool install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

**What cco-setup does:**
- Creates `~/.claude/commands/` (7 command files)
- Creates `~/.claude/agents/` (2 agent files)
- Adds CCO Rules to `~/.claude/CLAUDE.md`

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-audit` | Find security, quality, and test issues |
| `/cco-fix` | Auto-fix detected issues |
| `/cco-generate` | Create tests, docs, configs |
| `/cco-optimize` | Improve performance and reduce context |
| `/cco-commit` | Smart git commits |
| `/cco-status` | Check installation health |
| `/cco-help` | Command reference |

**Audit categories:**

| Category | What it checks |
|----------|---------------|
| `--security` | OWASP Top 10, XSS, SQLi, CSRF, secrets, CVEs |
| `--ai-security` | Prompt injection, PII, LLM security |
| `--database` | N+1 queries, missing indexes, connections |
| `--tests` | Coverage, isolation, test pyramid |
| `--tech-debt` | Dead code, complexity, duplication |
| `--performance` | Caching, algorithms, bottlenecks |
| `--docs` | Docstrings, API docs, README |
| `--cicd` | Pipeline, quality gates, deployment |
| `--containers` | Dockerfile, K8s security |
| `--supply-chain` | Dependency CVEs, SBOM |

**Meta-flags:**
- `--critical` = security + ai-security + database + tests
- `--production-ready` = security + performance + database + tests + docs
- `--all` = everything

**Quick start:**

```bash
/cco-audit --critical   # Find critical issues
/cco-fix --security     # Fix security issues
/cco-generate --tests   # Create missing tests
/cco-commit             # Commit changes
```

---

## Agents

| Agent | Purpose |
|-------|---------|
| `cco-agent-scan` | Read-only analysis (audit, detect, report) |
| `cco-agent-action` | Write operations (fix, generate, optimize) |

Agents are invoked automatically by commands.

---

## CCO Rules

Minimal guidelines added to CLAUDE.md (~80 tokens):

- **Paths** - Forward slash, relative, quote spaces
- **Reference Integrity** - Find all refs before delete/rename
- **Verification** - total = done + skip + fail
- **Safety** - Commit first, max 10 files/batch

---

## Verification

```bash
# Terminal
cco-status

# Claude Code
/cco-status
```

---

## Uninstallation

```bash
# Step 1: Remove global files
cco-remove

# Step 2: Uninstall package
pip uninstall claudecodeoptimizer
```

**Important:** Run `cco-remove` before `pip uninstall`.

---

## Requirements

- Python 3.11+
- Claude Code

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
