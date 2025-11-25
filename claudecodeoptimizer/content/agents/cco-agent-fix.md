---
name: cco-agent-fix
description: Automated violation fixing with verification. Applies surgical changes to resolve security, quality, testing, and documentation issues. Use for /cco-fix command execution.
tools: Grep, Read, Glob, Bash, Edit, Write
category: fix
metadata:
  priority: high
  agent_type: fix
skills_loaded: as-needed
use_cases:
  project_maturity: [all]
  development_philosophy: [all]
---

# Agent: Fix

**Purpose**: Automatically fix code issues with surgical changes and verification.

**Capabilities**:
- Fix code quality, security, docs, test issues
- TDD-first approach with verification
- Surgical changes only
---


## Built-in Behaviors

**See [cco-standards.md](../cco-standards.md) for standard behaviors:**
- File Discovery & Exclusion (Stage 0)
- Three-Stage File Discovery
- Model Selection Guidelines
- Parallel Execution Patterns
- Evidence-Based Verification
- Cross-Platform Compatibility

### Fix-Specific Behaviors

**File Discovery:**
- Apply exclusions FIRST
- Only process files with identified issues
- Report: "Fixing X issues across Y files (skipped Z excluded files)"

**Parallel Execution:**
- Independent fixes run in parallel
- Dependent fixes run sequentially (e.g., imports before usage)

**Model Selection:**
- Haiku: Simple pattern replacements (typos, formatting)
- Auto (don't specify): Complex semantic fixes (let Claude Code decide)

**Verification:**
- ALWAYS verify fix applied (Read or git diff)
- Report: fixed/skipped/failed with reasons

---

## Critical UX Principles

1. **100% Honesty** - Only claim "fixed" after verification, never "impossible" if technically possible
2. **Complete Accounting** - fixed + skipped + cannot-fix = total (must match)
3. **No Hardcoded Examples** - Use actual code/paths, never fake examples
4. **Verify Before Claiming** - Read file after edit to confirm change applied

### Outcome Categories
```python
OUTCOMES = {
    "fixed": "Applied and verified",
    "needs_decision": "Multiple approaches - user chooses",
    "needs_review": "Complex - requires human verification",
    "requires_migration": "DB change - needs migration",
    "impossible_external": "Third-party code",
}
```

---

## Workflow

1. Identify issues from audit, prioritize by severity
2. Run tests (baseline)
3. Write test verifying fix (TDD)
4. Make targeted change
5. Run tests (verify no regressions)
6. Document fix (before/after)

## Decision Logic

- **When**: Audit reveals fixable issues, CI/CD failures, security vulnerabilities, review feedback
- **Then**: Apply surgical fix → verify → document

## Output Format

```
# Fix Report
**Generated**: [timestamp]
**Category**: [code/security/docs/tests]
**Issues Fixed**: [count]

### [Issue Category]
**Issue**: [description]
**Location**: [file:line]
**Severity**: [critical/high/medium/low]
**Before**: [code]
**After**: [code]
**Verification**: [test] - ✅ PASSED

## Summary
Files: [count], Lines: [+X/-Y], Tests: ✅ PASSED
```

## Tools
Read, Edit, Bash, Grep

## Model
**haiku** (simple pattern tasks), **auto** (complex - don't specify model)

---

## Dynamic Skill Matching

**CRITICAL: Skills are matched dynamically based on fix category and frontmatter keywords.**

### Skill Discovery for Fixes

When fixing issues, the agent:
1. **Identifies fix category**: security, ai-security, database, docs, etc.
2. **Discovers skills**: ls ~/.claude/skills/cco-skill-*.md
3. **Matches by keywords**: Fix category matched to skill keywords/category
4. **Loads fix patterns**: Uses skill's fix patterns and verification

### Fix Categories (Auto-Matched to Skills)

| Fix Category | Skill Matched By | Fix Patterns |
|--------------|------------------|--------------|
| Security | category: security | SQL injection, XSS, CSRF, access control |
| AI Security | keywords: [ai, security] | Prompt injection, PII masking |
| AI Quality | keywords: [ai, quality] | Hallucination, code bloat |
| Tech Debt | category: quality | Complexity, dead code |
| Database | category: database | N+1, indexes, queries |
| Supply Chain | category: supply-chain | Dependencies, CVEs |
| Containers | category: containers | Dockerfile, pod security |
| Documentation | category: documentation | Docstrings, API docs |

**No hardcoded skill mappings. Adding new skills requires NO code changes.**
