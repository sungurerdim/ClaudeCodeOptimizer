---
name: cco-generate
description: Create missing project components with skill-guided generation
action_type: generate
parameters:
  tests:
    keywords: [unit tests, integration tests, coverage, pytest, test fixtures, untested functions]
    category: testing
    pain_points: [4]
  contract-tests:
    keywords: [contract tests, pact, consumer contracts, provider verification, api contracts]
    category: testing
    pain_points: [4]
  load-tests:
    keywords: [load tests, performance tests, stress tests, locust, k6]
    category: testing
    pain_points: [5]
  chaos-tests:
    keywords: [chaos tests, resilience tests, failure injection, chaos engineering]
    category: testing
    pain_points: [5]
  openapi:
    keywords: [openapi, swagger, api documentation, api spec, rest api docs]
    category: docs
    pain_points: [7]
  cicd:
    keywords: [cicd, pipeline, github actions, gitlab ci, deployment, quality gates]
    category: infrastructure
    pain_points: [6]
  docs:
    keywords: [documentation, docstrings, readme, code docs, usage examples]
    category: docs
    pain_points: [7]
  adr:
    keywords: [adr, architecture decision records, design decisions, technical decisions]
    category: docs
    pain_points: [7]
  runbook:
    keywords: [runbook, operational docs, incident response, deployment procedures]
    category: docs
    pain_points: [7]
  dockerfile:
    keywords: [dockerfile, docker, containerization, docker-compose, multi-stage build]
    category: infrastructure
    pain_points: [6]
  migration:
    keywords: [migration, database migration, schema migration, rollback, backup]
    category: database
    pain_points: [5]
  indexes:
    keywords: [indexes, database indexes, slow queries, query optimization]
    category: database
    pain_points: [5]
  monitoring:
    keywords: [monitoring, prometheus, grafana, dashboards, metrics]
    category: observability
    pain_points: [5]
  logging:
    keywords: [logging, structured logging, correlation ids, log config]
    category: observability
    pain_points: [5]
  slo:
    keywords: [slo, sla, service level objectives, alerts, error budgets]
    category: observability
    pain_points: [5]
  pre-commit:
    keywords: [pre-commit, git hooks, linting, formatting, code quality]
    category: infrastructure
    pain_points: [6]
  requirements:
    keywords: [requirements, dependencies, pyproject.toml, package.json]
    category: infrastructure
    pain_points: [6]
  review-checklist:
    keywords: [review checklist, pr checklist, code review guide, review template, merge checklist]
    category: docs
    pain_points: [11, 12]
---

# cco-generate

**Create missing project components with skill-guided generation.**

---

## Purpose

Generate missing tests, documentation, CI/CD configs, and other project components using specialized skills and the generate agent.

---

## Critical UX Principles

1. **100% Honesty** - Only claim "generated" if file actually created and verified
2. **Complete Accounting** - Report: generated + skipped + failed = total requested
3. **No Hardcoded Examples** - All examples use `{PLACEHOLDERS}`, never fake paths/names
4. **Phase Tracking** - Explicit start/end for each generation phase
5. **Consistent Counts** - Same counts shown everywhere (single source of truth)

### Generation Outcome Categories

```python
OUTCOMES = {
    "generated": "File created and verified",
    "skipped_exists": "File already exists - not overwritten",
    "skipped_conflict": "Would conflict with existing code",
    "needs_decision": "Multiple valid patterns - user must choose",
    "failed_deps": "Missing dependencies required first",
    "failed_template": "No suitable template for this context",
}
```

---

## Generation Types

### 🔴 Critical Missing (Pain #4: Biggest mistake)

1. **--tests** - Unit + integration tests
   - Skill: `cco-skill-test-pyramid-coverage-isolation`
   - Generates: Unit tests for untested functions, integration tests for APIs, fixtures

2. **--contract-tests** - API contract tests (Pact)
   - Skill: `cco-skill-api-testing-contract-load-chaos`
   - Generates: Consumer contracts, provider verification

### 🟡 High Priority

3. **--load-tests** - Performance/stress tests
   - Skill: `cco-skill-api-testing-contract-load-chaos`
   - Generates: Locust/k6 load tests, stress scenarios

4. **--chaos-tests** - Resilience tests
   - Skill: `cco-skill-api-testing-contract-load-chaos`
   - Generates: Chaos engineering tests (failure injection)

5. **--openapi** - OpenAPI/Swagger spec (Pain #7)
   - Skill: `cco-skill-docs-api-openapi-adr-runbooks`
   - Generates: Complete OpenAPI 3.0 spec from code

6. **--cicd** - CI/CD pipeline
   - Skill: `cco-skill-cicd-gates-deployment-automation`
   - Generates: GitHub Actions/GitLab CI with quality gates

### 🟢 Recommended

7. **--docs** - Code documentation
   - Skill: `cco-skill-docs-api-openapi-adr-runbooks`
   - Generates: Docstrings, README sections, usage examples

8. **--adr** - Architecture Decision Records
   - Skill: `cco-skill-docs-api-openapi-adr-runbooks`
   - Generates: ADR templates, decision logs

9. **--runbook** - Operational runbooks
   - Skill: `cco-skill-docs-api-openapi-adr-runbooks`, `cco-skill-incident-oncall-postmortem-playbooks`
   - Generates: Incident response, deployment procedures

10. **--dockerfile** - Docker configuration
    - Skill: `cco-skill-kubernetes-security-containers`
    - Generates: Dockerfile (multi-stage), docker-compose.yml

11. **--migration** - Database migration scripts
    - Skill: `cco-skill-data-migrations-backup-versioning`
    - Generates: Migration scripts with rollback, backup procedures

12. **--indexes** - Database indexes
    - Skill: `cco-skill-database-optimization-caching-profiling`
    - Generates: Index creation scripts for slow queries

13. **--monitoring** - Monitoring configuration
    - Skill: `cco-skill-observability-metrics-alerts-slo`
    - Generates: Prometheus metrics, Grafana dashboards

14. **--logging** - Structured logging config
    - Skill: `cco-skill-logging-structured-correlation-tracing`
    - Generates: Logging setup with correlation IDs

15. **--slo** - SLO/SLA definitions
    - Skill: `cco-skill-observability-metrics-alerts-slo`
    - Generates: SLO specs, SLA templates, alert rules

16. **--pre-commit** - Pre-commit hooks
    - Skill: `cco-skill-cicd-gates-deployment-automation`
    - Generates: .pre-commit-config.yaml with linting, security

17. **--requirements** - Dependency files
    - Skill: `cco-skill-supply-chain-dependencies-sast`
    - Generates: requirements.txt/pyproject.toml from imports

18. **--review-checklist** - Code review checklist (Pain #11, #12)
    - Skill: `cco-skill-code-review-quality-ai-guidance`
    - Generates: AI-aware review checklist template, PR checklist with quality gates
    - **2025 Critical**: Addresses 27% decline in code review comments
    - Includes:
      - General review checklist (security, testing, performance)
      - AI-specific checks (hallucination detection, bloat prevention)
      - Context-specific checks (async patterns, resource cleanup)
      - Review quality metrics (comment density, reviewer diversity)

---

## Execution Protocol

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# Generate Command

**What I do:**
I create missing project components like tests, documentation, CI/CD configs, and infrastructure files based on what's missing in your project.

**How it works:**
1. I analyze your project to detect missing components
2. You select which components to generate (individual files or groups)
3. I generate selected files following your project conventions
4. I report what was created with file paths and line counts

**What you'll get:**
- Unit and integration tests (significantly increase coverage)
- API documentation (OpenAPI specs, Swagger UI)
- CI/CD pipelines (GitHub Actions with quality gates)
- Infrastructure files (Dockerfile, docker-compose, monitoring configs)
- Operational docs (runbooks, ADRs)

**Time estimate:** 5-20 minutes depending on what you select

**New files WILL be created** - all files follow project conventions and can be reviewed before committing.
```

**Then ask for confirmation using AskUserQuestion:**

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start generating missing components?",
    header: "Start Generate",
    multiSelect: false,
    options: [
      {
        label: "Yes, start generating",
        description: "Analyze project and generate missing components"
      },
      {
        label: "No, cancel",
        description: "Exit without creating any files"
      }
    ]
  }]
})
```

**CRITICAL:**
- If user selects "No, cancel" → EXIT immediately, do NOT proceed
- If user selects "Yes, start generating" → Continue to Step 0.5

---

### Step 0.5: Project Context Discovery (Optional)

**Ask user if they want project documentation analyzed for better generation alignment.**

```python
AskUserQuestion({
  questions: [{
    question: "Extract context from project documentation?",
    header: "Project Context",
    multiSelect: false,
    options: [
      {
        label: "Yes (recommended)",
        description: "Extract project style from README/CONTRIBUTING, generated code aligns with style"
      },
      {
        label: "No",
        description: "Generate code only (faster)"
      }
    ]
  }]
})
```

**If "Yes" selected:**

```python
# Extract project context via Haiku sub-agent
context_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Extract project context summary (MAX 200 tokens).
    Focus on: naming conventions, testing patterns, documentation style.

    Files to check: README.md, CONTRIBUTING.md, ARCHITECTURE.md

    Return: Purpose, Tech Stack, Conventions (naming, testing, doc style)
    """
})

# Use context when generating code
project_context = context_result
```

**Benefits:** Generated tests/docs follow project conventions and style.

---

### Interactive Mode (No Parameters)

1. **Detect what's missing** using Glob/Grep:
   - No `tests/` directory → Missing tests
   - No `openapi.yaml` → Missing API spec
   - No `.github/workflows/` → Missing CI/CD
   - No `Dockerfile` → Missing containerization
   - Coverage below threshold → Need more tests

2. **Analyze what's missing first**, then **present specific generation steps using AskUserQuestion**:

**IMPORTANT - Dynamic Generation Options Protocol:**
You MUST analyze the project BEFORE presenting options:
1. Detect what EXISTS (tests/, openapi.yaml, Dockerfile, etc.)
2. Detect what's MISSING (compare to ideal project structure)
3. For missing components, count specifics:
   - How many untested functions? (grep for function definitions, check for tests)
   - How many undocumented endpoints? (find endpoints, check for OpenAPI entries)
   - Which files need generation? (list actual file paths)
4. Generate options with REAL counts and ACTUAL file/function names
5. Skip options for components that already exist

**Example analysis template (DO NOT use verbatim):**
```python
# Analysis phase:
untested_functions = find_functions_without_tests()
undocumented_endpoints = find_endpoints_without_docs()
missing_configs = check_for_cicd_dockerfile_etc()

# Then generate options:
for func in untested_functions:
    option = {
        label: f"Unit tests for {func.file} ({len(func.functions)} functions)",
        description: f"(Tests, {func.estimate}) {', '.join(func.functions[:3])}... | 🔴 CRITICAL"
    }
```

**IMPORTANT - Tab-Based Selection (Single Submit):**
AskUserQuestion supports **4 questions maximum** with **4 options maximum per question**. Group generation types by category to ensure ALL options are presented:

```python
# Analyze project first, then present tab-based selection
# Count missing components per category from REAL analysis

AskUserQuestion({
  questions: [
    {
      question: "Select Testing components to generate:",
      header: "🔴 Testing",
      multiSelect: true,
      options: [
        {
          label: f"Unit + Integration ({test_file_count} files)",
          description: f"Untested functions, API tests, fixtures | {untested_count} functions | Pain #4"
        },
        {
          label: f"Contract Tests ({contract_count} endpoints)",
          description: "Pact contracts, provider verification, broker config"
        },
        {
          label: f"Load + Chaos ({perf_count} scenarios)",
          description: "Locust/k6 load tests, chaos engineering, failure injection"
        },
        {
          label: "All Testing",
          description: "Generate all testing components (unit, integration, contract, load, chaos)"
        }
      ]
    },
    {
      question: "Select Documentation components to generate:",
      header: "🟡 Docs",
      multiSelect: true,
      options: [
        {
          label: f"OpenAPI Spec ({endpoint_count} endpoints)",
          description: "Complete OpenAPI 3.0, Swagger UI, schemas, examples | Pain #7"
        },
        {
          label: f"Docs + ADR ({undoc_count} items)",
          description: "Docstrings, README sections, Architecture Decision Records"
        },
        {
          label: "Review Checklist (AI-aware)",
          description: "Code review checklist with AI hallucination checks | Pain #11, #12 | 🔴 2025 CRITICAL"
        },
        {
          label: "Runbooks + Requirements",
          description: "Operational runbooks, incident response, dependency files"
        },
        {
          label: "All Documentation",
          description: "Generate all documentation components"
        }
      ]
    },
    {
      question: "Select CI/CD & Container components:",
      header: "🟢 CI/CD",
      multiSelect: true,
      options: [
        {
          label: "CI/CD Pipeline",
          description: "GitHub Actions/GitLab CI with quality gates, parallel jobs"
        },
        {
          label: "Pre-commit Hooks",
          description: ".pre-commit-config.yaml with linting, security, formatting"
        },
        {
          label: "Dockerfile",
          description: "Multi-stage build, docker-compose, .dockerignore, health checks"
        },
        {
          label: "All CI/CD & Containers",
          description: "Generate all CI/CD and container components"
        }
      ]
    },
    {
      question: "Select Database & Observability components:",
      header: "🟢 Ops",
      multiSelect: true,
      options: [
        {
          label: f"Migration + Indexes ({db_issue_count} items)",
          description: "Migration scripts with rollback, index creation for slow queries"
        },
        {
          label: "Monitoring + SLO",
          description: "Prometheus metrics, Grafana dashboards, SLO specs, alerts"
        },
        {
          label: "Logging",
          description: "Structured logging config with correlation IDs, tracing"
        },
        {
          label: "All Components",
          description: "✅ Generate ALL components across all categories (comprehensive setup)"
        }
      ]
    }
  ]
})
```

**Note about groupings:** Due to 4×4=16 slot limit with 17 generation types, these related items are grouped:
- **Load + Chaos** (both performance/resilience testing)
- **Docs + ADR** (both code documentation)
- **Runbooks + Requirements** (both operational documentation)
- **Migration + Indexes** (both database operations)
- **Monitoring + SLO** (both observability/alerting)

### Selection Processing

**After user submits, calculate and display selection summary:**

```markdown
## Generation Selection Summary

**Your selections:**
- 🔴 Testing: [list selected] → [component count] components
- 🟡 Docs: [list selected] → [component count] components
- 🟢 CI/CD: [list selected] → [component count] components
- 🟢 Ops: [list selected] → [component count] components

**Total: {{SELECTED_COUNT}} generation tasks selected**

⚠️ Only selected categories will be generated.
Categories NOT selected will be skipped entirely.
```

**IMPORTANT:**
- If user selects "All Components", ignore other selections and generate ALL
- If user selects "All [Category]", generate all components in that category
- Otherwise, generate ONLY the individually selected items
- For grouped items (e.g., "Load + Chaos"), generate both components
- Components can be generated in parallel when they don't conflict

3. **Present generation plan:**

```markdown
Selected: [list selected components or "All Recommended"]

Skills I'll use:
- [list skills for selected components]

Agent: cco-agent-generate (Sonnet for quality generation)

I'll create:

[For each selected component, explain what will be generated]

Example for Tests:
- Unit tests for untested functions
- Integration tests for API endpoints
- Test fixtures for database models
- Estimated: significant lines of test code
- Coverage: significantly increased (target: high coverage)

Time estimate: ~[X] minutes
Files to create: ~[Y] files
```

4. **Confirm generation** using AskUserQuestion:

```python
AskUserQuestion({
  questions: [{
    question: "Ready to generate the selected components?",
    header: "Confirm",
    multiSelect: false,
    options: [
      {
        label: "Yes, start generation",
        description: "Generate all selected components"
      },
      {
        label: "No, cancel",
        description: "Cancel and return to component selection"
      }
    ]
  }]
})
```

5. **Use TodoWrite** to track generation progress

5. **Launch Task with cco-agent-generate**:

```python
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate tests and documentation",
  prompt: """
  Generate missing tests, contract tests, and OpenAPI spec.

  Use these skills:
  - cco-skill-test-pyramid-coverage-isolation
  - cco-skill-api-testing-contract-load-chaos
  - cco-skill-docs-api-openapi-adr-runbooks

  TESTS:
  1. Analyze all Python files in src/ to find untested functions
  2. For each untested function:
     - Generate unit test with edge cases
     - Follow test pyramid (unit >> integration >> e2e)
     - Use pytest conventions
     - Include fixtures for dependencies
     - Target high coverage

  3. For each API endpoint:
     - Generate integration test
     - Test happy path + error cases
     - Test authentication/authorization
     - Test input validation

  CONTRACT TESTS:
  1. For each API endpoint, generate Pact contract
  2. Include request/response examples
  3. Generate provider verification tests
  4. Setup contract broker config

  OPENAPI:
  1. Analyze all API endpoints (Flask routes, FastAPI paths)
  2. Generate complete OpenAPI 3.0 spec
  3. Include schemas for all request/response types
  4. Document authentication (JWT, API keys)
  5. Add examples for each endpoint
  6. Setup Swagger UI integration

  Follow:
  - P_TEST_PYRAMID (unit >> integration >> e2e)
  - P_TEST_COVERAGE (high coverage target)
  - P_API_DOCUMENTATION_OPENAPI (complete spec)
  - U_NO_OVERENGINEERING (keep it simple)

  Report:
  - Files created with line counts
  - Coverage improvement estimate
  - How to run tests
  - How to view docs
  """
})
```

6. **Present results:**

**IMPORTANT - Dynamic Results Generation:**
Report ACTUAL files created and metrics. Use this template with REAL data:

```markdown
Generation Complete! ✓

[For each category generated, report REAL files:]
Tests Created:
✓ tests/unit/ ([ACTUAL_COUNT] test files, [ACTUAL_TEST_COUNT]+ unit tests)
  [List first 3-5 actual files created with real test counts]
  - ... ([remaining_count] more files)

✓ tests/integration/ ([ACTUAL_COUNT] API integration tests)
  [List actual integration test files created]

✓ tests/fixtures.py (database fixtures) [if created]
✓ tests/conftest.py (pytest configuration) [if created]

Coverage: [BEFORE]% → [AFTER]% ✓ (Target: high coverage)
Total tests: [ACTUAL_COUNT] tests created

[Repeat for other categories that were actually generated]

Impact:
- Addresses Pain #[X] ([PAIN_DESCRIPTION])
- Testing score: [BEFORE] → [AFTER] (+[DELTA] points)
- Documentation score: [BEFORE] → [AFTER] (+[DELTA] points)
- [Other actual improvements]

Next Steps:
1. Run tests: [actual test command for this project]
2. View coverage: [actual coverage command]
3. [Other actual next steps based on what was generated]
4. Commit changes: /cco-commit
```

**Never use placeholder examples - only report what was actually generated.**

### Parametrized Mode (Power Users)

```bash
# Single type
/cco-generate --tests

# Multiple types
/cco-generate --tests --openapi --cicd

# All recommended
/cco-generate --all
```

---

## Agent Usage

**Agent:** `cco-agent-generate` (Sonnet for code generation)

**Parallel Execution Pattern:**
```python
# Example: Generating multiple independent components in parallel

# All generate tasks run simultaneously (independent files)
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate unit tests for auth module",
  prompt: "Analyze auth.py and generate comprehensive unit tests..."
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate integration tests for API",
  prompt: "Analyze API endpoints and generate integration tests..."
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate OpenAPI spec",
  prompt: "Analyze all routes and generate OpenAPI 3.0 specification..."
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate CI/CD config",
  prompt: "Generate GitHub Actions workflow with tests and quality gates..."
})

# All run in parallel since outputs are independent
# Total time: significantly faster than sequential
# All use Sonnet for quality generation
```

**Why Sonnet:**
- Code generation requires accuracy
- Better understanding of project context
- Generates higher quality tests/docs
- Worth the cost for quality output

---

## Generation Best Practices

### Tests
- Follow test pyramid (unit >> integration >> e2e)
- Edge cases and error conditions
- Use fixtures for dependencies
- Descriptive test names
- Target high coverage

### Documentation
- Clear examples for every endpoint
- Authentication/security details
- Error codes and meanings
- Rate limiting information

### CI/CD
- Quality gates (linting, tests, security)
- Fail fast on issues
- Parallel execution where possible
- Deployment strategy (staging → production)

### Containerization
- Multi-stage builds (small images)
- Non-root user
- Security scanning
- Health checks

---

## Smart Detection

Before generation:
- **Check existing files** (don't overwrite)
- **Detect framework** (Flask vs FastAPI vs Django)
- **Check dependencies** (can we add pytest/Pact?)
- **Verify structure** (where should files go?)

Warn user if:
- Files already exist (offer to merge/skip)
- Dependencies missing (offer to add)
- Framework not recognized (ask for guidance)

---

## Success Criteria

- [OK] Missing components detected
- [OK] User selected what to generate
- [OK] Appropriate skills used
- [OK] cco-agent-generate executed with Sonnet
- [OK] Files created in correct locations
- [OK] Files follow framework conventions
- [OK] Quality verified (tests pass, specs valid)
- [OK] Impact summary presented
- [OK] Next steps provided
- [OK] Pain-point impact communicated

---

## Example Usage

```bash
# Generate missing tests
/cco-generate --tests

# Generate API documentation
/cco-generate --openapi --docs

# Setup CI/CD with quality gates
/cco-generate --cicd --pre-commit

# Full setup for new project
/cco-generate --tests --openapi --cicd --dockerfile --monitoring
```

---

## Integration with Other Commands

- **After /cco-audit --tests**: Generate missing tests
- **After /cco-audit --quick**: Follow action plan
- **With /cco-fix**: Fix existing, generate missing
- **Before /cco-commit**: Generate then commit
