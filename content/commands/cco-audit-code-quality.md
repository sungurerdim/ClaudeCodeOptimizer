---
description: Code quality, linting, type safety, duplication audit
category: audit
cost: 2
principles: ['U_DRY', 'U_NO_OVERENGINEERING', 'U_FAIL_FAST', 'U_INTEGRATION_CHECK', 'P_LINTING_SAST', 'P_TYPE_SAFETY', 'P_IMMUTABILITY_BY_DEFAULT', 'P_CODE_REVIEW_CHECKLIST_COMPLIANCE', 'P_NO_BACKWARD_COMPAT_DEBT', 'P_PRECISION_IN_CALCS']
---

# cco-audit-code-quality - Code Quality & Standards Audit

**Comprehensive code quality audit: linting, type safety, duplication, and code standards.**

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast linter execution
- Type checker runs
- Duplication detection
- Cost-effective for tool execution

**Analysis**: Sonnet (Plan agent)
- Violation severity assessment
- Pattern analysis
- Fix prioritization

**Execution Pattern**:
1. Launch 2 parallel Haiku agents:
   - Agent 1: Linters & formatters (style, syntax)
   - Agent 2: Type checkers & static analysis (correctness)
2. Aggregate with Sonnet for prioritization
3. Generate fix command recommendations

**Model Requirements**:
- Haiku for scanning (10-15 seconds)
- Sonnet for analysis

---

## Action

Use Task tool to launch parallel code quality audit agents.

### Step 1: Detect Available Tools

**Runtime tool detection** - automatically detect and run available tools.

- **Python**: black, ruff, mypy, pylint, flake8, bandit
- **JavaScript/TypeScript**: prettier, eslint, tslint, tsc
- **Go**: gofmt, goimports, golint, staticcheck
- **Rust**: rustfmt, clippy
- **Other**: Language-specific formatters, linters, type checkers

### Step 2: Parallel Quality Scans

**CRITICAL**: Launch BOTH agents in PARALLEL in a SINGLE message.

#### Agent 1: Linting & Formatting Scan

**Agent 1 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Linting and formatting audit

MUST LOAD FIRST:
1. @CLAUDE.md (Code Quality section)
2. @~/.cco/principles/code-quality.md
3. Print: "✓ Loaded 2 docs (~1,800 tokens)"

Audit principles:
- P_LINTING_SAST: Linting & SAST Enforcement
- U_DRY: DRY Enforcement (code duplication)
- P_CODE_REVIEW_CHECKLIST_COMPLIANCE: Code Review Standards
- U_NO_OVERENGINEERING: No Overengineering

Detect and run available tools:
- Python: black --check ., ruff check .
- JavaScript: prettier --check ., eslint .
- Go: gofmt -l ., golint ./...
- Rust: cargo fmt -- --check, cargo clippy

Scan for:
- Formatting violations (line length, indentation, spacing)
- Linting errors (unused imports, variables, undefined names)
- Code duplication (>50 lines similar code)
- Complexity issues (too many branches, nested loops)
- Dead code (unreachable code, unused functions)
- Magic numbers (hardcoded values)
- Inconsistent naming (camelCase vs snake_case)

Report with:
- Tool name and version
- Violation count by severity
- File:line references
- Suggested fixes
```

#### Agent 2: Type Safety & Static Analysis Scan

**Agent 2 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Type safety and static analysis audit

MUST LOAD FIRST:
1. @CLAUDE.md (Code Quality section)
2. @~/.cco/principles/code-quality.md
3. Print: "✓ Loaded 2 docs (~1,800 tokens)"

Audit principles:
- P_TYPE_SAFETY: Type Safety & Static Analysis
- U_FAIL_FAST: Fail-Fast Error Handling
- P_PRECISION_IN_CALCS: Numeric Precision
- P_IMMUTABILITY_BY_DEFAULT: Immutability Patterns

Detect and run available tools:
- Python: mypy .
- JavaScript: tsc --noEmit
- Go: go vet ./...
- Rust: cargo check

Scan for:
- Missing type annotations (Python, TypeScript)
- Type errors (incompatible types, undefined attributes)
- Null/undefined handling (missing null checks)
- Error handling issues (bare except, unhandled exceptions)
- Mutability issues (mutable defaults, global state)
- Numeric precision issues (float comparisons, integer overflow)
- Security issues (SQL injection, XSS, hardcoded secrets)

Report with:
- Tool name and version
- Error count by type
- File:line references
- Severity (blocking vs warning)
```

### Step 3: Quality Analysis & Prioritization

**After both agents complete**, use Sonnet Plan agent:

**Agent 3 Prompt:**
```
Subagent Type: Plan
Model: sonnet
Description: Code quality analysis

Task: Analyze code quality findings and prioritize fixes.

Input:
- Agent 1 findings (linting & formatting)
- Agent 2 findings (type safety & static analysis)

Analysis steps:
1. Merge all code quality findings
2. Group by severity (CRITICAL > HIGH > MEDIUM > LOW)
3. Identify patterns (same issue in multiple files)
4. Prioritize by: Severity × Spread × Fix Effort
5. Provide specific fix commands
6. Estimate fix effort (hours)
7. Calculate quality debt (total hours)

Output format:
- Findings by severity (CRITICAL > HIGH > MEDIUM > LOW)
- Each finding includes: principle, file:line, issue, fix command
- Master fix plan with priority tiers
- Quality debt estimate (total hours)

Focus on practical, high-impact fixes.
```

---

## Output Format

Report issues with severity and location:

```
Code Quality Audit Results
=========================

CRITICAL (blocking):
  - U_FAIL_FAST: Bare except clause catches all exceptions (src/api.py:45, src/db.py:23)
    Risk: Masks critical errors, hard to debug
    Pattern: 8 instances across codebase
    Command: /cco-fix error-handling --type bare-except --files src/

  - P_TYPE_SAFETY: Missing type annotations (15 functions in src/models.py)
    Risk: Runtime type errors
    Command: /cco-fix types --file src/models.py --strict

HIGH (should fix):
  - P_LINTING_SAST: 23 unused imports (src/)
    Impact: Code clutter
    Command: /cco-fix unused-imports --scope src/

  - U_DRY: Code duplication (src/auth.py:45-98, src/api.py:123-176)
    Duplication: 54 lines similar
    Impact: Bug fixes needed in multiple places
    Command: /cco-fix duplication --files src/auth.py:45-98,src/api.py:123-176 --extract src/shared/auth.py

MEDIUM (recommended):
  - P_LINTING_SAST: 15 formatting violations (line too long)
    Impact: Readability
    Command: /cco-fix formatting --scope all

  - P_CODE_REVIEW_CHECKLIST_COMPLIANCE: Inconsistent naming (src/config.py)
    Issue: Mixed camelCase and snake_case
    Command: /cco-fix naming --file src/config.py --style snake_case

LOW (optional):
  - P_IMMUTABILITY_BY_DEFAULT: Mutable default argument (src/utils.py:34)
    Risk: Shared state bugs
    Command: /cco-fix mutable-defaults --file src/utils.py
```

---

## Recommended Actions

**Analyze results and provide prioritized commands:**

```
🎯 Code Quality Fix Plan (Priority Order)
========================================

IMMEDIATE (CI Blockers):
────────────────────────
1. Fix bare except clauses
   Command: /cco-fix error-handling --type bare-except --files src/
   Impact: CRITICAL - Prevents error masking
   Effort: 1.5 hours
   Pattern: 8 instances

2. Add type annotations
   Command: /cco-fix types --file src/models.py --strict
   Impact: CRITICAL - Prevents runtime errors
   Effort: 2 hours

THIS WEEK (High Priority):
──────────────────────────
3. Remove unused imports
   Command: /cco-fix unused-imports --scope src/
   Impact: HIGH - Code cleanliness
   Effort: 15 minutes (automated)

4. Extract duplicated code
   Command: /cco-fix duplication --files src/auth.py:45-98,src/api.py:123-176 --extract src/shared/auth.py
   Impact: HIGH - Maintainability
   Effort: 2 hours

THIS SPRINT (Quality):
──────────────────────
5. Auto-format codebase
   Command: /cco-fix formatting --scope all
   Impact: MEDIUM - Consistency
   Effort: 5 minutes (automated)

6. Fix naming conventions
   Command: /cco-fix naming --file src/config.py --style snake_case
   Impact: MEDIUM - Consistency
   Effort: 30 minutes

BACKLOG (Minor):
────────────────
7. Fix mutable defaults
   Command: /cco-fix mutable-defaults --file src/utils.py
   Impact: LOW - Edge case prevention
   Effort: 15 minutes

Quality Debt: 6.5 hours | Code Health: 65% → 92%
```

**Command Generation Logic:**
1. **Severity Assessment:**
   - CRITICAL: Blocks CI, causes runtime errors
   - HIGH: Affects maintainability, many instances
   - MEDIUM: Code consistency, readability
   - LOW: Edge cases, minor issues

2. **Priority Tiers:**
   - IMMEDIATE: CI blockers, security issues (fix today)
   - THIS WEEK: Multiple instances, maintainability (fix this week)
   - THIS SPRINT: Consistency, standards (fix this sprint)
   - BACKLOG: Minor issues, edge cases (fix when convenient)

3. **Command Features:**
   - Specific flags: `--severity`, `--files`, `--scope`, `--type`
   - Pattern-based fixes: Fix all instances of same issue
   - Automated fixes: Use `--auto` where safe
   - Estimated impact for each action

4. **Grouping:**
   - Same issue type → Single command with multiple files
   - Same file → Single command with multiple fix types
   - Automated fixes → Batch together

---

## Related Commands

- `/cco-fix code` - Auto-fix code quality issues
- `/cco-audit-security` - Security audit
- `/cco-audit-comprehensive` - Full comprehensive audit
