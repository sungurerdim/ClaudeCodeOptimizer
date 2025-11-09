# Git Workflow Principles

**Generated**: 2025-11-09
**Principle Count**: 5

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