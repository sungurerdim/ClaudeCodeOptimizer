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

### Execution Order [CRITICAL]
1. **Read First**: NEVER propose edits to unread files
2. **Plan Before Act**: understand full scope before any action
3. **Incremental**: complete one step fully before starting next
4. **Verify**: confirm changes match stated intent

### Decision Making
- Challenge: question solutions that seem too perfect
- Ask: when uncertain, clarify before proceeding
- Confidence: explicitly state uncertainty level for non-obvious conclusions

### Prohibited Patterns
- Guessing file contents without reading
- Starting implementation before understanding scope
- Skipping verification steps
- Assuming user intent without confirmation

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

### Tool Configuration [STRICT]
```
Tool: AskUserQuestion
multiSelect: true (always)
```

### Ordering [REQUIRED]
Present items in priority order: CRITICAL → HIGH → MEDIUM → LOW

### Format [EXACT]
`{description} [{file:line}] [{safe|risky}]`

### Batch Options [REQUIRED]
- First option MUST be: "All ({N})" where N = total items
- Remaining options: individual items

### Pagination [LIMITS]
- Max 4 questions per AskUserQuestion call
- Max 4 options per question
- If more items: use multiple sequential calls

## Question Formatting

### Separation Rules [CRITICAL]
**YOU MUST present different question categories in SEPARATE batches.**

| Category Type | Examples | Batch |
|---------------|----------|-------|
| Settings | strictMode, timeout, format | Batch 1 |
| Permissions | readOnly, allowDelete | Batch 2 |
| Thresholds | coverage%, complexity | Batch 3 |

### Labels [MANDATORY]
Each option receives **exactly ONE** label (right side):

| Label | When to Use | Priority |
|-------|-------------|----------|
| `[current]` | Matches existing config | 1 (wins over detected) |
| `[detected]` | Auto-detected, not in config | 2 |
| `[recommended]` | Best practice, max 1/question | 3 (always show) |

**Precedence:** If detected AND current both apply → show `[current]` only

### Ordering [REQUIRED]
- Numeric values: ascending (60 → 70 → 80 → 90)
- Severity: safest → riskiest
- Scope: narrowest → widest

### Verification [PRE-OUTPUT]
Before calling AskUserQuestion, verify:
1. Categories separated into distinct question batches
2. Each option has exactly ONE label
3. Maximum ONE `[recommended]` per question
4. Options ordered per rules above

### Examples

<example type="correct">
**Batch 1 - Settings:**
Q: "Select output format"
- JSON [current]
- YAML
- XML [recommended]

**Batch 2 - Permissions:**
Q: "Select access level"
- Read-only [detected]
- Full access
</example>

<example type="incorrect" reason="Mixed categories">
Q: "Configure options"
- JSON output [current]
- Full access [detected]
- Strict mode
</example>

<example type="incorrect" reason="Multiple labels">
- JSON [current] [recommended]
</example>

<example type="incorrect" reason="Missing label on detected item">
- JSON (detected but no label shown)
</example>

## Output Formatting

### Table Characters [STRICT]
| Type | Characters |
|------|------------|
| Borders | `─│┌┐└┘├┤┬┴┼` |
| Headers | `═║╔╗╚╝` |

### Alignment [REQUIRED]
- Numbers: right-aligned
- Text: left-aligned
- Status indicators: centered

### Status Indicators [EXACT]
Use ONLY these values: `OK` | `WARN` | `FAIL` | `PASS` | `SKIP`

### Progress Bars [FORMULA]
`filled = round(percentage / 100 * 8)` → `████░░░░`

### Prohibited
- No emojis in tables
- No unicode decorations beyond specified characters
- No ASCII art headers

## Integration
- Context: read CCO_CONTEXT_START markers
- Apply: Guidelines, Thresholds, Applicable
- Tools: parallel independent, sequential dependent
- Thinking: 5K standard, 8K medium, 10K complex
<!-- CCO_STANDARDS_END -->
