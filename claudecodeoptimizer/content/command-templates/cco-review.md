---
name: cco-review
description: Strategic architecture review with fresh perspective
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Bash(wc:*), Bash(find:*), Edit(*), Task(*), TodoWrite
---

# /cco-review

**Strategic Review** - "If I built this from scratch, how would I do it?"

Analyzes architecture, identifies gaps, and provides actionable recommendations.

**Standards:** Command Flow | Fix Workflow | User Input | Approval Flow | Output Formatting

## Context

- Context check: !`grep -c "CCO_ADAPTIVE_START" ./CLAUDE.md 2>/dev/null || echo "0"`
- Project purpose: !`head -5 README.md 2>/dev/null`
- Structure: !`ls -d */ 2>/dev/null | head -10`
- Git activity: !`git log --oneline -5 2>/dev/null`

**Static context (Type, Maturity, Scale, Strategic Context) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO_ADAPTIVE in ./CLAUDE.md.**

If context check returns "0":
```
CCO_ADAPTIVE not found in ./CLAUDE.md

Run /cco-tune first to configure project context, then restart CLI.
```
**Stop execution immediately.**

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

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Map | `cco-agent-analyze` | `architecture` | Dependency graph, coupling metrics, pattern detection |
| Analyze | `cco-agent-analyze` | `scan` | Issue detection for findings |
| Apply | `cco-agent-apply` | `fix` | Implement approved recommendations |

**Architecture Analysis:** Use `cco-agent-analyze` with `scope: architecture` to get dependency graph, coupling/cohesion metrics, and detected architectural patterns.

## Flow

1. **Map Current State** - Analyze architecture, patterns, dependencies
2. **Identify Gaps** - Compare purpose vs implementation
3. **Stack Fitness** - Evaluate tech choices against purpose
4. **Fresh Perspective** - "If building from scratch" recommendations
5. **Prioritize** - Effort/impact matrix, risk assessment
6. **Report** - Structured findings with actionable items
7. **Apply** - Optional: implement approved recommendations

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
Current: Express.js
Issue: Heavy for simple CLI tool
Alternative: Native Node.js or minimal framework
Migration Path:
  1. Identify Express-specific code (routes, middleware)
  2. Abstract HTTP layer
  3. Replace incrementally
  4. Remove Express dependency
Effort: Medium (1-2 days)
Risk: Low (well-tested patterns)
```

## Phase 4: Fresh Perspective

"If I were building this project from scratch today..."

### Categories

| Area | Analysis |
|------|----------|
| Structure | Optimal directory layout |
| Patterns | Modern idioms for this stack |
| Abstractions | What to abstract, what to inline |
| Data Flow | Cleaner data pipelines |
| Testing | Better test strategy |
| DX | Developer experience improvements |

For each recommendation:
- Before/after comparison
- Concrete implementation steps
- Expected benefits

## Phase 5: Prioritization

### Effort/Impact Matrix

```
┌─ EFFORT/IMPACT MATRIX ───────────────────────────────────────┐
│                                                              │
│  HIGH   │ ★ Restructure auth  │ ○ Rewrite core    │         │
│  IMPACT │ ★ Add caching       │                   │         │
│         ├────────────────────┼───────────────────┤         │
│  LOW    │ ★ Fix imports       │ ○ Migrate DB      │         │
│  IMPACT │ ★ Update deps       │                   │         │
│         └────────────────────┴───────────────────┘         │
│              LOW EFFORT           HIGH EFFORT               │
│                                                              │
│  ★ = Recommended (high impact, low effort)                  │
│  ○ = Consider later                                          │
└──────────────────────────────────────────────────────────────┘
```

### Priority Levels

| Priority | Criteria |
|----------|----------|
| Do Now | High impact, low effort, low risk |
| Plan | High impact, medium effort |
| Consider | Medium impact, any effort |
| Backlog | Low impact or high risk |

## Phase 6: Report

### Output Structure

```
┌─ REVIEW SUMMARY ─────────────────────────────────────────────┐
│ Project: my-project | Type: CLI | Maturity: Active           │
│ Files: 45 | Modules: 8 | Dependencies: 12                    │
└──────────────────────────────────────────────────────────────┘

┌─ ARCHITECTURE HEALTH ────────────────────────────────────────┐
│ Metric           │ Value   │ Status                          │
├──────────────────┼─────────┼─────────────────────────────────┤
│ Avg Coupling     │ 4.2     │ OK                              │
│ Max Coupling     │ 12      │ WARN (utils.py)                 │
│ Circular Deps    │ 0       │ OK                              │
│ Cohesion Score   │ 78%     │ OK                              │
└──────────────────┴─────────┴─────────────────────────────────┘

┌─ GAPS FOUND ─────────────────────────────────────────────────┐
│ Type          │ Gap                    │ Location            │
├───────────────┼────────────────────────┼─────────────────────┤
│ Undocumented  │ Export feature         │ exporter.py         │
│ Overcomplicated│ Auth flow             │ auth/:42            │
│ Missing       │ Error handling pattern │ api/                │
└───────────────┴────────────────────────┴─────────────────────┘

┌─ RECOMMENDATIONS ────────────────────────────────────────────┐
│ # │ Recommendation           │ Impact │ Effort │ Priority   │
├───┼──────────────────────────┼────────┼────────┼────────────┤
│ 1 │ Simplify auth flow       │ HIGH   │ 2h     │ Do Now     │
│ 2 │ Add error boundaries     │ HIGH   │ 4h     │ Do Now     │
│ 3 │ Extract shared utils     │ MEDIUM │ 1d     │ Plan       │
│ 4 │ Migrate to async/await   │ LOW    │ 3d     │ Backlog    │
└───┴──────────────────────────┴────────┴────────┴────────────┘

┌─ WHAT'S WORKING WELL ────────────────────────────────────────┐
│ • Clean separation between CLI and core logic                │
│ • Consistent naming conventions throughout                   │
│ • Good test coverage for critical paths (92%)                │
│ • Well-structured configuration management                   │
│ • Clear module boundaries                                    │
└──────────────────────────────────────────────────────────────┘
```

## Phase 7: Apply (Optional)

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

- `/cco-audit` - For specific quality/security checks
- `/cco-refactor` - For safe structural changes
- `/cco-release` - For pre-release review
