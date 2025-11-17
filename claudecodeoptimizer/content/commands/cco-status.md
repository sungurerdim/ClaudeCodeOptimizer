# cco-status

**CCO installation health check with skill and agent availability.**

---

## Purpose

Verify CCO installation, show available commands, skills, agents, principles, and provide quick start guidance.

---

## Execution Protocol

### Check Installation

1. **Verify global directory exists:**
```bash
ls ~/.claude/
```

Expected structure:
```
~/.claude/
├── commands/      (11 core commands)
├── principles/    (105 principles: 8 C_, 6 U_, 91 P_)
├── skills/        (26 skills)
├── agents/        (3 agents)
└── CLAUDE.md      (principle markers)
```

2. **Count components:**
```bash
ls ~/.claude/commands/cco-*.md | wc -l    # Should be 11
ls ~/.claude/principles/*.md | wc -l       # Should be 105
ls ~/.claude/skills/cco-skill-*.md | wc -l # Should be 26
ls ~/.claude/agents/cco-agent-*.md | wc -l # Should be 3
```

3. **Check CLAUDE.md:**
```bash
cat ~/.claude/CLAUDE.md | head -20
```

Should contain principle markers (U_* and C_*).

### Output Format

```markdown
# CCO Installation Status

[OK] Health: Good
[OK] Location: ~/.claude/

---

## Components

**Commands (11 core):**
- Discovery (3): help, status, overview
- Critical (3): audit, fix, generate
- Productivity (3): optimize, commit, implement
- Management (2): update, remove

**Principles (105):**
- 8 Claude Guidelines (C_*) - Always active
- 6 Universal (U_*) - Always active
- 91 Project (P_*) - Progressive loading via skills

**Skills (26 - Auto-Activate on Demand):**

Security (5):
- cco-skill-security-owasp-xss-sqli-csrf
- cco-skill-ai-security-promptinjection-models
- cco-skill-supply-chain-dependencies-sast
- cco-skill-kubernetes-security-containers
- cco-skill-privacy-gdpr-compliance-encryption

Testing (2):
- cco-skill-test-pyramid-coverage-isolation
- cco-skill-api-testing-contract-load-chaos

Database (2):
- cco-skill-database-optimization-caching-profiling
- cco-skill-data-migrations-backup-versioning

Observability (3):
- cco-skill-observability-metrics-alerts-slo
- cco-skill-logging-structured-correlation-tracing
- cco-skill-incident-oncall-postmortem-playbooks

CI/CD (2):
- cco-skill-cicd-gates-deployment-automation
- cco-skill-deployment-bluegreen-canary-rollback

Code Quality (2):
- cco-skill-code-quality-refactoring-complexity
- cco-skill-content-optimization-automation

Documentation (1):
- cco-skill-docs-api-openapi-adr-runbooks

Git (2):
- cco-skill-git-branching-pr-review
- cco-skill-versioning-semver-changelog-compat

Performance (2):
- cco-skill-frontend-bundle-a11y-performance
- cco-skill-resilience-circuitbreaker-retry-bulkhead

Architecture (2):
- cco-skill-microservices-cqrs-mesh-di
- cco-skill-eventdriven-async-messaging-queues

Mobile (1):
- cco-skill-mobile-offline-battery-appstore

DevEx (1):
- cco-skill-devex-onboarding-tooling-parity

**Agents (3 - Parallel Execution):**
- cco-agent-audit (Haiku - Fast scanning, 10x cheaper)
- cco-agent-fix (Sonnet - Accurate fixes, better quality)
- cco-agent-generate (Sonnet - Code generation, better quality)

---

## Pain Points Addressed (2025 Industry Data)

[OK] #1 Security (51% top concern) - $500M+ cost
[OK] #2 Technical Debt (23% time waste)
[OK] #3 AI Reliability (45% unreliable AI code)
[OK] #4 Testing (biggest mistake) - Production bugs
[OK] #5 Time Waste (69% lose 8+ hours/week)
[OK] #6 Integration Failures - Deployment delays
[OK] #7 Documentation Gaps - Knowledge loss

---

## Architecture

**Zero Pollution:**
- Global storage: ~/.claude/ (all projects share)
- Project storage: ZERO files created
- Updates: One command updates all projects
- Token efficiency: 25-35K avg (vs 200K old system)

**Progressive Loading:**
- Always loaded: 14 baseline principles (8 C_ + 6 U_)
- Auto-activated: 26 skills via semantic matching (load 91 P_ principles on-demand)
- Context: 82-87% reduction (200K → 25-35K tokens)

**Skill-Based Intelligence:**
- Claude autonomously loads what's needed
- No manual skill activation required
- Skills reference relevant P_ principles

---

## Quick Start

**First time?**
```bash
/cco-overview              # See project health
/cco-audit --security      # Find vulnerabilities
/cco-fix --security        # Auto-fix issues
```

**Want comprehensive check?**
```bash
/cco-overview              # Full assessment
/cco-audit --all           # Find all issues
/cco-fix --all             # Fix safe issues
/cco-generate --all        # Create missing components
```

**Need help?**
```bash
/cco-help                  # Full command reference
```

---

## Troubleshooting

**Commands not found?**
```bash
ls ~/.claude/commands/cco-*.md
# If empty or < 11 files, run:
cco-setup
```

**Skills not loading?**
- Skills auto-activate via Claude's semantic matching
- No manual intervention needed
- Check availability: /cco-status (this command)

**Installation issues?**
```bash
# Reinstall
pip install -U git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup

# Or with pipx
pipx reinstall claudecodeoptimizer
```

---

## Version Info

**CCO Version:** [Read from package]
**Installation Method:** [Detect: pip/pipx/uv]
**Python Version:** [Detect]
**Platform:** [Detect: Windows/macOS/Linux]

---

[OK] CCO is ready!
All components installed and available.

Next: /cco-help (command reference) or /cco-overview (project health)
```

---

## Error Cases

If components missing:
```markdown
[ERROR] Health: Incomplete installation

Missing components:
- Commands: 8/11 (missing: update, remove, help)
- Skills: 23/26 (missing: 3 security skills)
- Agents: 3/3 [OK]

Fix: Run cco-setup to repair installation
```

If directory doesn't exist:
```markdown
[ERROR] CCO not installed

Directory ~/.claude/ not found.

Install:
1. pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
2. cco-setup

Or one-line: [provide install script URL]
```

---

## Success Criteria

- [OK] Installation verified
- [OK] Component counts displayed
- [OK] Skills categorized and listed
- [OK] Agents explained
- [OK] Pain points listed
- [OK] Quick start provided
- [OK] Troubleshooting included
