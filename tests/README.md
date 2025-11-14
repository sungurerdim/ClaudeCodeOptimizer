# CCO Test Suite

## Structure

```
tests/
├── unit/           # Unit tests (isolated, fast)
├── integration/    # Integration tests (multi-component)
├── conftest.py     # Shared fixtures
└── README.md       # This file
```

## Test Strategy

### Unit Tests
- Test individual functions/classes in isolation
- Mock external dependencies
- Fast execution (<100ms per test)
- Target: 60% coverage

### Integration Tests
- Test component interactions
- Use real filesystems (temp directories)
- Verify end-to-end workflows
- Target: Key user flows covered

## Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# With coverage
pytest --cov=claudecodeoptimizer --cov-report=html
```

## Coverage Goals (v0.2.0)

**Current**: 0%
**Target**: 60%

**Priority areas**:
1. Detection engine (ai/detection.py)
2. Principle selection (core/principle_selector.py)
3. Linking strategy (core/linking.py)
4. CLAUDE.md generation (core/claude_md_generator.py)
5. Command selection (ai/command_selection.py)

## Test Principles

- **P_INCREMENTAL_SAFETY_PATTERNS: Evidence-Based Verification** - All tests must verify with actual command output
- **P001: Fail-Fast** - Tests fail loudly, no silent failures
- **Isolation** - Each test is independent
- **Deterministic** - Same input always produces same output
