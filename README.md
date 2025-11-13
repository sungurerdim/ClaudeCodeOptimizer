# ClaudeCodeOptimizer (CCO)

**Unified AI workflow framework that maximizes Claude Code's effectiveness through intelligent project configuration, systematic development principles, and zero-pollution architecture.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-orange.svg)](https://github.com/sungurerdim/ClaudeCodeOptimizer/releases)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> **⚠️ Alpha Status**: Template-based architecture complete, comprehensive testing in progress. See [Roadmap](#roadmap).

---

## Core Philosophy

**CCO's defining characteristic: Every component is project-specific, dynamically evaluated by AI, with zero unnecessary elements.**

Unlike generic linters or static templates, CCO:
- 🎯 **Analyzes your project** - AI reads your code, docs, git history to understand context
- 🤖 **Selects only what's needed** - From 83 principles (14 universal + 69 project-specific), only applicable ones are loaded
- 🔄 **Adapts to your stack** - FastAPI project gets different principles than a CLI tool
- 🧹 **Zero waste** - No unused commands, no irrelevant principles, no boilerplate

**Example**: A security-focused web API gets P025-P043 (security principles) + P015-P024 (architecture), while a simple CLI tool gets just P001-P014 (code quality) + P044-P049 (testing). Same CCO, completely different configuration.

---

## Why CCO?

**Problem**: Claude AI models are powerful, but without systematic guidance they can be inconsistent, produce redundant work, and miss critical industry standards.

**Solution**: CCO provides a framework that:

🎯 **Enforces Consistency** - Comprehensive principles across quality, security, testing, and operations (loaded progressively)
⚡ **Optimizes Performance** - Multi-agent orchestration with smart model selection (Haiku for speed, Sonnet for reasoning)
🛡️ **Minimizes Risk** - Evidence-based verification prevents silent failures and incomplete implementations
💰 **Controls Costs** - Progressive disclosure + granular principle loading for minimal token usage
🔍 **Maximizes Quality** - AI-powered auto-detection of languages, frameworks, tools, and optimal configurations
🧹 **Zero Pollution** - Global storage with local symlinks keeps projects clean

---

## Who Should Use CCO?

**✅ Perfect For:**
- **Solo developers** building new projects (0→1 setup automation in seconds)
- **Small teams (2-5)** wanting consistent standards without CI/CD overhead
- **Open-source maintainers** enforcing contribution quality systematically
- **AI-heavy workflows** where Claude Code is the primary development tool
- **Legacy codebases** needing systematic audits and modernization
- **Learning developers** who want to absorb industry best practices quickly

**⚠️ Consider Alternatives If:**
- Team already has established CI/CD with enforced standards (may overlap)
- Not using Claude Code regularly (CCO is Claude Code-specific)
- Prefer manual control over every configuration decision (CCO automates heavily)
- Enterprise compliance requires custom principle sets (plugin system planned for v0.4.0+)

**Ideal Scenarios:**
1. **New project kickoff:** "I'm starting a FastAPI service, set me up with best practices in 10 seconds"
2. **Code quality rescue:** "This codebase has no tests/docs, help me audit and fix systematically"
3. **Team onboarding:** "New developer needs to understand our standards and workflows immediately"
4. **Commit discipline:** "My git history is chaotic, I need semantic commits and better organization"
5. **Consistency at scale:** "Multiple projects need the same quality standards, enforce globally"

---

## How CCO Compares

**Ecosystem Positioning:**

| Tool | Primary Focus | CCO's Position |
|------|---------------|----------------|
| **[claude-code-agents](https://github.com/wshobson/agents)** | Agent library, progressive disclosure pattern | CCO adds: project configuration, 83 industry principles (14 universal + 69 project-specific), unified command system, semantic commits |
| **[superpowers](https://github.com/obra/superpowers)** | Skill system for Claude | CCO adds: AI detection engine, audit/fix/generate workflows, git integration, zero-config init |
| **Manual .claude/ setup** | DIY configuration files | CCO automates: detection, principle selection, command deployment, template generation, conflict resolution |
| **Generic linters/formatters** | Code style enforcement | CCO adds: AI-powered analysis, cross-file reasoning, semantic understanding, guided fixes |

**CCO's Unique Value Proposition:**
- **Zero → Production in 10 seconds:** AI auto-detects everything, no config files to write
- **Systematic principles:** Comprehensive industry standards enforce quality, security, testing, architecture, operations (not just style)
- **Unified command system:** Specialized commands for complete development lifecycle (audit, fix, optimize, generate, commit)
- **Multi-agent orchestration:** Built-in parallelism (Haiku for speed, Sonnet for reasoning)
- **Zero pollution:** Global storage + local symlinks = clean projects, easy updates

**When CCO Shines:**
- You want **comprehensive** standards, not just code formatting
- You trust AI to **make smart decisions** (detection, selection, recommendations)
- You value **speed** over manual control (Quick mode = 10 seconds)
- You work across **multiple projects** (global storage, consistent standards)

---

## Quick Start

```bash
# Installation (creates global ~/.cco/ structure)
pip install claudecodeoptimizer

# Quick mode (AI auto-detects everything, ~10 seconds)
/cco-init

# Interactive mode (user confirms each decision, ~2-5 minutes)
/cco-init --mode=interactive
```

**What gets created:**

**Global Claude Commands (`~/.claude/commands/`)** - Only 2 commands:
- `cco-init.md` - Initialize CCO for any project
- `cco-remove.md` - Remove CCO from project

**Global CCO Storage (`~/.cco/`)** - Created once during installation:
- `commands/` - 28 specialized commands (deployed from content/commands/)
- `principles/` - Individual principle files with frontmatter (deployed from content/principles/):
  - `U001.md - U012.md` - Universal principles (12 files, auto-included in all projects)
  - `P001.md - P069.md` - Project-specific principles (69 files, AI-selected per project)
- `guides/` - Comprehensive guides (deployed from content/guides/)
- `skills/` - Language-specific skills (deployed from content/skills/)
- `agents/` - Task-specific agent definitions (deployed from content/agents/)
- `templates/` - Template files (deployed from templates/*.template, extensions removed):
  - `settings.json` - Claude Code settings template
  - `statusline.js` - Status line script
  - Other project templates (.editorconfig, .pre-commit-config.yaml, etc.)
- `projects/` - Project registries directory
- `config.json` - Global CCO configuration
- `.installed` - Installation marker

**Project Local (`.claude/`)** - Created during `/cco-init`:
- `project.json` - AI selections, detection results, command overrides (runtime config)
- `principles/` - Links to principles (using preference order):
  - All universal principles (U001-U014, 14 files, always included)
  - Selected project principles (P001-P069, 20-40 files, AI-selected)
- `commands/` - Links to selected commands (8-15 from 28 available)
- `guides/` - Links to relevant guides
- `skills/` - Links to language skills
- `agents/` - Links to task agents (if any)
- `statusline.js` - Link to ~/.cco/templates/statusline.js
- `settings.json` - Copy of ~/.cco/templates/settings.json (always copied, not linked)
- `CLAUDE.md` (in project root) - Minimal guide with principle references

**Project Configuration (`.claude/project.json`)** - Runtime config:
- Detection results (languages, frameworks, tools, team size, maturity, security level)
- Selected principles (universal + project-specific)
- Command overrides (dynamic principle loading per command)
- Selected commands, guides, skills, agents
- Wizard mode used (quick/interactive)
- Initialization timestamp

**Zero pollution philosophy:** All data lives in `~/.cco/`, projects only contain links + minimal config. Global `~/.claude/` has only 2 CCO commands (init/remove).

---

## Getting Started Journey

### 🌱 New to CCO? Follow This Path

**Level 1: First 5 Minutes** (Essential - Start Here)

Get CCO running and see immediate value:

```bash
# 1. Install globally
pip install claudecodeoptimizer

# 2. Navigate to your project
cd /path/to/your/project

# 3. Initialize (AI auto-detects everything)
/cco-init

# 4. Check project health
/cco-status

# 5. Run your first audit
/cco-audit
```

**What you'll have after 5 minutes:**
- ✅ Project configured with principles:
  - Universal principles (U001-U014, 14 always included)
  - Project-specific principles (P001-P069, 20-40 AI-selected)
- ✅ Specialized commands ready to use (8-15 selected from 28 available)
- ✅ `CLAUDE.md` with minimal principle references (existing content preserved)
- ✅ `.claude/project.json` storing AI selections (runtime dynamic loading)
- ✅ First audit report showing code quality, security, and test status

**Typical output:** "Found 12 code quality issues, 3 security concerns, test coverage at 45%"

---

**Level 2: Daily Workflow** (Common Tasks - Use These Regularly)

Once initialized, these commands become your daily tools:

**Fix Issues:**
```bash
/cco-fix code          # Fix code quality issues (unused imports, type hints, etc.)
/cco-fix security      # Fix security vulnerabilities (secrets, input validation, etc.)
/cco-fix docs          # Fix documentation issues (missing docstrings, outdated READMEs)
```

**Optimize & Generate:**
```bash
/cco-optimize-deps     # Update dependencies, fix known vulnerabilities
/cco-optimize-code     # Remove dead code, unused imports, deprecated functions
/cco-generate tests    # Generate test scaffolding for untested modules
/cco-generate docs     # Generate API documentation, README sections
```

**Semantic Commits:**
```bash
/cco-commit            # AI analyzes changes, groups logically, generates commit messages
                       # Preview mode: shows proposed commits, you confirm
```

**What you'll gain from daily usage:**
- ⚡ **Faster development:** Automated fixes save 30-60 minutes/day
- 🐛 **Fewer bugs:** Security and quality issues caught early
- 📝 **Better commits:** Semantic messages improve git history searchability
- 🧹 **Cleaner codebase:** Automated cleanup prevents tech debt accumulation

---

**Level 3: Power Features** (Advanced - When You're Ready)

Unlock full CCO capabilities:

**Multi-Agent Orchestration:**
- CCO automatically uses multiple agents in parallel (2-3x faster)
- Haiku for scanning/detection (fast & cheap)
- Sonnet for analysis/synthesis (smart & thorough)
- You don't configure this - it's built into commands

**Custom Configuration:**
```bash
/cco-init --mode=interactive    # Interactive mode: confirm each detection/decision
/cco-config                     # View/modify project configuration
```

**Advanced Workflows:**
- Git Flow integration (main, develop, feature branches)
- GitHub Flow with PR templates and code review checklists
- Semantic versioning automation
- Multi-project consistency (same standards across repos)

**Report Management:**
- All reports stored in `~/.cco/projects/<project>/reports/`
- Timestamped for history tracking
- Compare audits over time to measure improvement

**What you'll master:**
- 🎯 **Full control:** Customize principles, commands, workflows per project
- 🤝 **Team collaboration:** Consistent standards across team members
- 📊 **Progress tracking:** Measure code quality improvements over time
- 🔄 **Workflow automation:** CI/CD integration, pre-commit hooks, automated audits

---

### 📈 Progression Example

**Week 1:** Use Level 1 commands (init, status, audit) to understand current state
**Week 2:** Add Level 2 to daily workflow (fix, optimize, commit)
**Week 3:** Explore Level 3 for team collaboration and automation

**By Week 4:** CCO is integral to your development process, quality metrics improving measurably.

---

## Core Features

### 🎯 Essential Features (Start Here)

The features you'll use immediately to get value from CCO.

---

#### 🧙 Intelligent Project Initialization

**Two modes, unified decision engine:**

**Quick Mode** (~10s):
- AI auto-analyzes codebase (README, docs, git history, file structure)
- Detects: OS, shell, locale, languages, frameworks, tools, team size, project maturity
- Auto-decides: Project type, testing strategy, security level, git workflow
- Generates: Tailored CLAUDE.md, selected principles/commands/guides/skills/agents

**Interactive Mode** (~2-5m):
- **TIER 0**: System detection (automatic, shown for confirmation)
- **TIER 1**: Fundamental decisions
  - Project purpose, team size, maturity level, development philosophy
- **TIER 2**: Strategy decisions
  - Testing strategy, security level, documentation needs, git workflow
- **TIER 3**: Tactical decisions (dynamic based on TIER 1-2)
  - Specific tools, command selection, framework preferences

**Features:**
- Multi-select support for all applicable questions
- "Other" option available for custom inputs
- Claude Code UI integration (AskUserQuestion tool)
- Cascading recommendations (each answer refines next suggestions)
- Git history analysis for team size and activity patterns

### 📚 Progressive Disclosure System

**Two-tier principle architecture** - Maximum token efficiency + true project-specific loading

**Architecture:**
```
~/.claude/commands/               # Only 2 global CCO commands
├── cco-init.md                  # Initialize CCO
└── cco-remove.md                # Remove CCO

~/.cco/                          # All CCO data (single source of truth)
├── principles/                  # Individual principle files with frontmatter
│   ├── U001.md - U012.md       # Universal principles (12 files)
│   │                            # Always included in every project
│   │                            # Model selection, verification, token optimization, etc.
│   └── P001.md - P069.md       # Project-specific principles (69 files)
│                                # AI-selected per project (typically 20-40 selected)
│                                # Categories: code quality, security, architecture, etc.
├── guides/                      # 5 comprehensive how-to guides
│   ├── verification-protocol.md
│   ├── git-workflow.md
│   ├── security-response.md
│   ├── performance-optimization.md
│   └── container-best-practices.md
├── skills/                      # Language-specific and cross-language skills
│   ├── python/                 # async-patterns, packaging, testing, etc.
│   ├── typescript/             # TypeScript-specific skills
│   ├── rust/                   # Rust-specific skills
│   ├── go/                     # Go-specific skills
│   ├── verification-protocol.md     # Cross-language verification skill
│   ├── root-cause-analysis.md       # Cross-language debugging skill
│   ├── test-first-verification.md   # Cross-language testing skill
│   └── incremental-improvement.md   # Cross-language development skill
├── agents/                      # 3 task-specific agents: audit, fix, generate
└── commands/                    # 28 specialized commands

project/.claude/                 # Project-specific configuration
├── project.json                 # AI selections + runtime config (KEY FILE)
├── principles/                  # Symlinks to selected principles
│   ├── U001.md → ~/.cco/principles/U001.md  # Universal (all)
│   ├── U002.md → ~/.cco/principles/U002.md  # Universal (all)
│   ├── ...
│   ├── P001.md → ~/.cco/principles/P001.md  # Selected
│   ├── P036.md → ~/.cco/principles/P036.md  # Selected
│   └── ...
├── guides/                      # Symlinks to relevant guides
├── skills/                      # Symlinks to language skills
├── agents/                      # Symlinks to task agents
└── commands/                    # Symlinks to selected commands
```

**Dynamic Loading (NEW)**:

Commands read `.claude/project.json` at runtime to load only needed principles:

```json
{
  "selected_principles": {
    "universal": ["U001", "U002", "...", "U012"],
    "code_quality": ["P002", "P003", "P004"],
    "security_privacy": ["P036", "P037", "P038"]
  },
  "command_overrides": {
    "cco-audit-security": {
      "principles": ["U001", "P036", "P037", "P038"],
      "reason": "Standard API security - core validations only"
    }
  }
}
```

**CLAUDE.md Format (Minimal)**:
```markdown
# Project Name

<!-- CCO_START -->
## Development Principles & Guidelines

Follow the principles in `.claude/principles/`:
- Universal principles (U001-U014): Apply to all projects
- Project-specific principles (P001-P069): Selected for this project

<!-- CCO_END -->
```

**Token Efficiency:**
- **Init time**: AI selects only needed principles (e.g., 32 out of 74)
- **Runtime**: Commands load only selected principles (no waste)
- **Example**: `/cco-audit-security` on simple CLI tool → loads 4 principles (U001 + 3 security), not all 19
- **Result**: 80%+ token optimization maintained throughout lifecycle

---

#### 🎯 Development Principles

**Two-Tier Architecture:**

**Universal Principles (U001-U0XX, ~12 files)**:
- Always included in every project
- Model selection strategy (Haiku/Sonnet/Opus)
- Evidence-based verification protocol
- Token optimization techniques
- Complete action reporting
- Test-first development
- Root cause analysis
- Minimal touch policy
- Cross-platform bash commands
- Git workflow (atomic commits, semantic versioning)
- No overengineering
- Fail-fast error handling

**Project-Specific Principles (P001-P069, 69 files, AI-selected)**:
- **API Design** (2): RESTful conventions, error handling
- **Architecture** (10): Event-driven, microservices, separation of concerns, SOLID principles
- **Code Quality** (14): DRY, type safety, immutability, precision, documentation
- **Git Workflow** (8): Branch strategy, code review, PR templates
- **Operations** (10): IaC, observability, health checks, deployment automation
- **Performance** (5): Caching, async I/O, database optimization, profiling
- **Security & Privacy** (19): Encryption, zero-trust, secrets management, input validation, OWASP
- **Testing** (6): Test pyramid, coverage targets, isolation, CI gates

**Smart Selection Algorithm:**
- **Project type**: API, web app, CLI, library, data pipeline, embedded, ML/AI, mobile
- **Languages**: Python, JavaScript/TypeScript, Go, Rust, Java, Kotlin, C#, Ruby, PHP, Swift
- **Frameworks**: FastAPI, Django, React, Vue, Next.js, Gin, Actix, Spring, .NET
- **Team size**: Solo (1), Small (2-5), Medium (6-20), Large (21-50), Enterprise (50+)
- **Maturity**: Prototype, MVP, Beta, Production, Legacy
- **Philosophy**: Move fast, Balanced, Quality-first
- **Security level**: Basic, Standard, Strict, Paranoid
- **Stack characteristics**: Detected tools, test frameworks, CI/CD systems

**Result**:
- All universal principles (U001-U0XX) symlinked automatically
- Only applicable project principles (typically 20-40 from 74) symlinked
- Selections saved to `.claude/project.json` for runtime dynamic loading

---

#### 🔍 Universal Detection Engine

**Zero-dependency standalone module:**

**Detects:**
- **Languages**: Python, JS/TS, Rust, Go, Java, Kotlin, C#, Ruby, PHP, Swift, and more
- **Frameworks**: FastAPI, Django, React, Vue, Next.js, Gin, Actix, Spring, and more
- **Tools**: Docker, K8s, pytest, jest, ruff, eslint, GitHub Actions, and more

**Confidence-based scoring** with evidence:
```json
{
  "detected_value": "python",
  "confidence": 0.95,
  "evidence": ["24 .py files", "pyproject.toml present"]
}
```

---

### ⚡ Intermediate Features (Daily Use)

Features you'll use regularly after initial setup.

---

#### 🎛️ Slash Commands

**28 specialized commands for complete development lifecycle:**

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

**Generate & Sync**:
- `/cco-generate` - Generate code, tests, docs, CI/CD
- `/cco-sync` - Sync files across codebase
- `/cco-scan-secrets` - Scan for exposed secrets

**Optional Commands** (shown but not installed):
- User can enable later: `/cco-config enable <command>`

---

#### 🤖 Intelligent Commit System

**Sonnet-powered semantic analysis for high-quality commits**

**How It Works:**
1. Analyzes all changed files with AI (not just file paths)
2. Groups logically related changes (semantic, not directory-based)
3. Generates conventional commit messages
4. Follows git workflow principles (concise, atomic, semantic versioning)

**Features:**
- Multi-file semantic grouping
- Conventional commit format
- Safety checks (secrets, temp files, test execution)
- Preview mode with approval
- Auto-mode for batch commits
- Push support

**Usage:**
```bash
/cco-commit              # Interactive with preview
/cco-commit --auto       # Auto-commit without preview
/cco-commit --dry-run    # Show what would be committed
/cco-commit --push       # Commit and push
```

**Quality Impact:**
- Before: 10+ scattered commits with generic messages
- After: 2-3 logical commits with descriptive, searchable messages

---

#### 🔄 Git Workflow Selection

**Tailored to team size and project maturity:**

**Main-Only (Solo/Prototypes)**:
- Single `main` branch
- Direct commits
- Fast iteration

**GitHub Flow (Small/Medium Teams)**:
- `main` + feature branches
- Pull request workflow
- Code review gates

**Git Flow (Large Teams/Production)**:
- `main` + `develop` + release branches
- Feature/hotfix branch types
- Formal release process

**Selection Logic:**
- Auto-recommended based on team size detection (git history analysis)
- Interactive mode allows user override
- CLAUDE.md generated with workflow-specific guidance

---

### 🚀 Advanced Features (Power Users)

Features for optimization, automation, and team collaboration.

---

#### ⚡ Multi-Agent Orchestration

**Strategic model selection for optimal performance and cost:**

```bash
# Example: Security audit
Agent 1 (Haiku): Code scanning          → 3s
Agent 2 (Haiku): Dependency analysis    → 3s  } Parallel
Agent 3 (Haiku): Secret detection       → 3s
Agent 4 (Sonnet): Synthesis & report    → 5s
─────────────────────────────────────────────
Total: ~8s (vs 20s sequential, 60% faster)
```

**Model Selection Strategy:**
- **Haiku**: Data gathering, pattern matching, scanning, simple transformations
  - Examples: `grep`, file detection, secret scanning, dependency checks
- **Sonnet**: Analysis, decision-making, complex reasoning, synthesis
  - Examples: Architecture analysis, recommendation generation, code review
- **Opus**: Avoided (unnecessary cost for most tasks)

**Enforcement:**
- All commands explicitly specify model in frontmatter
- Commands auto-load relevant principles/guides for their agents
- Agents launched in parallel whenever possible (single message, multiple Task calls)

---

#### 📊 Project Registry System

**Global project tracking** - `~/.cco/projects/<project-name>.json`

**Registry Contents:**
```json
{
  "project_name": "MyProject",
  "project_root": "/absolute/path/to/project",
  "initialized_at": "2025-11-12T10:30:00Z",
  "wizard_mode": "quick",
  "detection_results": { ... },
  "selected_principles": ["code_quality.md", "security_privacy.md", ...],
  "selected_commands": ["cco-audit", "cco-status", ...],
  "selected_guides": ["verification-protocol.md", ...],
  "selected_skills": ["python/testing-pytest.md", ...],
  "selected_agents": [],
  "settings": {
    "backup_retention": 5,
    "report_retention": 10
  }
}
```

**Benefits:**
- Project directory stays clean (zero CCO-specific files)
- Centralized configuration management
- Easy project discovery and tracking
- Backup and report history management
- Migration support between systems

---

## Installation

### Requirements

- **Python 3.11+** - Core runtime
- **Claude Code** - Required for all features (commands, UI, agents)
- **Git** - Recommended for workflow features and history analysis

### Global Installation

```bash
# From PyPI (coming soon)
pip install claudecodeoptimizer

# From source (development)
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer
cd ClaudeCodeOptimizer
pip install -e ".[dev]"
```

**What happens during installation:**
1. Installs Python package from PyPI
2. Deploys knowledge base from `content/` to `~/.cco/`:
   - `commands/` - 28 command files (from content/commands/)
   - `principles/` - 74 principle files (from content/principles/)
   - `guides/` - Comprehensive guides (from content/guides/)
   - `skills/` - Language-specific skills (from content/skills/)
   - `agents/` - Task-specific agents (from content/agents/)
   - `templates/` - Deployed template files (from templates/*.template, extensions removed):
     - `CLAUDE.md` (from CLAUDE.md.template)
     - `settings.json` (from settings.json.template)
     - `statusline.js` (from statusline.js.template)
     - Other project templates (editorconfig, pre-commit, etc.)
   - `projects/` - Project registry directory (empty initially)
3. Creates `config.json` with global configuration
4. Creates `.installed` marker file
5. Adds `/cco-init` and `/cco-remove` to global `~/.claude/commands/`
6. CCO now available in **all Claude Code sessions**

### Project Initialization

**From within any Claude Code session:**

```bash
# Quick mode (AI auto-detects, 10 seconds)
/cco-init

# Interactive mode (user confirms each decision, 2-5 minutes)
/cco-init --mode=interactive
```

**What happens during initialization:**

**Phase 1: Analysis & Detection**
1. Reads project files (README, existing CLAUDE.md, package files, config files)
2. Analyzes git history (if available) for team size and activity patterns
3. Detects system context (OS, shell, locale)
4. Detects project characteristics:
   - Languages (Python, JavaScript/TypeScript, Go, Rust, etc.)
   - Frameworks (FastAPI, Django, React, Next.js, etc.)
   - Tools (Docker, pytest, eslint, GitHub Actions, etc.)
   - Project type (API, web app, CLI, library, etc.)
   - Team size (solo, small, medium, large, enterprise)
   - Maturity level (prototype, MVP, beta, production, legacy)

**Phase 2: Decision & Selection** (Interactive mode: user confirms; Quick mode: auto-decided)
5. Determines development philosophy (move fast, balanced, quality-first)
6. Selects testing strategy (basic, standard, comprehensive)
7. Selects security level (basic, standard, strict, paranoid)
8. Selects git workflow (main-only, GitHub Flow, Git Flow)
9. Selects documentation level (minimal, standard, comprehensive)
10. Chooses applicable principles from 83 total (typically 30-50 selected)
11. Chooses relevant commands from 28 available (typically 8-15 selected)
12. Chooses relevant guides (verification, security, performance, etc.)
13. Chooses language-specific skills based on detected languages

**Phase 3: File Generation**
14. Creates `.claude/` directory structure using preference order (symlink → hardlink → copy):
    - `.claude/project.json` - AI selections + runtime config (NEW)
    - `.claude/principles/` - Links to principles:
      - All universal principles (U001-U014, 14 files, always)
      - Selected project principles (P001-P069, 20-40 files, AI-selected)
    - `.claude/commands/` - Links to selected global commands (8-15 from 28 available)
    - `.claude/guides/` - Links to relevant guides
    - `.claude/skills/` - Links to language skills
    - `.claude/agents/` - Links to task agents (if any)
    - `.claude/statusline.js` - Link to ~/.cco/templates/statusline.js
15. Generates/updates `CLAUDE.md`:
    - If no existing CLAUDE.md: Creates minimal guide with principle references
    - If existing CLAUDE.md: Appends CCO section (preserves existing content)
    - No user approval needed (append-only, uninstall-safe)
16. Optionally copies `settings.json` from ~/.cco/templates/settings.json (always copied, not linked)
17. Updates `.gitignore` to exclude CCO-generated temp files (if applicable)

**Phase 4: Registration**
18. Creates project registry at `~/.cco/projects/<project-name>.json` with:
    - Detection results
    - Selected principles (universal + project-specific), commands, guides, skills
    - Command overrides (for dynamic loading)
    - Wizard mode used
    - Initialization timestamp
19. Displays completion summary with next steps

---

## Platform Notes

### 🪟 Windows

**Linking Strategy:**

CCO uses a **preference order** (not fallback) when creating links from global to local:

1. **Symlink** (preferred) - Auto-updates, zero duplication
2. **Hardlink** (good) - Same disk only, zero duplication
3. **Copy** (works everywhere) - Some duplication

**✅ Recommended Setup:**
1. **Use WSL2** (Windows Subsystem for Linux) for best experience:
   ```bash
   # Install WSL2 (PowerShell as Admin)
   wsl --install

   # Install Ubuntu
   wsl --install -d Ubuntu

   # Use CCO inside WSL
   cd /mnt/d/GitHub/YourProject
   pip install claudecodeoptimizer
   /cco-init
   ```

2. **Native Windows with Developer Mode:**
   - Open Settings → Update & Security → For Developers
   - Enable "Developer Mode"
   - Restart if prompted
   - CCO can now create symlinks

**How Preference Order Works:**
- CCO tries symlink first (optimal)
- If OS doesn't support, tries hardlink (good)
- If hardlink fails (network drives), uses copy (works everywhere)
- This is systematic preference, not error recovery
- All methods work correctly, symlink just provides auto-updates

**Path Handling:**
- CCO handles Windows paths correctly (`D:\GitHub\project`)
- Forward slashes work in git commands (git handles conversion)
- No manual path conversion needed
- Works with spaces in paths

**Known Limitations:**
- **Network drives:** Symlinks often fail, fallback to copies
- **OneDrive/Dropbox:** May not sync symlinks correctly
- **Antivirus:** Some AV software blocks symlink creation (whitelist `~/.cco/`)

---

### 🍎 macOS / 🐧 Linux

**No Special Setup Required:**
- Full symlink support out of the box
- Optimal performance (zero duplication)
- No permissions issues
- Recommended for development

**Installation:**
```bash
pip install claudecodeoptimizer
/cco-init
```

**Storage Location:**
- Global: `~/.cco/` (e.g., `/Users/username/.cco/` or `/home/username/.cco/`)
- Project: `.claude/` (symlinks to global)

---

### 🌐 Network Drives & Cloud Storage

**Network Drives (NAS, SMB, NFS):**
- ⚠️ Symlinks may not work (depends on filesystem and permissions)
- CCO automatically falls back to hardlinks or copies
- Performance may be slower due to network latency
- **Recommendation:** Use local drive for `~/.cco/`, projects can be on network

**Cloud Storage (OneDrive, Dropbox, Google Drive):**
- ⚠️ Symlinks may not sync correctly between devices
- **Recommendation:**
  - Keep `~/.cco/` local (not in cloud folder)
  - Projects in cloud folders work fine (symlinks point to local `~/.cco/`)
  - Each device runs its own `/cco-init` to create local symlinks

---

### 🔧 Troubleshooting

**"Permission denied" creating symlinks (Windows):**
```bash
# Solution 1: Enable Developer Mode (see Windows section above)
# Solution 2: Run terminal as Administrator (one time)
# Solution 3: Use WSL2 (recommended)
```

**Symlinks showing as text files:**
```bash
# Check if symlink creation succeeded
ls -la .claude/commands/  # Should show -> arrows

# If not, CCO fell back to copies (still works, minor duplication)
```

**CCO commands not found:**
```bash
# Ensure global commands installed
ls ~/.claude/commands/cco-*

# If missing, reinstall
pip install --force-reinstall claudecodeoptimizer
```

---

## Architecture

### Core Design Principles

1. **Zero Pollution** - Global storage with local links, no project-specific CCO files
2. **Single Source of Truth** - All knowledge in `content/` (repo), deployed to `~/.cco/` (global), projects reference via links
3. **Progressive Disclosure** - Load only applicable principles/guides, not entire knowledge base
4. **Dynamic Loading** - Commands read `.claude/project.json` at runtime for project-specific principle loading
5. **Two-Tier Principles** - Universal (U001-U014, always) + Project-specific (P001-P069, AI-selected)
6. **Minimal CLAUDE.md** - Reference-based, not template-driven; existing content preserved
7. **Evidence-Based** - AI detection with confidence scores and evidence trails
8. **Anti-Overengineering** - Simplest solution that works, no premature abstraction
9. **Multi-Agent First** - Parallel execution by default (Haiku for speed, Sonnet for reasoning)
10. **Linking Preference Order** - Try symlink → hardlink → copy (systematic preference, not fallback)
11. **Uninstall Safety** - Broken references ignored by Claude, no errors after CCO removal
12. **Document Consistency** - All documentation validated for internal consistency and efficiency
13. **No Version Tracking** - Only project version tracked, no versioning for principles/commands/guides
14. **No Dead Code** - Zero dead code, placeholders, fallbacks, or backward compatibility layers; always 100% current

### Linking Strategy

**Preference Order (Not Fallback)**

CCO uses a systematic preference order when creating links from global to local:

1. **Symlink** (preferred) - Auto-updates when global files change, zero duplication
2. **Hardlink** (good) - Same disk only, zero duplication, requires manual update
3. **Copy** (works everywhere) - Some duplication, requires manual update

This is a **preference order**, not a fallback. CCO tries each method until finding one the OS supports. The strategy applies universally to all file types: commands, principles, guides, skills, agents, and templates.

**Platform Support:**
- **macOS/Linux**: Full symlink support (optimal)
- **Windows**: Symlinks with Developer Mode, hardlinks otherwise
- **Windows WSL2**: Full symlink support (recommended)
- **Network drives**: Usually falls back to copy

### Directory Structure

**Repository (`content/`):**
```
content/                   # Single source of truth (tracked in git)
├── commands/             # 28 command source files (*.md)
├── principles/           # Principle source files (*.md with frontmatter)
│   ├── U001.md - U012.md    # Universal principles (12 files)
│   └── P001.md - P069.md    # Project-specific principles (69 files)
├── guides/               # Comprehensive guide source files (*.md)
├── skills/               # Language-specific and cross-language skill source files
│   ├── python/          # async-patterns, packaging, testing, type-hints, performance
│   ├── typescript/      # TypeScript-specific skills
│   ├── rust/            # Rust-specific skills
│   ├── go/              # Go-specific skills
│   ├── verification-protocol.md      # Cross-language verification skill
│   ├── root-cause-analysis.md        # Cross-language debugging skill
│   ├── test-first-verification.md    # Cross-language testing skill
│   └── incremental-improvement.md    # Cross-language development skill
└── agents/               # Task-specific agent source files
```

**Global Claude Commands (`~/.claude/commands/`):**
```
~/.claude/commands/       # Only 2 CCO commands
├── cco-init.md          # Initialize CCO for any project
└── cco-remove.md        # Remove CCO from project
```

**Global CCO Storage (`~/.cco/`):**
```
~/.cco/                   # Deployed from content/ during pip install
├── commands/             # 28 commands (deployed from content/commands/)
├── principles/           # Individual principle files with frontmatter (deployed from content/principles/)
│   ├── U001.md - U012.md    # Universal principles (12 files)
│   └── P001.md - P069.md    # Project-specific principles (69 files)
├── guides/               # 5 comprehensive guides (deployed from content/guides/)
├── skills/               # Language-specific and cross-language skills (deployed from content/skills/)
│   ├── python/          # Python-specific skills
│   ├── typescript/      # TypeScript-specific skills
│   ├── rust/            # Rust-specific skills
│   ├── go/              # Go-specific skills
│   ├── verification-protocol.md      # Cross-language verification skill
│   ├── root-cause-analysis.md        # Cross-language debugging skill
│   ├── test-first-verification.md    # Cross-language testing skill
│   └── incremental-improvement.md    # Cross-language development skill
├── agents/               # Task-specific agents (deployed from content/agents/)
├── templates/            # Template files (deployed from templates/*.template)
│   ├── settings.json    # Deployed from settings.json.template (extension removed)
│   ├── statusline.js    # Deployed from statusline.js.template (extension removed)
│   └── *.template files for projects (editorconfig, pre-commit, etc.)
├── projects/             # Project registries (<project>.json)
├── config.json           # Global CCO configuration
└── .installed            # Installation marker
```

**Project Structure (`.claude/`):**
```
project/.claude/          # Linked from global (using preference order)
├── project.json         # AI selections + runtime config (KEY FILE)
├── principles/          # Links to selected principles
│   ├── U001.md → ~/.cco/principles/U001.md (universal, always)
│   ├── U002.md → ~/.cco/principles/U002.md (universal, always)
│   ├── ...
│   ├── P001.md → ~/.cco/principles/P001.md (selected)
│   ├── P036.md → ~/.cco/principles/P036.md (selected)
│   └── ... (20-40 selected from 74)
├── commands/            # Links to selected global commands
│   ├── cco-audit.md → ~/.cco/commands/audit.md
│   └── ... (8-15 selected commands)
├── guides/              # Links to relevant guides
│   └── verification-protocol.md → ~/.cco/guides/verification-protocol.md
├── skills/              # Links to language skills
│   └── python/
│       └── testing-pytest.md → ~/.cco/skills/python/testing-pytest.md
├── agents/              # Links to task agents (if any)
├── statusline.js → ~/.cco/templates/statusline.js
└── settings.json        # Copy of ~/.cco/templates/settings.json (not linked)

project/CLAUDE.md        # Minimal guide with principle references
```

**Key Points:**
- All links use preference order (symlink → hardlink → copy)
- Universal principles (U001-U014) always linked to every project
- Project principles (P001-P069) only selected ones linked (AI-selected)
- `.claude/project.json` stores AI selections for runtime dynamic loading
- `settings.json` is always copied (not linked) to allow project-specific customization
- `statusline.js` is linked for auto-updates when CCO is upgraded
- `CLAUDE.md` is minimal with references, not template-based (existing content preserved)

**Source Code:**
```
ClaudeCodeOptimizer/
├── claudecodeoptimizer/
│   ├── ai/                    # AI-powered detection & recommendations
│   │   ├── detection.py       # UniversalDetector (languages, frameworks, tools)
│   │   ├── command_selection.py  # Smart command selection
│   │   └── recommendations.py # Cascading decision recommendations
│   ├── core/                  # Core installation & generation logic
│   │   ├── installer.py       # Global CCO installation
│   │   ├── knowledge_setup.py # Knowledge base deployment
│   │   ├── claude_md_generator.py  # Template-based CLAUDE.md generation
│   │   ├── principle_selector.py   # Dynamic principle selection
│   │   ├── linking.py         # Symlink/hardlink/copy management
│   │   ├── config.py          # Central configuration (paths, branding)
│   │   └── constants.py       # System constants
│   ├── wizard/                # Interactive initialization
│   │   ├── orchestrator.py   # Wizard flow (quick/interactive)
│   │   ├── decision_tree.py  # 3-tier decision tree
│   │   ├── system_detection.py   # OS/shell/locale detection
│   │   ├── ui_adapter.py     # Claude Code UI integration
│   │   └── renderer.py        # Terminal UI fallback
│   ├── schemas/               # Data models (Pydantic)
│   │   └── project_config.py  # Project configuration schema
│   └── install_hook.py        # Post-install hook for pip install
└── tests/                     # Test suite (in progress)
```

---

## Roadmap

### ✅ v0.1.0-alpha (Complete)
- Interactive wizard with 3-tier decision tree
- 83 principles (14 universal + 69 project-specific) across 9 categories
- Universal detection engine
- 28 slash commands
- Multi-agent orchestration

### ⏳ v0.2.0-alpha (In Progress - 95% Complete)

**P0: Production Readiness**
- ✅ P0.1: ALL TASKS COMPLETE
  - ✅ Export/import removal (cleaner workflow)
  - ✅ Command selection fixes (core + recommended only)
  - ✅ Model enforcement (Haiku/Sonnet explicit in all commands)
  - ✅ Git workflow selection (main-only, GitHub Flow, Git Flow)
- ✅ P0.2: DOCUMENT MANAGEMENT COMPLETE
  - ✅ Progressive disclosure system (docs/cco/)
  - ✅ Token optimization (76% reduction: 8500 → 2000 tokens)
  - ✅ Report management system with Windows compatibility
  - ✅ Principles split by category (9 files)
  - ✅ On-demand guides (5 comprehensive guides)
- ✅ P0.3: PRINCIPLE LOADING REFACTOR COMPLETE
  - ✅ Single Source of Truth (SSOT): .md files with frontmatter (principles.json removed)
  - ✅ Universal principles system (U001-U014) always active
  - ✅ python-frontmatter library integration for metadata parsing
  - ✅ principle_md_loader module for unified loading
  - ✅ 6 core files refactored (principles.py, loader, selector, generator, orchestrator)
  - ✅ Template updates (CLAUDE.md.template, settings.json.template, statusline.js.template)
  - ✅ Statusline enhancements (semantic colors, cross-platform compatibility)
- ✅ GitHub Actions: Security workflow fixes
- ✅ Code Quality: All ruff checks passed (F841, S110 fixed)
- ✅ Error Handling: P001 violations fixed (14 try-except-pass instances)
- ✅ Type Safety: All type annotations complete (ANN checks passed)
- ✅ Backup Management: /cco-remove backup notification
- ⏳ P0.4: Progressive disclosure for skills (3-tier loading)
- ⏳ P0.5: Smart Git Commit skill (universal, works in any project)
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
- Advanced workflow customization

### 📅 v1.0.0 (Stable Release)
- API stability guarantee
- Production-ready quality
- Comprehensive documentation
- Migration guides

---

## Contributing

We welcome contributions!

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

CCO follows a **zero-pollution philosophy** - all data lives in global storage, projects only contain symlinks.

### Project Directory Changes

CCO creates only `.claude/` directory with links (using preference order):

```
your-project/
├── CLAUDE.md              # Minimal guide with principle references
└── .claude/
    ├── project.json       # AI selections + runtime config (KEY FILE)
    ├── principles/        # Links to ~/.cco/principles/
    │   ├── U001.md → ~/.cco/principles/U001.md (universal, always)
    │   ├── U002.md → ~/.cco/principles/U002.md (universal, always)
    │   ├── ...
    │   ├── P001.md → ~/.cco/principles/P001.md (selected)
    │   ├── P036.md → ~/.cco/principles/P036.md (selected)
    │   └── ... (20-40 selected from 74)
    ├── commands/          # Links to ~/.cco/commands/ (symlink/hardlink/copy)
    │   ├── cco-audit.md → ~/.cco/commands/audit.md
    │   ├── cco-status.md → ~/.cco/commands/status.md
    │   ├── cco-fix.md → ~/.cco/commands/fix.md
    │   └── ... (8-15 selected commands)
    ├── guides/            # Links to ~/.cco/guides/
    │   └── verification-protocol.md → ~/.cco/guides/verification-protocol.md
    ├── skills/            # Links to ~/.cco/skills/
    │   └── python/
    │       └── testing-pytest.md → ~/.cco/skills/python/testing-pytest.md
    ├── agents/            # Links to ~/.cco/agents/ (if any)
    ├── statusline.js → ~/.cco/templates/statusline.js
    └── settings.json      # Copy (not link) of ~/.cco/templates/settings.json
```

**That's it!**
- No `.cco/` directory in project root
- Minimal duplication (only settings.json copied)
- Dynamic loading via project.json
- Global `~/.claude/` has only 2 CCO commands (init/remove)
- Zero pollution philosophy maintained

### Global Storage (`~/.cco/`)

All actual data lives here (deployed from repository during installation):

```
~/.cco/
├── commands/              # 28 commands (deployed from content/commands/)
├── principles/            # Individual principle files with frontmatter (deployed from content/principles/)
│   ├── U001.md - U012.md     # Universal principles (12 files)
│   └── P001.md - P069.md     # Project-specific principles (69 files)
├── guides/                # 5 comprehensive guides (deployed from content/guides/)
├── skills/                # Language-specific and cross-language skills (deployed from content/skills/)
│   ├── python/           # Python-specific skills
│   ├── typescript/       # TypeScript-specific skills
│   ├── rust/             # Rust-specific skills
│   ├── go/               # Go-specific skills
│   ├── verification-protocol.md      # Cross-language verification skill
│   ├── root-cause-analysis.md        # Cross-language debugging skill
│   ├── test-first-verification.md    # Cross-language testing skill
│   └── incremental-improvement.md    # Cross-language development skill
├── agents/                # 3 task-specific agents: audit, fix, generate (deployed from content/agents/)
├── templates/             # Templates (deployed from templates/*.template, extensions removed)
│   ├── settings.json     # From settings.json.template
│   ├── statusline.js     # From statusline.js.template
│   └── ... (other project templates)
├── projects/              # Project registries
│   └── MyProject.json    # Configuration, detection results, selections, command overrides
├── config.json            # Global CCO configuration
└── .installed             # Installation marker
```

### What Gets Committed to Git?

**Recommended** (team collaboration):
- ✅ `.claude/project.json` - Runtime config (team uses same AI selections)
- ✅ `.claude/commands/` - Links (team sees which commands are active)
- ✅ `.claude/principles/` - Links (team follows same principles: U*.md + selected P*.md)
- ✅ `.claude/guides/` - Links (team uses same guides)
- ✅ `.claude/skills/` - Links (team uses same skills)
- ✅ `.claude/statusline.js` - Link (team uses same statusline)
- ✅ `CLAUDE.md` - Project guide (team reference)
- ✅ `.claude/settings.json` - Optional (shared permissions)

**Why commit links + project.json?**
- Team members see which principles/commands are active
- Everyone runs `/cco-init` and `pip install claudecodeoptimizer` to create their own `~/.cco/` structure
- Links point to their own global storage (using preference order on their OS)
- `project.json` ensures everyone uses same AI-selected configuration
- Commands dynamically load same principles at runtime
- Consistent configuration across team
- Works with symlinks, hardlinks, or copies depending on each team member's OS

**Optional** (add to `.gitignore` if preferred):
- ❌ `.claude/` - If you want CCO to be personal preference only
- ❌ `CLAUDE.md` - If you have existing project docs

### Removal

CCO is designed for easy, clean removal:

**Option 1: Remove from Project** (Recommended - keeps global installation)
```bash
/cco-remove
```

**What `/cco-remove` does:**
1. Removes all CCO-created links:
   - `.claude/project.json` (runtime config)
   - `.claude/commands/cco-*.md` (symlinks/hardlinks/copies)
   - `.claude/principles/` (all linked principle files: U*.md + P*.md)
   - `.claude/guides/` (all linked guide files)
   - `.claude/skills/` (all linked skill files)
   - `.claude/agents/` (all linked agent files, if any)
   - `.claude/statusline.js` (link to template)
2. Optionally removes CCO section from `CLAUDE.md`:
   - Removes content between `<!-- CCO_START -->` and `<!-- CCO_END -->`
   - Preserves existing project-specific content
   - Asks for confirmation
3. Optionally removes `.claude/settings.json` (if CCO-generated, asks for confirmation)
4. Removes project registry from `~/.cco/projects/<project>.json`
5. Displays removal summary
6. Keeps global `~/.cco/` intact (ready for other projects)

**Uninstall Safety:**
- If CCO section not removed from CLAUDE.md, broken principle references are ignored by Claude (no errors)
- Project continues to work without CCO
- No backup needed (removal is clean, non-destructive)

**Option 2: Manual Project Removal**
```bash
# Remove all CCO links and files
rm .claude/project.json                 # Remove runtime config
rm -rf .claude/commands/cco-*.md       # Remove command links
rm -rf .claude/principles/              # Remove principle links (U*.md + P*.md)
rm -rf .claude/guides/                  # Remove guide links
rm -rf .claude/skills/                  # Remove skill links
rm -rf .claude/agents/                  # Remove agent links (if any)
rm .claude/statusline.js                # Remove statusline link
rm .claude/settings.json                # Optional: only if CCO-generated

# Remove CCO section from CLAUDE.md (optional)
# Manually delete lines between <!-- CCO_START --> and <!-- CCO_END -->

# Remove project registry
rm ~/.cco/projects/<project-name>.json
```

**Option 3: Complete CCO Uninstall** (Removes from all projects)
```bash
# Uninstall Python package
pip uninstall claudecodeoptimizer

# Remove global CCO installation
rm -rf ~/.cco/

# Remove global commands from Claude
rm ~/.claude/commands/cco-init.md
rm ~/.claude/commands/cco-remove.md
```

**Important Notes:**
- `/cco-remove` is clean and non-destructive (no backups needed)
- Removal does not affect non-CCO files in `.claude/`
- Broken principle references in CLAUDE.md are safely ignored by Claude (no errors)
- Global `~/.cco/` can be reused for other projects
- Team members can remove CCO independently (links are local)

**Key benefit**: Updating CCO (`pip install -U claudecodeoptimizer`) automatically updates all projects that use symlinks or hardlinks (copies require re-init).

---

## Support

- **Documentation**: Available in `~/.cco/guides/` after installation
- **Issues**: [GitHub Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sungurerdim/ClaudeCodeOptimizer/discussions)
- **Repository**: [github.com/sungurerdim/ClaudeCodeOptimizer](https://github.com/sungurerdim/ClaudeCodeOptimizer)

---

## Project Goals

CCO aims to solve common challenges in AI-assisted development:

**Consistency & Standards:**
- Enforce industry best practices systematically
- Prevent AI models from reinventing solutions
- Maintain consistent style and approach across sessions

**Efficiency & Productivity:**
- Eliminate repetitive setup and configuration tasks
- Automate tedious processes (commits, audits, documentation)
- Smart model selection (Haiku for speed, Sonnet for thinking)
- Parallel agent execution for 2-3x performance

**Quality & Reliability:**
- Evidence-based verification prevents silent failures
- Anti-overengineering principles prevent bloat
- Comprehensive principle coverage (83 principles: 14 universal + 69 project-specific, 9 categories)
- Progressive disclosure minimizes token waste

**Team Collaboration:**
- Zero-pollution architecture works for individuals and teams
- Git-committable configuration (symlinks, not data)
- Consistent setup across team members
- Intelligent git workflow selection

**Common Problems Solved:**
- ✅ New feature breaks existing features (principles enforce compatibility)
- ✅ Old feature partially removed (evidence-based verification catches this)
- ✅ Two features coexist creating conflicts (anti-overengineering prevents this)
- ✅ New feature implemented but not actively used (commands enforce usage)
- ✅ Documentation lags behind code (CLAUDE.md generation/merging)
- ✅ AI does more work than requested (principles limit scope)
- ✅ Token waste from loading irrelevant context (progressive disclosure)

---

*Built with Claude Code • Designed for Claude Code • Powered by AI*

Created by Sungur Zahid Erdim
