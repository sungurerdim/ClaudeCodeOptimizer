# CCO Skills Catalog

**Dynamic skill discovery - no hardcoded lists.**

---

## How Skills Work

Skills are Markdown files in ~/.claude/skills/ with YAML frontmatter.

### Discovery Protocol

**CRITICAL: Never hardcode skill lists. Always discover dynamically.**

```bash
# List all skills
ls ~/.claude/skills/cco-skill-*.md

# Count skills  
ls ~/.claude/skills/cco-skill-*.md | wc -l
```

### Frontmatter Fields

| Field | Purpose |
|-------|---------|
| name | Unique identifier |
| description | What skill provides |
| keywords | Semantic matching terms |
| category | Grouping (security, testing, docs, etc.) |
| pain_points | Industry pain points addressed |

---

## Auto-Activation

Skills auto-activate via Claude semantic matching:

1. Claude analyzes task context
2. Matches against skill keywords/categories
3. Loads relevant skills automatically

---

## Adding New Skills

1. Create ~/.claude/skills/cco-skill-{domain}.md
2. Add frontmatter with name, description, keywords, category
3. Skill auto-discovers when relevant

**No catalog updates needed. No code changes needed.**

---

## Removing Skills

1. Delete skill file
2. No catalog updates needed

---

## Viewing Available Skills

Run /cco-status to see all dynamically discovered skills.
