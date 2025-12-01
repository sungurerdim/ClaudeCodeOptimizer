# ClaudeCodeOptimizer

A process and standards layer for Claude Code.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()

---

## Quickstart

```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

Then inside Claude Code:

```
/cco-tune
/cco-audit --smart
```

---

## What CCO Does

**Claude Code with Opus 4.5 is already powerful.** CCO adds structured workflows on top:

- **Project tuning** - Configure context, AI performance, statusline and permissions in one flow
- **Structured commands** - Same audit categories, same verification patterns, every time
- **Approval flow** - Priority-based suggestions with risk labels, you decide what to apply
- **Context management** - Thinking budget, MCP limits matched to project complexity

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-tune` | Project tuning: context + AI performance + statusline + permissions |
| `/cco-audit` | Categorized checks with prioritized fix suggestions |
| `/cco-review` | Architecture analysis with structured output |
| `/cco-generate` | Generate tests, docs, CI configs following conventions |
| `/cco-health` | Metrics dashboard (coverage, complexity, issues) |
| `/cco-refactor` | Rename/restructure with reference verification |
| `/cco-optimize` | Reduce context size, remove dead code |
| `/cco-commit` | Commit with quality checks |

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

| Setting | Options | Default |
|---------|---------|---------|
| **Thinking Budget** | Off, 1K, 8K, 32K, 64K | Off |
| **MCP Output Limit** | 25K, 50K, 100K | 25K |
| **Prompt Caching** | Enabled, Disabled | Enabled |

**Complexity-based recommendations:**
- Simple projects (solo, <100 users): Thinking Off, MCP 25K
- Medium projects: Thinking 8K, MCP 25K
- Complex projects (10K+ users, legacy): Thinking 32K, MCP 50K

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
| `--ai-security` | Prompt injection, PII handling |
| `--ai-quality` | Hallucinated APIs, AI code patterns |
| `--database` | N+1, indexes, queries |
| `--tests` | Coverage, isolation, flaky |
| `--tech-debt` | Dead code, complexity |
| `--performance` | Caching, algorithms |
| `--hygiene` | TODOs, orphans, hardcoded |
| `--docs` | Docstrings, API docs |
| `--cicd` | Pipeline, quality gates |
| `--containers` | Dockerfile, K8s |
| `--supply-chain` | Dependency CVEs |

**Meta-flags:** `--smart`, `--critical`, `--all`, `--auto-fix`

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

## Standards

CCO adds standards to `~/.claude/CLAUDE.md`:

### Core (Always Apply)

| Section | Purpose |
|---------|---------|
| Workflow | Pre-Operation Safety, Context Read |
| Core | Paths, reference integrity, verification |
| Approval Flow | Priority tabs, risk labels |
| AI-Assisted | Plan→Act→Review workflow |
| Context Management | Thinking, MCP, session hygiene |
| Quality | Code quality, testing, security |

### Conditional (Apply When Relevant)

| Section | Trigger |
|---------|---------|
| Security Extended | Container/K8s, Scale 10K+, PII |
| Architecture | Scale 10K+, microservices |
| Operations | CI/CD detected |
| Performance | Scale 100-10K+ |
| API | REST/GraphQL endpoints |
| Frontend | Frontend frameworks |
| Reliability | SLA requirements |

---

## Structure

After `cco-setup`:

```
~/.claude/
├── commands/
│   └── cco-*.md          # 8 slash commands
├── agents/
│   └── cco-*.md          # 3 specialized agents
└── CLAUDE.md             # Standards
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

```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

Or use the quick installer:

```bash
curl -sSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/quick-install.py | python3
```

## Uninstallation

```bash
cco-remove
pip uninstall claudecodeoptimizer
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
