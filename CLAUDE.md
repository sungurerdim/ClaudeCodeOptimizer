# ClaudeCodeOptimizer

<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: Process orchestration and quality standards for Claude Code
Team: Solo | Scale: <100 | Data: Public | Compliance: None
Stack: Python 3.11+ (stdlib only), ruff, mypy, pytest | Type: CLI | DB: None | Rollback: Git
Maturity: Greenfield | Breaking: Allowed | Priority: Speed

## AI Performance
Thinking: 8K | MCP: 25K | Caching: on

## Guidelines
- Self-review sufficient, aggressive refactors OK
- Simple solutions preferred, optimize for clarity
- Basic input validation sufficient
- Clear error messages, help documentation
- No database migrations needed
- Simple git revert for rollback
- Aggressive refactors OK, establish patterns early
- Clean API over compatibility, rename freely
- MVP mindset, ship fast, iterate

## Operational
Tools: ruff format . (format), ruff check . && mypy claudecodeoptimizer/ (lint), pytest tests/ --cov (test)
Conventions: test_*.py in tests/unit/ and tests/integration/, relative imports internal, snake_case
Applicable: security, tech-debt, tests, hygiene, cicd, docs, ai-quality, supply-chain, self-compliance
Not Applicable: database, performance, containers, api-contract, dora, ai-security, compliance

## Auto-Detected
Structure: single-repo | Hooks: none | Coverage: 96%
- [x] Linting configured
- [ ] Pre-commit hooks
- [ ] API endpoints
- [ ] Container setup
- [ ] i18n setup
License: MIT
Secrets detected: no
Outdated deps: 0
<!-- CCO_CONTEXT_END -->
