---
description: Remove CCO from current project (keeps global installation)
cost: 0
principles: ['P001', 'P067', 'P071']
---

# CCO Project Removal

Remove CCO from the current project only. This does **NOT** affect:
- Global CCO installation
- Other projects using CCO
- Python package

**Run the removal command:**

```bash
python -m claudecodeoptimizer remove
```

The CLI will:
1. Check if project is initialized
2. Ask for confirmation
3. Remove all CCO files from `.claude/`
4. Unregister project from global registry

**That's it!** No AI agent needed - the Python CLI handles everything.

## What Gets Removed

From current project:
- All `cco-*.md` files from `.claude/commands/`
- `statusline.js` from `.claude/`
- Project entry from `~/.cco/projects/`

## What Stays Untouched

- Global CCO installation (`~/.cco/`)
- Python package (use `pip uninstall` to remove)
- Other `.claude/` files (settings, hooks, etc.)
- Your source code (untouched)
- Other projects using CCO

## Troubleshooting

**If command fails:**

1. Check if project is initialized:
   ```bash
   ls .claude/commands/cco-*.md
   ```

2. Check CCO is installed:
   ```bash
   python -c "import claudecodeoptimizer"
   ```

**Manual cleanup if needed:**
```bash
rm .claude/commands/cco-*.md
rm .claude/statusline.js
```

## Reinitialize Later

To add CCO back:
```bash
python -m claudecodeoptimizer init
```

Your previous configuration is **NOT** saved - you'll need to reconfigure.
