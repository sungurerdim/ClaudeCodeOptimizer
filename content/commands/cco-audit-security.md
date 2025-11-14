---
description: Security vulnerabilities, privacy violations, credential leaks audit
category: audit
cost: 2
principles: ['P_AUTH_AUTHZ', 'P_ENCRYPTION_AT_REST', 'P_ZERO_DISK_TOUCH', 'P_PRIVACY_FIRST', 'P_TTL_BASED_CLEANUP', 'P_ZERO_TRUST', 'P_SECRET_ROTATION', 'P_XSS_PREVENTION', 'P_SQL_INJECTION', 'P_AUDIT_LOGGING', 'P_SUPPLY_CHAIN_SECURITY', 'P_AI_ML_SECURITY', 'P_CONTAINER_SECURITY', 'P_K8S_SECURITY', 'P_PRIVACY_COMPLIANCE']
---

# cco-audit-security - Security & Privacy Audit

**Comprehensive security audit focusing on vulnerabilities, privacy violations, and credential leaks.**

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast security scanning and pattern detection
- Secret scanning and vulnerability detection
- Cost-effective for repetitive security checks

**Analysis**: Sonnet (Plan agent)
- Risk assessment and exploit scenario analysis
- Security debt calculation and prioritization
- Actionable remediation recommendations

**Execution Pattern**:
1. Launch 2 parallel Haiku agents:
   - Agent 1: Data security (secrets, PII, encryption)
   - Agent 2: Architecture security (auth, sessions, hardening)
2. Aggregate with Sonnet for intelligent risk analysis
3. Generate exploit-aware prioritized remediation plan

**Model Requirements**:
- Haiku for scanning (20-25 seconds)
- Sonnet for risk assessment and prioritization

---

## Action

Use Task tool to launch parallel security audit agents.

### Step 1: Parallel Security Scans

**CRITICAL**: Launch BOTH agents in PARALLEL in a SINGLE message for 2x speed boost.

#### Agent 1: Data Security Scan

**Agent 1 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Data security audit

CRITICAL - MUST LOAD FIRST:
1. Load @CLAUDE.md (Security section)
2. Load @~/.cco/guides/security-response.md
3. Load @~/.cco/principles/security.md
4. Print confirmation: "✓ Loaded 3 documents (~3,500 tokens)"

THEN audit these principles:
- P_PRIVACY_FIRST: Privacy-First by Default (no PII in logs, proper anonymization)
- P_ZERO_DISK_TOUCH: Zero Disk Touch (sensitive data not written to disk)
- P_SECRET_ROTATION: Secret Management (no hardcoded API keys, passwords, tokens)
- P_ENCRYPTION_AT_REST: Encryption Everywhere (proper crypto, no weak hashing)

Scan for:
- Unencrypted sensitive data in code
- Hardcoded secrets: API keys (sk_*, pk_*, api_key), passwords, tokens, JWT secrets
- .env files committed to git (check git history)
- Credential files (credentials.json, .pem, .key, .p12, .pfx)
- PII in log statements (emails, names, SSN, credit cards)
- Weak password hashing (MD5, SHA1, plain text)
- Sensitive data in comments or configuration

Compare findings against security-response.md checklist.
Report with file:line references and severity.
```

#### Agent 2: Architecture Security Scan

**Agent 2 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Security architecture audit

CRITICAL - MUST LOAD FIRST:
1. Load @CLAUDE.md (Security section)
2. Load @~/.cco/guides/security-response.md
3. Load @~/.cco/principles/security.md
4. Print confirmation: "✓ Loaded 3 documents (~3,500 tokens)"

THEN audit these principles:
- P_TTL_BASED_CLEANUP: TTL-Based Cleanup (sessions expire, data cleanup)
- P_ZERO_TRUST: Zero Trust Architecture (multiple security layers)
- P_AUTH_AUTHZ: Authentication & Authorization (HTTPS, headers, hardening)
- P_XSS_PREVENTION: Input Sanitization (XSS Prevention)
- P_SQL_INJECTION: SQL Injection Prevention (parameterized queries)
- P_AUDIT_LOGGING: Audit Logging (security events tracked)
- P_SUPPLY_CHAIN_SECURITY: Supply Chain Security (dependency scanning)
- P_CONTAINER_SECURITY: Container Security (if applicable)
- P_PRIVACY_COMPLIANCE: Privacy Compliance (GDPR, CCPA, etc.)

Check for:
- Session expiration configuration (TTL settings)
- HTTPS enforcement in config (redirect HTTP to HTTPS)
- Security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- Input validation and sanitization
- SQL injection prevention (parameterized queries, ORM usage)
- XSS prevention (output escaping, CSP)
- CORS policy (not overly permissive)
- Rate limiting on authentication endpoints
- Audit logging for security events
- Dependency vulnerabilities (npm audit, pip-audit, etc.)
- Container security best practices (if applicable)

Compare findings against security-response.md patterns.
Report with file:line references and exploit scenarios.
```

### Step 2: Risk Assessment & Prioritization

**After both agents complete**, use Sonnet Plan agent for intelligent analysis:

**Agent 3 Prompt:**
```
Subagent Type: Plan
Model: sonnet
Description: Security risk assessment

Task: Analyze security findings from 2 parallel security audits.

Input:
- Agent 1 findings (data security)
- Agent 2 findings (architecture security)

Analysis steps:
1. Merge all security findings from both agents
2. Assess actual risk level (not just theoretical)
3. Identify attack vectors and exploit scenarios
4. Prioritize by: Exploitability × Impact × Exposure
5. Provide specific remediation steps with commands
6. Estimate security debt (hours) and fix effort
7. Recommend immediate actions vs long-term hardening
8. Calculate risk reduction percentage for each fix

Output format:
- Findings by severity (CRITICAL > HIGH > MEDIUM > LOW)
- Each finding includes: principle, file:line, exploit scenario, fix command
- Master remediation plan with priority tiers
- Security debt estimate (total hours)

Focus on practical, actionable security improvements.
```

**Why use Sonnet for aggregation:**
- Risk assessment requires deep reasoning (not just data collection)
- Attack vector analysis needs intelligence and context
- Prioritization by real-world exploitability (not just severity)
- Context-aware remediation recommendations
- Pattern recognition across multiple findings
- Accurate effort estimation

---

## Output Format

Report security issues with risk level and exploit scenarios:

```
Security Audit Results
=====================

CRITICAL (immediate action required):
  - P_SECRET_ROTATION: Hardcoded AWS credentials in src/config.py:23
    Risk: Full AWS account compromise
    Exploit: Credentials visible in git history
    Command: /cco-fix secrets --rotate --files src/config.py

  - P_SQL_INJECTION: SQL injection in src/api.py:145
    Risk: Database breach, data exfiltration
    Exploit: Unsanitized user input in query
    Command: /cco-fix security --type sql-injection --file src/api.py:145

CRITICAL (data breach risk):
  - P_PRIVACY_FIRST: User emails logged in plaintext (src/auth.py:67)
    Risk: GDPR violation, privacy breach
    Exploit: Log aggregation exposes PII
    Command: /cco-fix privacy --type remove-logging --file src/auth.py:67

HIGH (security gap):
  - P_AUTH_AUTHZ: Missing HTTPS enforcement (src/app.py)
    Risk: Man-in-the-middle attacks
    Exploit: Network traffic interception
    Command: /cco-fix security --type https-redirect --file src/app.py

  - P_TTL_BASED_CLEANUP: Sessions never expire (src/session.py)
    Risk: Session hijacking, unlimited access
    Exploit: Stolen session tokens valid forever
    Command: /cco-fix security --type ttl --file src/session.py --ttl 24h

MEDIUM (hardening recommended):
  - P_ENCRYPTION_AT_REST: Weak password hashing (MD5 in src/auth.py:34)
    Risk: Rainbow table attacks
    Exploit: Password database compromise
    Command: /cco-fix security --type password-hashing --algorithm bcrypt --file src/auth.py

  - P_ZERO_DISK_TOUCH: Sensitive files not in .gitignore
    Risk: Accidental secret commit
    Files: .env.local, credentials.json
    Command: /cco-fix secrets --update-gitignore --add .env.local,credentials.json

LOW (best practice):
  - P_RATE_LIMITING: Missing rate limiting on API endpoints
    Risk: DoS, brute force attacks
    Impact: Service availability
    Command: /cco-generate middleware --type rate-limiter --endpoints /api/*
```

---

## Recommended Actions

**Analyze security findings and provide exploit-aware prioritization:**

```
🔒 Security Remediation Plan (Risk-Based Priority)
==================================================

IMMEDIATE (Deploy Blockers):
──────────────────────────────
1. Rotate compromised credentials
   Command: /cco-fix secrets --rotate --files src/config.py
   Impact: CRITICAL - Prevents AWS account takeover
   Effort: 5 minutes
   Risk Reduction: 40%

2. Fix SQL injection
   Command: /cco-fix security --type sql-injection --file src/api.py:145
   Impact: CRITICAL - Prevents database breach
   Effort: 30 minutes
   Risk Reduction: 25%

3. Remove PII from logs
   Command: /cco-fix privacy --type remove-logging --file src/auth.py:67
   Impact: CRITICAL - GDPR compliance
   Effort: 15 minutes
   Risk Reduction: 20%

THIS WEEK (High Risk):
─────────────────────
4. Enforce HTTPS
   Command: /cco-fix security --type https-redirect --file src/app.py
   Impact: HIGH - Prevents MITM attacks
   Effort: 1 hour
   Risk Reduction: 5%

5. Implement session expiration
   Command: /cco-generate session-management --ttl 24h --file src/session.py
   Impact: HIGH - Limits session hijacking window
   Effort: 2 hours
   Risk Reduction: 3%

THIS SPRINT (Hardening):
───────────────────────
6. Upgrade password hashing
   Command: /cco-fix security --type password-hashing --algorithm bcrypt --file src/auth.py
   Impact: MEDIUM - Protects against rainbow tables
   Effort: 1.5 hours
   Risk Reduction: 1%

7. Update .gitignore
   Command: /cco-fix secrets --update-gitignore --add .env.local,credentials.json
   Impact: MEDIUM - Prevents future leaks
   Effort: 10 minutes
   Risk Reduction: 0.5%

BACKLOG (Best Practice):
───────────────────────
8. Add rate limiting
   Command: /cco-generate middleware --type rate-limiter --endpoints /api/*
   Impact: LOW - DoS protection
   Effort: 3 hours
   Risk Reduction: 0.5%

Security Debt: 8.25 hours | Risk Reduction: 95%
```

**Command Generation Logic:**
1. **Risk = Exploitability × Impact × Exposure**
   - Exploitability: How easy to exploit? (trivial/easy/hard)
   - Impact: What's at stake? (data breach/service disruption/reputation)
   - Exposure: Is it exposed? (public API/internal/localhost)

2. **Priority Tiers:**
   - IMMEDIATE: Actively exploitable, high impact (fix in hours)
   - THIS WEEK: Exploitable with effort, medium-high impact (fix in days)
   - THIS SPRINT: Requires specific conditions, medium impact (fix in weeks)
   - BACKLOG: Low exploitability or impact (fix in months)

3. **Command Features:**
   - Specific fix type: `--type sql-injection`, `--type https-redirect`
   - Risk context: Why this matters (exploit scenario)
   - Effort estimate: Realistic time to fix
   - Impact metric: Risk reduction percentage

4. **Grouping:**
   - Same vulnerability type → Single command with multiple files
   - Same file → Single command with multiple fix types
   - Dependencies → Sequential commands with order

---

## Related Commands

- `/cco-fix security` - Fix security vulnerabilities automatically
- `/cco-audit-code-quality` - Code quality audit
- `/cco-audit-comprehensive` - Full comprehensive audit
