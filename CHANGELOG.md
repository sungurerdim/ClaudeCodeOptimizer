# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-13

### Added
- **CC v2.1.6+ compatibility** - Statusline now uses `used_percentage` field when available (with fallback for older versions)
- **LSP tool permissions** - Added to all permission levels (safe, balanced, permissive, full) for code intelligence features
- **Claude 4.5 optimization rules** - New rules for explicit instructions, parallel tool batching, and subagent delegation
- **Context awareness rules** - Complete tasks fully, no self-limiting, checkpoint long tasks
- **Progressive context warning** - Statusline shows early warnings at 50%/70%/85% thresholds with token breakdown
- **Todo progress indicator** - Statusline displays current task from TodoWrite tool
- **Benchmark Reports tab** - Executive summary with AI-powered comparison and 6-dimension scoring
- **Explicit model parameters** - All agent calls now have explicit model specification for clarity and maintainability
- **Scope-aware remove** - Statusline and permissions remove now ask for Global/Local scope
- **Unattended mode** - `--auto` flag for cco-config and cco-optimize enables CI/CD and benchmark integration
- **Dependency audit in pre-flight** - Security advisories are blockers, outdated packages are warnings
- **Dependency check in review** - Default focus option with version comparison and risk assessment
- **Agent delegation rules** - Complexity-based delegation to cco-agent-research in cco-ai.md
- **Targeted quality gates** - cco-commit runs format/lint/type on changed files only (~85% token reduction)
- **Diff-only commit messages** - cco-commit generates messages only from git diff content, not session memory
- **Language-agnostic gates** - No hardcoded file extensions in quality checks
- **DEP:SmartContractEVM rules** - Solidity/Foundry/Hardhat best practices (CEI, reentrancy, gas optimization)
- **DEP:SmartContractSolana rules** - Anchor framework best practices (PDA, CPI, compute budget)
- **DEP:Effect rules** - Effect-TS patterns (composition, Schema, Layers, Fibers)
- **DEP:AISDK rules** - Vercel AI SDK patterns (streaming, tool calling, provider abstraction)
- **DEP:FormValidation rules** - Conform, Valibot, Arktype integration patterns
- **DEP:TanStack rules** - TanStack Router/Start patterns (file routes, loaders, search params)
- **Infra:APIGateway rules** - Kong/Traefik/APISIX patterns
- **Infra:ServiceMesh rules** - Istio/Linkerd patterns (mTLS, traffic split)
- **Infra:BuildCache rules** - Turbo/Nx remote cache patterns
- **398 trigger patterns** - Comprehensive detection coverage in cco-triggers.md
- **Comprehensive benchmark suite** - CCO evaluation with Docker support, date tracking, and refresh functionality
- **Comprehensive test suite** - Unit and integration tests for install, local, operations, and ui modules
- **Opus + Haiku model architecture** - Dual-model implementation for optimized performance
- **Orphan framework detection** - Modern 2025 technology triggers and game engine support
- **--dry-run flag for cco-install** - Preview installation changes before applying
- **Debug logging** - Windows UTF-8 encoding fix diagnostics
- **Meta command `/cco:preflight`** - Pre-release workflow with quality gate, architecture review, changelog & docs sync, and go/no-go summary
- **Meta command `/cco:checkup`** - Regular maintenance routine with health dashboard and full quality audit
- **New command `/cco:research`** - Multi-source research with reliability scoring, contradiction detection, consensus mapping, bias detection, and AI-synthesized recommendations
- **New command `/cco:commit`** - Secrets detection, large file warnings, breaking change detection, and staged/unstaged handling with Modify/Merge/Split/Edit options
- **New agent `cco-agent-research`** - External source research with tiered reliability scoring (T1-T6), contradiction detection, and AI synthesis
- **4 new scopes for `cco-agent-analyze`** - `references` (cross-file mapping), `architecture` (dependency graphs), `conventions` (pattern discovery), `trends` (historical metrics)
- **Agent Integration sections** - All commands now document which agents and scopes they use
- **`--hygiene` flag for `/cco:optimize`** - Quick cleanup combining orphans + stale-refs + duplicates
- **Enhanced `/cco:preflight` pre-flight** - Version sync, leftover markers, feature trace, install self-test, semver review
- **Cleanliness category in `/cco:optimize`** - Orphans, stale references, and duplicates moved from audit
- **Dynamic Context Injection** - Commands use `!` backtick syntax for real-time context at load time (git status, branch, project info available instantly)
- **Tool Restrictions** - `allowed-tools` frontmatter limits each command to declared tools only, preventing accidental destructive operations
- **7 new CCO-Specific rules** - Parallel Execution, Quick Mode, Conservative Judgment, Skip Criteria, Task Tracking, Dynamic Context, Tool Restrictions
- **Unified table format** - All rules now use `| * Rule | Description |` format for consistent counting
- **Local mode for `/cco:config`** - Project-specific statusline and permissions via `cco-install --local`
- **Statusline enhancements** - Git release tag display, improved layout with dot separators, Full/Minimal modes
- **Permissions system** - Four levels (safe/balanced/permissive/full) derived from full.json template
- **AI Performance config** - Auto-detection based on project complexity in `/cco:config`
- **Impact Preview** - Direct files, dependents, test coverage, and risk assessment in Fix Workflow
- **Detection exclusions** - Prevent false positives from benchmarks/, examples/, test fixtures
- **Pre-check validation** - Setup functions fail fast with helpful message if `~/.claude/` doesn't exist
- **Module-level VERBOSE flag** - Centralized verbose control in install_hook.py
- **Configurable subprocess timeouts** - `CCO_SUBPROCESS_TIMEOUT` and `CCO_SUBPROCESS_TIMEOUT_PACKAGE` environment variables
- **`@cli_entrypoint` decorator** - Standardized exception handling for CLI entry points (KeyboardInterrupt → 130, Exception → 1)
- **Option Batching** - Questions with >4 options now paginated with "All (N)" bulk selection on first page
- **Unified /cco:config flow** - Configure, Remove, and Export in single multiSelect question
- **Remove Configuration** - Remove any setting (AI Performance, Statusline, Permissions, Rules)
- **Export content selection** - User chooses which sections to include in export
- **Rule exemplars** - Correct/incorrect examples for Question Formatting to improve AI consistency
- **Verification checkpoints** - Pre-output verification rules for consistent behavior
- **Scope Reference table** - Complete scope documentation in `docs/agents.md` with purpose and coverage
- **best-practices scope** - Added to all relevant commands (optimize, review) for pattern adherence checks

### Breaking Changes
- **Command renames** - All commands renamed for consistency:
  - `/cco-tune` → `/cco:config`
  - `/cco-health` → `/cco:status`
  - `/cco-audit` → `/cco:optimize`
  - `/cco-refactor` → `/cco:review`
  - `/cco-generate` → `/cco:research`
- **Agent consolidation** - `cco-agent-detect` + `cco-agent-scan` → `cco-agent-analyze`; `cco-agent-action` → `cco-agent-apply`
- **Deprecated `setup_claude_md` function** - Use `clean_claude_md` instead

### Security
- **Path traversal fix** - Resolve paths before validation in `_is_safe_path` to prevent symlink/traversal bypasses

### Changed
- **Model optimization** - cco-config uses haiku for file operations (cost reduction), opus reserved for code fixes
- **Improved UX** - Skip options and verified defaults in commands
- **Optimized question flow** - Scope compatibility improvements in commands
- **Timeout constant naming** - SUBPROCESS_TIMEOUT_DEFAULT and SUBPROCESS_TIMEOUT_PACKAGE_OPS for clarity
- **Parameter ordering** - Standardized in operations.py functions
- **Standards → Rules restructure** - Renamed "standards" to "rules" throughout the project
- **Directory renamed** - `content/slash-commands/` → `content/command-templates/` for consistency with `agent-templates/`
- **4-category rules system** - `cco-core.md`, `cco-ai.md`, `cco-tools.md`, `cco-adaptive.md` in `~/.claude/rules/`
- **Token optimization** - Only core + ai rules always loaded; tools rules on-demand (~3000 tokens saved)
- **Markers updated** - `CCO_CORE_START`, `CCO_AI_START`, `CCO_TOOLS_START`, `CCO_ADAPTIVE_START`
- **On-demand tool rules** - Commands/agents load cco-tools.md via `!` backtick syntax when needed
- **Rules restructured** into 4 categories: Core (38), AI (32), Tools (110), Adaptive (120 pool)
- **Rules optimized** - Table format with inheritance pattern, -37.7% lines, -26.8% tokens
- **Export integrated into main flow** - No separate `--export` flag needed, select from Export section
- **Export reads installed files** - Reads from `~/.claude/CLAUDE.md` + `./CLAUDE.md`, not command specs
- **Question Formatting enhanced** - CRITICAL markers, exemplars, verification checkpoints for consistency
- **Agents consolidated**: `cco-agent-detect` + `cco-agent-scan` → `cco-agent-analyze`; `cco-agent-action` → `cco-agent-apply`
- **Question Formatting** - Standardized labels ([detected], [current], [recommended]), ascending option ordering
- **Rule counts** - Now calculated dynamically at runtime (no hardcoded values)
- **Cumulative tier system** - Scale, Testing, Observability tiers properly include lower tier rules
- **Documentation expanded** - Added `docs/commands.md`, `docs/agents.md`, `docs/rules.md`
- **CCO-Specific rules** - Comprehensive workflow mechanisms (Command Flow, Fix Workflow, Approval Flow, Question Formatting, Output Formatting, Safety Classification, Impact Preview, Priority Levels)
- **CCO marker pattern** - Universal backward-compatible pattern for clean upgrades from any version
- **Command consolidation** - `/cco:checkup` Phase 2 now runs all scopes (security, quality, hygiene, best-practices) in single pass, Phase 3 removed
- **Command consolidation** - `/cco:preflight` Phase 2 now runs all scopes in single pass, Phase 3 (Cleanliness) merged, phases renumbered (7→6)
- **Flag consistency** - Standardized on `--fix` flag across all commands (replaced `--auto-fix`)
- **Help text expanded** - `__main__.py` now lists all 8 commands with descriptions
- **Agent Selection table** - Updated with correct scope assignments and orchestration notes
- **Architecture refactoring** - Extracted `operations.py` (shared removal functions) and `ui.py` (display functions) for better separation of concerns
- **DRY improvements** - `save_json_file` utility now used consistently across all modules (replaces inline json.dumps patterns)
- **Error handling** - `save_json_file` now wraps IO errors in RuntimeError with context
- **Module restructure** - Split `cco_uninstall.py` (503 lines) into `uninstall/` package (detection.py, removal.py, __init__.py)

### Fixed
- **Benchmark server security** - Now binds to localhost only
- **Python 3.10 compatibility** - StrEnum string conversion for path operations
- **cco-commit title limit** - 50-character enforcement
- **Benchmark timeout handling** - Output decode fix
- **Statusline non-git display** - Shows project name when not in git repo
- Rule counts consistent across all documentation (141 core + 68 AI + 1155 adaptive = 1364 total)
- Detection exclusions for test/example directories prevent false Container triggers
- Statusline emoji width calculation for proper alignment
- CLI/Library projects excluded from Operations rules (use CI Only instead)
- Snapshot Testing requires Frontend detection
- Kubernetes separated from Container rules
- Connection Pool duplication removed
- AI performance settings cleaned from permission files
- **Migration cleanup** - Added `cco-tools.md` to old rule file cleanup list
- **Complete rule cleanup** - `remove_rules_dir()` now removes `tools.md` and `adaptive.md` from cco/ subdirectory
- **Detection completeness** - `has_rules_dir()` checks for all possible CCO rule files
- **Local CLAUDE.md cleanup** - `/cco:config` now removes ALL CCO markers for v1.0.0 compatibility
- **Related Commands duplicates** - Removed duplicate entries in cco-checkup.md and cco-preflight.md
- **v1.0.0 CHANGELOG** - Corrected command list to match actual release
- **README expanded** - Added comprehensive Claude Code Integration section with feature sources
- **Universal marker cleanup** - cco-config uses pattern matching for all `CCO_*_START/END` markers
- **README statusline params** - Aligned documentation with CLI (`cco-full`/`cco-minimal` instead of `full`/`minimal`)

### Removed
- AI-Patterns Detection category from `/cco:optimize` (Claude already handles this)
- Production Readiness Mode from `/cco:review` (use `/cco:optimize --pre-release`)
- Redundant rule references from commands (use CCO-Specific rules)
- Hardcoded rule counts (now dynamic)
- Duplicate rules across categories

## [1.0.0] - 2025-12-02

### Added
- 8 slash commands: `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco:review`, `/cco:optimize`, `/cco-refactor`, `/cco-generate`, `/cco:commit`
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
