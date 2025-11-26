# ClaudeCodeOptimizer - Architecture

This document describes CCO's internal architecture, agent orchestration, and CCO Rules.

For installation and usage, see [README.md](README.md).

---

## Table of Contents

- [How CCO Works](#how-cco-works)
- [Architecture & Benefits](#architecture--benefits)
- [Agent Orchestration](#agent-orchestration)
- [Configuration](#configuration)
- [CCO Rules](#cco-rules)

---

## How CCO Works

### Command → Agent Flow

```
User runs command          Agent executes
─────────────────────────────────────────
/cco-audit --security  →   audit-agent (Haiku)
                           - Pattern matching
                           - Fast scanning
                           - Low cost

/cco-fix --security    →   fix-agent (Sonnet)
                           - Semantic analysis
                           - Code modifications
                           - High accuracy

/cco-generate --tests  →   generate-agent (Sonnet)
                           - Quality output
                           - Complete code

/cco-optimize          →   optimize-agent (Sonnet)
                           - CLAUDE.md analysis
                           - Token optimization
                           - Duplication detection
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

n**Flow:** Discovery (detect tech stack) → Audit (classify findings) → Fix (auto-apply safe, request risky) → Generate (create tests/docs with conventions)
### Model Selection Rationale

| Agent | Model | Why |
|-------|-------|-----|
| audit-agent | Haiku | Pattern matching doesn't need deep reasoning. Fast & cheap for scanning. |
| fix-agent | Sonnet | Code modifications need semantic understanding. Accuracy > speed. |
| generate-agent | Sonnet | Quality generation needs balanced reasoning. Good output quality. |

---

## Architecture & Benefits

### Zero Pollution

**Global Storage (`~/.claude/`):**
- **Commands** - Core functionality (cco-*.md)
- **Agents** - Parallel execution (cco-agent-*.md)
- **CLAUDE.md** - Inline CCO Rules (~350 tokens, research-based)
- **Templates** - Customizable template files (*.cco)

**Project Storage:**
- **ZERO files created** in your projects
- All CCO files live globally
- No `.cco/` or per-project configs

**Benefits:**
- One update → all projects get it instantly
- No config drift between projects
- Clean repositories (CCO leaves no trace)
- Share setup across unlimited projects

### Minimal Context Loading

**Always Loaded (~350 tokens):**
- CCO Rules (inline in CLAUDE.md): Cross-platform compatibility, reference integrity, verification protocol, file discovery stages, change safety, scope control

**On-Demand:**
- Commands load when invoked
- Agents spawn when tasks require parallel execution

**Context Efficiency:** Only CCO Rules loaded initially (~350 tokens). Commands and agents activate when needed, not upfront. This keeps context focused on current task.

### Key Features

**Project Context Discovery:**
- Optional analysis of project documentation (README, CONTRIBUTING, ARCHITECTURE)
- Haiku sub-agent extracts project context without consuming main context

### Specialized Agents

- **audit-agent** (Haiku) - Fast scanning, cost-efficient pattern detection
- **fix-agent** (Sonnet) - Accurate code modifications
- **generate-agent** (Sonnet) - Quality code generation
- **optimize-context-usage-agent** (Sonnet) - Context optimization and token reduction with quality preservation

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
| `~/.claude/agents/` | Agent files (cco-agent-*.md) | Specialized AI agents |
| `~/.claude/CLAUDE.md` | CCO Rules (~350 tokens) | Minimal, research-based guidelines |
| `~/.claude/*.cco` | Template files | Customizable templates |

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

## CCO Rules

CCO Rules are minimal (~350 tokens), research-based guidelines that complement Claude Opus 4.5's built-in capabilities. They're injected inline into `~/.claude/CLAUDE.md`.

### Design Philosophy

Based on research into:
- Claude's system prompts and built-in behaviors
- Claude Opus 4.5 capabilities (complex reasoning, Plan Mode, long-horizon tasks)
- Community CLAUDE.md best practices (October-November 2025)
- Anthropic's guidance on brevity and human-readability

**CCO Rules only include what Claude doesn't already do by default.**

### What's Included (~350 tokens)

1. **Cross-Platform Compatibility** - Forward slashes, relative paths, Git Bash commands
2. **Reference Integrity** - Find ALL refs before delete/rename/move/modify
3. **Verification Protocol** - Accounting formula: total = completed + skipped + failed + cannot-do
4. **File Discovery Stages** - files_with_matches → content with -C → Read offset+limit
5. **Change Safety** - Commit before bulk changes, max 10 files per batch
6. **Scope Control** - Define boundaries, one change = one purpose

### What's NOT Included (Claude Already Does This)

- Complex reasoning and tradeoff analysis
- Long-horizon autonomous tasks
- Plan Mode with clarifying questions
- Token-efficient code generation
- No over-engineering, minimal touch, follow patterns
- Professional objectivity and honest reporting

### Component Guidelines

All CCO components (commands, agents) follow these rules:
- **No Hardcoded Examples** - Use placeholders like `{FILE_PATH}`, `{LINE_NUMBER}`
- **Native Tool Interactions** - Use `AskUserQuestion` for user input
- **Complete Accounting** - All items: completed/skipped/failed/cannot-do
- **Token Efficiency** - Grep before Read, targeted reads, parallel operations

## Extension Points

CCO is designed for easy extension:

### Adding New Commands

1. Create `~/.claude/commands/cco-your-command.md`
2. Use YAML frontmatter for metadata
3. Follow command template format

### Adding New Agents

1. Create `~/.claude/agents/cco-agent-your-purpose.md`
2. Specify model selection strategy
3. Define execution patterns

---

## Recent Improvements (Last 24 Hours)

### Quality & Testing
- ✅ **100% Test Pass Rate** - All unit tests fixed and passing
- ✅ **Test Suite Modernization** - Updated to Python 3.11+ syntax
- ✅ **CI/CD Simplification** - Minimal test matrix for alpha stage

### Documentation
- ✅ **Architecture Decision Records** - docs/ADR/ directory with initial ADRs
- ✅ **Operational Runbooks** - docs/runbooks/ with installation, update, troubleshooting guides
- ✅ **PR Template** - Comprehensive checklist with CCO component guidelines

### Code Quality
- ✅ **CCO Rules Migration** - Replaced large principle files with ~350 token inline rules
- ✅ **Research-Based Design** - Rules based on Claude Opus 4.5 capabilities and community best practices
- ✅ **Hardcoded Examples Eliminated** - Full compliance with no-hardcoded-examples guideline
- ✅ **GitIgnore Cleanup** - Removed unnecessary entries

### Features
- ✅ **Context Optimization** - `/cco-optimize --context` for CLAUDE.md duplication elimination
- ✅ **Installation UX** - Before/after file count summary, template tracking
- ✅ **Command Enhancements** - audit, fix, generate, optimize, commit all improved
- ✅ **Context Passing Between Commands** - Built-in command chaining
  - `/cco-audit` → `/cco-fix`: Passes issue list, file paths, severity levels
  - `/cco-audit` → `/cco-generate`: Passes missing components, existing patterns
  - `/cco-fix` → `/cco-generate`: Passes fixed files, needed tests/docs
  - Eliminates duplicate analysis, significantly faster execution

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
