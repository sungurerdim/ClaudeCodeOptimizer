<!-- CCO_STANDARDS_START -->
# Universal Standards
*Software engineering best practices - any project, any AI*

## Quality

### Code
- Fail-Fast: immediate visible failure, no silent fallbacks
- DRY: single source of truth, zero duplicates
- No Orphans: every function called, every import used
- Type Safety: annotations + strict static analysis
- Complexity: cyclomatic <10 per function (context may override)
- Tech Debt: ratio <5%
- Maintainability: index >65
- No Overengineering: only requested changes, no one-time helpers, no hypothetical futures, minimum complexity
- Minimal Touch: only files required for task, no "while I'm here" improvements
- General Solutions: correct algorithms for all inputs, no test-specific hacks, use standard tools
- Clean Code: meaningful names, single responsibility
- Immutability: prefer immutable, mutate only for performance
- Profile First: measure before optimize
- Version: single source, SemVer (MAJOR.MINOR.PATCH)
- Paths: forward slash (/), relative, quote spaces
- No Unsolicited Files: never create unless requested; prefer editing existing
- Cleanup: remove temporary files created during iteration
- Timeouts: explicit for all external calls; never wait indefinitely
- Retry: exponential backoff + jitter for transient failures

### Testing
- Coverage: 80% min (context may adjust: solo 60%, enterprise 90%)
- Pyramid: 70% unit (<1ms), 20% integration (~100ms), 10% E2E (seconds)
- Integration: e2e for critical workflows
- CI Gates: lint + test + coverage + security before merge
- Isolation: no dependencies between tests
- TDD: tests first, code satisfies
- Test Integrity: tests define behavior; never edit tests to make code pass

### Security
- Input Validation: Pydantic/Joi/Zod at all entry points
- SQL: parameterized queries only
- Secrets: never hardcode, use env vars or vault
- XSS: sanitize all user input
- OWASP: API Top 10 compliance
- Dependencies: Dependabot, scan in CI

## Docs
- README: description, setup, usage, contributing
- CHANGELOG: version history, Keep a Changelog format
- API Docs: complete, accurate, auto-generated
- ADR: decisions + context + consequences
- Comments: why not what

## Workflow
- Read First: read files before proposing edits; never speculate about uninspected code
- Review Conventions: match existing patterns; be rigorous in searching for key facts
- Reference Integrity: find ALL refs → update in order → verify (grep old=0, new=expected)
- Verification: total = done + skip + fail + cannot_do, no "fixed" without proof
- Workflow: Plan → Act → Review → Repeat
- Decompose: break complex tasks into smaller steps
- No Vibe Coding: avoid rare langs/new frameworks without solid foundation
- Challenge: "are you sure?" for perfect-looking solutions
- No Example Fixation: use placeholders; misaligned examples encourage unwanted patterns

---

# Claude-Specific Standards
*Claude Code architecture, tools, and features*

## CCO Workflow

### Pre-Operation Safety
1. Check `git status` for uncommitted changes
2. If dirty: AskUserQuestion → Commit (cco-commit) / Stash / Continue
3. Clean state enables safe rollback
4. Use git for state persistence across sessions

### Context Read
1. Read `CCO_CONTEXT_START` from `./CLAUDE.md` (NOT `.claude/`)
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

## Core
- Exclusions: skip .git, node_modules, __pycache__, venv, dist, build, lockfiles, *.min.js
- Error Format: `❌ {What} → ↳ {Why} → → {Fix}` (consistent across all commands)
- Parallel Tools: batch independent calls in single message; sequential only when outputs inform inputs
- Moderate Triggers: "Use when..." not "CRITICAL: You MUST..."

## Approval Flow
- Single AskUserQuestion, 4 priority tabs (Critical/High/Medium/Low), skip empty
- Header: "{Priority} ({count})" | Options: "All ({N})" first, then top 3 by impact
- Format: "{desc} [{loc}] [{risk}]" with risk labels [safe]/[risky]/[extensive]
- MultiSelect enabled | Summary: "Applying {selected}/{total}"
- All items accessible via "All" option; blocked items report as "cannot_do"

## Prompt Engineering
- Positive Framing: tell what to do ("write prose") not what to avoid ("don't use markdown")
- Action vs Suggest: explicit mode—proactive implements, conservative recommends
- Contextual Motivation: explain WHY behaviors matter for better judgment
- Thinking Escalation: start at context default → increase on errors/complexity (set via MAX_THINKING_TOKENS)
- Subagent Delegation: delegate when separate context benefits; ensure tool descriptions are well-defined

## Frontend Generation (Avoid AI Slop)
- Typography: choose beautiful, unique fonts; avoid defaults (Arial, Inter, Roboto, system fonts)
- Color & Theme: CSS variables for consistency; dominant colors with sharp accents
- Motion: prioritize high-impact moments; one well-orchestrated page load with staggered reveals
- Backgrounds: create atmosphere and depth; avoid solid color defaults
- Distinctive Design: unexpected choices that feel genuinely designed, not generic AI output
- Avoid: clichéd purple gradients, predictable layouts, convergence on common AI patterns

## Context Management

### Extended Thinking (MAX_THINKING_TOKENS)
- Off (default): simple questions, file lookups, straightforward edits
- 8K-16K: standard coding, moderate refactors, single-file changes
- 16K-32K: multi-file refactors, complex debugging, architectural decisions
- 32K+: algorithm design, complex math, deep multi-step analysis
- Increase when: errors persist after 2+ attempts, task spans many files

### MCP Output Limit (MAX_MCP_OUTPUT_TOKENS)
- Default 25K: normal tool responses, standard file reads
- Increase when: /doctor shows "Large MCP tools context" warning
- Set in: ~/.claude/settings.json → env → MAX_MCP_OUTPUT_TOKENS

### Long Session Practices
- Don't stop tasks early: context auto-compacts, work can continue indefinitely
- Work incrementally: complete one step fully before starting next
- Track state: use JSON for structured data, plain text for progress notes
- Before using /compact: specify what to preserve (errors, decisions) and discard (exploration)
- Between unrelated tasks: use /clear to reset context
- After fresh start: review filesystem state, don't assume previous context
<!-- CCO_STANDARDS_END -->
