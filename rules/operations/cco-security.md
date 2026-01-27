# Security Rules
*Specific parameters and detection patterns*

**Trigger:** D:PII | D:Regulated | Compliance:*

## CWE Detection Patterns [CRITICAL]

| CWE | Pattern | Detection |
|-----|---------|-----------|
| CWE-79 | XSS | `.innerHTML=`, `v-html`, `dangerouslySetInnerHTML` |
| CWE-89 | SQL Injection | String concat/format in queries |
| CWE-78 | Command Injection | `shell=True`, `os.system()` |
| CWE-94 | Code Injection | `eval()`, `exec()` with user input |
| CWE-502 | Deserialization | `pickle.load()`, `yaml.load()` |
| CWE-798 | Hardcoded Credentials | Inline secrets in source |

## SSRF Block List

Block internal IPs: `10.x`, `172.16.x`, `192.168.x`, `127.x`, `169.254.x`, `::1`, `fc00::`

---

## Password Hashing Parameters

### Argon2id (Preferred)
```
memory: 19456 KiB (19 MiB minimum)
iterations: 2 minimum
parallelism: 1
```

### bcrypt (Acceptable)
```
cost: 12 minimum
password limit: 72 bytes (pre-hash longer)
```

### PBKDF2 (FIPS only)
```
iterations: 600,000 minimum (HMAC-SHA256)
salt: 16 bytes minimum
```

---

## Authentication Parameters

### Account Lockout

| Attempt | Delay |
|---------|-------|
| 1-3 | None |
| 4+ | `min(3600, 2^(attempts-3))` seconds |

Reset: 24h no attempts OR successful MFA login

### JWT/Token

| Parameter | Value |
|-----------|-------|
| Access Token TTL | 5-15 min |
| Refresh Token TTL | 7-30 days |
| Algorithm | RS256/ES256 |
| Storage | HttpOnly cookie |
| Key Rotation | 90 days |

### Session

| Parameter | Value |
|-----------|-------|
| ID Entropy | 128+ bits |
| Idle Timeout | 15-30 min (standard) |
| Idle Timeout | 2-5 min (high-security) |
| Absolute Timeout | 8-24 hours |

Cookie: `Secure; HttpOnly; SameSite=Strict; __Host-` prefix

### MFA Priority

| Method | Security | Use |
|--------|----------|-----|
| FIDO2/Passkeys | Highest | Preferred |
| TOTP | High | Standard |
| SMS | Low | Backup only |

---

## Rate Limits (Auth Endpoints)

| Endpoint | Per IP/Min | Per Account/Hour |
|----------|------------|------------------|
| Login | 5 | 10 |
| Password Reset | 3 | 3 |
| MFA Verify | 5 | 10 |
| Token Refresh | 30 | 60 |
