# Testing Rules
*Coverage targets and test patterns*

**Trigger:** {test_framework}, {coverage_config}, {test_dirs}

## Coverage Targets [CRITICAL]

| Code Type | Line | Branch | Examples |
|-----------|------|--------|----------|
| Critical | 90-100% | 85-100% | Payment, auth, security |
| Core | 80-90% | 75-85% | Business logic, APIs |
| Standard | 75-85% | 70-80% | Features, utilities |
| Infrastructure | 60-75% | 55-70% | Config, helpers |

### Mutation Testing

| Code Type | Target Score |
|-----------|-------------|
| Critical | 80-95% |
| Core | 75-85% |
| Standard | 70-80% |

Tools: PIT (Java), Stryker (JS/TS), mutmut (Python)

---

## Required Edge Cases

**Always test:**
- Empty/None/null
- Whitespace-only strings
- Boundary values: 0, 1, max, max+1
- Type coercion: string "1" vs int 1
- Unicode edge cases

---

## Test Isolation Requirements

| Resource | Mock Instead |
|----------|--------------|
| Database | Repository interface |
| File System | File interface |
| External APIs | HTTP client |
| System Time | Clock interface |
| Random | Generator interface |

---

## Naming Convention

`[Method]_[Scenario]_[Expected]`

Examples:
- `add_with_negative_numbers_raises_value_error`
- `login_with_valid_credentials_returns_token`
- `parse_empty_string_returns_none`

---

## Property-Based Testing

**Use when**: Large input space, properties should hold for ANY input

Common properties:
- Roundtrip: `decode(encode(x)) == x`
- Idempotent: `f(f(x)) == f(x)`
- Commutative: `f(a, b) == f(b, a)`
- Invariant: `len(sorted(xs)) == len(xs)`

---

## Security Testing Integration

| Phase | Tool Type | Gate |
|-------|-----------|------|
| Pre-commit | SAST | Block on new violations |
| Per-commit | SCA | Block on CRITICAL CVE |
| Post-build | DAST | Block deploy on failure |
| Pre-push | Secret Detection | Block on detected secrets |

Tools: Semgrep, Snyk, OWASP ZAP, gitleaks
