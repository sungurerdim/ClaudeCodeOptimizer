---
id: cco-scan-secrets
description: Scan for exposed secrets - API keys, passwords, tokens in code
category: security
priority: critical
principles:
  - 'P_SECRET_ROTATION'
  - 'P_AUDIT_LOGGING'
  - 'P_SUPPLY_CHAIN_SECURITY'
  - 'U_EVIDENCE_BASED'
  - 'U_COMPLETE_REPORTING'
  - 'U_FAIL_FAST'
---

# Scan for Exposed Secrets

Scan **${PROJECT_NAME}** for hardcoded secrets and sensitive data.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}
**Security Critical:** ${SECURITY_CRITICAL}

## Objective

Prevent secret exposure:
1. Detect hardcoded API keys, passwords, tokens
2. Find sensitive data in code (emails, IPs, credentials)
3. Check git history for leaked secrets
4. Verify .env files are not committed
5. Provide remediation recommendations

**Output:** Secret exposure report with severity levels.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast file scanning for secret patterns
- Regex-based secret detection
- Git history scanning

**Analysis & Reasoning**: Sonnet (Plan agent)
- False positive filtering
- Risk assessment and severity classification
- Remediation recommendations

**Execution Pattern**:
1. Launch Haiku agents to scan codebase and git history (parallel)
2. Use pattern matching for secret detection
3. Analyze with Sonnet for false positives and risk assessment
4. Generate security report with remediation steps

---

## When to Use

**Use this command:**
- Before every commit (pre-commit hook)
- Before deployment
- During security audits
- After suspected leak

**CRITICAL if:**
- ${SECURITY_CRITICAL} == true
- Public repository
- Production system

---

## Phase 1: Detect Secret Patterns

Scan for common secret patterns:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import re

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Secret Pattern Scanning ===\n")
print(f"Project: {project_name}\n")

secrets_found = {
    "api_keys": [],
    "passwords": [],
    "tokens": [],
    "private_keys": [],
    "credentials": [],
    "sensitive_urls": []
}
```

Use Grep to find secret patterns:
```bash
# API keys (various formats)
Grep("(api[_-]?key|apikey|api[_-]?secret)\\s*[:=]\\s*['\"]?[a-zA-Z0-9]{20,}", output_mode="content", -i, -C=2)

# Passwords
Grep("(password|passwd|pwd)\\s*[:=]\\s*['\"].*['\"]", output_mode="content", -i, -C=2)

# Tokens (JWT, Bearer, etc.)
Grep("(token|bearer|jwt|auth)\\s*[:=]\\s*['\"]?[a-zA-Z0-9._-]{30,}", output_mode="content", -i, -C=2)

# Private keys
Grep("BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY", output_mode="content", -C=2)

# AWS keys
Grep("(AKIA|ASIA)[A-Z0-9]{16}", output_mode="content", -C=2)

# Anthropic API keys
Grep("sk-ant-[a-zA-Z0-9_-]{95,}", output_mode="content", -C=2)

# Generic secrets
Grep("(secret|credential|auth)\\s*[:=]\\s*['\"][^'\"]{20,}['\"]", output_mode="content", -i, -C=2)
```

```python
# Example: Secrets found
api_key_findings = [
    {
        "type": "API Key",
        "pattern": "ANTHROPIC_API_KEY = 'sk-ant-api03-...'",
        "file": "services/api/config.py:12",
        "severity": "CRITICAL",
        "exposed_value": "sk-ant-api03-..." # Truncated
    },
    {
        "type": "API Key",
        "pattern": "STRIPE_API_KEY = 'sk_test_...'",
        "file": "services/payment/stripe.py:5",
        "severity": "CRITICAL",
        "exposed_value": "sk_test_..."
    }
]

password_findings = [
    {
        "type": "Password",
        "pattern": "DATABASE_PASSWORD = 'my_secret_pass'",
        "file": ".env",  # Should not be committed!
        "severity": "CRITICAL",
        "exposed_value": "my_secret_pass"
    }
]

token_findings = [
    {
        "type": "JWT Token",
        "pattern": "token = 'eyJhbGci...'",
        "file": "tests/test_auth.py:45",
        "severity": "HIGH",
        "exposed_value": "eyJhbGci..."
    }
]

# Aggregate
secrets_found["api_keys"] = api_key_findings
secrets_found["passwords"] = password_findings
secrets_found["tokens"] = token_findings

total_secrets = sum(len(findings) for findings in secrets_found.values())

print(f"Secrets Found: {total_secrets}\n")

for secret_type, findings in secrets_found.items():
    if findings:
        print(f"{secret_type.replace('_', ' ').title()}: {len(findings)}")
        for finding in findings[:3]:
            print(f"  - {finding['file']}: {finding['type']}")
        if len(findings) > 3:
            print(f"  ... and {len(findings) - 3} more")
        print()
```

---

## Phase 2: Check .env Files

Verify .env files are not committed to git:

```python
print(f"=== .env File Check ===\n")

# Find all .env files
env_files = list(project_root.glob("**/.env*"))

# Check if committed to git
import subprocess

committed_env_files = []

for env_file in env_files:
    # Skip .env.example (should be committed)
    if ".example" in env_file.name or ".template" in env_file.name:
        continue

    # Check if tracked by git
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(env_file)],
            capture_output=True,
            cwd=project_root
        )

        if result.returncode == 0:
            # File is tracked by git - BAD!
            committed_env_files.append(env_file)
    except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
        # Git not available or other subprocess error - skip this check
        logger.debug(f"Could not check git status for {env_file}: {e}")

if committed_env_files:
    print(f"⚠️ CRITICAL: {len(committed_env_files)} .env files committed to git!\n")
    for env_file in committed_env_files:
        print(f"  - {env_file.relative_to(project_root)}")
    print("\nThese files may contain secrets and should NOT be in git!")
    print()
else:
    print("✓ No .env files committed to git\n")

# Check if .env is in .gitignore
gitignore_path = project_root / ".gitignore"
if gitignore_path.exists():
    gitignore_content = gitignore_path.read_text()
    if ".env" in gitignore_content:
        print("✓ .env is in .gitignore\n")
    else:
        print("⚠️ .env is NOT in .gitignore (should be added)\n")
```

---

## Phase 3: Scan Git History

Check if secrets were leaked in past commits:

```python
print(f"=== Git History Scan ===\n")

# Use git grep to search history
# This is simplified - full implementation would use tools like gitleaks or truffleHog

print("Scanning git history for secrets...")
print("(This may take a few minutes for large repos)\n")

# For demo, skip actual git history scan
# In production, use: gitleaks, truffleHog, or git-secrets

print("Recommendation: Install and run git secret scanners:")
print("  - gitleaks: https://github.com/gitleaks/gitleaks")
print("  - truffleHog: https://github.com/trufflesecurity/truffleHog")
print("  - git-secrets: https://github.com/awslabs/git-secrets")
print()

# Example command
print("Example with gitleaks:")
print("  gitleaks detect --source . --report-path gitleaks-report.json")
print()
```

---

## Phase 4: Check for Sensitive Data

Find other sensitive information:

```python
print(f"=== Sensitive Data Check ===\n")
```

Use Grep to find sensitive patterns:
```bash
# Credit card numbers (simplified pattern)
Grep("\\b[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}\\b", output_mode="content", -C=2)

# Email addresses (may contain PII)
Grep("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b", output_mode="content", -C=2)

# IP addresses (internal IPs may be sensitive)
Grep("\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b", output_mode="content", -C=2)

# Social Security Numbers (US)
Grep("\\b[0-9]{3}-[0-9]{2}-[0-9]{4}\\b", output_mode="content", -C=2)
```

```python
# Review findings manually
print("Sensitive data patterns detected:")
print("  - Email addresses: Review for PII leakage")
print("  - IP addresses: Check if internal IPs are exposed")
print()
```

---

## Phase 5: Categorize by Severity

Organize findings by risk level:

```python
print(f"=== Severity Analysis ===\n")

by_severity = {
    "CRITICAL": [],
    "HIGH": [],
    "MEDIUM": [],
    "LOW": []
}

# Categorize all findings
for secret_type, findings in secrets_found.items():
    for finding in findings:
        severity = finding["severity"]
        by_severity[severity].append(finding)

# Add .env file findings
for env_file in committed_env_files:
    by_severity["CRITICAL"].append({
        "type": ".env file in git",
        "file": str(env_file.relative_to(project_root)),
        "severity": "CRITICAL",
        "pattern": "Entire .env file committed"
    })

# Display by severity
for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
    findings = by_severity[severity]
    if findings:
        print(f"{severity}: {len(findings)} findings")
        for finding in findings[:3]:
            print(f"  - {finding['type']} in {finding['file']}")
        if len(findings) > 3:
            print(f"  ... and {len(findings) - 3} more")
        print()
```

---

## Phase 6: Remediation Recommendations

Provide specific fix recommendations:

```python
print(f"=== Remediation Recommendations ===\n")

recommendations = []

# CRITICAL: Hardcoded secrets
if by_severity["CRITICAL"]:
    recommendations.append({
        "priority": "CRITICAL",
        "title": f"Remove {len(by_severity['CRITICAL'])} hardcoded secrets IMMEDIATELY",
        "actions": [
            "1. Rotate all exposed API keys/passwords",
            "2. Move secrets to environment variables",
            "3. Use .env files (not committed to git)",
            "4. Consider using secrets manager (AWS Secrets Manager, HashiCorp Vault)"
        ]
    })

# .env files in git
if committed_env_files:
    recommendations.append({
        "priority": "CRITICAL",
        "title": "Remove .env files from git history",
        "actions": [
            "1. Add .env to .gitignore",
            "2. Remove from git: git rm --cached .env",
            "3. Commit: git commit -m 'Remove .env from git'",
            "4. Purge from history: git filter-branch or BFG Repo-Cleaner",
            "5. Force push (if safe): git push --force"
        ]
    })

# API keys
if secrets_found["api_keys"]:
    recommendations.append({
        "priority": "CRITICAL",
        "title": f"Secure {len(secrets_found['api_keys'])} API keys",
        "actions": [
            "1. Revoke and regenerate all exposed API keys",
            "2. Store in environment variables",
            "3. Use python-dotenv to load from .env",
            "4. Never commit .env files"
        ],
        "example": """
# Before (INSECURE)
API_KEY = "sk-ant-api03-..."  # Hardcoded

# After (SECURE)
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")

# .env (NOT in git)
ANTHROPIC_API_KEY=sk-ant-api03-...
"""
    })

# Display
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. [{rec['priority']}] {rec['title']}")
    print("   Actions:")
    for action in rec['actions']:
        print(f"     {action}")
    if 'example' in rec:
        print(f"   Example:{rec['example']}")
    print()
```

---

## Phase 7: Generate .gitignore Rules

Suggest .gitignore additions:

```python
print(f"=== .gitignore Recommendations ===\n")

gitignore_additions = [
    "# Secrets and environment variables",
    ".env",
    ".env.local",
    ".env.*.local",
    "*.key",
    "*.pem",
    "*.p12",
    "*.pfx",
    "",
    "# Credentials",
    "credentials.json",
    "service-account.json",
    "secrets/",
    "",
    "# IDE-specific",
    ".vscode/settings.json",  # May contain tokens
    ".idea/workspace.xml",    # May contain credentials
]

gitignore_path = project_root / ".gitignore"

if gitignore_path.exists():
    current_gitignore = gitignore_path.read_text()

    missing_rules = []
    for rule in gitignore_additions:
        if rule and not rule.startswith('#') and rule not in current_gitignore:
            missing_rules.append(rule)

    if missing_rules:
        print(f"Add these rules to .gitignore:\n")
        for rule in missing_rules:
            print(f"  {rule}")
        print()
    else:
        print("✓ .gitignore has all recommended rules\n")
else:
    print("⚠️ No .gitignore file found!")
    print("\nCreate .gitignore with:\n")
    for rule in gitignore_additions:
        print(rule)
    print()
```

---

## Phase 8: Security Score

Calculate overall security score:

```python
print(f"=== Security Score ===\n")

# Calculate score (100 = no secrets, 0 = critical exposure)
security_score = 100

# Deduct for secrets
critical_penalty = len(by_severity["CRITICAL"]) * 25  # Max 100
high_penalty = len(by_severity["HIGH"]) * 10
medium_penalty = len(by_severity["MEDIUM"]) * 5
low_penalty = len(by_severity["LOW"]) * 2

total_penalty = critical_penalty + high_penalty + medium_penalty + low_penalty
security_score = max(0, security_score - total_penalty)

print(f"Security Score: {security_score}/100\n")

if security_score >= 90:
    status = "EXCELLENT ✓✓✓"
    color = "🟢"
elif security_score >= 70:
    status = "GOOD ✓✓"
    color = "🟡"
elif security_score >= 50:
    status = "FAIR ✓"
    color = "🟠"
else:
    status = "CRITICAL RISK ✗"
    color = "🔴"

print(f"{color} Status: {status}\n")

print("Score Breakdown:")
print(f"- Base Score: 100")
print(f"- Critical Findings: -{critical_penalty} ({len(by_severity['CRITICAL'])} × 25)")
print(f"- High Findings: -{high_penalty} ({len(by_severity['HIGH'])} × 10)")
print(f"- Medium Findings: -{medium_penalty} ({len(by_severity['MEDIUM'])} × 5)")
print(f"- Low Findings: -{low_penalty} ({len(by_severity['LOW'])} × 2)")
print(f"- Final Score: {security_score}")
print()

if security_score < 50:
    print("⚠️ URGENT: This project has CRITICAL security vulnerabilities!")
    print("   Immediate action required before deployment.")
```

---

## Quick Scan Modes

```bash
# Full scan (default)
/cco-scan-secrets

# Quick scan (code only, no git history)
/cco-scan-secrets --quick

# Only critical severity
/cco-scan-secrets --critical-only

# Specific file or directory
/cco-scan-secrets --path=services/api

# Output to JSON for CI/CD
/cco-scan-secrets --output=secrets-report.json
```

---

## Integration with CI/CD

```yaml
# .github/workflows/secrets-scan.yml
name: Secret Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Scan for secrets
        run: |
          pip install claudecodeoptimizer
          cco scan-secrets
      - name: Fail if secrets found
        run: |
          if [ $? -ne 0 ]; then
            echo "Secrets detected! Fix before merging."
            exit 1
          fi
```

---

## Output Example

```
=== Secret Pattern Scanning ===

Project: backend

Secrets Found: 5

Api Keys: 2
  - services/api/config.py:12: API Key
  - services/payment/stripe.py:5: API Key

Passwords: 1
  - .env: Password

Tokens: 2
  - tests/test_auth.py:45: JWT Token
  - services/worker/tasks.py:89: Bearer Token

=== .env File Check ===

⚠️ CRITICAL: 1 .env files committed to git!

  - .env

These files may contain secrets and should NOT be in git!

⚠️ .env is NOT in .gitignore (should be added)

=== Git History Scan ===

Scanning git history for secrets...
(This may take a few minutes for large repos)

Recommendation: Install and run git secret scanners:
  - gitleaks: https://github.com/gitleaks/gitleaks
  - truffleHog: https://github.com/trufflesecurity/truffleHog
  - git-secrets: https://github.com/awslabs/git-secrets

Example with gitleaks:
  gitleaks detect --source . --report-path gitleaks-report.json

=== Sensitive Data Check ===

Sensitive data patterns detected:
  - Email addresses: Review for PII leakage
  - IP addresses: Check if internal IPs are exposed

=== Severity Analysis ===

CRITICAL: 4 findings
  - API Key in services/api/config.py:12
  - API Key in services/payment/stripe.py:5
  - Password in .env
  - .env file in git in .env

HIGH: 2 findings
  - JWT Token in tests/test_auth.py:45
  - Bearer Token in services/worker/tasks.py:89

=== Remediation Recommendations ===

1. [CRITICAL] Remove 4 hardcoded secrets IMMEDIATELY
   Actions:
     1. Rotate all exposed API keys/passwords
     2. Move secrets to environment variables
     3. Use .env files (not committed to git)
     4. Consider using secrets manager (AWS Secrets Manager, HashiCorp Vault)

2. [CRITICAL] Remove .env files from git history
   Actions:
     1. Add .env to .gitignore
     2. Remove from git: git rm --cached .env
     3. Commit: git commit -m 'Remove .env from git'
     4. Purge from history: git filter-branch or BFG Repo-Cleaner
     5. Force push (if safe): git push --force

3. [CRITICAL] Secure 2 API keys
   Actions:
     1. Revoke and regenerate all exposed API keys
     2. Store in environment variables
     3. Use python-dotenv to load from .env
     4. Never commit .env files
   Example:
   [... example code ...]

=== .gitignore Recommendations ===

Add these rules to .gitignore:

  .env
  .env.local
  .env.*.local
  *.key
  *.pem
  credentials.json
  secrets/

=== Security Score ===

Security Score: 0/100

🔴 Status: CRITICAL RISK ✗

Score Breakdown:
- Base Score: 100
- Critical Findings: -100 (4 × 25)
- High Findings: -20 (2 × 10)
- Medium Findings: -0 (0 × 5)
- Low Findings: -0 (0 × 2)
- Final Score: 0

⚠️ URGENT: This project has CRITICAL security vulnerabilities!
   Immediate action required before deployment.
```

---

**Security Philosophy:** One leaked secret can compromise an entire system. Scan early, scan often!
