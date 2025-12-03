---
name: cco-audit
description: Standardized quality gates with prioritized fixes
---

# /cco-audit

**Quality gates** - Read context → run checks → prioritize → fix.

**Standards:** Pre-Operation Safety | Context Read | Fix Workflow | Priority & Approval | Safety Classification | UX/DX

## Context Application

| Field | Effect |
|-------|--------|
| Applicable | Only run checks from context's Applicable list |
| Data | PII/Regulated → security weight ×2, compliance checks mandatory |
| Scale | <100 → relaxed thresholds; 10K+ → strict, add performance checks |
| Priority | Speed → critical only; Quality → all severity levels |
| Maturity | Legacy → warn don't fail; Greenfield → strict enforcement |
| Team | Solo → self-review OK; 6+ → require documented findings |
| Compliance | If set → add compliance category, check against specific framework |

## Default Behavior

When called without flags, ask:
1. **Scope**: Quick | Smart [recommended] | Full
2. **Auto-fix**: Yes [recommended] | No

Explicit flags skip questions.

## Flow

0. **Context Check** - Run `/cco-tune --status`; handle completion/restart per cco-tune flow
1. **Read Context** - Read `./CLAUDE.md`, extract CCO_CONTEXT markers only, parse values
2. **Extract Standards** - Parse project docs for stated standards
3. **Scan** - Run checks including self-compliance
4. **Detection Report** - Per Detection Report standard
5. **Approval** - AskUserQuestion referencing report IDs
6. **Fix** - Execute approved fixes
7. **Verify** - Confirm all changes, show verification table

## Categories

**Core (always):**
- `--security` - OWASP, secrets, CVEs, AI security (prompt injection), supply-chain (dependencies)
- `--tech-debt` - Dead code, complexity, duplication, orphans, TODOs, hardcoded values, AI code patterns (hallucinations, over-engineering, generic solutions)
- `--self-compliance` - Check against project's own standards
- `--consistency` - Doc-code mismatch detection

**Stack-dependent (auto-skip if N/A):**
`--tests` `--database` `--performance` `--docs` `--cicd` `--containers` `--compliance` `--api-contract`

**Sub-category selection (only when single flag used):**
- `--security` → ask (multiSelect): All | OWASP | Secrets | CVEs | AI-Security | Supply-Chain
- `--tech-debt` → ask (multiSelect): All | Dead-Code | Complexity | Duplication | AI-Patterns

Note: Full/Smart/All modes include all sub-categories automatically (no sub-questions).

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
| `--critical` | security + database + tests |
| `--weekly` | security + tech-debt + tests + self-compliance + consistency |
| `--pre-release` | security + api-contract + docs + tests + consistency |
| `--all` | Everything applicable |
| `--auto-fix` | Skip asking, auto-fix safe issues |

## Output

**Standards:** Output Formatting

Tables:
1. **Audit Results** - Category | Score | Summary
2. **Issues Found** - Priority | Issue | Location | Status
3. **Verification** - {done} + {skip} + {fail} = {total}

## Usage

```bash
/cco-audit                   # Interactive
/cco-audit --smart           # Auto-detect applicable
/cco-audit --consistency     # Doc-code mismatch
/cco-audit --critical --auto-fix
```
