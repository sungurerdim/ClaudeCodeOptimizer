---
id: P_SQL_INJECTION
title: SQL Injection Prevention
category: project-specific
severity: critical
weight: 10
applicability:
  project_types: ['database', 'api', 'web']
  languages: ['python', 'javascript', 'typescript', 'java', 'go', 'php', 'ruby']
---

# P_SQL_INJECTION: SQL Injection Prevention 🔴

**Severity**: Critical

Always use parameterized queries, never string concatenation.

**Why**: Prevents credential leaks by storing secrets outside code in secure vaults

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **No String Concat Sql**: No string concatenation in SQL

**❌ Bad**:
```
cursor.execute(f'SELECT * FROM users WHERE id={user_id}')  # SQL injection!
```

**✅ Good**:
```
cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))  # Parameterized
```

## Autofix Available


