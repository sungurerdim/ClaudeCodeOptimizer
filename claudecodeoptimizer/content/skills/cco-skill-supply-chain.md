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
        },
        'gitleaks': {
            'config_files': ['.gitleaks.toml'],
            'languages': ['all']
        }
    }

    configured_tools = []
    for tool, config in sast_tools.items():
        if any(os.path.exists(f) for f in config['config_files']):
            configured_tools.append(tool)

    # Check CI/CD
    ci_files = glob.glob('.github/workflows/*.yml') + glob.glob('.gitlab-ci.yml')
    ci_sast_tools = []

    if ci_files:
        for ci_file in ci_files:
            with open(ci_file) as f:
                content = f.read()
                for tool in sast_tools.keys():
                    if tool in content:
                        ci_sast_tools.append(tool)

    return {
        'sast_configured': configured_tools,
        'sast_in_ci': ci_sast_tools,
        'has_secrets_detection': 'gitleaks' in configured_tools or 'trufflehog' in ci_sast_tools,
        'maturity': (
            'ADVANCED' if len(configured_tools) >= 3 else
            'BASIC' if len(configured_tools) >= 1 else
            'NONE'
        )
    }
```

---

### 6. Dependency Confusion Prevention

**Package Scoping:**
```bash
# .npmrc
@mycompany:registry=https://npm.mycompany.com/
registry=https://registry.npmjs.org/
always-auth=true
```

**Version Pinning:**
```json
{
  "dependencies": {
    "express": "4.18.2",  // Exact version
    "lodash": "4.17.21"
  }
}
```

**Detection Pattern:**
```python
def detect_dependency_confusion_risks() -> List[dict]:
    """Find dependency confusion vulnerabilities"""
    issues = []

    # Check package.json for floating versions
    if os.path.exists('package.json'):
        with open('package.json') as f:
            data = json.load(f)
            for dep_type in ['dependencies', 'devDependencies']:
                if dep_type in data:
                    for pkg, version in data[dep_type].items():
                        if version.startswith('^') or version.startswith('~'):
                            issues.append({
                                'type': 'dependency_confusion',
                                'subtype': 'floating_version',
                                'package': pkg,
                                'version': version,
                                'severity': 'MEDIUM',
                                'message': f'{pkg} uses floating version {version}'
                            })

    # Check for .npmrc scoping
    if os.path.exists('package.json'):
        if not os.path.exists('.npmrc'):
            issues.append({
                'type': 'dependency_confusion',
                'subtype': 'missing_npmrc',
                'severity': 'HIGH',
                'message': 'No .npmrc found - private packages may be vulnerable'
            })
        else:
            with open('.npmrc') as f:
                content = f.read()
                if '@' not in content or 'registry=' not in content:
                    issues.append({
                        'type': 'dependency_confusion',
                        'subtype': 'unscoped_packages',
                        'severity': 'HIGH',
                        'message': 'Private packages not scoped in .npmrc'
                    })

    # Check for lock file
    if os.path.exists('package.json') and not os.path.exists('package-lock.json'):
        issues.append({
            'type': 'dependency_confusion',
            'subtype': 'missing_lock_file',
            'severity': 'CRITICAL',
            'message': 'No package-lock.json (non-reproducible builds)'
        })

    if os.path.exists('requirements.txt') and not os.path.exists('poetry.lock') and not os.path.exists('Pipfile.lock'):
        issues.append({
            'type': 'dependency_confusion',
            'subtype': 'missing_lock_file',
            'severity': 'HIGH',
            'message': 'No Python lock file (poetry.lock or Pipfile.lock)'
        })

    return issues
```

---

### 7. Container Image Security

**Image Signing (Cosign):**
```bash
# Sign image
cosign sign --key cosign.key myimage:latest

# Verify signature
cosign verify --key cosign.pub myimage:latest
```

**Detection Pattern:**
```python
def detect_container_security() -> dict:
    """Assess container security practices"""
    issues = []

    if not os.path.exists('Dockerfile'):
        return {'has_dockerfile': False}

    with open('Dockerfile') as f:
        content = f.read()

        # Check base image pinning
        base_images = re.findall(r'FROM\s+(\S+)', content)
        for image in base_images:
            if ':latest' in image:
                issues.append({
                    'type': 'container_security',
                    'subtype': 'unpinned_image',
                    'severity': 'HIGH',
                    'image': image,
                    'message': f'Base image {image} uses :latest tag'
                })
            elif '@sha256:' not in image:
                issues.append({
                    'type': 'container_security',
                    'subtype': 'no_digest_pin',
                    'severity': 'MEDIUM',
                    'image': image,
                    'message': f'Base image {image} not pinned by digest'
                })

        # Check for running as root
        if 'USER' not in content:
            issues.append({
                'type': 'container_security',
                'subtype': 'runs_as_root',
                'severity': 'HIGH',
                'message': 'Container runs as root (no USER directive)'
            })

        # Check for secrets in build
        if re.search(r'(AWS_SECRET|API_KEY|PASSWORD|TOKEN)\s*=', content):
            issues.append({
                'type': 'container_security',
                'subtype': 'hardcoded_secrets',
                'severity': 'CRITICAL',
                'message': 'Potential secrets in Dockerfile'
            })

    # Check for image signing
    has_cosign = os.path.exists('.github/workflows/') and any(
        'cosign' in open(f).read()
        for f in glob.glob('.github/workflows/*.yml')
    )

    return {
        'has_dockerfile': True,
        'issues': issues,
        'image_signing': has_cosign,
        'severity_counts': {
            'CRITICAL': len([i for i in issues if i['severity'] == 'CRITICAL']),
            'HIGH': len([i for i in issues if i['severity'] == 'HIGH']),
            'MEDIUM': len([i for i in issues if i['severity'] == 'MEDIUM'])
        }
    }
```

---

## Patterns

### Complete Supply Chain Audit

```python
def audit_supply_chain() -> dict:
    """Comprehensive supply chain security assessment"""
    return {
        'sbom': check_sbom_presence(),
        'slsa_level': assess_slsa_level(),
        'build_security': detect_build_security_issues(),
        'vulnerability_scanning': detect_vulnerability_scanning(),
        'sast': detect_sast_configuration(),
        'dependency_confusion': detect_dependency_confusion_risks(),
        'container_security': detect_container_security(),
        'overall_score': calculate_supply_chain_score()
    }

def calculate_supply_chain_score() -> dict:
    """Supply chain security score: 0-100"""
    score = 100
    deductions = []

    # SBOM (-15 if missing)
    if not check_sbom_presence()['has_sbom']:
        score -= 15
        deductions.append('Missing SBOM (-15)')

    # SLSA Level (-20 if < 2)
    slsa = assess_slsa_level()
    if slsa['slsa_level'] < 2:
        score -= 20
        deductions.append(f'SLSA Level {slsa["slsa_level"]} < 2 (-20)')

    # Build security issues
    build_issues = detect_build_security_issues()
    critical_build = len([i for i in build_issues if i['severity'] == 'CRITICAL'])
    score -= critical_build * 10
    if critical_build:
        deductions.append(f'{critical_build} critical build issues (-{critical_build * 10})')

    # Vulnerability scanning (-15 if none)
    vuln_scan = detect_vulnerability_scanning()
    if vuln_scan['coverage'] == 'NONE':
        score -= 15
        deductions.append('No vulnerability scanning (-15)')

    # SAST (-10 if none)
    sast = detect_sast_configuration()
    if sast['maturity'] == 'NONE':
        score -= 10
        deductions.append('No SAST configured (-10)')

    # Dependency confusion risks
    dep_confusion = detect_dependency_confusion_risks()
    critical_dep = len([i for i in dep_confusion if i['severity'] == 'CRITICAL'])
    score -= critical_dep * 15
    if critical_dep:
        deductions.append(f'{critical_dep} critical dependency issues (-{critical_dep * 15})')

    score = max(0, score)

    return {
        'score': score,
        'grade': (
            'A' if score >= 90 else
            'B' if score >= 75 else
            'C' if score >= 60 else
            'D' if score >= 40 else
            'F'
        ),
        'deductions': deductions
    }
```

---

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
