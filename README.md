# Claude Code Optimizer (CCO)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-00A67E.svg)](https://github.com/anthropics/claude-code)

**Safety, quality, and decision layer for Claude Code.**

Same prompts, better outcomes. Fewer errors, fewer rollbacks, more consistent results.

---

## What CCO Does

| Without CCO | With CCO |
|-------------|----------|
| Claude applies generic patterns | Domain-specific best practices for your stack |
| Changes happen without pre-checks | Git status verified, clean state for rollback |
| Silent operations | Full accounting: `Applied: 5 | Failed: 0 | Total: 5` |
| "Add caching somewhere" | "Use TTL + invalidation for this data fetch" |

**CCO is a process layer, not a teaching layer.** Opus 4.5 already knows how to code. CCO adds safety between intent and action.

---

## Install

```bash
claude plugin marketplace remove ClaudeCodeOptimizer
claude plugin marketplace add https://github.com/sungurerdim/ClaudeCodeOptimizer
claude plugin install cco@ClaudeCodeOptimizer
```

**Restart Claude Code** to load the new commands.

### Update

```bash
/plugin marketplace update
```

### Uninstall

```bash
claude plugin uninstall cco@ClaudeCodeOptimizer
claude plugin marketplace remove ClaudeCodeOptimizer
```

---

## Quick Start

### 1. Configure Your Project

```
/cco-config
```

Auto-detects your stack (language, framework, database, tools) and generates project-specific rules.

### 2. Check Health

```
/cco-status
```

See security, quality, and hygiene scores for your codebase.

### 3. Fix Issues

```
/cco-optimize
```

Security + quality + hygiene fixes with approval flow for risky changes.

---

## What Gets Installed

| Component | Count | Purpose |
|-----------|-------|---------|
| Commands | 8 | `/cco-config`, `/cco-status`, `/cco-optimize`, etc. |
| Agents | 3 | Analyze, Apply, Research |
| Rules | **1364** | Core (141) + AI (68) + Adaptive (1155) |

### Rules Coverage

**62 rule files** covering:
- **27 languages** — Python, TypeScript, Go, Rust, Java, C#, Ruby, PHP, Swift, Kotlin, and more
- **35 domains** — API, Database, Testing, Security, CI/CD, Observability, Compliance, and more

Only relevant rules are loaded per project — zero unnecessary context.

---

## Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/cco-config` | Project configuration | First time, or when stack changes |
| `/cco-status` | Health dashboard | Start of session |
| `/cco-optimize` | Fix issues | Before PR, after major changes |
| `/cco-review` | Architecture analysis | Before refactoring |
| `/cco-commit` | Quality-gated commit | Every commit |
| `/cco-research` | Multi-source research | "Which library?", "Best practice?" |
| `/cco-preflight` | Pre-release workflow | Before release |
| `/cco-checkup` | Regular maintenance | Weekly or before PR |

See [Commands documentation](docs/commands.md) for flags and examples.

---

## Agents

| Agent | Purpose |
|-------|---------|
| `cco-agent-analyze` | Fast read-only analysis with severity scoring |
| `cco-agent-apply` | Code changes with verification and cascade fixing |
| `cco-agent-research` | Multi-source research with CRAAP+ reliability scoring |

See [Agents documentation](docs/agents.md) for detailed capabilities.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  Your Prompt                                                │
└─────────────────┬───────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  CCO Layer                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Pre-check   │→ │ Analyze     │→ │ Approve (if risky)  │  │
│  │ Git status  │  │ Find issues │  │ Safe = auto-apply   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                           ▼                                 │
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │ Verify      │← │ Apply                               │   │
│  │ Accounting  │  │ Execute with full tracking          │   │
│  └─────────────┘  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Every operation:** Pre-check → Analyze → Approve → Apply → Verify

---

## Safety Model

### Auto-Apply (Safe)
- Remove unused imports
- Parameterize SQL queries
- Move hardcoded secrets to env vars
- Fix lint/format issues
- Add missing type annotations

### Require Approval (Risky)
- Auth/CSRF changes
- Database schema changes
- API contract changes
- Delete files
- Rename public APIs

**Rollback:** All changes are made with clean git state. Use `git checkout` to revert.

---

## Requirements

- Claude Code CLI or IDE extension
- No additional dependencies

---

## Documentation

- [Getting Started](docs/getting-started.md) — First 10 minutes with CCO
- [Commands](docs/commands.md) — All commands with flags and examples
- [Agents](docs/agents.md) — Specialized agents and scopes
- [Rules](docs/rules.md) — Complete rules reference (1364 rules)

---

## Contributing

Issues and pull requests are welcome. Please read the existing code style and follow the patterns.

---

## License

MIT — see [LICENSE](LICENSE)

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**
