---
name: cco-tune
description: Project-specific AI tuning and configuration
---

# /cco-tune

**Project tuning** - Detection, configuration, and export for the current project.

**Standards:** Approval Flow | Output Formatting

## Scope

| Tool | Location | What It Does |
|------|----------|--------------|
| `cco-setup` | `~/.claude/` (global) | Standards + global statusline |
| `cco-tune` | `./` (project local) | Project context + local statusline/permissions |
| `cco-remove` | `~/.claude/` (global) | Uninstall CCO completely |

### Global vs Local

**cco-setup installs global files:**
- `~/.claude/CLAUDE.md` - Universal + AI-Specific + CCO-Specific standards
- `~/.claude/statusline.js` - Global statusline (Full mode)
- `~/.claude/settings.json` - Global statusLine config
- `~/.claude/commands/cco-*.md` - CCO commands
- `~/.claude/agents/cco-*.md` - CCO agents

**cco-tune creates local project files:**
- `./CLAUDE.md` - Project context + conditional standards
- `./.claude/statusline.js` - Local statusline script
- `./.claude/settings.json` - Local settings (AI Performance + Statusline + Permissions)

**Local settings.json merges all configurations:**
```json
{
  "env": {
    "MAX_THINKING_TOKENS": "{detected}",
    "MAX_MCP_OUTPUT_TOKENS": "{detected}",
    "DISABLE_PROMPT_CACHING": "0"
  },
  "statusLine": { "type": "command", "command": "..." },
  "permissions": { "allow": [...], "deny": [...] }
}
```

All values are auto-detected based on project complexity. See [AI Performance Auto-Detection](#ai-performance-auto-detection).

### Content Sources

Files are sourced from `claudecodeoptimizer/content/`:

| Content | Source | Target |
|---------|--------|--------|
| Statusline Full | `content/statusline/full.js` | `.claude/statusline.js` |
| Statusline Minimal | `content/statusline/minimal.js` | `.claude/statusline.js` |
| Permissions Safe | `content/permissions/safe.json` | `.claude/settings.json` |
| Permissions Balanced | `content/permissions/balanced.json` | `.claude/settings.json` |
| Permissions Permissive | `content/permissions/permissive.json` | `.claude/settings.json` |
| Permissions Full | `content/permissions/full.json` | `.claude/settings.json` |

Global `~/.claude/` files are never modified by cco-tune.

## Usage

```bash
/cco-tune              # Show status, then choose what to configure
/cco-tune --export     # Export standards (AGENTS.md or CLAUDE.md)
```

---

## Flow Overview

**Status first, all questions at start, uninterrupted execution after.**

```
1. STATUS     → Always show current project state first
2. CHOOSE     → What to configure? + ALL config questions
3. DETECT     → Run detection (if selected, no questions)
4. REVIEW     → Accept/Edit/Cancel (single confirmation)
5. APPLY      → Write all selected configurations
6. REPORT     → Summary
```

---

## Step 1: Status (Always Runs)

Show current project state before asking anything. Status shows **current values and locations only** - no reasoning (that comes in detection results).

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                              CCO PROJECT STATUS                                ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ PROJECT: {project_name}                                                        ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ CONTEXT (./CLAUDE.md)                                                          ║
├────────────────────────────────────────────────────────────────────────────────┤
║ Purpose         │ {purpose}                                                    ║
║ Team/Scale/Data │ {team} | {scale} | {data}                                    ║
║ Stack/Type      │ {stack} | {type}                                             ║
║ Maturity        │ {maturity} | Breaking: {breaking} | Priority: {priority}     ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ ACTIVE SETTINGS (./.claude/settings.json)                                      ║
├────────────────┬──────────────────────────────────────────────────────────────┤
║ Thinking       │ {value} tokens                                               ║
║ MCP Output     │ {value} tokens                                               ║
║ Caching        │ {on|off}                                                     ║
║ Statusline     │ {Full|Minimal|None}                    ./.claude/statusline.js║
║ Permissions    │ {level} ({N} rules)                                          ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ STANDARDS      │ ~{base} base + {N} project-specific = ~{total}               ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

**If no context exists (first run):**

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                              CCO PROJECT STATUS                                ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ PROJECT: {project_name}                                                        ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ CONTEXT         │ Not configured                                               ║
║ ACTIVE SETTINGS │ Not configured                                               ║
║ STANDARDS       │ ~{base_count} base only (no project-specific)                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## Step 2: Choose Actions + Configure

Based on status, show options with smart defaults. **All configuration questions are asked in this step.**

**If context exists:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ What would you like to do?                                              │
├─────────────────────────────────────────────────────────────────────────┤
│ ☐ Update Detection   Re-detect stack, standards, and AI Performance     │
│ ☐ AI Performance     Override auto-detected thinking/MCP tokens         │
│ ☐ Statusline         Local status bar (./.claude/)                      │
│ ☐ Permissions        Local permission levels (./.claude/)               │
│ ○ Nothing            Exit without changes                               │
└─────────────────────────────────────────────────────────────────────────┘
```

**If no context (first run):**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ What would you like to configure?                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ ☑ Project Detection  [recommended] Detect stack, standards, AI Perf     │
│ ☐ AI Performance     Override auto-detected thinking/MCP tokens         │
│ ☐ Statusline         Local status bar (./.claude/)                      │
│ ☐ Permissions        Local permission levels (./.claude/)               │
└─────────────────────────────────────────────────────────────────────────┘
```

- Detection is pre-selected and marked `[recommended]` when no context exists
- **Detection includes AI Performance auto-calculation** (see [AI Performance Auto-Detection](#ai-performance-auto-detection))
- AI Performance option is only for manual override of auto-detected values
- User can select multiple options
- **cco-tune NEVER modifies global ~/.claude/ files**

### Inline Configuration Questions

**If AI Performance selected** (override auto-detected values):
```
┌─────────────────────────────────────────────────────────────────────────┐
│ AI Performance Override (./.claude/settings.json)                       │
│ Auto-detected: Thinking {detected} | MCP {detected}                     │
├─────────────────────────────────────────────────────────────────────────┤
│ Thinking Tokens: (see AI Performance Auto-Detection for values)         │
│ ○ Standard [detected if score=0]    Simple operations                   │
│ ○ Medium [detected if score=1-2]    Multi-file changes                  │
│ ○ High [detected if score=3+]       Complex reasoning                   │
│                                                                         │
│ MCP Output Tokens: (see AI Performance Auto-Detection for values)       │
│ ○ Standard [detected if <100]       Official default                    │
│ ○ Large [detected if 100-500]       Multiple services                   │
│ ○ Very Large [detected if 500+]     Monorepo/Hyperscale                 │
│                                                                         │
│ Prompt Caching (DISABLE_PROMPT_CACHING):                                │
│ ● On [recommended]                  Reduces cost ~90%                   │
│ ○ Off                               Disable caching                     │
└─────────────────────────────────────────────────────────────────────────┘
```

**Note:** AI Performance is auto-detected during project detection. This option is only for manual override. See [AI Performance Auto-Detection](#ai-performance-auto-detection) for actual values.

**If Statusline selected**, ask mode:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Local statusline mode (./.claude/statusline.js)                         │
├─────────────────────────────────────────────────────────────────────────┤
│ ● Full [current]      5-column table with git info                      │
│ ○ Minimal             Project + git branch only                         │
│ ○ Disable             Remove local statusline                           │
└─────────────────────────────────────────────────────────────────────────┘
```

**When statusline is installed:**
- Copies `content/statusline/full.js` → `./.claude/statusline.js`
- Adds `statusLine` config to `./.claude/settings.json`
- **Local-only:** If `.claude/statusline.js` doesn't exist, nothing runs (no global fallback)

**If Permissions selected**, ask level (narrow → wide):
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Local permission level (./.claude/settings.json)                        │
│ Recommended based on: Team {team} | Data {data} | Compliance {compliance}│
├─────────────────────────────────────────────────────────────────────────┤
│ ○ Safe [recommended if Regulated/PII]        Most restrictive           │
│ ○ Balanced [recommended if Team 2+]          Auto: reads, lint/test     │
│ ○ Permissive                                 Auto: most ops | Ask: del  │
│ ○ Full [recommended if Solo+Public]          300+ allow rules           │
└─────────────────────────────────────────────────────────────────────────┘
```

**Permission Level Auto-Detection:**

| Condition | Recommended Level | Rationale |
|-----------|-------------------|-----------|
| Data: Regulated or Compliance: Any | Safe | Security-first for compliance |
| Data: PII or Confidential | Safe | Protect sensitive data |
| Team: 2+ (not Solo) | Balanced | Team coordination needs review |
| Team: Solo + Data: Public | Full | Maximum productivity for solo devs |
| Default | Balanced | Safe middle ground |

After all questions answered → proceed to detection/apply (no more questions)

---

## Step 3: Detection (if selected)

**Location:** `./CLAUDE.md` (project only)

**IMPORTANT:** Detection always scans from scratch, ignoring any existing CCO_CONTEXT values. Each element is freshly detected from actual project files. The Source column shows where the value was found.

### Auto-Detect Elements

| # | Element | Detection Source | Triggers | Standards |
|---|---------|------------------|----------|-----------|
| 1 | Purpose | README.md first paragraph | - | - |
| 2 | Stack | package.json, pyproject.toml, go.mod | - | - |
| 3 | Type | Entry points, project structure | CLI or Library | +5 |
| 4 | DB | Dependencies, config files | Backend > Data | +5 |
| 5 | CI/CD | .github/workflows/, .gitlab-ci.yml | Backend > Operations | +7 |
| 6 | API | Routes, endpoints, OpenAPI | Backend > API | +6 |
| 7 | Frontend | react, vue, angular in deps | Frontend | +10 |
| 8 | Mobile | Podfile, build.gradle, pubspec | Apps > Mobile | +6 |
| 9 | Desktop | electron, tauri in deps | Apps > Desktop | +4 |
| 10 | ML/AI | torch, tensorflow, sklearn | Specialized > ML/AI | +6 |
| 11 | Game | Unity, Unreal, Godot files | Specialized > Game | +4 |
| 12 | Serverless | serverless.yml, sam.yaml | Infra > Serverless | +4 |
| 13 | Monorepo | nx.json, turbo.json, lerna | Infra > Monorepo | +4 |
| 14 | Container | Dockerfile, docker-compose | Infra > Container | +5 |
| 15 | K8s | k8s/, helm/, kustomization | Infra > Container | +5 |
| 16 | i18n | locales/, i18n config | Collab > i18n | +5 |
| 17 | Microservices | Multiple services detected | Scale & Arch | +12 |
| 18 | License | LICENSE file | - | - |
| 19 | Coverage | pytest-cov, coverage reports | - | - |
| 20 | Secrets Risk | .env patterns, hardcoded | Security | +12 |
| 21 | AI Performance | Complexity score from above | → settings.json | - |

**GRANULAR:** Each detection triggers only its specific subsection. Multiple detections stack additively.

---

### AI Performance Auto-Detection

AI Performance settings are **automatically calculated** based on detected project complexity.

> **Note:** Claude Code does not define fixed tiers. These are **CCO-recommended values** based on project complexity. Official docs only specify: MAX_MCP_OUTPUT_TOKENS default=25000, warning at 10000. MAX_THINKING_TOKENS is disabled by default.

#### Thinking Tokens (MAX_THINKING_TOKENS)

| Complexity | CCO Value | Detected When | Rationale |
|------------|-----------|---------------|-----------|
| High | 10000 | Microservices, Monorepo, Enterprise, Hyperscale | Complex multi-service reasoning |
| Medium | 8000 | K8s, ML/AI, Multiple APIs, Large team/scale | Multi-file changes |
| Standard | 5000 | CLI, Library, Monolith, Solo/Small team | Simple operations |

**Scoring Logic:**
- +2: Microservices detected
- +2: Monorepo detected
- +1: K8s/Helm detected
- +1: ML/AI detected
- +1: Multiple API styles (REST + GraphQL + gRPC)
- +1: Team size Large (16+) or Enterprise (51+)
- +1: Scale Large (100K+) or Hyperscale (1M+)

**Score → Value mapping (CCO defaults, adjust per project):**
- Score 0 → Standard tier
- Score 1-2 → Medium tier
- Score 3+ → High tier

#### MCP Output Tokens (MAX_MCP_OUTPUT_TOKENS)

| Codebase Size | CCO Value | Detected When | Rationale |
|---------------|-----------|---------------|-----------|
| Very Large | 50000 | Monorepo, Hyperscale, 500+ files | Large tool outputs |
| Large | 35000 | 100-500 files, Multiple services | Medium tool outputs |
| Standard | 25000 | <100 files (official default) | Default per docs |

**Scoring Logic:**
- File count via `find . -type f -name "*.{py,js,ts,go,rs}" | wc -l`
- Monorepo → Very Large tier
- 100-500 files → Large tier
- <100 files → Standard tier (official default)

#### Prompt Caching (DISABLE_PROMPT_CACHING)

| Setting | Value | When |
|---------|-------|------|
| Enabled | `"0"` or not set | Always recommended (reduces cost ~90%) |
| Disabled | `"1"` | Only if explicitly requested |

**Note:** All `env` values must be **strings**, not numbers or booleans.

**Official Reference:** https://code.claude.com/docs/en/settings

---

### User-Configurable Elements

These elements cannot be auto-detected and require user input. Each option includes:
- **Description**: When to choose this option
- **Impact**: What standards/guidelines are activated
- **Labels**: `[detected]` from code, `[recommended]` best fit, `[current]` existing value

---

#### 1. Team Size

**Question:** How many people actively contribute to this codebase?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| Solo | `[recommended if no CODEOWNERS]` | Single developer, no code review needed | Guidelines only |
| Small (2-5) | `[recommended if small CODEOWNERS]` | Informal reviews, async communication works | +4 Team basics |
| Medium (6-15) | - | Formal reviews needed, communication overhead grows | +8 Team |
| Large (16-50) | - | Multiple teams, need CODEOWNERS, ADRs mandatory | +8 Team + ADR |
| Enterprise (51+) | - | Scaling frameworks (SAFe/LeSS), cross-team coordination | +8 Team + Scaling |

**Detection hints:** CODEOWNERS file, git log unique authors, team config files

---

#### 2. Scale (Users/Load)

**Question:** How many concurrent users or requests per second does your system handle?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| Prototype (<100) | `[recommended for new projects]` | Development/testing, no production traffic | - |
| Small (100-1K) | - | Early production, single instance sufficient | +3 Caching basics |
| Medium (1K-100K) | - | Growth stage, need horizontal scaling | +12 Scale & Arch |
| Large (100K-1M) | - | High traffic, requires sophisticated architecture | +12 Scale + +12 Security |
| Hyperscale (1M+) | - | Massive scale, distributed systems expertise required | +12 Scale + +12 Security + +6 Performance |

**Impact:** Higher scale activates circuit breakers, caching strategies, connection pooling, load balancing patterns.

---

#### 3. Data Sensitivity

**Question:** What is the most sensitive type of data your system processes?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| Public | `[recommended if no auth]` | Open data, no login required, no personal info | - |
| Internal | - | Company data, requires authentication | +2 Auth basics |
| Confidential | - | Business-sensitive, NDA-level protection | +4 Auth + Encryption |
| PII | `[recommended if user accounts]` | Personal Identifiable Information (names, emails, addresses) | +12 Security |
| Regulated | - | Healthcare (PHI), financial, or government data | +12 Security + Compliance |

**Impact:** Activates encryption at rest, audit logging, data retention policies, access controls.

---

#### 4. Compliance Requirements

**Question:** Which compliance frameworks must your system satisfy? (multi-select)

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| None | `[recommended if B2C/internal]` | No formal compliance requirements | - |
| SOC2 | - | B2B SaaS, enterprise customers require security attestation | +12 Security + Audit |
| HIPAA | `[recommended if healthcare]` | US healthcare data (PHI) protection | +12 Security + PHI controls |
| PCI-DSS | `[recommended if payments]` | Payment card data processing | +12 Security + PCI controls |
| GDPR | `[recommended if EU users]` | EU user data, privacy rights, consent management | +12 Security + Privacy |
| CCPA | - | California consumer privacy, similar to GDPR | +12 Security + Privacy |
| ISO27001 | - | International security management standard | +12 Security + ISMS |
| HITRUST | - | Healthcare + security combined framework | +12 Security + Full audit |
| FedRAMP | - | US federal government cloud services | +12 Security + Gov controls |
| DORA | - | EU financial services digital resilience (2025+) | +12 Security + Resilience |

**Impact:** Activates specific control frameworks, audit logging, data handling procedures, documentation requirements.

---

#### 5. Architecture Pattern

**Question:** What is the primary architecture pattern of your system?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| Monolith | `[recommended for small teams]` | Single deployable unit, simpler operations | - |
| Modular Monolith | - | Monolith with clear module boundaries, prep for splitting | +2 Bounded Contexts |
| Microservices | `[detected if multiple services]` | Independent services, complex but scalable | +12 Scale & Arch |
| Serverless | `[detected if Lambda/Functions]` | Event-driven functions, pay-per-use | +4 Serverless |
| Hybrid | - | Mix of patterns based on domain needs | Context-dependent |

**Impact:** Microservices activates service mesh, API versioning, distributed tracing, circuit breakers.

---

#### 6. API Style

**Question:** What API protocol does your system expose? (multi-select)

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| None | `[recommended for CLI/desktop]` | No external API, internal only | - |
| REST | `[detected if routes/endpoints]` | Standard HTTP APIs, resource-oriented | +6 API |
| GraphQL | `[detected if graphql deps]` | Flexible queries, single endpoint | +6 API + GraphQL |
| gRPC | `[detected if proto files]` | High-performance RPC, binary protocol | +6 API + gRPC |
| WebSocket | `[detected if ws deps]` | Real-time bidirectional communication | +3 Real-time |
| Webhook | - | Event callbacks to external systems | +2 Webhook patterns |

**Impact:** Activates OpenAPI specs, rate limiting, pagination, error handling standards.

---

#### 7. Deployment Strategy

**Question:** How is your application deployed to production?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| Manual | - | SSH/FTP deploys, no automation | - |
| CI/CD | `[detected if workflows]` | Automated build, test, deploy pipeline | +7 Operations |
| GitOps | - | Git as source of truth, ArgoCD/Flux | +7 Ops + +3 GitOps |
| Platform | - | PaaS (Heroku, Vercel, Railway) handles deployment | +7 Ops + +2 Platform |

**Impact:** Activates CI gates, deployment strategies (blue/green, canary), rollback procedures.

---

#### 8. Testing Strategy

**Question:** What level of testing does your project maintain?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| Minimal | - | Ad-hoc testing, no formal coverage | - |
| Unit | `[detected if test framework]` | Unit tests only, >60% coverage target | +3 Testing basics |
| Standard | `[recommended]` | Unit + integration tests, >80% coverage | +5 Testing |
| Comprehensive | - | Unit + integration + E2E + visual regression | +8 Full testing |
| Performance | - | Above + load testing, benchmarks | +8 Testing + +4 Perf |

**Impact:** Activates coverage requirements, test isolation, CI gates, performance benchmarks.

---

#### 9. SLA Level

**Question:** What uptime commitment does your system have?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| None | `[recommended for internal tools]` | No formal SLA, best-effort availability | - |
| Standard (99%) | - | ~7h downtime/month acceptable | +2 Monitoring basics |
| High (99.9%) | - | ~43min downtime/month, needs redundancy | +4 Observability |
| Critical (99.99%) | - | ~4min downtime/month, HA required | +8 HA + DR |
| Mission-Critical (99.999%) | - | ~26sec downtime/month, global redundancy | +12 Full resilience |

**Impact:** Activates health endpoints, alerting, disaster recovery, multi-region deployment patterns.

---

#### 10. Real-time Requirements

**Question:** Does your system require real-time data updates?

| Value | Label | Description | Standards |
|-------|-------|-------------|-----------|
| None | `[recommended for CRUD apps]` | Request-response only, polling acceptable | - |
| Soft (seconds) | - | Near real-time, SSE or polling every few seconds | +2 Basic real-time |
| Hard (100ms) | `[detected if websocket]` | WebSocket, immediate updates required | +5 Real-time |
| Ultra-low (<10ms) | - | Gaming, trading, requires specialized infrastructure | +8 Low-latency |

**Impact:** Activates WebSocket patterns, event-driven architecture, message queuing.

---

#### 11. Maturity Stage

**Question:** What is the current development stage of your project?

| Value | Label | Description | Guidelines |
|-------|-------|-------------|------------|
| Prototype | - | Proof of concept, may be discarded | Move fast, skip docs |
| Greenfield | `[recommended for new repos]` | New project, no legacy constraints | Aggressive refactoring OK |
| Active | - | Ongoing development, regular releases | Balanced approach |
| Stable | - | Feature-complete, maintenance mode | Conservative changes |
| Legacy | - | Old codebase, minimal changes | Wrap don't modify |
| Sunset | - | End of life, planning deprecation | Document for migration |

**Impact:** Affects refactoring aggressiveness, documentation requirements, testing rigor.

---

#### 12. Breaking Changes Policy

**Question:** How should breaking changes be handled?

| Value | Label | Description | Guidelines |
|-------|-------|-------------|------------|
| Allowed | `[recommended for v0.x]` | Breaking changes in any release | Clean API over compat |
| Minimize | `[recommended for v1.x+]` | Deprecate first, provide migration path | SemVer strictly |
| Never | - | Zero breaking changes (enterprise libraries) | Adapters required |

**Impact:** Affects API versioning, deprecation policies, migration tooling.

---

#### 13. Priority Focus

**Question:** What is the primary development priority?

| Value | Label | Description | Guidelines |
|-------|-------|-------------|------------|
| Speed | - | Ship fast, iterate quickly | MVP mindset |
| Balanced | `[recommended]` | Standard practices, reasonable coverage | Normal workflow |
| Quality | - | Thorough testing, extensive review | No shortcuts |
| Security | - | Security-first development | Threat modeling |
| Cost | - | Optimize for infrastructure costs | Efficiency focus |

**Impact:** Affects review rigor, testing requirements, documentation depth.

### AI Performance (Auto-Detected)

AI Performance is **automatically calculated** during detection. See [AI Performance Auto-Detection](#ai-performance-auto-detection) for values and scoring logic.

| Element | Settings Key | Tiers | Official Default |
|---------|--------------|-------|------------------|
| Thinking | `env.MAX_THINKING_TOKENS` | Standard / Medium / High | Disabled |
| MCP | `env.MAX_MCP_OUTPUT_TOKENS` | Standard / Large / Very Large | Standard |
| Caching | `env.DISABLE_PROMPT_CACHING` | `"0"` = on, `"1"` = off | on (not set) |

**Written to:** `./.claude/settings.json` (local only, never global)

---

## Step 4: Review Detection Results

Show unified table with dynamic standard counts. **Source column shows where value was detected; Standards column shows what gets triggered.**

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                            CCO DETECTION RESULTS                                     ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║  #  │ Element       │ Value                  │ Source                  │ Standards   ║
╠═════╪═══════════════╪════════════════════════╪═════════════════════════╪═════════════╣
║     │ AUTO-DETECTED (from project files)                                             ║
├─────┼───────────────┼────────────────────────┼─────────────────────────┼─────────────┤
║  1  │ Purpose       │ {purpose}              │ {file}:{line}           │ -           ║
║  2  │ Stack         │ {stack}                │ {config_file}           │ -           ║
║  3  │ Type          │ {type}                 │ {detection_method}      │ +{N} {cat}  ║
║  4  │ DB            │ {db|None}              │ {source|(not detected)} │ +5 Data     ║
║  5  │ CI/CD         │ {provider|None}        │ {workflow_path}         │ +7 Ops      ║
║  6  │ API           │ {style|None}           │ {source|(not detected)} │ +6 API      ║
║  7  │ Frontend      │ {framework|None}       │ {source|(not detected)} │ +10 Frontend║
║  8  │ Container     │ {yes|None}             │ {source|(not detected)} │ +5 Container║
║  9  │ License       │ {license_type}         │ {license_file}          │ -           ║
║ 10  │ Coverage      │ {N}%                   │ {coverage_source}       │ -           ║
║ 11  │ Secrets Risk  │ {yes|no}               │ {scan_result}           │ +12 Security║
╠═════╪═══════════════╪════════════════════════╪═════════════════════════╪═════════════╣
║     │ AI PERFORMANCE (auto-calculated → ./.claude/settings.json)                     ║
├─────┼───────────────┼────────────────────────┼─────────────────────────┼─────────────┤
║ 12  │ Thinking      │ {value} ({tier})       │ complexity: {score}     │ → env       ║
║ 13  │ MCP Output    │ {value} ({tier})       │ files: {count}          │ → env       ║
║ 14  │ Caching       │ {on|off}               │ {reason}                │ → env       ║
╠═════╪═══════════════╪════════════════════════╪═════════════════════════╪═════════════╣
║     │ USER CONFIGURABLE (defaults shown, editable)                                   ║
├─────┼───────────────┼────────────────────────┼─────────────────────────┼─────────────┤
║ 15  │ Team          │ {team_size}            │ {detection_hint}        │ {standards} ║
║ 16  │ Scale         │ {scale}                │ {source|default}        │ {standards} ║
║ 17  │ Data          │ {sensitivity}          │ {detection_hint}        │ {standards} ║
║ 18  │ Compliance    │ {frameworks|None}      │ {source|default}        │ {standards} ║
║ 19  │ Architecture  │ {pattern}              │ {detection_hint}        │ {standards} ║
║ 20  │ Deployment    │ {strategy}             │ {source}                │ (in #5)     ║
║ 21  │ Testing       │ {level}                │ {detection_hint}        │ {standards} ║
║ 22  │ Maturity      │ {stage}                │ {detection_hint}        │ guidelines  ║
║ 23  │ Breaking      │ {policy}               │ {detection_hint}        │ guidelines  ║
║ 24  │ Priority      │ {focus}                │ {source|default}        │ guidelines  ║
║ 25  │ SLA           │ {level|None}           │ {source|default}        │ {standards} ║
║ 26  │ Real-time     │ {requirement|None}     │ {detection_hint}        │ {standards} ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║ STANDARDS TRIGGERED                                                                  ║
├──────────────────────────────────────────────────────────────────────────────────────┤
║ {subsection} (+{N}) │ {subsection} (+{N}) │ ... = +{total} project-specific          ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║ TOTAL: ~{base_count} base + {N} project-specific = ~{total} standards                ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

**Source column values:**
| Source Type | Format | Description |
|-------------|--------|-------------|
| File detected | `{filename}` or `{filename}:{line}` | Specific file where value was found |
| Directory detected | `{path}/` | Directory pattern matched |
| Pattern matched | `{pattern} detected` | Code pattern or file structure matched |
| Not found | `(not detected)` | Element not present in project |
| Default value | `default` | User-configurable with no detection hint |
| Derived | `{derivation_source}` | Inferred from other project characteristics |
| Recommended | `recommended ({reason})` | CCO recommendation with rationale |

**Standards column values:**
- `+N {subsection}` - triggers N standards from named subsection
- `→ env` - writes to settings.json env section
- `guidelines` - affects guidelines generation, not standards count
- `(in #N)` - already counted in row N
- `-` - no standards triggered

**Standard counts are calculated dynamically** from `cco-standards-conditional.md` based on triggers.

### Review Options

```
┌─────────────────────────────────────────────────────────────────┐
│ Detection complete. What would you like to do?                  │
├─────────────────────────────────────────────────────────────────┤
│ ○ Accept        Apply this configuration                        │
│ ○ Edit          Change specific items                           │
│ ○ Cancel        Exit without changes                            │
└─────────────────────────────────────────────────────────────────┘
```

**If Edit selected**, ask which items to change:
```
┌─────────────────────────────────────────────────────────────────┐
│ Which items would you like to edit?                             │
├─────────────────────────────────────────────────────────────────┤
│ ☐ Edit all      Configure all editable items                    │
│ ☐ 21: Team      Currently: Solo                                 │
│ ☐ 22: Scale     Currently: <100                                 │
│ ☐ 23: Data      Currently: Public                               │
└─────────────────────────────────────────────────────────────────┘
```

- First option "Edit all" selects all editable items
- Other options show item number, name, and current value
- User selects which items to edit (multiSelect: true)
- Then show individual questions for each selected item

**For each selected item**, show options with recommendations and affected standards:

```
┌─────────────────────────────────────────────────────────────────┐
│ #{N} {element} - {question}?                                    │
├─────────────────────────────────────────────────────────────────┤
│ ○ {option_1}   [{current|detected}] {description}               │
│ ○ {option_2}   {description}                                    │
│ ○ {option_3}   {description}                                    │
│                                                                 │
│ Affects: {affected_categories}                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 5: Apply

Write all selected configurations to **project-local files only**:

| Selection | Target | Content |
|-----------|--------|---------|
| Detection | `./CLAUDE.md` | CCO_CONTEXT block |
| AI Performance | `./.claude/settings.json` | env.MAX_THINKING_TOKENS, env.MAX_MCP_OUTPUT_TOKENS, env.DISABLE_PROMPT_CACHING |
| Statusline | `./.claude/statusline.js` + `./.claude/settings.json` | Status bar script + statusLine config |
| Permissions | `./.claude/settings.json` | permissions.allow, permissions.deny, permissions.ask |

**CRITICAL:** All files are ALWAYS overwritten with the latest content from source files, even if they appear unchanged. This ensures any subtle differences from older versions are corrected.

**IMPORTANT:** cco-tune NEVER modifies global `~/.claude/` files. All settings are project-local.

### Statusline Files

**Source:** `claudecodeoptimizer/content/statusline/`

| Mode | Source File | Output |
|------|-------------|--------|
| Full | `statusline/full.js` | `Project \| Branch \| Changes` |
| Minimal | `statusline/minimal.js` | `Project \| Branch` |
| Disable | Remove files | No statusline |

**Target:** `./.claude/statusline.js` + `statusLine` config in `./.claude/settings.json`

**Local-Only Behavior:** Only runs if local `.claude/statusline.js` exists. No global fallback.

**Disable Mode:** Delete statusline.js and remove `statusLine` from settings.json.

### Statusline Verification

After writing statusline files, verify:
1. `./.claude/statusline.js` exists and is executable
2. `./.claude/settings.json` contains `statusLine` config pointing to local script
3. JSON structure is valid (same format as Claude Code settings)

---

### Permission Files

**Source:** `claudecodeoptimizer/content/permissions/`

| Level | Source File | Description |
|-------|-------------|-------------|
| Safe | `permissions/safe.json` | Most restrictive - read-only auto-approved |
| Balanced | `permissions/balanced.json` | Read + lint/test auto-approved, writes require approval |
| Permissive | `permissions/permissive.json` | Most operations auto-approved, only dangerous ops blocked |

**Target:** `./.claude/settings.json` → `permissions` key

**Permission Structure:**
```json
{
  "permissions": {
    "allow": [
      "# Allowed patterns - auto-approved",
      "git status *",
      "npm test"
    ],
    "deny": [
      "# Denied patterns - blocked or require approval",
      "rm -rf *",
      "git push --force *"
    ]
  }
}
```

**Permission Levels Summary:**

| Category | Safe | Balanced | Permissive |
|----------|------|----------|------------|
| Git read (status, log, diff) | Auto | Auto | Auto |
| Git write (commit, push) | Ask | Ask | Auto |
| Git dangerous (force push, reset --hard) | Deny | Deny | Deny |
| Lint/Format (check mode) | Ask | Auto | Auto |
| Lint/Format (write mode) | Ask | Ask | Auto |
| Test execution | Ask | Auto | Auto |
| Package install | Ask | Ask | Auto |
| File read (ls, cat) | Auto | Auto | Auto |
| File write (touch, mkdir) | Ask | Ask | Auto |
| File delete (rm) | Ask | Ask | Ask |
| File delete recursive (rm -rf) | Deny | Deny | Deny |
| Docker (non-privileged) | Ask | Ask | Auto |
| Docker (privileged) | Deny | Deny | Deny |
| System (sudo, chmod 777) | Deny | Deny | Deny |

### Permission Verification

After writing permission config, verify:
1. `./.claude/settings.json` contains valid `permissions` object
2. No conflicting patterns (same pattern in both allow and deny)
3. JSON syntax is valid

### CCO_CONTEXT Format

```markdown
<!-- CCO_CONTEXT_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | Data: {data} | Compliance: {compliance}
Stack: {stack} | Type: {type} | DB: {db} | Rollback: Git
Architecture: {pattern} | API: {style} | Deployment: {strategy}
Maturity: {maturity} | Breaking: {breaking} | Priority: {priority}
Testing: {strategy} | SLA: {level} | Real-time: {requirement}

## Guidelines
{generated based on values - see Guidelines Generation section}

## Operational
Tools: {format}, {lint}, {test}
Conventions: {detected patterns}
Applicable: {check categories}
Not Applicable: {excluded categories}

## Auto-Detected
Structure: {type} | Hooks: {status} | Coverage: {N}%
{checklist of detected features}
License: {type}
Secrets detected: {yes|no}
Outdated deps: {N}

## Conditional Standards (auto-applied)
**TOTAL: +{N} project-specific ({subsections})**

{matched project-specific standards with counts}
<!-- CCO_CONTEXT_END -->
```

**Note:** AI Performance settings are NOT stored in CLAUDE.md - they are only in `./.claude/settings.json` where Claude Code reads them. The CCO_CONTEXT documents project characteristics that inform AI Performance auto-detection.

---

## Step 6: Report

Show before/after comparison for all changed settings:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                            CCO TUNE COMPLETE                                   ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ CHANGES APPLIED (all local, no global modifications)                           ║
├────────────────┬───────────────────┬───────────────────┬───────────────────────┤
║ Setting        │ Before            │ After             │ Reason                ║
├────────────────┼───────────────────┼───────────────────┼───────────────────────┤
║ Context        │ {before|none}     │ {after}           │ {reason}              ║
║ Thinking       │ {before|none}     │ {value} tokens    │ complexity: {score}   ║
║ MCP Output     │ {before|none}     │ {value} tokens    │ files: {count}        ║
║ Caching        │ {before|none}     │ {on|off}          │ {reason}              ║
║ Statusline     │ {before|none}     │ {mode}            │ {reason}              ║
║ Permissions    │ {before|none}     │ {level} ({N})     │ {reason}              ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ STANDARDS                                                                      ║
├────────────────┬───────────────────────────────────────────────────────────────┤
║ Base           │ ~{base_count} (Universal + AI + CCO)                          ║
║ Project        │ +{N} ({triggered_subsections})                                ║
║ Total          │ ~{total} standards                                            ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ FILES WRITTEN                                                                  ║
├────────────────────────────────────────────────────────────────────────────────┤
║ ./CLAUDE.md                    Project context + conditional standards         ║
║ ./.claude/settings.json        env + statusLine + permissions                  ║
║ ./.claude/statusline.js        Status bar script (if statusline configured)    ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ Restart Claude Code for changes to take effect                                 ║
║ Next: /cco-health to verify | /cco-audit --smart to check                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

**Before/After rules:**
- `{none}` - setting didn't exist before
- `{unchanged}` - value is the same (skip row or show for reference)
- Only show rows for settings that were actually configured in this session
- Reason column shows detection source or user choice

---

## Export Mode (--export)

Export current configuration to portable format.

### Export Choice

```
┌─────────────────────────────────────────────────────────────────┐
│ Export format                                                   │
├─────────────────────────────────────────────────────────────────┤
│ ○ AGENTS.md     For other AI tools (Cursor, Windsurf, etc.)     │
│                 Universal + AI-Specific + Project-Specific      │
│                 (CCO-Specific excluded - not portable)          │
│                                                                 │
│ ○ CLAUDE.md     For sharing with other Claude Code projects     │
│                 All categories including CCO-Specific           │
└─────────────────────────────────────────────────────────────────┘
```

### Export Content by Format

| Category | AGENTS.md | CLAUDE.md |
|----------|-----------|-----------|
| Universal | Included | Included |
| AI-Specific | Included | Included |
| CCO-Specific | **Excluded** | Included |
| Project-Specific | Included (triggered only) | Included (triggered only) |

### AGENTS.md Format (Prose)

```markdown
# Project Standards

> Exported from CCO (ClaudeCodeOptimizer)

## Project Context
{type} project built with {stack}
Team: {team} | Scale: {scale} | Data: {data}

## Universal Standards
{all universal standards}

## AI-Specific Standards
{all AI-specific standards}

## Project-Specific Standards
{triggered standards only}
```

### CLAUDE.md Format

Exports the full CCO_CONTEXT block including CCO-Specific standards for use in other Claude Code projects.

---

## Standards Count Structure

Standards are organized in 4 categories. **All counts are dynamically calculated from source files.**

| Category | Source File | Scope |
|----------|-------------|-------|
| Universal | `cco-standards.md` | All projects |
| AI-Specific | `cco-standards.md` | All AI assistants |
| CCO-Specific | `cco-standards.md` | CCO users only |
| Project-Specific | `cco-standards-conditional.md` | Triggered by detection |

**Base standards:** Universal + AI-Specific + CCO-Specific = ~{base_count} (count `^- ` lines in source)
**Project-specific:** Up to ~{max_conditional} additional (count `^- ` lines in conditional source)

**Count calculation:**
- Count `^- ` lines (bullet points starting with `- `) in each section
- Tables count as guidance, not individual standards
- Counts are dynamic - always recalculate from source files

---

## Detection → Standards Mapping

**GRANULAR APPROACH:** Each subsection is independently evaluated. Only matching subsections are activated.

### Complete Trigger → Standards Mapping

#### Auto-Detected Triggers

| Trigger | Detection Method | Standards Activated |
|---------|------------------|---------------------|
| **Type: CLI** | `__main__.py`, `[project.scripts]`, `bin/` | Apps > CLI (+5) |
| **Type: Library** | No entry point, exports only | Library (+5) |
| **API: REST** | Routes, endpoints, OpenAPI spec | Backend > API (+6) |
| **API: GraphQL** | graphql deps, schema files | Backend > API (+6) + GraphQL |
| **API: gRPC** | `.proto` files, grpc deps | Backend > API (+6) + gRPC |
| **API: WebSocket** | ws/socket.io deps | Real-time (+5) |
| **DB detected** | ORM, migrations, connection strings | Backend > Data (+5) |
| **CI/CD detected** | `.github/workflows/`, `.gitlab-ci.yml` | Backend > Operations (+7) |
| **Frontend detected** | React/Vue/Angular/Svelte deps | Frontend (+10) |
| **Mobile detected** | Podfile, build.gradle, pubspec | Apps > Mobile (+6) |
| **Desktop detected** | Electron, Tauri deps | Apps > Desktop (+4) |
| **Container detected** | Dockerfile, docker-compose | Infra > Container (+5) |
| **K8s detected** | k8s/, helm/, kustomization | Infra > Container (+5) |
| **Serverless detected** | serverless.yml, sam.yaml | Infra > Serverless (+4) |
| **Monorepo detected** | nx.json, turbo.json, lerna | Infra > Monorepo (+4) |
| **ML/AI detected** | torch, tensorflow, sklearn | Specialized > ML/AI (+6) |
| **Game detected** | Unity, Unreal, Godot files | Specialized > Game (+4) |
| **i18n detected** | locales/, i18n config | Collab > i18n (+5) |
| **Microservices** | Multiple services detected | Scale & Arch (+12) |
| **Secrets Risk** | .env patterns, hardcoded | Security (+12) |

#### User-Configured Triggers

See [User-Configurable Elements](#user-configurable-elements) (sections 1-13) for complete options and their standards. The "Standards" column in each table shows what gets activated.

### Key Principles

1. **Granular selection** - Each trigger is independently evaluated
2. **No false positives** - CI/CD alone does NOT trigger API or Data standards
3. **Stacking allowed** - Multiple triggers stack additively
4. **No duplicates** - Each standard added exactly once
5. **Project-specific** - Only relevant standards applied

### Standard Count Reference

| Category | Subsections | Max Total |
|----------|-------------|-----------|
| Security & Compliance | - | 12 |
| Scale & Architecture | - | 12 |
| Backend Services | API (6) + Data (5) + Operations (7) | 18 |
| Frontend | Accessibility (4) + Performance (3) + Quality (3) | 10 |
| Apps | Mobile (6) + Desktop (4) + CLI (5) | 15 |
| Library | - | 5 |
| Infrastructure | Container (5) + Serverless (4) + Monorepo (4) | 13 |
| Specialized | ML/AI (6) + Game (4) | 10 |
| Collaboration | Team (4-8) + i18n (5) | 13 |
| Real-time | Basic (2) / Standard (5) / Low-latency (8) | 8 |
| Testing | Basic (3) / Standard (5) / Full (8) + Perf (4) | 12 |
| Observability | Basic (3) / Standard (4) / HA (8) / Full (12) | 12 |

**Note:** "/" means OR (tiered - only one selected), "+" means AND (stacking).

Standard counts from `^- ` lines in `cco-standards-conditional.md`.

**Dynamic calculation:** Count actual bullet points in source file, don't use hardcoded values.

---

## Guidelines Generation

Guidelines are generated based on user-configured values to provide context-aware recommendations.

### Team Size Guidelines

| Condition | Generated Guideline |
|-----------|---------------------|
| Team: Solo | Self-review sufficient, document for future |
| Team: Small (2-5) | Informal review, async communication |
| Team: Medium (6-15) | Formal review, CODEOWNERS required |
| Team: Large (16-50) | ADRs mandatory, cross-team sync |
| Team: Enterprise (51+) | Scaling frameworks, architecture governance |

### Scale Guidelines

| Condition | Generated Guideline |
|-----------|---------------------|
| Scale: Prototype (<100) | Simple solutions, clarity first |
| Scale: Small (100-1K) | Add basic caching, error tracking |
| Scale: Medium (1K-100K) | Horizontal scaling, monitoring |
| Scale: Large (100K-1M) | Performance critical, load testing |
| Scale: Hyperscale (1M+) | Distributed systems, global CDN |

### Data Sensitivity Guidelines

| Condition | Generated Guideline |
|-----------|---------------------|
| Data: Public | Basic validation sufficient |
| Data: Internal | Auth required, access logging |
| Data: Confidential | Encryption in transit/rest |
| Data: PII | Minimize retention, audit logs |
| Data: Regulated | Full compliance, external audit |

### Maturity Guidelines

| Condition | Generated Guideline |
|-----------|---------------------|
| Maturity: Prototype | Move fast, skip docs |
| Maturity: Greenfield | Aggressive refactors OK |
| Maturity: Active | Balanced refactors |
| Maturity: Stable | Conservative, stability first |
| Maturity: Legacy | Wrap don't modify |
| Maturity: Sunset | Document for migration |

### Breaking Changes Guidelines

| Condition | Generated Guideline |
|-----------|---------------------|
| Breaking: Allowed | Clean API over compatibility |
| Breaking: Minimize | Deprecate first, migration path |
| Breaking: Never | Adapters required |

### Priority Guidelines

| Condition | Generated Guideline |
|-----------|---------------------|
| Priority: Speed | MVP mindset, ship fast |
| Priority: Balanced | Standard practices |
| Priority: Quality | Thorough, no shortcuts |
| Priority: Security | Threat modeling first |
| Priority: Cost | Efficiency focus |

### SLA Guidelines

| Condition | Generated Guideline |
|-----------|---------------------|
| SLA: None | Best-effort availability |
| SLA: Standard (99%) | Basic monitoring, alerts |
| SLA: High (99.9%) | Redundancy required |
| SLA: Critical (99.99%) | HA architecture, DR plan |
| SLA: Mission-Critical | Global redundancy, chaos testing |

---

## Rules

1. **All questions at the start** - no mid-process interruptions
2. **Local files only** - AI Performance, statusline, permissions ALL in `./.claude/settings.json`, NEVER touch `~/.claude/`
3. **Dynamic counts** - standard counts calculated from source files
4. **Show affected standards** - when editing, show what standards change
5. **Preserve existing** - never overwrite non-CCO content in files
6. **ALWAYS overwrite files** - All selected configurations (AI Performance, statusline, permissions, context) are ALWAYS written to files from source content, even if files appear identical. Never skip writing because "files are up to date". This ensures any subtle differences from older CCO versions are corrected.
7. **Granular standard selection** - each subsection is independently evaluated, not atomic categories
8. **No duplicate standards** - each standard is added exactly once; deduplicate before writing to CLAUDE.md
9. **Never modify global** - cco-tune has NO permission to read/write/modify any file in `~/.claude/` directory
10. **Backward compatibility** - all CCO markers (`<!-- CCO_*_START -->...<!-- CCO_*_END -->`) are removed before inserting new content; ensures clean upgrades from any previous CCO version
11. **Labels on right** - All labels (`[recommended]`, `[detected]`, `[current]`) appear on the RIGHT side of option names, not in descriptions
12. **String env values** - All `env` values in settings.json must be strings per official Claude Code docs
