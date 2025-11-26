# ADR-001: Marker-based CLAUDE.md System

## Status
Accepted

## Context

ClaudeCodeOptimizer needs to inject minimal CCO Rules (~350 tokens) into the user's `~/.claude/CLAUDE.md` file without requiring manual editing. The system must support:

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
<!-- CCO_RULES_START -->
# CCO Rules

1. **Cross-Platform**: Forward slashes, relative paths, Git Bash commands
2. **Reference Integrity**: Find ALL refs before delete/rename/move/modify
3. **Verification**: Accounting formula: total = completed + skipped + failed + cannot-do
4. **File Discovery**: files_with_matches → content with -C → Read offset+limit
5. **Change Safety**: Commit before bulk changes, max 10 files per batch
6. **Scope Control**: Define boundaries, one change = one purpose
<!-- CCO_RULES_END -->
```

### Key Implementation Details

1. **Marker Format**: HTML comments that are invisible in rendered markdown
2. **Single Section**: One marker section for CCO Rules (~350 tokens)
3. **Line-based Replacement**: Find start/end markers, replace content between them
4. **Preservation**: Content outside markers is never touched
5. **Validation**: Verify markers exist before injection, create if missing
6. **Legacy Support**: Handle old CCO_PRINCIPLES markers for backward compatibility

### Marker Section

- `CCO_RULES_START/END`: Minimal inline rules (~350 tokens)
- Legacy: `CCO_PRINCIPLES_START/END` (removed on upgrade)

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

    if "CCO_RULES_START" not in content:
        content += "\n<!-- CCO_RULES_START -->\n<!-- CCO_RULES_END -->\n"

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

    # Remove CCO Rules section
    content = remove_between_markers(
        content,
        "<!-- CCO_RULES_START -->",
        "<!-- CCO_RULES_END -->"
    )

    # Remove legacy principles section (backward compatibility)
    content = remove_between_markers(
        content,
        "<!-- CCO_PRINCIPLES_START -->",
        "<!-- CCO_PRINCIPLES_END -->"
    )

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

- [CCO Installation Documentation](../runbooks/installation.md)

## Related ADRs

- [ADR-002: Zero Pollution Design](002-zero-pollution-design.md) - Explains why all content goes in `~/.claude/`
