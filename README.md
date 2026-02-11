# Claude Code Optimizer (CCO)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Structured guardrails for Claude Code.** Every rule tuned to how the model actually thinks — minimal touch, maximum impact.

*CCO adds just enough structure to prevent over-engineering, scope creep, and silent assumptions — without slowing Claude down.*

| Without CCO | With CCO |
|-------------|----------|
| Adds AbstractValidatorFactory for simple validation | Only requested changes |
| Edits 5 files when asked for 1 fix | Scoped to the task |
| Guesses requirements silently | Stops and asks |
| Method grows to 200 lines | ≤50 lines, ≤3 nesting |

---

## Install

**macOS / Linux:**

```bash
curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o cco && chmod +x cco && ./cco install
```

**Windows (PowerShell):**

```powershell
irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile cco.exe; .\cco.exe install
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

1. **Install** — Rules, skills, and agents are placed in `~/.claude/`
2. **Rules auto-load** — `~/.claude/rules/cco-rules.md` is loaded into every session automatically
3. **Use skills** — `/cco-optimize`, `/cco-align`, etc. (6 auto-invoke on natural language, 2 explicit)
4. **Update** — `/cco-update` checks for new versions

No hooks, no plugins, no dependencies. Just markdown files.

---

## Skills

| Skill | Purpose |
|-------|---------|
| [`/cco-optimize`](docs/commands.md#cco-optimize) | Fix security, types, performance issues |
| [`/cco-align`](docs/commands.md#cco-align) | Architecture and pattern analysis |
| [`/cco-commit`](docs/commands.md#cco-commit) | Atomic commits with quality gates |
| [`/cco-research`](docs/commands.md#cco-research) | Multi-source research with scoring |
| [`/cco-docs`](docs/commands.md#cco-docs) | Documentation gap analysis |
| [`/cco-blueprint`](docs/commands.md#cco-blueprint) | Project health assessment and transformation |
| [`/cco-pr`](docs/commands.md#cco-pr) | Release-please compatible pull requests |
| [`/cco-update`](docs/commands.md#cco-update) | Check and install updates |

8 skills · 3 [specialized agents](docs/agents.md) · Core rules via [auto-loaded rules file](docs/rules.md)

---

## Docs

- [Getting Started](docs/getting-started.md) — First 10 minutes
- [Skills](docs/commands.md) — Flags, scopes, and examples
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

**macOS / Linux:**
```bash
./cco install
```

**Windows:**
```powershell
.\cco.exe install
```

### Uninstall

**Using Go binary:**

```bash
./cco uninstall
```

**Manual:**

```bash
rm -f ~/.claude/rules/cco-rules.md
rm -rf ~/.claude/skills/cco-*/
rm -f ~/.claude/agents/cco-agent-*.md
```

### Migrate

<details>
<summary>From v3 (commands)</summary>

Run the v4 installer — it automatically migrates `commands/` to `skills/` and cleans up legacy files.

```bash
curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o cco && chmod +x cco && ./cco install
```

Or use `/cco-update` if you already have v3 installed.

</details>

<details>
<summary>From v2 (plugin)</summary>

#### 1. Uninstall plugin

```
/plugin uninstall cco@ClaudeCodeOptimizer
/plugin marketplace remove ClaudeCodeOptimizer
```

#### 2. Install v4

**macOS / Linux:**
```bash
curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o cco && chmod +x cco && ./cco install
```

**Windows:**
```powershell
irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile cco.exe; .\cco.exe install
```

</details>

<details>
<summary>From v1 (pip)</summary>

#### 1. Uninstall pip package

```bash
pip uninstall claudecodeoptimizer
```

#### 2. Install v4

```bash
curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o cco && chmod +x cco && ./cco install
```

</details>

<details>
<summary>Version history</summary>

| Version | Distribution | Mechanism |
|---------|-------------|-----------|
| v1.x | pip package | Python dependency |
| v2.x | Claude Code plugin | Marketplace + hooks |
| v3.x | Install script | curl/irm + rules/commands/agents |
| **v4.x** | **Go binary** | **Single cross-platform binary + rules/skills/agents** |

</details>

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**

MIT License
