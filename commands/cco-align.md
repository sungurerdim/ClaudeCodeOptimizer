---
description: Align codebase with ideal architecture - current vs ideal state gap analysis
argument-hint: "[--auto] [--preview]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
model: opus
---

# /cco-align

**Align with Ideal Architecture** — "If I designed from scratch, what would be best?"

**Philosophy:** Evaluate as if no technology choices exist yet. Given only the requirements, what's ideal? Compare current state to that ideal.

**Purpose:** Strategic, architecture-level assessment. For tactical file-level fixes, use `/cco-optimize`.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | All 6 scopes, all severities, no questions, single-line summary |
| `--preview` | Analyze only, show gaps and findings, don't apply |

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`

## Scopes (6 scopes, 77 checks)

| Scope | ID Range | Focus |
|-------|----------|-------|
| architecture | ARC-01 to ARC-15 | Coupling, cohesion, layers, dependencies |
| patterns | PAT-01 to PAT-12 | Design patterns, consistency, SOLID |
| testing | TST-01 to TST-10 | Coverage strategy, test quality, gaps |
| maintainability | MNT-01 to MNT-12 | Complexity, readability, documentation |
| ai-architecture | AIA-01 to AIA-10 | Over-engineering, local solutions, drift |
| functional-completeness | FUN-01 to FUN-18 | API completeness, CRUD, pagination, filtering, edge cases, schema validation, state transitions, data management |

## Execution Flow

Setup → Analyze → Gap Analysis → Recommendations → [Plan] → Apply → Summary

### Phase 1: Setup [SKIP IF --auto]

**Q1 (multiselect):** "Which areas to review?"
- Structure (Recommended): architecture + patterns
- Quality (Recommended): testing + maintainability
- Completeness & Data: functional-completeness + ai-architecture

### Phase 2: Analyze [PARALLEL SCOPES]

Launch scope groups as parallel Task calls to cco-agent-analyze (mode: review):
- Structure: architecture, patterns
- Quality: testing, maintainability
- Completeness: functional-completeness, ai-architecture

Merge findings and metrics. Filter by user-selected scopes.

### Phase 3: Gap Analysis [CURRENT vs IDEAL]

Define ideal metrics by project type:

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |

Calculate gaps: current vs ideal for coupling, cohesion, complexity, coverage. Display Current vs Ideal table.

Technology assessment: if agent found alternatives, show current vs ideal technology choices with migration cost. Recommend tech changes only with evidence (file:line), migration cost, and team familiarity consideration.

### Phase 4: Recommendations [80/20 PRIORITIZED]

Categorize by effort/impact: Quick Win (high impact, low effort) → Moderate → Complex → Major.

### Phase 5: Plan Review [when findings > 0, SKIP if --auto]

Display architectural plan before asking.

**Post-analysis Q2:**
- Action: Fix All (Recommended) / By Severity / Review Each / Report Only
- Severity filter (multiselect): CRITICAL / HIGH / MEDIUM / LOW

### Phase 6: Apply

Send recommendations to cco-agent-apply. Verify changes don't break functionality.

Count findings, not locations.

### Phase 6.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per CCO Rules: Needs-Approval Flow.

### Phase 7: Summary

Gap summary (before/after for coupling, cohesion, complexity, coverage), applied/failed/total accounting table, effort category breakdown.

--auto mode: `cco-align: {OK|WARN|FAIL} | Gaps: N | Applied: N | Failed: N | Needs Approval: N | Total: N`

Status: OK (failed=0, no gap>20%), WARN (failed>0 or gap>20%), FAIL (CRITICAL gap or error).
