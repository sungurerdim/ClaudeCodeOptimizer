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

- **[cco-standards.md](../cco-standards.md)** - Standard structure, execution protocol, file discovery
- **[cco-standards.md](../cco-standards.md)** - UX/DX, efficiency, simplicity, performance standards
- **[cco-patterns.md](../cco-patterns.md)** - Reusable patterns (Step 0, Selection, Accounting, Progress, Error Handling)
- **[cco-standards.md](../cco-standards.md)** - File discovery, model selection, parallel execution

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
├── principles/    ({PRINCIPLE_COUNT} principles: {U_PRINCIPLE_COUNT} universal + {C_PRINCIPLE_COUNT} claude-specific)
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

**See [cco-patterns.md](../cco-patterns.md#pattern-8-dynamic-results-generation) for reporting pattern.**

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
- {U_PRINCIPLE_COUNT} Universal (cco-principle-u-*) - Always active
- {C_PRINCIPLE_COUNT} Claude-specific (cco-principle-c-*) - Always active

**Skills ({SKILL_COUNT} - Auto-Activate on Demand):**

Security & Privacy (5):
- cco-skill-security-fundamentals (OWASP, XSS, SQL injection, CSRF)
- cco-skill-ai-security (prompt injection, model security)
- cco-skill-supply-chain (dependencies, SAST)
- cco-skill-containers (Kubernetes security)
- cco-skill-privacy (GDPR, compliance, encryption)

Quality & Testing (3):
- cco-skill-testing-fundamentals (test pyramid, coverage, isolation)
- cco-skill-code-quality (refactoring, complexity)
- cco-skill-ai-quality (code verification, tech debt)

Infrastructure (4):
- cco-skill-database-optimization (N+1, caching, profiling)
- cco-skill-observability (metrics, alerts, SLOs)
- cco-skill-cicd-automation (gates, deployment)
- cco-skill-resilience (circuit breaker, retry, bulkhead)

Architecture (2):
- cco-skill-microservices (CQRS, service mesh, DI)
- cco-skill-incident (on-call, postmortem, playbooks)

Documentation & Git (3):
- cco-skill-documentation (API docs, OpenAPI, ADRs)
- cco-skill-git-workflow (branching, PR review)
- cco-skill-versioning (SemVer, changelog)

Frontend & Mobile (3):
- cco-skill-frontend (bundle, a11y, performance)
- cco-skill-mobile (offline, battery, app store)
- cco-skill-platform-maturity (engineering maturity, DX)

**Agents ({AGENT_COUNT} - Parallel Execution):**
- cco-agent-audit (Haiku - Fast scanning, cost-efficient)
- cco-agent-fix (Sonnet - Accurate fixes, better quality)
- cco-agent-generate (Sonnet - Code generation, better quality)
- cco-agent-optimize (Haiku - Context optimization, token efficiency)

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
- Always loaded: All principles ({U_PRINCIPLE_COUNT} universal + {C_PRINCIPLE_COUNT} claude-specific)
- Auto-activated: {SKILL_COUNT} skills via semantic matching (domain guidance on-demand)

**Skill-Based Intelligence:**
- Claude autonomously loads what's needed
- No manual skill activation required
- Skills provide domain-specific guidance (security, testing, etc.)

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
