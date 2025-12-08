# ClaudeCodeOptimizer

<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: Process and standards layer for Claude Code
Team: Solo | Scale: Small (100-1K) | Data: Public | Compliance: None
Stack: Python 3.10+, ruff, mypy, pytest (stdlib only) | Type: CLI | DB: None | Rollback: Git
Architecture: Monolith | API: None | Deployment: CI/CD
Maturity: Active | Breaking: Minimize | Priority: Quality
Testing: Standard | SLA: None | Real-time: None

## Guidelines
- Self-review sufficient, document for future
- Add basic caching, error tracking
- Basic validation sufficient
- Balanced refactors
- Deprecate first, provide migration path
- Standard practices, reasonable coverage

## Operational
Tools: ruff format . (format), ruff check . && mypy claudecodeoptimizer/ (lint), pytest tests/ --cov (test)
Conventions: test_*.py in tests/unit/ and tests/integration/, relative imports internal, snake_case
Applicable: security, tech-debt, tests, cicd, docs, supply-chain, self-compliance
Not Applicable: database, performance, containers, api-contract, dora, ai-security, ai-quality, compliance

## Auto-Detected
Structure: single-repo | Hooks: none | Coverage: 99%
- [x] Linting configured
- [x] CI/CD configured
- [x] Test framework
- [ ] Container/Cloud setup
- [ ] Pre-commit hooks
- [ ] API endpoints
- [ ] i18n setup
- [ ] SLA requirements
License: MIT
Secrets detected: no
Outdated deps: 0

## Conditional Standards (auto-applied)
**TOTAL: +20 project-specific (CLI +5, Ops +7, Caching +3, Testing +5)**

### Apps > CLI (+5) - Type: CLI detected
- Help: --help with examples for every command
- Exit Codes: 0 success, non-zero failure with meaning
- Signals: handle SIGINT/SIGTERM gracefully
- Output Modes: human-readable default, --json for scripts
- Config Precedence: env vars > config file > CLI args > defaults

### Backend > Operations (+7) - CI/CD detected
- Config as Code: versioned, validated, env-aware
- Health Endpoints: /health + /ready
- Graceful Shutdown: drain connections on SIGTERM
- Observability: metrics, logs, traces (OpenTelemetry)
- CI Gates: lint + test + coverage before merge
- Blue/Green or Canary: zero-downtime deployments
- Feature Flags: decouple deploy from release

### Scale > Caching Basics (+3) - Scale: Small (100-1K)
- Caching: TTL, invalidation strategy, cache-aside pattern
- Lazy Load: defer non-critical resources
- Connection Pool: reuse connections, appropriate sizing

### Testing > Standard (+5) - Testing: Standard
- Integration Tests: test component interactions
- Test Fixtures: reusable, maintainable
- Coverage Target: >80% line coverage
- CI Integration: tests run on every PR
- Snapshot Testing: UI component stability
<!-- CCO_CONTEXT_END -->
