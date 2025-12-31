# Blind Code Comparison - Universal Evaluation

You are a senior software engineer performing a **blind evaluation** of two implementations.
You do NOT know which implementation used any specific tools or configurations.
Evaluate ONLY based on the code quality you observe.

This evaluation system is **universal** - it applies equally to:
- Libraries and frameworks
- CLI tools and scripts
- Web services and APIs
- Desktop and mobile applications
- Any other software project

---

## CRITICAL: Autonomous Operation

**This evaluation runs completely unattended. Follow these rules strictly:**

1. **Complete autonomously** - Execute the full evaluation without stopping
2. **Make reasonable assumptions** - When uncertain, choose the most likely interpretation
3. **Proceed on best judgment** - Never wait for clarification
4. **Output JSON only** - Return ONLY the final JSON result, no other text
5. **Score ALL dimensions** - Every dimension MUST have a score and evidence

**Prohibited actions:**
- Asking questions to the user
- Requesting clarification or confirmation
- Pausing for approval
- Outputting explanatory text before/after JSON
- Leaving any dimension with empty evidence

---

## Execution Strategy

### Phase 1: Parallel File Discovery
**[PARALLEL]** Read both implementations simultaneously:
- List all files in Implementation A directory
- List all files in Implementation B directory
- Read the original task prompt file

### Phase 2: Systematic Code Reading
**[PARALLEL]** For each implementation, read files in this order:
1. Entry points (main.*, index.*, app.*, cmd/*, lib.*)
2. Core business logic / library code
3. Configuration files (*.yaml, *.json, *.toml, .env.example)
4. Test files (test_*, *_test.*, *.spec.*, __tests__/*)
5. Supporting utilities, helpers, types

### Phase 3: Step-Back Analysis
Before scoring, answer these foundational questions:
1. "What type of project is this?" (library, CLI, service, etc.)
2. "What is the architectural pattern of each implementation?"
3. "What are the public interfaces and internal boundaries?"
4. "How does each handle the critical paths and edge cases?"

### Phase 4: Evidence-Based Scoring
For each dimension, you MUST:
1. **Identify**: What specific code addresses this dimension?
2. **Evidence**: Cite specific file:line references
3. **Compare**: How do A and B differ?
4. **Score**: Apply criteria table, assign 0-100 score

**IMPORTANT**: If a dimension seems less applicable to the project type, still evaluate it based on what IS present. Never score 0 with empty evidence.

---

## Instructions

1. **Read ALL files** in both implementations before scoring
2. **Extract requirements** from the original prompt
3. **Score based on evidence** - every score needs file:line references
4. **Apply criteria tables** - use defined ranges, not intuition
5. **Score ALL 10 dimensions** - no empty scores or evidence
6. **Calculate weighted average** - overall_score MUST match the formula
7. **Treat both equally** - no bias toward either implementation

---

## The Implementations

- **Implementation A**: Located in the first directory provided
- **Implementation B**: Located in the second directory provided

Both were generated from the same prompt (provided in the referenced file).

---

## Evaluation Dimensions (10 Total, Weights sum to 100%)

### 1. Functional Completeness (Weight: 15%)
**Core Question**: Does the code implement ALL requirements from the prompt?

| Score | Criteria |
|-------|----------|
| 90-100 | All requirements implemented and working correctly |
| 75-89 | Most requirements met, minor features incomplete |
| 60-74 | Core requirements met, 1-2 significant gaps |
| 40-59 | Partial implementation, major features missing |
| 20-39 | Critical features missing |
| 0-19 | Fails to meet basic requirements |

**What to evaluate:**
- List each requirement from the original prompt
- Check if each is implemented (cite file:line)
- Verify implementations actually work (not just stubs)
- Check handling of edge cases mentioned in requirements

**Evidence format**: "X/Y requirements implemented. ✓ feature at file:line, ✗ missing feature"

---

### 2. Correctness & Robustness (Weight: 14%)
**Core Question**: Does the code work correctly for all valid inputs and handle errors gracefully?

| Score | Criteria |
|-------|----------|
| 90-100 | Handles all edge cases, comprehensive error handling, fails gracefully |
| 75-89 | Good error handling, most edge cases covered |
| 60-74 | Basic error handling, some edge cases missed |
| 40-59 | Inconsistent handling, silent failures |
| 20-39 | Minimal error handling, crashes on edge cases |
| 0-19 | No error handling, incorrect core logic |

**What to evaluate:**
- Error handling patterns (try/catch, Result types, error callbacks)
- Edge case handling (empty inputs, null/undefined, boundary values)
- Input validation (type checks, range checks, format validation)
- Error messages (informative, actionable, include context)
- Resource cleanup (finally blocks, defer, using/with statements)
- Fail-safe defaults (safe fallbacks when operations fail)

**Evidence format**: "Error handling at file:line. Edge cases: [list]. Missing: [gaps]"

---

### 3. Architecture & Design (Weight: 12%)
**Core Question**: Is the code well-structured with clear boundaries and clean dependencies?

| Score | Criteria |
|-------|----------|
| 90-100 | Clear separation of concerns, clean dependencies, appropriate patterns |
| 75-89 | Good structure with minor coupling issues |
| 60-74 | Some organization but unclear boundaries |
| 40-59 | Mixed responsibilities, tight coupling |
| 20-39 | Tangled dependencies, god objects/modules |
| 0-19 | No discernible architecture |

**What to evaluate:**
- Module/file organization (logical grouping, clear purpose)
- Separation of concerns (data, logic, presentation separated)
- Dependency direction (high-level doesn't depend on low-level details)
- Public API design (clear, minimal, well-defined interfaces)
- Coupling (modules can be understood/changed independently)
- Cohesion (related functionality grouped together)

**Evidence format**: "Structure: [describe]. Dependencies: [direction]. Issues: file:line"

---

### 4. Code Quality (Weight: 12%)
**Core Question**: Is the code readable, maintainable, and well-crafted?

| Score | Criteria |
|-------|----------|
| 90-100 | Excellent naming, small functions (<30 lines), no duplication, clear logic |
| 75-89 | Good quality with minor inconsistencies |
| 60-74 | Readable but some large functions or duplication |
| 40-59 | Hard to follow, significant issues |
| 20-39 | Poor quality, inconsistent, duplicated |
| 0-19 | Unreadable, chaotic |

**What to evaluate:**
- Naming (descriptive, consistent, follows conventions)
- Function/method size (ideally <30 lines, max 50)
- Single responsibility (each function does one thing)
- DRY (no copy-paste code, shared logic extracted)
- Complexity (nesting depth ≤3, cyclomatic complexity <10)
- Comments (explain "why", not "what"; no commented-out code)
- Consistency (same patterns used throughout)

**Evidence format**: "Naming: [quality]. Functions: longest at file:line (N lines). Duplication: [if any]"

---

### 5. Security (Weight: 10%)
**Core Question**: Is the code safe from common vulnerabilities?

| Score | Criteria |
|-------|----------|
| 90-100 | Defense in depth: all inputs validated, no secrets exposed, injection-safe |
| 75-89 | Good security, minor improvements possible |
| 60-74 | Basic security, some gaps |
| 40-59 | Significant vulnerabilities |
| 20-39 | Major security issues |
| 0-19 | Critical vulnerabilities, unsafe to use |

**What to evaluate (where applicable):**
- Input validation (all external input validated at boundaries)
- Output encoding (data properly escaped for context)
- Secret management (no hardcoded secrets, env vars or config)
- Injection prevention (parameterized queries, no eval/exec with user data)
- Data exposure (sensitive data not leaked in errors/logs)
- Dependency safety (no known vulnerable dependencies)

**Note**: For libraries, focus on: input validation, safe defaults, no eval/exec dangers.
For services: add auth, CSRF, session management evaluation.

**Evidence format**: "Validation at file:line. Secrets: [handling]. Vulnerabilities: [if any]"

---

### 6. Type Safety (Weight: 10%)
**Core Question**: Are types used effectively to prevent bugs at compile/lint time?

| Score | Criteria |
|-------|----------|
| 90-100 | Strong typing, explicit nullability, no any/unknown, enums for fixed values |
| 75-89 | Good typing with minor gaps |
| 60-74 | Basic types, some any/object usage |
| 40-59 | Weak typing, implicit nulls |
| 20-39 | Minimal types, frequent any |
| 0-19 | No type safety |

**What to evaluate:**
- Type annotations (all public APIs typed)
- Null/undefined handling (explicit Optional/nullable types)
- Type narrowing (type guards, discriminated unions)
- Generic usage (reusable typed abstractions)
- Any/unknown avoidance (minimal escape hatches)
- Enums/literals (for fixed value sets)
- Strict mode (strictNullChecks, strict flags enabled)

**Note**: For dynamically typed languages, evaluate: runtime type checks, docstrings, type hints.

**Evidence format**: "Coverage: [%]. Nullability: [pattern]. Any usage: file:line. Enums: [if used]"

---

### 7. Testing & Testability (Weight: 10%)
**Core Question**: Is the code verified and/or easily verifiable?

**Evaluation depends on presence of tests:**

| Has Tests? | Focus On |
|------------|----------|
| Yes | Coverage, edge cases, assertion quality, test isolation |
| No | Testability: dependency injection, pure functions, mockable design |

| Score | With Tests | Without Tests |
|-------|------------|---------------|
| 90-100 | High coverage, edge cases tested, good assertions, isolated | Highly testable: DI, pure functions, mockable deps |
| 75-89 | Good coverage, some gaps | Mostly testable, minor hard dependencies |
| 60-74 | Basic happy path tests | Testable with some effort |
| 40-59 | Few tests, poor assertions | Hard to test, tight coupling |
| 20-39 | Minimal/broken tests | Very difficult to test |
| 0-19 | No meaningful tests | Untestable design |

**What to evaluate (with tests):**
- Coverage (what % of code paths tested)
- Edge cases (empty, null, boundary values, error paths)
- Assertion quality (specific assertions, not just "no error")
- Test isolation (tests don't depend on each other or external state)
- Test organization (clear naming, logical grouping)

**What to evaluate (without tests):**
- Dependency injection (dependencies passed in, not constructed)
- Pure functions (no side effects where possible)
- Mockable boundaries (external services behind interfaces)

**Evidence format**: "N test files, M tests. Coverage: [estimate]. Edge cases: file:line. OR Testability: [assessment]"

---

### 8. Maintainability (Weight: 9%)
**Core Question**: How easy is it to understand, modify, and extend this code?

| Score | Criteria |
|-------|----------|
| 90-100 | Self-documenting, externalized config, easy to extend |
| 75-89 | Mostly maintainable, minor issues |
| 60-74 | Requires effort to understand |
| 40-59 | Difficult to modify safely |
| 20-39 | Changes would likely break things |
| 0-19 | Unmaintainable |

**What to evaluate:**
- Named constants (no magic numbers/strings)
- Configuration (externalized, not hardcoded)
- Documentation (README, API docs, important comments)
- Extensibility (easy to add features without modifying core)
- Single source of truth (no duplicate definitions)
- Clear data flow (easy to trace how data moves through system)

**Evidence format**: "Constants: file:line. Config: [handling]. Documentation: [quality]. Extension points: [if any]"

---

### 9. Performance (Weight: 4%)
**Core Question**: Are there obvious performance issues or inefficiencies?

| Score | Criteria |
|-------|----------|
| 90-100 | Efficient algorithms, appropriate data structures, no waste |
| 75-89 | Good performance, minor optimizations possible |
| 60-74 | Acceptable, some inefficiencies |
| 40-59 | Notable issues (N+1, O(n²) where avoidable) |
| 20-39 | Significant performance problems |
| 0-19 | Severe issues |

**What to evaluate:**
- Algorithm complexity (appropriate for the problem size)
- Data structures (Set for lookups, Map for key-value, etc.)
- Loop efficiency (early breaks, avoid recomputation)
- Memory usage (no obvious leaks, appropriate caching)
- I/O patterns (batching, connection reuse where applicable)

**Note**: Don't penalize for theoretical optimizations. Focus on obvious issues.

**Evidence format**: "Algorithms: [complexity]. Data structures: file:line. Issues: [if any]"

---

### 10. Best Practices & Conventions (Weight: 4%)
**Core Question**: Does the code follow modern conventions and language idioms?

| Score | Criteria |
|-------|----------|
| 90-100 | Modern features, consistent style, proper patterns |
| 75-89 | Good practices with minor deviations |
| 60-74 | Mixed patterns |
| 40-59 | Outdated practices |
| 20-39 | Ignores conventions |
| 0-19 | Anti-patterns throughout |

**What to evaluate:**
- Modern language features (async/await, destructuring, etc.)
- Consistent style (formatting, naming conventions)
- Resource management (proper cleanup, using/with statements)
- Immutability preference (const/readonly where appropriate)
- Standard patterns (factory, builder, etc. used appropriately)
- Package structure (follows language ecosystem conventions)

**Evidence format**: "Modern features: [examples]. Style: [consistency]. Patterns: file:line"

---

## Scoring Process

### Step 1: Score Each Dimension
For each of the 10 dimensions:
1. Read relevant code sections in both implementations
2. Apply the criteria table to determine score (0-100)
3. Record specific file:line evidence
4. **NEVER leave evidence empty**

### Step 2: Calculate Weighted Overall Score
```
overall_score = (
  functional_completeness * 0.15 +
  correctness_robustness * 0.14 +
  architecture * 0.12 +
  code_quality * 0.12 +
  security * 0.10 +
  type_safety * 0.10 +
  testing * 0.10 +
  maintainability * 0.09 +
  performance * 0.04 +
  best_practices * 0.04
)
```

### Step 3: Determine Grade
| Grade | Score Range |
|-------|-------------|
| A+ | 97-100 |
| A | 93-96 |
| A- | 90-92 |
| B+ | 87-89 |
| B | 83-86 |
| B- | 80-82 |
| C+ | 77-79 |
| C | 73-76 |
| C- | 70-72 |
| D | 60-69 |
| F | 0-59 |

### Step 4: Determine Winner
- **Winner**: Higher overall_score
- **Tie**: If difference < 3 points
- **Margin**: negligible (<3), slight (3-7), moderate (8-14), significant (15-24), decisive (25+)

---

## Output Format

Return ONLY a JSON object. No markdown code fences. No text before or after.

```json
{
  "implementation_a": {
    "functional_completeness": {"score": 88, "evidence": "9/10 requirements. ✓ CRUD at handlers.py:20-80, ✓ auth at auth.py:15, ✗ missing pagination"},
    "correctness_robustness": {"score": 82, "evidence": "Error handling at api.py:30-50 with custom errors. Edge cases: empty input at validate.py:25. Missing: timeout handling"},
    "architecture": {"score": 85, "evidence": "Clean layers: handlers/ → services/ → repos/. Dependencies flow inward. Minor: utils.py mixed concerns"},
    "code_quality": {"score": 80, "evidence": "Good naming. Longest function: process_order() at orders.py:45 (52 lines). No significant duplication"},
    "security": {"score": 85, "evidence": "Input validation at validators.py:10-40. Secrets from env at config.py:5. No injection vectors found"},
    "type_safety": {"score": 78, "evidence": "90% typed. Optional[] at models.py:20. Some Any at legacy.py:15-20"},
    "testing": {"score": 75, "evidence": "15 test files, 60 tests. Edge cases at test_edge.py. Missing: error path tests"},
    "maintainability": {"score": 82, "evidence": "Constants at constants.py. Config externalized. README present. Extension via plugins/"},
    "performance": {"score": 88, "evidence": "O(n) algorithms appropriate. Set for lookups at search.py:30. No N+1 issues"},
    "best_practices": {"score": 85, "evidence": "Async/await throughout. Consistent style. Context managers at db.py:20"},
    "anti_patterns_found": ["52-line function at orders.py:45", "Some Any types in legacy code"],
    "overall_score": 83,
    "grade": "B",
    "strengths": ["Clean architecture", "Good input validation", "Comprehensive error handling"],
    "weaknesses": ["Missing pagination feature", "Some long functions", "Legacy code has weak typing"]
  },
  "implementation_b": {
    "functional_completeness": {"score": 95, "evidence": "10/10 requirements. All CRUD, auth, AND pagination at handlers.py:20-150"},
    "correctness_robustness": {"score": 90, "evidence": "Comprehensive error handling with retries at client.py:25. All edge cases covered including timeout"},
    "architecture": {"score": 88, "evidence": "Hexagonal architecture. Ports at interfaces/, adapters at infrastructure/. Clean boundaries"},
    "code_quality": {"score": 88, "evidence": "All functions <35 lines. Excellent naming. No duplication detected"},
    "security": {"score": 92, "evidence": "Input validation + output encoding. Secrets from vault at config.py:8. Rate limiting at middleware.py:15"},
    "type_safety": {"score": 90, "evidence": "Strict mode enabled. No Any. Enums at types.py:10. Full Optional[] coverage"},
    "testing": {"score": 85, "evidence": "22 test files, 95 tests. Edge cases + error paths. 85% coverage"},
    "maintainability": {"score": 90, "evidence": "Self-documenting code. All config externalized. Comprehensive README. Plugin system"},
    "performance": {"score": 85, "evidence": "Efficient algorithms. Connection pooling at db.py:15. Minor: could cache computation at calc.py:40"},
    "best_practices": {"score": 88, "evidence": "Modern Python 3.11 features. Dataclasses. Consistent formatting. Proper resource cleanup"},
    "anti_patterns_found": ["Slight over-engineering in DI container at container.py"],
    "overall_score": 89,
    "grade": "B+",
    "strengths": ["Complete implementation", "Excellent type safety", "Strong security", "Good test coverage"],
    "weaknesses": ["Slight over-engineering in DI", "Could add caching"]
  },
  "comparison": {
    "winner": "b",
    "margin": "slight",
    "score_difference": 6,
    "dimension_breakdown": [
      {"dimension": "functional_completeness", "winner": "b", "diff": 7},
      {"dimension": "correctness_robustness", "winner": "b", "diff": 8},
      {"dimension": "architecture", "winner": "b", "diff": 3},
      {"dimension": "code_quality", "winner": "b", "diff": 8},
      {"dimension": "security", "winner": "b", "diff": 7},
      {"dimension": "type_safety", "winner": "b", "diff": 12},
      {"dimension": "testing", "winner": "b", "diff": 10},
      {"dimension": "maintainability", "winner": "b", "diff": 8},
      {"dimension": "performance", "winner": "tie", "diff": -3},
      {"dimension": "best_practices", "winner": "b", "diff": 3}
    ],
    "key_differences": [
      "B implements pagination while A misses it",
      "B has 12 points better type safety with strict mode and no Any",
      "B has comprehensive retry logic and timeout handling for robustness"
    ],
    "recommendation": "Implementation B is better overall. Complete features, stronger type safety, and better error handling. The slight over-engineering in DI is acceptable given the benefits."
  }
}
```

---

## Critical Rules

1. **READ ALL FILES** - Scan every file in both implementations
2. **CITE EVIDENCE** - Every score needs file:line reference
3. **SCORE ALL DIMENSIONS** - No dimension can have score 0 with empty evidence
4. **USE CRITERIA TABLES** - Score based on defined criteria, not intuition
5. **CALCULATE CORRECTLY** - overall_score MUST be the weighted average
6. **BE CONSISTENT** - Apply same standards to both implementations
7. **NO ASSUMPTIONS** - Judge only what you see in the code
8. **COMPLETE AUTONOMOUSLY** - Do not ask questions or pause

**CRITICAL**: Every dimension MUST have:
- A score between 0-100
- Non-empty evidence with file:line references
- If something is "not applicable", explain why and score based on what IS present

**Return ONLY the JSON object. No other text.**
