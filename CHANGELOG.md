# Changelog

## [4.5.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.4.0...v4.5.0) (2026-02-24)


### Features

* **skills:** add --force-approve flag and harden extras ([#63](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/63)) ([361b750](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/361b750ab299836852f3a51d2262aeccbf43e3b4))

## [4.4.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.3.0...v4.4.0) (2026-02-23)


### Features

* **rules:** add behavioral guardrails and fix stale tag check ([#60](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/60)) ([c685443](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c6854434eb7067c5a0edead4050ca7a20588725b))

## [4.3.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.2.2...v4.3.0) (2026-02-21)


### Features

* **agents:** add worktree isolation for analyze agent ([#57](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/57)) ([bbb29b4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/bbb29b48caf29944dae838ead9c39e87b6a726f0))

## [4.2.2](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.2.1...v4.2.2) (2026-02-17)


### Bug Fixes

* **skills:** use pipe pattern for reliable skill context evaluation ([#47](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/47)) ([bf6c977](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/bf6c9777ba0168302e875216f0b198afcf4ad381))

## [4.2.1](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.2.0...v4.2.1) (2026-02-17)


### Bug Fixes

* agent invocation gates and false positive prevention ([#34](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/34)) ([7eed4c8](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/7eed4c8daabcaa35f44f63d4091865883aacb11b))
* **ci:** bypass release-please release creation with gh CLI fallback ([#38](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/38)) ([49a48fe](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/49a48fe17418b389fa8c3832ff27bd253cb1b22d))
* **ci:** revert to simple release-please workflow ([#39](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/39)) ([08860ab](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/08860ab10a76c82192b8a99438641945ec12bbaa))
* **ci:** scope manifest-sync regex to var blocks and fix test errcheck ([#35](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/35)) ([04c748e](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/04c748e78dd1a0498a0c34713aba35dbe36db5f9))

## [4.2.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.1.0...v4.2.0) (2026-02-16)


### Features

* **installer:** install binary to ~/.local/bin with PATH setup ([#31](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/31)) ([fbfbd40](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/fbfbd403f07299a3a23266a6f214803f5758b6b7))

## [4.1.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.0.0...v4.1.0) (2026-02-16)


### Features

* **skills:** expand scopes and improve agent integration ([#28](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/28)) ([c03964f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c03964f31e88c47780d2d0a4c9fbd769cd493c4f))

## [4.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.2.1...v4.0.0) (2026-02-11)


### ⚠ BREAKING CHANGES

* commands/ directory replaced by skills/ with SKILL.md files. Install scripts (install.sh, install.ps1) replaced by Go binary installer. Run ./cco install to migrate.

### Features

* migrate to skills and Go installer ([#24](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/24)) ([5c8a055](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5c8a0553eed7ec9582a61be311f68916993e28e5))

## [3.2.1](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.2.0...v3.2.1) (2026-02-08)


### Bug Fixes

* **install:** update v1 pip package name and present all findings ([#18](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/18)) ([aa52c65](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/aa52c65bb0865ba7115317d6e647c947fe13db2e))

## [3.2.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.1.0...v3.2.0) (2026-02-08)


### Features

* add blueprint, pr commands and feature branch workflow ([#11](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/11)) ([6243c7b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6243c7b65ec09d8dcdc56853f3404c36780aa298))

## [3.1.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.0.0...v3.1.0) (2026-02-07)


### Features

* **extras:** add statusline for Claude Code ([6a7afa9](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6a7afa940da6978e18479571e90eb64e2bfdd45e))


### Bug Fixes

* **install:** add full v1+v2 legacy cleanup ([5010517](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/50105177911f397e1f2a785ac8b00e076f011e12))

## [3.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v2.0.1...v3.0.0) (2026-02-06)


### ⚠ BREAKING CHANGES

* rule structure reorganized into 5 categories
* CCO is no longer distributed as a Claude Code plugin. Install via `curl -fsSL .../install.sh | bash` (Unix) or `irm .../install.ps1 | iex` (Windows). Commands renamed from `/cco:*` to `/cco-*` format.

### Features

* add stable/dev channel support to install scripts ([e735f83](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e735f83360ea80f04426ef506539cae05cc404dd))
* optimize all files for Opus 4.6 ([d6b2dbc](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d6b2dbc1c99ddddba0acfe2c2fe35d22e7848ce6))
* switch from plugin to install script distribution model ([33cffe6](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/33cffe63556a1bc84b4cd1ada0f809536dd7398a))


### Bug Fixes

* **ci:** add version consistency validation across all release-please managed files ([0f85b90](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0f85b90218158c3ea041268f42314f4e670dea85))
* **commands:** add channel support to cco-update and fix cco-commit parsing ([daa8e39](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/daa8e39e707d7eee7e4a1ea9c1278fd47df84ca6))
* **hooks:** flush stdout to prevent buffering issues ([475bff1](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/475bff19184d5e542b85703c1717f0337b88bd91))
* **install:** add preflight validation, content checks, and legacy cleanup ([1f3c6fb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1f3c6fb958bc979027262545ab1dc64474f9361d))
* **install:** use dev branch URL for dev channel installer ([a77fdb4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a77fdb468ed36248f52960d28c6207cc22e26b65))

## [2.0.1](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v2.0.0...v2.0.1) (2026-02-04)


### Bug Fixes

* **ci:** update workflow for new hooks-based structure ([95687bd](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/95687bd2eaf8bdaf50670612177198a8d69f60eb))
* **hooks:** simplify to Python script, add Windows encoding fix ([cfbdc0c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/cfbdc0ce1c92b561f4a20ff31d1b2e92e828a64b))
* **release:** configure manifest mode for release-please ([d983aec](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d983aeccce8272592014a08f2b0cee7f3e804f54))
* **release:** configure manifest mode for release-please ([0669e47](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0669e47b96dfc3a60cde2cbd8390e57a7038b752))
* **release:** switch to simple release type ([dc55817](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/dc5581784c637951cde2fa297f44f527a17d870e))
* **release:** use config file instead of hardcoded node type ([33e022d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/33e022dae6d21e317540c8491ac91bedbe273375))
* **release:** use config file instead of hardcoded node type ([a47ff8d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a47ff8d4406c01601c67d92fba55364e66daa613))
* **release:** use simple release type instead of node ([3e93f93](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/3e93f933897eb3b6305881a7a9bfae6d55e97973))


### Reverts

* **release:** restore original working config ([e45da1b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e45da1b64691c97bd97f6ab52df48bf5203c122b))

## [2.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/tag/v2.0.0) (2025-01-24)

### ⚠ BREAKING CHANGES

* **Command Changes** (v1 → v2):
  * `/cco-tune` → `/cco:tune`
  * `/cco-health` → removed (use `/cco:tune --preview` instead)
  * `/cco-generate` → removed (generation now handled inline by agents)
  * `/cco-audit` + `/cco-optimize` → `/cco:optimize` (merged)
  * `/cco-review` + `/cco-refactor` → `/cco:align` (merged)
* **Agent Restructure**:
  * `cco-agent-detect` + `cco-agent-scan` → `cco-agent-analyze`
  * `cco-agent-action` → `cco-agent-apply`
  * NEW: `cco-agent-research`

### Features

* **Zero Global Pollution** — CCO never writes to `~/.claude/` or any global directory
* **Context Injection** — Core rules injected via SessionStart hook, not file copying
* **Safe Updates** — All rules use `cco-` prefix; your own rules are never touched
* **Modular Rules** — 85 standards in 2 files → 45 focused rule files
* **SessionStart hook** — Injects core rules directly into context via `additionalContext`
* **`/cco:preflight`** — Pre-release workflow with quality gates
* **`/cco:research`** — Multi-source research with CRAAP+ reliability scoring
* **`/cco:docs`** — Documentation gap analysis
* **`cco-agent-research`** — External source research with reliability scoring (T1-T6)
* **Confidence scoring** — 0-100 scale for findings with ≥80 threshold for auto-fix
* **Phase gates** — Explicit checkpoints (GATE-1, GATE-2, etc.) in command workflows
* **Parallel scope execution** — Multiple scope groups analyzed concurrently
* **Test suite** — 69 tests covering commands, hooks, edge cases, and plugin structure
* **Permissions system** — Four levels (safe/balanced/permissive/full)

### Bug Fixes

* **Path traversal security** — Resolve paths before validation to prevent symlink bypasses
* **YAML frontmatter** — Quoted argument-hint values to prevent parsing errors
* **CI dependencies** — Added pyyaml for test execution
* **Task execution** — Switched to sync calls for reliable result handling

## 1.0.0 (2025-12-02)

### Features

* **8 slash commands** — `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco-optimize`, `/cco-review`, `/cco-generate`, `/cco-refactor`, `/cco-commit`
* **3 specialized agents** — `cco-agent-detect`, `cco-agent-scan`, `cco-agent-action`
* **85 standards** — 51 universal + 34 Claude-specific
* **Risk-based approval flow** — AskUserQuestion integration
* **Project-aware tuning** — Stack detection via `/cco-tune`
* **Doc-code mismatch detection** — SSOT resolution
