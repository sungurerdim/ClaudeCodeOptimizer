# cco-commit

**AI-assisted semantic commit workflow with atomic commit recommendations.**

---

## Purpose

Generate high-quality semantic commit messages, recommend atomic commit splits, and improve git workflow quality (Pain #5: Git quality).

---

## Skills Used

- `cco-skill-git-branching-pr-review`
- `cco-skill-versioning-semver-changelog-compat`

---

## Execution Protocol

### Step 1: Analyze Staged Changes

```bash
git status
git diff --cached --stat
git diff --cached
```

Analyze:
- Files changed and line counts
- Types of changes (feature, fix, refactor, docs)
- Related vs unrelated changes
- Breaking changes

### Step 2: Recommend Atomic Commits

If multiple change types detected:
```markdown
Analyzing staged changes...

Files changed: 8
Lines added: 234
Lines removed: 89

Detected changes:
- Security fix (api/users.py, api/posts.py)
- Feature addition (api/chat.py)
- Test addition (tests/test_api.py, tests/test_chat.py)
- Documentation (README.md, openapi.yaml)

Recommendation: Split into 3 atomic commits

Commit 1: Security Fix
Files: api/users.py, api/posts.py
Type: fix(security)

Commit 2: Feature Addition
Files: api/chat.py, tests/test_chat.py
Type: feat(api)

Commit 3: Documentation
Files: README.md, openapi.yaml, tests/test_api.py (doc updates)
Type: docs(api)

Proceed with split? (yes/no/customize)
```

### Step 3: Generate Semantic Commit Messages

For each commit, generate message following Conventional Commits:

```
<type>(<scope>): <summary>

<body>

BREAKING CHANGE: <description if applicable>
Refs: #<issue-number>
```

**Example:**
```markdown
Commit 1 Message:

fix(security): parameterize SQL queries to prevent injection

- Replace string concatenation with parameterized queries
- Affects endpoints: /users/:id, /posts/:id
- Addresses 2 critical SQL injection vulnerabilities (OWASP A03)
- Added input validation for user-supplied IDs

Skill used: cco-skill-security-owasp-xss-sqli-csrf

BREAKING CHANGE: None
Refs: #security-audit-2025
```

### Step 4: Create Commits

```bash
# Stage files for commit 1
git reset
git add api/users.py api/posts.py

# Create commit 1
git commit -m "$(cat <<'EOF'
fix(security): parameterize SQL queries to prevent injection

- Replace string concatenation with parameterized queries
- Affects endpoints: /users/:id, /posts/:id
- Addresses 2 critical SQL injection vulnerabilities (OWASP A03)
- Added input validation for user-supplied IDs

Refs: #security-audit-2025
EOF
)"

# Repeat for commits 2 and 3
```

### Step 5: Summary

```markdown
Created 3 atomic commits:

✓ fix(security): parameterize SQL queries to prevent injection
  Files: api/users.py, api/posts.py
  Lines: +45 / -23

✓ feat(api): add AI chat endpoint with security validation
  Files: api/chat.py, tests/test_chat.py
  Lines: +156 / -0

✓ docs(api): document chat endpoint usage
  Files: README.md, openapi.yaml, tests/test_api.py
  Lines: +33 / -66

Impact:
- Git workflow score: 68 → 85
- Addresses Pain #5 (better git practices)
- Benefits: Easier review, better history, simpler rollbacks

Next:
- Push: git push origin feature-branch
- Create PR: gh pr create
```

---

## Conventional Commits Format

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring (no feature/fix)
- `perf`: Performance improvement
- `test`: Add/update tests
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

**Scopes:** Module/component affected (api, auth, database, etc.)

**Breaking Changes:** Always document with `BREAKING CHANGE:`

---

## Success Criteria

- [OK] Staged changes analyzed
- [OK] Change types detected
- [OK] Atomic split recommended if needed
- [OK] Semantic messages generated
- [OK] Commits created with proper format
- [OK] Summary presented
- [OK] Pain-point impact communicated

---

## Example Usage

```bash
# Analyze staged changes and create commits
/cco-commit

# If no staged changes, stage all and analyze
git add .
/cco-commit
```
