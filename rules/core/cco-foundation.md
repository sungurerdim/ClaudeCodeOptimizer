# Foundation Rules
*Enforceable constraints with measurable thresholds*

## Uncertainty Protocol [BLOCKER]

When uncertain, STOP and surface it. Don't guess silently.

**Required actions:**
- **Stop-When-Unclear**: If task is ambiguous → ask before proceeding
- **Signal-Confidence**: State confidence level: "~90% sure", "uncertain about X", "assuming Y"

```
✓ "Before I proceed: [specific thing] is unclear."
✓ "I'm ~80% confident. Uncertainty: [what]."
✗ Silently picking one interpretation
✗ Proceeding despite confusion
```

## Complexity Limits [BLOCKER]

Code exceeding these limits = STOP and refactor first.

| Metric | Limit | Action if exceeded |
|--------|-------|-------------------|
| Cyclomatic Complexity | ≤ 15 | Split function |
| Method Lines | ≤ 50 | Extract methods |
| File Lines | ≤ 500 | Split file |
| Nesting Depth | ≤ 3 | Flatten logic |
| Parameters | ≤ 4 | Use object/config |

## File Creation [BLOCKER]

**BLOCK**: Creating new files without explicit user request.

```
User: "Add validation to user.py" → Edit user.py only
User: "Create a utils module" → OK to create file
```

Directories to skip: `.git`, `node_modules`, `vendor`, `venv`, `dist`, `build`, `__pycache__`

## Change Scope [BLOCKER]

**Test**: Can every changed line trace directly to user's request?

- NO → Revert that change
- If you notice unrelated issues → mention, don't fix

```
✓ User asked for X → only X changed
✗ User asked for X → X + "improvements" to nearby code
```

## Code Volume [CHECK]

Before completing, verify:

- [ ] No abstractions for single-use code
- [ ] No error handling for impossible scenarios
- [ ] If 100+ lines written → could it be 50? Rewrite if yes

**Ratio check**: If implementation > 4x the minimal solution, simplify.

## Success Criteria [CHECK]

Before starting multi-step tasks:

```
Goal: [one sentence]
Steps:
1. [action] → verify: [how to check]
2. [action] → verify: [how to check]
Done when: [measurable outcome]
```

**Every 5 steps**: "Original goal: [X]. Still on track?"

## Validation Boundaries [CHECK]

Public APIs MUST have:

| Input Type | Required Validation |
|------------|---------------------|
| Numbers | min/max bounds |
| Strings | max length |
| Arrays | max items |
| External calls | timeout value |
| Resources | cleanup in finally/with/using |

## Refactoring Safety [CHECK]

Before modifying shared code:

- [ ] **Delete**: Found ALL callers (grep/find-refs)
- [ ] **Rename**: Will update ALL references
- [ ] **Move**: Will update ALL imports
- [ ] **Signature**: Will update ALL call sites

## Output Format

Progress: `"Step 2/5: [action]..."`
Summary: `"Changed 3 files, added 2 tests"`
Errors: `"[SEVERITY] {what} in {file}:{line}"`
