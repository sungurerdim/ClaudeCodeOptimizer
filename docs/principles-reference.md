# Software Engineering Principles Reference

A comprehensive reference of software engineering principles used in CCO. Each principle includes its definition, rationale, and practical application.

---

## Design Principles

Foundational principles that guide software architecture and design decisions.

### SSOT (Single Source of Truth)
**Definition:** Every piece of knowledge or data should have a single, authoritative representation in the system.

**Why it matters:**
- Eliminates inconsistencies between duplicate representations
- Changes propagate automatically from the source
- Reduces bugs from out-of-sync data

**Application:**
```
❌ Bad: User email in users table AND orders table
✓ Good: User email only in users table, orders reference user_id
```

---

### DRY (Don't Repeat Yourself)
**Definition:** Extract common patterns to avoid duplication. Every piece of logic should exist in exactly one place.

**Why it matters:**
- One fix updates all usages
- Easier maintenance and refactoring
- Reduced code surface area

**Application:**
```
❌ Bad: Same validation logic in 5 different files
✓ Good: Single validate() function imported where needed
```

---

### YAGNI (You Aren't Gonna Need It)
**Definition:** Don't implement features until they're actually needed, not when you think you might need them.

**Why it matters:**
- Reduces complexity
- Saves development time
- Avoids maintaining unused code

**Application:**
```
❌ Bad: Building a plugin system "for future extensibility"
✓ Good: Hardcoded solution now, refactor when third plugin is needed
```

---

### KISS (Keep It Simple, Stupid)
**Definition:** Prefer the simplest solution that solves the problem correctly.

**Why it matters:**
- Easier to understand and debug
- Fewer edge cases
- Lower cognitive load

**Application:**
```
❌ Bad: Custom state machine for form validation
✓ Good: Simple if/else validation with early returns
```

---

### Separation of Concerns
**Definition:** Each module/component should handle one distinct aspect of the functionality.

**Why it matters:**
- Changes are isolated to relevant areas
- Easier testing of individual concerns
- Better code organization

**Application:**
```
❌ Bad: UI component that also makes API calls and manages state
✓ Good: UI component + API service + state manager (separate)
```

---

### Composition Over Inheritance
**Definition:** Prefer combining simple objects/functions over building complex inheritance hierarchies.

**Why it matters:**
- More flexible combinations
- Avoids "diamond problem" and deep hierarchies
- Easier to test individual pieces

**Application:**
```
❌ Bad: class AdminUser extends User extends Person extends Entity
✓ Good: User with roles: Role[], where Role is composed of permissions
```

---

### Idempotent
**Definition:** An operation that produces the same result regardless of how many times it's executed.

**Why it matters:**
- Safe to retry failed operations
- Simplifies error recovery
- Essential for distributed systems

**Application:**
```
❌ Bad: incrementBalance(+100) - calling twice doubles the amount
✓ Good: setBalance(currentBalance + 100, requestId) - second call is no-op
```

---

### Least Astonishment (Principle of Least Surprise)
**Definition:** Software should behave in a way that users and developers expect based on context and conventions.

**Why it matters:**
- Reduces errors from misunderstanding
- Faster onboarding
- Fewer support requests

**Application:**
```
❌ Bad: delete() returns the deleted item
✓ Good: delete() returns boolean/void, getAndDelete() if you need the item
```

---

## Code Quality Principles

Principles that ensure code is maintainable, readable, and robust.

### Fail-Fast
**Definition:** When an error occurs, fail immediately and visibly rather than continuing with corrupted state.

**Why it matters:**
- Errors caught at source, not downstream
- Easier debugging (stacktrace points to cause)
- Prevents data corruption

**Application:**
```
❌ Bad: user = getUser() || {}  // silently returns empty object
✓ Good: user = getUser(); if (!user) throw new UserNotFoundError(id)
```

---

### Immutability
**Definition:** Prefer data that cannot be modified after creation. Create new values instead of modifying existing ones.

**Why it matters:**
- No surprise mutations
- Thread-safe by default
- Easier to reason about

**Application:**
```
❌ Bad: user.age = 30; return user;
✓ Good: return { ...user, age: 30 };
```

---

### Type Safety
**Definition:** Use type annotations to catch errors at compile/lint time rather than runtime.

**Why it matters:**
- Catches errors before deployment
- Self-documenting code
- Better IDE support

**Application:**
```
❌ Bad: function process(data) { ... }
✓ Good: function process(data: ProcessInput): ProcessOutput { ... }
```

---

### Defensive Programming
**Definition:** Write code that anticipates and handles potential problems proactively.

**Why it matters:**
- Graceful handling of unexpected inputs
- Better error messages
- More robust system

**Application:**
```
❌ Bad: items.forEach(item => process(item))  // assumes items is array
✓ Good: (items ?? []).forEach(item => process(item))
```

---

### Single Responsibility
**Definition:** Each function/class/module should have one reason to change, one job to do.

**Why it matters:**
- Easier to test
- Easier to understand
- Changes don't ripple unexpectedly

**Application:**
```
❌ Bad: saveUserAndSendEmailAndLogActivity()
✓ Good: saveUser(), sendWelcomeEmail(), logActivity() - composed by caller
```

---

### Explicit Over Implicit
**Definition:** Make behavior obvious rather than relying on hidden conventions or magic values.

**Why it matters:**
- Code is self-documenting
- Fewer surprises
- Easier onboarding

**Application:**
```
❌ Bad: timeout = 0  // 0 means "no timeout" (magic value)
✓ Good: timeout = null, or timeout = Infinity, or hasTimeout = false
```

---

## Efficiency Principles

Principles for optimal resource usage and performance.

### Parallel-Independent
**Definition:** Run operations that don't depend on each other simultaneously.

**Why it matters:**
- Better resource utilization
- Faster execution
- Improved user experience

**Application:**
```
❌ Bad: await fetchUser(); await fetchOrders(); await fetchSettings();
✓ Good: await Promise.all([fetchUser(), fetchOrders(), fetchSettings()])
```

---

### Lazy Evaluation
**Definition:** Defer computation until the result is actually needed.

**Why it matters:**
- Avoids unnecessary work
- Reduces memory usage
- Faster startup times

**Application:**
```
❌ Bad: const allUsers = await db.users.findAll(); return allUsers.slice(0, 10);
✓ Good: return await db.users.findAll({ limit: 10 });
```

---

### Cache-Reuse
**Definition:** Store and reuse expensive computation results instead of recomputing.

**Why it matters:**
- Faster subsequent requests
- Reduced load on resources
- Better scalability

**Application:**
```
❌ Bad: Every request fetches user from database
✓ Good: Cache user object, invalidate on user update
```

---

## Error Handling Principles

Principles for robust error management.

### No-Swallow
**Definition:** Never catch an exception and ignore it silently.

**Why it matters:**
- Silent failures are hardest to debug
- Problems surface elsewhere
- Data corruption risks

**Application:**
```
❌ Bad: try { ... } catch (e) { /* ignore */ }
✓ Good: try { ... } catch (e) { logger.error(e); throw; }
```

---

### User-Actionable Errors
**Definition:** Error messages should tell users what went wrong AND what they can do about it.

**Why it matters:**
- Users can self-serve
- Reduced support load
- Better user experience

**Application:**
```
❌ Bad: "Error: ENOENT"
✓ Good: "Config file not found at ~/.config/app.json. Run 'app init' to create one."
```

---

### Rollback State
**Definition:** On failure, leave the system in a consistent state (ideally the state before the operation).

**Why it matters:**
- No partial updates
- Safe to retry
- Data integrity preserved

**Application:**
```
❌ Bad: Create user, then create profile (profile fails → orphan user)
✓ Good: Transaction: create user + profile together, rollback both on failure
```

---

## Analysis Principles

Principles for understanding and debugging systems.

### Architecture-First
**Definition:** Before fixing symptoms, understand the system design that led to the problem.

**Why it matters:**
- Fixes root cause, not symptoms
- Prevents similar issues
- Informs better solutions

**Application:**
```
❌ Bad: Adding another cache layer to fix slow queries
✓ Good: Understanding why queries are slow (N+1? missing index? wrong joins?)
```

---

### Root-Cause-Hunt
**Definition:** Ask "why does this pattern exist?" not just "what's wrong?"

**Why it matters:**
- Permanent fixes vs. temporary patches
- Reveals systemic issues
- Improves overall architecture

**Application:**
```
❌ Bad: "There's a null check missing here" → add null check
✓ Good: "Why can this be null? Should it be null? Fix at source."
```

---

## UX/DX Principles

Principles for great user and developer experience.

### Minimum Friction
**Definition:** Achieve the goal in the fewest possible steps.

**Why it matters:**
- Higher completion rates
- Better user satisfaction
- Less room for error

**Application:**
```
❌ Bad: 5-step wizard to create an item
✓ Good: Single form with smart defaults, advanced options expandable
```

---

### Maximum Clarity
**Definition:** Output should be unambiguous with clear next actions.

**Why it matters:**
- No guessing required
- Faster decision making
- Fewer errors

**Application:**
```
❌ Bad: "Operation completed"
✓ Good: "Created user john@example.com (ID: 123). View at /users/123"
```

---

### Predictable
**Definition:** Same inputs produce same outputs. Behavior is consistent across the system.

**Why it matters:**
- Users build accurate mental models
- Easier to automate
- Reduces errors

**Application:**
```
❌ Bad: Sometimes returns array, sometimes single object
✓ Good: Always returns array (single item = array of one)
```

---

### Fast Feedback
**Definition:** Show progress and results as quickly as possible.

**Why it matters:**
- Users know the system is working
- Can catch errors early
- Better perceived performance

**Application:**
```
❌ Bad: Spinner for 30 seconds, then all results at once
✓ Good: Stream results as they become available, show progress
```

---

## AI-Specific Principles

Principles specific to AI coding assistants.

### Read-First
**Definition:** Never propose edits to files that haven't been read first.

**Why it matters:**
- Accurate understanding of existing code
- No outdated assumptions
- Proper integration with existing patterns

---

### Plan-Before-Act
**Definition:** Understand the full scope of a task before making any changes.

**Why it matters:**
- Holistic solutions
- Proper sequencing
- Fewer rollbacks needed

---

### No-Hallucination
**Definition:** Only reference APIs, features, and functions that actually exist.

**Why it matters:**
- Code that actually works
- No debugging phantom APIs
- User trust preserved

---

### Visible-State
**Definition:** Users should always know what the AI is doing and what state the system is in.

**Why it matters:**
- User control
- Appropriate expectations
- Better collaboration

---

## Quick Reference Table

| Principle | Category | One-Line Summary |
|-----------|----------|------------------|
| SSOT | Design | One authoritative source for each piece of data |
| DRY | Design | Extract common patterns, no duplication |
| YAGNI | Design | Don't build until needed |
| KISS | Design | Simplest solution that works |
| Separation-of-Concerns | Design | One job per module |
| Composition | Design | Combine objects over inheritance |
| Idempotent | Design | Same result regardless of repetition |
| Least-Astonishment | Design | Behavior matches expectations |
| Fail-Fast | Quality | Immediate visible failure |
| Immutable | Quality | Don't modify, create new |
| Type-Safe | Quality | Catch errors at compile time |
| Defensive | Quality | Anticipate and handle problems |
| Single-Responsibility | Quality | One reason to change |
| Explicit | Quality | No magic values or hidden behavior |
| Parallel-Independent | Efficiency | Run unrelated ops simultaneously |
| Lazy-Evaluation | Efficiency | Defer until needed |
| Cache-Reuse | Efficiency | Store expensive results |
| No-Swallow | Error | Never silently catch exceptions |
| User-Actionable | Error | Tell users what to do |
| Rollback-State | Error | Consistent state on failure |
| Architecture-First | Analysis | Understand design before fixing |
| Root-Cause-Hunt | Analysis | Ask why, not just what |
| Minimum-Friction | UX/DX | Fewest steps to goal |
| Maximum-Clarity | UX/DX | Unambiguous output |
| Predictable | UX/DX | Consistent behavior |
| Fast-Feedback | UX/DX | Show progress immediately |
| Read-First | AI | Read before editing |
| Plan-Before-Act | AI | Understand before changing |
| No-Hallucination | AI | Only existing APIs |
| Visible-State | AI | User knows current state |

---

*See [Rules Documentation](rules.md) for implementation details.*

*Back to [README](../README.md)*
