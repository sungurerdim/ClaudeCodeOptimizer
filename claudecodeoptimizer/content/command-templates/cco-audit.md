---
name: cco-audit
description: Security and code quality analysis with auto-fix
allowed-tools: Bash(git:*), Bash(grep:*), Bash(find:*), Read(*), Grep(*), Glob(*), Edit(*), Task(*)
---

# /cco-audit

**Security & Code Quality** - Analyze → prioritize → fix → verify.

End-to-end: Detects security and quality issues AND fixes them.

**Standards:** Command Flow | Fix Workflow | Approval Flow | Safety Classification | Output Formatting

## Context

- Project type: !`grep "^Type:" ./CLAUDE.md 2>/dev/null | head -1`
- Applicable checks: !`grep "^Applicable:" ./CLAUDE.md 2>/dev/null`
- Git status: !`git status --short`

## Context Application

| Field | Effect |
|-------|--------|
| Applicable | Only run checks from context's Applicable list |
| Data | PII/Regulated → security weight ×2, compliance checks mandatory |
| Scale | <100 → relaxed thresholds; 10K+ → strict |
| Priority | Speed → critical only; Quality → all severity levels |
| Maturity | Legacy → warn don't fail; Greenfield → strict enforcement |
| Team | Solo → self-review OK; 6+ → require documented findings |

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Scan | `cco-agent-analyze` | `scan` | Issue detection with metrics |
| Fix | `cco-agent-apply` | `fix` | Execute approved fixes |

**Scan Phase:** Use `cco-agent-analyze` with `scope: scan` to detect security issues, tech debt, test gaps, and self-compliance violations with file:line locations.

## Default Behavior

When called without flags, ask (follow CCO "Question Formatting" standard):

| Question | Options (small → large) |
|----------|-------------------------|
| Scope? | Quick, Smart, Full |
| Auto-fix? | No, Yes |

**`[recommended]` placement:** Scope → Smart, Auto-fix → Yes

Explicit flags skip questions.

## Categories

### Security (`--security`)

Detect and fix security vulnerabilities:

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| OWASP vulnerabilities | Pattern matching, taint analysis | Suggest secure alternatives |
| Secrets detection | Regex patterns, entropy analysis | Remove + add to .gitignore |
| CVE/dependency vulnerabilities | Dependency scan | Upgrade commands |
| Supply-chain risks | Lock file analysis, typosquatting | Pin versions |
| Input validation gaps | Entry point analysis | Add validation boilerplate |

Report: `[SECURITY] {severity}: {issue} in {file:line}`

**Sub-categories (when --security used alone):**
Ask (multiSelect): All | OWASP | Secrets | CVEs | Supply-Chain | Input-Validation

### Tech Debt (`--tech-debt`)

Detect and fix technical debt:

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| Dead code | Unreachable code analysis | Remove with confirmation |
| Complexity | Cyclomatic complexity >10 | Suggest refactor + generate issue |
| TODO/FIXME tracking | Comment scanning | Prioritize + create issues |
| Hardcoded values | Magic number/string detection | Extract to constants/config |
| Type coverage gaps | Missing type annotations | Generate type stubs |

Report: `[TECH-DEBT] {severity}: {issue} in {file:line}`

**Sub-categories (when --tech-debt used alone):**
Ask (multiSelect): All | Dead-Code | Complexity | TODOs | Hardcoded | Types

### Consistency (`--consistency`)

Detect and fix doc-code mismatches:

| Category | Check | Resolution |
|----------|-------|------------|
| Feature Claims | README says "supports X" but not implemented | Update docs or implement |
| API Signatures | Docstring params ≠ actual function | Sync docstring |
| Config Values | Documented default ≠ actual default | Sync config docs |
| Behavior | Comment says X, code does Y | Update comment |
| Examples | README code uses deprecated API | Update examples |
| Dependencies | Documented version ≠ actual | Sync versions |

Report: `[CONSISTENCY] {category}: {doc} ≠ {code} in {file:line}`

**SSOT Resolution:** For each mismatch, ask: "Docs" (update code) | "Code" (update docs) | "Discuss"

### Self-Compliance (`--self-compliance`)

Check code against project's own stated standards:

| Source | Checks |
|--------|--------|
| README.md | Feature claims, installation steps, examples |
| CLAUDE.md | CCO standards, guidelines, conventions |
| CONTRIBUTING.md | Contribution guidelines, code style |
| Custom standards | Project-specific rules |

Report: `[SELF-COMPLIANCE] {standard} violated in {file:line}`

### Tests (`--tests`)

Analyze test quality and coverage:

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| Coverage gaps | Uncovered functions/branches | Generate test stubs (→ generate --tests) |
| Flaky tests | Inconsistent pass/fail patterns | Flag for review |
| Test quality | Assert count, mock usage | Suggest improvements |
| Missing edge cases | Boundary analysis | Generate edge case tests |
| Test isolation | Shared state detection | Suggest refactor |

Report: `[TESTS] {severity}: {issue} in {file:line}`

### Stack-Dependent Categories

Auto-skip if not applicable:

| Flag | When Applicable | Checks |
|------|-----------------|--------|
| `--database` | DB detected | SQL injection, N+1, migrations |
| `--performance` | Scale > Small | Bottlenecks, memory leaks |
| `--docs` | Always | Completeness, freshness |
| `--cicd` | CI/CD detected | Pipeline quality, secrets in CI |
| `--containers` | Docker detected | Image security, best practices |
| `--compliance` | Compliance set | Framework-specific checks |
| `--api-contract` | API detected | Breaking changes, versioning |

## Meta-flags

| Flag | Includes |
|------|----------|
| `--smart` | Auto-detect applicable + self-compliance + consistency |
| `--critical` | security + tests + database |
| `--weekly` | security + tech-debt + tests + self-compliance |
| `--pre-release` | security + tests + consistency + self-compliance + api-contract |
| `--all` | Everything applicable |
| `--auto-fix` | Auto-fix safe issues without asking |

## Output

### Summary Table
```
┌─ AUDIT SUMMARY ──────────────────────────────────────────────┐
│ Category      │ Score │ Issues │ Auto-fixable │ Status      │
├───────────────┼───────┼────────┼──────────────┼─────────────┤
│ Security      │ 92%   │ 2      │ 1            │ WARN        │
│ Tech-Debt     │ 85%   │ 5      │ 4            │ WARN        │
│ Consistency   │ 95%   │ 1      │ 0            │ WARN        │
│ Tests         │ 88%   │ 3      │ 2            │ WARN        │
├───────────────┼───────┼────────┼──────────────┼─────────────┤
│ OVERALL       │ 90%   │ 11     │ 7            │ WARN        │
└───────────────┴───────┴────────┴──────────────┴─────────────┘
```

### Issues Table
```
┌─ ISSUES FOUND ───────────────────────────────────────────────┐
│ Priority │ Type       │ Issue              │ Location       │
├──────────┼────────────┼────────────────────┼────────────────┤
│ CRITICAL │ Security   │ Hardcoded secret   │ config.py:42   │
│ HIGH     │ Security   │ SQL injection risk │ api.py:15      │
│ HIGH     │ Tech-Debt  │ Complexity: 15     │ utils.py:88    │
│ MEDIUM   │ Consistency│ Doc mismatch       │ README.md:35   │
│ LOW      │ Tech-Debt  │ Missing types      │ auth.py:20     │
└──────────┴────────────┴────────────────────┴────────────────┘
```

### Verification
```
Applied: 7 | Skipped: 2 | Failed: 0 | Manual: 2 | Total: 11
```

## Usage

```bash
/cco-audit                   # Interactive
/cco-audit --smart           # Auto-detect applicable
/cco-audit --pre-release     # Production readiness check
/cco-audit --security        # Security focus
/cco-audit --tech-debt       # Tech debt focus
/cco-audit --critical --auto-fix
```

## Related Commands

- `/cco-optimize` - For orphans, stale-refs, duplicates (code cleanliness)
- `/cco-health` - For metrics dashboard
- `/cco-release` - For full pre-release workflow
