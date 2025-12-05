# ClaudeCodeOptimizer

<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: Process and standards layer for Claude Code
Team: Solo | Scale: 100-10K | Data: Public | Compliance: None
Stack: Python 3.10+, ruff, mypy, pytest (stdlib only) | Type: CLI | DB: None | Rollback: Git
Maturity: Active | Breaking: Minimize | Priority: Quality

## AI Performance
Thinking: 8K | MCP: 25K | Caching: on

## Guidelines
- Self-review sufficient, balanced refactors, maintain momentum
- Consider caching strategies, add usage monitoring
- Basic input validation sufficient
- Clear error messages, help documentation
- No database migrations needed, simple git revert for rollback
- Deprecate first, provide migration path
- Thorough approach, no shortcuts

## Operational
Tools: ruff format . (format), ruff check . && mypy claudecodeoptimizer/ (lint), pytest tests/ --cov (test)
Conventions: test_*.py in tests/unit/ and tests/integration/, relative imports internal, snake_case
Applicable: security, tech-debt, tests, cicd, docs, supply-chain, self-compliance
Not Applicable: database, performance, containers, api-contract, dora, ai-security, ai-quality, compliance

## Auto-Detected
Structure: single-repo | Hooks: none | Coverage: 99%
- [x] Linting configured
- [x] CI/CD configured
- [ ] Pre-commit hooks
- [ ] API endpoints
- [ ] Container/Cloud setup
- [ ] i18n setup
- [ ] SLA requirements
License: MIT
Secrets detected: no
Outdated deps: 0

## Conditional Standards (auto-applied)
**Operations** (CI/CD detected):
- Config as Code: versioned, validated, env-aware
- Incremental Safety: stash → change → test → rollback on fail
<!-- CCO_CONTEXT_END -->
