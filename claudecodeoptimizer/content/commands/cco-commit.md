---
name: cco-commit
description: Smart semantic commits with atomic split recommendations
---

# /cco-commit

**Create semantic git commits**

---

## Flow: Analyze → Suggest → Execute → Done

### Analyze
1. Get all uncommitted changes (staged + unstaged + untracked)
2. Detect change types (feat, fix, refactor, docs, etc.)
3. Identify logical groupings

### Suggest
If multiple change types detected:
- Recommend atomic commit splits
- Show files per commit
- User confirms or customizes

### Execute
1. Stage files for each commit
2. Create commits with conventional format
3. Track progress with TodoWrite

### Done
1. Show created commits
2. Verify: created = planned
3. Suggest: `git push`

---

## Conventional Commits

```
<type>(<scope>): <subject>  ← 50 chars max

<body>                      ← 72 chars wrap
Explain WHAT and WHY.

BREAKING CHANGE: <desc>
Refs: #<issue>
```

**Types:** feat, fix, docs, style, refactor, perf, test, build, ci, chore

---

## Output Format

```markdown
# Commits Created

**Commits:** {count}

## Summary
✓ feat(auth): add JWT authentication
✓ fix(api): handle null response
✓ docs: update README

## Verification
Created: {count} = Planned: {count} ✓

## Next Steps
→ Push: git push origin {branch}
→ Create PR: gh pr create
```

---

## Usage

```bash
/cco-commit                   # Analyze all changes, create commits
/cco-commit "co-author info"  # With additional context
```
