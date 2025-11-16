# ClaudeCodeOptimizer (CCO)

**AI-powered project configuration for Claude Code. Zero config, instant setup, production-grade standards.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-orange.svg)](https://github.com/sungurerdim/ClaudeCodeOptimizer/releases)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> **⚠️ Alpha Status**: Core architecture complete, comprehensive testing in progress. See [Roadmap](docs/roadmap.md).

---

## Table of Contents

- [What is CCO?](#what-is-cco)
- [Quick Start](#quick-start)
- [What You Get](#what-you-get)
- [Installation](#installation)
- [Key Features](#key-features)
- [How CCO Compares](#how-cco-compares)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## What is CCO?

CCO analyzes your project and automatically configures Claude Code with production-grade development standards.

**In 10 seconds:**
```bash
pip install claudecodeoptimizer
/cco-init  # AI detects your stack → deploys 31-94 principles + 8-15 commands
```

**How it works:** Detects your stack (Python? FastAPI? React?) → Selects applicable principles from 94 standards → Deploys slash commands → Zero pollution (symlinks only).

**Example:** FastAPI security project gets 40 principles (security + architecture). CLI tool gets 25 (code quality + testing). Same CCO, different configuration.

> **See**: [Overview](docs/overview.md) for philosophy, problem/solution, and ideal use cases

---

## Quick Start

### Installation
```bash
# Install globally
pip install claudecodeoptimizer

# Navigate to your project
cd /path/to/your/project

# Initialize (AI auto-detects everything, ~10 seconds)
/cco-init

# Or interactive mode (you approve each decision)
/cco-init --mode=interactive
```

### First Commands
```bash
# Check project health
/cco-status

# Audit code quality, security, tests
/cco-audit

# Auto-fix issues
/cco-fix code
/cco-fix security

# Generate tests or docs
/cco-generate tests

# Semantic commits (AI-powered)
/cco-commit
```

**That's it!** CCO is now guiding all Claude Code interactions in this project.

[→ Full Tutorial](docs/tutorial.md) | [→ Installation Guide](docs/installation.md)

---

## What You Get

After running `/cco-init`, your project has:

### ✅ **Intelligent Principles** (31-94 per project from 94 total)
- **14 Universal** (always): Evidence-based verification, fail-fast errors, test-first development, DRY, atomic commits, minimal touch, change verification
- **10-63 Project-Specific** (AI-selected from 63): Security (17), architecture (8), code quality (8), testing (6), performance (5), API design (2), infrastructure (17)
- **17 Claude Guidelines** (always): No unnecessary files, prefer editing, production-grade code, minimal touch, model selection, token optimization, parallel agents

### ✅ **Slash Commands** (8-15 per project)
| Command | Purpose |
|---------|---------|
| `/cco-audit` | Comprehensive code/security/test audit |
| `/cco-fix` | Auto-fix issues (code, security, docs, tests) |
| `/cco-generate` | Generate code, tests, docs, CI/CD |
| `/cco-commit` | AI-powered semantic commits |
| `/cco-optimize-deps` | Update dependencies, fix vulnerabilities |
| `/cco-scan-secrets` | Detect exposed secrets |
| `/cco-status` | Quick health check |

[→ See All 33 Commands](docs/features.md#slash-commands)

### ✅ **Multi-Agent Orchestration**
CCO automatically uses parallel agents for 2-3x speed:
- **Haiku** for scanning, detection, simple tasks (fast & cheap)
- **Sonnet** for analysis, synthesis, complex reasoning (smart & thorough)

### ✅ **Zero Project Pollution & Zero State**
- All data stored globally (`~/.cco/`) - single source of truth
- Projects only contain symlinks (`.claude/` → `~/.cco/`)
- **No state files, no config, no project registry** - 100% stateless
- Clean uninstall: remove links, project restored to pre-CCO state
- Easy updates: `pip install -U claudecodeoptimizer` updates all projects instantly

[→ Full Feature List](docs/features.md) | [→ Architecture](docs/architecture.md)

---

## Installation

### Requirements
- **Python 3.11+**
- **Claude Code** (required for all features)
- **Git** (recommended for workflow features)

### Quick Install
```bash
# From PyPI (coming soon)
pip install claudecodeoptimizer

# From source (development)
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer
cd ClaudeCodeOptimizer
pip install -e ".[dev]"
```

### What Gets Installed

**Global (`~/.cco/`):**
- 33 slash commands
- 94 principles (14 universal + 63 project-specific + 17 Claude guidelines)
- 5 comprehensive guides
- 23 skills (18 language-specific + 5 cross-language)
- 3 task agents (audit, fix, generate)
- **No state files** - completely stateless

**Global (`~/.claude/commands/`):**
- `/cco-init` - Initialize CCO in any project (auto-detect everything)
- `/cco-remove` - Complete CCO removal (local + global cleanup)

**Project (`.claude/`):**
- Symlinks to selected principles, commands, guides, skills
- `CLAUDE.md` with CCO sections (original content preserved via markers)
- **No CCO-specific files** - only symlinks

[→ Platform-Specific Notes (Windows/Linux/macOS)](docs/installation.md#platform-specific-notes)

---

## Key Features

### 🧙 **Intelligent Project Initialization**
- **Quick Mode**: AI auto-detects everything (~10 seconds)
- **Interactive Mode**: You approve each decision (~2-5 minutes)
- **Clean Install**: Always removes previous CCO setup first
- Detects: Languages, frameworks, tools, team size, maturity level, git history
- Decides: Project type, testing strategy, security level, git workflow
- **100% Stateless**: No config files, no project registry - everything derived from code

### 📚 **Progressive Disclosure System**
- Loads only applicable principles (not all 94)
- Example: Simple CLI tool → 25 principles, FastAPI API → 45 principles
- **80%+ token savings** throughout project lifecycle
- Dynamic loading per command
- **No state tracking** - selection stored as symlinks in `.claude/`

### 🎯 **94 Industry Principles**
| Category | Count | Examples |
|----------|-------|----------|
| Universal | 14 | Evidence-based verification, fail-fast errors, test-first, DRY, atomic commits |
| Claude Guidelines | 17 | Token optimization, parallel agents, minimal touch, prefer editing, production-grade |
| Security & Privacy | 17 | Zero-trust, encryption, secrets management, OWASP, SQL injection prevention |
| Project Infrastructure | 17 | Git workflow, IaC, observability, health checks, CI/CD |
| Code Quality | 8 | Type safety, linting enforcement, immutability, code review |
| Architecture | 8 | Event-driven, microservices, CQRS, dependency injection |
| Testing | 6 | Test pyramid, coverage targets, CI gates, property testing |
| Performance | 5 | Caching, async I/O, database optimization, lazy loading |
| API Design | 2 | RESTful conventions, versioning strategy |

> **See**: [Features → Development Principles](docs/features.md#development-principles) for detailed principle descriptions

### 🎛️ **33 Slash Commands**
Commands grouped by workflow:
- **Core**: init, status, config
- **Audit**: audit, analyze
- **Fix**: fix (code/security/docs/tests), optimize (code/deps/docker)
- **Generate**: generate (code/tests/docs/CI), setup (CI/CD/monitoring)
- **Git**: commit, scan-secrets

> **See**: [Features → Slash Commands](docs/features.md#slash-commands) for complete command list with descriptions

### 🤖 **Multi-Agent Orchestration**
```bash
# Example: Security audit runs 4 parallel agents
Agent 1 (Haiku): Code scanning          → 3s  \
Agent 2 (Haiku): Dependency analysis    → 3s   } Parallel
Agent 3 (Haiku): Secret detection       → 3s  /
Agent 4 (Sonnet): Synthesis & report    → 5s
─────────────────────────────────────────────
Total: ~8s (vs 20s sequential, 60% faster)
```

### 🔄 **Git Workflow Selection**
- **Main-Only**: Solo developers, fast iteration
- **GitHub Flow**: Small/medium teams, PR workflow
- **Git Flow**: Large teams, formal releases

[→ Detailed Feature Documentation](docs/features.md)

---

## How CCO Compares

| Feature | Manual/Linters | Other Tools | CCO |
|---------|----------------|-------------|-----|
| Setup Time | Hours/30-60 min | 10-15 min | **10 seconds** |
| Auto-Detection | None | Partial | **Full stack detection** |
| Standards | Style only | Limited | **94 principles** (quality, security, architecture) |
| AI Integration | None | Basic | **Multi-agent orchestration** |
| Project Pollution | Config files | Varies | **Zero** (symlinks) |
| Claude Code Native | External tools | Plugins | **Built-in** slash commands |

**vs. Alternatives:** CCO adds comprehensive principles (not just style), AI detection, audit/fix/generate workflows, and zero-config init.

> **See**: [Overview](docs/overview.md) for ecosystem positioning and detailed comparison

---

## Documentation

### 📘 **Core Documentation**
- [Overview & Philosophy](docs/overview.md) - Why CCO exists, who should use it
- [Getting Started Tutorial](docs/tutorial.md) - 5 minutes to power user (3 levels)
- [Installation Guide](docs/installation.md) - Platform-specific setup (Windows/Linux/macOS)

### 🔧 **Technical Documentation**
- [Features](docs/features.md) - Detailed feature explanations with examples
- [Architecture](docs/architecture.md) - Design principles, directory structure, source code
- [Project Structure](docs/project-structure.md) - What CCO does to your project, removal guide

### 🗺️ **Project Information**
- [Roadmap](docs/roadmap.md) - Version history, future plans, project goals

### 🔗 **Quick Links**
- **Commands**: See [Features → Slash Commands](docs/features.md#slash-commands)
- **Principles**: See [Features → Development Principles](docs/features.md#development-principles)
- **Troubleshooting**: See [Installation → Troubleshooting](docs/installation.md#troubleshooting)
- **Removal**: See [Project Structure → Removal](docs/project-structure.md#removal)

---

## Contributing

We welcome contributions! Key areas:
- Language-specific skills (Python, TypeScript, Rust, Go)
- Additional slash commands
- Test coverage improvements
- Documentation enhancements

**Repository**: [github.com/sungurerdim/ClaudeCodeOptimizer](https://github.com/sungurerdim/ClaudeCodeOptimizer)

---

## Acknowledgments

**Inspired By:**
- [Superpowers by @obra](https://github.com/obra/superpowers) - Skills system and systematic workflows
- [Agents by @wshobson](https://github.com/wshobson/agents) - Progressive disclosure pattern and document structure

**Built For:**
- [Claude Code](https://claude.com/claude-code) - Anthropic's official CLI for Claude

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sungurerdim/ClaudeCodeOptimizer/discussions)
- **Documentation**: [docs/](docs/)

---

*Built with Claude Code • Designed for Claude Code • Powered by AI*

**Created by Sungur Zahid Erdim**
