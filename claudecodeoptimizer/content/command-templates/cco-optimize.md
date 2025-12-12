---
name: cco-optimize
description: Security and code quality analysis with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(wc:*), Bash(grep:*), Bash(find:*), Task(*), TodoWrite
---

# /cco-optimize

**Full-Stack Optimization** - Security + Quality + Hygiene in one command.

End-to-end: Detects security vulnerabilities, code quality issues, and hygiene problems AND fixes them.

**Rules:** User Input | Safety | Classification | Priority Assignment | Conservative Judgment | Skip Criteria | Task Tracking

## Context

- Context check: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Git status: !`git status --short`
- File count: !`find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" \) 2>/dev/null | wc -l`

**Static context (Applicable, Type, Scale, Data, Maturity, Breaking) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO context in ./.claude/rules/cco/context.md.**

If context check returns "0":
```
CCO context not found.

Run /cco-config first to configure project context, then restart CLI.
```
**Stop execution immediately.**

## Context Application

| Field | Effect |
|-------|--------|
| Applicable | Only these categories can run, others rejected |
| Data | PII/Regulated → security weight ×2 |
| Scale | <1K → relaxed thresholds; 10K+ → strict, smaller batches |
| Priority | Speed → critical only; Quality → all severity levels |
| Maturity | Legacy → warn don't fail, safe only; Greenfield → aggressive OK |
| Breaking | Never → preserve all interfaces; Allowed → simplify APIs |
| Type | CLI: startup time; API: response time; Library: bundle size |

## Execution Optimization

<use_parallel_tool_calls>
When calling multiple tools with no dependencies between them, make all independent
calls in a single message. For example:
- Multiple cco-agent-analyze scopes → launch simultaneously
- Multiple file reads → batch in parallel
- Multiple grep searches → parallel calls

Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>

## Default Behavior: 2-Tab Selection

When called without flags, use AskUserQuestion with 2 tabs:

**Tab 1: Scope**

| Question | Options | MultiSelect |
|----------|---------|-------------|
| What to check? | Security; Quality; Hygiene; All (Recommended) | true |

**Tab 2: Action**

| Question | Options | MultiSelect |
|----------|---------|-------------|
| How to handle findings? | Report Only; Auto-fix (Recommended); Full Auto-fix; Interactive | false |

**Option Descriptions:**

| Scope Option | Includes |
|--------------|----------|
| **Security** | OWASP vulnerabilities, secrets, CVEs, supply-chain, input validation |
| **Quality** | Complexity, type coverage, test quality, consistency, self-compliance |
| **Hygiene** | Orphans, stale-refs, duplicates, dead code, redundancy |
| **All** | Security + Quality + Hygiene (recommended) |

| Action Option | Behavior |
|---------------|----------|
| **Report Only** | Scan and report, no changes |
| **Auto-fix** | Fix safe issues automatically, ask for risky |
| **Full Auto-fix** | Fix all with confirmation for each risky issue |
| **Interactive** | Ask for every issue individually |

**Explicit flags skip questions.**

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Security Scan | `cco-agent-analyze` | `security` | Vulnerability detection |
| Quality Scan | `cco-agent-analyze` | `quality` | Tech debt, consistency |
| Hygiene Scan | `cco-agent-analyze` | `hygiene` | Orphans, duplicates |
| Fix | `cco-agent-apply` | `fix` | Execute approved fixes |
| Deps | `cco-agent-research` | `dependency` | Version analysis, CVEs |

### Parallel Scan Pattern [REQUIRED]

Launch parallel agents in a single message:

```
Launch simultaneously:
- Agent 1: cco-agent-analyze scope=security
- Agent 2: cco-agent-analyze scope=quality
- Agent 3: cco-agent-analyze scope=hygiene
```

---

# SECURITY SCOPE

## Security Categories (`--security`)

### OWASP Vulnerabilities

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| SQL Injection (CWE-89) | Pattern matching, taint analysis | Parameterized queries |
| XSS (CWE-79) | Output encoding analysis | Escape functions |
| Command Injection (CWE-78) | Shell call analysis | Safe subprocess calls |
| Path Traversal (CWE-22) | File path analysis | Path validation |
| SSRF (CWE-918) | URL construction analysis | Allowlist validation |

### Secrets Detection

| Pattern | Examples | Auto-fix |
|---------|----------|----------|
| API keys | `sk-`, `api_key=`, `apiKey:` | Remove + .gitignore |
| Tokens | `ghp_`, `gho_`, `Bearer ` | Environment variable |
| Passwords | `password=`, `passwd:`, `secret=` | Vault reference |
| Private keys | `-----BEGIN.*PRIVATE KEY-----` | Remove + warn |
| Connection strings | `mongodb://`, `postgres://` | Environment variable |

### CVE/Dependency Vulnerabilities

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| Known CVEs | Dependency scan against NVD | Upgrade commands |
| Supply-chain risks | Lock file analysis, typosquatting | Pin versions |
| Outdated with vulns | Version comparison | Update manifest |

### Input Validation Gaps

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| Entry points | Route/handler analysis | Add validation schema |
| Missing sanitization | Taint tracking | Add sanitize wrapper |
| Type coercion | Dynamic type analysis | Add type checks |

Report: `[SECURITY] {severity}: {issue} in {file:line}`

---

# QUALITY SCOPE

## Quality Categories (`--quality`)

### Tech Debt (`--tech-debt`)

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| Dead code | Unreachable code analysis | Remove with confirmation |
| Complexity | Cyclomatic complexity >10 | Suggest refactor |
| TODO/FIXME | Comment scanning | Create tracking issues |
| Hardcoded values | Magic number detection | Extract to constants |
| Type coverage | Missing annotations | Generate type stubs |

Report: `[TECH-DEBT] {severity}: {issue} in {file:line}`

### Consistency (`--consistency`)

| Category | Check | Resolution |
|----------|-------|------------|
| Feature Claims | README says X, not implemented | Update docs or implement |
| API Signatures | Docstring ≠ function | Sync docstring |
| Config Values | Documented ≠ actual | Sync config docs |
| Behavior | Comment says X, code does Y | Update comment |
| Examples | Deprecated API in docs | Update examples |

Report: `[CONSISTENCY] {category}: {doc} ≠ {code} in {file:line}`

### Self-Compliance (`--self-compliance`)

Check code against project's own stated rules:

| Source | Checks |
|--------|--------|
| README.md | Feature claims, examples |
| CLAUDE.md | CCO rules, conventions |
| CONTRIBUTING.md | Code style, guidelines |

Report: `[SELF-COMPLIANCE] {rule} violated in {file:line}`

### Tests (`--tests`)

| Check | Detection | Auto-fix |
|-------|-----------|----------|
| Coverage gaps | Uncovered functions | Generate test stubs |
| Flaky tests | Inconsistent results | Flag for review |
| Test quality | Assert count, mocks | Suggest improvements |
| Missing edge cases | Boundary analysis | Generate edge tests |

Report: `[TESTS] {severity}: {issue} in {file:line}`

---

# HYGIENE SCOPE

## Hygiene Categories (`--hygiene`)

### Orphans (`--orphans`)

| Type | Detection | Action |
|------|-----------|--------|
| Orphan file | No imports pointing to it | Delete with confirmation |
| Orphan function | Defined but never called | Delete or flag |
| Orphan export | Exported but never imported | Remove export |
| Orphan import | Imported but never used | Remove import |
| Orphan config | Config key not referenced | Remove or flag |

Report: `[ORPHAN] {type}: {name} in {file:line} (last modified: {date})`

### Stale References (`--stale-refs`)

| Type | Detection | Action |
|------|-----------|--------|
| Broken import | Import path doesn't exist | Remove or fix path |
| Dead link | URL returns 404 | Update or remove |
| Missing ref | Code references undefined | Fix or remove |
| Obsolete comment | References deleted code | Update comment |
| Phantom test | Test for non-existent function | Remove test |

Report: `[STALE-REF] {type}: {reference} → {missing_target} in {file:line}`

### Duplicates (`--duplicates`)

| Type | Similarity | Action |
|------|------------|--------|
| Exact duplicate | 100% | Consolidate → single source |
| Near-duplicate | >80% | Review → merge or justify |
| Semantic duplicate | Same logic | Extract shared abstraction |

Report: `[DUPLICATE] {type} ({similarity}%): {file1}:{line} ↔ {file2}:{line}`

### Dependencies (`--deps`)

Analyze dependency freshness and suggest safe updates.

**No auto-fix for dependencies. Every update requires explicit approval.**

| Type | SemVer | Risk | Action |
|------|--------|------|--------|
| Patch | `x.y.Z+n` | 🟢 Safe | Review |
| Minor | `x.Y+n.z` | 🟡 Low | Review |
| Major | `X+n.y.z` | 🔴 Breaking | Review + changelog |
| CVE | Security fix | 🔴 Critical | Urgent review |

Report: `[DEP] {risk}: {package} {current} → {latest} in {manifest}`

---

# RIGOR & VERIFICATION

## Audit Rigor [CRITICAL]

### Read-First Rule

**NEVER report an issue without reading the actual code.** Grep matches alone are insufficient.

### Context Verification

Before flagging:
1. Is this intentional? Check surrounding comments
2. Is there a `# noqa`, `// eslint-disable`, `cco-ignore`?
3. Does commit history explain the choice?

### Confidence Thresholds

| Severity | Min Confidence | Evidence Required |
|----------|---------------|-------------------|
| CRITICAL | 95% | Verified in code + reproducible |
| HIGH | 85% | Strong evidence, multiple indicators |
| MEDIUM | 70% | Probable issue, single indicator |
| LOW | 50% | Possible issue, style concern |

**False Positive Guard:** When uncertain, choose LOWER severity.

## Finding Correlation & Deduplication [CRITICAL]

### Root Cause Analysis

Group findings by root cause:

| Symptom Type | Root Cause | Dedup Action |
|--------------|------------|--------------|
| SQL injection in 5 endpoints | Missing input sanitization | 1 root cause + 5 locations |
| XSS in 3 templates | No output encoding | 1 root cause + 3 locations |

### Deduplication Rules

1. **Same CWE + Same File** → Merge into single finding
2. **Same CWE + Related Files** → Group under root cause
3. **Different CWE + Same Location** → Keep separate

**Benefit:** N findings → 1 actionable root cause

## False Positive Reduction [CRITICAL]

### Pre-Report Verification

| FP Indicator | Check | Action |
|--------------|-------|--------|
| Sanitization present | Is input sanitized upstream? | Skip if yes |
| Framework protection | Does framework auto-escape? | Skip if yes |
| Test/Mock code | Is this in test fixtures? | Skip if yes |
| Dead code path | Is this code reachable? | Skip if unreachable |
| Intentional pattern | Is there a security comment? | Skip if explained |

**Report FP Stats:** `Confirmed: {N} / Reported: {M} ({%} accuracy)`

## Business Impact Prioritization [OWASP Risk Rating]

### Risk Calculation

**Risk = Likelihood × Impact**

| Factor | Weight | Scoring |
|--------|--------|---------|
| Exploitability | 25% | Easy: 100, Medium: 60, Hard: 20 |
| Attack Surface | 25% | Public: 100, Authenticated: 60, Internal: 20 |
| Data Sensitivity | 25% | PII/Financial: 100, Internal: 50, Public: 10 |
| Business Criticality | 25% | Core: 100, Supporting: 50, Non-critical: 20 |

### Priority Levels

| Risk Score | Priority | SLA |
|------------|----------|-----|
| 90-100 | 🔴 P0 - Immediate | Fix within 24h |
| 70-89 | 🟠 P1 - Critical | Fix within 1 week |
| 50-69 | 🟡 P2 - High | Fix within 1 month |
| 30-49 | 🟢 P3 - Medium | Fix in next release |
| <30 | ⚪ P4 - Low | Backlog |

## Safe Removal Pattern [CRITICAL]

### Multi-Pattern Search

Before marking ANYTHING as orphan/removable, search ALL reference types:

| Pattern Type | Search Method |
|-------------|---------------|
| Direct imports | `import X`, `from X import`, `require('X')` |
| String references | `"module_name"`, `'function_name'` |
| Dynamic imports | `importlib.import_module`, `__import__` |
| Config references | JSON/YAML files, env vars |
| Test references | Test files, fixtures, mocks |
| Doc references | README, docstrings, comments |

### Confidence Gate

| Confidence | Action |
|------------|--------|
| 100% (zero refs) | Safe to suggest removal |
| 95-99% | Warn user, show what WAS found |
| <95% | Do NOT suggest removal |

**When in doubt, do NOT suggest removal.**

## Impact Analysis & Cascading Effects [CRITICAL]

### Dependency Chain Mapping

```
Target: utils/helpers.py::format_date()

Direct Dependents (Tier 1):
├─ api/users.py (import format_date)
├─ api/orders.py (import format_date)
└─ services/notification.py (import format_date)

Indirect Dependents (Tier 2):
├─ api/users.py → routes/user_routes.py
└─ services/notification.py → workers/email_worker.py

Impact Scope: 6 files | 3 modules | 2 entry points
```

### Impact Classification

| Dependents | Impact | Action |
|------------|--------|--------|
| 0 | 🟢 Safe | Auto-remove OK |
| 1-3 | 🟡 Low | Show impact, ask confirmation |
| 4-10 | 🟠 Medium | Detailed impact report |
| 10+ | 🔴 High | Manual review mandatory |

## Regression Risk Assessment [CRITICAL]

### Risk Score Calculation

```
Risk Score = (Impact × Probability) - Coverage Mitigation

Impact: dependents × criticality (0-100)
Probability: recently_used ? 0.8 : 0.2
Coverage Mitigation: has_tests ? 30 : 0
```

### Decision Matrix

| Risk Score | Test Coverage | Action |
|------------|---------------|--------|
| LOW (<30) | Any | ✅ Auto-remove |
| MEDIUM (30-60) | HIGH | ⚠️ Ask confirmation |
| MEDIUM (30-60) | LOW | ⚠️ Add test first |
| HIGH (>60) | HIGH | ⚠️ Manual review |
| HIGH (>60) | LOW | ❌ Do not remove |

## Remediation Verification [CRITICAL]

### Post-Fix Verification Loop

After applying ANY fix:

1. **Re-scan** - Same vulnerability still detected?
2. **Regression check** - Did fix introduce new issues?
3. **Completeness** - All instances of root cause fixed?

### Verification Report

```
┌─ REMEDIATION VERIFICATION ────────────────────────────────────┐
│ Finding: {finding_type} ({file}:{line})                       │
│ Fix Applied: {fix_description}                                │
├───────────────────────────────────────────────────────────────┤
│ {check_icon} Re-scan: {rescan_result}                         │
│ {check_icon} Regression: {regression_result}                  │
│ {check_icon} Completeness: {completeness_result}              │
│ Status: {verification_status}                                  │
└───────────────────────────────────────────────────────────────┘
```

**Never mark as fixed without verification.**

## Completion Verification [CRITICAL]

### Quality Gates

| Gate | Requirement | Status |
|------|-------------|--------|
| Tests pass | 100% green | Required |
| No new orphans | Re-scan clean | Required |
| No broken imports | Import check clean | Required |
| Metrics improved | Lines/tokens reduced | Expected |
| No regressions | Same functionality | Required |

---

# OUTPUT FORMAT

## Summary Table

```
┌─ OPTIMIZATION SUMMARY ───────────────────────────────────────┐
│ Category      │ Score │ Issues │ Fixed │ Status              │
├───────────────┼───────┼────────┼───────┼─────────────────────┤
│ Security      │ {n}%  │ {n}    │ {n}   │ {status}            │
│ Quality       │ {n}%  │ {n}    │ {n}   │ {status}            │
│ Hygiene       │ {n}%  │ {n}    │ {n}   │ {status}            │
├───────────────┼───────┼────────┼───────┼─────────────────────┤
│ OVERALL       │ {n}%  │ {n}    │ {n}   │ {status}            │
└───────────────┴───────┴────────┴───────┴─────────────────────┘
```

## Issues Table

```
┌─ PRIORITIZED FINDINGS ───────────────────────────────────────┐
│ Priority │ Scope    │ Issue              │ Location          │
├──────────┼──────────┼────────────────────┼───────────────────┤
│ {P}      │ {scope}  │ {issue}            │ {file}:{line}     │
│ {P}      │ {scope}  │ {issue}            │ {file}:{line}     │
│ ...                                                          │
└──────────┴──────────┴────────────────────┴───────────────────┘
```

## Metrics Summary

```
Before: {n} lines | {n} tokens | {n} KB
After:  {n} lines | {n} tokens | {n} KB
Saved:  {n} lines ({n}%) | {n} tokens ({n}%) | {n} KB ({n}%)
```

## Verification Summary

```
Applied: {n} | Skipped: {n} | Failed: {n} | Manual: {n} | Total: {n}
```

---

# FLAGS

## Scope Flags

| Flag | Scope |
|------|-------|
| `--security` | OWASP, secrets, CVEs, supply-chain, input validation |
| `--quality` | Tech-debt, consistency, self-compliance, tests |
| `--hygiene` | Orphans, stale-refs, duplicates, dead code |
| `--all` | All scopes (default when interactive) |

## Sub-Scope Flags

| Flag | Parent | Checks |
|------|--------|--------|
| `--owasp` | security | OWASP Top 10 vulnerabilities |
| `--secrets` | security | Secret detection |
| `--cves` | security | Dependency CVEs |
| `--tech-debt` | quality | Complexity, dead code, TODOs |
| `--consistency` | quality | Doc-code mismatches |
| `--tests` | quality | Coverage, flaky tests |
| `--orphans` | hygiene | Unreferenced code |
| `--stale-refs` | hygiene | Broken references |
| `--duplicates` | hygiene | Duplicate code |
| `--deps` | hygiene | Dependency freshness |

## Action Flags

| Flag | Effect |
|------|--------|
| `--report` | Report only, no fixes |
| `--fix` | Auto-fix safe issues (default when interactive) |
| `--fix-all` | Fix all with confirmation for risky |
| `--interactive` | Ask for each issue |

## Meta Flags

| Flag | Includes |
|------|----------|
| `--critical` | security + tests (pre-commit essentials) |
| `--pre-release` | security + quality + consistency (release gate) |
| `--quick` | hygiene only, auto-fix (fast cleanup) |
| `--deep` | All scopes, thorough analysis |

## Usage

```bash
/cco-optimize                      # Interactive 2-tab selection
/cco-optimize --all --fix          # Full optimization with auto-fix
/cco-optimize --security           # Security focus only
/cco-optimize --quality            # Quality focus only
/cco-optimize --hygiene            # Hygiene focus only (orphans, stale, dupes)
/cco-optimize --quick              # Fast hygiene cleanup
/cco-optimize --pre-release        # Pre-release gate checks
/cco-optimize --deps               # Dependency freshness check
/cco-optimize --all --report       # Full scan, no changes
```

## Related Commands

- `/cco-status` - For metrics dashboard
- `/cco-preflight` - For full pre-release workflow
- `/cco-checkup` - For regular maintenance routine

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Safety

- **Pre-op**: Check git status before any modifications
- **Dirty**: If uncommitted changes → prompt: `Commit; Stash; Continue anyway`
- **Rollback**: Clean git state enables `git checkout` on failure

### Classification

| Type | Examples | Action |
|------|----------|--------|
| Safe | Remove unused imports, fix lint, add types | Auto-apply |
| Risky | Auth changes, API contract, delete files | Require approval |

### Priority Assignment

| Severity | Criteria | Confidence |
|----------|----------|------------|
| CRITICAL | Security breach, data loss | HIGH required |
| HIGH | Broken functionality | HIGH required |
| MEDIUM | Error, incorrect behavior | MEDIUM ok |
| LOW | Style, cosmetic | LOW ok |

### Conservative Judgment [CRITICAL]

- **Lower**: When uncertain between two severities, choose lower
- **Evidence**: Require explicit evidence, not inference
- **No-Escalate**: Style issues → never CRITICAL or HIGH

### Batch Approval

- **MultiSelect**: true for batch approvals
- **All-Option**: First option = "All ({N})" for bulk
- **Priority-Order**: CRITICAL → HIGH → MEDIUM → LOW
- **Item-Format**: `{description} [{file:line}] [{safe|risky}]`

### Skip Criteria

- **Inline**: `// cco-ignore` or `# cco-ignore` skips line
- **File**: `// cco-ignore-file` skips entire file
- **Paths**: fixtures/, testdata/, examples/, benchmarks/

### Task Tracking

- **Create**: TODO list with all items before starting
- **Status**: pending → in_progress → completed
- **Accounting**: done + skip + fail = total
