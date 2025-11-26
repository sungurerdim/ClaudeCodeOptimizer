# ADR-002: Zero Pollution Design

## Status
Accepted

## Context

ClaudeCodeOptimizer enhances Claude Code with additional commands and agents. The system needs to store this content somewhere accessible to Claude Code while avoiding project pollution.

### The Problem

Many development tools suffer from "project pollution":
- Configuration files in every project directory (`.eslintrc`, `.prettierrc`, etc.)
- Lock files committed to version control
- Tool-specific directories (`.vscode/`, `.idea/`)
- Build artifacts and caches

This creates:
- Repository clutter
- Merge conflicts
- Onboarding friction (what is this file?)
- Maintenance burden (update config in every project)

### Forces at Play

- **Accessibility**: Claude Code must be able to find CCO content
- **User Experience**: Projects should remain clean and focused
- **Portability**: CCO should work across all projects without per-project setup
- **Discoverability**: Users should know where CCO content is stored
- **Maintainability**: One place to update, all projects benefit
- **Uninstallability**: Clean removal should be trivial

### Constraints

- Claude Code reads from `~/.claude/` directory by default
- Users may have multiple projects
- Different projects may need different CCO configurations
- Must work on Windows, macOS, and Linux

## Decision

Adopt a **zero pollution design** where ALL CCO content is stored in `~/.claude/` globally, with NO files created in project directories.

### Key Principles

1. **Global Installation**: Everything in `~/.claude/`
2. **Project Cleanliness**: Zero CCO files in project directories
3. **Single Source**: One installation serves all projects
4. **Optional Overrides**: Per-project customization via `.claudecodeoptimizerrc` (user-created, not auto-generated)

### Directory Structure

```
~/.claude/
├── commands/         # CCO slash commands (cco-*.md)
├── agents/          # CCO agent definitions (cco-agent-*.md)
├── CLAUDE.md        # Main config (with CCO Rules markers)
└── *.cco            # Template files for user customization
```

Project directories remain **completely clean** - no CCO files.

## Consequences

### Positive

- **Zero Clutter**: Projects stay focused on project code
- **No Merge Conflicts**: No CCO files to conflict in version control
- **Instant Availability**: Install once, works in all projects
- **Clean Uninstall**: Delete `~/.claude/`, CCO is gone
- **Reduced Onboarding**: New developers don't see mysterious CCO files
- **Consistent Behavior**: Same CCO version across all projects
- **No Gitignore**: No need to add CCO files to `.gitignore`
- **Clear Ownership**: Obvious that CCO is global, not project-specific
- **Easy Updates**: Update once globally, all projects benefit

### Negative

- **Less Flexibility**: Harder to have different CCO versions per project
- **Global State**: Changes affect all projects simultaneously
- **Hidden Configuration**: Less obvious what tools are active in a project
- **Sharing Challenges**: Team members must individually install CCO
- **No Project Overrides**: Difficult to disable CCO for specific projects (by design)

### Neutral

- **Home Directory Dependency**: Relies on `~/.claude/` being writable
- **Discoverability**: Users must know to look in `~/.claude/` for config
- **Backup Considerations**: `~/.claude/` should be backed up separately from projects

## Alternatives Considered

### Alternative 1: Per-Project Installation

**Description**: Install CCO files in each project's `.claudecode/` directory

**Why Rejected**:
- Creates clutter in every project
- Requires per-project installation/updates
- Merge conflicts when team members have different versions
- Need to add `.claudecode/` to `.gitignore` in every repo
- Violates DRY principle (same config in many places)
- Harder to maintain (update N projects instead of 1)
- Onboarding overhead (what is this directory?)

### Alternative 2: Hybrid Approach

**Description**: Global installation with per-project overrides in `.claudecode/`

**Why Rejected**:
- Complexity: Two configuration locations to check
- Merge Strategy: Unclear which config wins
- Still creates project pollution (`.claudecode/` directory)
- Harder to debug (where is this setting coming from?)
- Users would overuse overrides, defeating global purpose
- More code to maintain

### Alternative 3: Single Config File in Project Root

**Description**: Single `.claudecoderc` file in project root

**Why Rejected**:
- Still creates project pollution (one file per project)
- Team conflicts (different members want different settings)
- Must be in `.gitignore` (another file to maintain)
- Doesn't scale to large teams
- Update burden (change in every project)

### Alternative 4: System-Wide Installation (/usr/local/ or C:\Program Files\)

**Description**: Install to system directories like `/usr/local/share/claudecode/`

**Why Rejected**:
- Requires elevated privileges (sudo/admin)
- More complex installation process
- Harder to uninstall cleanly
- Platform-specific paths
- User isolation issues (multiple users on same machine)
- Claude Code may not check these locations

### Alternative 5: Environment Variables Only

**Description**: Configure CCO entirely via environment variables

**Why Rejected**:
- Can't store complex content (commands, skills) in env vars
- Poor user experience (editing shell configs)
- Platform-specific (different shells on different OSes)
- Hard to debug (env vars scattered across files)
- No structure (flat key-value, not hierarchical)

## Implementation Notes

### Installation Process

```python
def install_cco_globally() -> None:
    """Install CCO to ~/.claude/"""
    home = Path.home()
    claude_dir = home / ".claude"

    # Create directory structure
    claude_dir.mkdir(exist_ok=True)
    (claude_dir / "commands").mkdir(exist_ok=True)
    (claude_dir / "agents").mkdir(exist_ok=True)

    # Copy content files
    copy_commands(claude_dir / "commands")
    copy_agents(claude_dir / "agents")

    # Update CLAUDE.md with CCO Rules markers
    update_claude_md(claude_dir / "CLAUDE.md")
```

### Uninstallation

```python
def uninstall_cco() -> None:
    """Clean uninstall - remove all CCO content"""
    home = Path.home()
    claude_dir = home / ".claude"

    # Remove CCO files only (cco-*.md, cco-agent-*.md)
    for f in (claude_dir / "commands").glob("cco-*.md"):
        f.unlink()
    for f in (claude_dir / "agents").glob("cco-*.md"):
        f.unlink()

    # Remove CCO Rules markers from CLAUDE.md
    remove_cco_markers(claude_dir / "CLAUDE.md")
```

### Testing Approach

- Use `tmp_path` fixtures to simulate `~/.claude/`
- **NEVER create files outside project root in tests**
- Test clean installation in empty `~/.claude/`
- Test upgrade from previous CCO version
- Test uninstall leaves no traces
- Verify project directories remain untouched

### Design Principles

- **No files in project directories**: Zero pollution
- **Minimal touch**: Only modify `~/.claude/`

## References

- [Installation Runbook](../runbooks/installation.md)
- [Uninstallation Runbook](../runbooks/uninstallation.md)

## Related ADRs

- [ADR-001: Marker-based CLAUDE.md System](001-marker-based-claude-md.md) - How content is injected into global CLAUDE.md
