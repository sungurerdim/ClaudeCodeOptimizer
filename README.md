# ClaudeCodeOptimizer

A process and standards layer for Claude Code.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## What CCO Is (and Isn't)

**Claude Code with Opus 4.5 is already powerful.** It can analyze code, find bugs, refactor safely, and generate quality output. CCO doesn't replace or enhance these capabilities—they're already excellent.

**CCO adds process structure:**

- **Consistent workflows** - Same audit categories, same verification patterns, every time
- **Quality guardrails** - Standards injected into `CLAUDE.md` that the AI follows
- **Project calibration** - Context-aware thresholds based on your team size, scale, and data sensitivity

Think of it this way: Opus 4.5 knows *how* to fix a security issue. CCO provides a *systematic process* for finding all issues, prioritizing them, getting approval, and verifying fixes.

---

## Project Calibration

Different projects have different needs. A solo side project doesn't need the same rigor as a team building a fintech API.

**How `/cco-calibrate` works:**

1. **Detect** - Scans your project for stack, tools, team indicators
2. **Confirm** - You review and adjust the detected values
3. **Store** - Context saved to your project's `CLAUDE.md`
4. **Apply** - Commands adjust thresholds based on this context

**Example thresholds:**

| Context | Effect |
|---------|--------|
| Solo developer | Self-review sufficient, simpler solutions preferred |
| Team of 6+ | Formal review patterns, stricter quality gates |
| Handles PII | Security checks prioritized, encryption guidance |
| Public API | API stability warnings, versioning reminders |

**Stored format:**

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {detected}
Team: {Solo|2-5|6+} | Scale: {<100|100-10K|10K+} | Data: {Public|PII|Regulated}
Stack: {detected} | Type: {detected}

## Guidelines
- {context-specific guidance}
<!-- CCO_CONTEXT_END -->
```

---

## Installation

```bash
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

---

## Commands

| Command | What it does |
|---------|--------------|
| `/cco-audit` | Run categorized checks, get prioritized fix suggestions |
| `/cco-review` | Architecture analysis with structured output |
| `/cco-generate` | Generate tests, docs, CI configs following project conventions |
| `/cco-health` | Metrics dashboard (coverage, complexity, issues) |
| `/cco-refactor` | Rename/restructure with reference verification |
| `/cco-optimize` | Reduce context size, remove dead code |
| `/cco-commit` | Commit with quality checks |
| `/cco-calibrate` | Set project context for threshold calibration |
| `/cco-config` | Configure statusline and permissions |
| `/cco-status` | Check installation |
| `/cco-help` | Command reference |

---

## Usage Examples

**Find and fix issues:**
```bash
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
Finds ALL references, updates in order, verifies with grep.

**Optimize context:**
```bash
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
| `--security` | OWASP, secrets, CVEs |
| `--ai-security` | Prompt injection, PII |
| `--ai-quality` | Hallucinated APIs, AI patterns |
| `--database` | N+1, indexes, queries |
| `--tests` | Coverage, isolation, flaky |
| `--tech-debt` | Dead code, complexity |
| `--performance` | Caching, algorithms |
| `--hygiene` | TODOs, orphans, hardcoded |
| `--self-compliance` | Check against project's own stated rules |
| `--dora` | Deploy frequency, MTTR |
| `--compliance` | GDPR, licenses |
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
📁 project/src |👤 user    | 2.1M |CC 1.0.23|🤖 Opus 4.5
┌──────────────┬───────────┬──────┬─────────┬────────────┐
│🔗 repo:main  │Conflicts:0│Stash:2│Ahead: 3 │Last: 02:45 │
├──────────────┼───────────┼──────┼─────────┼────────────┤
│Unstaged +  42 -  18      │edit 3│new  2   │del  0│move 0│
│Staged   +  15 -   3      │edit 1│new  1   │del  0│move 0│
└──────────────┴───────────┴──────┴─────────┴────────────┘
```

**Features:** Path, user, project size, CC version, model, git branch, conflicts, stash, commits ahead, last commit time, unstaged/staged changes with line counts.

### Permission Levels

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

- Offers to commit before major changes
- Auto-detects stack, skips non-applicable checks
- Safe fixes can auto-apply; risky ones need approval
- Verification: `done + skip + fail + cannot_do = total`
- Reference integrity: find ALL refs → update in order → verify with grep

---

## Included Standards

CCO adds standards to `~/.claude/CLAUDE.md` that guide the AI's recommendations. These are guidelines, not rigid rules—the AI applies them with judgment based on your project context.

**18 categories, 132 guidelines** — [view full list](claudecodeoptimizer/content/standards/cco-standards.md)

| Category | Examples |
|----------|----------|
| **Core** | Path conventions, reference integrity, verification accounting |
| **Approval Flow** | Priority tabs, risk labels, multiselect options |
| **Code Quality** | Complexity limits, type annotations, SemVer |
| **Security** | Input validation, OWASP patterns, secrets management |
| **AI-Assisted** | Review AI output, Plan→Act→Review workflow |
| **Architecture** | Event-driven patterns, dependency injection |
| **Operations** | Infrastructure as Code, observability |
| **Testing** | Coverage targets, CI gates, contract testing |
| **Performance** | Indexing, N+1 prevention, caching patterns |
| **API** | REST conventions, pagination, error formats |
| **Accessibility** | WCAG guidance, semantic HTML |
| **Reliability** | Timeouts, retries, graceful degradation |

Not all standards apply to every project. The AI uses your project context (from `/cco-calibrate`) to decide which are relevant.

---

## Structure

After `cco-setup`, the following is added to `~/.claude/`:

```
~/.claude/
├── commands/
│   └── cco-*.md          # 11 slash commands
├── agents/
│   └── cco-*.md          # 3 specialized agents
└── CLAUDE.md             # Standards (17 categories)
```

---

## Verification

```bash
cco-status     # Terminal
/cco-status    # Claude Code
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

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
