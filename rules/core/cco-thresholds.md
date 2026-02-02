# CCO Thresholds Reference

## Code Complexity

| Metric | Threshold | Override When |
|--------|-----------|---------------|
| Cyclomatic complexity | ≤ 15 | Inherent branching (state machines, parsers, protocol handlers) |
| Method lines | ≤ 50 | Generated code, single logical operation, perf-critical hot paths |
| File lines | ≤ 500 | Generated files, test files, config/data files |
| Nesting depth | ≤ 3 | Data structure mirrors nesting; use early returns first |
| Parameters | ≤ 4 | Framework callbacks, math functions, builder steps |

## Test Coverage

| Metric | Threshold | Override When |
|--------|-----------|---------------|
| Target coverage | 70-80% | — |
| Minimum coverage | 60% | Legacy incremental improvement, prototypes, generated code |

## Architecture

| Metric | Threshold | Override When |
|--------|-----------|---------------|
| Coupling | < 40% good, < 50% acceptable | Tightly integrated subsystems by design |
| Cohesion | > 75% good, > 70% acceptable | Facade/adapter modules with intentional breadth |

## Confidence Scoring

| Level | Range | Meaning |
|-------|-------|---------|
| High | ≥ 80% | Strong evidence, tool-confirmed or multi-indicator |
| Medium | 50-79% | Likely issue, single indicator or heuristic match |
| Low | < 50% | Possible issue, may be false positive |

## Gap Analysis Severity

| Severity | Deviation | Example (complexity limit 15) |
|----------|-----------|-------------------------------|
| HIGH | > 2x threshold | 35 |
| MEDIUM | 1x-2x threshold | 20 |
| LOW | At or near threshold | 16 |

## References

| Source | Used For |
|--------|----------|
| McCabe (1976) | Cyclomatic complexity |
| Miller (1956) | Cognitive limits (parameters, method length) |
| Fowler, "Refactoring" | Code smells, method length |
| Martin, "Clean Code" | Parameter counts, function design |
| Google Testing Blog | Coverage targets |
| NASA/JPL Coding Standard | Line limits |
| Yourdon & Constantine | Coupling, cohesion |
| Linux Kernel Style | Nesting depth |

## Override Protocol

1. Document in code: `# threshold-override: {metric} - {reason}`
2. Set a local limit (e.g., allow 25, not unlimited)
3. Review during major refactors
