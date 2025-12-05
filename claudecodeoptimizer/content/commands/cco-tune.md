---
name: cco-tune
description: Project-specific AI tuning and configuration
---

# /cco-tune

**Project tuning** - Detection, configuration, and export for the current project.

**Standards:** Approval Flow | Output Formatting

## Scope

| Tool | Location | What It Does |
|------|----------|--------------|
| `cco-setup` | `~/.claude/` (global) | Standards + global statusline |
| `cco-tune` | `./` (project local) | Project context + local statusline/permissions |
| `cco-remove` | `~/.claude/` (global) | Uninstall CCO completely |

### Global vs Local

**cco-setup installs global files:**
- `~/.claude/CLAUDE.md` - Universal + AI-Specific + CCO-Specific standards
- `~/.claude/statusline.js` - Global statusline (Full mode)
- `~/.claude/settings.json` - Global statusLine config
- `~/.claude/commands/cco-*.md` - CCO commands
- `~/.claude/agents/cco-*.md` - CCO agents

**cco-tune creates local project files:**
- `./CLAUDE.md` - Project context + conditional standards
- `./.claude/statusline.js` - Local statusline (overrides global)
- `./.claude/settings.json` - Local permissions (overrides global)

### Content Sources

Files are sourced from `claudecodeoptimizer/content/`:

| Content | Source | Target |
|---------|--------|--------|
| Statusline Full | `content/statusline/full.js` | `statusline.js` |
| Statusline Minimal | `content/statusline/minimal.js` | `statusline.js` |
| Permissions Safe | `content/permissions/safe.json` | `settings.json` |
| Permissions Balanced | `content/permissions/balanced.json` | `settings.json` |
| Permissions Permissive | `content/permissions/permissive.json` | `settings.json` |

Global `~/.claude/` files are never modified by cco-tune.

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
║ LOCAL FEATURES  │ Status                           │ Location                  ║
├─────────────────┼──────────────────────────────────┼───────────────────────────┤
║ Statusline      │ {statusline_status}              │ ./.claude/statusline.js   ║
║ Permissions     │ {permissions_status}             │ ./.claude/settings.json   ║
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
║ LOCAL FEATURES  │ Not configured                                               ║
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
│ ☐ Statusline         Configure local status bar (./.claude/)            │
│ ☐ Permissions        Configure local permission levels (./.claude/)     │
│ ○ Nothing            Exit without changes                               │
└─────────────────────────────────────────────────────────────────────────┘
```

**If no context (first run):**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ What would you like to configure?                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ ☑ Project Detection  [recommended] Detect and apply standards           │
│ ☐ Statusline         Local status bar with git info (./.claude/)        │
│ ☐ Permissions        Local permission levels (./.claude/)               │
└─────────────────────────────────────────────────────────────────────────┘
```

- Detection is pre-selected and marked `[recommended]` when no context exists
- User can select multiple options

### Inline Configuration Questions

**If Statusline selected**, ask immediately:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Local statusline mode (./.claude/statusline.js)                         │
├─────────────────────────────────────────────────────────────────────────┤
│ ○ Full        [recommended] Project, git branch, changes                │
│ ○ Minimal     Project + git branch only                                 │
│ ○ Disable     Remove local statusline                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

**If Permissions selected**, ask immediately:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Local permission level (./.claude/settings.json)                        │
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

**IMPORTANT:** Detection always scans from scratch, ignoring any existing CCO_CONTEXT values. Each element is freshly detected from actual project files. The Source column shows where the value was found.

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
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                CCO PROJECT TUNE                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║  #  │ Element       │ Value                  │ Source                  │ Standards   ║
╠═════╪═══════════════╪════════════════════════╪═════════════════════════╪═════════════╣
║     │ AUTO-DETECTED                                                                  ║
├─────┼───────────────┼────────────────────────┼─────────────────────────┼─────────────┤
║  1  │ Purpose       │ CLI tool for X         │ README.md:1             │ -           ║
║  2  │ Stack         │ Python 3.10+, ruff     │ pyproject.toml          │ -           ║
║  3  │ Type          │ CLI                    │ __main__.py detected    │ +5 Apps     ║
║  4  │ DB            │ None                   │ no db deps found        │ -           ║
║  5  │ CI/CD         │ GitHub Actions         │ .github/workflows/      │ +7 Ops      ║
║  6  │ API           │ None                   │ no routes found         │ -           ║
║ ... │ ...           │ ...                    │ ...                     │ ...         ║
╠═════╪═══════════════╪════════════════════════╪═════════════════════════╪═════════════╣
║     │ DEFAULTS (editable)                                                            ║
├─────┼───────────────┼────────────────────────┼─────────────────────────┼─────────────┤
║ 21  │ Team          │ Solo                   │ default (not detected)  │ -           ║
║ 22  │ Scale         │ <100                   │ default (not detected)  │ -           ║
║ 23  │ Data          │ Public                 │ default (not detected)  │ -           ║
║ ... │ ...           │ ...                    │ ...                     │ ...         ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║ STANDARDS: +{N} project-specific ({matched categories})                              ║
║ TOTAL: {base} base + {project} selected = {total}                                    ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

**Source column rules:**
- Auto-detected: Show actual file path or detection method (e.g., `README.md:1`, `pyproject.toml`, `.github/workflows/`)
- Defaults: Show `default (not detected)` - indicates value was not found in project files
- Never use `current` as a source - always perform fresh detection

**Standard counts are calculated dynamically** from `cco-standards-conditional.md` based on triggers.

### Review Options

```
┌─────────────────────────────────────────────────────────────────┐
│ Detection complete. What would you like to do?                  │
├─────────────────────────────────────────────────────────────────┤
│ ○ Accept        Apply this configuration                        │
│ ○ Edit          Change specific items                           │
│ ○ Cancel        Exit without changes                            │
└─────────────────────────────────────────────────────────────────┘
```

**If Edit selected**, ask which items to change:
```
┌─────────────────────────────────────────────────────────────────┐
│ Which items would you like to edit?                             │
├─────────────────────────────────────────────────────────────────┤
│ ☐ Edit all      Configure all editable items                    │
│ ☐ 21: Team      Currently: Solo                                 │
│ ☐ 22: Scale     Currently: <100                                 │
│ ☐ 23: Data      Currently: Public                               │
└─────────────────────────────────────────────────────────────────┘
```

- First option "Edit all" selects all editable items
- Other options show item number, name, and current value
- User selects which items to edit (multiSelect: true)
- Then show individual questions for each selected item

**For each selected item**, show options with recommendations and affected standards:

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
| Statusline | `./.claude/statusline.js` + `./.claude/settings.json` | Status bar script + settings |
| Permissions | `./.claude/settings.json` | Permission config |

### Statusline Files

**Source:** `claudecodeoptimizer/content/statusline/`

| Mode | Source File | Output |
|------|-------------|--------|
| Full | `statusline/full.js` | `Project \| Branch \| Changes` |
| Minimal | `statusline/minimal.js` | `Project \| Branch` |
| Disable | Remove files | No statusline |

**Target:** `./.claude/statusline.js`

**Local Settings for Statusline** - `./.claude/settings.json`:
```json
{
  "statusLine": {
    "type": "command",
    "command": "node ./.claude/statusline.js"
  }
}
```

**Disable Mode**: Delete `./.claude/statusline.js` and remove `statusLine` from `./.claude/settings.json`.

### Statusline Verification

After writing statusline files, verify:
1. `./.claude/statusline.js` exists and is executable
2. `./.claude/settings.json` contains `statusLine` config pointing to local script
3. Local settings match the format used in global `~/.claude/settings.json`

---

### Permission Files

**Source:** `claudecodeoptimizer/content/permissions/`

| Level | Source File | Description |
|-------|-------------|-------------|
| Safe | `permissions/safe.json` | Most restrictive - read-only auto-approved |
| Balanced | `permissions/balanced.json` | Read + lint/test auto-approved, writes require approval |
| Permissive | `permissions/permissive.json` | Most operations auto-approved, only dangerous ops blocked |

**Target:** `./.claude/settings.json` → `permissions` key

**Permission Structure:**
```json
{
  "permissions": {
    "allow": [
      "# Allowed patterns - auto-approved",
      "git status *",
      "npm test"
    ],
    "deny": [
      "# Denied patterns - blocked or require approval",
      "rm -rf *",
      "git push --force *"
    ]
  }
}
```

**Permission Levels Summary:**

| Category | Safe | Balanced | Permissive |
|----------|------|----------|------------|
| Git read (status, log, diff) | Auto | Auto | Auto |
| Git write (commit, push) | Ask | Ask | Auto |
| Git dangerous (force push, reset --hard) | Deny | Deny | Deny |
| Lint/Format (check mode) | Ask | Auto | Auto |
| Lint/Format (write mode) | Ask | Ask | Auto |
| Test execution | Ask | Auto | Auto |
| Package install | Ask | Ask | Auto |
| File read (ls, cat) | Auto | Auto | Auto |
| File write (touch, mkdir) | Ask | Ask | Auto |
| File delete (rm) | Ask | Ask | Ask |
| File delete recursive (rm -rf) | Deny | Deny | Deny |
| Docker (non-privileged) | Ask | Ask | Auto |
| Docker (privileged) | Deny | Deny | Deny |
| System (sudo, chmod 777) | Deny | Deny | Deny |

### Permission Verification

After writing permission config, verify:
1. `./.claude/settings.json` contains valid `permissions` object
2. No conflicting patterns (same pattern in both allow and deny)
3. JSON syntax is valid

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
│                 Universal + AI-Specific + Project-Specific      │
│                 (CCO-Specific excluded - not portable)          │
│                                                                 │
│ ○ CLAUDE.md     For sharing with other Claude Code projects     │
│                 All categories including CCO-Specific           │
└─────────────────────────────────────────────────────────────────┘
```

### Export Content by Format

| Category | AGENTS.md | CLAUDE.md |
|----------|-----------|-----------|
| Universal | Included | Included |
| AI-Specific | Included | Included |
| CCO-Specific | **Excluded** | Included |
| Project-Specific | Included (triggered only) | Included (triggered only) |

### AGENTS.md Format (Prose)

```markdown
# Project Standards

> Exported from CCO (ClaudeCodeOptimizer)

## Project Context
{type} project built with {stack}
Team: {team} | Scale: {scale} | Data: {data}

## Universal Standards
{all universal standards}

## AI-Specific Standards
{all AI-specific standards}

## Project-Specific Standards
{triggered standards only}
```

### CLAUDE.md Format

Exports the full CCO_CONTEXT block including CCO-Specific standards for use in other Claude Code projects.

---

## Standards Count Structure

Standards are organized in 4 categories:

| Category | Source File | Count | Scope |
|----------|-------------|-------|-------|
| Universal | `cco-standards.md` | ~47 | All projects |
| AI-Specific | `cco-standards.md` | ~31 | All AI assistants |
| CCO-Specific | `cco-standards.md` | ~23 | CCO users only |
| Project-Specific | `cco-standards-conditional.md` | ~108 | Triggered by detection |

**Base standards:** Universal + AI-Specific + CCO-Specific = ~101 standards
**Project-specific:** Up to ~108 additional standards based on detected features

**Count calculation:**
- Count `^- ` lines in each standards file section
- Tables count as guidance, not individual standards
- Counts are approximate and may change as standards evolve

---

## Detection → Standards Mapping

| Detection | Category |
|-----------|----------|
| Data: PII/Regulated OR Scale: 10K+ OR Compliance != None | Security & Compliance |
| Scale: 10K+ OR Microservices OR Scale: 100+ | Scale & Architecture |
| API OR DB OR CI/CD detected | Backend Services |
| Frontend detected (React/Vue/Angular/Svelte/etc.) | Frontend |
| Mobile OR Desktop OR CLI detected | Apps |
| Type: library | Library |
| Container/K8s OR Serverless OR Monorepo detected | Infrastructure |
| ML/AI OR Game engine detected | Specialized |
| Team: 2+ OR i18n detected | Collaboration |

Standard counts calculated dynamically at runtime from source files.

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
