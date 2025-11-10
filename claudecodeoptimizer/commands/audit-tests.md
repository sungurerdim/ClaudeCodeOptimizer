---
id: cco-audit-tests
description: Test quality, coverage gaps, flaky tests
category: testing
priority: normal
---

# Audit Test Suite

Audit test quality, find coverage gaps, and detect flaky tests in **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Comprehensive test suite analysis:
1. Measure test coverage and identify gaps
2. Assess test quality and effectiveness
3. Detect flaky/unreliable tests
4. Find slow tests
5. Identify test anti-patterns

**Output:** Test quality report with improvement recommendations.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (fast test scanning)
- Parse test files
- Extract test metadata
- Collect coverage data

**Analysis & Reasoning**: Sonnet (quality assessment)
- Evaluate test quality
- Detect patterns and anti-patterns
- Generate recommendations

**Execution Pattern**:
1. Scan test files and extract metadata
2. Run tests with coverage analysis
3. Analyze test execution patterns
4. Detect quality issues
5. Generate improvement recommendations

---

## When to Use

**Use this command:**
- Before releases
- During test maintenance
- When tests are unreliable
- To improve test suite quality
- When CI/CD is slow

**Critical for:**
- Production systems
- High-stakes deployments
- Legacy test suites

---

## Phase 1: Test Discovery

Find and categorize all tests:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import ast
import re
from collections import defaultdict

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Test Suite Discovery ===\n")
print(f"Project: {project_name}\n")

# Find test files
test_patterns = ['test_*.py', '*_test.py', 'test*.py']
test_files = []

for pattern in test_patterns:
    test_files.extend(project_root.rglob(pattern))

# Deduplicate and filter
test_files = list(set([f for f in test_files if not any(ex in str(f) for ex in ['venv', '__pycache__', 'node_modules'])]))

print(f"Test Files Found: {len(test_files)}")

class TestExtractor(ast.NodeVisitor):
    """Extract test functions and metadata"""

    def __init__(self):
        self.tests = []
        self.fixtures = []
        self.current_class = None

    def visit_ClassDef(self, node):
        # Save class context
        old_class = self.current_class
        if node.name.startswith('Test'):
            self.current_class = node.name

        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        name = node.name

        # Check if it's a test function
        if name.startswith('test_'):
            # Extract assertions count
            assertion_count = sum(1 for n in ast.walk(node) if isinstance(n, ast.Assert))

            # Check for decorators
            decorators = [d.id if isinstance(d, ast.Name) else getattr(d, 'attr', '') for d in node.decorator_list]

            self.tests.append({
                'name': name,
                'line': node.lineno,
                'class': self.current_class,
                'assertions': assertion_count,
                'decorators': decorators,
                'params': len(node.args.args),
                'is_async': isinstance(node, ast.AsyncFunctionDef),
                'docstring': ast.get_docstring(node),
                'loc': node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
            })

        # Check if it's a fixture
        elif any(d.id == 'fixture' if isinstance(d, ast.Name) else getattr(d, 'attr', '') == 'fixture' for d in node.decorator_list):
            self.fixtures.append({
                'name': name,
                'line': node.lineno
            })

# Extract tests from all test files
all_tests = []
all_fixtures = []

for test_file in test_files:
    try:
        source = test_file.read_text()
        tree = ast.parse(source)

        extractor = TestExtractor()
        extractor.visit(tree)

        for test in extractor.tests:
            test['file'] = str(test_file.relative_to(project_root))
            all_tests.append(test)

        for fixture in extractor.fixtures:
            fixture['file'] = str(test_file.relative_to(project_root))
            all_fixtures.append(fixture)

    except:
        pass

print(f"Test Functions: {len(all_tests)}")
print(f"Fixtures: {len(all_fixtures)}")
print()

# Categorize tests
unit_tests = [t for t in all_tests if 'integration' not in t['file'] and 'e2e' not in t['file']]
integration_tests = [t for t in all_tests if 'integration' in t['file']]
e2e_tests = [t for t in all_tests if 'e2e' in t['file'] or 'end_to_end' in t['file']]

print("Test Distribution:")
print(f"  Unit Tests: {len(unit_tests)}")
print(f"  Integration Tests: {len(integration_tests)}")
print(f"  E2E Tests: {len(e2e_tests)}")
print()
```

---

## Phase 2: Run Tests with Coverage

Execute tests and measure coverage:

```python
print(f"=== Test Execution & Coverage ===\n")

import subprocess
import json
import time

# Run pytest with coverage
print("Running tests with coverage...")
start_time = time.time()

try:
    result = subprocess.run(
        ['python', '-m', 'pytest', '--cov=src', '--cov=.', '--cov-report=json', '--json-report', '--json-report-file=test-report.json', '-v'],
        capture_output=True,
        text=True,
        cwd=project_root,
        timeout=300
    )

    execution_time = time.time() - start_time

    print(f"Tests completed in {execution_time:.2f}s")
    print()

    # Parse results
    output = result.stdout

    # Extract test counts
    passed = output.count(' PASSED')
    failed = output.count(' FAILED')
    skipped = output.count(' SKIPPED')
    total = passed + failed + skipped

    print("Test Results:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {total}")
    print()

    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")

    if success_rate >= 95:
        print("  ✓✓✓ Excellent")
    elif success_rate >= 85:
        print("  ✓✓ Good")
    elif success_rate >= 70:
        print("  ✓ Fair")
    else:
        print("  ✗ Poor - many failing tests")
    print()

    # Parse coverage (if .coverage file exists)
    coverage_file = project_root / '.coverage'
    coverage_json = project_root / 'coverage.json'

    if coverage_json.exists():
        cov_data = json.loads(coverage_json.read_text())
        total_coverage = cov_data.get('totals', {}).get('percent_covered', 0)

        print(f"Code Coverage: {total_coverage:.1f}%")

        if total_coverage >= 80:
            print("  ✓✓✓ Excellent coverage")
        elif total_coverage >= 60:
            print("  ✓✓ Good coverage")
        elif total_coverage >= 40:
            print("  ✓ Fair coverage")
        else:
            print("  ✗ Poor coverage")
        print()

except subprocess.TimeoutExpired:
    print("⚠ Tests timed out (>5 minutes)")
    print("  Investigate slow tests")
except FileNotFoundError:
    print("ℹ pytest not found")
    print("  Install: pip install pytest pytest-cov pytest-json-report")
    print()
```

---

## Phase 3: Detect Flaky Tests

Find unreliable tests:

```python
print(f"=== Flaky Test Detection ===\n")

# Run tests multiple times to detect flakiness
print("Running tests 3 times to detect flaky behavior...")
print("(In production, run 10+ times for better detection)")
print()

test_results = defaultdict(list)

for run in range(3):
    try:
        result = subprocess.run(
            ['python', '-m', 'pytest', '-v', '--tb=no'],
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=60
        )

        # Parse results per test
        for line in result.stdout.splitlines():
            if ' PASSED' in line or ' FAILED' in line:
                test_name = line.split('::')[-1].split(' ')[0]
                status = 'PASSED' if ' PASSED' in line else 'FAILED'
                test_results[test_name].append(status)

    except (subprocess.TimeoutExpired, FileNotFoundError):
        break

# Identify flaky tests (inconsistent results)
flaky_tests = []

for test_name, results in test_results.items():
    if len(set(results)) > 1:  # Different results across runs
        flaky_tests.append({
            'name': test_name,
            'results': results,
            'pass_rate': results.count('PASSED') / len(results) * 100
        })

if flaky_tests:
    print(f"Flaky Tests Detected: {len(flaky_tests)}\n")

    for i, test in enumerate(flaky_tests, 1):
        print(f"{i}. {test['name']}")
        print(f"   Results: {', '.join(test['results'])}")
        print(f"   Pass Rate: {test['pass_rate']:.0f}%")
    print()

    print("Flaky tests are unreliable and should be fixed ASAP.")
    print("Common causes:")
    print("  - Race conditions")
    print("  - External dependencies")
    print("  - Time-dependent logic")
    print("  - Shared mutable state")
    print()
else:
    print("✓ No flaky tests detected (in 3 runs)\n")
```

---

## Phase 4: Identify Slow Tests

Find performance bottlenecks:

```python
print(f"=== Slow Test Detection ===\n")

# Run tests with duration tracking
try:
    result = subprocess.run(
        ['python', '-m', 'pytest', '--durations=0', '-v'],
        capture_output=True,
        text=True,
        cwd=project_root,
        timeout=60
    )

    # Parse durations
    duration_section = False
    test_durations = []

    for line in result.stdout.splitlines():
        if 'slowest' in line.lower():
            duration_section = True
            continue

        if duration_section and 's call' in line:
            # Parse: 0.50s call tests/test_foo.py::test_bar
            parts = line.strip().split()
            if len(parts) >= 3:
                duration = float(parts[0].replace('s', ''))
                test_name = parts[-1]
                test_durations.append({
                    'name': test_name,
                    'duration': duration
                })

    # Sort by duration
    test_durations.sort(key=lambda x: x['duration'], reverse=True)

    if test_durations:
        print("Slowest Tests:")
        for i, test in enumerate(test_durations[:10], 1):
            slow_marker = ""
            if test['duration'] > 5:
                slow_marker = " [VERY SLOW]"
            elif test['duration'] > 1:
                slow_marker = " [SLOW]"

            print(f"{i:2d}. {test['name']:60s} {test['duration']:.2f}s{slow_marker}")
        print()

        # Calculate total time
        total_time = sum(t['duration'] for t in test_durations)
        print(f"Total Test Time: {total_time:.2f}s")

        # Slow test threshold
        slow_tests = [t for t in test_durations if t['duration'] > 1.0]
        very_slow_tests = [t for t in test_durations if t['duration'] > 5.0]

        print(f"Slow Tests (>1s): {len(slow_tests)}")
        print(f"Very Slow Tests (>5s): {len(very_slow_tests)}")
        print()

        if very_slow_tests:
            print("⚠ Very slow tests detected!")
            print("  Consider: Mocking, parallelization, or moving to integration suite")
            print()

except (subprocess.TimeoutExpired, FileNotFoundError):
    pass
```

---

## Phase 5: Test Quality Assessment

Evaluate test effectiveness:

```python
print(f"=== Test Quality Assessment ===\n")

quality_issues = []

# 1. Tests without assertions
tests_no_assertions = [t for t in all_tests if t['assertions'] == 0]

if tests_no_assertions:
    quality_issues.append({
        'type': 'No Assertions',
        'severity': 'HIGH',
        'count': len(tests_no_assertions),
        'description': 'Tests that don\'t verify anything',
        'recommendation': 'Add assertions to verify expected behavior'
    })

# 2. Tests without docstrings
tests_no_docs = [t for t in all_tests if not t['docstring']]

if len(tests_no_docs) > len(all_tests) * 0.5:  # >50% without docs
    quality_issues.append({
        'type': 'Missing Docstrings',
        'severity': 'MEDIUM',
        'count': len(tests_no_docs),
        'description': 'Tests without documentation',
        'recommendation': 'Add docstrings explaining what is being tested'
    })

# 3. Very long tests (>50 lines)
long_tests = [t for t in all_tests if t['loc'] > 50]

if long_tests:
    quality_issues.append({
        'type': 'Long Tests',
        'severity': 'MEDIUM',
        'count': len(long_tests),
        'description': 'Tests that are too long',
        'recommendation': 'Break into smaller, focused tests'
    })

# 4. Tests with many assertions (>10)
many_assertions = [t for t in all_tests if t['assertions'] > 10]

if many_assertions:
    quality_issues.append({
        'type': 'Too Many Assertions',
        'severity': 'LOW',
        'count': len(many_assertions),
        'description': 'Tests verifying too many things',
        'recommendation': 'Split into multiple focused tests'
    })

# Display quality issues
if quality_issues:
    print(f"Quality Issues Found: {len(quality_issues)}\n")

    for issue in quality_issues:
        print(f"[{issue['severity']}] {issue['type']}")
        print(f"  Count: {issue['count']}")
        print(f"  Issue: {issue['description']}")
        print(f"  Fix: {issue['recommendation']}")
        print()
else:
    print("✓ No major quality issues detected\n")

# Quality score
quality_score = 100

for issue in quality_issues:
    if issue['severity'] == 'HIGH':
        quality_score -= 20
    elif issue['severity'] == 'MEDIUM':
        quality_score -= 10
    elif issue['severity'] == 'LOW':
        quality_score -= 5

quality_score = max(0, quality_score)

print(f"Test Quality Score: {quality_score}/100")

if quality_score >= 80:
    print("  ✓✓✓ High-quality test suite")
elif quality_score >= 60:
    print("  ✓✓ Good test suite")
elif quality_score >= 40:
    print("  ✓ Fair test suite - needs improvement")
else:
    print("  ✗ Poor test suite - major issues")
print()
```

---

## Phase 6: Test Anti-Patterns

Detect common anti-patterns:

```python
print(f"=== Test Anti-Pattern Detection ===\n")

anti_patterns = []

# 1. Sleep in tests (brittle timing)
for test_file in test_files:
    try:
        content = test_file.read_text()
        if 'time.sleep' in content or 'sleep(' in content:
            anti_patterns.append({
                'pattern': 'Sleep in Tests',
                'severity': 'HIGH',
                'file': str(test_file.relative_to(project_root)),
                'issue': 'Using sleep() makes tests slow and brittle',
                'fix': 'Use proper waiting mechanisms or mocks'
            })
    except:
        pass

# 2. Hardcoded values
for test_file in test_files:
    try:
        content = test_file.read_text()
        # Look for hardcoded URLs, IPs, etc.
        if re.search(r'https?://(?!localhost|127\.0\.0\.1|example\.com)', content):
            anti_patterns.append({
                'pattern': 'Hardcoded External URLs',
                'severity': 'MEDIUM',
                'file': str(test_file.relative_to(project_root)),
                'issue': 'Tests depend on external services',
                'fix': 'Mock external dependencies'
            })
    except:
        pass

# 3. Tests depending on execution order
for test in all_tests:
    if 'order' in test['name'].lower() or any('order' in d for d in test['decorators']):
        anti_patterns.append({
            'pattern': 'Order-Dependent Tests',
            'severity': 'HIGH',
            'file': test['file'],
            'issue': 'Tests should be independent',
            'fix': 'Ensure each test can run in isolation'
        })

if anti_patterns:
    print(f"Anti-Patterns Found: {len(anti_patterns)}\n")

    for ap in anti_patterns:
        print(f"[{ap['severity']}] {ap['pattern']}")
        print(f"  File: {ap['file']}")
        print(f"  Issue: {ap['issue']}")
        print(f"  Fix: {ap['fix']}")
        print()
else:
    print("✓ No common anti-patterns detected\n")
```

---

## Phase 7: Coverage Gap Analysis

Find untested code:

```python
print(f"=== Coverage Gap Analysis ===\n")

coverage_json = project_root / 'coverage.json'

if coverage_json.exists():
    try:
        cov_data = json.loads(coverage_json.read_text())
        files = cov_data.get('files', {})

        # Find files with low coverage
        low_coverage_files = []

        for file_path, file_data in files.items():
            coverage_percent = file_data.get('summary', {}).get('percent_covered', 0)

            if coverage_percent < 60:  # Less than 60%
                low_coverage_files.append({
                    'file': file_path,
                    'coverage': coverage_percent,
                    'missing_lines': file_data.get('summary', {}).get('missing_lines', 0)
                })

        low_coverage_files.sort(key=lambda x: x['coverage'])

        if low_coverage_files:
            print(f"Files with Low Coverage (<60%): {len(low_coverage_files)}\n")

            print("Top Priority (Lowest Coverage):")
            for i, file_info in enumerate(low_coverage_files[:10], 1):
                print(f"{i:2d}. {file_info['file']:50s} {file_info['coverage']:.1f}% ({file_info['missing_lines']} lines)")
            print()
        else:
            print("✓ All files have good coverage (>60%)\n")

    except:
        print("Could not parse coverage data\n")
else:
    print("No coverage data available")
    print("Run: pytest --cov --cov-report=json")
    print()
```

---

## Phase 8: Recommendations

Generate improvement plan:

```python
print(f"=== Recommendations ===\n")

recommendations = []

# Flaky tests
if flaky_tests:
    recommendations.append({
        'priority': 'CRITICAL',
        'title': f'Fix {len(flaky_tests)} flaky tests',
        'actions': [
            'Investigate race conditions',
            'Remove external dependencies',
            'Use proper test isolation',
            'Fix time-dependent logic'
        ]
    })

# Slow tests
if very_slow_tests:
    recommendations.append({
        'priority': 'HIGH',
        'title': f'Optimize {len(very_slow_tests)} very slow tests',
        'actions': [
            'Mock expensive operations',
            'Move to integration suite if appropriate',
            'Use test parallelization',
            'Optimize test data setup'
        ]
    })

# Quality issues
if quality_issues:
    recommendations.append({
        'priority': 'HIGH',
        'title': 'Improve test quality',
        'actions': [
            f'Add assertions to {tests_no_assertions and len(tests_no_assertions)} tests' if tests_no_assertions else None,
            f'Add docstrings to {tests_no_docs and len(tests_no_docs)} tests' if tests_no_docs else None,
            f'Split {len(long_tests)} long tests' if long_tests else None
        ]
    })

# Coverage gaps
if low_coverage_files:
    recommendations.append({
        'priority': 'MEDIUM',
        'title': f'Increase coverage for {len(low_coverage_files)} files',
        'actions': [
            'Start with critical business logic',
            'Use /cco-generate-tests for scaffolding',
            'Target 80% coverage minimum'
        ]
    })

# Display
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. [{rec['priority']}] {rec['title']}")
    for action in rec['actions']:
        if action:  # Filter None values
            print(f"   - {action}")
    print()

if not recommendations:
    print("✓ Test suite is in excellent shape!\n")
```

---

## Output Example

```
=== Test Suite Discovery ===

Project: backend

Test Files Found: 23

Test Functions: 342
Fixtures: 45

Test Distribution:
  Unit Tests: 298
  Integration Tests: 38
  E2E Tests: 6

=== Test Execution & Coverage ===

Running tests with coverage...
Tests completed in 24.56s

Test Results:
  Passed: 328
  Failed: 2
  Skipped: 12
  Total: 342

Success Rate: 95.9%
  ✓✓✓ Excellent

Code Coverage: 73.4%
  ✓✓ Good coverage

=== Flaky Test Detection ===

Running tests 3 times to detect flaky behavior...

Flaky Tests Detected: 2

1. test_concurrent_access
   Results: PASSED, FAILED, PASSED
   Pass Rate: 67%
2. test_cache_expiry
   Results: PASSED, PASSED, FAILED
   Pass Rate: 67%

=== Slow Test Detection ===

Slowest Tests:
 1. test_full_report_generation                               5.43s [VERY SLOW]
 2. test_database_migration                                   3.21s [SLOW]
 3. test_bulk_import                                          2.87s [SLOW]

Total Test Time: 24.56s
Slow Tests (>1s): 12
Very Slow Tests (>5s): 1

⚠ Very slow tests detected!
  Consider: Mocking, parallelization, or moving to integration suite

=== Test Quality Assessment ===

Quality Issues Found: 3

[HIGH] No Assertions
  Count: 8
  Issue: Tests that don't verify anything
  Fix: Add assertions to verify expected behavior

[MEDIUM] Long Tests
  Count: 5
  Issue: Tests that are too long
  Fix: Break into smaller, focused tests

Test Quality Score: 70/100
  ✓✓ Good test suite

=== Recommendations ===

1. [CRITICAL] Fix 2 flaky tests
   - Investigate race conditions
   - Remove external dependencies
   - Use proper test isolation
   - Fix time-dependent logic

2. [HIGH] Optimize 1 very slow tests
   - Mock expensive operations
   - Move to integration suite if appropriate
   - Use test parallelization
   - Optimize test data setup

3. [HIGH] Improve test quality
   - Add assertions to 8 tests
   - Split 5 long tests
```

---

**Testing Philosophy:** Flaky tests are worse than no tests - they erode trust in the entire suite. Fix or remove them immediately.
