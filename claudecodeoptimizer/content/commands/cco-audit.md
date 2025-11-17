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

### Interactive Mode (No Parameters)

1. **Use AskUserQuestion** to present multiselect UI:

```markdown
What should I audit? (pain-point priority order)

🔴 Critical Impact:
□ Security (51% #1 concern - OWASP, AI, supply chain)
□ Tech Debt (23% time waste - dead code, complexity)
□ AI Security (45% reliability - prompt injection, hallucination)

🟡 High Impact:
□ Tests (biggest mistake - coverage, quality, pyramid)
□ Integration (deployment failures - imports, deps)

🟢 Medium Impact:
□ Code Quality (bugs, errors, validation)
□ Documentation (knowledge gaps - API, code, drift)
□ Database (performance - N+1, indexes)
□ Observability (debugging time - logging, metrics)
□ Monitoring (SLOs, alerts)
□ CI/CD (pipeline quality, gates)
□ Containers (Docker, K8s security)
□ Supply Chain (CVEs, licenses)
□ Migrations (data safety)
□ Performance (response time, caching)
□ Architecture (patterns, coupling)
□ Git (commit quality, workflow)

☑ All (comprehensive scan)
```

2. **Confirm selected categories** and explain:
   - Which skills will be used
   - Which agent will run (cco-agent-audit)
   - What will be checked
   - How many files will be analyzed
   - Estimated time

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

```bash
# Single category
/cco-audit --security

# Multiple categories
/cco-audit --security --tech-debt --tests

# All critical
/cco-audit --security --tech-debt --ai-security

# Comprehensive
/cco-audit --all
```

Skip AskUserQuestion, run audit directly with specified categories.

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
