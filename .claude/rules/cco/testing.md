# Testing Rules

## Standard Testing (80% Coverage)
- **Unit-Isolated**: Fast, deterministic unit tests with no external dependencies
- **Mocking**: Use unittest.mock for external dependencies (APIs, databases)
- **Fixtures**: Pytest fixtures for reusable, maintainable test data
- **Integration-Tests**: Test component interactions in tests/integration/
- **Coverage-80**: Minimum 80% line coverage enforced in CI
- **CI-on-PR**: Tests run on every PR, block merge on failure
- **Test-Organization**: tests/unit/ for unit tests, tests/integration/ for integration tests
- **Test-Naming**: Use test_{feature}_{scenario} pattern
- **Assertions-Clear**: Descriptive assertion messages for failure clarity

## Edge Case Coverage [MANDATORY]
- **Empty/None**: empty string "", None, empty list [], empty dict {}
- **Whitespace**: spaces, tabs, newlines, whitespace-only strings
- **Boundaries**: 0, 1, max, max+1 (for numeric ranges)
- **Type Variations**: string vs int, case variations, unicode, emoji
- **State Combinations**: valid state pairs where multiple states interact

## Test Quality
- **Parametrize**: Use @pytest.mark.parametrize for testing multiple inputs
- **Skip-Conditional**: Use @pytest.mark.skipif for platform/version conditions
- **Isolation**: Each test independent, no shared state between tests
- **Performance**: Unit tests should complete in <1s, integration <10s
