# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Standards restructured** into 4 clear categories: Universal (43), AI-Specific (31), CCO-Specific (38), Project-Specific (167 pool)
- **Agents consolidated**: `cco-agent-detect` + `cco-agent-scan` → `cco-agent-analyze`; `cco-agent-action` → `cco-agent-apply`
- **Commands simplified**: Removed AI-patterns detection, merged production readiness into `--pre-release` flag
- **Export logic clarified**: AGENTS.md excludes CCO-Specific, CLAUDE.md includes all
- **Documentation expanded**: Added `docs/commands.md`, `docs/agents.md`, `docs/standards.md`
- **CCO-Specific standards expanded**: Comprehensive workflow mechanisms (Command Flow, Fix Workflow, Approval Flow, Question Formatting, Output Formatting, Safety Classification, Impact Preview, Priority Levels, Context Integration, Claude Code Integration)

### Removed
- AI-Patterns Detection category from `/cco-audit` (Claude already handles this)
- Production Readiness Mode from `/cco-review` (use `/cco-audit --pre-release`)
- Redundant standard references from commands (now use CCO-Specific standards)

### Fixed
- Standard counts now consistent across all documentation (112 base + 167 pool)
- Removed overlap between standards categories

## [1.0.0] - 2025-12-02

### Added
- 8 slash commands: `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco-optimize`, `/cco-review`, `/cco-generate`, `/cco-refactor`, `/cco-commit`
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
- 100% test coverage
