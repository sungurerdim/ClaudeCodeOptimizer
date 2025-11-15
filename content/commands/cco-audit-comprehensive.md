---
description: Comprehensive audit (code, security, tests, docs, principles, all)
category: audit
cost: 5
principles: ['U_EVIDENCE_BASED', 'U_FAIL_FAST', 'U_ATOMIC_COMMITS', 'U_CONCISE_COMMITS', 'U_NO_OVERENGINEERING', 'U_DRY', 'U_INTEGRATION_CHECK', 'P_NO_BACKWARD_COMPAT_DEBT', 'P_PRECISION_IN_CALCS', 'P_IMMUTABILITY_BY_DEFAULT', 'P_CODE_REVIEW_CHECKLIST_COMPLIANCE', 'P_LINTING_SAST', 'P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE', 'P_TYPE_SAFETY', 'P_VERSION_MANAGEMENT', 'C_GREP_FIRST_SEARCH_STRATEGY', 'P_EVENT_DRIVEN', 'P_SINGLETON_EXPENSIVE_RESOURCES', 'P_SEPARATION_OF_CONCERNS', 'P_MICROSERVICES_SERVICE_MESH', 'P_CQRS_PATTERN', 'P_DEPENDENCY_INJECTION', 'P_CIRCUIT_BREAKER_PATTERN', 'P_API_VERSIONING_STRATEGY', 'C_AGENT_ORCHESTRATION_PATTERNS', 'C_CONTEXT_WINDOW_MGMT', 'P_SCHEMA_VALIDATION', 'P_PRIVACY_FIRST', 'P_TTL_BASED_CLEANUP', 'P_ENCRYPTION_AT_REST', 'P_ZERO_DISK_TOUCH', 'P_AUTH_AUTHZ', 'P_SQL_INJECTION', 'P_SECRET_ROTATION', 'P_RATE_LIMITING', 'P_CORS_POLICY', 'P_XSS_PREVENTION', 'P_AUDIT_LOGGING', 'P_SUPPLY_CHAIN_SECURITY', 'P_AI_ML_SECURITY', 'P_CONTAINER_SECURITY', 'P_K8S_SECURITY', 'P_ZERO_TRUST', 'P_PRIVACY_COMPLIANCE', 'U_DEPENDENCY_MANAGEMENT', 'P_TEST_COVERAGE', 'P_TEST_ISOLATION', 'P_INTEGRATION_TESTS', 'P_TEST_PYRAMID', 'P_CI_GATES', 'P_PROPERTY_TESTING', 'P_COMMIT_MESSAGE_CONVENTIONS', 'P_BRANCHING_STRATEGY', 'P_PR_GUIDELINES', 'P_REBASE_VS_MERGE_STRATEGY', 'P_SEMANTIC_VERSIONING', 'P_AUTO_VERSIONING', 'P_CACHING_STRATEGY', 'P_DB_OPTIMIZATION', 'P_LAZY_LOADING', 'P_ASYNC_IO', 'P_CONTINUOUS_PROFILING', 'P_MINIMAL_RESPONSIBILITY', 'P_CONFIGURATION_AS_CODE', 'P_IAC_GITOPS', 'P_OBSERVABILITY_WITH_OTEL', 'P_HEALTH_CHECKS', 'P_GRACEFUL_SHUTDOWN', 'P_GITOPS_PRACTICES', 'P_INCIDENT_RESPONSE_READINESS', 'P_RESTFUL_API_CONVENTIONS', 'P_API_SECURITY']
---

# cco-audit-comprehensive - Comprehensive Audit (All Categories)

> **NOTE**: This is the comprehensive audit that covers everything. For faster, focused audits, consider using:
> - `/cco-audit-security` - Security vulnerabilities and privacy violations only
> - `/cco-audit-performance` - Performance bottlenecks only
> - `/cco-audit-architecture` - Architectural patterns only
> - `/cco-audit-testing` - Test coverage and quality only
> - `/cco-audit-code-quality` - Code quality and linting only

Run comprehensive audits on your codebase: code quality, security, tests, documentation, and principle compliance.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, thorough)
- File scanning and pattern detection
- Running linters and type checkers
- Collecting metrics and violations
- Cost-effective for repetitive checks

**Analysis & Reasoning**: Sonnet (Plan agent)
- Violation severity assessment
- Cross-reference with principles
- Prioritization and recommendations
- Comprehensive audit report generation

**Execution Pattern**:
1. Launch parallel Haiku agents for different audit types:
   - Code quality checks (linting, formatting, types)
   - Security scans (secrets, vulnerabilities)
   - Test analysis (coverage, flaky tests)
   - Documentation checks (completeness, accuracy)
2. Aggregate findings with Sonnet
3. Generate prioritized action items

**Model Requirements**:
- Haiku for all scanning and collection tasks
- Sonnet for final analysis and report

---

## Prerequisites: Load Required Context

**CRITICAL**: Before running any audit, load and verify required documents.

### 1. Auto-Load Relevant Principles (Progressive Disclosure)

The following principles are automatically loaded for audit commands:

**Core Principles** (Always loaded from CLAUDE.md):
- U_FAIL_FAST: Fail-Fast Error Handling
- U_EVIDENCE_BASED: Evidence-Based Verification
- U_NO_OVERENGINEERING: No Overengineering

**Additional Principles for This Command**:
Automatically loaded from `~/.cco/principles/`:
- All principles from `code_quality.md`
- All principles from `security_privacy.md`
- All principles from `testing.md`


Automatically loaded from `~/.cco/principles/`:
- U_DRY
- U_INTEGRATION_CHECK
- P_NO_BACKWARD_COMPAT_DEBT
- P_PRECISION_IN_CALCS
- P_CODE_REVIEW_CHECKLIST_COMPLIANCE
- P_LINTING_SAST
- P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE
- P_TYPE_SAFETY
- P_VERSION_MANAGEMENT
- P_PRIVACY_FIRST
- P_CACHING_STRATEGY
- P_DISTRIBUTED_CACHING
- P_RESTFUL_API_CONVENTIONS
- U_NO_OVERENGINEERING
- P_IMMUTABILITY_BY_DEFAULT
- P_API_VERSIONING_STRATEGY
- C_AGENT_ORCHESTRATION_PATTERNS
- C_CONTEXT_WINDOW_MGMT
- P_SCHEMA_VALIDATION
- P_TTL_BASED_CLEANUP
- P_ENCRYPTION_AT_REST
- P_ZERO_DISK_TOUCH
- P_AUTH_AUTHZ
- P_SQL_INJECTION
- P_SECRET_ROTATION
- P_RATE_LIMITING
- P_DB_OPTIMIZATION
- P_LAZY_LOADING
- P_ASYNC_IO
- P_CONTINUOUS_PROFILING
- P_MINIMAL_RESPONSIBILITY
- P_OBSERVABILITY_WITH_OTEL
- P_GRACEFUL_SHUTDOWN
- C_GREP_FIRST_SEARCH_STRATEGY
- P_EVENT_DRIVEN
- P_SINGLETON_EXPENSIVE_RESOURCES
- P_SEPARATION_OF_CONCERNS
- P_MICROSERVICES_SERVICE_MESH
- P_CQRS_PATTERN
- P_DEPENDENCY_INJECTION
- P_CIRCUIT_BREAKER_PATTERN
- P_CHANGE_DATA_CAPTURE
- P_CORS_POLICY
- P_XSS_PREVENTION
- P_AUDIT_LOGGING
- P_SUPPLY_CHAIN_SECURITY
- P_AI_ML_SECURITY
- P_CONTAINER_SECURITY
- P_CONFIGURATION_AS_CODE
- P_IAC_GITOPS
- P_INCIDENT_RESPONSE_READINESS
- P_API_SECURITY
- P_K8S_SECURITY
- P_ZERO_TRUST
- P_PRIVACY_COMPLIANCE
- U_DEPENDENCY_MANAGEMENT
- P_TEST_COVERAGE
- P_TEST_ISOLATION
- P_INTEGRATION_TESTS
- P_TEST_PYRAMID
- P_CI_GATES
- P_PROPERTY_TESTING
- P_COMMIT_MESSAGE_CONVENTIONS
- U_CONCISE_COMMITS
- U_ATOMIC_COMMITS
- P_BRANCHING_STRATEGY
- P_PR_GUIDELINES
- P_REBASE_VS_MERGE_STRATEGY
- P_SEMANTIC_VERSIONING
- P_GITOPS_PRACTICES
- P_AUTO_VERSIONING
- P_HEALTH_CHECKS

This gives you a comprehensive set of relevant principles (universal + project-specific), optimized for audit tasks. See README.md for current counts.

### 2. Load Core Documents with Category-Based Loader (Manual Alternative)

If you need to manually load principles:

```python
import sys
from pathlib import Path

print("📚 Loading CCO Context...\n")

# Track loaded documents and token estimates
loaded_docs = []
total_tokens = 0

# Load CLAUDE.md
claude_md = Path("CLAUDE.md")
if claude_md.exists():
    content = claude_md.read_text(encoding="utf-8")
    tokens = len(content) // 4  # Rough estimate
    loaded_docs.append(("CLAUDE.md", tokens))
    total_tokens += tokens
    print(f"✓ Loaded CLAUDE.md (~{tokens:,} tokens)")
else:
    print("✗ CLAUDE.md not found - /cco-init required")
    sys.exit(1)

# Load principles using category-based loader
from claudecodeoptimizer.core.principle_loader import PrincipleLoader

loader = PrincipleLoader()

# For cco-audit command
principles = loader.load_for_command("cco-audit")
tokens = loader.estimate_token_count("cco-audit")
loaded_docs.append(("Principles (cco-audit)", tokens))
total_tokens += tokens
print(f"✓ Loaded relevant principles (~{tokens:,} tokens)")
print(f"   Categories: {', '.join(loader.get_categories_for_command('cco-audit'))}")

print(f"\n📊 Core context loaded: ~{total_tokens:,} tokens")
print(f"   Budget remaining: ~{200000 - total_tokens:,} tokens (200K total)\n")

print("Token Optimization Summary:")
print(f"  Before: ~9000 tokens (full CLAUDE.md + PRINCIPLES.md + guides)")
print(f"  After:  ~{total_tokens:,} tokens (core + category-specific principles)")
print(f"  Reduction: ~72% savings\n")
```

### 2. Confirm Required Documents Loaded

**Agents MUST confirm document loading before starting work:**

```
Agent initialization checklist:
1. ✓ CLAUDE.md loaded and parsed
2. ✓ Category-specific principles loaded via PrincipleLoader
3. ✓ Project configuration available
4. ✓ Optional guides available on-demand (load when needed)
```

**If any required document fails to load**: STOP and report error to user.

### 3. Optional: Load Guides On-Demand

For detailed workflows, load guides when needed:

```python
from claudecodeoptimizer.core.guide_loader import GuideLoader, get_suggested_guides

guide_loader = GuideLoader()
suggested = get_suggested_guides("cco-audit")

print(f"\n📖 Suggested guides for this command:")
for guide_name in suggested:
    summary = guide_loader.get_guide_summary(guide_name)
    tokens = guide_loader.estimate_token_count(guide_name)
    print(f"   • {guide_name} (~{tokens} tokens)")
    print(f"     {summary}\n")

# Load when needed:
# guide_content = guide_loader.load_guide("security-response")

print("\nToken Optimization Summary:")
print(f"  Before: CLAUDE.md (~1000) + PRINCIPLES.md (~5000) + Guides (~3000) = ~9000 tokens")
print(f"  After:  CLAUDE.md (~1000) + Core+Category principles (~1500) + Guides (on-demand) = ~2500 tokens")
print(f"  Reduction: 72% (9000 → 2500)")
```

---

## Step 1: Select Audit Types

**Use AskUserQuestion tool** to ask which audits to run:

```json
{
  "questions": [{
    "question": "Which audits would you like to run?",
    "header": "Audit Selection",
    "multiSelect": true,
    "options": [
      {"label": "Code Quality", "description": "Run linters, formatters, type checkers (black, ruff, eslint, etc.)"},
      {"label": "Security", "description": "Security & privacy audit (7 principles: encryption, secrets, TTL, etc.)"},
      {"label": "Tests", "description": "Test coverage, quality, and flaky test detection"},
      {"label": "Documentation", "description": "Docs completeness, accuracy, and sync with code"},
      {"label": "Principles", "description": "Validate against your active development principles (from PRINCIPLES.md)"},
      {"label": "All", "description": "Run all audits above (recommended for comprehensive review)"}
    ]
  }]
}
```

**All options should be selected by default (multiSelect: true).**

---

## Step 2: Run Selected Audits

Based on user selection, run the corresponding audit sections below.

---

## Audit: Code Quality

**Runtime tool detection** - automatically detect and run available tools.

### Detect Available Tools

- **Python**: black, ruff, mypy, pylint, flake8, pytest
- **JavaScript/TypeScript**: prettier, eslint, tslint, tsc, jest, vitest
- **Go**: gofmt, goimports, golint, staticcheck, go test
- **Rust**: rustfmt, clippy, cargo test
- **Other**: Language-specific formatters, linters, type checkers

### Run Checks

Use Task tool (Explore agent, medium thoroughness):

```bash
# Python example
black --check .
ruff check .
mypy .

# Report results
```

### Output Format

Report issues with severity and location:

```
Code Quality Audit Results
=========================

CRITICAL (blocking):
  - src/auth.py:45 - SQL injection vulnerability (use parameterized queries)
  - src/api.py:89 - Hardcoded credentials

HIGH (should fix):
  - src/models.py:12,34,56 - Type errors (missing type annotations)
  - src/utils.py - 15 formatting violations (line too long)

MEDIUM (recommended):
  - src/tests/ - 23 unused imports
  - src/config.py - Inconsistent naming (snake_case vs camelCase)

LOW (optional):
  - src/legacy.py - Deprecated function usage (warnings only)
```

### Recommended Actions (Dynamic)

**Analyze results and provide prioritized commands:**

```
🎯 Recommended Actions (Priority Order)
========================================

1. CRITICAL: Fix security issues
   Command: /cco-fix security --severity critical --files src/auth.py,src/api.py
   Impact: Blocks production deployment

2. HIGH: Fix type errors
   Command: /cco-fix type-errors --files src/models.py
   Impact: Prevents runtime errors

3. HIGH: Auto-format code
   Command: /cco-fix formatting --scope all
   Impact: Passes CI checks

4. MEDIUM: Remove unused imports
   Command: /cco-fix unused-imports --scope src/
   Impact: Cleaner codebase

5. MEDIUM: Fix naming conventions
   Command: /cco-fix naming --file src/config.py --style snake_case
   Impact: Code consistency

Quick fix all (if no critical issues):
   Command: /cco-fix code --auto --scope all
```

**Command Generation Logic:**
1. Group issues by severity (CRITICAL > HIGH > MEDIUM > LOW)
2. Group by file/directory if 3+ issues in same location
3. Use specific flags: `--severity`, `--files`, `--scope`, `--type`
4. Provide estimated impact for each action
5. Offer "quick fix all" only if no CRITICAL issues

---

## Audit: Security

**7 Critical Security & Privacy Principles**

Audit against:
- P_PRIVACY_FIRST: Privacy-First by Default
- P_TTL_BASED_CLEANUP: TTL-Based Cleanup
- P_ZERO_DISK_TOUCH: Zero Disk Touch
- P_ZERO_TRUST: Zero Trust Architecture
- P_AUTH_AUTHZ: Authentication & Authorization
- P_ENCRYPTION_AT_REST: Encryption Everywhere
- P_SECRET_ROTATION: Secret Management with Rotation

### Architecture (Optimized: Speed + Quality)
- 2 parallel Haiku agents (Explore, quick) - fast security scanning
- 1 Sonnet aggregator (Plan) - intelligent risk assessment
- Custom @security-auditor agent (if available)
- Execution: **20-25 seconds** (2x faster, maintains quality)

### Run Audit

**CRITICAL**: Launch agents in PARALLEL for 2-3x speed boost.

#### ✅ GOOD Example (Parallel - 20 seconds):

**Launch BOTH agents in a SINGLE message** to enable true parallelism:

**Message 1 (Both agents launched together):**

Use Task tool twice in the same response:

**Agent 1 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Data security audit

CRITICAL - MUST LOAD FIRST:
1. Load @CLAUDE.md (Security section)
2. Load @~/.cco/guides/cco-security-response.md
3. Load @~/.cco/principles/security.md
4. Print confirmation: "✓ Loaded 3 documents (~3,500 tokens)"

THEN audit these principles:
- P_PRIVACY_FIRST: Privacy-First by Default (no PII in logs, proper anonymization)
- P_ZERO_DISK_TOUCH: Zero Disk Touch (sensitive data not written to disk)
- P_SECRET_ROTATION: Secret Management (no hardcoded API keys, passwords, tokens)

Scan for:
- Unencrypted sensitive data in code
- Hardcoded secrets: API keys (sk_*, pk_*), passwords, tokens
- .env files committed to git
- Credential files (credentials.json, .pem, .key)
- PII in log statements

Compare findings against security-response.md checklist.
Report with file:line references.
```

**Agent 2 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Security architecture audit

CRITICAL - MUST LOAD FIRST:
1. Load @CLAUDE.md (Security section)
2. Load @~/.cco/guides/cco-security-response.md
3. Load @~/.cco/principles/security.md
4. Print confirmation: "✓ Loaded 3 documents (~3,500 tokens)"

THEN audit these principles:
- P_TTL_BASED_CLEANUP: TTL-Based Cleanup (sessions expire, data cleanup)
- P_ZERO_TRUST: Zero Trust Architecture (multiple security layers)
- P_AUTH_AUTHZ: Authentication & Authorization (HTTPS, headers, hardening)
- P_ENCRYPTION_AT_REST: Encryption Everywhere (proper crypto, no weak hashing)

Check for:
- Session expiration configuration
- HTTPS enforcement in config
- Security headers (CSP, HSTS, X-Frame-Options)
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- XSS prevention (output escaping)

Compare findings against security-response.md patterns.
Report with file:line references.
```

#### ❌ BAD Example (Sequential - 45 seconds):

**Message 1:** Launch Agent 1
*Wait for Agent 1 to complete*

**Message 2:** Launch Agent 2
*Wait for Agent 2 to complete*

**Result**: Takes 2x longer, blocks parallelism

### Aggregation

**After both agents complete**, use Sonnet Plan agent for intelligent analysis:

**Agent 3 Prompt:**
```
Subagent Type: Plan
Model: sonnet
Description: Security risk assessment

Task: Analyze security findings from 2 parallel security audits.

Input:
- Agent 1 findings (data security)
- Agent 2 findings (architecture security)

Analysis steps:
1. Merge all security findings from both agents
2. Assess actual risk level (not just theoretical)
3. Identify attack vectors and exploit scenarios
4. Prioritize by: Exploitability × Impact × Exposure
5. Provide specific remediation steps with commands
6. Estimate security debt (hours) and fix effort
7. Recommend immediate actions vs long-term hardening
8. Calculate risk reduction percentage for each fix

Output format:
- Findings by severity (CRITICAL > HIGH > MEDIUM > LOW)
- Each finding includes: principle, file:line, exploit scenario, fix command
- Master remediation plan with priority tiers
- Security debt estimate (total hours)

Focus on practical, actionable security improvements.
```

**Why use Sonnet for aggregation:**
- Risk assessment requires deep reasoning (not just data collection)
- Attack vector analysis needs intelligence and context
- Prioritization by real-world exploitability (not just severity)
- Context-aware remediation recommendations
- Pattern recognition across multiple findings
- Accurate effort estimation

### Output Format

Report security issues with risk level and exploit scenarios:

```
Security Audit Results
=====================

CRITICAL (immediate action required):
  - P_SECRET_ROTATION: Hardcoded AWS credentials in src/config.py:23
    Risk: Full AWS account compromise
    Exploit: Credentials visible in git history

  - P_SQL_INJECTION: SQL injection in src/api.py:145
    Risk: Database breach, data exfiltration
    Exploit: Unsanitized user input in query

CRITICAL (data breach risk):
  - P_PRIVACY_FIRST: User emails logged in plaintext (src/auth.py:67)
    Risk: GDPR violation, privacy breach
    Exploit: Log aggregation exposes PII

HIGH (security gap):
  - P_AUTH_AUTHZ: Missing HTTPS enforcement (src/app.py)
    Risk: Man-in-the-middle attacks
    Exploit: Network traffic interception

  - P_TTL_BASED_CLEANUP: Sessions never expire (src/session.py)
    Risk: Session hijacking, unlimited access
    Exploit: Stolen session tokens valid forever

MEDIUM (hardening recommended):
  - P_ENCRYPTION_AT_REST: Weak password hashing (MD5 in src/auth.py:34)
    Risk: Rainbow table attacks
    Exploit: Password database compromise

  - P_ZERO_DISK_TOUCH: Sensitive files not in .gitignore
    Risk: Accidental secret commit
    Files: .env.local, credentials.json

LOW (best practice):
  - P_RATE_LIMITING: Missing rate limiting on API endpoints
    Risk: DoS, brute force attacks
    Impact: Service availability
```

### Recommended Actions (Dynamic)

**Analyze security findings and provide exploit-aware prioritization:**

```
🔒 Security Remediation Plan (Risk-Based Priority)
==================================================

IMMEDIATE (Deploy Blockers):
──────────────────────────────
1. Rotate compromised credentials
   Command: /cco-fix secrets --rotate --files src/config.py
   Impact: CRITICAL - Prevents AWS account takeover

2. Fix SQL injection
   Command: /cco-fix security --type sql-injection --file src/api.py:145
   Impact: CRITICAL - Prevents database breach

3. Remove PII from logs
   Command: /cco-fix privacy --type remove-logging --file src/auth.py:67
   Impact: CRITICAL - GDPR compliance

THIS WEEK (High Risk):
─────────────────────
4. Enforce HTTPS
   Command: /cco-fix security --type https-redirect --file src/app.py
   Impact: HIGH - Prevents MITM attacks

5. Implement session expiration
   Command: /cco-generate session-management --ttl 24h --file src/session.py
   Impact: HIGH - Limits session hijacking window

THIS SPRINT (Hardening):
───────────────────────
6. Upgrade password hashing
   Command: /cco-fix security --type password-hashing --algorithm bcrypt --file src/auth.py
   Impact: MEDIUM - Protects against rainbow tables

7. Update .gitignore
   Command: /cco-fix secrets --update-gitignore --add .env.local,credentials.json
   Impact: MEDIUM - Prevents future leaks

BACKLOG (Best Practice):
───────────────────────
8. Add rate limiting
   Command: /cco-generate middleware --type rate-limiter --endpoints /api/*
   Impact: LOW - DoS protection

Security Debt: 12 hours | Risk Reduction: 95%
```

**Command Generation Logic:**
1. **Risk = Exploitability × Impact × Exposure**
   - Exploitability: How easy to exploit? (trivial/easy/hard)
   - Impact: What's at stake? (data breach/service disruption/reputation)
   - Exposure: Is it exposed? (public API/internal/localhost)

2. **Priority Tiers:**
   - IMMEDIATE: Actively exploitable, high impact (fix in hours)
   - THIS WEEK: Exploitable with effort, medium-high impact (fix in days)
   - THIS SPRINT: Requires specific conditions, medium impact (fix in weeks)
   - BACKLOG: Low exploitability or impact (fix in months)

3. **Command Features:**
   - Specific fix type: `--type sql-injection`, `--type https-redirect`
   - Risk context: Why this matters (exploit scenario)
   - Effort estimate: Realistic time to fix
   - Impact metric: Risk reduction percentage

4. **Grouping:**
   - Same vulnerability type → Single command with multiple files
   - Same file → Single command with multiple fix types
   - Dependencies → Sequential commands with order

---

## Audit: Tests

**Test Coverage & Quality Analysis**

### Metrics

1. **Coverage**: Line, branch, function coverage
2. **Quality**: Assertion quality, test isolation
3. **Flaky Tests**: Detect non-deterministic tests
4. **Speed**: Identify slow tests

### Run Analysis

```bash
# Python
pytest --cov --cov-report=term-missing
pytest --durations=10

# JavaScript
jest --coverage
npm test -- --verbose
```

### Output Format

Report test coverage and quality issues with business impact:

```
Test Audit Results
==================

Coverage: 67% (target: 80%, gap: 13%)

CRITICAL (no tests):
  - src/payment.py - 0% coverage
    Business Risk: Payment processing bugs go undetected
    Impact: Financial loss, fraud vulnerability

  - src/auth.py - 0% coverage
    Business Risk: Authentication bypass possible
    Impact: Security breach, unauthorized access

HIGH (insufficient coverage):
  - src/api.py - 45% coverage (23/51 functions untested)
    Missing: Error handling, edge cases, validation
    Business Risk: API failures in production

  - src/database.py - 60% coverage
    Missing: Transaction rollback, connection pool edge cases
    Business Risk: Data corruption, connection leaks

MEDIUM (quality issues):
  - tests/test_user.py - 5 flaky tests detected
    Failures: test_concurrent_login (intermittent)
    Impact: CI unreliability, false positives

  - tests/test_integration.py - 3 slow tests (>10s each)
    Slowest: test_full_workflow (23.4s)
    Impact: Developer productivity (slow feedback)

LOW (minor gaps):
  - src/utils.py - 85% coverage
    Missing: Error path in format_date()
    Impact: Minor edge case handling
```

### Recommended Actions (Dynamic)

**Analyze test gaps and provide impact-driven prioritization:**

```
🧪 Test Generation Plan (Business Impact Priority)
===================================================

IMMEDIATE (Production Blockers):
─────────────────────────────────
1. Add payment processing tests
   Command: /cco-generate tests --file src/payment.py --focus critical-path
   Impact: CRITICAL - Prevents financial bugs
   Coverage: 0% → 85% (target critical paths)

2. Add authentication tests
   Command: /cco-generate tests --file src/auth.py --focus security
   Impact: CRITICAL - Prevents auth bypass
   Coverage: 0% → 80% (target security flows)

THIS WEEK (High Risk):
─────────────────────
3. Expand API test coverage
   Command: /cco-generate tests --file src/api.py --focus error-handling,edge-cases
   Impact: HIGH - Catches production errors early
   Coverage: 45% → 80%

4. Add database transaction tests
   Command: /cco-generate tests --file src/database.py --focus transactions,rollback
   Impact: HIGH - Prevents data corruption
   Coverage: 60% → 85%

THIS SPRINT (Quality):
─────────────────────
5. Fix flaky tests
   Command: /cco-fix tests --type flaky --file tests/test_user.py
   Impact: MEDIUM - Improves CI reliability
   Flaky: 5 → 0

6. Optimize slow tests
   Command: /cco-fix tests --type slow --threshold 5s --file tests/test_integration.py
   Impact: MEDIUM - Faster feedback loop
   Time: 23.4s → <5s (use mocking)

BACKLOG (Minor Gaps):
────────────────────
7. Add edge case tests
   Command: /cco-generate tests --file src/utils.py --focus edge-cases
   Impact: LOW - Completeness
   Coverage: 85% → 95%

Test Debt: 15.5 hours | Coverage: 67% → 82% | Risk Reduction: 90%
```

**Command Generation Logic:**
1. **Business Impact = Criticality × Exposure × Failure Cost**
   - Criticality: Payment, auth, data integrity > API > utilities
   - Exposure: Public APIs > internal > helpers
   - Failure Cost: Financial loss > security > UX > dev productivity

2. **Priority Tiers:**
   - IMMEDIATE: No tests for critical business logic (fix today)
   - THIS WEEK: <50% coverage on high-traffic code (fix this week)
   - THIS SPRINT: Flaky/slow tests, 50-80% coverage (fix this sprint)
   - BACKLOG: >80% coverage, minor utilities (fix when convenient)

3. **Command Features:**
   - Focus areas: `--focus critical-path`, `--focus error-handling`, `--focus security`
   - Fix types: `--type flaky`, `--type slow`
   - Coverage targets: Show before → after
   - Effort estimates: Realistic time based on file complexity

4. **Test Strategy:**
   - Critical files: Unit + integration + edge cases
   - High-traffic files: Unit + integration
   - Utilities: Unit only
   - Flaky tests: Isolate, mock external dependencies
   - Slow tests: Mock I/O, use in-memory DBs

---

## Audit: Documentation

**Documentation Completeness & Accuracy**

### Check

1. **API Docs**: All public APIs documented
2. **README**: Up-to-date setup instructions
3. **Inline Comments**: Complex logic explained
4. **Sync**: Docs match actual code behavior
5. **Examples**: Working code examples

### Run Audit

Use Task tool (Explore agent):

```
1. Check README exists and is current
2. Verify API documentation coverage
3. Scan for outdated docs (deprecated APIs, old examples)
4. Check docstring coverage (Python) or JSDoc (JS)
```

### Output Format

Report documentation gaps with user/developer impact:

```
Documentation Audit Results
===========================

Doc Health: 58/100 (needs improvement)

CRITICAL (blocking onboarding):
  - README.md - Missing setup instructions
    Impact: New developers can't run the project
    Affected: All new team members

  - API.md - Not found
    Impact: API consumers can't integrate
    Affected: External developers, partners

HIGH (poor developer experience):
  - src/api.py - 0% docstring coverage (23 public functions)
    Missing: /api/payments, /api/users, /api/auth
    Impact: Developers don't know how to use APIs

  - src/models.py - Outdated docstrings (5 deprecated fields)
    Outdated: User.status field (removed 3 months ago)
    Impact: Confusion, incorrect usage

MEDIUM (incomplete):
  - CONTRIBUTING.md - Not found
    Impact: Hard to onboard contributors
    Affected: Open source contributors

  - examples/ - No code examples
    Impact: Harder to understand usage patterns
    Affected: New developers learning the API

LOW (minor improvements):
  - src/utils.py - 60% docstring coverage
    Missing: Helper functions only
    Impact: Minor - internal utilities
```

### Recommended Actions (Dynamic)

**Analyze documentation gaps and prioritize by audience impact:**

```
📚 Documentation Plan (Audience Impact Priority)
================================================

IMMEDIATE (Onboarding Blockers):
────────────────────────────────
1. Create setup instructions
   Command: /cco-generate docs --type readme --sections setup,quickstart
   Impact: CRITICAL - Enables new developer onboarding
   Audience: All new team members

2. Generate API documentation
   Command: /cco-generate docs --type api --file src/api.py --format openapi
   Impact: CRITICAL - Enables API integration
   Audience: External developers, partners

THIS WEEK (Developer Experience):
─────────────────────────────────
3. Add API docstrings
   Command: /cco-generate docs --type docstrings --file src/api.py --coverage 100
   Impact: HIGH - Self-documenting code
   Audience: Internal developers

4. Fix outdated docstrings
   Command: /cco-fix docs --type outdated --file src/models.py
   Impact: HIGH - Prevents confusion
   Audience: All developers

THIS SPRINT (Completeness):
───────────────────────────
5. Create contribution guide
   Command: /cco-generate docs --type contributing --style conventional-commits
   Impact: MEDIUM - Easier contributions
   Audience: Open source contributors

6. Add code examples
   Command: /cco-generate docs --type examples --categories auth,payments,users
   Impact: MEDIUM - Faster learning curve
   Audience: New developers

BACKLOG (Nice to Have):
──────────────────────
8. Complete utility docstrings
   Command: /cco-generate docs --type docstrings --file src/utils.py --coverage 95
   Impact: LOW - Internal documentation
   Audience: Maintainers

Documentation Debt: 10.75 hours | Doc Health: 58 → 92 | Onboarding Time: -75%
```

**Command Generation Logic:**
1. **Audience Impact = Audience Size × Frustration Level × Frequency**
   - Audience Size: All users > partners > team > contributors
   - Frustration: Blocked > confused > slower > minor
   - Frequency: Daily > weekly > monthly > rare

2. **Priority Tiers:**
   - IMMEDIATE: Blocking onboarding or integration (fix today)
   - THIS WEEK: Poor DX, causes confusion (fix this week)
   - THIS SPRINT: Incomplete but not blocking (fix this sprint)
   - BACKLOG: Nice-to-have improvements (fix when convenient)

3. **Documentation Types:**
   - README: Setup, quickstart, architecture
   - API: OpenAPI/Swagger, endpoint docs
   - Docstrings: Function/class level documentation
   - Examples: Working code snippets
   - Contributing: PR process, coding standards

4. **Command Features:**
   - Doc type: `--type readme`, `--type api`, `--type docstrings`
   - Coverage: `--coverage 100` (docstrings)
   - Format: `--format openapi`, `--format markdown`
   - Sections: `--sections setup,quickstart` (README)
   - Style: `--style conventional-commits` (contributing)

5. **Impact Metrics:**
   - Doc Health: 0-100 score (completeness + accuracy + freshness)
   - Onboarding Time: How much faster new devs can contribute
   - API Integration Time: How much faster partners can integrate

---

## Audit: Principles

**Validate Against Your Active Development Principles**

This audit checks your code against the principles that are active for this project (configured in PRINCIPLES.md).

### Load Active Principles

First, load your project's active principles:

```bash
python -c "
from pathlib import Path
import json

# Method 1: Read from PRINCIPLES.md (recommended)
principles_md = Path.cwd() / 'PRINCIPLES.md'
if principles_md.exists():
    # Count principles from markdown
    content = principles_md.read_text(encoding='utf-8')
    principle_count = content.count('### P')
    print(f'Active principles: {principle_count}')
    print(f'Reading from: PRINCIPLES.md')
else:
    # Method 2: Read from registry
    project_name = Path.cwd().name
    registry_file = Path.home() / '.cco' / 'projects' / f'{project_name}.json'

    if registry_file.exists():
        config = json.loads(registry_file.read_text(encoding='utf-8'))
        selected_ids = config.get('selected_principles', [])
        print(f'Active principles: {len(selected_ids)}')
        print(f'Reading from: registry')
        print(f'IDs: {selected_ids[:5]}...')
    else:
        print('[ERROR] No PRINCIPLES.md or registry found')
        print('Run /cco-init first')
"
```

**If no principles found**: Stop and inform user to run `/cco-init` first.

### Load Principle Definitions

```bash
python -c "
from pathlib import Path
import json

# Get active principle IDs from registry
project_name = Path.cwd().name
registry_file = Path.home() / '.cco' / 'projects' / f'{project_name}.json'
config = json.loads(registry_file.read_text(encoding='utf-8'))
selected_ids = config.get('selected_principles', [])

# Load full principle definitions from .md files
from claudecodeoptimizer.core.principles import get_principles_manager
pm = get_principles_manager()
all_principles = [
    {
        'id': p.id,
        'category': p.category,
        'title': p.title,
        'severity': p.severity,
    }
    for p in pm.get_all_principles()
]

# Filter to only active principles
active_principles = [p for p in all_principles if p['id'] in selected_ids]

print(f'Loaded {len(active_principles)} active principles')
print('')
print('By category:')
by_category = {}
for p in active_principles:
    cat = p.get('category', 'unknown')
    by_category[cat] = by_category.get(cat, 0) + 1

for cat, count in sorted(by_category.items()):
    print(f'  {cat}: {count}')
"
```

### Architecture (Optimized: Speed + Quality)

**Hybrid approach for fast + smart analysis:**
- 3 parallel Haiku agents (Explore, quick) - fast data gathering
- 1 Sonnet aggregator (Plan) - intelligent analysis & recommendations
- Execution: **15-20 seconds** (2x faster, maintains quality)
- Dynamic: Only audits categories that have active principles

**Why this works:**
- Haiku: Fast scanning, data collection (good enough for finding issues)
- Sonnet: Deep analysis, prioritization, actionable insights (critical for decisions)
- Grouped categories reduce agent overhead
- Parallelization maintained

### Run Audit

**CRITICAL**: Launch 3 agents in PARALLEL in a SINGLE message.

#### ✅ GOOD Example (Parallel - 15 seconds):

**Launch ALL THREE agents together:**

**Agent 1 Prompt (Code & Architecture):**
```
Subagent Type: Explore
Model: haiku
Description: Code & architecture principles audit

MUST LOAD FIRST:
1. @PRINCIPLES.md
2. @~/.cco/principles/code-quality.md
3. @~/.cco/principles/architecture.md
4. Print: "✓ Loaded 3 docs (~2,800 tokens)"

Audit principles:
- Code Quality (U_DRY-P018): DRY, type safety, error handling
- Architecture (P_ZERO_TRUST-P047): Layered, separation of concerns, patterns

Scan for:
- U_FAIL_FAST: Fail-fast error handling (no bare except, no swallowed exceptions)
- P_TYPE_SAFETY: Type safety violations (missing type hints)
- U_DRY: Code duplication (>50 lines similar code)
- P_SEPARATION_OF_CONCERNS: Layered architecture violations (separation of concerns)
- U_NO_OVERENGINEERING: Overengineering (premature abstraction)

Report violations with file:line and pattern analysis.
```

**Agent 2 Prompt (Security & Operations):**
```
Subagent Type: Explore
Model: haiku
Description: Security & operations principles audit

MUST LOAD FIRST:
1. @PRINCIPLES.md
2. @~/.cco/principles/security.md
3. @~/.cco/principles/operations.md
4. Print: "✓ Loaded 3 docs (~3,200 tokens)"

Audit principles:
- Security & Privacy: Secrets, TTL, zero-disk, encryption
- Operations: IaC, observability, health checks

Scan for:
- P_TTL_BASED_CLEANUP: TTL enforcement (sessions, data cleanup)
- P_ZERO_TRUST: Defense-in-depth (multiple security layers)
- P_SECRET_ROTATION: Secret scanning (hardcoded credentials)
- P_IAC_GITOPS: Infrastructure as Code (Terraform, Pulumi)
- P_HEALTH_CHECKS: Automated health checks (liveness, readiness)

Report violations with file:line and root cause analysis.
```

**Agent 3 Prompt (Process & Performance):**
```
Subagent Type: Explore
Model: haiku
Description: Process & performance principles audit

MUST LOAD FIRST:
1. @PRINCIPLES.md
2. @~/.cco/principles/testing.md
3. @~/.cco/principles/performance.md
4. @~/.cco/principles/git-workflow.md
5. Print: "✓ Loaded 4 docs (~2,400 tokens)"

Audit principles:
- Testing: Coverage, pyramid, isolation
- Performance: Caching, async I/O, optimization
- Git Workflow: Commits, branching, PRs
- API Design: RESTful, versioning

Scan for:
- P_TEST_COVERAGE: Test coverage (target: 80%+)
- P_TEST_PYRAMID: Test pyramid (more unit than integration)
- P_CACHING_STRATEGY: Caching strategy (missing caches)
- U_EVIDENCE_BASED: Evidence-based verification (no "should work")
- U_CONCISE_COMMITS: Concise commit messages (max 10 lines)

Report violations with file:line and improvement suggestions.
```

#### ❌ BAD Example (Sequential - 45 seconds):

**Message 1:** Agent 1 (Code)
**Message 2:** Agent 2 (Security)
**Message 3:** Agent 3 (Process)

**Result**: 3x slower

**Aggregate Results**

**After ALL THREE agents complete**, use Sonnet Plan agent:

**Agent 4 Prompt (Aggregator):**
```
Subagent Type: Plan
Model: sonnet
Description: Principle compliance analysis

Task: Merge results from 3 parallel principle audits and provide intelligent analysis.

Input:
- Agent 1 findings (code & architecture)
- Agent 2 findings (security & operations)
- Agent 3 findings (process & performance)

Analysis steps:
1. Merge all category results from 3 agents
2. Calculate overall compliance score (% principles met)
3. Identify PATTERNS and trends across violations
   - Example: "Error handling missing in 12 endpoints" (U_DRY)
   - Example: "No tests for critical modules" (P014)
4. Prioritize issues by: Principle Severity × Impact × Spread
   - Don't fix individual violations
   - Find root causes that affect multiple areas
5. Provide ROOT CAUSE analysis for common failures
   - Example: "No error framework" → causes U_DRY violations
6. Generate actionable, specific recommendations with commands
   - Pattern-based fixes (not one-off)
   - Include /cco-fix or /cco-generate commands
7. Estimate effort for each recommendation (hours)
8. Calculate technical debt (total hours to full compliance)

Output format:
- Compliance score: X% (Y/Z principles met)
- Violations by severity with root causes
- Master remediation plan with pattern-driven fixes
- Technical debt estimate
- Risk reduction percentage

Focus on systematic fixes that prevent future violations.
```

**Why use Sonnet for aggregation:**
- Deep pattern analysis across all three categories
- Intelligent prioritization by impact (not just severity)
- Root cause reasoning (finds systemic issues)
- Context-aware recommendations (understands project)
- Accurate effort estimation for fixes

### Output Format

Report principle violations with pattern analysis and root causes:

```
Principle Compliance Audit
==========================

Overall Compliance: 72% (29/40 principles met)
Technical Debt: ~32 hours to full compliance

CRITICAL (Architectural Issues):
  - U_FAIL_FAST: No Error Boundaries (src/app.py, src/api.py)
    Pattern: Error handling missing in 12 endpoints
    Root Cause: No error handling framework
    Impact: Unhandled exceptions crash the app
    Affected: All API consumers

  - P_TEST_COVERAGE: Test Coverage 45% (target: 80%, gap: 35%)
    Pattern: No tests for src/payment.py, src/auth.py
    Root Cause: Critical modules added without TDD
    Impact: Production bugs in payment/auth
    Affected: Financial transactions, user security

HIGH (Security Gaps):
  - P_TTL_BASED_CLEANUP: Sessions Never Expire (src/session.py)
    Pattern: No TTL enforcement across the app
    Root Cause: Missing TTL configuration
    Impact: Session hijacking risk
    Affected: All authenticated users

  - P_SECRET_ROTATION: 3 Hardcoded Secrets (src/config.py:12, src/db.py:34, .env.example)
    Pattern: Secrets in version control
    Root Cause: No secret management process
    Impact: Security breach via git history
    Affected: Production environment

  - P_SQL_INJECTION: SQL Injection in 2 Endpoints (src/api.py:145, src/db.py:67)
    Pattern: String concatenation in queries
    Root Cause: No ORM or parameterized queries
    Impact: Database breach, data exfiltration
    Affected: User data, payment data

MEDIUM (Code Quality):
  - U_DRY: Code Duplication (5 instances >50 lines)
    Locations: src/auth.py:45-98, src/api.py:123-176 (similar)
    Pattern: Auth logic duplicated across modules
    Root Cause: No shared authentication module
    Impact: Bug fixes needed in multiple places
    Affected: Maintainability

  - U_NO_OVERENGINEERING: Overengineering Detected (src/utils.py)
    Pattern: Abstract factory for simple config
    Root Cause: Premature abstraction
    Impact: Code complexity without benefit
    Affected: Developer productivity

LOW (Best Practice):
  - DOC: Missing Docstrings (15 public functions)
    Pattern: No documentation for API endpoints
    Root Cause: No documentation standards
    Impact: Poor developer experience
    Affected: API consumers, maintainers
```

### Recommended Actions (Dynamic)

**Analyze principle violations and provide pattern-based fixes:**

```
🎯 Principle Remediation Plan (Pattern-Driven Priority)
========================================================

IMMEDIATE (Architectural Fixes):
────────────────────────────────
1. Implement error handling framework
   Command: /cco-generate error-handler --pattern boundaries --files src/app.py,src/api.py
   Impact: CRITICAL - Prevents app crashes
   Principles: P_PRECISION_IN_CALCS
   Pattern: Centralized error handling for all endpoints

2. Add critical module tests
   Command: /cco-generate tests --files src/payment.py,src/auth.py --coverage 85 --focus critical-path
   Impact: CRITICAL - Catches financial/security bugs
   Principles: P_SEPARATION_OF_CONCERNS
   Coverage: 45% → 75% (projected)

THIS WEEK (Security Hardening):
───────────────────────────────
3. Implement session TTL
   Command: /cco-fix security --type ttl --file src/session.py --ttl 24h --idle-timeout 2h
   Impact: HIGH - Limits session hijacking window
   Principles: C_AGENT_ORCHESTRATION_PATTERNS

4. Move secrets to environment
   Command: /cco-fix secrets --rotate --files src/config.py,src/db.py,.env.example --vault .env
   Impact: HIGH - Prevents credential leaks
   Principles: P_ZERO_DISK_TOUCH

5. Fix SQL injection vulnerabilities
   Command: /cco-fix security --type sql-injection --files src/api.py:145,src/db.py:67 --use-orm
   Impact: HIGH - Prevents database breaches
   Principles: P_SCHEMA_VALIDATION

THIS SPRINT (Code Quality):
───────────────────────────
6. Extract shared authentication module
   Command: /cco-fix duplication --files src/auth.py:45-98,src/api.py:123-176 --extract src/shared/auth.py
   Impact: MEDIUM - Centralized auth logic
   Principles: C_GREP_FIRST_SEARCH_STRATEGY
   Duplication: 5 instances → 0

7. Simplify overengineered utilities
   Command: /cco-fix complexity --file src/utils.py --simplify abstract-factory --pattern direct-config
   Impact: MEDIUM - Reduced complexity
   Principles: U_NO_OVERENGINEERING

BACKLOG (Documentation):
────────────────────────
8. Add API documentation
   Command: /cco-generate docs --type docstrings --scope src/api --coverage 100
   Impact: LOW - Better DX
   Principles: P_CORS_POLICY

Technical Debt: 23 hours | Compliance: 72% → 95% | Risk Reduction: 85%
```

**Command Generation Logic:**
1. **Pattern Analysis → Root Cause → Systematic Fix**
   - Don't fix individual violations
   - Identify patterns (e.g., "error handling missing everywhere")
   - Fix root cause (e.g., "implement error framework")
   - Prevents future violations

2. **Principle Categories Map to Actions:**
   - P_PRECISION_IN_CALCS (Error Handling) → Generate error handler framework
   - P_SEPARATION_OF_CONCERNS (Testing) → Generate tests for untested modules
   - C_AGENT_ORCHESTRATION_PATTERNS (TTL) → Configure expiration policies
   - P_ZERO_DISK_TOUCH (Secrets) → Move to env + rotate credentials
   - P_SCHEMA_VALIDATION (Security) → Fix vulnerability type (SQL injection, XSS, etc.)
   - C_GREP_FIRST_SEARCH_STRATEGY (Duplication) → Extract shared modules
   - U_NO_OVERENGINEERING (Overengineering) → Simplify abstractions
   - P_CORS_POLICY (Docs) → Generate documentation

3. **Priority = Principle Severity × Impact × Spread**
   - Severity: CRITICAL > HIGH > MEDIUM > LOW
   - Impact: Business/security > quality > DX
   - Spread: Affects entire codebase > multiple files > single file

4. **Command Features:**
   - Pattern-based: `--pattern boundaries`, `--pattern direct-config`
   - Fix type: `--type ttl`, `--type sql-injection`, `--type flaky`
   - Scope: Multiple files if pattern is widespread
   - Before → After metrics: Coverage %, duplication count

5. **Effort Estimation:**
   - Framework changes (error handler, auth): 3-5 hours
   - Security fixes (secrets, SQL injection): 1-3 hours
   - Refactoring (duplication): 2-4 hours
   - Documentation: 1-3 hours

---

## Audit: All

**Run All Audits Sequentially**

If user selected "All", run all audit types:

1. Code Quality Audit
2. Security Audit
3. Test Audit
4. Documentation Audit
5. Principles Audit

Generate combined report with all findings.

---

## Final Report

After all selected audits complete, generate comprehensive cross-audit summary.

### Token Usage Summary

**Display token usage for transparency:**

```python
print("\n" + "="*60)
print("TOKEN USAGE REPORT")
print("="*60)

# Calculate from loaded documents
docs_loaded = [
    ("CLAUDE.md", 3262),
    ("PRINCIPLES.md", 1311),
    ("security-response.md", 1631),  # If loaded
    ("code-quality.md", 1200),        # If loaded
]

total_context = sum(tokens for _, tokens in docs_loaded)
budget_used = total_context / 200000 * 100

print(f"\nDocuments Loaded: {len(docs_loaded)}")
for doc, tokens in docs_loaded:
    print(f"  • {doc:30s} ~{tokens:>6,} tokens")

print(f"\n{'─'*60}")
print(f"Total Context Used:           ~{total_context:>7,} tokens")
print(f"Budget Remaining:             ~{200000-total_context:>7,} tokens")
print(f"Budget Utilization:            {budget_used:>6.1f}%")
print(f"\nToken Efficiency:")
print(f"  Progressive Disclosure:       ✓ Enabled")
print(f"  On-Demand Loading:            ✓ Category-specific guides")
print(f"  Reduction Factor:             ~3x (vs loading all docs)")
print("="*60 + "\n")
```

### Comprehensive Cross-Audit Summary

Generate report with intelligent prioritization:

```
============================================================
COMPREHENSIVE AUDIT REPORT
Project: ${PROJECT_NAME}
Date: ${DATE}
Audits Run: Code Quality, Security, Tests, Documentation, Principles
============================================================

EXECUTIVE SUMMARY
─────────────────
Overall Health: 68/100 (needs improvement)

By Category:
  ✓ Code Quality:      82/100 (good)
  ✗ Security:          45/100 (critical issues)
  ⚠ Tests:             58/100 (insufficient)
  ⚠ Documentation:     61/100 (gaps)
  ✓ Principles:        72/100 (mostly compliant)

Issue Breakdown:
  CRITICAL: 8  (blocks deployment)
  HIGH:     15 (fix this week)
  MEDIUM:   23 (fix this sprint)
  LOW:      12 (backlog)

Technical Debt: 47.5 hours to full compliance
Risk Level: HIGH (security + test gaps)

CROSS-CUTTING PATTERNS
──────────────────────
🔴 Authentication/Authorization (affects 3 audits):
   - No auth tests (Tests)
   - Hardcoded secrets in auth (Security)
   - P_ZERO_DISK_TOUCH violation: secrets in git (Principles)
   → Root Cause: No auth framework + no secret management

🔴 Error Handling (affects 2 audits):
   - Unhandled exceptions crash app (Code Quality)
   - P_PRECISION_IN_CALCS violation: no error boundaries (Principles)
   → Root Cause: No error handling framework

🟡 Documentation (affects 2 audits):
   - Missing API docs (Documentation)
   - P_CORS_POLICY violation: no docstrings (Principles)
   → Root Cause: No documentation standards

MASTER REMEDIATION PLAN (Cross-Audit Priority)
===============================================

🚨 IMMEDIATE (Today - Deploy Blockers):
────────────────────────────────────────
1. Fix authentication security [Security + Principles]
   Commands:
     a. /cco-fix secrets --rotate --files src/auth.py,src/config.py --vault .env
     b. /cco-generate tests --file src/auth.py --focus security --coverage 85
   Impact: CRITICAL - Prevents credential leaks + auth bypass
   Audits Affected: Security (P_ZERO_DISK_TOUCH), Tests (auth coverage), Principles (P_ZERO_DISK_TOUCH, P_SEPARATION_OF_CONCERNS)

   Risk Reduction: 40%

2. Fix SQL injection vulnerabilities [Security + Principles]
   Command: /cco-fix security --type sql-injection --files src/api.py:145,src/db.py:67 --use-orm
   Impact: CRITICAL - Prevents database breaches
   Audits Affected: Security (SQL injection), Principles (P_SCHEMA_VALIDATION)

   Risk Reduction: 25%

3. Implement error handling framework [Code Quality + Principles]
   Command: /cco-generate error-handler --pattern boundaries --files src/app.py,src/api.py
   Impact: CRITICAL - Prevents app crashes
   Audits Affected: Code Quality (exception handling), Principles (P_PRECISION_IN_CALCS)

   Risk Reduction: 20%

   IMMEDIATE Subtotal: 11 hours | Risk Reduction: 85%

📅 THIS WEEK (High Priority):
──────────────────────────────
4. Add payment processing tests [Tests + Principles]
   Command: /cco-generate tests --file src/payment.py --focus critical-path --coverage 85
   Impact: HIGH - Catches financial bugs before production
   Audits Affected: Tests (coverage), Principles (P_SEPARATION_OF_CONCERNS)

5. Enforce HTTPS + session TTL [Security + Principles]
   Commands:
     a. /cco-fix security --type https-redirect --file src/app.py
     b. /cco-fix security --type ttl --file src/session.py --ttl 24h
   Impact: HIGH - Prevents MITM + session hijacking
   Audits Affected: Security (HTTPS, TTL), Principles (C_AGENT_ORCHESTRATION_PATTERNS, P_TTL_BASED_CLEANUP)

6. Fix type errors [Code Quality]
   Command: /cco-fix type-errors --files src/models.py --strict
   Impact: HIGH - Prevents runtime errors
   Audits Affected: Code Quality (type checking)

7. Generate API documentation [Documentation + Principles]
   Commands:
     a. /cco-generate docs --type api --file src/api.py --format openapi
     b. /cco-generate docs --type docstrings --file src/api.py --coverage 100
   Impact: HIGH - Enables integration + self-documenting code
   Audits Affected: Documentation (API docs), Principles (P_CORS_POLICY)

   THIS WEEK Subtotal: 10 hours

📆 THIS SPRINT (Important):
────────────────────────────
8. Refactor code duplication [Code Quality + Principles]
   Command: /cco-fix duplication --files src/auth.py:45-98,src/api.py:123-176 --extract src/shared/auth.py
   Impact: MEDIUM - Centralized auth, easier maintenance
   Audits Affected: Code Quality (DRY), Principles (C_GREP_FIRST_SEARCH_STRATEGY)

9. Auto-format codebase [Code Quality]
   Command: /cco-fix formatting --scope all --save
   Impact: MEDIUM - Passes CI, consistent style
   Audits Affected: Code Quality (formatting)

10. Create setup documentation [Documentation]
    Command: /cco-generate docs --type readme --sections setup,quickstart
    Impact: MEDIUM - Faster onboarding
    Audits Affected: Documentation (README)

11. Fix flaky tests [Tests]
    Command: /cco-fix tests --type flaky --file tests/test_user.py
    Impact: MEDIUM - CI reliability
    Audits Affected: Tests (flaky tests)

   THIS SPRINT Subtotal: 6.5 hours

📋 BACKLOG (Low Priority):
───────────────────────────
12. Complete utility tests + docs
13. Add rate limiting
14. Simplify overengineered code

   BACKLOG Subtotal: 8 hours

═══════════════════════════════════════════════════════════
TOTAL TECHNICAL DEBT: 35.5 hours (of 47.5 hours addressable)
RISK REDUCTION: 95% (from HIGH to LOW)
HEALTH IMPROVEMENT: 68 → 91 (expected)
═══════════════════════════════════════════════════════════

EXECUTION STRATEGY
──────────────────
Week 1 (Day 1-2): IMMEDIATE fixes - Deploy blockers only
Week 1 (Day 3-5): THIS WEEK fixes - High priority
Week 2: THIS SPRINT fixes - Important improvements
Ongoing: BACKLOG - Nice-to-haves

METRICS & TRACKING
──────────────────
Track these KPIs after each fix:
  • Security Score: 45 → 95 (target)
  • Test Coverage: 45% → 80%+ (target)
  • Doc Health: 61 → 92 (target)
  • Principle Compliance: 72% → 95% (target)

Re-run audit after IMMEDIATE fixes:
  Command: /cco-audit --types security,tests,principles
  Expected: CRITICAL issues → 0

============================================================
```

**Report Generation Logic:**

1. **Cross-Audit Pattern Analysis:**
   - Identify issues that appear in multiple audits
   - Find root causes that affect multiple areas
   - Group related issues for batch fixing

2. **Intelligent Prioritization:**
   - Priority = (Severity × Impact × Urgency) ÷ Effort
   - Severity: From audit category (CRITICAL > HIGH > MEDIUM > LOW)
   - Impact: How many audits/areas affected
   - Urgency: Deployment blocker > security > quality > documentation
   - Effort: Realistic time estimate

3. **Command Consolidation:**
   - Combine related fixes: "Fix auth security" includes rotating secrets + adding tests
   - Sequence dependencies: Fix security before testing
   - Batch similar operations: Format entire codebase in one command

4. **Metrics:**
   - Technical Debt: Sum of effort hours
   - Risk Reduction: Weighted by severity (CRITICAL=40%, HIGH=25%, etc.)
   - Health Improvement: Projected score after fixes
   - Execution Timeline: Realistic sprint planning

5. **Cross-Audit Command Features:**
   - Multi-audit tags: Show which audits each fix addresses
   - Combined effort: Total time for related fixes
   - Cascading impact: How one fix improves multiple scores

---

## Step: Save Findings & Ask for Auto-Fix

After generating final report, save all findings and ask user if they want automatic fixes:

### Save Findings

```bash
python -c "
from pathlib import Path
from claudecodeoptimizer.core.audit_findings import AuditFindingsManager, AuditFinding

project_root = Path.cwd()
manager = AuditFindingsManager(project_root)

# Example: Add findings from audit
# (In real usage, these would come from audit results)

manager.add_finding(AuditFinding(
    finding_id='SEC-001',
    category='security',
    severity='CRITICAL',
    priority_tier='IMMEDIATE',
    title='Hardcoded AWS credentials',
    description='AWS credentials visible in git history',
    command='/cco-fix secrets --rotate --files src/config.py',
    effort_hours=0.08,
    risk_reduction_percent=40,
    file='src/config.py',
    line=23,
    principle='P_ZERO_DISK_TOUCH',
    audits_affected=['security', 'principles']
))

# Save all findings
manager.save(
    overall_health=68,
    technical_debt_hours=35.5,
    risk_level='HIGH'
)

print('[OK] Audit findings saved to .cco/audit-findings.json')
print(f'     Total findings: {len(manager.findings)}')
print(f'     Technical debt: {manager.metadata[\"technical_debt_hours\"]} hours')
"
```

### Ask User for Auto-Fix

**Use AskUserQuestion tool:**

```json
{
  "questions": [{
    "question": "Audit complete! Would you like to automatically fix all findings now?",
    "header": "Auto-Fix",
    "multiSelect": false,
    "options": [
      {
        "label": "Yes, fix all findings",
        "description": "Run all fix commands automatically (35.5 hours of work)"
      },
      {
        "label": "Yes, fix only IMMEDIATE priority",
        "description": "Fix only critical deploy blockers (11 hours of work)"
      },
      {
        "label": "No, I'll fix them manually",
        "description": "I'll review findings and run commands myself"
      },
      {
        "label": "No, but save for later",
        "description": "Save findings to fix later with /cco-fix-audit-findings"
      }
    ]
  }]
}
```

### Execute Based on User Choice

**Option 1: Fix all findings**
```bash
# Run: /cco-fix-audit-findings --auto --all
```

**Option 2: Fix only IMMEDIATE priority**
```bash
# Run: /cco-fix-audit-findings --auto --priority IMMEDIATE
```

**Option 3 & 4: No action**
- Findings already saved in `.cco/audit-findings.json`
- User can run `/cco-fix-audit-findings` anytime

---

## Error Handling

- If tool not found (e.g., black not installed), skip and note in report
- If audit fails, show error and continue with other audits
- If project not initialized, show "/cco-init" message
- If findings file exists, ask user if they want to overwrite or append

---

## Related Commands

- `/cco-fix-audit-findings` - Fix saved audit findings (see dedicated command)
- `/cco-fix code` - Auto-fix code quality issues
- `/cco-fix security` - Fix security vulnerabilities
- `/cco-generate tests` - Generate missing tests
- `/cco-fix docs` - Update documentation
