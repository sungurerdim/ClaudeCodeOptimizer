---
name: privacy-compliance
description: Implement GDPR/HIPAA/CCPA compliance through PII encryption, consent management, data subject rights (access, erasure, portability), log sanitization, and retention automation
keywords: [GDPR, HIPAA, CCPA, PII encryption, consent management, data subject rights, privacy by design, log sanitization, retention policy]
category: security
related_commands:
  action_types: [audit, fix, generate]
  categories: [security]
pain_points: [3, 5, 8]
---

# Skill: Privacy, GDPR Compliance, Encryption
**Domain**: Data Protection
**Purpose**: Implement GDPR/HIPAA/CCPA compliance through PII encryption, consent management, data subject rights, and privacy-by-design.

## Core Techniques
- **PII Identification**: Scan models for PII keywords (email, phone, ssn, health), create GDPR Art. 30 data inventory
- **Field Encryption**: Use SQLAlchemy TypeDecorator for app-level encryption, pgcrypto for DB-level
- **Log Sanitization**: Regex-based PII masking in logs/errors, structured logging redaction
- **Consent Management**: Purpose-specific consent with provable metadata (timestamp, IP, user-agent)
- **Data Subject Rights**: Implement access (Art. 15), erasure (Art. 17), portability (Art. 20) endpoints
- **Retention Automation**: Celery task for automated deletion per retention policies

## Patterns

### ✅ Good - Field Encryption
```python
from cryptography.fernet import Fernet
from sqlalchemy import TypeDecorator, String

class EncryptedString(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return cipher.encrypt(value.encode()).decode() if value else None

    def process_result_value(self, value, dialect):
        return cipher.decrypt(value.encode()).decode() if value else None

class User(Base):
    email = Column(EncryptedString, nullable=False)  # GDPR Art. 32
    ssn = Column(EncryptedString)
```
**Why**: Transparent encryption at application layer, keys in KMS

### ✅ Good - Log Sanitization
```python
PII_PATTERNS = {
    'email': (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
    'ssn': (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]'),
}

class PIIFilter(logging.Filter):
    def filter(self, record):
        for pattern, replacement in PII_PATTERNS.values():
            record.msg = re.sub(pattern, replacement, record.msg)
        return True
```
**Why**: Prevents PII leakage in logs/errors

### ✅ Good - Consent with Proof
```python
class Consent(Base):
    user_id = Column(String, ForeignKey('users.id'))
    marketing_consent = Column(Boolean, default=False)
    consent_given_at = Column(DateTime)  # GDPR Art. 7(1)
    ip_address = Column(String)  # Evidence
    privacy_policy_version = Column(String)  # Track changes
```
**Why**: Provable consent meets GDPR requirements

### ✅ Good - Right to Erasure
```python
@router.delete("/api/erase-data")
async def erasure_request(user: User = Depends(get_current_user)):
    if has_legal_hold(user.id):
        raise HTTPException(403, "Legal hold")

    # Pseudonymize
    user.email = f"deleted_{user.id}@example.com"
    user.first_name = "[DELETED]"
    user.account_status = 'deleted'

    await delete_from_crm(user.id)
    db.commit()
```
**Why**: Complies with GDPR Art. 17, respects legal holds

### ❌ Bad - Plaintext PII
```python
class User(Base):
    email = Column(String)  # No encryption
    ssn = Column(String)
```
**Why**: GDPR Art. 32 requires encryption for sensitive data

### ❌ Bad - PII in Logs
```python
logger.info(f"User {user.email} registered")  # Plaintext email
```
**Why**: PII exposure in logs violates GDPR

### ❌ Bad - Blanket Consent
```python
accept_all_terms = Column(Boolean)  # Single checkbox
```
**Why**: GDPR Art. 7 requires purpose-specific consent

## Checklist
- [ ] PII fields identified and encrypted (use EncryptedString)
- [ ] Data inventory created (GDPR Art. 30: fields, lawful basis, retention)
- [ ] TLS 1.3 enforced for APIs
- [ ] Encryption keys in KMS, rotated every 90 days
- [ ] Logs sanitized (PIIFilter applied)
- [ ] Consent stored with timestamp, IP, policy version
- [ ] Data access endpoint returns all PII (Art. 15, <30 days)
- [ ] Erasure endpoint pseudonymizes/deletes (Art. 17, <30 days)
- [ ] Data export supports JSON/CSV (Art. 20)
- [ ] Retention policies automated (Celery task)
- [ ] Breach response plan tested (72h notification)
- [ ] Privacy Impact Assessment for new features

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for privacy compliance domain
action_types: [audit, fix, generate]
keywords: [GDPR, HIPAA, CCPA, PII, encryption, consent, privacy, data subject rights]
category: security
pain_points: [3, 5, 8]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: security`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.
