---
name: cco-context
description: Project context for calibrated recommendations
---

# /cco-context

**Project context** - Auto-detect + confirm project context for calibrated AI recommendations.

All context-aware commands (review, audit, optimize, refactor) run this first.

## Step 1: Check Existing Context

```bash
grep -A3 "CCO_CONTEXT_START" .claude/CLAUDE.md 2>/dev/null
```

If context exists, show current values and ask:

```
AskUserQuestion:
header: "Context"
question: "Project context found. What would you like to do?"
options:
  - label: "Use as-is"
    description: "Continue with current context"
  - label: "Update"
    description: "Re-detect and confirm all values"
```

If "Use as-is" → proceed to Step 4.

## Step 2: Auto-Detect

Scan project to detect values:

| Field | Detection Method |
|-------|------------------|
| Purpose | README.md first paragraph, package description |
| Team | `git shortlog -sn` contributor count |
| Scale | README mentions, user docs, analytics config |
| Data | Model fields (email, password, PII patterns) |
| Stack | File extensions, package.json, pyproject.toml, go.mod |
| Type | Entry points, folder structure, framework markers |
| DB | migrations/, prisma/, sqlalchemy, mongoose imports |
| Rollback | Has migrations + user models = user-data, has migrations = db, else git |

## Step 3: Confirm All Values

Present ALL questions with detected values marked. User confirms or corrects.

```
AskUserQuestion (single call, all questions):

Q1 - header: "Purpose"
question: "What is the project's purpose?"
(Show detected value as default, allow edit)

Q2 - header: "Team"
question: "Team size?"
options:
  - label: "Solo" (detected if 1 contributor)
  - label: "2-5" (detected if 2-5 contributors)
  - label: "6+" (detected if 6+ contributors)

Q3 - header: "Scale"
question: "Expected user scale?"
options:
  - label: "<100" - Internal tool, personal use
  - label: "100-10K" - Growing product, startup
  - label: "10K+" - Large scale, public platform

Q4 - header: "Data"
question: "Most sensitive data handled?"
options:
  - label: "Public" - No sensitive data
  - label: "Internal" - Business data, not personal
  - label: "PII" - Personal identifiable info (detected if user/email/password models)
  - label: "Regulated" - Financial, health data

Q5 - header: "Compliance" (skip if Data=Public)
question: "Compliance requirements?"
multiSelect: true
options:
  - label: "None"
  - label: "GDPR"
  - label: "SOC2"
  - label: "HIPAA"
  - label: "PCI-DSS"

Q6 - header: "Stack"
question: "Tech stack?"
(Show detected: "Python, FastAPI, PostgreSQL")
(Allow correction)

Q7 - header: "Type"
question: "Project type?"
options:
  - label: "backend-api" (detected if no frontend, has routes)
  - label: "frontend" (detected if React/Vue/Angular)
  - label: "fullstack" (detected if both)
  - label: "cli" (detected if argparse/click/commander)
  - label: "library" (detected if no entry point, has exports)
  - label: "mobile" (detected if React Native/Flutter)
  - label: "desktop" (detected if Electron/Tauri)

Q8 - header: "Database"
question: "Database type?"
options:
  - label: "None" (detected if no db imports)
  - label: "SQL" (detected if sqlalchemy/prisma/pg)
  - label: "NoSQL" (detected if mongo/redis/firebase)

Q9 - header: "Rollback"
question: "Rollback complexity?"
options:
  - label: "Git" - Code only, easy revert (detected if no migrations)
  - label: "DB" - Has migrations (detected if migrations/ exists)
  - label: "User-data" - Affects user data (detected if migrations + user models)
```

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

## Step 5: Store in CLAUDE.md

Insert or replace context block in `.claude/CLAUDE.md`:

```markdown
<!-- CCO_CONTEXT_START -->
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: {rollback}

Guidelines:
- {generated guideline 1}
- {generated guideline 2}
- {generated guideline 3}
...
<!-- CCO_CONTEXT_END -->
```

If block exists → replace. If not → append after first heading.

## Step 6: Offer Documentation Updates

If gaps were found in project docs:

```
AskUserQuestion:
header: "Docs"
question: "Update project documentation with context info?"
multiSelect: true
options:
  - label: "All"
  - label: "Add scale/users to README"
  - label: "Add SECURITY.md with data policy"
  - label: "Add CONTRIBUTING.md with team info"
  - label: "Skip"
```

Apply selected documentation updates.

## Step 7: Proceed

Context is now available in CLAUDE.md. Commands read and apply it.

---

## Context Usage in Commands

All commands MUST:

1. Read `<!-- CCO_CONTEXT_START -->` block from CLAUDE.md
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
