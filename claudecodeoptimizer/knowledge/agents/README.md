# Custom Agents

This directory contains custom agent definitions for task automation.

## What are Agents?

Agents are specialized AI assistants that perform complex, multi-step tasks autonomously. They combine instructions, context, and tools to accomplish specific objectives.

## Creating a Custom Agent

1. **Copy the template:**
   ```bash
   cp _template-agent.md my-custom-agent.md
   ```

2. **Fill in the details:**
   - Agent name and description
   - Capabilities and use cases
   - Detailed prompt with step-by-step instructions
   - Required tools
   - Model recommendation

3. **Test the agent:**
   Reference it in your project's CLAUDE.md:
   ```markdown
   @.claude/agents/my-custom-agent.md
   ```

## Agent Structure

```markdown
# Agent Name
## Description - What the agent does
## Capabilities - What it can do
## When to Use - Use cases
## Prompt - Detailed instructions
## Tools - Available tools
## Model - Recommended model
## Example - Usage example
```

## Best Practices

- **Clear objective**: Define exactly what the agent should accomplish
- **Step-by-step**: Break down complex tasks into clear steps
- **Tool specification**: List all tools the agent needs
- **Output format**: Specify expected output structure
- **Examples**: Include examples of successful outputs

## Example Agents

You can create agents for:
- Security auditing
- Performance analysis
- Code refactoring
- Documentation generation
- Dependency management
- Test generation
- Database migration
- API design
- Architecture review

## Using Agents in Projects

1. Create symlink during init:
   ```bash
   python -m claudecodeoptimizer init
   # Select your custom agent when prompted
   ```

2. Or manually link:
   ```bash
   # Windows
   mklink ".claude\agents\my-agent.md" "%USERPROFILE%\.cco\knowledge\agents\my-agent.md"

   # Unix/Linux/Mac
   ln -s ~/.cco/knowledge/agents/my-agent.md .claude/agents/my-agent.md
   ```

3. Reference in CLAUDE.md:
   ```markdown
   @.claude/agents/my-agent.md
   ```

## Sharing Agents

Custom agents in `~/.cco/knowledge/agents/` are:
- Local to your machine
- Not included in CCO package
- Can be shared via git/copy with team

To share:
1. Copy agent file to team repository
2. Team members copy to their `~/.cco/knowledge/agents/`
3. Reference in project CLAUDE.md

---

*Add your custom agents here to extend CCO functionality*
