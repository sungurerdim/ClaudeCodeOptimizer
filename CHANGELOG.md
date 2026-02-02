# Changelog

## [2.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/tag/v2.0.0) (2025-01-24)

### ⚠ BREAKING CHANGES

* **Command Changes** (v1 → v2):
  * `/cco-tune` → `/cco:tune`
  * `/cco-health` → removed (use `/cco:tune --preview` instead)
  * `/cco-generate` → `/cco:research`
  * `/cco-audit` + `/cco-optimize` → `/cco:optimize` (merged)
  * `/cco-review` + `/cco-refactor` → `/cco:align` (merged)
* **Agent Restructure**:
  * `Explore` + `Plan` → `cco-agent-analyze`
  * `Action` → `cco-agent-apply`
  * NEW: `cco-agent-research`

### Features

* **Zero Global Pollution** — CCO never writes to `~/.claude/` or any global directory
* **Context Injection** — Core rules injected via SessionStart hook, not file copying
* **Safe Updates** — All rules use `cco-` prefix; your own rules are never touched
* **Modular Rules** — 85 standards in 2 files → 45 focused rule files
* **SessionStart hook** — Injects core rules directly into context via `additionalContext`
* **`/cco:preflight`** — Pre-release workflow with quality gates
* **`/cco:docs`** — Documentation gap analysis
* **`cco-agent-research`** — External source research with reliability scoring (T1-T6)
* **Confidence scoring** — 0-100 scale for findings with ≥80 threshold for auto-fix
* **Phase gates** — Explicit checkpoints (GATE-1, GATE-2, etc.) in command workflows
* **Parallel scope execution** — Multiple scope groups analyzed concurrently
* **Test suite** — 61 tests covering commands, hooks, edge cases, and plugin structure
* **Permissions system** — Four levels (safe/balanced/permissive/full)

### Bug Fixes

* **Path traversal security** — Resolve paths before validation to prevent symlink bypasses
* **YAML frontmatter** — Quoted argument-hint values to prevent parsing errors
* **CI dependencies** — Added pyyaml for test execution
* **Task execution** — Switched to sync calls for reliable result handling

## 1.0.0 (2025-12-02)

### Features

* **8 slash commands** — `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco-optimize`, `/cco-review`, `/cco-generate`, `/cco-refactor`, `/cco-commit`
* **3 specialized agents** — Explore, Plan, Action
* **85 standards** — 51 universal + 34 Claude-specific
* **Risk-based approval flow** — AskUserQuestion integration
* **Project-aware tuning** — Stack detection via `/cco-tune`
* **Doc-code mismatch detection** — SSOT resolution
