# ClaudeCodeOptimizer - Architecture

This document describes CCO's internal architecture, agent orchestration, and design principles.

For installation and usage, see [README.md](README.md).

---

## Table of Contents

- [How CCO Works](#how-cco-works)
- [Architecture & Benefits](#architecture--benefits)
- [Agent Orchestration](#agent-orchestration)
- [Configuration](#configuration)
- [Universal Principles](#universal-principles)

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

/cco-slim              →   slim-agent (Sonnet)  →   Context optimization
                           - CLAUDE.md analysis     - Duplication detection
                           - Token optimization     - Quality preservation
                           - Semantic verification  - Content evaluation
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

## Architecture & Benefits

### Zero Pollution

**Global Storage (`~/.claude/`):**
- **Commands** - Core functionality
- **Principles** - Claude guidelines + universal + project (U_*, C_*, P_*)
- **Skills** - Auto-activate on demand
- **Agents** - Parallel execution (audit/Haiku, fix/Sonnet, generate/Sonnet, slim/Sonnet)
- **CLAUDE.md** - Marker-based principle injection (see [ADR-001](docs/ADR/001-marker-based-claude-md.md))

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

**Auto-Activating Skills (26 total):**
Skills load on-demand when Claude detects relevance:
- **Security (5):** OWASP, AI security, supply chain, K8s, privacy
- **Testing (2):** Test pyramid, API testing
- **Database (2):** Optimization, migrations
- **Observability (3):** Metrics, logging, incidents
- **CI/CD (2):** Gates, deployments
- **Code Quality (2):** Refactoring, content
- **Documentation (1):** API/OpenAPI/ADR/runbooks
- **Git (2):** Branching, versioning
- **Performance (2):** Frontend, resilience
- **Architecture (2):** Microservices, event-driven
- **Mobile (1):** Offline/battery
- **DevEx (1):** Onboarding/tooling

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

---

## Agent Orchestration

### Specialized Agents

- **audit-agent** (Haiku) - Fast scanning, cost-efficient pattern detection
- **fix-agent** (Sonnet) - Accurate code modifications
- **generate-agent** (Sonnet) - Quality code generation
- **slim-agent** (Sonnet) - Context optimization and token reduction with quality preservation

### Agent Format

Per SYNTAX.md + CCO extensions:

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

### Model Selection Strategy

- **Haiku (Fast & Cheap):** Pattern matching, simple scans
  - Integration checks, dependency scanning
  - Git workflow quality, container rule checks

- **Sonnet (Accurate):** Semantic analysis, code changes
  - Security vulnerabilities (SQL injection, XSS)
  - Architecture analysis, performance optimization
  - All code generation and fixes

### Parallel Execution Example

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

## Universal Principles

All CCO components (commands, skills, agents, principles) **MUST** follow these rules:

### 1. No Hardcoded Examples

AI models may interpret hardcoded examples as real data and use them literally.

```python
# ❌ BAD: Hardcoded (AI might use as-is)
"file": "src/auth/login.py", "line": 45

# ✅ GOOD: Dynamic placeholders
"file": "{FILE_PATH}", "line": "{LINE_NUMBER}"
```

### 2. Native Claude Code Tools for All Interactions

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

### 3. MultiSelect with "All" Option

Any question with multiple choices must be multiSelect with "All" option.

```python
options: [
  {label: "All", description: "Select all options"},
  {label: "Security", description: "..."},
  {label: "Testing", description: "..."},
]
# If "All" selected → all other options are default selected
```

### 4. 100% Honesty - No False Claims

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

### 5. Complete Accounting

Every item must have a disposition. Totals must match.

```python
# MUST verify: fixed + skipped + cannot_fix = total
assert len(fixed) + len(skipped) + len(cannot_fix) == total_issues
```

### 6. Best UX with Highest Quality

- Explicit phase transitions (start/complete announcements)
- Consistent counts (single source of truth)
- Progressive disclosure (simple start, detail on demand)
- Real-time feedback (streaming, not batch)

### 7. Token Optimization

- Minimize context usage without sacrificing quality
- Grep before Read
- Use offset+limit for large files
- Targeted reads, not full file dumps

### 8. Unlimited Sub-Agents for Concrete Benefit

Use as many sub-agents as needed when they provide concrete benefit.

```python
# Parallel agents for independent tasks
Task(model="haiku", prompt="Scan security...")
Task(model="haiku", prompt="Scan testing...")
Task(model="haiku", prompt="Scan database...")
# All run in parallel → faster, better results
```

### 9. Universal + Claude Principle Compliance

All components must align with:
- **U_*** principles (Evidence-based, DRY, Minimal touch, No overengineering)
- **C_*** principles (Context window, Cross-platform, Efficient file ops, Follow patterns)

**Full Principle Documentation:**

See `~/.claude/principles/` for complete details:
- **U_* (Universal)**: Core development best practices
- **C_* (Claude Guidelines)**: Claude Code-specific optimizations
- **P_* (Project-specific)**: Optional per-project overrides

---

## Performance Characteristics

### Typical Execution Times

| Command | Codebase Size | Time | Model Cost |
|---------|--------------|------|------------|
| `/cco-audit --quick` | Small (<1K files) | ~10s | $0.01 |
| `/cco-audit --security` | Medium (<5K files) | ~30s | $0.05 |
| `/cco-audit --all` | Large (5K+ files) | ~2min | $0.20 |
| `/cco-fix --security` | 10 issues | ~45s | $0.10 |
| `/cco-generate --tests` | 5 files | ~60s | $0.15 |

### Optimization Techniques

1. **Parallel Agent Execution**
   - Independent checks run simultaneously
   - 3-5x faster than sequential scanning

2. **Progressive Context Loading**
   - Only load relevant skills when needed
   - Baseline principles always loaded (~10KB)
   - Skills load on-demand (5-15KB each)

3. **Efficient File Operations**
   - Grep before Read (10x token savings)
   - Targeted reads with offset+limit
   - Pattern-based file discovery

4. **Model Selection**
   - Haiku for pattern matching (5x faster, 10x cheaper)
   - Sonnet for code analysis (balanced)
   - Opus only when strictly necessary (rare)

---

## Extension Points

CCO is designed for easy extension:

### Adding New Skills

1. Create `~/.claude/skills/cco-skill-your-domain.md`
2. Follow skill template format
3. Skills auto-activate via semantic matching

### Adding New Commands

1. Create `~/.claude/commands/cco-your-command.md`
2. Use YAML frontmatter for metadata
3. Follow command template format

### Adding New Agents

1. Create `~/.claude/agents/cco-agent-your-purpose.md`
2. Specify model selection strategy
3. Define execution patterns

### Adding New Principles

1. Create `~/.claude/principles/P_YOUR_PRINCIPLE.md`
2. Follow principle template format
3. Add marker to `~/.claude/CLAUDE.md`

---

## Recent Improvements (Last 24 Hours)

### Quality & Testing
- ✅ **100% Test Pass Rate** - All unit tests fixed and passing
- ✅ **Test Suite Modernization** - Updated to Python 3.11+ syntax
- ✅ **CI/CD Simplification** - Minimal test matrix for alpha stage

### Documentation
- ✅ **Architecture Decision Records** - docs/ADR/ directory with initial ADRs
- ✅ **Operational Runbooks** - docs/runbooks/ with installation, update, troubleshooting guides
- ✅ **PR Template** - Comprehensive checklist with CCO principle compliance

### Code Quality
- ✅ **Unused Code Removal** - Cleaned up principles.py and related tests
- ✅ **Hardcoded Examples Eliminated** - Full compliance with C_NO_HARDCODED_EXAMPLES principle
- ✅ **GitIgnore Cleanup** - Removed unnecessary entries

### Features
- ✅ **Context Optimization** - `/cco-slim` primary focus on CLAUDE.md duplication elimination
- ✅ **Installation UX** - Before/after file count summary, template tracking
- ✅ **Command Enhancements** - audit, fix, generate, slim, optimize, implement, commit all improved
- ✅ **Skill Integration** - Unused skills now properly integrated into commands
- ✅ **Context Passing Between Commands** - C_COMMAND_CONTEXT_PASSING principle implementation
  - `/cco-audit` → `/cco-fix`: Passes issue list, file paths, severity levels
  - `/cco-audit` → `/cco-generate`: Passes missing components, existing patterns
  - `/cco-fix` → `/cco-generate`: Passes fixed files, needed tests/docs
  - Eliminates duplicate analysis, significantly faster execution
  - See [C_COMMAND_CONTEXT_PASSING principle](claudecodeoptimizer/content/principles/C_COMMAND_CONTEXT_PASSING.md)

### Performance
- ✅ **Token Efficiency** - Context-first approach in slim command
- ✅ **Model Selection** - Optimal Haiku/Sonnet/Opus usage per task complexity

## Related Documentation

### Core Documentation
- [README.md](README.md) - Installation and quick start
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [LICENSE](LICENSE) - MIT License

### Architecture Decision Records
- [ADR-001: Marker-based CLAUDE.md System](docs/ADR/001-marker-based-claude-md.md)
- [ADR-002: Zero Pollution Design](docs/ADR/002-zero-pollution-design.md)
- [ADR-003: Progressive Skill Loading](docs/ADR/003-progressive-skill-loading.md)

### Operational Runbooks
- [Installation](docs/runbooks/installation.md)
- [Updates](docs/runbooks/updates.md)
- [Troubleshooting](docs/runbooks/troubleshooting.md)
- [Uninstallation](docs/runbooks/uninstallation.md)

### Development Resources
- [PR Template](.github/PULL_REQUEST_TEMPLATE.md)
- [CI/CD Workflows](.github/workflows/)

---

**Created by Sungur Zahid Erdim** | [GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)
