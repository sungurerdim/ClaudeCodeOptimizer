---
name: cco-audit
description: Standardized quality gates with prioritized fixes
---

# /cco-audit

**Quality gates** - Read context → run checks → prioritize → fix.

**Standards:** Pre-Operation Safety | Context Read | Fix Workflow | Priority & Approval | Safety Classification | Status Updates | UX/DX

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
- `--tech-debt` - Dead code, complexity, duplication, orphans, TODOs, hardcoded values
- `--ai-patterns` - AI-generated code quality issues (see AI-Patterns Detection below)
- `--self-compliance` - Check against project's own standards
- `--consistency` - Doc-code mismatch detection

**Stack-dependent (auto-skip if N/A):**
`--tests` `--database` `--performance` `--docs` `--cicd` `--containers` `--compliance` `--api-contract`

**Sub-category selection (only when single flag used):**
- `--security` → ask (multiSelect): All | OWASP | Secrets | CVEs | AI-Security | Supply-Chain
- `--tech-debt` → ask (multiSelect): All | Dead-Code | Complexity | Duplication
- `--ai-patterns` → ask (multiSelect): All | Almost-Right | Over-Engineering | Generic-Solutions | Hallucinations

Note: Full/Smart/All modes include all sub-categories automatically (no sub-questions).

## AI-Patterns Detection

Detects common issues in AI-generated code that appears correct but has subtle problems:

| Pattern | Detection | Example |
|---------|-----------|---------|
| **Almost-Right Logic** | Edge cases not handled, off-by-one errors, incorrect operator | `<=` vs `<`, missing null check |
| **Over-Engineering** | Unnecessary abstractions, premature optimization | Factory for single implementation |
| **Generic Solutions** | Copy-paste patterns that don't fit context | Redux for 3-field form |
| **Hallucinated APIs** | Non-existent methods, wrong signatures | `array.flatten()` in wrong language |
| **Incomplete Error Handling** | Happy path only, missing catch blocks | Try without proper catch |
| **Style Inconsistency** | Doesn't match project conventions | camelCase in snake_case project |

Report: `[AI-PATTERN] {type}: {description} in {file:line}`

**Confidence indicator:** Each finding includes confidence level (HIGH/MEDIUM/LOW) based on pattern match strength.

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
