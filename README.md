# ClaudeCodeOptimizer

A process and rules layer for Claude Code in the Opus 4.5 era.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/claudecodeoptimizer.svg)](https://pypi.org/project/claudecodeoptimizer/)
[![Claude 4 Best Practices](https://img.shields.io/badge/Claude_4-Best_Practices-blueviolet.svg)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
[![Opus 4.5 Ready](https://img.shields.io/badge/Opus_4.5-Ready-8A2BE2.svg)](https://www.anthropic.com/news/claude-opus-4-5)
[![Claude Code 2.0+](https://img.shields.io/badge/Claude_Code-2.0+-00A67E.svg)](https://github.com/anthropics/claude-code)

> Claude already knows how to code. **CCO adds safety, approval, and consistency.**

![CCO Environment](docs/screenshots/environment.png)
*CCO lives directly inside Claude Code, no extra UI.*

---

## Quickstart

```bash
pip install claudecodeoptimizer && cco-install
```

Inside Claude Code:
```
/cco-config    # Auto-detect your project, confirm once
/cco-status    # See your scores
```

**That's it.** Start coding with safety nets in place.

---

## What CCO Does

| Layer | What It Adds | Example |
|-------|--------------|---------|
| **Pre-** | Safety checks before action | Git status, dirty state handling |
| **Process** | Standardized workflows | Approval flow, priority classification |
| **Post-** | Verification and reporting | `Applied: N \| Skipped: N \| Failed: N` |
| **Context** | Project-aware behavior | Scale-adjusted thresholds, stack-specific checks |

## What CCO Does NOT Do

- **Teach Claude to code** - Opus 4.5 already knows
- **Replace your judgment** - Every change requires approval
- **Add overhead** - Rules are guidance, not blockers
- **Lock you in** - Export to AGENTS.md anytime

---

## Dynamic Context Injection

CCO commands use Claude Code's `!` backtick syntax for **real-time context at load time**:

```markdown
## Context
- Git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Project type: !`grep "^Type:" ./CLAUDE.md`
```

### How It Works

| Traditional | With Dynamic Context |
|-------------|---------------------|
| 1. Load command | 1. Load command |
| 2. AI calls `git status` tool | 2. Context **already injected** |
| 3. Wait for response | 3. AI starts immediately |
| 4. AI processes result | |
| 5. AI continues | |

### Benefits

| Benefit | Description |
|---------|-------------|
| **Speed** | No tool call round-trip, context ready instantly |
| **Accuracy** | AI sees real data, no assumptions or guessing |
| **Token savings** | Eliminates "Let me check..." dialogue |
| **Reduced hallucination** | Facts over inference |

*Inspired by official Claude Code command patterns.*

---

## Rules

CCO uses a 4-category rules system:

| Category | Scope | Loading |
|----------|-------|---------|
| **Core** | Fundamental principles | Always active in CLAUDE.md |
| **AI** | Model agnostic behavior | Always active in CLAUDE.md |
| **Tools** | CCO command/agent mechanisms | Loaded when commands/agents run |
| **Adaptive** | Stack-based rules pool | Only matching rules selected per project |

**Counting:** Rules use two formats:
- List format: `grep -c "^- \*\*" <file>` (core.md, ai.md)
- Table format: `grep -c "| \* " <file>` (adaptive.md)

Run `/cco-config` to see which adaptive rules apply to your project.

### Categories Explained

- **Core** - Fundamental software principles: DRY, Fail-Fast, Clean Code, Security, Testing
- **AI** - AI behavior patterns: Read First, No Hallucination, Semantic Density
- **Tools** - CCO workflow: Approval Flow, Fix Workflow, Safety Classification
- **Adaptive** - Stack-based: Frontend accessibility, API rules, Container security

### Adaptive Rules: 40+ Project Types

`/cco-config` scans your dependencies and project structure, then activates **only relevant rules**. No manual configuration needed.

<details>
<summary><b>Supported Project Types</b> (click to expand)</summary>

| Category | Types | Example Rules |
|----------|-------|---------------|
| **Languages** | Python, TypeScript, JavaScript, Go, Rust | Type hints, import order, error handling patterns |
| **App Types** | CLI, Library, API, Frontend, Mobile, Desktop | Exit codes, tree-shaking, REST methods, a11y |
| **Game Dev** | Pygame/Arcade, Phaser/Three.js, Unity/Unreal/Godot | Frame budget, asset loading, input mapping |
| **AI/ML** | Transformers, LangChain, Whisper, OpenAI, Anthropic | Lazy model load, quantization, batch inference |
| **Data** | Pandas, Polars, Dask, Spark | Chunked reading, lazy eval, memory optimization |
| **Media** | Audio (Whisper, Librosa), Video (FFmpeg, MoviePy), Image (OpenCV, Pillow) | Streaming, format handling, GPU acceleration |
| **Infrastructure** | Docker, K8s, Serverless, Monorepo | Multi-stage builds, probes, selective testing |
| **Backend** | REST, GraphQL, gRPC, WebSocket | Pagination, rate limiting, reconnect logic |
| **Database** | SQLAlchemy, Prisma, TypeORM + Redis, Memcached | N+1 prevention, migrations, cache invalidation |
| **Auth & Payment** | NextAuth, Clerk, Auth0 + Stripe, PayPal | Token security, webhook verification, audit trails |
| **Communication** | SendGrid, Twilio, Firebase, Elasticsearch | Bounce handling, delivery status, search indexing |
| **Blockchain** | Web3, Ethers, Hardhat | Gas estimation, nonce management, testnet-first |
| **XR** | OpenXR, WebXR, AR Foundation | 90fps budget, comfort settings, device fallbacks |
| **IoT** | MicroPython, MQTT, ESPHome | Reconnect logic, OTA updates, power management |

</details>

### Why Adaptive Rules Matter

| Without CCO | With CCO |
|-------------|----------|
| Claude applies generic patterns | Claude applies **domain-specific best practices** |
| "Add caching somewhere" | "Use TTL + invalidation for this data fetch" |
| Misses GPU memory management | Knows to clear CUDA cache, use context managers |
| Generic error handling | Language-specific: `raise from` (Python), `?` operator (Rust) |
| No awareness of dependencies | Sees `faster-whisper` → activates audio chunking, progress callbacks |

**Result:** Fewer iterations, domain-aware suggestions, production-ready code from the first try.

*[Full rules documentation](docs/rules.md)*

---

## Commands

### Base Commands

| Command | Purpose |
|---------|---------|
| `/cco-config` | Project configuration: detection + settings + export |
| `/cco-status` | Metrics dashboard with trends and actionable next steps |
| `/cco-optimize` | Quality + Security + Hygiene (merged audit + optimize) |
| `/cco-review` | Architecture analysis with fresh perspective |
| `/cco-research` | Multi-source research with reliability scoring |
| `/cco-commit` | Quality-gated atomic commits |

### Meta Commands

| Command | Purpose | Orchestrates |
|---------|---------|--------------|
| `/cco-preflight` | Pre-release workflow | optimize + review + changelog + verify |
| `/cco-checkup` | Regular maintenance | status + optimize --fix |

### /cco-optimize Features

- **Security Checks** - OWASP patterns, secrets, CVEs, dependency vulnerabilities
- **Quality Checks** - Complexity, type coverage, test quality, consistency
- **Hygiene Checks** - Orphan detection, stale refs, duplicates, dead code
- **Best Practices Checks** - Pattern adherence, efficiency, naming, error handling
- **2-Tab Selection** - Scope (Security/Quality/Hygiene/Best Practices) + Action (Report/Fix)
- **Smart Mode** - Auto-detect applicable checks based on project context
- **Fix Mode** - Safe fixes applied automatically, risky ones require approval

### /cco-research Features

- **Tiered Reliability Scoring** - 6-tier system (T1-T6) with 0-100 scores
- **Dynamic Modifiers** - Freshness, engagement, author credibility, cross-verification
- **Contradiction Detection** - Identifies conflicting information across sources
- **Consensus Mapping** - Weighted agreement analysis by source tier
- **Bias Detection** - Flags vendor self-promotion, sponsored content
- **AI Synthesis** - Confidence-rated recommendations with reasoning and caveats

### /cco-commit Features

- **Secrets Detection** - Blocks commits with API keys, tokens, passwords, private keys
- **Breaking Change Detection** - Warns on public API changes, prompts for BREAKING CHANGE footer
- **Staged/Unstaged Handling** - Smart analysis based on what user has staged
- **Atomic Grouping** - Auto-groups related changes (impl + tests, renames across files)
- **Large File Warning** - Warns on >1MB files, suggests Git LFS for binaries

### /cco-config Features

- **Unified Flow** - Configure, Remove, and Export in a single command
- **AI Performance Auto-Detection** - Sets thinking/MCP tokens based on project complexity
- **Statusline Configuration** - Full or Minimal mode per project
- **Permission Levels** - Safe, Balanced, Permissive, Full per project
- **Remove Configuration** - Remove any setting (AI Performance, Statusline, Permissions, Rules)
- **Rules Export** - Export to AGENTS.md (universal) or CLAUDE.md (Claude-specific)

### /cco-preflight Features

- **Pre-flight Checks** - Git state, branch, version, changelog, dependencies
- **Quality Gate** - All scopes (security, quality, hygiene, best-practices) via `/cco-optimize --pre-release --fix`
- **Architecture Review** - Quick gap analysis via `/cco-review --quick`
- **Final Verification** - Full test suite, build, lint, type check
- **Changelog & Docs** - Automatic release notes and documentation sync
- **Go/No-Go Summary** - Blockers vs warnings, clear next steps

### /cco-checkup Features

- **Health Dashboard** - Quick scores via `/cco-status --brief`
- **Quality Audit** - All scopes (security, quality, hygiene, best-practices) via `/cco-optimize --fix`
- **Trend Tracking** - Health score changes since last checkup
- **Scheduling** - Weekly recommended for active development

*[Full commands documentation](docs/commands.md)*

---

## Agents

| Agent | Purpose | Mode |
|-------|---------|------|
| **cco-agent-analyze** | Project detection and issue scanning | Read-only |
| **cco-agent-apply** | Execute changes with verification | Write |
| **cco-agent-research** | External source research with reliability scoring | Read-only |

*[Full agents documentation](docs/agents.md)*

---

## Project Configuration

`/cco-config` is the central configuration command with three action types:

**Configure:**
- Detection & Rules - Scan project, write context to `.claude/rules/cco/`
- AI Performance - Set thinking/MCP tokens in `./.claude/settings.json`
- Statusline - Configure status bar (Full or Minimal)
- Permissions - Set permission level (Safe, Balanced, Permissive, Full)

**Remove:**
- Remove any configuration (AI Performance, Statusline, Permissions, Rules)
- Mixed operations supported (e.g., Configure Rules + Remove AI Performance)

**Export:**
- AGENTS.md - Universal format for all AI tools (Codex, Cursor, Copilot, Cline, etc.)
- CLAUDE.md - Full export including Claude-specific tool rules

### AI Performance Auto-Detection

Thinking and MCP output tokens are automatically set based on project complexity:

| Setting | Standard | Medium | High |
|---------|----------|--------|------|
| Thinking Tokens | 5000 | 8000 | 10000 |
| MCP Output Tokens | 25000 | 35000 | 50000 |

> **Note:** Thinking mode toggle is in Claude Code `/config` (Tab to toggle). Enabled by default for Opus 4.5. `MAX_THINKING_TOKENS` controls token budget when enabled.

**Complexity scoring:**
- Microservices, Monorepo → +2 each
- K8s/Helm, ML/AI → +1 each
- Multiple API styles, Large team → +1 each

### Local Settings

All settings are written to `./.claude/settings.json` (project-local):
- AI Performance: `env.MAX_THINKING_TOKENS`, `env.MAX_MCP_OUTPUT_TOKENS`
- Statusline: `statusLine.command`
- Permissions: `permissions.allow`, `permissions.deny`

### Export

Export is integrated into `/cco-config` main flow. Select AGENTS.md (recommended) or CLAUDE.md.

**Format differences:**

| Format | Target | Content |
|--------|--------|---------|
| AGENTS.md | Universal (Codex, Cursor, Copilot, Cline, etc.) | Core + AI rules, model-agnostic |
| CLAUDE.md | Claude Code only | Core + AI + Tool rules, full content |

**AGENTS.md content filtering:**
- Removes Claude-specific tool references (`Read`, `Write`, `Task`, etc.)
- Removes `.claude/` path references
- Removes CCO-specific content (`/cco-*`, `cco-*`)
- Preserves model-agnostic principles (DRY, Fail-Fast, Read-First)

**What is NEVER exported:**
- AI Performance settings
- Statusline configuration
- Permission rules

Export reads from installed files (`~/.claude/rules/cco/` + `.claude/rules/cco/`).

---

## Safety Features

| Feature | What It Does |
|---------|--------------|
| **Git Safety** | Checks status before changes, enables rollback |
| **Approval Flow** | Priority-based (CRITICAL→LOW), safe vs risky classification |
| **Verification** | `Applied: N \| Skipped: N \| Failed: N` accounting |

### Fix Workflow

All fix operations follow: **Analyze → Report → Approve → Apply → Verify**

### Safety Classification

| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |
| Fix linting issues | Delete files |
| Add type annotations | Rename public APIs |

---

## Requirements

- **Python 3.10+** (tested on 3.10–3.14)
- **Claude Code** CLI or IDE extension
- **Zero runtime dependencies** - stdlib only

---

## Installation

```bash
# pip (recommended)
pip install claudecodeoptimizer && cco-install

# pipx (isolated)
pipx install claudecodeoptimizer && cco-install

# Development
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git && cco-install

# Upgrade
pip install -U claudecodeoptimizer && cco-install
```

### Local Mode (Project-Specific)

```bash
# Install statusline and permissions to current project
cco-install --local . --statusline cco-full --permissions balanced

# Statusline only
cco-install --local . --statusline cco-minimal

# Permissions only
cco-install --local . --permissions safe
```

| Statusline | Description |
|------------|-------------|
| `cco-full` | Project, Branch, Changes, Git status |
| `cco-minimal` | Project, Branch only |

| Permissions | Description |
|-------------|-------------|
| `safe` | Read-only auto-approved, writes require approval |
| `balanced` | Read + lint/test auto-approved, writes require approval |
| `permissive` | Most operations auto-approved, dangerous ops blocked |
| `full` | Maximum auto-approval, only destructive ops blocked |

## Uninstallation

```bash
cco-uninstall  # Complete removal with confirmation
```

---

## Design Principles

- **Transparency** - Announce before action, progress signals, no silent operations
- **User Control** - Approval required, priority levels, safe vs risky classification
- **Context-Aware** - Project detection drives thresholds and rules
- **Token Efficient** - Semantic density, conditional loading, bounded context

CCO implements fundamental software engineering principles including SSOT, DRY, YAGNI, KISS, Idempotent, and more. See [Principles Reference](docs/principles-reference.md) for detailed definitions and examples.

*[Full principles documentation](docs/design-principles.md)*

---

## Standards & Compliance

CCO is built on official Anthropic documentation and Claude Code best practices:

### Claude Code 2.0+ Native Features

| Feature | CCO Implementation | Reference |
|---------|-------------------|-----------|
| **[Slash Commands][slash-commands]** | 8 commands with YAML frontmatter | Dynamic context, tool restrictions |
| **[Sub-agents][sub-agents]** | 3 single-responsibility agents | Separate context, limited tools |
| **[Rules Directory][memory]** | 4-category rule system | `~/.claude/rules/cco/` |
| **[Settings.json][cc-changelog]** | Project-local configuration | AI tokens, statusline, permissions |
| **[Permissions][cc-changelog]** | 4 levels (safe→full) | Auto-approve/deny patterns |
| **[Statusline][cc-changelog]** | Custom status bar | Full/Minimal modes |
| **[Background Agents][cc-changelog]** | Parallel execution | Independent context windows |

### Claude 4 Best Practices

| Practice | CCO Implementation |
|----------|-------------------|
| **Parallel Tool Execution** | Independent operations run simultaneously |
| **Explicit Instructions** | Commands specify exact behaviors |
| **Context Motivation** | Rules explain "why" not just "what" |
| **Conservative Judgment** | Evidence-based severity, never guesses |
| **Long-horizon State Tracking** | TodoWrite for progress, git for state |
| **Structured Output** | Consistent `Applied: N \| Skipped: N \| Failed: N` |
| **Subagent Orchestration** | Automatic delegation based on task type |

### Opus 4.5 Optimizations

| Feature | Alignment |
|---------|-----------|
| **Multi-agent Coordination** | Parallel agent spawning |
| **Context Management** | Awareness prompts in commands |
| **Plan Mode Precision** | Commands structured for planning |
| **Tool Use Improvements** | Explicit tool lists in frontmatter |
| **Thinking Mode** | Token budget auto-detection |

### 217+ Rules Based On

- **SSOT, DRY, YAGNI, KISS** - Fundamental software principles
- **Read-First, No-Hallucination** - AI behavior patterns
- **Fail-Fast, Idempotent** - Reliability patterns
- **OWASP, Least-Privilege** - Security standards
- **40+ Project Types** - Stack-specific best practices

See [docs/claude-4-best-practices.md](docs/claude-4-best-practices.md) for implementation details.

### References

| Resource | Topics |
|----------|--------|
| [Claude 4 Best Practices][claude4-bp] | Prompt patterns, parallel execution, state tracking |
| [Claude Code Docs][slash-commands] | Commands, sub-agents, rules, permissions |
| [Claude Code Changelog][cc-changelog] | Feature history, new capabilities |
| [Opus 4.5 Announcement][opus-4-5] | Model capabilities |

[slash-commands]: https://code.claude.com/docs/en/slash-commands
[sub-agents]: https://code.claude.com/docs/en/sub-agents
[memory]: https://code.claude.com/docs/en/memory
[cc-changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[claude4-bp]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
[opus-4-5]: https://www.anthropic.com/news/claude-opus-4-5

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Created by Sungur Zahid Erdim** | [Issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
