<!-- CCO_STANDARDS_START -->
# Universal Standards
*AI/human agnostic - fundamental principles for all software projects*

## Code Quality
- Fail-Fast: no silent fallbacks, immediate visible failure
- DRY: single source of truth, no duplicates
- No Orphans: every function called, every import used
- Type-Safe: annotations where supported, prefer immutable
- Complexity: cyclomatic <10 per function
- Clean: meaningful names, single responsibility, consistent style
- Explicit: no magic values, clear intent
- Scope: only requested changes, general solutions

## File & Resource
- Minimal Touch: only files required for task
- No Unsolicited: never create files unless requested
- Paths: forward slash, relative, quote spaces
- Cleanup: temp files, handles, connections
- Skip: .git, node_modules, __pycache__, venv, dist, build

## Security
- Secrets: env vars or vault only
- Input: validate at system boundaries
- Access: least privilege, secure defaults
- Deps: review before adding, keep updated
- Defense: multiple layers, don't trust single control

## Testing
- Coverage: 60-90% context-adjusted
- Isolation: no inter-test deps, reproducible
- Integrity: never edit tests to pass code
- Critical Paths: e2e for critical workflows

## Error Handling
- Catch: log context, recover or propagate
- No Silent: never swallow exceptions
- User-Facing: clarity + actionable
- Logs: technical details only
- Rollback: consistent state on failure

## Documentation
- README: description, setup, usage
- CHANGELOG: versions with breaking changes
- Comments: why not what
- Examples: working, common use cases

## Workflow
- Conventions: match existing patterns
- Reference Integrity: find ALL refs, update, verify
- Decompose: break complex tasks into steps
- Version: SemVer (MAJOR.MINOR.PATCH)

## UX/DX
- Minimum Friction: fewest steps to goal
- Maximum Clarity: unambiguous output
- Predictable: consistent behavior

---

# AI-Specific Standards
*Portable across Claude/Codex/Gemini - AGENTS.md compatible*

## Context Optimization
- Semantic Density: concise over verbose
- Structured: tables/lists over prose
- Front-load: critical info first
- Hierarchy: H2 > H3 > bullets
- Scope: bounded, reference over repeat

## AI Behavior
- Read First: before proposing edits
- Plan Before Act: understand scope first
- Incremental: one step fully before next
- Verify: changes match intent
- Challenge: question perfect-looking solutions
- Ask: when uncertain, clarify first
- Confidence: state level for non-obvious

## Quality Control
- Understand First: no vibe coding
- Adapt: examples to context, don't copy blind
- No Hallucination: only existing APIs/features
- Positive: what to do, not what to avoid
- Motivate: explain why behaviors matter

## Status Updates
- Announce: before action, not after
- Progress: Starting > In progress > Completed
- Transitions: clear phase signals
- No Silent: user always knows state

## Multi-Model
- Agnostic: no model-specific syntax
- Graceful: account for different capabilities
- Portable: patterns work across models

## Output Standards
- Error: `[SEVERITY] {What} in {file:line}`
- Status: OK / WARN / FAIL
- Accounting: done + skip + fail = total
- Structured: JSON/table when needed

---

# CCO-Specific Standards
*CCO workflow mechanisms - excluded from AGENTS.md export*

## Command Flow
1. Context Check: verify CCO_CONTEXT, suggest /cco-tune if missing
2. Read Context: parse ./CLAUDE.md markers
3. Execute: command-specific logic
4. Report: results with accounting

## Safety
- Pre-op: git status before modifications
- Dirty: prompt Commit / Stash / Continue
- Rollback: clean state enables git checkout

### Classification
**Safe (auto-apply):**
- Remove unused imports
- Parameterize SQL
- Move secrets to env
- Fix linting issues
- Add type annotations

**Risky (require approval):**
- Auth/CSRF changes
- DB schema changes
- API contract changes
- Delete files
- Rename public APIs

## Fix Workflow
Flow: Analyze > Report > Approve > Apply > Verify
Output: `Applied: N | Skipped: N | Failed: N | Total: N`

## Impact Preview
- Direct: files to modify
- Dependents: files that import/use
- Tests: coverage of affected code
- Risk: LOW / MEDIUM / HIGH
- Skip: LOW risk, <=2 files, full coverage

## Priority
- CRITICAL: security, data exposure
- HIGH: high-impact, low-effort
- MEDIUM: balanced impact/effort
- LOW: style, minor optimization

## Approval Flow
- Tool: AskUserQuestion (multiSelect: true)
- Order: CRITICAL > HIGH > MEDIUM > LOW
- Format: `{description} [{file:line}] [{safe|risky}]`
- Batch: "All ({N})" first option
- Pagination: max 4 questions x 4 options

## Question Formatting
**Labels (right of option):**
- `[detected]` - auto-detected from analysis
- `[current]` - matches existing config
- `[recommended]` - best practice (max 1/question)

**Precedence:**
- detected + current: show current only
- Always show recommended

**Ordering:**
- Numeric: ascending
- Severity: safest to riskiest
- Scope: narrowest to widest

**Specs:**
- Tables for structure
- Placeholders: `{value}`, `{N}`, `{name}`
- No hardcoded values in specs

## Output Formatting
- Borders: `─│┌┐└┘├┤┬┴┼`
- Headers: `═║╔╗╚╝`
- Align: numbers right, text left
- Status: OK / WARN / FAIL / PASS / SKIP
- Progress: `████░░░░` proportional
- No emojis in tables

## Integration
- Context: read CCO_CONTEXT_START markers
- Apply: Guidelines, Thresholds, Applicable
- Tools: parallel independent, sequential dependent
- Thinking: 5K standard, 8K medium, 10K complex
<!-- CCO_STANDARDS_END -->
