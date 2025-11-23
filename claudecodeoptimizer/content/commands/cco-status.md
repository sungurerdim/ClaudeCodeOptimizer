---
name: cco-status
description: CCO installation health check showing available commands, skills, agents, and configuration status
action_type: status
keywords: [status, health, check, installation, verify, components, availability]
category: discovery
pain_points: []
---

# cco-status

**CCO installation health check with skill and agent availability.**
---

## Built-in References

**This command inherits standard behaviors from:**

- **[STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md)** - Standard structure, execution protocol, file discovery
- **[STANDARDS_QUALITY.md](../STANDARDS_QUALITY.md)** - UX/DX, efficiency, simplicity, performance standards
- **[LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md)** - Reusable patterns (Step 0, Selection, Accounting, Progress, Error Handling)
- **[STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md)** - File discovery, model selection, parallel execution

**See these files for detailed patterns. Only command-specific content is documented below.**

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
├── commands/      ({COMMAND_COUNT} core commands)
├── principles/    ({PRINCIPLE_COUNT} principles: {C_PRINCIPLE_COUNT} C_, {U_PRINCIPLE_COUNT} U_, {P_PRINCIPLE_COUNT} P_)
├── skills/        ({SKILL_COUNT} skills)
├── agents/        ({AGENT_COUNT} agents)
└── CLAUDE.md      (principle markers)
```

2. **Count components:**
```bash
ls ~/.claude/commands/cco-*.md | wc -l    # Count commands
ls ~/.claude/principles/*.md | wc -l       # Count principles
ls ~/.claude/skills/cco-skill-*.md | wc -l # Count skills
ls ~/.claude/agents/cco-agent-*.md | wc -l # Count agents
```

3. **Check CLAUDE.md:**
```bash
cat ~/.claude/CLAUDE.md | head -20
```

### Output Format

**See [LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md#pattern-8-dynamic-results-generation) for reporting pattern.**

```markdown
# CCO Installation Status

[OK] Health: Good
[OK] Location: ~/.claude/

---

## Components

**Commands ({COMMAND_COUNT} core):**
- Discovery: help, status
- Critical: audit, fix, generate
- Productivity: optimize, commit, implement
- Management: update, remove

**Principles ({PRINCIPLE_COUNT}):**
- {C_PRINCIPLE_COUNT} Claude Guidelines (C_*) - Always active
- {U_PRINCIPLE_COUNT} Universal (U_*) - Always active
- {P_PRINCIPLE_COUNT} Project (P_*) - Progressive loading via skills

**Skills ({SKILL_COUNT} - Auto-Activate on Demand):**

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

**Agents ({AGENT_COUNT} - Parallel Execution):**
- cco-agent-audit (Haiku - Fast scanning, cost-efficient)
- cco-agent-fix (Sonnet - Accurate fixes, better quality)
- cco-agent-generate (Sonnet - Code generation, better quality)

---

## Pain Points Addressed (12 - 2025 Industry Data)

[OK] #1 Security (top concern) - High cost
[OK] #2 Technical Debt (significant time waste)
[OK] #3 AI Reliability (unreliable AI code)
[OK] #4 Testing (biggest mistake) - Production bugs
[OK] #5 Time Waste (significant hours lost)
[OK] #6 Integration Failures - Deployment delays
[OK] #7 Documentation Gaps - Knowledge loss
[OK] #8 AI Code Quality - Hallucinated APIs
[OK] #9 Velocity Loss - DORA metrics decline
[OK] #10 AI Readiness Gaps - Immature CI/CD
[OK] #11 Code Review Decline - -27% comment rate
[OK] #12 Team Breakdowns - Knowledge silos

---

## Architecture

**Zero Pollution:**
- Global storage: ~/.claude/ (all projects share)
- Project storage: ZERO files created
- Updates: One command updates all projects
- Token efficiency: Optimized via progressive loading

**Progressive Loading:**
- Always loaded: Baseline principles ({C_PRINCIPLE_COUNT} C_ + {U_PRINCIPLE_COUNT} U_)
- Auto-activated: {SKILL_COUNT} skills via semantic matching (load {P_PRINCIPLE_COUNT} P_ on-demand)

**Skill-Based Intelligence:**
- Claude autonomously loads what's needed
- No manual skill activation required
- Skills reference relevant P_ principles

---

## Quick Start

**First time?**
```bash
/cco-audit --quick         # Fast health assessment
/cco-audit --security      # Find vulnerabilities
/cco-fix --security        # Auto-fix issues
```

**Want comprehensive check?**
```bash
/cco-audit --quick         # Fast health assessment
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
# If empty or fewer files than expected, run:
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

Next: /cco-help (command reference) or /cco-audit --quick (project health)
```

---

## Error Cases

**Pattern:** Pattern 5 (Error Handling)

If components missing:
```markdown
[ERROR] Health: Incomplete installation

Missing components:
- Commands: incomplete (missing: update, remove, help)
- Skills: incomplete (missing: some security skills)
- Agents: [OK]

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
