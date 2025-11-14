---
id: U_EXPLICIT_COMPLETION
title: Explicit Completion Criteria
category: universal
severity: critical
weight: 10
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_EXPLICIT_COMPLETION: Explicit Completion Criteria 🔴

**Severity**: Critical

Before creating TODOs, define EXPLICIT, VERIFIABLE completion criteria. Never mark "complete" based on assumed requirements.

**Why**: Prevents "partial completion blindness" - AI completing its own interpretation instead of user's actual request.

**Trigger**: EVERY TODO creation (works with U_CHANGE_VERIFICATION)

---

## Protocol

### When Creating TODOs

**MANDATORY format**:
```javascript
TodoWrite([
  {
    content: "Remove hardcoded counts from codebase",
    activeForm: "Removing hardcoded counts",
    status: "pending",
    // NEW: Explicit completion criteria
    completionCriteria: [
      "grep -r '82 principles' → 0 results (except README.md)",
      "grep -r '13 universal' → 0 results (except README.md)",
      "All counts reference README.md instead"
    ]
  }
])
```

**Key principle**: Criteria must be VERIFIABLE with commands, not subjective.

---

## Verification Before Completion

Before marking TODO as "completed":

```
1. READ the completionCriteria field
2. RUN each verification command
3. CHECK results match criteria
4. ONLY THEN mark complete
```

**Examples**:

### ❌ Bad (No Criteria)
```javascript
{
  content: "Fix authentication bug",
  status: "completed"  // ← HOW do you know it's fixed?
}
```

### ✅ Good (Explicit Criteria)
```javascript
{
  content: "Fix authentication bug",
  completionCriteria: [
    "Test: curl /api/login with valid creds → 200 OK",
    "Test: curl /api/login with invalid creds → 401 Unauthorized",
    "grep 'TODO' auth.py → 0 results"
  ],
  status: "completed"  // ← Only after running all tests
}
```

---

## Integration with U_CHANGE_VERIFICATION

**U_CHANGE_VERIFICATION** (Change Verification): Verifies code changes are complete
**U_EXPLICIT_COMPLETION** (Completion Criteria): Verifies TASK is complete per requirements

**Together**:
1. U_CHANGE_VERIFICATION: Find all affected files → create TODOs
2. U_EXPLICIT_COMPLETION: Each TODO has explicit completion criteria
3. U_CHANGE_VERIFICATION: Verify each change (grep, tests)
4. U_EXPLICIT_COMPLETION: Verify criteria met before "completed"

---

## Common Mistakes

### Mistake 1: Assumed Requirements
```
User: "Make the API faster"
AI assumes: Add caching
AI completes: Caching added ✓
ACTUAL requirement: Response time < 200ms

Fix: criteria = ["API response time: curl → < 200ms"]
```

### Mistake 2: Partial Implementation
```
User: "Remove all logging statements"
AI removes: Console.log in main.js
AI completes: ✓
ACTUAL: 50 other files still have logging

Fix: criteria = ["grep -r 'console.log' → 0 results"]
```

### Mistake 3: No Verification
```
User: "Update README"
AI writes: New content
AI completes: ✓ (no verification)
ACTUAL: Typos, broken links

Fix: criteria = ["Spell check passes", "All links return 200"]
```

---

## CCO Integration

**TodoWrite tool enhancement** (future):
```typescript
interface Todo {
  content: string;
  activeForm: string;
  status: "pending" | "in_progress" | "completed";
  completionCriteria?: string[];  // NEW field
  verificationCommands?: string[]; // NEW field
}
```

**AI behavior**:
- When marking "completed": CHECK criteria FIRST
- If criteria missing: ASK user for criteria before starting
- If criteria fails: Keep status "in_progress", report failure

---

## Examples

### Scenario 1: Code Refactoring
```javascript
{
  content: "Rename getUserData() → fetchUserProfile()",
  completionCriteria: [
    "grep -r 'getUserData' src/ → 0 results",
    "grep -r 'fetchUserProfile' src/ → 18 results (expected)",
    "npm test → all pass"
  ]
}
```

### Scenario 2: Documentation
```javascript
{
  content: "Document new API endpoints",
  completionCriteria: [
    "README.md has /api/users section",
    "README.md has /api/posts section",
    "Examples for each endpoint included",
    "No [TODO] markers in README"
  ]
}
```

### Scenario 3: Bug Fix
```javascript
{
  content: "Fix null pointer exception in payment flow",
  completionCriteria: [
    "Test: Process payment with null user → graceful error (not crash)",
    "Logs show error message (not stack trace)",
    "Sentry: 0 null pointer errors in last 24h"
  ]
}
```

---

## When to Use

**Always**:
- Any multi-step task
- Any task with ambiguous requirements
- Any task where "done" is subjective

**Can skip**:
- Single-line trivial fixes (typo correction)
- Tasks with obvious binary outcome (file exists/doesn't exist)

**If unsure**: ADD criteria. Better safe than sorry.

---

## Related Principles

- **U_EVIDENCE_BASED** (Evidence-Based Verification): Provides evidence, U_EXPLICIT_COMPLETION defines what evidence is needed
- **U_CHANGE_VERIFICATION** (Change Verification Protocol): Verifies changes, U_EXPLICIT_COMPLETION verifies task completion
- **U_TEST_FIRST** (Test-First Development): Tests are completion criteria for features

---

## Summary

**Before U_EXPLICIT_COMPLETION**:
```
User request → AI interpretation → AI implementation → "Done" (maybe wrong)
```

**With U_EXPLICIT_COMPLETION**:
```
User request → Explicit criteria defined → Implementation → Verify criteria → "Done" (proven correct)
```

**Key insight**: If you can't write verifiable criteria, you don't understand the requirement → ASK user to clarify.
