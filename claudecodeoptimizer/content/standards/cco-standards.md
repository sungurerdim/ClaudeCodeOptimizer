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
- Clean Code: meaningful names, single responsibility, consistent style
- Immutability: prefer immutable, mutate only when necessary
- No Overengineering: only requested changes, minimum complexity
- General Solutions: correct algorithms for all inputs, not just test cases
- Explicit Over Implicit: clear intent, no magic values
- Separation of Concerns: distinct responsibilities per module

## File & Resource Management
- Minimal Touch: only files required for task
- Paths: forward slash (/), relative paths, quote spaces
- No Unsolicited Files: never create unless requested
- Cleanup: remove temporary files after iteration
- Resource Cleanup: close handles, release connections, dispose properly
- Exclusions: skip .git, node_modules, __pycache__, venv, dist, build

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
- CHANGELOG: version history with breaking changes
- Comments: explain why, not what
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
- Predictability: consistent behavior across sessions
- Transparency: show what will happen before doing it

---

# AI-Specific Standards
*Applies to ALL AI coding assistants regardless of provider or model*
*AGENTS.md compatible - portable across Claude/Codex/Gemini/etc.*

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
- Accounting: done + skip + fail = total (always verify)
- Structured Results: JSON/table for machine-parseable output when needed

---

# CCO-Specific Standards
*CCO workflow mechanisms - only for CCO users*
*Included in CLAUDE.md export, excluded from AGENTS.md export*

## Command Flow
All CCO commands follow this flow:
1. **Context Check** - Verify CCO_CONTEXT exists; suggest `/cco-tune` if missing
2. **Read Context** - Parse `./CLAUDE.md` for CCO_CONTEXT markers
3. **Execute** - Run command-specific logic
4. **Report** - Show results with verification accounting

## Pre-Operation Safety
- Check `git status` for uncommitted changes before modifications
- If dirty: prompt user → Commit / Stash / Continue
- Clean state enables safe rollback via `git checkout .`

## Safety Classification
| Safe (auto-apply) | Risky (require approval) |
|-------------------|--------------------------|
| Remove unused imports | Auth/CSRF changes |
| Parameterize SQL | DB schema changes |
| Move secrets to env | API contract changes |
| Fix linting issues | Delete files |
| Add type annotations | Rename public APIs |

## Fix Workflow
All fix operations follow: **Analyze → Report → Approve → Apply → Verify**

1. **Analyze**: Scan target area for issues
2. **Report**: Show findings with priority, location, suggested fix
3. **Approve**: User selects which fixes to apply (AskUserQuestion)
4. **Apply**: Execute only approved fixes; respect Safety Classification
5. **Verify**: Confirm changes applied correctly
   ```
   Applied: N | Skipped: N | Failed: N | Total: N
   ```

## Impact Preview
Before applying changes, show potential ripple effects:

| Analysis | What It Shows |
|----------|---------------|
| **Direct Changes** | Files that will be modified |
| **Dependents** | Files that import/use changed code |
| **Test Coverage** | Which tests cover affected code |
| **Risk Score** | LOW/MEDIUM/HIGH based on scope |

Format:
```
┌─ IMPACT PREVIEW ─────────────────────────────────────┐
│ Direct:     {N} files                                │
│ Dependents: {N} files may be affected                │
│ Tests:      {N} tests cover this code                │
│ Risk:       {LOW|MEDIUM|HIGH} ({reason})             │
└──────────────────────────────────────────────────────┘
```

**Skip preview:** For LOW risk changes affecting ≤2 files with full test coverage.

## Priority Levels
| Level | Criteria | Examples |
|-------|----------|----------|
| CRITICAL | Security, data exposure | SQL injection, leaked secrets |
| HIGH | High impact, low effort | Dead code, missing validation |
| MEDIUM | Balanced impact/effort | Complexity, duplication |
| LOW | Low impact or high effort | Style, minor optimization |

## Approval Flow
- Use AskUserQuestion with multiSelect: true
- Priority tabs: CRITICAL → HIGH → MEDIUM → LOW
- Format: `{description} [{file:line}] [{safe|risky}]`
- First option: "All ({N})" for batch selection
- **Pagination**: Max 4 questions × 4 options each; paginate larger sets by priority

## Output Formatting
ASCII box-drawing tables in code blocks:
- Characters: `─│┌┐└┘├┤┬┴┼` borders, `═║╔╗╚╝` headers
- Column width: max cell width + padding; scan all values first
- Alignment: numbers right, text left
- Status: `OK`, `WARN`, `FAIL`, `PASS`, `SKIP` (text only)
- Progress: `████████░░░░░░░░░░░░` (proportional bar)
- No emojis in tables

## Context Integration
- Read `CCO_CONTEXT_START` markers from `./CLAUDE.md`
- Apply: Guidelines, Thresholds, Applicable checks
- Context fields affect command behavior (Scale → thresholds, Data → security weight)

## Claude Code Integration
- Parallel Tools: batch independent calls; sequential when outputs inform inputs
- Subagent Delegation: use Task tool for separate context benefits
- Resource Scaling: thinking tokens based on complexity (8K standard, 16K+ complex)

## Option Labels
When presenting options in AskUserQuestion:
- `[current]` - Value from existing context/config
- `[detected]` - Value discovered by detection
- `[recommended]` - Single best-fit option (only ONE per question)
<!-- CCO_STANDARDS_END -->
