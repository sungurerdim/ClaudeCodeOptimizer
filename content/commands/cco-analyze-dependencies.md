---
id: cco-analyze-dependencies
description: Dependency graph, circular deps, unused deps
category: analysis
priority: normal
principles:
  - 'U_EVIDENCE_BASED'
  - 'U_DEPENDENCY_MANAGEMENT'
  - 'P_SUPPLY_CHAIN_SECURITY'
  - 'U_COMPLETE_REPORTING'
  - 'U_ROOT_CAUSE_ANALYSIS'
---

# Analyze Dependencies

Analyze **${PROJECT_NAME}** dependency graph, detect circular dependencies, and identify unused packages.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Comprehensive dependency analysis:
1. Build complete dependency graph
2. Detect circular dependencies
3. Identify unused dependencies
4. Find outdated packages
5. Analyze dependency health and security

**Output:** Dependency report with graph visualization and actionable recommendations.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, fast)
- Parse package manifests (package.json, requirements.txt, etc.)
- Extract import statements from source files
- Scan for unused dependencies

**Analysis & Reasoning**: Sonnet (Plan agent)
- Build dependency graph
- Detect circular dependencies
- Generate recommendations

**Execution Pattern**:
1. Launch Haiku to scan manifests and imports (parallel)
2. Build dependency graph
3. Use Sonnet for circular dependency detection
4. Generate comprehensive analysis report

---

## When to Use

**Use this command:**
- Before major refactoring
- When experiencing dependency conflicts
- During dependency audits
- To reduce bundle size
- When cleaning up legacy code

**Critical for:**
- Microservices with shared dependencies
- Large monorepos
- Projects with many dependencies (>20)

---

## Phase 1: Parse Package Manifests

Extract dependencies from package files:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import json
import re
from collections import defaultdict

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Dependency Manifest Analysis ===\n")
print(f"Project: {project_name}\n")

declared_deps = {
    "production": {},
    "development": {},
    "optional": {}
}

def parse_package_json(file_path):
    """Parse Node.js package.json"""
    try:
        data = json.loads(file_path.read_text())
        return {
            "production": data.get("dependencies", {}),
            "development": data.get("devDependencies", {}),
            "optional": data.get("optionalDependencies", {})
        }
    except:
        return None

def parse_requirements_txt(file_path):
    """Parse Python requirements.txt"""
    try:
        deps = {}
        for line in file_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                # Parse: package==version or package>=version
                match = re.match(r'([a-zA-Z0-9_-]+)([><=!]+.*)?', line)
                if match:
                    package = match.group(1)
                    version = match.group(2) or ""
                    deps[package] = version.strip()
        return {"production": deps, "development": {}, "optional": {}}
    except:
        return None

def parse_pyproject_toml(file_path):
    """Parse Python pyproject.toml"""
    try:
        import tomli
        data = tomli.loads(file_path.read_text())

        deps = {}
        dev_deps = {}

        # Poetry format
        if "tool" in data and "poetry" in data["tool"]:
            deps = data["tool"]["poetry"].get("dependencies", {})
            dev_deps = data["tool"]["poetry"].get("dev-dependencies", {})

        # PEP 621 format
        elif "project" in data:
            deps_list = data["project"].get("dependencies", [])
            for dep in deps_list:
                match = re.match(r'([a-zA-Z0-9_-]+)', dep)
                if match:
                    deps[match.group(1)] = dep

        return {"production": deps, "development": dev_deps, "optional": {}}
    except:
        return None

# Find and parse manifest files
manifest_files = {
    "package.json": parse_package_json,
    "requirements.txt": parse_requirements_txt,
    "pyproject.toml": parse_pyproject_toml
}

manifests_found = []

for manifest_name, parser in manifest_files.items():
    for manifest_path in project_root.rglob(manifest_name):
        # Skip node_modules and venv
        if 'node_modules' in str(manifest_path) or 'venv' in str(manifest_path):
            continue

        result = parser(manifest_path)
        if result:
            manifests_found.append({
                "path": str(manifest_path.relative_to(project_root)),
                "type": manifest_name,
                "deps": result
            })

            # Merge into declared_deps
            for dep_type in ["production", "development", "optional"]:
                declared_deps[dep_type].update(result[dep_type])

print(f"Manifests Found: {len(manifests_found)}")
for m in manifests_found:
    print(f"  - {m['path']}")
print()

# Display declared dependencies
total_prod = len(declared_deps["production"])
total_dev = len(declared_deps["development"])
total_opt = len(declared_deps["optional"])

print(f"Declared Dependencies:")
print(f"  Production: {total_prod}")
print(f"  Development: {total_dev}")
print(f"  Optional: {total_opt}")
print(f"  Total: {total_prod + total_dev + total_opt}")
print()
```

---

## Phase 2: Extract Import Statements

Scan source code for actual imports:

```python
print(f"=== Import Analysis ===\n")

actual_imports = defaultdict(set)

def extract_imports_python(file_path):
    """Extract Python imports"""
    imports = []
    try:
        content = file_path.read_text()
        # Match: import X, from X import Y
        patterns = [
            r'^\s*import\s+([\w\.]+)',
            r'^\s*from\s+([\w\.]+)\s+import',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            imports.extend(matches)
    except:
        pass
    return imports

def extract_imports_javascript(file_path):
    """Extract JavaScript/TypeScript imports"""
    imports = []
    try:
        content = file_path.read_text()
        patterns = [
            r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)',
            r'import\([\'"]([^\'"]+)[\'"]\)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
    except:
        pass
    return imports

# Detect primary language
source_extensions = {
    'Python': ['.py'],
    'JavaScript': ['.js', '.jsx'],
    'TypeScript': ['.ts', '.tsx']
}

# Determine language and scanner
primary_language = None
extract_fn = None

for lang, exts in source_extensions.items():
    for ext in exts:
        if list(project_root.rglob(f'*{ext}')):
            primary_language = lang
            if lang == 'Python':
                extract_fn = extract_imports_python
            else:
                extract_fn = extract_imports_javascript
            break
    if extract_fn:
        break

if not extract_fn:
    print("Could not determine primary language")
else:
    print(f"Scanning {primary_language} imports...")

    # Scan source files
    source_files = []
    if primary_language == 'Python':
        source_files = list(project_root.rglob('*.py'))
    else:
        source_files = list(project_root.rglob('*.js')) + list(project_root.rglob('*.ts'))

    # Exclude common directories
    excluded = ['node_modules', 'venv', '__pycache__', 'dist', 'build', '.git']
    source_files = [f for f in source_files if not any(ex in str(f) for ex in excluded)]

    print(f"Source files: {len(source_files)}")

    # Extract imports
    for file_path in source_files:
        imports = extract_fn(file_path)
        for imp in imports:
            # Get base package name
            base_package = imp.split('.')[0].split('/')[0]
            if not base_package.startswith('.'):  # Skip relative imports
                actual_imports[base_package].add(str(file_path.relative_to(project_root)))

    print(f"Unique imports found: {len(actual_imports)}")
    print()
```

---

## Phase 3: Detect Unused Dependencies

Compare declared vs actual:

```python
print(f"=== Unused Dependency Detection ===\n")

unused_deps = []

# Check each declared dependency
all_declared = set(declared_deps["production"].keys()) | set(declared_deps["development"].keys())

for package in all_declared:
    # Check if package is imported anywhere
    if package not in actual_imports:
        # Try common variations (e.g., 'express' might be imported as 'express')
        # or package-name vs package_name
        alt_names = [
            package.replace('-', '_'),
            package.replace('_', '-'),
            package.lower()
        ]

        found = any(alt in actual_imports for alt in alt_names)

        if not found:
            dep_type = "production" if package in declared_deps["production"] else "development"
            unused_deps.append({
                "package": package,
                "type": dep_type,
                "version": declared_deps[dep_type].get(package, "")
            })

if unused_deps:
    print(f"Unused Dependencies: {len(unused_deps)}\n")

    # Group by type
    unused_prod = [d for d in unused_deps if d["type"] == "production"]
    unused_dev = [d for d in unused_deps if d["type"] == "development"]

    if unused_prod:
        print("Production:")
        for dep in unused_prod[:10]:
            print(f"  - {dep['package']}{dep['version']}")
        if len(unused_prod) > 10:
            print(f"  ... and {len(unused_prod) - 10} more")
        print()

    if unused_dev:
        print("Development:")
        for dep in unused_dev[:10]:
            print(f"  - {dep['package']}{dep['version']}")
        if len(unused_dev) > 10:
            print(f"  ... and {len(unused_dev) - 10} more")
        print()

    # Calculate potential savings
    print("Potential Impact:")
    print(f"  - Remove {len(unused_deps)} unused packages")
    print(f"  - Reduce install time")
    print(f"  - Smaller node_modules / site-packages")
    print()
else:
    print("✓ No unused dependencies detected\n")
```

---

## Phase 4: Build Dependency Graph

Create import dependency graph:

```python
print(f"=== Dependency Graph ===\n")

# Build internal module graph
internal_graph = defaultdict(set)

def is_internal_import(imp_str):
    """Check if import is internal (relative or from src)"""
    return imp_str.startswith('.') or not any(imp_str.startswith(pkg) for pkg in all_declared)

# Re-scan for internal dependencies
for file_path in source_files[:200]:  # Limit for performance
    imports = extract_fn(file_path)

    file_module = str(file_path.relative_to(project_root))

    for imp in imports:
        if is_internal_import(imp):
            internal_graph[file_module].add(imp)

print(f"Internal Modules: {len(internal_graph)}")
print(f"Internal Dependencies: {sum(len(deps) for deps in internal_graph.values())}")
print()

# Show most connected modules
module_scores = []
for module, deps in internal_graph.items():
    # Count both outgoing (imports) and incoming (imported by)
    outgoing = len(deps)
    incoming = sum(1 for other_deps in internal_graph.values() if module in other_deps)
    module_scores.append({
        "module": module,
        "outgoing": outgoing,
        "incoming": incoming,
        "total": outgoing + incoming
    })

module_scores.sort(key=lambda x: x["total"], reverse=True)

print("Most Connected Modules:")
for i, mod in enumerate(module_scores[:10], 1):
    print(f"{i:2d}. {mod['module']:50s} (imports: {mod['outgoing']}, imported by: {mod['incoming']})")
print()
```

---

## Phase 5: Detect Circular Dependencies

Find circular import chains:

```python
print(f"=== Circular Dependency Detection ===\n")

def find_circular_deps(graph):
    """Detect cycles in dependency graph using DFS"""
    cycles = []
    visited = set()
    rec_stack = []

    def dfs(node, path):
        if node in rec_stack:
            # Found cycle
            cycle_start = rec_stack.index(node)
            cycle = rec_stack[cycle_start:] + [node]
            cycles.append(cycle)
            return

        if node in visited:
            return

        visited.add(node)
        rec_stack.append(node)

        for neighbor in graph.get(node, []):
            dfs(neighbor, path + [node])

        rec_stack.pop()

    # Run DFS from each node
    for node in graph:
        if node not in visited:
            dfs(node, [])

    return cycles

circular_deps = find_circular_deps(internal_graph)

if circular_deps:
    print(f"Circular Dependencies Found: {len(circular_deps)}\n")

    # Remove duplicates (same cycle, different starting point)
    unique_cycles = []
    for cycle in circular_deps:
        # Normalize cycle (start from smallest element)
        normalized = tuple(sorted(cycle))
        if normalized not in [tuple(sorted(c)) for c in unique_cycles]:
            unique_cycles.append(cycle)

    print(f"Unique Circular Chains: {len(unique_cycles)}\n")

    for i, cycle in enumerate(unique_cycles[:5], 1):
        print(f"{i}. Circular chain (length {len(cycle)}):")
        for j, module in enumerate(cycle):
            arrow = " → " if j < len(cycle) - 1 else ""
            print(f"   {module}{arrow}")
        print()

    if len(unique_cycles) > 5:
        print(f"... and {len(unique_cycles) - 5} more circular dependencies\n")

    print("Impact:")
    print("  - Can cause import errors")
    print("  - Makes code harder to understand")
    print("  - Prevents proper module loading")
    print("  - Blocks tree-shaking optimizations")
    print()
else:
    print("✓ No circular dependencies detected\n")
```

---

## Phase 6: Dependency Health Check

Check for outdated and vulnerable packages:

```python
print(f"=== Dependency Health Check ===\n")

# Note: Full implementation would query package registries
# This is a simplified version

health_issues = []

# Check for wildcard versions (security risk)
for dep_type in ["production", "development"]:
    for package, version in declared_deps[dep_type].items():
        if version and ('*' in version or 'latest' in version.lower()):
            health_issues.append({
                "package": package,
                "type": dep_type,
                "issue": "Wildcard version",
                "severity": "MEDIUM",
                "recommendation": "Pin to specific version"
            })

# Check for missing versions
for dep_type in ["production", "development"]:
    for package, version in declared_deps[dep_type].items():
        if not version or version == "":
            health_issues.append({
                "package": package,
                "type": dep_type,
                "issue": "No version specified",
                "severity": "LOW",
                "recommendation": "Specify version range"
            })

if health_issues:
    print(f"Health Issues: {len(health_issues)}\n")

    for issue in health_issues[:10]:
        print(f"[{issue['severity']}] {issue['package']} ({issue['type']})")
        print(f"  Issue: {issue['issue']}")
        print(f"  Fix: {issue['recommendation']}")
        print()

    if len(health_issues) > 10:
        print(f"... and {len(health_issues) - 10} more issues\n")
else:
    print("✓ No major health issues detected\n")

print("For security vulnerabilities, run:")
if primary_language == 'Python':
    print("  pip-audit")
    print("  safety check")
else:
    print("  npm audit")
    print("  yarn audit")
print()
```

---

## Phase 7: Dependency Size Analysis

Analyze package sizes and bloat:

```python
print(f"=== Dependency Size Analysis ===\n")

# This would require actual package installation
# Simplified version showing approach

print("Dependency Size Impact:")
print("(Install packages to get actual sizes)\n")

if primary_language in ['JavaScript', 'TypeScript']:
    print("To analyze bundle size:")
    print("  npm install -g webpack-bundle-analyzer")
    print("  webpack-bundle-analyzer dist/bundle.js")
    print()

    print("To find large packages:")
    print("  npx du -sh node_modules/*")
    print()
elif primary_language == 'Python':
    print("To analyze package sizes:")
    print("  pip list --format=columns")
    print("  du -sh venv/lib/python*/site-packages/*")
    print()

# Estimate impact
print(f"Estimated Impact of Removing {len(unused_deps)} Unused Deps:")
print(f"  - Faster installs")
print(f"  - Smaller Docker images")
print(f"  - Reduced security surface")
print()
```

---

## Phase 8: Transitive Dependencies

Analyze dependency tree depth:

```python
print(f"=== Transitive Dependencies ===\n")

# This requires package manager APIs
# Simplified version

print("To view full dependency tree:\n")

if primary_language == 'Python':
    print("  pip install pipdeptree")
    print("  pipdeptree")
    print()
    print("  # Or with poetry:")
    print("  poetry show --tree")
elif primary_language in ['JavaScript', 'TypeScript']:
    print("  npm ls")
    print("  # Or for specific package:")
    print("  npm ls <package-name>")
    print()
    print("  # Yarn:")
    print("  yarn why <package-name>")

print()

# Detect potential duplication
print("Common Issues with Transitive Dependencies:")
print("  - Multiple versions of same package")
print("  - Deep dependency chains (>5 levels)")
print("  - Conflicting version requirements")
print()
```

---

## Phase 9: Recommendations

Generate actionable recommendations:

```python
print(f"=== Recommendations ===\n")

recommendations = []

# Unused dependencies
if unused_deps:
    recommendations.append({
        "priority": "HIGH",
        "title": f"Remove {len(unused_deps)} unused dependencies",
        "actions": [
            f"Remove from manifest files",
            f"Run install to update lock files",
            f"Test thoroughly after removal"
        ],
        "commands": [
            f"# Review unused deps:",
            f"# {', '.join(d['package'] for d in unused_deps[:5])}"
        ]
    })

# Circular dependencies
if circular_deps:
    recommendations.append({
        "priority": "CRITICAL",
        "title": f"Break {len(unique_cycles)} circular dependency chains",
        "actions": [
            "Extract shared code to separate module",
            "Use dependency injection",
            "Introduce interfaces/protocols",
            "Refactor import structure"
        ]
    })

# Health issues
if health_issues:
    recommendations.append({
        "priority": "MEDIUM",
        "title": f"Fix {len(health_issues)} dependency health issues",
        "actions": [
            "Pin wildcard versions",
            "Specify version ranges",
            "Run security audit",
            "Update outdated packages"
        ]
    })

# General best practices
recommendations.append({
    "priority": "LOW",
    "title": "Follow dependency best practices",
    "actions": [
        "Use lock files (package-lock.json, poetry.lock)",
        "Regular dependency updates",
        "Automated security scanning",
        "Minimize production dependencies"
    ]
})

# Display
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. [{rec['priority']}] {rec['title']}")
    for action in rec['actions']:
        print(f"   - {action}")
    if 'commands' in rec:
        for cmd in rec['commands']:
            print(f"   {cmd}")
    print()
```

---

## Phase 10: Generate Report

Export dependency report:

```python
print(f"=== Export Report ===\n")

report = {
    "project": project_name,
    "analysis_date": "2025-11-10",
    "declared_dependencies": {
        "production": len(declared_deps["production"]),
        "development": len(declared_deps["development"]),
        "total": len(declared_deps["production"]) + len(declared_deps["development"])
    },
    "actual_imports": len(actual_imports),
    "unused_dependencies": len(unused_deps),
    "circular_dependencies": len(unique_cycles) if circular_deps else 0,
    "health_issues": len(health_issues),
    "unused_list": [d["package"] for d in unused_deps],
    "circular_chains": unique_cycles[:10] if circular_deps else [],
    "recommendations": len(recommendations)
}

report_path = project_root / "dependency-analysis-report.json"
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print(f"Report saved to: {report_path.name}")
print()

# Generate removal script
if unused_deps:
    script_lines = ["#!/bin/bash", "# Auto-generated script to remove unused dependencies", ""]

    if primary_language == 'Python':
        for dep in unused_deps:
            script_lines.append(f"pip uninstall -y {dep['package']}")
    else:
        for dep in unused_deps:
            script_lines.append(f"npm uninstall {dep['package']}")

    script_path = project_root / "remove-unused-deps.sh"
    script_path.write_text('\n'.join(script_lines))
    print(f"Removal script: {script_path.name}")
    print("Review before running!")
```

---

## Output Example

```
=== Dependency Manifest Analysis ===

Project: backend

Manifests Found: 2
  - package.json
  - package.json (services/auth)

Declared Dependencies:
  Production: 34
  Development: 18
  Optional: 2
  Total: 54

=== Import Analysis ===

Scanning JavaScript imports...
Source files: 147
Unique imports found: 28

=== Unused Dependency Detection ===

Unused Dependencies: 8

Production:
  - moment (^2.29.1)
  - lodash (^4.17.21)
  - axios (^0.27.2)

Development:
  - @types/jest (^28.1.0)
  - eslint-plugin-unused-imports (^2.0.0)

Potential Impact:
  - Remove 8 unused packages
  - Reduce install time
  - Smaller node_modules / site-packages

=== Dependency Graph ===

Internal Modules: 89
Internal Dependencies: 234

Most Connected Modules:
 1. src/utils/helpers.js                               (imports: 12, imported by: 45)
 2. src/config/database.js                             (imports: 5, imported by: 38)
 3. src/models/User.js                                 (imports: 8, imported by: 32)

=== Circular Dependency Detection ===

Circular Dependencies Found: 3

Unique Circular Chains: 2

1. Circular chain (length 3):
   src/services/auth/AuthService.js →
   src/services/user/UserService.js →
   src/models/User.js →
   src/services/auth/AuthService.js

2. Circular chain (length 2):
   src/api/routes/orders.js →
   src/api/routes/customers.js →
   src/api/routes/orders.js

Impact:
  - Can cause import errors
  - Makes code harder to understand
  - Prevents proper module loading
  - Blocks tree-shaking optimizations

=== Dependency Health Check ===

Health Issues: 5

[MEDIUM] express (production)
  Issue: Wildcard version
  Fix: Pin to specific version

[LOW] dotenv (production)
  Issue: No version specified
  Fix: Specify version range

✓ No major health issues detected

For security vulnerabilities, run:
  npm audit
  yarn audit

=== Recommendations ===

1. [HIGH] Remove 8 unused dependencies
   - Remove from manifest files
   - Run install to update lock files
   - Test thoroughly after removal
   # Review unused deps:
   # moment, lodash, axios, @types/jest, eslint-plugin-unused-imports

2. [CRITICAL] Break 2 circular dependency chains
   - Extract shared code to separate module
   - Use dependency injection
   - Introduce interfaces/protocols
   - Refactor import structure

3. [MEDIUM] Fix 5 dependency health issues
   - Pin wildcard versions
   - Specify version ranges
   - Run security audit
   - Update outdated packages

=== Export Report ===

Report saved to: dependency-analysis-report.json
Removal script: remove-unused-deps.sh
Review before running!
```

---

**Dependency Philosophy:** Dependencies are liabilities. Every package adds complexity, attack surface, and maintenance burden. Minimize ruthlessly.
