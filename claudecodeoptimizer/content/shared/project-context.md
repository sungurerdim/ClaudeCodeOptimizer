# Project Context System

## Context File Location

Project context is stored in `.claude/cco_context.yaml`

## Context Check Flow

Before running context-aware commands, check for existing context:

### Step 1: Check Existing Context

```bash
# Check if context file exists
cat .claude/cco_context.yaml 2>/dev/null
```

### Step 2: Validate or Gather

**If context exists**, show summary and ask:

```
AskUserQuestion:
header: "Context"
question: "Found existing project context. Is this still accurate?"
options:
  - "Yes, use this" → proceed with existing
  - "Update some fields" → show multiselect of fields to update
  - "Start fresh" → re-ask all questions
```

**If "Update some fields"** selected:
```
AskUserQuestion:
header: "Update"
question: "Which fields need updating?"
multiSelect: true
options:
  - "Impact & Scale (who affected, how many)"
  - "Risk (data sensitivity, compliance, downtime)"
  - "Team (size, ownership)"
  - "Operations (rollback, time pressure)"
```

Then re-ask only the selected sections.

**If no context exists**, gather new context.

## Context Gathering (Conditional Questions)

Ask questions conditionally based on previous answers:

### Question 1: Impact (Always)
```
header: "Impact"
question: "If something goes wrong, who is affected?"
options:
  - label: "Just me"
    description: "Personal project, learning, experimentation"
  - label: "My team"
    description: "Internal tool, team productivity"
  - label: "Customers"
    description: "Paying users, B2B/B2C product"
  - label: "General public"
    description: "Public API, open platform, critical infrastructure"
```

### Question 2: Scale (Only if team+)
```
header: "Scale"
question: "How many people are affected?"
options:
  - label: "<100"
  - label: "100-10K"
  - label: "10K-1M"
  - label: "1M+"
```

### Question 3: Data Sensitivity (Only if customers+)
```
header: "Data"
question: "What's the most sensitive data you handle?"
options:
  - label: "Public"
    description: "No sensitive data, all public"
  - label: "Internal"
    description: "Business data, not personal"
  - label: "PII"
    description: "Personal identifiable information (names, emails, etc)"
  - label: "Financial/Health"
    description: "Payment data, health records, highly regulated"
```

### Question 4: Compliance (Only if PII+)
```
header: "Compliance"
question: "Which compliance requirements apply?"
multiSelect: true
options:
  - label: "GDPR/KVKK"
  - label: "SOC2"
  - label: "HIPAA"
  - label: "PCI-DSS"
```

### Question 5: Downtime Tolerance (Always)
```
header: "Downtime"
question: "How critical is uptime?"
options:
  - label: "Downtime OK"
    description: "Can be down for hours/days, no big deal"
  - label: "Hours"
    description: "Should be fixed within hours"
  - label: "Minutes"
    description: "Every minute matters"
  - label: "Seconds"
    description: "Real-time critical, SLA bound"
```

### Question 6: Revenue Impact (Only if minutes+)
```
header: "Revenue"
question: "Financial impact of downtime?"
options:
  - label: "None/Indirect"
  - label: "Hourly loss"
  - label: "Per-minute loss"
```

### Question 7: Team Size (Always)
```
header: "Team"
question: "How many developers work on this?"
options:
  - label: "Solo"
  - label: "2-5"
  - label: "6-15"
  - label: "15+"
```

### Question 8: Code Ownership (Only if 2+)
```
header: "Ownership"
question: "How is code ownership handled?"
options:
  - label: "Everyone everywhere"
    description: "Any developer can modify any code"
  - label: "Area ownership"
    description: "Teams/people own specific areas"
  - label: "Strict CODEOWNERS"
    description: "Formal ownership, required reviews"
```

### Question 9: Rollback Complexity (Always)
```
header: "Rollback"
question: "How hard is it to undo a bad deploy?"
options:
  - label: "Git revert"
    description: "Just revert commit, no side effects"
  - label: "DB migration"
    description: "Need to handle database changes"
  - label: "User data risk"
    description: "May affect user data, careful rollback needed"
```

### Question 10: Time Pressure (Always)
```
header: "Pressure"
question: "Current time pressure?"
options:
  - label: "Relaxed"
    description: "No deadline, quality over speed"
  - label: "Normal"
    description: "Reasonable timeline"
  - label: "Deadline"
    description: "Specific deadline approaching"
  - label: "Urgent"
    description: "Hotfix, emergency, ASAP"
```

## Store Context

After gathering, write to `.claude/cco_context.yaml`:

```yaml
# CCO Project Context
# Generated: {date}
# Run /cco-review, /cco-audit, etc. to use this context

version: 1
updated: {ISO date}

impact:
  affected: {answer}      # self | team | customers | public
  scale: {answer}         # <100 | 100-10k | 10k-1m | 1m+ (if team+)

risk:
  data_sensitivity: {answer}   # public | internal | pii | financial (if customers+)
  compliance: {list}           # [gdpr, soc2, hipaa, pci-dss] (if pii+)
  downtime_tolerance: {answer} # ok | hours | minutes | seconds
  revenue_impact: {answer}     # none | hourly | per-minute (if minutes+)

team:
  size: {answer}          # solo | 2-5 | 6-15 | 15+
  ownership: {answer}     # all | areas | strict (if 2+)

operations:
  rollback: {answer}      # git | db_migration | user_data
  time_pressure: {answer} # relaxed | normal | deadline | urgent
```

## Using Context in Commands

When a command includes this context system, inject the context into AI evaluation:

```markdown
## Project Context

{Read and include .claude/cco_context.yaml content here}

## Context-Aware Instructions

Based on the project context above, calibrate your analysis:

- **DO NOT** apply rigid, one-size-fits-all standards
- **DO** consider the trade-offs appropriate for this context
- **DO** prioritize recommendations based on impact vs context
- **DO** mention when you're relaxing or tightening standards based on context
- **DO** explain WHY certain things matter more/less for this context

For example:
- Solo MVP with "just me" affected → pragmatic, ship-fast recommendations
- Enterprise with financial data → rigorous, compliance-focused recommendations
- Urgent hotfix → focus on immediate fix, defer improvements
```
