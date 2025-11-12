# Claude Code Development Guide


**Project:** ClaudeCodeOptimizer
**Team:** Solo Developer
**Quality:** Strict
**Testing:** Balanced
**Generated:** 2025-11-12
---

## Development Principles

**⚠️ MANDATORY: All work MUST follow these principles ⚠️**

<!-- CCO_START -->
### Core Principles (Always Apply)
**Universal Principles** (apply to ALL projects):

#### U001: Evidence-Based Verification
Never claim completion without command execution proof. All verification requires fresh command output with exit codes.
**Details**: `.claude/principles/U001.md`

#### U002: Fail-Fast Error Handling
Errors must cause immediate, visible failure. No silent fallbacks, no swallowed exceptions.
**Details**: `.claude/principles/U002.md`

#### U003: Test-First Development
Write failing test FIRST, then implement feature, then verify test passes.
**Details**: `.claude/principles/U003.md`

**Additional Universal Principles:**
- **U004**: Root Cause Analysis → `.claude/principles/U004.md`
- **U005**: Minimal Touch Policy → `.claude/principles/U005.md`
- **U006**: Model Selection Strategy → `.claude/principles/U006.md`
- **U007**: Token Optimization → `.claude/principles/U007.md`
- **U008**: Complete Action Reporting → `.claude/principles/U008.md`
- **U009**: Atomic Commits → `.claude/principles/U009.md`
- **U010**: Concise Commit Messages → `.claude/principles/U010.md`
- **U011**: No Overengineering → `.claude/principles/U011.md`
- **U012**: Cross-Platform Bash Commands → `.claude/principles/U012.md`

### Project-Specific Principles
For detailed principles, see individual files:

**Code Quality** (5 selected):
- **P001**: DRY Enforcement → `.claude/principles/P001.md`
- **P002**: Complete Integration Check → `.claude/principles/P002.md`
- **P007**: Linting & SAST Enforcement → `.claude/principles/P007.md`
- **P009**: Type Safety & Static Analysis → `.claude/principles/P009.md`
- **P010**: Centralized Version Management → `.claude/principles/P010.md`

**Architecture** (1 selected):
- **P012**: Event-Driven Architecture → `.claude/principles/P012.md`

**Security & Privacy** (17 selected):
- **P022**: Schema-First Validation → `.claude/principles/P022.md`
- **P023**: Privacy-First by Default → `.claude/principles/P023.md`
- **P025**: Encryption Everywhere → `.claude/principles/P025.md`
- **P026**: Zero Disk Touch → `.claude/principles/P026.md`
- **P027**: Authentication & Authorization → `.claude/principles/P027.md`
- **P028**: SQL Injection Prevention → `.claude/principles/P028.md`
- **P029**: Secret Management with Rotation → `.claude/principles/P029.md`
- **P030**: Rate Limiting & Throttling → `.claude/principles/P030.md`
- **P032**: Input Sanitization (XSS Prevention) → `.claude/principles/P032.md`
- **P033**: Audit Logging → `.claude/principles/P033.md`
- **P034**: Supply Chain Security → `.claude/principles/P034.md`
- **P035**: AI/ML Security → `.claude/principles/P035.md`
- **P036**: Container Security → `.claude/principles/P036.md`
- **P037**: Kubernetes Security → `.claude/principles/P037.md`
- **P038**: Zero Trust Architecture → `.claude/principles/P038.md`
- **P039**: Privacy Compliance → `.claude/principles/P039.md`
- **P040**: Dependency Management → `.claude/principles/P040.md`

**Testing** (3 selected):
- **P041**: Test Coverage Targets → `.claude/principles/P041.md`
- **P043**: Integration Tests for Critical Paths → `.claude/principles/P043.md`
- **P045**: CI Gates → `.claude/principles/P045.md`

**Performance** (2 selected):
- **P054**: Database Query Optimization → `.claude/principles/P054.md`
- **P056**: Async I/O (Non-Blocking Operations) → `.claude/principles/P056.md`

**API Design** (1 selected):
- **P069**: API Security Best Practices → `.claude/principles/P069.md`

**Total**: 12 universal + 29 project-specific = 41 principles
<!-- CCO_END -->

---

<!-- CCO_SKILLS_START -->
## Available Skills

**Workflow Skills** (reusable patterns):

**Universal Skills:**
- **Incremental Improvement** → `.claude/skills/incremental-improvement.md`
- **Root Cause Analysis** → `.claude/skills/root-cause-analysis.md`
- **Security Emergency Response** → `.claude/skills/security-emergency-response.md`
- **Test First Verification** → `.claude/skills/test-first-verification.md`
- **Verification Protocol** → `.claude/skills/verification-protocol.md`

**Python-Specific Skills:**
- **Async Patterns** → `.claude/skills/python/async-patterns.md`
- **Packaging Modern** → `.claude/skills/python/packaging-modern.md`
- **Performance** → `.claude/skills/python/performance.md`
- **Testing Pytest** → `.claude/skills/python/testing-pytest.md`
- **Type Hints Advanced** → `.claude/skills/python/type-hints-advanced.md`

**Total**: 10 skills available
<!-- CCO_SKILLS_END -->

<!-- CCO_AGENTS_START -->
## Available Agents

**Specialized AI Agents** (autonomous task execution):

- **Audit Agent** → `.claude/agents/audit-agent.md`
  Comprehensive code quality, security, and best practices analysis
- **Fix Agent** → `.claude/agents/fix-agent.md`
  Automated issue resolution with root cause analysis
- **Generate Agent** → `.claude/agents/generate-agent.md`
  Code, test, and documentation generation

**Total**: 3 agents available
<!-- CCO_AGENTS_END -->

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

## Commit Guidelines

**Principles**: Follow applicable development principles
See `.claude/principles/` for detailed rules.

**Commit Management:**
- User manages all git operations via their preferred git client
- Never suggest git commands or commit messages
- Never create commits automatically
- User decides when and how to commit changes

**Note**: Additional workflow sections are dynamically added based on your project's configuration.

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
