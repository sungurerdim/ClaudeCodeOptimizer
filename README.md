# ClaudeCodeOptimizer

[![PyPI](https://img.shields.io/pypi/v/claudecodeoptimizer.svg)](https://pypi.org/project/claudecodeoptimizer/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code 2.0+](https://img.shields.io/badge/Claude_Code-2.0+-00A67E.svg)](https://github.com/anthropics/claude-code)

**A process and rules layer for Claude Code** — adds safety, approval workflows, and stack-specific best practices.

![CCO Environment](docs/screenshots/environment.png)

## Quick Start

```bash
pip install claudecodeoptimizer && cco-install
```

Then in Claude Code:
```
/cco-config    # Detect your project, configure settings
```

**Done.** Your project now has safety nets and domain-specific rules active.

## Why CCO?

| Without CCO | With CCO |
|-------------|----------|
| Claude applies generic patterns | Claude applies **domain-specific best practices** |
| No pre-action safety checks | Git status check, approval flow, clean state for rollback |
| Silent changes | `Applied: 5 | Skipped: 2 | Failed: 0` accounting |
| "Add caching somewhere" | "Use TTL + invalidation for this data fetch" |

**CCO doesn't teach Claude to code** — Opus 4.5 already knows. CCO adds the safety layer between intent and action.

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-config` | Project setup: detection + settings + export |
| `/cco-status` | Health dashboard with scores |
| `/cco-optimize` | Security + Quality + Hygiene fixes |
| `/cco-review` | Architecture analysis |
| `/cco-commit` | Quality-gated atomic commits |
| `/cco-research` | Multi-source research with reliability scoring |
| `/cco-preflight` | Pre-release workflow |
| `/cco-checkup` | Regular maintenance |

## Rules System

**1791 rules** organized in 4 categories:

| Category | Count | When Loaded |
|----------|-------|-------------|
| Core | 73 | Always (fundamental principles) |
| AI | 37 | Always (behavior patterns) |
| Tools | 107 | On-demand (CCO workflows) |
| Adaptive | 1574 | Per-project (stack-specific) |

<details>
<summary><b>Supported Stacks</b></summary>

**Languages:** Python, TypeScript, JavaScript, Go, Rust, Java, Kotlin, Swift, C#, Ruby, PHP, Elixir + 15 more

**Frameworks:** React, Vue, Angular, Svelte, Next.js, Django, FastAPI, Express, NestJS, Rails + 100 more

**Infrastructure:** Docker, Kubernetes, Serverless, Monorepo (nx/turbo), CI/CD

**Specialized:** ML/AI, Game Dev (Unity/Unreal/Godot), Blockchain, IoT, XR

</details>

## Installation

**Requirements:** Python 3.10+ • Claude Code CLI or IDE • Zero runtime dependencies

```bash
# Standard
pip install claudecodeoptimizer && cco-install

# Isolated (pipx)
pipx install claudecodeoptimizer && cco-install

# Upgrade
pip install -U claudecodeoptimizer && cco-install

# Uninstall
cco-uninstall
```

### Local Mode

```bash
cco-install --local . --statusline cco-full --permissions balanced
```

| Option | Values |
|--------|--------|
| `--statusline` | `cco-full` (all info) / `cco-minimal` (project + branch) |
| `--permissions` | `safe` / `balanced` / `permissive` / `full` |

## Documentation

| Doc | Content |
|-----|---------|
| [Commands](docs/commands.md) | All 8 commands with flags and examples |
| [Agents](docs/agents.md) | 3 specialized agents and their scopes |
| [Rules](docs/rules.md) | Full rule reference |

## Safety Features

**Fix Workflow:** Analyze → Report → Approve → Apply → Verify

| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |

**Accounting:** Every action reports `Applied: N | Skipped: N | Failed: N`

## Standards

Built on [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices) and official Claude Code documentation.

**Core Principles:** SSOT, DRY, YAGNI, KISS • **AI Rules:** Read-First, No-Hallucination • **Security:** OWASP, Least-Privilege

## License

MIT — see [LICENSE](LICENSE)

---

**[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** • Created by Sungur Zahid Erdim
