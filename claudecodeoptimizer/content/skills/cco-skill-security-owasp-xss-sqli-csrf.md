---
name: security-owasp-xss-sqli-csrf
description: Prevent OWASP Top 10 vulnerabilities including Broken Access Control (2025 #1), SQL injection, XSS, CSRF, and Exception Handling issues via secure coding patterns and comprehensive validation
keywords: [security, OWASP, broken access control, XSS, SQL injection, CSRF, auth, sanitize, escape, validate, injection, bcrypt, JWT, rate limiting, exception handling, authorization]
category: security
related_commands:
  action_types: [audit, fix, generate]
  categories: [security]
pain_points: [1, 2, 3]
---

# Security - OWASP Top 10, XSS, SQLi, CSRF, Access Control

Prevent OWASP Top 10 2025 vulnerabilities via secure coding patterns and comprehensive validation.

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
        return User.query.get(payload['user_id'])
    except jwt.ExpiredSignatureError as e:
        logger.warning(f"Expired token: {e}")
        abort(401, "Token expired")  # Fail closed
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        abort(401, "Invalid token")  # Fail closed
```

**No Silent Failures:**
```python
# ❌ BAD: Silent failure
try:
    result = critical_security_check()
except:
    pass  # Swallows all errors!

# ✅ GOOD: Explicit handling
try:
    result = critical_security_check()
except SecurityException as e:
    logger.error(f"Security check failed: {e}")
    raise  # Re-raise, don't swallow
except Exception as e:
    logger.critical(f"Unexpected error in security check: {e}")
    raise SecurityException("Security check failed") from e
```

**Detection Pattern:**
```python
def detect_exception_mishandling(code: str) -> List[dict]:
    """Find OWASP A10:2025 violations"""
    issues = []

    # Bare except with pass
    bare_excepts = re.finditer(r'except:\s+pass', code)
    for match in bare_excepts:
        issues.append({
            'type': 'exception_mishandling',
            'subtype': 'silent_failure',
            'severity': 'MEDIUM',
            'owasp': 'A10:2025',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'Silent exception handling (bare except + pass)'
        })

    # Failing open pattern
    failing_open = re.finditer(
        r'except.*?:\s+return\s+(default_|guest_|anonymous_|None)',
        code,
        re.IGNORECASE
    )
    for match in failing_open:
        # Check if in auth context
        func_start = code.rfind('def ', 0, match.start())
        func_end = match.start()
        func_code = code[func_start:func_end]

        if any(keyword in func_code.lower() for keyword in ['auth', 'login', 'verify', 'check']):
            issues.append({
                'type': 'exception_mishandling',
                'subtype': 'failing_open',
                'severity': 'HIGH',
                'owasp': 'A10:2025',
                'line': code[:match.start()].count('\n') + 1,
                'message': 'Authentication fails open on exception (security risk)'
            })

    # No logging in exception handlers
    try_blocks = re.finditer(
        r'try:(.*?)except.*?:(.*?)(?=\n(?:def|class|try|\Z))',
        code,
        re.DOTALL
    )
    for match in try_blocks:
        except_body = match.group(2)
        if 'log' not in except_body.lower() and 'print' not in except_body:
            issues.append({
                'type': 'exception_mishandling',
                'subtype': 'no_logging',
                'severity': 'LOW',
                'owasp': 'A10:2025',
                'line': code[:match.start()].count('\n') + 1,
                'message': 'Exception handler without logging (blind spots)'
            })

    return issues
```

---

## Patterns

### Complete Security Audit

```python
def audit_security(file_path: str) -> dict:
    """Comprehensive OWASP Top 10 2025 security audit"""
    with open(file_path) as f:
        code = f.read()

    return {
        'broken_access_control': detect_missing_access_control(code),  # A01
        'sql_injection': detect_sql_injection(code),  # A03
        'xss': detect_xss(code),  # A07
        'csrf': detect_csrf_issues(code),  # Included in A01
        'auth_issues': detect_auth_issues(code),  # A07
        'exception_handling': detect_exception_mishandling(code),  # A10
        'overall_score': calculate_security_score(code)
    }

def calculate_security_score(code: str) -> dict:
    """Security score: 0-100"""
    all_issues = []
    all_issues.extend(detect_missing_access_control(code))
    all_issues.extend(detect_sql_injection(code))
    all_issues.extend(detect_xss(code))
    all_issues.extend(detect_exception_mishandling(code))

    # Weight by severity
    critical = len([i for i in all_issues if i['severity'] == 'CRITICAL'])
    high = len([i for i in all_issues if i['severity'] == 'HIGH'])
    medium = len([i for i in all_issues if i['severity'] == 'MEDIUM'])
    low = len([i for i in all_issues if i['severity'] == 'LOW'])

    # Deduct points
    score = 100
    score -= critical * 25  # -25 per critical
    score -= high * 10      # -10 per high
    score -= medium * 5     # -5 per medium
    score -= low * 2        # -2 per low

    score = max(0, score)

    return {
        'score': score,
        'grade': (
            'A' if score >= 90 else
            'B' if score >= 75 else
            'C' if score >= 60 else
            'D' if score >= 40 else
            'F'
        ),
        'critical_issues': critical,
        'high_issues': high,
        'medium_issues': medium,
        'low_issues': low
    }
```

---

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

---

## AI-Specific Auth Bypass Patterns

AI-generated code frequently contains these auth vulnerabilities:

### Pattern 1: Tutorial Code Without Auth
```python
# ❌ AI copies tutorial code that skips auth
@app.route('/api/users')
def list_users():
    # AI-generated from tutorial - NO AUTH!
    return jsonify([u.to_dict() for u in User.query.all()])

# ✅ Add authentication wrapper
@app.route('/api/users')
@require_auth
@require_role('admin')
def list_users():
    return jsonify([u.to_dict() for u in User.query.all()])
```

### Pattern 2: AI Suggests "Quick Fix" That Bypasses
```python
# ❌ AI suggests env variable to "debug"
if os.getenv('SKIP_AUTH') == 'true':
    return get_data()  # Bypass in production!

# ✅ Proper environment-based auth
if os.getenv('ENV') == 'development' and ALLOW_DEV_BYPASS:
    logger.warning("DEV MODE: Auth bypassed")
    # Only in local dev, never production
```

### Pattern 3: AI Placeholder Comments
```python
# ❌ AI leaves TODO that gets deployed
@app.route('/api/admin/reset-password')
def reset_password(user_id):
    # TODO: Add authentication check
    user = User.query.get(user_id)
    user.password = generate_password()

# ✅ Fail secure with placeholder
@app.route('/api/admin/reset-password')
@require_auth
@require_role('admin')
def reset_password(user_id):
    user = User.query.get(user_id)
    user.password = generate_password()
```

### Detection: AI Auth Skip Signatures
```python
def detect_ai_auth_skips(code: str) -> List[dict]:
    """Detect AI-generated authentication bypasses"""
    issues = []

    # Pattern: Environment variable auth bypass
    env_bypass = re.finditer(
        r'if.*?getenv.*?(SKIP|BYPASS|DISABLE).*?AUTH',
        code,
        re.IGNORECASE
    )
    for match in env_bypass:
        issues.append({
            'type': 'ai_auth_bypass',
            'subtype': 'env_variable_bypass',
            'severity': 'CRITICAL',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'AI-generated environment variable auth bypass',
            'signature': 'ChatGPT/Copilot debugging pattern'
        })

    # Pattern: TODO comments in auth code
    auth_todos = re.finditer(
        r'(#|//).*?TODO.*?(auth|permission|access|check)',
        code,
        re.IGNORECASE
    )
    for match in auth_todos:
        # Check if in route/endpoint
        if '@app.route' in code[max(0, match.start()-500):match.start()]:
            issues.append({
                'type': 'ai_auth_bypass',
                'subtype': 'todo_placeholder',
                'severity': 'HIGH',
                'line': code[:match.start()].count('\n') + 1,
                'message': 'TODO auth check in deployed endpoint (AI placeholder)',
                'signature': 'AI tutorial pattern'
            })

    return issues
```

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for security domain
action_types: [audit, fix, generate]
keywords: [security, OWASP, broken access control, injection, XSS, CSRF, auth]
category: security
pain_points: [1, 2, 3]  # AI Tech Debt, AI Quality, Security
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: security`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.

---

## References

- [OWASP Top 10 2025](https://owasp.org/www-project-top-10/)
- [OWASP A01:2025 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [OWASP A03:2025 Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [OWASP A07:2025 XSS](https://owasp.org/Top10/A07_2021-Cross-site_Scripting_(XSS)/)
- [OWASP A10:2025 Exception Handling](https://owasp.org/)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
