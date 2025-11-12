# Claude Code Development Guide

---

## Development Principles

**⚠️ MANDATORY: All work MUST follow these principles ⚠️**

### Core Principles (Always Apply)

#### P001: Fail-Fast Error Handling

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

---

#### P067: Evidence-Based Verification

Never claim completion without command execution proof. All verification requires fresh command output with exit codes.

**Example**:
```
✅ [Runs: pytest] [Output: 34/34 passed] [Exit: 0] "All tests pass"
❌ "Tests should pass now"
```

---

#### P071: No Overengineering

Always choose the simplest solution that solves the problem. Avoid premature abstraction, unnecessary patterns, excessive architecture. Every line of code is a liability - write only what is needed now.

**Example**:
```python
# ✅ Good: Simple and direct
def send_email(to: str, subject: str, body: str):
    smtp.send(to, subject, body)

# ❌ Bad: Premature abstraction
class AbstractDataProcessorFactory:
    @abstractmethod
    def create_processor(self): pass
```

---

### Additional Principles by Category

For detailed principles in specific areas, see:

- **[Code Quality](~/.cco/principles/code_quality.md)** - DRY, type safety, immutability (14 principles)
- **[Security & Privacy](~/.cco/principles/security_privacy.md)** - Encryption, auth, secrets management (19 principles)
- **[Architecture](~/.cco/principles/architecture.md)** - Event-driven, microservices, patterns (10 principles)
- **[Testing](~/.cco/principles/testing.md)** - Coverage, isolation, CI gates (6 principles)
- **[Git Workflow](~/.cco/principles/git_workflow.md)** - Commits, branching, versioning (8 principles)
- **[Performance](~/.cco/principles/performance.md)** - Caching, optimization, async I/O (5 principles)
- **[Operations](~/.cco/principles/operations.md)** - Config as code, IaC, observability (10 principles)
- **[API Design](~/.cco/principles/api_design.md)** - RESTful, versioning, errors (2 principles)

**Total: 74 principles across 8 categories**

---

## Working Guidelines

### What NOT to Do
- ❌ No tests/linters/repo scans unless explicitly requested
- ❌ No TODO markers, debug prints, or dead code
- ❌ No breaking changes without approval
- ❌ Never create files unless absolutely necessary
- ❌ No proactive documentation files unless requested
- ❌ No git commit command suggestions (user manages commits)

### Always Prefer
- ✅ Edit existing files over creating new ones
- ✅ Follow existing code patterns
- ✅ Minimal, surgical changes
- ✅ Production-grade code from the start
- ✅ Parallel execution for multi-service tasks

### Critical Changes (Require Approval)
Submit a proposal before:
- New dependency/library additions
- Environment/infrastructure changes
- Breaking API changes
- Tasks affecting 5+ files

**Proposal format:**
```
PROPOSAL:
- Change: <one sentence>
- Reason: <one sentence>
- Impact: <files affected>
- Breaking: yes/no
```

---

## Verification Protocol

**BEFORE claiming any work is complete:**

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the command (fresh, complete output)
3. **VERIFY**: Check exit code, count failures
4. **REPORT**: State claim WITH evidence

**Never use**: "should work", "looks correct", "appears to", "seems like"
**Always show**: Command output, exit codes, actual results

---

## Complete Action Reporting

**CRITICAL: Every action must be explicitly reported to the user**

### Rules

1. **Report EVERY tool use in your response**
   - File operations (Read, Write, Edit, Bash rm/mv/cp)
   - Git operations (commit, push, branch, etc.)
   - Installation/configuration changes
   - Any system state modification

2. **Action Summary Pattern**
   ```
   ## ✅ Completed Actions

   1. **Updated README.md**:
      - Added installation instructions

   2. **Deleted files**:
      - temp.txt (cleanup)
   ```

3. **Use TodoWrite for multi-step tasks**
   - Mark each step as completed AS YOU DO IT
   - Don't batch completions
   - User can see real-time progress

4. **Hidden actions are FORBIDDEN**
   ```
   ❌ FORBIDDEN:
   - Bash("rm file") without mentioning in response
   - Edit file without explaining what changed

   ✅ REQUIRED:
   - "Deleted X because Y"
   - "Updated X: changed A to B"
   ```

5. **Verification commands don't need reporting**
   ```
   ✅ OK to not report: Read, Grep/Glob, Git status/diff checks
   ❌ MUST report: Any command that modifies state
   ```

---

## Test-First Development

**For new features:**
- Write failing test FIRST
- Run test, verify it fails
- Implement feature
- Run test, verify it passes

**For bugs:**
- Reproduce bug with failing test
- Verify test fails for the right reason
- Fix bug
- Verify test passes

---

## Root Cause Analysis

**When debugging, always trace to source:**

1. **Where does the bad value originate?**
   - Don't fix symptoms (validation checks deep in stack)
   - Trace backward through the call chain

2. **What called this with the bad value?**
   - Keep tracing up the stack
   - Find where it enters the system

3. **Fix at source, not symptom**
   - Add validation at entry point

**Example:**
```
Error: Function crashes with empty string
↓ Trace: ProcessData('') called function
↓ Trace: APIHandler passed empty string
↓ Trace: User input validation missing
✅ Fix: Add validation at API entry point
❌ Wrong: Add null check in ProcessData
```

---

## Minimal Touch Policy

- **Edit only required files** - no "drive-by improvements"
- **Preserve existing conventions** - don't reformat unnecessarily
- **No scope creep** - stick to the requested task
- **Production-grade only** - every change should be production-ready

---

## Token Optimization

**Model Selection:**
- **Haiku**: Simple edits <50 lines, grep/search, docs, formatting
- **Sonnet** (default): Features, bugs, API endpoints, security fixes

**Cross-Platform Bash Commands:**
```bash
# ✅ CORRECT: Cross-platform alternatives
git -C "/path/to/dir" status         # Best: Works on all platforms
git -C "D:/GitHub/project" status    # Windows: Forward slash works in git
(cd "/path" && git status)           # OK: Subshell (any platform)

# Path quoting (all platforms)
cd "/path/with spaces/dir"           # Always quote paths with spaces
```

**Grep-First Approach:**
```bash
Grep("pattern", path="file.py", output_mode="files_with_matches")  # Find files
Grep("pattern", path="file.py", output_mode="content", -C=5)       # Show context
Read(file.py, offset=40, limit=30)  # Read targeted section only
```

**Query Format:** `[file:line] → [action]`
```
Examples:
✅ "auth.py:127-145 → Add JWT refresh token support"
✅ "api/main.py:89 → Fix SQL injection with parameterized query"
❌ "Fix authentication bugs" (too vague)
```

---

## Multi-Agent Orchestration

**Use parallel sub-agents** for 2-3x performance boost on complex tasks.

### When to Use
- Scope: >5 files OR 2+ services
- Time: >5 minutes for sequential execution
- Complexity: Multiple independent operations

### Best Practices
- **CRITICAL**: Launch all parallel agents in a SINGLE message for true parallelism
- Never launch agents sequentially when they can run in parallel

**Model Selection:**
- **Haiku**: Simple edits <50 lines, grep/search, docs, formatting, data gathering
- **Sonnet**: Features, bugs, complex analysis, aggregation, synthesis
- **Opus**: Reserved for extremely complex reasoning (rarely needed)

---

## Git Workflow

**Atomic Commits (P073):** Each commit = one logical change. Group related files, separate unrelated changes.

**Commit Format (P072: Concise Commit Messages):**
```
type(scope): concise description (max 72 chars)

- Key change 1 with brief context
- Key change 2
- Key change 3

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Rules:**
- ✅ Max 10 lines total, 5 bullets max
- ✅ Co-Authored-By footer (GitHub contributor)
- ❌ No section headers or emojis

**Pre-Commit Checklist:**
Before each commit, run these checks locally:
- Code formatting check
- Linting
- Security vulnerabilities scan
- All tests pass

**Commit Management:**
- User manages all git operations via their preferred git client
- Never suggest git commands or commit messages
- Never create commits automatically
- User decides when and how to commit changes

---

## Documentation Updates

**When to update docs:**
- Architecture changes (new services, layer modifications)
- Data model changes (new fields, schema updates)
- API/CLI changes (new commands, parameters)
- Configuration changes (new env vars)

**How to update:**
- Present tense, clean slate approach (no "before/after")
- Concise (tables, lists, code blocks)
- Atomic updates (commit docs with code)

---

*Part of CCO Documentation System*
