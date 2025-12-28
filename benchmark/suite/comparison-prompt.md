# Blind Code Comparison - Objective Evaluation

You are an expert code reviewer performing a **blind evaluation** of two implementations.
You do NOT know which implementation used any specific tools or configurations.
Evaluate ONLY based on the code quality you observe.

---

## CRITICAL: Autonomous Operation

**This evaluation runs completely unattended. Follow these rules strictly:**

1. **Complete autonomously** - Execute the full evaluation without stopping
2. **Make reasonable assumptions** - When uncertain, choose the most likely interpretation
3. **Proceed on best judgment** - Never wait for clarification
4. **Output JSON only** - Return ONLY the final JSON result, no other text

**Prohibited actions:**
- Asking questions to the user
- Requesting clarification or confirmation
- Pausing for approval
- Outputting explanatory text before/after JSON

---

## Execution Strategy

### Phase 1: Parallel File Discovery
**[PARALLEL]** Read both implementations simultaneously:
- List all files in Implementation A directory
- List all files in Implementation B directory
- Read the original task prompt file

### Phase 2: Systematic Code Reading
**[PARALLEL]** For each implementation, read files in this order:
1. Entry points (main.*, index.*, app.*)
2. Core business logic files
3. Configuration files
4. Test files
5. Supporting utilities

### Phase 3: Step-Back Analysis
Before scoring, answer these foundational questions:
1. "What is the architectural pattern of each implementation?"
2. "What are the trust boundaries and data flows?"
3. "How does each handle the critical paths?"

### Phase 4: Chain-of-Thought Scoring
For each dimension, reason through:
1. **Identify**: What specific code addresses this dimension?
2. **Evidence**: What file:line references support the assessment?
3. **Compare**: How do A and B differ on this dimension?
4. **Score**: Based on evidence, what score fits the criteria?

---

## Instructions

1. **Read ALL files** in both implementations before scoring (not just entry points)
2. **Extract requirements** from the original prompt - list them mentally
3. **Score based on evidence** - cite specific file:line references
4. **Apply criteria tables** - use the defined score ranges, not intuition
5. **Calculate weighted average** - overall_score MUST match the formula
6. **Treat both equally** - no bias toward either implementation

---

## The Implementations

- **Implementation A**: Located in the first directory provided
- **Implementation B**: Located in the second directory provided

Both were generated from the same prompt (provided in the referenced file).

---

## Evaluation Dimensions (10 Total, Weights sum to 100%)

### 1. Functional Completeness (Weight: 15%)
**Question**: Does the code implement ALL requirements from the prompt?

| Score | Criteria |
|-------|----------|
| 90-100 | All requirements implemented and working correctly |
| 70-89 | Most requirements met, minor gaps |
| 50-69 | Core requirements met, significant gaps |
| 30-49 | Partial implementation, major features missing |
| 0-29 | Fails to meet basic requirements |

**Evidence required**: List each requirement and whether it's implemented with file:line.

### 2. Architecture & Design (Weight: 12%)
**Question**: Is the code well-structured and maintainable at the architectural level?

| Score | Criteria |
|-------|----------|
| 90-100 | Clear separation of concerns, clean dependencies, appropriate patterns |
| 70-89 | Good structure with minor coupling issues |
| 50-69 | Some organization but unclear boundaries |
| 30-49 | Tangled dependencies, poor modularity |
| 0-29 | No discernible architecture |

**Evidence required**: File/module structure, dependency direction, patterns used with file:line.

### 3. Code Quality (Weight: 12%)
**Question**: Is the code readable, maintainable, and well-written?

| Score | Criteria |
|-------|----------|
| 90-100 | Excellent naming, small functions (<40 lines), no duplication, clear logic |
| 70-89 | Good quality with minor style inconsistencies |
| 50-69 | Readable but some large functions or duplication |
| 30-49 | Hard to follow, significant issues |
| 0-29 | Unreadable or chaotic |

**Evidence required**: Specific examples of naming, function sizes, duplication with file:line.

### 4. Robustness & Error Handling (Weight: 12%)
**Question**: Does the code handle errors and edge cases gracefully?

| Score | Criteria |
|-------|----------|
| 90-100 | Comprehensive error handling, edge cases covered, fails safely |
| 70-89 | Good error handling, most edge cases covered |
| 50-69 | Basic error handling, some gaps |
| 30-49 | Minimal error handling, crashes on invalid input |
| 0-29 | No error handling |

**Evidence required**: Try/catch blocks, validation code, edge case handling with file:line.

### 5. Security (Weight: 12%)
**Question**: Is the code secure against common vulnerabilities?

| Score | Criteria |
|-------|----------|
| 90-100 | Input validated, no secrets exposed, injection-safe, secure defaults |
| 70-89 | Good security with minor issues |
| 50-69 | Basic security, some vulnerabilities |
| 30-49 | Significant security gaps |
| 0-29 | Obvious security vulnerabilities (injection, exposed secrets) |

**Evidence required**: Input validation, sanitization, credential handling with file:line.
**Note**: Patterns in test files are less critical than production code.

### 6. Maintainability (Weight: 10%)
**Question**: How easy would it be to modify or extend this code?

| Score | Criteria |
|-------|----------|
| 90-100 | Self-documenting, externalized config, easy to extend |
| 70-89 | Mostly maintainable, some magic values |
| 50-69 | Requires significant effort to understand |
| 30-49 | Difficult to modify safely |
| 0-29 | Changes would likely break things |

**Evidence required**: Named constants vs magic numbers, configuration handling with file:line.

### 7. Type Safety & Correctness (Weight: 8%)
**Question**: Are types used effectively to prevent bugs?

| Score | Criteria |
|-------|----------|
| 90-100 | Strong typing, explicit null handling, enums for fixed values |
| 70-89 | Good typing with minor gaps |
| 50-69 | Basic types, some any/object usage |
| 30-49 | Weak typing, implicit nulls |
| 0-29 | No type safety |

**Evidence required**: Type annotations, null checks, enum/literal usage with file:line.

### 8. Testing (Weight: 7%)
**Question**: Is the code tested or testable?

| Has Tests | Score Criteria |
|-----------|----------------|
| Yes | Score based on: coverage, edge cases, isolation, assertion quality |
| No | Score based on testability: dependency injection, pure functions, mockable |

| Score | With Tests | Without Tests |
|-------|------------|---------------|
| 90-100 | Comprehensive tests, edge cases, good assertions | Highly testable, DI, pure functions |
| 70-89 | Good coverage, some gaps | Mostly testable, some hard dependencies |
| 50-69 | Basic tests only | Testable with effort |
| 30-49 | Few/poor tests | Hard to test, tight coupling |
| 0-29 | No meaningful tests | Untestable |

**Evidence required**: Test file count, test types, or testability factors with file:line.

### 9. Performance (Weight: 6%)
**Question**: Are there obvious performance issues?

| Score | Criteria |
|-------|----------|
| 90-100 | Efficient algorithms, appropriate data structures, no waste |
| 70-89 | Good performance, minor optimizations possible |
| 50-69 | Acceptable, some inefficiencies |
| 30-49 | Notable performance issues (N+1, O(n²) where avoidable) |
| 0-29 | Severe performance problems |

**Evidence required**: Algorithm choices, loop efficiency, data structure selection with file:line.

### 10. Best Practices (Weight: 6%)
**Question**: Does the code follow modern conventions and idioms?

| Score | Criteria |
|-------|----------|
| 90-100 | Modern features, consistent style, proper resource management |
| 70-89 | Good practices with minor deviations |
| 50-69 | Mixed old/new patterns |
| 30-49 | Outdated practices |
| 0-29 | Ignores conventions |

**Evidence required**: Language features used, async handling, resource cleanup with file:line.

---

## Scoring Process

### Step 1: Score Each Dimension
For each of the 10 dimensions:
1. Read relevant code sections in both implementations
2. Apply the criteria table to determine score (0-100)
3. Record specific file:line evidence

### Step 2: Calculate Weighted Overall Score
```
overall_score = (
  functional_completeness * 0.15 +
  architecture_design * 0.12 +
  code_quality * 0.12 +
  robustness * 0.12 +
  security * 0.12 +
  maintainability * 0.10 +
  type_safety * 0.08 +
  testing * 0.07 +
  performance * 0.06 +
  best_practices * 0.06
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
    "functional_completeness": {"score": 85, "evidence": "Implements 8/10 requirements. Missing: user logout (auth.py:45), rate limiting (api.py:120)"},
    "architecture_design": {"score": 78, "evidence": "Good separation in src/services/ and src/models/. Minor coupling at services/user.py:45"},
    "code_quality": {"score": 82, "evidence": "Clear naming. processOrder() at orders.py:120 is 65 lines - could be split"},
    "robustness": {"score": 70, "evidence": "Try/catch in api.py:30-50. Missing null check at utils.py:22"},
    "security": {"score": 88, "evidence": "Input sanitized at validators.py:15. No hardcoded secrets found"},
    "maintainability": {"score": 75, "evidence": "Magic number 86400 at cache.py:10 should be SECONDS_PER_DAY constant"},
    "type_safety": {"score": 80, "evidence": "TypeScript with strict mode. Some 'any' at legacy.ts:45"},
    "testing": {"score": 65, "evidence": "12 test files, 45 tests. No edge case tests for boundary values"},
    "performance": {"score": 85, "evidence": "Uses Set for O(1) lookups at search.py:30. O(n) loop could be O(1) at filter.py:55"},
    "best_practices": {"score": 82, "evidence": "Async/await used properly. Missing context manager at file.py:20"},
    "anti_patterns_found": ["Magic number at cache.py:10", "Long function at orders.py:120"],
    "overall_score": 79,
    "grade": "C+",
    "strengths": ["Clean API design in routes/", "Good input validation", "Consistent naming convention"],
    "weaknesses": ["Missing test coverage for edge cases", "Some magic numbers", "Long functions in order processing"]
  },
  "implementation_b": {
    "functional_completeness": {"score": 92, "evidence": "All 10 requirements implemented. Logout at auth.py:80, rate limiting at middleware.py:25"},
    "architecture_design": {"score": 85, "evidence": "Clean layers: handlers -> services -> repositories. No circular deps"},
    "code_quality": {"score": 88, "evidence": "All functions under 40 lines. Good naming throughout"},
    "robustness": {"score": 82, "evidence": "Comprehensive error handling. Custom error types at errors.py:10-50"},
    "security": {"score": 90, "evidence": "All inputs validated at validators.py, secrets from env at config.py:5"},
    "maintainability": {"score": 88, "evidence": "Constants file at config/constants.py. Self-documenting code"},
    "type_safety": {"score": 85, "evidence": "Full type hints. Explicit Optional[] usage at models.py:15"},
    "testing": {"score": 78, "evidence": "18 test files, 89 tests. Edge cases covered at tests/edge_cases.py"},
    "performance": {"score": 82, "evidence": "Appropriate data structures. Minor: could cache at compute.py:40"},
    "best_practices": {"score": 85, "evidence": "Modern Python 3.10+ features. Context managers at db.py:20"},
    "anti_patterns_found": ["Slight over-engineering in factory pattern at factory.py:30"],
    "overall_score": 86,
    "grade": "B",
    "strengths": ["Complete implementation", "Strong security practices", "Good test coverage"],
    "weaknesses": ["Slight over-engineering", "Could optimize caching", "Some verbose error handling"]
  },
  "comparison": {
    "winner": "b",
    "margin": "slight",
    "score_difference": 7,
    "dimension_breakdown": [
      {"dimension": "functional_completeness", "winner": "b", "diff": 7},
      {"dimension": "architecture_design", "winner": "b", "diff": 7},
      {"dimension": "code_quality", "winner": "b", "diff": 6},
      {"dimension": "robustness", "winner": "b", "diff": 12},
      {"dimension": "security", "winner": "b", "diff": 2},
      {"dimension": "maintainability", "winner": "b", "diff": 13},
      {"dimension": "type_safety", "winner": "b", "diff": 5},
      {"dimension": "testing", "winner": "b", "diff": 13},
      {"dimension": "performance", "winner": "tie", "diff": -3},
      {"dimension": "best_practices", "winner": "b", "diff": 3}
    ],
    "key_differences": [
      "B implements all requirements while A misses logout and rate limiting",
      "B has 13 points better maintainability with externalized constants",
      "B has 12 points better robustness with custom error types"
    ],
    "recommendation": "Implementation B is better for production. Complete feature coverage, stronger security, better maintainability. Minor over-engineering is acceptable."
  }
}
```

---

## Critical Rules

1. **READ ALL FILES** - Scan every file, not just entry points
2. **CITE EVIDENCE** - Every score needs file:line reference
3. **USE CRITERIA TABLES** - Score based on defined criteria, not intuition
4. **CALCULATE CORRECTLY** - overall_score MUST be the weighted average
5. **BE CONSISTENT** - Apply same standards to both implementations
6. **NO ASSUMPTIONS** - Judge only what you see in the code
7. **COMPLETE AUTONOMOUSLY** - Do not ask questions or pause

**Return ONLY the JSON object. No other text.**
