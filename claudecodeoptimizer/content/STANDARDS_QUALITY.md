# CCO Command Quality Standards

**Purpose:** Enforce consistent UX/DX, maximum efficiency, simplicity, and performance across ALL CCO commands.

**Scope:** cco-audit, cco-fix, cco-generate, cco-optimize-code-performance, cco-optimize-context-usage, cco-implement, cco-commit

---

## Core Principles

Every CCO command MUST satisfy these requirements:

### 1. **Mükemmel UX/DX (User/Developer Experience)**

**Tutarlılık (Consistency):**
- ✅ Same step numbering across all commands (Step 0, 1, 2...)
- ✅ Same confirmation pattern (single AskUserQuestion at Step 0)
- ✅ Same progress reporting format
- ✅ Same error handling pattern
- ✅ Same output format (markdown with consistent headers)

**Öngörülebilirlik (Predictability):**
- ✅ Same parameter patterns (--security, --tests, --all)
- ✅ Same meta-flags (--critical, --production-ready, --code-health)
- ✅ Same accounting formulas (total = applied + skipped + failed)
- ✅ Same phase transitions (explicit START/COMPLETE)

**Minimum Friction:**
- ✅ Single confirmation point (Step 0 only, no pre-flight)
- ✅ Sensible defaults (auto-select common options)
- ✅ Progressive disclosure (show details only when needed)
- ✅ Clear next steps (always tell user what to do next)

### 2. **Maksimum Verimlilik (Maximum Efficiency)**

**Token Optimization:**
- ✅ File exclusions BEFORE processing (Stage 0)
- ✅ Three-stage file discovery (files_with_matches → content → Read)
- ✅ Lazy-load patterns (reference skills, don't duplicate)
- ✅ Placeholder usage (no hardcoded examples)

**Resource Optimization:**
- ✅ Right model for task (haiku/sonnet/opus)
- ✅ Parallel execution for independent tasks
- ✅ Cache strategies (principle loader caching)
- ✅ Minimal file reads (offset+limit)

### 3. **Maksimum Sadelik (Maximum Simplicity)**

**File Size Limits:**
- ✅ Commands: max 800 lines (target: 500-600)
- ✅ Agents: max 400 lines (target: 200-300)
- ✅ Skills: max 600 lines (target: 400-500)

**Complexity Limits:**
- ✅ Max 3 user questions per command
- ✅ Max 5 execution phases
- ✅ Single confirmation point
- ✅ No nested conditionals in flow

**Clarity:**
- ✅ Clear phase names (Discovery, Analysis, Execution, Report)
- ✅ Explicit state transitions
- ✅ Plain language (no jargon)
- ✅ Actionable error messages

### 4. **Maksimum Performans (Maximum Performance)**

**Execution Speed:**
- ✅ Parallel execution by default (independent tasks)
- ✅ Streaming results (real-time progress)
- ✅ Batched operations (group file operations)
- ✅ Early exit on critical errors

**Model Selection:**
- ✅ Haiku: Discovery, enumeration, pattern matching
- ✅ Sonnet: Analysis, fixes, generation (default)
- ✅ Opus: Architecture, complex algorithms (rare)

**Time Targets:**
- ✅ Discovery: < 30 seconds
- ✅ Quick mode: < 5 minutes
- ✅ Full scan: < 30 minutes
- ✅ Per-category: < 3 minutes

### 5. **Prensip Uyumu (100% Principle Compliance)**

**Required Principles (All Commands):**
- ✅ U_EVIDENCE_BASED_ANALYSIS - Verify before claiming
- ✅ U_CHANGE_VERIFICATION - Complete accounting
- ✅ U_NO_HARDCODED_EXAMPLES - Use placeholders
- ✅ C_NATIVE_TOOL_INTERACTIONS - AskUserQuestion with "All" option
- ✅ C_EFFICIENT_FILE_OPERATIONS - Three-stage discovery
- ✅ C_AGENT_ORCHESTRATION_PATTERNS - Right model, parallelization

**Command-Specific:**
- cco-audit, cco-fix, cco-generate: + U_FOLLOW_PATTERNS
- cco-fix, cco-optimize-code-performance: + U_MINIMAL_TOUCH
- cco-generate: + U_NO_OVERENGINEERING
- cco-optimize-context-usage: + C_CONTEXT_WINDOW_MGMT

---

## Standard Command Structure

Every command MUST follow this structure:

```markdown
---
name: cco-{command}
description: {One-line description}
principles: [{REQUIRED_PRINCIPLES}]
parameters: {...}
---

# cco-{command}

**{Purpose in one sentence}**

---

## Execution Guarantee

This command executes the FULL operation as planned.
No scope reduction due to time constraints.

**Estimated time:** Provided for transparency, NOT to limit scope.

---

## Step 0: Introduction and Confirmation

**Welcome to cco-{command} - {Title}**

This command {what it does in 2-3 sentences}.

### What This Command Does
{3-5 bullet points}

### What You'll Be Asked
{1-3 bullet points}

### Time Commitment
{Realistic time ranges}

### What You'll Get
{Expected outputs}

AskUserQuestion({
  questions: [{
    question: "Ready to start?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {label: "Start", description: "Begin {command}"},
      {label: "Cancel", description: "Exit"}
    ]
  }]
})

---

## Execution Protocol

### Phase 1: {Name}
{Description}

### Phase 2: {Name}
{Description}

### Phase 3: {Name}
{Description}

---

## Agent Usage

**Agent:** cco-agent-{type}
**Model:** {haiku/sonnet/opus}
**Why:** {Justification}

---

## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}
```

---

## Standard Patterns

### Single Confirmation Pattern

```python
# ✅ GOOD: Single confirmation at Step 0
Step 0: Introduction + Confirmation
  ├─ Show what will happen
  ├─ Show time estimate
  ├─ Get user approval
  └─ Proceed or exit

# ❌ BAD: Double confirmation
Step 0: Start? → Step N: Pre-flight? (REDUNDANT!)
```

### Accounting Formula

```python
# MUST be present in EVERY command that modifies state
class State:
    total: int
    applied: int
    skipped: int
    failed: int

    def verify_accounting(self) -> bool:
        return self.total == self.applied + self.skipped + self.failed

# Report MUST show:
Total: {total}
Applied: {applied}
Skipped: {skipped}
Failed: {failed}
Verification: {total} = {applied} + {skipped} + {failed} ✓
```

### Progress Reporting

```python
# Explicit phase transitions
print(f"Phase {N}/{TOTAL}: {NAME} ▶ STARTED")
# ... work ...
print(f"Phase {N}/{TOTAL}: {NAME} ✓ COMPLETE ({duration})")
```

### Error Handling

```python
# Standard error handling pattern
try:
    result = execute_operation()
except OperationError as e:
    AskUserQuestion({
        question: f"Operation failed: {e}. How to proceed?",
        options: [
            {label: "Retry", description: "Try again"},
            {label: "Skip", description: "Skip this item"},
            {label: "Cancel", description: "Stop entire operation"}
        ]
    })
```

---

## File Size Guidelines

**Commands:**
- Target: 500-600 lines
- Maximum: 800 lines
- If exceeding: Extract patterns to COMMAND_PATTERNS.md

**Agents:**
- Target: 200-300 lines
- Maximum: 400 lines
- If exceeding: Extract to AGENT_STANDARDS.md

**Skills:**
- Target: 400-500 lines
- Maximum: 600 lines
- If exceeding: Split into multiple skills

---

## Performance Targets

**Discovery Phase:**
- File enumeration: < 10 seconds
- Tech detection: < 20 seconds
- Total discovery: < 30 seconds

**Execution Phase:**
- Per-file analysis: < 1 second
- Per-check: < 3 minutes
- Full category: < 10 minutes

**Reporting Phase:**
- Result aggregation: < 5 seconds
- Score calculation: < 2 seconds
- Report generation: < 10 seconds

---

## Quality Checklist

Before merging ANY command changes, verify:

### UX/DX
- [ ] Single confirmation point
- [ ] Consistent step numbering
- [ ] Clear phase transitions
- [ ] Same output format
- [ ] Same error handling

### Efficiency
- [ ] File exclusions applied (Stage 0)
- [ ] Three-stage file discovery
- [ ] No hardcoded examples
- [ ] Lazy-loaded patterns

### Simplicity
- [ ] File size within limits
- [ ] Max 3 user questions
- [ ] Max 5 execution phases
- [ ] No nested flows

### Performance
- [ ] Parallel execution used
- [ ] Right model selected
- [ ] Streaming results
- [ ] Time targets met

### Principles
- [ ] All required principles listed in frontmatter
- [ ] U_EVIDENCE_BASED_ANALYSIS (accounting)
- [ ] U_NO_HARDCODED_EXAMPLES (placeholders)
- [ ] C_NATIVE_TOOL_INTERACTIONS (AskUserQuestion)
- [ ] C_EFFICIENT_FILE_OPERATIONS (three-stage)

---

## Enforcement

**How to enforce:**

1. **Pre-commit:** Automated checks for file size, structure
2. **Code review:** Manual verification of quality standards
3. **Testing:** Integration tests verify accounting formulas
4. **Documentation:** This file is the single source of truth

**When violations occur:**

1. Document violation in issue
2. Create fix plan aligned with standards
3. Apply fix with verification
4. Update this document if standards evolve

---

## References

- **Principle Files:** `~/.claude/principles/U_*.md`, `C_*.md`
- **Agent Standards:** `AGENT_STANDARDS.md` (Built-in Behaviors)
- **Command Patterns:** `COMMAND_PATTERNS.md` (Reusable Templates)
- **Active Principles:** `~/.claude/CLAUDE.md` (Principle markers)

---

**Last Updated:** 2025-01-23
**Version:** 1.0.0
**Status:** Active - All commands MUST comply
