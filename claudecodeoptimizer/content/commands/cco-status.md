---
name: cco-status
description: CCO installation health check showing available commands, skills, agents, and configuration status
action_type: status
keywords: [status, health, check, installation, verify, components, availability]
category: discovery
pain_points: []
---

# cco-status

**CCO installation health check with dynamic component discovery.**

---

## Built-in References

- **[cco-standards.md](../cco-standards.md)** - Standard structure, execution protocol
- **[cco-patterns.md](../cco-patterns.md)** - Reusable patterns (Progress, Error Handling)

---

## Purpose

Verify CCO installation by dynamically discovering all components from the file system.

---

## Execution Protocol

### 1. Discover Components Dynamically

**CRITICAL: All counts and lists MUST be read from file system, never hardcoded.**

```bash
# Count each component type
COMMANDS=$(ls ~/.claude/commands/cco-*.md 2>/dev/null | wc -l)
SKILLS=$(ls ~/.claude/skills/cco-skill-*.md 2>/dev/null | wc -l)
AGENTS=$(ls ~/.claude/agents/cco-agent-*.md 2>/dev/null | wc -l)
U_PRINCIPLES=$(ls ~/.claude/principles/cco-principle-u-*.md 2>/dev/null | wc -l)
C_PRINCIPLES=$(ls ~/.claude/principles/cco-principle-c-*.md 2>/dev/null | wc -l)
```

### 2. Read Component Details from Frontmatter

For each component, extract name and description from YAML frontmatter:

```yaml
---
name: cco-skill-security-fundamentals
description: OWASP Top 10, XSS, SQL injection prevention
keywords: [security, owasp, xss, sqli]
category: security
---
```

### 3. Generate Dynamic Output

```markdown
# CCO Installation Status

[OK] Health: Good
[OK] Location: ~/.claude/

---

## Components (Dynamically Discovered)

**Commands ({actual_count} found):**
[List each cco-*.md from ~/.claude/commands/ with description from frontmatter]

**Principles ({actual_count} found):**
- {u_count} Universal (cco-principle-u-*) - Always active
- {c_count} Claude-specific (cco-principle-c-*) - Always active

**Skills ({actual_count} found - Auto-Activate on Demand):**
[For each cco-skill-*.md in ~/.claude/skills/:
 - Read frontmatter
 - Extract: name, description, category, keywords
 - Group by category
 - List with description]

**Agents ({actual_count} found):**
[For each cco-agent-*.md in ~/.claude/agents/:
 - Read frontmatter
 - Extract: name, description, model
 - List with description]

---

## Architecture

**Zero Pollution:**
- Global storage: ~/.claude/ (all projects share)
- Project storage: ZERO files created
- Updates: One command updates all projects

**Dynamic Loading:**
- Principles: Auto-injected via CLAUDE.md markers
- Skills: Auto-activated via Claude's semantic matching
- No manual configuration required

---

## Quick Start

/cco-audit --quick         # Fast health assessment
/cco-help                  # Full command reference

---

## Troubleshooting

**Components missing?**
Run: cco-setup

**Skills not loading?**
Skills auto-activate via semantic matching. No manual intervention needed.
```

---

## Dynamic Discovery Rules

1. **Never hardcode counts** - Always count from file system
2. **Never hardcode lists** - Always read from actual files
3. **Read frontmatter** - Extract metadata from YAML header
4. **Group by category** - Use `category` field from frontmatter
5. **Show descriptions** - Use `description` field from frontmatter

---

## Success Criteria

- [OK] All counts from file system (not hardcoded)
- [OK] All lists from actual files (not hardcoded)
- [OK] Frontmatter parsed for metadata
- [OK] Components grouped by category
- [OK] New components auto-discovered
- [OK] Removed components auto-excluded
