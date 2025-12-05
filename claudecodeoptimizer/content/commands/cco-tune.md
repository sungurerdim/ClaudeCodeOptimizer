---
name: cco-tune
description: Project-specific AI tuning and configuration
---

# /cco-tune

**Project tuning** - Detection, statusline, permissions for the current project.

**Standards:** Output Formatting | Priority & Approval | Status Updates | UX/DX

## Scope

| Tool | Location | What It Does |
|------|----------|--------------|
| `cco-setup` | `~/.claude/` (global) | Universal + AI-Specific standards |
| `cco-tune` | `./` (project only) | Project-specific context + standards |

**cco-tune never modifies files outside the current project directory.**

## Usage

```bash
/cco-tune              # Show status, then choose what to configure
/cco-tune --export     # Export standards (AGENTS.md or CLAUDE.md)
```

---

## Flow Overview

**Status first, all questions at start, uninterrupted execution after.**

```
1. STATUS     → Always show current project state first
2. CHOOSE     → What to configure? + ALL config questions
3. DETECT     → Run detection (if selected, no questions)
4. REVIEW     → Accept/Edit/Cancel (single confirmation)
5. APPLY      → Write all selected configurations
6. REPORT     → Summary
```

---

## Step 1: Status (Always Runs)

Show current project state before asking anything:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                              CCO PROJECT STATUS                                ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ PROJECT: {project_name}                                                        ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ CONTEXT         │ ./CLAUDE.md                                                  ║
├─────────────────┼──────────────────────────────────────────────────────────────┤
║ Purpose         │ {purpose}                                                    ║
║ Team/Scale/Data │ {team} | {scale} | {data}                                    ║
║ Stack/Type      │ {stack} | {type}                                             ║
║ AI Performance  │ Thinking {thinking} | MCP {mcp} | Caching {caching}          ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ FEATURES        │ Status                                                       ║
├─────────────────┼──────────────────────────────────────────────────────────────┤
║ Statusline      │ {statusline_status}                                          ║
║ Permissions     │ {permissions_status}                                         ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ STANDARDS       │ {base} base + {project} project-specific = {total}           ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

**If no context exists (first run):**

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                              CCO PROJECT STATUS                                ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ PROJECT: {project_name}                                                        ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ CONTEXT         │ Not configured                                               ║
║ FEATURES        │ Not configured                                               ║
║ STANDARDS       │ {base} base only (no project-specific)                       ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## Step 2: Choose Actions + Configure

Based on status, show options with smart defaults. **All configuration questions are asked in this step.**

**If context exists:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ What would you like to do?                                              │
├─────────────────────────────────────────────────────────────────────────┤
│ ☐ Update Detection   Re-detect stack and update standards               │
│ ☐ Statusline         Configure status bar                               │
│ ☐ Permissions        Configure permission levels                        │
│ ○ Nothing            Exit without changes                               │
└─────────────────────────────────────────────────────────────────────────┘
```

**If no context (first run):**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ What would you like to configure?                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ ☑ Project Detection  [recommended] Detect and apply standards           │
│ ☐ Statusline         Rich status bar with git info                      │
│ ☐ Permissions        Quick permission cycling (shift+tab)               │
└─────────────────────────────────────────────────────────────────────────┘
```

- Detection is pre-selected and marked `[recommended]` when no context exists
- User can select multiple options

### Inline Configuration Questions

**If Statusline selected**, ask immediately:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Statusline mode                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ ○ Full        [recommended] Project, git, changes, permissions          │
│ ○ Minimal     Project + git branch only                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

**If Permissions selected**, ask immediately:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Permission level                                                        │
├─────────────────────────────────────────────────────────────────────────┤
│ ○ Safe        [recommended] Auto: reads, lint | Ask: writes, deletes   │
│ ○ Balanced    Auto: reads | Ask: all writes                             │
│ ○ Permissive  Auto: most ops | Ask: deletes, security-sensitive         │
└─────────────────────────────────────────────────────────────────────────┘
```

After all questions answered → proceed to detection/apply (no more questions)

---

## Step 3: Detection (if selected)

**Location:** `./CLAUDE.md` (project only)

### Auto-Detect Elements

| # | Element | Detection Source | Triggers |
|---|---------|------------------|----------|
| 1 | Purpose | README.md first paragraph | - |
| 2 | Stack | package.json, pyproject.toml, go.mod | - |
| 3 | Type | Entry points, project structure | CLI, Library |
| 4 | DB | Dependencies, config files | Data standards |
| 5 | CI/CD | .github/workflows/, .gitlab-ci.yml | Operations |
| 6 | API | Routes, endpoints, OpenAPI | API standards |
| 7 | Frontend | react, vue, angular in deps | Frontend |
| 8 | Mobile | Podfile, build.gradle, pubspec | Mobile |
| 9 | Desktop | electron, tauri in deps | Desktop |
| 10 | ML/AI | torch, tensorflow, sklearn | ML/AI |
| 11 | Game | Unity, Unreal, Godot files | Game Dev |
| 12 | Serverless | serverless.yml, sam.yaml | Serverless |
| 13 | Monorepo | nx.json, turbo.json, lerna | Monorepo |
| 14 | Container | Dockerfile, docker-compose | Container/K8s |
| 15 | K8s | k8s/, helm/, kustomization | Container/K8s |
| 16 | i18n | locales/, i18n config | i18n |
| 17 | Microservices | Multiple services detected | Architecture |
| 18 | License | LICENSE file | - |
| 19 | Coverage | pytest-cov, coverage reports | - |
| 20 | Secrets Risk | .env patterns, hardcoded | Security |

### Default Values (when not detectable)

| Element | Default | Can Be Overridden |
|---------|---------|-------------------|
| Team | Solo | Yes |
| Scale | <100 | Yes |
| Data | Public | Yes |
| Compliance | None (from Data) | Yes |
| Maturity | Active | Yes |
| Breaking | Minimize | Yes |
| Priority | Quality | Yes |

### AI Performance (Calculated)

| Element | Description | Default |
|---------|-------------|---------|
| Thinking | Claude extended thinking | 8K |
| MCP | MCP output limit | 25K |
| Caching | Prompt caching (reduces cost) | on |

---

## Step 4: Review Detection Results

Show unified table with dynamic standard counts:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                              CCO PROJECT TUNE                                  ║
╠════════════════════════════════════════════════════════════════════════════════╣
║  #  │ Element      │ Value                │ Source              │ Standards   ║
╠═════╪══════════════╪══════════════════════╪═════════════════════╪═════════════╣
║     │ AUTO-DETECTED                                                            ║
├─────┼──────────────┼──────────────────────┼─────────────────────┼─────────────┤
║  1  │ Purpose      │ {purpose}            │ {source}            │ -           ║
║  2  │ Stack        │ {languages/tools}    │ {config_file}       │ -           ║
║  3  │ Type         │ {project_type}       │ {detection_source}  │ +{N} {cat}  ║
║  4  │ DB           │ {db_type|None}       │ {detection_method}  │ -           ║
║  5  │ CI/CD        │ {ci_platform|None}   │ {ci_path}           │ +{N} Ops    ║
║  6  │ API          │ {api_type|None}      │ {detection_method}  │ -           ║
║ ... │ ...          │ ...                  │ ...                 │ ...         ║
╠═════╪══════════════╪══════════════════════╪═════════════════════╪═════════════╣
║     │ DEFAULTS                                                                 ║
├─────┼──────────────┼──────────────────────┼─────────────────────┼─────────────┤
║ 21  │ Team         │ Solo                 │ default             │ -           ║
║ 22  │ Scale        │ <100                 │ default             │ -           ║
║ 23  │ Data         │ Public               │ default             │ -           ║
║ ... │ ...          │ ...                  │ ...                 │ ...         ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ STANDARDS: +{N} project-specific ({matched categories})                        ║
║ TOTAL: {base} base + {project} selected = {total}                              ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

**Standard counts are calculated dynamically** from `cco-standards-conditional.md` based on triggers.

### Review Options

```
┌─────────────────────────────────────────────────────────────────┐
│ Detection complete. What would you like to do?                  │
├─────────────────────────────────────────────────────────────────┤
│ ○ Accept        Apply this configuration                        │
│ ○ Edit          Change specific items (enter: 21,22,23)         │
│ ○ Edit all      Configure all items interactively               │
│ ○ Cancel        Exit without changes                            │
└─────────────────────────────────────────────────────────────────┘
```

**If Edit**: Show options with recommendations and affected standards:

```
┌─────────────────────────────────────────────────────────────────┐
│ #{N} {element} - {question}?                                    │
├─────────────────────────────────────────────────────────────────┤
│ ○ {option_1}   [{current|detected}] {description}               │
│ ○ {option_2}   {description}                                    │
│ ○ {option_3}   {description}                                    │
│                                                                 │
│ Affects: {affected_categories}                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 5: Apply

Write all selected configurations to project-local files:

| Selection | Target | Content |
|-----------|--------|---------|
| Detection | `./CLAUDE.md` | CCO_CONTEXT block |
| Statusline | `./.claude/statusline.js` | Status bar script |
| Permissions | `./.claude/settings.json` | Permission config |

### CCO_CONTEXT Format

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: Git
Maturity: {maturity} | Breaking: {breaking} | Priority: {priority}

## AI Performance
Thinking: {value} | MCP: {value} | Caching: {on|off}

## Guidelines
{generated based on values}

## Operational
Tools: {format}, {lint}, {test}
Conventions: {detected patterns}
Applicable: {check categories}

## Auto-Detected
Structure: {type} | Coverage: {N}% | License: {type}
{checklist of detected features}

## Conditional Standards
{matched project-specific standards}
<!-- CCO_CONTEXT_END -->
```

---

## Step 6: Report

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                            CCO TUNE COMPLETE                                   ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ CONFIGURED                                                                     ║
├────────────────────────────────────────────────────────────────────────────────┤
║ ✓ Project Detection  → ./CLAUDE.md                                             ║
║ ✓ Statusline         → ./.claude/statusline.js                                 ║
║ ✓ Permissions        → ./.claude/settings.json (Safe mode)                     ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ STANDARDS: {base} base + {project} project-specific = {total}                  ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ Restart Claude Code for changes to take effect                                 ║
║ Next: /cco-health to verify | /cco-audit --smart to check                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## Export Mode (--export)

Export current configuration to portable format.

### Export Choice

```
┌─────────────────────────────────────────────────────────────────┐
│ Export format                                                   │
├─────────────────────────────────────────────────────────────────┤
│ ○ AGENTS.md     For other AI tools (Cursor, Windsurf, etc.)     │
│                 Prose format, universally readable              │
│                                                                 │
│ ○ CLAUDE.md     For sharing Claude Code context                 │
│                 Minimal format, CCO-compatible                  │
└─────────────────────────────────────────────────────────────────┘
```

### AGENTS.md Export (Prose Format)

```markdown
# Project Standards

> Exported from CCO (ClaudeCodeOptimizer)

## Project Context

This is a **{type}** project built with {stack}.

### Development Profile
- **{team} developer** - {team_guideline}
- **{scale} scale** - {scale_guideline}
- **{data} data** - {data_guideline}

### Technical Stack
{detected stack details in prose}

---

## Universal Standards
{all universal standards in prose format}

## AI-Specific Standards
{all AI-specific standards in prose format}

## Project-Specific Standards
{matched standards based on detection}
```

### CLAUDE.md Export

Exports the CCO_CONTEXT block for sharing with other Claude Code users or projects.

---

## Detection → Standards Mapping

| Detection | Triggers |
|-----------|----------|
| Data: PII/Regulated OR Scale: 10K+ | Security Enhanced |
| Scale: 10K+ OR Microservices | Architecture |
| CI/CD detected | Operations |
| Scale: 100+ | Performance |
| DB: SQL/NoSQL | Data |
| API: REST/GraphQL/gRPC | API |
| Frontend detected | Frontend |
| Mobile detected | Mobile |
| Desktop detected | Desktop |
| Type: cli | CLI |
| Type: library | Library |
| ML/AI detected | ML/AI |
| Game engine detected | Game Dev |
| Serverless detected | Serverless |
| Monorepo detected | Monorepo |
| Container/K8s detected | Container/K8s |
| Team: 2+ | Team Collaboration |
| Compliance: not None | Compliance |
| i18n detected | i18n |

Standard counts calculated dynamically at runtime.

---

## Guidelines Generation

| Condition | Generated Guideline |
|-----------|---------------------|
| Team: Solo | Self-review sufficient |
| Team: 2-5 | Informal review, document decisions |
| Team: 6+ | Formal review, CODEOWNERS |
| Scale: <100 | Simple solutions, clarity first |
| Scale: 100-10K | Add caching, monitoring |
| Scale: 10K+ | Performance critical, load test |
| Data: Public | Basic validation sufficient |
| Data: Internal | Auth required, audit logs |
| Data: PII | Encryption, minimize retention |
| Data: Regulated | Full compliance, external audit |
| Maturity: Greenfield | Aggressive refactors OK |
| Maturity: Active | Balanced refactors |
| Maturity: Maintenance | Conservative, stability first |
| Maturity: Legacy | Wrap don't modify |
| Breaking: Allowed | Clean API over compatibility |
| Breaking: Minimize | Deprecate first, migration path |
| Breaking: Never | Adapters required |
| Priority: Speed | MVP mindset, ship fast |
| Priority: Balanced | Standard practices |
| Priority: Quality | Thorough, no shortcuts |

---

## Rules

1. **All questions at the start** - no mid-process interruptions
2. **Local files only** - statusline/permissions in `./.claude/`, not global
3. **Dynamic counts** - standard counts calculated from source files
4. **Show affected standards** - when editing, show what standards change
5. **Preserve existing** - never overwrite non-CCO content in files
