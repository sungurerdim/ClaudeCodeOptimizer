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
```

Then run `/plugin`, go to **Discover** tab, select **cco**, and click **Install**.

<details>
<summary><strong>Alternative: Direct command</strong></summary>

```
/plugin install cco@ClaudeCodeOptimizer
```

</details>

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
/cco:config     # Configure project (auto-detects stack)
/cco:status     # Check health scores (0-100)
/cco:optimize   # Fix issues with approval flow
```

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

CCO never writes to `~/.claude/` or any global directory. Only `./.claude/rules/` is modified when you run `/cco:config`.

### Context Injection

Core rules are injected directly into session context via SessionStart hook — no files created, no cleanup needed. Rules are active immediately on every session.

### Safe Updates with `cco-` Prefix

All CCO rules use `cco-` prefix. Your own rules (without prefix) are never touched.

```
.claude/rules/
├── cco-context.md       ← Managed by CCO
├── cco-{language}.md    ← Managed by CCO
├── cco-{framework}.md   ← Managed by CCO
├── my-custom-rule.md    ← YOUR file, never touched
└── team-standards.md    ← YOUR file, never touched
```

---

## What's Included

| Component | Count | Purpose |
|-----------|-------|---------|
| Commands | 7 | `/cco:config`, `/cco:status`, `/cco:optimize`, etc. |
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
│  PROJECT (copied via /cco:config to .claude/rules/)         │
│    ├── cco-context.md      Project metadata (YAML)          │
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
| `/cco:config` | Project configuration (auto-detects stack) |
| `/cco:status` | Health dashboard (security, quality, hygiene scores) |
| `/cco:optimize` | Fix issues with approval flow for risky changes |
| `/cco:review` | Architecture analysis with 80/20 recommendations |
| `/cco:commit` | Quality-gated atomic commits |
| `/cco:research` | Multi-source research with reliability scoring |
| `/cco:preflight` | Pre-release workflow orchestration |

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
