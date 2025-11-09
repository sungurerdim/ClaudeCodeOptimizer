---
id: cco-analyze
description: Deep project analysis - structure, tech stack, complexity, recommendations
category: bootstrap
priority: medium
---

# CCO Project Analysis

Deep analysis of **${PROJECT_NAME}** structure, technology stack, and quality metrics.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}
**Services:** ${SERVICES_COUNT}

## Objective

Comprehensive project analysis:
1. Project structure detection (monorepo, microservices, monolith)
2. Technology stack identification (frameworks, libraries, tools)
3. Complexity metrics (LOC, cyclomatic complexity, dependencies)
4. Architecture pattern analysis
5. Quality metrics
6. Actionable recommendations

**Output:** Complete project analysis report with recommendations.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast file scanning and structure analysis
- Tech stack detection and pattern recognition
- Cost-effective codebase traversal

**Analysis & Reasoning**: Sonnet (Plan agent)
- Complex architecture analysis
- Complexity assessment and recommendations
- Strategic insights and synthesis

**Execution Pattern**:
1. Launch multiple Haiku agents to scan different aspects (parallel)
2. Aggregate structural data and metrics
3. Use Sonnet for deep analysis and recommendations
4. Generate comprehensive analysis report

---

## Phase 1: Project Structure Analysis

Detect project organization and architecture:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
from collections import defaultdict

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Project Structure Analysis ===\n")
print(f"Project: {project_name}")
print(f"Root: {project_root}\n")

# Detect structure type
structure_indicators = {
    "monorepo": False,
    "microservices": False,
    "monolith": False,
    "library": False
}

# Check for monorepo indicators
if (project_root / "packages").exists() or \
   (project_root / "apps").exists() or \
   (project_root / "services").exists() and len(list((project_root / "services").iterdir())) > 1:
    structure_indicators["monorepo"] = True

# Check for microservices
services_dir = project_root / "services"
if services_dir.exists():
    services = [d for d in services_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    if len(services) > 1:
        structure_indicators["microservices"] = True
        service_count = len(services)
    else:
        service_count = 0
else:
    service_count = 0

# Check for library
if (project_root / "setup.py").exists() or \
   (project_root / "pyproject.toml").exists() and not (project_root / "services").exists():
    structure_indicators["library"] = True

# Check for monolith
if not any([structure_indicators["monorepo"], structure_indicators["microservices"], structure_indicators["library"]]):
    structure_indicators["monolith"] = True

# Determine primary structure
if structure_indicators["microservices"]:
    structure_type = "Microservices"
elif structure_indicators["monorepo"]:
    structure_type = "Monorepo"
elif structure_indicators["library"]:
    structure_type = "Library"
else:
    structure_type = "Monolith"

print(f"Structure Type: {structure_type}")
if structure_type == "Microservices":
    print(f"Service Count: {service_count} services")

# Analyze directory structure
print("\n=== Directory Tree ===\n")

def analyze_tree(path, max_depth=3, current_depth=0, prefix=""):
    if current_depth >= max_depth:
        return

    try:
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))

        # Skip hidden, cache, and build directories
        skip_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'dist', 'build', '.pytest_cache', '.mypy_cache'}

        dirs = []
        files = []

        for item in items:
            if item.name.startswith('.') and item.name not in {'.github', '.claude', '.cco', '.cco'}:
                continue
            if item.name in skip_dirs:
                continue

            if item.is_dir():
                dirs.append(item)
            else:
                files.append(item)

        # Show important directories
        for i, d in enumerate(dirs[:10]):  # Limit to 10 directories per level
            is_last = (i == len(dirs) - 1) and len(files) == 0
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}{d.name}/")

            # Recurse
            extension = "    " if is_last else "│   "
            analyze_tree(d, max_depth, current_depth + 1, prefix + extension)

        # Show important files at root level only
        if current_depth == 0:
            important_files = [
                "README.md", "CLAUDE.md", "TECHNICAL_REQUIREMENTS.md",
                "setup.py", "pyproject.toml", "package.json", "Cargo.toml", "go.mod",
                "Dockerfile", "docker-compose.yml", ".env.example",
                "requirements.txt", "Pipfile", "poetry.lock"
            ]

            for f in files:
                if f.name in important_files:
                    print(f"{prefix}├── {f.name}")

    except PermissionError:
        pass

analyze_tree(project_root)
```

---

## Phase 2: Technology Stack Detection

Identify all technologies, frameworks, and tools:

```python
print("\n=== Technology Stack Detection ===\n")

tech_stack = {
    "languages": [],
    "frameworks": [],
    "databases": [],
    "caching": [],
    "queuing": [],
    "web_servers": [],
    "tools": [],
    "ci_cd": []
}

# Language detection (from file extensions)
file_extensions = defaultdict(int)

for file_path in project_root.rglob("*"):
    if file_path.is_file():
        ext = file_path.suffix
        if ext in {'.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java', '.cpp', '.c', '.rb', '.php'}:
            file_extensions[ext] += 1

# Map extensions to languages
ext_to_lang = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript',
    '.jsx': 'JavaScript',
    '.go': 'Go',
    '.rs': 'Rust',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.rb': 'Ruby',
    '.php': 'PHP'
}

for ext, count in sorted(file_extensions.items(), key=lambda x: x[1], reverse=True):
    lang = ext_to_lang.get(ext, ext)
    if lang not in tech_stack["languages"]:
        tech_stack["languages"].append(lang)

print(f"Languages Detected: {len(tech_stack['languages'])}")
for lang in tech_stack["languages"]:
    print(f"- {lang}")

# Framework detection (from files and imports)
framework_indicators = {
    # Python frameworks
    "fastapi": ["from fastapi", "import fastapi"],
    "flask": ["from flask", "import flask"],
    "django": ["from django", "import django", "manage.py"],
    "redis": ["import redis", "from redis"],
    "postgresql": ["import psycopg2", "from sqlalchemy"],
    "celery": ["from celery", "import celery"],

    # JavaScript frameworks
    "react": ["from 'react'", 'from "react"', "package.json:react"],
    "vue": ["from 'vue'", 'from "vue"', "package.json:vue"],
    "express": ["from 'express'", 'require("express")', "package.json:express"],
    "next.js": ["from 'next'", "package.json:next"],

    # Databases
    "mongodb": ["import pymongo", "from pymongo", "package.json:mongodb"],
    "mysql": ["import mysql", "from mysql"],

    # Tools
    "docker": ["Dockerfile", "docker-compose.yml"],
    "kubernetes": ["k8s/", "kubernetes/"],
    "terraform": [".tf files"]
}

# Search for framework indicators
```

Use Grep to search for framework imports:
```bash
# Python frameworks
Grep("from fastapi|import fastapi", glob="**/*.py", output_mode="files_with_matches")
Grep("from flask|import flask", glob="**/*.py", output_mode="files_with_matches")
Grep("from django|import django", glob="**/*.py", output_mode="files_with_matches")
Grep("import redis|from redis", glob="**/*.py", output_mode="files_with_matches")
Grep("import psycopg2|from sqlalchemy", glob="**/*.py", output_mode="files_with_matches")
Grep("from celery|import celery", glob="**/*.py", output_mode="files_with_matches")

# Check for package files
Glob("**/package.json")
Glob("**/requirements.txt")
Glob("**/Pipfile")
Glob("**/Cargo.toml")
Glob("**/go.mod")
```

**Aggregate detected frameworks:**
```python
print("\n=== Frameworks & Libraries ===\n")

# Example results from grep
detected_frameworks = {
    "fastapi": True,   # Found via grep
    "redis": True,     # Found via grep
    "postgresql": True # Found via grep
}

for framework, found in detected_frameworks.items():
    if found:
        tech_stack["frameworks"].append(framework)

print(f"Frameworks: {len(tech_stack['frameworks'])}")
for framework in tech_stack["frameworks"]:
    print(f"- {framework}")

# Database detection
databases = ["postgresql", "mysql", "mongodb", "redis", "sqlite"]
for db in databases:
    if db in tech_stack["frameworks"]:
        tech_stack["databases"].append(db)
        tech_stack["frameworks"].remove(db)

if tech_stack["databases"]:
    print(f"\nDatabases: {len(tech_stack['databases'])}")
    for db in tech_stack["databases"]:
        print(f"- {db}")

# CI/CD detection
ci_files = {
    ".github/workflows/": "GitHub Actions",
    ".gitlab-ci.yml": "GitLab CI",
    ".travis.yml": "Travis CI",
    "Jenkinsfile": "Jenkins",
    ".circleci/": "CircleCI"
}

for file_path, ci_name in ci_files.items():
    if (project_root / file_path).exists():
        tech_stack["ci_cd"].append(ci_name)

if tech_stack["ci_cd"]:
    print(f"\nCI/CD: {len(tech_stack['ci_cd'])}")
    for ci in tech_stack["ci_cd"]:
        print(f"- {ci}")
```

---

## Phase 3: Complexity Metrics

Calculate code complexity metrics:

```python
print("\n=== Complexity Metrics ===\n")

metrics = {
    "total_files": 0,
    "total_lines": 0,
    "code_lines": 0,
    "comment_lines": 0,
    "blank_lines": 0,
    "avg_file_length": 0,
    "max_file_length": 0,
    "functions": 0,
    "classes": 0
}

# Count files by language
lang_files = {
    ".py": [],
    ".js": [],
    ".ts": [],
    ".go": [],
    ".rs": []
}

for file_path in project_root.rglob("*"):
    if file_path.is_file():
        ext = file_path.suffix
        if ext in lang_files:
            lang_files[ext].append(file_path)
            metrics["total_files"] += 1

# Calculate LOC for each file
for ext, files in lang_files.items():
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

                for line in lines:
                    stripped = line.strip()
                    metrics["total_lines"] += 1

                    if not stripped:
                        metrics["blank_lines"] += 1
                    elif stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                        metrics["comment_lines"] += 1
                    else:
                        metrics["code_lines"] += 1

                file_length = len(lines)
                if file_length > metrics["max_file_length"]:
                    metrics["max_file_length"] = file_length

        except Exception:
            pass

# Calculate averages
if metrics["total_files"] > 0:
    metrics["avg_file_length"] = metrics["total_lines"] // metrics["total_files"]

# Count functions and classes
```

Use Grep to count functions and classes:
```bash
# Python
Grep("^def \\w+\\(", glob="**/*.py", output_mode="count")
Grep("^class \\w+", glob="**/*.py", output_mode="count")

# JavaScript/TypeScript
Grep("function \\w+\\(|const \\w+ = \\(.*\\) =>", glob="**/*.{js,ts}", output_mode="count")

# Go
Grep("^func \\w+\\(", glob="**/*.go", output_mode="count")
```

**Display metrics:**
```python
# Example counts from grep
metrics["functions"] = 250  # From grep count
metrics["classes"] = 45     # From grep count

print(f"Total Files: {metrics['total_files']}")
print(f"Total Lines: {metrics['total_lines']:,}")
print(f"  Code Lines: {metrics['code_lines']:,} ({metrics['code_lines']*100//max(1,metrics['total_lines'])}%)")
print(f"  Comment Lines: {metrics['comment_lines']:,} ({metrics['comment_lines']*100//max(1,metrics['total_lines'])}%)")
print(f"  Blank Lines: {metrics['blank_lines']:,} ({metrics['blank_lines']*100//max(1,metrics['total_lines'])}%)")

print(f"\nAverage File Length: {metrics['avg_file_length']} lines")
print(f"Max File Length: {metrics['max_file_length']} lines")

if metrics["max_file_length"] > 1000:
    print("  ⚠️ Warning: Some files exceed 1000 lines (consider refactoring)")

print(f"\nFunctions: {metrics['functions']}")
print(f"Classes: {metrics['classes']}")

# Code-to-comment ratio
if metrics["code_lines"] > 0:
    comment_ratio = metrics["comment_lines"] / metrics["code_lines"]
    print(f"\nComment Ratio: {comment_ratio:.2%}")
    if comment_ratio < 0.05:
        print("  ⚠️ Low comment coverage (target: 10-20%)")
    elif comment_ratio > 0.30:
        print("  ⚠️ Over-commented (may indicate unclear code)")
    else:
        print("  ✓ Good comment coverage")
```

---

## Phase 4: Dependency Analysis

Analyze project dependencies:

```python
print("\n=== Dependency Analysis ===\n")

dependencies = {
    "production": [],
    "development": [],
    "total": 0
}

# Python dependencies
requirements_file = project_root / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name (before ==, >=, etc.)
                pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                dependencies["production"].append(pkg_name)

# Check for pyproject.toml
pyproject_file = project_root / "pyproject.toml"
if pyproject_file.exists():
    # Parse dependencies from pyproject.toml
    # For demo, skip actual parsing
    pass

# JavaScript dependencies
package_json = project_root / "package.json"
if package_json.exists():
    import json
    with open(package_json, 'r') as f:
        data = json.load(f)
        if "dependencies" in data:
            dependencies["production"].extend(data["dependencies"].keys())
        if "devDependencies" in data:
            dependencies["development"].extend(data["devDependencies"].keys())

dependencies["total"] = len(dependencies["production"]) + len(dependencies["development"])

print(f"Total Dependencies: {dependencies['total']}")
print(f"  Production: {len(dependencies['production'])}")
print(f"  Development: {len(dependencies['development'])}")

# Show top dependencies
if dependencies["production"]:
    print("\nTop 10 Production Dependencies:")
    for i, dep in enumerate(dependencies["production"][:10], 1):
        print(f"{i}. {dep}")

# Dependency health warnings
if dependencies["total"] > 100:
    print("\n⚠️ High dependency count (>100). Consider:")
    print("   - Removing unused dependencies")
    print("   - Using lighter alternatives")
    print("   - Reviewing necessity of each dependency")
elif dependencies["total"] < 5:
    print("\n✓ Low dependency count (good for maintainability)")
```

---

## Phase 5: Architecture Pattern Detection

Identify architecture patterns:

```python
print("\n=== Architecture Patterns ===\n")

patterns = {
    "layered": False,
    "microservices": False,
    "event_driven": False,
    "repository_pattern": False,
    "service_layer": False,
    "api_gateway": False
}

# Layered architecture (controllers, services, repositories)
```

Use Glob and Grep to detect patterns:
```bash
# Layered architecture
Glob("**/controllers/**")
Glob("**/services/**")
Glob("**/repositories/**")
Glob("**/models/**")

# Event-driven
Grep("event|EventBus|publish|subscribe", output_mode="files_with_matches")

# Repository pattern
Grep("class.*Repository|def.*repository", glob="**/*.py", output_mode="files_with_matches")

# Service layer
Grep("class.*Service|def.*service", glob="**/*.py", output_mode="files_with_matches")

# API Gateway
Grep("gateway|reverse_proxy|nginx", output_mode="files_with_matches")
```

**Aggregate patterns:**
```python
# Example results
if (project_root / "services").exists():
    patterns["microservices"] = True

# Detect layered from directory structure
layered_dirs = ["controllers", "services", "repositories", "models"]
found_layers = sum(1 for d in layered_dirs if (project_root / d).exists() or list(project_root.rglob(f"**/{d}")))

if found_layers >= 3:
    patterns["layered"] = True

print("Detected Patterns:")
for pattern, detected in patterns.items():
    if detected:
        print(f"✓ {pattern.replace('_', ' ').title()}")

if not any(patterns.values()):
    print("No clear architecture pattern detected")
    print("Consider adopting: Layered Architecture or Repository Pattern")
```

---

## Phase 6: Quality Metrics

Calculate quality indicators:

```python
print("\n=== Quality Metrics ===\n")

quality_score = 0
max_score = 100

# Factor 1: Documentation (20 points)
has_readme = (project_root / "README.md").exists()
has_claude_md = (project_root / "CLAUDE.md").exists()
has_tech_req = (project_root / "TECHNICAL_REQUIREMENTS.md").exists()

doc_score = 0
if has_readme:
    doc_score += 10
if has_claude_md:
    doc_score += 5
if has_tech_req:
    doc_score += 5

quality_score += doc_score

# Factor 2: Testing (25 points)
```

Use Glob and Grep to detect tests:
```bash
Glob("**/test_*.py")
Glob("**/*_test.go")
Glob("**/*.test.{js,ts}")
Glob("**/tests/**")
```

```python
# Assume test files found
test_files = 50  # From glob
test_score = min(25, test_files // 2)  # 2 test files = 1 point, max 25
quality_score += test_score

# Factor 3: Type Safety (15 points)
```

Use Grep to check type hints:
```bash
Grep("def \\w+\\(.*\\) ->", glob="**/*.py", output_mode="count")
Grep(": \\w+", glob="**/*.ts", output_mode="count")
```

```python
# Type hints ratio
functions_with_types = 150  # From grep
type_coverage = functions_with_types / max(1, metrics["functions"])
type_score = int(type_coverage * 15)
quality_score += type_score

# Factor 4: Code organization (15 points)
if patterns["layered"] or patterns["microservices"]:
    quality_score += 15
elif patterns["repository_pattern"]:
    quality_score += 10
else:
    quality_score += 5

# Factor 5: Dependency management (10 points)
if dependencies["total"] < 50:
    quality_score += 10
elif dependencies["total"] < 100:
    quality_score += 5

# Factor 6: CI/CD (10 points)
if tech_stack["ci_cd"]:
    quality_score += 10

# Factor 7: Low complexity (5 points)
if metrics["avg_file_length"] < 300:
    quality_score += 5

print(f"Quality Score: {quality_score}/100\n")

if quality_score >= 80:
    grade = "A (Excellent)"
elif quality_score >= 60:
    grade = "B (Good)"
elif quality_score >= 40:
    grade = "C (Fair)"
else:
    grade = "D (Needs Improvement)"

print(f"Grade: {grade}\n")

print("Score Breakdown:")
print(f"- Documentation: {doc_score}/20")
print(f"- Testing: {test_score}/25")
print(f"- Type Safety: {type_score}/15")
print(f"- Code Organization: 15/15" if patterns["layered"] else "- Code Organization: 5-10/15")
print(f"- Dependency Management: 10/10" if dependencies["total"] < 50 else f"- Dependency Management: 5/10")
print(f"- CI/CD: 10/10" if tech_stack["ci_cd"] else "- CI/CD: 0/10")
print(f"- Low Complexity: 5/5" if metrics["avg_file_length"] < 300 else "- Low Complexity: 0/5")
```

---

## Phase 7: Recommendations

Provide actionable recommendations:

```python
print("\n=== Recommendations ===\n")

recommendations = []

# Documentation
if not has_readme:
    recommendations.append("CRITICAL: Add README.md with project overview and setup")
if not has_claude_md:
    recommendations.append("HIGH: Create CLAUDE.md for AI development guidance")

# Testing
if test_files < 20:
    recommendations.append("HIGH: Increase test coverage (currently low)")

# Type safety
if type_coverage < 0.5:
    recommendations.append("MEDIUM: Add type hints to functions (currently <50%)")

# Complexity
if metrics["max_file_length"] > 1000:
    recommendations.append("MEDIUM: Refactor large files (>1000 lines)")
if metrics["avg_file_length"] > 500:
    recommendations.append("LOW: Average file size is high (consider splitting)")

# Dependencies
if dependencies["total"] > 100:
    recommendations.append("MEDIUM: Review and remove unused dependencies")

# CI/CD
if not tech_stack["ci_cd"]:
    recommendations.append("HIGH: Setup CI/CD pipeline (GitHub Actions, GitLab CI, etc.)")

# Architecture
if not any([patterns["layered"], patterns["microservices"], patterns["repository_pattern"]]):
    recommendations.append("MEDIUM: Adopt clear architecture pattern (Layered or Repository)")

# Comment coverage
if metrics["code_lines"] > 0:
    comment_ratio = metrics["comment_lines"] / metrics["code_lines"]
    if comment_ratio < 0.05:
        recommendations.append("LOW: Add more inline documentation (comments)")

# Display recommendations
if recommendations:
    for i, rec in enumerate(recommendations, 1):
        severity = rec.split(':')[0]
        print(f"{i}. {rec}")
else:
    print("✓ No critical recommendations. Project is well-structured!")

print("\nNext Steps:")
print("1. Run /cco-audit-all to validate code quality")
print("2. Run /cco-fix-code to auto-fix violations")
print("3. Address high-priority recommendations")
```

---

## Phase 8: Save Analysis Results

Save analysis to state for tracking:

```python
from claudecodeoptimizer.core.state import StateTracker

state = StateTracker(project_name)

analysis_results = {
    "structure_type": structure_type,
    "service_count": service_count if structure_type == "Microservices" else 0,
    "tech_stack": tech_stack,
    "metrics": metrics,
    "dependencies": dependencies,
    "patterns": {k: v for k, v in patterns.items() if v},
    "quality_score": quality_score,
    "quality_grade": grade,
    "recommendations": recommendations,
    "analyzed_at": __import__('datetime').datetime.now().isoformat()
}

state.update_analysis(analysis_results)

print(f"\n✓ Analysis saved to: ~/.cco/projects/{project_name}.json")
print(f"\nView results anytime: /cco-status")
```

---

## Quick Analysis Mode

For fast analysis without detailed output:

```bash
/cco-analyze --quick

# Output:
# Structure: Microservices (5 services)
# Languages: Python, JavaScript
# Quality: 85/100 (A - Excellent)
# Recommendations: 3 items
```

---

## Comparative Analysis

Compare with previous analysis:

```bash
/cco-analyze --compare

# Shows:
# - Quality score trend (↗ improving / ↘ declining)
# - LOC change
# - Dependency changes
# - New recommendations
```

---

## Export Analysis Report

Generate shareable report:

```bash
/cco-analyze --export

# Creates: analysis-report-YYYYMMDD.md
```

---

## Output Example

```
=== Project Structure Analysis ===

Project: backend
Root: D:\GitHub\backend

Structure Type: Microservices
Service Count: 5 services

=== Directory Tree ===

├── services/
│   ├── api/
│   ├── analyzer/
│   ├── ledger/
│   ├── seed/
│   └── worker/
├── shared/
├── tests/
├── .claude/
├── .github/
├── README.md
├── CLAUDE.md
├── docker-compose.yml

=== Technology Stack Detection ===

Languages Detected: 2
- Python
- JavaScript

=== Frameworks & Libraries ===

Frameworks: 3
- fastapi
- celery
- redis

Databases: 2
- postgresql
- redis

CI/CD: 1
- GitHub Actions

=== Complexity Metrics ===

Total Files: 127
Total Lines: 15,234
  Code Lines: 10,500 (69%)
  Comment Lines: 1,200 (8%)
  Blank Lines: 3,534 (23%)

Average File Length: 120 lines
Max File Length: 856 lines

Functions: 250
Classes: 45

Comment Ratio: 11.43%
  ✓ Good comment coverage

=== Dependency Analysis ===

Total Dependencies: 42
  Production: 35
  Development: 7

Top 10 Production Dependencies:
1. fastapi
2. uvicorn
3. redis
4. psycopg2-binary
5. sqlalchemy
6. celery
7. pydantic
8. python-jose
9. passlib
10. python-multipart

✓ Low dependency count (good for maintainability)

=== Architecture Patterns ===

Detected Patterns:
✓ Microservices
✓ Layered
✓ Service Layer

=== Quality Metrics ===

Quality Score: 85/100

Grade: A (Excellent)

Score Breakdown:
- Documentation: 20/20
- Testing: 22/25
- Type Safety: 12/15
- Code Organization: 15/15
- Dependency Management: 10/10
- CI/CD: 10/10
- Low Complexity: 5/5

=== Recommendations ===

1. MEDIUM: Add type hints to functions (currently ~48%)
2. LOW: Increase test coverage to 90%

✓ Project is well-structured!

Next Steps:
1. Run /cco-audit-all to validate code quality
2. Run /cco-fix-code to auto-fix violations
3. Address high-priority recommendations

✓ Analysis saved to: ~/.cco/projects/backend.json

View results anytime: /cco-status
```

---

**Analysis Philosophy:** Know your codebase deeply. Measure, improve, repeat!
