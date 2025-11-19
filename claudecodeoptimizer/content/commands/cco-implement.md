---
name: cco-implement
description: AI-assisted feature implementation with TDD approach and automatic skill selection based on feature type
action_type: implement
keywords: [implement, feature, tdd, test-driven, development, generate, create, build]
category: productivity
pain_points: [1, 4]
---

# cco-implement

**AI-assisted feature implementation with TDD approach and skill auto-selection.**

---

## Purpose

Implement new features using Test-Driven Development (TDD), automatically selecting appropriate skills based on feature type.

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

### Phase State Tracking

```python
PHASES = {
    1: {"name": "Architecture Design", "duration": "{TIME}"},
    2: {"name": "TDD Red Phase", "duration": "{TIME}"},
    3: {"name": "TDD Green Phase", "duration": "{TIME}"},
    4: {"name": "Security Hardening", "duration": "{TIME}"},
    5: {"name": "Documentation", "duration": "{TIME}"},
}

# MUST announce each phase transition explicitly
print(f"Phase {N}/5: {PHASES[N]['name']} ▶ STARTED")
# ... work ...
print(f"Phase {N}/5: {PHASES[N]['name']} ✓ COMPLETE ({duration})")
```

---

## Execution Protocol

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# Implement Command

**What I do:**
I implement new features using Test-Driven Development (TDD), automatically selecting appropriate skills based on feature type.

**How it works:**
1. I analyze your feature request to determine complexity and required skills
2. I create a detailed implementation plan broken into 5 phases
3. You select which implementation steps to execute
4. I implement using TDD (write tests first, then make them pass)
5. I add security hardening and documentation

**What you'll get:**
- Complete feature implementation following TDD
- Architecture design for the feature
- Comprehensive tests (unit, integration, security) - high coverage goal
- Production-ready code with security hardening
- API documentation and usage examples

**Phases:**
1. Architecture Design (plan the feature structure)
2. Tests First - TDD Red Phase (write failing tests)
3. Implementation - TDD Green Phase (make tests pass)
4. Security Hardening (rate limiting, validation, etc.)
5. Documentation (OpenAPI, security best practices)

**Time estimate:** 10-30 minutes depending on feature complexity

**New code WILL be created** - complete feature implementation with tests.
```

**Then ask for confirmation using AskUserQuestion:**

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

**CRITICAL:**
- If user selects "No, cancel" → EXIT immediately, do NOT proceed
- If user selects "Yes, start implementation" → Continue to Step 0.5

---

### Step 0.5: Project Context Discovery (Optional)

**Ask user if they want project documentation analyzed for better implementation alignment.**

```python
AskUserQuestion({
  questions: [{
    question: "Proje dokümantasyonundan context çıkarılsın mı?",
    header: "Project Context",
    multiSelect: false,
    options: [
      {
        label: "Evet (önerilen)",
        description: "README/ARCHITECTURE'dan proje mimarisini çıkar, implementasyon mimari kararlara uygun olur"
      },
      {
        label: "Hayır",
        description: "Sadece feature implement et (daha hızlı)"
      }
    ]
  }]
})
```

**If "Evet" selected:**

```python
# Extract project context via Haiku sub-agent
context_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Extract project context summary (MAX 200 tokens).
    Focus on: architecture decisions, tech stack, coding conventions.

    Files to check: README.md, ARCHITECTURE.md, DESIGN.md, docs/ADR/*.md

    Return: Purpose, Architecture Notes, Tech Stack, Conventions
    """
})

# Use context in feature implementation
project_context = context_result
```

**Benefits:** Implementation respects existing architecture and integrates properly.

---

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

**IMPORTANT - Dynamic Skill Selection:**
Analyze the ACTUAL feature request and select appropriate skills:

```markdown
Analyzing feature: "[ACTUAL_FEATURE_REQUEST]"

Feature type: [DETECTED_TYPE based on keywords]
Complexity: [CALCULATED: simple/medium/complex]

Skills I'll use:
[List ACTUAL skills selected based on feature keywords - see auto-selection rules below]
```

**Auto-selection rules:**
- Keywords "auth", "login", "JWT", "security" → security skills
- Keywords "API", "endpoint", "REST" → API skills
- Keywords "database", "query", "schema" → database skills
- Keywords "frontend", "UI", "component" → frontend skills
- Keywords "deploy", "CI/CD", "pipeline" → deployment skills
- Always include: testing skills (TDD approach)

### Step 3: Create Implementation Plan and Get User Confirmation

Present implementation plan:

**IMPORTANT - Dynamic Plan Generation:**
Analyze the ACTUAL feature to create a realistic implementation plan:

```markdown
Implementation Plan (TDD Approach):

Feature: [ACTUAL_FEATURE_REQUEST]
Complexity: [CALCULATED_COMPLEXITY]
Skills: [SELECTED_SKILLS based on feature]

Phases:
1. Architecture Design ([TIME] min)
   - [ACTUAL design decisions for this feature]

2. Tests First ([TIME] min) - TDD Red Phase
   - [ACTUAL tests to create based on feature requirements]

3. Implementation ([TIME] min) - TDD Green Phase
   - [ACTUAL components to implement]

4. Security Hardening ([TIME] min) [if security-critical]
   - [ACTUAL security measures for this feature]

5. Documentation ([TIME] min)
   - [ACTUAL documentation needed]

Estimated time: [CALCULATED_TOTAL] minutes
Tests: [ESTIMATED_COUNT]+ tests (high coverage target)
```

**Then generate AskUserQuestion options from this plan:**

**Use AskUserQuestion** to let user select implementation steps (NOT phases, but individual steps):

```python
# Generate implementation step options from ACTUAL feature analysis
implementation_options = []

# Phase 1: Architecture - generate from actual design decisions
for design_step in architecture_design_steps:
    implementation_options.append({
        label: design_step.name,
        description: f"(Phase 1: Architecture, {design_step.time}) {design_step.description}"
    })

# Phase 2: Tests (TDD Red) - generate from actual test requirements
for test_step in test_creation_steps:
    implementation_options.append({
        label: test_step.name,
        description: f"(Phase 2: Tests, {test_step.time}) {test_step.tests_to_write} | 🔴 TDD Red Phase"
    })

# Phase 3: Implementation (TDD Green) - generate from actual components
for impl_step in implementation_steps:
    implementation_options.append({
        label: impl_step.name,
        description: f"(Phase 3: Implementation, {impl_step.time}) {impl_step.file} - {impl_step.description} | 🟢 TDD Green Phase"
    })

# Phase 4: Security (if applicable) - generate from actual security needs
for security_step in security_hardening_steps:
    implementation_options.append({
        label: security_step.name,
        description: f"(Phase 4: Security, {security_step.time}) {security_step.description}"
    })

# Phase 5: Documentation - generate from actual docs needed
for doc_step in documentation_steps:
    implementation_options.append({
        label: doc_step.name,
        description: f"(Phase 5: Documentation, {doc_step.time}) {doc_step.description}"
    })

# Add control options
implementation_options.extend([
    {
        label: "All Steps (Full TDD)",
        description: f"✅ RECOMMENDED: Execute ALL {len(implementation_options)} steps in order (Phases 1-5, complete TDD, production-ready)"
    },
    {
        label: "All Tests Only",
        description: f"🔴 Execute only {len(test_creation_steps)} test-writing steps (Phase 2) - TDD Red Phase"
    },
    {
        label: "All Implementation Only",
        description: f"🟢 Execute only {len(implementation_steps)} implementation steps (Phase 3) - TDD Green Phase (requires tests!)"
    },
    {
        label: "Skip Tests (NOT RECOMMENDED)",
        description: "⚠️ Skip Phase 2 (Tests) - Pain #4: Biggest mistake!"
    }
])

AskUserQuestion({
  questions: [{
    question: "Which implementation steps should I execute? Select the specific tasks you want:",
    header: "Implement",
    multiSelect: true,
    options: implementation_options
  }]
})
```

**Note:** All hardcoded JWT examples removed. Steps generated dynamically from actual feature analysis.

**IMPORTANT:**
- If user selects "All Steps (Full TDD)", ignore other selections and execute ALL steps in order
- If user selects "All Tests Only", execute only Phase 2 steps
- If user selects "All Implementation Only", execute only Phase 3 steps (warn if tests not written yet)
- If user selects "Skip Tests", execute all steps EXCEPT Phase 2 (warn about Pain #4)
- Otherwise, execute ONLY the individually selected steps
- Steps must be executed in phase order (Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5) even if selected out of order

### Step 4: Execute TDD Implementation

**Use TodoWrite** to track phases

**Launch Task** for each phase:

```python
# Phase 1: Architecture
Task({
  model: "sonnet",
  prompt: "Design JWT authentication architecture..."
})

# Phase 2: Tests (TDD - Write tests first)
Task({
  model: "sonnet",
  prompt: """
  Write tests FIRST (TDD approach):

  Use cco-skill-test-pyramid-coverage-isolation

  1. Unit tests for JWT operations:
     - test_create_access_token()
     - test_create_refresh_token()
     - test_validate_token_success()
     - test_validate_token_expired()
     - test_validate_token_tampered()

  2. Integration tests for auth endpoints:
     - test_login_success()
     - test_login_invalid_credentials()
     - test_refresh_token_success()
     - test_refresh_token_invalid()
     - test_logout_success()

  3. Security tests:
     - test_rate_limiting()
     - test_brute_force_protection()
     - test_weak_password_rejected()

  Create failing tests first (TDD red phase).
  """
})

# Phase 3: Implementation (Make tests pass)
Task({
  model: "sonnet",
  prompt: """
  Implement JWT authentication to make tests pass (TDD green phase):

  Use skills:
  - cco-skill-security-owasp-xss-sqli-csrf
  - cco-skill-api-rest-versioning-security

  1. {MODEL_FILE}:
     - Model definitions and schema
     - Data validation and constraints
     - Helper methods

  2. {SERVICE_FILE}:
     - Core business logic
     - Token/session management
     - Utility functions

  3. {API_FILE}:
     - POST {ENDPOINT_1}
     - POST {ENDPOINT_2}
     - POST {ENDPOINT_3}

  4. {MIDDLEWARE_FILE}:
     - Request validation middleware
     - Route protection decorator

  Run tests after each component to ensure TDD cycle.
  """
})

# Phase 4-5: Security & Documentation
# ... similar Task calls
```

### Step 5: Report Progress and Results

After each phase, report progress and continue automatically if "All Phases" was selected, otherwise ask for confirmation:

```markdown
Phase 1 Complete: Architecture Designed ✓

Feature Flow:
- POST {ENDPOINT_1} → {RESPONSE_1}
- POST {ENDPOINT_2} → {RESPONSE_2}
- POST {ENDPOINT_3} → {RESPONSE_3}

Data Schema:
- {TABLE_1}: {FIELDS_1}
- {TABLE_2}: {FIELDS_2}
```

**If "All Phases" NOT selected**, use AskUserQuestion for continuation:

```python
AskUserQuestion({
  questions: [{
    question: "Phase 1 complete. Ready to continue to Phase 2 (Tests)?",
    header: "Continue",
    multiSelect: false,
    options: [
      {
        label: "Yes, continue to Phase 2",
        description: "Write failing tests (TDD Red Phase)"
      },
      {
        label: "No, stop here",
        description: "Stop implementation and review results"
      }
    ]
  }]
})
```

Repeat for each phase transition.

**If "All Phases" WAS selected**, continue automatically without asking.

---

Final summary after all selected phases complete:

**IMPORTANT - Dynamic Summary Generation:**
Report ACTUAL implementation results. Use this template with REAL data:

```markdown
Implementation Summary:

Created:
[For each file actually created:]
✓ <real-file-path> ([actual component description])

[If security features were added:]
Security Features:
[List ACTUAL security features implemented]

Tests: [ACTUAL_PASSED] passed, [ACTUAL_FAILED] failed ([ACTUAL_COVERAGE]% coverage)

Impact:
- Addresses Pain #[X] ([PAIN_DESCRIPTION based on feature type])
- [Other actual improvements]
- Feature complete and production-ready ✓

Next Steps:
1. Run full test suite: [actual test command for this project]
2. Test manually: [actual endpoint/URL if applicable]
3. Review: /cco-audit --[relevant-category]
4. Commit: /cco-commit
```

**Never use hardcoded examples - only report what was actually implemented.**

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

## Agents Used

- `cco-agent-generate` - Scaffolding and tests
- `cco-agent-fix` - Implementation

Both use Sonnet for accuracy.

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
```
