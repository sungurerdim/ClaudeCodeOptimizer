# cco-test - Run Tests

**Execute tests with automatic framework detection.**

---

## Action

Use the **Task tool** to run tests:

```
subagent_type: Explore
thoroughness: quick
```

### What the Sub-agent Should Do:

**Step 1: Detect Test Framework**

Find the test framework used:

- **Python**: pytest, unittest, nose2
- **JavaScript/TypeScript**: jest, vitest, mocha, ava
- **Go**: go test (built-in)
- **Rust**: cargo test (built-in)
- **Other**: Check config files (pytest.ini, jest.config.js, etc.)

**Step 2: Run Tests**

Execute with coverage if possible:

**Python:**
```bash
pytest --cov --cov-report=term
```

**JavaScript:**
```bash
npm test -- --coverage
```

**Go:**
```bash
go test -cover ./...
```

**Rust:**
```bash
cargo test
```

**Step 3: Report Results**

Show:
- ✅ Tests passed / ❌ Failed
- ⏱️ Total execution time
- 📊 Coverage % (if available)
- 📝 Failed test details (file:line, error message)

---

## Example Output

```
Test Results
============
✅ 127 passed
❌ 3 failed
⏱️ 5.2s
📊 Coverage: 87%

Failed Tests:
1. test_user_login (tests/test_auth.py:42)
   AssertionError: Expected 200, got 401
2. test_data_validation (tests/test_api.py:156)
   ValueError: Invalid email format
```

---

## Notes

- **Fast execution** - quick mode for speed
- **Auto-detection** - no manual framework selection
- **Coverage support** - if framework supports it
- **Detailed failures** - shows exact locations
