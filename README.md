# Claude Code Optimizer (CCO)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-00A67E.svg)](https://github.com/anthropics/claude-code)

**Safety, quality, and decision layer for Claude Code.**

Same prompts, better outcomes. Fewer errors, fewer rollbacks, more consistent results.

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

CCO never writes to `~/.claude/` or any global directory. Your global config stays untouched.

```
~/.claude/           ← Never modified
~/.claude/rules/     ← Never modified
./.claude/rules/     ← Only modified when you run /config
```

### Context Injection (Not File Copying)

Core rules are injected directly into context via SessionStart hook — no files created, no cleanup needed.

```
SessionStart
    │
    ▼
Hook reads rules/core/cco-*.md from plugin
    │
    ▼
Returns JSON with additionalContext
    │
    ▼
Claude Code injects into session context
    │
    ▼
Rules active immediately (even on first session)
```

### Safe Updates with `cco-` Prefix

All CCO rules use `cco-` prefix. Your own rules (without prefix) are never touched during updates.

```
.claude/rules/
├── cco-{language}.md   ← Managed by CCO
├── cco-{framework}.md  ← Managed by CCO
├── my-custom-rule.md   ← YOUR file, never touched
└── team-standards.md   ← YOUR file, never touched
```

---

## Install

<details>
<summary><strong>Option A: From Claude Code (Recommended)</strong></summary>

1. Open Claude Code
2. Type `/plugins` to open plugin manager
3. Search for "Claude Code Optimizer" or "CCO"
4. Click **Install**
5. Restart Claude Code

</details>

<details>
<summary><strong>Option B: From Terminal</strong></summary>

```bash
# Add marketplace source
claude plugin marketplace add https://github.com/sungurerdim/ClaudeCodeOptimizer

# Install plugin
claude plugin install cco@ClaudeCodeOptimizer
```

Restart Claude Code to activate.

</details>

Core rules are automatically injected on every session start. No configuration required.

### Update

<details>
<summary>Update instructions</summary>

**From Claude Code:**
```
/plugins update CCO
```

**From Terminal:**
```bash
claude plugin marketplace update ClaudeCodeOptimizer
```

</details>

### Uninstall

<details>
<summary>Uninstall instructions</summary>

**From Claude Code:**
```
/plugins uninstall CCO
```

**From Terminal:**
```bash
claude plugin uninstall cco@ClaudeCodeOptimizer
claude plugin marketplace remove ClaudeCodeOptimizer
```

</details>

---

## Quick Start

### 1. Configure Your Project (Optional)

```
/cco:config
```

- Auto-detects languages, frameworks, and tools
- Asks 2 question groups (project profile + policies)
- Creates `cco-context.md` (YAML) + relevant rule files in `.claude/rules/`

<details>
<summary>What gets created</summary>

```
.claude/rules/
├── cco-context.md        ← YAML project metadata
├── cco-{language}.md     ← Detected language rules
├── cco-{framework}.md    ← Detected framework rules
└── cco-{operation}.md    ← Detected operation rules
```

</details>

### 2. Check Health

```
/cco:status
```

See security, quality, and hygiene scores (0-100).

### 3. Fix Issues

```
/cco:optimize
```

Security + quality + hygiene fixes with approval flow for risky changes.

---

## What's Included

| Component | Count | Purpose |
|-----------|-------|---------|
| Commands | 7 | `/cco:config`, `/cco:status`, `/cco:optimize`, etc. |
| Agents | 3 | Analyze, Apply, Research |
| Rules | 44 | Core (3) + Languages (21) + Frameworks (8) + Operations (12) |

### Rules Coverage

**44 rule files** covering:
- **21 languages** — Python, TypeScript, Go, Rust, Java, C#, Ruby, PHP, Swift, Kotlin, and 11 niche languages
- **20 domains** — API, Database, Testing, Security, CI/CD, Observability, Compliance, Infrastructure, and more

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

---

## Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/cco:config` | Project configuration | First time, or when stack changes |
| `/cco:status` | Health dashboard | Start of session |
| `/cco:optimize` | Fix issues | Before PR, after major changes |
| `/cco:review` | Architecture analysis | Before refactoring |
| `/cco:commit` | Quality-gated commit | Every commit |
| `/cco:research` | Multi-source research | "Which library?", "Best practice?" |
| `/cco:preflight` | Pre-release workflow | Before release |

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
Plugin installed
       │
       ▼
SessionStart hook fires
       │
       ▼
Core rules injected into context (no files)
       │
       ▼
/config copies project rules to .claude/rules/ (optional)
       │
       ▼
Claude Code auto-loads .claude/rules/*.md
       │
       ▼
Your prompts get stack-specific guidance
```

### CCO Flow

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
- [Rules](docs/rules.md) — Complete rules reference

---

## Contributing

Issues and pull requests are welcome. Please read the existing code style and follow the patterns.

---

## License

MIT — see [LICENSE](LICENSE)

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**
