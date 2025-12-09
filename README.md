# ClaudeCodeOptimizer

A process and rules layer for Claude Code in the Opus 4.5 era.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/claudecodeoptimizer.svg)](https://pypi.org/project/claudecodeoptimizer/)
[![Claude 4 Best Practices](https://img.shields.io/badge/Claude_4-Best_Practices-blueviolet.svg)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

> Claude already knows how to code. **CCO adds safety, approval, and consistency.**

![CCO Environment](docs/screenshots/environment.png)
*CCO lives directly inside Claude Code, no extra UI.*

---

## Quickstart

```bash
pip install claudecodeoptimizer && cco-setup
```

Inside Claude Code:
```
/cco-tune      # Auto-detect your project, confirm once
/cco-health    # See your scores
```

**That's it.** Start coding with safety nets in place.

---

## What CCO Does

| Layer | What It Adds | Example |
|-------|--------------|---------|
| **Pre-** | Safety checks before action | Git status, dirty state handling |
| **Process** | Standardized workflows | Approval flow, priority classification |
| **Post-** | Verification and reporting | `Applied: N \| Skipped: N \| Failed: N` |
| **Context** | Project-aware behavior | Scale-adjusted thresholds, stack-specific checks |

## What CCO Does NOT Do

- **Teach Claude to code** - Opus 4.5 already knows
- **Replace your judgment** - Every change requires approval
- **Add overhead** - Rules are guidance, not blockers
- **Lock you in** - Export to AGENTS.md anytime

---

## Dynamic Context Injection

CCO commands use Claude Code's `!` backtick syntax for **real-time context at load time**:

```markdown
## Context
- Git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Project type: !`grep "^Type:" ./CLAUDE.md`
```

### How It Works

| Traditional | With Dynamic Context |
|-------------|---------------------|
| 1. Load command | 1. Load command |
| 2. AI calls `git status` tool | 2. Context **already injected** |
| 3. Wait for response | 3. AI starts immediately |
| 4. AI processes result | |
| 5. AI continues | |

### Benefits

| Benefit | Description |
|---------|-------------|
| **Speed** | No tool call round-trip, context ready instantly |
| **Accuracy** | AI sees real data, no assumptions or guessing |
| **Token savings** | Eliminates "Let me check..." dialogue |
| **Reduced hallucination** | Facts over inference |

*Inspired by official Claude Code command patterns.*

---

## Rules

CCO uses a 4-category rules system:

| Category | Scope | Loading |
|----------|-------|---------|
| **Core** | Fundamental principles | Always active in CLAUDE.md |
| **AI** | Model agnostic behavior | Always active in CLAUDE.md |
| **Tools** | CCO command/agent mechanisms | Loaded when commands/agents run |
| **Adaptive** | Stack-based rules pool | Only matching rules selected per project |

**Counting:** `grep -c "| \* " <file>` - each rule row starts with `| * `

Run `/cco-tune` to see which adaptive rules apply to your project.

### Categories Explained

- **Core** - Fundamental software principles: DRY, Fail-Fast, Clean Code, Security, Testing
- **AI** - AI behavior patterns: Read First, No Hallucination, Semantic Density
- **Tools** - CCO workflow: Approval Flow, Fix Workflow, Safety Classification
- **Adaptive** - Stack-based: Frontend accessibility, API rules, Container security

*[Full rules documentation](docs/rules.md)*

---

## Commands

### Base Commands

| Command | Purpose |
|---------|---------|
| `/cco-tune` | Project tuning: detection + configuration + export |
| `/cco-health` | Metrics dashboard with trends and actionable next steps |
| `/cco-audit` | Security + code quality gates with prioritized fixes |
| `/cco-review` | Architecture analysis with fresh perspective |
| `/cco-research` | Multi-source research with reliability scoring |
| `/cco-optimize` | Cleanliness + efficiency improvements |
| `/cco-generate` | Convention-following generation |
| `/cco-refactor` | Safe structural changes with rollback |
| `/cco-commit` | Quality-gated atomic commits |

### Meta Commands

| Command | Purpose | Orchestrates |
|---------|---------|--------------|
| `/cco-release` | Pre-release workflow | audit + optimize + review + verify |
| `/cco-checkup` | Regular maintenance | health + audit --smart + optimize --hygiene |

### /cco-audit Features

- **Security Checks** - OWASP patterns, secrets, CVEs, dependency vulnerabilities
- **Input Validation** - Entry point analysis, validation gap detection
- **Type Coverage** - Missing annotations, any/unknown usage
- **Test Quality** - Flaky tests, coverage gaps, edge case detection
- **Doc-Code Mismatch** - Detect when documentation doesn't match implementation
- **Self-Compliance** - Check against project's own stated rules
- **Smart Mode** - Auto-detect applicable checks based on project context

### /cco-research Features

- **Tiered Reliability Scoring** - 6-tier system (T1-T6) with 0-100 scores
- **Dynamic Modifiers** - Freshness, engagement, author credibility, cross-verification
- **Contradiction Detection** - Identifies conflicting information across sources
- **Consensus Mapping** - Weighted agreement analysis by source tier
- **Bias Detection** - Flags vendor self-promotion, sponsored content
- **AI Synthesis** - Confidence-rated recommendations with reasoning and caveats

### /cco-commit Features

- **Secrets Detection** - Blocks commits with API keys, tokens, passwords, private keys
- **Breaking Change Detection** - Warns on public API changes, prompts for BREAKING CHANGE footer
- **Staged/Unstaged Handling** - Smart analysis based on what user has staged
- **Atomic Grouping** - Auto-groups related changes (impl + tests, renames across files)
- **Large File Warning** - Warns on >1MB files, suggests Git LFS for binaries

### /cco-optimize Features

- **Orphan Detection** - Find unreferenced files, functions, imports, exports
- **Stale Reference Cleanup** - Fix broken imports, dead links, phantom tests
- **Duplicate Detection** - Exact, near-duplicate (>80%), and semantic duplicates
- **Hygiene Mode** - Quick cleanup with `--hygiene` (orphans + stale-refs + duplicates)
- **Cross-File Analysis** - Detect redundant code, obsolete references
- **Consolidation** - Merge overlapping content into single source
- **Metrics** - Before/after comparison with lines, tokens, and KB saved

### /cco-tune Features

- **Unified Flow** - Configure, Remove, and Export in a single command
- **AI Performance Auto-Detection** - Sets thinking/MCP tokens based on project complexity
- **Statusline Configuration** - Full or Minimal mode per project
- **Permission Levels** - Safe, Balanced, Permissive, Full per project
- **Remove Configuration** - Remove any setting (AI Performance, Statusline, Permissions, Rules)
- **Rules Export** - Export to AGENTS.md or CLAUDE.md with selectable content

### /cco-release Features

- **Pre-flight Checks** - Git state, branch, version, changelog, dependencies
- **Quality Gate** - Security, tests, consistency via `/cco-audit --pre-release`
- **Cleanliness** - Orphans, stale refs, duplicates via `/cco-optimize --hygiene`
- **Architecture Review** - Quick gap analysis via `/cco-review --quick`
- **Final Verification** - Full test suite, build, lint, type check
- **Go/No-Go Summary** - Blockers vs warnings, clear next steps

### /cco-checkup Features

- **Health Dashboard** - Quick scores via `/cco-health --brief`
- **Smart Audit** - Context-aware checks via `/cco-audit --smart --auto-fix`
- **Quick Cleanup** - Hygiene fixes via `/cco-optimize --hygiene --auto-fix`
- **Trend Tracking** - Health score changes since last checkup
- **Scheduling** - Weekly recommended for active development

*[Full commands documentation](docs/commands.md)*

---

## Agents

| Agent | Purpose | Mode |
|-------|---------|------|
| **cco-agent-analyze** | Project detection and issue scanning | Read-only |
| **cco-agent-apply** | Execute changes with verification | Write |
| **cco-agent-research** | External source research with reliability scoring | Read-only |

*[Full agents documentation](docs/agents.md)*

---

## Project Tuning

`/cco-tune` is the central configuration command with three action types:

**Configure:**
- Detection & Rules - Scan project, write context to `./CLAUDE.md`
- AI Performance - Set thinking/MCP tokens in `./.claude/settings.json`
- Statusline - Configure status bar (Full or Minimal)
- Permissions - Set permission level (Safe, Balanced, Permissive, Full)

**Remove:**
- Remove any configuration (AI Performance, Statusline, Permissions, Rules)
- Mixed operations supported (e.g., Configure Rules + Remove AI Performance)

**Export:**
- CLAUDE.md - For other Claude Code projects (all rules)
- AGENTS.md - For other AI tools (Tool Rules excluded)

### AI Performance Auto-Detection

Thinking and MCP output tokens are automatically set based on project complexity:

| Setting | Standard | Medium | High |
|---------|----------|--------|------|
| Thinking Tokens | 5000 | 8000 | 10000 |
| MCP Output Tokens | 25000 | 35000 | 50000 |

**Complexity scoring:**
- Microservices, Monorepo → +2 each
- K8s/Helm, ML/AI → +1 each
- Multiple API styles, Large team → +1 each

### Local Settings

All settings are written to `./.claude/settings.json` (project-local):
- AI Performance: `env.MAX_THINKING_TOKENS`, `env.MAX_MCP_OUTPUT_TOKENS`
- Statusline: `statusLine.command`
- Permissions: `permissions.allow`, `permissions.deny`

### Export

Export is integrated into `/cco-tune` main flow. Select CLAUDE.md or AGENTS.md from the Export section.

**What gets exported (user-selectable):**
- Core Rules
- AI Rules
- Tool Rules (CLAUDE.md only)
- Project Context
- Adaptive Rules

**What is NEVER exported:**
- AI Performance settings
- Statusline configuration
- Permission rules

Export reads from installed files (`~/.claude/CLAUDE.md` + `./CLAUDE.md`), not from command specs.

---

## Safety Features

| Feature | What It Does |
|---------|--------------|
| **Git Safety** | Checks status before changes, enables rollback |
| **Approval Flow** | Priority-based (CRITICAL→LOW), safe vs risky classification |
| **Verification** | `Applied: N \| Skipped: N \| Failed: N` accounting |

### Fix Workflow

All fix operations follow: **Analyze → Report → Approve → Apply → Verify**

### Safety Classification

| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |
| Fix linting issues | Delete files |
| Add type annotations | Rename public APIs |

---

## Requirements

- **Python 3.10+** (tested on 3.10–3.14)
- **Claude Code** CLI or IDE extension
- **Zero runtime dependencies** - stdlib only

---

## Installation

```bash
# pip (recommended)
pip install claudecodeoptimizer && cco-setup

# pipx (isolated)
pipx install claudecodeoptimizer && cco-setup

# Development
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git && cco-setup

# Upgrade
pip install -U claudecodeoptimizer && cco-setup
```

### Local Mode (Project-Specific)

```bash
# Install statusline and permissions to current project
cco-setup --local . --statusline full --permissions balanced

# Statusline only
cco-setup --local . --statusline minimal

# Permissions only
cco-setup --local . --permissions safe
```

| Statusline | Description |
|------------|-------------|
| `full` | Project, Branch, Changes, Git status |
| `minimal` | Project, Branch only |

| Permissions | Description |
|-------------|-------------|
| `safe` | Read-only auto-approved, writes require approval |
| `balanced` | Read + lint/test auto-approved, writes require approval |
| `permissive` | Most operations auto-approved, dangerous ops blocked |
| `full` | Maximum auto-approval, only destructive ops blocked |

## Uninstallation

```bash
cco-remove  # Complete removal with confirmation
```

---

## Design Principles

- **Transparency** - Announce before action, progress signals, no silent operations
- **User Control** - Approval required, priority levels, safe vs risky classification
- **Context-Aware** - Project detection drives thresholds and rules
- **Token Efficient** - Semantic density, conditional loading, bounded context

*[Full principles documentation](docs/design-principles.md)*

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
