---
name: cco-review
description: Architecture review with pragmatic optimization
allowed-tools: Read(*), Grep(*), Glob(*), Bash(git:*), Edit(*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-review

**Strategic Review** - Fresh perspective diagnosis + pragmatic optimization via parallel agents.

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`

**DO NOT re-run these commands. Use the pre-collected values above.**

## Context Requirement [CRITICAL]

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop immediately.**

## Architecture

| Step | Name | Action |
|------|------|--------|
| 1 | Focus | Ask focus areas |
| 2 | Analyze | Run agent with scopes |
| 3 | Assessment | Show foundation assessment |
| 4 | Recommendations | Show prioritized 80/20 list |
| 5 | Approval | Ask which to apply |
| 6 | Apply | Execute approved changes |
| 7 | Summary | Show results |

---

## Progress Tracking [CRITICAL]

```javascript
TodoWrite([
  { content: "Step-1: Select focus areas", status: "in_progress", activeForm: "Selecting focus areas" },
  { content: "Step-2: Run analysis", status: "pending", activeForm: "Running analysis" },
  { content: "Step-3: Show assessment", status: "pending", activeForm: "Showing assessment" },
  { content: "Step-4: Show recommendations", status: "pending", activeForm: "Showing recommendations" },
  { content: "Step-5: Get approval", status: "pending", activeForm: "Getting approval" },
  { content: "Step-6: Apply changes", status: "pending", activeForm: "Applying changes" },
  { content: "Step-7: Show summary", status: "pending", activeForm: "Showing summary" }
])
```

---

## Step-1: Focus Areas

```javascript
AskUserQuestion([{
  question: "Focus areas?",
  header: "Focus",
  options: [
    { label: "Architecture", description: "Dependency graph, coupling, patterns, layers" },
    { label: "Code Quality", description: "Issues with file:line, complexity" },
    { label: "Testing & DX", description: "Test coverage, developer experience" },
    { label: "Best Practices", description: "Tool usage, execution patterns, efficiency" }
  ],
  multiSelect: true
}])
```

**Dynamic labels:** Add `(Recommended)` based on project context.

**Flags override:** `--focus=X` skips this question.

| Selection | Agent Scope |
|-----------|-------------|
| Architecture | architecture |
| Code Quality | scan (focus=quality) |
| Testing & DX | scan (focus=testing,dx) |
| Best Practices | best-practices |

### Validation
```
[x] User selected focus area(s)
→ Store as: focusAreas = {selections[]}
→ Map to agent scopes
→ Proceed to Step-2
```

---

## Step-2: Analysis

```javascript
agentResponse = Task("cco-agent-analyze", `
  scopes: ${JSON.stringify(mappedScopes)}
  Return findings JSON with:
  - foundation: { status: "SOUND"|"HAS ISSUES", details }
  - findings[]: { id, category, severity, title, file, line, description, recommendation, effort, impact }
  - summary: { total, by_category, by_severity }
`)
```

**CRITICAL:** ONE analyze agent. Never spawn multiple agents.

### Validation
```
[x] Agent returned valid response
[x] response.foundation exists
[x] response.findings exists
→ Proceed to Step-3
```

---

## Step-3: Foundation Assessment

Display foundation status:

| Status | Meaning |
|--------|---------|
| SOUND | Optimize within structure |
| HAS ISSUES | Targeted fixes (not rewrites) |

Show key metrics: coupling, complexity, test coverage, etc.

### Validation
```
[x] Assessment displayed
→ Proceed to Step-4
```

---

## Step-4: Recommendations

Apply 80/20 filter and prioritize:

| Priority | Criteria |
|----------|----------|
| Do Now | High impact, low effort |
| Plan | High impact, medium effort |
| Consider | Medium impact |
| Backlog | Low impact or high effort |

Display prioritized list with effort/impact indicators.

### Validation
```
[x] Recommendations displayed
[x] Prioritization applied
→ If --no-apply flag: Skip to Step-7
→ Proceed to Step-5
```

---

## Step-5: Approval [SKIP if --no-apply]

```javascript
AskUserQuestion([{
  question: "Apply recommendations?",
  header: "Apply",
  options: [
    { label: `All (${totalCount})`, description: "Apply all recommendations" },
    { label: "Select individual", description: "Choose which to apply" },
    { label: "Skip", description: "Report only, no changes" }
  ],
  multiSelect: false
}])
```

### If Select Individual

Show recommendations grouped by priority:

```javascript
AskUserQuestion([{
  question: "Select 'Do Now' items to apply:",
  header: "Do Now",
  options: doNowItems.map(item => ({
    label: item.title,
    description: `${item.file} - ${item.description}`
  })),
  multiSelect: true
}])
// Repeat for Plan, Consider, Backlog if needed
```

### Validation
```
[x] User made selection
→ Store as: approved = {selections[]}, declined = {unselected[]}
→ If Skip: Skip to Step-7
→ Proceed to Step-6
```

---

## Step-6: Apply [SKIP if nothing approved]

```javascript
Task("cco-agent-apply", `
  fixes: ${JSON.stringify(approved)}
  Apply approved recommendations. Verify each change.
`)
```

### Validation
```
[x] Approved changes applied
[x] No cascading errors
→ Store as: applied = {count}
→ Proceed to Step-7
```

---

## Step-7: Summary

Display:
- Foundation: {status}
- Total findings: {count}
- Applied: {applied} items
- Declined: {declined.length} items
- By priority: Do Now ({n}), Plan ({n}), Consider ({n}), Backlog ({n})

### Validation
```
[x] Summary displayed
[x] All todos marked completed
→ Done
```

---

## Reference

### Context Application

| Field | Effect |
|-------|--------|
| Maturity | Legacy → safe; Greenfield → restructure |
| Breaking | Never → flag as blockers |
| Priority | Speed → quick wins; Quality → comprehensive |
| Scale | 10K+ → performance; <100 → simplicity |
| Data | PII/Regulated → security mandatory |

### Best Practices Scope

| Category | Reviews |
|----------|---------|
| Execution | Parallel vs sequential, batching |
| Tool Selection | Right tool, subagent usage |
| Code Patterns | Async, error boundaries, state |
| Architecture | Layer separation, dependencies |

### Quick Mode (`--quick`)

When `--quick` flag:
- No questions - use smart defaults (Architecture + Code Quality)
- Report only (no apply phase)
- Complete in single message

### Flags

| Flag | Effect |
|------|--------|
| `--quick` | Smart defaults |
| `--focus=X` | architecture, quality, testing, dx, best-practices |
| `--best-practices` | Best practices only |
| `--no-apply` | Report only |
| `--matrix` | Effort/impact matrix |

---

## Rules

1. **Sequential execution** - Complete each step before proceeding
2. **Validation gates** - Check validation block before next step
3. **ONE analyze agent** - Never spawn multiple agents
4. **ONE apply agent** - Never spawn multiple agents
5. **80/20 filter** - Prioritize high-impact, low-effort items
6. **Evidence required** - Every recommendation needs justification
