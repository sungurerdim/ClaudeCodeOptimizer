# Claude Code Optimizer (CCO)

[![GitHub release](https://img.shields.io/github/v/release/sungurerdim/ClaudeCodeOptimizer)](https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Structured guardrails for Claude Code.** Every rule tuned to how the model actually thinks — minimal touch, maximum impact.

*CCO adds just enough structure to prevent over-engineering, scope creep, and silent assumptions — without slowing Claude down.*

| Without CCO | With CCO |
|-------------|----------|
| Adds AbstractValidatorFactory for simple validation | Only requested changes |
| Edits 5 files when asked for 1 fix | Scoped to the task |
| Guesses requirements silently | Stops and asks |
| Method grows to 200 lines | ≤50 lines, ≤3 nesting |
| Hallucinates imports that don't exist | Verifies before writing |
| Reports false positives | Reads context, discards FPs |

---

## Install

**macOS / Linux:**

```bash
mkdir -p ~/.local/bin && curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$(uname -m) -o ~/.local/bin/cco && chmod +x ~/.local/bin/cco && ~/.local/bin/cco install
```

**Windows (PowerShell):**

```powershell
$b="$HOME\.local\bin"; New-Item $b -ItemType Directory -Force >$null; irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile "$b\cco.exe"; & "$b\cco.exe" install
```

Restart Claude Code. Done.

---

## Quick Start

1. **`/cco-blueprint`** — Create a project profile in CLAUDE.md (priorities, constraints, targets)
2. **`/cco-align`** — Architecture gap analysis
3. **`/cco-optimize`** — Scan and fix security, quality, and hygiene issues

---

## How It Works

```
~/.claude/
├── rules/cco-rules.md          # Auto-loaded every session (passive)
├── skills/cco-*/SKILL.md       # Slash commands (active)
└── agents/cco-agent-*.md       # Specialized subagents
```

**Passive — Rules** load automatically at session start. Scope control, complexity limits, verification, and security patterns are always active. No commands needed.

**Active — Skills** are invoked via `/cco-*` slash commands. Each skill orchestrates a specific workflow (optimize, commit, PR, etc.).

**Feature branch workflow:**

```
main → /cco-commit → feature branch → work → /cco-pr → main
```

`/cco-commit` detects when you're on main and creates a feature branch automatically. `/cco-pr` creates a conventional-commit PR for clean changelogs.

---

## Skills

| Skill | What it does | Key Flags |
|-------|-------------|-----------|
| [`/cco-optimize`](docs/skills.md#cco-optimize) | Scan and fix security, types, performance, hygiene issues | `--auto`, `--preview`, `--scope=X`, `--loop` |
| [`/cco-align`](docs/skills.md#cco-align) | Analyze architecture gaps and fix structural issues | `--auto`, `--preview` |
| [`/cco-commit`](docs/skills.md#cco-commit) | Quality-gated atomic commits with branch management | `--preview`, `--single`, `--staged-only` |
| [`/cco-pr`](docs/skills.md#cco-pr) | Create release-please compatible PRs with auto-merge | `--auto`, `--preview`, `--no-auto-merge`, `--draft` |
| [`/cco-blueprint`](docs/skills.md#cco-blueprint) | Profile project health, set targets, track progress | `--auto`, `--init`, `--refresh`, `--scope=X` |
| [`/cco-docs`](docs/skills.md#cco-docs) | Find documentation gaps and generate missing content | `--auto`, `--preview`, `--scope=X`, `--update` |
| [`/cco-research`](docs/skills.md#cco-research) | Multi-source research with CRAAP+ reliability scoring | `--quick`, `--deep` |
| [`/cco-update`](docs/skills.md#cco-update) | Check for updates and install latest version | `--auto`, `--check` |

8 skills · 3 [specialized agents](docs/agents.md) · Core rules via [auto-loaded rules file](docs/rules.md)

---

## What the Rules Enforce

Rules are active in every session — no commands needed.

| Category | What it does |
|----------|-------------|
| Scope Control | Every changed line traces to the request; unrelated issues mentioned, not fixed |
| Complexity Limits | CC≤15, Method≤50 lines, File≤500 lines, Nesting≤3, Params≤4 |
| Production Standards | Security, privacy, performance, error handling applied by default |
| Output Brevity | Concise responses; no unnecessary praise, filler, or emojis |
| Verification | Verify imports and APIs exist before using; match existing code style |
| Uncertainty Protocol | State confidence levels; ask before proceeding on ambiguous tasks |

Full reference: [docs/rules.md](docs/rules.md)

---

## Docs

- [Getting Started](docs/getting-started.md) — First 10 minutes
- [Skills](docs/skills.md) — Flags, scopes, and examples
- [Agents](docs/agents.md) — Specialized agents
- [Rules](docs/rules.md) — Full rules reference
- [Architecture](docs/architecture.md) — System design and structure

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

```bash
cco install        # macOS/Linux
cco.exe install    # Windows
```

### Uninstall

```bash
cco uninstall
```

<details>
<summary>Manual removal</summary>

```bash
rm -f ~/.claude/rules/cco-rules.md
rm -rf ~/.claude/skills/cco-*/
rm -f ~/.claude/agents/cco-agent-*.md
```

</details>

<details>
<summary>Migration from previous versions</summary>

| Version | Distribution | Mechanism |
|---------|-------------|-----------|
| v1.x | pip package | Python dependency |
| v2.x | Claude Code plugin | Marketplace + hooks |
| v3.x | Install script | curl/irm + rules/commands/agents |
| **v4.x** | **Go binary** | **Single cross-platform binary + rules/skills/agents** |

**From v3:** Run the v4 installer — it automatically migrates `commands/` to `skills/` and cleans up legacy files. Or use `/cco-update`.

**From v2:** Uninstall plugin (`/plugin uninstall cco@ClaudeCodeOptimizer` + `/plugin marketplace remove ClaudeCodeOptimizer`), then run the v4 installer.

**From v1:** Uninstall pip package (`pip uninstall claudecodeoptimizer`), then run the v4 installer.

</details>

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**

MIT License
