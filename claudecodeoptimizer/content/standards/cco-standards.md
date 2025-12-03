<!-- CCO_STANDARDS_START -->
# Universal Standards
*Applies to ALL software projects regardless of language, framework, or domain*

## Quality

### Code
- Fail-Fast: immediate visible failure, no silent fallbacks
- DRY: single source of truth, zero duplicates
- No Orphans: every function called, every import used
- Type Safety: annotations + strict static analysis
- Complexity: cyclomatic <10 per function (context may override)
- Tech Debt: ratio <5%
- Maintainability: index >65
- No Overengineering: only requested changes, minimum complexity
- Minimal Touch: only files required for task
- General Solutions: correct algorithms for all inputs
- Clean Code: meaningful names, single responsibility
- Immutability: prefer immutable, mutate only for performance
- Profile First: measure before optimize
- Version: single source, SemVer (MAJOR.MINOR.PATCH)
- Paths: forward slash (/), relative, quote spaces
- No Unsolicited Files: never create unless requested
- Cleanup: remove temporary files created during iteration
- Timeouts: explicit for all external calls
- Retry: exponential backoff + jitter for transient failures
- Exclusions: skip .git, node_modules, __pycache__, venv, dist, build, *.min.js

### Testing
- Coverage: 80% min (context may adjust: solo 60%, enterprise 90%)
- Pyramid: 70% unit (<1ms), 20% integration (~100ms), 10% E2E (seconds)
- Integration: e2e for critical workflows
- CI Gates: lint + test + coverage + security before merge
- Isolation: no dependencies between tests
- TDD: tests first, code satisfies
- Test Integrity: tests define behavior; never edit tests to make code pass

### Security
- Secrets: never hardcode, use env vars or vault
- Dependencies: scan in CI, keep updated
- Input Boundaries: validate at system entry points
- Least Privilege: minimum necessary access/permissions
- Defense in Depth: multiple layers, don't trust single control

## Docs
- README: description, setup, usage, contributing
- CHANGELOG: version history, Keep a Changelog format
- API Docs: complete, accurate, auto-generated
- ADR: decisions + context + consequences
- Comments: why not what

## AI Content
Optimize content for AI consumption (any AI model):
- Semantic Density: max meaning per token; concise over verbose
- Structured Format: tables/lists over prose; JSON for data exchange
- Front-load Critical: important info first; Purpose → Details → Edge cases
- Scannable Hierarchy: clear H2 → H3 → bullets
- No Filler: remove verbose patterns, implicit info, redundancy
- Reference Over Repeat: cite by name instead of duplicating
- Positive Framing: tell what to do, not what to avoid
- Contextual Motivation: explain WHY behaviors matter

## Workflow
- Read First: read files before proposing edits
- Review Conventions: match existing patterns
- Reference Integrity: find ALL refs → update in order → verify
- Plan-Act-Review: iterate until complete
- Work Incrementally: complete one step fully before next
- Decompose: break complex tasks into smaller steps
- No Vibe Coding: avoid rare langs/new frameworks without foundation
- Challenge: "are you sure?" for perfect-looking solutions
- No Example Fixation: use placeholders

## Error Handling
- Fail Gracefully: catch, log context, recover or propagate
- No Silent Failures: never swallow exceptions without logging
- User-Friendly Messages: technical details in logs, clarity for users
- Rollback on Failure: leave system in consistent state

## Logging
- Structured Logs: JSON format, machine-parseable
- Log Levels: ERROR/WARN/INFO/DEBUG used correctly
- Context Rich: include request ID, user, operation
- No Sensitive Data: never log passwords, tokens, PII

## Configuration
- Externalize Config: no hardcoded env-specific values
- Env-Aware: dev/staging/prod configurations
- Validate Early: fail fast on invalid config at startup
- Defaults: sensible defaults, override via env vars

## UX/DX
All software should prioritize:
- Minimum friction: fewest steps to goal
- Maximum clarity: unambiguous output, clear next actions
- Fast feedback: progress indicators, incremental results
- Error recovery: actionable messages with fix suggestions
- Predictability: consistent behavior across invocations
- Transparency: show what will happen before doing it

---

# Claude-Specific Standards
*Specific to Claude's tools, settings, and capabilities*

## CCO Workflow

### Pre-Operation Safety
1. Check `git status` for uncommitted changes
2. If dirty: AskUserQuestion → Commit / Stash / Continue
3. Clean state enables safe rollback
4. Use git for state persistence across sessions

### Context Read
1. Read `CCO_CONTEXT_START` from `./CLAUDE.md`
2. If missing → suggest `/cco-tune`
3. Apply: Guidelines, Thresholds, AI Performance, Applicable checks

### Safety Classification
| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |
| Fix linting issues | Delete files |
| Add type annotations | Rename public APIs |

## Claude Tools
- Parallel Tools: batch independent calls; sequential when outputs inform inputs
- Subagent Delegation: use Task tool when separate context benefits
- Error Format: `[SEVERITY] {What} in {file:line} -> {Fix}`
- Moderate Triggers: "Use when..." not "CRITICAL: You MUST..."

## Resource Scaling
Scale thinking with task complexity:

| Complexity | Thinking | Use Case |
|------------|----------|----------|
| Simple | Off | File lookups, straightforward edits |
| Standard | 8K-16K | Single-file changes, moderate refactors |
| Complex | 16K-32K | Multi-file refactors, debugging, architecture |
| Deep | 32K+ | Algorithm design, complex math, multi-step analysis |

Increase when: errors persist 2+ attempts, task spans many files

## Session Management
- Track state: JSON for data, plain text for progress
- Before /compact: specify what to preserve/discard
- After fresh start: review filesystem state
- MCP Output: default 25K; increase when `/doctor` warns

## Output Formatting
ASCII box-drawing tables in code blocks:
- Characters: `─│┌┐└┘├┤┬┴┼` borders, `═║╔╗╚╝` headers
- Column width: max cell width + 2 padding; scan all values first
- Alignment: numbers right, text left, 1-space cell padding
- Status: `OK`, `WARN`, `FAIL`, `PASS`, `SKIP` (text only, no emoji)
- Progress: `████████░░░░░░░░░░░░` (20 chars proportional)
- ASCII-only: no emojis in tables (cause width misalignment)

## Priority & Approval

### Priority Levels
| Level | Criteria | Examples |
|-------|----------|----------|
| CRITICAL | Security, data exposure | SQL injection, leaked secrets |
| HIGH | High impact, low effort | Dead code, missing validation |
| MEDIUM | Balanced impact/effort | Complexity, duplication |
| LOW | Low impact or high effort | Style, minor optimization |

### Approval Flow
Single AskUserQuestion with severity tabs:
- multiSelect: true; First option: "All ({N})"
- Format: `{desc} [{file:line}] [{safe|risky|extensive}]`
- Empty severities skipped; never skip approval

**Pagination (when >4 per severity or >16 total):**
- Separate questions per severity level
- Per-severity pagination: 8 fixes → 2 questions (4+4)
- Sequential AskUserQuestion calls until all shown

### Option Labels
When presenting options in AskUserQuestion:
- `[current]` - Value from existing context/config
- `[detected]` - Value discovered by detection agent
- `[recommended]` - Single best-fit option based on detection

**[recommended] Rules:**
1. Only ONE option per question can have `[recommended]`
2. Only use when detection provides clear reasoning
3. If no clear winner, show no recommendation
4. Never mark multiple options as recommended

## Fix Workflow
All fix commands follow: **Analyze → Report → Approve → Apply → Verify**

1. **Analyze**: Full scan of target area
2. **Report**: Detection table with priority, location, fix action
3. **Approve**: Paginated approval per Priority & Approval standard
4. **Apply**: ONLY user-selected fixes; respect Safety Classification
5. **Verify**: Before/after comparison + accounting
   ```
   Applied: N | Skipped: N | Failed: N | Total: N
   ```
<!-- CCO_STANDARDS_END -->
