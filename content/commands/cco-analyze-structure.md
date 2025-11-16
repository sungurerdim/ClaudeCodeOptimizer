---
id: cco-analyze-structure
description: Analyze codebase structure and architectural patterns
category: analysis
priority: normal
principles:
  - 'U_EVIDENCE_BASED'
  - 'U_ROOT_CAUSE_ANALYSIS'
  - 'C_FOLLOW_PATTERNS'
  - 'U_NO_OVERENGINEERING'
  - 'U_COMPLETE_REPORTING'
---

# Analyze Codebase Structure

Analyze **${PROJECT_NAME}** architectural patterns, directory organization, and code structure.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Understand codebase organization: structure, patterns, inconsistencies, and coupling analysis.

**Output:** Structure analysis with architectural diagram and recommendations.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast directory tree traversal
- File and module enumeration
- Import/dependency extraction

**Analysis & Reasoning**: Sonnet (Plan agent)
- Pattern recognition and classification
- Architectural analysis
- Recommendations generation

**Execution Pattern**:
1. Launch Haiku agent to scan directory structure (fast)
2. Analyze file organization and naming patterns
3. Use Sonnet for architectural pattern detection
4. Generate structure diagram and recommendations

---

---

## Phase 1: Directory Tree Analysis

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import json
from collections import defaultdict

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Directory Structure Analysis ===\n")
print(f"Project: {project_name}\n")

# Build directory tree
def build_tree(path: Path, max_depth: int = 5, current_depth: int = 0):
    """Build directory tree structure"""
    if current_depth >= max_depth:
        return None

    tree = {
        "name": path.name,
        "path": str(path.relative_to(project_root)),
        "type": "directory" if path.is_dir() else "file",
        "children": []
    }

    if path.is_dir():
        try:
            for child in sorted(path.iterdir()):
                # Skip common ignore patterns
                if child.name.startswith('.') or child.name in ['node_modules', '__pycache__', 'venv', 'dist', 'build']:
                    continue

                child_tree = build_tree(child, max_depth, current_depth + 1)
                if child_tree:
                    tree["children"].append(child_tree)
        except PermissionError:
            pass

    return tree

tree = build_tree(project_root)

# Print tree visualization
def print_tree(node, prefix="", is_last=True):
    """Print tree with ASCII art"""
    if not node:
        return

    connector = "└── " if is_last else "├── "
    print(f"{prefix}{connector}{node['name']}")

    if node['type'] == 'directory' and node['children']:
        extension = "    " if is_last else "│   "
        for i, child in enumerate(node['children']):
            print_tree(child, prefix + extension, i == len(node['children']) - 1)

print("Directory Tree:")
print(f"{tree['name']}/")
for i, child in enumerate(tree['children']):
    print_tree(child, "", i == len(tree['children']) - 1)
print()

# Collect statistics
stats = {
    "total_dirs": 0,
    "total_files": 0,
    "by_extension": defaultdict(int),
    "by_directory": defaultdict(int)
}

def collect_stats(node, parent_dir=""):
    """Collect file and directory statistics"""
    if node['type'] == 'directory':
        stats["total_dirs"] += 1
        for child in node['children']:
            collect_stats(child, node['name'])
    else:
        stats["total_files"] += 1
        ext = Path(node['name']).suffix or 'no_extension'
        stats["by_extension"][ext] += 1
        stats["by_directory"][parent_dir] += 1

collect_stats(tree)

print(f"Statistics:")
print(f"- Total Directories: {stats['total_dirs']}")
print(f"- Total Files: {stats['total_files']}")
print()
```

---

## Phase 2: File Type Distribution

```python
print(f"=== File Type Distribution ===\n")

# Sort by count
sorted_extensions = sorted(stats["by_extension"].items(), key=lambda x: x[1], reverse=True)

print("File Types:")
for ext, count in sorted_extensions[:10]:
    percentage = (count / stats['total_files']) * 100
    bar_length = int(percentage / 2)
    bar = "█" * bar_length
    print(f"{ext:15s} {count:4d} ({percentage:5.1f}%) {bar}")

if len(sorted_extensions) > 10:
    others = sum(count for _, count in sorted_extensions[10:])
    print(f"{'Others':15s} {others:4d}")
print()

# Identify primary language
language_indicators = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.c': 'C'
}

primary_language = None
max_count = 0
for ext, count in sorted_extensions:
    if ext in language_indicators and count > max_count:
        primary_language = language_indicators[ext]
        max_count = count

if primary_language:
    print(f"Primary Language: {primary_language} ({max_count} files)")
else:
    print("Primary Language: Unknown")
print()
```

---

## Phase 3: Detect Architectural Patterns

```python
print(f"=== Architectural Pattern Detection ===\n")

# Common directory patterns
patterns_detected = []

def has_directory(name):
    """Check if directory exists in tree"""
    return any(name.lower() in str(p).lower() for p in project_root.rglob('*') if p.is_dir())

# MVC Pattern
if has_directory('models') and has_directory('views') and has_directory('controllers'):
    patterns_detected.append({
        "pattern": "MVC (Model-View-Controller)",
        "confidence": "HIGH",
        "evidence": ["models/", "views/", "controllers/"]
    })

# Clean Architecture / Layered
if has_directory('domain') or has_directory('core'):
    if has_directory('infrastructure') or has_directory('adapters'):
        patterns_detected.append({
            "pattern": "Clean Architecture / Hexagonal",
            "confidence": "HIGH",
            "evidence": ["domain/", "infrastructure/"]
        })

# Microservices
if has_directory('services') or has_directory('apps'):
    services_dir = project_root / 'services' if has_directory('services') else project_root / 'apps'
    if services_dir.exists():
        num_services = len([d for d in services_dir.iterdir() if d.is_dir()])
        if num_services > 1:
            patterns_detected.append({
                "pattern": "Microservices Architecture",
                "confidence": "HIGH",
                "evidence": [f"services/ ({num_services} services)"]
            })

# Feature-based structure
if has_directory('features') or has_directory('modules'):
    patterns_detected.append({
        "pattern": "Feature-based / Modular",
        "confidence": "MEDIUM",
        "evidence": ["features/", "modules/"]
    })

# DDD (Domain-Driven Design)
if has_directory('domain') and has_directory('application'):
    patterns_detected.append({
        "pattern": "Domain-Driven Design (DDD)",
        "confidence": "MEDIUM",
        "evidence": ["domain/", "application/"]
    })

# API-first
if has_directory('api') or has_directory('routes') or has_directory('endpoints'):
    patterns_detected.append({
        "pattern": "API-First / REST",
        "confidence": "MEDIUM",
        "evidence": ["api/", "routes/"]
    })

if patterns_detected:
    print("Detected Patterns:")
    for p in patterns_detected:
        print(f"- {p['pattern']} (Confidence: {p['confidence']})")
        print(f"  Evidence: {', '.join(p['evidence'])}")
    print()
else:
    print("No standard architectural patterns detected")
    print("Codebase may use custom or flat structure")
    print()
```

---

## Phase 4: Module Organization Analysis

```python
print(f"=== Module Organization ===\n")

# Find all module directories (containing __init__.py for Python)
modules = []

if primary_language == 'Python':
    for init_file in project_root.rglob('__init__.py'):
        module_dir = init_file.parent
        if module_dir != project_root:
            modules.append(module_dir)
elif primary_language in ['JavaScript', 'TypeScript']:
    # Look for package.json or index files
    for pkg_file in project_root.rglob('package.json'):
        modules.append(pkg_file.parent)

print(f"Modules Found: {len(modules)}")

if modules:
    # Analyze module sizes
    module_stats = []
    for module in modules[:20]:  # Limit to 20 for display
        files = list(module.rglob('*.py')) if primary_language == 'Python' else list(module.rglob('*.js'))
        loc = 0
        for f in files:
            try:
                loc += len(f.read_text().splitlines())
            except:
                pass

        module_stats.append({
            "path": str(module.relative_to(project_root)),
            "files": len(files),
            "loc": loc
        })

    # Sort by LOC
    module_stats.sort(key=lambda x: x['loc'], reverse=True)

    print("\nTop Modules by Size:")
    for i, mod in enumerate(module_stats[:10], 1):
        print(f"{i:2d}. {mod['path']:40s} {mod['files']:3d} files, {mod['loc']:6d} LOC")
    print()

# Check for common organizational issues
issues = []

# Issue: Too many top-level files
top_level_files = [f for f in project_root.iterdir() if f.is_file() and not f.name.startswith('.')]
if len(top_level_files) > 10:
    issues.append({
        "type": "Organization",
        "severity": "MEDIUM",
        "issue": f"{len(top_level_files)} files in root directory",
        "recommendation": "Consider organizing files into subdirectories"
    })

# Issue: Flat structure with many files
src_dir = project_root / 'src'
if src_dir.exists():
    src_files = list(src_dir.glob('*.py'))
    if len(src_files) > 20:
        issues.append({
            "type": "Organization",
            "severity": "LOW",
            "issue": f"{len(src_files)} files in src/ without subdirectories",
            "recommendation": "Consider grouping related files into modules"
        })

if issues:
    print("Organizational Issues:")
    for issue in issues:
        print(f"[{issue['severity']}] {issue['issue']}")
        print(f"  → {issue['recommendation']}")
    print()
```

---

## Phase 5: Dependency Analysis

```python
print(f"=== Dependency Analysis ===\n")

import re

# Extract imports from source files
imports = defaultdict(list)

def extract_imports_python(file_path):
    """Extract Python imports"""
    try:
        content = file_path.read_text()
        # Match: import X, from X import Y
        import_pattern = r'(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))'
        matches = re.findall(import_pattern, content)
        return [m[0] or m[1] for m in matches]
    except:
        return []

def extract_imports_javascript(file_path):
    """Extract JavaScript/TypeScript imports"""
    try:
        content = file_path.read_text()
        # Match: import X from 'Y', require('Y')
        import_pattern = r'(?:import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]|require\([\'"]([^\'"]+)[\'"]\))'
        matches = re.findall(import_pattern, content)
        return [m[0] or m[1] for m in matches]
    except:
        return []

# Scan files for imports
source_files = []
if primary_language == 'Python':
    source_files = list(project_root.rglob('*.py'))
    extract_fn = extract_imports_python
elif primary_language in ['JavaScript', 'TypeScript']:
    source_files = list(project_root.rglob('*.js')) + list(project_root.rglob('*.ts'))
    extract_fn = extract_imports_javascript
else:
    print("Import analysis not supported for this language")
    extract_fn = None

if extract_fn:
    for file_path in source_files[:100]:  # Limit to 100 files
        file_imports = extract_fn(file_path)
        for imp in file_imports:
            imports[imp].append(str(file_path.relative_to(project_root)))

    # Separate internal vs external
    internal_imports = {}
    external_imports = {}

    for imp, files in imports.items():
        if imp.startswith('.') or not any(c in imp for c in ['.', '/']):
            internal_imports[imp] = len(files)
        else:
            external_imports[imp] = len(files)

    # Display top external dependencies
    sorted_external = sorted(external_imports.items(), key=lambda x: x[1], reverse=True)

    print(f"External Dependencies: {len(sorted_external)}")
    print("\nMost Used External Libraries:")
    for imp, count in sorted_external[:15]:
        print(f"  {imp:30s} (used in {count} files)")
    print()

    # Display top internal dependencies
    sorted_internal = sorted(internal_imports.items(), key=lambda x: x[1], reverse=True)

    print(f"Internal Modules: {len(sorted_internal)}")
    print("\nMost Referenced Internal Modules:")
    for imp, count in sorted_internal[:10]:
        print(f"  {imp:30s} (used in {count} files)")
    print()
```

---

## Phase 6: Code Organization Quality

```python
print(f"=== Code Organization Quality ===\n")

quality_metrics = {
    "directory_depth": 0,
    "module_cohesion": 0,
    "naming_consistency": 0,
    "separation_of_concerns": 0
}

# 1. Directory depth (optimal: 3-5 levels)
max_depth = 0
for p in project_root.rglob('*'):
    if p.is_file():
        depth = len(p.relative_to(project_root).parts)
        max_depth = max(max_depth, depth)

quality_metrics["directory_depth"] = max_depth

print(f"Directory Depth: {max_depth} levels")
if max_depth <= 5:
    print("  ✓ Good: Shallow hierarchy (easy to navigate)")
elif max_depth <= 8:
    print("  ~ OK: Moderate hierarchy")
else:
    print("  ✗ Poor: Deep hierarchy (hard to navigate)")
print()

# 2. Naming consistency
naming_patterns = defaultdict(int)
for d in project_root.rglob('*'):
    if d.is_dir() and d.name not in ['.git', '__pycache__', 'node_modules']:
        # Check naming convention
        if '_' in d.name:
            naming_patterns['snake_case'] += 1
        elif '-' in d.name:
            naming_patterns['kebab-case'] += 1
        elif d.name[0].isupper():
            naming_patterns['PascalCase'] += 1
        else:
            naming_patterns['lowercase'] += 1

if naming_patterns:
    dominant_pattern = max(naming_patterns.items(), key=lambda x: x[1])
    consistency_ratio = dominant_pattern[1] / sum(naming_patterns.values())

    print(f"Naming Convention:")
    print(f"  Dominant: {dominant_pattern[0]} ({consistency_ratio*100:.1f}% consistent)")

    if consistency_ratio >= 0.8:
        print("  ✓ Good: Consistent naming")
    elif consistency_ratio >= 0.6:
        print("  ~ OK: Mostly consistent")
    else:
        print("  ✗ Poor: Inconsistent naming")
    print()

# 3. Separation of concerns
concerns = {
    'tests': 0,
    'config': 0,
    'docs': 0,
    'scripts': 0,
    'source': 0
}

for d in project_root.rglob('*'):
    if d.is_dir():
        name = d.name.lower()
        if 'test' in name:
            concerns['tests'] += 1
        elif 'config' in name or 'settings' in name:
            concerns['config'] += 1
        elif 'doc' in name:
            concerns['docs'] += 1
        elif 'script' in name or 'tool' in name:
            concerns['scripts'] += 1
        elif 'src' in name or 'lib' in name:
            concerns['source'] += 1

print("Separation of Concerns:")
for concern, count in concerns.items():
    if count > 0:
        print(f"  ✓ {concern.title()}: {count} directories")
    else:
        print(f"  - {concern.title()}: Not separated")
print()

# Overall quality score
scores = []

# Depth score (inverse: lower is better)
if max_depth <= 5:
    scores.append(100)
elif max_depth <= 8:
    scores.append(70)
else:
    scores.append(40)

# Naming score
scores.append(int(consistency_ratio * 100) if naming_patterns else 50)

# Separation score
separation_score = (sum(1 for c in concerns.values() if c > 0) / len(concerns)) * 100
scores.append(int(separation_score))

overall_quality = sum(scores) / len(scores)

print(f"Organization Quality Score: {overall_quality:.1f}/100")
if overall_quality >= 80:
    print("  ✓✓✓ Excellent organization")
elif overall_quality >= 60:
    print("  ✓✓ Good organization")
elif overall_quality >= 40:
    print("  ✓ Fair organization")
else:
    print("  ✗ Poor organization")
print()
```

---

## Phase 7: Anti-Pattern Detection

```python
print(f"=== Anti-Pattern Detection ===\n")

anti_patterns = []

# 1. God Module (too many files in one directory)
for d in project_root.rglob('*'):
    if d.is_dir():
        files = [f for f in d.iterdir() if f.is_file() and not f.name.startswith('.')]
        if len(files) > 30:
            anti_patterns.append({
                "pattern": "God Module",
                "location": str(d.relative_to(project_root)),
                "severity": "HIGH",
                "description": f"{len(files)} files in one directory",
                "fix": "Split into smaller, focused modules"
            })

# 2. Circular Dependencies (simplified check)
# Would need full import graph for accurate detection
print("Circular Dependency Check:")
print("  (Requires full import graph analysis)")
print("  Run: /cco-analyze-dependencies for detailed analysis")
print()

# 3. Missing Test Directory
test_dirs = [d for d in project_root.rglob('*') if 'test' in d.name.lower() and d.is_dir()]
if not test_dirs:
    anti_patterns.append({
        "pattern": "No Test Directory",
        "location": "project root",
        "severity": "MEDIUM",
        "description": "No dedicated test directory found",
        "fix": "Create tests/ or test/ directory"
    })

# 4. Mixed Concerns
src_dir = project_root / 'src'
if src_dir.exists():
    has_tests = any('test' in f.name.lower() for f in src_dir.rglob('*'))
    has_config = any('config' in f.name.lower() for f in src_dir.rglob('*'))

    if has_tests:
        anti_patterns.append({
            "pattern": "Mixed Concerns",
            "location": "src/",
            "severity": "LOW",
            "description": "Tests mixed with source code",
            "fix": "Move tests to separate tests/ directory"
        })

# 5. Flat Structure (too many top-level items)
top_level = [d for d in project_root.iterdir() if not d.name.startswith('.')]
if len(top_level) > 15:
    anti_patterns.append({
        "pattern": "Flat Structure",
        "location": "project root",
        "severity": "MEDIUM",
        "description": f"{len(top_level)} items in root directory",
        "fix": "Group related items into subdirectories"
    })

# Display anti-patterns
if anti_patterns:
    print(f"Anti-Patterns Found: {len(anti_patterns)}\n")
    for ap in anti_patterns:
        print(f"[{ap['severity']}] {ap['pattern']}")
        print(f"  Location: {ap['location']}")
        print(f"  Issue: {ap['description']}")
        print(f"  Fix: {ap['fix']}")
        print()
else:
    print("✓ No major anti-patterns detected\n")
```

---

## Phase 8: Recommendations

```python
print(f"=== Recommendations ===\n")

recommendations = []

# Structure recommendations
if max_depth > 8:
    recommendations.append({
        "priority": "HIGH",
        "category": "Structure",
        "title": "Reduce directory nesting depth",
        "actions": [
            "Flatten overly nested hierarchies",
            "Target 3-5 levels maximum",
            "Group by feature instead of type"
        ]
    })

if overall_quality < 60:
    recommendations.append({
        "priority": "HIGH",
        "category": "Organization",
        "title": "Improve code organization",
        "actions": [
            "Adopt consistent naming convention",
            "Separate concerns (tests, config, source)",
            "Create clear module boundaries"
        ]
    })

# Pattern recommendations
if not patterns_detected:
    recommendations.append({
        "priority": "MEDIUM",
        "category": "Architecture",
        "title": "Adopt architectural pattern",
        "actions": [
            "Consider MVC, Clean Architecture, or feature-based",
            "Document chosen architecture in README",
            "Refactor gradually toward pattern"
        ]
    })

# Module recommendations
if len(modules) == 0:
    recommendations.append({
        "priority": "MEDIUM",
        "category": "Modularity",
        "title": "Introduce modular structure",
        "actions": [
            "Break monolithic code into modules",
            "Create clear interfaces between modules",
            "Use dependency injection"
        ]
    })

# Testing recommendations
if not test_dirs:
    recommendations.append({
        "priority": "HIGH",
        "category": "Testing",
        "title": "Add test infrastructure",
        "actions": [
            "Create tests/ directory",
            "Set up testing framework",
            "Mirror source structure in tests"
        ]
    })

# Display recommendations
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['title']}")
    for action in rec['actions']:
        print(f"   - {action}")
    print()

if not recommendations:
    print("✓ Structure is well-organized. No major improvements needed.\n")
```

---

## Phase 9: Generate Structure Diagram

```python
print(f"=== Architecture Diagram ===\n")

# ASCII diagram of key directories
def generate_diagram(root_path, max_items=15):
    """Generate ASCII architecture diagram"""
    diagram = []

    # Get top-level important directories
    important_dirs = []
    for item in sorted(root_path.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            if item.name not in ['node_modules', '__pycache__', 'venv', 'dist', 'build']:
                important_dirs.append(item)

    # Limit to most important
    important_dirs = important_dirs[:max_items]

    diagram.append("┌─────────────────────────────────────┐")
    diagram.append(f"│  {project_name:^33s}  │")
    diagram.append("└─────────────────────────────────────┘")
    diagram.append("              │")

    for i, dir_path in enumerate(important_dirs):
        is_last = (i == len(important_dirs) - 1)
        connector = "└──" if is_last else "├──"

        # Count contents
        try:
            contents = list(dir_path.iterdir())
            files = sum(1 for c in contents if c.is_file())
            dirs = sum(1 for c in contents if c.is_dir())
            label = f"[{files}f, {dirs}d]"
        except:
            label = ""

        diagram.append(f"              {connector} {dir_path.name}/ {label}")

    return "\n".join(diagram)

print(generate_diagram(project_root))
print()
```

---

## Phase 10: Export Report

```python
print(f"=== Export Report ===\n")

report = {
    "project": project_name,
    "analysis_date": "2025-11-10",
    "statistics": {
        "total_directories": stats["total_dirs"],
        "total_files": stats["total_files"],
        "primary_language": primary_language,
        "max_depth": max_depth
    },
    "patterns": [p["pattern"] for p in patterns_detected],
    "quality_score": overall_quality,
    "anti_patterns": [ap["pattern"] for ap in anti_patterns],
    "recommendations": len(recommendations)
}

report_path = project_root / "structure-analysis-report.json"
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print(f"Report saved to: {report_path.name}")
print()
```

---

---

**Structure Philosophy:** Good architecture is invisible - it guides without constraining, organizes without complicating.
