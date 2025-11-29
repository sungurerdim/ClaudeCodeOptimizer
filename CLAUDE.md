# ClaudeCodeOptimizer

<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: Process orchestration and quality standards for Claude Code
Team: Solo | Scale: <100 | Data: Public | Compliance: None
Stack: Python 3.11+ (stdlib only), ruff, mypy, pytest | Type: CLI | DB: None | Rollback: Git

## Guidelines
- Self-review sufficient, aggressive refactors OK
- Simple solutions preferred, optimize for clarity
- Basic input validation sufficient
- Clear error messages, help documentation
- No database migrations needed
- Simple git revert for rollback

## Operational
Tools: ruff (format+lint), mypy (types), pytest --cov (test)
Conventions: test_*.py naming, relative imports internal, snake_case
Applicable: security, tech-debt, tests, hygiene, cicd, docs, ai-quality, supply-chain
Not Applicable: database, performance, containers, api-contract, dora
<!-- CCO_CONTEXT_END -->
