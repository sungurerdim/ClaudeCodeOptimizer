# Git Workflow Principles

**Generated**: 2025-11-09
**Principle Count**: 6

---

### P043: Commit Message Conventions 🟡

**Severity**: Medium

Use Conventional Commits: feat/fix/docs/refactor/test.

**❌ Bad**:
```
git commit -m 'fixed stuff'
```

**✅ Good**:
```
git commit -m 'fix(api): handle null user_id in /jobs endpoint'
```

---

### P072: Concise Commit Messages 🟡

**Severity**: Medium

Commit messages must be compact: max 10 lines, 5 bullets, no verbosity.

**Format**:
```
type(scope): concise description (max 72 chars)

- Key change 1 with brief context
- Key change 2
- Key change 3
```

**Rules**:
- ✅ Max 10 lines total, 5 bullets max
- ✅ One line per bullet
- ❌ No section headers ("Changes:", "Rationale:")
- ❌ No emojis, decorative elements, or footers

**❌ Bad - Too Verbose**:
```
refactor: eliminate tool redundancy

Tool Consolidation (3 tools instead of 5):
- Replace Black + mypy + Bandit with Ruff
- Keep pip-audit (CVE scanning)
...

Dependency Changes (pyproject.toml):
- Remove: black, mypy from dev dependencies
...
[15 more lines]
```

**✅ Good - Compact**:
```
refactor(ci): consolidate tools (P071)

- Replace Black/Bandit/mypy with Ruff (format+lint+security)
- Remove tool configs from pyproject.toml
- Simplify workflow to 3 jobs, 5 steps total
```

**Detailed Guide**: [@docs/cco/guides/git-workflow.md](../guides/git-workflow.md)

---

### P044: Branching Strategy 🟡

**Severity**: Medium

Git Flow for releases, Trunk-Based for CI/CD.

**❌ Bad**:
```
# Everyone commits to main
```

**✅ Good**:
```
# Feature branches -> main (with CI/CD)
```

---

### P045: PR Guidelines 🟡

**Severity**: Medium

PR template with description, tests, breaking changes checklist.

**❌ Bad**:
```
# No PR template, inconsistent reviews
```

**✅ Good**:
```
# .github/pull_request_template.md with checklist
```

---

### P046: Rebase vs Merge Strategy 🟢

**Severity**: Low

Rebase feature branches, merge to main (clean history).

**❌ Bad**:
```
# Merge commits everywhere, messy history
```

**✅ Good**:
```
git rebase main  # Clean feature branch\ngit merge --no-ff feature  # To main
```

---

### P047: Semantic Versioning 🟡

**Severity**: Medium

SemVer: MAJOR.MINOR.PATCH for breaking/features/fixes.

**Project Types**: library, api

**❌ Bad**:
```
# Random version numbers
```

**✅ Good**:
```
# v2.0.0 (breaking), v1.5.0 (feature), v1.4.1 (fix)
```

---

---

**Loading**: These principles load automatically when running relevant commands

**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly