---
name: cco-implement
description: AI-assisted feature implementation with TDD approach and automatic skill selection based on feature type

keywords: [implement, feature, tdd, test-driven, development, generate, create, build]
category: productivity
pain_points: [1, 4]
---

# cco-implement

**AI-assisted feature implementation with TDD approach and skill auto-selection.**

**Implementation Note:** This command follows [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md) for file discovery (exclusions applied BEFORE processing), token optimization (three-stage discovery), parallelization (Task calls in single message), and cross-platform compatibility.
---

## Built-in References

**This command inherits standard behaviors from:**

- **[STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md)** - Standard structure, execution protocol, file discovery
- **[STANDARDS_QUALITY.md](../STANDARDS_QUALITY.md)** - UX/DX, efficiency, simplicity, performance standards
- **[LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md)** - Reusable patterns (Step 0, Selection, Accounting, Progress, Error Handling)
- **[STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md)** - File discovery, model selection, parallel execution
- **model selection** - Strategic Opus model selection, complexity scoring, ROI guidelines

**See these files for detailed patterns. Only command-specific content is documented below.**

---

## Execution Guarantee

This command executes the FULL TDD implementation cycle.
All phases (Red → Green → Refactor) completed without shortcuts.

**Estimated time: Provided for transparency, NOT to skip steps.**

---

## Step 0: Introduction and Confirmation

**Pattern:** Pattern 1 (Step 0 Introduction)

**Command-Specific Details:**

**What I do:**
I implement new features using Test-Driven Development (TDD), automatically selecting appropriate skills based on feature type.

**Process:**
1. Analyze feature request → determine complexity and required skills
2. Create detailed implementation plan (5 phases)
3. User selects implementation steps
4. Implement using TDD (tests first, then make them pass)
5. Add security hardening and documentation

**Output:**
- Complete feature implementation following TDD
- Architecture design for the feature
- Comprehensive tests (unit, integration, security) - high coverage goal
- Production-ready code with security hardening
- API documentation and usage examples

**Phases:**
1. Architecture Design (plan feature structure)
2. Tests First - TDD Red Phase (write failing tests)
3. Implementation - TDD Green Phase (make tests pass)
4. Security Hardening (rate limiting, validation, etc.)
5. Documentation (OpenAPI, security best practices)

**Time:** 10-30 minutes depending on feature complexity

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start implementing the feature?",
    header: "Start Implement",
    multiSelect: false,
    options: [
      {
        label: "Yes, start implementation",
        description: "Analyze feature and begin TDD implementation"
      },
      {
        label: "No, cancel",
        description: "Exit without implementing anything"
      }
    ]
  }]
})
```

**If user selects "No, cancel":** EXIT immediately
**If user selects "Yes, start implementation":** Continue to Step 0.5

---

### Step 0.5: Project Context Discovery

**Pattern:** Pattern 2 (Multi-Select with "All")

**Command-Specific Details:**

**Benefits for /cco-implement:**
- Implementation respects existing architecture and integrates properly
- Follows project coding conventions and patterns
- Uses established tech stack and libraries

**Context Used:**
- Architecture decisions inform feature design
- Tech stack guides implementation choices
- Conventions ensure consistent code style

---

### Step 0.6: Tech Stack Detection & Feature Complexity Analysis

**Pattern:** Pattern 10 (Tech Stack Detection)

```markdown
Detecting tech stack...

✓ Tech stack detected: {DETECTED_LANGUAGES}, {DETECTED_FRAMEWORKS}, {DETECTED_TESTING}
✓ Available patterns identified
✓ Complexity analysis: {FEATURE_COMPLEXITY}
```

### Step 0.7: Opus Upgrade Opportunity (Complex Features)

**Pattern:** Pattern 11 (Opus Upgrade Opportunity - See model selection standards)

**Trigger:** Feature complexity == "high" OR requires novel algorithm

**Complexity Scoring:** Use algorithm from model selection
**ROI Calculation:** See model selection standards for cost/benefit analysis

```python
if feature_complexity == "high":
    selected_model = offer_opus_upgrade(
        task_name="Feature Implementation",
        task_description=f"Implementing: {feature_name}",
        complexity_reason="novel algorithm design, complex integration, or architectural changes",
        expected_benefit="Better architecture, cleaner code, better edge case handling (30-40% improvement)",
        default_model="sonnet"
    )
```

---

## Critical UX Principles

1. **100% Honesty** - Only claim "implemented" if code works and tests pass
2. **Complete Accounting** - Report: implemented + skipped + blocked = total planned
3. **No Hardcoded Examples** - All examples use `{PLACEHOLDERS}`, never fake code
4. **Phase Tracking** - Explicit start/end for each TDD phase with timestamps
5. **Consistent Counts** - Same counts shown everywhere (single source of truth)

### Implementation Outcome Categories

```python
OUTCOMES = {
    "implemented": "Code written, tests pass, verified working",
    "tests_written": "TDD red phase complete, implementation pending",
    "needs_decision": "Multiple implementation approaches - user must choose",
    "blocked_deps": "Requires other features/modules first",
    "blocked_design": "Needs architectural clarification",
    "failed_tests": "Tests written but cannot make pass - needs review",
}
```

---

## Design Principles

**See:** STANDARDS_QUALITY.md
- UX/DX principles (transparency, progressive disclosure, zero surprises)
- Honesty & accurate reporting (no false positives/negatives)
- No hardcoded examples (use placeholders: `{FILE_PATH}`, `{LINE_NUMBER}`)

---

## Execution Protocol

### Step 1: Analyze Feature Request

User provides feature description:
```
/cco-implement "[FEATURE_DESCRIPTION]"
```

Analyze the ACTUAL feature request to determine:
- Feature type (API, frontend, database, etc.)
- Complexity (simple, medium, complex)
- Required skills (based on keywords in request)
- Security considerations (if applicable)
- Testing needs (always TDD)

### Step 2: Select Skills

Auto-select skills based on feature keywords:

**Auto-selection rules:**
- Keywords "auth", "login", "JWT", "security" → security skills
- Keywords "API", "endpoint", "REST" → API skills
- Keywords "database", "query", "schema" → database skills
- Keywords "frontend", "UI", "component" → frontend skills
- Keywords "deploy", "CI/CD", "pipeline" → deployment skills
- Keywords "mobile", "offline", "battery", "app store", "iOS", "Android" → cco-skill-mobile-offline-battery-appstore
- Always include: testing skills (TDD approach)

### Step 3: Create Implementation Plan and Get User Confirmation

Generate implementation plan from ACTUAL feature analysis:

```markdown
Implementation Plan (TDD Approach):

Feature: {ACTUAL_FEATURE_REQUEST}
Complexity: {CALCULATED_COMPLEXITY}
Skills: {SELECTED_SKILLS}

Phases:
1. Architecture Design ({TIME} min)
   - {ACTUAL design decisions for this feature}

2. Tests First ({TIME} min) - TDD Red Phase
   - {ACTUAL tests to create based on feature requirements}

3. Implementation ({TIME} min) - TDD Green Phase
   - {ACTUAL components to implement}

4. Security Hardening ({TIME} min) [if security-critical]
   - {ACTUAL security measures for this feature}

5. Documentation ({TIME} min)
   - {ACTUAL documentation needed}

Estimated time: {CALCULATED_TOTAL} minutes
Tests: {ESTIMATED_COUNT}+ tests (high coverage target)
```

**Generate AskUserQuestion options from actual feature analysis:**

```python
# Generate implementation step options from ACTUAL feature analysis
implementation_options = [
    # Phase 1: Architecture steps
    # Phase 2: Test creation steps
    # Phase 3: Implementation steps
    # Phase 4: Security steps (if applicable)
    # Phase 5: Documentation steps
    # Control options
    {label: "All Steps (Full TDD)", description: "Execute ALL steps in order"},
    {label: "All Tests Only", description: "Execute only test-writing steps"},
    {label: "All Implementation Only", description: "Execute only implementation steps"},
    {label: "Skip Tests ⚠️", description: "STRONGLY NOT RECOMMENDED - Violates TDD"}
]

AskUserQuestion({
  questions: [{
    question: "Which implementation steps should I execute?",
    header: "Implement",
    multiSelect: true,
    options: implementation_options
  }]
})
```

### Step 4: Execute TDD Implementation

**Pattern:** Pattern 3 (Progress Reporting)

**Use TodoWrite** to track phases:
```python
TodoWrite([
    {"content": "Phase 1: Architecture Design", "status": "in_progress", "activeForm": "Designing architecture"},
    {"content": "Phase 2: TDD Red Phase (Tests First)", "status": "pending", "activeForm": "Writing failing tests"},
    {"content": "Phase 3: TDD Green Phase (Implementation)", "status": "pending", "activeForm": "Implementing feature"},
    {"content": "Phase 4: Security Hardening", "status": "pending", "activeForm": "Adding security measures"},
    {"content": "Phase 5: Documentation", "status": "pending", "activeForm": "Writing documentation"}
])
```

**Launch Task** for each phase:

```python
# Phase 1: Architecture Design
Task({
  model: "sonnet",
  prompt: "Design {FEATURE} architecture..."
})

# Phase 2: TDD Red Phase (Tests First)
Task({
  model: "sonnet",
  prompt: """
  Write tests FIRST (TDD approach):
  Use cco-skill-test-pyramid-coverage-isolation
  [ACTUAL test requirements based on feature]
  """
})

# Phase 3: TDD Green Phase (Implementation)
Task({
  model: "sonnet",
  prompt: """
  Implement {FEATURE} to make tests pass (TDD green phase):
  Use skills: {SELECTED_SKILLS}
  [ACTUAL components to implement]
  """
})

# Phase 4: Security Hardening (if applicable)
Task({
  model: "sonnet",
  prompt: "Add rate limiting, input validation, and security hardening..."
})

# Phase 5: Documentation
Task({
  model: "sonnet",
  prompt: "Generate OpenAPI spec and usage documentation..."
})
```

### Step 5: Report Progress and Results

**See [LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md#pattern-8-dynamic-results-generation) for standard results pattern.**

**Command-Specific Details:**

**Accounting formula enforced:** `total = implemented + tests_written + needs_decision + blocked`

**Real metrics (no placeholders):**

```markdown
Implementation Summary:

Created:
{for each file actually created:}
✓ {real-file-path} ({actual component description})

{if security features were added:}
Security Features:
{list ACTUAL security features implemented}

Tests: {ACTUAL_PASSED} passed, {ACTUAL_FAILED} failed ({ACTUAL_COVERAGE}% coverage)

Impact:
- Addresses Pain #{X} ({PAIN_DESCRIPTION based on feature type})
- {Other actual improvements}
- Feature complete and production-ready ✓

Next Steps:
1. Run full test suite: {actual test command for this project}
2. Test manually: {actual endpoint/URL if applicable}
3. Review: /cco-audit --{relevant-category}
4. Commit: /cco-commit
```

---

## Agent Usage

**See [STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md) for:**
- Parallel execution patterns (fan-out, pipeline, hierarchical)
- Model selection strategy (Haiku/Sonnet/Opus)
- Error handling protocols
- Agent communication patterns

**Command-Specific Agent Configuration:**

**Agents Used:**
- `cco-agent-generate` (Sonnet) - Scaffolding and tests
- `cco-agent-fix` (Sonnet) - Implementation

**Pattern:** Pipeline (sequential phases with dependencies)

**Skills:** Auto-selected based on feature keywords

---

## Agent Error Handling

**Pattern:** Pattern 5 (Error Handling)

**Command-Specific Handling:**

If implementation agent execution fails:

```python
AskUserQuestion({
  questions: [{
    question: "implement-agent (Sonnet) failed: {error_message}. How to proceed?",
    header: "implement-agent Error",
    multiSelect: false,
    options: [
      {label: "Retry", description: "Run agent again with same parameters"},
      {label: "Retry with different model", description: "Try Sonnet/Haiku/Opus"},
      {label: "Manual implementation", description: "Guide manual step-by-step implementation"},
      {label: "Skip failing step", description: "Continue with next implementation step"},
      {label: "Cancel", description: "Stop entire command"}
    ]
  }]
})
```

---

## TDD Cycle

1. **Red:** Write failing tests first
2. **Green:** Write minimal code to pass tests
3. **Refactor:** Improve code while keeping tests green

Always follow this cycle for quality and confidence.

---

## Skills Auto-Selection

Based on feature keywords:
- "authentication", "auth", "login" → security skills
- "API", "endpoint", "REST" → API skills
- "database", "query", "schema" → database skills
- "frontend", "UI", "component" → frontend skills
- "deploy", "CI/CD", "pipeline" → deployment skills
- "test", "coverage" → testing skills

Multiple skills used when feature spans domains.

---

## Success Criteria

- [OK] Feature analyzed and understood
- [OK] Appropriate skills auto-selected
- [OK] Implementation plan created
- [OK] TDD approach followed (tests first)
- [OK] All tests pass with high coverage
- [OK] Security hardened
- [OK] Documentation created
- [OK] Pain-point impact communicated
- [OK] Production-ready code

---

## Example Usage

```bash
# Implement new feature (provide actual feature description)
/cco-implement "[Your feature description]"

# Examples of feature types:
# - "Add user authentication with JWT"
# - "Add caching layer using Redis"
# - "Add real-time notifications with WebSockets"
# - "Add payment processing with Stripe"
# - "Add email notifications"

# With additional context (optional prompt)
/cco-implement "Add JWT authentication" "Use HS256, 24h expiry, refresh tokens"
/cco-implement "Add rate limiting" "100 requests per minute per IP"
/cco-implement "Add payment processing" "Stripe integration, support EUR and USD"
```

**Optional Prompt Support:**
Any additional text is treated as context for the feature implementation. The AI will:
- Use specified technical requirements
- Follow mentioned standards or libraries
- Incorporate specific constraints or preferences
- Adapt architecture based on your guidance
