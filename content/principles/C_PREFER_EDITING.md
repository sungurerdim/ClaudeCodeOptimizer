---
id: C_PREFER_EDITING
title: Prefer Editing Over Creating
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_PREFER_EDITING: Prefer Editing Over Creating 🔴

**Severity**: High

Always prefer editing existing files over creating new ones. Search for existing implementations first, add to existing files when possible, and only create new files when editing is genuinely not viable.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Creating files instead of editing causes codebase bloat and fragmentation:**

- **Codebase Bloat** - Unnecessary new files cause exponential growth: 1000-file codebase becomes 2000 files unnecessarily
- **Duplication** - New files often duplicate logic from existing files, violating DRY principle
- **Fragmentation** - Related functionality scattered across many files is harder to understand and maintain
- **Review Difficulty** - New files are harder to review than edits; reviewers must understand entirely new context
- **Navigation Overhead** - More files = more time searching and navigating the codebase
- **Merge Conflicts** - New files are less likely to conflict, hiding integration issues that edits would surface

### Core Techniques

**1. Search for Existing Files First**

Before creating, always search for existing files that could be edited:

```bash
# Task: Add email validation function

# Step 1: Search for existing validation code
Grep("def validate", output_mode="files_with_matches")
# → src/utils/validators.py exists!

Grep("validate.*email|email.*valid",
     path="src/utils/validators.py",
     output_mode="content",
     "-C": 3)
# → Found email validation helpers in validators.py

# Step 2: Edit existing file
Read("src/utils/validators.py", offset=50, limit=100)
Edit("src/utils/validators.py",
     old_string="# Email validation helpers",
     new_string="# Email validation helpers\n\ndef validate_email_format(email: str) -> bool:\n    ...")

# ✅ GOOD: Added to existing validators.py
# ❌ BAD: Creating new email_validator.py
```

**2. Use Edit Tool for Existing Files**

Always use Edit tool instead of Write tool for existing files:

```python
# ❌ BAD: Using Write on existing file (overwrites entire file!)
Write("src/config.py", new_complete_content)  # DANGEROUS!

# ✅ GOOD: Using Edit to modify specific section
Edit("src/config.py",
     old_string="MAX_RETRIES = 3",
     new_string="MAX_RETRIES = 5")
```

**3. Decision Tree: Edit vs Create**

```
Should I create a new file?
  ↓
Does similar functionality exist?
  Yes → Find existing file → Edit it ✅
  No → ↓
Would this fit in an existing file?
  Yes → Add to existing file → Edit it ✅
  No → ↓
Is this genuinely new module/domain?
  Yes → Create new file (document why) ✅
  No → Find closest existing file → Edit it ✅
```

**4. When Editing is Appropriate**

Edit existing files when:

- Adding new function to existing module
- Updating configuration values
- Adding new test cases to existing test file
- Extending existing class with new methods
- Adding new route to existing API file
- Updating documentation in existing docs
- Fixing bugs in existing code

**5. When Creating is Appropriate**

Create new files only when:

- Introducing genuinely new domain concept (e.g., new `payments` module when only `auth` exists)
- File would exceed reasonable size (>500-1000 lines)
- New functionality is unrelated to any existing file
- Architecture requires new layer (e.g., new `middleware/` directory)
- User explicitly requests new file structure

---

### Implementation Patterns

#### ✅ Good: Edit Existing Utilities File

```python
# Task: Add date formatting utility

# Step 1: Search for existing utilities
Grep("def format|def parse", output_mode="files_with_matches")
# → src/utils/formatters.py exists

# Step 2: Read existing file
Read("src/utils/formatters.py")
# Contains: format_currency(), format_phone(), parse_json()

# Step 3: Edit to add new function
Edit("src/utils/formatters.py",
     old_string="""def parse_json(json_str: str) -> dict:
    \"\"\"Parse JSON string with error handling.\"\"\"
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise ValueError(f"Invalid JSON: {e}") from e""",
     new_string="""def parse_json(json_str: str) -> dict:
    \"\"\"Parse JSON string with error handling.\"\"\"
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise ValueError(f"Invalid JSON: {e}") from e

def format_date(date: datetime, fmt: str = "%Y-%m-%d") -> str:
    \"\"\"Format datetime object as string.\"\"\"
    if not isinstance(date, datetime):
        raise TypeError(f"Expected datetime, got {type(date)}")
    return date.strftime(fmt)""")

# ✅ RESULT: Added to existing formatters.py
# ❌ AVOIDED: Creating new date_formatter.py
```

**Why this is good:**
- Functionality grouped with related formatters
- Easier to find (all formatters in one place)
- Simpler imports (`from utils.formatters import format_date`)
- Maintains existing file structure

---

#### ✅ Good: Add Test to Existing Test File

```python
# Task: Add test for new login feature

# ❌ BAD: Create new test file
Write("tests/test_login_new_feature.py", test_code)  # Fragments tests!

# ✅ GOOD: Edit existing test file
Grep("def test.*login", output_mode="files_with_matches")
# → tests/test_auth.py already has login tests

Read("tests/test_auth.py", offset=200, limit=50)
Edit("tests/test_auth.py",
     old_string="""class TestLogin:
    def test_login_success(self):
        # ...

    def test_login_invalid_credentials(self):
        # ...""",
     new_string="""class TestLogin:
    def test_login_success(self):
        # ...

    def test_login_invalid_credentials(self):
        # ...

    def test_login_with_mfa_enabled(self):
        \"\"\"Test login when MFA is enabled.\"\"\"
        user = create_user_with_mfa()
        response = login(user.email, user.password)
        assert response.requires_mfa is True
        assert response.mfa_token is not None""")

# ✅ RESULT: Tests stay together in test_auth.py
```

**Why this is good:**
- All login tests in one file
- Easy to find related tests
- Shared setup/fixtures available
- Test runner runs related tests together

---

#### ❌ Bad: Creating New File for Single Function

```python
# Task: Add email validation

# ❌ BAD: Create new single-function file
Write("src/utils/email_validator.py", """
def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
""")

# ✅ GOOD: Add to existing validators.py
Grep("validate", output_mode="files_with_matches")
# → src/utils/validators.py exists

Edit("src/utils/validators.py",
     old_string="# Add new validators below",
     new_string="""# Add new validators below

def validate_email(email: str) -> bool:
    \"\"\"Validate email format.\"\"\"
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None""")
```

**Why creating was bad:**
- Single-function file adds overhead
- `import` now requires two paths instead of one
- Future validators scattered across multiple files
- Harder to discover existing validators

---

#### ❌ Bad: Creating Near-Duplicate Files

```python
# ❌ BAD: Creating similar files
Write("src/api/users.py", user_routes)
Write("src/api/posts.py", post_routes)
Write("src/api/comments.py", comment_routes)
# All follow same pattern, could be in one routes.py

# ✅ GOOD: One cohesive routes file
Edit("src/api/routes.py",
     old_string="# API routes",
     new_string="""# API routes

# User routes
@app.route('/users/<id>')
def get_user(id):
    ...

# Post routes
@app.route('/posts/<id>')
def get_post(id):
    ...

# Comment routes
@app.route('/comments/<id>')
def get_comment(id):
    ...""")
```

**Why creating was bad:**
- Three files with similar structure
- Import overhead: `from api.users import *; from api.posts import *; ...`
- Harder to see all routes at once
- Duplication of route setup logic

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Create-First Mentality

**Problem**: Creating new files without searching for existing ones.

```python
# Task: Add JSON parsing utility

# ❌ BAD: Immediately create new file
Write("src/utils/json_parser.py", json_parsing_code)

# ✅ GOOD: Search first, then edit
Grep("json|parse", output_mode="files_with_matches")
# → src/utils/parsers.py exists
Edit("src/utils/parsers.py", ...)  # Add JSON parsing to existing file
```

**Impact:**
- Codebase bloats with unnecessary files
- Related functionality fragmented
- Duplicate code across multiple files

---

### ❌ Anti-Pattern 2: One Function Per File

**Problem**: Creating separate file for every small function.

```bash
# ❌ BAD: Excessive file creation
src/utils/format_date.py       # Single function
src/utils/format_currency.py   # Single function
src/utils/format_phone.py      # Single function
src/utils/format_address.py    # Single function

# ✅ GOOD: Cohesive grouping
src/utils/formatters.py  # All format functions together
```

**Impact:**
- 4 files instead of 1
- 4 imports instead of 1: `from utils.formatters import format_date, format_currency, ...`
- Harder to discover related utilities

---

### ❌ Anti-Pattern 3: Test File Per Feature

**Problem**: Creating new test file for every small feature.

```bash
# ❌ BAD: Test fragmentation
tests/test_login.py
tests/test_login_mfa.py          # Should be in test_login.py
tests/test_login_oauth.py        # Should be in test_login.py
tests/test_login_password_reset.py  # Should be in test_login.py

# ✅ GOOD: Cohesive test organization
tests/test_auth.py  # All authentication tests together
  - TestLogin
    - test_login_success
    - test_login_mfa
    - test_login_oauth
    - test_login_password_reset
```

**Impact:**
- 4 test files instead of 1
- Shared test fixtures duplicated across files
- Harder to run all login tests together

---

## Implementation Checklist

### Before Creating a File

- [ ] **Search existing files** - Grep/Glob for similar functionality
- [ ] **Check related modules** - Look in expected directory (utils/, models/, api/)
- [ ] **Review file sizes** - Would edit make file too large? (>500-1000 lines)
- [ ] **Consider cohesion** - Does new function fit thematically with existing file?
- [ ] **Document decision** - If creating, note why editing wasn't viable

### When Editing

- [ ] **Use Edit tool** - Never use Write on existing files
- [ ] **Read file first** - Use Read to see current contents
- [ ] **Match style** - Follow existing patterns (naming, formatting, organization)
- [ ] **Add to appropriate section** - Place new code with related functionality
- [ ] **Update imports** - If needed, add new imports at top of file

### When Creating is Justified

- [ ] **New domain concept** - Genuinely new module (e.g., first `payments/` module)
- [ ] **File size limit** - Editing would exceed reasonable size (>1000 lines)
- [ ] **Architectural separation** - New layer required (e.g., `middleware/auth.py`)
- [ ] **User request** - User explicitly requested new file structure
- [ ] **Document rationale** - Add comment or commit message explaining why new file was necessary

---

## Summary

**Prefer Editing Over Creating** means always searching for and editing existing files before creating new ones. Only create new files when editing is genuinely not viable due to size, architectural separation, or new domain concepts.

**Core Rules:**

- **Search first** - Grep/Glob for existing files before creating
- **Edit existing** - Use Edit tool to add to existing files
- **Create sparingly** - Only create when editing truly isn't viable
- **Document creation** - Explain why new file was necessary
- **Group cohesively** - Related functionality belongs in same file
