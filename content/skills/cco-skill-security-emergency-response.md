---
title: Security Emergency Response Skill
category: security
description: Immediate P0 CRITICAL security remediation
metadata:
  name: "Security Emergency Response"
  activation_keywords: ["P0 critical", "hardcoded secrets", "exposed keys", "security emergency"]
  category: "security"
  priority: high
principles: ['U_FAIL_FAST', 'P_SECRET_ROTATION', 'P_AUDIT_LOGGING', 'P_AUTH_AUTHZ', 'P_SUPPLY_CHAIN_SECURITY', 'P_ZERO_DISK_TOUCH']
use_cases:
  security_stance: [production, high]
  project_maturity: [active-dev, production, legacy]
---

# Security Emergency Response

Stop everything when P0 CRITICAL security issue detected. Fix immediately before continuing.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

### When This Skill Activates

This skill activates IMMEDIATELY upon detecting P0 CRITICAL security issues:
- Hardcoded API keys, passwords, tokens
- Exposed private keys, certificates
- Database credentials in code
- JWT secrets in source control

**Trigger:** ANY P0 CRITICAL security violation detected

**Behavior:** INTERRUPT current operation, demand immediate fix

### The Core Principle

**P0 CRITICAL security issues are deployment blockers. Fix NOW, not later.**

Why?
- Exposed secrets can be exploited within minutes
- Once in git history, secrets are compromised forever
- Every second counts

### Severity Classification

#### P0 CRITICAL (Emergency Response)
**Stop everything. Fix immediately.**

Examples:
- `API_KEY = "sk_live_51H7K9..."` (production API key)
- `PASSWORD = "admin123"` (database password)
- `JWT_SECRET = "my-secret-key"` (auth secret)
- Private keys in `.pem` files committed to git
- `.env` file with real secrets in git history

**Response time:** IMMEDIATE (within 5 minutes)
**Block:** YES (don't continue audit until fixed)

#### P1 HIGH (Urgent, Not Emergency)
**Fix today, but can finish current audit first.**

Examples:
- Missing rate limiting on API endpoints
- Cache without TTL (memory leak risk)
- SQL queries with string concatenation (injection risk)
- Missing HTTPS redirect

**Response time:** Within 1 hour
**Block:** NO (fix after completing audit)

#### P2 MEDIUM, P3 LOW
**Fix in normal workflow.**

### Emergency Response Protocol

#### Phase 1: DETECT & INTERRUPT

When P0 CRITICAL detected:

```
EMERGENCY: P0 CRITICAL SECURITY VIOLATION DETECTED

services/api/client.py:23
  API_KEY = "sk_live_51H7K9..."

This appears to be a REAL production API key.

AUDIT PAUSED. Fix this immediately before continuing.
```

#### Phase 2: CONFIRM Severity

Ask user to confirm:

```
Is this a REAL secret or a test/example value?

1. REAL - This is a production secret (EMERGENCY)
2. EXAMPLE - This is a placeholder like "your-api-key-here"
3. TEST - This is a test fixture like "test_key_123"

Choice (1/2/3):
```

If REAL → Continue emergency response
If EXAMPLE/TEST → Downgrade to P2, add comment, continue audit

#### Phase 3: REVOKE Secret

```
IMMEDIATE ACTION REQUIRED:

1. Revoke this key at your API provider
   Provider detected: Stripe
   Revocation URL: https://dashboard.stripe.com/apikeys

Open revocation page? (y/n)
```

If yes → Open browser to revocation URL

```
Waiting for confirmation...

Have you revoked the old key? (y/n)
```

If no → Refuse to continue

```
This key is LIVE in production. Cannot continue until revoked.
Please revoke at: https://dashboard.stripe.com/apikeys

Type "revoked" when complete:
```

#### Phase 4: GENERATE New Secret

```
Generating replacement secret...

Option 1: Generate new key at provider
Option 2: Use environment variable placeholder

Recommended: Option 2 (environment variable)
Choice (1/2):
```

If Option 2 (recommended):

```
Creating fix:
1. Replace hardcoded key with os.getenv("STRIPE_API_KEY")
2. Create .env.example with placeholder
3. Add .env to .gitignore
4. Document in README.md

Apply fix? (y/n)
```

#### Phase 5: APPLY Fix

```
Applying emergency fix...

✓ Updated services/api/client.py:
  - OLD: API_KEY = "sk_live_51H7K9..."
  + NEW: API_KEY = os.getenv("STRIPE_API_KEY")

✓ Created .env.example:
  STRIPE_API_KEY=your-stripe-key-here

✓ Updated .gitignore:
  + .env
  + .env.local

✓ Updated README.md:
  ## Environment Variables
  Copy .env.example to .env and fill in:
  - STRIPE_API_KEY: Get from https://dashboard.stripe.com/apikeys

✓ Created docs/SECRETS.md with key management guide
```

#### Phase 6: VERIFY Fix

```
Verifying secret removal...

Running secret scan...
✓ No hardcoded secrets in services/api/client.py
✓ No secrets matching pattern "sk_live_" found in codebase

Checking git history...
⚠ Secret found in git history (commit a3b4c5d)

RECOMMENDATION: Rewrite git history
This is DANGEROUS. Proceed only if:
  1. Repository is private
  2. No one else has pulled recently
  3. You can force-push

Rewrite history to remove secret? (y/n/skip)
```

If yes:
```
⚠ This will rewrite git history

git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch services/api/client.py' \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all

Execute? (yes/no - type full word)
```

If skip:
```
Secret remains in git history.
IMPORTANT: This key is compromised. Use the NEW key in .env

Continue? (y/n)
```

#### Phase 7: CREATE Prevention

```
Adding preventive measures...

✓ Created .git/hooks/pre-commit:
  #!/bin/bash
  # Block commits with secrets
  if grep -r "sk_live_" . --exclude-dir=.git; then
    echo "BLOCKED: Hardcoded Stripe key detected"
    exit 1
  fi

✓ Updated .gitignore:
  .env
  .env.*
  !.env.example
  *.pem
  *.key
  secrets/

✓ Added to pyproject.toml:
  [tool.ruff]
  select = ["S", ...] # Security checks

✓ Created docs/SECURITY.md:
  # Security Guidelines
  ## Secret Management
  - NEVER commit secrets
  - Use environment variables
  - Rotate keys quarterly
  - ...
```

#### Phase 8: RESUME Audit

```
Emergency resolved

Secret revoked
Code fixed
Git history cleaned
Prevention added

Resuming security audit...
```

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

### Example 1: Hardcoded API Key

```
User runs: /cco-audit-security

Scanning services/api/client.py...

EMERGENCY: P0 CRITICAL DETECTED

Line 23: API_KEY = "sk_live_51H7K9C8Dk3b..."

This is a Stripe LIVE API key.

AUDIT PAUSED.

Is this a REAL key or test value? (real/test)
User: real

IMMEDIATE ACTIONS REQUIRED:

1. Open Stripe dashboard to revoke key? (y/n)
User: y
[Opens https://dashboard.stripe.com/apikeys]

2. Have you revoked the key? (y/n)
User: y

3. Generating fix...
✓ Created .env.example
✓ Updated code to use os.getenv()
✓ Added .env to .gitignore

4. Verify fix...
✓ No secrets in code
⚠ Secret in git history (3 commits ago)

5. Rewrite history? (y/n)
User: y
✓ History rewritten
✓ Force-pushed to remote

6. Add prevention...
✓ Pre-commit hook installed
✓ .gitignore updated
✓ Security docs created

Emergency resolved
Resuming audit...

Scanning services/worker/...
```

### Example 2: Multiple Secrets

```
User runs: /cco-scan-secrets

Scanning codebase for secrets...

EMERGENCY: 3 P0 CRITICAL VIOLATIONS

1. services/api/client.py:23
   API_KEY = "sk_live_..."

2. shared/config.py:45
   DB_PASSWORD = "postgres_prod_2024"

3. worker/.env.backup:12
   JWT_SECRET = "super-secret-key"

AUDIT PAUSED. Fix all 3 before continuing.

Strategy:
1. Fix most critical first (database password)
2. Then API key
3. Then JWT secret

Start emergency response? (y/n)
User: y

=== VIOLATION 1/3: Database Password ===

shared/config.py:45
  DB_PASSWORD = "postgres_prod_2024"

CRITICAL: Database password in source code!

Actions:
1. Change database password NOW
   Provider: PostgreSQL
   How to: ALTER USER postgres PASSWORD 'new_password';

Change password? (y/n)
User: y

Enter new password (or 'generate' for random):
User: generate

Generated: kL9$mN2#pQ7@vR4^sT8
Copied to clipboard.

Execute SQL:
  ALTER USER postgres PASSWORD 'kL9$mN2#pQ7@vR4^sT8';

Done? (y/n)
User: y

Fixing code...
✓ Updated shared/config.py to use os.getenv()
✓ Added DB_PASSWORD to .env.example
✓ Updated deployment docs

1/3 resolved

=== VIOLATION 2/3: API Key ===
[Same process...]

=== VIOLATION 3/3: JWT Secret ===
[Same process...]

All 3 emergencies resolved
Resuming audit...
```

### Example 3: False Positive

```
User runs: /cco-audit-security

EMERGENCY: P0 CRITICAL DETECTED

tests/fixtures/api_mock.py:12
  API_KEY = "test_key_abc123"

Is this a REAL key or test value? (real/test)
User: test

Downgraded to P2 (false positive).

Recommendation: Add nosec comment
  API_KEY = "test_key_abc123"  # nosec - test fixture

Apply? (y/n)
User: y

✓ Added nosec comment
✓ Future scans will ignore this line

Continuing audit...
```

### Secret Detection Patterns

#### High-Confidence (Always P0)

```python
SECRET_PATTERNS = {
    "stripe_live_key": r"sk_live_[A-Za-z0-9]{24,}",
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "github_token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "jwt_secret": r"(jwt|JWT)_SECRET\s*=\s*['\"][^'\"]{20,}['\"]",
    "private_key_header": r"-----BEGIN (RSA |)PRIVATE KEY-----",
    "slack_webhook": r"hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+",
}
```

#### Medium-Confidence (Ask User)

```python
MAYBE_SECRETS = {
    "api_key_pattern": r"api[_-]?key\s*=\s*['\"][A-Za-z0-9]{16,}['\"]",
    "password_pattern": r"password\s*=\s*['\"][^'\"]{8,}['\"]",
    "secret_pattern": r"secret\s*=\s*['\"][^'\"]{12,}['\"]",
}
```

#### Low-Confidence (Ignore in Tests)

```python
TEST_FIXTURES = [
    "test_api_key",
    "password123",
    "your-api-key-here",
    "example.com",
]
```

### Integration with Commands

#### audit-security.md
Add at the very beginning (Phase 0):

```markdown
## Phase 0: Emergency Detection (highest priority)

Before starting parallel agents, activate security-emergency-response:

Use Skill tool:
Skill("security-emergency-response")

The skill will:
1. Quick scan for P0 CRITICAL patterns (hardcoded secrets)
2. If found → INTERRUPT and demand immediate fix
3. If none → Continue with normal 4-agent parallel audit

This ensures critical issues handled before time spent on full audit.
```

#### scan-secrets.md
Make this the PRIMARY workflow:

```markdown
scan-secrets.md is a wrapper for security-emergency-response skill

Always use:
Skill("security-emergency-response")

No custom logic needed - skill handles everything.
```

### State Management

Track emergency fixes in `.cco/state/{PROJECT}/security-emergencies.json`:

```json
{
  "emergencies": [
    {
      "id": "sec-2025-01-11-001",
      "detected_at": "2025-01-11T14:32:15Z",
      "severity": "P0_CRITICAL",
      "type": "hardcoded_api_key",
      "location": "services/api/client.py:23",
      "secret_pattern": "sk_live_*",
      "provider": "Stripe",
      "status": "resolved",
      "actions_taken": [
        "Key revoked at provider",
        "Code updated to use env var",
        "Git history rewritten",
        "Pre-commit hook added"
      ],
      "resolved_at": "2025-01-11T14:45:33Z",
      "time_to_resolve": "13m 18s"
    }
  ]
}
```

### Anti-Patterns to Prevent

#### WRONG: Continue Audit with Exposed Secret

```
Scanner: "Found hardcoded API key"
<Continues scanning...>
<Finishes audit 2 minutes later>
Report: "15 security issues found, including 1 CRITICAL"
User: "I'll fix them tomorrow"
<API key exploited overnight>
```

#### RIGHT: Emergency Stop

```
Scanner: "Found hardcoded API key"
EMERGENCY DETECTED
AUDIT PAUSED
"Fix this NOW before continuing"
<Guides user through revocation>
<Verifies fix>
<Adds prevention>
"Emergency resolved. Resuming audit..."
```

### Success Metrics

**Before (without skill):**
- Detection: Found in audit report (after scan completes)
- Response time: Hours or days (user procrastinates)
- Exploitation risk: HIGH (secret live while user delays)

**After (with skill):**
- Detection: IMMEDIATE (interrupts scan)
- Response time: Minutes (guided fix)
- Exploitation risk: LOW (revoked before exposure)

### When to Skip This Skill

Never skip for P0 CRITICAL.

For P1/P2/P3:
- User can choose to fix later
- Skill documents issue, doesn't block

For false positives:
- User confirms "test fixture"
- Skill adds nosec comment
- Future scans ignore
