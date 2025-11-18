# C_FOLLOW_PATTERNS: Follow Existing Patterns

**Severity**: High

Always follow existing code patterns, naming conventions, architectural decisions, and coding styles. Consistency > personal preference.

---

## Why

Inconsistent patterns create cognitive load, maintenance burden, review friction, onboarding difficulty, hidden bugs, and merge conflicts.

---

## Core Techniques

### 1. Examine Existing Code First
```python
# Task: Add new API endpoint

# Step 1: Find existing
Grep("@app.route", output_mode="content", "-C": 5)
# Pattern: snake_case, jsonify(), try/except

# Step 2: Match pattern
@app.route('/api/users')  # Match route style
def <old_function_name>():  # snake_case
    try:
        users = db.query_users()
        return jsonify(users)
    except DatabaseError as e:
        return jsonify({'error': str(e)}), 500
```

### 2. Match Naming Conventions
```python
# Existing uses snake_case
# existing_function(), process_data()

# ❌ BAD: camelCase
def <function_name>(email):

# ✅ GOOD: snake_case
def <function_name>(email):
```

### 3. Follow Error Handling
```python
# Discover pattern
Grep("try.*except", output_mode="content", "-C": 3)

# ❌ BAD: Different handling
try:
    result = my_op()
except Exception:  # Too broad
    print("Error")    # Print, not logging
    return None       # Return, not raise

# ✅ GOOD: Match pattern
try:
    result = my_op()
except SpecificError as e:  # Specific
    logger.error(f"Op failed: {e}")  # Log
    raise  # Raise
```

### 4. Replicate File Organization
```bash
# Existing:
# src/<model_file>.py, product.py
# <service_dir>/auth_service.py
# <util_dir>/validators.py

# ❌ BAD: New pattern
# src/helpers/email_helper.py

# ✅ GOOD: Follow existing
# <util_dir>/email_utils.py
```

### 5. Match Testing Patterns
```python
# Existing uses classes
# class TestAuth:
#     def test_login_success(self):

# ❌ BAD: Different structure
def test_payment():
    assert <function_name>(100) == success

# ✅ GOOD: Match pattern
class TestPayment:
    def test_payment_success(self):
        result = <function_name>(100)
        assert result.success is True
```

---

## Anti-Patterns

### ❌ "My Way is Better"
```python
# Existing uses if/else
if user.is_admin:
    grant_access()
else:
    deny_access()

# ❌ BAD: Introduce ternary
grant_access() if user.is_admin else deny_access()

# ✅ GOOD: Match existing
if user.is_admin:
    grant_access()
else:
    deny_access()
```

### ❌ Framework Fighting
```python
# Django ORM everywhere
users = User.objects.filter(active=True)

# ❌ BAD: Raw SQL
users = db.execute("SELECT * FROM users WHERE active = 1")

# ✅ GOOD: Use ORM
users = User.objects.filter(active=True)
```

---

## Checklist

### Before Writing
- [ ] Search for similar code (Grep/Glob)
- [ ] Identify patterns (naming, structure, errors)
- [ ] Check framework conventions
- [ ] Review style guide if exists

### While Writing
- [ ] Match naming conventions exactly
- [ ] Use same class/function organization
- [ ] Use same try/except patterns
- [ ] Import libraries same way
- [ ] Follow documentation style

### After Writing
- [ ] Compare with existing code
- [ ] Run project linters
- [ ] Verify tests follow patterns
- [ ] Check consistency
