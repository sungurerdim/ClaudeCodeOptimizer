# Claude Code Optimizer (CCO)

> **This project has evolved into [dev-skills](https://github.com/sungurerdim/dev-skills)** — a tool-agnostic, production-grade skill system covering the full software lifecycle.

[![Successor: dev-skills](https://img.shields.io/badge/successor-dev--skills-blue?style=for-the-badge)](https://github.com/sungurerdim/dev-skills)

---

## What happened?

CCO started as a Claude Code-specific guardrail system — structured rules to prevent scope creep, over-engineering, and hallucinated imports. After 800+ commits and 4 major versions, the core ideas proved valuable enough to generalize:

| What CCO proved | What dev-skills does with it |
|----------------|------------------------------|
| Quality gates prevent AI mistakes | Multi-phase execution with gates in every skill |
| Structured rules > free-form prompts | 19 orchestrated skills with phases, gates, and error recovery |
| AI has systematic weaknesses | 8 weaknesses explicitly addressed (hallucination, scope creep, confidence bias, ...) |
| Skills need coordination | `.findings.md` inter-skill communication standard |
| One tool isn't enough | Works with Claude Code, Cursor, Copilot, Windsurf, Aider, and any AI coding tool |

## What's in dev-skills?

19 production-grade skills covering the full software lifecycle:

```
scaffold → code → test → review → commit → PR → deploy → launch → marketing → analytics
```

Every CCO skill has a dev-skills equivalent — plus 11 new skills that CCO never had:

| CCO Skill | dev-skills Equivalent | New in dev-skills |
|-----------|----------------------|-------------------|
| `/cco-review` | `/ds-review` | `/ds-compliance` — regulatory audit (GDPR, CCPA, HIPAA) |
| `/cco-commit` | `/ds-commit` | `/ds-mobile` — mobile app audit (145+ rules) |
| `/cco-pr` | `/ds-pr` | `/ds-fix` — universal format/lint/typecheck |
| `/cco-blueprint` | `/ds-blueprint` | `/ds-test` — test generation and lifecycle |
| `/cco-docs` | `/ds-docs` | `/ds-init` — project scaffolding |
| `/cco-research` | `/ds-research` | `/ds-deploy` — deployment and infrastructure |
| `/cco-repo` | `/ds-repo` | `/ds-launch` — store submission and release |
| | | `/ds-backend` — API, database, auth design |
| | | `/ds-market` — marketing strategy and growth |
| | | `/ds-analytics` — privacy-first analytics |
| | | `/ds-cv` — professional CV generation |

## Migrate to dev-skills

```bash
git clone https://github.com/sungurerdim/dev-skills.git /tmp/dev-skills

# Copy any skill you need
cp -r /tmp/dev-skills/ds-review ~/.claude/skills/ds-review
cp -r /tmp/dev-skills/ds-commit ~/.claude/skills/ds-commit
# ... or copy all: cp -r /tmp/dev-skills/ds-* ~/.claude/skills/

rm -rf /tmp/dev-skills
```

No binary, no installer, no build step. Just markdown files.

## CCO guardrails

CCO's passive guardrails (`cco-rules.md`) remain valuable as global rules for Claude Code. They complement dev-skills without conflict. If you're already using them, keep them — they work independently.

---

> **[Go to dev-skills →](https://github.com/sungurerdim/dev-skills)**

---

<details>
<summary>Original CCO documentation (archived)</summary>

### What CCO was

**Structured guardrails for Claude Code.** Every rule tuned to how the model actually thinks — minimal touch, maximum impact.

| Without CCO | With CCO |
|-------------|----------|
| Adds AbstractValidatorFactory for simple validation | Only requested changes |
| Edits 5 files when asked for 1 fix | Scoped to the task |
| Guesses requirements silently | Stops and asks |
| Method grows to 200 lines | ≤50 lines, ≤3 nesting |
| Hallucinates imports that don't exist | Verifies before writing |

### Skills (archived)

| Skill | What it did |
|-------|------------|
| `/cco-review` | Scan and fix code quality + architecture issues |
| `/cco-commit` | Quality-gated atomic commits with branch management |
| `/cco-pr` | Create release-please compatible PRs with auto-merge |
| `/cco-blueprint` | Profile project health, set targets, track progress |
| `/cco-docs` | Find documentation gaps and generate missing content |
| `/cco-research` | Multi-source research with CRAAP+ reliability scoring |
| `/cco-repo` | Repository health, settings, CI/CD, and team config |

### Install (archived)

**macOS / Linux:**
```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') && mkdir -p ~/.local/bin && curl -fsSL https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-$(uname -s | tr A-Z a-z)-$ARCH -o ~/.local/bin/cco && chmod +x ~/.local/bin/cco && ~/.local/bin/cco install
```

**Windows (PowerShell):**
```powershell
$b="$HOME\.local\bin"; New-Item $b -ItemType Directory -Force >$null; irm https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/latest/download/cco-windows-amd64.exe -OutFile "$b\cco.exe"; & "$b\cco.exe" install
```

</details>

**[GitHub](https://github.com/sungurerdim/ClaudeCodeOptimizer)** · **[Changelog](CHANGELOG.md)** · MIT License
