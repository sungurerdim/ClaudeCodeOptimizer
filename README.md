# ClaudeCodeOptimizer

A process and standards layer for Claude Code.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Quickstart

```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

Then inside Claude Code:

```
/cco-calibrate
/cco-audit --smart
```

---

## What CCO Is (and Isn't)

**Claude Code with Opus 4.5 is already powerful.** It can analyze code, find bugs, refactor safely and generate quality output. CCO doesn't replace or enhance these capabilities. They're already excellent.

**CCO turns that power into repeatable workflows:**

- **Context-aware commands** - Each command reads your project profile and adjusts its behavior
- **Structured processes** - Same audit categories, same verification patterns, every time
- **Approval flow** - Priority-based suggestions with risk labels, you decide what to apply

Think of it this way: Opus 4.5 knows *how* to fix a security issue. CCO provides *structured commands* that scan systematically, prioritize by impact, get your approval and verify the fixes.

---

## Project Calibration

Different projects have different needs. A solo side project doesn't need the same rigor as a team building a fintech API.

**How `/cco-calibrate` works:**

1. **Check** - Verify CCO installation and config health
2. **Detect** - Scan your project for stack, tools, team indicators
3. **Confirm** - You review and adjust the detected values
4. **Store** - Context saved to your project's `CLAUDE.md`
5. **Status** - Display complete CCO status and next steps

**What gets confirmed (12 questions):**

| Call | Questions |
|------|-----------|
| Core | Purpose, Team, Scale, Data |
| Technical | Stack, Type, Database, Rollback |
| Approach | Maturity, Breaking Changes, Priority |
| Compliance | Requirements (if Data≠Public) |

**Example thresholds:**

| Context | Effect |
|---------|--------|
| Solo developer | Self-review sufficient, simpler solutions preferred |
| Team of 6+ | Formal review patterns, stricter quality gates |
| Handles PII | Security checks prioritized, encryption guidance |
| Maturity: Legacy | Wrap don't modify, strangler pattern preferred |
| Priority: Speed | MVP mindset, ship fast, iterate |
| Breaking: Never | Adapters required, full backward compatibility |

**Auto-detected (no questions asked):**

Monorepo structure, pre-commit hooks, current coverage, linting setup, API endpoints, containers, i18n, auth patterns, license type, secrets in repo, outdated deps.

**Stored format:**

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {detected}
Team: {Solo|2-5|6+} | Scale: {<100|100-10K|10K+} | Data: {Public|PII|Regulated}
Stack: {detected} | Type: {detected} | DB: {None|SQL|NoSQL} | Rollback: {Git|DB|User-data}
Maturity: {Greenfield|Active|Maintenance|Legacy} | Breaking: {Allowed|Minimize|Never} | Priority: {Speed|Balanced|Quality}

## Guidelines
- {context-specific guidance}

## Operational
Tools: {format}, {lint}, {test}
Applicable: {checks list}

## Auto-Detected
Structure: {monorepo|single-repo} | Hooks: {pre-commit|none} | Coverage: {N%}
License: {type} | Secrets: {yes|no} | Outdated: {N deps}
<!-- CCO_CONTEXT_END -->
```

---

## Installation

```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

---

## Why Commands?

You can always ask Claude Code directly: *"Check my code for security issues"*. It works. So why use `/cco-audit --security`?

**The difference:**

| Manual Prompt | CCO Command |
|---------------|-------------|
| Results vary each time | Same structured output every time |
| You remember what to check | Categories defined, nothing missed |
| Generic suggestions | Calibrated to your project context |
| You track what's done | Verification: `done + skip + fail = total` |
| Approval is implicit | Priority tabs with risk labels |

**Example flow:**

```
/cco-audit --security

1. Read project context (team size, data sensitivity, stack)
2. Scan with applicable checks (skip non-relevant)
3. Prioritize findings (Critical → High → Medium → Low)
4. Present with risk labels ([safe], [risky], [extensive])
5. You select what to fix
6. Apply fixes, verify each one
7. Summary: "5 done, 1 skipped, 0 failed"
```

This is **on-demand quality**: you decide when to run it, CCO ensures it's thorough and consistent.

---

## Commands

| Command | What it does |
|---------|--------------|
| `/cco-calibrate` | Set project context + check installation + show status |
| `/cco-audit` | Run categorized checks, get prioritized fix suggestions |
| `/cco-review` | Architecture analysis with structured output |
| `/cco-generate` | Generate tests, docs, CI configs following project conventions |
| `/cco-health` | Metrics dashboard (coverage, complexity, issues) |
| `/cco-refactor` | Rename/restructure with reference verification |
| `/cco-optimize` | Reduce context size, remove dead code |
| `/cco-commit` | Commit with quality checks |
| `/cco-config` | Configure statusline and permissions |

---

## Usage Examples

**Find and fix issues:**
```bash
/cco-audit                      # Interactive: choose scope + auto-fix
/cco-audit --smart              # Auto-detect stack, find issues, offer fixes
/cco-audit --security --auto-fix  # Auto-fix safe security issues
/cco-audit --critical           # security + ai-security + database + tests
```

**Generate missing components:**
```bash
/cco-generate --tests           # Unit/integration tests
/cco-generate --openapi         # API documentation
/cco-generate --cicd            # CI/CD pipelines
```

**Safe refactoring:**
```bash
/cco-refactor rename oldName newName
```
Guides Claude to find all references, update them in order and verify with grep.

**Optimize context:**
```bash
/cco-optimize                   # Interactive: choose mode
/cco-optimize --context         # Reduce CLAUDE.md tokens
/cco-optimize --code-quality    # Remove dead code, unused imports
```

**Strategic review:**
```bash
/cco-review                     # Full architecture review
/cco-review --quick             # Gap analysis only
/cco-review --focus=structure   # Focus on organization
```

**Project context:**
```bash
/cco-calibrate                  # Auto-detect and confirm project context
/cco-calibrate --update         # Force re-detection
```
Sets team size, scale, data sensitivity for calibrated recommendations.

**Configure settings:**
```bash
/cco-config                     # Interactive (scope, statusline, permissions)
/cco-config --global            # Apply to all projects (~/.claude/)
/cco-config --local             # This project only (./.claude/)
```

---

## Audit Categories

| Flag | Checks |
|------|--------|
| `--security` | OWASP-inspired patterns, secrets, CVE patterns |
| `--ai-security` | Prompt injection, PII handling |
| `--ai-quality` | Hallucinated APIs, AI code patterns |
| `--database` | N+1, indexes, queries |
| `--tests` | Coverage, isolation, flaky |
| `--tech-debt` | Dead code, complexity |
| `--performance` | Caching, algorithms |
| `--hygiene` | TODOs, orphans, hardcoded |
| `--self-compliance` | Check against project's own stated rules |
| `--dora` | DORA-style indicators (deploy frequency, MTTR hints) |
| `--compliance` | GDPR-related risks, license checks (not legal advice) |
| `--api-contract` | Breaking changes |
| `--docs` | Docstrings, API docs |
| `--cicd` | Pipeline, quality gates |
| `--containers` | Dockerfile, K8s |
| `--supply-chain` | Dependency CVEs |

**Meta-flags:** `--smart`, `--critical`, `--weekly`, `--pre-release`, `--all`, `--auto-fix`

---

## Configuration

`/cco-config` helps configure Claude Code's statusline and permission settings.

### Statusline

Optional status display with git integration:

```
 project/src       |   user   |  2.1MB  | CC 1.0.23 |  Opus 4.5
┌───────────────────┬──────────┬─────────┬───────────┬────────────┐
│ main              │ Conf 0   │ Stash 2 │ Ahead 3   │ Last 02:45 │
├───────────────────┼──────────┼─────────┼───────────┼────────────┤
│ Unstaged +42 -18  │ edit 3   │ new 2   │ del 0     │ move 0     │
│ Staged   +15 -3   │ edit 1   │ new 1   │ del 0     │ move 0     │
└───────────────────┴──────────┴─────────┴───────────┴────────────┘
```

**Features:** Path, user, project size, CC version, model, git branch, conflicts, stash, commits ahead, last commit time, unstaged/staged changes with line counts.

### Permission Levels

CCO never tells Claude to "do anything it wants". Every command runs inside an allow-list and deny-list model so that risky actions are explicit, reviewable and easy to disable.

| Level | Model | Security | Flexibility | Use Case |
|-------|-------|----------|-------------|----------|
| **Safe** | Whitelist | High | Low | Maximum security, manual approval |
| **Balanced** | Whitelist | High | Medium | Normal workflow (recommended) |
| **Permissive** | Blacklist | Medium | High | Minimal prompts, trusted projects |

### Core Commands (300+ pre-approved)

Cross-platform CLI tools auto-approved in Balanced/Permissive modes:

| Category | Commands |
|----------|----------|
| **Git** | status, diff, log, show, branch, commit, stash, blame, bisect, reflog... |
| **File System** | ls, dir, cat, head, tail, find, tree, ln, stat, file, mktemp... |
| **Text Processing** | grep, rg, sed, awk, jq, yq, sort, uniq, cut, tr, column, paste... |
| **Hash/Checksum** | md5sum, sha256sum, sha512sum, shasum, cksum, b2sum, openssl dgst |
| **Archive** | tar, zip, gzip, bzip2, xz, zstd, lz4, 7z, rar, cpio |
| **Encoding** | base64, base32, xxd, od, hexdump, iconv, dos2unix |
| **Process/Time** | timeout, sleep, time, watch, nohup, nice, ps, top, htop, uptime |
| **Disk/Storage** | du, df, lsblk, findmnt, mount, ncdu, duf |
| **Network** | ping, curl, wget, nc, nslookup, dig, whois, netstat, ss, lsof |
| **System Info** | env, date, whoami, hostname, uname, arch, neofetch |
| **Math** | bc, dc, expr, factor, seq, shuf, numfmt |
| **Terminal** | printf, tput, stty, clear, screen, tmux |
| **Windows/PowerShell** | findstr, tasklist, wmic, Get-*, Select-*, Format-*, ConvertTo-Json |

### Stack-Specific Commands

Auto-detected based on project files, added to allow list:

| Stack | Tools |
|-------|-------|
| **Python** | python, pip, poetry, uv, conda, pytest, ruff, mypy, black, bandit, sphinx, uvicorn, celery, jupyter |
| **Node.js** | node, npm, yarn, pnpm, bun, eslint, prettier, tsc, jest, vitest, playwright, webpack, vite, prisma |
| **Rust** | cargo, rustc, rustfmt, clippy, cargo-audit, cargo-nextest, miri, wasm-pack |
| **Go** | go, gofmt, golangci-lint, govulncheck, delve, air, wire |
| **Java** | java, javac, mvn, gradle, checkstyle, junit, spring-boot, quarkus |
| **.NET** | dotnet, nuget, msbuild, xunit, nunit |
| **Ruby** | ruby, gem, bundle, rake, rails, rspec, rubocop |
| **PHP** | php, composer, phpunit, phpstan, laravel |
| **Swift** | swift, swiftlint, xcodebuild, fastlane, pod |
| **C/C++** | gcc, clang, cmake, ninja, meson, valgrind, gdb |
| **Docker** | docker, docker-compose, podman, buildah, trivy, hadolint |
| **Kubernetes** | kubectl, helm, k9s, kustomize, minikube, argocd, flux |
| **Terraform** | terraform, tofu, terragrunt, tflint, tfsec, checkov |
| **Cloud** | aws, gcloud, az, pulumi, vercel, netlify, fly |
| **Database** | psql, mysql, redis-cli, mongosh, sqlite3 |
| **Data/ML** | dvc, mlflow, airflow, dbt, spark-submit |

### Always Denied (Security)

These are blocked at all permission levels:

| Category | Blocked Commands |
|----------|------------------|
| **Destructive** | `rm -rf /`, `rm -rf ~/`, `format`, `mkfs`, `dd if=` |
| **Privilege** | `sudo`, `su`, `chmod 777`, `chown root` |
| **System** | `shutdown`, `reboot`, `halt` |
| **Git Dangerous** | `git push --force`, `git reset --hard`, `git clean -fdx` |
| **Sensitive Files** | Edit `~/.ssh/`, `~/.aws/`, `**/.env*`, `**/secrets/**` |

---

## Behaviors

- Offers to commit before major changes (Pre-Operation Safety)
- Auto-detects stack, skips non-applicable checks
- Safe fixes can auto-apply; risky ones need approval (Safety Classification)
- Verification: `done + skip + fail + cannot_do = total`
- Reference integrity: find all refs, update in order, verify with grep

---

## Standards Structure

CCO adds standards to `~/.claude/CLAUDE.md` that guide the AI's recommendations. These are guidelines, not rigid rules. The AI applies them with judgment based on your project context.

### Core Standards (Always Apply)

| Section | Purpose |
|---------|---------|
| **Workflow** | Pre-Operation Safety, Context Read, Safety Classification |
| **Core** | Path conventions, reference integrity, verification accounting |
| **Approval Flow** | Priority tabs, risk labels, multiselect options |
| **AI-Assisted** | Review AI output, Plan→Act→Review workflow |
| **Quality** | Code quality, testing, security core (always applicable) |
| **Docs** | README, API docs, ADR, comments |

### Conditional Standards (Apply When Relevant)

| Section | When Applied |
|---------|--------------|
| **Security Extended** | Container/K8s detected, Scale 10K+, PII/Regulated data |
| **Architecture** | Scale 10K+, microservices detected |
| **Operations** | Scale 10K+, CI/CD detected |
| **Performance** | Scale 100-10K+, performance critical |
| **Data** | Database detected |
| **API** | REST/GraphQL endpoints detected |
| **Frontend** | Frontend frameworks detected |
| **i18n** | Multi-language requirement detected |
| **Reliability** | Scale 10K+, SLA requirements |
| **Cost** | Cloud/Container infrastructure detected |
| **DX** | Team size 2-5+ |
| **Compliance** | Compliance requirements detected |

[View full standards](claudecodeoptimizer/content/standards/cco-standards.md)

---

## Structure

After `cco-setup`, the following is added to `~/.claude/`:

```
~/.claude/
├── commands/
│   └── cco-*.md          # 9 slash commands
├── agents/
│   └── cco-*.md          # 3 specialized agents
└── CLAUDE.md             # Standards (Core + Conditional)
```

---

## Verification

```bash
/cco-calibrate    # Check installation, config health, project context
```

---

## Uninstallation

```bash
cco-remove
pip uninstall claudecodeoptimizer
```

---

## Requirements

- Python 3.11+
- Claude Code

---

## What CCO Doesn't Do

CCO is not a magic "fix everything" button. It's a thin, opinionated layer on top of Claude Code that standardizes how you ask for audits, refactors, fixes and reviews, and how Claude reports back what it did.

CCO doesn't directly modify your codebase. It gives Claude Code a consistent workflow and standards to follow, so that each command produces structured, reproducible results.

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
