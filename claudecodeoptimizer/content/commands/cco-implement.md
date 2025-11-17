# cco-implement

**AI-assisted feature implementation with TDD approach and skill auto-selection.**

---

## Purpose

Implement new features using Test-Driven Development (TDD), automatically selecting appropriate skills based on feature type.

---

## Execution Protocol

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# Implement Command

**What I do:**
I implement new features using Test-Driven Development (TDD), automatically selecting appropriate skills based on feature type.

**How it works:**
1. I analyze your feature request to determine complexity and required skills
2. I create a detailed implementation plan broken into 5 phases
3. You select which implementation steps to execute
4. I implement using TDD (write tests first, then make them pass)
5. I add security hardening and documentation

**What you'll get:**
- Complete feature implementation following TDD
- Architecture design for the feature
- Comprehensive tests (unit, integration, security) - 100% coverage goal
- Production-ready code with security hardening
- API documentation and usage examples

**Phases:**
1. Architecture Design (plan the feature structure)
2. Tests First - TDD Red Phase (write failing tests)
3. Implementation - TDD Green Phase (make tests pass)
4. Security Hardening (rate limiting, validation, etc.)
5. Documentation (OpenAPI, security best practices)

**Time estimate:** 10-30 minutes depending on feature complexity

**New code WILL be created** - complete feature implementation with tests.
```

**Then ask for confirmation using AskUserQuestion:**

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start implementing the feature?",
    header: "Start Implement",
    multiSelect: false,
    options: [
      {
        label: "Yes, start implementation",
        description: "Analyze feature and begin TDD implementation"
      },
      {
        label: "No, cancel",
        description: "Exit without implementing anything"
      }
    ]
  }]
})
```

**CRITICAL:**
- If user selects "No, cancel" → EXIT immediately, do NOT proceed
- If user selects "Yes, start implementation" → Continue to Step 1

---

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

### Step 3: Create Implementation Plan and Get User Confirmation

Present implementation plan:

```markdown
Implementation Plan (TDD Approach):

Feature: [feature description]
Complexity: [Simple/Medium/Complex]
Skills: [list skills]

Phases:
1. Architecture Design (X min)
   - [design decisions]

2. Tests First (X min) - TDD Red Phase
   - [tests to create]

3. Implementation (X min) - TDD Green Phase
   - [components to implement]

4. Security Hardening (X min)
   - [security measures]

5. Documentation (X min)
   - [documentation to create]

Estimated time: XX minutes
Tests: XX+ tests (100% coverage target)
```

**IMPORTANT:** The descriptions below are EXAMPLES based on JWT auth feature. You MUST:
- Break down the ACTUAL feature into specific implementation steps
- List each concrete task with its phase in parentheses
- Provide realistic time estimates for each step
- Replace example steps with REAL feature-specific steps

**Use AskUserQuestion** to let user select implementation steps (NOT phases, but individual steps):

```python
AskUserQuestion({
  questions: [{
    question: "Which implementation steps should I execute? Select the specific tasks you want:",
    header: "Implement",
    multiSelect: true,
    options: [
      # Phase 1: Architecture Design - Break into concrete steps
      {
        label: "Design authentication flow",
        description: "(Phase 1: Architecture, 1 min) Design login/refresh/logout endpoints, token flow"
      },
      {
        label: "Define JWT payload structure",
        description: "(Phase 1: Architecture, 1 min) Define user_id, roles, expiry in JWT claims"
      },
      {
        label: "Plan database schema",
        description: "(Phase 1: Architecture, 1 min) Design users and refresh_tokens tables"
      },

      # Phase 2: Tests First (TDD Red Phase) - Break into concrete test files
      {
        label: "Write unit tests for JWT operations",
        description: "(Phase 2: Tests, 2 min) test_create_token, test_validate_token, test_token_expiry, test_token_tampered | 🔴 TDD Red Phase"
      },
      {
        label: "Write integration tests for auth endpoints",
        description: "(Phase 2: Tests, 2 min) test_login_success, test_login_invalid, test_refresh, test_logout | 🔴 TDD Red Phase"
      },
      {
        label: "Write security tests",
        description: "(Phase 2: Tests, 1 min) test_rate_limiting, test_brute_force, test_weak_password | 🔴 TDD Red Phase"
      },

      # Phase 3: Implementation (TDD Green Phase) - Break into concrete files
      {
        label: "Implement User model",
        description: "(Phase 3: Implementation, 2 min) models/user.py - User model with password hashing (bcrypt) | 🟢 TDD Green Phase"
      },
      {
        label: "Implement JWT service",
        description: "(Phase 3: Implementation, 3 min) services/auth.py - create_token, validate_token, hash_password | 🟢 TDD Green Phase"
      },
      {
        label: "Implement auth endpoints",
        description: "(Phase 3: Implementation, 3 min) api/auth.py - POST /login, /refresh, /logout | 🟢 TDD Green Phase"
      },
      {
        label: "Implement auth middleware",
        description: "(Phase 3: Implementation, 2 min) middleware/auth.py - JWT validation decorator @require_auth | 🟢 TDD Green Phase"
      },

      # Phase 4: Security Hardening - Break into concrete features
      {
        label: "Add rate limiting",
        description: "(Phase 4: Security, 1 min) 5 attempts per 5 minutes on auth endpoints"
      },
      {
        label: "Add brute force protection",
        description: "(Phase 4: Security, 1 min) Account lockout after failed attempts"
      },
      {
        label: "Add password requirements",
        description: "(Phase 4: Security, 1 min) Minimum 8 chars, complexity validation"
      },

      # Phase 5: Documentation - Break into concrete docs
      {
        label: "Create OpenAPI documentation",
        description: "(Phase 5: Documentation, 1 min) Update openapi.yaml with auth endpoints, schemas, examples"
      },
      {
        label: "Document security best practices",
        description: "(Phase 5: Documentation, 1 min) Add security.md with token storage, rotation, best practices"
      },

      # Special options
      {
        label: "All Steps (Full TDD)",
        description: "✅ RECOMMENDED: Execute ALL steps above in order (Phases 1-5, complete TDD implementation, production-ready)"
      },
      {
        label: "All Tests Only",
        description: "🔴 Execute only test-writing steps (Phase 2: all test steps) - TDD Red Phase preparation"
      },
      {
        label: "All Implementation Only",
        description: "🟢 Execute only implementation steps (Phase 3: all implementation steps) - TDD Green Phase (requires tests written first!)"
      },
      {
        label: "Skip Tests (NOT RECOMMENDED)",
        description: "⚠️ Execute Architecture + Implementation + Security + Docs, but SKIP Phase 2 (Tests). Pain #4: Biggest mistake!"
      }
    ]
  }]
})
```

**IMPORTANT:**
- If user selects "All Steps (Full TDD)", ignore other selections and execute ALL steps in order
- If user selects "All Tests Only", execute only Phase 2 steps
- If user selects "All Implementation Only", execute only Phase 3 steps (warn if tests not written yet)
- If user selects "Skip Tests", execute all steps EXCEPT Phase 2 (warn about Pain #4)
- Otherwise, execute ONLY the individually selected steps
- Steps must be executed in phase order (Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5) even if selected out of order

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

After each phase, report progress and continue automatically if "All Phases" was selected, otherwise ask for confirmation:

```markdown
Phase 1 Complete: Architecture Designed ✓

Auth Flow:
- POST /auth/login → access_token (15min) + refresh_token (7days)
- POST /auth/refresh → new access_token
- POST /auth/logout → invalidate refresh_token

Database Schema:
- users: id, email, password_hash, created_at
- refresh_tokens: id, user_id, token_hash, expires_at
```

**If "All Phases" NOT selected**, use AskUserQuestion for continuation:

```python
AskUserQuestion({
  questions: [{
    question: "Phase 1 complete. Ready to continue to Phase 2 (Tests)?",
    header: "Continue",
    multiSelect: false,
    options: [
      {
        label: "Yes, continue to Phase 2",
        description: "Write failing tests (TDD Red Phase)"
      },
      {
        label: "No, stop here",
        description: "Stop implementation and review results"
      }
    ]
  }]
})
```

Repeat for each phase transition.

**If "All Phases" WAS selected**, continue automatically without asking.

---

Final summary after all selected phases complete:

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
