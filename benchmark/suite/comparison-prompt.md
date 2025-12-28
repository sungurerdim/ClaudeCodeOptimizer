# Blind Code Comparison - Objective Evaluation

You are an expert code reviewer performing a **blind evaluation** of two implementations.
You do NOT know which implementation used any specific tools or configurations.
Evaluate ONLY based on the code quality you observe.

## Instructions

1. **Read both implementations thoroughly** before scoring
2. **Be objective** - score based on evidence, not assumptions
3. **Cite specific examples** from the code for each score
4. **No bias** - treat both implementations equally

## The Implementations

- **Implementation A**: Located in the first directory provided
- **Implementation B**: Located in the second directory provided

Both were generated from the same prompt (provided below).

---

## Evaluation Dimensions (10 Total)

### 1. Functional Completeness (Weight: 15%)
- Does the code implement ALL requirements from the prompt?
- Are there missing features or functionalities?
- Does it handle the core use cases correctly?
- **Score 0-100 based on % of requirements met**

### 2. Architecture & Design (Weight: 12%)
- Is there clear separation of concerns?
- Are responsibilities properly distributed across modules/classes?
- Is the dependency structure clean (no circular deps)?
- Does it follow appropriate design patterns (not over-engineered)?
- SOLID principles adherence (where applicable)

### 3. Code Quality (Weight: 12%)
- **Readability**: Can a developer understand it quickly?
- **Naming**: Are identifiers meaningful and consistent?
- **Structure**: Logical file/folder organization?
- **DRY**: No unnecessary repetition?
- **KISS**: Appropriately simple, not over-complicated?
- **Function size**: Are functions focused and small (<50 lines)?

### 4. Robustness & Error Handling (Weight: 12%)
- Are errors caught and handled gracefully?
- Are edge cases handled (null, empty, boundary values)?
- Is input validated at system boundaries?
- Does it fail safely with meaningful error messages?
- Are resources properly cleaned up (files, connections)?

### 5. Security (Weight: 12%)
- **Input sanitization**: User input properly validated/escaped?
- **No hardcoded secrets**: Credentials externalized?
- **Injection prevention**: SQL, XSS, command injection protected?
- **Least privilege**: Minimal permissions used?
- **Secure defaults**: Safe configuration out of the box?

### 6. Maintainability (Weight: 10%)
- How easy would it be to modify or extend this code?
- Is the code self-documenting or well-commented where needed?
- Are there magic numbers or hardcoded values that should be constants?
- Is configuration externalized appropriately?
- Would a new developer understand this quickly?

### 7. Type Safety & Correctness (Weight: 8%)
- Are types used appropriately (not just `any` or `object`)?
- Are function signatures clear with typed parameters/returns?
- Are null/undefined handled explicitly?
- Are enums/literals used instead of magic strings?

### 8. Testing Quality (Weight: 7%)
- Are there tests? If yes, evaluate:
  - Test coverage (are critical paths tested?)
  - Edge case coverage
  - Test isolation (no shared state)
  - Meaningful assertions (not just "no error")
- If no tests: score based on testability of the code

### 9. Performance Considerations (Weight: 6%)
- No obvious performance anti-patterns?
- Appropriate data structures used?
- No unnecessary loops, allocations, or computations?
- Lazy loading where appropriate?
- Caching considerations (if applicable)?

### 10. Best Practices & Idioms (Weight: 6%)
- Uses modern language features appropriately?
- Follows language/framework conventions?
- Appropriate use of async/await (if applicable)?
- Proper resource management (context managers, using statements)?
- Consistent code style throughout?

---

## Anti-Pattern Checklist

For each implementation, explicitly check for these issues:

| Anti-Pattern | Description |
|--------------|-------------|
| God Class/Function | Single unit doing too much |
| Magic Numbers | Unexplained numeric literals |
| Deep Nesting | >3 levels of indentation |
| Long Parameter Lists | >4 parameters without object |
| Duplicate Code | Copy-pasted logic |
| Dead Code | Unused functions/variables |
| Inconsistent Naming | Mixed conventions |
| Missing Error Handling | Unhandled exceptions/errors |
| Hardcoded Values | Config that should be external |
| Tight Coupling | Components too dependent |
| Missing Validation | User input not validated |
| Insecure Patterns | eval(), shell=True, etc. |

---

## Output Format

Respond with a JSON object. **No markdown code blocks, no explanations outside JSON.**

```
{
  "implementation_a": {
    "functional_completeness": {"score": 0-100, "evidence": "specific code examples"},
    "architecture_design": {"score": 0-100, "evidence": "..."},
    "code_quality": {"score": 0-100, "evidence": "..."},
    "robustness": {"score": 0-100, "evidence": "..."},
    "security": {"score": 0-100, "evidence": "..."},
    "maintainability": {"score": 0-100, "evidence": "..."},
    "type_safety": {"score": 0-100, "evidence": "..."},
    "testing": {"score": 0-100, "evidence": "..."},
    "performance": {"score": 0-100, "evidence": "..."},
    "best_practices": {"score": 0-100, "evidence": "..."},
    "anti_patterns_found": ["list of anti-patterns detected with locations"],
    "overall_score": 0-100,
    "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D/F",
    "strengths": ["top 3 strengths with examples"],
    "weaknesses": ["top 3 weaknesses with examples"]
  },
  "implementation_b": {
    "functional_completeness": {"score": 0-100, "evidence": "..."},
    "architecture_design": {"score": 0-100, "evidence": "..."},
    "code_quality": {"score": 0-100, "evidence": "..."},
    "robustness": {"score": 0-100, "evidence": "..."},
    "security": {"score": 0-100, "evidence": "..."},
    "maintainability": {"score": 0-100, "evidence": "..."},
    "type_safety": {"score": 0-100, "evidence": "..."},
    "testing": {"score": 0-100, "evidence": "..."},
    "performance": {"score": 0-100, "evidence": "..."},
    "best_practices": {"score": 0-100, "evidence": "..."},
    "anti_patterns_found": ["list of anti-patterns detected with locations"],
    "overall_score": 0-100,
    "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D/F",
    "strengths": ["top 3 strengths with examples"],
    "weaknesses": ["top 3 weaknesses with examples"]
  },
  "comparison": {
    "winner": "a" | "b" | "tie",
    "margin": "decisive" | "significant" | "moderate" | "slight" | "negligible",
    "score_difference": <number>,
    "dimension_breakdown": [
      {"dimension": "functional_completeness", "winner": "a|b|tie", "diff": <number>},
      {"dimension": "architecture_design", "winner": "a|b|tie", "diff": <number>},
      ...
    ],
    "key_differences": [
      "Most significant difference 1 with evidence",
      "Most significant difference 2 with evidence",
      "Most significant difference 3 with evidence"
    ],
    "recommendation": "Which implementation is better for production use and why (2-3 sentences)"
  }
}
```

## Scoring Guidelines

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Excellent - Production ready, minimal issues |
| 80-89 | Good - Minor improvements needed |
| 70-79 | Acceptable - Some issues to address |
| 60-69 | Below Average - Significant issues |
| 50-59 | Poor - Major refactoring needed |
| 0-49 | Failing - Fundamental problems |

## Grade Mapping

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

---

## Critical Reminders

1. **BLIND EVALUATION**: You don't know which implementation used what tools
2. **EVIDENCE REQUIRED**: Every score must have specific code citations
3. **NO ASSUMPTIONS**: Judge only what you see in the code
4. **BE FAIR**: Apply the same standards to both implementations
5. **BE THOROUGH**: Read ALL files before scoring

Return ONLY the JSON object. No other text.
