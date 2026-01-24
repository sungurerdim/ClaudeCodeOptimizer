# Safety Rules
*Non-negotiable standards - violations require immediate fix*

## Non-Negotiable Standards [CRITICAL]

These are NEVER acceptable, regardless of context. Trigger CRITICAL severity automatically:

| # | Standard | Violation | Required Action |
|---|----------|-----------|-----------------|
| 1 | **No Silent Failures** | Error without logging AND user feedback | Add logging + user message |
| 2 | **No Broad Catches** | `except:` or `catch (e)` without specific types | Catch specific exception types |
| 3 | **No Hidden Fallbacks** | Fallback behavior without explicit justification | Document or remove fallback |
| 4 | **No Hardcoded Secrets** | API keys, passwords, tokens in source | Move to env vars or vault |
| 5 | **No Unvalidated Input** | External data used without sanitization | Add input validation |
| 6 | **No Empty Handlers** | Empty catch/except blocks | Add handling or propagate |
| 7 | **No Mocks in Production** | Test doubles in non-test code | Remove or guard with test flag |

**Enforcement:** Finding any of these = CRITICAL severity, confidence 100, must fix before proceeding.

## Security Priority

- **Security-Priority**: Security rules are non-negotiable. Prioritize security over convenience and speed
- **Block-On-Violation**: Security violation = STOP. Fix before continuing. Warn user explicitly
- **Defense-Assume**: When uncertain about security impact, assume the worst and protect accordingly

## Rule Enforcement

- **Apply-All-Rules**: Every change MUST comply with ALL rules currently in context (global + project-specific)
- **Verify-After-Change**: After EVERY code change, verify compliance before proceeding
- **Fix-Immediately**: Violation detected = stop, fix, re-verify. Fix now, not later ("cleanup later" is not acceptable)
- **Full-Compliance**: Fix all violations before proceeding. 100% compliance required, not "mostly compliant"

## Base Security (OWASP A01-A10)

### Access Control (A01)
- **Access-Control-Enforce**: Deny by default, require explicit grants. Verify permissions server-side on every request
- **Least-Privilege**: Minimum necessary access for users and services
- **SSRF-Prevent**: Validate URLs, block internal IPs (10.x, 172.16.x, 192.168.x, 127.x), use allowlists

### Configuration Security (A02)
- **Safe-Defaults**: Production defaults must be secure: debug off, verbose errors off, restrictive CORS
- **Secrets**: Env vars or vault only, never in code or version control
- **Error-Disclosure**: Show generic error messages to users. Keep stack traces server-side

### Supply Chain Security (A03)
- **Lockfile-Required**: Use dependency lockfile, pin versions, no floating ranges
- **Deps-Audit**: Review dependencies before adding, prefer well-maintained packages

### Input & Output (A04, A05)
- **Input-Boundary**: Validate ALL user input at system entry points. Use schema validation
- **Output-Encode**: Encode output based on context (HTML, URL, JS, CSS)
- **Deserialize-Safe**: Deserialize only trusted data using safe formats (JSON). Never pickle/yaml.load/eval

### Authentication (A07)
- **Session-Security**: Secure + HttpOnly + SameSite=Lax/Strict cookies, token TTL with refresh strategy
- **Password-Security**: Store passwords with bcrypt/argon2/scrypt using appropriate cost factor
- **Auth-Identical-Errors**: Use identical auth failure messages (prevents user enumeration)

### Logging & Monitoring (A09)
- **Audit-Log**: Immutable logging for security-critical actions. Include who, what, when, from-where
- **Redact-Sensitive**: Redact/mask secrets, tokens, credentials, PII in all output

### Error Handling (A10)
- **Error-Graceful**: Handle exceptional conditions gracefully, fail secure (deny access on error)
- **Error-No-Leak**: Never expose internal state, paths, or stack traces to users
- **Fail-Closed**: On security-related errors, default to deny access

### Data Protection
- **Data-Minimization**: Collect and store only necessary data. Each field requires justification
- **Encrypt-Transit**: TLS 1.2+ for all network communication
- **Encrypt-Rest**: AES-256-GCM for sensitive data at rest
- **Timeout-Required**: All external calls must have explicit timeout
