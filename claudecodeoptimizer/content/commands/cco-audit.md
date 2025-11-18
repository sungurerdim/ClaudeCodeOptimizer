# cco-audit

**Comprehensive issue detection across {{CATEGORY_COUNT}} categories, pain-point priority ordered.**

---

## Dynamic Value Calculation (CRITICAL)

**ALL placeholder values MUST be calculated at runtime. NEVER use hardcoded numbers.**

### Required Calculations

```bash
# Calculate these BEFORE presenting any information to user
CATEGORY_COUNT=$(grep -c "^\d\+\. \*\*--" ~/.claude/commands/cco-audit.md)
SKILL_COUNT=$(ls ~/.claude/skills/cco-skill-*.md 2>/dev/null | wc -l)
GRANULAR_CHECK_COUNT=# Sum checks from all categories (Security:15 + Database:10 + Tests:12 + ...)
```

### Placeholder Reference

| Placeholder | Calculation | Example |
|-------------|-------------|---------|
| `{{CATEGORY_COUNT}}` | Count numbered items in "Audit Categories" section | - |
| `{{SKILL_COUNT}}` | Count files in skills/ directory | - |
| `{{GRANULAR_CHECK_COUNT}}` | Sum all individual checks | - |
| `{{SELECTED_COUNT}}` | Count user's selections at runtime | - |
| `{{CHECK_COUNT}}` | Calculate checks for selected categories | - |

**IMPORTANT:** When displaying counts, always calculate from actual data. Never copy example numbers.

---

## Purpose

Find security vulnerabilities, technical debt, testing gaps, and other issues using specialized skills and parallel agent execution.

---

## Audit Categories (Pain-Point Priority Order)

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
I scan your codebase for issues across {{CATEGORY_COUNT}} categories including security vulnerabilities, technical debt, testing gaps, and performance problems.

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
        description: "Choose from {{CATEGORY_COUNT}} categories (Security, Tests, Database, etc.) - Balanced approach"
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
        description: "📋 COMPREHENSIVE (20-30 min) - All {{CATEGORY_COUNT}} categories, complete scan | Weekly/monthly review"
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
- All {{CATEGORY_COUNT}} categories
```

---

### Level 2: Category Level (Tab-Based Selection)

**Multi-tab single-submit interface using maximum options per question.**

AskUserQuestion supports **4 questions maximum** with **4 options maximum per question**. This structure provides:
- All categories visible in one interface (tabs)
- Single submit for all selections
- "All [group]" option in each tab
- Dynamic selection count summary

```python
AskUserQuestion({
  questions: [
    {
      question: "Select Critical Impact categories:",
      header: "🔴 Critical",
      multiSelect: true,
      options: [
        {
          label: "Security",
          description: "OWASP vulnerabilities, CVEs, secrets, auth/authz | Pain #1"
        },
        {
          label: "Tech Debt",
          description: "Dead code, complexity, duplication, anti-patterns | Pain #2"
        },
        {
          label: "AI Security",
          description: "Prompt injection, hallucinations, output validation | Pain #3"
        },
        {
          label: "All Critical",
          description: "Select all Critical categories above"
        }
      ]
    },
    {
      question: "Select High Impact categories:",
      header: "🟡 High",
      multiSelect: true,
      options: [
        {
          label: "Tests",
          description: "Coverage, pyramid, isolation, edge cases | Pain #4"
        },
        {
          label: "Integration",
          description: "Dependencies, imports, conflicts | Pain #6"
        },
        {
          label: "Code Quality",
          description: "Syntax errors, logic bugs, type errors, error handling"
        },
        {
          label: "Docs",
          description: "README, API docs, docstrings, ADRs | Pain #7"
        }
      ]
    },
    {
      question: "Select Medium Impact categories (Data & Operations):",
      header: "🟢 Data/Ops",
      multiSelect: true,
      options: [
        {
          label: "Database",
          description: "N+1 queries, indexes, connection pooling | Pain #5"
        },
        {
          label: "Observability",
          description: "Structured logging, correlation IDs, metrics"
        },
        {
          label: "Monitoring",
          description: "Dashboards, alerts, Prometheus/Grafana"
        },
        {
          label: "CI/CD",
          description: "Pipeline, quality gates, deployment | Pain #6"
        }
      ]
    },
    {
      question: "Select Medium Impact categories (Infrastructure):",
      header: "🟢 Infra",
      multiSelect: true,
      options: [
        {
          label: "Containers + Supply Chain",
          description: "Dockerfile, CVEs, licenses, SBOM, dependencies"
        },
        {
          label: "Migrations",
          description: "Strategy, rollback, consistency, backups"
        },
        {
          label: "Performance",
          description: "Response times, caching, bundle size | Pain #5"
        },
        {
          label: "Architecture + Git",
          description: "Patterns, coupling, versioning, branching | Pain #5"
        }
      ]
    }
  ]
})
```

**Note:** Due to 4×4=16 slot limit, these related categories are grouped:
- **Containers + Supply Chain** (both relate to deployment/dependency security)
- **Architecture + Git** (both relate to code organization/workflow)

### Selection Processing

**After user submits, calculate and display selection summary:**

```markdown
## Selection Summary

**Your selections:**
- 🔴 Critical: [list selected]
- 🟡 High: [list selected]
- 🟢 Data/Ops: [list selected]
- 🟢 Infra: [list selected]

**Total: {{SELECTED_COUNT}} categories selected → {{CHECK_COUNT}} checks will be performed**

⚠️ Only selected categories will be audited.
Categories NOT selected will be skipped entirely.
```

### Selection Processing Logic

When processing selections:

```python
# Expand selections to individual categories
selected_categories = []

# Critical tab
if "All Critical" in critical_selections:
    selected_categories.extend(["security", "tech-debt", "ai-security"])
else:
    if "Security" in critical_selections:
        selected_categories.append("security")
    if "Tech Debt" in critical_selections:
        selected_categories.append("tech-debt")
    if "AI Security" in critical_selections:
        selected_categories.append("ai-security")

# High tab (all individual)
if "Tests" in high_selections:
    selected_categories.append("tests")
if "Integration" in high_selections:
    selected_categories.append("integration")
if "Code Quality" in high_selections:
    selected_categories.append("code-quality")
if "Docs" in high_selections:
    selected_categories.append("docs")

# Data/Ops tab (all individual)
if "Database" in data_ops_selections:
    selected_categories.append("database")
if "Observability" in data_ops_selections:
    selected_categories.append("observability")
if "Monitoring" in data_ops_selections:
    selected_categories.append("monitoring")
if "CI/CD" in data_ops_selections:
    selected_categories.append("cicd")

# Infra tab (2 grouped pairs due to slot limit)
if "Containers + Supply Chain" in infra_selections:
    selected_categories.extend(["containers", "supply-chain"])
if "Migrations" in infra_selections:
    selected_categories.append("migrations")
if "Performance" in infra_selections:
    selected_categories.append("performance")
if "Architecture + Git" in infra_selections:
    selected_categories.extend(["architecture", "git"])

# Calculate check count dynamically from actual checks in each category
total_checks = sum(get_check_count(cat) for cat in selected_categories)
```

### Execution Filter (CRITICAL)

**ONLY audit selected categories. Never run unselected categories:**

```python
# Example: User selected only Security and Tests
selected_categories = ["security", "tests"]

# Launch ONLY these agents
for category in selected_categories:
    Task({
        subagent_type: "general-purpose",
        model: "haiku",
        prompt: f"Audit {category} category using relevant skills..."
    })

# CI/CD was NOT selected - NO CI/CD checks will run
# Database was NOT selected - NO database checks will run
```

**IMPORTANT:** If no categories are selected, prompt user to select at least one category.

---

### Level 3: Granular Level (Specific Checks)

**If user selected "Granular Level", use hierarchical selection to stay within 4-option limit:**

**IMPORTANT - Hierarchical Approach (Required for 4-Option Limit):**
Since AskUserQuestion has a **maximum of 4 options per question**, the granular checks MUST be presented in 2 stages:

**Stage 1:** Select check CATEGORIES (9 categories → 3 questions with 3-4 options each)
**Stage 2:** For each selected category, select individual checks (max 15 per category → paginated if needed)

**Tech Stack Detection (Required First):**
```python
# Analyze project to determine applicable checks
detected_tech = {
    "languages": [],      # python, javascript, java, go, etc.
    "frameworks": [],     # flask, fastapi, django, react, vue, etc.
    "databases": [],      # postgresql, mysql, mongodb, redis, etc.
    "platforms": [],      # web, mobile, api, desktop, etc.
    "tools": []           # docker, kubernetes, ci/cd, etc.
}

# Detection using Glob/Grep
Glob("**/*.py") → Add "python" to languages
Glob("**/requirements.txt") → Check for flask, django, fastapi
Glob("**/package.json") → Add "javascript", check dependencies
Glob("**/Dockerfile") → Add "docker" to tools
Glob("**/*.sql") → Add "sql" to databases
Grep("SELECT|INSERT|UPDATE", output_mode="files_with_matches") → SQL usage
```

---

## 📋 Complete Granular Audit Checklist

**This is the MASTER LIST organized into 9 categories for hierarchical selection.**

### Stage 1: Select Check Categories

```python
# FIRST detect tech stack
detected_tech = analyze_project()
applicable_counts = count_applicable_checks_per_category(detected_tech)

# THEN present CATEGORIES in groups of 3-4 (respecting 4-option limit)
# Question 1: Critical categories
AskUserQuestion({
  questions: [{
    question: "Which check categories do you want? (Page 1/3 - Critical Impact):",
    header: "Categories",
    multiSelect: true,
    options: [
      {
        label: "Security Checks",
        description: f"🔴 CRITICAL - {applicable_counts['security']}/15 applicable checks (SQL injection, XSS, CSRF, secrets, CVEs)"
      },
      {
        label: "Database Checks",
        description: f"🔴 CRITICAL - {applicable_counts['database']}/10 applicable checks (N+1, indexes, slow queries)"
      },
      {
        label: "Test Checks",
        description: f"🔴 CRITICAL - {applicable_counts['tests']}/12 applicable checks (coverage, isolation, pyramid)"
      },
      {
        label: "More categories...",
        description: "Continue to page 2 for more categories"
      }
    ]
  }]
})

# Question 2: High priority categories
AskUserQuestion({
  questions: [{
    question: "Which check categories do you want? (Page 2/3 - High Priority):",
    header: "Categories",
    multiSelect: true,
    options: [
      {
        label: "Code Quality Checks",
        description: f"🟡 HIGH - {applicable_counts['quality']}/15 applicable checks (dead code, complexity, linting)"
      },
      {
        label: "Performance Checks",
        description: f"🟡 HIGH - {applicable_counts['performance']}/10 applicable checks (caching, algorithms, memory)"
      },
      {
        label: "CI/CD Checks",
        description: f"🟡 HIGH - {applicable_counts['cicd']}/8 applicable checks (pipeline, gates, automation)"
      },
      {
        label: "More categories...",
        description: "Continue to page 3 for more categories"
      }
    ]
  }]
})

# Question 3: Medium priority + All option
AskUserQuestion({
  questions: [{
    question: "Which check categories do you want? (Page 3/3 - Medium Priority):",
    header: "Categories",
    multiSelect: true,
    options: [
      {
        label: "Documentation Checks",
        description: f"🟢 MEDIUM - {applicable_counts['docs']}/8 applicable checks (docstrings, API docs, README)"
      },
      {
        label: "Container Checks",
        description: f"🟢 MEDIUM - {applicable_counts['containers']}/6 applicable checks (Dockerfile, non-root, size)"
      },
      {
        label: "Tech Debt Checks",
        description: f"🟢 MEDIUM - {applicable_counts['debt']}/8 applicable checks (deprecated APIs, coupling)"
      },
      {
        label: "All Granular Checks",
        description: "✅ Run ALL checks across all categories"
      }
    ]
  }]
})
```

### Stage 2: Select Individual Checks per Category

**For each selected category, present individual checks (paginated if >4):**

```python
# Example: If user selected "Security Checks"
# Show applicable checks from that category
security_checks = get_applicable_checks("security", detected_tech)

# If <= 4 checks, show in one question
# If > 4 checks, paginate (3 checks + "More...")
AskUserQuestion({
  questions: [{
    question: f"Which Security checks to run? ({len(security_checks)} applicable):",
    header: "Security",
    multiSelect: true,
    options: generate_paginated_options(security_checks)
    # Options generated dynamically with REAL applicability from tech stack detection
  }]
})
```

---

## 📋 Check Reference by Category

**Security:** SQL injection, XSS, CSRF, hardcoded secrets, authentication, authorization, CVE scan, AI prompt injection, SSRF, XXE, path traversal, command injection, insecure deserialization, weak crypto, security headers

**Database:** N+1 queries, missing indexes, slow queries, connection pooling, query optimization, transaction isolation, deadlock detection, migration consistency, raw SQL usage, database credentials

**Tests:** Coverage analysis, untested functions, test isolation, test pyramid, edge cases, flaky tests, test naming, assertion quality, mock overuse, test data management, integration coverage, e2e coverage

**Code Quality:** Dead code, complexity, duplication, type errors, linting, code smells, long functions, long files, deep nesting, magic numbers, TODO comments, commented code, import organization, naming conventions, error handling

**Performance:** Slow queries, large bundles, no caching, circuit breakers, memory leaks, inefficient algorithms, large loops, file I/O, network calls in loops, lazy loading

**Documentation:** Missing docstrings, API documentation, README completeness, documentation drift, code comments, examples, ADRs, runbooks

**CI/CD:** Pipeline existence, quality gates, secret management, build optimization, test automation, deployment automation, rollback strategy, environment parity

**Containers:** Dockerfile best practices, multi-stage builds, non-root user, image size, base image vulnerabilities, layer optimization

**Tech Debt:** Deprecated APIs, legacy code, hard dependencies, tight coupling, god objects, feature envy, data clumps, shotgun surgery

---

## 📝 Applicability Detection Rules

**Dynamic detection - mark checks as applicable based on project analysis:**

```python
# Security checks applicability
"SQL Injection" → applicable if: databases detected OR Grep("execute|query") finds results
"XSS" → applicable if: Glob("**/templates/**") OR Grep("render_template|innerHTML")
"CSRF" → applicable if: Grep("<form") OR web framework detected
"Hardcoded secrets" → applicable if: ALWAYS (all projects)
"AI prompt injection" → applicable if: Grep("openai|anthropic|langchain")

# Database checks applicability
"N+1 queries" → applicable if: ORM imports detected (SQLAlchemy, Django ORM)
"Missing indexes" → applicable if: database detected
"Connection pooling" → applicable if: database connection code found

# Test checks applicability
"Test coverage" → applicable if: tests/ directory found
"Untested functions" → applicable if: ALWAYS

# And so on for all checks...
```

---

## 📝 Implementation Instructions for Level 3

**CRITICAL - Hierarchical Selection Protocol:**

1. **Tech Stack Detection (MUST DO FIRST):**
   - Use Glob/Grep to detect languages, frameworks, databases, tools
   - Count applicable checks per category based on detection

2. **Stage 1 - Category Selection:**
   - Present 9 categories across 3 questions (3-4 options each)
   - Include "All Granular Checks" option on last page

3. **Stage 2 - Individual Check Selection:**
   - For each selected category, present individual checks
   - Paginate if category has >4 applicable checks (3 checks + "More...")
   - Generate descriptions dynamically with REAL applicability data

4. **Execution:**
   - Run only selected checks
   - If "All Granular Checks" selected, run everything
   - If category group selected, run all checks in that category

**Example: User selects "Security Checks" category**
→ Show 15 security checks paginated (4 pages × 3-4 options)
→ Each option shows real applicability from project analysis
→ User selects specific checks or "All Security Checks"

---

### Common Step for All Levels

2. **Present analysis plan and confirm** using AskUserQuestion:
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
        label: "Show All Checks",
        description: "📋 Display ALL checks (including non-applicable ones marked with ⚪)"
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
        description: "✅ RUN ALL CHECKS - Comprehensive granular audit (ignores other selections)"
      }
    ]
  }]
})
```

**Summary of Granular Checks:**
- Security: [count from list above]
- Database: [count from list above]
- Tests: [count from list above]
- Code Quality: [count from list above]
- Performance: [count from list above]
- Documentation: [count from list above]
- CI/CD: [count from list above]
- Containers: [count from list above]
- Tech Debt: [count from list above]

**Total: {{GRANULAR_CHECK_COUNT}} checks** (calculate by summing all category checks above)

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
   - For each check, determine if applicable based on detected_tech
   - Mark with ✅ APPLICABLE or ⚪ NOT APPLICABLE
   - Update description with specific reason

3. **Filtering Options:**
   - Default: Show only applicable checks (recommended)
   - Optional: "Show All Checks" to see everything

4. **User Selection:**
   - Individual checks: Run ONLY selected
   - Category group (e.g., "All Security Checks"): Run all in that category
   - "All Granular Checks": Run ALL checks

**IMPORTANT:**
- If user selects "All Granular Checks", run ALL checks
- If user selects "All [Category] Checks", run all checks in that category
- Otherwise, run ONLY the individually selected checks
- Show real data in descriptions (e.g., "Found 23 functions without tests")

---

### Common Step for All Levels

2. **Present analysis plan and confirm** using AskUserQuestion:

```markdown
Selected categories: [list selected categories or "All {{CATEGORY_COUNT}} categories"]

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

**IMPORTANT - Dynamic Results Generation:**
Generate results from ACTUAL audit findings. Use this template structure but fill with REAL data:

```markdown
[Category] Audit Results:

🔴 Critical ([REAL_COUNT]):
1. [REAL_ISSUE_TYPE] in <file>:<line>
   Skill: [ACTUAL_SKILL_USED]
   Risk: [REAL_RISK_DESCRIPTION]
   Fix: [SPECIFIC_FIX_FOR_THIS_CODE]

[... list ALL critical issues found ...]

🟡 High Priority ([REAL_COUNT]):
- [REAL_ISSUE_1] in <file>:<line>
- [REAL_ISSUE_2] in <file>:<line>
[... list ALL high priority issues ...]

🟢 Medium Priority ([REAL_COUNT]):
[... list ALL medium priority issues ...]

Impact:
- Addresses Pain #[X] ([PAIN_DESCRIPTION])
- Vulnerabilities found: [ACTUAL_TOTAL] total
- Risk level: [CALCULATED_RISK_LEVEL]

➜ Next: /cco-fix --[category] (auto-fixes [ACTUAL_AUTO_FIXABLE_COUNT] issues)
```

**Never use placeholder examples in actual results - only show what was really found.**

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
