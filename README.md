# ClaudeCodeOptimizer (CCO)

**Unified AI workflow framework that maximizes Claude Code's effectiveness through intelligent project configuration, multi-agent orchestration, and evidence-based development principles.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-orange.svg)](https://github.com/sungurerdim/ClaudeCodeOptimizer/releases)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> **⚠️ Alpha Status**: Core functionality complete, production readiness in progress (P0.2 completed). See [Roadmap](#roadmap).

---

## Why CCO?

**Problem**: Claude AI models are powerful, but without structure they can be inconsistent and inefficient.

**Solution**: CCO provides a framework that:

🎯 **Enforces Consistency** - 74 development principles across 8 categories
⚡ **Optimizes Performance** - Multi-agent parallelism for 2-3x faster execution
🛡️ **Minimizes Risk** - Evidence-based verification prevents silent failures
💰 **Controls Costs** - Smart model selection + 76% token reduction via progressive disclosure
🔍 **Maximizes Quality** - Auto-detection of 20+ languages, 25+ frameworks, 30+ tools

---

## Quick Start

```bash
# Installation
pip install claudecodeoptimizer

# Quick mode (10 seconds)
python -m claudecodeoptimizer init

# Interactive mode (2-5 minutes)
python -m claudecodeoptimizer init --mode=interactive

# Or in Claude Code
/cco-init
```

**What it creates:**
- `.cco/project.json` - Project configuration
- `PRINCIPLES.md` - Active development principles (~500 tokens, load with `@PRINCIPLES.md`)
- `.claude/commands/` - Slash commands (8-12 commands tailored to your stack)
- `docs/cco/` - Comprehensive documentation system

---

## Core Features

### 🧙 Intelligent Project Initialization

**Two modes, same decision engine:**

**Quick Mode** (~10s):
- AI auto-analyzes your codebase
- Detects: OS, shell, locale, languages, frameworks, tools
- Auto-decides: Project type, team size, maturity, philosophy
- Configures: Principles, commands, security, documentation

**Interactive Mode** (~2-5m):
- **TIER 0**: System detection (automatic)
- **TIER 1**: Fundamental decisions (4 questions)
  - Project purpose, team size, maturity, philosophy
- **TIER 2**: Strategy decisions (4 questions)
  - Principles, testing, security, documentation, git workflow
- **TIER 3**: Tactical decisions (dynamic)
  - Tool preferences, command selection

**Cascading AI hints** - Each answer informs next recommendations.

### 📚 Progressive Disclosure Documentation System

**NEW in P0.2** - Inspired by [wshobson/agents](https://github.com/wshobson/agents)

**Token Optimization** (76% reduction):
- **Before**: ~8500 tokens (all content loaded)
- **After**: ~2000 tokens (core only, load on-demand)

**Structure:**
```
docs/cco/
├── principles/              # 9 files (split by category)
│   ├── core.md             # 3 critical principles (~500 tokens)
│   ├── code-quality.md     # 14 principles
│   ├── security.md         # 19 principles
│   ├── testing.md          # 6 principles
│   ├── architecture.md     # 10 principles
│   ├── performance.md      # 5 principles
│   ├── operations.md       # 10 principles
│   ├── git-workflow.md     # 5 principles
│   └── api-design.md       # 2 principles
│
├── guides/                  # 5 comprehensive guides (on-demand)
│   ├── verification-protocol.md
│   ├── git-workflow.md
│   ├── security-response.md
│   ├── performance-optimization.md
│   └── container-best-practices.md
│
└── skills/                  # Language-specific skills (planned)
    ├── python/
    ├── typescript/
    ├── rust/
    └── go/
```

**Usage:**
```
# Load core principles (always loaded, ~500 tokens)
@PRINCIPLES.md

# Load category-specific principles (on-demand)
@docs/cco/principles/security.md

# Load detailed guides (on-demand)
@docs/cco/guides/performance-optimization.md
```

**Automatic Loading:**
- `/cco-audit code` → loads `code-quality.md`
- `/cco-audit security` → loads `security.md`
- `/cco-test` → loads `testing.md`
- `/cco-optimize` → loads `performance.md`

### 🎯 Development Principles (74 Total)

**8 Categories:**
- **Core** (3): Fail-fast, evidence-based verification, anti-overengineering
- **Code Quality** (14): DRY, type safety, immutability, precision
- **Security** (19): Encryption, zero-trust, secrets management, input validation
- **Testing** (6): Test pyramid, coverage targets, isolation, CI gates
- **Architecture** (10): Event-driven, microservices, separation of concerns
- **Performance** (5): Caching, async I/O, database optimization
- **Operations** (10): IaC, observability, health checks
- **Git Workflow** (5): Commit conventions, branching, versioning
- **API Design** (2): RESTful conventions, error handling

**Smart Selection** based on:
- Project type (API, web app, CLI, library, data pipeline, etc.)
- Primary language (Python, JavaScript, Go, Rust, Java, etc.)
- Team size (solo → enterprise)
- Project maturity (prototype → production)
- Development philosophy (move fast → quality-first)

### ⚡ Multi-Agent Orchestration

**Parallel execution for 2-3x performance boost:**

```bash
# Example: Security audit
Agent 1 (Haiku): Data security scan     → 3s
Agent 2 (Haiku): Architecture audit     → 3s  } Parallel
Agent 3 (Sonnet): Analysis & synthesis  → 5s
─────────────────────────────────────────────
Total: ~8s (vs 15s sequential, 47% faster)
```

**Cost Optimization:**
- **Haiku**: Data gathering (grep, detection, scans) - Fast & cheap
- **Sonnet**: Complex reasoning (analysis, synthesis) - Smarter decisions
- **Opus**: Reserved for extreme complexity (rarely needed)

**Model Enforcement** - All 12+ commands specify Haiku/Sonnet usage explicitly.

### 📊 Report Management System

**NEW in P0.2** - Timestamped report storage:

```
.cco/reports/
├── audit/
│   ├── 2025-11-09-165530-audit.md
│   └── latest-audit.md              # Copy of latest (Windows compat)
├── status/
├── fix/
├── analyze/
└── sync/
```

**Features:**
- Timestamped filenames: `YYYY-MM-DD-HHMMSS-{command}.md`
- Latest tracking: `latest-{command}.md`
- Automatic cleanup: Keep last 10 reports (configurable)
- Report history: `get_report_history(command, limit=10)`

**API:**
```python
from claudecodeoptimizer.core.report_manager import ReportManager

manager = ReportManager()
report_path = manager.save_report("audit", content)
latest = manager.get_latest_report("audit")
history = manager.get_report_history("audit", limit=5)
```

### 🔍 Universal Detection Engine

**Zero-dependency standalone module:**

**Detects:**
- **20+ languages**: Python, JS/TS, Rust, Go, Java, Kotlin, C#, Ruby, PHP, Swift, etc.
- **25+ frameworks**: FastAPI, Django, React, Vue, Next.js, Gin, Actix, Spring, etc.
- **30+ tools**: Docker, K8s, pytest, jest, ruff, eslint, GitHub Actions, etc.

**Confidence-based scoring** with evidence:
```json
{
  "detected_value": "python",
  "confidence": 0.95,
  "evidence": ["24 .py files", "pyproject.toml present"]
}
```

### 🎛️ Slash Commands

**12+ specialized commands** (core + recommended installed):

**Core Commands** (always installed):
- `/cco-init` - Initialize CCO for project
- `/cco-status` - Quick health check
- `/cco-config` - Configuration management

**Audit & Analysis**:
- `/cco-audit` - Comprehensive codebase audit (code, security, tests, docs)
- `/cco-analyze` - Deep project analysis (structure, tech stack, recommendations)

**Fix & Optimize**:
- `/cco-fix` - Auto-fix issues (code, security, docs, tests)
- `/cco-optimize-code` - Remove unused code and imports
- `/cco-optimize-deps` - Update dependencies, fix vulnerabilities
- `/cco-optimize-docker` - Optimize Dockerfiles

**Generate & Sync**:
- `/cco-generate` - Generate code, tests, docs, CI/CD
- `/cco-sync` - Sync files across codebase
- `/cco-scan-secrets` - Scan for exposed secrets

**Optional Commands** (shown but not installed):
- User can enable later: `/cco-config enable <command>`

### 🔄 Git Workflow Selection

**NEW in P0.2** - Customizable per team size:

**Main-Only (Solo)**:
- Single `main` branch
- Direct commits
- Simple, fast, pragmatic

**GitHub Flow (Small Teams)**:
- Feature branches + PRs
- Code review required
- Branch protection

**Git Flow (Large Teams/Production)**:
- `main` + `develop` branches
- Feature/release/hotfix branches
- Formal release process

**Auto-selected** during init based on team size, with option to customize.

---

## Installation

### Requirements

- Python 3.11+
- Claude Code (for slash commands)
- Git (for version control features)

### Install

```bash
# From PyPI (coming soon)
pip install claudecodeoptimizer

# From source
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer
cd ClaudeCodeOptimizer
pip install -e ".[dev]"
```

### Initialize

```bash
# Quick mode (recommended)
python -m claudecodeoptimizer init

# Interactive mode
python -m claudecodeoptimizer init --mode=interactive
```

---

## Architecture

### Project Structure

```
ClaudeCodeOptimizer/
├── claudecodeoptimizer/
│   ├── ai/                    # AI-powered modules
│   │   ├── detection.py       # UniversalDetector (20+ langs, 25+ frameworks)
│   │   ├── command_selection.py  # Smart command recommendation
│   │   └── recommendations.py # Cascading AI hints
│   ├── core/                  # Core functionality
│   │   ├── installer.py       # CCO installation
│   │   ├── principle_selector.py  # Dynamic principle selection
│   │   ├── claude_md_generator.py  # CLAUDE.md generation
│   │   └── report_manager.py # Report management (NEW)
│   ├── wizard/                # Interactive wizard
│   │   ├── orchestrator.py   # Wizard flow control
│   │   ├── decision_tree.py  # 3-tier decision tree
│   │   └── renderer.py        # Terminal UI
│   ├── commands/              # Slash command definitions
│   ├── knowledge/             # Knowledge base
│   │   └── principles.json    # 74 principles database
│   └── schemas/               # Data models
├── docs/cco/                  # CCO documentation (NEW)
│   ├── principles/            # 9 category files
│   └── guides/                # 5 comprehensive guides
├── .github/workflows/         # CI/CD
│   └── security.yml           # Security scanning (FIXED)
└── tests/                     # Test suite
```

### Design Principles

1. **Progressive Disclosure** - Load only what's needed, when needed
2. **Evidence-Based** - Every claim requires proof
3. **Anti-Overengineering** - Simplest solution that works
4. **Cascading Intelligence** - Each decision informs the next
5. **Multi-Agent First** - Parallel execution by default

---

## Roadmap

### ✅ v0.1.0-alpha (Complete)
- Interactive wizard with 3-tier decision tree
- 74 principles across 8 categories
- Universal detection engine
- 12+ slash commands
- Multi-agent orchestration

### ⏳ v0.2.0-alpha (In Progress - 85% Complete)

**P0: Production Readiness**
- ✅ P0.1: Command selection fixes (core + recommended only)
- ✅ P0.1: Model enforcement (Haiku/Sonnet explicit in all commands)
- ✅ P0.1: Git workflow selection (main-only, GitHub Flow, Git Flow)
- ✅ P0.2: Document management system (progressive disclosure)
- ✅ P0.2: Token optimization (76% reduction: 8500 → 2000 tokens)
- ✅ P0.2: Report management system
- ✅ GitHub Actions: Security workflow fixes
- ⏳ P0.3: Progressive disclosure for skills (3-tier loading)
- ⏳ P0.3: Category-based principle loading
- ⏳ P0.0: Smart Git Commit skill (version bump detection)
- ⏳ Testing: 0% → 60% coverage
- ⏳ CI/CD: Automated testing, linting, security scans

**Release Criteria**:
- 60% test coverage
- CI/CD operational
- Zero critical bugs
- Documentation complete

### 📅 v0.3.0-beta (User Experience)
- Enhanced wizard UX
- Command autocomplete
- Better error messages
- Performance optimizations

### 📅 v0.4.0-rc (Extensibility)
- Plugin system
- Custom principle definitions
- Command templates
- Export/import configurations

### 📅 v1.0.0 (Stable Release)
- API stability guarantee
- Production-ready quality
- Comprehensive documentation
- Migration guides

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Key areas:**
- Language-specific skills (Python, TypeScript, Rust, Go)
- Additional slash commands
- Test coverage improvements
- Documentation enhancements

---

## Acknowledgments

**Inspired By**:
- [Superpowers by @obra](https://github.com/obra/superpowers) - Skills system concept and systematic workflow patterns
- [Agents by @wshobson](https://github.com/wshobson/agents) - Progressive disclosure pattern, 3-tier skill loading, language-specific skill organization, document management structure

**Built For**:
- [Claude Code](https://claude.com/claude-code) - Anthropic's official CLI for Claude

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## CCO Project Footprint

**"What does CCO actually do to my project?"**

CCO follows a **zero-pollution philosophy** - your project directory stays clean.

### Project Directory Changes

CCO creates/modifies only these files in your project:

```
your-project/
├── PRINCIPLES.md          # Generated (optional - can gitignore)
├── CLAUDE.md              # Generated (optional - can gitignore)
└── .claude/
    ├── commands/          # Slash commands (symlinked from ~/.cco/commands/)
    │   ├── cco-audit.md
    │   ├── cco-fix.md
    │   ├── cco-generate.md
    │   └── ... (8-12 commands total)
    └── statusline.js      # Project statusline (copied from ~/.cco/)
```

**That's it!** No `.cco/` directory, no hidden files, no pollution.

### Global Storage (~/.cco/)

All CCO data lives in global storage:

```
~/.cco/
├── commands/              # Master command templates
├── knowledge/             # Principles database
├── projects/
│   └── your-project/
│       ├── backups/       # PRINCIPLES.md, CLAUDE.md backups (last 5)
│       ├── reports/       # Audit/analyze/fix reports
│       ├── temp/          # Temporary files
│       ├── changes.json   # Change tracking
│       └── registry.json  # Project configuration
└── statusline.js          # Global statusline template
```

### What Gets Committed to Git?

**By default** (recommended):
- ✅ `.claude/commands/` - Slash commands
- ✅ `.claude/statusline.js` - Statusline
- ✅ `PRINCIPLES.md` - Development principles (team reference)
- ✅ `CLAUDE.md` - Project guide (team reference)

**Optional** (uncomment in `.gitignore` if you prefer):
- ❌ `PRINCIPLES.md` - If you consider it noise
- ❌ `CLAUDE.md` - If you consider it noise

### Removal

CCO is designed for easy removal:

```bash
# Remove CCO from project (keeps global installation)
/cco-remove

# Or manually:
rm -rf .claude/commands/cco-*.md .claude/statusline.js PRINCIPLES.md CLAUDE.md
```

**That's literally everything.** No hidden `.cco/` to hunt down, no scattered config files.

---

## Support

- **Documentation**: [docs/cco/guides/](docs/cco/guides/)
- **Issues**: [GitHub Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sungurerdim/ClaudeCodeOptimizer/discussions)

---

*Built with Claude Code • Optimized for Claude Code • Enhanced by Claude Code*
