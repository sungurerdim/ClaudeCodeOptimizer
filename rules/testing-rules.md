# Testing Rules
*Test coverage and quality requirements by tier*

**Inheritance:** Higher tiers include lower.

## Basics (Testing:60%)
- **Unit-Isolated**: Fast, deterministic unit tests
- **Mocking**: Isolate tests from external dependencies
- **Coverage-60**: Minimum 60% line coverage

## Standard (Testing:80%)
- **Integration**: Test component interactions
- **Fixtures**: Reusable, maintainable test data
- **Coverage-80**: Minimum 80% line coverage
- **CI-on-PR**: Tests run on every PR
- **Edge-Cases-Standard**: Test empty, None, single item, typical, boundary values

## Full (Testing:90%)
- **E2E**: End-to-end tests for critical user flows
- **Contract**: Consumer-driven contract testing (if Architecture:Microservices)
- **Mutation**: Mutation testing for test effectiveness (if Priority:Quality)
- **Coverage-90**: Minimum 90% line coverage
- **Edge-Cases-Full**: Test whitespace-only, unicode, max+1, state combinations, concurrent access

## Edge Case Checklist [MANDATORY - ALL TIERS]
When generating tests, always include:
- **Empty-None**: empty string, None, empty list/dict
- **Whitespace**: spaces, tabs, newlines, whitespace-only strings
- **Boundaries**: 0, 1, max, max+1, negative (if applicable)
- **Type-Variations**: string vs int representations, case variations for strings
- **State-Combinations**: all valid state pairs where multiple states can interact
- **Unicode**: emojis, RTL text, special characters (if string handling)
- **Timing**: expired dates, future dates, boundary timestamps
