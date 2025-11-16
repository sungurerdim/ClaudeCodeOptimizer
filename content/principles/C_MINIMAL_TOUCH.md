---
id: C_MINIMAL_TOUCH
title: Minimal Touch Policy
category: claude-guidelines
severity: critical
weight: 10
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_MINIMAL_TOUCH: Minimal Touch Policy 🔴

**Severity**: Critical

Make minimal, surgical changes. Only modify what's strictly necessary to complete the task. Don't refactor unrelated code, don't fix style issues, don't rename variables unless specifically requested.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Excessive changes create risk and review overhead:**

- **Bug Introduction** - Touching unrelated code risks introducing new bugs in working functionality
- **Review Burden** - Large diffs with unnecessary changes slow code reviews dramatically
- **Difficult Rollback** - Mixed changes (bug fix + refactor) complicate rollback if needed
- **Obscured Intent** - Actual necessary changes hidden among unnecessary modifications
- **Merge Conflicts** - More changes = higher likelihood of conflicts with other work
- **Testing Scope Creep** - Unrelated changes expand what needs testing

### Core Techniques

**1. Surgical Edits Only**

```python
# Task: Fix bug where user.age is accessed incorrectly

# ❌ BAD: Fix + unnecessary refactoring
Edit("src/user.py",
     old_string="""def get_user_info(user):
    name = user.name
    age = user.years  # Bug: should be user.age
    return f"{name} is {age}"

def get_user_email(user):
    return user.email""",
     new_string="""def get_user_info(user):
    return f"{user.name} is {user.age}"  # Fixed bug + inlined everything

def retrieve_user_email_address(user):  # Renamed unnecessarily
    return user.email""")

# ✅ GOOD: Fix bug only, minimal change
Edit("src/user.py",
     old_string="age = user.years  # Bug: should be user.age",
     new_string="age = user.age  # Fixed: was user.years")
```

---

**2. Don't Touch Unrelated Code**

```python
# Task: Add email validation to signup()

# ❌ BAD: Modify unrelated functions in same file
Edit("auth.py",
     old_string="""def signup(email, password):
    user = create_user(email, password)
    return user

def login(email, password):
    return authenticate(email, password)

def logout(session_id):
    return destroy_session(session_id)""",
     new_string="""def signup(email, password):
    if not validate_email(email):
        raise ValueError("Invalid email")
    user = create_user(email, password)
    return user

def login(email, password):
    # Refactored unnecessarily
    if not email or not password:
        raise ValueError("Missing credentials")
    return authenticate(email, password)

def logout(session_id):
    # Also refactored
    if not session_id:
        raise ValueError("No session")
    return destroy_session(session_id)""")

# ✅ GOOD: Only modify signup(), leave others untouched
Edit("auth.py",
     old_string="""def signup(email, password):
    user = create_user(email, password)
    return user""",
     new_string="""def signup(email, password):
    if not validate_email(email):
        raise ValueError("Invalid email")
    user = create_user(email, password)
    return user""")
```

---

**3. Don't Fix Style Unless Requested**

```python
# Task: Fix null pointer bug

# ❌ BAD: Fix bug + reformat entire file
Edit("service.py",
     old_string="""def process(data):
    result=None  # Bad style but WORKING
    if data:
        result=data.process()
    return result.value  # Bug: result might be None""",
     new_string="""def process(data):
    result = None  # Fixed style
    if data:
        result = data.process()
    return result.value if result else None  # Fixed bug + style""")

# ✅ GOOD: Fix bug only, ignore style
Edit("service.py",
     old_string="return result.value  # Bug: result might be None",
     new_string="return result.value if result else None")
```

---

**4. One Logical Change Per Edit**

```python
# Task: Add rate limiting to API

# ❌ BAD: Multiple unrelated changes
Edit("api.py",
     old_string=old_api_code,
     new_string="""# Added rate limiting + changed DB + updated logging + refactored""")

# ✅ GOOD: One logical change - add rate limiting
Edit("api.py",
     old_string="""@app.route('/api/data')
def get_data():
    return fetch_data()""",
     new_string="""@app.route('/api/data')
@rate_limit(requests=100, window=60)
def get_data():
    return fetch_data()""")
```

---

**5. When Refactoring IS Needed**

```python
# User: "Add feature X, and refactor the auth module for clarity"

# ✅ GOOD: User explicitly requested refactoring
# Make changes as requested, both feature and refactor

# BUT: Still keep commits separate if possible
# Commit 1: Add feature X
# Commit 2: Refactor auth module
```

---

### Implementation Patterns

#### ✅ Good: Minimal Bug Fix

```python
# Bug: Division by zero in calculate_average()

# Read to find exact location
Read("stats.py", offset=50, limit=20)
# Lines 55-65:
# def calculate_average(numbers):
#     total = sum(numbers)
#     return total / len(numbers)  # Bug: len() might be 0

# ✅ GOOD: Fix only the bug
Edit("stats.py",
     old_string="return total / len(numbers)",
     new_string="return total / len(numbers) if numbers else 0")

# ✅ Result: 1-line change, surgical fix
```

---

#### ✅ Good: Targeted Feature Addition

```python
# Task: Add logging to critical function

# ✅ GOOD: Add only what's requested
Edit("processor.py",
     old_string="""def process_payment(amount):
    result = payment_api.charge(amount)
    return result""",
     new_string="""def process_payment(amount):
    logger.info(f"Processing payment: ${amount}")
    result = payment_api.charge(amount)
    logger.info(f"Payment result: {result.status}")
    return result""")

# Added logging, didn't refactor, didn't change error handling
```

---

#### ❌ Bad: Scope Creep

```python
# Task: Fix bug in login()

# ❌ BAD: Fix + refactor + style + rename
Edit("auth.py",
     old_string="""def login(username, password):
    user = db.get_user(username)
    if user and user.password == password:  # Bug: plain text comparison
        return create_session(user)
    return None

def logout(session_id):
    destroy_session(session_id)

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password""",
     new_string="""def authenticate_user(email, pwd):  # Renamed everything
    \"\"\"Authenticate user with email and password.\"\"\"  # Added docstrings
    user_record = db.query_user(email)  # Changed function names
    if user_record and verify_password(pwd, user_record.password_hash):  # Fixed
        return generate_session(user_record)  # Renamed
    raise AuthenticationError("Invalid credentials")  # Changed return style

def terminate_session(session_identifier):  # Renamed
    \"\"\"Terminate user session.\"\"\"  # Added docstring
    destroy_session(session_identifier)

class UserModel:  # Renamed class
    \"\"\"User data model.\"\"\"  # Added docstring
    def __init__(self, email, password_hash):  # Changed parameters
        self.email = email  # Renamed field
        self.password_hash = password_hash  # Changed field""")

# Problems:
# - Fixed bug (good) but also...
# - Renamed functions, parameters, classes
# - Changed return style (None → exception)
# - Added docstrings everywhere
# - Refactored db calls
# - Changed field names
# → IMPOSSIBLE to review; can't isolate the actual bug fix!
```

---

#### ❌ Bad: Opportunistic Refactoring

```python
# Task: Add email field to User model

# ❌ BAD: Add field + refactor everything else
Edit("models.py",
     old_string="""class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return f"{self.name}, {self.age}"

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price""",
     new_string="""class User:
    def __init__(self, name, age, email):  # Added email
        self._name = name  # Made private
        self._age = age    # Made private
        self._email = email  # Added email

    @property
    def name(self):  # Added property
        return self._name

    @property
    def age(self):  # Added property
        return self._age

    def get_info(self):
        return f"{self._name}, {self._age}, {self._email}"

class Product:  # Also refactored Product unnecessarily
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name""")

# ✅ GOOD: Just add email field
Edit("models.py",
     old_string="""class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age""",
     new_string="""class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email""")
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Fixing Style While Fixing Bugs

**Problem**: Mixing functional changes with style fixes.

```python
# ❌ BAD: Bug fix + style fix in one change
Edit("calc.py",
     old_string="def calculate(x,y): return x/y",  # No spaces, one line
     new_string="""def calculate(x, y):  # Fixed style
    \"\"\"Calculate division.\"\"\"  # Added docstring
    if y == 0:  # Fixed bug
        raise ValueError("Division by zero")
    return x / y  # Fixed style""")

# ✅ GOOD: Fix bug only
Edit("calc.py",
     old_string="return x/y",
     new_string="if y == 0: raise ValueError('Division by zero')\nreturn x/y")

# If style is also needed:
# User: "Also fix the style"
# Then make separate edit for style
```

**Impact:**
- Can't separate bug fix from style change in git blame
- If style change causes issue, can't roll back just that
- Review overhead: "Is this change functional or cosmetic?"

---

### ❌ Anti-Pattern 2: Scope Creep "While I'm Here"

**Problem**: "While I'm here, let me also..."

```python
# Task: Add validation to create_user()

# ❌ BAD: "While I'm here" syndrome
Edit("users.py",
     old_string=existing_code,
     new_string="""# Added validation (requested)
# Also renamed functions (not requested)
# Also added docstrings (not requested)
# Also refactored error handling (not requested)
# Also changed import structure (not requested)""")

# ✅ GOOD: Only validation
Edit("users.py",
     old_string="""def create_user(email, password):
    user = User(email, password)
    db.save(user)
    return user""",
     new_string="""def create_user(email, password):
    if not email or '@' not in email:
        raise ValueError("Invalid email")
    if len(password) < 8:
        raise ValueError("Password too short")
    user = User(email, password)
    db.save(user)
    return user""")
```

**Impact:**
- Changes unrelated to task
- Increases risk unnecessarily
- Makes rollback complicated

---

## Implementation Checklist

### Before Making Changes

- [ ] **Read exact location** - Use Read with offset/limit to see current code
- [ ] **Identify minimal change** - What's the smallest edit that accomplishes the goal?
- [ ] **Verify scope** - Am I touching only what's necessary?
- [ ] **Check for scope creep** - Am I adding unrequested improvements?

### During Editing

- [ ] **Use Edit, not Write** - Edit makes surgical changes; Write replaces entire file
- [ ] **Match existing style** - Don't reformat unless requested
- [ ] **One logical change** - Fix bug OR add feature OR refactor, not all three
- [ ] **Don't rename** - Leave variable/function names unchanged unless requested

### After Editing

- [ ] **Verify minimal diff** - Did I change only what's necessary?
- [ ] **No style fixes** - Did I resist fixing unrelated style issues?
- [ ] **No opportunistic refactoring** - Did I avoid "while I'm here" changes?
- [ ] **Clear intent** - Is it obvious WHY each line changed?

---

## Summary

**Minimal Touch Policy** means making surgical, targeted changes to only what's strictly necessary. Don't refactor unrelated code, don't fix style, don't rename unless explicitly requested. Small, focused changes are safer, faster to review, and easier to roll back.

**Core Rules:**

- **Surgical edits** - Change only the minimum required lines
- **No unrelated changes** - Don't touch code unrelated to the task
- **No style fixes** - Ignore style issues unless specifically requested
- **One logical change** - Fix bug OR add feature OR refactor, not mixed
- **No "while I'm here"** - Resist opportunistic improvements
