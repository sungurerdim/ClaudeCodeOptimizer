---
name: cco-review
description: Strategic architecture review with fresh perspective
---

# /cco-review

**Strategic review** - Understand intent → analyze architecture → compare with ideal → recommend improvements.

**Standards:** Pre-Operation Safety | Context Read | Fix Workflow | Priority & Approval | Safety Classification | Status Updates | UX/DX

## Context Application

| Field | Effect |
|-------|--------|
| Maturity | Legacy → safe incremental improvements; Greenfield → can suggest restructuring |
| Breaking | Never → flag interface changes as blockers; Allowed → suggest API simplifications |
| Priority | Speed → quick wins only; Quality → comprehensive analysis |
| Scale | 10K+ → emphasize performance, caching, scaling patterns; <100 → simplicity focus |
| Team | Solo → pragmatic suggestions; 6+ → consider coordination, documentation needs |
| Data | PII/Regulated → security review mandatory, compliance check |
| Type | API → contract stability; Library → backward compatibility; CLI → UX consistency |

## Flow

0. **Context Check** - Run `/cco-tune --status`; handle completion/restart per cco-tune flow
1. **Read Context** - Read `./CLAUDE.md`, extract CCO_CONTEXT markers only, parse values
2. **Map Current State** - Analyze architecture, patterns, dependencies
3. **Identify Gaps** - Compare purpose vs implementation
4. **Stack Fitness** - Evaluate tech choices against purpose
5. **Fresh Perspective** - "If building from scratch" recommendations
6. **Prioritize** - Quick wins vs major refactors, risk assessment
7. **Report** - Structured findings with actionable items

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

Check against CLAUDE.md standards:
- DRY violations
- Orphan code (unused functions, dead imports)
- Complexity violations (cyclomatic >10)
- Missing type annotations
- Test coverage gaps
- Security standard violations

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
- Apply AI Content standards (semantic density, no duplicates, structured format)
- Present optimized ideal, not just "from scratch"
- Show before/after comparison where applicable

Output: **Stack Fitness Report** + **Optimized "From Scratch" Recommendations**

## Phase 4: Prioritization

**By Effort:** Quick Win (<1h) | Small (<1d) | Medium (<1w) | Major (>1w)

**By Impact:** Critical | High | Medium | Low

**By Risk:** Safe | Low | Medium | High

Priority = Impact / Effort (prefer high impact, low effort, low risk)

## Report Structure

**Standards:** Output Formatting

Sections:
1. **Context** - Team, scale, data, type, purpose (inline)
2. **Architecture Overview** - Prose description of current state
3. **Stack Fitness** - Choice | Serves Purpose? | Alternative | Why
4. **Gap Analysis** - Gap | Location | Details
5. **Recommendations** - Priority | Recommendation | Effort | Risk
6. **What's Working Well** - Prose list of positive observations

## Apply

For each approved recommendation:
1. Show what will change
2. Make the changes
3. Verify (tests pass, lint clean)
4. Report: done + skipped + failed = total

## Flags

- `--quick` - Phase 1-3 only, skip "from scratch" analysis
- `--focus=X` - Focus on specific area (structure, patterns, deps, tests, security, dx)

Note: Use approval flow for apply behavior (select none = report-only, select all = auto-apply)

## Usage

```bash
/cco-review                    # Full review → approve → apply
/cco-review --quick            # Quick analysis, skip from-scratch
/cco-review --focus=structure  # Focus on organization
/cco-review --focus=security   # Focus on security review
```
