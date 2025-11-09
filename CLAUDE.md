# Claude Code Development Guide

**Universal guide for working with Claude Code across any project**

---

## CCO Initialization (First Time Setup)

### Quick Start

```bash
# Quick Mode - AI auto-configures everything (~10 seconds)
python -m claudecodeoptimizer init

# Interactive Mode - Full wizard with 8 questions (~2-5 minutes)
python -m claudecodeoptimizer init --mode=interactive

# Or in Claude Code
/cco-init
```

### How It Works

**Two Modes, Same Decision Tree:**

1. **Quick Mode** (Recommended)
   - AI analyzes your project automatically
   - Auto-decides: Project type, team size, maturity, philosophy
   - Configures: Principles, commands, security, documentation
   - Duration: ~10 seconds

2. **Interactive Mode** (Full Control)
   - **TIER 0**: System detection (automatic)
   - **TIER 1**: Fundamental decisions (4 questions)
   - **TIER 2**: Strategy decisions (4 questions)
   - **TIER 3**: Tactical decisions (dynamic)

**Output Files:**
```
.cco/
  ├── project.json      # Full project configuration
  └── commands.json     # Enabled commands registry

PRINCIPLES.md           # Active development principles

.claude/
  └── commands/         # Slash command files (cco-*.md)
```

---

## Development Principles

**⚠️ MANDATORY: All work MUST follow these principles ⚠️**

```
@PRINCIPLES.md
```

This file contains the mandatory development principles for this project. **You MUST**:
- Follow ALL applicable principles in EVERY task
- Never deviate from these principles without explicit approval
- Check compliance before claiming work is complete
- Reference principles when making decisions

**Core Principles** (always apply):
- **P001**: Fail-Fast Error Handling
- **P067**: Evidence-Based Verification
- **P071**: Anti-Overengineering

For detailed principles by category, see:
- [Code Quality](docs/cco/principles/code-quality.md)
- [Security](docs/cco/principles/security.md)
- [Testing](docs/cco/principles/testing.md)
- [Architecture](docs/cco/principles/architecture.md)
- [Performance](docs/cco/principles/performance.md)
- [Operations](docs/cco/principles/operations.md)

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

**Examples:**
```
✅ [Runs pytest] [Shows: 34/34 passed] "All tests pass"
❌ "Tests should pass now"

✅ [Runs npm run build] [Shows: Build successful] "Build succeeds"
❌ "Build looks correct"
```

**Never use**: "should work", "looks correct", "appears to", "seems like"
**Always show**: Command output, exit codes, actual results

**Detailed guide**: [@docs/cco/guides/verification-protocol.md](docs/cco/guides/verification-protocol.md)

---

## Complete Action Reporting & Transparency

**CRITICAL: Every action must be explicitly reported to the user**

### The Problem
```
❌ BAD: Silent actions without reporting
Bash("rm temp.txt")           # File deleted
[No mention in response]      # User unaware

✅ GOOD: All actions reported
Bash("rm temp.txt")
"Deleted temp.txt (cleanup)"  # User informed
```

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
      - Added alpha status warning

   2. **Deleted files**:
      - requirements.txt.lock (no longer needed)
      - README.tmp (temporary file)

   3. **Updated .gitignore**:
      - Added *.lock pattern
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
   - Create files without listing them
   - Any "cleanup" without reporting

   ✅ REQUIRED:
   - "Deleted X because Y"
   - "Updated X: changed A to B"
   - "Created X with Y content"
   - "Cleaned up: removed X, Y, Z"
   ```

5. **Verification commands don't need reporting**
   ```
   ✅ OK to not report:
   - Read commands (reading files for analysis)
   - Grep/Glob searches
   - Git status/diff checks
   - Tool version checks

   ❌ MUST report:
   - Any command that modifies state
   - File creation/deletion/modification
   - Configuration changes
   - System installations
   ```

### Template for Task Completion

**Always end complex tasks with**:

```markdown
## ✅ Summary of Changes

**Modified**:
- `file1.py` - Added feature X
- `file2.json` - Updated configuration Y

**Created**:
- `new_file.md` - Documentation for Z

**Deleted**:
- `temp_file.txt` - Cleanup after operation
- `old_config.json` - Replaced by new format

**Actions Taken**:
1. Did X
2. Did Y
3. Did Z

**Next Steps**:
- User should review X
- User should test Y
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

**Why:** Confirms you're testing the right thing, prevents false positives

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
   - Consider defense-in-depth for critical paths

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
git status                           # Best: Stay in current directory

# Path quoting (all platforms)
cd "/path/with spaces/dir"           # Always quote paths with spaces
git -C "/path/with spaces" status    # Quote in all commands
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

**Parallel Execution:**
- **CRITICAL**: Launch all parallel agents in a SINGLE message for true parallelism
- Never launch agents sequentially when they can run in parallel

**Model Selection for Cost Optimization:**
- **Haiku**: Simple edits <50 lines, grep/search, docs, formatting, data gathering
- **Sonnet**: Features, bugs, complex analysis, aggregation, synthesis
- **Opus**: Reserved for extremely complex reasoning (rarely needed)

### Performance Metrics
- 2-3x speed boost for parallel operations
- 5x parallel task execution capacity demonstrated
- 79% faster feature delivery (industry data)

---

## Git Workflow

**Commit Management:**
- User manages all git operations via their preferred git client
- Never suggest git commands or commit messages
- Never create commits automatically
- User decides when and how to commit changes

**Pull Requests:**
- User creates PRs via their preferred method
- Never auto-create PRs without explicit request

**Detailed guide**: [@docs/cco/guides/git-workflow.md](docs/cco/guides/git-workflow.md)

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

## Detailed Guides (On-Demand Loading)

For comprehensive workflows, load these guides as needed:

### Verification & Quality
- **[@docs/cco/guides/verification-protocol.md](docs/cco/guides/verification-protocol.md)**
  - Evidence-based verification workflow
  - Examples of good/bad verification
  - Implements P067

### Development Workflow
- **[@docs/cco/guides/git-workflow.md](docs/cco/guides/git-workflow.md)**
  - Branch strategies (Main-Only, GitHub Flow, Git Flow)
  - Commit conventions and versioning
  - Daily workflow examples

### Security
- **[@docs/cco/guides/security-response.md](docs/cco/guides/security-response.md)**
  - Pre-commit security review
  - Security analysis workflow
  - Common vulnerabilities & fixes
  - Incident response plan

### Performance
- **[@docs/cco/guides/performance-optimization.md](docs/cco/guides/performance-optimization.md)**
  - Common bottlenecks (O(n²), N+1, caching)
  - Two-tool framework (Claude.ai + Claude Code)
  - Benchmarking and profiling

### Infrastructure
- **[@docs/cco/guides/container-best-practices.md](docs/cco/guides/container-best-practices.md)**
  - Dockerfile optimization (multi-stage, minimal base)
  - Kubernetes patterns (resources, health checks)
  - GitOps workflow

---

## Token Optimization Summary

**Progressive Disclosure Strategy:**
- **CLAUDE.md**: ~1500 tokens (core guidelines)
- **PRINCIPLES.md**: ~500 tokens (core principles)
- **Guides**: ~500-2000 tokens each (load on-demand)
- **Total reduction**: 5-10x (typical usage)

**Load guides as needed:**
```
@docs/cco/guides/verification-protocol.md
@docs/cco/guides/git-workflow.md
@docs/cco/guides/security-response.md
@docs/cco/guides/performance-optimization.md
@docs/cco/guides/container-best-practices.md
```

**Load category-specific principles:**
```
@docs/cco/principles/code-quality.md
@docs/cco/principles/security.md
@docs/cco/principles/testing.md
@docs/cco/principles/architecture.md
@docs/cco/principles/performance.md
```

---

*Part of CCO Documentation System*
*Pattern from wshobson/agents: Progressive disclosure*
