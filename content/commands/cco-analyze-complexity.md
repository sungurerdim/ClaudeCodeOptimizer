---
id: cco-analyze-complexity
description: Cyclomatic complexity, code smells, refactoring candidates
category: analysis
priority: normal
principles:
  - 'U_EVIDENCE_BASED'
  - 'U_ROOT_CAUSE_ANALYSIS'
  - 'P_LINTING_SAST'
  - 'U_NO_OVERENGINEERING'
  - 'U_COMPLETE_REPORTING'
---

# Analyze Code Complexity

Analyze **${PROJECT_NAME}** cyclomatic complexity, detect code smells, and identify refactoring opportunities.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Identify complex and problematic code: cyclomatic complexity, code smells, refactoring candidates, and cognitive complexity.

**Output:** Complexity report with prioritized refactoring targets.

---

## Architecture & Model Selection

**Data Gathering**: Sonnet (complexity requires understanding)
- Parse AST (Abstract Syntax Tree)
- Calculate complexity metrics
- Identify code patterns

**Analysis & Reasoning**: Sonnet (Plan agent)
- Interpret metrics
- Detect anti-patterns
- Generate refactoring recommendations

**Execution Pattern**:
1. Parse source files into AST
2. Calculate complexity metrics (cyclomatic, cognitive)
3. Detect code smells
4. Prioritize refactoring candidates
5. Generate actionable recommendations

---

---

## Phase 1: Calculate Cyclomatic Complexity

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import ast
import re
from collections import defaultdict

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Cyclomatic Complexity Analysis ===\n")
print(f"Project: {project_name}\n")

class ComplexityVisitor(ast.NodeVisitor):
    """Calculate cyclomatic complexity using AST"""

    def __init__(self):
        self.complexity = 1  # Base complexity
        self.functions = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        """Visit function definition"""
        # Save parent context
        parent_function = self.current_function

        # Create new function context
        func_visitor = ComplexityVisitor()
        func_visitor.current_function = node.name

        # Visit function body
        for child in node.body:
            func_visitor.visit(child)

        self.functions.append({
            'name': node.name,
            'line': node.lineno,
            'complexity': func_visitor.complexity,
            'params': len(node.args.args),
            'loc': node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
        })

        # Restore parent context
        self.current_function = parent_function

    def visit_If(self, node):
        """Count if statements"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """Count while loops"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        """Count for loops"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        """Count except handlers"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """Count boolean operators (and/or)"""
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Lambda(self, node):
        """Count lambda expressions"""
        self.complexity += 1
        self.generic_visit(node)

# Analyze all Python files
all_functions = []
file_complexities = []

python_files = list(project_root.rglob('*.py'))
# Exclude common directories
python_files = [f for f in python_files if not any(ex in str(f) for ex in ['venv', '__pycache__', 'node_modules', '.git'])]

print(f"Analyzing {len(python_files)} Python files...\n")

for file_path in python_files:
    try:
        source = file_path.read_text()
        tree = ast.parse(source)

        visitor = ComplexityVisitor()
        visitor.visit(tree)

        if visitor.functions:
            for func in visitor.functions:
                func['file'] = str(file_path.relative_to(project_root))
                all_functions.append(func)

            # File-level complexity
            file_complexity = sum(f['complexity'] for f in visitor.functions)
            file_complexities.append({
                'file': str(file_path.relative_to(project_root)),
                'complexity': file_complexity,
                'functions': len(visitor.functions)
            })
    except (SyntaxError, UnicodeDecodeError):
        pass

# Sort by complexity
all_functions.sort(key=lambda x: x['complexity'], reverse=True)
file_complexities.sort(key=lambda x: x['complexity'], reverse=True)

print(f"Functions Analyzed: {len(all_functions)}")
print(f"Files Analyzed: {len(file_complexities)}")
print()

# Display top complex functions
print("Most Complex Functions:")
for i, func in enumerate(all_functions[:15], 1):
    complexity_label = ""
    if func['complexity'] > 20:
        complexity_label = "CRITICAL"
    elif func['complexity'] > 10:
        complexity_label = "HIGH"
    elif func['complexity'] > 5:
        complexity_label = "MEDIUM"
    else:
        complexity_label = "LOW"

    print(f"{i:2d}. {func['name']:30s} CC={func['complexity']:2d} [{complexity_label}]")
    print(f"    {func['file']}:{func['line']} ({func['loc']} lines)")
print()

# Display top complex files
print("Most Complex Files:")
for i, file_info in enumerate(file_complexities[:10], 1):
    avg_complexity = file_info['complexity'] / file_info['functions']
    print(f"{i:2d}. {file_info['file']:50s} CC={file_info['complexity']:3d} (avg={avg_complexity:.1f})")
print()

# Complexity distribution
complexity_buckets = {
    '1-5 (Simple)': 0,
    '6-10 (Moderate)': 0,
    '11-20 (Complex)': 0,
    '21+ (Very Complex)': 0
}

for func in all_functions:
    cc = func['complexity']
    if cc <= 5:
        complexity_buckets['1-5 (Simple)'] += 1
    elif cc <= 10:
        complexity_buckets['6-10 (Moderate)'] += 1
    elif cc <= 20:
        complexity_buckets['11-20 (Complex)'] += 1
    else:
        complexity_buckets['21+ (Very Complex)'] += 1

print("Complexity Distribution:")
for bucket, count in complexity_buckets.items():
    percentage = (count / len(all_functions) * 100) if all_functions else 0
    bar_length = int(percentage / 2)
    bar = "█" * bar_length
    print(f"{bucket:20s} {count:4d} ({percentage:5.1f}%) {bar}")
print()
```

---

## Phase 2: Detect Code Smells

```python
print(f"=== Code Smell Detection ===\n")

code_smells = []

# 1. Long Functions (>50 lines)
for func in all_functions:
    if func['loc'] > 50:
        code_smells.append({
            'type': 'Long Function',
            'severity': 'HIGH',
            'location': f"{func['file']}:{func['line']}",
            'function': func['name'],
            'metric': f"{func['loc']} lines",
            'recommendation': 'Extract smaller functions, use composition'
        })

# 2. High Complexity (CC > 10)
for func in all_functions:
    if func['complexity'] > 10:
        code_smells.append({
            'type': 'High Complexity',
            'severity': 'CRITICAL' if func['complexity'] > 20 else 'HIGH',
            'location': f"{func['file']}:{func['line']}",
            'function': func['name'],
            'metric': f"CC={func['complexity']}",
            'recommendation': 'Simplify logic, reduce branching, extract methods'
        })

# 3. Too Many Parameters (>5)
for func in all_functions:
    if func['params'] > 5:
        code_smells.append({
            'type': 'Too Many Parameters',
            'severity': 'MEDIUM',
            'location': f"{func['file']}:{func['line']}",
            'function': func['name'],
            'metric': f"{func['params']} parameters",
            'recommendation': 'Use parameter object or configuration object'
        })

# 4. God Class (file with >500 LOC)
for file_info in file_complexities:
    # Estimate LOC (rough)
    file_path = project_root / file_info['file']
    if file_path.exists():
        try:
            loc = len(file_path.read_text().splitlines())
            if loc > 500:
                code_smells.append({
                    'type': 'God Class',
                    'severity': 'HIGH',
                    'location': file_info['file'],
                    'function': '',
                    'metric': f"{loc} lines",
                    'recommendation': 'Split into multiple focused classes/modules'
                })
        except:
            pass

# Group by severity
by_severity = defaultdict(list)
for smell in code_smells:
    by_severity[smell['severity']].append(smell)

print(f"Code Smells Detected: {len(code_smells)}\n")

for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    smells = by_severity[severity]
    if smells:
        print(f"{severity}: {len(smells)} smells")

        # Group by type
        by_type = defaultdict(list)
        for smell in smells:
            by_type[smell['type']].append(smell)

        for smell_type, instances in by_type.items():
            print(f"  - {smell_type}: {len(instances)}")
print()

# Show top smells
print("Top Priority Smells:")
priority_smells = sorted(code_smells, key=lambda x: (x['severity'] == 'CRITICAL', x['severity'] == 'HIGH'), reverse=True)

for i, smell in enumerate(priority_smells[:10], 1):
    print(f"{i:2d}. [{smell['severity']}] {smell['type']}")
    print(f"    Location: {smell['location']}")
    if smell['function']:
        print(f"    Function: {smell['function']} ({smell['metric']})")
    else:
        print(f"    {smell['metric']}")
    print(f"    Fix: {smell['recommendation']}")
    print()
```

---

## Phase 3: Cognitive Complexity

```python
print(f"=== Cognitive Complexity ===\n")

# Cognitive complexity is harder to measure but approximates mental effort
# Simplified version: complexity + nesting depth + recursion

class CognitiveComplexityVisitor(ast.NodeVisitor):
    """Calculate cognitive complexity"""

    def __init__(self):
        self.cognitive_complexity = 0
        self.nesting_level = 0
        self.functions = []

    def visit_FunctionDef(self, node):
        func_visitor = CognitiveComplexityVisitor()
        func_visitor.nesting_level = self.nesting_level

        for child in node.body:
            func_visitor.visit(child)

        self.functions.append({
            'name': node.name,
            'line': node.lineno,
            'cognitive': func_visitor.cognitive_complexity
        })

    def visit_If(self, node):
        self.cognitive_complexity += (1 + self.nesting_level)
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_While(self, node):
        self.cognitive_complexity += (1 + self.nesting_level)
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_For(self, node):
        self.cognitive_complexity += (1 + self.nesting_level)
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1

cognitive_scores = []

for file_path in python_files[:50]:  # Sample
    try:
        source = file_path.read_text()
        tree = ast.parse(source)

        visitor = CognitiveComplexityVisitor()
        visitor.visit(tree)

        for func in visitor.functions:
            func['file'] = str(file_path.relative_to(project_root))
            cognitive_scores.append(func)
    except:
        pass

# Sort by cognitive complexity
cognitive_scores.sort(key=lambda x: x['cognitive'], reverse=True)

print("Functions with High Cognitive Load:")
for i, func in enumerate(cognitive_scores[:10], 1):
    print(f"{i:2d}. {func['name']:30s} Cognitive={func['cognitive']:2d}")
    print(f"    {func['file']}:{func['line']}")
print()

print("Note: Cognitive complexity measures mental effort required to understand code.")
print("High cognitive complexity = harder to maintain, more bugs.")
print()
```

---

## Phase 4: Detect Duplicate Code

```python
print(f"=== Duplicate Code Detection ===\n")

# Simplified duplicate detection using hash
def get_code_blocks(source, block_size=5):
    """Extract code blocks (N consecutive lines)"""
    lines = [line.strip() for line in source.splitlines()]
    # Remove blank and comment lines
    lines = [line for line in lines if line and not line.startswith('#')]

    blocks = []
    for i in range(len(lines) - block_size + 1):
        block = '\n'.join(lines[i:i+block_size])
        if len(block) > 50:  # Ignore very short blocks
            blocks.append((hash(block), i, block))

    return blocks

duplicates = defaultdict(list)

for file_path in python_files[:100]:  # Sample
    try:
        source = file_path.read_text()
        blocks = get_code_blocks(source, block_size=5)

        for block_hash, line_num, block_text in blocks:
            duplicates[block_hash].append({
                'file': str(file_path.relative_to(project_root)),
                'line': line_num,
                'text': block_text[:100]  # First 100 chars
            })
    except:
        pass

# Find actual duplicates (appears more than once)
actual_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}

print(f"Duplicate Code Blocks: {len(actual_duplicates)}\n")

if actual_duplicates:
    print("Top Duplicates:")
    sorted_dups = sorted(actual_duplicates.items(), key=lambda x: len(x[1]), reverse=True)

    for i, (block_hash, instances) in enumerate(sorted_dups[:5], 1):
        print(f"{i}. Duplicated {len(instances)} times:")
        print(f"   Code: {instances[0]['text']}...")
        print(f"   Locations:")
        for inst in instances[:3]:
            print(f"     - {inst['file']}:{inst['line']}")
        if len(instances) > 3:
            print(f"     ... and {len(instances) - 3} more")
        print()

    print("Recommendation: Extract duplicated code into shared functions")
    print()
else:
    print("✓ No significant code duplication detected\n")
```

---

## Phase 5: Function Length Analysis

```python
print(f"=== Function Length Analysis ===\n")

# Categorize by length
length_buckets = {
    '1-10 lines': 0,
    '11-20 lines': 0,
    '21-50 lines': 0,
    '51-100 lines': 0,
    '100+ lines': 0
}

for func in all_functions:
    loc = func['loc']
    if loc <= 10:
        length_buckets['1-10 lines'] += 1
    elif loc <= 20:
        length_buckets['11-20 lines'] += 1
    elif loc <= 50:
        length_buckets['21-50 lines'] += 1
    elif loc <= 100:
        length_buckets['51-100 lines'] += 1
    else:
        length_buckets['100+ lines'] += 1

print("Function Length Distribution:")
for bucket, count in length_buckets.items():
    percentage = (count / len(all_functions) * 100) if all_functions else 0
    bar_length = int(percentage / 2)
    bar = "█" * bar_length
    print(f"{bucket:15s} {count:4d} ({percentage:5.1f}%) {bar}")
print()

# Find longest functions
longest = sorted(all_functions, key=lambda x: x['loc'], reverse=True)

print("Longest Functions:")
for i, func in enumerate(longest[:10], 1):
    print(f"{i:2d}. {func['name']:30s} {func['loc']:3d} lines")
    print(f"    {func['file']}:{func['line']}")
print()
```

---

## Phase 6: Class Complexity (OOP)

```python
print(f"=== Class Complexity Analysis ===\n")

class ClassVisitor(ast.NodeVisitor):
    """Analyze class complexity"""

    def __init__(self):
        self.classes = []

    def visit_ClassDef(self, node):
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]

        class_info = {
            'name': node.name,
            'line': node.lineno,
            'methods': len(methods),
            'method_names': [m.name for m in methods],
            'loc': node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
        }

        self.classes.append(class_info)
        self.generic_visit(node)

classes = []

for file_path in python_files[:100]:
    try:
        source = file_path.read_text()
        tree = ast.parse(source)

        visitor = ClassVisitor()
        visitor.visit(tree)

        for cls in visitor.classes:
            cls['file'] = str(file_path.relative_to(project_root))
            classes.append(cls)
    except:
        pass

if classes:
    print(f"Classes Found: {len(classes)}\n")

    # Sort by method count
    classes.sort(key=lambda x: x['methods'], reverse=True)

    print("Classes with Most Methods:")
    for i, cls in enumerate(classes[:10], 1):
        status = ""
        if cls['methods'] > 20:
            status = "[GOD CLASS]"
        elif cls['methods'] > 10:
            status = "[COMPLEX]"

        print(f"{i:2d}. {cls['name']:30s} {cls['methods']:2d} methods {status}")
        print(f"    {cls['file']}:{cls['line']}")
    print()

    # Detect god classes
    god_classes = [c for c in classes if c['methods'] > 20 or c['loc'] > 500]

    if god_classes:
        print(f"God Classes Detected: {len(god_classes)}")
        print("Recommendation: Split into smaller, focused classes")
        print()
else:
    print("No classes found (functional programming style)\n")
```

---

## Phase 7: Refactoring Priority

```python
print(f"=== Refactoring Priority ===\n")

refactoring_targets = []

for func in all_functions:
    # Calculate priority score
    score = 0

    # High complexity (most important)
    if func['complexity'] > 20:
        score += 10
    elif func['complexity'] > 10:
        score += 5

    # Long function
    if func['loc'] > 100:
        score += 8
    elif func['loc'] > 50:
        score += 4

    # Many parameters
    if func['params'] > 5:
        score += 3

    if score > 0:
        refactoring_targets.append({
            'function': func['name'],
            'file': func['file'],
            'line': func['line'],
            'score': score,
            'complexity': func['complexity'],
            'loc': func['loc'],
            'params': func['params']
        })

# Sort by priority score
refactoring_targets.sort(key=lambda x: x['score'], reverse=True)

print(f"Refactoring Targets: {len(refactoring_targets)}\n")

print("Top Priority (Start Here):")
for i, target in enumerate(refactoring_targets[:15], 1):
    print(f"{i:2d}. {target['function']:30s} (Priority: {target['score']})")
    print(f"    {target['file']}:{target['line']}")
    print(f"    Complexity: {target['complexity']}, Lines: {target['loc']}, Params: {target['params']}")

    # Specific recommendations
    recs = []
    if target['complexity'] > 10:
        recs.append("Reduce complexity: simplify conditionals")
    if target['loc'] > 50:
        recs.append("Extract smaller functions")
    if target['params'] > 5:
        recs.append("Use parameter object")

    if recs:
        print(f"    Actions: {', '.join(recs)}")
    print()
```

---

## Phase 8: Maintainability Index

```python
print(f"=== Maintainability Index ===\n")

# Simplified maintainability index
# Real formula: MI = 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(L)
# Where V = Halstead Volume, G = Cyclomatic Complexity, L = Lines of Code

# Simplified: Based on complexity and length
file_maintainability = []

for file_info in file_complexities:
    file_path = project_root / file_info['file']
    if file_path.exists():
        try:
            loc = len(file_path.read_text().splitlines())
            avg_complexity = file_info['complexity'] / file_info['functions'] if file_info['functions'] > 0 else 0

            # Simple maintainability score (0-100)
            # Lower complexity and shorter length = higher maintainability
            score = 100
            score -= min(avg_complexity * 3, 30)  # Complexity penalty
            score -= min(loc / 10, 50)  # Length penalty
            score = max(0, score)

            file_maintainability.append({
                'file': file_info['file'],
                'score': score,
                'complexity': file_info['complexity'],
                'loc': loc
            })
        except:
            pass

file_maintainability.sort(key=lambda x: x['score'])

print("Least Maintainable Files:")
for i, file_info in enumerate(file_maintainability[:10], 1):
    status = ""
    if file_info['score'] < 20:
        status = "CRITICAL"
    elif file_info['score'] < 40:
        status = "POOR"
    elif file_info['score'] < 60:
        status = "FAIR"
    else:
        status = "GOOD"

    print(f"{i:2d}. {file_info['file']:50s} Score: {file_info['score']:.1f} [{status}]")
print()

# Overall project maintainability
if file_maintainability:
    avg_maintainability = sum(f['score'] for f in file_maintainability) / len(file_maintainability)
    print(f"Project Maintainability: {avg_maintainability:.1f}/100")

    if avg_maintainability >= 70:
        print("  ✓✓✓ Excellent maintainability")
    elif avg_maintainability >= 50:
        print("  ✓✓ Good maintainability")
    elif avg_maintainability >= 30:
        print("  ✓ Fair maintainability - improvement needed")
    else:
        print("  ✗ Poor maintainability - urgent refactoring needed")
    print()
```

---

## Phase 9: Generate Recommendations

```python
print(f"=== Recommendations ===\n")

recommendations = []

# High complexity functions
high_complexity = [f for f in all_functions if f['complexity'] > 10]
if high_complexity:
    recommendations.append({
        'priority': 'CRITICAL',
        'title': f"Refactor {len(high_complexity)} high-complexity functions",
        'actions': [
            f"Start with: {', '.join(f['name'] for f in high_complexity[:3])}",
            "Break into smaller functions",
            "Simplify conditionals (use early returns)",
            "Extract complex logic into helper functions"
        ]
    })

# Long functions
long_functions = [f for f in all_functions if f['loc'] > 50]
if long_functions:
    recommendations.append({
        'priority': 'HIGH',
        'title': f"Shorten {len(long_functions)} long functions",
        'actions': [
            "Target: Keep functions under 50 lines",
            "Extract cohesive blocks into separate functions",
            "Use composition over monolithic functions"
        ]
    })

# Code smells
if code_smells:
    recommendations.append({
        'priority': 'HIGH',
        'title': f"Fix {len(code_smells)} code smells",
        'actions': [
            f"Address {len(by_severity['CRITICAL'])} critical smells first",
            "Use automated refactoring tools where possible",
            "Add tests before refactoring"
        ]
    })

# Duplicates
if actual_duplicates:
    recommendations.append({
        'priority': 'MEDIUM',
        'title': f"Remove {len(actual_duplicates)} duplicate code blocks",
        'actions': [
            "Extract common code into shared functions",
            "Use DRY principle (Don't Repeat Yourself)",
            "Consider using design patterns (Strategy, Template Method)"
        ]
    })

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. [{rec['priority']}] {rec['title']}")
    for action in rec['actions']:
        print(f"   - {action}")
    print()
```

---

---

**Complexity Philosophy:** Simplicity is the ultimate sophistication. Every branch, every line adds cognitive load. Minimize ruthlessly.
