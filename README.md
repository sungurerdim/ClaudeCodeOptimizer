# ClaudeCodeOptimizer

**Pain-point driven development assistant that configures Claude Code to tackle 2025's costliest problems: security vulnerabilities, technical debt, AI code quality issues, and collaboration breakdowns.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **v1.0.0**: Configuration layer providing Claude Code with specialized commands, skills, and agents for 12 critical industry pain points based on 2025 data.

---

## What Problems Does CCO Solve?

### The 12 Critical Pain Points (2025 Data)

| # | Problem | Impact | Solution |
|---|---------|--------|----------|
| 1 | Security | Vulnerabilities | `/cco-audit --security` |
| 2 | Tech Debt | Wasted time | `/cco-audit --tech-debt` |
| 3 | AI Security | Prompt injection | `/cco-audit --ai-security` |
| 4 | Missing Tests | Production bugs | `/cco-audit --tests` |
| 5 | Performance | Slow queries | `/cco-audit --performance` |
| 6 | Integration | Broken builds | `/cco-audit --integration` |
| 7 | Documentation | Onboarding delays | `/cco-audit --docs` |
| 8 | AI Quality | Hallucinated APIs | `/cco-audit --ai-quality` |
| 9 | Velocity Loss | Slow delivery | `/cco-audit --code-review` |
| 10 | AI Readiness | Can't leverage AI | `/cco-audit --platform` |
| 11 | Code Review | -27% comments | `/cco-audit --code-review` |
| 12 | Team Gaps | Knowledge silos | `/cco-audit --code-review` |

**What CCO Provides:**
- **Commands** that configure Claude Code to address these pain points
- **Skills** that provide Claude Code with specialized knowledge (OWASP 2025, DORA metrics, etc.)
- **Agents** that execute audits, fixes, and generation in parallel
- **Principles** that ensure Claude Code follows best practices (DRY, honesty, verification)

---

## What is CCO?

**CCO = Pain-point driven configuration layer for Claude Code** (like ESLint config → ESLint)

| Component | What It Is |
|-----------|-----------|
| **Commands** | Instructions for Claude (e.g., `/cco-audit`) |
| **Skills** | Domain knowledge (OWASP 2025, DORA metrics) |
| **Agents** | Execution patterns (parallel, pipeline) |
| **Principles** | Behavioral guidelines (DRY, verification) |

---

## CCO Component Design Principles

All CCO components follow strict design rules. **For detailed principles, see `~/.claude/principles/` after installation.**

### Essential Principles

- **No Hardcoded Examples** - Use placeholders like `{FILE_PATH}`, `{LINE_NUMBER}` (See `cco-principle-u-no-hardcoded-examples`)
- **Native Tool Interactions** - Use `AskUserQuestion` for user input (See `cco-principle-c-native-tool-interactions`)
- **100% Honest Reporting** - Never claim "fixed" without verification (See `cco-principle-u-evidence-based-analysis`)
- **Complete Accounting** - All items: completed/skipped/failed/cannot-do. Totals must match.
- **MultiSelect with "All"** - Every multiSelect question must have "All" option
- **Principle Adherence** - Follow cco-principle-u-* (Universal) and cco-principle-c-* (Claude-specific) principles
- **Token Efficiency** - Grep before Read, targeted reads, parallel operations
- **UX/DX Excellence** - Progress tracking, actionable results, streaming feedback

**Quick Verification Checklist:**

- [ ] No hardcoded examples (use placeholders)
- [ ] Honest reporting (verify before claiming)
- [ ] Complete accounting (all items accounted for)
- [ ] MultiSelect has "All" option
- [ ] Follows cco-principle-u-* and cco-principle-c-* principles

## Quick Start

### Installation

**Simplest Method (Works Everywhere):**

```bash
# Install
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git

# Setup (with before/after file count summary)
cco-setup
```

**Or One-Line Install (Zero Dependencies):**

```bash
# Any platform - pure Python, no git/pip knowledge needed
python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/quick-install.py').read())"
```

**Optional: Isolated Install (if you have pipx/uv):**

```bash
# With pipx (isolated, clean uninstall)
pipx install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup

# With uv (modern, fast)
uv tool install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

> **Note**: pipx/uv provide isolated environments (good for avoiding conflicts), but plain `pip` works perfectly fine. Use what you already have.

**How Installation Works:**

1. `pip install` → Installs Python package globally
2. `cco-setup` → Copies content files to `~/.claude/` directory
   - Creates `~/.claude/commands/` (all CCO commands)
   - Creates `~/.claude/principles/` (cco-principle-u-*, cco-principle-c-* principles)
   - Creates `~/.claude/skills/` (domain-specific skills)
   - Creates `~/.claude/agents/` (specialized agents)
   - Copies `~/.claude/cco-*.md` (structure and quality standards)
   - Copies `~/.claude/cco-patterns.md` (reusable patterns)
   - Generates `~/.claude/CLAUDE.md` (marker-based principle injection - see [ADR-001](docs/ADR/001-marker-based-claude-md.md))
   - Copies `~/.claude/settings.json.cco` (optional: Claude Code config template)
   - Copies `~/.claude/statusline.js.cco` (optional: status line script template)
   - Shows before/after file count summary
   - If files exist, asks before overwriting (always overwrites after confirmation)
3. Done! Commands available in all projects immediately via Claude Code


### Verifying Installation

Check CCO installation status and available components:

```bash
# Check installation health
cco-status

# Or inside Claude Code
/cco-status
```

**What cco-status shows:**
- Installation health (Good/Incomplete)
- Component counts (commands, principles, skills, agents)
- Version info and installation method
- Architecture overview
- Quick start guidance

### Optional Configuration

CCO provides template files for Claude Code configuration. **These are completely optional** - CCO works out of the box without them.

**Available Templates:**

1. **`~/.claude/settings.json.cco`** - Claude Code settings
   - Pre-configured permissions for CCO commands
   - Status line integration
   - Security safeguards (blocked destructive commands)

2. **`~/.claude/statusline.js.cco`** - Enhanced status line (see [Statusline Documentation](#statusline) below)

**How to Use:**

```bash
# Option 1: Copy and customize
cp ~/.claude/settings.json.cco ~/.claude/settings.json
cp ~/.claude/statusline.js.cco ~/.claude/statusline.js
# Edit files to match your preferences

# Option 2: Use as reference
# Keep .cco files as reference, manually add desired parts to your existing config
```

**Important Notes:**
- CCO **never** overwrites your existing `settings.json` or `statusline.js`
- `.cco` template files are updated on every `cco-setup` to provide latest templates
- You can safely ignore these templates - CCO commands work without them

### Statusline

The CCO statusline provides real-time project and git information in a compact, privacy-focused display.

**Example Output:**
```
 📁 {project}/{dir} | 👤 {username} | {git size} | {claude code version} | 🤖 {active ai model}
┌────────────────────┬──────────────┬──────────┬──────────┬─────────────┐
│ 🔗 {repo}:{branch} │ Conflicts: # │ Stash: # │ Ahead: # │ Last: hh:mm │
├────────────────────┼──────────────┼──────────┼──────────┼─────────────┤
│ Unstaged +### -### │ edit ##      │ new ##   │ del ##   │ move ##     │
│ Staged   +### -### │ edit ##      │ new ##   │ del ##   │ move ##     │
└────────────────────┴──────────────┴──────────┴──────────┴─────────────┘
```

**Title Row:**
| Field | Description |
|-------|-------------|
| 📁 {project}/{dir} | Last 2 segments of current directory |
| 👤 {username} | System username |
| {git size} | Project size excluding `.gitignore`'d files |
| {claude code version} | Installed Claude Code version |
| 🤖 {active ai model} | Currently active AI model |

**Git Info Row:**
| Field | Description |
|-------|-------------|
| 🔗 Repo:Branch | Repository name and current branch |
| Conflicts | Merge conflict count (`git status` UU/AA/DD) |
| Stash | Stash count (`git stash list`) |
| Ahead | Unpushed commits (`git rev-list @{u}..HEAD`) |
| Last | Time since last commit (`hh:mm` or `#d #h`) |

**Unstaged Row:**
| Field | Description |
|-------|-------------|
| +/- | Total lines added/removed (working tree) |
| edit | Modified files |
| new | Untracked files (not in `.gitignore`) |
| del | Deleted files |
| move | Renamed files |

**Staged Row:**
Same as Unstaged, but for files added to index (`git add`) ready to commit.

**Features:**
- ✅ OS-agnostic (Windows, Linux, macOS)
- ✅ Fully dynamic (no hardcoded values)
- ✅ Privacy-focused (minimal path exposure)
- ✅ Respects `.gitignore` for size calculation
- ✅ Cross-platform git integration

**Installation:**
```bash
cp ~/.claude/statusline.js.cco ~/.claude/statusline.js
```

### Uninstallation

**Complete Uninstall (2 Steps - ORDER MATTERS):**

```bash
# Step 1: Remove global files FIRST
# Option 1: Use slash command (inside Claude Code)
cco-remove

# Option 2: Use CLI command (terminal)
cco-remove
# This removes:
# - ~/.claude/commands/ (all cco-*.md files)
# - ~/.claude/principles/ (all cco-principle-c-*, cco-principle-u-* files)
# - ~/.claude/skills/ (all cco-skill-*.md files)
# - ~/.claude/agents/ (all cco-agent-*.md files)
# - ~/.claude/cco-*.md (all standards files)
# - ~/.claude/cco-patterns.md (pattern library)
# - ~/.claude/CLAUDE.md (principle markers)

# Step 2: Uninstall package (outside Claude Code)
pip uninstall claudecodeoptimizer
# Or if you used pipx/uv:
pipx uninstall claudecodeoptimizer
uv tool uninstall claudecodeoptimizer
```

**Why This Order?**

`# Option 1: Use slash command (inside Claude Code)
cco-remove

# Option 2: Use CLI command (terminal)
cco-remove` is a Claude Code slash command, so it only works when the package is installed. If you run `pip uninstall` first, you lose access to `cco-remove` and must manually delete `~/.claude/` files.

**What Gets Removed:**
- ✓ Python package (claudecodeoptimizer)
- ✓ Global directory (`~/.claude/`)
- ✓ All commands, principles, skills, agents
- ✓ Zero trace left on your system

**What Does NOT Get Removed:**
- Your project files (CCO never touches them)
- Your git history
- Your dependencies
- Other Claude Code configurations

**Verification:**
```bash
# After uninstall, these should fail:
pip show claudecodeoptimizer  # Should show "not found"
ls ~/.claude/  # Should show "no such file or directory"
```

### First Commands - Immediate Impact

Open any project in Claude Code:

```bash
# START HERE: Fast health assessment with scores
/cco-audit --quick
# Shows scores for security, testing, code quality, etc.

# Find critical security issues
/cco-audit --security
# Detects SQL injections, hardcoded secrets, AI prompt injection risks

# Auto-fix safe issues
/cco-fix --security
# Applies safe fixes: parameterized queries, externalized secrets

# Generate missing tests
/cco-generate --tests
# Creates unit + integration tests for uncovered code

# Get comprehensive help
/cco-help
```

**Results:**
- Security issues identified and fixed
- Test coverage improved
- Code quality enhanced
- Time saved on manual review

---

## Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/cco-status` | Health check | `/cco-status` |
| `/cco-help` | Command reference | `/cco-help` |
| `/cco-audit --security` | Find security issues | `/cco-audit --security --ai-quality --code-review` |
| `/cco-fix --security` | Auto-fix problems | `/cco-fix --security --ai-quality --tech-debt` |
| `/cco-generate --tests` | Create tests/docs | `/cco-generate --tests --openapi --review-checklist` |
| `/cco-optimize --performance --database` | Speed up code | `/cco-optimize --performance --database --docker` |
| `/cco-commit` | Smart git commits | `git add . && /cco-commit` |
| `/cco-generate --feature "feature"` | Build with TDD | `/cco-generate --feature "Add JWT authentication"` |
| `cco-setup` | Update version | `cco-setup` |
| `/cco-optimize --context` | Reduce context tokens | `/cco-optimize --context` |
| `cco-remove` | Clean uninstall | `cco-remove` |

**Audit Categories:** `--quick`, `--security`, `--ai-security`, `--ai-quality`, `--tests`, `--database`, `--performance`, `--tech-debt`, `--code-review`, `--platform`, `--ci-cd`, `--containers`, `--supply-chain`, `--all`

---

## Quick Example Walkthrough

```bash
# Step 1: Find security issues
/cco-audit --security
# Detects SQL injections, secrets, CSRF risks

# Step 2: Auto-fix safe issues
/cco-fix --security
# Parameterizes queries, externalizes secrets, flags risky changes

# Step 3: Generate tests
/cco-generate --tests
# Creates unit + integration tests for uncovered code

# Step 4: Verify
/cco-audit --security
# Shows reduced issue count
```

---

## Example Workflows

### New Project Setup
```bash
/cco-audit --quick         # Fast health assessment
/cco-generate --tests --openapi --cicd --dockerfile
# Creates tests, docs, CI/CD, containerization
```

### Security Hardening
```bash
/cco-audit --security --ai-security --supply-chain
# Finds SQL injections, secrets, AI risks, CVEs
/cco-fix --security
# Fixes safe issues automatically, flags risky ones for review
```

### Performance Optimization
```bash
/cco-audit --performance --database
# Finds N+1 queries, missing indexes
/cco-optimize --performance --database --docker
# Faster queries, smaller images (with metrics)
```

### Quality Improvement
```bash
/cco-audit --code-quality --tech-debt --tests
/cco-fix --tech-debt
/cco-generate --tests
# Cleaner code, better tests, reduced complexity
```

### AI Code Quality (New in 2025)
```bash
/cco-audit --ai
# Detects hallucinated APIs, code bloat, vibe coding
/cco-fix --ai
# Fixes AI-generated quality issues
```

### Platform Maturity Assessment (New in 2025)
```bash
/cco-audit --platform
# Assesses CI/CD, test automation, IaC, deployment automation, DX
# Shows AI readiness score and DORA metrics
```

### Complete Health Check
```bash
/cco-audit --quick         # Get baseline scores
/cco-audit --all           # Find all issues
/cco-fix --all             # Fix safe issues
/cco-generate --all        # Create missing components
/cco-optimize --performance --all        # Performance tuning
/cco-commit                # Clean commits
```

---

## Requirements

- **Python 3.11+**
- **Claude Code** (required)
- **Git** (optional, for workflow features)

---

## Troubleshooting

### Commands not found

```bash
# Verify installation
ls ~/.claude/commands/cco-*  # Unix/macOS
dir %USERPROFILE%\.claude\commands\cco-*  # Windows

# If missing, run setup
cco-setup

# Restart Claude Code
```

### Skills not loading

Skills auto-activate via Claude's semantic matching. No manual intervention needed.

```bash
# Verify skills exist
/cco-status
# Shows all available skills
```

### Package installation fails

```bash
# Verbose install
pip install -v git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup

# Or from source (development)
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer
cd ClaudeCodeOptimizer
pip install -e .
cco-setup
```

---

## Documentation

### Core Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed architecture, agent orchestration, principles
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines
- **Skills Reference** - See `~/.claude/skills/` after installation

### Architecture Decision Records (ADR)
- **[ADR-001: Marker-based CLAUDE.md System](docs/ADR/001-marker-based-claude-md.md)** - How CCO injects content into CLAUDE.md
- **[ADR-002: Zero Pollution Design](docs/ADR/002-zero-pollution-design.md)** - Why all content goes in `~/.claude/`
- **[ADR-003: Progressive Skill Loading](docs/ADR/003-progressive-skill-loading.md)** - How skills auto-activate on demand
- **[ADR Index](docs/ADR/README.md)** - All architectural decisions

### Operational Runbooks
- **[Installation Runbook](docs/runbooks/installation.md)** - Step-by-step installation guide
- **[Update Runbook](docs/runbooks/updates.md)** - Update existing CCO installation
- **[Troubleshooting Runbook](docs/runbooks/troubleshooting.md)** - Common issues and solutions
- **[Uninstallation Runbook](docs/runbooks/uninstallation.md)** - Clean removal procedures
- **[Runbook Index](docs/runbooks/README.md)** - All operational procedures

### Development Resources
- **[PR Template](.github/PULL_REQUEST_TEMPLATE.md)** - Comprehensive PR checklist with CCO principle compliance
- **[CI/CD Workflows](.github/workflows/)** - Automated testing and quality checks

---

## Contributing

Contributions welcome! Priority areas:
- Language-specific skills (TypeScript, Rust, Go)
- Pain-point measurement tools
- Integration with monitoring systems
- Test coverage improvements

[Open an issue](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues) or submit a PR.

---

## Acknowledgments

**Inspired by:**
- [Superpowers](https://github.com/obra/superpowers) by @obra - Skills system
- [Agents](https://github.com/wshobson/agents) by @wshobson - Progressive disclosure

**Built for:**
- [Claude Code](https://claude.com/claude-code) - Anthropic's official CLI

**Driven by:**
- Industry pain point research and developer feedback

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues) | [Discussions](https://github.com/sungurerdim/ClaudeCodeOptimizer/discussions)

**CCO:** Find issues, fix them automatically, generate missing components. Zero project pollution.
