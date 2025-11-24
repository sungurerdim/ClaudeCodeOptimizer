---
id: P_DEPENDENCY_MANAGEMENT
title: Dependency Management
category: universal
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_DEPENDENCY_MANAGEMENT: Dependency Management 🔴

**Severity**: High

Keep dependencies updated and scan for vulnerabilities. Lock versions, audit regularly, update proactively.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Known vulnerabilities** - most breaches exploit known CVEs
- **Dependency rot** - Outdated dependencies become unmaintainable
- **Breaking updates** - Surprise breaking changes in production
- **Supply chain attacks** - Malicious packages (event-stream, ua-parser-js)
- **License violations** - Incompatible licenses create legal risk

### Core Practices

**Every project MUST:**
1. ✅ **Lock dependencies** - Lock files committed (package-lock.json, poetry.lock, Cargo.lock)
2. ✅ **Scan for CVEs** - Automated vulnerability scanning in CI
3. ✅ **Update regularly** - Monthly dependency updates
4. ✅ **Audit licenses** - Ensure compatible licenses
5. ✅ **Pin versions** - No floating versions in production

### Implementation Patterns

#### ✅ Good: Locked Dependencies
```json
// package.json
{
  "dependencies": {
    "express": "4.18.2"  // ✅ Exact version
  }
}

// package-lock.json committed to git
// ✅ Reproducible builds guaranteed
```

#### ❌ Bad: Floating Versions
```json
// package.json
{
  "dependencies": {
    "express": "^4.0.0"  // ❌ Any 4.x version
  }
}

// No lock file committed
// ❌ Different versions in dev/staging/prod
```

---

## Automated Tools

### Python: pip-audit, Safety
```bash
# Install security scanner
pip install pip-audit safety

# Scan for vulnerabilities
pip-audit
safety check

# CI integration
pip-audit --require-hashes --format json > audit.json
```

### Python: Dependabot/Renovate
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### JavaScript: npm audit, Snyk
```bash
# Built-in audit
npm audit
npm audit fix  # Auto-fix

# Third-party scanning
npx snyk test
npx snyk monitor

# CI enforcement
npm audit --audit-level=high || exit 1
```

### Go: govulncheck
```bash
# Install
go install golang.org/x/vuln/cmd/govulncheck@latest

# Scan
govulncheck ./...

# CI integration
govulncheck -json ./... > vuln-report.json
```

### Rust: cargo audit
```bash
# Install
cargo install cargo-audit

# Scan
cargo audit

# CI enforcement
cargo audit --deny warnings
```

---

## Dependency Update Strategy

### Weekly: Patch Updates (Security)
```bash
# Auto-merge patch updates (1.2.3 → 1.2.4)
# These should be safe (bug fixes only)

# Configure Dependabot
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    schedule:
      interval: "weekly"
    # Auto-merge patches
    automerge-strategy: "semver-patch"
```

### Monthly: Minor Updates (Features)
```bash
# Review minor updates (1.2.0 → 1.3.0)
# May include new features, review changelog

# Manual review required
# Create PR, review changes, test, merge
```

### Quarterly: Major Updates (Breaking)
```bash
# Plan major updates (1.x → 2.x)
# Breaking changes, requires migration work

# Dedicated sprint for major updates
# Read migration guide, update code, test thoroughly
```

---

## Anti-Patterns

### ❌ Never Update
```bash
# package.json from 2019
{
  "dependencies": {
    "express": "4.16.0",  # 5 years old, 20+ CVEs
    "lodash": "4.17.4",   # Critical vulnerabilities
    "axios": "0.18.0"     # Severe security issues
  }
}

# Result: Security nightmare, technical debt accumulation
```

### ❌ Update Everything at Once
```bash
# ❌ BAD: Annual "update day"
npm update  # Updates 150 packages

# Result: Everything breaks, can't identify root cause
# Takes weeks to fix
```

### ❌ No Lock File
```bash
# ❌ BAD: No package-lock.json committed
.gitignore:
package-lock.json  # ❌ NEVER ignore lock files

# Result: Different versions in dev/staging/prod
# "Works on my machine" syndrome
```

### ❌ Ignoring Vulnerabilities
```bash
# ❌ BAD: Suppressing all warnings
npm audit --audit-level=critical  # Only critical, ignores high/moderate

# Or worse:
npm audit || true  # Ignore all audit failures

# Result: Known vulnerabilities in production
```

---

## CVE Response Process

### 1. Detection (Automated)
```bash
# CI runs security scan on every PR
- name: Security Scan
  run: npm audit --audit-level=high
```

### 2. Assessment (Within 24 Hours)
```bash
# Check severity and exploitability
- Critical: Patch immediately (same day)
- High: Patch within 72 hours
- Medium: Patch within 1 week
- Low: Patch in next regular update
```

### 3. Fix (As Fast As Possible)
```bash
# Option 1: Update dependency
npm update package-with-vulnerability

# Option 2: If no fix available, find alternative
npm uninstall vulnerable-package
npm install secure-alternative

# Option 3: If no alternative, apply workaround
# Document workaround in README.md
```

### 4. Verification
```bash
# Re-scan after fix
npm audit
# Should show 0 vulnerabilities

# Test application still works
npm test
npm run build
```

---

## License Management

### Check Licenses
```bash
# Python
pip-licenses

# JavaScript
npx license-checker

# Go
go-licenses check ./...

# Rust
cargo-license
```

### Allowed Licenses (Example)
```yaml
# license-policy.yml
allowed:
  - MIT
  - Apache-2.0
  - BSD-3-Clause
  - BSD-2-Clause
  - ISC

forbidden:
  - GPL-3.0  # Copyleft (may require open-sourcing your code)
  - AGPL-3.0  # Strong copyleft
  - SSPL  # Server Side Public License
```

---

## Implementation Checklist

- [ ] **Lock files committed** (package-lock.json, poetry.lock, Cargo.lock, go.sum)
- [ ] **Dependabot/Renovate enabled** (automated PRs for updates)
- [ ] **CI security scan** (fails build on high/critical CVEs)
- [ ] **Weekly patch updates** (auto-merge if tests pass)
- [ ] **Monthly minor updates** (manual review + merge)
- [ ] **Quarterly major updates** (planned migration sprints)
- [ ] **License audit** (check for incompatible licenses)
- [ ] **CVE response process** (documented SLA for each severity)

---

## CI Integration

### GitHub Actions
```yaml
name: Dependency Check

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: npm ci

      - name: Security audit
        run: npm audit --audit-level=high

      - name: License check
        run: npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-3-Clause'

      - name: Outdated dependencies
        run: npm outdated || true  # Don't fail, just report
```

---

## Metrics and Monitoring

### Key Indicators
- **Vulnerability count** - Number of known CVEs (aim for 0)
- **Dependency age** - Average age of dependencies (aim for <6 months)
- **Update frequency** - Days since last dependency update (aim for <30)
- **License compliance** - % of dependencies with approved licenses (aim for 100%)

### Dashboards
```bash
# Snyk dashboard
snyk monitor  # Sends data to Snyk dashboard

# Dependabot insights
# GitHub: Insights → Dependency graph → Dependabot

# Custom metrics
echo "dependencies_with_vulnerabilities $(npm audit --json | jq '.metadata.vulnerabilities.total')" | curl --data-binary @- https://metrics.example.com/
```

---

## Summary

**Dependency Management** means keeping dependencies updated, scanning for vulnerabilities, locking versions, and auditing licenses. Proactive management prevents security incidents and technical debt.

**Core Rule**: Lock versions, scan weekly, update monthly, audit constantly.
---

## Checklist

Before implementation:
- [ ] Principle requirements reviewed
- [ ] Implementation follows P_DEPENDENCY_MANAGEMENT guidelines
- [ ] Code verified against principle standards
- [ ] Documentation updated if needed

