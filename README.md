# ClaudeCodeOptimizer

A process and standards layer for Claude Code in the Opus 4.5 era.

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
- **Add overhead** - Standards are guidance, not blockers
- **Lock you in** - Export to AGENTS.md anytime

---

## Standards

CCO uses a 4-category standards system:

| Category | Scope | Export |
|----------|-------|--------|
| **Universal** | All projects, AI/human agnostic | Both |
| **AI-Specific** | All AI assistants, model agnostic | Both |
| **CCO-Specific** | CCO workflow mechanisms | CLAUDE.md only |
| **Project-Specific** | Selected by /cco-tune based on detection | Both |

| Type | Count |
|------|-------|
| Universal | 38 |
| AI-Specific | 28 |
| CCO-Specific | 48 |
| **Base Total** | **114** |
| Project-Specific Pool | 170 |
| **Total Pool** | **284** |

Run `/cco-tune` to see which project-specific standards apply to your project.

### Categories Explained

- **Universal** - Core software principles: DRY, Fail-Fast, Clean Code, Security, Testing
- **AI-Specific** - AI behavior patterns: Read First, No Hallucination, Semantic Density
- **CCO-Specific** - CCO workflow: Approval Flow, Fix Workflow, Safety Classification
- **Project-Specific** - Stack-based: Frontend accessibility, API standards, Container security

*[Full standards documentation](docs/standards.md)*

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-tune` | Project tuning: detection + configuration + export |
| `/cco-health` | Metrics dashboard with actionable next steps |
| `/cco-audit` | Quality gates with prioritized fixes |
| `/cco-review` | Architecture analysis with recommendations |
| `/cco-optimize` | Efficiency improvements (context, docs, code) |
| `/cco-generate` | Convention-following generation |
| `/cco-refactor` | Safe structural changes with rollback |
| `/cco-commit` | Quality-gated atomic commits |

### /cco-audit Features

- **Orphan Detection** - Find unreferenced files, functions, imports, exports
- **Stale Reference Detection** - Find broken imports, dead links, phantom tests
- **Doc-Code Mismatch** - Detect when documentation doesn't match implementation
- **Self-Compliance** - Check against project's own stated standards
- **Smart Mode** - Auto-detect applicable checks based on project context

### /cco-commit Features

- **Secrets Detection** - Blocks commits with API keys, tokens, passwords, private keys
- **Breaking Change Detection** - Warns on public API changes, prompts for BREAKING CHANGE footer
- **Staged/Unstaged Handling** - Smart analysis based on what user has staged
- **Atomic Grouping** - Auto-groups related changes (impl + tests, renames across files)
- **Large File Warning** - Warns on >1MB files, suggests Git LFS for binaries

### /cco-optimize Features

- **Cross-File Analysis** - Detect duplicates, redundant code, obsolete references
- **Deduplication** - Exact, near-duplicate (>80%), and semantic duplicate detection
- **Consolidation** - Merge overlapping content into single source
- **Metrics** - Before/after comparison with lines, tokens, and KB saved

### /cco-tune Features

- **AI Performance Auto-Detection** - Sets thinking/MCP tokens based on project complexity
- **Statusline Configuration** - Full or Minimal mode per project
- **Permission Levels** - Safe, Balanced, Permissive, Full per project
- **Standards Export** - Export to AGENTS.md for other AI tools

*[Full commands documentation](docs/commands.md)*

---

## Agents

| Agent | Purpose | Mode |
|-------|---------|------|
| **cco-agent-analyze** | Project detection and issue scanning | Read-only |
| **cco-agent-apply** | Execute changes with verification | Write |

*[Full agents documentation](docs/agents.md)*

---

## Project Tuning

`/cco-tune` is the central configuration command:

1. **Detects** your project: stack, type, scale, team size
2. **Selects** relevant Project-Specific standards
3. **Writes** context to `./CLAUDE.md`
4. **Configures** AI settings (thinking tokens, MCP limits)

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

```bash
/cco-tune --export
```

- **AGENTS.md** - For other AI tools (Universal + AI-Specific + Project-Specific)
- **CLAUDE.md** - For Claude Code (includes CCO-Specific)

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
- **Zero Python dependencies** - stdlib only

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
- **Context-Aware** - Project detection drives thresholds and standards
- **Token Efficient** - Semantic density, conditional loading, bounded context

*[Full principles documentation](docs/design-principles.md)*

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
