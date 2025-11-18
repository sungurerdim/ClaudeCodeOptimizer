---
name: cco-hooks
description: Manage Claude Code hooks for automated quality checks and protection
action_type: configuration
---

# CCO Hooks

**Manage automated hooks for quality checks and protection. Toggle hooks on/off with a single command.**

---

## Design Principles

1. **No Default Hooks** - All hooks are opt-in, nothing forced
2. **Toggle Interface** - Multiselect list shows current state, easy to change
3. **Zero Manual Editing** - No need to edit settings.json
4. **Reversible** - Easy to disable what you enabled

---

## Available Hooks

### PreToolUse (Before Action)

| Hook | Description | Use Case |
|------|-------------|----------|
| **secrets-guard** | Block access to .env, credentials, API keys | Prevent accidental secret exposure |
| **dangerous-cmd-guard** | Block rm -rf, DROP DATABASE, etc. | Prevent destructive accidents |

### PostToolUse (After Edit)

| Hook | Description | Use Case |
|------|-------------|----------|
| **auto-lint** | Run linter after file edit | Catch style issues immediately |
| **auto-typecheck** | Run type checker after edit | Catch type errors immediately |
| **auto-format** | Run formatter after edit | Keep code formatted |

---

## Execution Protocol

### Step 1: Read Current State

```python
# Read ~/.claude/settings.json to get current hooks
current_hooks = read_settings()
active_hooks = parse_active_hooks(current_hooks)
```

### Step 2: Present Toggle Interface

```python
AskUserQuestion({
  questions: [
    {
      question: "Select PreToolUse hooks (protection before actions):",
      header: "Protection",
      multiSelect: true,
      options: [
        {
          label: "secrets-guard",
          description: "Block access to .env, credentials, API keys | Prevents accidental exposure"
        },
        {
          label: "dangerous-cmd-guard",
          description: "Block rm -rf, DROP DATABASE, etc. | Prevents destructive commands"
        }
      ]
    },
    {
      question: "Select PostToolUse hooks (automation after edits):",
      header: "Automation",
      multiSelect: true,
      options: [
        {
          label: "auto-lint",
          description: "Run linter (ruff/eslint) after edit | Catch style issues"
        },
        {
          label: "auto-typecheck",
          description: "Run type checker (mypy/tsc) after edit | Catch type errors"
        },
        {
          label: "auto-format",
          description: "Run formatter (black/prettier) after edit | Keep formatted"
        }
      ]
    }
  ]
})
```

**IMPORTANT:** Pre-select options that are currently active in settings.json

### Step 3: Apply Changes

```python
# Compare selection with current state
selected = get_user_selection()
to_enable = selected - active_hooks
to_disable = active_hooks - selected

# Update settings.json
update_hooks(to_enable, to_disable)

# Show summary
print_summary(to_enable, to_disable)
```

### Step 4: Show Summary

```markdown
## Hooks Updated

**Enabled:**
- auto-lint
- auto-typecheck

**Disabled:**
- dangerous-cmd-guard

**Current Active Hooks:**
- secrets-guard (was already active)
- auto-lint (newly enabled)
- auto-typecheck (newly enabled)

Hooks are now active. They will run automatically during your session.
```

---

## Hook Implementations

### secrets-guard (PreToolUse)

```json
{
  "matcher": "Edit|Write|Read",
  "hooks": [
    {
      "type": "command",
      "command": "python -c \"import sys,json,re; d=json.load(sys.stdin); f=d.get('tool_input',{}).get('file_path',''); p=['.env','.env.','/credentials','/secrets','/apikey','id_rsa','.pem','.key']; blocked=any(x in f.lower() for x in p); print(json.dumps({'decision':'block','reason':f'Protected file: {f}'} if blocked else {'decision':'allow'}))\""
    }
  ]
}
```

**Protected patterns:**
- `.env`, `.env.*`
- `*credentials*`, `*secrets*`, `*apikey*`
- `id_rsa`, `*.pem`, `*.key`

### dangerous-cmd-guard (PreToolUse)

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "python -c \"import sys,json; d=json.load(sys.stdin); c=d.get('tool_input',{}).get('command',''); dangerous=['rm -rf /','rm -rf ~','DROP DATABASE','DROP TABLE','truncate','--no-preserve-root',':(){:|:&};:']; blocked=any(x in c for x in dangerous); print(json.dumps({'decision':'block','reason':f'Dangerous command blocked: {c[:50]}'} if blocked else {'decision':'allow'}))\""
    }
  ]
}
```

**Blocked patterns:**
- `rm -rf /`, `rm -rf ~`
- `DROP DATABASE`, `DROP TABLE`, `truncate`
- `--no-preserve-root`
- Fork bombs

### auto-lint (PostToolUse)

```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "python -c \"import sys,json,subprocess,os; d=json.load(sys.stdin); f=d.get('tool_input',{}).get('file_path',''); ext=os.path.splitext(f)[1]; cmd={'py':'ruff check --fix','js':'eslint --fix','ts':'eslint --fix'}.get(ext[1:]); r=subprocess.run(cmd.split()+[f],capture_output=True,text=True) if cmd else None; print(json.dumps({'decision':'allow'}))\""
    }
  ]
}
```

**Supported:**
- Python → ruff
- JavaScript/TypeScript → eslint

### auto-typecheck (PostToolUse)

```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "python -c \"import sys,json,subprocess,os; d=json.load(sys.stdin); f=d.get('tool_input',{}).get('file_path',''); ext=os.path.splitext(f)[1]; cmd={'py':'mypy --ignore-missing-imports','ts':'tsc --noEmit'}.get(ext[1:]); r=subprocess.run(cmd.split()+[f],capture_output=True,text=True) if cmd else None; o=r.stdout if r and r.returncode!=0 else ''; print(json.dumps({'decision':'allow','systemMessage':o} if o else {'decision':'allow'}))\""
    }
  ]
}
```

**Supported:**
- Python → mypy
- TypeScript → tsc

### auto-format (PostToolUse)

```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "python -c \"import sys,json,subprocess,os; d=json.load(sys.stdin); f=d.get('tool_input',{}).get('file_path',''); ext=os.path.splitext(f)[1]; cmd={'py':'ruff format','js':'prettier --write','ts':'prettier --write'}.get(ext[1:]); subprocess.run(cmd.split()+[f],capture_output=True) if cmd else None; print(json.dumps({'decision':'allow'}))\""
    }
  ]
}
```

**Supported:**
- Python → ruff format
- JavaScript/TypeScript → prettier

---

## Settings File Location

Hooks are stored in: `~/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      // secrets-guard, dangerous-cmd-guard
    ],
    "PostToolUse": [
      // auto-lint, auto-typecheck, auto-format
    ]
  }
}
```

---

## CLI Usage

### Interactive (Default)

```bash
/cco-hooks
```

Shows multiselect interface with current state.

### Quick Enable/Disable

```bash
# Enable specific hooks
/cco-hooks --enable secrets-guard,auto-lint

# Disable specific hooks
/cco-hooks --disable auto-format

# Show current status only
/cco-hooks --status

# Disable all hooks
/cco-hooks --disable-all
```

---

## Parametrized Mode

When called with parameters, skip AskUserQuestion:

```python
if args.enable:
    hooks_to_enable = parse_hooks(args.enable)
    enable_hooks(hooks_to_enable)

if args.disable:
    hooks_to_disable = parse_hooks(args.disable)
    disable_hooks(hooks_to_disable)

if args.status:
    show_current_hooks()

if args.disable_all:
    disable_all_hooks()
```

---

## Output Examples

### Status Output

```markdown
## CCO Hooks Status

**Active Hooks:**

PreToolUse (Protection):
- secrets-guard ✓

PostToolUse (Automation):
- auto-lint ✓
- auto-typecheck ✓

**Inactive Hooks:**
- dangerous-cmd-guard
- auto-format

Run `/cco-hooks` to change.
```

### After Toggle

```markdown
## Hooks Updated

**Changes:**
- ✓ Enabled: auto-format
- ✗ Disabled: auto-typecheck

**Now Active:**
- secrets-guard
- auto-lint
- auto-format

Hooks are active for this and future sessions.
```

---

## Important Notes

### Tool Requirements

Hooks require these tools to be installed:

| Hook | Required Tool | Install |
|------|--------------|---------|
| auto-lint (Python) | ruff | `pip install ruff` |
| auto-lint (JS/TS) | eslint | `npm install -g eslint` |
| auto-typecheck (Python) | mypy | `pip install mypy` |
| auto-typecheck (TS) | tsc | `npm install -g typescript` |
| auto-format (Python) | ruff | `pip install ruff` |
| auto-format (JS/TS) | prettier | `npm install -g prettier` |

If tool is not installed, hook silently skips (no error).

### Performance Considerations

- **auto-lint**: Fast (<1s per file)
- **auto-typecheck**: Medium (1-3s per file)
- **auto-format**: Fast (<1s per file)

PostToolUse hooks run after every Edit/Write, so consider performance impact.

### Scope

Hooks apply to all projects (global `~/.claude/settings.json`).

---

## Success Criteria

- [ ] Current hooks detected from settings.json
- [ ] Multiselect shows active hooks pre-selected
- [ ] Selection updates settings.json correctly
- [ ] Summary shows what changed
- [ ] Parametrized mode works without interaction
