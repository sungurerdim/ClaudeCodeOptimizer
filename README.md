# Claude Code Optimizer (CCO)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Structured guardrails for Claude Code.** Optimized by Opus 4.6, for Opus 4.6 — every rule tuned to how the model actually thinks.

*Minimal touch, maximum impact.* CCO adds just enough structure to prevent over-engineering, scope creep, and silent assumptions — without slowing Claude down.

| Without CCO | With CCO |
|-------------|----------|
| Adds AbstractValidatorFactory for simple validation | Only requested changes |
| Edits 5 files when asked for 1 fix | Scoped to the task |
| Guesses requirements silently | Stops and asks |
| Method grows to 200 lines | ≤50 lines, ≤3 nesting |

---

## Install

**Mac / Linux:**

```bash
curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash
```

**Windows (PowerShell):**

```powershell
irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.ps1 | iex
```

Restart Claude Code. Done.

---

## Quick Start

```
/cco-optimize   # Fix issues
/cco-align      # Architecture gaps
/cco-commit     # Quality-gated commits
```

---

## How It Works

1. **Install** — Rules, commands, and agents are placed in `~/.claude/`
2. **Rules auto-load** — `~/.claude/rules/cco-rules.md` is loaded into every session automatically
3. **Use commands** — `/cco-optimize`, `/cco-align`, etc.
4. **Update** — `/cco-update` checks for new versions

No hooks, no plugins, no dependencies. Just markdown files.

---

## Commands

| Command | Purpose |
|---------|---------|
| [`/cco-optimize`](docs/commands.md#cco-optimize) | Fix security, types, performance issues |
| [`/cco-align`](docs/commands.md#cco-align) | Architecture and pattern analysis |
| [`/cco-commit`](docs/commands.md#cco-commit) | Atomic commits with quality gates |
| [`/cco-research`](docs/commands.md#cco-research) | Multi-source research with scoring |
| [`/cco-docs`](docs/commands.md#cco-docs) | Documentation gap analysis |
| [`/cco-blueprint`](docs/commands.md#cco-blueprint) | Project health assessment and transformation |
| [`/cco-pr`](docs/commands.md#cco-pr) | Release-please compatible pull requests |
| [`/cco-update`](docs/commands.md#cco-update) | Check and install updates |

8 commands · 3 [specialized agents](docs/agents.md) · Core rules via [auto-loaded rules file](docs/rules.md)

---

## Docs

- [Getting Started](docs/getting-started.md) — First 10 minutes
- [Commands](docs/commands.md) — Flags, scopes, and examples
- [Agents](docs/agents.md) — Specialized agents
- [Rules](docs/rules.md) — Full rules reference

---

## Extras

Optional add-ons that complement CCO.

| Extra | Description |
|-------|-------------|
| [Statusline](extras/statusline/) | Git, model, and context info in your Claude Code status bar |

---

## Maintenance

### Update

```
/cco-update
```

Or re-run the installer:

**Mac / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash
```

**Windows:**
```powershell
irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.ps1 | iex
```

### Uninstall

**Mac / Linux:**

```bash
rm -f ~/.claude/rules/cco-rules.md
rm -f ~/.claude/commands/cco-*.md
rm -f ~/.claude/agents/cco-agent-*.md
```

**Windows (PowerShell):**

```powershell
Remove-Item ~\.claude\rules\cco-rules.md -ErrorAction SilentlyContinue
Remove-Item ~\.claude\commands\cco-*.md -ErrorAction SilentlyContinue
Remove-Item ~\.claude\agents\cco-agent-*.md -ErrorAction SilentlyContinue
```

### Migrate

<details>
<summary>From v2 (plugin)</summary>

#### 1. Uninstall plugin

```
/plugin uninstall cco@ClaudeCodeOptimizer
/plugin marketplace remove ClaudeCodeOptimizer
```

#### 2. Install v3

**Mac / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash
```

**Windows:**
```powershell
irm https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.ps1 | iex
```

#### Command mapping

| v2 | v3 |
|----|-----|
| `/cco:optimize` | `/cco-optimize` |
| `/cco:align` | `/cco-align` |
| `/cco:commit` | `/cco-commit` |
| `/cco:research` | `/cco-research` |
| `/cco:docs` | `/cco-docs` |
| — | `/cco-update` (new) |
| — | `/cco-blueprint` (new) |
| — | `/cco-pr` (new) |

</details>

<details>
<summary>From v1 (pip)</summary>

#### 1. Uninstall pip package

```bash
pip uninstall claudecodeoptimizer
```

#### 2. Remove old files

```bash
rm -f ~/.claude/rules/cco-*.md
rm -f .claude/rules/cco-*.md
rm -f .claude/commands/cco-*.md
```

#### 3. Install v3

```bash
curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/install.sh | bash
```

</details>

<details>
<summary>Version history</summary>

| Version | Distribution | Mechanism |
|---------|-------------|-----------|
| v1.x | pip package | Python dependency |
| v2.x | Claude Code plugin | Marketplace + hooks |
| **v3.x** | **Install script** | **curl/irm + rules/commands/agents** |

</details>

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**

MIT License
