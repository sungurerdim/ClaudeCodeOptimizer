# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-08

### Added
- **Dynamic Context Injection** - Commands use `!` backtick syntax for real-time context at load time (git status, branch, project info available instantly)
- **Tool Restrictions** - `allowed-tools` frontmatter limits each command to declared tools only, preventing accidental destructive operations
- **7 new CCO-Specific standards** - Parallel Execution, Quick Mode, Conservative Judgment, Skip Criteria, Task Tracking, Dynamic Context, Tool Restrictions
- **Unified table format** - All standards now use `| * Standard | Rule |` format for consistent counting with `grep -c "| \* "`
- **New command `/cco-research`** - Multi-source research with reliability scoring, contradiction detection, consensus mapping, bias detection, and AI-synthesized recommendations
- **New command `/cco-commit`** - Secrets detection, large file warnings, breaking change detection, and staged/unstaged handling with Modify/Merge/Split/Edit options
- **Local mode for `/cco-tune`** - Project-specific statusline and permissions via `cco-setup --local`
- **Statusline enhancements** - Git release tag display, improved layout with dot separators, Full/Minimal modes
- **Permissions system** - Four levels (safe/balanced/permissive/full) derived from full.json template
- **AI Performance config** - Auto-detection based on project complexity in `/cco-tune`
- **Impact Preview** - Direct files, dependents, test coverage, and risk assessment in Fix Workflow
- **Detection exclusions** - Prevent false positives from benchmarks/, examples/, test fixtures
- **Unified /cco-tune flow** - Configure, Remove, and Export in single multiSelect question
- **Remove Configuration** - Remove any setting (AI Performance, Statusline, Permissions, Standards)
- **Export content selection** - User chooses which sections to include in export
- **Standards exemplars** - Correct/incorrect examples for Question Formatting to improve AI consistency
- **Verification checkpoints** - Pre-output verification rules for consistent behavior

### Changed
- **Standards restructured** into 4 categories: Universal (38), AI-Specific (28), CCO-Specific (50), Project-Specific (170 pool)
- **Standards optimized** - Table format with inheritance pattern, -37.7% lines, -26.8% tokens
- **Export integrated into main flow** - No separate `--export` flag needed, select from Export section
- **Export reads installed files** - Reads from `~/.claude/CLAUDE.md` + `./CLAUDE.md`, not command specs
- **Question Formatting enhanced** - CRITICAL markers, exemplars, verification checkpoints for consistency
- **Agents consolidated**: `cco-agent-detect` + `cco-agent-scan` → `cco-agent-analyze`; `cco-agent-action` → `cco-agent-apply`
- **Question Formatting** - Standardized labels ([detected], [current], [recommended]), ascending option ordering
- **Standard counts** - Now calculated dynamically at runtime (no hardcoded values)
- **Cumulative tier system** - Scale, Testing, Observability tiers properly include lower tier standards
- **Documentation expanded** - Added `docs/commands.md`, `docs/agents.md`, `docs/standards.md`
- **CCO-Specific standards** - Comprehensive workflow mechanisms (Command Flow, Fix Workflow, Approval Flow, Question Formatting, Output Formatting, Safety Classification, Impact Preview, Priority Levels)
- **CCO marker pattern** - Universal backward-compatible pattern for clean upgrades from any version

### Fixed
- Standard counts consistent across all documentation (116 base + 170 pool)
- Detection exclusions for test/example directories prevent false Container triggers
- Statusline emoji width calculation for proper alignment
- CLI/Library projects excluded from Operations standards (use CI Only instead)
- Snapshot Testing requires Frontend detection
- Kubernetes separated from Container standards
- Connection Pool duplication removed
- AI performance settings cleaned from permission files
- Quick-install Python version and timeouts corrected

### Removed
- AI-Patterns Detection category from `/cco-audit` (Claude already handles this)
- Production Readiness Mode from `/cco-review` (use `/cco-audit --pre-release`)
- Redundant standard references from commands (use CCO-Specific standards)
- Hardcoded standard counts (now dynamic)
- Duplicate standards across categories

## [1.0.0] - 2025-12-02

### Added
- 7 slash commands: `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco-review`, `/cco-optimize`, `/cco-generate`, `/cco-refactor`
- 3 specialized agents: Detect, Scan, Action
- Standards system with Universal, AI-Specific, and Conditional categories
- Risk-based approval flow with AskUserQuestion
- Project-aware tuning via `/cco-tune`
- Doc-code mismatch detection with SSOT resolution
- AI context optimization principles
- Full alignment with Claude 4 Best Practices

### Technical
- Python 3.10+ support (tested on 3.10-3.14)
- Zero dependencies (stdlib only)
- CLI and IDE extension compatible
- 99% test coverage
