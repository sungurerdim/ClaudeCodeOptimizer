# ClaudeCodeOptimizer

**Pain-point driven development assistant that configures Claude Code to tackle 2025's costliest problems: security vulnerabilities, technical debt, AI code quality issues, and collaboration breakdowns.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **v0.1.0**: Configuration layer providing Claude Code with specialized commands, skills, and agents for 12 critical industry pain points based on 2025 data.

---

## What Problems Does CCO Solve?

### The 12 Critical Pain Points (2025 Data)

| # | Pain Point | Impact | CCO Solution |
|---|------------|--------|--------------|
| **1** | **Security** | Vulnerabilities in production | `/cco-audit --security` detects OWASP Top 10 2025, supply chain risks |
| **2** | **Technical Debt** | Wasted developer time | `/cco-audit --tech-debt` finds dead code, complexity hotspots |
| **3** | **AI Security** | Prompt injection, PII leakage | `/cco-audit --ai-security` detects OWASP A01:2025 in AI code |
| **4** | **Missing Tests** | Production bugs, delays | `/cco-audit --tests` identifies untested critical paths |
| **5** | **Time Waste** | Inefficient queries, slow builds | `/cco-audit --performance` finds N+1 queries, missing indexes |
| **6** | **Integration Failures** | Broken builds, deploy delays | `/cco-audit --integration` finds import errors, conflicts |
| **7** | **Documentation Gaps** | Onboarding delays | `/cco-audit --docs` measures docstring coverage |
| **8** | **AI Code Quality** | Hallucinated APIs, code bloat | `/cco-audit --ai-quality` detects non-existent APIs, vibe coding |
| **9** | **Velocity Loss** | Slow feature delivery | `/cco-audit --code-review` analyzes DORA metrics decline |
| **10** | **AI Readiness Gaps** | Can't leverage AI tooling | `/cco-audit --platform` assesses CI/CD maturity, test automation |
| **11** | **Code Review Decline** | -27% comment rate (2025) | `/cco-audit --code-review` measures review quality, diversity |
| **12** | **Team Breakdowns** | Knowledge silos | `/cco-audit --code-review` detects echo chambers, rework rates |

**What CCO Provides:**
- **Commands** that configure Claude Code to address these pain points
- **Skills** that provide Claude Code with specialized knowledge (OWASP 2025, DORA metrics, etc.)
- **Agents** that execute audits, fixes, and generation in parallel
- **Principles** that ensure Claude Code follows best practices (DRY, honesty, verification)

---

## What is CCO?

CCO is a **pain-point driven configuration layer** that provides Claude Code with specialized commands, skills, agents, and principles to tackle 2025's costliest development problems.

### Reality Check: What CCO Actually Does

**CCO provides the "what to do"** - Claude Code executes the "how to do it":

| Component | What It Is | What It's NOT |
|-----------|------------|---------------|
| **CCO** | Configuration files in `~/.claude/` | NOT a standalone tool |
| **Commands** | Instructions for Claude Code | NOT executable scripts |
| **Skills** | Domain knowledge for Claude | NOT code libraries |
| **Agents** | Execution patterns for Claude | NOT separate processes |
| **Principles** | Guidelines for Claude's behavior | NOT enforced rules |

**How it works:**
1. You run `/cco-audit --security` in Claude Code
2. CCO's command file tells Claude Code what to check for
3. CCO's security skill provides Claude Code with OWASP 2025 patterns
4. Claude Code executes the actual grepping, reading, and analysis
5. CCO's audit-agent guides Claude Code on how to organize results

**CCO is to Claude Code what:**
- ESLint config is to ESLint
- Prettier config is to Prettier
- Docker Compose files are to Docker

**The Challenge:** Development teams face recurring problems: security vulnerabilities slip through, technical debt accumulates, AI-generated code has quality issues, and team collaboration breaks down.

**CCO's Approach:**
1. **Intelligent commands** (`/cco-audit`, `/cco-fix`, `/cco-generate`) that Claude Code executes
2. **Specialized skills** (OWASP 2025, DORA metrics, AI quality) that provide Claude Code with current knowledge
3. **Agent patterns** (audit-agent, fix-agent, generate-agent) that guide Claude Code's execution strategy
4. **Universal principles** (DRY, honesty, verification) that shape Claude Code's behavior
5. **Zero project pollution** - everything lives in `~/.claude/`, shared across all projects

One CCO update propagates to all projects instantly.

---

## CCO Component Design Principles

All CCO components (commands, skills, agents, principles) follow strict design rules to ensure consistency, quality, and optimal Claude Code integration:

### 1. No Hardcoded Examples (Critical)
**Problem:** AI models cannot distinguish between "example" and "real data"

**Rule:** Use placeholders like `{FILE_PATH}`, `{LINE_NUMBER}`, `{FUNCTION_NAME}` instead of hardcoded examples like `src/auth/login.py:45`

**Why:** Prevents AI from using fictional examples as real data, causing incorrect references and fabricated issues

**Reference:** `C_NO_HARDCODED_EXAMPLES` principle

### 2. Native Tool Interactions (Critical)
**Problem:** Text-based prompts break UX flow and lack validation

**Rule:** Always use native Claude Code tools (`AskUserQuestion`) for user interactions

**Why:** Provides consistent UI, validation, accessibility, and cross-platform compatibility

**Reference:** `C_NATIVE_TOOL_INTERACTIONS` principle

### 3. MultiSelect with "All" Option (Critical)
**Problem:** Users waste time clicking individual items

**Rule:** Every `multiSelect` question must include "All" as the first option

**Implementation:** When "All" is selected, treat it as all other options selected

**Why:** Enables efficient bulk selection without repetitive clicking

### 4. 100% Honest Reporting (Critical)
**Problem:** False claims erode trust and create production incidents

**Rule:** Never claim "fixed/completed" without verification, distinguish technical possibility from impossibility accurately

**Why:** Users make decisions based on reports - inaccuracy causes real damage

**Reference:** `C_HONEST_REPORTING`, `U_EVIDENCE_BASED_ANALYSIS` principles

### 5. Complete Accounting (Critical)
**Problem:** Losing track of items creates incomplete work

**Rule:** Every item must have a disposition: completed, skipped (reason), failed (reason), or cannot-do (reason)

**Formula:** `total = completed + skipped + failed + cannot-do`

**Why:** Ensures nothing falls through cracks, provides full transparency

**Reference:** `U_COMPLETE_REPORTING` principle

### 6. Optimal UX/DX (High)
**Problem:** Poor experience reduces adoption and productivity

**Rule:** Design every interaction for clarity, speed, and user satisfaction

**Examples:**
- Progress tracking: "Phase 2/5 (40% complete)"
- Clear categorization: Critical/High/Medium
- Actionable results with file:line references
- Streaming results for long operations

### 7. Principle Adherence (High)
**Problem:** Inconsistent behavior across components

**Rule:** All components must follow both Universal (U_*) and Claude-specific (C_*) principles

**Key Principles:**
- `U_DRY`: Single source of truth
- `U_MINIMAL_TOUCH`: Edit only required files
- `U_CHANGE_VERIFICATION`: Verify before claiming
- `C_AGENT_ORCHESTRATION_PATTERNS`: Parallel execution where beneficial
- `C_CONTEXT_WINDOW_MGMT`: Token optimization

### 8. Token Efficiency with Quality (High)
**Problem:** Wasting tokens reduces conversation length and increases costs

**Rule:** Minimize token usage while maximizing output quality

**Techniques:**
- Grep before Read (discovery → preview → precise read)
- Use Haiku for simple tasks, Sonnet for development, Opus for architecture
- Parallel operations where independent
- Targeted file reads with offset+limit

### 9. Strategic Sub-Agent Use (Medium)
**Problem:** Sequential operations create bottlenecks

**Rule:** Use sub-agents with appropriate models for parallelizable work

**Examples:**
- Security audit + Performance audit + Test audit (parallel, 3x faster)
- Multiple module analysis (parallel Haiku agents)
- Sequential only when dependencies exist

### 10. Progress Transparency (Medium)
**Problem:** Long operations feel unresponsive

**Rule:** Display current phase, total phases, percentage, and streaming results for operations >30 seconds

**Format:** `Phase 3/5: Analyzing security patterns... (60% complete)`

### 11. Universal Skill Utilization (Medium)
**Problem:** Skills created but not used waste effort

**Rule:** Every relevant skill must be utilized by appropriate commands/agents

**Verification:** Each skill should be referenced in at least one command or agent

### 12. Complete Documentation (Medium)
**Problem:** Users can't discover or use features effectively

**Rule:** All components documented with examples, listed in appropriate indexes

**Locations:**
- Commands: Listed in `/cco-help` and README
- Skills: Listed in `/cco-status` and skills/README.md
- Agents: Referenced in command documentation
- Principles: Listed in CLAUDE.md markers

### 13. Command Prompt Support (High)
**Problem:** Users can't provide additional context with commands

**Rule:** All commands must support optional prompt after command

**Format:** `/cco-audit --security "Focus on authentication endpoints"`

**Implementation:** AI reads and treats as additional instruction

### 14. Enhanced Help System (High)
**Problem:** Users struggle to discover and use features

**Rule:** `/cco-help` must be UX/DX focused, comprehensive, and accessible to all skill levels

**Requirements:**
- Pain-point organized (not alphabetical)
- Clear examples for each command
- Common workflows
- Beginner-friendly language
- Quick reference format

### Self-Enforcement

These principles apply to:
1. **Component definitions** - Templates and existing components must follow rules
2. **Runtime execution** - AI follows principles when executing commands
3. **Generated outputs** - All results respect principles (no hardcoded examples in output)

### Verification Checklist

Before finalizing any CCO component:
- [ ] No hardcoded examples (use placeholders)
- [ ] Native tools for user interaction (no text prompts)
- [ ] MultiSelect questions have "All" option
- [ ] Honest reporting (verify before claiming)
- [ ] Complete accounting (all items have disposition)
- [ ] Progress tracking for long operations
- [ ] Token-optimized implementation
- [ ] Follows all relevant U_* and C_* principles
- [ ] Documented in appropriate locations
- [ ] Supports optional prompt parameter (commands)


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
   - Creates `~/.claude/principles/` (U_*, C_*, P_* principles)
   - Creates `~/.claude/skills/` (domain-specific skills)
   - Creates `~/.claude/agents/` (specialized agents)
   - Generates `~/.claude/CLAUDE.md` (marker-based principle injection - see [ADR-001](docs/ADR/001-marker-based-claude-md.md))
   - Copies `~/.claude/settings.json.example` (optional: Claude Code config template)
   - Copies `~/.claude/statusline.js.example` (optional: status line script template)
   - Shows before/after file count summary
   - If files exist, asks before overwriting (interactive mode)
   - Use `cco-setup --force` to skip confirmation and overwrite
3. Done! Commands available in all projects immediately via Claude Code

**What's New (Recent Updates):**
- ✅ 100% test pass rate (all tests fixed and passing)
- ✅ Enhanced command UX with unused skills integration
- ✅ Context optimization focus in `/cco-slim` (CLAUDE.md duplication elimination)
- ✅ Comprehensive PR template with CCO principle compliance checklist
- ✅ Architecture Decision Records (ADR) and operational runbooks
- ✅ Installation tracking improvements with before/after summary

**Installation Options:**
```bash
cco-setup          # Interactive mode (asks before overwriting)
cco-setup --force  # Force overwrite without asking
cco-setup --help   # Show usage
```

### Optional Configuration

CCO provides template files for Claude Code configuration. **These are completely optional** - CCO works out of the box without them.

**Available Templates:**

1. **`~/.claude/settings.json.example`** - Claude Code settings
   - Pre-configured permissions for CCO commands
   - Status line integration
   - Security safeguards (blocked destructive commands)

2. **`~/.claude/statusline.js.example`** - Enhanced status line
   - Git status (branch, changes, commits)
   - CCO project info
   - Real-time metrics

**How to Use:**

```bash
# Option 1: Copy and customize
cp ~/.claude/settings.json.example ~/.claude/settings.json
cp ~/.claude/statusline.js.example ~/.claude/statusline.js
# Edit files to match your preferences

# Option 2: Use as reference
# Keep .example files as reference, manually add desired parts to your existing config
```

**Important Notes:**
- CCO **never** overwrites your existing `settings.json` or `statusline.js`
- `.example` files are updated on every `cco-setup` to provide latest templates
- You can safely ignore these templates - CCO commands work without them

### Uninstallation

**Complete Uninstall (2 Steps - ORDER MATTERS):**

```bash
# Step 1: Remove global files FIRST (inside Claude Code)
/cco-remove
# This removes:
# - ~/.claude/commands/ (all cco-*.md files)
# - ~/.claude/principles/ (all C_*, U_*, P_* files)
# - ~/.claude/skills/ (all cco-skill-*.md files)
# - ~/.claude/agents/ (all cco-agent-*.md files)
# - ~/.claude/CLAUDE.md (principle markers)

# Step 2: Uninstall package (outside Claude Code)
pip uninstall claudecodeoptimizer
# Or if you used pipx/uv:
pipx uninstall claudecodeoptimizer
uv tool uninstall claudecodeoptimizer
```

**Why This Order?**

`/cco-remove` is a Claude Code slash command, so it only works when the package is installed. If you run `pip uninstall` first, you lose access to `/cco-remove` and must manually delete `~/.claude/` files.

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

### Discovery (Know Your Problems)

**`/cco-status`** - Check CCO installation health
- Verify CCO setup, show installed commands (10), skills (30), agents (3)
- Example: `/cco-status`

**`/cco-help`** - Quick command reference
- All 10 commands with clear examples, common tasks, 5 typical workflows
- Example: `/cco-help`

### Critical Action (Fix Your Problems)

**`/cco-audit`** - Find problems in your code ⭐ START HERE
- **Quick mode:** `--quick` (5 min health check with scores)
- **Core (7):** `--security`, `--tech-debt`, `--tests`, `--database`, `--performance`, `--integration`, `--docs`
- **AI (2025):** `--ai-security`, `--ai-quality`, `--ai` (meta: all AI), `--ai-debt` (meta: AI + tech-debt)
- **Team (2025):** `--code-review`, `--platform`
- **Infrastructure:** `--ci-cd`, `--containers`, `--supply-chain`
- **Total: 14 categories** (security, ai-security, tech-debt, ai-quality, tests, database, performance, integration, docs, code-review, platform, ci-cd, containers, supply-chain)
- **Presets:** `--all` (comprehensive scan)
- Example: `/cco-audit --security --ai-quality --code-review`

**`/cco-fix`** - Auto-fix detected problems
- Safe fixes auto-applied (SQL parameterization, remove dead code, API hallucination removal)
- Risky fixes require approval (CSRF protection, auth changes)
- Same 14 categories as audit (plus meta-flags: `--ai`, `--ai-debt`)
- Auto-runs audit if needed
- Example: `/cco-fix --security --ai-quality --tech-debt`

**`/cco-generate`** - Create tests, docs, configs (18 types)
- **Critical:** `--tests`, `--contract-tests`
- **High:** `--load-tests`, `--chaos-tests`, `--openapi`, `--cicd`
- **Team (2025):** `--review-checklist` (PR quality gates, DORA metrics tracking)
- **Recommended:** `--docs`, `--adr`, `--runbook`, `--dockerfile`, `--migration`, `--indexes`, `--monitoring`, `--logging`, `--slo`, `--pre-commit`, `--requirements`
- Example: `/cco-generate --tests --openapi --review-checklist`

### Productivity (Save Time)

**`/cco-optimize`** - Speed up your code with metrics
- **Types:** `--database` (queries), `--docker` (image size), `--bundle` (frontend), `--performance` (bottlenecks)
- Shows before/after metrics for all optimizations
- Example: `/cco-optimize --database --docker`

**`/cco-commit`** - Smart git commits
- AI-generated semantic commit messages, atomic commit recommendations
- Example: `git add . && /cco-commit`

**`/cco-implement`** - Build new features with TDD
- Test-Driven Development approach, auto-skill selection based on feature type
- Example: `/cco-implement "Add JWT authentication"`

### Management

**`/cco-update`** - Update to latest version
- One command updates all projects instantly

**`/cco-remove`** - Clean uninstall (Step 1 of 2)
- Removes all global CCO files (`~/.claude/`), shows what will be deleted before confirmation
- Must be run BEFORE `pip uninstall` (requires package to work)

---

## End-to-End Example

Here's a complete walkthrough of a security audit on a Flask API project:

### Step 1: Run Security Audit

```bash
/cco-audit --security
```

**Sample Output:**
```
Phase 1: Tech Stack Detection
─────────────────────────────
✓ Python 3.11 detected
✓ Flask framework found
✓ SQLAlchemy ORM detected
✓ PostgreSQL database

Phase 2: Security Scanning
──────────────────────────
Scanning for OWASP Top 10 vulnerabilities...

Found 4 issues:

CRITICAL (1):
• SQL Injection in {FILE_PATH}:{LINE_NUMBER}
  db.execute(f"SELECT * FROM users WHERE id = {user_id}")
  → Use parameterized query

HIGH (2):
• Hardcoded secret in {FILE_PATH}:{LINE_NUMBER}
  SECRET_KEY = "mysecretkey123"
  → Move to environment variable

• Missing CSRF protection in {FILE_PATH}:{LINE_NUMBER}
  → Add CSRF token validation

MEDIUM (1):
• Debug mode enabled in {FILE_PATH}:{LINE_NUMBER}
  DEBUG = True
  → Disable in production

Summary: 4 issues (1 critical, 2 high, 1 medium)
```

### Step 2: Auto-Fix Safe Issues

```bash
/cco-fix --security
```

**Sample Output:**
```
Analyzing 4 security issues...

Safe Fixes (auto-applied):
──────────────────────────
✓ {FILE_PATH}:{LINE_NUMBER} - Parameterized SQL query
  Before: db.execute(f"SELECT * FROM users WHERE id = {user_id}")
  After:  db.execute("SELECT * FROM users WHERE id = :id", {"id": user_id})

✓ {FILE_PATH}:{LINE_NUMBER} - Externalized secret
  Before: SECRET_KEY = "mysecretkey123"
  After:  SECRET_KEY = os.environ.get("SECRET_KEY")
  Note: Add SECRET_KEY to your .env file

Risky Fixes (need approval):
────────────────────────────
? {FILE_PATH}:{LINE_NUMBER} - Add CSRF protection
  This requires adding middleware and updating forms.
  Apply this fix? [y/n]

Skipped:
────────
• {FILE_PATH}:{LINE_NUMBER} - Debug mode
  Reason: Environment-specific, configure manually

Summary: 2 fixed, 1 needs approval, 1 skipped
```

### Step 3: Generate Missing Tests

```bash
/cco-generate --tests
```

**Sample Output:**
```
Analyzing test coverage...

Current coverage: 45%
Target coverage: 80%

Generating tests for uncovered code:
────────────────────────────────────
✓ tests/test_api_users.py - 5 test cases
  - test_get_user_success
  - test_get_user_not_found
  - test_create_user_valid
  - test_create_user_duplicate_email
  - test_sql_injection_prevented

✓ tests/test_api_auth.py - 4 test cases
  - test_login_success
  - test_login_invalid_password
  - test_csrf_token_required
  - test_session_expiry

Created: 2 test files, 9 test cases
Run: pytest tests/ to verify
```

### Step 4: Verify Results

```bash
/cco-audit --security
```

**Sample Output:**
```
Phase 2: Security Scanning
──────────────────────────
Found 1 issue:

MEDIUM (1):
• Debug mode enabled in {FILE_PATH}:{LINE_NUMBER}
  → Disable in production (environment-specific)

Summary: 1 issue (0 critical, 0 high, 1 medium)
Previously: 4 issues → Now: 1 issue
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
/cco-optimize --database --docker
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
/cco-optimize --all        # Performance tuning
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
