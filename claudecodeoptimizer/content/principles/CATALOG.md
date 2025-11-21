# CCO Principles Index

**Complete reference for all CCO principles**

---

## Summary

**Total Principles**: 110

**Categories**:
- **Universal (U_*)**: 6 - Core development best practices (apply everywhere)
- **Claude-Specific (C_*)**: 13 - Optimizations for Claude Code
- **Project-Specific (P_*)**: 91 - Optional per-project overrides

---

## Table of Contents

- [Universal Principles (U_*)](#universal-principles-u_)
- [Claude-Specific Principles (C_*)](#claude-specific-principles-c_)
- [Project-Specific Principles (P_*)](#project-specific-principles-p_)
  - [Security](#security)
  - [Testing & Quality](#testing--quality)
  - [Infrastructure & DevOps](#infrastructure--devops)
  - [Architecture & Design](#architecture--design)
  - [Observability & Monitoring](#observability--monitoring)
  - [Performance](#performance)
  - [Git & Versioning](#git--versioning)
  - [Documentation](#documentation)

---

## Universal Principles (U_*)

**Core development best practices - Apply everywhere**

These principles are fundamental to all development work, regardless of language, framework, or project type.

### 1. U_CHANGE_VERIFICATION

**Verify all changes BEFORE claiming completion**

- Never claim "done" without evidence
- Run commands, check outputs, confirm results
- Prevents incomplete work and integration failures

**File**: `U_CHANGE_VERIFICATION.md`

---

### 2. U_COMPLETE_REPORTING

**Every action must be explicitly reported with precise file references**

- Always use `file_path:line_number` format
- Report all actions (reads, edits, searches)
- No hidden operations

**File**: `U_COMPLETE_REPORTING.md`

---

### 3. U_DRY

**Every piece of knowledge must have a single, unambiguous representation**

- No duplicate functions or data
- Database = truth, cache = derived
- Configuration defined once, referenced everywhere

**File**: `U_DRY.md`

---

### 4. U_EVIDENCE_BASED_ANALYSIS

**Never claim completion without command execution proof**

- Show command output, exit codes, timestamps
- Use 5 Whys for root cause analysis
- Fix at source, not symptom

**File**: `U_EVIDENCE_BASED_ANALYSIS.md`

---

### 5. U_MINIMAL_TOUCH

**Edit only required files - No drive-by improvements**

- Touch ONLY files REQUIRED for task
- No scope creep, no "while I'm here" changes
- Surgical, focused edits only

**File**: `U_MINIMAL_TOUCH.md`

---

### 6. U_NO_OVERENGINEERING

**Choose simplest solution - Avoid premature abstraction**

- Solve current problem, not hypothetical ones
- Extract abstractions after 3rd duplication (Rule of Three)
- Simple > complex, always

**File**: `U_NO_OVERENGINEERING.md`

---

## Claude-Specific Principles (C_*)

**Optimizations for Claude Code - Claude AI best practices**

These principles optimize Claude Code's behavior for efficiency, cost, and quality.

### 1. C_AGENT_ORCHESTRATION_PATTERNS

**Use parallel agents, pipelines, and appropriate model selection**

- Parallel fan-out for independent tasks
- Sequential pipeline for dependencies
- Haiku for simple, Sonnet for development, Opus for architecture

**File**: `C_AGENT_ORCHESTRATION_PATTERNS.md`

---

### 2. C_BREAKING_CHANGES_APPROVAL

**Never make breaking changes without explicit user approval**

- Detect breaking changes before implementation
- Propose with full context and migration path
- Offer non-breaking alternatives

**File**: `C_BREAKING_CHANGES_APPROVAL.md`

---

### 3. C_COMMAND_CONTEXT_PASSING

**Always pass context when calling another slash command**

- Provide summary, file paths, counts before SlashCommand call
- Eliminates duplicate analysis
- Significantly faster execution

**File**: `C_COMMAND_CONTEXT_PASSING.md`

---

### 4. C_CONTEXT_WINDOW_MGMT

**Optimize context via targeted reads and strategic model selection**

- Grep → Preview → Precise Read (3-stage strategy)
- Use offset+limit for large files
- Parallel operations where independent

**File**: `C_CONTEXT_WINDOW_MGMT.md`

---

### 5. C_CROSS_PLATFORM_BASH

**Use cross-platform compatible commands and paths**

- Always forward slashes (Windows accepts them)
- Git Bash commands (ls, grep, cat, find)
- Quote paths with spaces

**File**: `C_CROSS_PLATFORM_BASH.md`

---

### 6. C_EFFICIENT_FILE_OPERATIONS

**Grep-first: discovery → preview → precise read**

- Stage 1: files_with_matches (find which files)
- Stage 2: content with context (verify relevance)
- Stage 3: targeted Read with offset+limit (exact section)

**File**: `C_EFFICIENT_FILE_OPERATIONS.md`

---

### 7. C_FOLLOW_PATTERNS

**Always follow existing code patterns and conventions**

- Examine existing code first
- Match naming conventions exactly
- Consistency > personal preference

**File**: `C_FOLLOW_PATTERNS.md`

---

### 8. C_HONEST_REPORTING

**Report exact truth only - Never claim without verification**

- Distinguish difficulty from impossibility accurately
- Complete accounting (all items have disposition)
- Consistent counts (single source of truth)

**File**: `C_HONEST_REPORTING.md`

---

### 9. C_MODEL_SELECTION

**Choose appropriate model based on task complexity**

- Haiku: Grep, format, read, simple edits
- Sonnet: Features, bugs, code review (default)
- Opus: Architecture, complex algorithms (rare)

**File**: `C_MODEL_SELECTION.md`

---

### 10. C_NATIVE_TOOL_INTERACTIONS

**All user interactions must use native Claude Code tools**

- Use AskUserQuestion (not text prompts)
- Every multiSelect must have "All" option first
- Consistent UI, validation, accessibility

**File**: `C_NATIVE_TOOL_INTERACTIONS.md`

---

### 11. C_NO_HARDCODED_EXAMPLES

**Never use hardcoded examples in templates**

- Use placeholders: {FILE_PATH}, {LINE_NUMBER}, {FUNCTION_NAME}
- AI models cannot distinguish example from real data
- Runtime outputs must use actual project data

**File**: `C_NO_HARDCODED_EXAMPLES.md`

---

### 12. C_NO_UNSOLICITED_FILE_CREATION

**Never create files unless explicitly requested**

- Prefer editing existing files
- Always ask before creating documentation
- Avoid temp files (use sandboxed .tmp/)

**File**: `C_NO_UNSOLICITED_FILE_CREATION.md`

---

### 13. C_PROJECT_CONTEXT_DISCOVERY

**Use Haiku sub-agent to extract project context before analysis**

- Read README, CONTRIBUTING, ARCHITECTURE docs
- Extract goals, conventions, tech stack
- Align findings with project objectives

**File**: `C_PROJECT_CONTEXT_DISCOVERY.md`

---

### 14. C_TEMP_FILE_SANDBOXING

**Only create temp files in project .tmp/ directory**

- ONLY allowed: {PROJECT_ROOT}/.tmp/
- FORBIDDEN: /tmp, C:\tmp, D:\tmp, ~/.claude/.tmp/
- Path verification before ANY file operation

**File**: `C_TEMP_FILE_SANDBOXING.md`

---

## Project-Specific Principles (P_*)

**Optional per-project overrides - 91 available**

These are optional principles you can enable for specific projects. They cover domain-specific best practices.

### Security

Authentication, authorization, encryption, vulnerability prevention

- `P_API_SECURITY.md` - API security best practices
- `P_AUTH_AUTHZ.md` - Authentication and authorization
- `P_CONTAINER_SECURITY.md` - Docker/container security
- `P_CORS_POLICY.md` - CORS configuration
- `P_ENCRYPTION_AT_REST.md` - Data encryption
- `P_K8S_SECURITY.md` - Kubernetes security
- `P_PII_MASKING_IN_LOGS.md` - Privacy in logs
- `P_PRIVACY_COMPREHENSIVE.md` - GDPR compliance
- `P_SECRET_ROTATION.md` - Credential management
- `P_SQL_INJECTION.md` - SQL injection prevention
- `P_SUPPLY_CHAIN_SECURITY.md` - Dependency scanning
- `P_XSS_PREVENTION.md` - Cross-site scripting prevention
- `P_ZERO_TRUST.md` - Zero trust security model

**Total Security Principles**: 13

---

### Testing & Quality

Test pyramid, coverage, TDD, quality gates

- `P_CODE_REVIEW_CHECKLIST_COMPLIANCE.md` - PR review standards
- `P_CODE_SMELL_DETECTION.md` - Anti-pattern detection
- `P_COGNITIVE_COMPLEXITY.md` - Complexity limits
- `P_CYCLOMATIC_COMPLEXITY_LIMITS.md` - Code complexity
- `P_INTEGRATION_CHECK.md` - Integration validation
- `P_INTEGRATION_TESTS.md` - Integration testing
- `P_LINTING_SAST.md` - Static analysis
- `P_PROPERTY_TESTING.md` - Property-based testing
- `P_REFACTORING_PATTERNS.md` - Safe refactoring
- `P_TEST_COVERAGE.md` - Coverage targets
- `P_TEST_FIRST_TDD.md` - Test-driven development
- `P_TEST_ISOLATION.md` - Test independence
- `P_TEST_PYRAMID.md` - Test strategy

**Total Testing Principles**: 13

---

### Infrastructure & DevOps

CI/CD, containers, deployment, infrastructure as code

- `P_BLUE_GREEN_DEPLOYMENT.md` - Zero-downtime deployments
- `P_CANARY_RELEASES.md` - Gradual rollouts
- `P_CI_GATES.md` - Quality gates
- `P_COMPLIANCE_AS_CODE.md` - Automated compliance
- `P_CONFIGURATION_AS_CODE.md` - Config management
- `P_DEPLOYMENT_BLUEGREEN_CANARY_ROLLBACK.md` - Deployment strategies
- `P_GRACEFUL_SHUTDOWN.md` - Clean shutdown
- `P_HEALTH_CHECKS.md` - Service health
- `P_IAC_GITOPS.md` - Infrastructure as code
- `P_ROLLBACK_STRATEGY.md` - Rollback procedures

**Total Infrastructure Principles**: 10

---

### Architecture & Design

Microservices, patterns, distributed systems

- `P_BULKHEAD_PATTERN.md` - Failure isolation
- `P_CIRCUIT_BREAKER_PATTERN.md` - Cascading failure prevention
- `P_CQRS_PATTERN.md` - Command Query Responsibility Segregation
- `P_DEPENDENCY_INJECTION.md` - Inversion of control
- `P_EVENT_DRIVEN.md` - Event-driven architecture
- `P_MICROSERVICES_SERVICE_MESH.md` - Service mesh patterns
- `P_SEPARATION_OF_CONCERNS.md` - Clean architecture
- `P_SINGLETON_EXPENSIVE_RESOURCES.md` - Resource management

**Total Architecture Principles**: 8

---

### Observability & Monitoring

Logging, metrics, tracing, alerting

- `P_AUDIT_LOGGING.md` - Audit trail
- `P_CENTRALIZED_LOGGING.md` - Log aggregation
- `P_CONTINUOUS_PROFILING.md` - Performance profiling
- `P_CORRELATION_IDS.md` - Distributed tracing
- `P_ERROR_BUDGETS.md` - SLO tracking
- `P_LOG_LEVELS_STRATEGY.md` - Log level guidelines
- `P_OBSERVABILITY_WITH_OTEL.md` - OpenTelemetry
- `P_STRUCTURED_LOGGING.md` - Structured logs

**Total Observability Principles**: 8

---

### Performance

Optimization, caching, profiling

- `P_ASYNC_IO.md` - Asynchronous operations
- `P_CACHING_STRATEGY.md` - Cache patterns
- `P_DB_OPTIMIZATION.md` - Database performance
- `P_LAZY_LOADING.md` - Deferred loading
- `P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE.md` - Measure first

**Total Performance Principles**: 5

---

### Git & Versioning

Branching, commits, versioning

- `P_AUTO_VERSIONING.md` - Automated versioning
- `P_BRANCHING_STRATEGY.md` - Git branching
- `P_CHANGELOG_MAINTENANCE.md` - Changelog
- `P_COMMIT_MESSAGE_CONVENTIONS.md` - Commit standards
- `P_GIT_COMMIT_QUALITY.md` - Quality commits
- `P_PR_GUIDELINES.md` - Pull request standards
- `P_REBASE_VS_MERGE_STRATEGY.md` - Merge strategy
- `P_SEMANTIC_VERSIONING.md` - SemVer

**Total Git Principles**: 8

---

### Documentation

API docs, ADRs, runbooks

- `P_ADR_ARCHITECTURE_DECISIONS.md` - Architecture decision records
- `P_API_DOCUMENTATION_OPENAPI.md` - OpenAPI specs
- `P_API_VERSIONING_STRATEGY.md` - API versioning
- `P_CODE_DOCUMENTATION_STANDARDS.md` - Docstring standards
- `P_RESTFUL_API_CONVENTIONS.md` - REST conventions
- `P_RUNBOOK_OPERATIONAL_DOCS.md` - Operational docs

**Total Documentation Principles**: 6

---

### Resilience & Reliability

Retries, timeouts, fallbacks

- `P_DEAD_LETTER_QUEUE.md` - Failed message handling
- `P_FAIL_FAST_STRATEGY.md` - Fail fast
- `P_FEATURE_FLAGS.md` - Feature toggles
- `P_GRACEFUL_DEGRADATION.md` - Partial functionality
- `P_INCIDENT_RESPONSE_READINESS.md` - Incident handling
- `P_RETRY_WITH_BACKOFF.md` - Retry patterns
- `P_TIMEOUT_CONFIGURATION.md` - Timeout strategy

**Total Resilience Principles**: 7

---

### Other

Miscellaneous best practices

- `P_DEPENDENCY_MANAGEMENT.md` - Dependency hygiene
- `P_IMMUTABILITY_BY_DEFAULT.md` - Immutable data
- `P_INCREMENTAL_SAFETY_PATTERNS.md` - Progressive safety
- `P_MINIMAL_RESPONSIBILITY.md` - Single responsibility
- `P_NO_BACKWARD_COMPAT_DEBT.md` - Avoid legacy cruft
- `P_PRECISION_IN_CALCS.md` - Numerical precision
- `P_PRODUCTION_GRADE.md` - Production readiness
- `P_SCHEMA_VALIDATION.md` - Input validation
- `P_TECHNICAL_DEBT_TRACKING.md` - Debt management
- `P_TTL_BASED_CLEANUP.md` - Automatic cleanup
- `P_TYPE_SAFETY.md` - Type systems
- `P_VERSION_MANAGEMENT.md` - Version control
- `P_ZERO_DISK_TOUCH.md` - Minimize I/O

**Total Other Principles**: 13

---

## Using Principles

### In CLAUDE.md

Principles are automatically injected via markers:

```markdown
<!-- CCO_PRINCIPLES_START -->
@principles/U_CHANGE_VERIFICATION.md
@principles/C_HONEST_REPORTING.md
<!-- CCO_PRINCIPLES_END -->
```

See [ADR-001: Marker-based CLAUDE.md System](../../docs/ADR/001-marker-based-claude-md.md)

### Principle Selection

- **Universal (U_*)**: Always loaded (6 principles)
- **Claude (C_*)**: Always loaded (13 principles)
- **Project (P_*)**: Optional, enable per project needs

### Adding Project Principles

1. Identify needed principles from P_* list above
2. Add to CLAUDE.md between CCO_PRINCIPLES markers
3. Principles activate automatically via Claude Code

---

## Principle Compliance

All CCO components (commands, skills, agents) follow these principles:

- ✅ No hardcoded examples (C_NO_HARDCODED_EXAMPLES)
- ✅ Native tool interactions (C_NATIVE_TOOL_INTERACTIONS)
- ✅ Honest reporting (C_HONEST_REPORTING)
- ✅ Evidence-based (U_EVIDENCE_BASED_ANALYSIS)
- ✅ Complete accounting (C_HONEST_REPORTING)

See [PR Template](../../.github/PULL_REQUEST_TEMPLATE.md) for full compliance checklist.

---

**Total**: 110 principles across 3 categories
