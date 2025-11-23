# CCO Skill Standards - Skill Development & Format Guide

**Purpose:** Define standard structure, format, and quality requirements for ALL CCO skills.

**DRY Principle:** Define skill format once, all skills follow the same structure.

---

## How to Use in Skill Files

```markdown
---
name: {skill-slug}
description: {One-line description with key techniques and outcomes}
keywords: [{keyword1}, {keyword2}, ...]
category: {security|testing|database|infrastructure|docs|performance|quality}
related_commands:
  action_types: [{audit|fix|generate|optimize}]
  categories: [{category-list}]
pain_points: [{pain-point-numbers}]
---

# {Skill Title}

{One-sentence description of what this skill provides}

**See [SKILL_STANDARDS.md](../SKILL_STANDARDS.md) for:**
- Standard Section Structure
- Code Example Format
- Detection Pattern Format
- Anti-Pattern Format
- Checklist Format

---

## Domain

{Which types of systems/code this skill applies to}

---

## Purpose

{Why this skill exists, what problems it solves, key context}

---

## Core Techniques

### 1. {Technique Name}

{Description}

**Code Examples:**
\`\`\`{language}
# ❌ BAD: {what's wrong}
{bad-example}

# ✅ GOOD: {what's right}
{good-example}
\`\`\`

**Detection Pattern:**
\`\`\`python
def detect_{issue}(code: str) -> List[Finding]:
    """Detect {issue} in code."""
    findings = []
    # Detection logic
    return findings
\`\`\`

---

## Anti-Patterns

### ❌ {Anti-Pattern Name}

**Problem:** {What's wrong}

**Example:**
\`\`\`{language}
{bad-code}
\`\`\`

**Fix:** {How to fix}

---

## Checklist

Before merging code:
- [ ] {Check 1}
- [ ] {Check 2}
- [ ] {Check 3}

---

## References

- **Documentation:** {links}
- **Tools:** {tools-used}
- **Related Skills:** {other-skills}
```

---

## Standard Skill Structure

Every skill MUST follow this structure:

### 1. Frontmatter (Required)

```yaml
---
name: {slug-format}
description: {One-line with key outcomes}
keywords: [{10-15 relevant keywords}]
category: {primary-category}
related_commands:
  action_types: [{which-commands-use-this}]
  categories: [{which-categories}]
pain_points: [{pain-point-numbers-addressed}]
---
```

**Naming Convention:**
- Slug format: `{category}-{focus}-{subtopics}`
- Example: `security-owasp-xss-sqli-csrf`
- Example: `database-optimization-caching-profiling`

**Categories:**
- `security` - Security, auth, encryption, access control
- `testing` - Unit, integration, E2E, load, chaos
- `database` - Queries, indexes, migrations, optimization
- `infrastructure` - CI/CD, Docker, K8s, deployment
- `docs` - API docs, ADR, runbooks, docstrings
- `performance` - Caching, profiling, bundle optimization
- `quality` - Code quality, refactoring, tech debt
- `observability` - Logging, metrics, alerts, tracing
- `architecture` - Patterns, microservices, event-driven

### 2. Title & Description (Required)

```markdown
# {Skill Title} - Descriptive but Concise

{One-sentence purpose statement}
```

### 3. Domain Section (Required)

```markdown
## Domain

{1-2 sentences: What types of systems/code does this skill apply to?}

Examples:
- "Web applications, APIs, authentication systems, data validation"
- "Microservices architectures, event-driven systems, message queues"
- "SQL databases, ORMs, query optimization, database migrations"
```

### 4. Purpose Section (Required)

```markdown
## Purpose

{2-5 sentences: Why does this skill exist? What problems does it solve?}

**Key context:**
- {Context point 1}
- {Context point 2}
- {Context point 3}
```

### 5. Core Techniques Section (Required)

```markdown
## Core Techniques

### 1. {Technique Name}

**{Brief description of technique}**

**Code Examples:**
\`\`\`{language}
# ❌ BAD: {Specific problem}
{bad-code-example}

# ✅ GOOD: {Specific solution}
{good-code-example}
\`\`\`

**Why This Matters:**
{1-2 sentences on impact}

**Detection Pattern:**
\`\`\`python
def detect_{issue}(code: str) -> List[Finding]:
    """
    Detect {issue} in code.

    Args:
        code: Source code to analyze

    Returns:
        List of Finding objects with file, line, severity
    """
    findings = []

    # Pattern 1: {description}
    pattern = r'{regex-pattern}'
    for match in re.finditer(pattern, code):
        findings.append(Finding(
            severity="{critical|high|medium|low}",
            line=get_line_number(match),
            code=match.group(),
            risk="{specific-risk-description}",
            fix="{specific-fix-recommendation}"
        ))

    return findings
\`\`\`

### 2. {Next Technique}

{Repeat structure}
```

### 6. Anti-Patterns Section (Required)

```markdown
## Anti-Patterns

### ❌ {Anti-Pattern Name}

**Problem:** {What's wrong and why it matters}

**Example:**
\`\`\`{language}
{demonstrative-bad-code}
\`\`\`

**Impact:**
- {Consequence 1}
- {Consequence 2}

**Fix:**
\`\`\`{language}
{demonstrative-good-code}
\`\`\`

### ❌ {Next Anti-Pattern}

{Repeat structure}
```

### 7. Checklist Section (Required)

```markdown
## Checklist

Before claiming this area is secure/optimized/complete:

- [ ] {Verification step 1}
- [ ] {Verification step 2}
- [ ] {Verification step 3}
- [ ] {Verification step 4}
- [ ] {Verification step 5}

**Minimum:** 5 checkpoints
**Maximum:** 15 checkpoints
```

### 8. References Section (Optional but Recommended)

```markdown
## References

**Documentation:**
- [{Tool/Framework} Official Docs]({url})
- [{Standard} Specification]({url})

**Tools:**
- `{tool-name}` - {what-it-does}
- `{tool-name}` - {what-it-does}

**Related Skills:**
- `{skill-name}` - {why-related}
- `{skill-name}` - {why-related}
```

---

## Code Example Format Standards

### Bad/Good Pattern (Required Format)

```markdown
**{Context about the scenario}:**

\`\`\`{language}
# ❌ BAD: {Specific problem this example demonstrates}
{bad-code}
# {Optional: Why this is bad inline comment}

# ✅ GOOD: {Specific solution this example demonstrates}
{good-code}
# {Optional: Why this is good inline comment}
\`\`\`

**Impact:** {Consequences of bad vs benefits of good}
```

### Real-World Examples (Preferred)

```python
# ✅ Use realistic scenarios
# Example: User authentication endpoint
@app.route('/api/login')
def login():
    username = request.json.get('username')
    # ... realistic code ...

# ❌ Avoid toy examples
# Example: foo/bar variables
def process(foo):
    bar = foo + 1
    return bar
```

### Placeholder Usage

```python
# Use {PLACEHOLDERS} for variable parts
user_id = request.args.get('{PARAM_NAME}')
query = f"SELECT * FROM {TABLE_NAME} WHERE {COLUMN} = {VALUE}"

# NOT hardcoded examples
user_id = request.args.get('user_id')  # ❌ Hardcoded
```

---

## Detection Pattern Format Standards

### Standard Template

```python
def detect_{issue_name}(file_path: str) -> List[Finding]:
    """
    Detect {issue-name} in {file-type} files.

    Looks for:
    - {Pattern 1 description}
    - {Pattern 2 description}
    - {Pattern 3 description}

    Args:
        file_path: Path to file to analyze

    Returns:
        List of Finding objects with severity, line, code, risk, fix
    """
    findings = []
    content = Read(file_path)

    # Pattern 1: {Specific pattern description}
    pattern_1 = r'{regex-or-description}'
    matches = Grep(pattern_1, path=file_path, output_mode="content", "-n": True)

    for match in matches:
        findings.append(Finding(
            severity="{critical|high|medium|low}",
            file=file_path,
            line=match.line_number,
            code=match.content,
            risk="{specific-risk-explanation}",
            fix="{actionable-fix-recommendation}"
        ))

    # Pattern 2: {Next pattern}
    # ...

    return findings
```

### Severity Guidelines

- **Critical:** Exploitable security vulnerabilities, data loss risk
- **High:** Security weaknesses, performance degradation, broken functionality
- **Medium:** Code quality issues, tech debt, maintainability problems
- **Low:** Style violations, minor improvements, nice-to-haves

### Risk Description Format

```python
# ✅ GOOD: Specific, actionable
risk="SQL injection: User input concatenated into query allows attackers to modify query logic and exfiltrate data"

# ❌ BAD: Vague
risk="Security issue"
```

### Fix Recommendation Format

```python
# ✅ GOOD: Actionable with code
fix="Use parameterized queries: db.execute('SELECT * FROM users WHERE id = ?', (user_id,))"

# ❌ BAD: Vague
fix="Fix the query"
```

---

## Anti-Pattern Format Standards

### Template

```markdown
### ❌ {Anti-Pattern Name}

**Problem:** {What's wrong - be specific}

**Example:**
\`\`\`{language}
# Code demonstrating the anti-pattern
{bad-code}
\`\`\`

**Why This Fails:**
- {Reason 1 with specific impact}
- {Reason 2 with specific impact}

**Correct Approach:**
\`\`\`{language}
# Code demonstrating the solution
{good-code}
\`\`\`

**Benefits:**
- {Benefit 1 of correct approach}
- {Benefit 2 of correct approach}
```

---

## Checklist Format Standards

### Structure

```markdown
## Checklist

**Before claiming {area} is {status}:**

**{Category 1}:**
- [ ] {Specific verification step}
- [ ] {Specific verification step}

**{Category 2}:**
- [ ] {Specific verification step}
- [ ] {Specific verification step}

**Verification:**
- [ ] {How to verify compliance}
- [ ] {How to measure success}
```

### Checklist Item Quality

```markdown
# ✅ GOOD: Specific, verifiable
- [ ] All API endpoints require authentication (verify with: grep '@app.route' | grep -v '@require_auth')
- [ ] Database queries use parameterized statements (no string concatenation detected)
- [ ] Test coverage > 80% (run: pytest --cov)

# ❌ BAD: Vague, unverifiable
- [ ] Code is secure
- [ ] Tests exist
- [ ] Performance is good
```

---

## File Size Limits

**Target:** 400-500 lines per skill
**Maximum:** 600 lines per skill

**If exceeding maximum:**
- Split into multiple related skills
- Extract verbose examples to separate documentation
- Reference external documentation rather than duplicating

---

## Quality Checklist for Skills

Before merging a skill file:

**Structure:**
- [ ] Frontmatter complete with all required fields
- [ ] All required sections present (Domain, Purpose, Core Techniques, Anti-Patterns, Checklist)
- [ ] Sections in correct order

**Content:**
- [ ] Code examples use Bad/Good format consistently
- [ ] Detection patterns follow standard template
- [ ] Anti-patterns include both problem and solution
- [ ] Checklist items are specific and verifiable
- [ ] No hardcoded examples (use placeholders)

**Quality:**
- [ ] Real-world examples (not toy foo/bar code)
- [ ] Specific risk descriptions (not vague)
- [ ] Actionable fix recommendations (with code)
- [ ] File size within limits (< 600 lines)

**References:**
- [ ] Documentation links valid
- [ ] Tools mentioned are accessible
- [ ] Related skills accurately referenced

---

## Maintenance

**When updating skills:**
1. Verify structure still matches SKILL_STANDARDS.md
2. Update version date in frontmatter (if exists)
3. Ensure examples use current best practices
4. Verify detection patterns still work
5. Update related skills if necessary

**When creating new skills:**
1. Copy template from SKILL_STANDARDS.md
2. Fill in all required sections
3. Follow format standards exactly
4. Run through quality checklist
5. Get review before merging

---

## References

- **Quality Standards:** `COMMAND_QUALITY_STANDARDS.md`
- **Agent Standards:** `AGENT_STANDARDS.md`
- **Command Patterns:** `COMMAND_PATTERNS.md`
- **Principle Format:** `PRINCIPLE_FORMAT.md`

---

**Last Updated:** 2025-01-23
**Version:** 1.0.0
**Status:** Active - All skills MUST comply
