---
name: cco-review
description: Strategic architecture review with fresh perspective
---

# /cco-review

**Strategic review** - Understand intent → analyze architecture → compare with ideal → recommend improvements.

## Pre-Operation

Before starting:
1. Check `git status` for uncommitted changes
2. If dirty, AskUserQuestion: → Commit first / Stash / Continue anyway

## Project Context

**First:** Run `/cco-calibrate` to ensure context is loaded.

Read `CCO_CONTEXT_START` block from project root `CLAUDE.md` (NOT `.claude/CLAUDE.md`). Follow the Guidelines listed there.

## Flow

1. **Map Current State** - Analyze architecture, patterns, dependencies
2. **Identify Gaps** - Compare purpose vs implementation
3. **Stack Fitness** - Evaluate tech choices against purpose
4. **Fresh Perspective** - "If building from scratch" recommendations
5. **Prioritize** - Quick wins vs major refactors, risk assessment
6. **Report** - Structured findings with actionable items

## Phase 1: Map Current State

Analyze:
- Directory structure and organization
- Module boundaries and responsibilities
- Dependency graph (internal and external)
- Entry points and data flow
- Patterns in use (design patterns, conventions)
- Test structure and coverage areas
- Configuration and environment handling

Output: **Architecture Map** (what the project actually is)

## Phase 2: Gap Analysis

Compare Intent vs Implementation:
- Features promised but not implemented
- Implemented but not documented
- Overcomplicated vs stated simplicity goals
- Missing vs stated patterns
- Scope creep beyond stated goals

Check against CLAUDE.md principles:
- DRY violations
- Orphan code (unused functions, dead imports)
- Complexity violations (cyclomatic >10)
- Missing type annotations
- Test coverage gaps
- Security principle violations

Output: **Gap Report** with file:line references

## Phase 3: Stack Fitness & Fresh Perspective

### 3a: Stack Fitness (Purpose vs Current Choices)

Evaluate current technology choices against North Star purpose and constraints:

**Evaluate each major choice:**

| Current Choice | Serves Purpose? | Better Alternative? | Why? |
|----------------|-----------------|---------------------|------|
| Language | ✓/✗ | If ✗, suggest | Reasoning |
| Framework | ✓/✗ | If ✗, suggest | Reasoning |
| Database | ✓/✗ | If ✗, suggest | Reasoning |
| Architecture | ✓/✗ | If ✗, suggest | Reasoning |
| Key dependencies | ✓/✗ | If ✗, suggest | Reasoning |

**Questions to ask:**
- Is this language/framework the best fit for this purpose?
- Is it compatible with stated constraints (performance, team size)?
- Does it make meeting success criteria easier or harder?
- Is there a simpler/better alternative?

**Example output format:**
```
❌ {current_choice} → {recommended_alternative}
↳ Purpose: "{project_purpose}"
↳ {reason_current_doesnt_fit}
↳ Context: {relevant_context_from_calibration}

✓ {current_choice} appropriate
↳ Purpose: "{project_purpose}"
↳ Current choice aligns with purpose
```

### 3b: From Scratch Perspective

Answer: "If I were building this project from scratch today, knowing everything I now know..."

Consider:
- Would I use the same directory structure?
- Would I organize modules differently?
- Are there simpler patterns for the same goals?
- What abstractions are over/under-engineered?
- Which decisions were right vs accidental complexity?

Categories:
- **Structure** - Directory layout, module organization
- **Patterns** - Design patterns, conventions, idioms
- **Abstractions** - Too much, too little, wrong level
- **Data Flow** - How data moves through the system
- **Testing** - Strategy, coverage, maintainability
- **DX** - Developer experience, onboarding, tooling

Output: **Stack Fitness Report** + **"From Scratch" Recommendations**

## Phase 4: Prioritization

Classify each recommendation:

**By Effort:**
- Quick Win (< 1 hour, single file)
- Small Refactor (< 1 day, few files)
- Medium Refactor (< 1 week, module-level)
- Major Refactor (> 1 week, cross-cutting)

**By Impact:**
- Critical - Blocks goals or causes failures
- High - Significantly improves quality/DX
- Medium - Noticeable improvement
- Low - Nice to have

**By Risk:**
- Safe - No behavior change, easy rollback
- Low - Minimal behavior change
- Medium - Some behavior change, needs testing
- High - Significant change, needs careful review

Priority = Impact / Effort (prefer high impact, low effort, low risk)

## Report Structure

```
## Context
Team: {team} | Scale: {scale} | Data: {data} | Type: {type}
Purpose: {purpose}

**Calibration:** [Standard/Relaxed/Strict rigor] because [context reason].

## Architecture Overview
[Current state - structure, patterns, key decisions]

## Stack Fitness
| Choice | Verdict | Recommendation |
|--------|---------|----------------|
| Language | ✓/✗ | Alternative if needed |
| Framework | ✓/✗ | Alternative if needed |
| Database | ✓/✗ | Alternative if needed |
| Architecture | ✓/✗ | Alternative if needed |

## Gap Analysis
- [gap]: [file:line] - [details]
  ↳ Context: {field}: {value} → {why}

## Recommendations by Priority
[Grouped by: Critical → Quick Wins → Medium → Nice to Have]

## What's Working Well
[Positive observations - patterns to keep]
```

## Approval & Apply Flow

**Follow CCO Approval Flow standard from cco-standards.**

Apply to: recommendations from review analysis.

### Apply Selected

For each approved recommendation:
1. Show what will change (files, scope)
2. Make the changes
3. Verify (tests pass, lint clean)
4. Report: done + skipped + failed = total

### Recommendation Types

**Auto-applicable (can apply directly):**
- Directory restructuring
- File moves/renames
- Pattern standardization
- Dead code removal
- Import reorganization

**Requires discussion (present plan, ask before each):**
- API changes
- Data model changes
- Major refactors
- Dependency changes

## Flags

- `--quick` - Phase 1-3 only, skip "from scratch" analysis
- `--deep` - Include line-by-line code review
- `--focus=X` - Focus on specific area (structure, patterns, deps, tests, security, dx)
- `--report-only` - Show report without offering to apply changes
- `--auto-apply` - Auto-apply safe recommendations without asking

## Usage

```bash
/cco-review                    # Full review → approve → apply
/cco-review --quick            # Gap analysis only
/cco-review --focus=structure  # Focus on organization
/cco-review --report-only      # Just show findings, don't apply
/cco-review --deep             # Include detailed code review
```
