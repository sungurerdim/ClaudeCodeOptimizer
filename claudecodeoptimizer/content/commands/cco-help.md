---
name: cco-help
description: Comprehensive CCO command reference guide organized by pain-point priority with examples and workflows
action_type: help
keywords: [help, guide, reference, commands, documentation, usage, examples]
category: discovery
pain_points: []
---

# cco-help

**Quick command reference for ClaudeCodeOptimizer**

---

## Purpose

Show all available CCO commands with clear examples and common use cases. Maximum clarity, minimum noise.

---

## Output Format

```markdown
# ClaudeCodeOptimizer - Command Reference

**Production-ready development assistant for Claude Code**

---

## 🚀 Start Here (First Time?)

### 1️⃣ First Command - Quick Health Check
```bash
/cco-audit --quick
```
See your project health scores. That's it!

### 2️⃣ Second Command - Find Issues
```bash
/cco-audit --security
```
Find security issues. Simple!

### 3️⃣ Third Command - Auto-Fix
```bash
/cco-fix --security
```
Auto-fix safe issues. Watch it work!

### 💡 Pro Move - Add Context
```bash
/cco-audit --security "Check API authentication"
```
Add quotes after command = focused results!

---

## 🎯 Pro Tip: Optional Prompts

**ALL commands support additional context:**

```bash
/cco-[command] --[flag] "[Your additional context here]"
```

**What you can do:**
- Focus on specific areas: `"Check authentication endpoints"`
- Set constraints: `"Conservative fixes only"`
- Provide domain context: `"Payment processing is critical"`
- Reference requirements: `"Follow OWASP 2025 guidelines"`

**Examples:**
```bash
/cco-audit --security "Focus on API authentication"
/cco-fix --tech-debt "High-complexity functions only"
/cco-generate --tests "Edge cases for payment logic"
/cco-optimize --database "Payment queries are priority"
```

**This works with EVERY command and EVERY flag!**

---

## 📋 All Commands

### Find Issues

**`/cco-audit`** → Find problems in your code
- **Quick mode:** `--quick` (health check with scores)
- **Core:** `--security`, `--tech-debt`, `--tests`, `--database`, `--performance`, `--integration`, `--docs`
- **AI (2025):** `--ai-security`, `--ai-quality`, `--ai-debt`, `--ai` (meta-flag: combines all AI)
- **Team (2025):** `--code-review`, `--platform`
- **Infrastructure:** `--ci-cd`, `--containers`, `--supply-chain`
- **Presets:** `--all` (comprehensive scan)
- Example: `/cco-audit --security --ai-quality --code-review`

**`/cco-status`** → Check CCO installation health
- Shows installed commands, skills, agents
- Verifies configuration
- Example: `/cco-status`

---

### Fix Issues

**`/cco-fix`** → Auto-fix detected problems
- **Same categories as audit** (including `--ai`, `--ai-quality`, `--ai-debt`)
- Safe fixes auto-applied (SQL parameterization, remove dead code, API hallucination removal)
- Risky fixes require approval (CSRF protection, auth changes)
- Auto-runs audit if needed
- Example: `/cco-fix --security --ai-quality --tech-debt`

**`/cco-optimize`** → Speed up your code with metrics
- **Types:** `--database` (queries), `--docker` (image size), `--bundle` (frontend), `--performance` (bottlenecks)
- Shows before/after metrics
- Note: For code cleanup use `/cco-fix --tech-debt`
- Example: `/cco-optimize --database`

---

### Create Missing Parts

**`/cco-generate`** → Create tests, docs, configs
- **Critical:** `--tests`, `--contract-tests`
- **High:** `--load-tests`, `--chaos-tests`, `--openapi`, `--cicd`
- **Team (2025):** `--review-checklist` (PR quality gates, DORA metrics tracking)
- **Recommended:** `--docs`, `--adr`, `--runbook`, `--dockerfile`, `--migration`, `--indexes`, `--monitoring`, `--logging`, `--slo`, `--pre-commit`, `--requirements`
- Example: `/cco-generate --tests --openapi --review-checklist`

**`/cco-implement`** → Build new features with TDD
- Test-Driven Development approach
- Auto-skill selection based on feature type
- Example: `/cco-implement "Add JWT authentication"`

---

### Workflow Support

**`/cco-commit`** → Smart git commits
- AI-generated semantic commit messages
- Atomic commit recommendations
- Example: `git add . && /cco-commit`

**`/cco-help`** → This guide
- Quick command reference
- Example: `/cco-help`

**`/cco-update`** → Update to latest CCO version
- Updates all commands, skills, agents
- One update → all projects get it instantly
- Example: `/cco-update`

**`/cco-remove`** → Clean uninstall (Step 1 of 2)
- Removes all global CCO files (`~/.claude/`)
- Must run BEFORE `pip uninstall` (requires package)
- Example: `/cco-remove` → then `pip uninstall claudecodeoptimizer`

---

## 🎯 Common Tasks

| I want to... | Run this |
|--------------|----------|
| **See project health** | `/cco-audit --quick` |
| **Fix security bugs** | `/cco-audit --security` → `/cco-fix --security` |
| **Add missing tests** | `/cco-generate --tests` |
| **Speed up database** | `/cco-optimize --database` |
| **Clean up code** | `/cco-fix --tech-debt` |
| **Create API docs** | `/cco-generate --openapi` |
| **Build new feature** | `/cco-implement "feature description"` |
| **Make good commits** | `/cco-commit` |
| **Full health check** | `/cco-audit --all` → `/cco-fix --all` |

---

## 📊 Quick Reference Table

| Command | Primary Use | Optional Prompt Example |
|---------|-------------|-------------------------|
| `/cco-audit --quick` | Health check | "Focus on production-critical areas" |
| `/cco-audit --security` | Security scan | "Prioritize authentication" |
| `/cco-fix --security` | Auto-fix | "Conservative fixes only" |
| `/cco-generate --tests` | Create tests | "Edge cases for payments" |
| `/cco-implement` | New feature | "[Feature] with [tech requirements]" |
| `/cco-optimize --database` | DB optimization | "Focus on checkout queries" |
| `/cco-commit` | Smart commit | N/A |
| `/cco-status` | Health check | N/A |

---

## 📖 Audit/Fix Categories

**🔴 Critical Impact:**
- **Security** - SQL injection, XSS, CSRF, secrets, CVEs, auth bypass (OWASP 2025)
- **AI Security** - Prompt injection, PII leakage, broken access control (OWASP A01:2025)
- **Database** - N+1 queries, missing indexes, slow queries
- **Tests** - Coverage gaps, isolation issues, pyramid violations

**🟡 High Impact:**
- **Tech Debt** - Dead code, complexity, duplication, tight coupling
- **AI Quality** - API hallucinations, code bloat, vibe coding patterns
- **Performance** - Caching, algorithms, bottlenecks
- **CI/CD** - Pipeline issues, deployment gates
- **Supply Chain** - CVE scanning, SBOM, SLSA compliance

**🟢 Medium Impact:**
- **Documentation** - Missing docstrings, outdated API docs
- **Code Review** - Commit quality, reviewer diversity, DORA metrics
- **Platform** - CI/CD maturity, test automation, AI readiness
- **Containers** - Dockerfile issues, Pod Security, Kubernetes security
- **Integration** - Import errors, dependency conflicts

**Use with:** `--security`, `--ai-security`, `--database`, `--tests`, `--tech-debt`, `--ai-quality`, `--performance`, `--ci-cd`, `--supply-chain`, `--docs`, `--code-review`, `--platform`, `--containers`, `--integration`

**Meta-flags (Convenience Shortcuts):**
- `--ai` → All AI-related (ai-security + ai-quality + ai-debt)
- `--critical` → Critical impact (security + ai-security + database + tests)
- `--production-ready` → Pre-deploy essentials (security + performance + database + tests + docs)
- `--code-health` → Quality focus (tech-debt + code-quality + tests + docs)
- `--team-metrics` → Team performance (code-review + platform + cicd)

**Examples:**
```bash
/cco-audit --critical          # Focus on critical issues only
/cco-fix --production-ready    # Fix everything needed for deploy
/cco-audit --code-health       # Assess code quality
/cco-audit --team-metrics      # Check team collaboration metrics
```

---

## 🔧 How CCO Works

**Zero Project Pollution:**
- All CCO files live in `~/.claude/` (globally shared)
- Your projects stay clean
- One update → all projects benefit

**Smart Agent Selection:**
- **audit-agent** (Haiku) - Fast scanning, cost-efficient
- **fix-agent** (Sonnet) - Accurate code modifications
- **generate-agent** (Sonnet) - Quality code generation

**Auto-Activating Skills:**
- Skills load on-demand based on context
- Security (OWASP 2025), AI quality, code review (DORA), platform engineering, and more
- No manual skill selection needed

---

## 💡 Typical Workflows

**New Project Setup:**
```bash
/cco-audit --quick                    # Health baseline
/cco-generate --tests --openapi --cicd --dockerfile
/cco-commit
```

**Security Hardening:**
```bash
/cco-audit --security
/cco-fix --security
/cco-commit
```

**Quality Improvement:**
```bash
/cco-audit --code-quality --tech-debt
/cco-fix --tech-debt
/cco-generate --tests
/cco-commit
```

**Performance Tuning:**
```bash
/cco-audit --performance --database
/cco-optimize --database --docker
/cco-commit
```

**Complete Health Check:**
```bash
/cco-audit --quick      # See scores
/cco-audit --all        # Find all issues
/cco-fix --all          # Fix safe issues
/cco-generate --all     # Fill gaps
/cco-optimize --all     # Optimize
/cco-commit             # Commit changes
```

---

## 📚 Pain Points Addressed (12 Total - 2025 Data)

🔴 **#1 Security** - OWASP Top 10 2025, supply chain, CVE scanning
🔴 **#2 Technical Debt** - Dead code, complexity, coupling, legacy patterns
🔴 **#3 AI Security** - Prompt injection, PII leakage, broken access control (A01:2025)
🔴 **#4 Missing Tests** - Coverage gaps, untested critical paths, pyramid violations
🟡 **#5 Time Waste** - N+1 queries, missing indexes, slow builds
🟡 **#6 Integration Failures** - Import errors, dependency conflicts, broken builds
🟢 **#7 Documentation Gaps** - Missing docstrings, outdated API docs, no runbooks
🟡 **#8 AI Code Quality** - Hallucinated APIs, code bloat, vibe coding
🟡 **#9 Velocity Loss** - DORA metrics decline, slow feature delivery
🟢 **#10 AI Readiness Gaps** - Immature CI/CD, missing test automation, poor DX
🟡 **#11 Code Review Decline** - -27% comment rate (2025), shallow reviews, echo chambers
🟡 **#12 Team Breakdowns** - Knowledge silos, reviewer diversity issues, high rework rates

---

## ❓ Common Questions

**Q: How do I focus a command on specific code?**
A: Add quoted text after flags: `/cco-audit --security "Focus on auth endpoints"`

**Q: What's the difference between --quick and --all?**
A:
- `--quick` = 5min health scores (overview)
- `--all` = comprehensive scan (detailed findings)

**Q: Do I need to run audit before fix?**
A: No! `/cco-fix` auto-runs audit if needed.

**Q: Can I use multiple flags?**
A: Yes! `/cco-audit --security --tech-debt --tests`

**Q: What's the --ai meta-flag?**
A: Combines `--ai-security + --ai-quality + --ai-debt` (saves typing)

**Q: How do I add optional context?**
A: Put it in quotes after flags: `/cco-fix --tech-debt "High-complexity functions only"`

**Q: Which commands need quotes for feature description?**
A: Only `/cco-implement`: `/cco-implement "Add JWT auth"`

**Q: How do I update CCO?**
A: Run `/cco-update` (updates all commands/skills/agents globally)

**Q: How do I uninstall CCO?**
A: Two steps: 1) `/cco-remove` (requires package) 2) `pip uninstall claudecodeoptimizer`

**Q: Where are CCO files stored?**
A: `~/.claude/` (global, shared across all projects - zero project pollution)

---

## 🔗 More Information

- **Installation health:** `/cco-status`
- **Full documentation:** https://github.com/sungurerdim/ClaudeCodeOptimizer#readme
- **GitHub Issues:** https://github.com/sungurerdim/ClaudeCodeOptimizer/issues
- **Discussions:** https://github.com/sungurerdim/ClaudeCodeOptimizer/discussions

---

**Built for production. Optimized for your workflow. Zero project pollution.**
```

---

## Success Criteria

- [OK] All 10 commands documented with clear examples
- [OK] Pain-point focus maintained
- [OK] "What do I want to do?" → Command mapping clear
- [OK] Quick start guide included
- [OK] Common workflows provided
- [OK] No placeholders - real numbers only
- [OK] Action-oriented language
- [OK] Maximum clarity, minimum noise
