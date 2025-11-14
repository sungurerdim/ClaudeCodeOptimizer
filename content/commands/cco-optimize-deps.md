---
id: cco-optimize-deps
description: Optimize dependencies - remove unused, update outdated, fix vulnerabilities
category: devops
priority: high
principles:
  - 'U_DEPENDENCY_MANAGEMENT'
  - 'P_SUPPLY_CHAIN_SECURITY'
  - 'U_EVIDENCE_BASED'
  - 'U_CHANGE_VERIFICATION'
  - 'U_MINIMAL_TOUCH'
---

# Optimize Dependencies - Dependency Management & Security

Optimize dependencies for **${PROJECT_NAME}** by removing unused packages, updating outdated versions, and fixing security vulnerabilities.

**Project Type:** ${PROJECT_TYPE}
**Services:** ${SERVICES_COUNT}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Comprehensive dependency optimization across 6 dimensions:
1. **Unused Dependencies** - Remove packages never imported
2. **Outdated Dependencies** - Update to latest stable versions
3. **Security Vulnerabilities** - Fix known CVEs
4. **Duplicate Dependencies** - Consolidate across services
5. **Dependency Tree** - Reduce bloat, flatten tree
6. **Lighter Alternatives** - Suggest smaller replacements

**Output:** Optimized dependency files with security and performance improvements.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast dependency tree analysis
- Scan for unused imports
- Vulnerability database lookup

**Analysis & Reasoning**: Sonnet (Plan agent)
- Complex dependency conflict resolution
- Breaking change assessment
- Strategic update recommendations

**Execution Pattern**:
1. Launch Haiku agents for dependency scanning (parallel)
2. Check security databases for vulnerabilities
3. Use Sonnet for update strategy and conflict resolution
4. Generate dependency optimization report

---

## Phase 1: Discover Dependencies

Find all dependency files in the project:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Dependency Optimization for {project_name} ===\n")

print("Discovering dependency files...\n")
```

**Use Glob to find dependency files:**

```
Pattern: requirements.txt → Python
Pattern: package.json → Node.js
Pattern: go.mod → Go
Pattern: Cargo.toml → Rust
Pattern: pom.xml → Java
```

```python
# Collect all dependency files
dep_files = {
    "python": [],
    "node": [],
    "go": [],
    "rust": [],
    "java": []
}

# Python
python_files = list(project_root.glob("**/requirements.txt"))
dep_files["python"] = [str(f.relative_to(project_root)) for f in python_files]

# Node.js
node_files = list(project_root.glob("**/package.json"))
dep_files["node"] = [str(f.relative_to(project_root)) for f in node_files]

# Go
go_files = list(project_root.glob("**/go.mod"))
dep_files["go"] = [str(f.relative_to(project_root)) for f in go_files]

# Rust
rust_files = list(project_root.glob("**/Cargo.toml"))
dep_files["rust"] = [str(f.relative_to(project_root)) for f in rust_files]

# Display findings
total_files = sum(len(files) for files in dep_files.values())
print(f"Found {total_files} dependency files:\n")

for lang, files in dep_files.items():
    if files:
        print(f"{lang.capitalize()}:")
        for file in files:
            print(f"  - {file}")
        print()

# Determine primary language
primary_lang = max(dep_files.items(), key=lambda x: len(x[1]))[0]
print(f"Primary Language: {primary_lang}\n")
```

---

## Phase 2: Analyze Dependencies

### 2.1 Detect Unused Dependencies

**Python - Use Grep to find imports:**

```python
print(f"=== Analyzing Python Dependencies ===\n")

if dep_files["python"]:
    print("Checking for unused dependencies...\n")

    # Read requirements.txt
    requirements_path = project_root / "requirements.txt"
    if requirements_path.exists():
        requirements = []
        for line in requirements_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                # Extract package name (before ==, >=, etc.)
                pkg_name = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                requirements.append(pkg_name)

        print(f"Total dependencies: {len(requirements)}\n")

        # For each requirement, check if it's imported
        unused = []

        for pkg in requirements:
            # Normalize package name (pip install name → import name)
            # e.g., "python-dotenv" → "dotenv"
            import_name = pkg.replace("-", "_").lower()

            # Use Grep to search for imports
            # Pattern: ^import {pkg_name} OR ^from {pkg_name}
            # This is where you'd actually use Grep tool

            # Example result (simulated)
            imported = False  # Would come from Grep result

            if not imported:
                unused.append(pkg)

        if unused:
            print(f"Unused dependencies ({len(unused)}):")
            for pkg in unused:
                print(f"  - {pkg}")
            print()
        else:
            print("✓ No unused dependencies detected\n")
```

**Use Grep patterns:**

For each package in requirements.txt:
```
Pattern: ^import {package_name}
Pattern: ^from {package_name}
Output: files_with_matches
Path: **/*.py
```

If no matches → Package is unused

**Node.js - Use depcheck:**

```bash
# Install depcheck
npm install -g depcheck

# Run analysis
depcheck

# Output shows:
# - Unused dependencies
# - Unused devDependencies
# - Missing dependencies
```

---

### 2.2 Detect Outdated Dependencies

**Python - Use pip-audit or pip list --outdated:**

```bash
# Check outdated packages
pip list --outdated

# Example output:
# Package    Version  Latest   Type
# fastapi    0.95.0   0.104.1  wheel
# redis      4.5.0    5.0.1    wheel
```

```python
print("Checking for outdated dependencies...\n")

# Simulated outdated packages
outdated = [
    {
        "package": "fastapi",
        "current": "0.95.0",
        "latest": "0.104.1",
        "severity": "MEDIUM",
        "reason": "Bug fixes and performance improvements"
    },
    {
        "package": "redis",
        "current": "4.5.0",
        "latest": "5.0.1",
        "severity": "LOW",
        "reason": "New features available"
    },
    {
        "package": "pydantic",
        "current": "1.10.0",
        "latest": "2.5.0",
        "severity": "HIGH",
        "reason": "Major version upgrade with breaking changes"
    }
]

if outdated:
    print(f"Outdated dependencies ({len(outdated)}):\n")
    for pkg in outdated:
        print(f"  [{pkg['severity']}] {pkg['package']}")
        print(f"    Current: {pkg['current']}")
        print(f"    Latest:  {pkg['latest']}")
        print(f"    Reason:  {pkg['reason']}")
        print()
else:
    print("✓ All dependencies up to date\n")
```

**Node.js - Use npm outdated:**

```bash
npm outdated

# Example output:
# Package    Current  Wanted  Latest
# express    4.17.0   4.18.2  4.18.2
# lodash     4.17.20  4.17.21 4.17.21
```

---

### 2.3 Security Vulnerability Scan

**Python - Use pip-audit or safety:**

```bash
# Option 1: pip-audit (official)
pip install pip-audit
pip-audit

# Option 2: safety
pip install safety
safety check
```

```python
print("Scanning for security vulnerabilities...\n")

# Simulated vulnerabilities
vulnerabilities = [
    {
        "package": "urllib3",
        "version": "1.26.5",
        "cve": "CVE-2023-45803",
        "severity": "CRITICAL",
        "description": "Cookie request header isn't stripped during cross-origin redirects",
        "fixed_in": "1.26.18",
        "cvss": 9.1
    },
    {
        "package": "certifi",
        "version": "2022.12.7",
        "cve": "CVE-2023-37920",
        "severity": "HIGH",
        "description": "Removal of e-Tugra root certificate",
        "fixed_in": "2023.07.22",
        "cvss": 7.5
    }
]

if vulnerabilities:
    print(f"Security vulnerabilities ({len(vulnerabilities)}):\n")
    for vuln in vulnerabilities:
        print(f"  [{vuln['severity']}] {vuln['package']} {vuln['version']}")
        print(f"    CVE: {vuln['cve']} (CVSS: {vuln['cvss']})")
        print(f"    Description: {vuln['description']}")
        print(f"    Fixed in: {vuln['fixed_in']}")
        print()
else:
    print("✓ No known vulnerabilities detected\n")
```

**Node.js - Use npm audit:**

```bash
npm audit

# Fix automatically
npm audit fix

# Force major version updates (may break)
npm audit fix --force
```

---

### 2.4 Duplicate Dependencies (Multi-Service)

Check for version mismatches across services:

```python
print("Checking for duplicate dependencies across services...\n")

if len(dep_files["python"]) > 1:
    print("Analyzing Python dependencies across services:\n")

    # Parse all requirements.txt files
    all_deps = {}

    for req_file in dep_files["python"]:
        req_path = project_root / req_file
        service_name = req_file.split("/")[0] if "/" in req_file else "root"

        for line in req_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                # Parse package==version
                if "==" in line:
                    pkg, version = line.split("==", 1)
                    pkg = pkg.strip()
                    version = version.strip()

                    if pkg not in all_deps:
                        all_deps[pkg] = {}

                    all_deps[pkg][service_name] = version

    # Find duplicates with different versions
    duplicates = []

    for pkg, versions in all_deps.items():
        if len(versions) > 1:
            unique_versions = set(versions.values())
            if len(unique_versions) > 1:
                duplicates.append({
                    "package": pkg,
                    "versions": versions
                })

    if duplicates:
        print(f"Version mismatches ({len(duplicates)}):\n")
        for dup in duplicates:
            print(f"  {dup['package']}:")
            for service, version in dup['versions'].items():
                print(f"    {service}: {version}")
            print()

        print("Recommendation: Consolidate to root requirements.txt or use shared/")
        print()
    else:
        print("✓ No version mismatches detected\n")
```

---

### 2.5 Dependency Tree Analysis

**Python - Use pipdeptree:**

```bash
pip install pipdeptree
pipdeptree

# Example output:
# fastapi==0.104.1
#   ├── pydantic [required: >=1.7.4, installed: 2.5.0]
#   │   └── typing-extensions [required: >=4.6.1, installed: 4.8.0]
#   └── starlette [required: >=0.27.0, installed: 0.27.0]
```

```python
print("Analyzing dependency tree depth...\n")

# Simulated tree analysis
tree_analysis = {
    "total_deps": 45,
    "direct_deps": 12,
    "transitive_deps": 33,
    "max_depth": 5,
    "heavy_deps": [
        {
            "package": "tensorflow",
            "size": "500 MB",
            "transitive_count": 25,
            "reason": "Large ML library with many dependencies"
        }
    ]
}

print(f"Dependency Tree:")
print(f"  Direct dependencies: {tree_analysis['direct_deps']}")
print(f"  Transitive dependencies: {tree_analysis['transitive_deps']}")
print(f"  Total: {tree_analysis['total_deps']}")
print(f"  Max depth: {tree_analysis['max_depth']}")
print()

if tree_analysis['heavy_deps']:
    print("Heavy dependencies (consider alternatives):\n")
    for dep in tree_analysis['heavy_deps']:
        print(f"  {dep['package']} ({dep['size']})")
        print(f"    Transitive: {dep['transitive_count']} packages")
        print(f"    Reason: {dep['reason']}")
        print()
```

---

### 2.6 Suggest Lighter Alternatives

```python
print("Suggesting lighter alternatives...\n")

alternatives = [
    {
        "package": "requests",
        "size": "500 KB",
        "alternative": "httpx",
        "alternative_size": "300 KB",
        "savings": "200 KB",
        "note": "Modern alternative with async support"
    },
    {
        "package": "pandas",
        "size": "40 MB",
        "alternative": "polars",
        "alternative_size": "15 MB",
        "savings": "25 MB",
        "note": "Faster and more memory-efficient (Rust-based)"
    },
    {
        "package": "pillow",
        "size": "3 MB",
        "alternative": "pillow-simd",
        "alternative_size": "3 MB",
        "savings": "0 MB (but 4-6x faster)",
        "note": "Drop-in replacement with SIMD optimizations"
    }
]

if alternatives:
    print(f"Lighter alternatives available ({len(alternatives)}):\n")
    for alt in alternatives:
        print(f"  {alt['package']} ({alt['size']})")
        print(f"    → {alt['alternative']} ({alt['alternative_size']})")
        print(f"    Savings: {alt['savings']}")
        print(f"    Note: {alt['note']}")
        print()
```

---

## Phase 3: Optimization Summary

```python
print(f"=== Optimization Summary ===\n")

# Calculate total issues
total_issues = (
    len(unused) +
    len(outdated) +
    len(vulnerabilities) +
    len(duplicates)
)

print(f"Total Issues: {total_issues}\n")

# By category
print("By Category:")
print(f"  Unused: {len(unused)}")
print(f"  Outdated: {len(outdated)}")
print(f"  Vulnerabilities: {len(vulnerabilities)} ({sum(1 for v in vulnerabilities if v['severity'] == 'CRITICAL')} critical)")
print(f"  Duplicates: {len(duplicates)}")
print()

# Potential improvements
print("Potential Improvements:")
print()

# Size savings
if unused:
    print(f"  Remove {len(unused)} unused packages")
    print(f"  Estimated savings: ~{len(unused) * 5} MB")  # Average 5 MB per package
    print()

# Security improvements
critical_vulns = [v for v in vulnerabilities if v['severity'] == 'CRITICAL']
if critical_vulns:
    print(f"  Fix {len(critical_vulns)} CRITICAL vulnerabilities")
    print(f"  Fix {len(vulnerabilities) - len(critical_vulns)} other vulnerabilities")
    print()

# Alternative savings
if alternatives:
    total_savings = sum(
        int(alt['savings'].replace(' MB', '').replace(' KB', '').replace('~', ''))
        for alt in alternatives
        if 'MB' in alt['savings']
    )
    print(f"  Switch to lighter alternatives")
    print(f"  Estimated savings: ~{total_savings} MB")
    print()
```

---

## Phase 4: Auto-Fix Options

Offer automated fixes for safe changes:

```python
print(f"=== Auto-Fix Options ===\n")

print("Safe auto-fixes available:\n")

# 1. Remove unused dependencies
if unused:
    print(f"1. Remove {len(unused)} unused dependencies")
    print("   Command: /cco-optimize-deps --remove-unused")
    print()

# 2. Update non-breaking versions
safe_updates = [pkg for pkg in outdated if pkg['severity'] != 'HIGH']
if safe_updates:
    print(f"2. Update {len(safe_updates)} packages (patch/minor versions)")
    print("   Command: /cco-optimize-deps --update-safe")
    print()

# 3. Fix security vulnerabilities
if vulnerabilities:
    print(f"3. Fix {len(vulnerabilities)} security vulnerabilities")
    print("   Command: /cco-optimize-deps --fix-security")
    print()

# 4. Consolidate duplicates
if duplicates:
    print(f"4. Consolidate {len(duplicates)} duplicate dependencies")
    print("   Command: /cco-optimize-deps --consolidate")
    print()

print("Or run all auto-fixes:")
print("  /cco-optimize-deps --auto")
print()
```

**Use AskUserQuestion for confirmation:**

```
Question: Which optimizations would you like to apply?
multiSelect: true
Options:
1. label: "Remove unused dependencies"
   description: f"Remove {len(unused)} packages never imported ({len(unused) * 5} MB savings)"

2. label: "Update safe packages"
   description: f"Update {len(safe_updates)} packages to latest patch/minor versions"

3. label: "Fix security vulnerabilities"
   description: f"Update {len(vulnerabilities)} packages with known CVEs"

4. label: "Consolidate duplicates"
   description: f"Merge {len(duplicates)} version mismatches across services"
```

---

## Phase 5: Apply Optimizations

If user selects optimizations:

```python
print(f"=== Applying Optimizations ===\n")

# Backup current state
print("Creating backup...\n")
print("git stash push -m 'CCO: backup before dependency optimization'")
print()
```

### 5.1 Remove Unused Dependencies

```python
print("Step 1: Removing unused dependencies...\n")

for pkg in unused:
    print(f"  - Removing {pkg}")

    # For Python
    # Update requirements.txt
    req_path = project_root / "requirements.txt"
    content = req_path.read_text()

    # Remove lines containing the package
    new_content = "\n".join(
        line for line in content.splitlines()
        if not line.strip().startswith(pkg)
    )

    req_path.write_text(new_content)

print(f"\n✓ Removed {len(unused)} unused dependencies\n")
```

### 5.2 Update Safe Packages

```python
print("Step 2: Updating safe packages...\n")

for pkg in safe_updates:
    print(f"  - Updating {pkg['package']}: {pkg['current']} → {pkg['latest']}")

    # For Python
    req_path = project_root / "requirements.txt"
    content = req_path.read_text()

    # Replace version
    new_content = content.replace(
        f"{pkg['package']}=={pkg['current']}",
        f"{pkg['package']}=={pkg['latest']}"
    )

    req_path.write_text(new_content)

print(f"\n✓ Updated {len(safe_updates)} packages\n")
```

### 5.3 Fix Security Vulnerabilities

```python
print("Step 3: Fixing security vulnerabilities...\n")

for vuln in vulnerabilities:
    print(f"  - Fixing {vuln['package']}: {vuln['version']} → {vuln['fixed_in']}")
    print(f"    ({vuln['cve']} - {vuln['severity']})")

    # Update to fixed version
    req_path = project_root / "requirements.txt"
    content = req_path.read_text()

    new_content = content.replace(
        f"{vuln['package']}=={vuln['version']}",
        f"{vuln['package']}=={vuln['fixed_in']}"
    )

    req_path.write_text(new_content)

print(f"\n✓ Fixed {len(vulnerabilities)} vulnerabilities\n")
```

### 5.4 Consolidate Duplicates

```python
print("Step 4: Consolidating duplicate dependencies...\n")

for dup in duplicates:
    # Choose latest version
    versions = list(dup['versions'].values())
    latest_version = max(versions)  # Simple comparison (works for most semantic versions)

    print(f"  - {dup['package']}: consolidating to {latest_version}")

    # Update all services to use latest version
    for service, version in dup['versions'].items():
        if version != latest_version:
            service_req = project_root / service / "requirements.txt"
            if service_req.exists():
                content = service_req.read_text()
                new_content = content.replace(
                    f"{dup['package']}=={version}",
                    f"{dup['package']}=={latest_version}"
                )
                service_req.write_text(new_content)
                print(f"    Updated {service}: {version} → {latest_version}")

print(f"\n✓ Consolidated {len(duplicates)} dependencies\n")
```

---

## Phase 6: Verification

Test that dependencies work after optimization:

```python
print(f"=== Verification ===\n")

print("Step 1: Reinstalling dependencies...\n")
```

**Python:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Verify installation
pip check
```

**Node.js:**
```bash
# Reinstall
npm ci

# Verify
npm ls
```

```python
print("Step 2: Running tests...\n")
```

**Run project tests:**
```bash
# Python
pytest

# Node.js
npm test
```

```python
print("Step 3: Verification results:\n")

# If tests pass
print("✓ All tests passed")
print("✓ Dependencies optimized successfully")
print()

print("Changes:")
print(f"  - Removed: {len(unused)} packages")
print(f"  - Updated: {len(safe_updates)} packages")
print(f"  - Fixed: {len(vulnerabilities)} vulnerabilities")
print(f"  - Consolidated: {len(duplicates)} duplicates")
print()

print("Next steps:")
print("1. Review changes: git diff requirements.txt")
print("2. Test thoroughly in development environment")
print("3. Commit: git add requirements.txt && git commit -m 'Optimize dependencies'")
print()
```

**If tests fail:**

```python
# Rollback
print("❌ Tests failed. Rolling back changes...\n")
print("git stash pop")
print()
print("Please review failures and apply optimizations manually.")
```

---

## Language-Specific Commands

### Python

```bash
# Remove unused
pip-autoremove <package>

# Update all
pip list --outdated | cut -d ' ' -f1 | xargs -n1 pip install -U

# Security scan
pip-audit
safety check

# Generate lock file
pip freeze > requirements.txt
```

### Node.js

```bash
# Remove unused
npm prune

# Update all (interactive)
npx npm-check-updates -u
npm install

# Security scan
npm audit
npm audit fix

# Generate lock file
npm install  # Updates package-lock.json
```

### Go

```bash
# Remove unused
go mod tidy

# Update all
go get -u ./...
go mod tidy

# Security scan
go list -json -m all | nancy sleuth

# Verify
go mod verify
```

### Rust

```bash
# Update all
cargo update

# Security scan
cargo audit

# Remove unused (manual - check Cargo.lock)
cargo tree
```

---

## Best Practices

```python
print(f"=== Dependency Management Best Practices ===\n")
```

### 1. Pin Exact Versions

```txt
# ✅ GOOD: Exact versions
fastapi==0.104.1
pydantic==2.5.0

# ❌ BAD: Unpinned versions
fastapi
pydantic>=2.0
```

**Why:** Reproducible builds, avoid breaking changes

### 2. Separate Dev Dependencies

```txt
# Python: requirements.txt (production)
fastapi==0.104.1
redis==5.0.1

# requirements-dev.txt (development)
pytest==7.4.3
black==23.12.1
ruff==0.1.8
```

**Why:** Smaller production images, faster deployments

### 3. Use Lock Files

```bash
# Python
pip freeze > requirements.txt

# Node.js
npm ci  # Uses package-lock.json

# Go
go mod download  # Uses go.sum

# Rust
cargo build  # Uses Cargo.lock
```

**Why:** Deterministic builds across environments

### 4. Regular Audits

```bash
# Weekly security scan
pip-audit
npm audit

# Monthly dependency updates
/cco-optimize-deps --update-safe

# Quarterly major version reviews
/cco-optimize-deps --check-major
```

### 5. Multi-Service Consolidation

```txt
# ❌ BAD: Each service has own requirements.txt
services/api/requirements.txt:     fastapi==0.95.0
services/worker/requirements.txt:  fastapi==0.104.1

# ✅ GOOD: Shared dependencies
requirements.txt:                  fastapi==0.104.1
services/api/requirements.txt:     -r ../../requirements.txt
services/worker/requirements.txt:  -r ../../requirements.txt
```

---

## Output Example

```
=== Dependency Optimization for backend ===

Discovering dependency files...

Found 5 dependency files:

Python:
  - requirements.txt
  - services/api/requirements.txt
  - services/worker/requirements.txt

Node:
  - package.json

Primary Language: python

=== Analyzing Python Dependencies ===

Checking for unused dependencies...

Total dependencies: 25

Unused dependencies (3):
  - colorama
  - wheel
  - setuptools

Checking for outdated dependencies...

Outdated dependencies (5):

  [MEDIUM] fastapi
    Current: 0.95.0
    Latest:  0.104.1
    Reason:  Bug fixes and performance improvements

  [HIGH] pydantic
    Current: 1.10.0
    Latest:  2.5.0
    Reason:  Major version upgrade with breaking changes

Scanning for security vulnerabilities...

Security vulnerabilities (2):

  [CRITICAL] urllib3 1.26.5
    CVE: CVE-2023-45803 (CVSS: 9.1)
    Description: Cookie request header isn't stripped during cross-origin redirects
    Fixed in: 1.26.18

  [HIGH] certifi 2022.12.7
    CVE: CVE-2023-37920 (CVSS: 7.5)
    Description: Removal of e-Tugra root certificate
    Fixed in: 2023.07.22

Checking for duplicate dependencies across services...

Version mismatches (2):

  fastapi:
    root: 0.95.0
    services/api: 0.104.1
    services/worker: 0.95.0

  redis:
    root: 4.5.0
    services/api: 5.0.1

=== Optimization Summary ===

Total Issues: 12

By Category:
  Unused: 3
  Outdated: 5
  Vulnerabilities: 2 (1 critical)
  Duplicates: 2

Potential Improvements:

  Remove 3 unused packages
  Estimated savings: ~15 MB

  Fix 1 CRITICAL vulnerabilities
  Fix 1 other vulnerabilities

=== Auto-Fix Options ===

Safe auto-fixes available:

1. Remove 3 unused dependencies
   Command: /cco-optimize-deps --remove-unused

2. Update 4 packages (patch/minor versions)
   Command: /cco-optimize-deps --update-safe

3. Fix 2 security vulnerabilities
   Command: /cco-optimize-deps --fix-security

4. Consolidate 2 duplicate dependencies
   Command: /cco-optimize-deps --consolidate

Or run all auto-fixes:
  /cco-optimize-deps --auto

[User selects all optimizations]

=== Applying Optimizations ===

Creating backup...
git stash push -m 'CCO: backup before dependency optimization'

Step 1: Removing unused dependencies...
  - Removing colorama
  - Removing wheel
  - Removing setuptools

✓ Removed 3 unused dependencies

Step 2: Updating safe packages...
  - Updating fastapi: 0.95.0 → 0.104.1
  - Updating redis: 4.5.0 → 5.0.1

✓ Updated 2 packages

Step 3: Fixing security vulnerabilities...
  - Fixing urllib3: 1.26.5 → 1.26.18
    (CVE-2023-45803 - CRITICAL)
  - Fixing certifi: 2022.12.7 → 2023.07.22
    (CVE-2023-37920 - HIGH)

✓ Fixed 2 vulnerabilities

Step 4: Consolidating duplicate dependencies...
  - fastapi: consolidating to 0.104.1
    Updated root: 0.95.0 → 0.104.1
    Updated services/worker: 0.95.0 → 0.104.1
  - redis: consolidating to 5.0.1
    Updated root: 4.5.0 → 5.0.1

✓ Consolidated 2 dependencies

=== Verification ===

Step 1: Reinstalling dependencies...
pip install -r requirements.txt
✓ Installation successful

Step 2: Running tests...
pytest
✓ All tests passed (45 passed)

Step 3: Verification results:

✓ All tests passed
✓ Dependencies optimized successfully

Changes:
  - Removed: 3 packages
  - Updated: 2 packages
  - Fixed: 2 vulnerabilities
  - Consolidated: 2 duplicates

Next steps:
1. Review changes: git diff requirements.txt
2. Test thoroughly in development environment
3. Commit: git add requirements.txt && git commit -m 'Optimize dependencies'
```

---

## Quick Optimization Modes

```bash
# Full optimization (default)
/cco-optimize-deps

# Only remove unused
/cco-optimize-deps --remove-unused

# Only update safe packages
/cco-optimize-deps --update-safe

# Only fix security issues
/cco-optimize-deps --fix-security

# Only consolidate duplicates
/cco-optimize-deps --consolidate

# Auto-apply all safe fixes
/cco-optimize-deps --auto

# Dry-run (detect only, no changes)
/cco-optimize-deps --dry-run
```

---

## Integration with Other Commands

```bash
# Before deployment, optimize dependencies
/cco-optimize-deps && /cco-optimize-docker

# Complete DevOps workflow
/cco-optimize-deps && /cco-optimize-docker && /cco-generate-ci

# Weekly maintenance
/cco-optimize-deps --fix-security && /cco-audit-security
```

---

**Dependency Philosophy:** Keep dependencies minimal, updated, and secure. Less is more!
