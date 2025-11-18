# P_PII_MASKING_IN_LOGS: PII Masking in Logs

**Severity**: Critical

 Unmasked PII in logs becomes exposed in breaches (logs are common targets) GDPR, HIPAA, PCI-DSS require PII protection; unmasked logs = fines Employees with log access can extract customer data Log a.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
import re
import logging
from typing import Any, Dict

class PIIMaskingFormatter(logging.Formatter):
    """Log formatter that masks PII in log messages."""

    # PII patterns to mask
    PII_PATTERNS = {
        'email': (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '***@***.***'),
        'credit_card': (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '****-****-****-****'),
        'ssn': (r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****'),
        'password': (r'password["\']?\s*[:=]\s*["\']?[^"\']+["\']?', 'password=***'),
        'token': (r'(token|auth|bearer)\s*["\']?([a-zA-Z0-9._-]+)["\']?', r'\1=***'),
        'api_key': (r'(api_key|apikey)["\']?\s*[:=]\s*["\']?[^"\']+["\']?', r'\1=***'),
        'phone': (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '***-***-****'),
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: Sensitive data exposed in logs
logger.info(f"User login: email={user.email}, password={password}, ip={ip_address}")
# Output: "User login: email=<email>, password=<password-value>, ip=<ip-address>"
# Problem: Password in logs! Email exposed! Compliance violation!

logger.error(f"Payment failed: credit_card={cc}, user_id={user_id}")
# Output: "Payment failed: credit_card=<full-cc>, user_id=<user-id>"
# Problem: Full credit card in logs! PCI-DSS violation! Fines!

logger.debug(f"Auth token: {token}")
# Output: "Auth token: <token-value>"
```
**Why wrong**: ---

---

## Checklist

- [ ] No passwords in logs - Password fields never logged, ever
- [ ] No full credit cards - Only last 4 digits if needed
- [ ] No auth tokens - Never log JWT, OAuth, API keys
- [ ] No SSN/PII - Mask social security, phone, addresses
- [ ] Email masking - Mask email addresses in logs
- [ ] IP masking - Mask internal IPs (192.168, 10.0, 127.0)
- [ ] API key masking - Never log API keys or secrets
