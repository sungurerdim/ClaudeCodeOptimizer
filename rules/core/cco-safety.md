# Safety Rules
*Non-negotiable standards - violations = CRITICAL severity*

## Non-Negotiable Standards [CRITICAL]

| # | Violation | Required Action |
|---|-----------|-----------------|
| 1 | Error without logging AND user feedback | Add logging + user message |
| 2 | `except:` or `catch (e)` without specific types | Catch specific exceptions |
| 3 | Fallback without explicit justification | Document or remove |
| 4 | API keys, passwords, tokens in source | Move to env vars/vault |
| 5 | External data used without sanitization | Add input validation |
| 6 | Empty catch/except blocks | Add handling or propagate |
| 7 | Test doubles in non-test code | Remove or guard with test flag |

**Finding any = CRITICAL severity, confidence 100, must fix before proceeding.**

## Enforcement [CRITICAL]

- **Block-On-Violation**: Security violation = STOP. Fix before continuing
- **Fix-Immediately**: Violation detected = stop, fix, re-verify
- **Full-Compliance**: 100% required, not "mostly compliant"

## Specific Security Values

| What | Safe | Unsafe |
|------|------|--------|
| Deserialize | `json.loads()` | `pickle.load()`, `yaml.load()`, `eval()` |
| Passwords | bcrypt, argon2, scrypt | MD5, SHA1, plaintext |
| Transit | TLS 1.2+ | HTTP, TLS 1.0/1.1 |
| Rest | AES-256-GCM | DES, 3DES, ECB mode |

## SSRF Prevention

Block internal IPs: `10.x`, `172.16.x`, `192.168.x`, `127.x`, `169.254.x`, `::1`, `fc00::`
