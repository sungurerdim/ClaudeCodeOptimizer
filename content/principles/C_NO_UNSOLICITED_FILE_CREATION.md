---
id: C_NO_UNSOLICITED_FILE_CREATION
title: No Unsolicited File Creation
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_NO_UNSOLICITED_FILE_CREATION: No Unsolicited File Creation 🔴

**Severity**: High

Never create files (especially documentation) unless explicitly requested or genuinely required for new functionality. Always prefer editing existing files. Ask before creating documentation; respect user's file management strategy.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Unsolicited file creation causes codebase pollution and workflow disruption:**

- **Project Clutter** - Unnecessary files pollute project structure
- **Review Overhead** - Reviewers must examine every new file
- **Wrong Format/Location** - User may have specific requirements (Markdown vs RST, docs/ vs wiki)
- **User Control Loss** - User loses control over documentation/file management strategy
- **Maintenance Burden** - Every file requires ongoing maintenance
- **Git History Noise** - Unnecessary files clutter git history

---

## Core Techniques

### 1. Before Creating ANY File, Ask:

```
❓ Can I edit an existing file instead?
❓ Does similar functionality already exist?
❓ Is this genuinely new domain logic?
❓ Did the user explicitly request a new file?
❓ Is this documentation? (Always ask first!)

If any answer is "No" → Don't create the file
```

### 2. Prefer Editing Existing Files

```python
# Task: Add logging utility

# ❌ BAD: Create new file without checking
Write("src/utils/logger.py", logging_code)

# ✅ GOOD: Check for existing files first
Grep("logger|logging", output_mode="files_with_matches")
# → src/utils/helpers.py has logging functions

# Edit existing file instead
Edit("src/utils/helpers.py", ...)
```

### 3. Never Create Temporary/Experimental Files

```bash
# ❌ BAD: Creating temporary files
Write("test.py", experimental_code)
Write("temp.txt", debug_output)
Write("scratch.js", trying_something)

# ✅ GOOD: Use existing files or don't create at all
# - Test in existing test files
# - Use logging instead of temp output files
# - Experiment in existing modules
```

### 4. Always Ask Before Creating Documentation

```bash
# ❌ BAD: Creating docs without request
Write("README.md", usage_guide)        # Unsolicited
Write("CONTRIBUTING.md", guidelines)    # Unsolicited
Write("docs/API.md", api_documentation) # Unsolicited

# ✅ GOOD: Ask first
"I've completed the feature. Would you like me to:
1. Update the existing README with usage examples?
2. Create API documentation?
3. Add inline docstrings (no new files)?
4. Nothing - you'll handle docs"
```

### 5. Inline Documentation is OK (No File Creation)

```python
# ✅ GOOD: Inline docstrings don't create files
def authenticate_user(username: str, password: str) -> AuthResult:
    """
    Authenticate user with credentials.

    Args:
        username: User's email or username
        password: Plain text password (will be hashed)

    Returns:
        AuthResult with user data and token

    Raises:
        AuthenticationError: Invalid credentials
    """
    # Implementation...

# ✅ GOOD: Code comments are fine
# TODO: Add rate limiting (per user request)
```

---

## Implementation Patterns

### ✅ Good: Edit Existing File Instead of Creating New

```python
# Task: Add email validation

# Step 1: Search for existing validation code
Grep("validate|validator", output_mode="files_with_matches")
# → src/utils/validators.py exists!

# Step 2: Edit existing file
Edit("src/utils/validators.py",
     old_string="# Validators module",
     new_string="# Validators module\n\ndef validate_email(email: str) -> bool:\n    ...")

# ✅ Result: No new file created, functionality added to existing file
```

---

### ✅ Good: Ask Before Creating Documentation

```python
# After implementing feature:

# ❌ BAD: Proactively create docs
Write("docs/new_feature.md", documentation)

# ✅ GOOD: Ask user first
"""
Feature complete! The new authentication system is working.

Would you like me to:
1. Update the existing README with usage examples?
2. Create API documentation?
3. Add inline code comments only?
"""
```

---

### ✅ Good: Update Existing Docs When Code Changes

```python
# User changes auth.py, README already documents auth

# Update existing README to reflect changes
Edit("README.md",
     old_string="## Authentication\n\nBasic auth with username/password",
     new_string="## Authentication\n\nSupports username/password and OAuth")

# This is maintaining existing docs, not creating new ones
```

---

## Anti-Patterns

### ❌ Creating Files "Just in Case"

```python
# ❌ BAD: Preemptive file creation
Write("src/utils/cache.py", cache_stub)     # No caching needed yet
Write("src/models/user_stats.py", stub)     # Not implemented yet
Write("config/production.yaml", stub_config) # Not deploying yet

# ✅ GOOD: Create only when genuinely needed
# Wait until caching is actually required
# Wait until user stats feature is implemented
# Wait until production deployment is imminent
```

**Impact:**
- Clutters codebase with unused files
- Creates false impression of completeness
- Files become stale and outdated

---

### ❌ One-Function Files

```bash
# ❌ BAD: Excessive file granularity
src/utils/format_date.py      # 5 lines
src/utils/format_currency.py  # 8 lines
src/utils/format_phone.py     # 6 lines

# ✅ GOOD: Cohesive single file
src/utils/formatters.py  # 30 lines, all formatters together
```

**Impact:**
- File proliferation
- Import complexity
- Navigation overhead

---

### ❌ Unsolicited Documentation Files

```bash
# ❌ BAD: Proactive doc creation
Write("README.md", comprehensive_guide)
Write("ARCHITECTURE.md", system_design)
Write("API_DOCS.md", api_reference)
# User only asked for code implementation!

# ✅ GOOD: Ask first
"Implementation complete. Would you like me to create documentation?"
```

**Impact:**
- May conflict with existing docs
- User may have specific doc requirements
- Wastes effort if user doesn't want it

---

## Implementation Checklist

### Before Creating ANY File

- [ ] **Search for existing** - Grep/Glob for similar files
- [ ] **Can I edit instead?** - Check if existing file can be extended
- [ ] **Is this truly necessary?** - Could functionality live elsewhere?
- [ ] **Did user request this?** - Explicit request or implicit requirement?
- [ ] **Is this documentation?** - ALWAYS ask before creating docs

### File Types to AVOID Creating

- [ ] **Temporary files** - test.py, temp.txt, scratch.md, debug.log
- [ ] **Single-function files** - One file per small function
- [ ] **Premature configs** - Configs for features not yet built
- [ ] **Unsolicited docs** - README, CONTRIBUTING, API docs without request
- [ ] **Duplicate utilities** - When existing utils file could be extended

### When Creation IS Justified

- [ ] **User explicitly requested** - "Create a new payments module"
- [ ] **Genuinely new domain** - First file for new major feature area
- [ ] **Architectural requirement** - New layer (middleware, controllers)
- [ ] **File size limit** - Existing file would exceed 1000 lines
- [ ] **Clear separation** - Functionality genuinely unrelated to existing files

### What's OK Without Asking

- [ ] **Inline docstrings** - Function/class documentation in code
- [ ] **Code comments** - Explaining complex logic in comments
- [ ] **Type hints** - Adding types to function signatures
- [ ] **Updating existing docs** - Updating README when code changes
- [ ] **Commit messages** - Documenting changes in git history

---

## Summary

**No Unsolicited File Creation** means never creating files (especially documentation) unless explicitly requested or genuinely required. Always prefer editing existing files, and always ask before creating documentation.

**Core Rules:**

- **Edit first** - Always prefer editing existing files over creating new
- **Search before create** - Grep/Glob for existing files that could be extended
- **Ask for docs** - Never create documentation files without user request
- **No temp files** - Never create temporary, debug, or experimental files
- **Justify creation** - Every new file should be necessary for the task
- **Inline docs OK** - Docstrings and code comments don't need approval
- **Respect "no"** - If user declines docs, don't create them
