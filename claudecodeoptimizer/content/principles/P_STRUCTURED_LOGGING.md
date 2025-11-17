# P_STRUCTURED_LOGGING: Structured Logging

**Severity**: Critical

Use JSON key-value pairs, not free-form text. Unstructured logs: can't query, can't correlate, 10x slower searches, 4hr → 15min MTTR.

---

## Rules

- **JSON format** - Machine-parseable key-value pairs
- **Consistent fields** - Same concept = same field name always
- **Extract objects** - Don't stringify; log relevant fields
- **UTC timestamps** - Always timezone-aware
- **Type consistency** - Boolean as bool, not string "true"

---

## Examples

### ✅ Good
```python
logger.info("Authentication attempt",
    username=username,
    ip_address=ip_address,
    timestamp=datetime.utcnow().isoformat()
)
# Output: {"level":"INFO","message":"Authentication attempt","username":"john","ip_address":"192.168.1.1","timestamp":"2024-01-15T10:30:45Z"}
# Can query: username="john", can aggregate, can correlate
```
**Why right**: Machine-parseable, queryable, consistent schema

### ❌ Bad
```python
logger.info(f"User {username} logged in from {ip_address} at {datetime.now()}")
# Output: "User john logged in from 192.168.1.1 at 2024-01-15 10:30:45"
# Cannot query for user 123; grep returns false positives
```
**Why wrong**: Free-form text; can't parse, can't query, can't aggregate

---

## Anti-Patterns

**❌ Unstructured Text**: Free-form strings impossible to parse/query/aggregate
**❌ Inconsistent Fields**: Same concept has different names (`method`, `http_method`, `req_method`) - aggregation fails
**❌ Stringifying Objects**: `logger.info(f"User: {user}")` → can't extract user_id, email, is_admin
**❌ Mixing Formats**: Some structured, some not - parser can't handle inconsistency

---

## Checklist

- [ ] JSON output format
- [ ] Consistent field names across all logs
- [ ] No f-strings or string interpolation
- [ ] Extract object fields, don't stringify
- [ ] UTC timestamps
- [ ] Document standard fields
