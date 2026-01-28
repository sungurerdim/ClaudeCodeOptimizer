# CCO Thresholds Reference
*Documented magic numbers, thresholds, and their justifications*

This file serves as the single source of truth for all hardcoded thresholds used across CCO rules, agents, and commands. Each threshold includes its rationale and conditions for override.

---

## Code Complexity Limits

### Cyclomatic Complexity: ≤ 15

| Aspect | Value |
|--------|-------|
| **Threshold** | 15 |
| **Used in** | Foundation rules, analyze agent, complexity checks |
| **Source** | McCabe, T.J. (1976) "A Complexity Measure" |

**Rationale:** McCabe's original research established that functions with cyclomatic complexity >10 are difficult to test and maintain. The industry standard has settled on 10-15 as acceptable, with 15 being the upper bound for complex but still maintainable code.

| Range | Interpretation |
|-------|----------------|
| 1-10 | Simple, low risk |
| 11-15 | Moderate complexity, acceptable |
| 16-20 | High complexity, consider refactoring |
| >20 | Very high risk, refactor required |

**Override when:** Algorithm inherently requires branching (state machines, parsers, protocol handlers). Document with `# complexity: justified - {reason}`.

---

### Method Lines: ≤ 50

| Aspect | Value |
|--------|-------|
| **Threshold** | 50 lines |
| **Used in** | Foundation rules, code review, refactoring suggestions |
| **Source** | NASA/JPL Coding Standards, Martin Fowler's Refactoring |

**Rationale:** Research shows developers can hold approximately 7±2 chunks of information in working memory (Miller's Law). A 50-line function fits on most screens and can be understood in a single reading session. NASA/JPL standards recommend 60 lines max; 50 provides safety margin.

**Override when:**
- Generated code (serializers, migrations)
- Single logical operation that would be fragmented by extraction
- Performance-critical hot paths where inlining matters

---

### File Lines: ≤ 500

| Aspect | Value |
|--------|-------|
| **Threshold** | 500 lines |
| **Used in** | Foundation rules, architecture analysis |
| **Source** | Industry practice, Google Style Guides |

**Rationale:** Files over 500 lines typically indicate multiple responsibilities. Studies show code review effectiveness drops significantly for files >400 lines. The 500-line limit balances practicality with maintainability.

**Override when:**
- Generated files (protobuf, OpenAPI)
- Test files with many test cases
- Configuration/data files

---

### Nesting Depth: ≤ 3

| Aspect | Value |
|--------|-------|
| **Threshold** | 3 levels |
| **Used in** | Foundation rules, readability checks |
| **Source** | Linux Kernel Coding Style, cognitive load research |

**Rationale:** Each nesting level multiplies cognitive load. The Linux kernel coding style famously states "if you need more than 3 levels of indentation, you're screwed anyway." Deep nesting correlates with bugs and makes code paths difficult to trace.

```python
# BAD: 4+ levels deep
if condition:
    for item in items:
        if item.valid:
            for sub in item.subs:  # Level 4 - too deep
                process(sub)

# GOOD: Extract to reduce nesting
def process_valid_items(items):
    for item in items:
        if item.valid:
            process_subitems(item.subs)
```

**Override when:** Deeply nested data structures require matching code structure. Use early returns and extraction first.

---

### Parameters: ≤ 4

| Aspect | Value |
|--------|-------|
| **Threshold** | 4 parameters |
| **Used in** | Foundation rules, function signature analysis |
| **Source** | Clean Code (Robert Martin), Miller's Law |

**Rationale:** Functions with >4 parameters are hard to call correctly without IDE support. They often indicate the function is doing too much or parameters should be grouped into an object.

```python
# BAD: Too many parameters
def create_user(name, email, age, address, phone, role, department):
    ...

# GOOD: Group related parameters
@dataclass
class UserData:
    name: str
    email: str
    contact: ContactInfo
    role: RoleInfo

def create_user(data: UserData):
    ...
```

**Override when:**
- Callback signatures dictated by frameworks
- Mathematical functions with inherently many inputs
- Builder pattern intermediate steps

---

## Test Coverage Thresholds

### Target Coverage: 70-80%

| Aspect | Value |
|--------|-------|
| **Threshold** | 70-80% line coverage |
| **Used in** | Quality gates, CI/CD checks |
| **Source** | Google Testing Blog, industry research |

**Rationale:** Google's testing research found diminishing returns above 80% coverage. The cost of achieving 90%+ coverage often exceeds the bug-prevention benefit. 70-80% covers critical paths while allowing pragmatic exceptions for edge cases.

| Coverage | Interpretation |
|----------|----------------|
| <60% | Insufficient, high risk |
| 60-70% | Minimum acceptable |
| 70-80% | Target range, good balance |
| 80-90% | High coverage, watch for test maintenance burden |
| >90% | Diminishing returns, may indicate over-testing |

---

### Minimum Coverage: 60%

| Aspect | Value |
|--------|-------|
| **Threshold** | 60% line coverage |
| **Used in** | Quality gates, PR requirements |
| **Source** | Industry practice |

**Rationale:** Below 60%, too many code paths are untested to have confidence in refactoring or changes. This is the minimum threshold for code that will be maintained long-term.

**Override when:**
- Legacy code being incrementally improved
- Prototype/experimental code (mark clearly)
- Generated code that's tested by generator's tests

---

## Architecture Metrics

### Coupling Threshold: <40-50%

| Aspect | Value |
|--------|-------|
| **Threshold** | <40% (good), <50% (acceptable) |
| **Used in** | align command, architecture analysis |
| **Source** | Structured Design (Yourdon & Constantine) |

**Rationale:** Coupling measures interdependence between modules. High coupling (>50%) means changes ripple across the codebase. Yourdon & Constantine's research established that loosely coupled systems are easier to maintain and test.

| Coupling % | Interpretation |
|------------|----------------|
| <30% | Excellent, highly modular |
| 30-40% | Good, maintainable |
| 40-50% | Acceptable, monitor trends |
| >50% | High risk, consider restructuring |

**Calculation:** `(external_dependencies / total_dependencies) * 100`

---

### Cohesion Threshold: >70-75%

| Aspect | Value |
|--------|-------|
| **Threshold** | >75% (good), >70% (acceptable) |
| **Used in** | align command, architecture analysis |
| **Source** | Structured Design (Yourdon & Constantine) |

**Rationale:** Cohesion measures how related the elements within a module are. High cohesion (>75%) indicates single responsibility. Low cohesion suggests the module should be split.

| Cohesion % | Interpretation |
|------------|----------------|
| >85% | Excellent, single purpose |
| 75-85% | Good, focused |
| 70-75% | Acceptable, minor improvements possible |
| <70% | Consider splitting module |

**Calculation:** Based on method-to-attribute access patterns (LCOM variants).

---

## Confidence Scoring

### High Confidence: ≥80%

| Aspect | Value |
|--------|-------|
| **Threshold** | 80-100% |
| **Used in** | analyze agent, finding classification |
| **Meaning** | Strong evidence, high certainty |

**Factors contributing to high confidence:**
- Static analysis tool confirmed
- Pattern matches known vulnerability signature
- Multiple indicators present
- Clear specification violation

---

### Medium Confidence: 50-79%

| Aspect | Value |
|--------|-------|
| **Threshold** | 50-79% |
| **Used in** | analyze agent, finding classification |
| **Meaning** | Likely issue, warrants review |

**Factors:**
- Heuristic match without confirmation
- Context suggests but doesn't prove issue
- Single indicator present

---

### Low Confidence: <50%

| Aspect | Value |
|--------|-------|
| **Threshold** | <50% |
| **Used in** | analyze agent, finding classification |
| **Meaning** | Possible issue, manual review required |

**Factors:**
- Fuzzy pattern match
- May be false positive
- Unusual code pattern that might be intentional

---

## Severity Classification

### HIGH Severity: >2x threshold deviation

| Aspect | Value |
|--------|-------|
| **Threshold** | More than 2x the target threshold |
| **Used in** | Gap analysis, prioritization |
| **Example** | Cyclomatic complexity 35 when limit is 15 |

**Rationale:** Deviations this large indicate systemic issues, not edge cases. Prioritize immediate attention.

---

### MEDIUM Severity: >1x threshold deviation

| Aspect | Value |
|--------|-------|
| **Threshold** | Between 1x and 2x the target threshold |
| **Used in** | Gap analysis, prioritization |
| **Example** | Cyclomatic complexity 20 when limit is 15 |

**Rationale:** Notable deviation that should be addressed but isn't critical. Schedule for near-term improvement.

---

### LOW Severity: At or near threshold

| Aspect | Value |
|--------|-------|
| **Threshold** | At threshold or slightly over |
| **Used in** | Gap analysis, prioritization |
| **Example** | Cyclomatic complexity 16 when limit is 15 |

**Rationale:** Minor deviation, address opportunistically during related work.

---

## References

| Source | Citation | Used For |
|--------|----------|----------|
| McCabe (1976) | "A Complexity Measure", IEEE Trans. Software Engineering | Cyclomatic complexity |
| Miller (1956) | "The Magical Number Seven", Psychological Review | Cognitive limits |
| Martin Fowler | "Refactoring: Improving the Design of Existing Code" | Code smells, method length |
| Robert Martin | "Clean Code" | Parameter counts, function design |
| Google Testing Blog | "Code Coverage Best Practices" | Coverage targets |
| NASA/JPL | "JPL Institutional Coding Standard for C" | Line limits, safety |
| Yourdon & Constantine | "Structured Design" | Coupling, cohesion metrics |
| Linux Kernel | "Linux Kernel Coding Style" | Nesting depth |

---

## Override Protocol

When overriding a threshold:

1. **Document the override** in code or config
2. **State the reason** (e.g., `# threshold-override: complexity - state machine`)
3. **Set a local limit** if possible (e.g., allow 25 but not unlimited)
4. **Review periodically** - overrides should be reconsidered during major refactors
