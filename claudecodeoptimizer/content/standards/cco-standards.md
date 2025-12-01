<!-- CCO_STANDARDS_START -->
# Universal Standards
*Software engineering best practices - any project, any language, any tool*

## Quality

### Code
- Fail-Fast: immediate visible failure, no silent fallbacks
- DRY: single source of truth, zero duplicates
- No Orphans: every function called, every import used
- Type Safety: annotations + strict static analysis
- Complexity: cyclomatic <10 per function (context may override)
- Tech Debt: ratio <5%
- Maintainability: index >65
- No Overengineering: only changes directly requested or clearly necessary
  - Don't add features, refactor, or improve beyond what was asked
  - Don't create helpers/utilities for one-time operations
  - Don't design for hypothetical future requirements
  - Minimum complexity needed for current task
- General Solutions: implement for all valid inputs, not just test cases
  - Don't hard-code values that make tests pass
  - Focus on correct algorithms, not passing specific tests
  - No helper scripts or workarounds; use standard tools
- Clean Code: meaningful names, single responsibility
- Immutability: prefer immutable, mutate only for performance
- Profile First: measure before optimize
- Version: single source, SemVer (MAJOR.MINOR.PATCH)

### Testing
- Coverage: 80% min (context may adjust: solo 60%, enterprise 90%)
- Integration: e2e for critical workflows
- CI Gates: lint + test + coverage + security before merge
- Isolation: no dependencies between tests
- TDD: tests first, code satisfies
- Test Integrity: never remove or edit tests to make code pass
  - Tests define expected behavior; code must satisfy them

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

---

# Claude-Specific Standards
*AI assistant behavior, workflow, and interaction patterns*

## Workflow

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
- Paths: forward slash (/), relative, quote spaces
- Reference Integrity: find ALL refs → update in order → verify (grep old=0, new=expected)
- Verification: total = done + skip + fail + cannot_do, no "fixed" without Read proof
- Error Format: `❌ {What} → ↳ {Why} → → {Fix}` (consistent across all commands)
- Parallel Tools: make all independent tool calls in parallel for efficiency
  - If no dependencies between calls, batch them in single message
  - Sequential only when outputs inform subsequent inputs
- Moderate Triggers: use "when..." phrasing for tool guidance
  - Avoid aggressive language like "CRITICAL: You MUST use this tool"
  - Prefer: "Use this tool when..." or "Consider using..."
- Cleanup: remove temporary files created during iteration at task end

## Approval Flow
- Single call, 4 tabs: one AskUserQuestion with 4 questions max (Critical/High/Medium/Low)
- Each priority = one tab: user sees all levels at once, selects per-tab
- Header format: "{Priority} ({count})" - e.g., "Critical (2)", "High (5)"
- Options per tab (max 4):
  - Option 1: "All ({N})" - always first, includes all items in this priority
  - Options 2-4: top 3 individual items by impact, format: "{desc} [{loc}] [{risk}]"
  - If >3 items: remaining are included in "All" (count shows total)
- Risk labels: [safe], [risky], or [extensive] per item
- MultiSelect: true - "All" + individual items can be combined
- Skip empty tabs: don't show priority levels with 0 items
- Summary before apply: "Applying {selected}/{total} items"
- No silent skipping: ALL items accessible via "All ({N})" option
- Apply all selected: user selection = commitment, fix everything chosen
- Blocked items: report as "cannot_do" with reason after attempt

## Agentic Coding
- Read First: ALWAYS read and understand relevant files before proposing code edits
  - Never speculate about code you have not inspected
  - Inspect specific files referenced by users before explaining or proposing fixes
- No Speculation: never make claims about code before investigating
  - Investigate relevant files before answering code questions
  - Provide grounded, hallucination-free answers
- Review Conventions: thoroughly review codebase style, conventions, and abstractions before implementing
  - Be rigorous and persistent in searching code for key facts
  - Match existing patterns in the codebase
- Positive Framing: tell what to do, not what to avoid
  - "Write in flowing prose" vs "Don't use markdown"
  - Negative framing can paradoxically increase unwanted behavior
- Action vs Suggest: be explicit about when to act vs suggest
  - For proactive: "Implement changes rather than only suggesting them"
  - For conservative: "Provide recommendations unless explicitly requested to change"
- Contextual Motivation: explain WHY a behavior matters
  - Helps Claude understand goals and apply judgment appropriately

## AI-Assisted
- Review AI Code: treat as junior output, verify
- Workflow: Plan → Act → Review → Repeat
- Test AI Output: unit tests before integration
- Decompose: break complex tasks for AI
- No Vibe Coding: avoid rare langs/new frameworks without solid foundation
- Human-AI: humans architect, AI implements, humans review
- Challenge: "are you sure?" for perfect-looking solutions
- No Example Fixation: use placeholders, avoid anchoring bias from hardcoded examples
  - Examples are scrutinized carefully; ensure they align with desired behaviors
  - Misaligned examples encourage unwanted patterns
- Thinking Escalation: auto-increase budget on complexity/errors
  - Start: context default (off/8K/32K from AI Performance)
  - Escalate: error_count > 2 OR multi-file refactor OR architectural decision
  - Ceiling: 64K for complex, 32K for medium, 8K for simple projects
- Subagent Delegation: recognize when tasks benefit from specialized subagents
  - Ensure subagent tools are well-defined in descriptions
  - For conservative: "Only delegate when task clearly benefits from separate context"

## Context Management

### When to Use Extended Thinking
- Use Off for: simple questions, file lookups, straightforward edits
- Use 8K for: standard coding, moderate refactors, single-file changes
- Use 16K+ for: multi-file refactors, complex debugging, architectural decisions
- Use 32K for: algorithm design, complex math, deep analysis requiring multiple steps
- Increase budget when: errors persist after 2+ attempts, task spans many files
- Word sensitivity: when thinking is off, say "consider/evaluate" instead of "think"

### When to Increase MCP Limit
- Keep 25K for: normal tool responses, standard file reads
- Use 50K for: large file analysis, multiple tool results
- Use 100K for: codebase-wide searches, extensive grep results

### Long Session Practices
- Don't stop tasks early: context auto-compacts, work can continue indefinitely
- Work incrementally: complete one step fully before starting next
- Track state: use JSON for structured data, plain text for progress notes
- Before using /compact: specify what to preserve (errors, decisions) and discard (exploration)
- Between unrelated tasks: use /clear to reset context
- After fresh start: review filesystem state, don't assume previous context
<!-- CCO_STANDARDS_END -->
