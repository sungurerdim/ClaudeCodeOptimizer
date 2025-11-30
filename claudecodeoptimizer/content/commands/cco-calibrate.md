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
  Commands: {count}/9
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

**Auto-Detected (no user input needed):**
- monorepo, preCommitHooks, currentCoverage, lintingConfigured
- apiEndpoints, containerSetup, i18nSetup, authPatterns
- licenseType, secretsDetected, depsOutdated, gitDefaultBranch
- hasReadme, hasChangelog, deadCodeRisk

## Step 4: Confirm Values

Present ALL detected values for user confirmation. Use multiple AskUserQuestion calls (max 4 questions each).

**Call 1 - Core Context:**
```
Q1 - header: "Purpose"
question: "What is the project's purpose?"
options: Show detected + 2-3 alternatives (pre-select detected)

Q2 - header: "Team"
question: "Team size?"
options: Solo | 2-5 | 6+ (pre-select detected)

Q3 - header: "Scale"
question: "Expected user scale?"
options: <100 | 100-10K | 10K+ (pre-select detected)

Q4 - header: "Data"
question: "Most sensitive data handled?"
options: Public | Internal | PII | Regulated (pre-select detected)
```

**Call 2 - Technical Context:**
```
Q5 - header: "Stack"
question: "Tech stack correct?"
options: Show detected stack + "Edit" option (pre-select detected)

Q6 - header: "Type"
question: "Project type?"
options: backend-api | frontend | fullstack | cli | library | mobile | desktop (pre-select detected)

Q7 - header: "Database"
question: "Database type?"
options: None | SQL | NoSQL (pre-select detected)

Q8 - header: "Rollback"
question: "Rollback complexity?"
options: Git | DB | User-data (pre-select detected)
```

**Call 3 - Project Approach:**
```
Q9 - header: "Maturity"
question: "Project maturity phase?"
options:
  - Greenfield: New project, aggressive changes OK
  - Active: Growing project, balanced approach
  - Maintenance: Stable, minimize changes
  - Legacy: Old codebase, wrap don't modify

Q10 - header: "Breaking"
question: "Breaking changes tolerance?"
options:
  - Allowed: Can rename, restructure freely
  - Minimize: Deprecate first, provide migration
  - Never: Full backward compatibility required

Q11 - header: "Priority"
question: "Quality vs speed priority?"
options:
  - Speed: Ship fast, iterate, fix later OK
  - Balanced: Standard practices, reasonable coverage
  - Quality: Thorough review, high coverage, no shortcuts
```

**Call 4 - Compliance (skip if Data=Public):**
```
Q12 - header: "Compliance"
question: "Compliance requirements?"
multiSelect: true
options: None | GDPR | SOC2 | HIPAA | PCI-DSS (pre-select detected)
```

**Important:** All fields must be confirmed. Detected values are defaults, not auto-accepted.

## Step 5: Generate Guidelines

Based on confirmed values:

| If Value | Add Guideline |
|----------|---------------|
| Team: solo | Self-review sufficient |
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
| Maturity: greenfield | Aggressive refactors OK, establish patterns early |
| Maturity: active | Balanced refactors, maintain momentum |
| Maturity: maintenance | Conservative changes, stability over improvement |
| Maturity: legacy | Wrap don't modify, strangler pattern preferred |
| Breaking: allowed | Clean API over compatibility, rename freely |
| Breaking: minimize | Deprecate first, provide migration path |
| Breaking: never | Adapters required, never break existing consumers |
| Priority: speed | MVP mindset, ship fast, iterate |
| Priority: balanced | Standard practices, reasonable coverage |
| Priority: quality | Thorough review, high coverage, no shortcuts |

## Step 6: Store Context

Insert or replace context block in project root `CLAUDE.md`:

**Path:** `{project_root}/CLAUDE.md` (NOT `.claude/CLAUDE.md`)

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: {rollback}
Maturity: {maturity} | Breaking: {breaking} | Priority: {priority}

## Guidelines
- {generated guideline 1}
- {generated guideline 2}
...

## Operational
Tools: {format}, {lint}, {test}
Conventions: {testNaming}, {importStyle}
Applicable: {applicable checks list}
Not Applicable: {not applicable checks list}

## Auto-Detected
Structure: {monorepo|single-repo} | Hooks: {pre-commit|none} | Coverage: {N%|unknown}
- [x] Linting configured
- [x] Pre-commit hooks
- [ ] API endpoints
- [ ] Container setup
- [ ] i18n setup
License: {MIT|Apache-2.0|GPL|unknown}
Secrets detected: {yes|no}
Outdated deps: {N|unknown}
<!-- CCO_CONTEXT_END -->
```

## Step 7: Display Status

Show complete status:

```
CCO Status: OK
Location: ~/.claude/
Commands: 9 | Agents: 3 | Standards: inline

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
