<!-- CCO_HEADER_START -->
# Claude Code Development Guide

**Project:** ClaudeCodeOptimizer | **Team:** Solo Developer | **Quality:** Strict | **Testing:** Balanced
**Generated:** 2025-11-16
<!-- CCO_HEADER_END -->

<!-- CCO_PRINCIPLES_START -->
## Development Principles

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
- **P_API_VERSIONING_STRATEGY**: API Versioning Strategy → `.claude/principles/P_API_VERSIONING_STRATEGY.md`
- **P_AUDIT_LOGGING**: Audit Logging → `.claude/principles/P_AUDIT_LOGGING.md`
- **P_AUTO_VERSIONING**: Automated Semantic Versioning → `.claude/principles/P_AUTO_VERSIONING.md`
- **P_BRANCHING_STRATEGY**: Branching Strategy → `.claude/principles/P_BRANCHING_STRATEGY.md`
- **P_CI_GATES**: CI Gates → `.claude/principles/P_CI_GATES.md`
- **P_CODE_REVIEW_CHECKLIST_COMPLIANCE**: Code Review Checklist Compliance → `.claude/principles/P_CODE_REVIEW_CHECKLIST_COMPLIANCE.md`
- **P_COMMIT_MESSAGE_CONVENTIONS**: Commit Message Conventions → `.claude/principles/P_COMMIT_MESSAGE_CONVENTIONS.md`
- **P_COMPLIANCE_AS_CODE**: Compliance as Code → `.claude/principles/P_COMPLIANCE_AS_CODE.md`
- **P_CONFIGURATION_AS_CODE**: Configuration as Code → `.claude/principles/P_CONFIGURATION_AS_CODE.md`
- **P_CONTAINER_SECURITY**: Container Security → `.claude/principles/P_CONTAINER_SECURITY.md`
- **P_CONTINUOUS_PROFILING**: Continuous Profiling → `.claude/principles/P_CONTINUOUS_PROFILING.md`
- **P_DB_OPTIMIZATION**: Database Query Optimization → `.claude/principles/P_DB_OPTIMIZATION.md`
- **P_DEPENDENCY_INJECTION**: Dependency Injection → `.claude/principles/P_DEPENDENCY_INJECTION.md`
- **P_ENCRYPTION_AT_REST**: Encryption Everywhere → `.claude/principles/P_ENCRYPTION_AT_REST.md`
- **P_GITOPS_PRACTICES**: GitOps Practices → `.claude/principles/P_GITOPS_PRACTICES.md`
- **P_IAC_GITOPS**: Infrastructure as Code + GitOps → `.claude/principles/P_IAC_GITOPS.md`
- **P_IMMUTABILITY_BY_DEFAULT**: Immutability by Default → `.claude/principles/P_IMMUTABILITY_BY_DEFAULT.md`
- **P_INCIDENT_RESPONSE_READINESS**: Incident Response Readiness → `.claude/principles/P_INCIDENT_RESPONSE_READINESS.md`
- **P_INCREMENTAL_SAFETY_PATTERNS**: Incremental Safety Patterns → `.claude/principles/P_INCREMENTAL_SAFETY_PATTERNS.md`
- **P_LINTING_SAST**: Linting & SAST Enforcement → `.claude/principles/P_LINTING_SAST.md`
- **P_MINIMAL_RESPONSIBILITY**: Minimal Responsibility (Zero Maintenance) → `.claude/principles/P_MINIMAL_RESPONSIBILITY.md`
- **P_NO_BACKWARD_COMPAT_DEBT**: No Backward Compatibility Debt → `.claude/principles/P_NO_BACKWARD_COMPAT_DEBT.md`
- **P_PRECISION_IN_CALCS**: Precision in Calculations → `.claude/principles/P_PRECISION_IN_CALCS.md`
- **P_PRIVACY_COMPLIANCE**: Privacy Compliance → `.claude/principles/P_PRIVACY_COMPLIANCE.md`
- **P_PRIVACY_FIRST**: Privacy-First by Default → `.claude/principles/P_PRIVACY_FIRST.md`
- **P_PR_GUIDELINES**: PR Guidelines → `.claude/principles/P_PR_GUIDELINES.md`
- **P_SECRET_ROTATION**: Secret Management with Rotation → `.claude/principles/P_SECRET_ROTATION.md`
- **P_SEMANTIC_VERSIONING**: Semantic Versioning → `.claude/principles/P_SEMANTIC_VERSIONING.md`
- **P_SEPARATION_OF_CONCERNS**: Separation of Concerns → `.claude/principles/P_SEPARATION_OF_CONCERNS.md`
- **P_SINGLETON_EXPENSIVE_RESOURCES**: Singleton Pattern for Expensive Resources → `.claude/principles/P_SINGLETON_EXPENSIVE_RESOURCES.md`
- **P_SUPPLY_CHAIN_SECURITY**: Supply Chain Security → `.claude/principles/P_SUPPLY_CHAIN_SECURITY.md`
- **P_TEST_COVERAGE**: Test Coverage Targets → `.claude/principles/P_TEST_COVERAGE.md`
- **P_TEST_ISOLATION**: Test Isolation → `.claude/principles/P_TEST_ISOLATION.md`
- **P_TEST_PYRAMID**: Test Pyramid → `.claude/principles/P_TEST_PYRAMID.md`
- **P_TTL_BASED_CLEANUP**: TTL-Based Cleanup → `.claude/principles/P_TTL_BASED_CLEANUP.md`
- **P_TYPE_SAFETY**: Type Safety & Static Analysis → `.claude/principles/P_TYPE_SAFETY.md`
- **P_VERSION_MANAGEMENT**: Centralized Version Management → `.claude/principles/P_VERSION_MANAGEMENT.md`
- **P_ZERO_DISK_TOUCH**: Zero Disk Touch → `.claude/principles/P_ZERO_DISK_TOUCH.md`
<!-- CCO_PRINCIPLES_END -->

<!-- CCO_SKILLS_START -->
## Available Skills

- **Incremental Improvement Protocol** → `.claude/skills/cco-skill-incremental-improvement.md`
- **Root Cause Analysis** → `.claude/skills/cco-skill-root-cause-analysis.md`
- **Security Emergency Response** → `.claude/skills/cco-skill-security-emergency-response.md`
- **Test-First Verification** → `.claude/skills/cco-skill-test-first-verification.md`
- **Verification Protocol** → `.claude/skills/cco-skill-verification-protocol.md`
- **Python Async Patterns** → `.claude/skills/cco-skill-async-patterns.md`
- **Modern Python Packaging** → `.claude/skills/cco-skill-packaging-modern.md`
- **Python Performance Optimization** → `.claude/skills/cco-skill-performance.md`
- **Pytest Testing Patterns** → `.claude/skills/cco-skill-testing-pytest.md`
- **Advanced Python Type Hints** → `.claude/skills/cco-skill-type-hints-advanced.md`
<!-- CCO_SKILLS_END -->

<!-- CCO_AGENTS_START -->
## Available Agents

- **Audit Agent** → `.claude/agents/cco-agent-audit.md`
- **Fix Agent** → `.claude/agents/cco-agent-fix.md`
- **Generate Agent** → `.claude/agents/cco-agent-generate.md`
<!-- CCO_AGENTS_END -->

<!-- CCO_COMMANDS_START -->
## Available Commands

- **/cco-analyze-dependencies**: Analyze Dependencies
- **/cco-audit-all**: Audit All
- **/cco-audit-code**: Audit Code
- **/cco-audit-docs**: Audit Docs
- **/cco-audit-principles**: Audit Principles
- **/cco-check-principle**: Check Principle
- **/cco-configure**: Configure
- **/cco-fix-code**: Fix Code
- **/cco-fix-docs**: Fix Docs
- **/cco-fix-security**: Fix Security
- **/cco-generate-tests**: Generate Tests
- **/cco-help**: Help
- **/cco-optimize-docs**: Optimize Docs
- **/cco-self-optimize**: Self Optimize
- **/cco-setup-cicd**: Setup Cicd
- **/cco-status**: Project Status Check
- **/cco-sync-spec-to-code**: Sync Spec To Code
- **/cco-verify-implementation**: Verify Implementation
<!-- CCO_COMMANDS_END -->

<!-- CCO_GUIDES_START -->
## Available Guides

- **Git Workflow** → `.claude/guides/cco-git-workflow.md`
- **Security Incident Response** → `.claude/guides/cco-security-response.md`
- **Verification Protocol** → `.claude/guides/cco-verification-protocol.md`
<!-- CCO_GUIDES_END -->

<!-- CCO_CLAUDE_START -->
## Claude Guidelines

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

