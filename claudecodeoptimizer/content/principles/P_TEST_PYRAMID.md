# P_TEST_PYRAMID: Test Pyramid

**Severity**: Medium

Maintain 70% unit, 20% integration, 10% E2E tests. Inverted pyramids (too many E2E) are slow, flaky, hard to debug, and expensive.

---

## Rules

- **70% Unit** - Fast (<1ms), isolated, no dependencies
- **20% Integration** - Medium (~100ms), test component interactions
- **10% E2E** - Slow (seconds), critical user journeys only
- **Organize by type** - Separate test directories

---

## Examples

### ✅ Unit Test
```python
def test_calculate_discount():
    assert calculate_discount(100, 0.2) == 80.0  # <1ms
```
**Why right**: Fast, isolated, no dependencies

### ❌ Bad: E2E for Business Logic
```javascript
// ❌ Testing validation with E2E (5-10 seconds)
test("user cannot submit invalid email", async () => {
    await page.goto("https://localhost:3000/register");
    await page.fill("#email", "invalid");
    await expect(page.locator(".error")).toHaveText("Invalid email");
});

// ✅ Unit test instead (<1ms)
test("validateEmail rejects invalid", () => {
    expect(validateEmail("invalid")).toBe(false);
});
```
**Why wrong**: 5000x slower (5s vs 1ms); can't test all edge cases

---

## Anti-Patterns

**❌ Testing Business Logic with E2E**: 5000x slower; flaky; can't test edge cases
**❌ No Integration Tests**: Don't discover integration issues until slow E2E
**❌ Flaky E2E Tests**: Team ignores them; add proper waits

---

## Checklist

- [ ] 70% unit (fast, isolated)
- [ ] 20% integration (component interactions)
- [ ] 10% E2E (critical flows only)
- [ ] Measure ratio in CI
- [ ] Organize by type: tests/unit, tests/integration, tests/e2e
