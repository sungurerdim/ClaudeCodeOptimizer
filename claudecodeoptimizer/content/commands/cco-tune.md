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
  │     └─ Call 4: AI Performance (Thinking, MCP, Compact, Caching)
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

### Call 1 - Core Context
```
Q1 - header: "Purpose"
question: "Project purpose?"
options: [detected] + 2-3 alternatives

Q2 - header: "Team"
question: "Team size?"
options: Solo | 2-5 | 6+

Q3 - header: "Scale"
question: "Expected users?"
options: <100 | 100-10K | 10K+

Q4 - header: "Data"
question: "Most sensitive data?"
options: Public | Internal | PII | Regulated
```

### Call 2 - Technical
```
Q5 - header: "Stack"
question: "Tech stack correct?"
options: [detected stack] | Edit

Q6 - header: "Type"
question: "Project type?"
options: backend-api | frontend | fullstack | cli | library | mobile | desktop

Q7 - header: "Database"
question: "Database type?"
options: None | SQL | NoSQL

Q8 - header: "Rollback"
question: "Rollback complexity?"
options: Git | DB | User-data
```

### Call 3 - Approach
```
Q9 - header: "Maturity"
question: "Project phase?"
options:
  - Greenfield: New, aggressive changes OK
  - Active: Growing, balanced approach
  - Maintenance: Stable, minimize changes
  - Legacy: Old, wrap don't modify

Q10 - header: "Breaking"
question: "Breaking changes tolerance?"
options:
  - Allowed: Rename/restructure freely
  - Minimize: Deprecate first
  - Never: Full backward compatibility

Q11 - header: "Priority"
question: "Quality vs speed?"
options:
  - Speed: Ship fast, iterate
  - Balanced: Standard practices
  - Quality: Thorough, no shortcuts
```

### Call 4 - AI Performance
```
Q12 - header: "Thinking"
question: "Extended thinking budget?"
options:
  - label: "Off"
    description: "Disabled (default)"
  - label: "1K"
    description: "Minimum - basic reasoning"
  - label: "8K"
    description: "Moderate - most tasks [recommended: medium projects]"
  - label: "32K"
    description: "Deep - complex analysis [recommended: complex projects]"
  - label: "64K"
    description: "Benchmark-level analysis"

Q13 - header: "MCP Limit"
question: "MCP tool output limit?"
options:
  - label: "25K"
    description: "Default (warns at 10K)"
  - label: "50K"
    description: "Extended for larger outputs"
  - label: "100K"
    description: "Maximum for complex tools"

Q14 - header: "Caching"
question: "Prompt caching?"
options:
  - label: "Enabled"
    description: "Faster, cheaper (default)"
  - label: "Disabled"
    description: "Fresh reasoning, higher cost"
```

**Complexity-based recommendations:**
- Simple (Scale <100, Type: cli/library): Thinking Off, MCP 25K, Caching Enabled
- Medium (Scale 100-10K): Thinking 8K, MCP 25K, Caching Enabled
- Complex (Scale 10K+ OR Maturity: legacy): Thinking 32K, MCP 50K, Caching Enabled

**Note:** Auto-compact can only be toggled via `/config` UI, not programmatically.

## Step 5: Configuration

### Scope & Features
```
Q16 - header: "Scope"
question: "Configuration scope?"
options:
  - label: "Global"
    description: "~/.claude/ - applies to all projects"
  - label: "Local"
    description: "./.claude/ - this project only"

Q17 - header: "Features"
question: "What to configure?"
multiSelect: true
options:
  - label: "Statusline"
    description: "Visual status bar with git info"
  - label: "Permissions"
    description: "Tool access rules"
  - label: "Skip"
    description: "Context only, no config changes"
```

### Permission Level (if Permissions selected)
```
Q18 - header: "Permissions"
question: "Permission level?"
options:
  - label: "Safe"
    description: "Ask for all writes/commands"
  - label: "Balanced"
    description: "Allow safe commands, ask risky [recommended]"
  - label: "Permissive"
    description: "Allow most, deny dangerous"
```

## Step 6: Apply Changes

### Write CCO_CONTEXT to ./CLAUDE.md

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: {rollback}
Maturity: {maturity} | Breaking: {breaking} | Priority: {priority}

## Guidelines
{generated from confirmed values}

## AI Performance
Thinking: {off|1K|8K|32K|64K} | MCP: {25K|50K|100K} | Caching: {on|off}

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
<!-- CCO_CONTEXT_END -->
```

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
