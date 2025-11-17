# cco-generate

**Create missing project components with skill-guided generation.**

---

## Purpose

Generate missing tests, documentation, CI/CD configs, and other project components using specialized skills and the generate agent.

---

## 17 Generation Types

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
- Unit and integration tests (increase coverage from 45% → 80%+)
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
- If user selects "Yes, start generating" → Continue to Step 1

---

### Interactive Mode (No Parameters)

1. **Detect what's missing** using Glob/Grep:
   - No `tests/` directory → Missing tests
   - No `openapi.yaml` → Missing API spec
   - No `.github/workflows/` → Missing CI/CD
   - No `Dockerfile` → Missing containerization
   - Coverage < 80% → Need more tests

2. **Analyze what's missing first**, then **present specific generation steps using AskUserQuestion**:

**IMPORTANT:** The steps below are EXAMPLES. You MUST:
- Analyze actual project to detect missing components
- List EACH specific file/component to generate as a separate option
- Count real gaps (e.g., actual untested functions, actual endpoints without docs)
- Include actual file paths and function names
- Replace ALL example steps with REAL project-specific generation tasks
- Skip options for components that already exist

```python
AskUserQuestion({
  questions: [{
    question: "What should I generate? Select specific files/components you need:",
    header: "Generate",
    multiSelect: true,
    options: [
      # Tests - Each specific test file
      {
        label: "Unit tests for api/users.py (5 functions)",
        description: "(Tests, 3 min) test_get_user, test_create_user, test_update_user, test_delete_user, test_list_users | 🔴 CRITICAL"
      },
      {
        label: "Unit tests for services/auth.py (8 functions)",
        description: "(Tests, 4 min) test_hash_password, test_verify_password, test_create_token, test_validate_token, etc. | 🔴 CRITICAL"
      },
      {
        label: "Integration tests for /api/users endpoints",
        description: "(Tests, 3 min) test_user_crud_flow, test_user_auth, test_user_validation | 🔴 CRITICAL"
      },
      {
        label: "Integration tests for /api/posts endpoints",
        description: "(Tests, 3 min) test_post_crud_flow, test_post_ownership, test_post_pagination | 🔴 CRITICAL"
      },
      {
        label: "Test fixtures for User model",
        description: "(Tests, 2 min) user_factory, admin_user, regular_user fixtures | 🔴 CRITICAL"
      },
      {
        label: "Test fixtures for Post model",
        description: "(Tests, 2 min) post_factory, published_post, draft_post fixtures | 🔴 CRITICAL"
      },
      {
        label: "Generate conftest.py with pytest configuration",
        description: "(Tests, 2 min) Setup fixtures, database, test client | 🔴 CRITICAL"
      },

      # Contract Tests - Each endpoint
      {
        label: "Pact contract for POST /api/users",
        description: "(Contract Tests, 2 min) Consumer contract + provider verification | 🔴 CRITICAL"
      },
      {
        label: "Pact contract for GET /api/users/:id",
        description: "(Contract Tests, 2 min) Consumer contract + provider verification | 🔴 CRITICAL"
      },
      {
        label: "Pact contract for POST /api/auth/login",
        description: "(Contract Tests, 2 min) Consumer contract + provider verification | 🔴 CRITICAL"
      },

      # OpenAPI - Each component
      {
        label: "OpenAPI spec for /api/users endpoints",
        description: "(OpenAPI, 3 min) 5 endpoints with request/response schemas | 🟡 HIGH"
      },
      {
        label: "OpenAPI spec for /api/posts endpoints",
        description: "(OpenAPI, 3 min) 6 endpoints with request/response schemas | 🟡 HIGH"
      },
      {
        label: "OpenAPI spec for /api/auth endpoints",
        description: "(OpenAPI, 2 min) 3 endpoints with JWT authentication docs | 🟡 HIGH"
      },
      {
        label: "Setup Swagger UI integration",
        description: "(OpenAPI, 2 min) Add /docs endpoint with interactive UI | 🟡 HIGH"
      },

      # Load Tests - Each scenario
      {
        label: "Load test for user registration flow",
        description: "(Load Tests, 2 min) Locust scenario, 100 users/sec target | 🟡 HIGH"
      },
      {
        label: "Load test for authentication flow",
        description: "(Load Tests, 2 min) Locust scenario, login/refresh load | 🟡 HIGH"
      },

      # CI/CD - Each job
      {
        label: "Create .github/workflows/ci.yml",
        description: "(CI/CD, 3 min) GitHub Actions workflow file | 🟡 HIGH"
      },
      {
        label: "Add linting job (black, ruff, mypy)",
        description: "(CI/CD, 2 min) Code quality checks | 🟡 HIGH"
      },
      {
        label: "Add testing job (pytest with coverage)",
        description: "(CI/CD, 2 min) Run tests, generate coverage report | 🟡 HIGH"
      },
      {
        label: "Add security scanning job (bandit, safety)",
        description: "(CI/CD, 2 min) Vulnerability detection | 🟡 HIGH"
      },
      {
        label: "Add deployment job (staging + production)",
        description: "(CI/CD, 3 min) Deploy on merge to main | 🟡 HIGH"
      },

      # Monitoring - Each component
      {
        label: "Create Prometheus metrics endpoints",
        description: "(Monitoring, 3 min) /metrics endpoint with custom metrics | 🟢 RECOMMENDED"
      },
      {
        label: "Create Grafana dashboard JSON",
        description: "(Monitoring, 3 min) Dashboard for API metrics, errors, latency | 🟢 RECOMMENDED"
      },
      {
        label: "Create alert rules (Prometheus)",
        description: "(Monitoring, 2 min) Alerts for high error rate, slow queries | 🟢 RECOMMENDED"
      },

      # Logging
      {
        label: "Setup structured logging with correlation IDs",
        description: "(Logging, 3 min) JSON logging, request tracking | 🟢 RECOMMENDED"
      },

      # Migrations
      {
        label: "Create migration for adding indexes",
        description: "(Migrations, 2 min) Add 3 indexes with rollback | 🟢 RECOMMENDED"
      },

      # Dockerfile
      {
        label: "Create multi-stage Dockerfile",
        description: "(Docker, 3 min) Production-ready Dockerfile | 🟢 RECOMMENDED"
      },
      {
        label: "Create docker-compose.yml",
        description: "(Docker, 2 min) App + database + redis setup | 🟢 RECOMMENDED"
      },

      # Runbooks
      {
        label: "Create deployment runbook",
        description: "(Runbook, 2 min) Step-by-step deployment guide | 🟢 RECOMMENDED"
      },
      {
        label: "Create incident response runbook",
        description: "(Runbook, 2 min) How to handle production issues | 🟢 RECOMMENDED"
      },

      # Pre-commit
      {
        label: "Create .pre-commit-config.yaml",
        description: "(Pre-commit, 2 min) Black, ruff, mypy, bandit hooks | 🟢 RECOMMENDED"
      },

      # Group options
      {
        label: "All Unit Tests",
        description: "✅ Generate all unit tests above (tests for all untested functions)"
      },
      {
        label: "All Integration Tests",
        description: "✅ Generate all integration tests above (tests for all endpoints)"
      },
      {
        label: "All Test Components",
        description: "✅ Generate unit tests + integration tests + fixtures + conftest | Pain #4"
      },
      {
        label: "All Contract Tests",
        description: "✅ Generate all Pact contracts above"
      },
      {
        label: "All OpenAPI Components",
        description: "✅ Generate complete OpenAPI spec + Swagger UI | Pain #7"
      },
      {
        label: "All CI/CD Components",
        description: "✅ Generate complete CI/CD pipeline | Pain #6"
      },
      {
        label: "All Monitoring Components",
        description: "✅ Generate Prometheus + Grafana + Alerts | Pain #5"
      },
      {
        label: "All Docker Components",
        description: "✅ Generate Dockerfile + docker-compose"
      },
      {
        label: "All Components",
        description: "✅ Generate ALL components above (comprehensive project setup)"
      }
    ]
  }]
})
```

**IMPORTANT:**
- If user selects "All Components", ignore other selections and generate ALL
- If user selects "All [Category] Components", generate all in that category
- Otherwise, generate ONLY the individually selected items
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
- Unit tests for 45 untested functions
- Integration tests for 15 API endpoints
- Test fixtures for 3 database models
- Estimated: 500+ lines of test code
- Coverage: 45% → 80%+ (target: 85%)

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
     - Target 80%+ coverage

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
  - P_TEST_COVERAGE (80%+ target)
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

```markdown
Generation Complete! ✓

Tests Created:
✓ tests/unit/ (45 test files, 200+ unit tests)
  - test_api_users.py (15 tests)
  - test_api_posts.py (12 tests)
  - test_services_auth.py (20 tests)
  - ... (42 more files)

✓ tests/integration/ (15 API integration tests)
  - test_user_api.py (5 tests)
  - test_post_api.py (4 tests)
  - test_auth_flow.py (6 tests)

✓ tests/fixtures.py (database fixtures)
✓ tests/conftest.py (pytest configuration)

Coverage: 45% → 82% ✓ (Target: 80%+)
Total tests: 215 tests created

Contract Tests:
✓ tests/contracts/ (15 Pact contract files)
✓ Contract verification added to CI
✓ Pactflow broker configured

OpenAPI:
✓ openapi.yaml (complete specification)
  - 15 endpoints documented
  - All request/response schemas
  - Authentication flows
  - Example requests/responses
✓ Swagger UI: http://localhost:8000/docs
✓ ReDoc: http://localhost:8000/redoc

Impact:
- Addresses Pain #4 (missing tests = biggest mistake)
- Addresses Pain #7 (documentation gaps)
- Testing score: 58 → 85 (+27 points)
- Documentation score: 62 → 90 (+28 points)

Next Steps:
1. Run tests: pytest tests/ -v
2. View coverage: pytest --cov=src tests/
3. View API docs: http://localhost:8000/docs
4. Commit changes: /cco-commit
```

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
# Total time: ~15s (vs 60s sequential)
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
- Target 80%+ coverage

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
- **After /cco-overview**: Follow action plan
- **With /cco-fix**: Fix existing, generate missing
- **Before /cco-commit**: Generate then commit
