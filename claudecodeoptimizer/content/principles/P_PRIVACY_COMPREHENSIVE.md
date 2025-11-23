---
name: privacy-comprehensive
description: Implement comprehensive privacy protection including PII handling, data minimization, and regulatory compliance (GDPR, CCPA, PIPEDA)
type: project
severity: critical
keywords: [privacy, pii, gdpr, ccpa, pipeda, data-minimization, encryption, compliance]
category: [security, compliance]
related_skills: []
---

# P_PRIVACY_COMPREHENSIVE: Comprehensive Privacy Protection

**Severity**: Critical

 GDPR fines up to €20M or 4% of global revenue PII lingering in memory/logs increases breach impact Privacy violations damage reputation permanently Non-compliance with CCPA, GDPR, PIPEDA, etc. Unprot.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
# ✅ GOOD: Explicit PII cleanup
def process_payment(user_id: str, card_number: str):
    # Load PII
    encrypted_card = encrypt(card_number)

    try:
        # Use PII
        result = payment_gateway.charge(encrypted_card)
        return result
    finally:
        # CRITICAL: Secure cleanup
        secure_zero(card_number)
        secure_zero(encrypted_card)

# ❌ BAD: PII lingers in memory
def process_payment(user_id: str, card_number: str):
```
**Why right**: ---
---

## Checklist

- [ ] *No rules extracted*

