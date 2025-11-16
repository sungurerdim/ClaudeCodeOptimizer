---
id: C_FOLLOW_PATTERNS
title: Follow Existing Patterns
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_FOLLOW_PATTERNS: Follow Existing Patterns 🔴

**Severity**: High

Always follow existing code patterns, naming conventions, architectural decisions, and coding styles. Match the codebase's established patterns instead of introducing new ones. Consistency is more important than personal preference.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Inconsistent patterns create cognitive overhead and maintenance issues:**

- **Cognitive Load** - Developers must learn multiple patterns for same concept (e.g., error handling done 3 different ways)
- **Maintenance Burden** - Inconsistent code is harder to maintain; developers can't rely on patterns
- **Review Friction** - Reviewers flag inconsistencies, slowing reviews
- **Onboarding Difficulty** - New developers struggle when patterns vary across codebase
- **Hidden Bugs** - Pattern inconsistencies often indicate misunderstood architecture
- **Merge Conflicts** - Different styles for same functionality increase conflict likelihood

### Core Techniques

**1. Examine Existing Code First**

Before writing any new code, examine similar existing code:

```python
# Task: Add new API endpoint

# Step 1: Find existing API endpoints
Grep("@app.route", output_mode="content", "-C": 5)
# Examine patterns:
# - All use snake_case for function names
# - All return JSON via jsonify()
# - All use try/except with specific exceptions

# Step 2: Match the pattern
@app.route('/api/users')  # Match existing route style
def get_users():  # snake_case like others
    try:
        users = db.query_users()
        return jsonify(users)  # JSON like others
    except DatabaseError as e:  # Specific exceptions like others
        return jsonify({'error': str(e)}), 500
```

**2. Match Naming Conventions**

```python
# Examine existing code:
# existing_function()
# process_data()
# validate_input()
# → Pattern: snake_case for functions

# ❌ BAD: Introduce camelCase
def validateEmail(email):  # Inconsistent!
    pass

# ✅ GOOD: Match snake_case
def validate_email(email):  # Consistent
    pass
```

**3. Follow Error Handling Patterns**

```python
# Existing pattern inspection:
Grep("try.*except", output_mode="content", "-C": 3)

# Pattern found: All code uses specific exceptions + logging
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise

# ❌ BAD: Different error handling
try:
    result = my_operation()
except Exception:  # Too broad, inconsistent
    print("Error")  # Print instead of logging, inconsistent
    return None  # Return instead of raise, inconsistent

# ✅ GOOD: Match pattern
try:
    result = my_operation()
except SpecificError as e:  # Specific like others
    logger.error(f"Operation failed: {e}")  # Log like others
    raise  # Raise like others
```

**4. Replicate File Organization**

```bash
# Existing structure:
# src/
#   models/
#     user.py
#     product.py
#   services/
#     auth_service.py
#     payment_service.py
#   utils/
#     validators.py

# ❌ BAD: Introduce new structure
# src/
#   helpers/  # New pattern, inconsistent
#     email_helper.py

# ✅ GOOD: Follow existing structure
# src/
#   utils/  # Existing pattern
#     email_utils.py  # Matches naming (utils suffix)
```

**5. Match Testing Patterns**

```python
# Examine existing tests:
# tests/test_auth.py:
#   class TestAuth:
#       def test_login_success(self):
#           ...
#       def test_login_failure(self):
#           ...

# ❌ BAD: Different test structure
def test_payment():  # Not using class
    assert process_payment(100) == success  # Different assertion style

# ✅ GOOD: Match pattern
class TestPayment:  # Class like others
    def test_payment_success(self):  # Naming pattern
        result = process_payment(100)
        assert result.success is True  # Assertion style like others
```

---

### Implementation Patterns

#### ✅ Good: Pattern Discovery Before Implementation

```python
# Task: Add email validation function

# Step 1: Find existing validators
Grep("def validate", output_mode="content", "-C": 3)
# Pattern discovered:
# - Functions named validate_*
# - Raise ValueError on failure
# - Return True on success
# - Have docstrings

# Step 2: Match the pattern
def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid

    Raises:
        ValueError: If email format is invalid
    """
    if not email or '@' not in email:
        raise ValueError(f"Invalid email: {email}")
    return True
```

---

#### ✅ Good: Following Architectural Patterns

```python
# Existing architecture inspection:
Grep("class.*Service", output_mode="content", "-C": 10)

# Pattern found: All services follow same structure:
# - Inherit from BaseService
# - Constructor takes db and logger
# - Methods use self.logger for logging
# - Return Result objects, not raw values

# ✅ GOOD: Match the pattern
class EmailService(BaseService):  # Inherit like others
    def __init__(self, db, logger):  # Constructor like others
        super().__init__(db, logger)

    def send_email(self, to, subject, body):
        self.logger.info(f"Sending email to {to}")  # Log like others
        try:
            result = self._send_via_smtp(to, subject, body)
            return Result(success=True, data=result)  # Result object like others
        except SMTPError as e:
            self.logger.error(f"Email failed: {e}")
            return Result(success=False, error=str(e))  # Result object like others
```

---

#### ❌ Bad: Introducing New Patterns

```python
# Existing codebase uses async/await:
async def fetch_user(user_id):
    return await db.get_user(user_id)

async def fetch_products():
    return await db.get_products()

# ❌ BAD: Introduce synchronous pattern
def fetch_orders():  # Not async, inconsistent!
    return db.get_orders()  # Blocking call, inconsistent!

# ✅ GOOD: Match async pattern
async def fetch_orders():  # Async like others
    return await db.get_orders()  # Await like others
```

---

#### ❌ Bad: Mixing Naming Conventions

```python
# Existing code uses snake_case:
def process_payment(amount):
    pass

def validate_user(user):
    pass

# ❌ BAD: Mix camelCase and snake_case
def calculateTotal(items):  # camelCase, inconsistent
    pass

class userManager:  # lowercase class, inconsistent (should be UserManager)
    def ProcessData(self):  # PascalCase method, inconsistent
        pass

# ✅ GOOD: Consistent snake_case
def calculate_total(items):  # snake_case like others
    pass

class UserManager:  # PascalCase class like others
    def process_data(self):  # snake_case method like others
        pass
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "My Way is Better"

**Problem**: Introducing "better" patterns without team agreement.

```python
# Existing codebase uses simple if/else:
if user.is_admin:
    grant_access()
else:
    deny_access()

# ❌ BAD: Introduce ternary operator pattern
grant_access() if user.is_admin else deny_access()  # "More concise!"

# ✅ GOOD: Match existing simple pattern
if user.is_admin:
    grant_access()
else:
    deny_access()
```

**Impact:**
- Creates pattern inconsistency
- Forces reviewers to evaluate new pattern
- May not align with team skill levels or preferences

---

### ❌ Anti-Pattern 2: Framework Fighting

**Problem**: Fighting framework conventions instead of following them.

```python
# Django project uses Django ORM everywhere:
users = User.objects.filter(active=True)

# ❌ BAD: Introduce raw SQL
users = db.execute("SELECT * FROM users WHERE active = 1")  # Raw SQL, inconsistent

# ✅ GOOD: Use Django ORM like rest of codebase
users = User.objects.filter(active=True)  # ORM like others
```

**Impact:**
- Bypasses framework features (migrations, validation)
- Inconsistent data access patterns
- Harder maintenance

---

### ❌ Anti-Pattern 3: Language Feature Hopping

**Problem**: Using latest language features before codebase adopts them.

```python
# Codebase is Python 3.8, uses traditional typing:
from typing import List, Dict

def process(items: List[str]) -> Dict[str, int]:
    pass

# ❌ BAD: Use Python 3.10+ features
def process_new(items: list[str]) -> dict[str, int]:  # 3.10+ syntax, inconsistent
    pass

# ✅ GOOD: Match existing typing style
from typing import List, Dict

def process_new(items: List[str]) -> Dict[str, int]:  # Match existing
    pass
```

**Impact:**
- May not work on older Python versions
- Inconsistent with existing code
- Creates cognitive load (why is this different?)

---

## Implementation Checklist

### Before Writing Code

- [ ] **Search for similar code** - Grep/Glob for existing implementations
- [ ] **Identify patterns** - What naming, structure, error handling patterns exist?
- [ ] **Check framework conventions** - What does the framework recommend?
- [ ] **Review project docs** - Does project have style guide or conventions doc?

### While Writing Code

- [ ] **Match naming** - Follow existing naming conventions exactly
- [ ] **Match structure** - Use same class/function organization as existing code
- [ ] **Match error handling** - Use same try/except patterns
- [ ] **Match imports** - Import libraries the same way others do
- [ ] **Match comments/docs** - Follow existing documentation style

### After Writing Code

- [ ] **Compare with existing** - Does new code look like existing code?
- [ ] **Run linters** - Do project linters accept the new code?
- [ ] **Test consistency** - Do tests follow existing test patterns?
- [ ] **Review patterns** - Are all patterns consistent with codebase?

---

## Summary

**Follow Existing Patterns** means matching the codebase's established naming conventions, architectural decisions, error handling, file organization, and coding styles. Consistency trumps personal preference. When in doubt, do what existing code does.

**Core Rules:**

- **Examine first** - Search existing code for patterns before writing new code
- **Match exactly** - Follow naming, structure, error handling exactly as existing code does
- **Framework conventions** - Follow framework patterns, don't fight them
- **Consistency > perfection** - Matching existing pattern is better than introducing "better" inconsistent pattern
- **When to diverge** - Only introduce new patterns with explicit team/user agreement
