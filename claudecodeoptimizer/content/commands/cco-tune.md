---
name: cco-tune
description: Project-specific AI tuning and configuration
---

# /cco-tune

**Project tuning** - Context + AI Performance + Statusline + Permissions in one flow.

**Standards:** Output Formatting | Priority & Approval | Resource Scaling | UX/DX

## Required Context Elements

Complete context requires ALL of these elements:

| Category | Element | Required | Options |
|----------|---------|----------|---------|
| **Strategic** | Purpose | YES | Free text description |
| | Team | YES | Solo / 2-5 / 6+ |
| | Scale | YES | <100 / 100-10K / 10K+ |
| | Data | YES | Public / Internal / PII / Regulated |
| | Compliance | YES | None / GDPR / HIPAA / PCI-DSS / SOC2 |
| **Technical** | Stack | YES | Languages, frameworks, tools |
| | Type | YES | backend-api / frontend / fullstack / cli / library / mobile / desktop |
| | DB | YES | None / SQL / NoSQL |
| | Rollback | YES | Git / DB / User-data |
| **Approach** | Maturity | YES | Greenfield / Active / Maintenance / Legacy |
| | Breaking | YES | Allowed / Minimize / Never |
| | Priority | YES | Speed / Balanced / Quality |
| **AI Perf** | Thinking | YES | Off / 8K / 16K / 32K |
| | MCP | YES | 25K / 50K / 100K |
| | Caching | YES | on / off |
| **Operational** | Tools | YES | format, lint, test commands |
| | Conventions | AUTO | Detected from codebase |
| | Applicable | AUTO | Checks that apply |
| **Auto** | Structure | AUTO | Detected |
| | Coverage | AUTO | Detected |
| | License | AUTO | Detected |

**Total:** 15 required + 5 auto-detected = 20 elements

## Flow

1. **Health Check** - Verify CCO installation, validate configs
2. **Context Analysis** - Parse existing context, show completeness status
3. **Detection** - Run `cco-agent-detect scope:full`
4. **Gap Fill** - Ask ONLY for missing/incomplete elements
5. **Configuration** - Scope + optional features (statusline/permissions)
6. **Apply** - Write files, validate
7. **Report** - Show changes, ask restart

**--status Mode:** Steps 1-2 only → if incomplete, ask to complete → if user accepts, continue flow

## Step 1: Health Check

**CCO Installation:** Count commands/agents in `~/.claude/`, check standards in CLAUDE.md.

**Config Validation:** Check both scopes (`~/.claude/`, `./.claude/`):
- settings.json: valid JSON, no conflicting rules
- statusline.js: valid JS, activated in settings

If issues → show warning with fix command.

## Step 2: Context Analysis

Parse `<!-- CCO_CONTEXT_START -->` to `<!-- CCO_CONTEXT_END -->` from `./CLAUDE.md`.

### If Context Exists

Show completeness status with required elements checklist:

```
╔══════════════════════════════════════════════════════════════╗
║                    CONTEXT STATUS                            ║
╠══════════════════════════════════════════════════════════════╣
║ Completeness: 14/15 required elements (93%)                  ║
╠══════════════════════════════════════════════════════════════╣
║ Category    │ Element    │ Status │ Value                    ║
╠═════════════╪════════════╪════════╪══════════════════════════╣
║ Strategic   │ Purpose    │ OK     │ Process and standards... ║
║             │ Team       │ OK     │ Solo                     ║
║             │ Scale      │ OK     │ <100                     ║
║             │ Data       │ OK     │ Public                   ║
║             │ Compliance │ OK     │ None                     ║
╠═════════════╪════════════╪════════╪══════════════════════════╣
║ Technical   │ Stack      │ OK     │ Python 3.10+, ruff...    ║
║             │ Type       │ OK     │ CLI                      ║
║             │ DB         │ OK     │ None                     ║
║             │ Rollback   │ OK     │ Git                      ║
╠═════════════╪════════════╪════════╪══════════════════════════╣
║ Approach    │ Maturity   │ OK     │ Active                   ║
║             │ Breaking   │ OK     │ Minimize                 ║
║             │ Priority   │ OK     │ Quality                  ║
╠═════════════╪════════════╪════════╪══════════════════════════╣
║ AI Perf     │ Thinking   │ OK     │ 16K                      ║
║             │ MCP        │ OK     │ 50K                      ║
║             │ Caching    │ MISS   │ -                        ║
╠═════════════╪════════════╪════════╪══════════════════════════╣
║ Operational │ Tools      │ OK     │ ruff format, pytest...   ║
╚══════════════════════════════════════════════════════════════╝

Missing: Caching
```

Then ask: "Context is 93% complete. What to do?"
- **Complete missing** - Fill only missing elements
- **Update all** - Re-run full configuration
- **Use as-is** - Continue with current (warn if incomplete)

### If No Context

Show empty status, proceed to full detection and configuration.

## Step 3: Detection

Run `cco-agent-detect scope:full` → returns technical + strategic + autoDetected JSON.

## Step 4: Gap Fill (or Full Configuration)

**Mode:** If "Complete missing" → ask only missing elements. If "Update all" or no context → full flow.

**Labels:** Per Option Labels standard (`[current]`, `[detected]`, `[recommended]`)

### Strategic Elements (if missing)

| Element | Question | Options |
|---------|----------|---------|
| Purpose | Project purpose? | {detected} + 2-3 alternatives |
| Team | Team size? | Solo \| 2-5 \| 6+ |
| Scale | Expected users? | <100 \| 100-10K \| 10K+ |
| Data | Most sensitive data? | Public \| Internal \| PII \| Regulated |
| Compliance | Compliance requirements? | None \| GDPR \| HIPAA \| PCI-DSS \| SOC2 |

*Note: Compliance auto-derived if Data=Public/Internal→None, ask explicitly otherwise*

### Technical Elements (if missing)

| Element | Question | Options |
|---------|----------|---------|
| Stack | Tech stack correct? | {detected} \| Edit |
| Type | Project type? | backend-api \| frontend \| fullstack \| cli \| library \| mobile \| desktop |
| DB | Database type? | None \| SQL \| NoSQL |
| Rollback | Rollback complexity? | Git \| DB \| User-data |

### Approach Elements (if missing)

| Element | Question | Options |
|---------|----------|---------|
| Maturity | Project phase? | Greenfield \| Active \| Maintenance \| Legacy |
| Breaking | Breaking changes? | Allowed \| Minimize \| Never |
| Priority | Quality vs speed? | Speed \| Balanced \| Quality |

### AI Performance Elements (if missing)

**Profile Detection:** Based on Scale + Type + Maturity:
| Profile | Condition | Thinking | MCP |
|---------|-----------|----------|-----|
| simple | Scale:<100 + cli/library | Off | 25K |
| complex | Scale:10K+ OR Legacy | 16K | 50K |
| medium | else | 8K | 25K |

Mark the profile-matched value as `[recommended]` per Option Labels standard.

| Element | Question | Options |
|---------|----------|---------|
| Thinking | Extended thinking? | Off \| 8K \| 16K \| 32K |
| MCP | MCP output limit? | 25K \| 50K \| 100K |
| Caching | Prompt caching? | on \| off |

### Operational Elements (if missing)

| Element | Question | Options |
|---------|----------|---------|
| Tools | Tool commands correct? | {detected format/lint/test} \| Edit |

**Batch into AskUserQuestion calls:** Group up to 4 questions per call. Skip elements that already have values (unless "Update all" mode).

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

### Context Activation

If any changes were made, show warning and ask:

```
╔══════════════════════════════════════════════════════════════╗
║ ⚠️  CONTEXT UPDATED                                          ║
╠══════════════════════════════════════════════════════════════╣
║ Changes saved to ./CLAUDE.md                                 ║
║                                                              ║
║ To activate new context:                                     ║
║ • Option 1: Restart Claude Code (recommended)                ║
║ • Option 2: Continue - commands will re-read context         ║
║             explicitly but cached values may persist         ║
╚══════════════════════════════════════════════════════════════╝
```

**AskUserQuestion:**
```
header: "Activation"
question: "How to proceed?"
options:
  - Restart: "End session now - run 'claude' to start fresh with new context"
  - Continue: "Stay in session - subsequent commands will re-read context"
```

**If Restart selected:**
1. Output: "Session ending. To start with updated context, run: `claude`"
2. End command execution immediately
3. Do NOT show "Next Steps"

**If Continue selected:**
1. Show: "Continuing. Commands will re-read CCO_CONTEXT from file."
2. Show Next Steps: /cco-health, /cco-audit --smart

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
