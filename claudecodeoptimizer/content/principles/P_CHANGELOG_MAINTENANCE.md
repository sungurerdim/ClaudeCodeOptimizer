# P_CHANGELOG_MAINTENANCE: Changelog Maintenance

**Severity**: High

Users don't know what changed; hesitant to upgrade Breaking changes hidden; production breaks on upgrade "What's new?" floods support channels Security fixes not highlighted; vulnerabilities persist M.

---

## Rules

- *No rules extracted*

---

## Examples

### ❌ Bad
```markdown
# ❌ BAD: No changelog
# Users upgrade and discover breaking changes → production crashes

# ❌ BAD: Outdated changelog
## [3.0.0] - 2022-01-15  (from 2 years ago!)
- "Updated dependencies"
- "Bug fixes"

# Problems: Vague, no breaking changes documented, 20+ releases undocumented
```
**Why wrong**: ---
