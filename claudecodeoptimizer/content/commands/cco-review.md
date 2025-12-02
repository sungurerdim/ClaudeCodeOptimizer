---
name: cco-review
description: Strategic architecture review with fresh perspective
---

# /cco-review

**Strategic review** - Understand intent → analyze architecture → compare with ideal → recommend improvements.

**Standards:** Pre-Operation Safety | Context Read | Approval Flow | Safety Classification | Verification | Error Format

## Context Application
- **Maturity** - If Legacy → focus on safe incremental improvements; if Greenfield → can suggest restructuring
- **Breaking** - If Never → flag any interface changes; if Allowed → suggest API simplifications
- **Priority** - If Speed → quick wins only; if Quality → comprehensive analysis

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

### 3a: Stack Fitness

Evaluate current technology choices against purpose and constraints:

| Current Choice | Serves Purpose? | Better Alternative? | Why? |
|----------------|-----------------|---------------------|------|
| Language | Y/N | If N, suggest | Reasoning |
| Framework | Y/N | If N, suggest | Reasoning |
| Database | Y/N | If N, suggest | Reasoning |
| Architecture | Y/N | If N, suggest | Reasoning |

### 3b: From Scratch Perspective (Optimized)

Answer: "If I were building this project from scratch today, optimized..."

**Standards:** AI Context (Universal) - apply to all recommendations

Categories: Structure, Patterns, Abstractions, Data Flow, Testing, DX

For each recommendation:
- Apply AI Content Optimization principles (semantic density, no duplicates, structured format)
- Present optimized ideal, not just "from scratch"
- Show before/after comparison where applicable

Output: **Stack Fitness Report** + **Optimized "From Scratch" Recommendations**

## Phase 4: Prioritization

**By Effort:** Quick Win (<1h) | Small (<1d) | Medium (<1w) | Major (>1w)

**By Impact:** Critical | High | Medium | Low

**By Risk:** Safe | Low | Medium | High

Priority = Impact / Effort (prefer high impact, low effort, low risk)

## Report Structure

```
## Context
Team: {team} | Scale: {scale} | Data: {data} | Type: {type}
Purpose: {purpose}

## Architecture Overview
[Current state - structure, patterns, key decisions]

## Stack Fitness
[Table of choices and verdicts]

## Gap Analysis
- [gap]: [file:line] - [details]

## Recommendations by Priority
[Grouped by: Critical → Quick Wins → Medium → Nice to Have]

## What's Working Well
[Positive observations - patterns to keep]
```

## Apply

For each approved recommendation:
1. Show what will change
2. Make the changes
3. Verify (tests pass, lint clean)
4. Report: done + skipped + failed = total

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
/cco-review --report-only      # Just show findings
```
