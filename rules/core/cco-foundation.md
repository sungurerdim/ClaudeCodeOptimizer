# Foundation Rules
*Constraints and thresholds for code quality - not principles Opus already knows*

## Decision Guard

Before adding code/feature, ask:
1. Does absence break something?
2. Does absence confuse users?
3. Is adding worth complexity cost?

**All NO = don't add.**

## Complexity Thresholds [CRITICAL]

| Metric | Good | Review | Refactor |
|--------|------|--------|----------|
| Cyclomatic Complexity | 1-10 | 11-15 | 16+ |
| Cognitive Complexity | < 15 | 15-20 | 21+ |
| Method Lines | < 50 | 50-100 | 100+ |
| File Lines | < 500 | 500-1000 | 1000+ |
| Nesting Depth | ≤ 3 | 4 | 5+ |
| Parameters | ≤ 4 | 5-7 | 8+ |

## File Handling [CRITICAL]

- **Minimal-Touch**: Only files required for task
- **Request-First**: Create files only when explicitly requested
- **Skip**: `.git`, `node_modules`, `vendor`, `venv`, `dist`, `out`, `target`, `.idea`, `.vscode`, `*.min.*`, `@generated`

## Validation Boundaries [CRITICAL]

All public APIs MUST validate input:
- **Range-Bounds**: Numeric inputs need min/max limits
- **String-Length**: String inputs need max length
- **Collection-Size**: Arrays need max items limit
- **Timeout-Required**: ALL external calls need explicit timeout
- **Close-Always**: Resources closed in finally/with/using

## Refactoring Safety

Before modifying:
- **Delete**: Identify ALL callers before removing
- **Rename**: Find refs → update ALL → verify builds
- **Move**: Update all import statements
- **Signature-Change**: Update all call sites

## Output Format [CRITICAL]

- **Step-Progress**: "Step 2/5: Building..."
- **Summary-Final**: "Changed 3 files, added 2 tests"
- **Impact-Explain**: "This reduces bundle size by 15%"
- **Error-Actionable**: `[SEVERITY] {What} in {file}:{line}`

## Team Scale

| Team Size | Applies |
|-----------|---------|
| < 6 | Informal review OK |
| 6+ | CODEOWNERS, branch protection required |
