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

Before analysis, establish project context for calibrated recommendations.

### Check Existing Context

First, check if context already exists:

```bash
cat .claude/cco_context.yaml 2>/dev/null
```

### If Context Exists

Show the current context summary and ask:

```
AskUserQuestion:
header: "Context"
question: "Found existing project context:\n\n[show key values: affected, scale, data sensitivity, team size, time pressure]\n\nIs this still accurate?"
options:
  - label: "Yes, use this"
    description: "Proceed with existing context"
  - label: "Update some fields"
    description: "Select which fields to update"
  - label: "Start fresh"
    description: "Re-answer all context questions"
```

If "Update some fields", ask multiselect:
```
AskUserQuestion:
header: "Update"
question: "Which sections need updating?"
multiSelect: true
options:
  - label: "Impact & Scale"
    description: "Who affected, how many users"
  - label: "Risk & Compliance"
    description: "Data sensitivity, compliance requirements"
  - label: "Team"
    description: "Team size, ownership model"
  - label: "Operations"
    description: "Rollback complexity, time pressure"
```

Then re-ask only selected sections' questions.

### If No Context Exists

Gather context with conditional questions (see content/shared/project-context.md for full question flow):

**Always ask:** Impact → Downtime → Team Size → Rollback → Time Pressure

**Conditional:**
- Scale (if team+)
- Data Sensitivity (if customers+)
- Compliance (if PII+)
- Revenue Impact (if minutes+)
- Code Ownership (if 2+ devs)

After gathering, write to `.claude/cco_context.yaml`

### Using Context

Include the gathered/loaded context in your analysis. Calibrate all recommendations based on:
- **Impact level** → How rigorous should review be?
- **Data sensitivity** → Security focus depth
- **Team size** → Documentation and review needs
- **Time pressure** → Trade-off recommendations
- **Rollback complexity** → Risk assessment for changes

**DO NOT** apply fixed standards regardless of context.
**DO** explain how context affects your recommendations.

## Flow

1. **Understand Intent** - Read all docs, extract goals and constraints
2. **Map Current State** - Analyze architecture, patterns, dependencies
3. **Identify Gaps** - Compare intent vs implementation
4. **Fresh Perspective** - "If building from scratch" recommendations
5. **Prioritize** - Quick wins vs major refactors, risk assessment
6. **Report** - Structured findings with actionable items

## Phase 1: Understand Intent

Read and synthesize:
- README.md - Project purpose, features, usage
- CONTRIBUTING.md - Development guidelines, conventions
- CLAUDE.md - AI-specific rules, principles
- docs/ - Architecture decisions, design docs
- pyproject.toml / package.json - Dependencies, scripts, config
- .github/ - CI/CD, templates, workflows

Extract:
- Stated goals and non-goals
- Target users and use cases
- Design principles and constraints
- Stated architecture decisions
- Success criteria

Output: **Intent Summary** (what the project aims to be)

## Phase 2: Map Current State

Analyze:
- Directory structure and organization
- Module boundaries and responsibilities
- Dependency graph (internal and external)
- Entry points and data flow
- Patterns in use (design patterns, conventions)
- Test structure and coverage areas
- Configuration and environment handling

Output: **Architecture Map** (what the project actually is)

## Phase 3: Gap Analysis

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

## Phase 4: Fresh Perspective

Answer: "If I were building this project from scratch today, knowing everything I now know..."

Consider:
- Would I use the same directory structure?
- Would I organize modules differently?
- Are there simpler patterns for the same goals?
- Which dependencies would I keep/replace/remove?
- What abstractions are over/under-engineered?
- Which decisions were right vs accidental complexity?

Categories:
- **Structure** - Directory layout, module organization
- **Patterns** - Design patterns, conventions, idioms
- **Dependencies** - External libs, internal coupling
- **Abstractions** - Too much, too little, wrong level
- **Data Flow** - How data moves through the system
- **Testing** - Strategy, coverage, maintainability
- **DX** - Developer experience, onboarding, tooling

Output: **"From Scratch" Recommendations**

## Phase 5: Prioritization

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
## Context Summary
[Brief summary of project context and how it affects this review]
- Impact: {affected} ({scale} users)
- Risk Profile: {data_sensitivity}, {compliance}
- Team: {size}, {ownership}
- Current Pressure: {time_pressure}

**Review Calibration:** Based on this context, this review [applies standard rigor / relaxes certain standards / applies strict standards] because [reason].

## Intent Summary
[What the project aims to be - 3-5 sentences]

## Architecture Overview
[Current state - structure, patterns, key decisions]

## Gap Analysis
### Docs vs Code Mismatches
- [gap]: [file:line] - [details]

### Principle Violations
- [principle]: [file:line] - [details]

## Recommendations by Priority
[Grouped for approval]

## What's Working Well
[Positive observations - patterns to keep, good decisions]
```

## Approval & Apply Flow

After analysis, present all recommendations in a **single AskUserQuestion call** with up to 4 questions (one per priority level):

```
AskUserQuestion (single call, multiple questions):

Question 1 - header: "Critical"
"Found X critical improvements. Which to apply?"
multiSelect=true
- "All" (first option)
- Individual critical items...

Question 2 - header: "Quick Wins"
"Found X quick wins (high impact, low effort). Which to apply?"
multiSelect=true
- "All"
- Individual quick win items...

Question 3 - header: "Medium"
"Found X medium priority improvements. Which to apply?"
multiSelect=true
- "All"
- Individual medium items...

Question 4 - header: "Nice to Have"
"Found X nice-to-have improvements. Which to apply?"
multiSelect=true
- "All"
- Individual low priority items...
```

**Rules:**
- Only include questions for priority levels that have recommendations
- Skip empty priority levels
- Max 4 options per question - group if needed

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
