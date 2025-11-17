# cco-implement

**AI-assisted feature implementation with TDD approach and skill auto-selection.**

---

## Purpose

Implement new features using Test-Driven Development (TDD), automatically selecting appropriate skills based on feature type.

---

## Execution Protocol

### Step 1: Analyze Feature Request

User provides feature description:
```
/cco-implement "Add user authentication with JWT"
```

Analyze to determine:
- Feature type (API, frontend, database, etc.)
- Complexity (simple, medium, complex)
- Required skills
- Security considerations
- Testing needs

### Step 2: Select Skills

Auto-select skills based on feature:
```markdown
Analyzing feature: "Add user authentication with JWT"

Feature type: Security-critical API feature
Complexity: Medium

Skills I'll use:
- cco-skill-security-owasp-xss-sqli-csrf (auth/security)
- cco-skill-api-rest-versioning-security (API design)
- cco-skill-test-pyramid-coverage-isolation (testing)
- cco-skill-database-optimization-caching-profiling (user storage)
```

### Step 3: Create Implementation Plan

```markdown
Implementation Plan (TDD Approach):

Phase 1: Architecture Design (2 min)
- Design authentication flow
  * POST /auth/login → access_token + refresh_token
  * POST /auth/refresh → new access_token
  * POST /auth/logout → invalidate refresh_token
- Define JWT payload structure
- Plan database schema (users, refresh_tokens tables)

Phase 2: Tests First (5 min) - TDD
- Unit tests for JWT creation/validation
- Integration tests for auth endpoints
- Security tests (token expiry, tampering)
- Edge cases (expired tokens, invalid credentials)

Phase 3: Implementation (10 min)
- User model + password hashing (bcrypt)
- JWT token generation/validation
- Auth endpoints (login, refresh, logout)
- Middleware for protected routes

Phase 4: Security Hardening (3 min)
- Rate limiting on auth endpoints (5 attempts/5min)
- Brute force protection
- Secure password requirements (min 8 chars)
- Token refresh mechanism

Phase 5: Documentation (2 min)
- API documentation (OpenAPI)
- Security best practices
- Example usage

Estimated time: 22 minutes
Tests created: 25+ tests (100% coverage target)

Start implementation? (yes/no)
```

### Step 4: Execute TDD Implementation

**Use TodoWrite** to track phases

**Launch Task** for each phase:

```python
# Phase 1: Architecture
Task({
  model: "sonnet",
  prompt: "Design JWT authentication architecture..."
})

# Phase 2: Tests (TDD - Write tests first)
Task({
  model: "sonnet",
  prompt: """
  Write tests FIRST (TDD approach):

  Use cco-skill-test-pyramid-coverage-isolation

  1. Unit tests for JWT operations:
     - test_create_access_token()
     - test_create_refresh_token()
     - test_validate_token_success()
     - test_validate_token_expired()
     - test_validate_token_tampered()

  2. Integration tests for auth endpoints:
     - test_login_success()
     - test_login_invalid_credentials()
     - test_refresh_token_success()
     - test_refresh_token_invalid()
     - test_logout_success()

  3. Security tests:
     - test_rate_limiting()
     - test_brute_force_protection()
     - test_weak_password_rejected()

  Create failing tests first (TDD red phase).
  """
})

# Phase 3: Implementation (Make tests pass)
Task({
  model: "sonnet",
  prompt: """
  Implement JWT authentication to make tests pass (TDD green phase):

  Use skills:
  - cco-skill-security-owasp-xss-sqli-csrf
  - cco-skill-api-rest-versioning-security

  1. models/user.py:
     - User model (id, email, password_hash)
     - Password hashing with bcrypt (cost factor: 12)
     - Password validation (min 8 chars, complexity)

  2. services/auth.py:
     - create_access_token(user_id) → JWT (15min expiry)
     - create_refresh_token(user_id) → JWT (7 days expiry)
     - validate_token(token) → user_id or None
     - hash_password(password) → hash
     - verify_password(password, hash) → bool

  3. api/auth.py:
     - POST /auth/login
     - POST /auth/refresh
     - POST /auth/logout

  4. middleware/auth.py:
     - JWT validation middleware
     - Protect routes with @require_auth decorator

  Run tests after each component to ensure TDD cycle.
  """
})

# Phase 4-5: Security & Documentation
# ... similar Task calls
```

### Step 5: Report Progress and Results

```markdown
Phase 1 Complete: Architecture Designed ✓

Auth Flow:
- POST /auth/login → access_token (15min) + refresh_token (7days)
- POST /auth/refresh → new access_token
- POST /auth/logout → invalidate refresh_token

Database Schema:
- users: id, email, password_hash, created_at
- refresh_tokens: id, user_id, token_hash, expires_at

Continue to Phase 2 (Tests)? (yes/no)

---

Phase 2 Complete: Tests Created ✓ (TDD Red Phase)

Created 25 failing tests:
✓ tests/unit/test_auth.py (12 unit tests)
✓ tests/integration/test_auth_api.py (8 integration tests)
✓ tests/security/test_auth_security.py (5 security tests)

Test results: 25 failed (expected - TDD red phase)

Continue to Phase 3 (Implementation)? (yes/no)

---

Phase 3 Complete: Implementation Done ✓ (TDD Green Phase)

Created:
✓ models/user.py (User model + password hashing)
✓ services/auth.py (JWT operations)
✓ api/auth.py (3 endpoints)
✓ middleware/auth.py (JWT validation)

Test results: 25 passed, 0 failed ✓ (TDD green phase)
Coverage: 100% ✓

Continue to Phase 4 (Security)? (yes/no)

---

All Phases Complete! ✓

Implementation Summary:

Created:
✓ models/user.py (User model + password hashing)
✓ services/auth.py (JWT token operations)
✓ api/auth.py (3 auth endpoints)
✓ middleware/auth.py (JWT validation)
✓ tests/ (25 tests, 100% coverage)
✓ openapi.yaml (updated with auth docs)

Security Features:
✓ Bcrypt password hashing (cost factor: 12)
✓ Rate limiting (5 attempts/5min)
✓ JWT with HS256 (secret from env)
✓ Token expiry (access: 15min, refresh: 7days)
✓ Secure token storage (HTTP-only cookies)
✓ Password requirements (min 8 chars, complexity)

Tests: 25 passed, 0 failed (100% coverage)

Impact:
- Addresses Pain #1 (51% security concern)
- Addresses Pain #4 (TDD = tests first, no bugs)
- Feature complete and production-ready ✓

Next Steps:
1. Run full test suite: pytest tests/
2. Test manually: http://localhost:8000/auth/login
3. Review security: /cco-audit --security
4. Commit: /cco-commit
```

---

## TDD Cycle

1. **Red:** Write failing tests first
2. **Green:** Write minimal code to pass tests
3. **Refactor:** Improve code while keeping tests green

Always follow this cycle for quality and confidence.

---

## Skills Auto-Selection

Based on feature keywords:
- "authentication", "auth", "login" → security skills
- "API", "endpoint", "REST" → API skills
- "database", "query", "schema" → database skills
- "frontend", "UI", "component" → frontend skills
- "deploy", "CI/CD", "pipeline" → deployment skills
- "test", "coverage" → testing skills

Multiple skills used when feature spans domains.

---

## Agents Used

- `cco-agent-generate` - Scaffolding and tests
- `cco-agent-fix` - Implementation

Both use Sonnet for accuracy.

---

## Success Criteria

- [OK] Feature analyzed and understood
- [OK] Appropriate skills auto-selected
- [OK] Implementation plan created
- [OK] TDD approach followed (tests first)
- [OK] All tests pass with 100% coverage
- [OK] Security hardened
- [OK] Documentation created
- [OK] Pain-point impact communicated
- [OK] Production-ready code

---

## Example Usage

```bash
# Implement new feature
/cco-implement "Add user authentication with JWT"

# Implement with specific guidance
/cco-implement "Add caching layer using Redis"

# Complex feature
/cco-implement "Add real-time notifications with WebSockets"
```
