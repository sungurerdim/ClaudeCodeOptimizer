---
name: cco-tune
description: Project-specific AI tuning and configuration
---

# /cco-tune

**Project tuning** - Context + AI Performance + Statusline + Permissions in one flow.

## Decision Tree

```
User runs /cco-tune
  │
  ├─► Step 1: Health Check (no agent)
  │     ├─ CCO installation status
  │     └─ Config validation (settings.json, statusline.js)
  │
  ├─► Step 2: Existing Context?
  │     ├─ Yes → Show summary, ask: Use / Update
  │     └─ No → Continue to detection
  │
  ├─► Step 3: Detection (cco-agent-detect scope: full)
  │     ├─ Technical: stack, tools, conventions
  │     └─ Strategic: purpose, team, scale, data
  │
  ├─► Step 4: Confirmation (AskUserQuestion calls)
  │     ├─ Call 1: Core Context (Purpose, Team, Scale, Data)
  │     ├─ Call 2: Technical (Stack, Type, DB, Rollback)
  │     ├─ Call 3: Approach (Maturity, Breaking, Priority)
  │     └─ Call 4: AI Performance (Thinking, MCP, Caching)
  │
  ├─► Step 5: Configuration (AskUserQuestion)
  │     ├─ Scope: Global / Local
  │     ├─ Features: Statusline / Permissions / Both / Skip
  │     └─ Permission Level (if selected): Safe / Balanced / Permissive
  │
  ├─► Step 6: Apply
  │     ├─ Write CCO_CONTEXT to ./CLAUDE.md
  │     ├─ Write statusline.js (if selected)
  │     ├─ Update settings.json (statusLine + permissions + env)
  │     └─ Validate all changes
  │
  └─► Step 7: Status Display
```

## Step 1: Health Check

### CCO Installation
```
globalCommands = count(~/.claude/commands/cco-*.md)
globalAgents = count(~/.claude/agents/cco-*.md)
globalStandards = exists(~/.claude/CLAUDE.md) with CCO_STANDARDS
```

If issues:
```
CCO Status: WARNING
  Commands: {count}/9 | Agents: {count}/3 | Standards: {OK|MISSING}
→ Run: pip install claudecodeoptimizer && cco-setup
```

### Config Validation
Check both scopes (~/.claude/ and ./.claude/):

**settings.json:**
- JSON syntax valid
- No conflicting rules (same pattern in allow AND deny)
- Dangerous commands in deny list

**statusline.js:**
- JavaScript syntax valid (if exists)
- settings.json has statusLine config pointing to it

If issues:
```
Config Issues:
  ⚠ {scope} settings.json: {issue}
  ⚠ {scope} statusline.js exists but not activated in settings
```

## Step 2: Existing Context Check

Read `<!-- CCO_CONTEXT_START -->` from `./CLAUDE.md`:

If exists, display:
```
Current Context:
  Purpose: {purpose}
  Team: {team} | Scale: {scale} | Type: {type}
  AI: Thinking {budget} | MCP {limit} | Compact {mode}
  Config: Statusline {Y/N} | Permissions {level}
```

Then ask:
```
header: "Context"
question: "Use existing context or update?"
options:
  - label: "Use as-is"
    description: "Continue with current settings"
  - label: "Update"
    description: "Re-detect and reconfigure"
```

If "Use as-is" → display status and exit.

## Step 3: Detection

Run `cco-agent-detect` with `scope: full`:

**Technical:**
- Stack (languages, frameworks, databases, infrastructure)
- Tools (format, lint, test commands)
- Conventions (testNaming, importStyle)
- Applicable checks list

**Strategic:**
- Purpose, Team, Scale, Data, Type, Rollback

**Auto-Detected:**
- monorepo, preCommitHooks, currentCoverage, lintingConfigured
- apiEndpoints, containerSetup, i18nSetup, authPatterns
- licenseType, secretsDetected, depsOutdated, gitDefaultBranch

## Step 4: Confirmation

**Label System (apply to ALL options):**
```
[current]               - Value from existing CCO_CONTEXT
[detected]              - Auto-detected from codebase analysis
[recommended:{profile}] - Recommended for complexity profile
```

**Label Rules:**
- Append matching labels to description: `"{base_description} {labels}"`
- Multiple labels allowed when applicable
- Omit labels that don't apply (no empty brackets)
- Order: base description, then [current], [detected], [recommended:{profile}]

### Call 1 - Core Context
```
Q1 - header: "Purpose"
question: "Project purpose?"
options:
  - label: "{detected.purpose}"
    description: "Detected from codebase {labels}"
  - 2-3 alternatives based on {detected.type}

Q2 - header: "Team"
question: "Team size?"
options: Solo | 2-5 | 6+
description_template: "{base_description} {labels}"

Q3 - header: "Scale"
question: "Expected users?"
options: <100 | 100-10K | 10K+
description_template: "{base_description} {labels}"

Q4 - header: "Data"
question: "Most sensitive data?"
options: Public | Internal | PII | Regulated
description_template: "{base_description} {labels}"
```

### Call 2 - Technical
```
Q5 - header: "Stack"
question: "Tech stack correct?"
options:
  - label: "{detected.stack}"
    description: "{labels}"
  - label: "Edit"
    description: "Modify the detected stack"

Q6 - header: "Type"
question: "Project type?"
options: backend-api | frontend | fullstack | cli | library | mobile | desktop
description_template: "{base_description} {labels}"
note: Show 4 most relevant based on {detected.type}

Q7 - header: "Database"
question: "Database type?"
options: None | SQL | NoSQL
description_template: "{base_description} {labels}"

Q8 - header: "Rollback"
question: "Rollback complexity?"
options: Git | DB | User-data
description_template: "{base_description} {labels}"
```

### Call 3 - Approach
```
Q9 - header: "Maturity"
question: "Project phase?"
options: Greenfield | Active | Maintenance | Legacy
description_template: "{base_description} {labels}"

Q10 - header: "Breaking"
question: "Breaking changes tolerance?"
options: Allowed | Minimize | Never
description_template: "{base_description} {labels}"

Q11 - header: "Priority"
question: "Quality vs speed?"
options: Speed | Balanced | Quality
description_template: "{base_description} {labels}"
```

### Call 4 - AI Performance

**Complexity Profile Mapping:**
| Profile | Criteria | Thinking | MCP |
|---------|----------|----------|-----|
| simple | Scale <100, Type: cli/library | Off | 25K |
| medium | Scale 100-10K | 8K | 25K |
| complex | Scale 10K+ OR Maturity: legacy | 16K-32K | 50K |

**Extended Thinking Reference:**
- Min: 1,024 tokens | Max: 32K
- Ideal for: math, coding challenges, multi-step logic, research synthesis

```
Q12 - header: "Thinking"
question: "Extended thinking budget?"
options:
  - Off: "Simple tasks, retrieval {labels}" [recommended:simple]
  - 8K: "Standard coding, moderate complexity {labels}" [recommended:medium]
  - 16K: "Complex logic, deep analysis {labels}"
  - 32K: "Maximum budget {labels}" [recommended:complex]

Q13 - header: "MCP"
question: "MCP tool output limit?"
options:
  - 25K: "{base_description} {labels}" [recommended:simple,medium]
  - 50K: "{base_description} {labels}" [recommended:complex]
  - 100K: "{base_description} {labels}"

Q14 - header: "Caching"
question: "Prompt caching?"
options:
  - Enabled: "{base_description} {labels}" [recommended:all]
  - Disabled: "{base_description} {labels}"
```

**Note:** Auto-compact can only be toggled via `/config` UI.

## Step 5: Configuration

### Scope & Features
```
Q15 - header: "Scope"
question: "Configuration scope?"
options: Global | Local
description_template: "{base_description} {labels}"

Q16 - header: "Features"
question: "What to configure?"
multiSelect: true
options: Statusline | Permissions | Skip
description_template: "{base_description} {labels}"
```

### Permission Level (if Permissions selected)
```
Q17 - header: "Permissions"
question: "Permission level?"
options:
  - Safe: "{base_description} {labels}"
  - Balanced: "{base_description} {labels}" [recommended:all]
  - Permissive: "{base_description} {labels}"
```

## Step 6: Apply Changes

### Write CCO_CONTEXT to ./CLAUDE.md

**Source files:**
- Global: `cco-standards.md` → Universal + Claude-Specific (already in ~/.claude/CLAUDE.md)
- Conditional: `cco-standards-conditional.md` → filtered by detection, written to local only

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: {rollback}
Maturity: {maturity} | Breaking: {breaking} | Priority: {priority}

## AI Performance
Thinking: {off|8K|16K|32K} | MCP: {25K|50K|100K} | Caching: {on|off}

## Guidelines
{generated from confirmed values}

## Operational
Tools: {format}, {lint}, {test}
Conventions: {testNaming}, {importStyle}
Applicable: {checks list}
Not Applicable: {excluded checks}

## Auto-Detected
Structure: {monorepo|single-repo} | Hooks: {pre-commit|none} | Coverage: {N%}
- [x/] Linting configured
- [x/] Pre-commit hooks
- [x/] API endpoints
- [x/] Container setup
- [x/] i18n setup
License: {type}
Secrets detected: {yes|no}
Outdated deps: {N}

## Conditional Standards (auto-applied)
{Only sections from cco-standards-conditional.md where "When:" matches detected values}
<!-- CCO_CONTEXT_END -->
```

### Conditional Selection Logic

Read `cco-standards-conditional.md` and include sections where "When:" condition matches:

| Conditional | Include When |
|-------------|--------------|
| Security Extended | Container/K8s detected OR Scale: 10K+ OR Data: PII/Regulated |
| Architecture | Scale: 10K+ OR Type: backend-api with microservices |
| Operations | Scale: 10K+ OR CI/CD detected |
| Performance | Scale: 100-10K+ OR Performance in Applicable |
| Data | DB != None |
| API | API endpoints detected |
| Frontend | Type: frontend/fullstack |
| i18n | i18n setup detected |
| Reliability | Scale: 10K+ OR SLA requirements |
| Cost | Container/Cloud setup detected |
| DX | Team: 2-5+ |
| Compliance | Compliance != None |

**Write only matching sections** - do not include conditionals that don't apply.

### Write Statusline (if selected)

1. Write `{scope}/statusline.js` (full code from cco-config)
2. **Check and update** `{scope}/settings.json`:

```javascript
// Check if statusLine config exists
const settings = readJSON('{scope}/settings.json') || {};

// Ensure statusLine is configured
if (!settings.statusLine) {
  settings.statusLine = {
    "type": "command",
    "command": "node -e \"const p=require('path'),o=require('os'),{spawnSync:s}=require('child_process'),r=s('node',[p.join(o.homedir(),'.claude','statusline.js')],{stdio:['inherit','inherit','inherit']});process.exit(r.status||0)\""
  };
}

// For local scope, adjust path
if (scope === 'local') {
  settings.statusLine.command = settings.statusLine.command.replace(
    "o.homedir(),'.claude'",
    "process.cwd(),'.claude'"
  );
}

writeJSON('{scope}/settings.json', settings);
```

### Write Permissions (if selected)

Update `{scope}/settings.json` with permissions based on level.

### Write AI Performance Settings

Update `{scope}/settings.json`:

```json
{
  "env": {
    "MAX_THINKING_TOKENS": "{value or omit if off}",
    "MAX_MCP_OUTPUT_TOKENS": "{value}",
    "DISABLE_PROMPT_CACHING_OPUS": "{1 if disabled, omit if enabled}"
  }
}
```

## Step 7: Status Display

```
CCO Tune Complete

Project Context: ./CLAUDE.md
  Team: {team} | Scale: {scale} | Type: {type}
  AI: Thinking {budget} | MCP {limit}

Configuration: {scope}
  Statusline: {configured|skipped}
  Permissions: {level|skipped}
  AI Settings: Applied to settings.json

Quick start:
  /cco-audit --smart    # Run calibrated audit
  /cco-review           # Strategic review
```

## Statusline Code

See `claudecodeoptimizer/content/statusline/statusline.js` for complete implementation.

## Permission Lists

See `claudecodeoptimizer/content/permissions/` for Safe/Balanced/Permissive definitions.

## Guidelines Generation

| If Value | Add Guideline |
|----------|---------------|
| Team: solo | Self-review sufficient |
| Team: 2-5 | Informal review, document decisions |
| Team: 6+ | Formal review required |
| Scale: <100 | Simple solutions, optimize for clarity |
| Scale: 100-10K | Add monitoring, consider caching |
| Scale: 10K+ | Performance critical, load test |
| Data: public | Basic validation sufficient |
| Data: internal | Add authentication, audit logs |
| Data: pii | Encryption required, minimize retention |
| Data: regulated | Full compliance, external audit |
| Maturity: greenfield | Aggressive refactors OK, establish patterns early |
| Maturity: active | Balanced refactors, maintain momentum |
| Maturity: maintenance | Conservative changes, stability first |
| Maturity: legacy | Wrap don't modify, strangler pattern |
| Breaking: allowed | Clean API over compatibility |
| Breaking: minimize | Deprecate first, migration path |
| Breaking: never | Adapters required |
| Priority: speed | MVP mindset, ship fast |
| Priority: balanced | Standard practices |
| Priority: quality | Thorough, no shortcuts |

## Compact Instructions Template

When auto-compact is set to manual, add to CLAUDE.md:

```markdown
## Compact Instructions
When using /compact, preserve:
- All code changes with file paths
- Error messages and stack traces
- User requirements and decisions
- Test results and coverage data

Discard:
- Exploratory searches that found nothing
- Superseded plans
- Verbose tool outputs already processed
```

## Usage

```bash
/cco-tune              # Full interactive flow
/cco-tune --update     # Force re-detection
/cco-tune --status     # Show current without changes
```

## Rules

1. NEVER auto-apply without user confirmation
2. ALWAYS preserve non-CCO settings in JSON files
3. ALWAYS validate JSON syntax before writing
4. Backup before replacement if file exists
5. Local scope overrides global for that project
