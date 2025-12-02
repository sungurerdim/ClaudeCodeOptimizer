# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-02

### Added
- 8 slash commands: `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco-optimize`, `/cco-review`, `/cco-generate`, `/cco-refactor`, `/cco-commit`
- 3 specialized agents: Detect, Scan, Action
- 94 standards (51 universal + 43 Claude-specific)
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
