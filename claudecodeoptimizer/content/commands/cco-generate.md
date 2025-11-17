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

### Interactive Mode (No Parameters)

1. **Detect what's missing** using Glob/Grep:
   - No `tests/` directory → Missing tests
   - No `openapi.yaml` → Missing API spec
   - No `.github/workflows/` → Missing CI/CD
   - No `Dockerfile` → Missing containerization
   - Coverage < 80% → Need more tests

2. **Use AskUserQuestion** to present recommendations:

```markdown
What should I generate? (based on your project)

🔴 Critical Missing (Pain #4: Biggest mistake):
□ Tests (45 untested functions, 45% coverage)
□ Contract Tests (15 API endpoints, no contracts)

🟡 High Priority:
□ OpenAPI (15 endpoints, no spec - Pain #7)
□ Load Tests (no performance testing)
□ CI/CD (no GitHub Actions)

🟢 Recommended:
□ Monitoring (Prometheus/Grafana configs)
□ Logging (structured logging setup)
□ Migration Scripts (3 schema changes detected)
□ Database Indexes (3 slow queries detected)
□ Dockerfile (no containerization)
□ Runbook (no operational docs)
□ Pre-commit Hooks (no quality gates)

☑ All Recommended
```

3. **Confirm selection** and explain:

```markdown
Selected: Tests, Contract Tests, OpenAPI

Skills used:
- cco-skill-test-pyramid-coverage-isolation
- cco-skill-api-testing-contract-load-chaos
- cco-skill-docs-api-openapi-adr-runbooks

Agent: cco-agent-generate (Sonnet)

I'll create:

Tests:
- Unit tests for 45 untested functions
- Integration tests for 15 API endpoints
- Test fixtures for 3 database models
- Estimated: 500+ lines of test code
- Coverage: 45% → 80%+ (target: 85%)

Contract Tests:
- Pact contracts for 15 API endpoints
- Provider verification tests
- Consumer stub generation
- Contract broker setup (Pactflow)

OpenAPI:
- Complete OpenAPI 3.0 specification
- Request/response schemas for all endpoints
- Authentication/security docs
- Interactive docs at /docs (Swagger UI)
- Example requests/responses

Time estimate: ~10 minutes
Files created: ~60 files

Continue? (yes/no)
```

4. **Use TodoWrite** to track generation progress

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
