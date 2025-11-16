---
id: C_NO_PROACTIVE_DOCS
title: No Proactive Documentation
category: claude-guidelines
severity: medium
weight: 5
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_NO_PROACTIVE_DOCS: No Proactive Documentation 🟡

**Severity**: Medium

Never create documentation files (README.md, CONTRIBUTING.md, API docs, etc.) unless explicitly requested by the user. Ask before creating documentation; respect user's documentation strategy and preferences.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Unsolicited documentation wastes effort and creates conflicts:**

- **Wasted Effort** - User may not want documentation or may want different format/style
- **Conflicts with Existing** - Proactive docs may conflict with established documentation patterns
- **Wrong Format** - User may prefer Markdown, ReStructuredText, AsciiDoc, or no docs at all
- **Wrong Location** - Documentation placement varies (docs/, README, wiki, separate repo)
- **User Control Loss** - User loses control over their documentation strategy
- **Review Overhead** - Unwanted documentation files add review burden

### Core Techniques

**1. Always Ask Before Creating Documentation**

```python
# After completing feature:

# ❌ BAD: Proactively create docs
Write("README.md", usage_guide)
Write("docs/API.md", api_docs)

# ✅ GOOD: Ask user first
"""
Feature complete!

Would you like me to:
1. Update the existing README with usage examples?
2. Create API documentation?
3. Add inline docstrings (no new files)?
4. Nothing - you'll handle docs
"""
```

**2. Inline Documentation is OK (Not File Creation)**

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

**3. Update Existing Docs When Code Changes**

```python
# ✅ GOOD: User changes auth.py, README already documents auth

# Update existing README to reflect changes
Edit("README.md",
     old_string="## Authentication\n\nBasic auth with username/password",
     new_string="## Authentication\n\nSupports username/password and OAuth")

# This is maintaining existing docs, not creating new ones
```

**4. Offer, Don't Assume**

```python
# After significant implementation:

# ❌ BAD: Create docs without asking
Write("ARCHITECTURE.md", system_design_doc)

# ✅ GOOD: Offer to create
"""
Implementation complete. The new microservices architecture is running.

I can create documentation if you'd like:
- Architecture diagrams and explanations
- API endpoint reference
- Deployment guide

Would you like any of these?
"""
```

**5. Respect "No" Answers**

```python
# User: "Add payment processing"
# You: Complete implementation
# You: "Would you like documentation?"
# User: "No, we use Confluence for docs"

# ✅ GOOD: Accept the "no"
# Don't create documentation

# ❌ BAD: Create anyway
Write("docs/payments.md", comprehensive_guide)  # User said no!
```

---

### Implementation Patterns

#### ✅ Good: Ask Before Creating Documentation

```python
# After implementing new API endpoints:

"""
API endpoints complete. All 12 endpoints tested and working.

Would you like me to create documentation? I can:
1. Add OpenAPI/Swagger spec (docs/openapi.yaml)
2. Create README section with endpoint examples
3. Add inline docstrings only (no new files)
4. Nothing - you have your own docs process

Which would you prefer?
"""

# Wait for user choice before creating anything
```

---

#### ✅ Good: Update Existing Docs Only

```python
# User requests feature that's already documented

# Check if README exists
Read("README.md")
# → README exists with "## Features" section

# Update existing documentation
Edit("README.md",
     old_string="## Features\n\n- User authentication\n- Data export",
     new_string="## Features\n\n- User authentication\n- Data export\n- Real-time notifications (NEW)")

# ✅ RESULT: Updated existing docs, didn't create new file
```

---

#### ✅ Good: Inline Documentation (No File Creation)

```python
# Add comprehensive docstrings

# ✅ GOOD: Inline docs don't create files
class PaymentProcessor:
    """
    Process payments through multiple payment gateways.

    Supports Stripe, PayPal, and Square with automatic failover.

    Usage:
        processor = PaymentProcessor(gateway='stripe')
        result = processor.charge(amount=100.00, currency='USD')

    Attributes:
        gateway: Primary payment gateway
        failover_gateways: List of backup gateways
    """

    def charge(self, amount: Decimal, currency: str) -> PaymentResult:
        """
        Charge payment to customer.

        Args:
            amount: Payment amount (must be positive)
            currency: ISO 4217 currency code (e.g., 'USD')

        Returns:
            PaymentResult with transaction ID and status

        Raises:
            PaymentError: Payment processing failed
            ValueError: Invalid amount or currency
        """
        # Implementation...

# ✅ Result: Code is well-documented, no files created
```

---

#### ❌ Bad: Creating README Without Request

```python
# ❌ BAD: Proactive README creation
Write("README.md", """
# My Project

## Installation
...

## Usage
...

## API Reference
...
""")

# Problems:
# - User may already have README
# - User may want different format (RST, AsciiDoc)
# - User may not want README at all
# - User may use external docs (Confluence, Notion)

# ✅ GOOD: Ask first
"""
Implementation complete! Would you like me to create a README file?
"""
```

---

#### ❌ Bad: Creating Multiple Doc Files

```python
# ❌ BAD: Creating comprehensive doc suite without request
Write("README.md", readme_content)
Write("CONTRIBUTING.md", contribution_guide)
Write("CODE_OF_CONDUCT.md", code_of_conduct)
Write("docs/ARCHITECTURE.md", architecture_doc)
Write("docs/API.md", api_reference)
# User only asked for code implementation!

# ✅ GOOD: Implement code, then ask about docs
"""
Feature complete and tested.

I can create documentation if needed:
- README with usage examples
- API reference
- Architecture overview
- Contributing guidelines

Would you like any of these?
"""
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "Helpful" Documentation Creation

**Problem**: Creating docs to be "helpful" without asking.

```python
# ❌ BAD: Assuming user wants docs
Write("docs/getting-started.md", tutorial)
Write("docs/faq.md", faq)
# "I'm just being helpful!"

# ✅ GOOD: Offer to help with docs
"Feature complete. Would you like me to create getting-started docs or FAQ?"
```

**Impact:**
- User may have docs elsewhere (wiki, Confluence)
- May use different format (RST, AsciiDoc)
- Wastes effort if user doesn't want it

---

### ❌ Anti-Pattern 2: Overwriting Existing Docs

**Problem**: Creating documentation files that already exist.

```python
# ❌ BAD: Writing to README without reading first
Write("README.md", new_readme)  # Overwrites existing!

# ✅ GOOD: Read first, then edit
Read("README.md")
Edit("README.md", old_string="...", new_string="...")
```

**Impact:**
- Loss of existing documentation
- User's careful work overwritten
- Potential data loss

---

### ❌ Anti-Pattern 3: Documentation "Just in Case"

**Problem**: Creating placeholder documentation for future features.

```python
# ❌ BAD: Premature documentation
Write("docs/caching.md", "# Caching (Coming Soon)")
Write("docs/api-v2.md", "# API v2 (Planned)")

# ✅ GOOD: Document when implemented, if requested
# Wait until features exist
# Ask user if they want docs
```

**Impact:**
- Stale placeholder docs
- Confusion about what exists vs planned
- Maintenance burden for non-existent features

---

## Implementation Checklist

### Before Creating Documentation Files

- [ ] **Ask user first** - "Would you like documentation for this feature?"
- [ ] **Check existing** - Read existing README/docs to avoid conflicts
- [ ] **Clarify format** - Ask about preferred format (Markdown, RST, etc.)
- [ ] **Clarify location** - Where should docs go? (docs/, wiki, README section?)
- [ ] **Get explicit approval** - Wait for "yes" before creating

### What's OK Without Asking

- [ ] **Inline docstrings** - Function/class documentation in code
- [ ] **Code comments** - Explaining complex logic in comments
- [ ] **Type hints** - Adding types to function signatures
- [ ] **Updating existing docs** - Updating README when code changes
- [ ] **Commit messages** - Documenting changes in git history

### What's NOT OK Without Asking

- [ ] **README.md** - Never create without explicit request
- [ ] **CONTRIBUTING.md** - Only if user requests
- [ ] **API documentation files** - Ask first
- [ ] **Architecture docs** - Only if requested
- [ ] **Guides/tutorials** - Ask before creating

---

## Summary

**No Proactive Documentation** means never creating documentation files (README, API docs, guides) unless explicitly requested. Always ask first, respect user's documentation strategy, and only create when user approves.

**Core Rules:**

- **Ask before creating** - Never create doc files without explicit request
- **Inline docs OK** - Docstrings and code comments don't need approval
- **Edit existing OK** - Updating existing docs is maintenance, not creation
- **Respect "no"** - If user declines docs, don't create them
- **Offer, don't assume** - Provide options, let user choose
