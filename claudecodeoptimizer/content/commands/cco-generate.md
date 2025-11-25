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

# CCO Generate Command

**Create missing project components with skill-guided generation.**

**Implementation Note:** This command follows [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md) for file discovery (exclusions applied BEFORE processing), token optimization (three-stage discovery), parallelization (Task calls in single message), and cross-platform compatibility. See cco-audit.md for reference implementation.
---

## Built-in References

**This command inherits standard behaviors from:**

- **[STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md)** - Standard structure, execution protocol, file discovery
- **[STANDARDS_QUALITY.md](../STANDARDS_QUALITY.md)** - UX/DX, efficiency, simplicity, performance standards
- **[LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md)** - Reusable patterns (Step 0, Selection, Accounting, Progress, Error Handling)
- **[STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md)** - File discovery, model selection, parallel execution
- **model selection** - Haiku for mechanical tasks, let Claude Code decide for complex tasks
- **[STANDARDS_TECH_DETECTION.md](../STANDARDS_TECH_DETECTION.md)** - Fast tech detection (<2s), applicability filtering, pre-filtering UI

**See these files for detailed patterns. Only command-specific content is documented below.**

---

## Purpose

Generate missing tests, documentation, CI/CD configs, and other project components using specialized skills and the generate agent.

---

## CRITICAL: Check for Context from Calling Command

**BEFORE any discovery/analysis, check conversation for "CONTEXT FOR /cco-generate:"**

✓ **If found**: Use provided findings, skip discovery, focus ONLY on specified items
✗ **If not found**: Proceed with normal full discovery

**Why**: Eliminates duplicate work - previous command already analyzed.

See **C_COMMAND_CONTEXT_PASSING** principle.

---

## Execution Guarantee

This command executes the FULL operation as planned.
No scope reduction due to time constraints or "workload concerns".

**Estimated time: Provided for transparency, NOT to reduce scope.**

---

## Design Principles

**See:** STANDARDS_QUALITY.md
- UX/DX principles (transparency, progressive disclosure, zero surprises)
- Honesty & accurate reporting (no false positives/negatives)
- No hardcoded examples (use placeholders: `{FILE_PATH}`, `{LINE_NUMBER}`)

---

## Generation Outcome Categories

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
   - Skills: `cco-skill-cicd-gates-deployment-automation`, `cco-skill-deployment-bluegreen-canary-rollback`
   - Generates: GitHub Actions/GitLab CI with quality gates, deployment strategies

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

### Step 0: Introduction and Confirmation

**Pattern:** Pattern 1 (Step 0 Introduction)

**Command-Specific Details:**

**What I do:** Create missing tests, docs, CI/CD configs, and infrastructure files based on what's missing

**Process:** Analyze project → Detect missing components → You select → I generate following conventions → Report results

**Output:** Complete files (tests, OpenAPI specs, CI/CD pipelines, Dockerfile, monitoring configs)

**Time:** 5-20 minutes depending on selection

**New files WILL be created** - all follow project conventions, reviewable before committing

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start generating missing components?",
    header: "Start Generate",
    multiSelect: false,
    options: [
      {label: "Yes, start generating", description: "Analyze project and generate missing components"},
      {label: "No, cancel", description: "Exit without creating any files"}
    ]
  }]
})
```

**If Cancel:** Exit immediately, do NOT proceed
**If Start:** Continue to Project Context Discovery

---

### Step 0.5: Project Context Discovery

**Pattern:** Pattern 2 (Multi-Select with "All")

**Command-Specific Details:**

**Benefits for /cco-generate:** Generated tests/docs follow project conventions and style

**Context Used:** Project naming conventions, testing patterns, documentation style applied to all generated files

---

### Step 0.6: Tech Stack Detection for Template Selection

**Pattern:** Pattern 10 (Tech Stack Detection)

**Purpose:** Select appropriate templates and patterns for generation

```markdown
Detecting tech stack for template selection...

✓ Testing framework: {DETECTED_TESTING} → Using {TESTING_FRAMEWORK} templates
✓ Language: {DETECTED_LANGUAGE} → {LANGUAGE}-specific patterns
✓ Web framework: {DETECTED_FRAMEWORK} → {FRAMEWORK} test patterns
✓ DevOps: {DETECTED_DEVOPS} → {DEVOPS} workflow templates

Tech stack determines:
- Test file naming ({TEST_PATTERN_1} vs {TEST_PATTERN_2})
- Test structure ({STRUCTURE_1} vs {STRUCTURE_2})
- CI/CD templates ({CICD_1} vs {CICD_2})
- Documentation style ({DOC_STYLE_1} vs {DOC_STYLE_2})
```

---


---

### Step 1: Detection and Selection

**Pattern:** Pattern 3 (Progress Reporting)

**Command-Specific Details:**

**Detection Phase:**

1. Detect what EXISTS (tests/, openapi.yaml, Dockerfile, etc.)
2. Detect what's MISSING (compare to ideal project structure)
3. Count specifics:
   - How many untested functions? (grep for definitions, check for tests)
   - How many undocumented endpoints? (find endpoints, check for OpenAPI)
   - Which files need generation? (list actual file paths)

**Dynamic Generation Options:**

Generate options with REAL counts and ACTUAL file/function names from analysis.

**Tab-Based Selection (4×4 limit, 17 generation types):**

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
        {label: "All Testing", description: "Generate all testing components (unit, integration, contract, load, chaos)"},
        {label: f"Unit + Integration ({test_file_count} files)", description: f"Untested functions, API tests, fixtures | {untested_count} functions | Pain #4"},
        {label: f"Contract Tests ({contract_count} endpoints)", description: "Pact contracts, provider verification"},
        {label: f"Load + Chaos ({perf_count} scenarios)", description: "Locust/k6 load tests, chaos engineering"}
      ]
    },
    {
      question: "Select Documentation components to generate:",
      header: "🟡 Docs",
      multiSelect: true,
      options: [
        {label: "All Documentation", description: "Generate all documentation components"},
        {label: f"OpenAPI Spec ({endpoint_count} endpoints)", description: "Complete OpenAPI 3.0, Swagger UI | Pain #7"},
        {label: f"Docs + ADR ({undoc_count} items)", description: "Docstrings, README sections, Architecture Decision Records"},
        {label: "Review Checklist (AI-aware)", description: "Code review checklist with AI hallucination checks | Pain #11, #12 | 🔴 2025 CRITICAL"}
      ]
    },
    {
      question: "Select CI/CD & Container components:",
      header: "🟢 CI/CD",
      multiSelect: true,
      options: [
        {label: "All CI/CD & Containers", description: "Generate all CI/CD and container components"},
        {label: "CI/CD Pipeline", description: "GitHub Actions/GitLab CI with quality gates"},
        {label: "Pre-commit Hooks", description: ".pre-commit-config.yaml with linting, security"},
        {label: "Dockerfile", description: "Multi-stage build, docker-compose, health checks"}
      ]
    },
    {
      question: "Select Database & Observability components:",
      header: "🟢 Ops",
      multiSelect: true,
      options: [
        {label: "All Ops", description: "Select all database and observability components"},
        {label: f"Migration + Indexes ({db_issue_count} items)", description: "Migration scripts with rollback, index creation"},
        {label: "Monitoring + SLO", description: "Prometheus metrics, Grafana dashboards, SLO specs"},
        {label: "Logging", description: "Structured logging config with correlation IDs"}
      ]
    }
  ]
})
```

**Grouped items (due to 4×4=16 slot limit with 17 types):**
- **Load + Chaos** (both performance/resilience testing)
- **Docs + ADR** (both code documentation)
- **Migration + Indexes** (both database operations)
- **Monitoring + SLO** (both observability/alerting)

**Selection Processing:**

```markdown
## Generation Selection Summary

**Your selections:**
- 🔴 Testing: [list selected] → {COMPONENT_COUNT} components
- 🟡 Docs: [list selected] → {COMPONENT_COUNT} components
- 🟢 CI/CD: [list selected] → {COMPONENT_COUNT} components
- 🟢 Ops: [list selected] → {COMPONENT_COUNT} components

**Total: {SELECTED_COUNT} generation tasks selected**

⚠️ Only selected categories will be generated.
```

**Processing rules:**
- "All Components" → generate ALL
- "All [Category]" → generate all in category
- Grouped items (e.g., "Load + Chaos") → generate both
- Otherwise → generate ONLY individually selected items

---

### Step 2: Pre-Flight Confirmation

**Pattern:** Pattern 4 (Complete Accounting)

**Command-Specific Details:**

**Present generation plan with file estimates and time:**

```markdown
Selected: [list selected components]

Skills I'll use: [list skills for selected components]

Agent: generate-agent (Sonnet for quality generation)

I'll create:
[For each selected component, explain what will be generated]

Time estimate: ~{X} minutes
Files to create: ~{Y} files
```

---

### Step 3: Generate Components

**See [STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md) for agent delegation patterns.**

**Command-Specific Details:**

**Agent:** `generate-agent` (Sonnet)

**Why Sonnet:** Code generation requires accuracy, better understanding of project context, generates higher quality tests/docs

**Parallel Execution:** Agent automatically parallelizes independent generation tasks (different files)

**TodoWrite tracking:** All generation tasks tracked in real-time

**Generation Protocol:**

```python
Task({
  subagent_type: "generate-agent",
  model: "sonnet",
  prompt: """
  Generate missing {COMPONENT_TYPE}.

  Use these skills:
  - {SKILL_LIST_FOR_COMPONENT}

  {COMPONENT_TYPE_SPECIFIC_INSTRUCTIONS}

  Follow:
  - {RELEVANT_PATTERNS}
  - U_NO_OVERENGINEERING (keep it simple)
  - U_FOLLOW_PATTERNS (match project conventions)

  Report:
  - Files created with line counts
  - {COMPONENT_SPECIFIC_METRICS}
  - How to {USE_GENERATED_COMPONENT}
  """
})
```

**Example for Tests:**

```python
Task({
  subagent_type: "generate-agent",
  model: "sonnet",
  prompt: """
  Generate missing tests.

  Use these skills:
  - cco-skill-test-pyramid-coverage-isolation
  - cco-skill-api-testing-contract-load-chaos

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

  Follow:
  - P_TEST_PYRAMID (unit >> integration >> e2e)
  - P_TEST_COVERAGE (high coverage target)
  - U_NO_OVERENGINEERING (keep it simple)

  Report:
  - Files created with line counts
  - Coverage improvement estimate
  - How to run tests
  """
})
```

---

### Step 4: Results Report

**See [LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md#pattern-8-results-generation) for standard results pattern.**

**Command-Specific Details:**

**Accounting formula enforced:** `total = generated + skipped + failed`

**Real metrics (no placeholders):**

```markdown
Generation Complete! ✓

[For each category generated, report REAL files:]
Tests Created:
✓ tests/unit/ ({ACTUAL_COUNT} test files, {ACTUAL_TEST_COUNT}+ unit tests)
  {LIST_FIRST_3_5_ACTUAL_FILES_WITH_REAL_TEST_COUNTS}
  - ... ({REMAINING_COUNT} more files)

✓ tests/integration/ ({ACTUAL_COUNT} API integration tests)
  {LIST_ACTUAL_INTEGRATION_TEST_FILES}

✓ tests/fixtures.py (database fixtures) [if created]
✓ tests/conftest.py (pytest configuration) [if created]

Coverage: {BEFORE}% → {AFTER}% ✓
Total tests: {ACTUAL_COUNT} tests created

[Repeat for other categories that were actually generated]

Impact:
- Addresses Pain #{X} ({PAIN_DESCRIPTION})
- Testing score: {BEFORE} → {AFTER} (+{DELTA} points)
- Documentation score: {BEFORE} → {AFTER} (+{DELTA} points)

Next Steps:
1. Run tests: {ACTUAL_TEST_COMMAND_FOR_THIS_PROJECT}
2. View coverage: {ACTUAL_COVERAGE_COMMAND}
3. {OTHER_ACTUAL_NEXT_STEPS}
4. Commit changes: /cco-commit
```

**Never use placeholder examples - only report what was actually generated.**

---

## Agent Usage

**See [STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md) for:**
- Parallel execution patterns (fan-out, pipeline, hierarchical)
- Model selection (Haiku for mechanical, auto for complex)
- Error handling protocols
- Agent communication patterns

**Command-Specific Agent Configuration:**

**Agent:** generate-agent (Sonnet)
**Pattern:** Automatic parallelization (independent files generated in parallel)
**Skills:** Selected based on generation type (tests → test skills, docs → doc skills, etc.)

---

## Agent Error Handling

**Pattern:** Pattern 5 (Error Handling)

**Command-Specific Handling:**

Options: Retry | Retry with different model | Manual generation | Skip this component | Cancel

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
- [OK] generate-agent executed with Sonnet
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

# With additional context (optional prompt)
/cco-generate --tests "Focus on edge cases for payment logic"
/cco-generate --openapi "Include authentication examples"
/cco-generate --all "Follow company documentation standards"
```

**Optional Prompt Support:**
Any text after the flags is treated as additional context for generation. The AI will:
- Incorporate domain-specific requirements
- Follow project-specific conventions
- Include relevant examples based on your context
- Adapt output format to your preferences

---

## Integration with Other Commands

- **After /cco-audit --tests**: Generate missing tests
- **After /cco-audit --quick**: Follow action plan
- **With /cco-fix**: Fix existing, generate missing
- **Before /cco-commit**: Generate then commit

---
