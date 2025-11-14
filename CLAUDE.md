# Claude Code Development Guide


**Project:** ClaudeCodeOptimizer
**Team:** Solo Developer
**Quality:** Strict
**Testing:** Balanced
**Generated:** 2025-11-14

## Development Principles

<!-- CCO_PRINCIPLES_START -->
**Universal Principles** (apply to all projects):
- **U_ATOMIC_COMMITS**: Atomic Commits → `.claude/principles/U_ATOMIC_COMMITS.md`
- **U_CHANGE_VERIFICATION**: Change Verification Protocol → `.claude/principles/U_CHANGE_VERIFICATION.md`
- **U_COMPLETE_REPORTING**: Complete Action Reporting → `.claude/principles/U_COMPLETE_REPORTING.md`
- **U_CONCISE_COMMITS**: Concise Commit Messages → `.claude/principles/U_CONCISE_COMMITS.md`
- **U_DEPENDENCY_MANAGEMENT**: Dependency Management → `.claude/principles/U_DEPENDENCY_MANAGEMENT.md`
- **U_DRY**: DRY Enforcement & Single Source of Truth → `.claude/principles/U_DRY.md`
- **U_EVIDENCE_BASED**: Evidence-Based Verification → `.claude/principles/U_EVIDENCE_BASED.md`
- **U_EXPLICIT_COMPLETION**: Explicit Completion Criteria → `.claude/principles/U_EXPLICIT_COMPLETION.md`
- **U_FAIL_FAST**: Fail-Fast Error Handling → `.claude/principles/U_FAIL_FAST.md`
- **U_INTEGRATION_CHECK**: Complete Integration Check → `.claude/principles/U_INTEGRATION_CHECK.md`
- **U_MINIMAL_TOUCH**: Minimal Touch Policy → `.claude/principles/U_MINIMAL_TOUCH.md`
- **U_NO_OVERENGINEERING**: No Overengineering → `.claude/principles/U_NO_OVERENGINEERING.md`
- **U_ROOT_CAUSE_ANALYSIS**: Root Cause Analysis → `.claude/principles/U_ROOT_CAUSE_ANALYSIS.md`
- **U_TEST_FIRST**: Test-First Development → `.claude/principles/U_TEST_FIRST.md`

**Project-Specific Principles:**

*Code Quality:*
- **P_LINTING_SAST**: Linting & SAST Enforcement → `.claude/principles/P_LINTING_SAST.md`
- **P_TYPE_SAFETY**: Type Safety & Static Analysis → `.claude/principles/P_TYPE_SAFETY.md`
- **P_VERSION_MANAGEMENT**: Centralized Version Management → `.claude/principles/P_VERSION_MANAGEMENT.md`

*Architecture:*
- **P_API_VERSIONING_STRATEGY**: API Versioning Strategy → `.claude/principles/P_API_VERSIONING_STRATEGY.md`
- **P_EVENT_DRIVEN**: Event-Driven Architecture → `.claude/principles/P_EVENT_DRIVEN.md`

*Security & Privacy:*
- **P_AI_ML_SECURITY**: AI/ML Security → `.claude/principles/P_AI_ML_SECURITY.md`
- **P_AUDIT_LOGGING**: Audit Logging → `.claude/principles/P_AUDIT_LOGGING.md`
- **P_AUTH_AUTHZ**: Authentication & Authorization → `.claude/principles/P_AUTH_AUTHZ.md`
- **P_CONTAINER_SECURITY**: Container Security → `.claude/principles/P_CONTAINER_SECURITY.md`
- **P_ENCRYPTION_AT_REST**: Encryption Everywhere → `.claude/principles/P_ENCRYPTION_AT_REST.md`
- **P_K8S_SECURITY**: Kubernetes Security → `.claude/principles/P_K8S_SECURITY.md`
- **P_PRIVACY_COMPLIANCE**: Privacy Compliance → `.claude/principles/P_PRIVACY_COMPLIANCE.md`
- **P_PRIVACY_FIRST**: Privacy-First by Default → `.claude/principles/P_PRIVACY_FIRST.md`
- **P_RATE_LIMITING**: Rate Limiting & Throttling → `.claude/principles/P_RATE_LIMITING.md`
- **P_SCHEMA_VALIDATION**: Schema-First Validation → `.claude/principles/P_SCHEMA_VALIDATION.md`
- **P_SECRET_ROTATION**: Secret Management with Rotation → `.claude/principles/P_SECRET_ROTATION.md`
- **P_SQL_INJECTION**: SQL Injection Prevention → `.claude/principles/P_SQL_INJECTION.md`
- **P_SUPPLY_CHAIN_SECURITY**: Supply Chain Security → `.claude/principles/P_SUPPLY_CHAIN_SECURITY.md`
- **P_XSS_PREVENTION**: Input Sanitization (XSS Prevention) → `.claude/principles/P_XSS_PREVENTION.md`
- **P_ZERO_DISK_TOUCH**: Zero Disk Touch → `.claude/principles/P_ZERO_DISK_TOUCH.md`
- **P_ZERO_TRUST**: Zero Trust Architecture → `.claude/principles/P_ZERO_TRUST.md`

*Testing:*
- **P_CI_GATES**: CI Gates → `.claude/principles/P_CI_GATES.md`
- **P_INTEGRATION_TESTS**: Integration Tests for Critical Paths → `.claude/principles/P_INTEGRATION_TESTS.md`
- **P_TEST_COVERAGE**: Test Coverage Targets → `.claude/principles/P_TEST_COVERAGE.md`

*Performance:*
- **P_ASYNC_IO**: Async I/O (Non-Blocking Operations) → `.claude/principles/P_ASYNC_IO.md`
- **P_DB_OPTIMIZATION**: Database Query Optimization → `.claude/principles/P_DB_OPTIMIZATION.md`

*API Design:*
- **P_API_SECURITY**: API Security Best Practices → `.claude/principles/P_API_SECURITY.md`
<!-- CCO_PRINCIPLES_END -->

## Available Skills

<!-- CCO_SKILLS_START -->
- **Incremental Improvement** → `.claude/skills/incremental-improvement.md`
- **Async Patterns (Python)** → `.claude/skills/python/async-patterns.md`
- **Packaging Modern (Python)** → `.claude/skills/python/packaging-modern.md`
- **Performance (Python)** → `.claude/skills/python/performance.md`
- **Testing Pytest (Python)** → `.claude/skills/python/testing-pytest.md`
- **Type Hints Advanced (Python)** → `.claude/skills/python/type-hints-advanced.md`
- **Root Cause Analysis** → `.claude/skills/root-cause-analysis.md`
- **Security Emergency Response** → `.claude/skills/security-emergency-response.md`
- **Test First Verification** → `.claude/skills/test-first-verification.md`
- **Verification Protocol** → `.claude/skills/verification-protocol.md`
<!-- CCO_SKILLS_END -->

## Available Agents

<!-- CCO_AGENTS_START -->
- **Audit Agent** → `.claude/agents/audit-agent.md`
- **Fix Agent** → `.claude/agents/fix-agent.md`
- **Generate Agent** → `.claude/agents/generate-agent.md`
<!-- CCO_AGENTS_END -->

## Claude Guidelines

<!-- CCO_CLAUDE_START -->
- **C_AGENT_ORCHESTRATION_PATTERNS**: Agent Orchestration Patterns → `.claude/principles/C_AGENT_ORCHESTRATION_PATTERNS.md`
- **C_BREAKING_CHANGES_APPROVAL**: Breaking Changes Need Approval → `.claude/principles/C_BREAKING_CHANGES_APPROVAL.md`
- **C_CONTEXT_WINDOW_MGMT**: Context Window Management → `.claude/principles/C_CONTEXT_WINDOW_MGMT.md`
- **C_CRITICAL_CHANGES_PROPOSAL**: Critical Changes Require Proposal → `.claude/principles/C_CRITICAL_CHANGES_PROPOSAL.md`
- **C_CROSS_PLATFORM_BASH**: Cross-Platform Bash Commands → `.claude/principles/C_CROSS_PLATFORM_BASH.md`
- **C_FOLLOW_PATTERNS**: Follow Existing Patterns → `.claude/principles/C_FOLLOW_PATTERNS.md`
- **C_GREP_FIRST_SEARCH_STRATEGY**: Grep-First Search Strategy → `.claude/principles/C_GREP_FIRST_SEARCH_STRATEGY.md`
- **C_MINIMAL_TOUCH**: Minimal Touch Policy → `.claude/principles/C_MINIMAL_TOUCH.md`
- **C_MODEL_SELECTION**: Model Selection Strategy → `.claude/principles/C_MODEL_SELECTION.md`
- **C_NO_GIT_SUGGESTIONS**: No Git Commit Suggestions → `.claude/principles/C_NO_GIT_SUGGESTIONS.md`
- **C_NO_PROACTIVE_DOCS**: No Proactive Documentation → `.claude/principles/C_NO_PROACTIVE_DOCS.md`
- **C_NO_UNNECESSARY_FILES**: No Unnecessary File Creation → `.claude/principles/C_NO_UNNECESSARY_FILES.md`
- **C_NO_UNSOLICITED_TESTS**: No Unsolicited Tests or Linters → `.claude/principles/C_NO_UNSOLICITED_TESTS.md`
- **C_PARALLEL_AGENTS**: Use Parallel Agents for Performance → `.claude/principles/C_PARALLEL_AGENTS.md`
- **C_PREFER_EDITING**: Prefer Editing Over Creating → `.claude/principles/C_PREFER_EDITING.md`
- **C_PRODUCTION_GRADE**: Production-Grade Code Only → `.claude/principles/C_PRODUCTION_GRADE.md`
- **C_TOKEN_OPTIMIZATION**: Token Optimization → `.claude/principles/C_TOKEN_OPTIMIZATION.md`
<!-- CCO_CLAUDE_END -->
