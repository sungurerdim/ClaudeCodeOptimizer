# CCO Features

## Core Features

### 🎯 Essential Features (Start Here)

The features you'll use immediately to get value from CCO.

---

#### 🧙 Intelligent Project Initialization

**Two modes, unified decision engine:**

**Quick Mode** (~10s):
- **Clean install**: Removes previous CCO setup first (if any)
- AI auto-analyzes codebase (README, docs, git history, file structure)
- Detects: OS, shell, locale, languages, frameworks, tools, team size, project maturity
- Auto-decides: Project type, testing strategy, security level, git workflow
- Generates: Tailored CLAUDE.md, selected principles/commands/guides/skills/agents as symlinks
- **No state files created** - completely stateless

**Interactive Mode** (~2-5m):
- **Clean install**: Removes previous CCO setup first (if any)
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
- **No state tracking** - selections applied as symlinks immediately

### 📚 Progressive Disclosure System

**Two-tier principle architecture** - Maximum token efficiency + true project-specific loading

CCO uses a global storage model with local project links. All CCO data lives in `~/.cco/` (commands, principles, guides, skills, agents), and projects reference only what they need via symlinks in `.claude/`.

**Architecture Overview:**
- **Global storage** (`~/.cco/`): 95 principles (19 universal + 64 project-specific + 12 Claude guidelines), 28 commands, 5 guides, 23 skills, 3 agents
- **Project local** (`.claude/`): Symlinks to selected principles (24-44 total), commands (8-15), and relevant guides/skills
- **Zero pollution**: Projects contain only links, no duplicated files
- **Zero state**: No config files, no project registry - selection stored as symlinks

> **See**: [Architecture → Directory Structure](architecture.md#directory-structure) for complete directory trees

**Dynamic Loading (NEW)**:

**CLAUDE.md Format (Minimal)**:
```markdown
# Project Name

<!-- CCO_START -->
## Development Principles & Guidelines

Follow the principles in `.claude/principles/`:
- Universal principles (19 total): Apply to all projects
- Project-specific principles (24 total): Selected for this project

<!-- CCO_END -->
```

**Token Efficiency:**
- **Init time**: AI selects only needed principles (e.g., 25 out of 43)
- **Runtime**: Commands load only selected principles (no waste)
- **Example**: `/cco-audit-security` on simple CLI tool → loads 4 principles (U_EVIDENCE_BASED + 3 security), not all
- **Result**: 80%+ token optimization maintained throughout lifecycle

---

#### 🎯 Development Principles

**Two-Tier Architecture:**

**Universal Principles (19 total)**:
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
- DRY enforcement
- Complete integration check
- SQL injection prevention
- Secret management with rotation
- Dependency management

**Project-Specific Principles (24 total, AI-selected)**:
- **API Design** (1): API security best practices
- **Architecture** (1): Event-driven architecture
- **Code Quality** (3): Linting & SAST, type safety, version management
- **Performance** (2): Database optimization, async I/O
- **Security & Privacy** (14): Encryption, zero-trust, rate limiting, input validation, audit logging, container & K8s security
- **Testing** (3): Coverage targets, integration tests, CI gates

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
- All universal principles (19 total) symlinked automatically
- Only applicable project principles (typically 5-20 from 24) symlinked

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

**28 slash commands for complete development lifecycle:**

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

#### 🔄 **Stateless Architecture**

**Zero state management** - CCO operates without any config files or project registries

**How It Works:**
- Selected principles/commands/guides stored as **symlinks in `.claude/`**
- No `~/.cco/projects/` directory
- No `~/.cco/config.json` file
- No project registry whatsoever
- All project configuration derived from:
  - Symlink presence in `.claude/`
  - CLAUDE.md marker content
  - Live codebase analysis

**Benefits:**
- **Zero pollution**: Project directory contains only symlinks
- **Single source of truth**: Content in `~/.cco/`, links in `.claude/`
- **No sync issues**: No state to get out of sync
- **Clean removal**: Delete symlinks, project restored to pre-CCO state
- **Simple updates**: `pip install -U claudecodeoptimizer` updates all projects instantly

**Example:**
```bash
# Project state is determined by what's linked, not what's stored
.claude/
├── commands/
│   └── cco-audit.md -> ~/.cco/commands/cco-audit.md  # ✅ Selected
├── principles/
│   ├── U_ATOMIC_COMMITS.md -> ~/.cco/principles/...  # ✅ Selected
│   └── P_LINTING_SAST.md -> ~/.cco/principles/...    # ✅ Selected
└── guides/
    └── cco-security-response.md -> ~/.cco/guides/... # ✅ Selected

# No project registry needed - links ARE the state
```

---
