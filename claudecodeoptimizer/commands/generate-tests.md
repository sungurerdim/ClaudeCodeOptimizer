---
id: cco-generate-tests
description: Auto-generate unit tests for untested code
category: testing
priority: normal
---

# Generate Unit Tests

Auto-generate unit tests for untested code in **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Increase test coverage:
1. Identify untested functions and methods
2. Generate comprehensive unit tests
3. Include edge cases and error scenarios
4. Follow testing best practices
5. Achieve target coverage (>80%)

**Output:** Generated test files with comprehensive test cases.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (fast scanning)
- Identify source files without tests
- Parse function signatures
- Extract existing test patterns

**Test Generation**: Haiku (efficient for straightforward tests)
- Generate test scaffolding
- Create test cases for common scenarios
- Follow project test conventions

**Execution Pattern**:
1. Scan codebase for coverage gaps
2. Analyze function signatures and logic
3. Generate test files in parallel
4. Validate generated tests compile/run

---

## When to Use

**Use this command:**
- Low test coverage (<60%)
- New features without tests
- Legacy code with no tests
- Before major refactoring (safety net)
- CI/CD test failures

**Critical for:**
- Production systems
- Public APIs
- Security-sensitive code

---

## Phase 1: Identify Untested Code

Find functions without test coverage:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import ast
import re

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Untested Code Identification ===\n")
print(f"Project: {project_name}\n")

# Find all source files
source_files = list(project_root.rglob('*.py'))
source_files = [f for f in source_files if 'test' not in str(f) and not any(ex in str(f) for ex in ['venv', '__pycache__', 'node_modules'])]

# Find all test files
test_files = list(project_root.rglob('test_*.py')) + list(project_root.rglob('*_test.py'))

print(f"Source Files: {len(source_files)}")
print(f"Test Files: {len(test_files)}")
print()

class FunctionExtractor(ast.NodeVisitor):
    """Extract function definitions"""

    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        # Skip private functions (starting with _)
        if not node.name.startswith('_'):
            self.functions.append({
                'name': node.name,
                'line': node.lineno,
                'args': [arg.arg for arg in node.args.args if arg.arg != 'self'],
                'returns': ast.unparse(node.returns) if node.returns else None,
                'docstring': ast.get_docstring(node),
                'is_async': isinstance(node, ast.AsyncFunctionDef)
            })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

# Extract all functions from source
all_functions = []

for file_path in source_files:
    try:
        source = file_path.read_text()
        tree = ast.parse(source)

        extractor = FunctionExtractor()
        extractor.visit(tree)

        for func in extractor.functions:
            func['file'] = str(file_path.relative_to(project_root))
            func['module'] = file_path.stem
            all_functions.append(func)
    except:
        pass

print(f"Public Functions Found: {len(all_functions)}")

# Check which functions have tests
tested_functions = set()

for test_file in test_files:
    try:
        content = test_file.read_text()
        # Look for test function names
        test_pattern = r'def\s+test_(\w+)'
        matches = re.findall(test_pattern, content)
        tested_functions.update(matches)
    except:
        pass

print(f"Functions with Tests: {len(tested_functions)}")

# Find untested functions
untested = [f for f in all_functions if f['name'] not in tested_functions]

print(f"Untested Functions: {len(untested)}")
print()

coverage_percent = ((len(all_functions) - len(untested)) / len(all_functions) * 100) if all_functions else 0

print(f"Estimated Coverage: {coverage_percent:.1f}%")
if coverage_percent >= 80:
    print("  ✓✓✓ Excellent coverage")
elif coverage_percent >= 60:
    print("  ✓✓ Good coverage")
elif coverage_percent >= 40:
    print("  ✓ Fair coverage - improvement needed")
else:
    print("  ✗ Poor coverage - critical gap")
print()
```

---

## Phase 2: Analyze Function Signatures

Understand what to test:

```python
print(f"=== Function Signature Analysis ===\n")

# Categorize by complexity
categorized = {
    'simple': [],      # No args or 1-2 args
    'moderate': [],    # 3-5 args
    'complex': [],     # 6+ args or async
}

for func in untested:
    arg_count = len(func['args'])

    if func['is_async'] or arg_count > 5:
        categorized['complex'].append(func)
    elif arg_count > 2:
        categorized['moderate'].append(func)
    else:
        categorized['simple'].append(func)

print("Untested Functions by Complexity:")
for category, funcs in categorized.items():
    print(f"  {category.title()}: {len(funcs)}")
print()

# Show samples
print("Sample Untested Functions:")
for i, func in enumerate(untested[:10], 1):
    args_str = ', '.join(func['args']) if func['args'] else 'no args'
    async_marker = '[async] ' if func['is_async'] else ''
    print(f"{i:2d}. {async_marker}{func['name']}({args_str})")
    print(f"    {func['file']}:{func['line']}")
    if func['docstring']:
        print(f"    Doc: {func['docstring'][:60]}...")
print()
```

---

## Phase 3: Generate Test Scaffolding

Create test file structure:

```python
print(f"=== Test File Generation ===\n")

from collections import defaultdict

# Group by source file
by_file = defaultdict(list)
for func in untested:
    by_file[func['file']].append(func)

print(f"Files Needing Tests: {len(by_file)}")
print()

def generate_test_file(source_file, functions):
    """Generate test file for source module"""

    # Determine test file path
    source_path = project_root / source_file
    test_dir = project_root / 'tests'
    test_dir.mkdir(exist_ok=True)

    # Mirror source structure in tests
    rel_path = source_path.relative_to(project_root)
    if 'src' in rel_path.parts:
        # Remove 'src' from path
        rel_parts = [p for p in rel_path.parts if p != 'src']
        test_path = test_dir / Path(*rel_parts[:-1]) / f"test_{rel_parts[-1]}"
    else:
        test_path = test_dir / f"test_{source_path.name}"

    test_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate test content
    module_name = source_path.stem
    import_path = str(source_path.relative_to(project_root)).replace('/', '.').replace('\\', '.')[:-3]

    lines = [
        '"""',
        f'Unit tests for {source_file}',
        'Auto-generated test scaffolding',
        '"""',
        '',
        'import pytest',
        f'from {import_path} import *',
        '',
        ''
    ]

    # Generate test class or functions
    for func in functions:
        # Test function name
        test_name = f"test_{func['name']}"

        # Generate test docstring
        lines.append(f"def {test_name}():")
        lines.append(f'    """Test {func["name"]} function"""')

        # Generate test cases based on args
        if not func['args']:
            # No args - simple call
            lines.append(f'    # Test basic functionality')
            lines.append(f'    result = {func["name"]}()')
            lines.append(f'    assert result is not None')
        else:
            # With args - generate sample inputs
            lines.append(f'    # Test with valid inputs')
            sample_args = ', '.join([f'arg_{arg}' for arg in func['args']])
            lines.append(f'    # TODO: Replace with actual test values')
            lines.append(f'    # result = {func["name"]}({sample_args})')
            lines.append(f'    # assert result == expected_value')
            lines.append(f'    pass  # TODO: Implement test')

        lines.append('')

        # Add edge case test
        lines.append(f"def {test_name}_edge_cases():")
        lines.append(f'    """Test {func["name"]} edge cases"""')
        lines.append(f'    # TODO: Test edge cases:')
        lines.append(f'    # - Null/None inputs')
        lines.append(f'    # - Empty inputs')
        lines.append(f'    # - Boundary values')
        lines.append(f'    pass  # TODO: Implement test')
        lines.append('')

        # Add error test
        lines.append(f"def {test_name}_errors():")
        lines.append(f'    """Test {func["name"]} error handling"""')
        lines.append(f'    # TODO: Test error scenarios:')
        lines.append(f'    # - Invalid input types')
        lines.append(f'    # - Out of range values')
        lines.append(f'    with pytest.raises(Exception):')
        lines.append(f'        pass  # TODO: Call with invalid input')
        lines.append('')
        lines.append('')

    return test_path, '\n'.join(lines)

# Generate test files
generated_files = []

for source_file, functions in list(by_file.items())[:5]:  # Limit for demo
    test_path, test_content = generate_test_file(source_file, functions)

    print(f"Generated: {test_path.relative_to(project_root)}")
    print(f"  Tests for {len(functions)} functions")

    # Write file
    # test_path.write_text(test_content)  # Commented out for safety

    generated_files.append({
        'path': str(test_path.relative_to(project_root)),
        'source': source_file,
        'function_count': len(functions),
        'content': test_content
    })

print()
print(f"Total Test Files Generated: {len(generated_files)}")
print()
```

---

## Phase 4: Generate Specific Test Cases

Create detailed test implementations:

```python
print(f"=== Specific Test Case Generation ===\n")

def generate_test_cases(func_info):
    """Generate specific test cases for a function"""

    test_cases = []

    # Analyze function to determine test scenarios
    func_name = func_info['name']
    args = func_info['args']

    # 1. Happy path test
    test_cases.append({
        'name': f'test_{func_name}_happy_path',
        'description': f'Test {func_name} with valid inputs',
        'type': 'positive',
        'code': f'''
def test_{func_name}_happy_path():
    """Test {func_name} with valid inputs"""
    # Arrange
    # TODO: Set up test data

    # Act
    # result = {func_name}(...)

    # Assert
    # assert result == expected
    pass
'''
    })

    # 2. Edge cases
    if args:
        test_cases.append({
            'name': f'test_{func_name}_empty_input',
            'description': f'Test {func_name} with empty/null inputs',
            'type': 'edge_case',
            'code': f'''
def test_{func_name}_empty_input():
    """Test {func_name} with empty inputs"""
    # Test with None
    # Test with empty string
    # Test with empty list/dict
    pass
'''
        })

    # 3. Error cases
    test_cases.append({
        'name': f'test_{func_name}_invalid_input',
        'description': f'Test {func_name} with invalid inputs',
        'type': 'negative',
        'code': f'''
def test_{func_name}_invalid_input():
    """Test {func_name} error handling"""
    with pytest.raises(ValueError):
        {func_name}(invalid_value)
'''
    })

    # 4. Boundary tests
    if any('count' in arg or 'size' in arg or 'length' in arg for arg in args):
        test_cases.append({
            'name': f'test_{func_name}_boundaries',
            'description': f'Test {func_name} boundary values',
            'type': 'boundary',
            'code': f'''
def test_{func_name}_boundaries():
    """Test {func_name} with boundary values"""
    # Test with 0
    # Test with max value
    # Test with negative values
    pass
'''
        })

    return test_cases

# Generate for sample functions
print("Sample Test Cases:")

for i, func in enumerate(untested[:3], 1):
    print(f"\n{i}. Function: {func['name']}")
    print(f"   File: {func['file']}")

    test_cases = generate_test_cases(func)

    print(f"   Generated {len(test_cases)} test cases:")
    for tc in test_cases:
        print(f"     - {tc['name']} ({tc['type']})")
```

---

## Phase 5: Add Fixtures and Mocks

Generate test helpers:

```python
print(f"\n=== Test Fixtures Generation ===\n")

def generate_conftest(project_root):
    """Generate pytest conftest.py with common fixtures"""

    conftest_content = '''"""
Pytest configuration and shared fixtures
Auto-generated
"""

import pytest

@pytest.fixture
def sample_data():
    """Provide sample test data"""
    return {
        "id": 1,
        "name": "Test",
        "value": 100
    }

@pytest.fixture
def mock_database(monkeypatch):
    """Mock database connection"""
    class MockDB:
        def __init__(self):
            self.data = {}

        def get(self, key):
            return self.data.get(key)

        def set(self, key, value):
            self.data[key] = value

    return MockDB()

@pytest.fixture
def temp_file(tmp_path):
    """Create temporary test file"""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path

@pytest.fixture(autouse=True)
def reset_state():
    """Reset state before each test"""
    # Reset global state
    yield
    # Cleanup after test
    pass
'''

    conftest_path = project_root / 'tests' / 'conftest.py'
    return conftest_path, conftest_content

conftest_path, conftest_content = generate_conftest(project_root)

print(f"Generated: {conftest_path.relative_to(project_root)}")
print("Contains common fixtures:")
print("  - sample_data: Test data fixture")
print("  - mock_database: Database mock")
print("  - temp_file: Temporary file fixture")
print("  - reset_state: Auto cleanup")
print()
```

---

## Phase 6: Generate Integration Test Stubs

Create integration test scaffolding:

```python
print(f"=== Integration Test Generation ===\n")

integration_test_content = '''"""
Integration tests
Auto-generated scaffolding
"""

import pytest

class TestIntegration:
    """Integration test suite"""

    def test_end_to_end_workflow(self):
        """Test complete workflow"""
        # Arrange: Set up system state
        # Act: Execute workflow
        # Assert: Verify end state
        pass

    def test_service_integration(self):
        """Test service-to-service integration"""
        # Test how services interact
        pass

    def test_database_integration(self):
        """Test database operations"""
        # Test actual DB interactions
        pass

    def test_api_integration(self):
        """Test API endpoints"""
        # Test HTTP requests/responses
        pass
'''

print("Generated integration test stubs:")
print("  - test_end_to_end_workflow")
print("  - test_service_integration")
print("  - test_database_integration")
print("  - test_api_integration")
print()
```

---

## Phase 7: Validate Generated Tests

Check tests can run:

```python
print(f"=== Test Validation ===\n")

import subprocess

# Try to run pytest on generated tests
print("Validating generated tests...")

try:
    result = subprocess.run(
        ['python', '-m', 'pytest', '--collect-only', 'tests/'],
        capture_output=True,
        text=True,
        cwd=project_root,
        timeout=30
    )

    if result.returncode == 0:
        # Parse output to count tests
        output = result.stdout
        test_count = output.count('test_')

        print(f"✓ Tests are valid")
        print(f"  Collected {test_count} tests")
    else:
        print(f"⚠ Some tests have syntax errors")
        print(f"  Check pytest output for details")
except subprocess.TimeoutExpired:
    print("⚠ Test collection timed out")
except FileNotFoundError:
    print("ℹ pytest not found - install with: pip install pytest")

print()
```

---

## Phase 8: Generate Test Documentation

Document testing approach:

```python
print(f"=== Test Documentation ===\n")

test_readme = f'''# Test Suite

Auto-generated tests for {project_name}

## Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_*.py            # Unit tests (mirror source)
└── integration/         # Integration tests
```

## Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_module.py

# With coverage
pytest --cov=src --cov-report=html

# Verbose
pytest -v
```

## Coverage Goals

- Unit tests: >80% coverage
- Integration tests: Critical paths
- Edge cases: All error scenarios

## Writing Tests

Follow AAA pattern:
1. **Arrange**: Set up test data
2. **Act**: Execute function
3. **Assert**: Verify results

## TODO

Generated tests contain TODO comments.
Replace with actual test implementations:
- [ ] Add real test data
- [ ] Implement assertions
- [ ] Add more edge cases
- [ ] Remove placeholder pass statements
'''

readme_path = project_root / 'tests' / 'README.md'

print(f"Generated: {readme_path.relative_to(project_root)}")
print()
print("Documentation includes:")
print("  - Directory structure")
print("  - Running instructions")
print("  - Coverage goals")
print("  - Writing guidelines")
print()
```

---

## Phase 9: Generate Coverage Report

Show coverage gaps:

```python
print(f"=== Coverage Report ===\n")

print("To measure actual coverage:")
print()
print("  1. Install coverage tool:")
print("     pip install pytest-cov")
print()
print("  2. Run tests with coverage:")
print("     pytest --cov=src --cov-report=html")
print()
print("  3. View report:")
print("     open htmlcov/index.html")
print()

print("Target Coverage:")
print("  Minimum: 60%")
print("  Good: 80%")
print("  Excellent: 90%+")
print()
```

---

## Phase 10: Summary Report

Final summary:

```python
print(f"=== Summary ===\n")

summary = {
    'total_functions': len(all_functions),
    'tested_functions': len(tested_functions),
    'untested_functions': len(untested),
    'test_files_generated': len(generated_files),
    'coverage_before': coverage_percent,
    'coverage_target': 80.0
}

print(f"Analysis Results:")
print(f"  Total Functions: {summary['total_functions']}")
print(f"  Already Tested: {summary['tested_functions']}")
print(f"  Untested: {summary['untested_functions']}")
print()

print(f"Generated Tests:")
print(f"  Test Files: {summary['test_files_generated']}")
print(f"  Estimated New Tests: {len(untested) * 3}")  # 3 tests per function
print()

print(f"Coverage:")
print(f"  Current: {summary['coverage_before']:.1f}%")
print(f"  Target: {summary['coverage_target']:.1f}%")
gap = summary['coverage_target'] - summary['coverage_before']
if gap > 0:
    print(f"  Gap: {gap:.1f}% to reach target")
else:
    print(f"  ✓ Target achieved!")
print()

print("Next Steps:")
print("  1. Review generated test files")
print("  2. Replace TODO comments with real tests")
print("  3. Add actual test data and assertions")
print("  4. Run tests: pytest -v")
print("  5. Measure coverage: pytest --cov")
print()
```

---

## Output Example

```
=== Untested Code Identification ===

Project: backend

Source Files: 147
Test Files: 23

Public Functions Found: 523
Functions with Tests: 312
Untested Functions: 211

Estimated Coverage: 59.7%
  ✓ Fair coverage - improvement needed

=== Function Signature Analysis ===

Untested Functions by Complexity:
  Simple: 98
  Moderate: 87
  Complex: 26

Sample Untested Functions:
 1. calculate_total(items, discount)
    src/utils/calculator.py:45
 2. [async] fetch_user_data(user_id)
    src/services/user.py:89
 3. validate_email(email)
    src/validators/email.py:12

=== Test File Generation ===

Files Needing Tests: 67

Generated: tests/test_calculator.py
  Tests for 8 functions
Generated: tests/test_user.py
  Tests for 12 functions
Generated: tests/test_email.py
  Tests for 3 functions

Total Test Files Generated: 5

=== Test Fixtures Generation ===

Generated: tests/conftest.py
Contains common fixtures:
  - sample_data: Test data fixture
  - mock_database: Database mock
  - temp_file: Temporary file fixture
  - reset_state: Auto cleanup

=== Summary ===

Analysis Results:
  Total Functions: 523
  Already Tested: 312
  Untested: 211

Generated Tests:
  Test Files: 5
  Estimated New Tests: 633

Coverage:
  Current: 59.7%
  Target: 80.0%
  Gap: 20.3% to reach target

Next Steps:
  1. Review generated test files
  2. Replace TODO comments with real tests
  3. Add actual test data and assertions
  4. Run tests: pytest -v
  5. Measure coverage: pytest --cov
```

---

**Testing Philosophy:** Tests are not overhead - they are insurance. Write tests that would catch the bugs you've actually seen.
