# Security Rules
*Secure code patterns aligned with OWASP Top 10:2025 and CWE/SANS Top 25*

**Trigger:** D:PII | D:Regulated | Scale:Large | Compliance:*

## Access Control

- **Access-Deny-Default**: Check permissions server-side on every request. Return 403 if denied
- **Auth-Verify**: Verify authentication token/session on every protected endpoint
- **Path-Validate**: Validate file paths: `os.path.realpath()` to resolve, reject if outside allowed directory
- **SSRF-Prevent**: Validate URLs before fetching. Block internal IPs: `10.x`, `172.16.x`, `192.168.x`, `127.x`, `169.254.x`, `::1`, `fc00::`

## Input Validation

- **Input-Validate**: Validate ALL user input with schema validation. Reject invalid, don't sanitize-and-continue
- **Input-Bounds**: Set `max_length`, `max_items`, `ge/le` bounds on all input fields
- **Input-Whitespace**: Strip whitespace, reject whitespace-only strings
- **Enum-Validate**: Validate enum values server-side: `if value not in ValidEnum: raise ValueError`

## Injection Prevention

- **SQL-Parameterized**: Use parameterized queries: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
- **Command-Safe**: Use list args, never shell=True: `subprocess.run(["ls", "-la", path], shell=False)`
- **XSS-Encode**: Encode output by context. Use framework auto-escaping in templates
- **Deserialize-Safe**: Use `json.loads()` only. Never `pickle.load()`, `yaml.load()`, or `eval()`

### CWE/SANS Detection Patterns

| CWE | Pattern | Detection |
|-----|---------|-----------|
| CWE-79 | XSS | `.innerHTML=`, `v-html`, `dangerouslySetInnerHTML`, f-string in templates |
| CWE-89 | SQL Injection | String concat/format in SQL queries |
| CWE-78 | Command Injection | `subprocess.run(..., shell=True)`, `os.system()` |
| CWE-94 | Code Injection | `eval()`, `exec()` with user input |
| CWE-502 | Deserialization | `pickle.load()`, `yaml.load()` without SafeLoader |
| CWE-798 | Hardcoded Credentials | Inline API keys, passwords, secrets in source |

---

## Cryptography

- **Crypto-Approved**: Use AES-256-GCM, RSA-2048+, Ed25519. Never implement custom crypto
- **Timing-Safe**: Use `secrets.compare_digest()` or `crypto.timingSafeEqual()` for secret comparison
- **Random-Secure**: Use `secrets.token_bytes()` or `crypto.randomBytes()` for security-sensitive randomness

### Password Hashing Parameters

**Argon2id** (Preferred):
```
memory (m): 19456 KiB (19 MiB minimum)
iterations (t): 2 minimum
parallelism (p): 1
```

**bcrypt** (Acceptable):
```
cost factor: 12 minimum (2025 standard)
password limit: 72 bytes (pre-hash with SHA-256 if longer)
```

**PBKDF2** (FIPS compliance only):
```
iterations: 600,000 minimum with HMAC-SHA256
salt: 16 bytes minimum
```

---

## Authentication

### Account Lockout Strategy

**Track failures per account**, not per IP (prevents legitimate user abuse):

| Attempt | Delay | Action |
|---------|-------|--------|
| 1-3 | None | Allow |
| 4 | 1s | Start backoff |
| 5 | 2s | Warning |
| 6 | 4s | Notify user |
| 7+ | 8s...3600s | Exponential cap at 1 hour |

**Formula**: `delay = min(3600, 2^(attempts-3))` seconds

**Reset**: After 24 hours of no attempts OR successful login with MFA

### JWT/Token Security

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Access Token TTL | 5-15 min | Short-lived access |
| Refresh Token TTL | 7-30 days | Long-lived refresh |
| Signing Algorithm | RS256/ES256 | Asymmetric for public APIs |
| Storage | HttpOnly cookie | NOT localStorage |

**Required Claims**:
- `iss`: Issuer identifier
- `aud`: Audience (API identifier)
- `exp`: Expiration timestamp
- `iat`: Issued-at timestamp
- `jti`: Unique token ID (for revocation)
- `sub`: Subject (user identifier)

**Key Management**:
- Include `kid` header for key rotation
- Rotate signing keys every 90 days
- Keep previous key valid for token lifetime after rotation

### MFA Requirements

| Method | Security Level | Use Case |
|--------|----------------|----------|
| FIDO2/Passkeys | Highest | Preferred (phishing-resistant) |
| TOTP | High | Standard (offline-capable) |
| SMS | Low | Backup only (SIM swap risk) |

**Required for**:
- Password changes
- Email changes
- New device login
- Sensitive operations (payment, admin)

**Password policy**:
- 8+ characters WITH MFA enabled
- 15+ characters WITHOUT MFA
- Check against breached password databases

### Session Security

**Cookie Configuration**:
```
Set-Cookie: session=xxx; Secure; HttpOnly; SameSite=Strict; Path=/; __Host-
```

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Session ID entropy | 128+ bits | Prevent brute force |
| Idle timeout | 15-30 min | Standard apps |
| Idle timeout | 2-5 min | High-security (banking) |
| Absolute timeout | 8-24 hours | Force re-auth |

**Regenerate session on**:
- Login
- Privilege escalation
- Sensitive operations

**Use `__Host-` prefix** for sensitive cookies (enforces Secure + Path=/ + no Domain)

### Rate Limiting for Auth Endpoints

| Endpoint | Per IP/Min | Per IP/Hour | Per Account/Hour |
|----------|------------|-------------|------------------|
| Login | 5 | 20 | 10 |
| Password Reset | 3 | 6 | 3 |
| MFA Verify | 5 | 15 | 10 |
| Token Refresh | 30 | 120 | 60 |

**Response**: 429 with `Retry-After` header

---

## Error Handling

- **Error-Generic**: Return generic messages to users: `"Authentication failed"` not `"User not found"`
- **Error-No-Leak**: Never expose stack traces, file paths, or SQL errors in API responses
- **Fail-Secure**: On security errors, deny access: `return 403` not silent continue
- **Error-Identical**: Use identical error messages for auth failures (prevents user enumeration)

## Logging

- **Log-Redact**: Never log passwords, tokens, or PII. Mask sensitive data: `"token": "***"`
- **Audit-Log**: Log security events: login, logout, permission changes, failed auth attempts
- **Log-Correlation**: Include request_id/trace_id in all security logs
