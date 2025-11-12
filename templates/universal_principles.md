### U001: Evidence-Based Verification

Never claim completion without command execution proof.

**Example**:
```
✅ [Runs: pytest] [Output: 34/34 passed] [Exit: 0] "All tests pass"
❌ "Tests should pass now"
```

**Why**: Catches silent failures early.

---

### U002: Fail-Fast Error Handling

Errors must cause immediate, visible failure. No silent fallbacks, no swallowed exceptions.

**Example**:
```python
# ✅ Good
try:
    result = risky()
except SpecificError as e:
    logger.error(f'Failed: {e}')
    raise

# ❌ Bad
try:
    result = risky()
except:
    pass
```

**Why**: Catches bugs early before production.

---

### U003: Test-First Development

Write failing test FIRST, then implement, then verify test passes.

**Process**: Test (fail) → Implement → Test (pass)

**Why**: Ensures tests actually verify behavior.

---

### U004: Root Cause Analysis

Trace to source. Fix at entry point, not deep in stack.

**Example**:
```
Error: Function crashes with empty string
↓ Trace: ProcessData('')
↓ Trace: APIHandler passed empty
↓ Trace: Missing input validation
✅ Fix: Add validation at API entry
❌ Wrong: Add null check in ProcessData
```

**Why**: Prevents band-aid fixes.

---

### U005: Minimal Touch Policy

Edit only required files. No "drive-by improvements", no scope creep.

**Rule**: Change only what's needed for the task.

**Why**: Reduces merge conflicts, makes changes reviewable.

---

### U006: Model Selection Strategy

Strategic model selection for cost optimization.

- **Haiku**: Data gathering, scanning, simple edits <50 lines
- **Sonnet** (default): Analysis, reasoning, features, bugs
- **Opus**: Avoided (use only for extreme complexity)

**Why**: Optimizes cost and latency.

---

### U007: Token Optimization

Grep-first approach, targeted reads.

**Pattern**:
```bash
Grep("pattern", output_mode="files_with_matches")  # Find
Grep("pattern", output_mode="content", -C=5)       # Context
Read(file.py, offset=40, limit=30)                 # Targeted
```

**Why**: Reduces token costs, improves speed.

---

### U008: Complete Action Reporting

Every action must be explicitly reported. No hidden operations.

**Rule**: Report EVERY tool use that modifies state.

**Forbidden**: Bash("rm file") without mentioning in response

**Required**: "Deleted X because Y"

**Why**: Builds trust, prevents surprises.

---

### U009: Atomic Commits

One commit = one logical change. Never mix unrelated changes.

**Example**:
```bash
✅ git commit -m "fix(auth): handle expired tokens"
   Modified: auth.py

❌ git commit -m "fix login, add tests, update README"
   Modified: auth.py, tests/, README.md, db.py
```

**Why**: Makes git bisect, revert, review easier.

---

### U010: Concise Commit Messages

Max 10 lines total, max 5 bullets in body.

**Format**:
```
type(scope): description (max 72 chars)

- Key change 1
- Key change 2

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Why**: Fast to read, easy to scan in history.

---

### U011: No Overengineering

Choose the simplest solution. Avoid premature abstraction.

**Example**:
```python
# ✅ Good: Simple and direct
def send_email(to, subject, body):
    smtp.send(to, subject, body)

# ❌ Bad: Premature abstraction
class AbstractDataProcessorFactory:
    @abstractmethod
    def create_processor(self): pass
```

**Rule**: Wait for 3+ similar use cases before abstracting.

**Why**: Every line of code is a liability.

---

### U012: Cross-Platform Bash Commands

Use cross-platform compatible commands.

**Best Practice**:
```bash
✅ git -C "/path/to/dir" status  # Works everywhere
✅ cd "/path/with spaces/dir"    # Always quote paths
✅ (cd "/path" && git status)    # Subshell works

❌ cd C:\Windows\path            # Windows-only
```

**Why**: Works on Windows, macOS, Linux without modification.
