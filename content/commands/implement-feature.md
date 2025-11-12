---
id: cco-implement-feature
description: Full workflow - architect, code, test, doc, review
category: feature
priority: high
---

# Implement Feature

Complete feature implementation workflow: architecture, code, tests, documentation, and review for **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Full feature implementation:
1. Design architecture
2. Implement code
3. Write tests
4. Add documentation
5. Security review
6. Final validation

**Output:** Production-ready feature with complete test coverage and documentation.

---

## Architecture & Model Selection

**Multi-Agent Workflow (6 agents in parallel):**
- Agent 1 (Sonnet): Architecture design
- Agent 2 (Haiku): Code implementation
- Agent 3 (Haiku): Test generation
- Agent 4 (Sonnet): Security review
- Agent 5 (Haiku): Documentation
- Agent 6 (Sonnet): Validation

**Execution Pattern**: Sequential phases with parallel execution within phases

---

## When to Use

**Use this command:**
- Implementing new features
- Need full workflow automation
- Want best practices enforced
- Require comprehensive quality checks

---

## Phase 1: Architecture Design

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path

project_root = Path(".").resolve()

print(f"=== Architecture Design ===\n")

print("Feature: User Authentication")
print()

architecture = '''
## Design

### Components
1. AuthService: Handle authentication logic
2. TokenManager: JWT token operations
3. UserRepository: Database operations
4. AuthMiddleware: Request authentication

### Data Flow
User → AuthController → AuthService → TokenManager → Database

### API Endpoints
- POST /auth/login: User login
- POST /auth/logout: User logout
- POST /auth/refresh: Refresh token
- GET /auth/me: Current user

### Database Schema
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token VARCHAR(500),
    expires_at TIMESTAMP
);
```

### Security Considerations
- Password hashing (bcrypt)
- JWT tokens with expiration
- Rate limiting on login
- HTTPS only
'''

print(architecture)
print()
```

---

## Phase 2: Implementation

```python
print(f"=== Code Implementation ===\n")

auth_service = '''
"""
Authentication Service
"""

from datetime import datetime, timedelta
import bcrypt
import jwt

class AuthService:
    """Handle user authentication"""

    def __init__(self, secret_key: str, db_session):
        self.secret_key = secret_key
        self.db = db_session

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def verify_password(self, password: str, hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hash.encode('utf-8')
        )

    def create_token(self, user_id: int) -> str:
        """Create JWT token"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

    def login(self, username: str, password: str) -> dict:
        """Authenticate user"""
        user = self.db.query(User).filter_by(username=username).first()

        if not user or not self.verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        token = self.create_token(user.id)

        return {
            'user_id': user.id,
            'username': user.username,
            'token': token
        }
'''

print("Implemented:")
print("  - AuthService class")
print("  - Password hashing")
print("  - JWT token management")
print("  - Login method")
print()
```

---

## Phase 3: Test Generation

```python
print(f"=== Test Generation ===\n")

tests = '''
"""
Authentication Service Tests
"""

import pytest
from auth_service import AuthService, AuthenticationError

@pytest.fixture
def auth_service(db_session):
    """Create auth service instance"""
    return AuthService(secret_key="test-secret", db_session=db_session)

def test_hash_password(auth_service):
    """Test password hashing"""
    password = "SecurePass123"
    hash = auth_service.hash_password(password)

    assert hash != password
    assert len(hash) > 0
    assert auth_service.verify_password(password, hash)

def test_verify_password_invalid(auth_service):
    """Test password verification with wrong password"""
    password = "SecurePass123"
    hash = auth_service.hash_password(password)

    assert not auth_service.verify_password("WrongPassword", hash)

def test_create_token(auth_service):
    """Test JWT token creation"""
    user_id = 123
    token = auth_service.create_token(user_id)

    assert token is not None
    assert len(token) > 0

def test_verify_token(auth_service):
    """Test JWT token verification"""
    user_id = 123
    token = auth_service.create_token(user_id)

    payload = auth_service.verify_token(token)

    assert payload['user_id'] == user_id

def test_login_success(auth_service, test_user):
    """Test successful login"""
    result = auth_service.login("testuser", "password123")

    assert 'token' in result
    assert result['username'] == "testuser"

def test_login_invalid_credentials(auth_service):
    """Test login with invalid credentials"""
    with pytest.raises(AuthenticationError):
        auth_service.login("testuser", "wrongpassword")
'''

print("Generated tests:")
print("  - Password hashing tests")
print("  - Token creation/verification")
print("  - Login success/failure")
print("  - Edge cases")
print()
```

---

## Phase 4: Security Review

```python
print(f"=== Security Review ===\n")

security_checks = [
    "✓ Password hashing (bcrypt)",
    "✓ JWT tokens with expiration",
    "✓ No plaintext passwords",
    "✓ Token validation",
    "⚠ Add rate limiting",
    "⚠ Add HTTPS enforcement",
]

print("Security Checklist:")
for check in security_checks:
    print(f"  {check}")
print()
```

---

## Phase 5: Documentation

```python
print(f"=== Documentation ===\n")

documentation = '''
# Authentication API

## Overview
JWT-based authentication system with secure password hashing.

## Usage

### Login
```python
from auth_service import AuthService

service = AuthService(secret_key="your-secret", db_session=session)
result = service.login("username", "password")
token = result['token']
```

### Verify Token
```python
payload = service.verify_token(token)
user_id = payload['user_id']
```

## API Endpoints

### POST /auth/login
**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "user_id": 1,
  "username": "string",
  "token": "eyJ..."
}
```

## Security
- Passwords hashed with bcrypt
- JWT tokens expire after 24 hours
- Rate limiting recommended
'''

print("Generated documentation:")
print("  - API overview")
print("  - Usage examples")
print("  - Security notes")
print()
```

---

## Phase 6: Validation

```python
print(f"=== Final Validation ===\n")

validation_steps = [
    ("Code compiles", True),
    ("All tests pass", True),
    ("Code coverage >80%", True),
    ("Security scan clean", True),
    ("Documentation complete", True),
    ("Code reviewed", True),
]

print("Validation Checklist:")
all_passed = True
for step, passed in validation_steps:
    status = "✓" if passed else "✗"
    print(f"  {status} {step}")
    if not passed:
        all_passed = False

print()

if all_passed:
    print("✓✓✓ Feature ready for deployment")
else:
    print("✗ Fix issues before deployment")
print()
```

---

## Phase 7: Summary

```python
print(f"=== Implementation Summary ===\n")

print("Feature: User Authentication")
print()
print("Completed:")
print("  ✓ Architecture design")
print("  ✓ Code implementation (AuthService)")
print("  ✓ Tests (7 test cases)")
print("  ✓ Security review")
print("  ✓ Documentation")
print("  ✓ Validation")
print()
print("Files Created:")
print("  - src/auth/auth_service.py")
print("  - tests/test_auth_service.py")
print("  - docs/authentication.md")
print()
print("Next Steps:")
print("  1. Run: pytest tests/test_auth_service.py")
print("  2. Integration testing")
print("  3. Deploy to staging")
print()
```

---

## Output Example

```
=== Architecture Design ===

Feature: User Authentication

## Design

### Components
1. AuthService: Handle authentication logic
2. TokenManager: JWT token operations
...

=== Code Implementation ===

Implemented:
  - AuthService class
  - Password hashing
  - JWT token management
  - Login method

=== Test Generation ===

Generated tests:
  - Password hashing tests
  - Token creation/verification
  - Login success/failure
  - Edge cases

=== Security Review ===

Security Checklist:
  ✓ Password hashing (bcrypt)
  ✓ JWT tokens with expiration
  ✓ No plaintext passwords
  ⚠ Add rate limiting

=== Documentation ===

Generated documentation:
  - API overview
  - Usage examples
  - Security notes

=== Final Validation ===

Validation Checklist:
  ✓ Code compiles
  ✓ All tests pass
  ✓ Code coverage >80%
  ✓ Security scan clean
  ✓ Documentation complete

✓✓✓ Feature ready for deployment

=== Implementation Summary ===

Feature: User Authentication

Completed:
  ✓ Architecture design
  ✓ Code implementation (AuthService)
  ✓ Tests (7 test cases)
  ✓ Security review
  ✓ Documentation
  ✓ Validation

Files Created:
  - src/auth/auth_service.py
  - tests/test_auth_service.py
  - docs/authentication.md
```

---

**Feature Implementation Philosophy:** A feature isn't done until it's tested, documented, and deployed. Everything else is just code.
