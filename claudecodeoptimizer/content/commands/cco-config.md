---
name: cco-config
description: Configure statusline and permissions
---

# /cco-config

Configure Claude Code settings globally or per-project.

## Step 1: Scope Selection

AskUserQuestion:
→ **Global** (~/.claude/) - Applies to all projects
→ **Local** (./.claude/) - This project only

---

## Step 2: Conflict Detection

After scope selection, check for conflicts between global and local:

### If Local selected but Global has settings:
Check ~/.claude/ for existing statusline.js or settings.json permissions.
If found, inform user: "Global settings exist and will be overridden by local settings."

### If Global selected but Local has settings:
Check ./.claude/ for existing statusline.js or settings.json permissions.
If found:
AskUserQuestion:
→ **Continue** - Local will still override global for this project
→ **Sync to Local** - Copy global changes to local too
→ **Remove Local** - Delete local settings, use global only

---

## Step 3: Feature Selection

AskUserQuestion with multiSelect=true:
→ [ ] Statusline (terminal status display)
→ [ ] Permissions (auto-allow safe commands)

---

## Statusline

Target path: `{scope}/statusline.js`

### If statusline.js NOT exists in target scope:
1. Write statusline.js to target scope
2. Add statusLine config to settings.json (preserve other settings)

### If statusline.js EXISTS in target scope:
AskUserQuestion:
→ Cancel (keep existing)
→ Prepend (add new above existing)
→ Append (add new below existing)
→ Replace (backup existing as statusline.js.bak, use new)

### Cross-Scope Statusline Conflict
If BOTH global and local statusline.js exist when configuring:
AskUserQuestion:
→ **Keep Both** - Local overrides global (normal behavior)
→ **Unify to Global** - Delete local, configure global only
→ **Unify to Local** - Delete global, configure local only

---

## Permissions

Target path: `{scope}/settings.json`

### Permission Levels

AskUserQuestion:
→ **Safe** - Maximum security, read-only operations
→ **Balanced** - Normal development workflow (recommended)
→ **Permissive** - Minimal prompts, trust all operations

#### Safe Mode
```
allow: Read, Glob, Grep, WebSearch, WebFetch, Task
ask: Write, Edit, all Bash commands
deny: (dangerous commands)
```

#### Balanced Mode (default)
```
allow: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Task
       Bash (read-only + project tools)
ask: Bash (install, delete, push)
deny: (dangerous commands)
```

#### Permissive Mode
```
allow: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Task
       Bash (most operations including delete)
ask: Bash (push, system commands)
deny: (dangerous commands)
```

### Always Deny (all modes, non-negotiable)

These are OS-independent and project-independent dangerous commands:

```json
"deny": [
  "Bash(rm -rf /*:*)",
  "Bash(rm -rf ~/*:*)",
  "Bash(rm -rf /:*)",
  "Bash(sudo:*)",
  "Bash(su :*)",
  "Bash(doas:*)",
  "Bash(git push --force:*)",
  "Bash(git push -f:*)",
  "Bash(git reset --hard:*)",
  "Bash(git clean -fdx:*)",
  "Bash(chmod -R 777:*)",
  "Bash(mkfs:*)",
  "Bash(dd if=/dev/:*)",
  "Bash(shutdown:*)",
  "Bash(reboot:*)",
  "Bash(kill -9 -1:*)",
  "Bash(:(){ :|:& };::*)",
  "Edit(**/.env)",
  "Edit(**/secrets/**)",
  "Edit(**/*.pem)",
  "Edit(**/*.key)",
  "Edit(**/.ssh/**)",
  "Edit(**/.aws/credentials)",
  "Write(**/.env)",
  "Write(**/secrets/**)",
  "Write(**/*.pem)",
  "Write(**/*.key)",
  "Read(**/.ssh/id_*)",
  "Read(**/.aws/credentials)",
  "Read(**/.env)"
]
```

### If settings.json EXISTS in target scope:

1. **Read** existing settings.json completely
2. **Preserve** all non-permission settings (statusLine, hooks, etc.)
3. **Analyze** existing allow/deny/ask lists:
   - Check if dangerous commands are properly denied
   - Check if selected mode's requirements are met
4. **Merge** changes:
   - Add missing items based on selected mode
   - Remove items that conflict with selected mode
   - Ensure always-deny list is complete
5. **Write** back with preserved structure

**Example merge logic:**
```
Existing allow: ["Read(./**)", "Bash(python:*)"]
Selected mode: Balanced
Detected stack: Python + pytest

Result allow: 
  - Keep: "Read(./**)", "Bash(python:*)"
  - Add: "Write(./**)", "Edit(./**)", "Bash(pytest:*)", "Bash(pip:*)"
```

### If settings.json NOT exists in target scope:

1. **Detect** project stack using detect-agent
2. **Generate** fresh permissions based on selected mode
3. **Write** new settings.json with only permissions section

### Cross-Scope Permission Conflict

If BOTH global and local settings.json have permissions:
AskUserQuestion:
→ **Keep Both** - Local overrides global (normal behavior)
→ **Merge to Global** - Combine both, delete local permissions
→ **Merge to Local** - Combine both, keep only in local
→ **Analyze Diff** - Show differences, then decide

---

## Pre-Write Validation

Before writing ANY config file, validate:

### settings.json Validation
1. **JSON Syntax** - Must be valid JSON (parseable)
2. **Schema Check** - Only known Claude Code keys allowed:
   - `permissions.allow[]`, `permissions.deny[]`, `permissions.ask[]`
   - `statusLine.command`
   - `hooks.*`
   - `mcpServers.*`
   - Warn (don't block) for unknown keys
3. **Rule Conflicts** - Same pattern cannot be in both allow and deny
4. **Security Check** - Dangerous commands must be in deny, not allow

### statusline.js Validation
1. **JavaScript Syntax** - Must be valid JS
2. **Export Check** - Must export a function or object

### On Validation Failure
```
Validation failed:
  ✗ JSON syntax error at line 15: unexpected token
  ✗ Conflict: "Bash(rm:*)" in both allow and deny
  ✗ Security: "Bash(sudo:*)" should be denied

Fix issues before saving? [Y/n]
```

If user confirms, auto-fix safe issues:
- Remove conflicts (keep in deny)
- Add missing dangerous command denials
- Cannot auto-fix syntax errors → show location, abort

---

## Usage

```bash
/cco-config                    # Interactive (scope + features)
/cco-config --global           # Global scope
/cco-config --local            # Local scope
/cco-config --statusline       # Statusline only
/cco-config --permissions      # Permissions only
/cco-config --permissions safe # Direct mode selection
```

## Important Rules

1. **NEVER modify** non-permission settings in settings.json
2. **ALWAYS preserve** existing structure and formatting
3. **ALWAYS include** dangerous command denials regardless of mode
4. **ONLY add/remove** items in allow/deny/ask arrays
5. **Backup** before any replacement operation
6. **Scope precedence**: Local always overrides Global for that project
7. **ALWAYS validate** before writing any config file
