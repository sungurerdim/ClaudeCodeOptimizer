---
name: cco-audit
description: Standardized quality gates with prioritized fixes
---

# /cco-audit

**Quality gates** - Scan → prioritize → approve → fix → verify.

**Standards:** Command Flow | Fix Workflow | Approval Flow | Safety Classification | Output Formatting

## Context Application

| Field | Effect |
|-------|--------|
| Applicable | Only run checks from context's Applicable list |
| Data | PII/Regulated → security weight ×2, compliance checks mandatory |
| Scale | <100 → relaxed thresholds; 10K+ → strict |
| Priority | Speed → critical only; Quality → all severity levels |
| Maturity | Legacy → warn don't fail; Greenfield → strict enforcement |
| Team | Solo → self-review OK; 6+ → require documented findings |

## Default Behavior

When called without flags, ask:
1. **Scope**: Quick | Smart [recommended] | Full
2. **Auto-fix**: Yes [recommended] | No

Explicit flags skip questions.

## Categories

**Core (always):**
- `--security` - OWASP, secrets, CVEs, supply-chain (dependencies)
- `--tech-debt` - Dead code, complexity, duplication, orphans, TODOs, hardcoded values
- `--self-compliance` - Check against project's own standards
- `--consistency` - Doc-code mismatch detection
- `--orphans` - Unreferenced files, functions, imports, exports
- `--stale-refs` - References to non-existent code, broken imports

**Stack-dependent (auto-skip if N/A):**
`--tests` `--database` `--performance` `--docs` `--cicd` `--containers` `--compliance` `--api-contract`

**Sub-category selection (only when single flag used):**
- `--security` → ask (multiSelect): All | OWASP | Secrets | CVEs | Supply-Chain
- `--tech-debt` → ask (multiSelect): All | Dead-Code | Complexity | Duplication | Orphans
- `--consistency` → ask (multiSelect): All | Doc-Code | Config | API-Signature | Examples

Note: Full/Smart/All modes include all sub-categories automatically.

## Self-Compliance

Extract from project docs (README, CLAUDE.md, CONTRIBUTING.md): stated standards, goals, constraints.

Check all files. Report: `[SELF-COMPLIANCE] <standard> violated in <file:line>`

## Doc-Code Mismatch

| Category | Check |
|----------|-------|
| Feature Claims | README says "supports X" but not implemented |
| API Signatures | Docstring params ≠ actual function |
| Config Values | Documented default ≠ actual default |
| Behavior | Comment says X, code does Y |
| Examples | README code uses deprecated API |
| Dependencies | Documented version ≠ actual |

Report: `[DOC-CODE MISMATCH] {category}: {doc} ≠ {code} in {file:line}`

**SSOT Resolution:** For each mismatch, ask: "Docs" (update code) | "Code" (update docs) | "Discuss"

## Orphan Detection

Build dependency graph → find unreferenced items:

| Type | Detection Method | Example |
|------|------------------|---------|
| Orphan file | No imports pointing to it | `old_utils.py` never imported |
| Orphan function | Defined but never called | `def legacy_parse():` unused |
| Orphan export | Exported but never imported | `export { unusedHelper }` |
| Orphan import | Imported but never used | `import { never_used }` |
| Orphan config | Config key not referenced | `OLD_API_KEY` in .env |

Report: `[ORPHAN] {type}: {name} in {file:line} (last modified: {date})`

**Resolution:** For each orphan, ask: "Delete" | "Keep (add reference)" | "Skip"

## Stale Reference Detection

Scan all references → verify targets exist:

| Type | Detection | Example |
|------|-----------|---------|
| Broken import | Import path doesn't exist | `from deleted_module import x` |
| Dead link | URL returns 404 | `[docs](http://old.url/gone)` |
| Missing ref | Code references undefined | `config.REMOVED_KEY` |
| Obsolete comment | Comment references deleted code | `// see old_function()` |
| Phantom test | Test for non-existent function | `test_removed_feature()` |

Report: `[STALE-REF] {type}: {reference} → {missing_target} in {file:line}`

## Meta-flags

| Flag | Includes |
|------|----------|
| `--smart` | Auto-detect applicable + self-compliance + consistency + orphans |
| `--critical` | security + tests + database + stale-refs |
| `--weekly` | security + tech-debt + tests + self-compliance + orphans |
| `--pre-release` | security + tests + docs + api-contract + consistency + stale-refs |
| `--hygiene` | orphans + stale-refs + consistency (codebase cleanliness) |
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
│ Orphans       │ 100%  │ 0      │ 0            │ OK          │
│ Stale-Refs    │ 78%   │ 3      │ 2            │ WARN        │
│ Consistency   │ 95%   │ 1      │ 0            │ WARN        │
├───────────────┼───────┼────────┼──────────────┼─────────────┤
│ OVERALL       │ 88%   │ 11     │ 7            │ WARN        │
└───────────────┴───────┴────────┴──────────────┴─────────────┘
```

### Issues Table
```
┌─ ISSUES FOUND ───────────────────────────────────────────────┐
│ Priority │ Type       │ Issue              │ Location       │
├──────────┼────────────┼────────────────────┼────────────────┤
│ CRITICAL │ Security   │ Hardcoded secret   │ config.py:42   │
│ HIGH     │ Stale-Ref  │ Broken import      │ api.py:15      │
│ HIGH     │ Orphan     │ Unused function    │ utils.py:88    │
│ MEDIUM   │ Tech-Debt  │ Code duplication   │ auth.py:20     │
│ LOW      │ Consistency│ Doc mismatch       │ README.md:35   │
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
/cco-audit --hygiene         # Orphans + stale-refs + consistency
/cco-audit --orphans         # Find unreferenced code
/cco-audit --stale-refs      # Find broken references
/cco-audit --critical --auto-fix
```
