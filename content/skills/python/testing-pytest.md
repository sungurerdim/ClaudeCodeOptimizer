---
metadata:
  name: "Pytest Testing Patterns"
  activation_keywords: ["test", "pytest", "fixture", "mock", "parametrize"]
  category: "language-python"
principles: ['U_TEST_FIRST', 'U_EVIDENCE_BASED', 'P_TEST_COVERAGE', 'P_TEST_PYRAMID', 'P_CI_GATES', 'P_TEST_ISOLATION']
---

# Pytest Testing Patterns

Master pytest fixtures, parametrization, and mocking strategies for comprehensive test coverage.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Core Pytest Concepts:**
- Fixtures provide reusable test dependencies (scope: function, class, module, session)
- `@pytest.mark.parametrize` runs test with multiple input sets
- `conftest.py` shares fixtures across test files
- `pytest-mock` provides `mocker` fixture for mocking
- Assertions use plain `assert` with detailed failure messages

**Key Patterns:**
1. Use fixtures for setup/teardown (avoid `setUp()`/`tearDown()`)
2. Parametrize tests instead of writing multiple similar tests
3. Mock external dependencies (APIs, databases, file I/O)
4. Use `autouse=True` for fixtures that should always run
5. Organize tests in `tests/` directory mirroring source structure

**Fixture Scopes:**
- `function` (default): New instance per test
- `class`: Shared within test class
- `module`: Shared within test file
- `session`: Shared across all tests

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Test Structure:**
```python
# tests/test_calculator.py
import pytest
from calculator import Calculator

def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)
```

**Fixtures:**
```python
@pytest.fixture
def calculator():
    """Provides Calculator instance for tests."""
    return Calculator()

@pytest.fixture
def sample_data():
    return {"users": [{"id": 1, "name": "Alice"}]}

def test_with_fixtures(calculator, sample_data):
    result = calculator.process(sample_data)
    assert result is not None
```

**Fixture Scopes and Cleanup:**
```python
@pytest.fixture(scope="module")
def database():
    """Database connection shared across module."""
    db = Database.connect("test.db")
    yield db  # Provide to tests
    db.close()  # Cleanup after all tests

@pytest.fixture(scope="session")
def api_client():
    """API client shared across all tests."""
    client = APIClient()
    client.login("test_user", "password")
    yield client
    client.logout()
```

**Parametrized Tests:**
```python
@pytest.mark.parametrize("x,y,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(calculator, x, y, expected):
    assert calculator.add(x, y) == expected

@pytest.mark.parametrize("input_str,expected", [
    ("hello", "HELLO"),
    ("", ""),
    ("MiXeD", "MIXED"),
], ids=["lowercase", "empty", "mixed"])
def test_uppercase(input_str, expected):
    assert input_str.upper() == expected
```

**Mocking with pytest-mock:**
```python
def test_api_call(mocker):
    # Mock external API call
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {"status": "ok"}
    mock_get.return_value.status_code = 200

    result = fetch_user_data(user_id=1)

    assert result["status"] == "ok"
    mock_get.assert_called_once_with("https://api.example.com/users/1")

def test_file_operations(mocker, tmp_path):
    # Mock file system
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="test"))

    content = read_config_file("config.yaml")

    assert content == "test"
    mock_open.assert_called_once()
```

**conftest.py for Shared Fixtures:**
```python
# tests/conftest.py
import pytest
from myapp import create_app, db

@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture(scope="function")
def db_session(app):
    """Create clean database for each test."""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for HTTP requests."""
    return app.test_client()
```

**Markers for Test Organization:**
```python
import pytest

@pytest.mark.slow
def test_long_running_operation():
    # Takes several seconds
    pass

@pytest.mark.integration
def test_database_integration(db_session):
    pass

@pytest.mark.unit
def test_pure_function():
    pass

# Run specific markers:
# pytest -m "not slow"  # Skip slow tests
# pytest -m integration  # Run only integration tests
```

**Fixtures with Parameters:**
```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    """Runs tests with multiple database types."""
    return request.param

def test_database_operations(database_type):
    db = connect_database(database_type)
    assert db.query("SELECT 1") is not None
```

**Async Test Support (pytest-asyncio):**
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

@pytest.fixture
async def async_client():
    client = AsyncAPIClient()
    await client.connect()
    yield client
    await client.disconnect()
```

**Testing Exceptions and Warnings:**
```python
def test_exception_message():
    with pytest.raises(ValueError, match="invalid input"):
        process_data("bad_data")

def test_warning_raised():
    with pytest.warns(DeprecationWarning):
        legacy_function()
```

**Pytest Configuration (pytest.ini):**
```ini
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers --cov=myapp --cov-report=html"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

**Anti-Patterns to Avoid:**
```python
# ✗ Don't use global state
global_db = Database()  # Bad!

# ✓ Use fixtures
@pytest.fixture
def db():
    return Database()

# ✗ Don't write brittle assertions
assert result == {"id": 1, "name": "Alice", "created_at": "2024-01-01"}  # Fails if timestamp changes

# ✓ Assert what matters
assert result["id"] == 1
assert result["name"] == "Alice"
assert "created_at" in result
```
