---
id: C_NO_UNNECESSARY_FILES
title: No Unnecessary File Creation
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_NO_UNNECESSARY_FILES: No Unnecessary File Creation 🔴

**Severity**: High

Never create files unless absolutely necessary for achieving the task goal. Always prefer editing existing files, and only create new files when genuinely required for new functionality or architectural separation.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Unnecessary file creation causes codebase pollution:**

- **Project Clutter** - Unnecessary files (temp files, experimental code, unused utilities) pollute project structure
- **Review Overhead** - Reviewers must examine every new file; unnecessary files waste review time
- **False Complexity** - More files suggest more complexity even when functionality is simple
- **Discoverability Issues** - Developers searching for functionality must check more files
- **Maintenance Burden** - Every file requires ongoing maintenance, even if barely used
- **Git History Noise** - Unnecessary files clutter git history and blame logs

### Core Techniques

**1. Before Creating ANY File, Ask These Questions:**

```
❓ Can I edit an existing file instead?
❓ Does similar functionality already exist?
❓ Is this genuinely new domain logic?
❓ Would this file have >50 lines of content?
❓ Did the user explicitly request a new file?

If any answer is "No" → Don't create the file
```

**2. Prefer Editing Existing Files**

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

**3. Never Create Temporary/Experimental Files**

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

**4. Don't Create Documentation Files Proactively**

```bash
# ❌ BAD: Creating docs without request
Write("README.md", usage_guide)        # Unsolicited
Write("CONTRIBUTING.md", guidelines)    # Unsolicited
Write("docs/API.md", api_documentation) # Unsolicited

# ✅ GOOD: Ask first
"I've completed the feature. Would you like me to update the README with usage examples?"
```

**5. Don't Create Configuration Files Unless Required**

```bash
# ❌ BAD: Creating configs "just in case"
Write(".prettierrc", config)      # User didn't ask
Write(".eslintignore", patterns)  # Not needed yet
Write("tsconfig.json", ts_config) # No TypeScript files exist!

# ✅ GOOD: Only create when genuinely needed
# User: "Add TypeScript support"
Write("tsconfig.json", minimal_config)  # Now justified
```

---

### Implementation Patterns

#### ✅ Good: Edit Existing File Instead of Creating New

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

#### ✅ Good: Ask Before Creating Documentation

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
3. Add inline code comments?
"""
```

---

#### ❌ Bad: Creating Unnecessary Utility Files

```python
# ❌ BAD: Creating single-purpose utility files
Write("src/utils/date_formatter.py", "def format_date...")  # 1 function
Write("src/utils/string_helper.py", "def capitalize...")    # 1 function
Write("src/utils/math_utils.py", "def round_decimal...")    # 1 function

# ✅ GOOD: Add to existing utils or create one cohesive file
Edit("src/utils/formatters.py",
     old_string="# Formatters",
     new_string="""# Formatters

def format_date(date):
    ...

def capitalize(text):
    ...

def round_decimal(num):
    ...""")
```

---

#### ❌ Bad: Creating Temporary/Debug Files

```python
# ❌ BAD: Leaving temporary files
Write("debug_output.txt", debug_data)
Write("test_temp.py", experimental_code)
Write("scratch.md", notes)

# ✅ GOOD: Don't create these files at all
# - Use logging instead of debug files
# - Experiment in existing test files
# - Use comments in code for notes
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Creating Files "Just in Case"

**Problem**: Creating files for functionality that might be needed later.

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

### ❌ Anti-Pattern 2: One-Function Files

**Problem**: Creating separate file for every small function.

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

### ❌ Anti-Pattern 3: Unsolicited Documentation Files

**Problem**: Creating documentation the user didn't request.

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
- [ ] **>50 lines of content?** - Will file have substantial content?

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

---

## Summary

**No Unnecessary File Creation** means never creating files unless absolutely necessary. Always prefer editing existing files, and only create when genuinely required for new functionality, architectural separation, or explicit user request.

**Core Rules:**

- **Edit first** - Always prefer editing existing files over creating new
- **Search before create** - Grep/Glob for existing files that could be extended
- **Ask for docs** - Never create documentation files without user request
- **No temp files** - Never create temporary, debug, or experimental files
- **Justify creation** - Every new file should be necessary for the task
