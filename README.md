# ClaudeCodeOptimizer

A process and standards layer for Claude Code in the Opus 4.5 era.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Claude 4 Best Practices](https://img.shields.io/badge/Claude_4-Best_Practices-blueviolet.svg)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

> **Fully aligned with [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)** - Agentic coding, extended thinking, parallel tools, context management, and design quality standards.

**TL;DR**
- Thin layer on top of Claude Code + Opus 4.5
- Three-layer standards (universal, Claude-specific, project) shaping all Claude workflows—not just `/cco-*` commands and agents
- Risk-based approval flow, no silent changes

---

Claude Code already gives you strong refactors, tests and multi-file edits with Opus-class models.
CCO sits on top of that and adds three things you usually have to build by hand:

1. **Project-aware tuning** with a single `/cco-tune` flow that writes your context and AI settings into `CLAUDE.md`
2. **Standards-driven commands** that all read from one shared `cco-standards.md` file
3. **Risk-based approval flow** so no change is applied silently and git safety checks are always part of the workflow

No servers, no dashboards, no extra dependencies. Just a thin standards layer on top of the tools you already use every day.

---

## Requirements

- **Python 3.10+** (tested on 3.10, 3.11, 3.12, 3.13, 3.14)
- **Claude Code** - CLI or IDE extension
- **Zero Python dependencies** - uses only Python standard library

## Quickstart

```bash
# 1. Install
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git

# 2. Setup (installs commands, agents, standards to ~/.claude/)
cco-setup

# 3. Inside Claude Code, tune for your project
/cco-tune

# 4. Start using
/cco-audit --smart
```

**What each step does:**
| Step | Command | Result |
|------|---------|--------|
| Install | `pip install ...` | Downloads CCO package |
| Setup | `cco-setup` | Copies 8 commands, 3 agents, 85 standards to `~/.claude/` |
| Tune | `/cco-tune` | Detects stack, writes project context + conditional standards to `./CLAUDE.md` |
| Use | `/cco-*` | All commands now follow your project's standards |

---

## Why CCO?

The Claude Code ecosystem is full of powerful workflows: built-in refactors and tests, Opus 4.5 and newer Opus-class models, large orchestration frameworks with many agents and dashboards.

CCO does not try to replace any of that.

Instead, it focuses on one missing layer:
- A **single standards file** that all commands follow
- A **lightweight process layer** for audits, reviews, refactors and generators
- A **predictable approval flow** on top of Claude Code, not instead of it

> All the power of Claude Code + Opus 4.5, plus a small layer that makes it repeatable, auditable and safe across every repo.

---

## How CCO Works

### What CCO Does NOT Do

CCO is not teaching Claude how to code. Opus 4.5 already knows:
- How to write clean, maintainable code
- Security best practices
- Testing patterns
- Refactoring techniques

### What CCO Actually Does

CCO adds **process layers** around what Claude already does well:

| Layer | What It Adds | Example |
|-------|--------------|---------|
| **Pre-** | Safety checks before action | `git status` check, dirty state handling |
| **Process** | Standardized workflows | Approval flow format, priority tabs |
| **Post-** | Verification and reporting | `done + skip + fail = total`, error format |
| **Context** | Project-aware behavior | Scale, team size, data sensitivity → adjusted thresholds |

```
Claude/Opus 4.5 already knows:       CCO adds:
────────────────────────────         ─────────────────────────
• Writing good code                  • Pre: git safety checks
• Security best practices            • Process: approval workflows
• Refactoring patterns               • Post: verification accounting
• Test generation                    • Context: project parameters
```

### Why Explicit Standards?

CCO provides 85 core standards (51 universal + 34 Claude-specific) plus 80 conditional standards selected per-project. Why, if Claude already knows them?

| Benefit | Explanation |
|---------|-------------|
| **Transparency** | Users see exactly what rules apply to their project |
| **Consistency** | Same standards across all projects, every session |
| **Overridability** | Context can adjust thresholds (coverage: 60% solo → 90% enterprise) |
| **Auditability** | Clear reference for code reviews and compliance |
| **Predictability** | No surprises - behavior is documented and reproducible |

---

## Commands

*Ordered by typical workflow: Setup → Observe → Fix → Improve → Create → Change*

| Command | Purpose |
|---------|---------|
| `/cco-tune` | Project tuning: context + AI performance + configuration |
| `/cco-health` | Metrics dashboard with actionable next steps |
| `/cco-audit` | Quality gates with SSOT resolution |
| `/cco-optimize` | AI context, docs, code, performance optimization |
| `/cco-review` | Strategic architecture analysis |
| `/cco-generate` | Convention-following generation |
| `/cco-refactor` | Safe structural changes with rollback |
| `/cco-commit` | Quality-gated atomic commits |

---

## Command Details

### `/cco-tune` - Project Tuning
Central configuration: detects stack, sets AI performance, writes context to CLAUDE.md.

| Feature | Description |
|---------|-------------|
| **Auto-Detection** | Stack, tools, conventions, team size, scale |
| **AI Performance** | Thinking budget, MCP limits, caching |
| **Configuration** | Statusline, permissions (Safe/Balanced/Permissive) |

**Flags:** `--status` (show current), `--update` (force re-detection)

### `/cco-health` - Metrics Dashboard
Single view of project health with actionable next steps.

| Score | Based On |
|-------|----------|
| **Security** | Vulnerabilities found |
| **Tests** | Coverage + quality |
| **Tech Debt** | Complexity, dead code |
| **Self-Compliance** | Alignment with stated rules |

**Flags:** `--focus=X` (security/tests/tech-debt/hygiene/self-compliance)

### `/cco-audit` - Quality Gates
Find issues, resolve inconsistencies, fix with approval.

| Feature | Description |
|---------|-------------|
| **Doc-Code Consistency** | Detect mismatches between documentation and code |
| **SSOT Resolution** | Per-mismatch choice: align code→docs, docs→code, or discuss |
| **Self-Compliance** | Check code against project's own stated rules |
| **Prioritized Fixes** | Critical → High → Medium → Low with file:line |

**Core:** `--security`, `--tech-debt`, `--hygiene`, `--self-compliance`, `--consistency`
**Stack:** `--tests`, `--database`, `--performance`, `--ai-security`, `--ai-quality`, `--docs`, `--cicd`, `--containers`, `--supply-chain`, `--compliance`, `--api-contract`
**Meta:** `--smart`, `--critical`, `--weekly`, `--pre-release`, `--all`, `--auto-fix`

### `/cco-optimize` - Efficiency Optimization
Reduce waste, improve quality, measure impact.

| Category | What It Does |
|----------|--------------|
| **AI Context** | Optimize CLAUDE.md, prompts for max understanding with min tokens |
| **Cross-File** | Detect duplicate/redundant/obsolete content across ALL files |
| **Code Quality** | Apply standards: DRY, complexity, type safety |
| **Performance** | N+1 queries, caching, blocking I/O |

**Categories:** `--context`, `--docs`, `--code-quality`, `--code-efficiency`, `--performance`, `--cross-file`, `--all`
**Modes:** `--conservative`, `--balanced`, `--aggressive`

### `/cco-review` - Strategic Review
Architecture analysis with fresh perspective.

| Phase | Output |
|-------|--------|
| **Map Current State** | Structure, patterns, dependencies, data flow |
| **Gap Analysis** | Intent vs implementation, principle violations |
| **Stack Fitness** | Technology choices vs project needs |
| **Fresh Perspective** | "If building from scratch" recommendations |

**Flags:** `--quick`, `--deep`, `--focus=X`, `--report-only`, `--auto-apply`

### `/cco-generate` - Convention-Following Generation
Generate components that match existing project patterns.

| Type | What It Generates |
|------|-------------------|
| **Tests** | Unit/integration tests (+ contract/load if applicable) |
| **Docs** | Docstrings, README, OpenAPI (if API) |
| **Infra** | CI/CD pipelines, Dockerfile, pre-commit |

**Flags:** `--tests`, `--docs`, `--infra`, `--all`

### `/cco-refactor` - Safe Refactoring
Rename/restructure with reference verification and rollback.

| Feature | Description |
|---------|-------------|
| **Reference Mapping** | Find ALL refs before changing |
| **Ordered Transform** | Definition → types → callers → imports → tests |
| **Verification** | Grep old=0, new=expected after each change |
| **Rollback** | Auto-revert on any failure |

**Operations:** `rename`, `move`, `extract`, `inline`

### `/cco-commit` - Quality-Gated Commits
Pre-commit checks + atomic grouping + traceability.

| Step | What Happens |
|------|--------------|
| **Quality Gates** | Format → Lint → Test (stop on failure) |
| **Atomic Grouping** | Related changes together, unrelated separate |
| **Commit Order** | Types → Core → Dependent → Tests → Docs |

**Flags:** `--dry-run`, `--single`, `--skip-checks`

---

## Agents

Specialized subagents for CCO commands:

| Agent | Purpose | Tools |
|-------|---------|-------|
| **cco-agent-detect** | Structured project detection (JSON output) | Glob, Read, Grep, Bash |
| **cco-agent-scan** | Read-only analysis with file:line findings | Glob, Read, Grep, Bash |
| **cco-agent-action** | Write operations with verification accounting | All tools |

**Detection Scopes:** `tools` (2s) → `technical` (5s) → `full` (10s)

**Action Accounting:** `done + skip + fail + cannot_do = total`

---

## Project Tuning

`/cco-tune` is the central configuration command. It combines:

1. **Health Check** - CCO installation + config validation
2. **Project Context** - Purpose, team, scale, data sensitivity, stack
3. **AI Performance** - Thinking budget, MCP limits, caching
4. **Configuration** - Statusline and permission settings

### Context Questions

| Call | Questions |
|------|-----------|
| Core | Purpose, Team, Scale, Data |
| Technical | Stack, Type, Database, Rollback |
| Approach | Maturity, Breaking Changes, Priority |
| AI Performance | Thinking, MCP Limit, Caching |

### AI Performance Settings

| Setting | Env Variable | Default |
|---------|--------------|---------|
| **Extended Thinking** | `MAX_THINKING_TOKENS` | Off |
| **MCP Output Limit** | `MAX_MCP_OUTPUT_TOKENS` | 25000 |
| **Prompt Caching** | `DISABLE_PROMPT_CACHING` | Enabled |

Set in `~/.claude/settings.json`:
```json
{
  "env": {
    "MAX_THINKING_TOKENS": "16000",
    "MAX_MCP_OUTPUT_TOKENS": "50000"
  }
}
```

**When to increase thinking budget:**
- Off: simple questions, file lookups
- 8K-16K: standard coding, single-file changes
- 16K-32K: multi-file refactors, complex debugging
- 32K+: algorithm design, deep multi-step analysis

**When to increase MCP limit:**
- Check with `/doctor` - shows "Large MCP tools context" warning if needed

### Stored Format

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: {rollback}
Maturity: {maturity} | Breaking: {breaking} | Priority: {priority}

## AI Performance
Thinking: {budget} | MCP: {limit} | Caching: {on|off}

## Guidelines
- {context-specific guidance}

## Operational
Tools: {format}, {lint}, {test}
Applicable: {checks list}
Not Applicable: {excluded checks}

## Auto-Detected
Structure: {monorepo|single-repo} | Hooks: {pre-commit|none} | Coverage: {N%}
License: {type} | Secrets: {yes|no} | Outdated: {N deps}
<!-- CCO_CONTEXT_END -->
```

---

## Audit Categories

| Flag | Checks |
|------|--------|
| `--security` | OWASP patterns, secrets, CVE patterns |
| `--consistency` | Doc-code mismatches with SSOT resolution |
| `--self-compliance` | Project's own stated rules |
| `--tech-debt` | Dead code, complexity |
| `--hygiene` | TODOs, orphans, hardcoded |
| `--tests` | Coverage, isolation, flaky |
| `--performance` | Caching, algorithms |
| `--database` | N+1, indexes, queries |
| `--ai-security` | Prompt injection, PII handling |
| `--ai-quality` | Hallucinated APIs, AI code patterns |
| `--docs` | Docstrings, API docs |
| `--cicd` | Pipeline, quality gates |
| `--containers` | Dockerfile, K8s |
| `--supply-chain` | Dependency CVEs |

**Meta-flags:** `--smart` (all applicable), `--critical`, `--weekly`, `--pre-release`, `--all`, `--auto-fix`

---

## Statusline

Optional status display with git integration:

```
 project/src       |   user   |  2.1MB  | CC 2.0.55 |  Opus 4.5
┌───────────────────┬──────────┬─────────┬───────────┬────────────┐
│ main              │ Conf 0   │ Stash 2 │ Ahead 3   │ Last 02:45 │
├───────────────────┼──────────┼─────────┼───────────┼────────────┤
│ Unstaged +42 -18  │ edit 3   │ new 2   │ del 0     │ move 0     │
│ Staged   +15 -3   │ edit 1   │ new 1   │ del 0     │ move 0     │
└───────────────────┴──────────┴─────────┴───────────┴────────────┘
```

---

## Permission Levels

| Level | Model | Use Case |
|-------|-------|----------|
| **Safe** | Whitelist | Maximum security, manual approval |
| **Balanced** | Whitelist | Normal workflow (recommended) |
| **Permissive** | Blacklist | Minimal prompts, trusted projects |

### Always Denied

| Category | Blocked |
|----------|---------|
| Destructive | `rm -rf /`, `format`, `mkfs`, `dd if=` |
| Privilege | `sudo`, `su`, `chmod 777` |
| Git Dangerous | `git push --force`, `git reset --hard` |
| Sensitive | `~/.ssh/`, `~/.aws/`, `**/.env*` |

---

## Standards Architecture

CCO uses a three-category standards system for minimal context usage:

```
Source Files                              Destination
────────────────────────────────────────────────────────────────
cco-standards.md                        → ~/.claude/CLAUDE.md
├── Universal Standards (51 rules)         (loaded for ALL projects)
│   └── Quality (code, testing, security) + Docs + Workflow
└── Claude-Specific Standards (34 rules)
    └── CCO Workflow, Core, Approval, Prompt Engineering, Frontend Gen, Context

cco-standards-conditional.md            → ./CLAUDE.md (filtered)
└── Conditional Standards (80 rules)       (only matching rules)
    └── Security, Architecture, API, Frontend, etc.
```

### Universal Standards (51 rules)
*Software engineering best practices - any project, any AI*

| Section | # | Standards |
|---------|---|-----------|
| **Code** | 19 | Fail-Fast, DRY, No Orphans, Type Safety, Complexity, Tech Debt, Maintainability, No Overengineering, Minimal Touch, General Solutions, Clean Code, Immutability, Profile First, Version, Paths, No Unsolicited Files, Cleanup, Timeouts, Retry |
| **Testing** | 7 | Coverage, Pyramid, Integration, CI Gates, Isolation, TDD, Test Integrity |
| **Security** | 6 | Input Validation, SQL Params, Secrets, XSS, OWASP, Dependencies |
| **Docs** | 5 | README, CHANGELOG, API Docs, ADR, Comments |
| **AI Context** | 5 | Semantic Density, Structured Format, Front-load Critical, Scannable Hierarchy, No Filler |
| **Workflow** | 9 | Read First, Review Conventions, Reference Integrity, Verification, Plan-Act-Review, Decompose, No Vibe Coding, Challenge, No Example Fixation |

### Claude-Specific Standards (34 rules)
*Claude Code architecture, tools, and features*

| Section | # | Standards |
|---------|---|-----------|
| **CCO Workflow** | — | Pre-Op Safety, Context Read, Safety Classification *(process framework)* |
| **Core** | 4 | Exclusions, Error Format, Parallel Tools, Moderate Triggers |
| **Approval Flow** | 5 | Single Call, Priority Headers, Risk Format, MultiSelect, All Access |
| **Prompt Engineering** | 5 | Positive Framing, Action vs Suggest, Contextual Motivation, Thinking Escalation, Subagent Delegation |
| **Frontend Gen** | 6 | Typography, Color & Theme, Motion, Backgrounds, Distinctive Design, Avoid Clichés |
| **Context Mgmt** | 14 | Extended Thinking (Off/8K-32K+), MCP Output Limit, Don't Stop Early, Work Incrementally, Track State, Before /compact, Between Tasks, After Fresh Start |

### Conditional Standards (80 rules)
*Domain-specific rules - selected by /cco-tune, written to local CLAUDE.md only*

| Conditional | # | Trigger | Standards |
|-------------|---|---------|-----------|
| **Security+** | 12 | Container/K8s, 10K+, PII | Privacy, Encryption, Zero Disk, Auth, Rate Limit, Supply Chain, AI Security, Container, K8s, Policy-as-Code, Audit Log, Incident Response |
| **Architecture** | 9 | 10K+, microservices | Event-Driven, Service Mesh, DI, Dependency Rule, Circuit Breaker, Bounded Contexts, API Versioning, Idempotency, Event Sourcing |
| **Operations** | 10 | CI/CD detected | Zero Maintenance, Config as Code, IaC + GitOps, Observability, Health, Graceful Shutdown, Blue/Green, Canary, Feature Flags, Incremental Safety |
| **Performance** | 7 | Scale 100-10K+ | DB Indexing, Async I/O, Caching, Cache Hit, Connection Pool, Lazy Load, Compression |
| **Data** | 3 | Database detected | Backup, Migrations, Retention |
| **API** | 7 | REST/GraphQL | REST Methods, Pagination, Docs, Errors, GraphQL Limits, Contract, CORS |
| **Frontend** | 11 | Frontend frameworks | WCAG 2.2, Semantic HTML, ARIA, Keyboard, Screen Reader, Contrast, Focus, A11y Testing, Core Web Vitals, Bundle Size, Lazy Loading |
| **i18n** | 5 | Multi-language | Externalized, Unicode, RTL, Locale, Pluralization |
| **Reliability** | 4 | SLA requirements | Chaos, Resilience, Bulkhead, Fallback |
| **Cost** | 4 | Cloud/Container | FinOps, Tagging, Auto-Scale, Green |
| **DX** | 5 | Team 2-5+ | Local Parity, Fast Feedback, Self-Service, Golden Paths, Runbooks |
| **Compliance** | 3 | SOC2/HIPAA/PCI | License, Frameworks, Classification |

**Result:** Only relevant rules load into context. A CLI project won't carry Frontend or API standards.

---

## Structure

After `cco-setup`:

```
~/.claude/                              # Global (all projects)
├── commands/
│   └── cco-*.md                        # 8 slash commands
├── agents/
│   └── cco-*.md                        # 3 specialized agents
├── statusline.js                       # Optional statusline
├── settings.json                       # AI performance + permissions
└── CLAUDE.md                           # 85 rules (51 universal + 34 Claude-specific)

./CLAUDE.md                             # Local (per project, after /cco-tune)
├── CCO_CONTEXT_START
│   ├── Strategic Context               # Purpose, team, scale, stack
│   ├── AI Performance                  # Thinking, MCP, caching
│   ├── Guidelines                      # Project-specific rules
│   ├── Operational                     # Tools, conventions
│   ├── Auto-Detected                   # CI/CD, coverage, flags
│   └── Conditional Standards           # 0-80 rules (filtered by project type)
└── CCO_CONTEXT_END
```

---

## Usage Examples

```bash
# Initial setup
/cco-tune                       # Full interactive tuning

# Find and fix issues
/cco-audit --smart              # Auto-detect, find issues, offer fixes
/cco-audit --security           # Security-focused audit
/cco-audit --critical           # security + tests + database

# Generate components
/cco-generate --tests           # Unit/integration tests
/cco-generate --cicd            # CI/CD pipelines

# Safe refactoring
/cco-refactor rename oldName newName

# Strategic review
/cco-review                     # Full architecture review
```

---

## Requirements

- Python 3.11+
- Claude Code

---

## Installation

**Standard (pip):**
```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

**Alternative (pipx - isolated environment):**
```bash
pipx install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

**One-liner:**
```bash
curl -sSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/quick-install.py | python3
```

## Uninstallation

> **Note:** `pip uninstall` only removes the Python package. It does NOT remove files from `~/.claude/`. Use `cco-remove` for complete cleanup.

```bash
# Complete removal (recommended)
cco-remove          # Removes commands, agents, standards from ~/.claude/
                    # Also uninstalls the Python package (with confirmation)

# Manual removal
pip uninstall claudecodeoptimizer   # Package only
rm ~/.claude/commands/cco-*.md      # Commands
rm ~/.claude/agents/cco-*.md        # Agents
# Edit ~/.claude/CLAUDE.md to remove CCO_STANDARDS section
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
