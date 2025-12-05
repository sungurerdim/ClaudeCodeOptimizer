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

**Stack-dependent (auto-skip if N/A):**
`--tests` `--database` `--performance` `--docs` `--cicd` `--containers` `--compliance` `--api-contract`

**Sub-category selection (only when single flag used):**
- `--security` → ask (multiSelect): All | OWASP | Secrets | CVEs | Supply-Chain
- `--tech-debt` → ask (multiSelect): All | Dead-Code | Complexity | Duplication

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

## Meta-flags

| Flag | Includes |
|------|----------|
| `--smart` | Auto-detect applicable + self-compliance + consistency |
| `--critical` | security + tests + database |
| `--weekly` | security + tech-debt + tests + self-compliance |
| `--pre-release` | security + tests + docs + api-contract + consistency (production readiness) |
| `--all` | Everything applicable |
| `--auto-fix` | Auto-fix safe issues without asking |

## Output

Tables per Output Formatting standard:
1. **Audit Results** - Category | Score | Summary
2. **Issues Found** - Priority | Issue | Location | Status
3. **Verification** - Applied: N | Skipped: N | Failed: N | Total: N

## Usage

```bash
/cco-audit                   # Interactive
/cco-audit --smart           # Auto-detect applicable
/cco-audit --pre-release     # Production readiness check
/cco-audit --critical --auto-fix
```
