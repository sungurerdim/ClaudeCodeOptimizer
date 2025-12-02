---
name: cco-tune
description: Project-specific AI tuning and configuration
---

# /cco-tune

**Project tuning** - Context + AI Performance + Statusline + Permissions in one flow.

**Standards:** Output Formatting

## Flow

1. **Health Check** - Verify CCO installation, validate configs
2. **Existing Context** - If exists in `./CLAUDE.md` → ask: Use / Update
3. **Detection** - Run `cco-agent-detect scope:full`
4. **Confirmation** - 4 AskUserQuestion calls for all settings
5. **Configuration** - Scope + optional features (statusline/permissions)
6. **Apply** - Write files, validate
7. **Report** - Show changes table

## Step 1: Health Check

**CCO Installation:** Count commands/agents in `~/.claude/`, check standards in CLAUDE.md.

**Config Validation:** Check both scopes (`~/.claude/`, `./.claude/`):
- settings.json: valid JSON, no conflicting rules
- statusline.js: valid JS, activated in settings

If issues → show warning with fix command.

## Step 2: Existing Context

Parse `<!-- CCO_CONTEXT_START -->` to `<!-- CCO_CONTEXT_END -->` from `./CLAUDE.md`.

Extract key-value pairs dynamically (don't hardcode fields). Display parsed content, ask: "Use as-is" / "Update".

## Step 3: Detection

Run `cco-agent-detect scope:full` → returns technical + strategic + autoDetected JSON.

## Step 4: Confirmation

**Label System:** `[current]` `[detected]` `[recommended:{profile}]` - append to option descriptions.

### Call 1 - Core Context

| Q | Header | Question | Options |
|---|--------|----------|---------|
| 1 | Purpose | Project purpose? | {detected} + 2-3 alternatives |
| 2 | Team | Team size? | Solo \| 2-5 \| 6+ |
| 3 | Scale | Expected users? | <100 \| 100-10K \| 10K+ |
| 4 | Data | Most sensitive data? | Public \| Internal \| PII \| Regulated |

Compliance auto-derived: Public/Internal→None, PII→GDPR/CCPA, Regulated→ask which.

### Call 2 - Technical

| Q | Header | Question | Options |
|---|--------|----------|---------|
| 5 | Stack | Tech stack correct? | {detected} \| Edit |
| 6 | Type | Project type? | backend-api \| frontend \| fullstack \| cli \| library \| mobile \| desktop |
| 7 | Database | Database type? | None \| SQL \| NoSQL |
| 8 | Rollback | Rollback complexity? | Git \| DB \| User-data |

### Call 3 - Approach

| Q | Header | Question | Options |
|---|--------|----------|---------|
| 9 | Maturity | Project phase? | Greenfield \| Active \| Maintenance \| Legacy |
| 10 | Breaking | Breaking changes? | Allowed \| Minimize \| Never |
| 11 | Priority | Quality vs speed? | Speed \| Balanced \| Quality |

### Call 4 - AI Performance

**Profile Detection:** `simple` (Scale<100 + cli/library), `complex` (Scale:10K+ or Legacy), else `medium`.

**Defaults:** simple→Off/25K, medium→8K/25K, complex→16K/50K

| Q | Header | Question | Options |
|---|--------|----------|---------|
| 12 | Thinking | Extended thinking? | Off \| 8K \| 16K \| 32K |
| 13 | MCP | MCP output limit? | 25K \| 50K \| 100K |
| 14 | Caching | Prompt caching? | Enabled \| Disabled |

## Step 5: Configuration

| Q | Header | Question | Options |
|---|--------|----------|---------|
| 15 | Scope | Where to save? | Global (~/.claude/) \| Local (./.claude/) |
| 16 | Features | Additional config? | Statusline \| Permissions \| Skip (multiSelect) |
| 17 | Permissions | Permission level? | Safe \| Balanced \| Permissive (if selected) |

## Step 6: Apply

### Write CCO_CONTEXT to ./CLAUDE.md

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: {rollback}
Maturity: {maturity} | Breaking: {breaking} | Priority: {priority}

## AI Performance
Thinking: {value} | MCP: {value} | Caching: {on|off}

## Guidelines
{generated from values - see Guidelines table}

## Operational
Tools: {format}, {lint}, {test}
Conventions: {testNaming}, {importStyle}
Applicable: {checks}
Not Applicable: {excluded}

## Auto-Detected
Structure: {monorepo|single-repo} | Hooks: {status} | Coverage: {N%}
{checklist of detected features}
License: {type} | Secrets: {yes|no} | Outdated: {N}

## Conditional Standards
{filtered from cco-standards-conditional.md by detection}
<!-- CCO_CONTEXT_END -->
```

### Conditional Selection

Include sections from `cco-standards-conditional.md` where conditions match:

| Conditional | When |
|-------------|------|
| Security Extended | Container OR Scale:10K+ OR Data:PII/Regulated |
| Operations | Scale:10K+ OR CI/CD detected |
| Performance | Scale:100-10K+ |
| Data | DB != None |
| API | API endpoints detected |
| Frontend | Type: frontend/fullstack |
| Compliance | Compliance != None |

### Write Settings

**AI Performance** → `{scope}/settings.json` env section:
- MAX_THINKING_TOKENS (if not Off)
- MAX_MCP_OUTPUT_TOKENS
- DISABLE_PROMPT_CACHING (if disabled)

**Statusline** (if selected) → Write `{scope}/statusline.js`, update settings.json statusLine config.

**Permissions** (if selected) → Update settings.json with permission rules.

## Step 7: Report

**Standards:** Output Formatting

Tables:
1. **Header** - Double-line box "CCO Tune Complete"
2. **Changes Applied** - Category | Field | Before | After | Changed
3. **Files Modified** - File | Action
4. **Summary** - {changed}/{total} fields
5. **Current Configuration** - Key settings box
6. **Next Steps** - /cco-health, /cco-audit --smart

Note: Include restart warning.

## Guidelines Generation

| Value | Guideline |
|-------|-----------|
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
| Maturity: greenfield | Aggressive refactors OK |
| Maturity: active | Balanced refactors, maintain momentum |
| Maturity: maintenance | Conservative changes, stability first |
| Maturity: legacy | Wrap don't modify, strangler pattern |
| Breaking: allowed | Clean API over compatibility |
| Breaking: minimize | Deprecate first, migration path |
| Breaking: never | Adapters required |
| Priority: speed | MVP mindset, ship fast |
| Priority: balanced | Standard practices |
| Priority: quality | Thorough, no shortcuts |

## References

- Statusline code: `claudecodeoptimizer/content/statusline/statusline.js`
- Permission lists: `claudecodeoptimizer/content/permissions/`

## Usage

```bash
/cco-tune              # Full interactive flow
/cco-tune --update     # Force re-detection
/cco-tune --status     # Show current without changes
```

## Rules

1. NEVER auto-apply without confirmation
2. ALWAYS preserve non-CCO settings in JSON
3. ALWAYS validate JSON before writing
4. Local scope overrides global
