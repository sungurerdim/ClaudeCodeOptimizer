---
name: cco-skill-security-fundamentals
description: Prevent OWASP Top 10 vulnerabilities including Broken Access Control (2025 #1), SQL injection, XSS, CSRF, and Exception Handling issues via secure coding patterns and comprehensive validation
keywords: [security, OWASP, broken access control, XSS, SQL injection, CSRF, auth, sanitize, escape, validate, injection, bcrypt, JWT, rate limiting, exception handling, authorization]
category: security
related_commands:
  action_types: [audit, fix, generate]
  categories: [security]
pain_points: [1, 2, 3]
---

# Security - OWASP Top 10, XSS, SQLi, CSRF, Access Control

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


Prevent OWASP Top 10 2025 vulnerabilities via secure coding patterns and comprehensive validation.
---

---

## Domain

Web applications, APIs, authentication systems, data validation.

---

## Purpose

**OWASP Top 10 2025 Critical Changes:**
- **Broken Access Control → #1** (was #5 in 2021) - Most exploited vulnerability
- **Injection → #3** (was #1 in 2021) - Still critical but overtaken
- **Exception Handling → #10** (NEW category) - Failing open creates security risks

**Why These Changes:**
- AI-generated code often skips authentication checks (tutorial patterns)
- Developers copy/paste endpoints without adding auth decorators
- Exception handling frequently fails open instead of closed

---

## Core Techniques

### 1. Broken Access Control (OWASP A01:2025 - NEW #1)

**Why #1:** Most common vulnerability, easy to exploit, AI code frequently missing auth.

**Horizontal Privilege Escalation:**
```python
# ❌ BAD: User can access any user's data
@app.route('/api/user/<user_id>')
def get_user(user_id):
    user = db.query(User).filter_by(id=user_id).first()
    return jsonify(user.to_dict())
# Missing: Is current_user allowed to view this user?

# ✅ GOOD: Verify ownership
@app.route('/api/user/<user_id>')
@require_auth
def get_user(user_id):
    # Check horizontal access
    if str(current_user.id) != user_id and not current_user.is_admin:
        abort(403, "Forbidden: Cannot access other users' data")

    user = db.query(User).filter_by(id=user_id).first()
    return jsonify(user.to_dict())
```

**Vertical Privilege Escalation:**
```python
# ❌ BAD: No role check
@app.route('/api/admin/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.query(User).filter_by(id=user_id).delete()
    db.commit()
    return {'status': 'deleted'}

# ✅ GOOD: Role-based access control
@app.route('/api/admin/delete-user/<user_id>', methods=['DELETE'])
@require_auth
@require_role('admin')  # Vertical access control
def delete_user(user_id):
    # Additional check: Can't delete yourself
    if str(current_user.id) == user_id:
        abort(400, "Cannot delete your own account")

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        abort(404, "User not found")

    db.delete(user)
    db.commit()

    audit_log.log_deletion(current_user.id, user_id)
    return {'status': 'deleted'}
```

**Detection Pattern:**
```python
def detect_missing_access_control(code: str) -> List[dict]:
    """Find endpoints without proper access control"""
    issues = []

    # Find all route definitions
    routes = re.findall(
        r'@app\.route\([\'"](.+?)[\'"]\s*(?:,\s*methods=\[(.+?)\])?\).*?def\s+(\w+)',
        code,
        re.DOTALL
    )

    for route, methods, func_name in routes:
        # Get function body
        func_match = re.search(
            rf'def {func_name}\(.*?\):(.+?)(?=\ndef|$)',
            code,
            re.DOTALL
        )
        if not func_match:
            continue

        func_body = func_match.group(1)

        # Check for authentication
        has_auth = any(keyword in code[:func_match.start()] for keyword in [
            '@require_auth', '@login_required', '@authenticate'
        ])

        # Check for authorization
        has_authz = any(keyword in func_body for keyword in [
            'current_user.id', 'check_permission', 'require_role',
            'is_admin', 'can_access'
        ])

        # Check for data modification
        modifies_data = any(keyword in func_body for keyword in [
            'db.add', 'db.delete', 'db.update', 'db.commit',
            '.save()', '.delete()', '.update()', 'DELETE', 'UPDATE', 'INSERT'
        ])

        # Check HTTP methods
        dangerous_methods = methods and any(m in methods.upper() for m in ['POST', 'PUT', 'DELETE', 'PATCH'])

        # Report issues
        if modifies_data and not has_auth:
            issues.append({
                'type': 'broken_access_control',
                'subtype': 'missing_authentication',
                'route': route,
                'function': func_name,
                'severity': 'CRITICAL',
                'owasp': 'A01:2025',
                'message': f"Route '{route}' modifies data without authentication"
            })

        if (modifies_data or dangerous_methods) and has_auth and not has_authz:
            issues.append({
                'type': 'broken_access_control',
                'subtype': 'missing_authorization',
                'route': route,
                'function': func_name,
                'severity': 'HIGH',
                'owasp': 'A01:2025',
                'message': f"Route '{route}' has authentication but no authorization check"
            })

    return issues
```

---

### 2. SQL Injection (OWASP A03:2025)

**Parameterized Queries:**
```python
# ❌ BAD: String concatenation
def get_user_by_email(email: str):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return db.execute(query).fetchone()
# Vulnerable: email = "' OR '1'='1" → returns all users

# ✅ GOOD: Parameterized query
def get_user_by_email(email: str):
    query = "SELECT * FROM users WHERE email = %s"
    return db.execute(query, (email,)).fetchone()
```

**ORM Usage:**
```python
# ❌ BAD: Raw SQL with f-string
def search_products(query: str):
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    return db.execute(sql).fetchall()

# ✅ GOOD: ORM (SQLAlchemy)
def search_products(query: str):
    return db.query(Product).filter(
        Product.name.ilike(f'%{query}%')
    ).all()
```

**Detection Pattern:**
```python
def detect_sql_injection(code: str) -> List[dict]:
    """Find SQL injection vulnerabilities"""
    issues = []

    # Pattern 1: f-string with SQL keywords
    f_string_sql = re.finditer(
        r'f["\'].*?(SELECT|INSERT|UPDATE|DELETE|WHERE|FROM).*?{.*?}.*?["\']',
        code,
        re.IGNORECASE
    )
    for match in f_string_sql:
        issues.append({
            'type': 'sql_injection',
            'subtype': 'f_string_sql',
            'severity': 'CRITICAL',
            'owasp': 'A03:2025',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'SQL query with f-string interpolation (injection risk)'
        })

    # Pattern 2: String concatenation with SQL
    concat_sql = re.finditer(
        r'(SELECT|INSERT|UPDATE|DELETE).*?\+.*?(request\.|input\(|user\.)',
        code,
        re.IGNORECASE
    )
    for match in concat_sql:
        issues.append({
            'type': 'sql_injection',
            'subtype': 'string_concatenation',
            'severity': 'CRITICAL',
            'owasp': 'A03:2025',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'SQL query with string concatenation (injection risk)'
        })

    # Pattern 3: execute() without parameterization
    execute_no_params = re.finditer(
        r'\.execute\([\'"](?:SELECT|INSERT|UPDATE|DELETE).*?[\'"](?!\s*,)',
        code,
        re.IGNORECASE
    )
    for match in execute_no_params:
        if 'WHERE' in match.group().upper() or 'VALUES' in match.group().upper():
            issues.append({
                'type': 'sql_injection',
                'subtype': 'no_parameterization',
                'severity': 'HIGH',
                'owasp': 'A03:2025',
                'line': code[:match.start()].count('\n') + 1,
                'message': 'SQL execute without parameters (potential injection)'
            })

    return issues
```

---

### 3. Cross-Site Scripting (XSS) (OWASP A07:2025)

**Output Encoding:**
```python
# ❌ BAD: Direct HTML rendering
@app.route('/profile/<username>')
def profile(username):
    user = get_user(username)
    return f"<h1>Welcome {user.name}</h1>"  # XSS if name = "<script>alert(1)</script>"

# ✅ GOOD: Template auto-escaping
@app.route('/profile/<username>')
def profile(username):
    user = get_user(username)
    return render_template('profile.html', name=user.name)
# Template: <h1>Welcome {{ name }}</h1>  (auto-escaped)
```

**CSP Headers:**
```python
# ✅ Content Security Policy
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.example.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response
```

**Detection Pattern:**
```python
def detect_xss(code: str) -> List[dict]:
    """Find XSS vulnerabilities"""
    issues = []

    # Pattern 1: innerHTML with user input
    innerhtml = re.finditer(
        r'\.innerHTML\s*=.*?(request\.|params\.|user\.|input\()',
        code
    )
    for match in innerhtml:
        issues.append({
            'type': 'xss',
            'subtype': 'innerhtml',
            'severity': 'CRITICAL',
            'owasp': 'A07:2025',
            'message': 'innerHTML with user input (XSS risk)'
        })

    # Pattern 2: Direct HTML string building
    html_concat = re.finditer(
        r'f["\']<.*?>.*?{.*?}.*?</.*?>["\']',
        code
    )
    for match in html_concat:
        issues.append({
            'type': 'xss',
            'subtype': 'html_concatenation',
            'severity': 'HIGH',
            'owasp': 'A07:2025',
            'message': 'HTML string building with interpolation (XSS risk)'
        })

    # Pattern 3: Missing CSP headers
    if 'Content-Security-Policy' not in code and '@app.after_request' in code:
        issues.append({
            'type': 'xss',
            'subtype': 'missing_csp',
            'severity': 'MEDIUM',
            'owasp': 'A07:2025',
            'message': 'No Content-Security-Policy headers configured'
        })

    return issues
```

---

### 4. CSRF Protection

**Token-Based Protection:**
```python
# ❌ BAD: No CSRF protection
@app.route('/api/transfer', methods=['POST'])
def transfer_funds():
    amount = request.form['amount']
    to_account = request.form['to_account']
    # Vulnerable to CSRF attacks
    process_transfer(current_user, to_account, amount)

# ✅ GOOD: CSRF token validation
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

@app.route('/api/transfer', methods=['POST'])
@csrf.exempt  # Only if using custom CSRF
def transfer_funds():
    # CSRF token automatically validated by decorator
    amount = request.form['amount']
    to_account = request.form['to_account']
    process_transfer(current_user, to_account, amount)
```

**SameSite Cookies:**
```python
# ✅ SameSite cookie configuration
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # or 'Strict'
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JS access
```

---

### 5. Authentication & Authorization

**Password Hashing:**
```python
# ❌ BAD: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # Weak!

# ❌ BAD: Plain text
user.password = password  # NEVER!

# ✅ GOOD: bcrypt or argon2
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)  # Cost factor 12
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())
```

**JWT Configuration:**
```python
# ❌ BAD: Long-lived tokens
jwt.encode({'user_id': user.id}, SECRET, algorithm='HS256')
# No expiration!

# ✅ GOOD: Short-lived with refresh
from datetime import datetime, timedelta

def create_access_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),  # 15min
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')

def create_refresh_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=30),  # 30 days
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm='HS256')
```

---

### 6. Exception Handling Security (OWASP A10:2025 - NEW)

**Fail Closed, Not Open:**
```python
# ❌ BAD: Failing open
def authenticate_user(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return User.query.get(payload['user_id'])
    except jwt.ExpiredSignatureError:
        return get_guest_user()  # DANGEROUS: Fails open!

# ✅ GOOD: Fail closed
def authenticate_user(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
## Checklist

### Broken Access Control (A01:2025)
- [ ] All endpoints have authentication decorators
- [ ] Horizontal access control (user can't access other users' data)
- [ ] Vertical access control (role-based permissions)
- [ ] Resource ownership validated
- [ ] Admin functions require admin role

### SQL Injection (A03:2025)
- [ ] No string concatenation in SQL queries
- [ ] Parameterized queries or ORM used
- [ ] No f-strings with SQL keywords
- [ ] Input validation before database queries

### XSS (A07:2025)
- [ ] Template auto-escaping enabled
- [ ] No innerHTML with user input
- [ ] CSP headers configured
- [ ] No direct HTML string building

### CSRF
- [ ] CSRF tokens on POST/PUT/DELETE
- [ ] SameSite cookies configured
- [ ] Framework CSRF protection enabled

### Authentication
- [ ] bcrypt or argon2 for passwords
- [ ] JWT expiration < 15 minutes
- [ ] Refresh tokens implemented
- [ ] Secure cookie flags set

### Exception Handling (A10:2025)
- [ ] No bare except with pass
- [ ] Authentication fails closed, not open
- [ ] All exceptions logged
- [ ] Specific exception types caught

### Error Boundaries (Frontend)
- [ ] React components have ErrorBoundary wrappers
- [ ] Vue global error handler configured
- [ ] Angular GlobalErrorHandler implemented
- [ ] Error IDs generated for user support
- [ ] No stack traces exposed to users

### Graceful Degradation
- [ ] Circuit breaker pattern for external services
- [ ] Retry with exponential backoff implemented
- [ ] Feature flags for non-essential features
- [ ] Fallback responses for degraded mode
- [ ] Health checks for dependency monitoring

### Error Logging
- [ ] Structured logging (JSON format)
- [ ] Trace ID correlation across services
- [ ] PII sanitization in logs (email, phone, SSN, CC)
- [ ] Sensitive fields masked (password, token, api_key)
- [ ] Different messages for logs vs user responses
- [ ] No raw error messages exposed to users

---

