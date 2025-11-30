---
name: cco-calibrate
description: Calibrate AI recommendations to project context
---

# /cco-calibrate

**Project calibration** - Auto-detect + confirm project context for calibrated AI recommendations.

All context-aware commands (review, audit, optimize, refactor) read context from here.

## Default Behavior

### If Context Exists

Display current context clearly, then ask:

```
header: "Context"
question: "Use this context or update it?"
options:
  - label: "Use as-is"
    description: "Continue with current context shown above"
  - label: "Update"
    description: "Re-detect and confirm all values"
```

If "Use as-is" → display status and exit.
If "Update" → continue to detection flow.

### If No Context

Run full detection → confirm → store → display status.

## Step 1: Installation Check

Verify CCO installation:
- Commands in ~/.claude/commands/cco-*.md
- Agents in ~/.claude/agents/cco-*.md
- Standards in ~/.claude/CLAUDE.md

If issues found, show:
```
CCO Status: WARNING
  Commands: {count}/10
  Agents: {count}/3
  Standards: {OK|MISSING}

→ Run: pip install claudecodeoptimizer && cco-setup
```

## Step 2: Config Health Check

Check both global (~/.claude/) and local (./.claude/) scopes:

**settings.json:**
- JSON syntax valid
- No conflicting rules (same pattern in allow and deny)
- Dangerous commands properly denied

**statusline.js:**
- JavaScript syntax valid (if exists)

If issues found, show:
```
Config Issues:
  ⚠ {scope} settings.json: {issue}
→ Run /cco-config to fix
```

## Step 3: Run Detection

Run `cco-agent-detect` with `scope: full`:

**Technical:**
- Stack (languages, frameworks, databases, infrastructure, cicd, testing)
- Tools (format, lint, test)
- Conventions (testNaming, importStyle)
- Applicable checks list

**Strategic:**
- Purpose, Team, Scale, Data, Type, Rollback

## Step 4: Confirm Values

Present detected values for user confirmation:

```
AskUserQuestion (single call):

Q1 - header: "Purpose"
question: "What is the project's purpose?"
(Show detected value, allow edit)

Q2 - header: "Team"
options: Solo | 2-5 | 6+ (pre-select detected)

Q3 - header: "Scale"
options: <100 | 100-10K | 10K+ (pre-select detected)

Q4 - header: "Data"
options: Public | Internal | PII | Regulated (pre-select detected)
```

Additional questions if needed: Compliance, Stack, Type, Database, Rollback.

## Step 5: Generate Guidelines

Based on confirmed values:

| If Value | Add Guideline |
|----------|---------------|
| Team: solo | Self-review sufficient, aggressive refactors OK |
| Team: 2-5 | Informal review recommended, document key decisions |
| Team: 6+ | Formal review required, consider change impact |
| Scale: <100 | Simple solutions preferred, optimize for clarity |
| Scale: 100-10K | Add monitoring, consider caching |
| Scale: 10K+ | Performance critical, load test changes |
| Data: public | Basic input validation sufficient |
| Data: internal | Add authentication, audit logs |
| Data: pii | Encryption required, minimize retention |
| Data: regulated | Full compliance controls, external audit trail |
| Type: library | API stability critical, semantic versioning |
| Type: cli | Clear error messages, help documentation |
| DB: sql | Plan migrations, backward compatible changes |
| DB: nosql | Schema versioning, data migration strategy |
| Rollback: db | Test rollback scripts, staged deployments |
| Rollback: user-data | Backup before changes, soft deletes preferred |

## Step 6: Store Context

Insert or replace context block in project root `CLAUDE.md`:

**Path:** `{project_root}/CLAUDE.md` (NOT `.claude/CLAUDE.md`)

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

## Operational
Tools: {format}, {lint}, {test}
Conventions: {testNaming}, {importStyle}
Applicable: {applicable checks list}
Not Applicable: {not applicable checks list}
<!-- CCO_CONTEXT_END -->
```

## Step 7: Display Status

Show complete status:

```
CCO Status: OK
Location: ~/.claude/
Commands: 10 | Agents: 3 | Standards: inline

Project Context: OK
  Team: {team} | Scale: {scale} | Type: {type}
  Applicable: {count} checks

Config Health:
  Global settings.json: OK
  Local settings.json: {OK|not configured}

Quick start: /cco-audit --smart
```

## Context Usage

All commands MUST:
1. Read `<!-- CCO_CONTEXT_START -->` block from project root `CLAUDE.md`
2. Follow the Guidelines listed in context
3. Reference context when making recommendations

## Anti-patterns

- Ignoring context Guidelines
- Applying universal "best practices"
- Treating documented architecture as "correct"

**Principle:** Guidelines in context define the rules. Commands follow them.

## Usage

```bash
/cco-calibrate           # Full flow or status display
/cco-calibrate --update  # Force re-detection
```
