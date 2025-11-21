# Operational Runbooks

This directory contains operational runbooks for ClaudeCodeOptimizer installation, maintenance, and troubleshooting.

## Available Runbooks

- [Installation](installation.md) - Install CCO from scratch
- [Updates](updates.md) - Update existing CCO installation
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Uninstallation](uninstallation.md) - Clean removal procedures

## What is a Runbook?

A runbook is a step-by-step guide for completing operational tasks. Unlike documentation that explains "what" or "why", runbooks focus on "how" with concrete, actionable steps.

## When to Use These Runbooks

| Scenario | Runbook |
|----------|---------|
| First-time CCO installation | [Installation](installation.md) |
| Updating to newer CCO version | [Updates](updates.md) |
| CCO not working as expected | [Troubleshooting](troubleshooting.md) |
| Want to remove CCO completely | [Uninstallation](uninstallation.md) |

## Runbook Structure

Each runbook follows this structure:

1. **Purpose**: What this runbook accomplishes
2. **Prerequisites**: What you need before starting
3. **Procedure**: Step-by-step instructions
4. **Verification**: How to verify success
5. **Rollback**: How to undo if something goes wrong
6. **Troubleshooting**: Common issues and solutions

## Contributing

When creating new runbooks:

1. Follow the standard template
2. Use clear, numbered steps
3. Include verification steps
4. Provide rollback procedures
5. Test all steps before committing
6. Update this index

## Runbook Template

```markdown
# Runbook: {TITLE}

## Purpose
What is this runbook for? What will be accomplished?

## Prerequisites
- Prerequisite 1
- Prerequisite 2

## Procedure

### Step 1: {FIRST_ACTION}

1. Action 1
   ```bash
   command here
   ```

2. Action 2
   ```bash
   command here
   ```

**Expected Result:** What you should see

### Step 2: {SECOND_ACTION}

...

## Verification

How to verify the procedure succeeded:

1. Verification step 1
   ```bash
   verification command
   ```
   **Expected output:** ...

2. Verification step 2
   ...

## Rollback

If something goes wrong, follow these steps to undo:

1. Rollback step 1
2. Rollback step 2

## Troubleshooting

### Issue: {COMMON_PROBLEM}

**Symptoms:**
- Symptom 1
- Symptom 2

**Solution:**
1. Solution step 1
2. Solution step 2

## References
- Related runbooks
- Related documentation
```

## Best Practices

1. **Atomic Steps**: Each step should be a single, clear action
2. **Copy-Pasteable Commands**: All commands should work as-is
3. **Platform-Specific Notes**: Call out Windows/macOS/Linux differences
4. **Safety First**: Include warnings about destructive operations
5. **Verification**: Always include verification steps
6. **Rollback**: Provide rollback for any significant change
7. **Keep Updated**: Review and update quarterly

## Support

If runbooks don't resolve your issue:

1. Check [Troubleshooting](troubleshooting.md) runbook
2. Search [GitHub Issues](https://github.com/yourusername/ClaudeCodeOptimizer/issues)
3. Create a new issue with:
   - Which runbook you followed
   - Which step failed
   - Error messages
   - Your environment (OS, Python version, etc.)
