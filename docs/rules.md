# CCO Rules

**Single Source of Truth** for all CCO rules organized by category.

## Summary

| Category     | Rules    | Location                           | Loading       |
|--------------|----------|------------------------------------|---------------|
| Core         | 141      | `rules/core.md`                    | Always active |
| AI           | 68       | `rules/ai.md`                      | Always active |
| Adaptive     | 1155     | `rules/*.md` (60 files)            | Per-project   |
| **Total**    | **1364** |                                    |               |

*Note: Tool rules (workflow mechanisms) are embedded directly in command/agent templates.*

**Counting:** `grep -c "^- \*\*" <file>` for all rule files

---

## Rules Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  ALWAYS ACTIVE (Core + AI Rules)                                │
├─────────────────────────────────────────────────────────────────┤
│  Core         - All projects, AI/human agnostic (141 rules)     │
│  AI           - All AI assistants, model agnostic (68 rules)    │
│  Location:    rules/core.md, rules/ai.md                        │
├─────────────────────────────────────────────────────────────────┤
│  ADAPTIVE (Per-Project Rules)                                   │
├─────────────────────────────────────────────────────────────────┤
│  Languages    - 27 language-specific rule files                 │
│  Domains      - 35 domain-specific rule files                   │
│  Location:    rules/*.md (60 files, 1155 rules)                 │
├─────────────────────────────────────────────────────────────────┤
│  DYNAMICALLY GENERATED (Project Context)                        │
├─────────────────────────────────────────────────────────────────┤
│  Selected by: /cco-config based on stack detection              │
│  Written to:  .claude/cco.md (@imports relevant rules)          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Rules

*AI/human agnostic - fundamental principles for all software projects.*

### Design Principles

- **SSOT**: Single source of truth for every piece of data/logic
- **DRY**: Extract common patterns, avoid repetition
- **YAGNI**: Add only requested features + robustness (validation, edge cases, error handling) - robustness is required, features are not
- **KISS**: Simplest solution that works correctly for all valid inputs
- **Separation-of-Concerns**: Distinct responsibilities per module
- **Composition**: Prefer composition over inheritance
- **Idempotent**: Same operation, same result, safe to retry
- **Least-Astonishment**: Behavior matches user expectations
- **Defensive-Default**: Assume bad input, validate anyway. Cost of validation << cost of bug
- **Depend-Abstract**: High-level modules depend on abstractions, not implementations. Enables testing and flexibility
- **Single-Instance**: For shared state (config, connection pools, caches), use single instance per process. Not universal—apply only when state must be globally shared

### Code Quality

- **Fail-Fast**: Immediate visible failure, propagate errors explicitly
- **Used-Only**: Keep only called functions and used imports
- **Type-Safe**: Full type annotations on all public APIs. Prefer stricter types (Literal, enums over strings)
- **Immutable**: Prefer immutable, mutate only when necessary
- **Complexity**: Cyclomatic <10 per function
- **Clean**: Meaningful names, single responsibility
- **Explicit**: Use named constants, clear intent
- **Scope**: Only requested changes, general solutions
- **Robust**: Handle all valid input variations (whitespace, case, empty, None, boundary values)
- **Async-Await**: Use async/await for I/O operations, avoid blocking in async context
- **Graceful-Shutdown**: Handle termination signals, drain connections before exit

### File & Resource

- **Minimal-Touch**: Only files required for task
- **Request-First**: Create files only when explicitly requested
- **Paths**: Forward slash, relative, quote spaces
- **Cleanup**: Temp files, handles, connections
- **Skip**: VCS (.git, .svn), deps (node_modules, vendor, venv), build (dist, out, target), IDE (.idea, .vscode), generated (*.min.*, @generated)

### Efficiency

- **Parallel-Independent**: Run unrelated operations simultaneously
- **Sequential-Dependent**: Chain dependent operations
- **Lazy-Evaluation**: Defer work until needed
- **Cache-Reuse**: Cache results, reuse computations
- **Batch-Operations**: Group similar operations

### Security

- **Secrets**: Env vars or vault only
- **Input-Boundary**: Validate at system entry points
- **Least-Privilege**: Minimum necessary access
- **Deps-Audit**: Review before adding, keep updated
- **Defense-in-Depth**: Multiple layers, verify each control independently
- **OWASP-Top10**: Prevent injection (SQL, XSS, Command), broken auth, sensitive data exposure, security misconfiguration. Input-Boundary + Defense-in-Depth cover most vectors
- **Lockfile-Required**: Dependency lockfile mandatory in repo. Pin versions, no floating ranges for production
- **Safe-Defaults**: Production defaults must be secure: debug off, verbose errors off, restrictive CORS, no wildcard origins
- **No-Secrets-Logged**: Never log secrets, tokens, credentials, PII. Redact/mask sensitive fields in all output
- **Data-Minimization**: Collect and store only necessary data. Each field requires justification
- **Session-Security**: Secure + HttpOnly + SameSite=Lax/Strict cookies, token TTL with refresh strategy, logout invalidates server-side. Use __Host- prefix for sensitive cookies
- **Password-Security**: Never store plaintext. Use bcrypt/argon2/scrypt with appropriate cost factor. Salt per-password, pepper application-wide
- **Error-Disclosure**: Never expose stack traces, internal paths, or system details to users. Generic messages for auth failures (prevent user enumeration)
- **Timeout-Required**: All external calls must have explicit timeout. Connection timeout + read timeout. Prevent resource exhaustion

### Testing

- **Coverage**: 60-90% context-adjusted
- **Isolation**: Independent tests, reproducible results
- **Integrity**: Fix code to pass tests, tests define expected behavior
- **Critical-Paths**: E2E for critical user workflows
- **Edge-Cases-Mandatory**: Always test: empty/None, whitespace-only, boundary values (0, 1, max, max+1), state combinations, invalid type coercion
- **Input-Variations**: Test normalized vs raw input (leading/trailing whitespace, case variations, unicode)
- **State-Matrix**: Test all valid state combinations where multiple states interact

### Error Handling

- **Catch-Context**: Log context, recover or propagate
- **Log-All**: Log all exceptions with context before handling
- **User-Actionable**: Clarity + next steps for users
- **Logs-Technical**: Technical details only in logs
- **Rollback-State**: Consistent state on failure

### Analysis

- **Architecture-First**: Before fixing symptoms, understand system design
- **Dependency-Mapping**: Trace impact through component relationships
- **Root-Cause-Hunt**: Ask "why does this pattern exist?" not just "what's wrong?"
- **Cross-Cutting-Concerns**: Check for issues that span multiple modules
- **Systemic-Patterns**: Identify recurring problems indicating design flaws

### Documentation

- **README**: Description, setup, usage
- **CHANGELOG**: Versions with breaking changes
- **Comments-Why**: Explain why, not what
- **Examples**: Working, common use cases

### Workflow

- **Match-Conventions**: Follow existing patterns
- **Reference-Integrity**: Find ALL refs, update, verify
- **Decompose**: Break complex tasks into steps
- **SemVer**: MAJOR.MINOR.PATCH

### Refactoring Safety

- **Delete-Impact**: Before deleting function/class/file, identify ALL callers and dependents
- **Rename-Cascade**: Rename operation = find refs + update ALL + verify builds
- **Move-Imports**: When moving code between files, update all import statements
- **Signature-Propagate**: Changing function signature requires updating all call sites
- **Type-Cascade**: Type changes must propagate to all consumers

### UX/DX

- **Minimum-Friction**: Fewest steps to goal
- **Maximum-Clarity**: Unambiguous output
- **Predictable**: Consistent behavior
- **Fast-Feedback**: Progress indicators, incremental results
- **Step-Progress**: Multi-step operations show "Step 2/5: Building..."
- **Summary-Final**: End with summary: "Changed 3 files, added 2 tests"
- **Impact-Explain**: Show why: "This reduces bundle size by 15%"
- **Diff-Before-Destruct**: Show diff before delete/overwrite operations
- **Error-Actionable**: Errors include file:line AND suggested fix

---

## AI Rules

*Portable across Claude/Codex/Gemini - AGENTS.md compatible.*

### Rule Enforcement [CRITICAL]

- **Apply-All-Rules**: Every change MUST comply with ALL rules currently in context (global + project-specific)
- **Verify-After-Change**: After EVERY code change, verify compliance before proceeding
- **Fix-Immediately**: Violation detected → stop, fix, re-verify. Never defer ("cleanup later" is not acceptable)
- **No-Partial-Compliance**: Do not proceed with known violations. 100% compliance required, not "mostly compliant"
- **Security-Priority**: Security rules are non-negotiable. Never trade security for convenience or speed
- **Block-On-Violation**: Security violation = STOP. Do not continue until fixed. Warn user explicitly
- **Defense-Assume**: When uncertain about security impact, assume the worst and protect accordingly

### Context Optimization

- **Semantic-Density**: Concise over verbose
- **Structured**: Tables/lists over prose
- **Front-load**: Critical info first
- **Hierarchy**: H2 > H3 > bullets
- **Reference**: Cite by name, don't duplicate

### Execution Order [CRITICAL]

- **Read-First**: Read and comprehend files completely before proposing any edits
- **Investigation-Block**: BLOCK any edit operation until target file has been read in current session. No read = no edit. Violation = stop, read file first, then proceed
- **Plan-Before-Act**: Understand full scope before any action
- **Incremental**: Complete one step fully before starting next
- **Verify**: Confirm changes match stated intent

### Agent Delegation

Specialized agents for complex tasks. **Choose based on complexity, not task type.**

| Complexity | Tool | Example |
|------------|------|---------|
| **Simple** | WebSearch/WebFetch direct | Single URL, quick fact, known source |
| **Complex** | `cco-agent-research` | Multiple sources, synthesis, reliability critical |

#### When to Delegate

| Pattern | Agent | Trigger |
|---------|-------|---------|
| Multi-source research | `cco-agent-research` | 3+ sources needed |
| Dependency/CVE audit | `cco-agent-research` | Security implications |
| Conflicting information | `cco-agent-research` | Need resolution |

#### vs Default Tools

| Aspect | WebSearch/WebFetch | cco-agent-research |
|--------|-------------------|-------------------|
| Source scoring | None | CRAAP+ (T1-T6 tiers) |
| Reliability | No verification | Cross-verification required |
| Contradictions | Not tracked | Explicit resolution |
| Confidence | Implicit | Scored (HIGH/MEDIUM/LOW) |
| Freshness | Not weighted | Currency scoring (+10/-15) |
| Bias detection | None | Vendor/promo penalties |
| Parallel search | Manual | Auto (4 strategies) |
| Saturation | Manual stop | Auto (3× theme repeat) |

**When to use default:** Single quick lookup, known-good URL, simple fact check.
**When to delegate:** Research requiring synthesis, multiple sources, reliability matters.

### Decision Making

- **Challenge**: Question solutions that seem too perfect
- **Ask**: When uncertain, clarify before proceeding
- **Confidence**: State uncertainty level for non-obvious conclusions
- **Read-To-Know**: Read file contents before referencing them
- **Confirm-Intent**: Confirm user intent before making assumptions
- **No-Hallucination**: Never invent APIs, methods, parameters, or file contents. Verify existence before use (alias: Verify-APIs + Read-To-Know)
- **Security-Evidence**: Security claims require code/config evidence. No evidence → state "unverified" and list checks needed

### Reasoning Strategies

#### Step-Back Prompting (Complex Tasks)

Before diving into specifics, ask the broader question first:

| Task Type | Step-Back Question |
|-----------|-------------------|
| Refactoring | "What is the architectural pattern here?" |
| Bug fix | "What is the expected behavior of this system?" |
| Security audit | "What are the trust boundaries in this codebase?" |
| Performance | "What are the critical paths in this flow?" |

#### Chain of Thought (Critical Decisions)

For CRITICAL-HIGH severity decisions, explicitly reason through steps:

```
1. Identify: What exactly is the issue?
2. Impact: Who/what is affected?
3. Evidence: What confirms this assessment?
4. Severity: Based on evidence, what's the appropriate level?
```

#### Self-Consistency (CRITICAL Decisions Only)

For CRITICAL severity findings, validate with multiple reasoning paths:

1. **Path A**: Analyze from attacker perspective
2. **Path B**: Analyze from system design perspective
3. **Consensus**: If both paths agree → confirm CRITICAL. If disagree → downgrade to HIGH

### Quality Control

- **Adapt**: Adjust examples to context, verify before applying
- **Verify-APIs**: Use only documented, existing APIs and features
- **Positive**: State what to do, not what to avoid
- **Motivate**: Explain why behaviors matter

### Code Generation [CRITICAL]

- **Validation-First**: Add input validation for all public APIs. Validate at boundaries, trust internals
- **Bounds-Always**: Set min/max limits on strings (max_length), numbers (ge/le), collections (max_items)
- **Whitespace-Normalize**: Strip/normalize string inputs in validators. Whitespace-only is usually invalid
- **State-Complete**: Handle all valid state combinations, not just happy path
- **Enum-Prefer**: Use enums/Literal types over raw strings for fixed values
- **Optional-Explicit**: Distinguish None (absent) vs empty string/list (present but empty)
- **Coercion-Document**: If auto-coercing types, document behavior. Prefer explicit over magic
- **Error-Rich**: Validation errors should be specific, actionable, field-level
- **Security-By-Default**: New code must include: input validation, output encoding, error handling, timeout configuration
- **No-Hardcoded-Secrets**: Never write secrets, API keys, passwords in code. Use environment variables or config

### Status Updates

- **Announce-Before**: State action before starting
- **Progress-Track**: Starting > In progress > Completed
- **Transitions**: Clear phase signals
- **Visible-State**: User always knows current state

### Multi-Model

- **Agnostic**: No model-specific syntax
- **Graceful**: Account for different capabilities
- **Portable**: Patterns work across models

### Output Standards

- **Error-Format**: `[SEVERITY] {What} in {file:line}`
- **Status-Values**: OK / WARN / FAIL
- **Accounting**: done + fail = total
- **Structured**: JSON/table when needed

#### Output Examples

**Error reporting:**
```
[{severity}] {issue_description} in {file_path}:{line_number}
```

**Status summary:**
```
Status: {status} | Applied: {n} | Failed: {n} | Total: {n}
```

---

## Tool Rules (Reference)

*CCO workflow mechanisms - embedded in command/agent templates. Excluded from AGENTS.md export.*

> **Note:** These rules are not installed as a separate file. They are built into each command and agent template for context efficiency. Listed here for documentation purposes.

### User Input [MANDATORY]

- **AskUserQuestion-Required**: ALL questions/confirmations → AskUserQuestion tool
- **No-Plain-Text-Questions**: Plain text questions = VIOLATION, stop command
- **No-Workarounds**: Cannot skip by rephrasing as statement
- **All-Stages**: Start, middle, end, follow-up → all use tool
- **MultiSelect-When-Valid**: Use `multiSelect: true` when multiple selections valid
- **Semicolon-Separator**: Use `;` to separate options, never comma
- **Self-Check**: Before `?` or choices → must use AskUserQuestion

### Command Flow

- **Context-Check**: Verify context.md exists, suggest /cco-config if missing
- **Read-Context**: Load `.claude/rules/cco/context.md`
- **Execute**: Command-specific logic
- **Report**: Results with accounting

### Safety

- **Pre-op**: Git status before modifications
- **Dirty-Handling**: Prompt Commit / Stash / Continue
- **Rollback**: Clean state enables git checkout
- **Safe-Auto**: Remove imports, parameterize SQL, move secrets, fix lint, add types
- **Risky-Approval**: Auth changes, DB schema, API contract, delete files, rename public

### Fix Workflow

- **Flow**: Analyze > Report > Approve > Apply > Verify
- **Output-Accounting**: `Applied: N | Failed: N | Total: N`

### Impact Preview

- **Direct**: Files to modify
- **Dependents**: Files that import/use
- **Tests**: Coverage of affected code
- **Risk**: LOW / MEDIUM / HIGH
- **Skip-Preview**: LOW risk, <=2 files, full coverage

### Priority

- **CRITICAL**: Security, data exposure
- **HIGH**: High-impact, low-effort
- **MEDIUM**: Balanced impact/effort
- **LOW**: Style, minor optimization

### Question Patterns

- **Max-Questions**: 4 per AskUserQuestion call
- **Max-Options**: 4 per question
- **Overflow**: Use multiple sequential calls
- **Option-Batching**: Split 5+ options into sequential questions (4+4+... pattern)
- **First-Batch-Exit**: Include "None"/"Skip" in first batch for early exit
- **Subsequent-Skip**: Include "Skip" in each subsequent batch
- **Batch-Numbering**: Label as "(1/N)", "(2/N)", etc.
- **Batch-Grouping**: Group related options (by category, region, severity)
- **MultiSelect-Batch**: true for batch approvals
- **All-Option**: First option = "All ({N})" for bulk
- **Priority-Order**: CRITICAL → HIGH → MEDIUM → LOW
- **Item-Format**: `{description} [{file:line}] [{safe|risky}]`

### Labels

- **One-Label**: Each option has exactly ONE label
- **Current**: `[current]` - matches existing config (priority 1)
- **Detected**: `[detected]` - auto-detected (priority 2)
- **Recommended**: `(Recommended)` - max 1/question (priority 3)
- **Precedence**: detected AND current → show `[current]` only

### Ordering

- **Numeric**: Ascending (60 → 70 → 80 → 90)
- **Severity**: Safest → riskiest
- **Scope**: Narrowest → widest

### Output Formatting

- **Table-Borders**: `─│┌┐└┘├┤┬┴┼`
- **Table-Headers**: `═║╔╗╚╝`
- **Numbers-Right**: Right-aligned
- **Text-Left**: Left-aligned
- **Status-Center**: Centered
- **Status-Values**: OK | WARN | FAIL | PASS | SKIP
- **Progress-Bar**: `filled = round(percentage / 100 * 8)` → `████░░░░`
- **No-Emojis**: No emojis in tables
- **No-Extra-Unicode**: No unicode decorations beyond specified

### Dynamic Context

- **Backtick-Syntax**: Use `!` backtick for real-time context
- **Git-Status**: `` `git status --short` ``
- **Branch**: `` `git branch --show-current` ``
- **CCO-Context**: `` `head -30 .claude/rules/cco/context.md` ``
- **Accuracy**: Real-time accuracy over stale assumptions
- **Anti-Hallucination**: Reduces hallucination risk

### Parallel Execution

- **Independent-Parallel**: Launch parallel agents for independent scans
- **Batch-Reads**: Multiple file reads in single call
- **Unrelated-Simultaneous**: Run unrelated checks simultaneously
- **Dependent-Sequential**: Run dependent operations sequentially
- **Agent-Launch**: Launch agents simultaneously in single message
- **Agent-Scope**: Each agent handles distinct scope
- **Agent-Diverse**: Use varied search strategies per agent
- **Agent-Merge**: Merge results after all complete

### Agent Propagation

- **Context-Pass**: Pass context.md summary to all agents
- **Rules-Pass**: Include applicable rules from context
- **Format-Pass**: Specify exact output format expected
- **Todo-Pass**: Tell agents: "Make a todo list first"

### Quick Mode

- **No-Questions**: Do not ask questions
- **Defaults**: Use smart defaults for all options
- **No-Intermediate**: Do not output intermediate text
- **Summary-Only**: Only tool calls, then final summary
- **Single-Message**: Complete ALL steps in a single message

### Conservative Judgment

- **Severity-Keywords**: crash/data loss → CRITICAL, broken → HIGH, error → MEDIUM, style → LOW
- **False-Positive-Prevention**: False positives erode trust faster than missed issues
- **Lower-When-Uncertain**: When uncertain between severities, choose lower
- **Genuine-Issues**: Only flag issues that genuinely block users
- **Evidence-Required**: Require explicit evidence, not inference
- **Style-Never-High**: Style issues → never CRITICAL or HIGH
- **Single-Never-Critical**: Single occurrence → never CRITICAL unless security

### Skip Criteria

- **Line-Ignore**: `// cco-ignore` or `# cco-ignore` - skip line
- **File-Ignore**: `// cco-ignore-file` or `# cco-ignore-file` - skip file
- **Markdown-Ignore**: `<!-- cco-ignore -->` - skip in markdown
- **Test-Fixtures**: Skip `fixtures/`, `testdata/`, `__snapshots__/`
- **Examples**: Skip `examples/`, `samples/`, `demo/`, `benchmarks/`

### Progress Tracking (TodoWrite)

- **Start-With-Todo**: Create todo list with ALL steps at command start
- **Track-In-Progress**: Mark `in_progress` before starting each step
- **Update-Completed**: Mark `completed` immediately after each step
- **Single-Active**: Exactly ONE item `in_progress` at a time
- **Immediate-Update**: Update status immediately, not batched
- **No-Skip-Items**: Never skip items - update status instead
- **ActiveForm-Continuous**: Use present continuous (-ing form)
- **Content-Imperative**: Use imperative form

### Artifact Handling

- **Reference-Large**: Reference large outputs by path/ID, not inline
- **Tokenize-Efficiently**: Use `[artifact:path]` notation for files >500 lines
- **Summarize-First**: Provide digest before full artifact access
- **Chunk-Processing**: Process large data in manageable segments
- **Cache-Artifacts**: Reuse analyzed artifacts within session

### Strategy Evolution

- **Learnings-Location**: `.claude/rules/cco/context.md` → `## Learnings` section
- **Avoid-Section**: Pattern + why it failed + what works instead
- **Prefer-Section**: Pattern + why it works + impact level
- **Systemic-Section**: Issue + root cause + recommendation
- **Session-Start**: Read context.md, note Learnings section
- **Check-Avoid**: Check Avoid patterns before recommending
- **Max-Items**: 5 per category (remove oldest when full)
- **Update-Existing**: Update existing instead of adding duplicate

---

## Adaptive Rules

*Dynamically selected by /cco-config based on project detection.*

### Detection Types

| Type            | Method            | Example                                      |
|-----------------|-------------------|----------------------------------------------|
| **Auto-Detect** | Manifest/code scan | Language, API, Database, Dependencies        |
| **User-Input**  | AskUserQuestion   | Team, Scale, Data, Compliance, Testing, SLA  |
| **Guidelines**  | context.md only   | Maturity, Breaking, Priority                 |

### User-Input Elements

| Element    | Options                                                              | Default  | Affects            |
|------------|----------------------------------------------------------------------|----------|--------------------|
| Team       | Solo; 2-5; 6+                                                        | Solo     | Team rules         |
| Scale      | Prototype; Small (100+); Medium (1K+); Large (10K+)                  | Small    | Scale rules        |
| Data       | Public; PII; Regulated                                               | Public   | Security rules     |
| Compliance | None; SOC2; HIPAA; PCI; GDPR; CCPA; ISO27001; FedRAMP; DORA; HITRUST | None     | Compliance rules   |
| Testing    | Basics (60%); Standard (80%); Full (90%)                             | Standard | Testing rules      |
| SLA        | None; 99%; 99.9%; 99.99%                                             | None     | Observability rules |

#### User-Input Descriptions

**Team:** How many people actively contribute?
- **Solo**: Single developer, no review process needed
- **2-5**: Small team, async PR reviews work well
- **6+**: Large team, needs ADR, CODEOWNERS, formal process

**Scale:** Expected concurrent users or requests/second?
- **Prototype (<100)**: Dev/testing only, no production traffic
- **Small (100+)**: Early production, basic caching helps
- **Medium (1K+)**: Growth stage, connection pooling and async needed
- **Large (10K+)**: High traffic, circuit breakers and API versioning required

**Data:** Most sensitive data your system handles?
- **Public**: Open data, no login required
- **PII**: Personal data (names, emails, addresses) - activates security rules
- **Regulated**: Healthcare (HIPAA), financial (PCI), government - strictest rules

**Compliance:** Required compliance frameworks? (multi-select)
- **SOC2**: B2B SaaS with enterprise customers
- **HIPAA**: US healthcare data (PHI)
- **PCI**: Payment card processing
- **GDPR**: EU user data, privacy rights
- **CCPA**: California consumer privacy
- **ISO27001**: International security standard
- **FedRAMP**: US government cloud
- **DORA**: EU financial services (2025+)
- **HITRUST**: Healthcare + security combined

**Testing:** Test coverage level?
- **Basics (60%)**: Unit tests, basic mocking
- **Standard (80%)**: + Integration tests, fixtures, CI gates
- **Full (90%)**: + E2E, contract testing, mutation testing

**SLA:** Uptime commitment?
- **None**: Best effort, no formal SLA
- **99%**: ~7h downtime/month, basic monitoring
- **99.9%**: ~43min/month, needs redundancy
- **99.99%**: ~4min/month, multi-region, chaos testing

### Guidelines (context.md only)

| Element  | Options                            | Purpose                    |
|----------|------------------------------------|----------------------------|
| Maturity | Prototype; Active; Stable; Legacy  | Refactoring aggressiveness |
| Breaking | Allowed; Minimize; Never           | API versioning approach    |
| Priority | Speed; Balanced; Quality; Security | Development focus          |

**Maturity:** Project development stage? (guideline only)
- **Prototype**: Proof of concept, may be discarded
- **Active**: Ongoing development, regular releases
- **Stable**: Feature-complete, maintenance mode
- **Legacy**: Old codebase, minimal changes

**Breaking:** How to handle breaking changes? (guideline only)
- **Allowed**: OK in any release (v0.x projects)
- **Minimize**: Deprecate first, provide migration path (v1.x+)
- **Never**: Zero breaking changes (enterprise libraries)

**Priority:** Primary development focus? (guideline only)
- **Speed**: Ship fast, iterate quickly
- **Balanced**: Standard practices, reasonable coverage
- **Quality**: Thorough testing, extensive review
- **Security**: Security-first, threat modeling

*Guidelines influence AI behavior but don't generate separate rule files. Stored in context.md.*

### Tier System

**Cumulative tiers:** Higher tiers include all rules from lower tiers.

| Category      | Tiers                              | Behavior                         |
|---------------|------------------------------------|----------------------------------|
| Scale         | Small → Medium → Large             | Large includes Medium + Small    |
| Testing       | Basics → Standard → Full           | Full includes Standard + Basics  |
| Observability | Basics → Standard → HA → Critical  | Each includes lower tiers        |
| Team          | Small → Large                      | Large includes Small             |
| Real-time     | Basic → Low-latency                | Higher includes lower            |

### Categories & Triggers

| Category | Trigger |
|----------|---------|
| Language | Manifest files detected (27 languages: Python, TS, JS, Go, Rust, Java, Kotlin, Swift, C#, Ruby, PHP, Elixir, Gleam, Scala, Zig, Dart, C, C++, Lua, Haskell, F#, OCaml, R, Julia, Perl, Clojure, Erlang) |
| Security | D:PII, D:Regulated, Scale:Large, Compliance:* |
| Compliance | User-selected (SOC2, HIPAA, PCI, GDPR, CCPA, ISO27001, FedRAMP, DORA, HITRUST) |
| Scale | 100+ users (cumulative tiers) |
| Team | Team 2+ (cumulative tiers) |
| Backend > API | REST/GraphQL/gRPC detected |
| Backend > Data | DB != None |
| Backend > Operations | CI/CD AND NOT CLI/Library |
| Backend > CI Only | CI/CD AND (CLI OR Library) |
| Frontend | React/Vue/Angular/Svelte detected |
| Apps > CLI | Type: CLI |
| Apps > Library | Type: Library |
| Apps > Mobile | iOS/Android/RN/Flutter |
| Apps > Desktop | Electron/Tauri |
| Infra > Container | Dockerfile detected (not in examples/) |
| Infra > Kubernetes | K8s/Helm detected |
| Infra > Serverless | Lambda/Functions/Vercel/Netlify |
| Infra > Monorepo | nx/turbo/lerna/pnpm-workspace |
| ML/AI | torch/tensorflow/sklearn/transformers/langchain |
| Game | Unity/Unreal/Godot |
| i18n | locales/i18n/messages/ detected |
| Real-time | WebSocket/SSE detected (cumulative tiers) |
| Testing | User-selected (cumulative tiers) |
| Observability | SLA-based (cumulative tiers) |
| DEP:* | 57 dependency categories (GPU, Audio, Video, HTTP, ORM, Auth, Cache, AI Agents, CDC, etc.) |
| Infra:* | 11 infrastructure categories (API Gateway, Service Mesh, Build Cache, Container, K8s, Serverless, Edge, WASM, etc.) |

### Full Adaptive Rules List

#### Language Rules

**Python (L:Python)**
*Trigger: pyproject.toml | setup.py | requirements.txt | *.py*

- **Python-Type-Hints**: Type annotations for public APIs (functions, methods, classes)
- **Docstrings**: Google-style docstrings for public functions/classes
- **Import-Order**: stdlib > third-party > local (isort compatible)
- **Exception-Context**: Use `raise X from Y` for exception chaining

**TypeScript (L:TypeScript)**
*Trigger: tsconfig.json | *.ts/*.tsx*

- **Strict-Mode**: Enable strict in tsconfig.json
- **Explicit-Return**: Return types on public functions
- **No-Any**: Avoid any, use unknown for truly unknown types
- **Null-Safety**: Strict null checks enabled

**JavaScript (L:JavaScript)**
*Trigger: package.json (no TS) | *.js/*.jsx*

- **JSDoc-Types**: Type hints via JSDoc for public APIs
- **ES-Modules**: ESM over CommonJS (import/export)
- **Const-Default**: const > let > var preference

**Go (L:Go)**
*Trigger: go.mod | *.go*

- **Error-Wrap**: Wrap errors with context (fmt.Errorf %w)
- **Interface-Small**: Small, focused interfaces (1-3 methods)
- **Goroutine-Safe**: Channel or sync primitives for concurrency
- **Defer-Cleanup**: defer for cleanup operations

**Rust (L:Rust)**
*Trigger: Cargo.toml | *.rs*

- **Result-Propagate**: Use ? operator for error propagation
- **Ownership-Clear**: Clear ownership patterns, minimize clones
- **Clippy-Clean**: No clippy warnings in CI
- **Unsafe-Minimize**: Minimize unsafe blocks, document when necessary

#### Security Rules
*Trigger: D:PII | D:Regulated | Scale:Large | Compliance:**

- **Input-Validation**: Validate at system entry points (Pydantic/Zod/JSON Schema)
- **SQL-Safe**: Parameterized queries only, no string concatenation
- **XSS-Prevent**: Sanitize output + CSP headers
- **Auth-Verify**: Verify authentication on every request
- **Rate-Limit**: Per-user/IP limits on public endpoints
- **Encrypt-Rest**: AES-256 for PII/sensitive data at rest
- **Audit-Log**: Immutable logging for security-critical actions
- **CORS-Strict**: Explicit origins, no wildcard in production
- **License-Track**: Review GPL/AGPL deps before adding

#### Compliance Rules
*Trigger: User-selected compliance framework(s)*

**Base Compliance**

- **Data-Classification**: Classify data by sensitivity level
- **Access-Control**: Role-based access with least privilege
- **Incident-Response**: Documented incident response plan

**SOC2**

- **SOC2-Audit-Trail**: Complete audit trail for all data access
- **SOC2-Change-Mgmt**: Documented change management process
- **SOC2-Access-Review**: Quarterly access reviews

**HIPAA**

- **HIPAA-PHI-Encrypt**: Encrypt PHI at rest and in transit
- **HIPAA-BAA**: Business Associate Agreements for vendors
- **HIPAA-Access-Log**: Log all PHI access with user, time, purpose
- **HIPAA-Minimum**: Minimum necessary access to PHI

**PCI-DSS**

- **PCI-Card-Mask**: Mask PAN (show only last 4 digits)
- **PCI-No-Storage**: Store only masked payment data, exclude CVV/CVC
- **PCI-Network-Seg**: Network segmentation for cardholder data
- **PCI-Key-Mgmt**: Cryptographic key management procedures

**GDPR**

- **GDPR-Consent**: Explicit consent with purpose specification
- **GDPR-Right-Access**: Implement data subject access requests
- **GDPR-Right-Delete**: Implement right to erasure
- **GDPR-Data-Portability**: Export user data in portable format
- **GDPR-Breach-Notify**: 72-hour breach notification procedure

**CCPA**

- **CCPA-Opt-Out**: "Do Not Sell" opt-out mechanism
- **CCPA-Disclosure**: Disclose categories of data collected
- **CCPA-Delete**: Honor deletion requests within 45 days

**ISO27001**

- **ISO-Risk-Assess**: Regular risk assessments
- **ISO-Asset-Inventory**: Maintain information asset inventory
- **ISO-Policy-Docs**: Documented security policies

**FedRAMP**

- **FedRAMP-Boundary**: Documented system boundary
- **FedRAMP-Continuous**: Continuous monitoring implementation
- **FedRAMP-FIPS**: FIPS 140-2 validated cryptography

**DORA**

- **DORA-ICT-Risk**: ICT risk management framework
- **DORA-Incident**: Major ICT incident reporting
- **DORA-Resilience**: Digital operational resilience testing

**HITRUST**

- **HITRUST-CSF**: Align with HITRUST CSF controls
- **HITRUST-Inherit**: Leverage inherited controls from providers

#### Scale Rules
*Trigger: User-selected scale level (cumulative tiers)*

**Small (Scale:100+)**

- **Caching**: TTL + invalidation strategy for data fetching
- **Lazy-Load**: Defer loading of non-critical resources

**Medium (Scale:1K+)** — *includes Small rules*

- **Conn-Pool**: Connection pooling with appropriate sizing
- **Async-IO**: Non-blocking I/O operations

**Large (Scale:10K+)** — *includes Medium + Small rules*

- **Circuit-Breaker**: Fail-fast pattern for external services
- **Idempotency**: Safe retries for write operations
- **API-Version**: Version in URL or header for public APIs
- **Compression**: gzip/brotli for large responses

#### Team Rules
*Trigger: User-selected team size (cumulative tiers)*

**Small (Team:2-5)**

- **PR-Review**: Async code review on all changes
- **README-Contributing**: Clear contribution guidelines

**Large (Team:6+)** — *includes Small rules*

- **ADR**: Architecture Decision Records for significant decisions
- **CODEOWNERS**: Clear ownership via CODEOWNERS file
- **PR-Templates**: Standardized PR descriptions
- **Branch-Protection**: Require reviews before merge

#### Testing Rules
*Trigger: User-selected testing level (cumulative tiers)*

**Basics (Testing:60%)**

- **Unit-Isolated**: Fast, deterministic unit tests
- **Mocking**: Isolate tests from external dependencies
- **Coverage-60**: Minimum 60% line coverage

**Standard (Testing:80%)** — *includes Basics rules*

- **Integration**: Test component interactions
- **Fixtures**: Reusable, maintainable test data
- **Coverage-80**: Minimum 80% line coverage
- **CI-on-PR**: Tests run on every PR

**Full (Testing:90%)** — *includes Standard + Basics rules*

- **E2E**: End-to-end tests for critical user flows
- **Contract**: Consumer-driven contract testing
- **Mutation**: Mutation testing for test effectiveness
- **Coverage-90**: Minimum 90% line coverage

#### Observability Rules
*Trigger: SLA-based user selection (cumulative tiers)*

**Basics (SLA:Any)**

- **Error-Tracking**: Sentry or similar error tracking
- **Critical-Alerts**: Immediate notification for critical errors

**Standard (SLA:99%+)** — *includes Basics rules*

- **Correlation-ID**: Request tracing across services
- **RED-Metrics**: Rate, Error, Duration dashboards
- **Distributed-Trace**: OpenTelemetry/Jaeger for multi-service

**HA (SLA:99.9%+)** — *includes Standard + Basics rules*

- **Redundancy**: No single point of failure
- **Auto-Failover**: Automatic recovery mechanisms
- **Runbooks**: Documented incident response

**Critical (SLA:99.99%+)** — *includes HA + Standard + Basics rules*

- **Multi-Region**: Geographic redundancy
- **Chaos-Engineering**: Fault injection testing
- **DR-Tested**: Disaster recovery procedures tested

#### Backend Rules

**API (REST/GraphQL/gRPC)**
*Trigger: routes/ | @Get/@Post decorators | express.Router | *.proto | schema.graphql*

- **REST-Methods**: Proper HTTP verbs and status codes
- **Pagination**: Cursor-based pagination for lists
- **OpenAPI-Spec**: Synced spec with examples
- **Error-Format**: Consistent format, no stack traces in prod
- **GQL-Limits**: Query depth and complexity limits (GraphQL)
- **GQL-Persisted**: Persisted queries in production (GraphQL)
- **Proto-Version**: Backward compatible proto changes (gRPC)

**Data (DB:*)**
*Trigger: ORM deps | migrations/ | prisma/schema.prisma*

- **Backup-Strategy**: Automated backups with tested restore
- **Schema-Versioned**: Migration files with rollback plan
- **Connection-Secure**: SSL/TLS, credentials in env vars
- **Query-Timeout**: Prevent runaway queries

**Operations (CI/CD)**
*Trigger: CI/CD config detected AND NOT CLI/Library*

- **Config-as-Code**: Versioned, environment-aware config
- **Health-Endpoints**: /health + /ready endpoints
- **Graceful-Shutdown**: Drain connections on SIGTERM
- **Observability**: Metrics + logs + traces
- **CI-Gates**: lint + test + coverage gates
- **Zero-Downtime**: Blue-green or canary deployments
- **Feature-Flags**: Decouple deploy from release

**CI-Only Operations (CLI/Library)**
*Trigger: CI/CD config detected AND (CLI OR Library)*

- **Config-as-Code**: Versioned configuration
- **CI-Gates**: lint + test + coverage gates

#### Apps Rules

**CLI (T:CLI)**
*Trigger: __main__.py | bin/ | cli/ | "bin" in package.json*

- **Help-Examples**: --help with usage examples
- **Exit-Codes**: 0=success, N=specific error codes
- **Signal-Handle**: Graceful SIGINT/SIGTERM handling
- **Output-Modes**: Human-readable + --json option
- **Config-Precedence**: env > file > args > defaults

**Library (T:Library)**
*Trigger: exports in package.json | __init__.py with __all__*

- **Minimal-Deps**: Minimize transitive dependencies
- **Tree-Shakeable**: ESM with no side effects (JS/TS)
- **Types-Included**: TypeScript types or JSDoc
- **Deprecation-Path**: Warn before removing APIs

**Mobile (iOS/Android/RN/Flutter)**
*Trigger: Podfile | build.gradle (Android) | pubspec.yaml*

- **Offline-First**: Local-first with sync capability
- **Battery-Optimize**: Minimize background work and wake locks
- **Deep-Links**: Universal links / app links
- **Platform-Guidelines**: iOS HIG / Material Design compliance

**Desktop (Electron/Tauri)**
*Trigger: electron/tauri in deps*

- **Auto-Update**: Silent updates with manual option
- **Native-Integration**: System tray, notifications
- **Memory-Cleanup**: Prevent memory leaks in long-running apps

#### Infrastructure Rules

**Container (Dockerfile)**
*Trigger: Dockerfile (not in examples/test/)*

- **Multi-Stage**: Separate build and runtime stages
- **Non-Root**: Run as non-root user
- **CVE-Scan**: Automated scanning in CI
- **Resource-Limits**: CPU/memory bounds
- **Distroless**: Minimal attack surface for production

**Kubernetes (K8s/Helm)**
*Trigger: k8s/ | helm/ | kustomization.yaml*

- **Security-Context**: Non-root, read-only filesystem
- **Network-Policy**: Explicit allow rules
- **Probes**: liveness + readiness probes
- **Resource-Quotas**: Namespace resource limits

**Serverless (Lambda/Functions/Vercel/Netlify)**
*Trigger: serverless.yml | sam.yaml | vercel.json | netlify.toml*

- **Minimize-Bundle**: Reduce cold start time
- **Graceful-Timeout**: Clean shutdown before timeout
- **Stateless**: No local state between invocations
- **Right-Size**: Memory optimization

**Monorepo (nx/turbo/lerna/pnpm)**
*Trigger: nx.json | turbo.json | lerna.json | pnpm-workspace.yaml*

- **Package-Boundaries**: Clear ownership per package
- **Selective-Test**: Test only affected packages
- **Shared-Deps**: Hoisted and versioned dependencies
- **Build-Cache**: Remote build cache

#### Frontend Rules
*Trigger: react/vue/angular/svelte in deps*

- **A11y-WCAG**: WCAG 2.2 AA, keyboard navigation
- **Perf-Core-Vitals**: LCP<2.5s, INP<200ms, CLS<0.1
- **State-Predictable**: Single source of truth for state
- **Code-Split**: Lazy load routes and heavy components

#### Specialized Rules

**ML/AI**
*Trigger: torch/tensorflow/sklearn/transformers/langchain in deps*

- **Reproducibility**: Seed everything, pin versions
- **Experiment-Track**: MLflow/W&B for experiments
- **Model-Registry**: Versioned model artifacts
- **Bias-Detection**: Fairness metrics for user-facing AI

**Game (Unity/Unreal/Godot)**
*Trigger: Unity (.csproj) | Unreal (*.uproject) | Godot (project.godot)*

- **Frame-Budget**: 16ms (60fps) or 8ms (120fps) target
- **Asset-LOD**: Level of detail + streaming
- **Save-Versioned**: Migration support for old saves
- **Determinism**: Fixed timestep for multiplayer/replay

#### i18n Rules
*Trigger: locales/ | i18n/ | messages/ | translations/*

- **Strings-External**: No hardcoded user-facing text
- **UTF8-Encoding**: Consistent UTF-8 encoding
- **RTL-Support**: Bidirectional layout for RTL languages
- **Locale-Format**: Culture-aware date/time/number formatting

#### Real-time Rules
*Trigger: websocket/socket.io/sse deps (cumulative tiers)*

**Basic (RT:Basic)**

- **Reconnect-Logic**: Automatic reconnection with backoff
- **Heartbeat**: Connection health monitoring
- **Stale-Data**: Handle disconnection gracefully

**Low-Latency (RT:Low-latency)** — *includes Basic rules*

- **Binary-Protocol**: Protobuf/msgpack for performance
- **Edge-Compute**: Edge deployment for global users

#### Dependency-Based Rules (DEP:*)

**DEP:GPU**
*Trigger: cuda-python, cupy, torch+cuda, tensorflow-gpu, numba, pycuda, triton, jax*

- **Device-Selection**: Explicit CUDA_VISIBLE_DEVICES
- **Memory-Management**: Clear cache, use context managers
- **Batch-Sizing**: Dynamic batch based on VRAM
- **Mixed-Precision**: FP16/BF16 where applicable
- **Fallback-CPU**: Graceful CPU fallback
- **Stream-Async**: CUDA streams for parallelism

**DEP:Audio**
*Trigger: faster-whisper, whisper, pydub, librosa, soundfile, pyaudio, speechrecognition, pedalboard*

- **Chunk-Processing**: Stream in chunks, don't load all
- **Sample-Rate**: Normalize sample rates
- **Format-Agnostic**: Support wav, mp3, m4a, etc.
- **Memory-Stream**: Use file handles, not full load
- **Silence-Detection**: VAD before heavy processing
- **Progress-Callback**: Report progress for long operations

**DEP:Video**
*Trigger: ffmpeg-python, moviepy, opencv-video, decord, av, imageio-ffmpeg*

- **Frame-Iterator**: Yield frames, don't load all
- **Codec-Fallback**: Multiple codec support
- **Resolution-Aware**: Scale before heavy processing
- **Temp-Cleanup**: Auto-cleanup intermediate files
- **Seek-Efficient**: Keyframe seeking for random access
- **Hardware-Accel**: NVENC/VAAPI when available

**DEP:HeavyModel**
*Trigger: transformers, sentence-transformers, langchain, llama-cpp-python, vllm, ollama, openai, anthropic*

- **Lazy-Model-Load**: Load on first use, not import
- **Model-Singleton**: Single instance, reuse
- **Quantization-Aware**: Support INT8/INT4 variants
- **Batch-Inference**: Batch for throughput
- **Timeout-Guard**: Max time limits on inference
- **Model-Memory-Cleanup**: Explicit GC after heavy ops
- **Download-Cache**: Cache models locally

**DEP:Image**
*Trigger: opencv-python, pillow, scikit-image, imageio, albumentations, kornia*

- **Lazy-Decode**: Decode on access
- **Size-Validate**: Max dimensions check
- **Format-Preserve**: Maintain original format/quality
- **EXIF-Handle**: Rotation, metadata handling
- **Memory-Map**: mmap for huge files

**DEP:DataHeavy**
*Trigger: pandas, polars, dask, pyspark, ray, vaex, modin, arrow*

- **Chunk-Read**: chunksize parameter for large files
- **Lazy-Eval**: Defer until needed (polars/dask)
- **Type-Optimize**: Downcast dtypes
- **Index-Usage**: Set appropriate indexes
- **Parallel-Process**: Use available cores
- **Spill-Disk**: Allow disk spillover

**DEP:GamePython**
*Trigger: pygame, arcade, ursina, panda3d, pyglet, raylib*

- **Game-Loop**: Fixed timestep, variable render
- **Asset-Preload**: Load screens, progress bars
- **Input-Mapping**: Configurable keybindings
- **State-Machine**: Clean state transitions
- **Delta-Time**: Frame-independent movement

**DEP:GameJS**
*Trigger: phaser, pixijs, three, babylon, playcanvas, matter-js*

- **Sprite-Atlas**: Texture packing
- **Object-Pool**: Reuse frequently created objects
- **RAF-Loop**: requestAnimationFrame
- **WebGL-Fallback**: Canvas 2D fallback
- **Audio-Context**: Single AudioContext

**DEP:GameEngine**
*Trigger: Unity (.csproj), Unreal (*.uproject), Godot (project.godot)*

- **Scene-Organization**: Clear hierarchy, naming convention
- **Prefab-Reuse**: Prefabs/scenes over copies
- **Build-Profiles**: Platform-specific settings
- **Asset-LFS**: Git LFS for binary assets
- **Input-System**: Input actions, rebindable keys
- **Platform-Optimize**: Quality presets per platform

**DEP:HTTP**
*Trigger: requests, httpx, aiohttp, urllib3, got, axios, fetch*

- **Timeout-Always**: Explicit timeouts
- **Retry-Transient**: Exponential backoff
- **Session-Reuse**: Connection pooling
- **Error-Handle**: Status code handling
- **Response-Validate**: Schema validation

**DEP:ORM**
*Trigger: sqlalchemy, django.db, prisma, typeorm, sequelize, drizzle, peewee*

- **N+1-Prevent**: Eager load or batch queries
- **Query-Optimize**: EXPLAIN analysis
- **Loading-Strategy**: Explicit eager/lazy per use case
- **Transaction-Boundary**: Clear scope, rollback on error
- **Index-Design**: Indexes for WHERE/JOIN columns
- **Bulk-Operations**: Use bulk insert/update APIs

**DEP:Auth**
*Trigger: passport, auth0, clerk, nextauth, supabase-auth, firebase-auth, oauth2, jwt*

- **Token-Secure**: HttpOnly, Secure flags
- **Refresh-Flow**: Refresh token rotation
- **RBAC-Clear**: Role-based permissions
- **Session-Invalidate**: Clear all sessions option
- **MFA-Support**: Optional 2FA for sensitive ops

**DEP:Payment**
*Trigger: stripe, paypal, braintree, adyen, square, paddle, razorpay*

- **Webhook-Verify**: Signature validation
- **Idempotency-Key**: Prevent duplicate charges
- **Amount-Server**: Server-side price calculation
- **Payment-Error-Handle**: User-friendly payment errors
- **Audit-Trail**: Complete payment logs

**DEP:Email**
*Trigger: sendgrid, resend, postmark, mailgun, ses, nodemailer, smtp*

- **Template-System**: Reusable templates
- **Queue-Async**: Background sending
- **Bounce-Handle**: Process bounces/complaints
- **Rate-Aware**: Respect provider limits
- **Unsubscribe**: One-click unsubscribe

**DEP:SMS**
*Trigger: twilio, nexmo, vonage, messagebird, plivo, sns*

- **Delivery-Status**: Track delivery callbacks
- **Rate-Throttle**: Respect carrier limits
- **Opt-Out**: Honor STOP requests
- **Fallback-Provider**: Secondary provider
- **Message-Template**: Pre-approved templates

**DEP:Notification**
*Trigger: firebase-messaging, onesignal, pusher, ably, expo-notifications, apns*

- **Channel-Preference**: User-configurable channels
- **Batch-Send**: Batch API calls
- **Silent-Push**: Background updates
- **Token-Refresh**: Handle token rotation
- **Fallback-Channel**: Email if push fails

**DEP:Search**
*Trigger: elasticsearch, opensearch, meilisearch, algolia, typesense, solr*

- **Index-Strategy**: Separate vs combined indexes
- **Sync-Mechanism**: Real-time vs batch sync
- **Relevance-Tune**: Custom ranking
- **Typo-Tolerance**: Fuzzy matching
- **Facet-Design**: Efficient faceting

**DEP:Queue**
*Trigger: celery, rq, bull, rabbitmq, sqs, kafka, redis-queue*

- **Idempotent-Tasks**: Same input = same result
- **Result-Backend**: Configure result storage
- **Timeout-Task**: Per-task time limits
- **Dead-Letter**: DLQ for inspection
- **Priority-Queues**: Separate by priority

**DEP:Cache**
*Trigger: redis, memcached, cachetools, diskcache, node-cache, ioredis*

- **TTL-Strategy**: Explicit expiration
- **Key-Namespace**: Prefixed keys
- **Serialization**: Consistent serializer
- **Cache-Aside**: Load on miss pattern
- **Invalidation**: Clear related keys

**DEP:Logging**
*Trigger: structlog, loguru, pino, winston, bunyan, log4j, serilog*

- **Structured-Format**: JSON logging in production
- **Level-Config**: Configurable log level
- **Context-Inject**: Request ID, user ID
- **Sensitive-Redact**: Mask PII
- **Rotation-Strategy**: Size/time rotation

**DEP:ObjectStore**
*Trigger: boto3, s3, gcs, azure-storage, minio, cloudinary, r2*

- **Presigned-URLs**: Time-limited URLs
- **Content-Type**: Validate MIME type
- **Size-Limit**: Max file size
- **Path-Structure**: Organized paths
- **Lifecycle-Rules**: Auto-expiry for temp files

**DEP:PDF**
*Trigger: reportlab, weasyprint, puppeteer-pdf, pdfkit, fpdf, jspdf, pdf-lib*

- **Template-Based**: HTML/template generation
- **Async-Generate**: Background processing
- **Stream-Output**: Stream don't buffer
- **Font-Embed**: Embed for consistency
- **Accessibility**: Tagged PDF when possible

**DEP:Excel**
*Trigger: openpyxl, xlsxwriter, pandas.excel, exceljs, sheetjs, closedxml*

- **Stream-Write**: Write in chunks
- **Formula-Safe**: Escape formula injection
- **Style-Template**: Reusable styles
- **Memory-Optimize**: Write-only mode
- **Sheet-Naming**: Valid sheet names

**DEP:Scraping**
*Trigger: beautifulsoup, scrapy, playwright, puppeteer, selenium, cheerio, crawlee*

- **Politeness-Delay**: Respectful delays
- **Robots-Respect**: Honor robots.txt
- **User-Agent-Honest**: Identify your bot
- **Selector-Resilient**: Handle structure changes
- **Headless-Default**: Headless unless debugging
- **Anti-Block**: Rotate IPs/proxies if needed

**DEP:Blockchain**
*Trigger: web3, ethers, solana-web3, wagmi, viem, hardhat, foundry*

- **Gas-Estimate**: Pre-estimate gas
- **Nonce-Manage**: Track nonce locally
- **Event-Listen**: Indexed event handling
- **Testnet-First**: Test before mainnet
- **Key-Security**: Store keys in vault or env vars only

**DEP:ARVR**
*Trigger: aframe, three-xr, babylonxr, unity-xr, unreal-vr, webxr*

- **XR-Frame-Budget**: 90fps minimum
- **Comfort-Settings**: Teleport/snap turn options
- **Fallback-Mode**: Non-XR fallback
- **Input-Abstract**: Abstract input layer
- **Performance-Tier**: Quality presets per device

**DEP:IoT**
*Trigger: mqtt, paho-mqtt, aws-iot, azure-iot, particle, micropython*

- **IoT-Reconnect**: Auto-reconnect
- **Power-Aware**: Sleep modes for battery
- **OTA-Update**: Remote updates
- **Data-Buffer**: Local buffer for unreliable network
- **Watchdog**: Hardware watchdog

**DEP:Crypto**
*Trigger: cryptography, pycryptodome, bcrypt, argon2, nacl, crypto-js, jose*

- **Algorithm-Modern**: AES-256-GCM, ChaCha20
- **Key-Rotation**: Scheduled rotation
- **IV-Unique**: Generate unique IV/nonce for each operation
- **Timing-Safe**: Constant-time compare
- **Key-Derivation**: Argon2/scrypt, not MD5/SHA1

---

## Export Behavior

### Format Comparison

| Format        | Target                                          | Core | AI  | Tool | Adaptive        |
|---------------|-------------------------------------------------|------|-----|------|-----------------|
| **AGENTS.md** | Universal (Codex, Cursor, Copilot, Cline, etc.) | Yes  | Yes | No   | Yes (triggered) |
| **CLAUDE.md** | Claude Code only                                | Yes  | Yes | Yes  | Yes (triggered) |

### Why AGENTS.md Excludes Tool Rules

Tool rules depend on Claude Code specific features:
- `AskUserQuestion`, `TodoWrite`, `Task` tool references
- `.claude/` directory structure
- CCO command integration (`/cco-*`)

### Content Filtering (AGENTS.md)

AGENTS.md export filters Claude-specific content for cross-tool compatibility:

| Category     | Filtered                                     | Reason                       |
|--------------|----------------------------------------------|------------------------------|
| Tool names   | `Read`, `Write`, `Edit`, `Bash`, `Task`, etc. | Claude Code specific         |
| Paths        | `~/.claude/`, `.claude/`                     | Claude directory structure   |
| Product refs | "Claude Code", "Claude"                      | Vendor-specific              |
| CCO refs     | `cco-*`, `/cco-*`                            | CCO-specific features        |

Model-agnostic principles (DRY, Fail-Fast, Read-First) are preserved.

---

*Back to [README](../README.md)*
