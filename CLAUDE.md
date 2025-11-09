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
   - Detects: OS, terminal, locale, languages, frameworks, tools
   - Auto-decides: Project type, team size, maturity, philosophy
   - Configures: Principles, commands, security, documentation
   - Duration: ~10 seconds

2. **Interactive Mode** (Full Control)
   - **TIER 0**: System detection (automatic)
   - **TIER 1**: Fundamental decisions (4 questions)
     - Project purpose (API/Web/Library/CLI/Data/Desktop/Mobile)
     - Team dynamics (Solo/Small/Growing/Large)
     - Project maturity (Prototype/MVP/Active/Production/Maintenance)
     - Development philosophy (Move Fast/Balanced/Quality-First)
   - **TIER 2**: Strategy decisions (4 questions)
     - Principle selection (Minimal/Recommended/Comprehensive/Custom)
     - Testing approach (None/Critical/Balanced/Comprehensive)
     - Security stance (Standard/Production/High)
     - Documentation level (Minimal/Practical/Comprehensive)
   - **TIER 3**: Tactical decisions (dynamic)
     - Tool preferences (when conflicts: ruff vs black, pytest vs unittest)
     - Command selection (12+ specialized commands)

**Key Features:**
- 🎯 **Cascading AI Hints**: Each answer informs next recommendations
- 🔧 **Tool Comparison**: Smart recommendations with clear rationale
  - "You have: black, ruff → Recommend: ruff (faster, all-in-one)"
- 🚫 **Anti-Overengineering**: Principle P071 enforces pragmatic solutions
- 🌍 **Multi-Language**: Auto-detects locale (Turkish, English, etc.)
- ⚡ **Context-Aware**: Command selection based on project needs

**Output Files:**
```
.cco/
  ├── project.json      # Full project configuration
  └── commands.json     # Enabled commands registry

PRINCIPLES.md           # Active development principles (reference with @PRINCIPLES.md)

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

**Usage:**
```
@PRINCIPLES.md  # Read at start of every session
@PRINCIPLES.md Check if this code follows our principles
@PRINCIPLES.md What principle applies to error handling?
```

**Compliance is non-negotiable.** These principles are not suggestions - they are requirements.

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

### Why This Matters

1. **Trust**: User knows exactly what you did
2. **Verification**: User can check each action
3. **Debugging**: If something breaks, user knows what changed
4. **Learning**: User understands the process
5. **Compliance**: Audit trail for all changes

### Enforcement

- This is **MANDATORY**, not optional
- Violation = incomplete work
- TodoWrite helps track this automatically
- Use P067 (Evidence-Based Verification) pattern

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
- Haiku: Simple edits <50 lines, grep/search, docs, formatting
- Sonnet (default): Features, bugs, API endpoints, security fixes

**Cross-Platform Bash Commands:**
```bash
# ❌ WRONG: Platform-specific syntax
cd /d D:\path && git status          # Windows CMD (causes permission errors)
cd C:\Users && ls                    # Backslashes fail on Linux/macOS

# ✅ CORRECT: Cross-platform alternatives
git -C "/path/to/dir" status         # Best: Works on all platforms
git -C "D:/GitHub/project" status    # Windows: Forward slash works in git
(cd "/path" && git status)           # OK: Subshell (any platform)
git status                           # Best: Stay in current directory

# Path quoting (all platforms)
cd "/path/with spaces/dir"           # Always quote paths with spaces
git -C "/path/with spaces" status    # Quote in all commands
```

**Cross-Platform Encoding (Test Scripts):**
```python
# Universal encoding fix for test scripts (Windows/Linux/macOS)
import sys, io

# Configure UTF-8 on all platforms
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8',
        errors='replace',
        line_buffering=True
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer,
        encoding='utf-8',
        errors='replace',
        line_buffering=True
    )
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
❌ "Improve error handling" (no location)
```

**For large files (>500 lines):**
1. Grep to find location
2. Read with offset+limit (only ±20 lines around target)

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
- Example: Research tasks across multiple modules

**Model Selection for Cost Optimization:**
- **Haiku**: Simple edits <50 lines, grep/search, docs, formatting, data gathering
- **Sonnet**: Features, bugs, complex analysis, aggregation, synthesis
- **Opus**: Reserved for extremely complex reasoning (rarely needed)

**Agent Specialization:**
- Create custom agents for repeated specialized tasks
- Use Explore agents for codebase analysis
- Use Plan agents for multi-step workflows
- Reuse agent patterns across similar tasks

### Performance Metrics
- 2-3x speed boost for parallel operations
- 5x parallel task execution capacity demonstrated
- 79% faster feature delivery (industry data)

### Cost Optimization
- Haiku for data gathering: Fast, cheap, efficient
- Sonnet for synthesis: Better reasoning when needed
- Avoid over-provisioning (don't use Sonnet for simple tasks)
- Monitor token usage and optimize model selection

### Example Pattern
```
# GOOD: Parallel agents in SINGLE message
Task("analyze auth module", model="haiku")
Task("analyze api module", model="haiku")
Task("analyze db module", model="haiku")
# All three run simultaneously

# Then aggregate with Sonnet
Task("synthesize findings from all modules", model="sonnet")

# BAD: Sequential launches (slow)
result1 = Task("analyze auth")
# Wait...
result2 = Task("analyze api")
# Wait...
result3 = Task("analyze db")
```

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

---

## Git Workflow

**Solo developer workflow** - Simple, practical, anti-overengineering

### Branch Strategy: Main-Only

**Simple is better**:
- ✅ Work directly on `main` branch
- ✅ Always keep it in working state
- ✅ No feature branches (solo dev = no need)
- ✅ Rollback via commit history if needed

**Rationale**: P071 (Anti-Overengineering) - Branch complexity unnecessary for solo projects

---

### Commit Strategy: Grouped & Categorized

**Format**: `type(scope): subject`

**Types**:
```
feat:     New feature
fix:      Bug fix
docs:     Documentation only
refactor: Code improvement (no behavior change)
test:     Add/update tests
chore:    Build, deps, config
```

**Scopes** (CCO-specific):
```
wizard, installer, detection, principles, commands,
skills, core, cli, tests, docs, deps, ci
```

**Examples**:
```bash
# Good: Grouped changes, same category
feat(docs): restructure documentation system
- Create docs/cco/ structure
- Move PRINCIPLES.md to docs/cco/
- Split principles by category
- Update references in code

# Good: Single logical change
fix(installer): handle Windows permission errors

# Bad: Multiple unrelated changes
feat: updates and fixes
```

**Commit Rules**:
- ✅ Group related changes in same category
- ✅ One logical unit per commit
- ✅ Include related tests + docs
- ❌ Don't mix different topics/categories
- ❌ No WIP commits
- ❌ No failing tests

---

### Push Strategy: Task-Based

**When to push**:
```bash
# After each TODO task completes
git add .
git commit -m "feat(docs): create docs/cco structure"
git push origin main

# After grouped changes
git commit -m "refactor(principles): split by category"
git push origin main
```

**Benefits**:
- 📊 Every change tracked
- ⏮️ Easy rollback per task
- 📝 Clear history
- 🔄 Safe incremental progress

**Never push**:
- ❌ Failing tests
- ❌ Syntax errors
- ❌ Incomplete features

---

### Versioning: Semantic + Milestone-Based

**Format**: `MAJOR.MINOR.PATCH-prerelease`

**Rules**:
- **MINOR** bump: Every milestone (P0, v0.2.0, v0.3.0, etc.)
- **MAJOR** bump: Breaking changes or significant architecture changes
- **PATCH** bump: Bug fixes between milestones

**Current Roadmap**:
```
v0.1.0-alpha  ✅ Initial release
v0.2.0-alpha  ⏳ P0 + Production readiness
v0.3.0-beta      UX improvements
v0.4.0-rc        Extensibility
v1.0.0           Stable release (MAJOR bump)
```

**When to tag**:
```bash
# After milestone complete
git tag -a v0.2.0-alpha -m "Production Readiness Milestone

Completed:
- P0: wshobson/agents integration
- 60% test coverage
- CI/CD pipeline operational
- Zero critical bugs

See CHANGELOG.md for details"

git push origin v0.2.0-alpha
```

**Major Version Triggers** (0.x → 1.x):
- ✅ API stability guarantee
- ✅ Production-ready quality
- ✅ Breaking changes minimized
- ✅ Migration guide provided

**Major Version Triggers** (1.x → 2.x):
- ✅ Fundamental architecture change
- ✅ Breaking API changes
- ✅ Plugin system overhaul
- ✅ Must provide upgrade path

---

### Example Workflow

**Daily Work Pattern**:

```bash
# Morning: Start on TODO task
# ... work on P0.1 Task 1 (Export/import removal) ...

# Midday: Task 1 complete
git add claudecodeoptimizer/commands/config.md \
        claudecodeoptimizer/ai/command_selection.py
git commit -m "feat(commands): remove export/import functionality

- Remove export/import from config.md
- Remove export/import rules from command_selection.py
- Update command descriptions
- Tests pass

Closes #P0.1-Task1"

git push origin main

# Afternoon: Task 2 complete
git add claudecodeoptimizer/wizard/orchestrator.py \
        claudecodeoptimizer/core/installer.py \
        tests/unit/test_installer.py
git commit -m "fix(wizard): install only recommended commands

- Filter commands to core + recommended only
- Update installer to accept command list
- Add tests for command filtering
- Verify ~/.claude/commands/ contains only 8-12 commands

Closes #P0.1-Task2"

git push origin main

# End of day: Update TODO
git add TODO.md
git commit -m "docs(todo): mark P0.1 tasks 1-2 as complete"
git push origin main
```

**Milestone Complete**:

```bash
# All P0 tasks done, tests pass, ready for v0.2.0
git tag -a v0.2.0-alpha -m "Production Readiness

- P0 integration complete
- 60% test coverage achieved
- CI/CD operational
- Documentation restructured
- Token optimization implemented"

git push origin main --tags

# Update CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs(changelog): add v0.2.0-alpha release notes"
git push origin main
```

---

### Commit Quality Checklist

**Before committing**:
- [ ] All files in commit are related (same category/topic)
- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Linter clean (`ruff check .`)
- [ ] No debug code or commented blocks
- [ ] Commit message follows format
- [ ] Related docs updated

**Verification**:
```bash
# Check what's staged
git status
git diff --cached

# Verify tests
pytest tests/ -v

# Verify linting
ruff check .

# Commit only if all pass
git commit -m "type(scope): message"
```

---

### Rollback Strategies

**Undo last commit** (not pushed):
```bash
git reset --soft HEAD~1  # Keep changes
git reset --hard HEAD~1  # Discard changes
```

**Undo pushed commit** (task-based history makes this easy):
```bash
# Find commit to revert
git log --oneline

# Revert specific commit
git revert <commit-hash>
git push origin main
```

**Rollback to specific task**:
```bash
# Each task = 1 commit, easy to identify
git log --grep="P0.1-Task1"
git checkout <commit-hash>
```

---

### .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
.pytest_cache/
htmlcov/
.coverage

# CCO
.cco/reports/          # Generated reports
.cco/cache/            # Cache (future)

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Temp
*.tmp
*.log
```

---

### Best Practices Summary

**DO**:
- ✅ Commit per TODO task
- ✅ Group related changes
- ✅ Push after each task
- ✅ Tag at milestones
- ✅ Keep main working
- ✅ Write clear messages

**DON'T**:
- ❌ Mix unrelated changes
- ❌ Commit WIP code
- ❌ Push failing tests
- ❌ Create feature branches
- ❌ Batch multiple tasks
- ❌ Skip commit messages

**Anti-Overengineering (P071)**:
- No complex branching (solo dev)
- No PR reviews (solo dev)
- No git hooks (unless CI requires)
- Simple is sufficient

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

## Security Incident Response

**Shift-left security approach:** Integrate security analysis into the development loop, not as a final gate.

### Pre-Commit Security Review
**Always scan before commits:**
- SQL injection and ORM security
- Cross-site scripting (XSS) vulnerabilities
- Authentication/authorization gaps
- Sensitive data exposure
- Third-party package vulnerabilities

### Security Analysis Workflow

**Quick Triage (Claude.ai):**
- Paste code snippets for immediate vulnerability assessment
- Get threat modeling for new features before implementation
- Transform scanner reports into ranked, actionable steps
- Ask specific questions (API key storage, file upload safety, authentication)

**System-Wide Analysis (Claude Code):**
- Analyze authentication flows across entire codebase
- Identify specific files/line numbers with vulnerabilities
- Implement targeted fixes integrated with existing security architecture
- Examine dependencies and trace security issues systematically

### Native Sandboxing

**Two essential isolation mechanisms (both required):**

**1. Filesystem Isolation:**
- Restrict access to specific directories only
- Allow read/write to current working directory
- Block external modifications
- Prevents compromised agents from modifying sensitive system files

**2. Network Isolation:**
- Limit connections to approved servers only
- Use proxy server to enforce domain restrictions
- Handle user confirmations for new requests
- Prevents data exfiltration and malware downloads

**Benefits:**
- Reduced friction (fewer approval delays)
- Maintained security (compromised processes remain isolated)
- Improved transparency (boundary violations trigger immediate alerts)

---

## Performance Optimization

**Proactive performance engineering:** Analyze code continuously rather than waiting for production issues.

### Common Performance Bottlenecks
- Nested loops creating O(n²) complexity
- N+1 database query problems (database calls inside loops)
- Inefficient queries lacking proper indexes
- Missing caching layers for repeated operations
- Redundant data processing

### Two-Tool Performance Framework

**Quick Investigation (Claude.ai):**
1. Paste problematic functions for complexity analysis
2. Get specific optimization recommendations
3. Determine if issues are algorithmic, structural, or configuration-related
4. Decide between quick code changes or comprehensive architectural reviews

**Comprehensive Optimization (Claude Code):**
1. Request optimization analysis of critical paths
2. Let Claude identify bottlenecks across multiple files
3. Automatically create tests and implement fixes
4. Validate improvements with generated benchmarks

### Strategic Implementation
- Focus analysis on performance-critical directories (api/, core/)
- Identify recurring inefficiency patterns for systematic improvements
- Use automated testing to prevent regressions
- Combine traditional profiling tools (Chrome DevTools, New Relic, Datadog) with AI analysis
- Measure performance improvements objectively using benchmark tests

### Expected Impact
- Eliminating N+1 queries: 10-100x response time improvements
- Algorithmic replacements (O(n²) to O(n)): Gains proportional to dataset size

---

## Container & Kubernetes Best Practices

**For containerized applications:**

### Dockerfile Optimization
- Multi-stage builds for smaller images
- Minimal base images (alpine, distroless)
- Layer caching optimization
- Security hardening (non-root user, read-only filesystem)
- Dependency scanning and vulnerability patching

### Kubernetes Patterns
- Declarative manifests (no imperative kubectl commands)
- Resource requests and limits
- Health checks (liveness, readiness, startup probes)
- ConfigMaps and Secrets (never hardcode configuration)
- Pod security policies and admission controllers

### GitOps Workflow
- Infrastructure as Code (Terraform/Pulumi)
- Automated reconciliation (ArgoCD/Flux)
- Drift detection and correction
- Version control for all infrastructure changes
