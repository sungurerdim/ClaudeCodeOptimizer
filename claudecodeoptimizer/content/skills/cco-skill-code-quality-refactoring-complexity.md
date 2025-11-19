---
name: code-quality-refactoring-complexity
description: Manage code quality through complexity reduction and technical debt tracking. Includes cyclomatic/cognitive complexity limits, code smell detection, refactoring patterns (Extract Method, Split Class), and debt prioritization with impact/effort analysis.
keywords: [refactor, complexity, code smell, technical debt, maintainability, cyclomatic, cognitive, duplication, SOLID, clean code]
category: quality
related_commands:
  action_types: [audit, fix, optimize]
  categories: [quality]
pain_points: [1, 2, 3]
---

# Skill: Code Quality & Refactoring

## Purpose

Manage code quality through complexity reduction and technical debt tracking.

**Solves**: Unmaintainable code (complexity >10), technical debt accumulation, code smells, slow feature velocity

**Impact**: High

---

## Principles Included

### P_CODE_SMELL_DETECTION
Automated detection of duplication, long methods, god objects, feature envy

### P_REFACTORING_PATTERNS
Safe refactoring techniques (Extract Method, Replace Conditional) with automated tests

### P_TECHNICAL_DEBT_TRACKING
Quantify, prioritize, schedule debt paydown (interest rate, principal, impact)

### P_CYCLOMATIC_COMPLEXITY_LIMITS
Functions >10 cyclomatic complexity exponentially harder to test/debug

### P_COGNITIVE_COMPLEXITY
Cognitive complexity >15 exceeds working memory capacity

### P_FAIL_FAST_STRATEGY
Fail immediately on invalid conditions vs propagating errors
@content/principles/P_FAIL_FAST_STRATEGY.md

### P_INTEGRATION_CHECK
Prevent dead code, ensure all paths reachable and tested
@content/principles/P_INTEGRATION_CHECK.md

### P_PRODUCTION_GRADE
No TODOs, placeholders, or incomplete implementations in production
@content/principles/P_PRODUCTION_GRADE.md

---

## Activation

Auto-loads on: refactor, complexity, code smell, technical debt, maintainability keywords

---

## Examples

**Complexity Detection**
```
User: "Review this function" (cyclomatic complexity 18)
Result: Flags violation, suggests Extract Method to reduce <10
```

**Code Smell**
```
User: "Class hard to maintain" (1200 lines, 30 methods)
Result: Identifies God Object, suggests Split Class by responsibility
```

**Refactoring**
```
User: "Refactor duplicated code across 5 files"
Result: Applies Extract Function, creates shared module, updates 5 files
```

**Technical Debt**
```
User: "Prioritize TODO comments"
Result: Scans codebase, categorizes by impact/effort, generates paydown roadmap
```

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, fix, optimize]
keywords: [refactor, complexity, code smell, technical debt, SOLID, clean code]
category: quality
pain_points: [1, 2, 3]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: quality`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.

---

## Analysis Patterns (Claude Executes)

When auditing tech debt or code quality, use these analysis patterns:

### Code Smell Detection

```bash
# 1. Large files (>300 lines)
find . -name "*.py" -type f ! -path "*/venv/*" ! -path "*/__pycache__/*" -exec wc -l {} \; | awk '$1 > 300 {print}'

# 2. TODO/FIXME/HACK markers
grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG\|OPTIMIZE" --include="*.py" --include="*.js" --include="*.ts" .

# 3. Console/print statements (debug leftovers)
grep -rn "console\.log\|print(" --include="*.py" --include="*.js" --include="*.ts" .

# 4. Deep nesting (>4 levels)
grep -n "^        " --include="*.py" -r . | grep "if \|for \|while \|try:\|with "

# 5. Parameter bloat (>5 parameters)
grep -rn "def .*(.*, .*, .*, .*, .*)" --include="*.py" .
```

### Complexity Analysis

```bash
# Using radon (if installed)
radon cc -s -a --min C .

# Using flake8 with mccabe
flake8 --max-complexity 10 --select=C901 .

# Manual complexity indicators
grep -rn "if \|elif \|for \|while \|and \|or \|except " --include="*.py" . | \
  awk -F: '{files[$1]++} END {for (f in files) if (files[f] > 15) print f, files[f]}'
```

### Dependency Analysis

```bash
# 1. Outdated packages
pip list --outdated --format=columns

# 2. Unused imports (use ruff)
ruff check --select=F401 .

# 3. Security vulnerabilities
pip-audit  # or: safety check
```

### Dead Code Detection

```bash
# 1. Comprehensive dead code (use vulture)
vulture . --min-confidence 80

# 2. Commented-out code blocks
grep -rn "^#.*def \|^#.*class \|^#.*if \|^#.*for " --include="*.py" .
```

---

## Technical Debt Register Template

```markdown
## Technical Debt Register

| ID | Category | Description | File:Line | Severity | Effort | Interest | Status |
|----|----------|-------------|-----------|----------|--------|----------|--------|
| TD-001 | Quality | Function complexity=18 | {file}:{line} | High | 2h | High | Open |
| TD-002 | Architecture | Tight coupling | {module_a}↔{module_b} | Medium | 4h | Medium | Open |
| TD-003 | Test | Missing payment tests | src/payments/ | Critical | 8h | Critical | Open |

### Severity
- **Critical**: Blocking production quality
- **High**: Fix this sprint
- **Medium**: Fix within month
- **Low**: Fix when convenient

### Interest Rate (cost over time)
- **Critical**: Daily (bugs, incidents)
- **High**: Weekly (slowdowns)
- **Medium**: Monthly (maintenance)
- **Low**: Stable

### Sprint Allocation
- 20% of sprint for debt paydown
- Prioritize: Interest > Severity > Effort
```

---

## Debt Categories

1. **Code Quality** - Complexity, long methods, smells
2. **Architecture** - Coupling, patterns, boundaries
3. **Test** - Missing tests, low coverage, flaky
4. **Documentation** - Missing/outdated docs
5. **Dependency** - Outdated packages, CVEs
6. **Performance** - N+1, no caching, slow algos
7. **Security** - Vulnerabilities, weak auth
8. **Infrastructure** - Manual deploys, no CI/CD
9. **Design** - God objects, feature envy
