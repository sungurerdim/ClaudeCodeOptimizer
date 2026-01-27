# Claude Code Optimizer (CCO)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-00A67E.svg)](https://github.com/anthropics/claude-code)

**Safety, quality, and decision layer for Claude Code.**

Same prompts, better outcomes. Fewer errors, fewer rollbacks, more consistent results.

---

## Quick Install

**In Claude Code:**
```
/plugin marketplace add sungurerdim/ClaudeCodeOptimizer
/plugin install cco@ClaudeCodeOptimizer
```

<details>
<summary><strong>Alternative: From terminal</strong></summary>

```bash
claude plugin marketplace add sungurerdim/ClaudeCodeOptimizer
claude plugin install cco@ClaudeCodeOptimizer
```

</details>

**Restart Claude Code** to activate.

---

## Quick Start

```
/cco:tune       # Configure CCO for this project (run once)
/cco:optimize   # Fix issues with approval flow
/cco:align      # Architecture gap analysis
/cco:commit     # Quality-gated atomic commits
```

**First time?** Run `/cco:tune` to analyze your project and create a profile. Other commands will prompt for setup if needed.

---

## Why CCO?

| Without CCO | With CCO |
|-------------|----------|
| Claude applies generic patterns | Domain-specific best practices for your stack |
| Changes happen without pre-checks | Git status verified, clean state for rollback |
| Silent operations | Full accounting: `Applied: 5 | Failed: 0 | Total: 5` |
| "Add caching somewhere" | "Use TTL + invalidation for this data fetch" |

**CCO is a process layer, not a teaching layer.** Claude already knows how to code. CCO adds safety between intent and action.

---

## Key Features

### Zero Global Pollution

CCO never writes to `~/.claude/` or any global directory. Only `./.claude/rules/` is modified during project setup.

### Context Injection

Core rules are injected directly into session context via SessionStart hook — no files created, no cleanup needed. Rules are active immediately on every session.

### Safe Updates with `cco-` Prefix

All CCO rules use `cco-` prefix. Your own rules (without prefix) are never touched.

```
.claude/rules/
├── cco-profile.md       ← Managed by CCO
├── cco-{language}.md    ← Managed by CCO
├── cco-{framework}.md   ← Managed by CCO
├── my-custom-rule.md    ← YOUR file, never touched
└── team-standards.md    ← YOUR file, never touched
```

---

## What's Included

| Component | Count | Purpose |
|-----------|-------|---------|
| Commands | 7 | `/cco:tune`, `/cco:optimize`, `/cco:align`, `/cco:commit`, `/cco:research`, `/cco:preflight`, `/cco:docs` |
| Agents | 3 | Analyze, Apply, Research |
| Rules | 44 | Core (3) + Languages (21) + Frameworks (8) + Operations (12) |

### Rules Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CORE (injected via SessionStart hook)                      │
│  → cco-foundation.md   Design principles, code quality      │
│  → cco-safety.md       Non-negotiable security standards    │
│  → cco-workflow.md     AI execution patterns                │
├─────────────────────────────────────────────────────────────┤
│  PROJECT (copied during setup to .claude/rules/)            │
│    ├── cco-profile.md      Project metadata (YAML)          │
│    ├── cco-{language}.md   Language-specific rules          │
│    ├── cco-{framework}.md  Framework-specific rules         │
│    └── cco-{operation}.md  Operations rules                 │
└─────────────────────────────────────────────────────────────┘
```

**Coverage:** 21 languages (Python, TypeScript, Go, Rust, Java, C#, Ruby, PHP, Swift, Kotlin, +11 niche) and 20 domains (API, Database, Testing, Security, CI/CD, Observability, Compliance, Infrastructure, and more).

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cco:tune` | Configure CCO for this project - analyze stack, create profile |
| `/cco:optimize` | Fix issues with approval flow for risky changes |
| `/cco:align` | Architecture gap analysis - current vs ideal state |
| `/cco:commit` | Quality-gated atomic commits |
| `/cco:research` | Multi-source research with reliability scoring |
| `/cco:preflight` | Pre-release workflow orchestration |
| `/cco:docs` | Documentation gap analysis - generate missing docs |

**Note:** Run `/cco:tune` first to configure CCO for your project. Other commands will prompt if profile is missing.

See [Commands documentation](docs/commands.md) for flags and examples.

---

## Agents

| Agent | Purpose |
|-------|---------|
| `cco-agent-analyze` | Fast read-only analysis with severity scoring |
| `cco-agent-apply` | Code changes with verification and cascade fixing. Also handles project config via `scope=config` |
| `cco-agent-research` | Multi-source research with CRAAP+ reliability scoring |

See [Agents documentation](docs/agents.md) for detailed capabilities.

---

## Safety Model

| Category | Examples |
|----------|----------|
| **Auto-Apply (Safe)** | Unused imports, SQL parameterization, lint/format fixes, type annotations |
| **Require Approval (Risky)** | Auth/CSRF changes, DB schema, API contracts, file deletions |

**Rollback:** All changes require clean git state. Use `git checkout` to revert.

---

## Update & Uninstall

<details>
<summary><strong>Update</strong></summary>

```
/plugin marketplace update ClaudeCodeOptimizer
```

</details>

<details>
<summary><strong>Uninstall</strong></summary>

```
/plugin uninstall cco@ClaudeCodeOptimizer
/plugin marketplace remove ClaudeCodeOptimizer
```

</details>

---

## Documentation

- [Getting Started](docs/getting-started.md) — First 10 minutes with CCO
- [Commands](docs/commands.md) — All commands with flags and examples
- [Agents](docs/agents.md) — Specialized agents and scopes
- [Rules](docs/rules.md) — Complete rules reference

---

## Requirements

- Claude Code CLI or IDE extension
- No additional dependencies

---

## Contributing

Issues and pull requests are welcome.

---

## License

MIT — see [LICENSE](LICENSE)

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**
