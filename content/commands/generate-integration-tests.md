---
id: cco-generate-integration-tests
description: Generate integration tests for service interactions
category: testing
priority: normal
---

# Generate Integration Tests

Generate integration tests for service interactions in **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Create comprehensive integration tests:
1. Identify service boundaries and interactions
2. Generate API endpoint tests
3. Create database integration tests
4. Test external service integrations
5. Verify end-to-end workflows

**Output:** Complete integration test suite covering critical paths.

---

## Architecture & Model Selection

**Data Gathering**: Sonnet (requires understanding)
- Map service architecture
- Identify integration points
- Extract API contracts

**Test Generation**: Sonnet (complex scenarios)
- Generate realistic test scenarios
- Create test data
- Handle async operations

**Execution Pattern**:
1. Analyze service architecture
2. Identify integration points
3. Generate test scenarios
4. Create test implementations
5. Validate tests run successfully

---

## When to Use

**Use this command:**
- Microservices architecture
- API-heavy applications
- Before major releases
- When adding new services
- Integration test coverage is low

---

## Phase 1: Analyze Service Architecture

Map services and their interactions:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import ast
import re
from collections import defaultdict

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Service Architecture Analysis ===\n")
print(f"Project: {project_name}\n")

# Identify services
services = []
service_dirs = [
    'services',
    'apps',
    'api',
    'microservices'
]

for service_dir_name in service_dirs:
    service_path = project_root / service_dir_name
    if service_path.exists():
        for item in service_path.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                services.append({
                    'name': item.name,
                    'path': str(item.relative_to(project_root)),
                    'type': 'microservice' if service_dir_name == 'microservices' else 'service'
                })

print(f"Services Found: {len(services)}")
for svc in services:
    print(f"  - {svc['name']} ({svc['path']})")
print()

# Identify API endpoints
api_endpoints = []

def extract_routes_fastapi(file_path):
    """Extract FastAPI routes"""
    routes = []
    try:
        content = file_path.read_text()
        # Match: @app.get("/path"), @router.post("/path")
        patterns = [
            r'@(?:app|router)\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for method, path in matches:
                routes.append({
                    'method': method.upper(),
                    'path': path,
                    'file': str(file_path.relative_to(project_root))
                })
    except:
        pass
    return routes

def extract_routes_flask(file_path):
    """Extract Flask routes"""
    routes = []
    try:
        content = file_path.read_text()
        # Match: @app.route("/path", methods=["GET"])
        pattern = r'@(?:app|bp)\.route\(["\']([^"\']+)["\'].*?methods\s*=\s*\[([^\]]+)\]'
        matches = re.findall(pattern, content)
        for path, methods in matches:
            method_list = [m.strip().strip('"\'') for m in methods.split(',')]
            for method in method_list:
                routes.append({
                    'method': method.upper(),
                    'path': path,
                    'file': str(file_path.relative_to(project_root))
                })
    except:
        pass
    return routes

# Scan for API endpoints
python_files = list(project_root.rglob('*.py'))
python_files = [f for f in python_files if not any(ex in str(f) for ex in ['venv', '__pycache__', 'test'])]

for py_file in python_files:
    api_endpoints.extend(extract_routes_fastapi(py_file))
    api_endpoints.extend(extract_routes_flask(py_file))

print(f"API Endpoints Found: {len(api_endpoints)}")

# Group by HTTP method
by_method = defaultdict(int)
for endpoint in api_endpoints:
    by_method[endpoint['method']] += 1

for method, count in sorted(by_method.items()):
    print(f"  {method}: {count}")
print()
```

---

## Phase 2: Identify Integration Points

Find cross-service dependencies:

```python
print(f"=== Integration Point Detection ===\n")

integration_points = []

# 1. HTTP Client calls
for py_file in python_files[:100]:
    try:
        content = py_file.read_text()

        # requests library
        if 'requests.' in content:
            http_calls = re.findall(r'requests\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', content)
            for method, url in http_calls:
                integration_points.append({
                    'type': 'HTTP_CLIENT',
                    'method': method.upper(),
                    'target': url,
                    'source_file': str(py_file.relative_to(project_root))
                })

        # httpx library
        if 'httpx.' in content or 'AsyncClient' in content:
            http_calls = re.findall(r'(?:client\.|httpx\.)(get|post|put|delete|patch)\(["\']([^"\']+)["\']', content)
            for method, url in http_calls:
                integration_points.append({
                    'type': 'HTTP_CLIENT_ASYNC',
                    'method': method.upper(),
                    'target': url,
                    'source_file': str(py_file.relative_to(project_root))
                })

    except:
        pass

# 2. Database connections
db_integration = []

for py_file in python_files[:100]:
    try:
        content = py_file.read_text()

        # SQLAlchemy
        if 'create_engine' in content or 'sessionmaker' in content:
            db_integration.append({
                'type': 'DATABASE',
                'technology': 'SQLAlchemy',
                'file': str(py_file.relative_to(project_root))
            })

        # MongoDB
        if 'MongoClient' in content or 'pymongo' in content:
            db_integration.append({
                'type': 'DATABASE',
                'technology': 'MongoDB',
                'file': str(py_file.relative_to(project_root))
            })

        # Redis
        if 'redis.Redis' in content or 'aioredis' in content:
            db_integration.append({
                'type': 'CACHE',
                'technology': 'Redis',
                'file': str(py_file.relative_to(project_root))
            })

    except:
        pass

print(f"HTTP Integration Points: {len([i for i in integration_points if 'HTTP' in i['type']])}")
print(f"Database Integrations: {len(db_integration)}")
print()

# Show sample integration points
if integration_points:
    print("Sample HTTP Integrations:")
    for i, ip in enumerate(integration_points[:5], 1):
        print(f"{i}. {ip['method']} {ip['target']}")
        print(f"   From: {ip['source_file']}")
    print()

if db_integration:
    print("Database Technologies:")
    tech_counts = defaultdict(int)
    for db in db_integration:
        tech_counts[db['technology']] += 1

    for tech, count in tech_counts.items():
        print(f"  - {tech}: {count} files")
    print()
```

---

## Phase 3: Generate API Integration Tests

Create endpoint tests:

```python
print(f"=== API Integration Test Generation ===\n")

def generate_api_test(endpoint):
    """Generate integration test for API endpoint"""

    method = endpoint['method']
    path = endpoint['path']
    test_name = f"test_{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '').strip('_')}"

    # Determine test type based on method
    if method == 'GET':
        test_code = f'''
def {test_name}(client):
    """Test GET {path}"""
    # Arrange
    # Set up test data if needed

    # Act
    response = client.get("{path}")

    # Assert
    assert response.status_code == 200
    assert response.json() is not None
'''

    elif method == 'POST':
        test_code = f'''
def {test_name}(client):
    """Test POST {path}"""
    # Arrange
    test_data = {{
        # TODO: Add request body
    }}

    # Act
    response = client.post("{path}", json=test_data)

    # Assert
    assert response.status_code in [200, 201]
    assert "id" in response.json()  # Assuming ID is returned
'''

    elif method == 'PUT':
        test_code = f'''
def {test_name}(client):
    """Test PUT {path}"""
    # Arrange
    test_data = {{
        # TODO: Add request body
    }}

    # Act
    response = client.put("{path}", json=test_data)

    # Assert
    assert response.status_code == 200
'''

    elif method == 'DELETE':
        test_code = f'''
def {test_name}(client):
    """Test DELETE {path}"""
    # Act
    response = client.delete("{path}")

    # Assert
    assert response.status_code in [200, 204]
'''

    else:
        test_code = f'''
def {test_name}(client):
    """Test {method} {path}"""
    # TODO: Implement test
    pass
'''

    return test_name, test_code.strip()

# Generate tests for all endpoints
api_tests = []

for endpoint in api_endpoints[:20]:  # Limit for demo
    test_name, test_code = generate_api_test(endpoint)
    api_tests.append({
        'name': test_name,
        'code': test_code,
        'endpoint': endpoint
    })

print(f"Generated API Tests: {len(api_tests)}")
print()

# Create test file
api_test_content = '''"""
API Integration Tests
Auto-generated
"""

import pytest
from fastapi.testclient import TestClient
# from your_app import app  # TODO: Import your app

@pytest.fixture
def client():
    """Test client fixture"""
    # client = TestClient(app)  # TODO: Create test client
    # return client
    pass

'''

# Add all tests
for test in api_tests[:10]:  # Sample
    api_test_content += '\n' + test['code'] + '\n'

print("Sample API Test File:")
print(api_test_content[:500] + "...")
print()
```

---

## Phase 4: Generate Database Integration Tests

Create DB tests:

```python
print(f"=== Database Integration Test Generation ===\n")

db_test_content = '''"""
Database Integration Tests
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session():
    """Create test database session"""
    # Create test database
    engine = create_engine("sqlite:///:memory:")  # In-memory DB for tests

    # Create tables
    # Base.metadata.create_all(engine)  # TODO: Import your models

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Cleanup
    session.close()

def test_create_user(db_session):
    """Test creating a user in database"""
    # Arrange
    user_data = {
        "username": "test_user",
        "email": "test@example.com"
    }

    # Act
    # user = User(**user_data)  # TODO: Use your model
    # db_session.add(user)
    # db_session.commit()

    # Assert
    # assert user.id is not None
    # assert user.username == "test_user"
    pass

def test_read_user(db_session):
    """Test reading user from database"""
    # Arrange: Create test user first
    # user = User(username="test", email="test@example.com")
    # db_session.add(user)
    # db_session.commit()

    # Act
    # found_user = db_session.query(User).filter_by(username="test").first()

    # Assert
    # assert found_user is not None
    # assert found_user.username == "test"
    pass

def test_update_user(db_session):
    """Test updating user in database"""
    # Arrange
    # user = User(username="test", email="old@example.com")
    # db_session.add(user)
    # db_session.commit()

    # Act
    # user.email = "new@example.com"
    # db_session.commit()

    # Assert
    # updated_user = db_session.query(User).filter_by(username="test").first()
    # assert updated_user.email == "new@example.com"
    pass

def test_delete_user(db_session):
    """Test deleting user from database"""
    # Arrange
    # user = User(username="test", email="test@example.com")
    # db_session.add(user)
    # db_session.commit()

    # Act
    # db_session.delete(user)
    # db_session.commit()

    # Assert
    # found_user = db_session.query(User).filter_by(username="test").first()
    # assert found_user is None
    pass

def test_transaction_rollback(db_session):
    """Test database transaction rollback"""
    # Arrange
    # user = User(username="test", email="test@example.com")
    # db_session.add(user)

    # Act
    db_session.rollback()

    # Assert
    # found_user = db_session.query(User).filter_by(username="test").first()
    # assert found_user is None
    pass
'''

print("Generated Database Integration Tests")
print()
```

---

## Phase 5: Generate End-to-End Tests

Create workflow tests:

```python
print(f"=== End-to-End Test Generation ===\n")

e2e_test_content = '''"""
End-to-End Integration Tests
Test complete workflows across services
"""

import pytest

class TestUserWorkflow:
    """Test complete user registration and login workflow"""

    def test_user_registration_to_login(self, client):
        """Test user can register and then login"""
        # Step 1: Register new user
        register_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "SecurePass123!"
        }

        register_response = client.post("/api/auth/register", json=register_data)
        assert register_response.status_code == 201
        user_id = register_response.json()["id"]

        # Step 2: Login with credentials
        login_data = {
            "username": "newuser",
            "password": "SecurePass123!"
        }

        login_response = client.post("/api/auth/login", json=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Step 3: Access protected resource with token
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = client.get(f"/api/users/{user_id}", headers=headers)
        assert profile_response.status_code == 200
        assert profile_response.json()["username"] == "newuser"

class TestOrderWorkflow:
    """Test complete order creation and processing workflow"""

    def test_create_and_process_order(self, client, auth_token):
        """Test order from creation to completion"""
        # Step 1: Create order
        order_data = {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 1}
            ]
        }

        create_response = client.post(
            "/api/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert create_response.status_code == 201
        order_id = create_response.json()["id"]
        assert create_response.json()["status"] == "pending"

        # Step 2: Process payment
        payment_data = {
            "order_id": order_id,
            "method": "credit_card",
            "amount": 150.00
        }

        payment_response = client.post("/api/payments", json=payment_data)
        assert payment_response.status_code == 200

        # Step 3: Verify order status updated
        order_response = client.get(f"/api/orders/{order_id}")
        assert order_response.status_code == 200
        assert order_response.json()["status"] == "paid"

        # Step 4: Ship order
        ship_response = client.post(f"/api/orders/{order_id}/ship")
        assert ship_response.status_code == 200

        # Step 5: Verify final status
        final_response = client.get(f"/api/orders/{order_id}")
        assert final_response.json()["status"] == "shipped"

class TestServiceIntegration:
    """Test integration between microservices"""

    def test_user_service_to_order_service(self, client):
        """Test data flow from user service to order service"""
        # This tests that services can communicate
        # and share data correctly

        # Get user from user service
        user_response = client.get("/api/users/1")
        assert user_response.status_code == 200
        user_data = user_response.json()

        # Create order in order service (references user)
        order_data = {
            "user_id": user_data["id"],
            "items": [{"product_id": 1, "quantity": 1}]
        }

        order_response = client.post("/api/orders", json=order_data)
        assert order_response.status_code == 201

        # Verify order references correct user
        order = order_response.json()
        assert order["user_id"] == user_data["id"]
'''

print("Generated End-to-End Tests:")
print("  - User registration → login workflow")
print("  - Order creation → processing workflow")
print("  - Cross-service integration")
print()
```

---

## Phase 6: Generate Test Fixtures

Create reusable test data:

```python
print(f"=== Integration Test Fixtures ===\n")

fixtures_content = '''"""
Integration test fixtures
"""

import pytest
from typing import Generator

@pytest.fixture(scope="session")
def test_database():
    """Set up test database for entire test session"""
    # Create test database
    # Run migrations
    # Seed with test data

    yield

    # Teardown: Drop test database

@pytest.fixture(scope="function")
def clean_database(test_database):
    """Clean database before each test"""
    # Truncate all tables

    yield

    # Cleanup after test

@pytest.fixture
def test_user(db_session):
    """Create test user"""
    user = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "is_active": True
    }

    # db_session.add(User(**user))
    # db_session.commit()

    return user

@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token for test user"""
    response = client.post("/api/auth/login", json={
        "username": test_user["username"],
        "password": "testpass123"
    })

    return response.json()["access_token"]

@pytest.fixture
def mock_external_api(monkeypatch):
    """Mock external API calls"""
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(*args, **kwargs):
        return MockResponse({"status": "success"})

    # monkeypatch.setattr(requests, "get", mock_get)

    return mock_get

@pytest.fixture
def test_products(db_session):
    """Create test products"""
    products = [
        {"id": 1, "name": "Product 1", "price": 50.00},
        {"id": 2, "name": "Product 2", "price": 75.00},
        {"id": 3, "name": "Product 3", "price": 100.00}
    ]

    # for product_data in products:
    #     product = Product(**product_data)
    #     db_session.add(product)
    # db_session.commit()

    return products
'''

print("Generated Fixtures:")
print("  - test_database: Session-scoped DB")
print("  - clean_database: Per-test cleanup")
print("  - test_user: Sample user")
print("  - auth_token: Authentication token")
print("  - mock_external_api: External API mock")
print("  - test_products: Sample products")
print()
```

---

## Phase 7: Generate Test Utilities

Helper functions:

```python
print(f"=== Test Utilities ===\n")

utils_content = '''"""
Integration test utilities
"""

import time
from typing import Callable, Any

def wait_for_condition(
    condition: Callable[[], bool],
    timeout: int = 10,
    interval: float = 0.5,
    error_message: str = "Condition not met"
) -> None:
    """Wait for a condition to become true"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        if condition():
            return

        time.sleep(interval)

    raise TimeoutError(error_message)

def assert_eventually(
    condition: Callable[[], bool],
    timeout: int = 5,
    message: str = "Condition not met in time"
) -> None:
    """Assert that a condition becomes true eventually"""
    wait_for_condition(condition, timeout, error_message=message)

def create_test_data(db_session, model, count: int = 10, **kwargs):
    """Create multiple test records"""
    records = []

    for i in range(count):
        data = {**kwargs, "id": i + 1}
        # record = model(**data)
        # db_session.add(record)
        # records.append(record)

    # db_session.commit()

    return records

def assert_response_schema(response_json: dict, expected_keys: list):
    """Assert response has expected structure"""
    for key in expected_keys:
        assert key in response_json, f"Missing key: {key}"

def assert_status_code(response, expected_code: int):
    """Assert response status code with helpful message"""
    assert response.status_code == expected_code, \
        f"Expected {expected_code}, got {response.status_code}. Response: {response.text}"
'''

print("Generated Utilities:")
print("  - wait_for_condition: Async waiting")
print("  - assert_eventually: Eventually consistent checks")
print("  - create_test_data: Bulk data creation")
print("  - assert_response_schema: Response validation")
print()
```

---

## Phase 8: Summary

```python
print(f"=== Generation Summary ===\n")

summary = {
    'services': len(services),
    'api_endpoints': len(api_endpoints),
    'integration_points': len(integration_points),
    'generated_tests': len(api_tests),
}

print(f"Architecture:")
print(f"  Services: {summary['services']}")
print(f"  API Endpoints: {summary['api_endpoints']}")
print(f"  Integration Points: {summary['integration_points']}")
print()

print(f"Generated Integration Tests:")
print(f"  API Tests: {summary['generated_tests']}")
print(f"  DB Tests: Complete CRUD suite")
print(f"  E2E Tests: 3 workflows")
print(f"  Fixtures: 6 reusable fixtures")
print(f"  Utilities: 5 helper functions")
print()

print("Files Created:")
print("  - tests/integration/test_api.py")
print("  - tests/integration/test_database.py")
print("  - tests/integration/test_e2e.py")
print("  - tests/integration/conftest.py")
print("  - tests/integration/utils.py")
print()

print("Next Steps:")
print("  1. Review generated tests")
print("  2. Add real test data")
print("  3. Configure test database")
print("  4. Run: pytest tests/integration/ -v")
print()
```

---

## Output Example

```
=== Service Architecture Analysis ===

Project: backend

Services Found: 3
  - auth (services/auth)
  - orders (services/orders)
  - payments (services/payments)

API Endpoints Found: 34
  GET: 18
  POST: 10
  PUT: 4
  DELETE: 2

=== Integration Point Detection ===

HTTP Integration Points: 12
Database Integrations: 8

Sample HTTP Integrations:
1. POST http://payment-service/api/process
   From: services/orders/payment.py
2. GET http://user-service/api/users/{id}
   From: services/orders/orders.py

Database Technologies:
  - SQLAlchemy: 5 files
  - Redis: 3 files

=== API Integration Test Generation ===

Generated API Tests: 34

=== End-to-End Test Generation ===

Generated End-to-End Tests:
  - User registration → login workflow
  - Order creation → processing workflow
  - Cross-service integration

=== Generation Summary ===

Architecture:
  Services: 3
  API Endpoints: 34
  Integration Points: 12

Generated Integration Tests:
  API Tests: 34
  DB Tests: Complete CRUD suite
  E2E Tests: 3 workflows
  Fixtures: 6 reusable fixtures
  Utilities: 5 helper functions

Files Created:
  - tests/integration/test_api.py
  - tests/integration/test_database.py
  - tests/integration/test_e2e.py
  - tests/integration/conftest.py
  - tests/integration/utils.py

Next Steps:
  1. Review generated tests
  2. Add real test data
  3. Configure test database
  4. Run: pytest tests/integration/ -v
```

---

**Integration Testing Philosophy:** Unit tests prove components work. Integration tests prove the system works. Both are essential.
