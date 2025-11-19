# ClaudeCodeOptimizer

**Pain-point driven development assistant for Claude Code. Tackles 2025's costliest problems: security vulnerabilities, technical debt, missing tests, and time waste.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **v0.1.0**: Production-ready command system addressing 7 critical industry pain points based on 2025 data.

---

## What Problems Does CCO Solve?

### The 7 Critical Pain Points

| Pain Point | Impact | CCO Solution |
|------------|--------|--------------|
| **Security** | Vulnerabilities in production | `/cco-audit --security` + auto-fix (OWASP Top 10, AI security, supply chain) |
| **Technical Debt** | Wasted developer time | `/cco-fix --tech-debt` removes dead code, reduces complexity |
| **AI Code Reliability** | Unreliable AI-generated code | `/cco-audit --ai-security` detects prompt injection, hallucination risks |
| **Missing Tests** | Production bugs, delays | `/cco-generate --tests` creates unit + integration tests |
| **Time Waste** | Inefficient workflows | `/cco-optimize` improves queries, builds, removes dead code |
| **Integration Failures** | Deployment delays, broken builds | `/cco-audit --integration` finds import errors, dependency conflicts |
| **Documentation Gaps** | Onboarding delays, knowledge loss | `/cco-generate --openapi` creates complete API specs |

**What CCO Does:**
- Finds and fixes security vulnerabilities automatically
- Removes dead code and reduces complexity
- Generates comprehensive test suites
- Optimizes database queries and build times
- Creates complete API documentation

---

## What is CCO?

CCO is a **pain-point driven development assistant** that automatically configures Claude Code with production-grade principles and intelligent commands.

**The Challenge:** Development teams face recurring problems: security vulnerabilities slip through, technical debt accumulates, tests are missing, and workflows are inefficient.

**CCO's Approach:**
1. **Intelligent commands** that address these pain points directly
2. **Specialized skills** that auto-activate based on your needs
3. **AI agents** for parallel execution (audit, fix, generate)
4. **Zero project pollution** - everything lives in `~/.claude/`, shared across all projects

One update propagates to all projects instantly.

---

## How CCO Works

### Command → Agent → Skill Flow

```
User runs command          Agent executes           Skills activate
─────────────────────────────────────────────────────────────────────
/cco-audit --security  →   audit-agent (Haiku)  →   Security skill
                           - Pattern matching       - OWASP checks
                           - Fast scanning          - AI security
                           - Low cost               - Supply chain

/cco-fix --security    →   fix-agent (Sonnet)   →   Security skill
                           - Semantic analysis      - Safe fixes
                           - Code modifications     - Risky approvals
                           - High accuracy          - Verification

/cco-generate --tests  →   generate-agent       →   Testing skill
                           (Sonnet)                 - Unit tests
                           - Quality output         - Integration tests
                           - Complete code          - Coverage targets
```

### Data Flow: audit → fix → generate

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   AUDIT     │ ──→ │    FIX      │ ──→ │  GENERATE   │
│             │     │             │     │             │
│ • Discover  │     │ • Auto-fix  │     │ • Create    │
│   issues    │     │   safe      │     │   tests     │
│ • Classify  │     │ • Request   │     │ • Create    │
│   severity  │     │   approval  │     │   docs      │
│ • Report    │     │   for risky │     │ • Fill      │
│   findings  │     │ • Verify    │     │   gaps      │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      └───────────────────┴───────────────────┘
                          │
                    Shared Context:
                    • Tech stack detection
                    • Project conventions
                    • Finding categories
```

**Flow Details:**

1. **Discovery Phase** (All commands)
   - Detect tech stack via Glob patterns (`**/*.py`, `**/Dockerfile`)
   - Identify frameworks (Flask, Django, FastAPI)
   - Store context for downstream commands

2. **Audit Phase**
   - Run applicable checks based on flags
   - Categorize findings by severity (critical/high/medium/low)
   - Report with file:line references

3. **Fix Phase**
   - Reuse audit findings (auto-runs audit if needed)
   - Safe fixes: Apply automatically (parameterize SQL, remove dead code)
   - Risky fixes: Request user approval (auth changes, CSRF)
   - Verify each fix

4. **Generate Phase**
   - Use tech stack context
   - Follow project conventions
   - Create missing components (tests, docs, configs)

### Model Selection Rationale

| Agent | Model | Why |
|-------|-------|-----|
| audit-agent | Haiku | Pattern matching doesn't need deep reasoning. Fast & cheap for scanning. |
| fix-agent | Sonnet | Code modifications need semantic understanding. Accuracy > speed. |
| generate-agent | Sonnet | Quality generation needs balanced reasoning. Good output quality. |

### Skill Auto-Activation

Skills load dynamically based on Claude's semantic understanding:

```
User: /cco-audit --security

Claude detects:
- "security" keyword → loads Security skill
- Python files found → loads Python-specific checks
- Flask detected → loads web security patterns

Skills activated:
- cco-skill-security-owasp-xss-sqli-csrf
- cco-skill-ai-security-promptinjection-models
```

No manual skill selection needed. Claude matches context to relevant skills automatically.

---

## Quick Start

### Installation

**Simplest Method (Works Everywhere):**

```bash
# Install
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git

# Setup
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
   - Creates `~/.claude/commands/` (commands)
   - Creates `~/.claude/principles/` (principles)
   - Creates `~/.claude/skills/` (skills)
   - Creates `~/.claude/agents/` (agents)
   - Generates `~/.claude/CLAUDE.md` (principle markers)
3. Done! Commands available in all projects immediately via Claude Code

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

## Core Commands (Pain-Point Priority)

### Discovery (Know Your Problems)

**`/cco-status`** - Installation health check
- Verify CCO setup
- Show available skills and agents
- Quick start guidance

**`/cco-help`** - Full command reference
- All commands with examples
- Pain-point focus
- Workflow recommendations

### Critical Action (Fix Your Problems)

**`/cco-audit`** - Comprehensive issue detection ⭐ START HERE
- **Quick mode:** `--quick` (fast health assessment with scores, ~5 min)
- **Pain #1:** `--security` (OWASP, AI security, supply chain)
- **Pain #2:** `--tech-debt` (dead code, complexity)
- **Pain #3:** `--ai-security` (prompt injection, hallucinations)
- **Pain #4:** `--tests` (coverage, pyramid, isolation)
- **Pain #6:** `--integration` (imports, dependencies)
- Plus: code-quality, docs, database, observability, monitoring, cicd, containers, supply-chain, migrations, performance, architecture, git
- **Agent:** cco-agent-audit (Haiku - fast & cheap)
- **Impact:** Find all issues in 1-2 minutes

**`/cco-fix`** - Auto-fix detected issues
- Same categories as audit
- Safe fixes auto-applied (parameterize SQL, remove dead code, externalize secrets)
- Risky fixes require approval (CSRF protection, auth changes)
- Auto-runs audit if needed
- **Agent:** cco-agent-fix (Sonnet - accurate)
- **Impact:** Fix issues automatically

**`/cco-generate`** - Create missing components
- **Pain #4:** `--tests` (unit + integration)
- **Pain #7:** `--openapi` (complete API spec)
- Also: `--contract-tests`, `--load-tests`, `--chaos-tests`, `--cicd`, `--dockerfile`, `--migration`, `--monitoring`, `--logging`, `--slo`, and more
- **Agent:** cco-agent-generate (Sonnet - quality)
- **Impact:** Generate comprehensive tests and complete API documentation

### Productivity (Save Time)

**`/cco-optimize`** - Performance optimization with metrics
- **Pain #5:** `--database` (query profiling, execution times)
- **Pain #5:** `--docker` (image size, build time)
- **Pain #5:** `--bundle` (frontend bundle size)
- **Pain #5:** `--performance` (response times, bottlenecks)
- Measures before/after metrics for all optimizations
- **Agent:** cco-agent-fix (Sonnet)
- **Impact:** Faster queries, smaller images, measurable improvements
- **Note:** For code cleanup use `/cco-fix --tech-debt`

**`/cco-commit`** - Semantic commits
- AI-generated commit messages
- Atomic commit recommendations
- **Pain #5:** Better git workflow
- **Impact:** Faster, more consistent commits

**`/cco-implement`** - Feature development with TDD
- Test-Driven Development approach
- Auto-skill selection based on feature type
- High test coverage target
- **Pain #1 + #4:** Security-first + tests-first
- **Impact:** Production-ready features with comprehensive tests

### Management

**`/cco-update`** - Update to latest version
- One command updates all projects instantly
- **Impact:** Zero maintenance across projects

**`/cco-remove`** - Clean uninstall
- Complete transparency
- **Impact:** Zero project pollution

---

## Architecture & Benefits

### Zero Pollution

**Global Storage (`~/.claude/`):**
- **Commands** - Core functionality
- **Principles** - Claude guidelines + universal + project
- **Skills** - Auto-activate on demand
- **Agents** - Parallel execution (audit/Haiku, fix/Sonnet, generate/Sonnet)
- **CLAUDE.md** - Principle markers

**Project Storage:**
- **ZERO files created** in your projects
- All CCO files live globally
- No `.cco/` or per-project configs

**Benefits:**
- One update → all projects get it instantly
- No config drift between projects
- Clean repositories (CCO leaves no trace)
- Share setup across unlimited projects

### Progressive Loading (On-Demand Context)

**Always Loaded (baseline principles):**
- Claude Guidelines (C_*): Token optimization, parallel agents, efficient file ops, honest reporting, native tools, project context discovery
- Universal (U_*): Evidence-based verification, DRY, minimal touch, no overengineering

**Auto-Activated Skills:**
Skills load on-demand when Claude detects relevance:
- **Security:** OWASP, AI security, supply chain, K8s, privacy
- **Testing:** Test pyramid, API testing
- **Database:** Optimization, migrations
- **Observability:** Metrics, logging, incidents
- **CI/CD:** Gates, deployments
- **Code Quality:** Refactoring, content
- **API:** REST versioning & security
- **Documentation:** API/OpenAPI/ADR/runbooks
- **Git:** Branching, versioning
- **Performance:** Frontend, resilience
- **Architecture:** Microservices, event-driven
- **Mobile:** Offline/battery
- **DevEx:** Onboarding/tooling

**Context Efficiency:** Only baseline principles loaded initially. Skills activate when needed, not upfront. This keeps context focused on current task.

### Key Features

**Project Context Discovery:**
- Optional analysis of project documentation (README, CONTRIBUTING, ARCHITECTURE)
- Haiku sub-agent extracts project context without consuming main context
- Ensures findings/fixes align with project goals and conventions

**Full Control Mode (Audit):**
- Three modes: Quick Presets, Category Mode, Full Control
- Full Control shows all available checks with applicability status
- Individual check selection for maximum precision

**YAML Frontmatter:**
- All commands/agents include structured metadata
- Command Discovery Protocol for semantic matching
- Enables intelligent command recommendations

### Universal Principles for CCO Components

**All commands, skills, agents, and principles MUST follow these rules:**

#### 1. No Hardcoded Examples
AI models may interpret hardcoded examples as real data and use them literally.

```python
# ❌ BAD: Hardcoded (AI might use as-is)
"file": "src/auth/login.py", "line": 45

# ✅ GOOD: Dynamic placeholders
"file": "{FILE_PATH}", "line": "{LINE_NUMBER}"
```

#### 2. Native Claude Code Tools for All Interactions
All user interactions must use native tools (AskUserQuestion, etc.).

```python
# ❌ BAD: Text-based prompts
print("Select option (1/2/3): ")

# ✅ GOOD: Native tool
AskUserQuestion({
  questions: [{
    question: "Which checks to run?",
    header: "Audit",
    multiSelect: true,
    options: [...]
  }]
})
```

#### 3. MultiSelect with "All" Option
Any question with multiple choices must be multiSelect with "All" option.

```python
options: [
  {label: "All", description: "Select all options"},
  {label: "Security", description: "..."},
  {label: "Testing", description: "..."},
]
# If "All" selected → all other options are default selected
```

#### 4. 100% Honesty - No False Claims
- Never claim "fixed" unless change verified
- Never say "impossible" if technically possible
- Never claim "generated" unless file exists
- Report exact truth, nothing more or less

```python
# Accurate outcome categories
OUTCOMES = {
    "fixed": "Applied and verified",
    "needs_decision": "Multiple approaches - user chooses",
    "needs_review": "Complex - requires human verification",
    "requires_migration": "DB change - needs migration script",
    "impossible_external": "Issue in third-party code",
}
```

#### 5. Complete Accounting
Every item must have a disposition. Totals must match.

```python
# MUST verify: fixed + skipped + cannot_fix = total
assert len(fixed) + len(skipped) + len(cannot_fix) == total_issues
```

#### 6. Best UX with Highest Quality
- Explicit phase transitions (start/complete announcements)
- Consistent counts (single source of truth)
- Progressive disclosure (simple start, detail on demand)
- Real-time feedback (streaming, not batch)

#### 7. Token Optimization
- Minimize context usage without sacrificing quality
- Grep before Read
- Use offset+limit for large files
- Targeted reads, not full file dumps

#### 8. Unlimited Sub-Agents for Concrete Benefit
Use as many sub-agents as needed when they provide concrete benefit.

```python
# Parallel agents for independent tasks
Task(model="haiku", prompt="Scan security...")
Task(model="haiku", prompt="Scan testing...")
Task(model="haiku", prompt="Scan database...")
# All run in parallel → faster, better results
```

#### 9. Universal + Claude Principle Compliance
All components must align with:
- **U_*** principles (Evidence-based, DRY, Minimal touch, No overengineering)
- **C_*** principles (Context window, Cross-platform, Efficient file ops, Follow patterns)

---

### Agent Orchestration & Model Selection

**3 Specialized Agents:**
- **audit-agent** (Haiku) - Fast scanning, pattern detection
- **fix-agent** (Sonnet) - Accurate code modifications
- **generate-agent** (Sonnet) - Quality code generation

**Agent Format (per SYNTAX.md + CCO extensions):**
```yaml
---
name: agent-name                # Required (lowercase-with-hyphens)
description: When to use...     # Required
tools: Grep, Read, Bash         # Optional (Claude Code spec)
model: haiku                    # Optional (haiku/sonnet/opus)
category: analysis              # CCO extension
metadata:                       # CCO extension
  priority: high
  agent_type: scan
skills_loaded: as-needed        # CCO extension
use_cases:                      # CCO extension
  project_maturity: [all]
---
```

**Model Selection Strategy:**

- **Haiku (Fast & Cheap):** Pattern matching, simple scans
  - Integration checks, dependency scanning
  - Git workflow quality, container rule checks

- **Sonnet (Accurate):** Semantic analysis, code changes
  - Security vulnerabilities (SQL injection, XSS)
  - Architecture analysis, performance optimization
  - All code generation and fixes

**Parallel Execution Example:**
```python
# Security audit with parallel agents
Task(model="haiku", prompt="Scan SQL injection patterns...")
Task(model="haiku", prompt="Scan hardcoded secrets...")
Task(model="haiku", prompt="Check dependency CVEs...")
# All run in parallel → faster execution
```

---

## Configuration

CCO uses a zero-configuration approach by design. All settings are optimized for production use.

### Storage Locations

| Location | Contents | Purpose |
|----------|----------|---------|
| `~/.claude/commands/` | Command files (cco-*.md) | Slash commands for Claude Code |
| `~/.claude/principles/` | Principle files (U_*, C_*, P_*) | Guidelines and best practices |
| `~/.claude/skills/` | Skill files (cco-skill-*.md) | Domain-specific knowledge |
| `~/.claude/agents/` | Agent files (cco-agent-*.md) | Specialized AI agents |
| `~/.claude/CLAUDE.md` | Principle markers | Links principles to Claude |

### Built-in Defaults

**Thresholds (constants.py):**
- Test coverage targets: 50% (minimum) → 80% (good) → 90% (excellent)
- Codebase size: <1000 files (small), <5000 (medium), 5000+ (large)
- Command timeout: 300 seconds default

**Model Selection:**
- audit-agent: Haiku (fast scanning)
- fix-agent: Sonnet (accurate modifications)
- generate-agent: Sonnet (quality output)

### Customization Options

**Override via Environment Variables:**
```bash
# Example: Set custom timeout
export CCO_TIMEOUT=600

# Example: Set verbose mode
export CCO_VERBOSE=1
```

**Override via Command Flags:**
```bash
# Specify categories explicitly
/cco-audit --security --tests

# Run in quick mode (fast health assessment)
/cco-audit --quick
```

### What CCO Does NOT Touch

- **Your project files** - Zero pollution, nothing added to your repo
- **Claude Code settings** - Works alongside existing Claude configuration
- **Other tools** - No conflicts with linters, formatters, or CI/CD

### Verifying Configuration

```bash
# Check CCO installation status
/cco-status

# Shows:
# - Installed commands
# - Available skills
# - Agent configuration
# - Version info
```

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
• SQL Injection in api/users.py:45
  db.execute(f"SELECT * FROM users WHERE id = {user_id}")
  → Use parameterized query

HIGH (2):
• Hardcoded secret in config.py:12
  SECRET_KEY = "mysecretkey123"
  → Move to environment variable

• Missing CSRF protection in api/auth.py:78
  → Add CSRF token validation

MEDIUM (1):
• Debug mode enabled in app.py:5
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
✓ api/users.py:45 - Parameterized SQL query
  Before: db.execute(f"SELECT * FROM users WHERE id = {user_id}")
  After:  db.execute("SELECT * FROM users WHERE id = :id", {"id": user_id})

✓ config.py:12 - Externalized secret
  Before: SECRET_KEY = "mysecretkey123"
  After:  SECRET_KEY = os.environ.get("SECRET_KEY")
  Note: Add SECRET_KEY to your .env file

Risky Fixes (need approval):
────────────────────────────
? api/auth.py:78 - Add CSRF protection
  This requires adding middleware and updating forms.
  Apply this fix? [y/n]

Skipped:
────────
• app.py:5 - Debug mode
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
• Debug mode enabled in app.py:5
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
