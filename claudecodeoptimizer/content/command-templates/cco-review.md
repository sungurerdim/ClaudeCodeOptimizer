---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Bash(wc:*), Bash(find:*), Edit(*), Task(*), TodoWrite
---

# /cco-review

**Strategic Review** - Fresh perspective diagnosis + pragmatic optimization.

Two-layer analysis: First identify what's wrong (including fundamental issues), then solve with minimum effort for maximum impact.

**Rules:** User Input | Safety | Priority Assignment | Conservative Judgment | Quick Mode | Task Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Project purpose: !`head -5 README.md 2>/dev/null`
- Structure: !`ls -d */ 2>/dev/null | head -10`
- Git activity: !`git log --oneline -5 2>/dev/null`

**Static context (Type, Maturity, Scale, Strategic Context) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Focus Selection

When called without flags, use **AskUserQuestion**:

| Question | Options | multiSelect |
|----------|---------|-------------|
| What areas to review? | Foundation (architecture, patterns); Code Quality (complexity, DRY, standards); Dependencies (coupling, external deps); Testing (coverage, strategy); DX (developer experience); All | true |

**Default:** All (if user doesn't specify)

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

## Execution Optimization

<use_parallel_tool_calls>
When calling multiple tools with no dependencies between them, make all independent
calls in a single message. For example:
- Multiple cco-agent-analyze scopes → launch simultaneously
- Multiple file reads → batch in parallel
- Multiple grep searches → parallel calls

Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Map | `cco-agent-analyze` | `architecture` | Dependency graph, coupling metrics, pattern detection |
| Analyze | `cco-agent-analyze` | `scan` | Issue detection for findings |
| Apply | `cco-agent-apply` | `fix` | Implement approved recommendations |

**Architecture Analysis:** Use `cco-agent-analyze` with `scope: architecture` to get dependency graph, coupling/cohesion metrics, and detected architectural patterns.

## Review Rigor [CRITICAL]

### Evidence-Based Recommendations

**Every recommendation MUST cite specific evidence:**

| Recommendation Type | Required Evidence |
|--------------------|-------------------|
| "Code is complex" | Specific `file:line` with complexity metric |
| "Pattern inconsistent" | 3+ examples showing the inconsistency |
| "Should refactor X" | Current behavior verified by reading code |
| "Missing abstraction" | 2+ places where duplication exists |

### Pattern Discovery Rule

Before concluding "this is a pattern" or "this is inconsistent":
1. Read at least **3 examples** of similar code
2. Document where each example is (`file:line`)
3. Only then make pattern-based recommendations

### No Speculation

**Do NOT recommend changes to code you haven't read.**

Wrong: "The auth module probably needs refactoring"
Right: "auth/handler.py:45-120 has cyclomatic complexity 15, consider extracting validation"

## Flow

1. **Map Current State** - Analyze architecture, patterns, dependencies
2. **Identify Gaps** - Compare purpose vs implementation
3. **Stack Fitness** - Evaluate tech choices against purpose
4. **Fresh Eye Diagnosis** - Is the foundation sound? Identify structural issues
5. **Pragmatic Solutions** - Minimum effort, maximum impact fixes
6. **Prioritize** - Effort/impact matrix with 80/20 focus
7. **Report** - Structured findings with actionable items
8. **Apply** - Optional: implement approved recommendations

## Phase 1: Map Current State

### Architecture Analysis
- Directory structure and organization
- Module boundaries and responsibilities
- Entry points and data flow
- Patterns in use (design patterns, conventions)
- Test structure and coverage areas
- Configuration and environment handling

### Dependency Analysis
- Internal dependency graph
- External dependencies (packages)
- Circular dependency detection
- Dependency depth analysis

### Coupling & Cohesion Analysis

| Metric | Detection | Healthy Range |
|--------|-----------|---------------|
| Afferent coupling (Ca) | Incoming dependencies | Lower is better |
| Efferent coupling (Ce) | Outgoing dependencies | <10 per module |
| Instability (I) | Ce / (Ca + Ce) | 0-1, balanced mix |
| Abstractness (A) | Abstract types / total | 0.3-0.7 ideal |
| Distance from main | \|A + I - 1\| | <0.3 |

Report: Modules in "zone of pain" (concrete + stable) or "zone of uselessness" (abstract + unstable)

Output: **Architecture Map**

## Phase 2: Gap Analysis

Compare Intent vs Implementation:

| Gap Type | Detection |
|----------|-----------|
| Features promised | README claims vs actual code |
| Undocumented features | Code exists but no docs |
| Overcomplicated | Complexity vs stated goals |
| Missing patterns | Stated patterns not implemented |
| Scope creep | Beyond stated purpose |

Standards check:
- DRY violations
- Complexity violations (>10)
- Missing type annotations
- Test coverage gaps
- Security issues

Output: **Gap Report** with file:line references

## Phase 3: Stack Fitness

Evaluate current technology choices:

| Category | Evaluation |
|----------|------------|
| Language | Fits purpose? Alternatives? |
| Framework | Overhead vs benefit? |
| Database | Fits data model? Scale? |
| Architecture | Monolith vs services fit? |
| Dependencies | Necessary? Maintained? |

### Migration Paths

For each suboptimal choice, provide:

```
Current: {current_tech}
Issue: {why_suboptimal}
Alternative: {better_option}
Migration Path:
  1. {step_1}
  2. {step_2}
  3. {step_3}
  ...
Effort: {effort_level}
Risk: {risk_level}
```

## Phase 4: Fresh Eye Diagnosis

**Question: "Is the foundation sound, or fundamentally flawed?"**

Evaluate with fresh eyes, unconstrained by current implementation:

### Foundation Check

| Check | Question | If Flawed |
|-------|----------|-----------|
| Architecture | Does the structure fit the purpose? | Flag as STRUCTURAL |
| Patterns | Are core patterns appropriate? | Flag as STRUCTURAL |
| Abstractions | Right level of abstraction? | Flag as STRUCTURAL |
| Data Model | Does data structure match domain? | Flag as STRUCTURAL |
| Tech Stack | Right tools for the job? | Flag as STACK |

### Structural Issue Detection

```
┌─ FOUNDATION ASSESSMENT ──────────────────────────────────────┐
│ Foundation Status: SOUND / HAS ISSUES                        │
├──────────────────────────────────────────────────────────────┤
│ If SOUND: Proceed to pragmatic optimization                  │
│ If HAS ISSUES: List structural problems first                │
└──────────────────────────────────────────────────────────────┘
```

**Structural issues require attention before optimization.**

Example structural issues:
- Wrong architectural pattern (monolith for highly distributed needs)
- Missing core abstraction (auth scattered everywhere)
- Inverted dependencies (core depends on UI)
- Data model mismatch (relational for graph data)

## Phase 5: Pragmatic Solutions

**Principle: Minimum effort for maximum impact (80/20 rule)**

### Solution Types

| Foundation | Solution Approach |
|------------|-------------------|
| SOUND | Optimize within current structure |
| HAS ISSUES | Targeted structural fixes (not rewrites) |

### Anti-Overengineering Rules

| Instead of... | Do this... |
|---------------|------------|
| Full rewrite | Incremental refactor |
| New abstraction layer | Fix existing layer |
| Framework migration | Configuration change |
| Custom solution | Standard library/pattern |
| Premature optimization | Measure first, optimize bottlenecks |

### Pragmatic Fix Template

```
Issue: [What's wrong - from Fresh Eye]
Impact: HIGH/MEDIUM/LOW
Current: [How it works now]
Proposed: [Minimum change to fix]
Effort: [Hours/days, not weeks]
Risk: LOW/MEDIUM (HIGH = reconsider)
Steps:
  1. [Concrete step]
  2. [Concrete step]
  ...
```

**YAGNI Check:** Before recommending, ask "Is this needed NOW or hypothetically?"

## Phase 6: Prioritization

### 80/20 Focus

**Target: 80% of improvement with 20% of effort**

```
┌─ EFFORT/IMPACT MATRIX ───────────────────────────────────────┐
│                                                              │
│  HIGH   │ ★ {quick_win_1}      │ ○ {big_project_1} │         │
│  IMPACT │ ★ {quick_win_2}      │                   │         │
│         ├─────────────────────┼───────────────────┤         │
│  LOW    │ ★ {small_fix_1}      │ ○ {defer_item_1}  │         │
│  IMPACT │ ★ {small_fix_2}      │                   │         │
│         └─────────────────────┴───────────────────┘         │
│              LOW EFFORT            HIGH EFFORT               │
│                                                              │
│  ★ = Do Now (high impact / low effort ratio)                │
│  ○ = Backlog (low ratio or high risk)                       │
└──────────────────────────────────────────────────────────────┘
```

### Priority Levels

| Priority | Criteria | Action |
|----------|----------|--------|
| Do Now | High impact, low effort, low risk | Implement immediately |
| Plan | High impact, medium effort | Schedule for next sprint |
| Consider | Medium impact, needs discussion | Review with team |
| Backlog | Low ratio or high risk | Document, defer |

**Reject recommendations where effort > impact.**

## Phase 7: Report

### Output Structure

```
┌─ REVIEW SUMMARY ─────────────────────────────────────────────┐
│ Project: {project} | Type: {type} | Maturity: {maturity}     │
│ Files: {n} | Modules: {n} | Dependencies: {n}                │
└──────────────────────────────────────────────────────────────┘

┌─ FOUNDATION STATUS ──────────────────────────────────────────┐
│ Status: SOUND ✓ | HAS ISSUES ⚠                               │
│ {foundation_assessment}                                       │
│ (if issues:)                                                  │
│ • {structural_issue_1}                                        │
│ • {structural_issue_2}                                        │
└──────────────────────────────────────────────────────────────┘

┌─ ARCHITECTURE HEALTH ────────────────────────────────────────┐
│ Metric           │ Value   │ Status                          │
├──────────────────┼─────────┼─────────────────────────────────┤
│ Avg Coupling     │ {n}     │ {status}                        │
│ Max Coupling     │ {n}     │ {status} ({file})               │
│ Circular Deps    │ {n}     │ {status}                        │
│ Cohesion Score   │ {n}%    │ {status}                        │
└──────────────────┴─────────┴─────────────────────────────────┘

┌─ RECOMMENDATIONS (80/20 filtered) ───────────────────────────┐
│ # │ Recommendation           │ Impact │ Effort │ Priority   │
├───┼──────────────────────────┼────────┼────────┼────────────┤
│ 1 │ {recommendation}         │ {imp}  │ {time} │ {priority} │
│ 2 │ {recommendation}         │ {imp}  │ {time} │ {priority} │
│ ...                                                          │
└───┴──────────────────────────┴────────┴────────┴────────────┘
│ Filtered out: {n} low-impact items (see --verbose)           │

┌─ WHAT'S WORKING WELL ────────────────────────────────────────┐
│ • {positive_finding_1}                                       │
│ • {positive_finding_2}                                       │
│ • {positive_finding_3}                                       │
└──────────────────────────────────────────────────────────────┘
```

## Phase 8: Apply (Optional)

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply recommendations? | All ({N}); Select individual; Skip | false |

If "Select individual" chosen:

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Which recommendations to apply? | {rec1} [{priority}]; {rec2} [{priority}]; ... | true |

For each approved recommendation:
1. Show detailed change plan
2. Implement changes
3. Verify (tests pass, lint clean)
4. Report: done + skipped + failed = total

## Flags

| Flag | Effect |
|------|--------|
| `--quick` | Skip from-scratch analysis, faster |
| `--focus=X` | Focus area: structure, patterns, deps, tests, security, dx |
| `--no-apply` | Report only, skip apply phase |
| `--matrix` | Show effort/impact matrix visualization |

## Usage

```bash
/cco-review                    # Full review → approve → apply
/cco-review --quick            # Quick analysis
/cco-review --focus=structure  # Focus on organization
/cco-review --focus=deps       # Focus on dependencies
/cco-review --focus=dx         # Focus on developer experience
/cco-review --matrix           # Show prioritization matrix
```

## Related Commands

- `/cco-optimize` - For specific quality/security checks
- `/cco-optimize` - For safe structural changes
- `/cco-preflight` - For pre-release review

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Safety

- **Pre-op**: Check git status before Apply phase
- **Dirty**: If uncommitted changes → prompt: `Commit; Stash; Continue anyway`
- **Rollback**: Clean git state enables `git checkout` on failure

### Priority Assignment

| Priority | Criteria |
|----------|----------|
| Do Now | High impact, low effort, blocking |
| Plan | High impact, medium effort |
| Consider | Medium impact, various effort |
| Backlog | Low impact or high effort |

### Conservative Judgment [CRITICAL]

| Keyword | Severity | Confidence Required |
|---------|----------|---------------------|
| crash, data loss, security breach | CRITICAL | HIGH |
| broken, blocked, cannot use | HIGH | HIGH |
| error, fail, incorrect | MEDIUM | MEDIUM |
| style, minor, cosmetic | LOW | LOW |

- **Lower**: When uncertain between two severities, choose lower
- **Evidence**: Require explicit evidence, not inference
- **No-Escalate**: Style issues → never CRITICAL or HIGH

### Quick Mode

When `--quick` flag:
- **No-Questions**: Use smart defaults
- **Single-Message**: Complete analysis in one message
- **Brief-Output**: Summary only, skip detailed breakdown

### Task Tracking

- **Create**: TODO list with review phases
- **Status**: pending → in_progress → completed
- **Accounting**: reviewed + applied + skipped = total
