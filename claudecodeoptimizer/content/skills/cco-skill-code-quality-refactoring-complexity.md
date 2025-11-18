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
