---
name: supply-chain-security
description: Supply chain security with dependency management and SAST analysis
---

# Skill: Supply Chain Security & SAST
**Domain**: Security, Dependencies, Static Analysis
**Purpose**: Implement vulnerability scanning, SAST, license compliance, and dependency attack prevention (typosquatting, confusion).

## Core Techniques
- **SBOM Generation**: Create Software Bill of Materials for transparency
- **Vulnerability Scanning**: Detect CVEs in dependencies (npm audit, pip-audit, Trivy)
- **SAST**: Static analysis for security issues (Bandit, Semgrep, CodeQL)
- **Dependency Confusion Prevention**: Scope packages, pin versions, verify integrity
- **License Compliance**: Enforce allowed licenses, block forbidden ones
- **Auto-Updates**: Use Dependabot/Renovate for automated patching

## Patterns

### ✅ Good: SBOM Generation
```bash
# Python
cyclonedx-py -o sbom.json

# Node.js
npx @cyclonedx/bom -o sbom.json

# Go
cyclonedx-gomod -json -output sbom.json
```
**Why**: CycloneDX format provides standardized, machine-readable dependency inventory

### ✅ Good: Multi-Scanner Vulnerability Detection
```bash
# Python
pip-audit --desc --fix

# Node.js
npm audit --audit-level=high
snyk test --severity-threshold=high || exit 1

# Multi-language
trivy fs --severity CRITICAL --exit-code 1 .
```
**Why**: Multiple scanners increase CVE detection coverage

### ✅ Good: SAST Integration
```bash
# Python: Detect hardcoded secrets, SQL injection
bandit -r src/ -f json -o bandit-report.json
semgrep --config=p/owasp-top-ten src/

# JavaScript: Security linting
eslint --plugin security .

# Secrets
gitleaks detect --source . --report-path report.json
```
**Why**: Static analysis catches vulnerabilities before runtime

### ✅ Good: Dependency Pinning
```json
{
  "dependencies": {
    "express": "4.18.2",
    "lodash": "4.17.21"
  }
}
```
**Why**: Exact versions prevent supply chain attacks via unexpected updates

### ✅ Good: Scoped Private Packages
```bash
# .npmrc
@mycompany:registry=https://npm.mycompany.com/
registry=https://registry.npmjs.org/
```
**Why**: Prevents dependency confusion attacks by scoping internal packages

### ✅ Good: Automated Dependabot Updates
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    automerge:
      - dependency-type: "direct:production"
        update-types: ["patch"]
```
**Why**: Auto-patches security vulnerabilities without manual intervention

### ✅ Good: License Compliance
```python
ALLOWED = ['MIT', 'Apache-2.0', 'BSD-3-Clause']
FORBIDDEN = ['GPL-3.0', 'AGPL-3.0']

for pkg, info in licenses.items():
    if info['license'] in FORBIDDEN:
        raise ValueError(f"Forbidden license: {pkg}")
```
**Why**: Prevents legal issues from incompatible copyleft licenses

### ❌ Bad: Floating Versions
```json
{
  "dependencies": {
    "express": "^4.0.0",
    "lodash": "~4.17.0"
  }
}
```
**Why**: Allows malicious version substitution attacks

### ❌ Bad: No Lock Files
```bash
# Missing: package-lock.json, poetry.lock, go.sum
```
**Why**: Non-reproducible builds, transitive dependency confusion

### ❌ Bad: Skipping Transitive Dependencies
```bash
# Only scanning direct dependencies
npm ls --depth=0
```
**Why**: 90% of vulnerabilities are in transitive dependencies

### ❌ Bad: Manual Dependency Updates
```bash
# Manual npm update every few months
```
**Why**: Delays critical security patches by weeks/months

## Checklist
- [ ] SBOM generated (CycloneDX/SPDX)
- [ ] Vulnerability scans in CI (Trivy/Snyk/npm audit)
- [ ] SAST enabled (Bandit/Semgrep/CodeQL)
- [ ] Secrets detection (Gitleaks/TruffleHog)
- [ ] Lock files committed (package-lock.json, poetry.lock, go.sum)
- [ ] Exact version pinning (no ^/~)
- [ ] Private packages scoped (@company/*)
- [ ] Dependabot/Renovate configured
- [ ] License policy enforced (block GPL/AGPL)
- [ ] CVE database updated daily
- [ ] Critical vulnerabilities block deployment
