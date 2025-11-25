# CCO Standards - Unified Standards Document

**Purpose:** Single source of truth for all CCO component standards.

**Scope:** Commands, Agents, Skills, Principles

---

## Section 1: Core Principles

### 1.1 Priority Order

1. **UX/DX** - User experience comes first
2. **Process Standardization** - Consistent, predictable behavior
3. **Output Quality** - Accurate, reliable results
4. **Token Efficiency** - Minimum context usage
5. **Simplicity** - Minimum complexity

### 1.2 Model Selection

**Model selection is delegated to Claude:**
- Claude manages its own effort parameter
- Extended thinking is automatically active
- Agents do not specify model
- Model parameter in Task() is optional

---

## Section 2: Command Standards

### 2.1 Execution Guarantee

Every command that performs operations must include:

```markdown
## Execution Guarantee

This command executes the FULL operation as planned.
No scope reduction due to time constraints.

**Estimated time:** Provided for transparency, NOT to limit scope.
```

### 2.2 Step 0: Introduction & Confirmation

Every command must start with user confirmation:

```python
AskUserQuestion({
  questions: [{
    question: "Ready to start {command}?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {label: "Start", description: "Begin {action}"},
      {label: "Cancel", description: "Exit"}
    ]
  }]
})
```

**CRITICAL:**
- Cancel → Exit immediately
- Start → Continue

### 2.3 Native UI Tools

**REQUIRED: All user interactions via AskUserQuestion:**

```python
# ❌ FORBIDDEN: Text-based prompts
print("Ready to proceed? (y/n)")

# ✅ REQUIRED: AskUserQuestion
AskUserQuestion({...})
```

**MultiSelect MUST include "All" option:**

```python
options: [
  {label: "All", description: "Select all options"},
  {label: "Security", description: "..."},
  {label: "Testing", description: "..."}
]
```

### 2.4 File Discovery Protocol

**Exclusion lists MUST be applied FIRST:**

```python
EXCLUDED_DIRS = [
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".pytest_cache", "dist", "build", ".next", "target",
    "bin", "obj", ".egg-info", "coverage", ".tox"
]

EXCLUDED_FILES = [
    "package-lock.json", "yarn.lock", "poetry.lock",
    "*.min.js", "*.min.css", "*.map",
    "*.pyc", "*.so", "*.dll", "*.exe", "*.log"
]
```

### 2.5 Concise Reporting

```markdown
## Summary

**Metric 1:** {VALUE}
**Metric 2:** {VALUE}

{2-3 sentence interpretation}
```

### 2.6 Cross-Platform Compatibility

```bash
# ❌ BAD: Backslashes
cd C:\Users\project

# ✅ GOOD: Forward slashes
cd C:/Users/project

# ❌ BAD: Redundant cd
cd "D:/GitHub/Project" && ruff check .

# ✅ GOOD: Direct execution
ruff check .
```

### 2.7 Parallel Execution

```python
# ✅ GOOD: Parallel (single message)
Task("Analyze module A")
Task("Analyze module B")
Task("Analyze module C")
# All run simultaneously

# ❌ BAD: Sequential
Task("Analyze module A")  # Wait
Task("Analyze module B")  # Wait
```

### 2.8 Complete Accounting

```python
# Formula: total = completed + skipped + failed + cannot_do
assert len(completed) + len(skipped) + len(failed) + len(cannot_do) == total
```

### 2.9 No Hardcoded Examples

```python
# ❌ BAD: Hardcoded
"file": "src/auth/login.py"

# ✅ GOOD: Placeholders
"file": "{FILE_PATH}"
```

---

## Section 3: Agent Standards

### 3.1 Agent Frontmatter

```yaml
---
name: cco-agent-{name}
description: {One-line description}
tools: {tool-list}
---
```

### 3.2 Three-Stage File Discovery

```python
# Stage 1: Discovery (~10 tokens)
Grep("pattern", output_mode="files_with_matches")

# Stage 2: Preview (~100 tokens)
Grep("pattern", path=file, output_mode="content", "-C": 3)

# Stage 3: Precise Read (~50 tokens)
Read(file, offset=start-5, limit=20)
```

### 3.3 Evidence-Based Verification

```python
# NEVER trust agent output blindly
agent_result = Task("Fix bug")

# ALWAYS verify
content = Read(file, offset=line, limit=10)
assert expected_fix in content
```

### 3.4 Outcome Categories

```python
OUTCOMES = {
    "fixed": "Change applied AND verified",
    "generated": "File created AND exists",
    "needs_decision": "Multiple approaches - user must choose",
    "needs_review": "Complex change - review required",
    "impossible_external": "Issue in third-party code"
}
```

---

## Section 4: Skill Standards

### 4.1 Skill Frontmatter

```yaml
---
name: cco-skill-{slug}
description: {One-line with key outcomes}
keywords: [{10-15 keywords}]
category: {security|testing|database|quality|...}
related_commands:
  action_types: [{audit|fix|generate|optimize}]
pain_points: [{1,2,3...}]
---
```

### 4.2 Standard Sections

1. **Domain** - What systems this applies to
2. **Purpose** - Why it exists, what it solves
3. **Core Techniques** - Key techniques with ❌/✅ examples
4. **Anti-Patterns** - Patterns to avoid
5. **Checklist** - Verification steps

### 4.3 Code Example Format

```python
# ❌ BAD: {Specific problem}
{bad-code}

# ✅ GOOD: {Specific solution}
{good-code}
```

### 4.4 File Size Limits

- **Target:** 400-500 lines
- **Maximum:** 600 lines

---

## Section 5: Principle Standards

### 5.1 Prefix Conventions

- **CCO_C_*** - Claude Code behavior (always active)
- **CCO_U_*** - Universal standards (always active)
- **P_*** - Domain-specific (lazy-load with skills)

### 5.2 Severity Levels

- **Critical:** Immediate failure, security risk
- **High:** Significant quality/performance issues
- **Medium:** Moderate technical debt
- **Low:** Minor style inconsistencies

### 5.3 Standard Structure

```markdown
# {PREFIX}_{NAME}: {Title}

**Severity**: {Level}

{One-sentence description}

## Why
{Justification}

## Rules
- ✅ {Do this}
- ❌ {Don't do this}

## Examples
### ❌ Bad
### ✅ Good

## Checklist
- [ ] {Verification step}
```

---

## Section 6: Error Handling

### 6.1 Agent Error Pattern

```python
try:
    result = Task(...)
except Exception as e:
    AskUserQuestion({
        questions: [{
            question: f"Agent failed: {e}. How to proceed?",
            header: "Error",
            options: [
                {label: "Retry", description: "Try again"},
                {label: "Skip", description: "Continue without"},
                {label: "Cancel", description: "Stop operation"}
            ]
        }]
    })
```

### 6.2 File Error Pattern

```python
try:
    Read(file_path)
except FileNotFoundError:
    skipped.append((file_path, "Not found"))
except PermissionError:
    failed.append((file_path, "Permission denied"))
```

---

## Section 7: Performance Targets

### 7.1 Time Targets

- **Discovery:** < 30 seconds
- **Quick mode:** < 5 minutes
- **Full scan:** < 30 minutes
- **Per-category:** < 3 minutes

### 7.2 Token Targets

- **Three-stage vs full read:** 42x reduction
- **Targeted Read:** ~50 tokens (vs 1000+ full)

---

## Section 8: Quality Checklist

Verification for each component:

### Commands
- [ ] Execution Guarantee
- [ ] Step 0 Confirmation
- [ ] Native UI Tools (AskUserQuestion)
- [ ] MultiSelect has "All"
- [ ] File Discovery with exclusions
- [ ] Complete Accounting
- [ ] No hardcoded examples
- [ ] Cross-platform paths

### Agents
- [ ] Three-stage discovery
- [ ] Evidence-based verification
- [ ] Outcome categorization
- [ ] No model specification

### Skills
- [ ] Standard frontmatter
- [ ] All required sections
- [ ] ❌/✅ example pairs
- [ ] Checklist items
- [ ] < 600 lines

### Principles
- [ ] Correct prefix (CCO_C_, CCO_U_, P_)
- [ ] Severity level
- [ ] Why section with justification
- [ ] Actionable rules
- [ ] Real-world examples
- [ ] Verifiable checklist

---

## References

**Principles:** `~/.claude/principles/CCO_*.md`
**Commands:** `~/.claude/commands/cco-*.md`
**Skills:** `~/.claude/skills/cco-skill-*.md`
**Agents:** `~/.claude/agents/cco-agent-*.md`

---

**Last Updated:** 2025-11-25
**Status:** Active - All CCO components MUST comply
