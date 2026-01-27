# Claude Code Optimizer (CCO)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-00A67E.svg)](https://github.com/anthropics/claude-code)

**Enforceable constraints for Claude Code.** Stops over-engineering, scope creep, and silent assumptions.

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
/cco:tune       # Configure for this project (once)
/cco:optimize   # Fix issues
/cco:align      # Architecture gaps
/cco:commit     # Quality-gated commits
```

---

## Why CCO?

Claude Code is powerful but unconstrained:

| Problem | CCO Solution |
|---------|--------------|
| Adds AbstractValidatorFactory for simple validation | [**Change Scope**](docs/rules.md#foundation-rules-blocker): Only requested changes |
| Edits 5 files when asked for 1 fix | [**Read-Before-Edit**](docs/rules.md#workflow-rules-blocker): Must read first |
| Guesses requirements silently | [**Uncertainty Protocol**](docs/rules.md#foundation-rules-blocker): Stop and ask |
| Method grows to 200 lines | [**Complexity Limits**](docs/rules.md#foundation-rules-blocker): ≤50 lines, ≤3 nesting |

These are **BLOCKER** rules — execution stops, not suggestions to ignore.

---

## How It Works

```
Install CCO → SessionStart hook injects core rules (every session, automatic)
                                    ↓
/cco:tune   → Creates .claude/rules/cco-*.md (once per project)
                                    ↓
            → Claude Code auto-loads .claude/rules/*.md (native behavior)
                                    ↓
            → Rules active. Zero manual activation.
```

### Why This Matters

| Traditional Approach | CCO Approach |
|---------------------|--------------|
| Custom CLI wrapper (`mytool --with-rules`) | Native Claude Code |
| Manual rule activation per session | Automatic on every session start |
| Separate config files to maintain | Uses Claude Code's native `.claude/rules/` |
| Breaks when Claude Code updates | Uses official plugin API |

**Result:**
- **Install once** → Core rules active in ALL projects immediately
- **`/cco:tune` once per project** → Project rules auto-load every session
- **No manual activation** → Open Claude Code, rules already working
- **No performance cost** → Native mechanism, not a wrapper

---

## Commands

| Command | Purpose |
|---------|---------|
| [`/cco:tune`](docs/commands.md#ccotune) | Detect stack, create project profile |
| [`/cco:optimize`](docs/commands.md#ccooptimize) | Fix security, types, lint, performance |
| [`/cco:align`](docs/commands.md#ccoalign) | Architecture and pattern analysis |
| [`/cco:commit`](docs/commands.md#ccocommit) | Atomic commits with quality gates |
| [`/cco:research`](docs/commands.md#ccoresearch) | Multi-source research with scoring |
| [`/cco:preflight`](docs/commands.md#ccopreflight) | Pre-release verification |
| [`/cco:docs`](docs/commands.md#ccodocs) | Documentation gap analysis |

---

## What's Included

| Component | Count | Details |
|-----------|-------|---------|
| Commands | 7 | [Reference](docs/commands.md#command-overview) |
| Agents | 3 | [analyze, apply, research](docs/agents.md) |
| Rules | 44 | [3 core](docs/rules.md#core-rules-3-categories) + [21 languages](docs/rules.md#language-rules-21-files) + [8 frameworks](docs/rules.md#framework-rules-8-files) + [12 operations](docs/rules.md#operations-rules-12-files) |

### Core Rules: Hard Limits

| Metric | Limit | Exceeds → |
|--------|-------|-----------|
| Cyclomatic Complexity | ≤ 15 | STOP, refactor |
| Method Lines | ≤ 50 | STOP, split |
| File Lines | ≤ 500 | STOP, extract |
| Nesting Depth | ≤ 3 | STOP, flatten |
| Parameters | ≤ 4 | STOP, use object |

### Accounting (No Silent Skips)

Every operation ends with: `Applied: 12 | Failed: 1 | Total: 13`

Formula: **`applied + failed = total`** — no "declined" category. AI cannot silently skip.

---

## Safety

- Your rules (without `cco-` prefix) are never touched
- CCO only writes to `.claude/rules/`, never global
- All changes require clean git state for rollback

See [Safety Model](docs/rules.md#safety-rules-blocker) for security patterns.

---

## Docs

- [Getting Started](docs/getting-started.md) — First 10 minutes
- [Commands](docs/commands.md) — Flags and examples
- [Agents](docs/agents.md) — Specialized agents
- [Rules](docs/rules.md) — Full rules reference

---

## Update / Uninstall

```
/plugin marketplace update ClaudeCodeOptimizer
```

```
/plugin uninstall cco@ClaudeCodeOptimizer
```

```
/plugin marketplace remove ClaudeCodeOptimizer
```

---

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)** · **[Changelog](CHANGELOG.md)**

MIT License
