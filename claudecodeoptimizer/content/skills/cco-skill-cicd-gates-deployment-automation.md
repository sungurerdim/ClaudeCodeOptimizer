---
name: cco-skill-cicd-gates-deployment-automation
description: |
  Use this skill when CI/CD pipelines, deployment, automation, or quality gates are mentioned:
  - CI/CD, continuous integration, continuous deployment, continuous delivery, pipeline
  - deployment, deploy, release, rollout, production deployment, staging deployment
  - automation, automate, automated testing, automated deployment, build automation
  - quality gates, build gates, test gates, coverage gates, security gates, deployment gates
  - GitHub Actions, GitLab CI, Jenkins, CircleCI, Travis CI, Azure DevOps
  - blue-green deployment, canary release, rolling deployment, feature flags
  - rollback, rollback strategy, disaster recovery, deployment failure
  - infrastructure as code, IaC, GitOps, Terraform, Ansible, CloudFormation
  - Files: .github/workflows/*, .gitlab-ci.yml, Jenkinsfile, azure-pipelines.yml, *.tf, deploy.sh

  Triggers: CI/CD, pipeline, deployment, deploy, automation, gates, build, release, rollback, blue-green, canary, IaC, GitOps
---

# Skill: CI/CD - Quality Gates, Deployment & Automation

## Purpose

Prevent production incidents through automated quality gates, safe deployment strategies, and infrastructure automation.

**Solves**:
- **Broken Builds**: 30%+ defects reach production without CI gates
- **Slow Deployments**: Manual takes 2-8h vs 5-15min automated
- **Deployment Failures**: 40% fail without automated rollback
- **Environment Drift**: Manual infrastructure causes "works on my machine" (60%+ teams)

**Impact**: Critical

---

## Principles Included

### P_CI_GATES
**Category**: Quality Enforcement
**Why**: Automated gates (lint, test, coverage, security) block broken code
**Triggers**: Setting up CI, quality thresholds, pipeline failures

### P_IAC_GITOPS
**Category**: Infrastructure Automation
**Why**: IaC enables version control, review, automated provisioning
**Triggers**: Infrastructure deployment, environment management

### P_BLUE_GREEN_DEPLOYMENT
**Category**: Deployment Strategy
**Why**: Zero-downtime by switching traffic between identical environments
**Triggers**: Production deploys, zero-downtime releases, rollback

### P_CANARY_RELEASES
**Category**: Progressive Deployment
**Why**: Gradual rollout (5% → 25% → 100%) detects issues early
**Triggers**: High-risk deploys, A/B testing, gradual rollout

### P_ROLLBACK_STRATEGY
**Category**: Incident Response
**Why**: Automated rollback <5min prevents prolonged outages
**Triggers**: Deployment failures, performance degradation, error spikes

### P_GIT_COMMIT_QUALITY
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

## Related Commands

- `/cco-audit-cicd` - Analyze pipeline coverage, gate completeness, deployment strategies
- `/cco-fix-cicd` - Add missing gates, fix failures, optimize build times
- `/cco-generate-cicd` - Generate GitHub Actions, GitLab CI, Terraform templates

---

## Related Skills

- **cco-skill-git-branching-pr-review**: Git events trigger pipelines
- **cco-skill-test-pyramid-coverage-isolation**: Test pyramid defines gate thresholds
- **cco-skill-security-owasp-xss-sqli-csrf**: Security scanning as gate

---

## Examples

### File Context
```
User opens: .github/workflows/ci.yml → Skill loads → P_CI_GATES active
Result: Reviews gate completeness (lint, test, coverage, security)
```

### Deployment Strategy
```
User: "Deploy high-risk feature to production?"
Principles: P_CANARY_RELEASES, P_BLUE_GREEN_DEPLOYMENT
Result: Recommends canary (5% → 25% → 100%) + automated rollback
```

### Pipeline Failure
```
User: "Pipeline failing - coverage 65%"
Principle: P_CI_GATES
Result: Analyzes threshold (80%), identifies gaps, generates tests
```
