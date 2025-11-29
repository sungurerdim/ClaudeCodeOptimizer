---
name: cco-calibrate
description: Calibrate AI recommendations to project context
---

# /cco-calibrate

**Project calibration** - Auto-detect + confirm project context for calibrated AI recommendations.

All context-aware commands (review, audit, optimize, refactor) run this first.

## Step 1: Check Existing Context

```bash
grep -A20 "CCO_CONTEXT_START" ./CLAUDE.md 2>/dev/null
```

If context exists, **first display it clearly to the user**, then ask for confirmation:

**Display format:**

```
### Current Project Context

| Field | Value |
|-------|-------|
| Purpose | {purpose from context} |
| Team | {team} |
| Scale | {scale} |
| Data | {data} |
| Compliance | {compliance} |
| Stack | {stack} |
| Type | {type} |
| Database | {db} |
| Rollback | {rollback} |

**Guidelines:**
- {guideline 1}
- {guideline 2}
...

**Tools:** {tools}
**Applicable:** {applicable checks}
```

Then ask:

```
AskUserQuestion:
header: "Context"
question: "Use this context or update it?"
options:
  - label: "Use as-is"
    description: "Continue with current context shown above"
  - label: "Update"
    description: "Re-detect and confirm all values"
```

If "Use as-is" → skip to Step 7 (context already complete).
If "Update" → continue to Step 2 (full re-detection).

## Step 2: Run Detection

Run `cco-agent-detect` with `scope: full` to get complete project analysis:

**Technical:**
- Stack (languages, frameworks, databases, infrastructure, cicd, testing)
- Tools (format, lint, test)
- Conventions (testNaming, importStyle)
- Applicable checks list

**Strategic:**
- Purpose, Team, Scale, Data, Type, Rollback

All detection logic lives in the detect agent. Calibrate command only processes results.

## Step 3: Confirm All Values

Present detected values for user confirmation. Show detect agent results as defaults.

```
AskUserQuestion (single call, all questions):

Q1 - header: "Purpose"
question: "What is the project's purpose?"
(Show detected value, allow edit)

Q2 - header: "Team"
question: "Team size?"
options: Solo | 2-5 | 6+ (pre-select detected)

Q3 - header: "Scale"
question: "Expected user scale?"
options: <100 | 100-10K | 10K+ (pre-select detected)

Q4 - header: "Data"
question: "Most sensitive data handled?"
options: Public | Internal | PII | Regulated (pre-select detected)

Q5 - header: "Compliance" (skip if Data=Public)
question: "Compliance requirements?"
multiSelect: true
options: None | GDPR | SOC2 | HIPAA | PCI-DSS

Q6 - header: "Stack"
question: "Tech stack?"
(Show detected, allow correction)

Q7 - header: "Type"
question: "Project type?"
options: backend-api | frontend | fullstack | cli | library | mobile | desktop

Q8 - header: "Database"
question: "Database type?"
options: None | SQL | NoSQL (pre-select detected)

Q9 - header: "Rollback"
question: "Rollback complexity?"
options: Git | DB | User-data (pre-select detected)
```

Detection logic is in `cco-agent-detect`. This step only confirms.

## Step 4: Generate Guidelines

Based on confirmed values, generate strategic guidelines:

| If Value | Add Guideline |
|----------|---------------|
| Team: solo | Self-review sufficient, aggressive refactors OK |
| Team: 2-5 | Informal review recommended, document key decisions |
| Team: 6+ | Formal review required, consider change impact on others |
| Scale: <100 | Simple solutions preferred, optimize for clarity |
| Scale: 100-10K | Add monitoring, consider caching |
| Scale: 10K+ | Performance critical, load test changes |
| Data: public | Basic input validation sufficient |
| Data: internal | Add authentication, audit logs |
| Data: pii | Encryption required, minimize data retention |
| Data: regulated | Full compliance controls, external audit trail |
| Compliance: gdpr | Data deletion capability, consent tracking |
| Compliance: hipaa | PHI encryption, access logging |
| Compliance: pci-dss | No card data in logs, secure key management |
| Type: library | API stability critical, semantic versioning |
| Type: cli | Clear error messages, help documentation |
| DB: sql | Plan migrations, backward compatible changes |
| DB: nosql | Schema versioning, data migration strategy |
| Rollback: db | Test rollback scripts, staged deployments |
| Rollback: user-data | Backup before changes, soft deletes preferred |

## Step 5: Store in Project Root CLAUDE.md

Insert or replace context block in project root `CLAUDE.md`:

**Path:** `{project_root}/CLAUDE.md` (e.g., `/home/user/myproject/CLAUDE.md`)

**CRITICAL - Correct vs Wrong paths:**
- ✅ CORRECT: `./CLAUDE.md` or `CLAUDE.md` (project root)
- ❌ WRONG: `./.claude/CLAUDE.md` or `.claude/CLAUDE.md`
- ❌ WRONG: `~/.claude/CLAUDE.md` (global, not project-specific)

The `.claude/` directory is for Claude Code settings (statusline.js, settings.json), NOT for CLAUDE.md.

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: {rollback}

## Guidelines
- {generated guideline 1}
- {generated guideline 2}
...

## Operational (from detect agent)
Tools: {format}, {lint}, {test}
Conventions: {testNaming}, {importStyle}
Applicable: {applicable checks list}
Not Applicable: {not applicable checks list}
<!-- CCO_CONTEXT_END -->
```

**IMPORTANT:** Store ONLY the template above. Do NOT add:
- Development instructions (belongs in README)
- Setup commands (belongs in README)
- Any sections outside the template

If block exists → replace. If not → append after first heading.

## Step 6: Offer Documentation Updates

If gaps were found in project docs:

**Follow CCO Approval Flow standard from cco-standards.**

Apply to: documentation updates based on detected gaps.

## Step 7: Proceed

Context is now available in project root `CLAUDE.md`. Commands read and apply it.

---

## Context Usage in Commands

All commands MUST:

1. Read `<!-- CCO_CONTEXT_START -->` block from project root `CLAUDE.md` (NOT `.claude/CLAUDE.md`)
2. Follow the Guidelines listed in context
3. Reference context when making recommendations

### Recommendation Format

```
[Recommendation]
↳ Guideline: {relevant guideline from context}
```

### Anti-patterns

- ❌ Ignoring context Guidelines
- ❌ Applying universal "best practices"
- ❌ Treating documented architecture as "correct"

**Principle:** Guidelines in context define the rules. Commands follow them.
