# Code Comparison Evaluation Criteria

You are comparing two code implementations generated from the same prompt. Evaluate both fairly and objectively.

## Evaluation Dimensions

### 1. Prompt Compliance (Weight: 30%)
- Does the code fulfill ALL requirements from the original prompt?
- Are there missing features or functionalities?
- Are there unnecessary extras that weren't requested?
- Rate: How well does each implementation match the prompt's intent?

### 2. Code Quality (Weight: 20%)
- Readability: Is the code easy to understand?
- Naming: Are variables, functions, classes named meaningfully?
- Structure: Is the code well-organized?
- DRY: Is there unnecessary repetition?
- KISS: Is the solution appropriately simple?

### 3. Robustness (Weight: 20%)
- Error handling: Are errors caught and handled gracefully?
- Edge cases: Does the code handle unusual inputs?
- Input validation: Are inputs validated at boundaries?
- Defensive programming: Does it fail safely?

### 4. Security (Weight: 15%)
- Input sanitization: Is user input properly sanitized?
- No hardcoded secrets: Are credentials externalized?
- Safe patterns: No SQL injection, XSS, command injection risks?
- Principle of least privilege observed?

### 5. Best Practices (Weight: 15%)
- Type safety: Are types used appropriately?
- Documentation: Are complex parts documented?
- Modern patterns: Does it use current language idioms?
- Testability: Is the code easy to test?

## Output Format

Respond with a JSON object (no markdown code blocks):

{
  "cco": {
    "prompt_compliance": {"score": 0-100, "notes": "..."},
    "code_quality": {"score": 0-100, "notes": "..."},
    "robustness": {"score": 0-100, "notes": "..."},
    "security": {"score": 0-100, "notes": "..."},
    "best_practices": {"score": 0-100, "notes": "..."},
    "overall_score": 0-100,
    "grade": "A+ to F",
    "strengths": ["top 3 strengths"],
    "weaknesses": ["top 3 weaknesses"]
  },
  "vanilla": {
    "prompt_compliance": {"score": 0-100, "notes": "..."},
    "code_quality": {"score": 0-100, "notes": "..."},
    "robustness": {"score": 0-100, "notes": "..."},
    "security": {"score": 0-100, "notes": "..."},
    "best_practices": {"score": 0-100, "notes": "..."},
    "overall_score": 0-100,
    "grade": "A+ to F",
    "strengths": ["top 3 strengths"],
    "weaknesses": ["top 3 weaknesses"]
  },
  "comparison": {
    "winner": "cco" | "vanilla" | "tie",
    "margin": "decisive" | "moderate" | "slight" | "negligible",
    "verdict": "Strong CCO Advantage" | "Moderate CCO Advantage" | "Mixed Results" | "Moderate Vanilla Advantage" | "Strong Vanilla Advantage",
    "key_differences": ["difference 1", "difference 2", "difference 3"],
    "recommendation": "Which to use for production and why (1-2 sentences)"
  }
}

IMPORTANT: Return ONLY the JSON, no explanations.
