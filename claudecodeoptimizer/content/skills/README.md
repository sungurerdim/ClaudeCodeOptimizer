# Custom Skills

This directory contains custom skill definitions for reusable workflows.

## What are Skills?

Skills are reusable workflows that can be invoked via slash commands. They provide structured processes for common development tasks.

## Creating a Custom Skill

1. **Copy the template:**
   ```bash
   cp _template-skill.md my-custom-skill.md
   ```

2. **Fill in the details:**
   - Skill name and use cases
   - Step-by-step process
   - Example outputs
   - Related skills/commands
   - Best practices and troubleshooting

3. **Test the skill:**
   Reference it in your project's CLAUDE.md:
   ```markdown
   - `/my-custom-skill` - @.claude/skills/my-custom-skill.md
   ```

## Skill Structure

```markdown
# Skill Name
## When to Use - Use cases
## Process - Step-by-step workflow
## Example Output - Expected results
## Related Skills - Connected workflows
## Best Practices - Tips
## Common Issues - Troubleshooting
```

## Best Practices

- **Clear workflow**: Define clear, sequential steps
- **Actionable**: Each step should have concrete actions
- **Examples**: Show example outputs
- **Error handling**: Include common issues and solutions
- **Related skills**: Link to complementary workflows

## Example Skills

You can create skills for:
- Code review workflow
- Deployment checklist
- API testing procedure
- Database backup process
- Performance profiling
- Security scanning
- Documentation update
- Migration steps
- Release preparation
- Onboarding tasks

## Using Skills in Projects

1. Create symlink during init:
   ```bash
   python -m claudecodeoptimizer init
   # Select your custom skill when prompted
   ```

2. Or manually copy:
   ```bash
   # Windows
   copy my-skill.md "%USERPROFILE%\.claude\skills\"

   # Unix/Linux/Mac
   cp my-skill.md ~/.claude/skills/
   ```

3. Skills auto-activate based on Claude's semantic matching - no manual reference needed.

4. Use via Claude Code when relevant to your task.

## Sharing Skills

Custom skills in `~/.claude/skills/` are:
- Local to your machine
- Not included in CCO package
- Can be shared via git/copy with team

To share:
1. Copy skill file to team repository
2. Team members copy to their `~/.claude/skills/`
3. Reference in project CLAUDE.md

---

*Add your custom skills here to create reusable workflows*
