# Claude Code Optimizer (CCO)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-00A67E.svg)](https://github.com/anthropics/claude-code)

**Enforceable constraints for Claude Code.** Stops over-engineering, scope creep, and silent assumptions.

| Without CCO | With CCO |
|-------------|----------|
| Adds AbstractValidatorFactory for simple validation | Only requested changes — enforced |
| Edits 5 files when asked for 1 fix | Must read before edit — enforced |
| Guesses requirements silently | Stops and asks — enforced |
| Method grows to 200 lines | ≤50 lines, ≤3 nesting — enforced |

These are **BLOCKER** rules — execution stops, not suggestions to ignore.

---

## Install

```
/plugin marketplace add sungurerdim/ClaudeCodeOptimizer
```

```
/plugin install cco@ClaudeCodeOptimizer
```

Restart Claude Code. Done.

<details>
<summary>Alternative: Terminal</summary>

```bash
claude plugin marketplace add sungurerdim/ClaudeCodeOptimizer
```

```bash
claude plugin install cco@ClaudeCodeOptimizer
```
</details>

---

## Quick Start

```
/cco:optimize   # Fix issues
/cco:align      # Architecture gaps
/cco:commit     # Quality-gated commits
```

---

## How It Works

1. **Install** → SessionStart hook injects core rules every session, automatically
2. **Use commands** → `/cco:optimize`, `/cco:align`, etc.
3. Core rules always active via hook — no configuration needed

Your project files are never modified by CCO. Rules are injected via hook, not written to disk.

---

## Commands

| Command | Purpose |
|---------|---------|
| [`/cco:optimize`](docs/commands.md#ccooptimize) | Fix security, types, performance issues |
| [`/cco:align`](docs/commands.md#ccoalign) | Architecture and pattern analysis |
| [`/cco:commit`](docs/commands.md#ccocommit) | Atomic commits with quality gates |
| [`/cco:research`](docs/commands.md#ccoresearch) | Multi-source research with scoring |
| [`/cco:preflight`](docs/commands.md#ccopreflight) | Pre-release verification |
| [`/cco:docs`](docs/commands.md#ccodocs) | Documentation gap analysis |

6 commands · 3 [specialized agents](docs/agents.md) · Core rules via [SessionStart hook](docs/rules.md)

---

## Docs

- [Getting Started](docs/getting-started.md) — First 10 minutes
- [Commands](docs/commands.md) — Flags and examples
- [Agents](docs/agents.md) — Specialized agents
- [Rules](docs/rules.md) — Full rules reference

---

## Update

```
/plugin marketplace update ClaudeCodeOptimizer
```

```
/plugin update cco@ClaudeCodeOptimizer
```

<details>
<summary>Alternative: Terminal</summary>

```bash
claude plugin marketplace update ClaudeCodeOptimizer
```

```bash
claude plugin update cco@ClaudeCodeOptimizer
```
</details>

## Uninstall

```
/plugin uninstall cco@ClaudeCodeOptimizer
```

```
/plugin marketplace remove ClaudeCodeOptimizer
```

<details>
<summary>Alternative: Terminal</summary>

```bash
claude plugin uninstall cco@ClaudeCodeOptimizer
```

```bash
claude plugin marketplace remove ClaudeCodeOptimizer
```
</details>

---

<details>
<summary>Migrating from v1</summary>

### 1. Uninstall pip package

```bash
pip uninstall claude-code-optimizer
```

### 2. Remove global rules

```bash
# Linux / macOS
rm -f ~/.claude/rules/cco-*.md

# Windows (PowerShell)
Remove-Item ~\.claude\rules\cco-*.md -ErrorAction SilentlyContinue
```

### 3. Remove old project files

```bash
rm -f .claude/rules/cco-*.md
rm -f .claude/commands/cco-*.md
```

### 4. Clean up CLAUDE.md

Remove any `@import` lines referencing CCO rules — v2 uses SessionStart hooks instead.

### 5. Install v2

```
/plugin marketplace add sungurerdim/ClaudeCodeOptimizer
/plugin install cco@ClaudeCodeOptimizer
```

### Command mapping

| v1 | v2 |
|----|-----|
| `/cco-tune` | removed (rules now injected via hook) |
| `/cco-health` | removed |
| `/cco-generate` | removed |
| — | `/cco:research` (new) |
| `/cco-audit` | `/cco:optimize` |
| `/cco-optimize` | `/cco:optimize` |
| `/cco-review` | `/cco:align` |
| `/cco-refactor` | `/cco:align` |

</details>

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**

MIT License
