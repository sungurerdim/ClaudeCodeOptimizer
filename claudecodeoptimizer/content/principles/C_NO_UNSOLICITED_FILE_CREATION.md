# C_NO_UNSOLICITED_FILE_CREATION: No Unsolicited File Creation

**Severity**: High

Never create files (especially documentation) unless explicitly requested or genuinely required. Always prefer editing existing files.

---

## Why

Unsolicited file creation causes project clutter, review overhead, wrong format/location, user control loss, maintenance burden, and git history noise.

---

## Decision Framework

Before creating ANY file:
```
❓ Can I edit existing file instead?
❓ Does similar functionality exist?
❓ Is this genuinely new domain logic?
❓ Did user explicitly request new file?
❓ Is this documentation? (Always ask first!)

If any NO → Don't create
```

---

## Patterns

### 1. Prefer Editing Existing
```python
# Task: Add logging utility

# ❌ BAD: Create without checking
Write("src/utils/logger.py", code)

# ✅ GOOD: Check existing
Grep("logger|logging", output_mode="files_with_matches")
# → src/utils/helpers.py has logging

# Edit existing
Edit("src/utils/helpers.py", ...)
```

### 2. Never Create Temp Files
```bash
# ❌ BAD: Temporary files
Write("test.py", experimental_code)
Write("temp.txt", debug_output)

# ✅ GOOD
# - Test in existing files
# - Use logging, not temp files
```

### 3. Always Ask for Docs
```bash
# ❌ BAD: Create without request
Write("README.md", guide)
Write("CONTRIBUTING.md", guidelines)

# ✅ GOOD: Ask first
"Feature complete. Create documentation?
1. Update existing README?
2. Create API docs?
3. Add inline docstrings (no files)?
4. Nothing - you handle docs"
```

### 4. Inline Docs OK (No Files)
```python
# ✅ GOOD: Inline docstrings
def authenticate_user(username: str, password: str) -> AuthResult:
    """
    Authenticate user with credentials.

    Args:
        username: User's email or username
        password: Plain text password (will be hashed)

    Returns:
        AuthResult with user data and token
    """
    # Implementation...
```

---

## Legitimate Exceptions

### ✅ User Explicitly Requested
```
User: "Create new payments module"
✅ Create: src/payments/processor.py
```

### ✅ Genuinely New Domain
```
User: "Add payment processing"
No existing payment code
✅ Create: src/payments/
```

### ✅ Architectural Requirement
```
User: "Add middleware layer"
✅ Create: src/middleware/
```

### ✅ File Size Limit
```
Existing file would exceed 1000 lines
✅ Split into new file
```

---

## Anti-Patterns

### ❌ Creating "Just in Case"
```python
# ❌ BAD: Preemptive
Write("src/utils/cache.py", stub)  # Not needed yet
Write("config/production.yaml", stub)  # Not deploying

# ✅ GOOD: Create when needed
```

### ❌ One-Function Files
```bash
# ❌ BAD: Excessive granularity
src/utils/format_date.py      # 5 lines
src/utils/format_currency.py  # 8 lines

# ✅ GOOD: Cohesive
src/utils/formatters.py  # All formatters
```

### ❌ Unsolicited Docs
```bash
# ❌ BAD: Proactive docs
Write("README.md", guide)
Write("ARCHITECTURE.md", design)

# ✅ GOOD: Ask first
"Implementation complete. Create documentation?"
```

---

## Checklist

### Before Creating ANY File
- [ ] Search for existing files (Grep/Glob)
- [ ] Can edit existing instead?
- [ ] Truly necessary?
- [ ] User explicitly requested?
- [ ] Documentation? (ALWAYS ask)

### Avoid Creating
- [ ] Temp files (test.py, temp.txt, debug.log)
- [ ] Single-function files
- [ ] Premature configs
- [ ] Unsolicited docs (README, CONTRIBUTING)
- [ ] Duplicate utilities

### OK Without Asking
- [ ] Inline docstrings
- [ ] Code comments
- [ ] Type hints
- [ ] Updating existing docs
- [ ] Commit messages
