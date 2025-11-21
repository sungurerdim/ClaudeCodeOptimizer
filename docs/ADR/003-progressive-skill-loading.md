# ADR-003: Progressive Skill Loading

## Status
Accepted

## Context

ClaudeCodeOptimizer provides specialized skills (auto-activating functions) that enhance Claude Code's capabilities. These skills need to be:

1. **Automatically Available**: No manual activation required
2. **Context-Aware**: Only load when relevant to current task
3. **Non-Intrusive**: Don't consume context when not needed
4. **Discoverable**: Users should know what skills are available
5. **Extensible**: Easy to add new skills

### The Problem

Traditional approaches to plugin/skill systems:

- **Always-On**: All skills loaded all the time (waste context tokens)
- **Manual Activation**: User must remember and type skill names (poor UX)
- **Static Loading**: Fixed set loaded at startup (not context-aware)
- **Configuration Heavy**: Requires complex config files

### Forces at Play

- **Context Window Limits**: Claude has finite context (200K tokens)
- **Performance**: Loading unused skills wastes tokens and time
- **User Experience**: Should "just work" without configuration
- **Discoverability**: Users need to know what's available
- **Flexibility**: Different tasks need different skills

### Constraints

- Claude Code reads CLAUDE.md at conversation start
- Skills defined in `~/.claude/skills/` directory
- Each skill is a markdown file with frontmatter
- Must work with ADR-001 (marker-based injection)

## Decision

Implement **progressive skill loading** using `use_cases` metadata in skill frontmatter:

1. **Metadata-Driven**: Each skill declares its `use_cases`
2. **Auto-Activation**: Claude Code automatically loads relevant skills
3. **Marker Injection**: Skills referenced in CLAUDE.md via CCO markers
4. **Context Matching**: Skills loaded when use_case matches current task

### Skill Structure

```markdown
---
title: Database Migration Skill
description: Automated database migration generation
category: development
use_cases:
  - "database schema changes"
  - "migration file generation"
  - "SQL DDL automation"
tags: [database, migration, sql]
---

# Database Migration Skill

When user requests database changes, automatically generate migration files...
```

### CLAUDE.md Integration

```markdown
<!-- CCO_SKILLS_START -->
@skills/database-migration.md
@skills/test-generation.md
@skills/api-documentation.md
<!-- CCO_SKILLS_END -->
```

### Progressive Loading

Claude Code loads ALL skills from CLAUDE.md at conversation start, but skills are written to be:
- **Self-Describing**: Clear use_cases in frontmatter
- **Lightweight**: Concise definitions
- **Lazy Activation**: Only "activate" (use) when context matches

## Consequences

### Positive

- **Zero Configuration**: Works out of the box
- **Context Efficient**: Skills are reference-loaded, not always-active
- **Discoverable**: All skills listed in CLAUDE.md
- **Extensible**: Add new skills by creating markdown files
- **Transparent**: Users can see available skills in CLAUDE.md
- **Flexible**: Easy to enable/disable via marker comments
- **Team Sharing**: Same skills available to whole team

### Negative

- **Startup Context**: All skill definitions loaded at conversation start (mitigated by concise writing)
- **Activation Overhead**: Claude must recognize when to use skill (mitigated by clear use_cases)
- **Discovery Delay**: Users might not know skill exists until they need it
- **No Runtime Loading**: Can't add skills mid-conversation (need to restart)

### Neutral

- **Skill Quality**: Effectiveness depends on clear use_cases and descriptions
- **Maintenance**: Adding skills requires updating both file and markers
- **Version Control**: Skills stored in `~/.claude/` not in project repo

## Alternatives Considered

### Alternative 1: Always-Active All Skills

**Description**: Load all skills as active functions at startup

**Why Rejected**:
- Wastes context tokens on unused skills
- Slower conversation startup
- Confusion (too many options always visible)
- Doesn't scale (adding skills increases cost linearly)

### Alternative 2: Manual Skill Activation

**Description**: User types `/activate-skill database-migration` to load skill

**Why Rejected**:
- Poor UX (must remember skill names)
- Breaks flow (stop to activate, then continue)
- Discovery problem (how do users know what exists?)
- Extra commands to learn
- Friction for every task

### Alternative 3: Directory-Based Auto-Loading

**Description**: Drop skill files in project directory, auto-load from there

**Why Rejected**:
- Violates ADR-002 (zero pollution design)
- Creates clutter in project directories
- Merge conflicts (team members with different skills)
- Need to add to `.gitignore`
- Per-project duplication

### Alternative 4: Skill Marketplace/Registry

**Description**: Central registry of skills, users install via `cco install skill-name`

**Why Rejected**:
- Requires server infrastructure
- Dependency on external service
- Versioning complexity
- Installation friction
- Network dependency
- Not needed for core CCO skills

### Alternative 5: Configuration File Skill Selection

**Description**: User edits `.claudecoderc` to list desired skills

**Why Rejected**:
- Configuration overhead
- Must restart to reload
- Easy to misconfigure
- Duplicates information (skills already in `~/.claude/skills/`)
- Violates zero-config principle

## Implementation Notes

### Skill Creation Template

```markdown
---
title: {SKILL_NAME}
description: {ONE_SENTENCE_DESCRIPTION}
category: {CATEGORY}
use_cases:
  - "{WHEN_TO_USE_1}"
  - "{WHEN_TO_USE_2}"
  - "{WHEN_TO_USE_3}"
tags: [{TAG1}, {TAG2}, {TAG3}]
metadata:
  complexity: low|medium|high
  token_cost: low|medium|high
---

# {SKILL_NAME}

## When to Use

This skill activates when:
- Use case 1
- Use case 2

## How it Works

1. Step 1
2. Step 2
3. Step 3

## Example

User: "Generate migration for adding email index"
Assistant: *uses database-migration skill to generate SQL*
```

### Installation Process

```python
def install_skills(claude_dir: Path) -> None:
    """Install skills to ~/.claude/skills/"""
    skills_dir = claude_dir / "skills"
    skills_dir.mkdir(exist_ok=True)

    # Copy skill files
    for skill_file in get_bundled_skills():
        target = skills_dir / skill_file.name
        target.write_text(skill_file.read_text())

    # Update CLAUDE.md markers
    update_skill_markers(claude_dir / "CLAUDE.md", skills_dir)
```

### Marker Update

```python
def update_skill_markers(claude_md: Path, skills_dir: Path) -> None:
    """Update CCO_SKILLS markers with current skills"""
    skill_files = sorted(skills_dir.glob("*.md"))

    skill_refs = [f"@skills/{f.name}" for f in skill_files]

    inject_content(
        claude_md,
        marker="SKILLS",
        content="\n".join(skill_refs)
    )
```

### Skill Discovery

Users can discover skills by:
1. Viewing CLAUDE.md (see all `@skills/` references)
2. Running `/cco-help` command (lists available skills)
3. Browsing `~/.claude/skills/` directory

### Testing Approach

- Test skill file parsing (frontmatter extraction)
- Test marker injection with multiple skills
- Test skill discovery commands
- Test adding/removing skills
- Verify CLAUDE.md updates correctly

### Principles Compliance

- **C_NO_UNSOLICITED_FILE_CREATION**: Skills only created in `~/.claude/`, not in projects
- **U_NO_OVERENGINEERING**: Simple file-based system, no database or complex state
- **U_FOLLOW_PATTERNS**: Skills follow consistent template and structure

## References

- [Skill Development Guide](../guides/skill-development.md) (if it exists)
- [CCO Skills Directory](../../claudecodeoptimizer/content/skills/)
- [MetadataManager Documentation](../../claudecodeoptimizer/core/metadata_manager.py)

## Related ADRs

- [ADR-001: Marker-based CLAUDE.md System](001-marker-based-claude-md.md) - How skills are injected into CLAUDE.md
- [ADR-002: Zero Pollution Design](002-zero-pollution-design.md) - Why skills are in `~/.claude/` not project directories

## Future Considerations

### Potential Enhancements

1. **Skill Analytics**: Track which skills are most used
2. **Skill Recommendations**: Suggest skills based on project type
3. **Skill Versioning**: Support multiple versions of same skill
4. **Skill Dependencies**: Skills that depend on other skills
5. **Community Skills**: User-contributed skill repository

### Migration Path

If we move beyond progressive loading:
- New ADR would supersede this one
- Migration guide for users
- Backward compatibility period
- Clear communication of changes
