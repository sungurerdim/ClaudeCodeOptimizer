# CCO Project Structure

**"What does CCO actually do to my project?"**

CCO follows a **zero-pollution philosophy** - all data lives in global storage, projects only contain symlinks.

## Project Directory Changes

CCO creates only `.claude/` directory with links using [preference order](architecture.md#linking-strategy):

**What gets created in your project:**
- `CLAUDE.md` - Minimal guide with principle references
- `.claude/principles/` - Links to 34-54 selected principles (14 universal + 20-40 project-specific)
- `.claude/commands/` - Links to 8-15 selected commands
- `.claude/guides/` - Links to relevant guides
- `.claude/skills/` - Links to language-specific skills
- `.claude/agents/` - Links to task agents (if any)

**That's it!** No `.cco/` directory, no duplication, zero pollution.

> **See**: [Architecture → Directory Structure](architecture.md#directory-structure) for complete directory trees

## Global Storage (`~/.cco/`)

All actual CCO data lives in global storage (one-time installation):

**Contains:**
- 83 principles (14 universal U001-U014 + 69 project-specific P001-P069)
- 28 slash commands
- 5 comprehensive guides
- 23 skills (18 language-specific + 5 cross-language)
- 3 task agents (audit, fix, generate)
- Project registries and configuration

> **See**: [Architecture → Global CCO Storage](architecture.md#directory-structure) for complete structure

## What Gets Committed to Git?

**Recommended** (team collaboration):
- ✅ `.claude/commands/` - Links (team sees which commands are active)
- ✅ `.claude/principles/` - Links (team follows same principles: U*.md + selected P*.md)
- ✅ `.claude/guides/` - Links (team uses same guides)
- ✅ `.claude/skills/` - Links (team uses same skills)
- ✅ `CLAUDE.md` - Project guide (team reference)
- [Optional] `settings.json.template` - Example configuration (not auto-deployed)

**Optional** (add to `.gitignore` if preferred):
- ❌ `.claude/` - If you want CCO to be personal preference only
- ❌ `CLAUDE.md` - If you have existing project docs

## Removal

CCO is designed for easy, clean removal:

### Option 1: Remove from Project (Recommended - keeps global installation)

```bash
/cco-remove
```

**What `/cco-remove` does:**
1. Removes all CCO-created links:
   - `.claude/commands/cco-*.md` (symlinks/hardlinks/copies)
   - `.claude/principles/` (all linked principle files: U*.md + P*.md)
   - `.claude/guides/` (all linked guide files)
   - `.claude/skills/` (all linked skill files)
   - `.claude/agents/` (all linked agent files, if any)
2. Optionally removes CCO section from `CLAUDE.md`:
   - Removes content between `<!-- CCO_START -->` and `<!-- CCO_END -->`
   - Preserves existing project-specific content
   - Asks for confirmation
3. Does not remove user-customized `.claude/settings.json` if present (created manually)
4. Removes project registry from `~/.cco/projects/<project>.json`
5. Displays removal summary
6. Keeps global `~/.cco/` intact (ready for other projects)

**Uninstall Safety:**
- If CCO section not removed from CLAUDE.md, broken principle references are ignored by Claude (no errors)
- Project continues to work without CCO
- No backup needed (removal is clean, non-destructive)

### Option 2: Manual Project Removal

```bash
# Remove all CCO links and files
rm -rf .claude/commands/cco-*.md       # Remove command links
rm -rf .claude/principles/              # Remove principle links (U*.md + P*.md)
rm -rf .claude/guides/                  # Remove guide links
rm -rf .claude/skills/                  # Remove skill links
rm -rf .claude/agents/                  # Remove agent links (if any)
# rm .claude/settings.json                # Only if you created it manually

# Remove CCO section from CLAUDE.md (optional)
# Manually delete lines between <!-- CCO_START --> and <!-- CCO_END -->

# Remove project registry
rm ~/.cco/projects/<project-name>.json
```

### Option 3: Complete CCO Uninstall (Removes from all projects)

```bash
# Uninstall Python package
pip uninstall claudecodeoptimizer

# Remove global CCO installation
rm -rf ~/.cco/

# Remove global commands from Claude
rm ~/.claude/commands/cco-init.md
rm ~/.claude/commands/cco-remove.md
```

## Important Notes

- `/cco-remove` is clean and non-destructive (no backups needed)
- Removal does not affect non-CCO files in `.claude/`
- Broken principle references in CLAUDE.md are safely ignored by Claude (no errors)
- Global `~/.cco/` can be reused for other projects
- Team members can remove CCO independently (links are local)

**Key benefit**: Updating CCO (`pip install -U claudecodeoptimizer`) automatically updates all projects that use symlinks or hardlinks (copies require re-init).
