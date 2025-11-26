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

## Coverage Goals

**Current**: 82%
**Target**: 85%

**Priority areas**:
1. Knowledge setup (core/knowledge_setup.py)
2. CCO status (cco_status.py)
3. CCO update (cco_update.py)
4. Content management (content handling)
5. CLI commands (install, remove, status, update)

## Testing Guidelines

- **Evidence-Based Verification** - All tests must verify with actual command output
- **Fail-Fast** - Tests fail loudly, no silent failures
- **Isolation** - Each test is independent
- **Deterministic** - Same input always produces same output
