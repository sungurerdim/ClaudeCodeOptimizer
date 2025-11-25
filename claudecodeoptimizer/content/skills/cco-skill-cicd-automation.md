---
name: cco-skill-cicd-automation
description: Use this skill when CI/CD pipelines, deployment, automation, or quality gates are mentioned
keywords: [cicd, pipeline, continuous integration, continuous deployment, deployment, deploy, release, rollout, automation, quality gates, build gates, github actions, gitlab ci, jenkins, circleci, blue-green, canary, rollback, infrastructure as code, gitops, terraform]
category: infrastructure
related_commands:
  action_types: [audit, fix, generate]
  categories: [infrastructure]
pain_points: [6]
---

# Skill: CI/CD - Quality Gates, Deployment & Automation

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Domain
CI/CD pipelines, deployment automation, quality gates

## Purpose
Prevent production incidents through automated quality gates, safe deployment strategies, and infrastructure automation.

**Solves**:
- **Broken Builds**: Many defects reach production without CI gates
- **Slow Deployments**: Manual takes hours vs minutes automated
- **Deployment Failures**: Many fail without automated rollback
- **Environment Drift**: Manual infrastructure causes "works on my machine" issues

**Impact**: Critical
---

---

## Guidance Areas

### CI Gates
**Category**: Quality Enforcement
**Why**: Automated gates (lint, test, coverage, security) block broken code
**Triggers**: Setting up CI, quality thresholds, pipeline failures

### Infrastructure as Code (IaC/GitOps)
**Category**: Infrastructure Automation
**Why**: IaC enables version control, review, automated provisioning
**Triggers**: Infrastructure deployment, environment management

### Blue-Green Deployment
**Category**: Deployment Strategy
**Why**: Zero-downtime by switching traffic between identical environments
**Triggers**: Production deploys, zero-downtime releases, rollback

### Canary Releases
**Category**: Progressive Deployment
**Why**: Gradual rollout in stages detects issues early
**Triggers**: High-risk deploys, A/B testing, gradual rollout

### Rollback Strategy
**Category**: Incident Response
**Why**: Fast automated rollback prevents prolonged outages
**Triggers**: Deployment failures, performance degradation, error spikes

### Git Commit Quality
**Category**: Git Best Practices
**Why**: Quality commits enable deployment tracking, changelog automation
**Triggers**: CI/CD pipelines, deployment automation, release management

---

## Activation

Auto-loads when detecting:
- **Keywords**: CI/CD, pipeline, deployment, deploy, automation, gates, build, release, rollback, blue-green, canary, IaC
- **Intent**: "setup CI/CD", "automate deployment", "fix pipeline", "deployment strategy"
- **Files**: `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, `*.tf`, `deploy.sh`, `azure-pipelines.yml`

---

## Related Skills

- **Git workflow skills**: Git events trigger pipelines
- **Testing skills**: Test pyramid defines gate thresholds
- **Security skills**: Security scanning as gate

---

## Examples

### File Context
```
User opens: .github/workflows/ci.yml → Skill loads → CI Gates guidance active
Result: Reviews gate completeness (lint, test, coverage, security)
```

### Deployment Strategy
```
User: "Deploy high-risk feature to production?"
Guidance: Canary Releases, Blue-Green Deployment
Result: Recommends canary deployment with gradual rollout + automated rollback
```

### Pipeline Failure
```
User: "Pipeline failing - coverage below threshold"
Guidance: CI Gates
Result: Analyzes threshold, identifies gaps, generates tests
```

---

## CI/CD Templates

Use these templates when generating CI/CD configurations:

### GitHub Actions - Python

```yaml
name: cco-skill-cicd-automation
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - name: Install dependencies
        run: pip install -e .[dev]
      - name: Lint
        run: ruff check .
      - name: Format check
        run: ruff format --check .
      - name: Type check
        run: mypy .
      - name: Security scan
        run: bandit -r src/
      - name: Test with coverage
        run: pytest --cov --cov-report=xml --cov-fail-under=80
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

### GitHub Actions - Node.js

```yaml
name: cco-skill-cicd-automation
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
      - run: npm run build
```

### GitLab CI - Python

```yaml
stages: [lint, test, security, build, deploy]

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/

lint:
  stage: lint
  script:
    - pip install ruff mypy
    - ruff check .
    - ruff format --check .
    - mypy .

test:
  stage: test
  script:
    - pip install -e .[dev]
    - pytest --cov --cov-report=xml --cov-fail-under=80
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

security:
  stage: security
  script:
    - pip install bandit safety
    - bandit -r src/
    - safety check

deploy:
  stage: deploy
  script:
    - echo "Deploy to production"
  only:
    - main
  when: manual
```

### Pre-commit Config

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
```

### Dockerfile - Python

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir build && python -m build --wheel

# Production stage
FROM python:3.11-slim
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir *.whl && rm *.whl
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "-m", "app"]
```
