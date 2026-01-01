# Project Context

## Project Critical
Purpose: A process and rules layer for Claude Code in the Opus 4.5 era
Constraints: Zero runtime dependencies (stdlib only), Python 3.10+ compatibility
Invariants: 80% test coverage (CI requirement), Type-safe public APIs
Non-negotiables: Breaking changes allowed in v0.x, Speed over perfection

## Strategic Context
Team: Solo | Scale: Small (100-1K) | Data: Public | Compliance: None
Stack: Python 3.10+, ruff, mypy, pytest (stdlib only) | Type: CLI/Library | DB: None | Rollback: Git
Architecture: Monolith | API: None | Deployment: CI/CD (PyPI)
Maturity: Prototype | Breaking: Allowed | Priority: Speed
Testing: Standard (80% coverage) | SLA: None | Real-time: None

## Guidelines
- Ship fast, iterate quickly - speed over perfection
- Breaking changes OK in any release (v0.x approach)
- Proof of concept phase - may pivot or discard features
- Self-review sufficient, minimal documentation needed
- Basic caching and error tracking acceptable
- Standard test coverage maintained (80% from CI requirement)
- Zero runtime dependencies (stdlib only)
- Multi-version support (Python 3.10-3.14)

## Operational
Tools: ruff format . (format), ruff check . && mypy claudecodeoptimizer/ (lint), pytest tests/ --cov (test)
Conventions: test_*.py in tests/unit/ and tests/integration/, relative imports internal, snake_case
Release: GitHub Actions → PyPI on tag

## Auto-Detected
Structure: single-repo | Hooks: none | Coverage: 80% (CI requirement)
- [x] Linting configured (ruff)
- [x] Type checking (mypy)
- [x] CI/CD configured (GitHub Actions)
- [x] Test framework (pytest)
- [x] Security scanning (bandit, safety)
- [ ] Container/Cloud setup
- [ ] Pre-commit hooks

License: MIT
Secrets detected: no
