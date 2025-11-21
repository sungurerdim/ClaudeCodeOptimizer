---
name: no-hardcoded-examples
description: Never use hardcoded examples in templates; AI models interpret them as real data
type: universal
severity: critical
keywords: [templates, placeholders, examples, AI models, code generation]
category: [quality, workflow]
---

# U_NO_HARDCODED_EXAMPLES: No Hardcoded Examples in Templates

**Severity**: Critical

Never use hardcoded examples in commands, skills, agents, or principles. AI models interpret them as real data and use them literally.

---

## Why

AI models cannot distinguish between "example" and "real data" in context. Hardcoded examples like `src/auth/login.py:45` get used as-is, causing incorrect file references, wrong line numbers, and fabricated issues.

---

## Rules

### Use Placeholders Always

```python
# ❌ BAD: Hardcoded (AI uses as-is)
"file": "src/auth/login.py"
"line": 45
"function": "authenticate()"
"table": "users"
"column": "email"

# ✅ GOOD: Placeholders
"file": "{FILE_PATH}"
"line": "{LINE_NUMBER}"
"function": "{FUNCTION_NAME}"
"table": "{TABLE_NAME}"
"column": "{COLUMN_NAME}"
```

### Placeholder Naming Convention

```python
# File/Location
{FILE_PATH}, {LINE_NUMBER}, {DIRECTORY}

# Code Elements
{FUNCTION_NAME}, {CLASS_NAME}, {VARIABLE_NAME}, {METHOD_NAME}

# Database
{TABLE_NAME}, {COLUMN_NAME}, {INDEX_NAME}, {QUERY}

# Values
{COUNT}, {PERCENTAGE}, {DURATION}, {SIZE}

# Descriptive
{ISSUE_DESCRIPTION}, {ERROR_MESSAGE}, {REASON}
```

### When Generating Output

```python
# ❌ BAD: Return template as-is
return "SQL Injection in auth.py:45"

# ✅ GOOD: Use actual data
return f"{finding.issue} in {finding.file}:{finding.line}"
```

---

## Self-Enforcement

This principle applies to:
1. **CCO component definitions** - Commands, skills, agents must use placeholders
2. **Runtime execution** - When components run, they must use actual project data
3. **Output generation** - All reports must contain real findings, not examples

### Verification

Before finalizing any CCO component:
```python
# Check for hardcoded patterns
FORBIDDEN_PATTERNS = [
    r"src/\w+/\w+\.py",      # Hardcoded Python paths
    r":\d{2,3}",              # Hardcoded line numbers
    r"def \w+\(\)",           # Hardcoded function names
    r"users\.\w+",            # Hardcoded table.column
    r"@example\.com",         # Hardcoded domains
]

for pattern in FORBIDDEN_PATTERNS:
    if re.search(pattern, content):
        raise ValueError(f"Hardcoded example found: {pattern}")
```

---

## Examples

### ❌ Bad - Skill with Hardcoded Examples

```markdown
## SQL Injection Detection

Look for patterns like:
- `User.objects.filter(email=request.GET['email'])`
- `db.execute(f"SELECT * FROM users WHERE id={user_id}")`
```

### ✅ Good - Skill with Placeholders

```markdown
## SQL Injection Detection

Look for patterns like:
- `{MODEL}.objects.filter({FIELD}=request.GET['{PARAM}'])`
- `db.execute(f"SELECT * FROM {TABLE} WHERE {COLUMN}={VARIABLE}")`
```

### ❌ Bad - Command Output

```markdown
Found 3 issues:
- SQL Injection in api/users.py:45
- Missing index on users.email
- N+1 query in models/order.py:89
```

### ✅ Good - Command Output

```markdown
Found {ISSUE_COUNT} issues:
- {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}
- {ISSUE_TYPE} on {TABLE_NAME}.{COLUMN_NAME}
- {ISSUE_TYPE} in {FILE_PATH}:{LINE_NUMBER}
```

---

## Checklist

- [ ] No specific file paths (use `{FILE_PATH}`)
- [ ] No specific line numbers (use `{LINE_NUMBER}`)
- [ ] No specific function/class names (use `{FUNCTION_NAME}`, `{CLASS_NAME}`)
- [ ] No specific table/column names (use `{TABLE_NAME}`, `{COLUMN_NAME}`)
- [ ] No specific domains/emails (use `{DOMAIN}`, `{EMAIL}`)
- [ ] No specific numeric values without context (use `{COUNT}`, `{THRESHOLD}`)
- [ ] Runtime outputs use actual project data
