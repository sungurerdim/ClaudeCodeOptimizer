---
id: cco-audit-docs
description: Documentation completeness, accuracy, drift
category: documentation
priority: normal
---

# Audit Documentation

Audit documentation completeness, accuracy, and detect documentation drift in **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Comprehensive documentation analysis:
1. Check documentation completeness
2. Detect documentation drift (code changed, docs didn't)
3. Verify code examples are valid
4. Assess documentation quality
5. Identify missing documentation

**Output:** Documentation audit report with improvement recommendations.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (fast scanning)
**Analysis & Reasoning**: Haiku (straightforward checks)
**Execution Pattern**: Sequential scanning and validation

---

## When to Use

**Use this command:**
- Before releases
- After major refactoring
- When onboarding new team members
- Documentation feels outdated

---

## Phase 1: Documentation Discovery

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
project_root = Path(".").resolve()

print(f"=== Documentation Discovery ===\n")

# Find all documentation files
doc_files = {
    'markdown': list(project_root.rglob('*.md')),
    'restructured': list(project_root.rglob('*.rst')),
    'text': list(project_root.rglob('*.txt'))
}

# Exclude common directories
excluded = ['node_modules', 'venv', '__pycache__', '.git']
doc_files = {k: [f for f in v if not any(ex in str(f) for ex in excluded)] for k, v in doc_files.items()}

total_docs = sum(len(v) for v in doc_files.values())

print(f"Documentation Files: {total_docs}")
for doc_type, files in doc_files.items():
    if files:
        print(f"  {doc_type}: {len(files)}")
print()

# Check for essential docs
essential_docs = {
    'README.md': (project_root / 'README.md').exists(),
    'CONTRIBUTING.md': (project_root / 'CONTRIBUTING.md').exists(),
    'LICENSE': any((project_root / name).exists() for name in ['LICENSE', 'LICENSE.md', 'LICENSE.txt']),
    'CHANGELOG.md': (project_root / 'CHANGELOG.md').exists(),
    'docs/ directory': (project_root / 'docs').exists(),
}

print("Essential Documentation:")
for doc, exists in essential_docs.items():
    status = "✓" if exists else "✗"
    print(f"  {status} {doc}")
print()
```

---

## Phase 2: Check Docstring Coverage

```python
print(f"=== Docstring Coverage ===\n")

import ast

class DocstringChecker(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node):
        self.functions.append({
            'name': node.name,
            'line': node.lineno,
            'has_docstring': ast.get_docstring(node) is not None
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append({
            'name': node.name,
            'line': node.lineno,
            'has_docstring': ast.get_docstring(node) is not None
        })
        self.generic_visit(node)

python_files = [f for f in project_root.rglob('*.py') if not any(ex in str(f) for ex in excluded + ['test'])]

all_functions = []
all_classes = []

for py_file in python_files[:100]:
    try:
        source = py_file.read_text()
        tree = ast.parse(source)
        checker = DocstringChecker()
        checker.visit(tree)

        for func in checker.functions:
            func['file'] = str(py_file.relative_to(project_root))
            all_functions.append(func)

        for cls in checker.classes:
            cls['file'] = str(py_file.relative_to(project_root))
            all_classes.append(cls)
    except:
        pass

documented_funcs = [f for f in all_functions if f['has_docstring']]
documented_classes = [c for c in all_classes if c['has_docstring']]

func_coverage = len(documented_funcs) / len(all_functions) * 100 if all_functions else 0
class_coverage = len(documented_classes) / len(all_classes) * 100 if all_classes else 0

print(f"Functions: {len(documented_funcs)}/{len(all_functions)} documented ({func_coverage:.1f}%)")
print(f"Classes: {len(documented_classes)}/{len(all_classes)} documented ({class_coverage:.1f}%)")
print()
```

---

## Phase 3: Detect Documentation Drift

```python
print(f"=== Documentation Drift Detection ===\n")

import re

drift_issues = []

# Check if README mentions files that don't exist
readme_path = project_root / 'README.md'
if readme_path.exists():
    readme_content = readme_path.read_text()

    # Find file/directory references
    references = re.findall(r'`([a-zA-Z0-9_/-]+\.[a-zA-Z]+)`', readme_content)

    for ref in set(references):
        if '/' in ref:
            ref_path = project_root / ref
            if not ref_path.exists():
                drift_issues.append({
                    'type': 'Missing File Reference',
                    'file': 'README.md',
                    'issue': f'References non-existent file: {ref}'
                })

if drift_issues:
    print(f"Drift Issues: {len(drift_issues)}")
    for issue in drift_issues[:5]:
        print(f"  - {issue['type']}: {issue['issue']}")
else:
    print("✓ No obvious drift detected")
print()
```

---

## Phase 4: Validate Code Examples

```python
print(f"=== Code Example Validation ===\n")

# Extract code blocks from markdown
code_blocks = []

for md_file in doc_files['markdown']:
    try:
        content = md_file.read_text()

        # Find code blocks
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)

        for lang, code in matches:
            code_blocks.append({
                'file': str(md_file.relative_to(project_root)),
                'language': lang or 'unknown',
                'code': code.strip()
            })
    except:
        pass

print(f"Code Examples Found: {len(code_blocks)}")

# Validate Python code blocks
python_blocks = [b for b in code_blocks if b['language'] in ['python', 'py']]
valid_python = 0
invalid_python = []

for block in python_blocks:
    try:
        compile(block['code'], '<string>', 'exec')
        valid_python += 1
    except SyntaxError:
        invalid_python.append(block)

if python_blocks:
    print(f"  Python examples: {valid_python}/{len(python_blocks)} valid")
    if invalid_python:
        print(f"  ⚠ {len(invalid_python)} examples have syntax errors")

print()
```

---

## Phase 5: Documentation Quality Score

```python
print(f"=== Documentation Quality ===\n")

quality_score = 100

# Penalize missing essential docs
missing_essential = sum(1 for exists in essential_docs.values() if not exists)
quality_score -= missing_essential * 15

# Penalize low docstring coverage
if func_coverage < 50:
    quality_score -= 20
elif func_coverage < 70:
    quality_score -= 10

# Penalize drift
quality_score -= len(drift_issues) * 5

quality_score = max(0, quality_score)

print(f"Documentation Quality Score: {quality_score}/100")

if quality_score >= 80:
    print("  ✓✓✓ Excellent")
elif quality_score >= 60:
    print("  ✓✓ Good")
else:
    print("  ✗ Needs improvement")
print()
```

---

## Phase 6: Recommendations

```python
print(f"=== Recommendations ===\n")

recommendations = []

if not essential_docs['README.md']:
    recommendations.append("Create README.md with project overview")

if func_coverage < 70:
    recommendations.append(f"Improve docstring coverage ({func_coverage:.0f}% → 70%+)")

if drift_issues:
    recommendations.append(f"Fix {len(drift_issues)} documentation drift issues")

if invalid_python:
    recommendations.append(f"Fix {len(invalid_python)} invalid code examples")

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

print()
```

---

## Output Example

```
=== Documentation Discovery ===

Documentation Files: 23
  markdown: 18
  restructured: 3
  text: 2

Essential Documentation:
  ✓ README.md
  ✗ CONTRIBUTING.md
  ✓ LICENSE
  ✓ CHANGELOG.md
  ✓ docs/ directory

=== Docstring Coverage ===

Functions: 298/412 documented (72.3%)
Classes: 45/67 documented (67.2%)

=== Documentation Drift Detection ===

Drift Issues: 3
  - Missing File Reference: References non-existent file: src/old_module.py
  - Missing File Reference: References non-existent file: docs/api.md

=== Code Example Validation ===

Code Examples Found: 47
  Python examples: 28/32 valid
  ⚠ 4 examples have syntax errors

=== Documentation Quality ===

Documentation Quality Score: 68/100
  ✓✓ Good

=== Recommendations ===

1. Create CONTRIBUTING.md with project overview
2. Fix 3 documentation drift issues
3. Fix 4 invalid code examples
```

---

**Documentation Philosophy:** Code tells you how, documentation tells you why. Both are essential.
