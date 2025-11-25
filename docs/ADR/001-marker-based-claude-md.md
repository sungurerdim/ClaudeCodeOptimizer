# ADR-001: Marker-based CLAUDE.md System

## Status
Accepted

## Context

ClaudeCodeOptimizer needs to inject content (commands, skills, agents, principles) into the user's `~/.claude/CLAUDE.md` file without requiring manual editing. The system must support:

1. **Automatic Updates**: When CCO is updated, new content should automatically appear in CLAUDE.md
2. **User Preservation**: User-written content outside CCO sections must be preserved
3. **Clean Removal**: When CCO is uninstalled, all CCO content should be cleanly removed
4. **Idempotency**: Running install multiple times should not duplicate content
5. **Versioning**: Different CCO versions may have different content

### Forces at Play

- **User Control**: Users should own their CLAUDE.md file and be able to edit it freely
- **Automation**: Manual editing for every update is error-prone and tedious
- **Transparency**: Users should clearly see what is CCO-managed vs their own content
- **Safety**: System must not corrupt or lose user data
- **Simplicity**: Implementation should be maintainable and debuggable

### Constraints

- CLAUDE.md is a markdown file (limited programmatic manipulation)
- Must work across platforms (Windows, macOS, Linux)
- No database or complex state management
- Users may edit CLAUDE.md while CCO is installed

## Decision

Implement a **marker-based injection system** using HTML comment markers:

```markdown
<!-- CCO_PRINCIPLES_START -->
@principles/cco-principle-u-change-verification.md
@principles/cco-principle-u-cross-platform-compatibility.md
@principles/cco-principle-u-dry.md
@principles/cco-principle-u-evidence-based-analysis.md
@principles/cco-principle-u-follow-patterns.md
@principles/cco-principle-u-minimal-touch.md
@principles/cco-principle-u-no-hardcoded-examples.md
@principles/cco-principle-u-no-overengineering.md
@principles/cco-principle-c-context-window-mgmt.md
@principles/cco-principle-c-efficient-file-operations.md
@principles/cco-principle-c-native-tool-interactions.md
@principles/cco-principle-c-no-unsolicited-file-creation.md
@principles/cco-principle-c-project-context-discovery.md
<!-- CCO_PRINCIPLES_END -->
```

### Key Implementation Details

1. **Marker Format**: HTML comments that are invisible in rendered markdown
2. **Content Sections**: Separate markers for each content type (principles, commands, skills, agents)
3. **Line-based Replacement**: Find start/end markers, replace content between them
4. **Preservation**: Content outside markers is never touched
5. **Validation**: Verify markers exist before injection, create if missing

### Marker Sections

- `CCO_PRINCIPLES_START/END`: User-selected and Claude-selected principles
- `CCO_COMMANDS_START/END`: Available slash commands
- `CCO_SKILLS_START/END`: Auto-activating skills
- `CCO_AGENTS_START/END`: Available agents

## Consequences

### Positive

- **Automatic Updates**: Content updates automatically when CCO is updated
- **User Transparency**: Markers clearly delineate CCO-managed sections
- **Safe Uninstall**: Removing markers cleanly removes all CCO content
- **Idempotent**: Running install multiple times produces same result
- **User Freedom**: Users can edit content outside markers freely
- **Simple Implementation**: Straightforward string manipulation
- **Platform Independent**: Works identically on all platforms
- **No Database**: No separate state to maintain or sync

### Negative

- **Manual Marker Setup**: Users must add markers to CLAUDE.md initially (mitigated by installer)
- **Corruption Risk**: If user deletes markers, system can't update that section
- **Order Dependent**: Content order within markers is determined by CCO, not user
- **Merge Conflicts**: Git merge conflicts possible if markers change between branches

### Neutral

- **Visibility**: Markers visible in raw markdown (not in rendered view)
- **Coupling**: CLAUDE.md structure coupled to CCO's content organization
- **Testing**: Requires file system testing (tmp_path fixtures)

## Alternatives Considered

### Alternative 1: Manual Editing Instructions

**Description**: Provide instructions for users to manually copy-paste content into CLAUDE.md

**Why Rejected**:
- Error-prone (users make typos, miss sections)
- Time-consuming (every update requires manual work)
- No way to cleanly remove content on uninstall
- Difficult to version (no way to know what's installed)
- Poor user experience

### Alternative 2: Complete File Replacement

**Description**: CCO completely owns CLAUDE.md and replaces it on every install

**Why Rejected**:
- Destroys user content
- No way for users to customize their CLAUDE.md
- Violates principle of user control
- Breaking change for existing users
- Data loss risk

### Alternative 3: Append-Only System

**Description**: Append new content to end of CLAUDE.md on each install

**Why Rejected**:
- Duplicates content on repeated installs
- No way to update existing content
- No way to remove content on uninstall
- File grows unbounded
- Cluttered and confusing

### Alternative 4: Separate File Includes

**Description**: Keep CCO content in separate files and use `@include` syntax

**Why Rejected**:
- Requires Claude Code to support include syntax (not guaranteed)
- More complex file management
- Harder for users to see full context
- Debugging more difficult
- Still needs markers or similar mechanism

### Alternative 5: JSON/YAML Configuration

**Description**: Use structured format instead of markdown markers

**Why Rejected**:
- CLAUDE.md must be markdown (Claude Code requirement)
- Would require separate config file
- More complex parsing
- Harder for users to read/edit
- Adds complexity without clear benefit

## Implementation Notes

### Marker Creation

```python
def ensure_markers_exist(claude_md_path: Path) -> None:
    """Add CCO markers if they don't exist"""
    content = claude_md_path.read_text()

    if "CCO_PRINCIPLES_START" not in content:
        content += "\n<!-- CCO_PRINCIPLES_START -->\n<!-- CCO_PRINCIPLES_END -->\n"

    claude_md_path.write_text(content)
```

### Content Injection

```python
def inject_content(claude_md_path: Path, marker: str, content: str) -> None:
    """Inject content between markers"""
    lines = claude_md_path.read_text().splitlines()

    start_marker = f"<!-- CCO_{marker}_START -->"
    end_marker = f"<!-- CCO_{marker}_END -->"

    start_idx = find_marker(lines, start_marker)
    end_idx = find_marker(lines, end_marker)

    new_lines = (
        lines[:start_idx + 1] +
        content.splitlines() +
        lines[end_idx:]
    )

    claude_md_path.write_text("\n".join(new_lines))
```

### Clean Removal

```python
def remove_cco_content(claude_md_path: Path) -> None:
    """Remove all CCO markers and content"""
    content = claude_md_path.read_text()

    # Remove each marker section
    for marker in ["PRINCIPLES", "COMMANDS", "SKILLS", "AGENTS"]:
        start = f"<!-- CCO_{marker}_START -->"
        end = f"<!-- CCO_{marker}_END -->"
        content = remove_between_markers(content, start, end)

    claude_md_path.write_text(content)
```

### Testing Approach

- Use `tmp_path` pytest fixture for isolated testing
- Test marker creation in empty files
- Test content injection with existing markers
- Test preservation of user content
- Test removal/uninstall workflow
- Test repeated installs (idempotency)

### Migration Considerations

- Version 1.0 users: Add markers to existing CLAUDE.md
- Provide migration script for pre-marker installations
- Backup CLAUDE.md before first marker injection
- Clear documentation on marker format and purpose

## References

- [cco-principle-u-no-hardcoded-examples](../../claudecodeoptimizer/content/principles/cco-principle-u-no-hardcoded-examples.md)
- [CCO Installation Documentation](../runbooks/installation.md)
- [GitHub Issue: CLAUDE.md Management](#) (if applicable)

## Related ADRs

- [ADR-002: Zero Pollution Design](002-zero-pollution-design.md) - Explains why all content goes in `~/.claude/`
- [ADR-003: Progressive Skill Loading](003-progressive-skill-loading.md) - How skills are auto-activated via CLAUDE.md
