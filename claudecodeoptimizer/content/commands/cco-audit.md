# cco-audit

**Comprehensive issue detection across 17 categories, pain-point priority ordered.**

---

## Purpose

Find security vulnerabilities, technical debt, testing gaps, and other issues using specialized skills and parallel agent execution.

---

## 17 Audit Categories (Pain-Point Priority Order)

### 🔴 Critical Impact

1. **--security** (Pain #1: 51% top concern)
   - Skills: `cco-skill-security-owasp-xss-sqli-csrf`, `cco-skill-ai-security-promptinjection-models`, `cco-skill-supply-chain-dependencies-sast`
   - Checks: SQL injection, XSS, CSRF, secrets, auth/authz, CVEs, AI prompt injection

2. **--tech-debt** (Pain #2: 23% time waste)
   - Skills: `cco-skill-code-quality-refactoring-complexity`, `cco-skill-content-optimization-automation`
   - Checks: Dead code, complexity, duplication, TODO comments, anti-patterns

3. **--ai-security** (Pain #3: 45% reliability)
   - Skills: `cco-skill-ai-security-promptinjection-models`
   - Checks: Prompt injection, hallucination risks, AI output validation, rate limiting

### 🟡 High Impact

4. **--tests** (Pain #4: Biggest mistake)
   - Skills: `cco-skill-test-pyramid-coverage-isolation`, `cco-skill-api-testing-contract-load-chaos`
   - Checks: Coverage, untested critical functions, test isolation, pyramid compliance, edge cases

5. **--integration** (Pain #6: Deployment failures)
   - Skills: `cco-skill-supply-chain-dependencies-sast`
   - Checks: Import errors, dependency conflicts, outdated dependencies, circular imports

### 🟢 Medium Impact

6. **--code-quality**
   - Skills: `cco-skill-code-quality-refactoring-complexity`
   - Checks: Syntax errors, logic bugs, off-by-one, missing error handling, type errors

7. **--docs** (Pain #7: Knowledge gaps)
   - Skills: `cco-skill-docs-api-openapi-adr-runbooks`
   - Checks: README, API docs, docstrings, documentation drift, ADRs, runbooks

8. **--database** (Pain #5: Performance)
   - Skills: `cco-skill-database-optimization-caching-profiling`, `cco-skill-data-migrations-backup-versioning`
   - Checks: N+1 queries, missing indexes, connection pooling, migrations

9. **--observability** (Pain #5: Debugging time)
   - Skills: `cco-skill-observability-metrics-alerts-slo`, `cco-skill-logging-structured-correlation-tracing`, `cco-skill-incident-oncall-postmortem-playbooks`
   - Checks: Structured logging, correlation IDs, metrics, alerts, SLOs, runbooks

10. **--monitoring**
    - Skills: `cco-skill-observability-metrics-alerts-slo`
    - Checks: Prometheus/Grafana, key metrics, alert rules, dashboards

11. **--cicd** (Pain #6: Deployment)
    - Skills: `cco-skill-cicd-gates-deployment-automation`, `cco-skill-deployment-bluegreen-canary-rollback`
    - Checks: Pipeline, quality gates, deployment strategy, rollback, secret management

12. **--containers**
    - Skills: `cco-skill-kubernetes-security-containers`
    - Checks: Dockerfile best practices, vulnerabilities, non-root user, K8s security

13. **--supply-chain** (Pain #1 related)
    - Skills: `cco-skill-supply-chain-dependencies-sast`
    - Checks: CVEs, SBOM, license compliance, typosquatting, unmaintained packages

14. **--migrations**
    - Skills: `cco-skill-data-migrations-backup-versioning`
    - Checks: Migration strategy, rollback, consistency checks, backup procedures

15. **--performance** (Pain #5: Time waste)
    - Skills: `cco-skill-database-optimization-caching-profiling`, `cco-skill-frontend-bundle-a11y-performance`, `cco-skill-resilience-circuitbreaker-retry-bulkhead`
    - Checks: Response times, query performance, caching, bundle size, circuit breakers

16. **--architecture**
    - Skills: `cco-skill-microservices-cqrs-mesh-di`, `cco-skill-eventdriven-async-messaging-queues`
    - Checks: Separation of concerns, coupling, circular dependencies, patterns

17. **--git** (Pain #5: Workflow quality)
    - Skills: `cco-skill-git-branching-pr-review`, `cco-skill-versioning-semver-changelog-compat`
    - Checks: Commit quality, branch naming, PR process, semantic versioning, changelog

---

## Execution Protocol

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# Audit Command

**What I do:**
I scan your codebase for issues across 17 categories including security vulnerabilities, technical debt, testing gaps, and performance problems.

**How it works:**
1. You select which categories to audit (or "All" for comprehensive scan)
2. I analyze your project files using specialized skills
3. I report all issues with severity, file locations, and recommended fixes
4. Results are saved for /cco-fix to use

**What you'll get:**
- Detailed list of issues by severity (Critical/High/Medium/Low)
- Exact file:line references for each issue
- Risk explanations and fix recommendations
- Pain-point impact analysis (addresses Pain #1: 51% security concern, Pain #2: 23% tech debt, etc.)

**Time estimate:** 2-10 minutes depending on project size and selected categories

**No changes will be made** - this is analysis only.
```

**Then ask for confirmation using AskUserQuestion:**

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start the audit?",
    header: "Start Audit",
    multiSelect: false,
    options: [
      {
        label: "Yes, start audit",
        description: "Begin analyzing the codebase for issues"
      },
      {
        label: "No, cancel",
        description: "Exit without running audit"
      }
    ]
  }]
})
```

**CRITICAL:**
- If user selects "No, cancel" → EXIT immediately, do NOT proceed
- If user selects "Yes, start audit" → Continue to Step 1

---

### Interactive Mode (No Parameters)

**STEP 1: Ask user what level of audit detail they want:**

```python
AskUserQuestion({
  questions: [{
    question: "What level of audit detail do you need?",
    header: "Audit Level",
    multiSelect: false,
    options: [
      {
        label: "Quick Presets",
        description: "Use-case based audit groups (Pre-commit, Pre-deployment, Performance focus, etc.) - Fastest, recommended for specific goals"
      },
      {
        label: "Category Level",
        description: "Choose from 17 categories (Security, Tests, Database, etc.) - Balanced approach"
      },
      {
        label: "Granular Level",
        description: "Select specific checks (SQL injection only, N+1 queries only, etc.) - Most detailed control"
      }
    ]
  }]
})
```

---

### Level 1: Quick Presets (Use-Case Based)

**If user selected "Quick Presets", present these preset audit groups:**

```python
AskUserQuestion({
  questions: [{
    question: "Which preset audit would you like to run?",
    header: "Preset Audits",
    multiSelect: false,
    options: [
      {
        label: "Pre-Commit Quick Check",
        description: "⚡ FAST (2-3 min) - Critical issues only: Syntax errors, linting, secrets, obvious bugs | Perfect before git commit"
      },
      {
        label: "Pre-Deployment Security",
        description: "🔒 SECURITY (5-7 min) - All security checks: SQL injection, XSS, CSRF, secrets, CVEs, auth/authz | Run before deploying"
      },
      {
        label: "Performance Focus",
        description: "⚡ PERFORMANCE (8-10 min) - N+1 queries, missing indexes, slow code, large bundles, no caching | Optimize before launch"
      },
      {
        label: "Code Quality Focus",
        description: "🧹 QUALITY (10-12 min) - Dead code, complexity, duplication, tech debt, code smells | Weekly cleanup"
      },
      {
        label: "Testing Gaps",
        description: "🧪 TESTS (5-7 min) - Coverage gaps, missing tests, test quality, isolation issues | Improve test suite"
      },
      {
        label: "Production Readiness",
        description: "🚀 PRODUCTION (15-20 min) - Security + Performance + Observability + CI/CD + Containers | Before going live"
      },
      {
        label: "Comprehensive Weekly",
        description: "📋 COMPREHENSIVE (20-30 min) - All 17 categories, complete scan | Weekly/monthly review"
      }
    ]
  }]
})
```

**Preset Mappings (what gets checked):**

```markdown
Pre-Commit Quick Check:
- Syntax errors (grep for common syntax issues)
- Hardcoded secrets (API keys, passwords)
- Linting issues (if linter exists)
- Type errors (if type checker exists)
- Obvious bugs (null pointer, division by zero)

Pre-Deployment Security:
- All Security category checks
- All AI Security checks
- All Supply Chain checks
- Auth/authz validation

Performance Focus:
- All Database optimization checks
- All Performance checks
- Bundle size analysis
- Code complexity

Code Quality Focus:
- All Tech Debt checks
- All Code Quality checks
- Dead code removal
- Complexity reduction

Testing Gaps:
- All Tests category checks
- Coverage analysis
- Missing test detection

Production Readiness:
- Security + Performance + Database
- Observability + Monitoring
- CI/CD + Containers
- Migrations

Comprehensive Weekly:
- All 17 categories
```

---

### Level 2: Category Level (Current System)

**If user selected "Category Level", analyze project first** to get real numbers, then **use AskUserQuestion** to present multiselect UI:

**IMPORTANT:** The numbers in option descriptions below are EXAMPLES. You MUST:
- Run Glob/Grep to analyze the actual project
- Count real issues (e.g., actual number of untested functions, actual CVEs, etc.)
- Replace example numbers with REAL project-specific data
- Calculate real percentages based on actual findings

```python
AskUserQuestion({
  questions: [{
    question: "What should I audit? Select all categories you want to check:",
    header: "Audit",
    multiSelect: true,
    options: [
      {
        label: "Security",
        description: "🔴 CRITICAL - 51% #1 concern: OWASP vulnerabilities, AI security, supply chain (SQL injection, XSS, CSRF, secrets, CVEs)"
      },
      {
        label: "Tech Debt",
        description: "🔴 CRITICAL - 23% time waste: Dead code, complexity, duplication, TODO comments, anti-patterns"
      },
      {
        label: "AI Security",
        description: "🔴 CRITICAL - 45% reliability: Prompt injection, hallucination risks, AI output validation, rate limiting"
      },
      {
        label: "Tests",
        description: "🟡 HIGH - Biggest mistake: Coverage gaps, untested functions, test isolation, pyramid compliance, edge cases"
      },
      {
        label: "Integration",
        description: "🟡 HIGH - Deployment failures: Import errors, dependency conflicts, outdated deps, circular imports"
      },
      {
        label: "Code Quality",
        description: "🟢 MEDIUM - Syntax errors, logic bugs, off-by-one, missing error handling, type errors"
      },
      {
        label: "Documentation",
        description: "🟢 MEDIUM - Pain #7 knowledge gaps: README, API docs, docstrings, documentation drift, ADRs, runbooks"
      },
      {
        label: "Database",
        description: "🟢 MEDIUM - Pain #5 performance: N+1 queries, missing indexes, connection pooling, migrations"
      },
      {
        label: "Observability",
        description: "🟢 MEDIUM - Pain #5 debugging time: Structured logging, correlation IDs, metrics, alerts, SLOs, runbooks"
      },
      {
        label: "Monitoring",
        description: "🟢 MEDIUM - Prometheus/Grafana setup, key metrics, alert rules, dashboards"
      },
      {
        label: "CI/CD",
        description: "🟢 MEDIUM - Pain #6 deployment: Pipeline quality, gates, deployment strategy, rollback, secret management"
      },
      {
        label: "Containers",
        description: "🟢 MEDIUM - Dockerfile best practices, vulnerabilities, non-root user, K8s security"
      },
      {
        label: "Supply Chain",
        description: "🟢 MEDIUM - Pain #1 related: CVEs, SBOM, license compliance, typosquatting, unmaintained packages"
      },
      {
        label: "Migrations",
        description: "🟢 MEDIUM - Migration strategy, rollback, consistency checks, backup procedures"
      },
      {
        label: "Performance",
        description: "🟢 MEDIUM - Pain #5 time waste: Response times, query performance, caching, bundle size, circuit breakers"
      },
      {
        label: "Architecture",
        description: "🟢 MEDIUM - Separation of concerns, coupling, circular dependencies, design patterns"
      },
      {
        label: "Git",
        description: "🟢 MEDIUM - Pain #5 workflow: Commit quality, branch naming, PR process, semantic versioning, changelog"
      },
      {
        label: "All",
        description: "✅ Comprehensive scan - Run all 17 audit categories (recommended for initial assessment)"
      }
    ]
  }]
})
```

**IMPORTANT:** If user selects "All", ignore all other selections and audit all 17 categories.

---

### Level 3: Granular Level (Specific Checks)

**If user selected "Granular Level", present individual checks with multiselect:**

**IMPORTANT - Sabit Liste Yaklaşımı:**
1. **Aşağıdaki liste SABİTTİR** - Her projede aynı 92 check gösterilir
2. **Proje analizi yapılır** - Tech stack detect edilir (Python, Flask, PostgreSQL, React, etc.)
3. **Smart filtering uygulanır:**
   - ✅ APPLICABLE: Projeye uygun checkler (yeşil, enabled)
   - ⚪ NOT APPLICABLE: Projeye uygun olmayan checkler (grayed out, disabled veya gizli)
4. **Kullanıcı seçer:**
   - "Show All 92 Checks" → Hepsini göster (applicable + non-applicable)
   - "Show Only Applicable" → Sadece uygun olanları göster (default)

**Tech Stack Detection - Analiz et:**
```python
# Proje analizi
detected_tech = {
    "languages": [],      # python, javascript, java, go, etc.
    "frameworks": [],     # flask, fastapi, django, react, vue, etc.
    "databases": [],      # postgresql, mysql, mongodb, redis, etc.
    "platforms": [],      # web, mobile, api, desktop, etc.
    "tools": []          # docker, kubernetes, ci/cd, etc.
}

# Glob/Grep ile tespit et
- Glob("**/*.py") → Python detected
- Glob("**/requirements.txt") → Check for flask, django, fastapi
- Glob("**/package.json") → JavaScript detected, check dependencies
- Glob("**/Dockerfile") → Docker detected
- Glob("**/*.sql") → SQL usage detected
- Glob("**/templates/**") → Web templates detected
- etc.
```

---

## 📋 Complete Granular Audit Checklist (92 Checks)

**This is the MASTER LIST - same for all projects.**

```python
# BEFORE showing options, DETECT tech stack
detected_tech = analyze_project()
# Example result: {"languages": ["python"], "frameworks": ["flask"], "databases": ["postgresql"], "platforms": ["web"], "tools": ["docker"]}

# THEN show options with applicable markers
AskUserQuestion({
  questions: [{
    question: "Select specific checks to run (showing X applicable, Y not applicable):",
    header: "Granular Audit",
    multiSelect: true,
    options: [
      # ========================================
      # SECURITY CHECKS (15 checks)
      # ========================================
      {
        label: "SQL Injection check",
        description: "(Security, 1 min) Check for string concatenation in SQL | ✅ APPLICABLE - SQL detected | 🔴 CRITICAL"
        # Applicable if: databases detected OR sql files found OR ORM imports found
      },
      {
        label: "XSS vulnerability check",
        description: "(Security, 1 min) Check for unescaped template variables | ✅ APPLICABLE - Templates detected | 🔴 CRITICAL"
        # Applicable if: templates/** found OR render_template/render used
      },
      {
        label: "CSRF protection check",
        description: "(Security, 1 min) Verify CSRF tokens on forms | ✅ APPLICABLE - Forms detected | 🔴 CRITICAL"
        # Applicable if: <form> tags found OR web framework detected
      },
      {
        label: "Hardcoded secrets check",
        description: "(Security, 1 min) Find API keys, passwords, tokens in code | ✅ APPLICABLE - Always applicable | 🔴 CRITICAL"
        # Applicable if: ALWAYS (all projects)
      },
      {
        label: "Authentication check",
        description: "(Security, 2 min) Verify authentication on protected endpoints | ✅ APPLICABLE - API/Web detected | 🔴 CRITICAL"
        # Applicable if: API endpoints found OR web app detected
      },
      {
        label: "Authorization check",
        description: "(Security, 2 min) Verify authorization/permissions | ✅ APPLICABLE - API/Web detected | 🔴 CRITICAL"
        # Applicable if: API endpoints found OR web app detected
      },
      {
        label: "Dependency CVE scan",
        description: "(Security, 2 min) Check all dependencies for known vulnerabilities | ✅ APPLICABLE - Dependencies detected | 🔴 CRITICAL"
        # Applicable if: requirements.txt OR package.json OR go.mod found
      },
      {
        label: "AI prompt injection check",
        description: "(Security, 1 min) Check for AI prompt injection risks | ⚪ NOT APPLICABLE - No AI usage detected | 🔴 CRITICAL"
        # Applicable if: openai/anthropic/langchain imports found
      },
      {
        label: "SSRF vulnerability check",
        description: "(Security, 1 min) Check for Server-Side Request Forgery | ✅ APPLICABLE - HTTP requests detected | 🔴 CRITICAL"
        # Applicable if: requests/http/fetch usage found
      },
      {
        label: "XXE vulnerability check",
        description: "(Security, 1 min) Check for XML External Entity attacks | ⚪ NOT APPLICABLE - No XML parsing detected | 🔴 CRITICAL"
        # Applicable if: XML parsing libraries found
      },
      {
        label: "Path traversal check",
        description: "(Security, 1 min) Check for directory traversal vulnerabilities | ✅ APPLICABLE - File operations detected | 🔴 CRITICAL"
        # Applicable if: file operations (open, read, write) found
      },
      {
        label: "Command injection check",
        description: "(Security, 1 min) Check for OS command injection | ✅ APPLICABLE - Shell commands detected | 🔴 CRITICAL"
        # Applicable if: subprocess/os.system/exec usage found
      },
      {
        label: "Insecure deserialization check",
        description: "(Security, 1 min) Check for unsafe pickle/yaml.load usage | ✅ APPLICABLE - Serialization detected | 🔴 CRITICAL"
        # Applicable if: pickle/yaml/json deserialization found
      },
      {
        label: "Weak cryptography check",
        description: "(Security, 1 min) Check for weak crypto (MD5, SHA1, DES) | ✅ APPLICABLE - Crypto usage detected | 🔴 CRITICAL"
        # Applicable if: hashlib/crypto imports found
      },
      {
        label: "Security headers check",
        description: "(Security, 1 min) Check for missing security headers (CSP, HSTS, etc.) | ✅ APPLICABLE - Web app detected | 🟡 HIGH"
        # Applicable if: web framework detected
      },

      # ========================================
      # DATABASE CHECKS (10 checks)
      # ========================================
      {
        label: "N+1 query detection",
        description: "(Database, 2 min) Find N+1 patterns (loops with queries) | ✅ APPLICABLE - ORM detected | 🔴 CRITICAL"
        # Applicable if: ORM imports (SQLAlchemy, Django ORM, etc.) found
      },
      {
        label: "Missing indexes check",
        description: "(Database, 2 min) Analyze slow queries for missing indexes | ✅ APPLICABLE - SQL detected | 🔴 CRITICAL"
        # Applicable if: database detected
      },
      {
        label: "Slow queries check",
        description: "(Database, 2 min) Find queries taking >100ms | ✅ APPLICABLE - SQL detected | 🔴 CRITICAL"
        # Applicable if: database detected
      },
      {
        label: "Connection pooling check",
        description: "(Database, 1 min) Verify database connection pooling | ✅ APPLICABLE - Database detected | 🟡 HIGH"
        # Applicable if: database connection code found
      },
      {
        label: "Query optimization check",
        description: "(Database, 2 min) Find inefficient queries (SELECT *, unnecessary JOINs) | ✅ APPLICABLE - SQL detected | 🟡 HIGH"
        # Applicable if: SQL queries found
      },
      {
        label: "Transaction isolation check",
        description: "(Database, 1 min) Verify transaction isolation levels | ✅ APPLICABLE - Transactions detected | 🟡 HIGH"
        # Applicable if: transaction usage found
      },
      {
        label: "Deadlock detection",
        description: "(Database, 2 min) Check for potential deadlock scenarios | ✅ APPLICABLE - SQL detected | 🟢 MEDIUM"
        # Applicable if: database detected
      },
      {
        label: "Migration consistency check",
        description: "(Database, 1 min) Verify migration files are consistent | ✅ APPLICABLE - Migrations detected | 🟡 HIGH"
        # Applicable if: migrations/ directory found
      },
      {
        label: "Raw SQL usage check",
        description: "(Database, 1 min) Find raw SQL instead of ORM (security risk) | ✅ APPLICABLE - SQL detected | 🟡 HIGH"
        # Applicable if: SQL queries found
      },
      {
        label: "Database credentials check",
        description: "(Database, 1 min) Check for hardcoded database credentials | ✅ APPLICABLE - Database detected | 🔴 CRITICAL"
        # Applicable if: database connection code found
      },

      # ========================================
      # TEST CHECKS (12 checks)
      # ========================================
      {
        label: "Test coverage analysis",
        description: "(Tests, 2 min) Calculate coverage %, find gaps | ✅ APPLICABLE - Tests detected | 🔴 CRITICAL"
        # Applicable if: tests/ directory found
      },
      {
        label: "Untested functions detection",
        description: "(Tests, 2 min) List all functions without tests | ✅ APPLICABLE - Always applicable | 🔴 CRITICAL"
        # Applicable if: ALWAYS
      },
      {
        label: "Test isolation check",
        description: "(Tests, 1 min) Find tests with external dependencies | ✅ APPLICABLE - Tests detected | 🟡 HIGH"
        # Applicable if: tests found
      },
      {
        label: "Test pyramid validation",
        description: "(Tests, 1 min) Verify unit >> integration >> e2e ratio | ✅ APPLICABLE - Tests detected | 🟡 HIGH"
        # Applicable if: tests found
      },
      {
        label: "Edge case coverage check",
        description: "(Tests, 1 min) Check for error case testing | ✅ APPLICABLE - Tests detected | 🟡 HIGH"
        # Applicable if: tests found
      },
      {
        label: "Flaky tests detection",
        description: "(Tests, 2 min) Find tests that fail intermittently | ✅ APPLICABLE - Tests detected | 🟡 HIGH"
        # Applicable if: tests found
      },
      {
        label: "Test naming check",
        description: "(Tests, 1 min) Verify test names are descriptive | ✅ APPLICABLE - Tests detected | 🟢 MEDIUM"
        # Applicable if: tests found
      },
      {
        label: "Assertion quality check",
        description: "(Tests, 1 min) Check for weak assertions (assertTrue only) | ✅ APPLICABLE - Tests detected | 🟡 HIGH"
        # Applicable if: tests found
      },
      {
        label: "Mock overuse check",
        description: "(Tests, 1 min) Find tests with excessive mocking | ✅ APPLICABLE - Tests detected | 🟢 MEDIUM"
        # Applicable if: tests found
      },
      {
        label: "Test data management check",
        description: "(Tests, 1 min) Verify test data setup/teardown | ✅ APPLICABLE - Tests detected | 🟡 HIGH"
        # Applicable if: tests found
      },
      {
        label: "Integration test coverage",
        description: "(Tests, 2 min) Check integration test coverage | ✅ APPLICABLE - API detected | 🟡 HIGH"
        # Applicable if: API endpoints found
      },
      {
        label: "E2E test coverage",
        description: "(Tests, 2 min) Check end-to-end test coverage | ✅ APPLICABLE - Web app detected | 🟢 MEDIUM"
        # Applicable if: web frontend detected
      },

      # ========================================
      # CODE QUALITY CHECKS (15 checks)
      # ========================================
      {
        label: "Dead code detection",
        description: "(Code Quality, 2 min) Find unused functions, imports | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Complexity analysis",
        description: "(Code Quality, 2 min) Find functions with cyclomatic complexity >10 | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Code duplication check",
        description: "(Code Quality, 2 min) Find duplicate code blocks (copy-paste) | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Type errors check",
        description: "(Code Quality, 1 min) Run type checker (mypy, TypeScript) | ✅ APPLICABLE - Type hints detected | 🟡 HIGH"
        # Applicable if: type hints found OR TypeScript detected
      },
      {
        label: "Linting issues check",
        description: "(Code Quality, 1 min) Run linter (pylint, eslint, etc.) | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Code smells detection",
        description: "(Code Quality, 2 min) Find long parameter lists, god classes, etc. | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Long functions check",
        description: "(Code Quality, 1 min) Find functions >50 lines | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Long files check",
        description: "(Code Quality, 1 min) Find files >500 lines | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Deep nesting check",
        description: "(Code Quality, 1 min) Find code with >4 nesting levels | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Magic numbers check",
        description: "(Code Quality, 1 min) Find hardcoded numbers (not 0, 1, -1) | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "TODO comments check",
        description: "(Code Quality, 1 min) Find TODO/FIXME/HACK comments | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Commented code check",
        description: "(Code Quality, 1 min) Find large blocks of commented code | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Import organization check",
        description: "(Code Quality, 1 min) Check import ordering and grouping | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Naming conventions check",
        description: "(Code Quality, 1 min) Verify snake_case, camelCase, PascalCase | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Error handling check",
        description: "(Code Quality, 2 min) Find bare except, missing error handling | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },

      # ========================================
      # PERFORMANCE CHECKS (10 checks)
      # ========================================
      {
        label: "Slow query detection",
        description: "(Performance, 2 min) Find queries taking >100ms | ✅ APPLICABLE - Database detected | 🔴 CRITICAL"
        # Applicable if: database detected
      },
      {
        label: "Large bundle analysis",
        description: "(Performance, 2 min) Check frontend bundle size | ✅ APPLICABLE - Frontend detected | 🟡 HIGH"
        # Applicable if: webpack/vite/rollup config found
      },
      {
        label: "No caching check",
        description: "(Performance, 1 min) Find expensive operations without caching | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Circuit breaker check",
        description: "(Performance, 1 min) Verify circuit breakers on external calls | ✅ APPLICABLE - API calls detected | 🟢 MEDIUM"
        # Applicable if: HTTP client usage found
      },
      {
        label: "Memory leak detection",
        description: "(Performance, 2 min) Find potential memory leaks | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Inefficient algorithms check",
        description: "(Performance, 2 min) Find O(n²) or worse algorithms | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Large loops check",
        description: "(Performance, 1 min) Find loops processing >10k items | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "File I/O optimization check",
        description: "(Performance, 1 min) Find inefficient file operations | ✅ APPLICABLE - File I/O detected | 🟡 HIGH"
        # Applicable if: file operations found
      },
      {
        label: "Network calls in loops check",
        description: "(Performance, 1 min) Find API calls inside loops | ✅ APPLICABLE - HTTP usage detected | 🔴 CRITICAL"
        # Applicable if: HTTP client usage found
      },
      {
        label: "Lazy loading check",
        description: "(Performance, 1 min) Verify lazy loading for heavy resources | ✅ APPLICABLE - Frontend detected | 🟢 MEDIUM"
        # Applicable if: frontend framework detected
      },

      # ========================================
      # DOCUMENTATION CHECKS (8 checks)
      # ========================================
      {
        label: "Missing docstrings check",
        description: "(Documentation, 1 min) Find functions without docstrings | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "API documentation check",
        description: "(Documentation, 1 min) Verify OpenAPI/Swagger exists | ✅ APPLICABLE - API detected | 🟡 HIGH"
        # Applicable if: API endpoints found
      },
      {
        label: "README completeness check",
        description: "(Documentation, 1 min) Verify README has setup, usage, contributing | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Documentation drift check",
        description: "(Documentation, 2 min) Find code-doc inconsistencies | ✅ APPLICABLE - Docs detected | 🟢 MEDIUM"
        # Applicable if: docs/ directory found
      },
      {
        label: "Code comments check",
        description: "(Documentation, 1 min) Check comment quality and relevance | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Examples check",
        description: "(Documentation, 1 min) Verify code examples in docs | ✅ APPLICABLE - Docs detected | 🟢 MEDIUM"
        # Applicable if: docs/ directory found
      },
      {
        label: "Architecture docs check (ADRs)",
        description: "(Documentation, 1 min) Check for Architecture Decision Records | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Runbooks check",
        description: "(Documentation, 1 min) Verify operational runbooks exist | ✅ APPLICABLE - Production app | 🟡 HIGH"
        # Applicable if: production deployment indicators
      },

      # ========================================
      # CI/CD CHECKS (8 checks)
      # ========================================
      {
        label: "Pipeline existence check",
        description: "(CI/CD, 1 min) Verify CI/CD pipeline exists | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Quality gates check",
        description: "(CI/CD, 1 min) Verify linting, testing in pipeline | ✅ APPLICABLE - Pipeline detected | 🟡 HIGH"
        # Applicable if: CI config found
      },
      {
        label: "Secret management check",
        description: "(CI/CD, 1 min) Verify secrets not in pipeline files | ✅ APPLICABLE - Pipeline detected | 🔴 CRITICAL"
        # Applicable if: CI config found
      },
      {
        label: "Build optimization check",
        description: "(CI/CD, 1 min) Check for build caching, parallel jobs | ✅ APPLICABLE - Pipeline detected | 🟢 MEDIUM"
        # Applicable if: CI config found
      },
      {
        label: "Test automation check",
        description: "(CI/CD, 1 min) Verify tests run automatically | ✅ APPLICABLE - Pipeline detected | 🟡 HIGH"
        # Applicable if: CI config found
      },
      {
        label: "Deployment automation check",
        description: "(CI/CD, 1 min) Verify automated deployment | ✅ APPLICABLE - Pipeline detected | 🟡 HIGH"
        # Applicable if: CI config found
      },
      {
        label: "Rollback strategy check",
        description: "(CI/CD, 1 min) Verify rollback capability | ✅ APPLICABLE - Deployment detected | 🟡 HIGH"
        # Applicable if: deployment config found
      },
      {
        label: "Environment parity check",
        description: "(CI/CD, 1 min) Verify dev/staging/prod consistency | ✅ APPLICABLE - Multiple envs detected | 🟡 HIGH"
        # Applicable if: multiple environment configs found
      },

      # ========================================
      # CONTAINER CHECKS (6 checks)
      # ========================================
      {
        label: "Dockerfile best practices",
        description: "(Containers, 1 min) Check for anti-patterns | ✅ APPLICABLE - Docker detected | 🟡 HIGH"
        # Applicable if: Dockerfile found
      },
      {
        label: "Multi-stage builds check",
        description: "(Containers, 1 min) Verify multi-stage Dockerfile | ✅ APPLICABLE - Docker detected | 🟡 HIGH"
        # Applicable if: Dockerfile found
      },
      {
        label: "Non-root user check",
        description: "(Containers, 1 min) Verify container runs as non-root | ✅ APPLICABLE - Docker detected | 🔴 CRITICAL"
        # Applicable if: Dockerfile found
      },
      {
        label: "Image size check",
        description: "(Containers, 1 min) Check Docker image size | ✅ APPLICABLE - Docker detected | 🟡 HIGH"
        # Applicable if: Dockerfile found
      },
      {
        label: "Base image vulnerabilities",
        description: "(Containers, 2 min) Scan base images for CVEs | ✅ APPLICABLE - Docker detected | 🔴 CRITICAL"
        # Applicable if: Dockerfile found
      },
      {
        label: "Layer optimization check",
        description: "(Containers, 1 min) Check layer ordering for caching | ✅ APPLICABLE - Docker detected | 🟢 MEDIUM"
        # Applicable if: Dockerfile found
      },

      # ========================================
      # TECH DEBT CHECKS (8 checks)
      # ========================================
      {
        label: "Deprecated APIs check",
        description: "(Tech Debt, 2 min) Find usage of deprecated APIs/libraries | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Legacy code detection",
        description: "(Tech Debt, 2 min) Find old code needing refactoring | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Hard dependencies check",
        description: "(Tech Debt, 1 min) Find tight coupling to external services | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "Tight coupling check",
        description: "(Tech Debt, 2 min) Find modules with high coupling | ✅ APPLICABLE - Always applicable | 🟡 HIGH"
        # Applicable if: ALWAYS
      },
      {
        label: "God objects detection",
        description: "(Tech Debt, 2 min) Find classes doing too much | ✅ APPLICABLE - OOP detected | 🟡 HIGH"
        # Applicable if: classes found
      },
      {
        label: "Feature envy detection",
        description: "(Tech Debt, 1 min) Find methods using other class data excessively | ✅ APPLICABLE - OOP detected | 🟢 MEDIUM"
        # Applicable if: classes found
      },
      {
        label: "Data clumps check",
        description: "(Tech Debt, 1 min) Find repeated parameter groups | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },
      {
        label: "Shotgun surgery check",
        description: "(Tech Debt, 2 min) Find changes requiring edits in many places | ✅ APPLICABLE - Always applicable | 🟢 MEDIUM"
        # Applicable if: ALWAYS
      },

      # ========================================
      # GROUP OPTIONS - Category-wise
      # ========================================
      {
        label: "All Security Checks",
        description: "✅ Run all 15 security checks (SQL injection, XSS, CSRF, secrets, auth, authz, CVEs, AI, SSRF, XXE, path traversal, command injection, deserialization, weak crypto, headers)"
      },
      {
        label: "All Database Checks",
        description: "✅ Run all 10 database checks (N+1, indexes, slow queries, pooling, optimization, transactions, deadlocks, migrations, raw SQL, credentials)"
      },
      {
        label: "All Test Checks",
        description: "✅ Run all 12 test checks (coverage, untested functions, isolation, pyramid, edge cases, flaky tests, naming, assertions, mocks, data management, integration, e2e)"
      },
      {
        label: "All Code Quality Checks",
        description: "✅ Run all 15 code quality checks (dead code, complexity, duplication, types, linting, smells, long functions/files, nesting, magic numbers, TODOs, commented code, imports, naming, error handling)"
      },
      {
        label: "All Performance Checks",
        description: "✅ Run all 10 performance checks (slow queries, bundles, caching, circuit breakers, memory leaks, algorithms, loops, file I/O, network calls, lazy loading)"
      },
      {
        label: "All Documentation Checks",
        description: "✅ Run all 8 documentation checks (docstrings, API docs, README, drift, comments, examples, ADRs, runbooks)"
      },
      {
        label: "All CI/CD Checks",
        description: "✅ Run all 8 CI/CD checks (pipeline, quality gates, secrets, build optimization, test automation, deployment automation, rollback, environment parity)"
      },
      {
        label: "All Container Checks",
        description: "✅ Run all 6 container checks (Dockerfile best practices, multi-stage, non-root, image size, base image vulnerabilities, layer optimization)"
      },
      {
        label: "All Tech Debt Checks",
        description: "✅ Run all 8 tech debt checks (deprecated APIs, legacy code, hard dependencies, tight coupling, god objects, feature envy, data clumps, shotgun surgery)"
      },

      # ========================================
      # FILTERING OPTIONS
      # ========================================
      {
        label: "Show All 92 Checks",
        description: "📋 Display ALL 92 checks (including non-applicable ones marked with ⚪)"
      },
      {
        label: "Show Only Applicable",
        description: "✅ Display only applicable checks for this project (default, recommended)"
      },

      # ========================================
      # MASTER OPTION
      # ========================================
      {
        label: "All Granular Checks",
        description: "✅ RUN ALL 92 CHECKS - Comprehensive granular audit (ignores other selections)"
      }
    ]
  }]
})
```

**Summary of 92 Granular Checks:**
- Security: 15 checks
- Database: 10 checks
- Tests: 12 checks
- Code Quality: 15 checks
- Performance: 10 checks
- Documentation: 8 checks
- CI/CD: 8 checks
- Containers: 6 checks
- Tech Debt: 8 checks

**Total: 92 checks**

---

## 📝 Implementation Instructions for Level 3

**CRITICAL - Sabit Liste + Smart Filtering Protocol:**

1. **Tech Stack Detection (MUST DO FIRST):**
   ```python
   detected_tech = {
       "languages": [],
       "frameworks": [],
       "databases": [],
       "platforms": [],
       "tools": []
   }

   # Use Glob to detect
   if Glob("**/*.py").found:
       detected_tech["languages"].append("python")
   if Glob("**/requirements.txt").found:
       # Read and check for flask, django, fastapi
   if Glob("**/package.json").found:
       detected_tech["languages"].append("javascript")
       # Read and check for react, vue, angular
   if Glob("**/Dockerfile").found:
       detected_tech["tools"].append("docker")
   if Glob("**/*.sql").found or Glob("**/migrations/**").found:
       detected_tech["databases"].append("sql")
   # etc...
   ```

2. **Applicability Determination:**
   - For each of the 92 checks, determine if applicable based on detected_tech
   - Mark with ✅ APPLICABLE or ⚪ NOT APPLICABLE
   - Update description with specific reason

3. **Filtering Options:**
   - Default: Show only applicable checks (recommended)
   - Optional: "Show All 92 Checks" to see everything

4. **User Selection:**
   - Individual checks: Run ONLY selected
   - Category group (e.g., "All Security Checks"): Run all in that category
   - "All Granular Checks": Run ALL 92 checks

**IMPORTANT:**
- If user selects "All Granular Checks", run ALL checks
- If user selects "All [Category] Checks", run all checks in that category
- Otherwise, run ONLY the individually selected checks
- Show real data in descriptions (e.g., "Found 23 functions without tests")

---

### Common Step for All Levels

2. **Present analysis plan and confirm** using AskUserQuestion:

```markdown
Selected categories: [list selected categories or "All 17 categories"]

Skills I'll use:
- [list skills for selected categories]

Agent: cco-agent-audit (Haiku for fast scanning, Sonnet for complex analysis)

I'll check:
- [specific checks for each selected category]
- [estimated file count] files to analyze
- Estimated time: [X] minutes
```

```python
AskUserQuestion({
  questions: [{
    question: "Ready to start the audit with the configuration above?",
    header: "Confirm",
    multiSelect: false,
    options: [
      {
        label: "Yes, start audit",
        description: "Begin auditing selected categories"
      },
      {
        label: "No, cancel",
        description: "Cancel and return to category selection"
      }
    ]
  }]
})
```

3. **Use TodoWrite** to track audit progress per category

4. **Launch Task tool** with `cco-agent-audit`:
```python
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: """
  Run security audit using:
  - cco-skill-security-owasp-xss-sqli-csrf
  - cco-skill-ai-security-promptinjection-models
  - cco-skill-supply-chain-dependencies-sast

  Check for:
  - SQL injection (grep for string concatenation in queries)
  - XSS vulnerabilities (unescaped template variables)
  - Hardcoded secrets (API keys, passwords, tokens)
  - CSRF protection on forms
  - Authentication/authorization gaps
  - Dependency CVEs (check all dependencies)
  - AI prompt injection risks (if AI features exist)

  Return detailed report with:
  - Issue severity (Critical/High/Medium/Low)
  - File:line references
  - Explanation of risk
  - Recommended fix
  - Skill used for detection
  """
})
```

5. **Present results** with pain-point impact:
```markdown
Security Audit Results:

🔴 Critical (8):
1. SQL injection in api/users.py:45
   Skill: cco-skill-security-owasp
   Risk: Unauthorized data access
   Fix: Use parameterized query

2. AI prompt injection in api/chat.py:67
   Skill: cco-skill-ai-security-promptinjection
   Risk: User control of model behavior
   Fix: Add input sanitization + output validation

[... more issues ...]

🟡 High Priority (12):
- No CSRF tokens on 5 forms
- Missing input validation on 8 endpoints
- Weak password hashing (MD5 detected)

Impact:
- Addresses Pain #1 (51% security concern)
- Vulnerabilities found: 20 total
- Risk level: CRITICAL

➜ Next: /cco-fix --security (auto-fixes 15 issues)
```

6. **Recommend next action** with specific command

### Parametrized Mode (Power Users)

**Category Level (Original System):**
```bash
# Single category
/cco-audit --security

# Multiple categories
/cco-audit --security --tech-debt --tests

# All categories
/cco-audit --all
```

**Preset Level (Use-Case Based):**
```bash
# Quick presets
/cco-audit --preset=pre-commit
/cco-audit --preset=pre-deployment
/cco-audit --preset=performance
/cco-audit --preset=quality
/cco-audit --preset=testing
/cco-audit --preset=production
/cco-audit --preset=comprehensive
```

**Granular Level (Specific Checks):**
```bash
# Single check
/cco-audit --check=sql-injection

# Multiple checks
/cco-audit --check=sql-injection --check=xss --check=secrets

# Category group
/cco-audit --check-group=all-security
/cco-audit --check-group=all-database
```

**Examples:**
```bash
# Quick pre-commit check (2-3 min)
/cco-audit --preset=pre-commit

# Only check for SQL injection and N+1 queries
/cco-audit --check=sql-injection --check=n1-queries

# Pre-deployment security scan
/cco-audit --preset=pre-deployment

# All security checks only
/cco-audit --check-group=all-security

# Traditional category mode
/cco-audit --security --database --tests
```

Skip AskUserQuestion, run audit directly with specified parameters.

---

## Agent Usage

**Agent:** `cco-agent-audit` (Haiku for fast scanning, Sonnet for complex analysis)

**Model Selection by Category:**

**Haiku (Fast & Cheap - Pattern Matching):**
- `--integration` → Import errors, dependency conflicts
- `--supply-chain` → CVE scanning, dependency versions
- `--git` → Commit quality, branch naming patterns
- `--containers` → Dockerfile rule checks

**Sonnet (Accurate - Semantic Analysis):**
- `--security` → SQL injection, XSS, CSRF (context-aware)
- `--architecture` → Design patterns, coupling analysis
- `--tech-debt` → Dead code, complexity (semantic)
- `--ai-security` → Prompt injection detection
- `--performance` → Bottleneck identification
- `--database` → N+1 queries, query optimization

**Parallel Execution Pattern:**
```python
# Example: Security audit with parallel agents
# All scan tasks run in parallel, synthesis runs after

# Phase 1: Parallel scanning (Haiku - fast & cheap)
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Scan SQL injection patterns",
  prompt: "Grep for string concatenation in SQL queries..."
})
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Scan hardcoded secrets",
  prompt: "Search for API keys, passwords, tokens..."
})
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Check dependency CVEs",
  prompt: "Analyze package versions for known vulnerabilities..."
})

# Phase 2: Synthesis (Sonnet - accurate)
# Wait for all parallel tasks to complete, then:
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Synthesize audit findings",
  prompt: "Analyze all findings, calculate severity, generate report..."
})

# Total time: ~5s (vs 15s sequential)
# Total cost: $0.30 (vs $1.50 all Sonnet)
```

---

## Smart Detection

- **No database?** Skip database/migrations audit
- **No AI features?** Skip AI security audit
- **No tests?** Report as critical gap
- **No Docker?** Skip container audit
- **No CI/CD?** Skip CI/CD audit

Before running audit, check if components exist using Glob/Grep.

---

## Output Requirements

For each issue found:
- **Severity:** 🔴 Critical / 🟡 High / 🟢 Medium / ⚪ Low
- **Location:** file_path:line_number
- **Skill Used:** Which skill detected it
- **Risk:** What could go wrong
- **Fix:** Specific recommendation
- **Pain Point:** Which pain point it addresses

Final summary:
- Total issues by severity
- Pain points addressed
- Recommended next command
- Impact estimate (time saved, risk reduced)

---

## Success Criteria

- [OK] User selected categories (interactive or parametrized)
- [OK] Appropriate skills activated for each category
- [OK] Agent executed with Haiku model
- [OK] All issues reported with file:line references
- [OK] Pain-point impact communicated
- [OK] Next action recommended
- [OK] Results saved for /cco-fix to use
