---
description: Complete CCO removal (local + global cleanup)
cost: 0
principles: ['U_EVIDENCE_BASED', 'U_FAIL_FAST']
---

# CCO Complete Removal

Remove CCO from the current project and/or global installation.

**Three removal scopes:**
- **local**: Remove CCO from current project only (default)
- **global**: Remove entire `~/.cco/` directory
- **both**: Complete removal (project + global + ~/.claude/commands/)

## Quick Removal (Local Only)

Remove CCO from current project:

```python
from pathlib import Path
from claudecodeoptimizer.core.remove import remove_cco

result = remove_cco(
    project_root=Path.cwd(),
    scope="local",
    clean_claude_md=True  # Remove CCO markers from CLAUDE.md
)

print(f"✓ {result['actions']}")
```

## Complete Removal (Everything)

Remove CCO entirely (project + global):

```python
from pathlib import Path
from claudecodeoptimizer.core.remove import remove_cco

result = remove_cco(
    project_root=Path.cwd(),
    scope="both",  # Remove local + global
    clean_claude_md=True
)

print(f"✓ Removed: {', '.join(result['actions'])}")
```

## What Gets Removed

### Local Removal (scope="local"):
- ✓ All CCO symlinks from `.claude/`
  - `commands/cco-*.md`
  - `principles/*.md` (all U_*, C_*, P_*)
  - `guides/cco-*.md`
  - `skills/cco-*.md`
  - `agents/cco-*.md`
- ✓ CCO markers from `CLAUDE.md` (if `clean_claude_md=True`)

### Global Removal (scope="global"):
- ✓ Entire `~/.cco/` directory
- ✓ `~/.claude/commands/cco-init.md`
- ✓ `~/.claude/commands/cco-remove.md`

### Both (scope="both"):
- ✓ Everything from local + global

## What Stays Untouched

- ✓ Python package (use `pip uninstall claudecodeoptimizer` separately)
- ✓ Your `.claude/settings.json` and other custom files
- ✓ All your source code
- ✓ Git history
- ✓ Original CLAUDE.md content (outside CCO markers)

## Interactive Mode (Recommended)

Ask user for confirmation:

```python
from pathlib import Path
from claudecodeoptimizer.core.remove import CCORemover

# Ask user via AskUserQuestion tool
answers = AskUserQuestion({
    "questions": [{
        "question": "What do you want to remove?",
        "header": "Removal Scope",
        "multiSelect": false,
        "options": [
            {
                "label": "Current project only",
                "description": "Keep CCO installed, remove from this project"
            },
            {
                "label": "Everything (project + global)",
                "description": "Complete removal - CCO will be uninstalled"
            }
        ]
    }]
})

scope = "local" if "project only" in answers else "both"

remover = CCORemover(Path.cwd())
result = remover.remove(scope=scope, clean_claude_md=True)

print(f"✓ Removal complete: {result['actions']}")
```

## Verification

After removal, verify clean state:

```bash
# Check local
ls .claude/commands/cco-*.md  # Should be empty

# Check global (if scope was "global" or "both")
ls ~/.cco/  # Should not exist

# Check CLAUDE.md
grep "CCO_PRINCIPLES_START" CLAUDE.md  # Should be empty
```

## Reinstall Later

To add CCO back:

```bash
/cco-init
```

**Note:** No state is saved - you'll reconfigure from scratch (AI auto-detection).

## Troubleshooting

**If removal fails:**

1. Check permissions:
   ```bash
   ls -la .claude/
   ```

2. Manual cleanup:
   ```python
   import shutil
   from pathlib import Path

   # Remove local
   for file in Path(".claude").rglob("cco-*"):
       file.unlink(missing_ok=True)

   # Remove global
   shutil.rmtree(Path.home() / ".cco", ignore_errors=True)
   ```

3. Check if CCO is installed:
   ```bash
   pip show claudecodeoptimizer
   ```

## See Also

- `/cco-init` - Reinitialize CCO
- `/cco-status` - Check CCO installation status
