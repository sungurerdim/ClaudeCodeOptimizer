# cco-help

**Comprehensive CCO command guide with pain-point focus.**

---

## Purpose

Show all available CCO commands, organized by pain-point priority, with examples and use cases.

---

## Output Format

```markdown
# ClaudeCodeOptimizer (CCO) - Command Reference

**Production-grade development assistant built on 2025 industry pain points**

---

## Pain Points Addressed

🔴 **#1 Security (51% top concern)** - $500M+ cost from vulnerabilities
🔴 **#2 Technical Debt (23% time waste)** - Developers lose 23% of time
🔴 **#3 AI Reliability (45%)** - Unreliable AI-generated code
🟡 **#4 Testing (Biggest mistake)** - Production bugs, delays
🟡 **#5 Time Waste (69%)** - $2M annually per enterprise (8+ hours/week)
🟢 **#6 Integration Failures** - Deployment delays, broken builds
🟢 **#7 Documentation Gaps** - Onboarding delays, knowledge loss

---

## 11 Core Commands (Pain-Point Priority Order)

### Discovery Commands (3)

**`/cco-help`** - This guide
- Show all commands with examples

**`/cco-status`** - Installation health check
- Verify CCO installation
- Show available skills (25) and agents (3)
- Check configuration
- Usage: `/cco-status`

**`/cco-overview`** ⭐ START HERE
- Complete project health assessment
- Tech stack appropriateness evaluation
- Current vs ideal scenario comparison
- Prioritized action plan by pain-point impact
- Addresses: All 7 pain points
- Usage: `/cco-overview`

---

### Critical Action Commands (3)

**`/cco-audit`** 🔍 FIND ISSUES
- Comprehensive issue detection across 17 categories
- Pain-point priority ordering
- Uses: 25 skills + cco-agent-audit (Haiku)
- Categories:
  * 🔴 Critical: security, tech-debt, ai-security
  * 🟡 High: tests, integration
  * 🟢 Medium: code-quality, docs, database, observability,
              monitoring, cicd, containers, supply-chain,
              migrations, performance, architecture, git

Addresses Pain #1, #2, #3, #4, #5, #6, #7

Usage:
```bash
/cco-audit                     # Interactive selection
/cco-audit --security          # Single category
/cco-audit --security --tests  # Multiple categories
/cco-audit --all               # Comprehensive scan
```

**`/cco-fix`** 🔧 AUTO-FIX
- Automated issue resolution
- Auto-runs audit if needed
- Safe/risky categorization
- Uses: Same 25 skills + cco-agent-fix (Sonnet)
- Same 17 categories as audit

Addresses Pain #1, #2, #3, #4, #5, #6, #7

Usage:
```bash
/cco-fix                       # Interactive selection
/cco-fix --security            # Fix security issues
/cco-fix --security --tests    # Fix multiple categories
/cco-fix --all                 # Fix everything
```

**`/cco-generate`** 📝 CREATE MISSING
- Generate missing project components
- 17 generation types
- Uses: Appropriate skills + cco-agent-generate (Sonnet)
- Types:
  * 🔴 Critical: tests, contract-tests
  * 🟡 High: load-tests, chaos-tests, openapi, cicd
  * 🟢 Recommended: docs, adr, runbook, dockerfile, migration,
                    indexes, monitoring, logging, slo, pre-commit, requirements

Addresses Pain #4, #7

Usage:
```bash
/cco-generate                  # Interactive selection
/cco-generate --tests          # Generate tests
/cco-generate --openapi --cicd # Multiple types
/cco-generate --all            # Generate all recommended
```

---

### Productivity Commands (3)

**`/cco-optimize`** ⚡ PERFORMANCE
- Performance optimization across 6 areas
- Uses: 6 specialized skills + cco-agent-fix (Sonnet)
- Types: code, deps, docker, database, bundle, performance

Addresses Pain #5 (Time waste), Pain #2 (Tech debt)

Usage:
```bash
/cco-optimize                  # Interactive selection
/cco-optimize --database       # Optimize queries
/cco-optimize --docker         # Reduce image size
/cco-optimize --all            # All optimizations
```

**`/cco-commit`** 📝 SEMANTIC COMMITS
- AI-assisted commit workflow
- Semantic commit message generation
- Atomic commit recommendations
- Uses: git skills (no agent - lightweight)

Addresses Pain #5 (Git quality)

Usage:
```bash
git add .
/cco-commit                    # Analyze and create commits
```

**`/cco-implement`** 🚀 FEATURE DEVELOPMENT
- AI-assisted feature implementation
- TDD approach (tests first)
- Auto-skill selection
- Uses: Auto-selected skills + both agents

Addresses Pain #1, #4 (TDD prevents bugs)

Usage:
```bash
/cco-implement "Add user authentication with JWT"
/cco-implement "Add caching layer using Redis"
```

---

### Management Commands (2)

**`/cco-update`** - Update CCO
- Update to latest version
- Sync all skills, principles, commands
- Usage: `/cco-update`

**`/cco-remove`** - Uninstall CCO
- Complete removal with transparency
- Shows exactly what will be deleted
- Confirmation required
- Usage: `/cco-remove`

---

## 25 Skills (Auto-Activate on Demand)

**Security (5):**
- security-owasp, ai-security, supply-chain, k8s-security, privacy

**Testing (2):**
- test-pyramid, api-testing

**Database (2):**
- database-optimization, data-migrations

**Observability (3):**
- observability, logging, incident-response

**CI/CD (2):**
- cicd-gates, deployment-strategies

**Code Quality (2):**
- code-quality, content-optimization

**Documentation (1):**
- docs-api-adr-runbooks

**Git (2):**
- git-branching, versioning

**Performance (2):**
- frontend-performance, resilience

**Architecture (2):**
- microservices, event-driven

**Mobile (1):**
- mobile-best-practices

**DevEx (1):**
- developer-experience

---

## 3 Agents (Parallel Execution)

- **cco-agent-audit** - Fast scanning (Haiku - 10x cheaper)
- **cco-agent-fix** - Accurate fixes (Sonnet - better quality)
- **cco-agent-generate** - Code generation (Sonnet - better quality)

---

## Typical Workflows

### New Project Setup
```bash
/cco-overview              # Assess health
/cco-generate --tests --openapi --cicd --dockerfile
/cco-commit
```

### Security Hardening
```bash
/cco-audit --security --ai-security --supply-chain
/cco-fix --security
/cco-commit
```

### Quality Improvement
```bash
/cco-audit --code-quality --tech-debt
/cco-fix --tech-debt
/cco-optimize --code
/cco-commit
```

### Performance Optimization
```bash
/cco-audit --performance --database
/cco-optimize --database --docker
/cco-commit
```

### Complete Health Check
```bash
/cco-overview              # Full assessment
/cco-audit --all           # Find all issues
/cco-fix --all             # Fix safe issues
/cco-generate --all        # Create missing components
/cco-optimize --all        # Performance tuning
/cco-commit                # Semantic commits
```

---

## Getting Help

- **This guide:** `/cco-help`
- **Health check:** `/cco-status`
- **Project assessment:** `/cco-overview`
- **GitHub Issues:** https://github.com/sungurerdim/ClaudeCodeOptimizer/issues
- **Discussions:** https://github.com/sungurerdim/ClaudeCodeOptimizer/discussions

---

## Quick Reference Card

| Need | Command |
|------|---------|
| Start here | `/cco-overview` |
| Find security issues | `/cco-audit --security` |
| Fix vulnerabilities | `/cco-fix --security` |
| Generate tests | `/cco-generate --tests` |
| Speed up queries | `/cco-optimize --database` |
| Clean up code | `/cco-optimize --code` |
| Create commits | `/cco-commit` |
| Implement feature | `/cco-implement "description"` |
| Full check | `/cco-audit --all` |
| Help | `/cco-help` |

---

**Built for production. Driven by 2025 industry pain points. Optimized for your workflow.**
```

---

## Success Criteria

- [OK] All 11 commands documented
- [OK] Pain-point context provided
- [OK] Usage examples for each command
- [OK] Workflow examples provided
- [OK] Skills and agents explained
- [OK] Quick reference included
