# Safety Rules
*BLOCKER violations - must fix before proceeding*

## Security Violations [BLOCKER]

Finding ANY = STOP immediately. Fix before continuing.

| # | Pattern | Required Fix |
|---|---------|--------------|
| 1 | API keys, passwords, tokens in source | Move to env vars |
| 2 | `except:` / `catch (e)` without specific types | Catch specific exceptions |
| 3 | Empty catch/except blocks | Add handling or propagate |
| 4 | External data used without sanitization | Add input validation |
| 5 | `eval()`, `pickle.load()`, `yaml.load()` | Use safe alternatives |

## Security Lookup [CHECK]

| Category | Safe | Unsafe |
|----------|------|--------|
| Deserialize | `json.loads()` | `pickle.load()`, `eval()`, `yaml.load()` |
| Passwords | bcrypt, argon2, scrypt | MD5, SHA1, plaintext |
| Transit | TLS 1.2+ | HTTP, TLS 1.0/1.1 |
| Encryption | AES-256-GCM | DES, 3DES, ECB mode |
| Internal IPs | Block all | `10.x`, `172.16.x`, `192.168.x`, `127.x`, `::1` |

## Enforcement

```
Violation detected?
├── YES → STOP. Fix. Verify fix. Then continue.
└── NO → Proceed.
```

100% compliance required. "Mostly secure" = not secure.
