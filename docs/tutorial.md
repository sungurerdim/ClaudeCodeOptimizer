# Getting Started with CCO

## Getting Started Journey

### New to CCO? Follow This Path

**Level 1: First 5 Minutes** (Essential - Start Here)

Get CCO running and see immediate value:

```bash
# 1. Install globally
pip install claudecodeoptimizer

# 2. Navigate to your project
cd /path/to/your/project

# 3. Initialize (AI auto-detects everything)
/cco-init

> **See**: [Features → Intelligent Project Initialization](features.md#intelligent-project-initialization) for how AI detection works

# 4. Check project health
/cco-status

# 5. Run your first audit
/cco-audit
```

**What you'll have after 5 minutes:**
- ✅ Project configured with principles:
  - Universal principles (U001-U014, 14 always included)
  - Project-specific principles (P001-P069, 20-40 AI-selected)
- ✅ Slash commands ready to use (8-15 selected from 28 available)

> **See**: [Features → Slash Commands](features.md#slash-commands) for complete command list
- ✅ `CLAUDE.md` with minimal principle references (existing content preserved)
- ✅ First audit report showing code quality, security, and test status

**Typical output:** "Found 12 code quality issues, 3 security concerns, test coverage at 45%"

---

**Level 2: Daily Workflow** (Common Tasks - Use These Regularly)

Once initialized, these commands become your daily tools:

**Fix Issues:**
```bash
/cco-fix code          # Fix code quality issues (unused imports, type hints, etc.)
/cco-fix security      # Fix security vulnerabilities (secrets, input validation, etc.)
/cco-fix docs          # Fix documentation issues (missing docstrings, outdated READMEs)
```

**Optimize & Generate:**
```bash
/cco-optimize-deps     # Update dependencies, fix known vulnerabilities
/cco-optimize-code     # Remove dead code, unused imports, deprecated functions
/cco-generate tests    # Generate test scaffolding for untested modules
/cco-generate docs     # Generate API documentation, README sections
```

**Semantic Commits:**
```bash
/cco-commit            # AI analyzes changes, groups logically, generates commit messages
                       # Preview mode: shows proposed commits, you confirm
```

**What you'll gain from daily usage:**
- ⚡ **Faster development:** Automated fixes save 30-60 minutes/day
- 🐛 **Fewer bugs:** Security and quality issues caught early
- 📝 **Better commits:** Semantic messages improve git history searchability
- 🧹 **Cleaner codebase:** Automated cleanup prevents tech debt accumulation

---

**Level 3: Power Features** (Advanced - When You're Ready)

Unlock full CCO capabilities:

**Multi-Agent Orchestration:**
- CCO automatically uses multiple agents in parallel (2-3x faster)
- Haiku for scanning/detection (fast & cheap)
- Sonnet for analysis/synthesis (smart & thorough)
- You don't configure this - it's built into commands

**Custom Configuration:**
```bash
/cco-init --mode=interactive    # Interactive mode: confirm each detection/decision
/cco-config                     # View/modify project configuration
```

**Advanced Workflows:**
- Git Flow integration (main, develop, feature branches)
- GitHub Flow with PR templates and code review checklists
- Semantic versioning automation
- Multi-project consistency (same standards across repos)

**Report Management:**
- All reports stored in `~/.cco/projects/<project>/reports/`
- Timestamped for history tracking
- Compare audits over time to measure improvement

**What you'll master:**
- 🎯 **Full control:** Customize principles, commands, workflows per project
- 🤝 **Team collaboration:** Consistent standards across team members
- 📊 **Progress tracking:** Measure code quality improvements over time
- 🔄 **Workflow automation:** CI/CD integration, pre-commit hooks, automated audits

---

### Progression Example

**Week 1:** Use Level 1 commands (init, status, audit) to understand current state
**Week 2:** Add Level 2 to daily workflow (fix, optimize, commit)
**Week 3:** Explore Level 3 for team collaboration and automation

**By Week 4:** CCO is integral to your development process, quality metrics improving measurably.
