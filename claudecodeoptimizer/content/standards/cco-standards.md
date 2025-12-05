<!-- CCO_STANDARDS_START -->
# Universal Standards
*Applies to ALL software projects regardless of language, framework, or team size*
*AI/human agnostic - fundamental principles that always apply*

## Code Quality
- Fail-Fast: immediate visible failure, no silent fallbacks
- DRY: single source of truth, zero duplicates
- No Orphans: every function called, every import used
- Type Safety: annotations where language supports
- Complexity: cyclomatic <10 per function
- Clean Code: meaningful names, single responsibility
- Immutability: prefer immutable, mutate only when necessary
- No Overengineering: only requested changes, minimum complexity
- General Solutions: correct algorithms for all inputs
- Explicit Over Implicit: clear intent, no magic values
- Separation of Concerns: distinct responsibilities per module
- Consistent Style: follow language/framework idioms

## File & Resource Management
- Minimal Touch: only files required for task
- Paths: forward slash (/), relative, quote spaces
- No Unsolicited Files: never create unless requested
- Cleanup: remove temporary files after iteration
- Exclusions: skip .git, node_modules, __pycache__, venv, dist, build
- Resource Cleanup: close handles, release connections, dispose properly

## Security Fundamentals
- Secrets: never hardcode, use env vars or vault
- Input Boundaries: validate at system entry points
- Least Privilege: minimum necessary access/permissions
- Dependencies: keep updated, review before adding
- Defense in Depth: multiple layers, don't trust single control
- Secure Defaults: opt-in to less secure, not opt-out

## Testing Fundamentals
- Coverage: meaningful coverage (context-adjusted: 60-90%)
- Isolation: no dependencies between tests
- Test Integrity: never edit tests to make code pass
- Critical Paths: e2e for critical workflows
- Reproducible: same input → same result, no flaky tests

## Error Handling
- Fail Gracefully: catch, log context, recover or propagate
- No Silent Failures: never swallow exceptions without logging
- User-Friendly: technical details in logs, clarity for users
- Rollback on Failure: leave system in consistent state
- Actionable Errors: include what went wrong and how to fix

## Documentation
- README: description, setup, usage
- CHANGELOG: version history
- Comments: why not what
- Examples: working examples for common use cases

## Workflow
- Review Conventions: match existing patterns
- Reference Integrity: find ALL refs → update in order → verify
- Decompose: break complex tasks into smaller steps
- Version: SemVer (MAJOR.MINOR.PATCH)

## UX/DX
- Minimum Friction: fewest steps to goal
- Maximum Clarity: unambiguous output, clear next actions
- Fast Feedback: progress indicators, incremental results
- Error Recovery: actionable messages with fix suggestions
- Predictability: consistent behavior
- Transparency: show what will happen before doing it

---

# AI-Specific Standards
*Applies to ALL AI coding assistants for better quality/efficiency*
*AGENTS.md compatible - portable across AI tools*

## Context Optimization
- Semantic Density: max meaning per token, concise over verbose
- Structured Format: tables/lists over prose for clarity
- Front-load Critical: important info first (Purpose → Details → Edge cases)
- Scannable Hierarchy: clear H2 → H3 → bullets
- Reference Over Repeat: cite by name instead of duplicating
- Bounded Context: provide relevant scope, not entire codebase

## AI Behavior
- Read First: always read files before proposing edits
- Plan Before Act: understand scope before making changes
- Work Incrementally: complete one step fully before next
- Verify Changes: confirm changes match intent
- Challenge Assumptions: question "perfect-looking" solutions
- Ask When Uncertain: clarify ambiguous requirements before proceeding
- State Confidence: indicate certainty level for non-obvious suggestions

## Quality Control
- No Vibe Coding: avoid unfamiliar frameworks without understanding
- No Example Fixation: adapt examples to context, don't copy blindly
- No Hallucination: don't invent APIs, methods, or features that don't exist
- Positive Framing: tell what to do, not what to avoid
- Contextual Motivation: explain WHY behaviors matter

## Status Updates
- Announce Before Action: state what will be done before starting
- Progress Signals: "Starting...", "In progress...", "Completed"
- Timing Accuracy: announce at the right moment (not after completion)
- Phase Transitions: clear signals when moving between workflow phases
- No Silent Operations: user should always know what's happening

## Multi-Model Compatibility
- Model-Agnostic Instructions: no model-specific syntax in shared rules
- Capability Awareness: account for different model strengths
- Graceful Degradation: work with models that lack certain features
- Tool-Agnostic Patterns: patterns that work across Claude/Codex/Gemini/etc.

## Output Standards
- Error Format: [SEVERITY] {What} in {file:line}
- Status Values: OK/WARN/FAIL (consistent terminology)
- Accounting: done + skip + fail = total
- Structured Results: JSON/table for machine-parseable output when needed

---

# CCO-Workflow
*CCO-specific mechanisms - only for CCO users*
*Not exported to AGENTS.md*

## Pre-Operation Safety
1. Check `git status` for uncommitted changes
2. If dirty: AskUserQuestion → Commit / Stash / Continue
3. Clean state enables safe rollback
4. Use git for state persistence across sessions

## Safety Classification
| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |
| Fix linting issues | Delete files |
| Add type annotations | Rename public APIs |

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

## Priority & Approval

### Priority Levels
| Level | Criteria | Examples |
|-------|----------|----------|
| CRITICAL | Security, data exposure | SQL injection, leaked secrets |
| HIGH | High impact, low effort | Dead code, missing validation |
| MEDIUM | Balanced impact/effort | Complexity, duplication |
| LOW | Low impact or high effort | Style, minor optimization |

### Approval Flow
- AskUserQuestion with severity tabs
- multiSelect: true; First option: "All ({N})"
- Format: `{desc} [{file:line}] [{safe|risky}]`
- Never skip approval for risky changes

**Pagination (when >4 per severity or >16 total):**
- Separate questions per severity level
- Per-severity pagination: 8 fixes → 2 questions (4+4)

## Context Read
1. Read `CCO_CONTEXT_START` from `./CLAUDE.md`
2. If missing → suggest `/cco-tune`
3. Apply: Guidelines, Thresholds, AI Performance, Applicable checks

## Claude Code Integration
- Parallel Tools: batch independent calls; sequential when outputs inform inputs
- Subagent Delegation: use Task tool when separate context benefits
- Resource Scaling: thinking tokens Off/8K/16K/32K based on complexity
- MCP Output: default 25K; increase for large outputs

## Output Formatting
ASCII box-drawing tables in code blocks:
- Characters: `─│┌┐└┘├┤┬┴┼` borders, `═║╔╗╚╝` headers
- Column width: max cell width + padding; scan all values first
- Alignment: numbers right, text left
- Status: `OK`, `WARN`, `FAIL`, `PASS`, `SKIP` (text only)
- Progress: `████████░░░░░░░░░░░░` (proportional bar)
- ASCII-only: no emojis in tables

## Option Labels
When presenting options in AskUserQuestion:
- `[current]` - Value from existing context/config
- `[detected]` - Value discovered by detection agent
- `[recommended]` - Single best-fit option based on detection
Only ONE option per question can have `[recommended]`
<!-- CCO_STANDARDS_END -->
