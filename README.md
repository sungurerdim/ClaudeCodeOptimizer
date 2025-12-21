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

## Quick Start

### Step 1: Install
```bash
pip install claudecodeoptimizer && cco-install
```

### Step 2: Configure (First Run)
Inside Claude Code:
```
/cco-config    # Auto-detect your project, confirm settings
```
This creates your project context in `.claude/rules/cco/context.md`. Restart Claude Code after.

### Step 3: Verify
```
/cco-status    # See your project scores and metrics
```

**Done.** Start coding with safety nets in place.

### Common Workflows

| I want to... | Use |
|--------------|-----|
| Set up a new project | `/cco-config` |
| See project health | `/cco-status` |
| Fix security/quality issues | `/cco-optimize` |
| Review architecture | `/cco-review` |
| Make a commit | `/cco-commit` |
| Prepare a release | `/cco-preflight` |
| Regular maintenance | `/cco-checkup` |
| Research a topic | `/cco-research` |

---

## What CCO Does

| Layer | What It Adds | Example |
|-------|--------------|---------|
| **Pre-** | Safety checks before action | Git status, dirty state handling |
| **Process** | Standardized workflows | Approval flow, priority classification |
| **Post-** | Verification and reporting | `Applied: N | Skipped: N | Failed: N` |
| **Context** | Project-aware behavior | Scale-adjusted thresholds, stack-specific checks |

## What CCO Does NOT Do

- **Teach Claude to code** - Opus 4.5 already knows
- **Replace your judgment** - Every change requires approval
- **Add overhead** - Rules are guidance, not blockers
- **Lock you in** - Export to AGENTS.md anytime

---

## Commands

| Command | Purpose |
|---------|---------|
| `/cco-config` | Project configuration: detection + settings + export |
| `/cco-status` | Metrics dashboard with trends |
| `/cco-optimize` | Security + Quality + Hygiene scans with fix mode |
| `/cco-review` | Architecture analysis |
| `/cco-research` | Multi-source research with reliability scoring |
| `/cco-commit` | Quality-gated atomic commits |
| `/cco-preflight` | Pre-release workflow (optimize + review + verify) |
| `/cco-checkup` | Regular maintenance (status + optimize --fix) |

**Agents:** `cco-agent-analyze` (read-only), `cco-agent-apply` (write), `cco-agent-research` (read-only)

*[Full commands documentation](docs/commands.md)* | *[Full agents documentation](docs/agents.md)*

---

## Rules

CCO uses a 4-category rules system with **925 rules total**:

| Category | Rules | Loading |
|----------|-------|---------|
| **Core** | 62 | Always active (`~/.claude/rules/cco/`) |
| **AI** | 39 | Always active (`~/.claude/rules/cco/`) |
| **Tools** | 106 | Built into commands/agents |
| **Adaptive** | 718 | Selected per project → `.claude/rules/cco/` |

**Categories:**
- **Core** - Fundamental principles: DRY, Fail-Fast, Clean Code, Security, Testing
- **AI** - Behavior patterns: Read First, No Hallucination, Semantic Density
- **Tools** - CCO workflow: Approval Flow, Fix Workflow, Safety Classification
- **Adaptive** - Stack-based: 5 languages, 20+ frameworks, 25+ dependencies

### Supported Stacks

<details>
<summary><b>Click to expand full list</b></summary>

| Category | Supported | Example Rules |
|----------|-----------|---------------|
| **Languages** | Python, TypeScript, JavaScript, Go, Rust | Type hints, import order, error handling |
| **App Types** | CLI, Library, API, Frontend, Mobile, Desktop | Exit codes, tree-shaking, REST methods, a11y |
| **Game Dev** | Pygame, Phaser, Three.js, Unity, Unreal, Godot | Frame budget, asset loading, input mapping |
| **AI/ML** | Transformers, LangChain, Whisper, OpenAI, Anthropic | Lazy model load, quantization, batch inference |
| **Data** | Pandas, Polars, Dask, Spark | Chunked reading, lazy eval, memory optimization |
| **Media** | FFmpeg, MoviePy, OpenCV, Pillow, Librosa | Streaming, format handling, GPU acceleration |
| **Infrastructure** | Docker, K8s, Serverless, Monorepo | Multi-stage builds, probes, selective testing |
| **Backend** | REST, GraphQL, gRPC, WebSocket | Pagination, rate limiting, reconnect logic |
| **Database** | SQLAlchemy, Prisma, TypeORM, Redis | N+1 prevention, migrations, cache invalidation |
| **Auth & Payment** | NextAuth, Clerk, Stripe, PayPal | Token security, webhook verification, audit trails |
| **Communication** | SendGrid, Twilio, Firebase, Elasticsearch | Bounce handling, delivery status, search indexing |
| **Blockchain** | Web3, Ethers, Hardhat, Foundry | Gas estimation, nonce management, testnet-first |
| **XR** | WebXR, OpenXR, AR Foundation | 90fps budget, comfort settings, device fallbacks |
| **IoT** | MQTT, MicroPython, ESPHome | Reconnect logic, OTA updates, power management |

</details>

### Why Adaptive Rules Matter

| Without CCO | With CCO |
|-------------|----------|
| Claude applies generic patterns | Claude applies **domain-specific best practices** |
| "Add caching somewhere" | "Use TTL + invalidation for this data fetch" |
| Generic error handling | Language-specific: `raise from` (Python), `?` operator (Rust) |

*[Full rules documentation](docs/rules.md)*

---

## Safety Features

| Feature | What It Does |
|---------|--------------|
| **Git Safety** | Checks status before changes, enables rollback |
| **Approval Flow** | Priority-based (CRITICAL→LOW), safe vs risky classification |
| **Verification** | `Applied: N | Skipped: N | Failed: N` accounting |

**Fix Workflow:** Analyze → Report → Approve → Apply → Verify

| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |

---

## Installation

**Requirements:** Python 3.10+ | Claude Code CLI or IDE extension | Zero runtime dependencies

```bash
# pip (recommended)
pip install claudecodeoptimizer && cco-install

# pipx (isolated)
pipx install claudecodeoptimizer && cco-install

# Upgrade
pip install -U claudecodeoptimizer && cco-install

# Uninstall
cco-uninstall
```

### Local Mode (Project-Specific)

```bash
cco-install --local . --statusline cco-full --permissions balanced
```

| Statusline | Description |
|------------|-------------|
| `cco-full` | Project, Branch, Changes, Git status |
| `cco-minimal` | Project, Branch only |

| Permissions | Description |
|-------------|-------------|
| `safe` | Read-only auto-approved |
| `balanced` | Read + lint/test auto-approved |
| `permissive` | Most operations auto-approved |
| `full` | Maximum auto-approval |

---

## Advanced

<details>
<summary><b>Dynamic Context Injection</b></summary>

CCO commands use Claude Code's `!` backtick syntax for **real-time context at load time**:

```markdown
## Context
- Git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Project type: !`grep "^Type:" .claude/rules/cco/context.md`
```

| Traditional | With Dynamic Context |
|-------------|---------------------|
| 1. Load command | 1. Load command |
| 2. AI calls `git status` tool | 2. Context **already injected** |
| 3. Wait for response | 3. AI starts immediately |
| 4. AI processes result | |

**Benefits:** No tool call round-trip | Real data, no guessing | Reduced hallucination

</details>

---

## Standards & Compliance

Built on official Anthropic documentation and Claude Code best practices:

| Feature | CCO Implementation |
|---------|-------------------|
| [Slash Commands][slash-commands] | 8 commands with YAML frontmatter |
| [Sub-agents][sub-agents] | 3 single-responsibility agents |
| [Rules Directory][memory] | 4-category rule system (925 rules) |
| [Permissions][cc-changelog] | 4 levels (safe→full) |

**Rules Based On:** SSOT, DRY, YAGNI, KISS (Core) | Read-First, No-Hallucination (AI) | OWASP, Least-Privilege (Security)

### References

| Resource | Topics |
|----------|--------|
| [Claude 4 Best Practices][claude4-bp] | Prompt patterns, parallel execution |
| [Claude Code Docs][slash-commands] | Commands, sub-agents, rules |
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
