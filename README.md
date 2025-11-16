# ClaudeCodeOptimizer

**Configuration manager for Claude Code. Auto-detects your stack, deploys production-grade principles, zero project pollution.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Alpha Status**: Core architecture complete, comprehensive testing in progress. [See Roadmap](docs/roadmap.md)

## What is CCO?

CCO automatically configures Claude Code with production-grade development principles tailored to your project.

**The Challenge**: While Claude Code's `CLAUDE.md` system works well, managing project instructions manually is time-consuming and fragmented. Each project needs hand-written instructions, best practices aren't standardized, and keeping multiple projects consistent requires constant manual updates.

**CCO's Approach**: Instead of writing ad-hoc notes for each project, CCO detects your stack and deploys curated, tested principles from a library of 94 industry standards. A FastAPI security project gets different principles than a CLI tool—same CCO, intelligent adaptation. One global update propagates to all your projects instantly.

## Quick Start

### Installation

```bash
# Install from source (PyPI coming soon)
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer
cd ClaudeCodeOptimizer
pip install -e .

# Navigate to any project
cd /path/to/your/project

# Initialize in 10 seconds
/cco-init
```

### First Commands

```bash
/cco-status              # Health check (git, dependencies, tests, docs)
/cco-audit-code          # Comprehensive quality audit
/cco-fix-code            # Auto-fix detected issues
/cco-generate-tests      # Generate missing tests
```

CCO now guides all Claude Code interactions with project-specific intelligence.

## Features

### Intelligent Configuration

**Auto-Detection:**
- Languages, frameworks, tools (Python/FastAPI/pytest, TypeScript/React/Vitest, etc.)
- Project maturity (MVP vs production-ready)
- Team size (solo vs collaborative)
- Git workflow (main-only, GitHub Flow, Git Flow)
- Testing strategy (unit-heavy, integration-focused, manual)

**Intelligent Deployment:**
- Deploys 30-50 principles tailored to your project (from 94 total)
- 8-15 slash commands based on detected stack
- 3-8 skills (Python async, pytest patterns, type hints, etc.)
- Workflow guides (git, security response, verification protocols)

### 94 Production-Grade Principles

| Category | Count | Examples |
|----------|-------|----------|
| Universal | 14 | Evidence-based verification, fail-fast errors, test-first, DRY, atomic commits |
| Claude Guidelines | 17 | Token optimization, parallel agents, minimal touch, prefer editing |
| Security & Privacy | 17 | Zero-trust, encryption, secrets management, OWASP compliance |
| Infrastructure | 17 | GitOps, IaC, observability, health checks, CI/CD |
| Code Quality | 8 | Type safety, linting enforcement, immutability |
| Architecture | 8 | Event-driven, microservices, CQRS, dependency injection |
| Testing | 6 | Test pyramid, coverage targets, CI gates |
| Performance | 5 | Caching, async I/O, database optimization |
| API Design | 2 | RESTful conventions, versioning |

[See all principles](docs/features.md#development-principles)

### 33 Slash Commands

**Core Workflows:**
- `/cco-status` - Quick health check
- `/cco-audit-code` - Comprehensive quality audit
- `/cco-audit-docs` - Documentation completeness check
- `/cco-fix-code` - Auto-fix code issues
- `/cco-fix-security` - Fix security vulnerabilities
- `/cco-generate-tests` - Generate missing tests
- `/cco-setup-cicd` - Generate CI/CD configs
- `/cco-analyze-dependencies` - Dependency analysis (graph, circular deps, unused)

[See all commands](docs/features.md#slash-commands)

### Zero Pollution Architecture

**Global Storage (`~/.cco/`):**
- 33 commands, 94 principles, 23 skills, 5 guides, 3 agents
- Single source of truth for all projects
- Zero state files (100% stateless)

**Project Storage (`.claude/`):**
- Symlinks only (no actual files)
- `CLAUDE.md` with CCO sections (original content preserved)
- Clean uninstall: remove symlinks, project restored

**Benefits:**
- One update (`pip install -U`) updates all projects instantly
- No config drift between projects
- No version conflicts or stale data
- Zero maintenance overhead

### Multi-Agent Orchestration

```bash
# Example: Security audit uses 4 parallel agents
Agent 1 (Haiku): Code scanning       → 3s  \
Agent 2 (Haiku): Dependency check    → 3s   } Parallel
Agent 3 (Haiku): Secret detection    → 3s  /
Agent 4 (Sonnet): Synthesis          → 5s
───────────────────────────────────────────
Total: ~8s (vs 20s sequential, 60% faster)
```

Automatic model selection:
- **Haiku**: Scanning, detection, simple tasks (fast & cheap)
- **Sonnet**: Analysis, synthesis, complex reasoning (thorough)

## Documentation

- [Overview & Philosophy](docs/overview.md) - Why CCO exists, problem/solution, use cases
- [Tutorial](docs/tutorial.md) - 5-minute walkthrough (beginner → power user)
- [Installation](docs/installation.md) - Platform-specific setup (Windows/Linux/macOS)
- [Features](docs/features.md) - Detailed feature explanations
- [Architecture](docs/architecture.md) - Design principles, directory structure
- [Project Structure](docs/project-structure.md) - What CCO does to your project
- [Roadmap](docs/roadmap.md) - Version history, future plans

## Requirements

- **Python 3.11+**
- **Claude Code** (required)
- **Git** (optional, for workflow features)

## Contributing

Contributions welcome! Priority areas:
- Language-specific skills (TypeScript, Rust, Go)
- Additional slash commands
- Test coverage improvements
- Documentation enhancements

[Open an issue](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues) or submit a PR.

## Acknowledgments

**Inspired by:**
- [Superpowers](https://github.com/obra/superpowers) by @obra - Skills system and systematic workflows
- [Agents](https://github.com/wshobson/agents) by @wshobson - Progressive disclosure pattern

**Built for:**
- [Claude Code](https://claude.com/claude-code) - Anthropic's official CLI

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues) | [Discussions](https://github.com/sungurerdim/ClaudeCodeOptimizer/discussions)
