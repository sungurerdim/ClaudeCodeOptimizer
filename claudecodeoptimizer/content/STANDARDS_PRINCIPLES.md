# CCO Principle Format Guide

**Purpose:** Standard format for all CCO principle files (Universal, Claude-specific, Project).

**Scope:** Format guide ONLY - content of each principle is unique.

---

## Standard Principle Structure

```markdown
# {PREFIX}_{PRINCIPLE_NAME}: {Title}

**Severity**: {Critical|High|Medium|Low}

{One-sentence description of what this principle enforces}

---

## Why

{2-5 sentences: Why does this principle exist? What problems does it prevent?}

{Optional: Statistics/data supporting the principle}

---

## Rules

{3-7 concise rules that define the principle}

- ✅ {Rule 1 - what TO do}
- ✅ {Rule 2 - what TO do}
- ❌ {Rule 3 - what NOT to do}
- ❌ {Rule 4 - what NOT to do}

---

## Examples

### ❌ Bad - {Violation Description}

\`\`\`{language}
{code-demonstrating-violation}
\`\`\`

### ✅ Good - {Compliance Description}

\`\`\`{language}
{code-demonstrating-compliance}
\`\`\`

{Repeat for 2-5 example pairs}

---

## Checklist

Before {claiming-compliance-condition}:

- [ ] {Verification step 1}
- [ ] {Verification step 2}
- [ ] {Verification step 3}
- [ ] {Verification step 4}
- [ ] {Verification step 5}

---

## References (Optional)

- **Related Principles:** {list-of-related-principles}
- **Documentation:** {external-links}
- **Tools:** {tools-that-help-enforce-this}
```

---

## Naming Convention

### Prefixes

- **U_** - Universal principles (apply everywhere)
  - Example: `U_DRY`, `U_EVIDENCE_BASED_ANALYSIS`, `U_MINIMAL_TOUCH`

- **C_** - Claude Code specific principles (Claude AI usage)
  - Example: `C_EFFICIENT_FILE_OPERATIONS`, `C_CONTEXT_WINDOW_MGMT`

- **P_** - Project/Domain principles (software engineering best practices)
  - Example: `P_TEST_COVERAGE`, `P_SQL_INJECTION`, `P_API_VERSIONING`

### Name Format

- ALL_CAPS_SNAKE_CASE
- Descriptive but concise
- Max 4 words
- Examples:
  - `U_DRY` (short, clear)
  - `U_EVIDENCE_BASED_ANALYSIS` (descriptive)
  - `C_CONTEXT_WINDOW_MGMT` (specific to Claude)
  - `P_CONTAINER_SECURITY` (domain-specific)

---

## Severity Levels

**Critical:**
- Violations cause immediate failures, security risks, or data corruption
- MUST be enforced at all times
- Examples: `U_EVIDENCE_BASED_ANALYSIS`, `U_NO_HARDCODED_EXAMPLES`

**High:**
- Violations cause significant quality/performance/maintenance issues
- SHOULD be enforced in most cases
- Examples: `U_DRY`, `U_MINIMAL_TOUCH`, `C_EFFICIENT_FILE_OPERATIONS`

**Medium:**
- Violations cause moderate issues or technical debt
- RECOMMENDED to enforce
- Examples: `P_CODE_DOCUMENTATION_STANDARDS`, `P_SEMANTIC_VERSIONING`

**Low:**
- Violations cause minor issues or style inconsistencies
- OPTIONAL enforcement
- Examples: Style guides, naming conventions (if not critical)

---

## Section Requirements

### Required Sections

1. **Title** - Prefix + Name + Human-readable title
2. **Severity** - Critical/High/Medium/Low
3. **Why** - Justification for the principle
4. **Rules** - Specific, actionable rules
5. **Examples** - Bad/Good code pairs
6. **Checklist** - Verification steps

### Optional Sections

1. **References** - Links to related materials
2. **Anti-Patterns** - Common violations (if not covered in Examples)
3. **Edge Cases** - Special scenarios
4. **Exceptions** - When to break the rule

---

## Content Guidelines

### "Why" Section

```markdown
# ✅ GOOD: Specific, quantifiable
## Why

Prevents 60%+ production bugs caused by assumption-based development.
Symptom fixing creates whack-a-mole debugging. Band-aids accumulate
technical debt leading to 3x maintenance costs.

# ❌ BAD: Vague
## Why

This is important for code quality.
```

### "Rules" Section

```markdown
# ✅ GOOD: Specific, actionable
- ✅ Verify all changes with command execution (exit code 0)
- ✅ Complete accounting: total = completed + skipped + failed
- ❌ Never claim "fixed" without file verification
- ❌ Never trust agent output blindly

# ❌ BAD: Vague
- Be thorough
- Check your work
- Don't make mistakes
```

### "Examples" Section

```markdown
# ✅ GOOD: Real-world, specific
### ❌ Bad - Assumption Without Verification

\`\`\`python
# ❌ Claim fix without proof
agent_result = Task("Fix auth bug")
# No verification!
\`\`\`

### ✅ Good - Evidence-Based Verification

\`\`\`python
# ✅ Verify fix applied
agent_result = Task("Fix auth bug")
content = Read("auth.py", offset=145, limit=20)
assert "session['user_id']" in content  # Verify
\`\`\`

# ❌ BAD: Toy examples
### ❌ Bad
\`\`\`python
x = 1
y = 2
\`\`\`

### ✅ Good
\`\`\`python
x = 2
y = 3
\`\`\`
```

### "Checklist" Section

```markdown
# ✅ GOOD: Verifiable, specific
- [ ] Ran grep to find ALL affected points (grep -r "old_name")
- [ ] Created TODO for each affected file/location
- [ ] Verified each change (grep old_name in file = 0 results)
- [ ] Final verification: grep -r "old_name" returns 0 results
- [ ] Verified new name exists where expected

# ❌ BAD: Vague
- [ ] Did the work
- [ ] Checked everything
- [ ] It works
```

---

## File Size Guidelines

**Target:** 100-200 lines per principle
**Maximum:** 300 lines per principle

**If exceeding:**
- Split into multiple related principles
- Move verbose examples to external documentation
- Reference rather than duplicate

---

## Cross-References

### Principle Dependencies

When a principle relies on another:

```markdown
## References

**Depends On:**
- `U_EVIDENCE_BASED_ANALYSIS` - Must verify before claiming compliance
- `C_EFFICIENT_FILE_OPERATIONS` - Use three-stage discovery

**Related:**
- `U_DRY` - Avoid duplicating this principle's checks
- `U_MINIMAL_TOUCH` - Apply only to affected files
```

### Skill/Command References

When a principle is enforced by specific skills/commands:

```markdown
## References

**Enforced By:**
- `/cco-audit --{category}` - Checks compliance
- `/cco-fix --{category}` - Auto-fixes violations

**Related Skills:**
- `cco-skill-{name}` - Provides detection patterns
- `cco-skill-{name}` - Provides fix patterns
```

---

## Version Control

### Updating Principles

When updating a principle:

1. Update content following format guide
2. Add note at bottom:
   ```markdown
   ---
   **Last Updated:** YYYY-MM-DD
   **Changes:** {summary-of-changes}
   ```

3. Update any dependent principles/skills/commands
4. Verify all references still accurate

### Deprecating Principles

When removing a principle:

1. Mark as deprecated in title:
   ```markdown
   # U_OLD_PRINCIPLE: Old Principle [DEPRECATED]

   **Status:** DEPRECATED - Use `U_NEW_PRINCIPLE` instead
   **Deprecated:** YYYY-MM-DD
   **Removal:** YYYY-MM-DD (3 months notice)
   ```

2. Update all references to new principle
3. Remove after notice period

---

## Quality Checklist

Before merging principle changes:

**Structure:**
- [ ] Proper prefix (U_, C_, P_)
- [ ] ALL_CAPS_SNAKE_CASE name
- [ ] Severity level set
- [ ] All required sections present

**Content:**
- [ ] "Why" section explains justification with data/impact
- [ ] Rules are specific and actionable (not vague)
- [ ] Examples show real-world scenarios (not toys)
- [ ] Checklist items are verifiable (not subjective)
- [ ] File size within limits (<300 lines)

**Quality:**
- [ ] No hardcoded examples (use placeholders)
- [ ] No contradictions with other principles
- [ ] Cross-references accurate
- [ ] Examples use correct format (❌ Bad / ✅ Good)

---

## References

- **Quality Standards:** `COMMAND_QUALITY_STANDARDS.md`
- **Agent Standards:** `AGENT_STANDARDS.md`
- **Command Patterns:** `COMMAND_PATTERNS.md`
- **Skill Standards:** `SKILL_STANDARDS.md`

---

**Last Updated:** 2025-01-24
**Status:** Active - All principles SHOULD follow this format
