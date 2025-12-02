# ClaudeCodeOptimizer

<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: Process orchestration and quality standards for Claude Code
Team: Solo | Scale: <100 | Data: Public | Compliance: None
Stack: Python 3.10+, ruff, mypy, pytest (stdlib only) | Type: CLI | DB: None | Rollback: Git
Maturity: Greenfield | Breaking: Allowed | Priority: Speed

## AI Performance
Thinking: 8K | MCP: 25K | Caching: on

## Guidelines
- Self-review sufficient, aggressive refactors OK, establish patterns early
- Simple solutions preferred, optimize for clarity
- Basic input validation sufficient
- Clear error messages, help documentation
- No database migrations needed, simple git revert for rollback
- Clean API over compatibility, rename freely
- MVP mindset, ship fast, iterate

## Operational
Tools: ruff format . (format), ruff check . && mypy claudecodeoptimizer/ (lint), pytest tests/ --cov (test)
Conventions: test_*.py in tests/unit/ and tests/integration/, relative imports internal, snake_case
Applicable: security, tech-debt, tests, hygiene, cicd, docs, supply-chain, self-compliance
Not Applicable: database, performance, containers, api-contract, dora, ai-security, ai-quality, compliance

## Auto-Detected
Structure: single-repo | Hooks: none | Coverage: 87%
- [x] Linting configured
- [x] CI/CD configured
- [ ] Pre-commit hooks
- [ ] API endpoints
- [ ] Container/Cloud setup
- [ ] i18n setup
- [ ] SLA requirements
License: MIT
Secrets detected: no
Outdated deps: 3

## Conditional Standards (auto-applied)
**Operations** (CI/CD detected):
- Config as Code: versioned, validated, env-aware
- Incremental Safety: stash → change → test → rollback on fail
<!-- CCO_CONTEXT_END -->
