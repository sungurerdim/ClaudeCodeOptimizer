---
name: cco-skill-supply-chain
description: Comprehensive supply chain security including SBOM, vulnerability scanning, SAST, SLSA framework, build security, provenance verification, dependency confusion prevention, and automated patching (OWASP A03:2025 expanded scope)
keywords: [SBOM, vulnerability scanning, SAST, Bandit, Semgrep, Trivy, license compliance, dependency confusion, Dependabot, supply chain, SLSA, provenance, build security, VEX, image signing]
category: security
related_commands:
  action_types: [audit, fix, generate]
  categories: [security, cicd]
pain_points: [3, 10]
---

# Supply Chain Security, Dependencies & SAST

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


Comprehensive supply chain security including SBOM, SAST, SLSA, build security, and provenance verification.
---

---

## Domain

Dependency management, build pipelines, container registries, package repositories, static analysis.

---

## Purpose

**OWASP A03:2025 Expanded Scope:**
- **Software and Data Integrity Failures** now includes **build security**
- Supply chain attacks increased 742% (Sonatype 2025)
- SLSA Framework adoption critical for preventing tampering
- Provenance verification mandatory for critical systems

**2025 Critical Updates:**
- SBOM + VEX documents (vulnerability exploitability exchange)
- SLSA Level 2+ requirements for production deployments
- Image signing and verification (Sigstore/Cosign)
- AI model supply chain security (model poisoning risks)

---

## Core Techniques

### 1. SBOM Generation & VEX Documents

**SBOM (Software Bill of Materials):**
```bash
# Python - CycloneDX
pip install cyclonedx-bom
cyclonedx-py -o sbom.json

# Node.js
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Go
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest
cyclonedx-gomod app -json -output sbom.json

# Container images
trivy image --format cyclonedx myimage:latest > sbom.json
```

**VEX Document (Vulnerability Exploitability eXchange):**
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "vulnerabilities": [
    {
      "id": "CVE-2024-1234",
      "source": {
        "name": "NVD",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2024-1234"
      },
      "analysis": {
        "state": "not_affected",
        "justification": "code_not_reachable",
        "response": ["will_not_fix"],
        "detail": "Vulnerable function not used in our codebase"
      }
    }
  ]
}
```

**Detection Pattern:**
```python
def check_sbom_presence() -> dict:
    """Check if SBOM exists and is current"""
    sbom_files = glob.glob('**/sbom.json', recursive=True) + \
                 glob.glob('**/bom.json', recursive=True)

    if not sbom_files:
        return {
            'has_sbom': False,
            'severity': 'HIGH',
            'message': 'No SBOM found - supply chain visibility missing'
        }

    # Check age
    sbom_path = sbom_files[0]
    age_days = (datetime.now() - datetime.fromtimestamp(
        os.path.getmtime(sbom_path)
    )).days

    return {
        'has_sbom': True,
        'path': sbom_path,
        'age_days': age_days,
        'stale': age_days > 7,
        'recommendation': 'Regenerate SBOM weekly or on dependency changes'
    }
```

---

### 2. SLSA Framework (Supply-chain Levels for Software Artifacts)

**SLSA Level Requirements:**

**Level 1: Documentation**
```yaml
# .github/workflows/build.yml
- name: Generate provenance
  uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.9.0
  with:
    base64-subjects: "${{ steps.hash.outputs.hashes }}"
```

**Level 2: Build Service**
```yaml
# Use hosted build service (GitHub Actions, GitLab CI)
# No local builds for production
steps:
  - uses: actions/checkout@v4
  - run: npm ci  # Reproducible builds
  - run: npm run build
  - uses: slsa-framework/slsa-github-generator@v1.9.0
```

**Level 3: Provenance Verification**
```bash
# Verify SLSA provenance
slsa-verifier verify-artifact \
  --provenance-path build.intoto.jsonl \
  --source-uri github.com/myorg/myrepo
```

**Detection Pattern:**
```python
def assess_slsa_level() -> dict:
    """Determine SLSA compliance level"""
    score = 0
    issues = []

    # Level 1: Build process documented
    if os.path.exists('.github/workflows/build.yml') or os.path.exists('.gitlab-ci.yml'):
        score = 1
    else:
        issues.append('No CI/CD pipeline found')

    # Level 2: Hosted build service
    ci_files = glob.glob('.github/workflows/*.yml') + glob.glob('.gitlab-ci.yml')
    if ci_files:
        with open(ci_files[0]) as f:
            content = f.read()
            if 'slsa-github-generator' in content or 'slsa-provenance' in content:
                score = 2

    # Level 3: Provenance verification
    if glob.glob('**/*.intoto.jsonl', recursive=True):
        score = 3

    return {
        'slsa_level': score,
        'target': 2,  # Minimum for production
        'compliant': score >= 2,
        'issues': issues,
        'recommendation': (
            'Implement SLSA Level 2+' if score < 2 else
            'SLSA compliant'
        )
    }
```

---

### 3. Build Security

**Hermetic Builds:**
```dockerfile
# ❌ BAD: Non-hermetic build
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl git
RUN curl -s https://install.example.com | bash

# ✅ GOOD: Hermetic build
FROM ubuntu:24.04@sha256:abc123...  # Pinned digest
COPY --from=build /app/dist /app
# No network access during build
```

**Dependency Integrity:**
```bash
# ✅ Verify checksums
npm ci --audit-signatures  # Verify npm package signatures

# Python
pip install --require-hashes -r requirements.txt

# requirements.txt with hashes
requests==2.31.0 --hash=sha256:abc123...
```

**Detection Pattern:**
```python
def detect_build_security_issues() -> List[dict]:
    """Find build security problems"""
    issues = []

    # Check Dockerfile
    if os.path.exists('Dockerfile'):
        with open('Dockerfile') as f:
            content = f.read()

            # Non-pinned base images
            if re.search(r'FROM.*:latest', content):
                issues.append({
                    'type': 'build_security',
                    'subtype': 'unpinned_base_image',
                    'severity': 'HIGH',
                    'file': 'Dockerfile',
                    'message': 'Base image uses :latest tag (non-reproducible)'
                })

            # curl | bash pattern
            if re.search(r'curl.*\|.*bash', content, re.IGNORECASE):
                issues.append({
                    'type': 'build_security',
                    'subtype': 'pipe_to_shell',
                    'severity': 'CRITICAL',
                    'file': 'Dockerfile',
                    'message': 'Piping curl to bash (supply chain risk)'
                })

    # Check package.json for integrity checks
    if os.path.exists('package-lock.json'):
        with open('package-lock.json') as f:
            data = json.load(f)
            if 'packages' in data:
                no_integrity = [
                    name for name, pkg in data['packages'].items()
                    if pkg.get('integrity') is None and name != ''
                ]
                if no_integrity:
                    issues.append({
                        'type': 'build_security',
                        'subtype': 'missing_integrity',
                        'severity': 'MEDIUM',
                        'count': len(no_integrity),
                        'message': f'{len(no_integrity)} packages without integrity hashes'
                    })

    # Check requirements.txt for hashes
    if os.path.exists('requirements.txt'):
        with open('requirements.txt') as f:
            content = f.read()
            lines_with_packages = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
            lines_with_hashes = [l for l in lines_with_packages if '--hash=' in l]

            if lines_with_packages and not lines_with_hashes:
                issues.append({
                    'type': 'build_security',
                    'subtype': 'missing_hashes',
                    'severity': 'MEDIUM',
                    'file': 'requirements.txt',
                    'message': 'Python dependencies without hashes (use pip-compile --generate-hashes)'
                })

    return issues
```

---

### 4. Vulnerability Scanning

**Multi-Scanner Approach:**
```bash
# Container images
trivy image --severity CRITICAL,HIGH myimage:latest

# Filesystem
trivy fs --scanners vuln,secret,misconfig .

# Python
pip-audit --desc --fix

# Node.js
npm audit --audit-level=high
snyk test --severity-threshold=high

# SAST
semgrep --config=p/owasp-top-ten --json src/
```

**Detection Pattern:**
```python
def detect_vulnerability_scanning() -> dict:
    """Check if vulnerability scanning is configured"""
    scanners_found = []
    scanners_missing = []

    # Check CI/CD for scanners
    ci_files = glob.glob('.github/workflows/*.yml') + glob.glob('.gitlab-ci.yml')

    scanner_patterns = {
        'trivy': r'trivy\s+(image|fs)',
        'snyk': r'snyk\s+test',
        'npm_audit': r'npm\s+audit',
        'pip_audit': r'pip-audit',
        'bandit': r'bandit\s+-r',
        'semgrep': r'semgrep\s+--config',
    }

    if ci_files:
        for ci_file in ci_files:
            with open(ci_file) as f:
                content = f.read()
                for scanner, pattern in scanner_patterns.items():
                    if re.search(pattern, content):
                        scanners_found.append(scanner)

    # Determine missing scanners based on project type
    if os.path.exists('package.json'):
        if 'npm_audit' not in scanners_found and 'snyk' not in scanners_found:
            scanners_missing.append('npm_audit or snyk')

    if os.path.exists('requirements.txt') or os.path.exists('pyproject.toml'):
        if 'pip_audit' not in scanners_found and 'snyk' not in scanners_found:
            scanners_missing.append('pip-audit or snyk')
        if 'bandit' not in scanners_found:
            scanners_missing.append('bandit')

    if os.path.exists('Dockerfile'):
        if 'trivy' not in scanners_found:
            scanners_missing.append('trivy')

    return {
        'scanners_configured': scanners_found,
        'scanners_missing': scanners_missing,
        'coverage': (
            'GOOD' if len(scanners_found) >= 2 else
            'BASIC' if len(scanners_found) == 1 else
            'NONE'
        ),
        'recommendation': (
            'Add missing scanners' if scanners_missing else
            'Scanning configured'
        )
    }
```

---

### 5. SAST (Static Application Security Testing)

**Language-Specific SAST:**
```bash
# Python
bandit -r src/ -f json -o bandit-report.json
semgrep --config=p/security-audit src/

# JavaScript/TypeScript
eslint --plugin security .
semgrep --config=p/javascript src/

# Secrets detection (all languages)
gitleaks detect --source . --report-path gitleaks-report.json
trufflehog filesystem . --json > trufflehog-report.json
```

**Detection Pattern:**
```python
def detect_sast_configuration() -> dict:
    """Check SAST setup"""
    sast_tools = {
        'bandit': {
            'config_files': ['bandit.yml', '.bandit'],
            'languages': ['python']
        },
        'semgrep': {
            'config_files': ['.semgrep.yml', 'semgrep.yml'],
            'languages': ['python', 'javascript', 'java', 'go']
        },
        'eslint-security': {
            'config_files': ['.eslintrc.js', '.eslintrc.json'],
            'languages': ['javascript', 'typescript']
## Checklist

### SBOM & Provenance
- [ ] SBOM generated (CycloneDX/SPDX format)
- [ ] VEX document for vulnerability status
- [ ] SBOM regenerated weekly or on changes
- [ ] SLSA Level 2+ compliance
- [ ] Provenance attestations generated

### Build Security
- [ ] Base images pinned by digest
- [ ] Hermetic builds (reproducible)
- [ ] No curl | bash patterns
- [ ] Dependency integrity checks (hashes)
- [ ] Lock files committed

### Vulnerability Scanning
- [ ] Container image scanning (Trivy)
- [ ] Dependency scanning (npm audit, pip-audit, Snyk)
- [ ] Scans run in CI/CD
- [ ] Critical vulnerabilities block deployment
- [ ] CVE database updated daily

### SAST
- [ ] Language-specific SAST (Bandit, Semgrep, ESLint)
- [ ] Secrets detection (Gitleaks, TruffleHog)
- [ ] SAST runs in CI/CD
- [ ] Security findings reviewed

### Dependency Security
- [ ] Exact version pinning (no ^/~)
- [ ] Private packages scoped (@company/*)
- [ ] Lock files committed and current
- [ ] Dependabot/Renovate configured
- [ ] License compliance enforced

### Container Security
- [ ] Images signed (Cosign/Notation)
- [ ] Signature verification in deployment
- [ ] Non-root USER directive
- [ ] No secrets in Dockerfile
- [ ] Multi-stage builds for minimal images

---

---

## References

- [OWASP A03:2025 Software and Data Integrity Failures](https://owasp.org/Top10/A03_2021-Software_and_Data_Integrity_Failures/)
- [SLSA Framework](https://slsa.dev/)
- [CycloneDX SBOM Standard](https://cyclonedx.org/)
- [Sigstore/Cosign - Container Signing](https://www.sigstore.dev/)
- [NIST SSDF - Secure Software Development Framework](https://csrc.nist.gov/Projects/ssdf)
- [Sonatype State of the Software Supply Chain 2025](https://www.sonatype.com/resources/state-of-the-software-supply-chain)
