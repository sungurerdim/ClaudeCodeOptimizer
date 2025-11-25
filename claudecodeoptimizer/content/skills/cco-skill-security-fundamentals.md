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

### 7. Error Boundaries (Frontend Security)

**React Error Boundaries:**
```jsx
// ✅ GOOD: Error boundary prevents cascade
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, errorId: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log to error tracking service
    const errorId = crypto.randomUUID();
    this.setState({ errorId });

    // ✅ GOOD: Structured error logging
    errorService.log({
      id: errorId,
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString(),
      userId: getCurrentUserId(),  // No PII in error logs!
      url: window.location.pathname
    });
  }

  render() {
    if (this.state.hasError) {
      // ✅ GOOD: Generic error message (no stack traces to user)
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>Error ID: {this.state.errorId}</p>
          <p>Please refresh or contact support with this ID.</p>
          <button onClick={() => window.location.reload()}>
            Refresh Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage: Wrap critical sections
<ErrorBoundary>
  <PaymentForm />  {/* Errors contained here */}
</ErrorBoundary>
```

**Vue Error Handling:**
```javascript
// ✅ GOOD: Global Vue error handler
app.config.errorHandler = (err, vm, info) => {
  const errorId = crypto.randomUUID();

  // Log structured error
  errorService.log({
    id: errorId,
    error: err.message,
    stack: err.stack,
    component: vm?.$options?.name || 'Unknown',
    info: info,  // Lifecycle hook where error occurred
    timestamp: new Date().toISOString()
  });

  // Show user-friendly notification
  vm.$notify({
    type: 'error',
    title: 'An error occurred',
    message: `Error ID: ${errorId}. Please try again.`
  });
};

// ❌ BAD: Exposing error details
app.config.errorHandler = (err) => {
  alert(err.stack);  // NEVER expose stack traces!
};
```

**Angular Error Handler:**
```typescript
// ✅ GOOD: Global Angular error handler
@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private errorService: ErrorService) {}

  handleError(error: Error): void {
    const errorId = crypto.randomUUID();

    // Distinguish client vs server errors
    if (error instanceof HttpErrorResponse) {
      // Server error
      this.errorService.logServerError({
        id: errorId,
        status: error.status,
        message: error.message,
        url: error.url
      });
    } else {
      // Client error
      this.errorService.logClientError({
        id: errorId,
        name: error.name,
        message: error.message,
        stack: error.stack
      });
    }

    // Show generic message
    this.notificationService.error(`Error ID: ${errorId}`);
  }
}

// Register in module
@NgModule({
  providers: [
    { provide: ErrorHandler, useClass: GlobalErrorHandler }
  ]
})
```

---

### 8. Graceful Degradation Patterns

**Circuit Breaker Pattern:**
```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreaker:
    """Prevents cascade failures with graceful degradation."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        fallback: Callable = None
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = timedelta(seconds=recovery_timeout)
        self.fallback = fallback

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""

        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker: HALF_OPEN, testing recovery")
            else:
                logger.warning("Circuit breaker: OPEN, using fallback")
                return self._execute_fallback(*args, **kwargs)

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure(e)
            return self._execute_fallback(*args, **kwargs)

    def _should_attempt_reset(self) -> bool:
        return (
            self.last_failure_time and
            datetime.now() - self.last_failure_time >= self.recovery_timeout
        )

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self, error: Exception):
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        logger.error(f"Circuit breaker: failure #{self.failure_count}: {error}")

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.critical(
                f"Circuit breaker: OPEN after {self.failure_count} failures"
            )

    def _execute_fallback(self, *args, **kwargs) -> Any:
        if self.fallback:
            return self.fallback(*args, **kwargs)
        raise CircuitOpenError("Service unavailable, please retry later")


# ✅ GOOD: Usage with fallback
def get_cached_user(user_id: int):
    """Fallback: return cached data."""
    return cache.get(f"user:{user_id}") or {"id": user_id, "status": "unknown"}

user_service = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=60,
    fallback=get_cached_user
)

def get_user(user_id: int):
    return user_service.call(database.get_user, user_id)
```

**Retry with Exponential Backoff:**
```python
import time
import random
from functools import wraps
from typing import Tuple, Type
import logging

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retry with exponential backoff.

    ✅ GOOD: Prevents thundering herd with jitter
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(
                            f"All {max_retries} retries failed for {func.__name__}: {e}"
                        )
                        raise

                    # Exponential backoff with jitter
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )
                    jitter = random.uniform(0, delay * 0.1)  # 10% jitter
                    sleep_time = delay + jitter

                    logger.warning(
                        f"Retry {attempt + 1}/{max_retries} for {func.__name__} "
                        f"after {sleep_time:.2f}s: {e}"
                    )
                    time.sleep(sleep_time)

            raise last_exception

        return wrapper
    return decorator


# ✅ GOOD: Usage
@retry_with_backoff(
    max_retries=3,
    base_delay=1.0,
    retryable_exceptions=(ConnectionError, TimeoutError)
)
def call_external_api(endpoint: str):
    response = requests.get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()
```

**Feature Degradation:**
```python
class FeatureFlags:
    """Graceful feature degradation based on system health."""

    def __init__(self):
        self.health_checks = {}
        self.degradation_levels = {
            "healthy": 0,
            "degraded": 1,
            "critical": 2
        }

    def check_feature(self, feature: str, fallback: Callable = None):
        """
        Check if feature is available, use fallback if degraded.

        ✅ GOOD: Transparent degradation
        """
        health = self.get_system_health()

        if health == "critical":
            logger.warning(f"Feature {feature}: DISABLED (critical)")
            if fallback:
                return fallback()
            return None

        if health == "degraded" and self.is_non_essential(feature):
            logger.info(f"Feature {feature}: DEGRADED mode")
            if fallback:
                return fallback()
            return None

        return True  # Feature available

    def get_system_health(self) -> str:
        """Check overall system health."""
        failing_services = sum(
            1 for check in self.health_checks.values()
            if not check()
        )

        if failing_services >= 3:
            return "critical"
        if failing_services >= 1:
            return "degraded"
        return "healthy"


# ✅ GOOD: Usage in route
@app.route('/api/recommendations')
def get_recommendations(user_id: int):
    # Non-essential feature - degrade gracefully
    if not features.check_feature(
        'recommendations',
        fallback=lambda: get_popular_items()
    ):
        return jsonify(get_popular_items())

    return jsonify(recommendation_service.get_for_user(user_id))
```

---

### 9. Error Logging Best Practices

**Structured Logging:**
```python
import logging
import json
from datetime import datetime
from typing import Any, Optional
import traceback


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }

        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in (
                'name', 'msg', 'args', 'created', 'filename',
                'funcName', 'levelname', 'levelno', 'lineno',
                'module', 'msecs', 'pathname', 'process',
                'processName', 'relativeCreated', 'stack_info',
                'thread', 'threadName', 'exc_info', 'exc_text',
                'message'
            ):
                log_data[key] = value

        return json.dumps(log_data)


# ✅ GOOD: Configure structured logging
def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter())

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


# ✅ GOOD: Usage with context
logger = logging.getLogger(__name__)

def process_order(order_id: str, user_id: str):
    logger.info(
        "Processing order",
        extra={
            "order_id": order_id,
            "user_id": user_id,  # Anonymize if PII concerns
            "action": "order_process_start"
        }
    )

    try:
        result = order_service.process(order_id)
        logger.info(
            "Order processed successfully",
            extra={
                "order_id": order_id,
                "action": "order_process_success",
                "total": result.total
            }
        )
        return result
    except PaymentError as e:
        logger.error(
            "Payment failed",
            extra={
                "order_id": order_id,
                "action": "order_process_failed",
                "error_type": "payment",
                "error_code": e.code
            },
            exc_info=True
        )
        raise
```

**Error Correlation (Distributed Tracing):**
```python
import uuid
from contextvars import ContextVar
from functools import wraps

# Context variable for request tracing
trace_id_var: ContextVar[str] = ContextVar('trace_id', default=None)
span_id_var: ContextVar[str] = ContextVar('span_id', default=None)


class TraceContext:
    """Distributed tracing context for error correlation."""

    @staticmethod
    def new_trace():
        trace_id_var.set(str(uuid.uuid4()))
        span_id_var.set(str(uuid.uuid4())[:8])

    @staticmethod
    def get_trace_id() -> Optional[str]:
        return trace_id_var.get()

    @staticmethod
    def get_span_id() -> Optional[str]:
        return span_id_var.get()


# ✅ GOOD: Middleware for trace propagation
@app.before_request
def start_trace():
    # Check for incoming trace header
    trace_id = request.headers.get('X-Trace-ID')
    if trace_id:
        trace_id_var.set(trace_id)
    else:
        TraceContext.new_trace()

    # Add to response headers
    g.trace_id = TraceContext.get_trace_id()


@app.after_request
def add_trace_header(response):
    response.headers['X-Trace-ID'] = g.trace_id
    return response


# ✅ GOOD: Correlated logging
def log_with_trace(level: str, message: str, **extra):
    """Log with automatic trace correlation."""
    extra['trace_id'] = TraceContext.get_trace_id()
    extra['span_id'] = TraceContext.get_span_id()

    getattr(logger, level)(message, extra=extra)


# Usage
def call_payment_service(order_id: str):
    log_with_trace("info", "Calling payment service", order_id=order_id)

    try:
        # Pass trace to downstream service
        response = requests.post(
            PAYMENT_URL,
            json={"order_id": order_id},
            headers={"X-Trace-ID": TraceContext.get_trace_id()}
        )
        return response.json()
    except Exception as e:
        log_with_trace(
            "error",
            "Payment service call failed",
            order_id=order_id,
            error=str(e)
        )
        raise
```

**Security-Safe Error Messages:**
```python
class SecureErrorHandler:
    """
    Error handler that prevents information leakage.

    ✅ GOOD: Different messages for logs vs users
    """

    # Map internal errors to user-safe messages
    ERROR_MESSAGES = {
        "DatabaseError": "A database error occurred. Please try again.",
        "AuthenticationError": "Invalid credentials.",
        "AuthorizationError": "You don't have permission for this action.",
        "ValidationError": "Invalid input data.",
        "RateLimitError": "Too many requests. Please wait and try again.",
        "ServiceUnavailable": "Service temporarily unavailable."
    }

    @staticmethod
    def handle(error: Exception, context: dict = None) -> dict:
        error_id = str(uuid.uuid4())
        error_type = type(error).__name__

        # ✅ GOOD: Full details in logs
        logger.error(
            f"Error {error_id}: {error_type}",
            extra={
                "error_id": error_id,
                "error_type": error_type,
                "error_message": str(error),
                "context": context or {},
                "traceback": traceback.format_exc()
            }
        )

        # ✅ GOOD: Safe message for user
        user_message = SecureErrorHandler.ERROR_MESSAGES.get(
            error_type,
            "An unexpected error occurred."
        )

        return {
            "error": {
                "id": error_id,
                "message": user_message
            }
        }


# ✅ GOOD: Usage in Flask
@app.errorhandler(Exception)
def handle_exception(error):
    response = SecureErrorHandler.handle(error, {
        "path": request.path,
        "method": request.method
    })

    # Determine status code
    if isinstance(error, ValidationError):
        status = 400
    elif isinstance(error, AuthenticationError):
        status = 401
    elif isinstance(error, AuthorizationError):
        status = 403
    elif isinstance(error, NotFoundError):
        status = 404
    else:
        status = 500

    return jsonify(response), status
```

**PII Protection in Logs:**
```python
import re
from typing import Any


class PIISanitizer:
    """Remove or mask PII from log data."""

    PATTERNS = {
        'email': (
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            '[EMAIL_REDACTED]'
        ),
        'phone': (
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            '[PHONE_REDACTED]'
        ),
        'ssn': (
            r'\b\d{3}-\d{2}-\d{4}\b',
            '[SSN_REDACTED]'
        ),
        'credit_card': (
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            '[CC_REDACTED]'
        ),
        'ip_address': (
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            '[IP_REDACTED]'
        ),
        'jwt': (
            r'eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+',
            '[JWT_REDACTED]'
        )
    }

    # Fields to always mask
    SENSITIVE_FIELDS = {
        'password', 'secret', 'token', 'api_key', 'apikey',
        'authorization', 'auth', 'credential', 'private_key'
    }

    @classmethod
    def sanitize(cls, data: Any) -> Any:
        """Recursively sanitize data structure."""
        if isinstance(data, dict):
            return {
                k: cls._sanitize_field(k, v)
                for k, v in data.items()
            }
        if isinstance(data, list):
            return [cls.sanitize(item) for item in data]
        if isinstance(data, str):
            return cls._sanitize_string(data)
        return data

    @classmethod
    def _sanitize_field(cls, key: str, value: Any) -> Any:
        """Sanitize based on field name."""
        key_lower = key.lower()

        # Mask sensitive fields entirely
        if any(sf in key_lower for sf in cls.SENSITIVE_FIELDS):
            return '[REDACTED]'

        return cls.sanitize(value)

    @classmethod
    def _sanitize_string(cls, text: str) -> str:
        """Apply PII patterns to string."""
        for pattern, replacement in cls.PATTERNS.values():
            text = re.sub(pattern, replacement, text)
        return text


# ✅ GOOD: Usage in logging
class SanitizedFormatter(StructuredFormatter):
    def format(self, record: logging.LogRecord) -> str:
        # Sanitize extra fields
        for key in list(record.__dict__.keys()):
            if key not in self._builtin_keys:
                record.__dict__[key] = PIISanitizer.sanitize(
                    record.__dict__[key]
                )

        return super().format(record)
```

**Detection Pattern for Error Handling Issues:**
```python
def detect_error_handling_issues(code: str) -> List[dict]:
    """Comprehensive error handling security audit."""
    issues = []

    # Pattern 1: Stack trace exposure
    stack_exposure = re.finditer(
        r'(return|send|render|jsonify).*?(traceback|stack|exc_info|format_exc)',
        code,
        re.IGNORECASE
    )
    for match in stack_exposure:
        issues.append({
            'type': 'error_handling',
            'subtype': 'stack_trace_exposure',
            'severity': 'HIGH',
            'owasp': 'A10:2025',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'Stack trace potentially exposed to user'
        })

    # Pattern 2: Generic error messages with details
    error_detail = re.finditer(
        r'(return|Response).*?(error|exception).*?str\(.*?\)',
        code,
        re.IGNORECASE
    )
    for match in error_detail:
        issues.append({
            'type': 'error_handling',
            'subtype': 'error_detail_leak',
            'severity': 'MEDIUM',
            'owasp': 'A10:2025',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'Raw error message may leak sensitive details'
        })

    # Pattern 3: No error handler configured
    if '@app.errorhandler' not in code and 'app = Flask' in code:
        issues.append({
            'type': 'error_handling',
            'subtype': 'no_global_handler',
            'severity': 'MEDIUM',
            'owasp': 'A10:2025',
            'message': 'No global error handler configured (default may leak info)'
        })

    # Pattern 4: Logging PII
    pii_logging = re.finditer(
        r'log.*?\.(info|debug|error|warning).*?(email|password|ssn|credit|phone)',
        code,
        re.IGNORECASE
    )
    for match in pii_logging:
        issues.append({
            'type': 'error_handling',
            'subtype': 'pii_in_logs',
            'severity': 'HIGH',
            'owasp': 'A10:2025',
            'line': code[:match.start()].count('\n') + 1,
            'message': 'Potential PII logged without sanitization'
        })

    # Pattern 5: No error boundary in React
    if 'React' in code or 'react' in code:
        if 'componentDidCatch' not in code and 'ErrorBoundary' not in code:
            issues.append({
                'type': 'error_handling',
                'subtype': 'no_error_boundary',
                'severity': 'LOW',
                'owasp': 'A10:2025',
                'message': 'React component without error boundary'
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

---

## References

- [OWASP Top 10 2025](https://owasp.org/www-project-top-10/)
- [OWASP A01:2025 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [OWASP A03:2025 Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [OWASP A07:2025 XSS](https://owasp.org/Top10/A07_2021-Cross-site_Scripting_(XSS)/)
- [OWASP A10:2025 Exception Handling](https://owasp.org/)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
