# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-24

### Highlights

- **Zero Global Pollution** — CCO never writes to `~/.claude/` or any global directory
- **Context Injection** — Core rules injected via SessionStart hook, not file copying
- **Safe Updates** — All rules use `cco-` prefix; your own rules are never touched
- **Modular Rules** — 85 standards in 2 files → 44 focused rule files

### Architecture Changes

| Before (v1) | After (v2) |
|-------------|------------|
| 2 standards files (85 standards) | 44 modular rule files |
| Rules copied to `~/.claude/rules/` | Rules injected into context (no files) |
| @import syntax in CLAUDE.md | Direct context injection via hook |
| Global config pollution | Zero global side effects |

### Breaking Changes

**Command Changes** (v1 → v2):
- `/cco-tune` → `/cco:tune`
- `/cco-health` → removed (use `/cco:tune --check` instead)
- `/cco-generate` → `/cco:research`
- `/cco-audit` + `/cco-optimize` → `/cco:optimize` (merged)
- `/cco-review` + `/cco-refactor` → `/cco:align` (merged)

**Agent Restructure**:
- `Explore` + `Plan` → `cco-agent-analyze`
- `Action` → `cco-agent-apply`
- NEW: `cco-agent-research`

### Added

- **SessionStart hook** — Injects core rules directly into context via `additionalContext`
- **`cco-` prefix** — All rule files prefixed for safe identification and updates
- **Organized structure** — Rules organized into `languages/`, `frameworks/`, `operations/`
- **`/cco:preflight`** — NEW command for pre-release workflow with quality gates
- **`cco-agent-research`** — NEW agent for external source research with reliability scoring (T1-T6)
- **New analyze scopes** — `references`, `architecture`, `conventions`, `trends`
- **Simplify scope** — `/cco:optimize` scope (SIM-01 to SIM-10) for code complexity reduction
- **`/cco:docs`** — NEW command for documentation gap analysis
- **Confidence scoring** — 0-100 scale for findings with ≥80 threshold for auto-fix
- **Phase gates** — Explicit checkpoints (GATE-1, GATE-2, etc.) in command workflows
- **Parallel scope execution** — Multiple scope groups analyzed concurrently
- **Standard output envelope** — Unified `{status, summary, data, error}` format across commands
- **Test suite** — 63 tests covering commands, hooks, edge cases, and plugin structure
- **Permissions system** — Four levels (safe/balanced/permissive/full)
- **Dynamic context injection** — Commands use real-time context at load time
- **Tool restrictions** — `allowed-tools` frontmatter limits each command to declared tools
- **Explicit fixable definition** — Clear criteria in `/cco:optimize` for what can be auto-fixed
- **Scope detection rules** — Deterministic commit scope detection from file paths
- **Metric rationale** — Evidence-based thresholds in `/cco:align` with academic sources

### Changed

- **Core rules** — Now injected via hook instead of file copying
- **Project rules** — Copied to `./.claude/rules/` only (local, portable)
- **Rule files renamed** — All files now have `cco-` prefix
- **Folder structure** — `rules/core/`, `rules/languages/`, `rules/frameworks/`, `rules/operations/`
- **Claude Code 2.1.16+ compatibility** — Migrated from TodoWrite to task management system
- **Model optimization** — Haiku for file operations, Opus reserved for code fixes
- **Model strategy** — Opus + Haiku only (no Sonnet)
- **Commands streamlined** — Removed redundant explanations (~90 lines)
- **Agent output mandatory** — `cco-agent-analyze` guarantees valid JSON with error field
- **Rules optimized** — ~40% token reduction for Opus 4.5 compatibility
- **Tune expanded** — 8 questions with full auto-detection for all config values

### Fixed

- **Path traversal security** — Resolve paths before validation to prevent symlink bypasses
- **YAML frontmatter** — Quoted argument-hint values to prevent parsing errors
- **CI dependencies** — Added pyyaml for test execution
- **Task execution** — Switched to sync calls for reliable result handling

### Removed

- **compass-mcp** — MCP server removed (4000+ token overhead)
- **Global file operations** — No more writing to `~/.claude/`
- **18 redundant rules** — Merged or removed (c, cpp, zig, dart, lua, javascript, team, documentation, etc.)

### Migration

```bash
# If upgrading from v1, reset your project config:
/cco:tune --reset
```

---

## [1.0.0] - 2025-12-02

### Added

- **8 slash commands** — `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco-optimize`, `/cco-review`, `/cco-generate`, `/cco-refactor`, `/cco-commit`
- **3 specialized agents** — Explore, Plan, Action
- **85 standards** — 51 universal + 34 Claude-specific
- **Risk-based approval flow** — AskUserQuestion integration
- **Project-aware tuning** — Stack detection via `/cco-tune`
- **Doc-code mismatch detection** — SSOT resolution

### Technical

- Python 3.10+ support (tested on 3.10-3.14)
- Zero dependencies (stdlib only)
- CLI and IDE extension compatible
- 96% test coverage
