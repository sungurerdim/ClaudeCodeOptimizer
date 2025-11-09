---
description: Comprehensive audit (code, security, tests, docs, principles, all)
category: audit
cost: 3
---

# CCO Audit Commands

Run comprehensive audits on your codebase: code quality, security, tests, documentation, and principle compliance.

## Prerequisites: Load Project Context

**BEFORE running any audit**, load the following documents to understand project standards:

### Required Project Documents

1. **CLAUDE.md** - Main development guide
   - Load: `@CLAUDE.md`
   - Contains: Core development principles, verification protocol, test-first development, git workflow, security standards

2. **PRINCIPLES.md** - Active principles for this project
   - Load: `@PRINCIPLES.md`
   - Contains: Project-specific mandatory development principles

3. **Project Configuration** - Project preferences and standards
   - Load from: `.cco/project.json` (if exists) or global registry
   - Check with:
   ```bash
   python -c "
   from pathlib import Path
   import json

   project_name = Path.cwd().name
   registry_file = Path.home() / '.cco' / 'projects' / f'{project_name}.json'

   if registry_file.exists():
       config = json.loads(registry_file.read_text())
       print(json.dumps(config, indent=2))
   else:
       print('Project not initialized. Run /cco-init first.')
   "
   ```

### Category-Specific Guide Documents

Load these **on-demand** based on audit type:

- **Code Quality**: `@docs/cco/guides/verification-protocol.md`, `@docs/cco/principles/code-quality.md`
- **Security**: `@docs/cco/guides/security-response.md`, `@docs/cco/principles/security.md`
- **Tests**: `@docs/cco/principles/testing.md`
- **Documentation**: `@docs/cco/principles/code-quality.md` (docstring section)
- **Performance**: `@docs/cco/guides/performance-optimization.md`, `@docs/cco/principles/performance.md`
- **Operations**: `@docs/cco/guides/container-best-practices.md`, `@docs/cco/principles/operations.md`
- **Architecture**: `@docs/cco/principles/architecture.md`
- **API Design**: `@docs/cco/principles/api-design.md`
- **Git Workflow**: `@docs/cco/guides/git-workflow.md`, `@docs/cco/principles/git-workflow.md`

---

## Step 1: Select Audit Types

**Use AskUserQuestion tool** to ask which audits to run:

```json
{
  "questions": [{
    "question": "Which audits would you like to run?",
    "header": "Audit Selection",
    "multiSelect": true,
    "options": [
      {"label": "Code Quality", "description": "Run linters, formatters, type checkers (black, ruff, eslint, etc.)"},
      {"label": "Security", "description": "Security & privacy audit (7 principles: encryption, secrets, TTL, etc.)"},
      {"label": "Tests", "description": "Test coverage, quality, and flaky test detection"},
      {"label": "Documentation", "description": "Docs completeness, accuracy, and sync with code"},
      {"label": "Principles", "description": "Validate against your active development principles (from PRINCIPLES.md)"},
      {"label": "All", "description": "Run all audits above (recommended for comprehensive review)"}
    ]
  }]
}
```

**All options should be selected by default (multiSelect: true).**

---

## Step 2: Run Selected Audits

Based on user selection, run the corresponding audit sections below.

---

## Audit: Code Quality

**Standards Reference**:
- Load `@CLAUDE.md` (Verification Protocol, Minimal Touch Policy, Root Cause Analysis)
- Load `@docs/cco/guides/verification-protocol.md` (Evidence-based verification)
- Load `@docs/cco/principles/code-quality.md` (P001-P018 principles)
- Check project config for code quality standards (test coverage target, linting rules)

**Runtime tool detection** - automatically detect and run available tools.

### Detect Available Tools

- **Python**: black, ruff, mypy, pylint, flake8, pytest
- **JavaScript/TypeScript**: prettier, eslint, tslint, tsc, jest, vitest
- **Go**: gofmt, goimports, golint, staticcheck, go test
- **Rust**: rustfmt, clippy, cargo test
- **Other**: Language-specific formatters, linters, type checkers

### Run Checks

Use Task tool (Explore agent, medium thoroughness):

**Agent must**:
1. Read and understand CLAUDE.md code quality standards
2. Read and understand docs/cco/principles/code-quality.md
3. Check project configuration for specific standards
4. Run detected tools
5. Compare results against project standards (from CLAUDE.md and PRINCIPLES.md)
6. Report violations with principle references (e.g., "Violates P001: Fail-Fast Error Handling")

```bash
# Python example
black --check .
ruff check .
mypy .

# Report results with principle references
```

### Output

- Formatting issues found (with CLAUDE.md standards reference)
- Lint violations (with principle references)
- Type errors
- Violations of code quality principles (P001-P018)
- Recommendations for fixes aligned with CLAUDE.md

**Next Step**: Use `/cco-fix code` to auto-fix issues.

---

## Audit: Security

**Standards Reference**:
- Load `@CLAUDE.md` (Security standards, pre-commit security review)
- Load `@docs/cco/guides/security-response.md` (Security response protocol, common vulnerabilities)
- Load `@docs/cco/principles/security.md` (P019-P037 security principles)
- Check project config for security requirements (deployment target, business domain)

**7 Critical Security & Privacy Principles**

Audit against:
- P019: Privacy-First Design
- P020: TTL Enforcement
- P021: Zero-Disk Policy
- P022: Defense-in-Depth
- P024: Secure Configuration
- P025: Key Derivation
- P026: Secret Scanning
- Plus additional security principles from PRINCIPLES.md

### Architecture (Optimized: Speed + Quality)
- 2 parallel Haiku agents (Explore, quick) - fast security scanning
- 1 Sonnet aggregator (Plan) - intelligent risk assessment
- Custom @security-auditor agent (if available)
- Execution: **20-25 seconds** (2x faster, maintains quality)

### Run Audit

Launch 2 agents in **single message** (critical for parallelism):

**Agent 1: Data Security** (Haiku, quick):
```
Task(Explore, "Audit encryption, privacy, and secrets", model="haiku", thoroughness="quick")

MUST load before scanning:
- @CLAUDE.md (Security section)
- @docs/cco/guides/security-response.md (Common vulnerabilities checklist)
- @docs/cco/principles/security.md (Security principles P019-P037)

Checks:
- P019: Privacy-First Design
- P021: Zero-Disk Policy
- P026: Secret Scanning
- Scan for unencrypted sensitive data
- Detect hardcoded secrets (API keys, passwords, tokens)
- Check .env, config files
- Verify .gitignore for secrets
- Compare against security-response.md checklist
```

**Agent 2: Security Architecture** (Haiku, quick):
```
Task(Explore, "Audit security architecture and config", model="haiku", thoroughness="quick")

MUST load before scanning:
- @CLAUDE.md (Security section)
- @docs/cco/guides/security-response.md (Security architecture patterns)
- @docs/cco/principles/security.md (Security principles P019-P037)

Checks:
- P020: TTL Enforcement
- P022: Defense-in-Depth
- P024: Secure Configuration
- P025: Key Derivation
- Validate security headers
- Check HTTPS enforcement
- Verify data expiration
- Check input validation
- Compare against security-response.md patterns
```

### Aggregation

Use Sonnet Plan agent for intelligent risk assessment:
```
Task(Plan, "Analyze security audit findings", model="sonnet", prompt="""
Analyze security findings from 2 parallel security audits.

MUST reference in analysis:
- CLAUDE.md security standards
- docs/cco/guides/security-response.md (incident response, common fixes)
- docs/cco/principles/security.md (all security principles)
- Project config (deployment target, business domain for context)

Tasks:
1. Merge all security findings
2. Assess actual risk level (not just theoretical)
3. Identify attack vectors and exploit scenarios
4. Prioritize by: exploitability × impact
5. Provide specific remediation steps (reference security-response.md fixes)
6. Estimate security debt and fix effort
7. Recommend immediate actions vs long-term hardening
8. Reference specific principles violated (e.g., "Violates P020: TTL Enforcement")
9. Align recommendations with CLAUDE.md pre-commit security checklist

Focus on practical, actionable security improvements aligned with project standards.
""")
```

Why Sonnet here:
- Risk assessment requires reasoning (not just data)
- Attack vector analysis needs intelligence
- Prioritization by real-world exploitability
- Context-aware remediation recommendations aligned with project docs

---

## Audit: Tests

**Standards Reference**:
- Load `@CLAUDE.md` (Test-First Development, Verification Protocol)
- Load `@docs/cco/principles/testing.md` (P013-P018 testing principles)
- Check project config for test coverage target (default: 80%)

**Test Coverage & Quality Analysis**

### Metrics

1. **Coverage**: Line, branch, function coverage
   - Compare against project target from config (default: 80%)
2. **Quality**: Assertion quality, test isolation
   - Check adherence to P013-P018 principles
3. **Flaky Tests**: Detect non-deterministic tests
4. **Speed**: Identify slow tests
5. **Test-First**: Verify tests exist BEFORE implementation (P067)

### Run Analysis

**Agent must**:
1. Read CLAUDE.md Test-First Development section
2. Read docs/cco/principles/testing.md
3. Load project test coverage target from config
4. Run coverage tools
5. Analyze against testing principles
6. Report violations with principle references

```bash
# Python
pytest --cov --cov-report=term-missing
pytest --durations=10

# JavaScript
jest --coverage
npm test -- --verbose

# Compare results against project target
```

### Output

- Coverage percentage vs project target (e.g., "65% < 80% target" - violates project config)
- Uncovered files/lines
- Flaky test detection
- Slow tests (>5s)
- Testing principle violations (P013-P018)
- Alignment with CLAUDE.md Test-First Development

**Next Step**: Use `/cco-generate tests` for missing coverage.

---

## Audit: Documentation

**Standards Reference**:
- Load `@CLAUDE.md` (Documentation Updates section)
- Load `@docs/cco/principles/code-quality.md` (Docstring requirements)
- Check project config for documentation standards

**Documentation Completeness & Accuracy**

### Check

1. **API Docs**: All public APIs documented
2. **README**: Up-to-date setup instructions
3. **Inline Comments**: Complex logic explained (per CLAUDE.md)
4. **Sync**: Docs match actual code behavior
5. **Examples**: Working code examples
6. **CLAUDE.md Alignment**: Documentation follows project standards

### Run Audit

Use Task tool (Explore agent):

**Agent must**:
1. Read CLAUDE.md Documentation Updates section
2. Read docs/cco/principles/code-quality.md (docstring section)
3. Understand project documentation standards
4. Scan documentation
5. Compare against CLAUDE.md requirements

```
1. Check README exists and is current
2. Verify API documentation coverage
3. Scan for outdated docs (deprecated APIs, old examples)
4. Check docstring coverage (Python) or JSDoc (JS)
5. Verify alignment with CLAUDE.md documentation standards:
   - Present tense, clean slate approach
   - Concise (tables, lists, code blocks)
   - Atomic updates (docs with code)
```

### Output

- Missing documentation (with CLAUDE.md standards)
- Outdated documentation
- Documentation quality score
- Violations of documentation principles
- Alignment with CLAUDE.md documentation standards

**Next Step**: Use `/cco-fix docs` to update documentation.

---

## Audit: Principles

**Standards Reference**:
- Load `@CLAUDE.md` (ALL sections - core development standards)
- Load `@PRINCIPLES.md` (Project-specific active principles)
- Load category-specific principle documents based on active principles:
  - `@docs/cco/principles/core.md` (P001, P067, P071 - ALWAYS)
  - `@docs/cco/principles/code-quality.md` (P001-P018)
  - `@docs/cco/principles/architecture.md` (P038-P048)
  - `@docs/cco/principles/security.md` (P019-P037)
  - `@docs/cco/principles/testing.md` (P013-P018)
  - `@docs/cco/principles/performance.md` (P054-P058)
  - `@docs/cco/principles/operations.md` (P059-P063)
  - `@docs/cco/principles/api-design.md` (P049-P053)
  - `@docs/cco/principles/git-workflow.md` (P064-P072)
- Check project config for context (team size, maturity, deployment target)

**Validate Against Your Active Development Principles**

This audit checks your code against the principles that are active for this project (configured in PRINCIPLES.md).

### Load Active Principles

First, load your project's active principles:

```bash
python -c "
from pathlib import Path
import json

# Method 1: Read from PRINCIPLES.md (recommended)
principles_md = Path.cwd() / 'PRINCIPLES.md'
if principles_md.exists():
    # Count principles from markdown
    content = principles_md.read_text()
    principle_count = content.count('### P')
    print(f'Active principles: {principle_count}')
    print(f'Reading from: PRINCIPLES.md')
else:
    # Method 2: Read from registry
    project_name = Path.cwd().name
    registry_file = Path.home() / '.cco' / 'projects' / f'{project_name}.json'

    if registry_file.exists():
        config = json.loads(registry_file.read_text())
        selected_ids = config.get('selected_principles', [])
        print(f'Active principles: {len(selected_ids)}')
        print(f'Reading from: registry')
        print(f'IDs: {selected_ids[:5]}...')
    else:
        print('[ERROR] No PRINCIPLES.md or registry found')
        print('Run /cco-init first')
"
```

**If no principles found**: Stop and inform user to run `/cco-init` first.

### Load Principle Definitions

```bash
python -c "
from pathlib import Path
import json

# Get active principle IDs from registry
project_name = Path.cwd().name
registry_file = Path.home() / '.cco' / 'projects' / f'{project_name}.json'
config = json.loads(registry_file.read_text())
selected_ids = config.get('selected_principles', [])

# Load full principle definitions
knowledge_file = Path.home() / '.cco' / 'knowledge' / 'principles.json'
all_principles = json.loads(knowledge_file.read_text())['principles']

# Filter to only active principles
active_principles = [p for p in all_principles if p['id'] in selected_ids]

print(f'Loaded {len(active_principles)} active principles')
print('')
print('By category:')
by_category = {}
for p in active_principles:
    cat = p.get('category', 'unknown')
    by_category[cat] = by_category.get(cat, 0) + 1

for cat, count in sorted(by_category.items()):
    print(f'  {cat}: {count}')
"
```

### Architecture (Optimized: Speed + Quality)

**Hybrid approach for fast + smart analysis:**
- 3 parallel Haiku agents (Explore, quick) - fast data gathering
- 1 Sonnet aggregator (Plan) - intelligent analysis & recommendations
- Execution: **15-20 seconds** (2x faster, maintains quality)
- Dynamic: Only audits categories that have active principles

**Why this works:**
- Haiku: Fast scanning, data collection (good enough for finding issues)
- Sonnet: Deep analysis, prioritization, actionable insights (critical for decisions)
- Grouped categories reduce agent overhead
- Parallelization maintained

### Run Audit

**Launch 3 Parallel Agents (SINGLE MESSAGE)**

Grouped by focus area:

**Agent 1 - Code & Architecture** (Haiku, quick):
```
Task(Explore, "Audit code quality and architecture principles", model="haiku", thoroughness="quick")

MUST load before auditing:
- @CLAUDE.md (All sections)
- @PRINCIPLES.md (Active principles)
- @docs/cco/principles/core.md (P001, P067, P071)
- @docs/cco/principles/code-quality.md (P001-P018)
- @docs/cco/principles/architecture.md (P038-P048)
- Project config for context

Audit:
- Code Quality principles (P001-P018)
- Architecture principles (P038-P048)
- Core principles (P001, P067, P071)
Focus: Static code analysis, pattern detection
```

**Agent 2 - Security & Operations** (Haiku, quick):
```
Task(Explore, "Audit security and operations principles", model="haiku", thoroughness="quick")

MUST load before auditing:
- @CLAUDE.md (Security, Operations sections)
- @PRINCIPLES.md (Active principles)
- @docs/cco/principles/security.md (P019-P037)
- @docs/cco/principles/operations.md (P059-P063)
- @docs/cco/guides/security-response.md
- @docs/cco/guides/container-best-practices.md
- Project config (deployment target, business domain)

Audit:
- Security & Privacy principles (P019-P037)
- Operational Excellence principles (P059-P063)
Focus: Runtime & config analysis, security patterns
```

**Agent 3 - Process & Performance** (Haiku, quick):
```
Task(Explore, "Audit testing, performance, API, and git principles", model="haiku", thoroughness="quick")

MUST load before auditing:
- @CLAUDE.md (Test-First, Git Workflow, Performance sections)
- @PRINCIPLES.md (Active principles)
- @docs/cco/principles/testing.md (P013-P018)
- @docs/cco/principles/performance.md (P054-P058)
- @docs/cco/principles/api-design.md (P049-P053)
- @docs/cco/principles/git-workflow.md (P064-P072)
- @docs/cco/guides/git-workflow.md
- @docs/cco/guides/performance-optimization.md
- Project config (test coverage target)

Audit:
- Testing principles (P013-P018)
- Performance principles (P054-P058)
- API Design principles (P049-P053)
- Git Workflow principles (P064-P072)
Focus: Process quality, optimization, API design
```

**Aggregate Results**

Use Sonnet Plan agent (intelligent analysis):
```
Task(Plan, "Analyze principle audit results", model="sonnet", prompt="""
Merge results from 3 parallel principle audits and provide intelligent analysis.

MUST reference in analysis:
- CLAUDE.md (ALL sections - development standards)
- PRINCIPLES.md (Active principles for this project)
- All category-specific principle documents loaded by agents
- All guide documents loaded by agents
- Project config (team size, maturity, deployment target, test coverage target)

Tasks:
1. Merge all category results
2. Calculate overall compliance score by category
3. Identify patterns and trends across violations
4. Prioritize issues by impact (not just severity)
5. Provide root cause analysis for common failures
6. Generate actionable, specific recommendations
7. Reference specific principles violated (e.g., "Violates P001: Fail-Fast Error Handling")
8. Reference CLAUDE.md sections for remediation guidance
9. Align recommendations with project config and context
10. Estimate effort for each recommendation

Output format:
- Overall compliance score
- Compliance by category
- Critical violations (with principle IDs and CLAUDE.md references)
- Recommendations (prioritized, with effort estimates)
- Next steps aligned with project standards

Output should be clear, prioritized, and actionable based on project documentation.
""")
```

Why Sonnet here:
- Deep pattern analysis across categories and documents
- Intelligent prioritization (impact > severity, context-aware)
- Root cause reasoning with reference to CLAUDE.md
- Context-aware recommendations aligned with project config

### Output

```
============================================================
PRINCIPLE COMPLIANCE AUDIT
============================================================

Overall Compliance: 85% (34/40 principles)

By Category:
✓ Code Quality:     9/10 (90%)
✓ Architecture:     7/8  (88%)
⚠ Security:         9/12 (75%)
✓ Operations:       6/6  (100%)
✗ Testing:          3/6  (50%)

Critical Violations:
❌ P015: Test Coverage <80% (current: 45%)
❌ P020: TTL Not Enforced (sessions never expire)
⚠  P011: Code Duplication (3 instances >50 lines)

Recommendations:
1. Increase test coverage to 80%+
2. Implement session TTL
3. Refactor duplicated code in auth module
============================================================
```

---

## Audit: All

**Run All Audits Sequentially**

**IMPORTANT**: Before running any audits, load all project context:
1. Load `@CLAUDE.md` (complete)
2. Load `@PRINCIPLES.md` (complete)
3. Load project config from registry
4. Load all relevant guide documents
5. Load all relevant principle category documents

If user selected "All", run all audit types:

1. **Code Quality Audit** - with CLAUDE.md, verification-protocol.md, code-quality.md
2. **Security Audit** - with CLAUDE.md, security-response.md, security.md
3. **Test Audit** - with CLAUDE.md, testing.md
4. **Documentation Audit** - with CLAUDE.md, code-quality.md
5. **Principles Audit** - with CLAUDE.md, PRINCIPLES.md, all category docs

Generate combined report with all findings, referencing project standards throughout.

---

## Final Report

After all selected audits complete, generate summary:

**Report must include**:
- References to violated principles (with IDs)
- References to CLAUDE.md sections for remediation
- Project config context (team size, maturity, targets)
- Alignment with project standards

```
============================================================
COMPREHENSIVE AUDIT REPORT
Project: ${PROJECT_NAME}
Date: ${DATE}
Project Standards: CLAUDE.md, PRINCIPLES.md (${PRINCIPLE_COUNT} principles)
Project Config: Team=${TEAM_SIZE}, Maturity=${MATURITY}, Target Coverage=${TEST_COVERAGE_TARGET}%
============================================================

Audits Run: [selected audits]

Summary (vs Project Standards):
✓ Code Quality:    [score] - [violations of P001-P018]
⚠ Security:        [score] - [violations of P019-P037]
✓ Tests:           [score] - Coverage: [actual]% vs [target]% (from config)
⚠ Documentation:   [score] - [violations of CLAUDE.md docs standards]
✓ Principles:      [score] - [total compliance with PRINCIPLES.md]

Critical Issues: [count] (with principle IDs and CLAUDE.md references)
Warnings: [count]
Passed: [count]

Top Violations:
❌ P015: Test Coverage - 65% < 80% target (CLAUDE.md: Test-First Development)
❌ P020: TTL Enforcement - Sessions never expire (security-response.md: Common Vulnerabilities)
⚠  P011: Code Duplication - 3 instances >50 lines (code-quality.md: DRY)

Next Steps (prioritized by impact, aligned with CLAUDE.md):
1. Fix critical security issues (Reference: security-response.md)
2. Increase test coverage to project target (Reference: CLAUDE.md Test-First)
3. Update outdated documentation (Reference: CLAUDE.md Documentation Updates)
4. Refactor code duplication (Reference: code-quality.md P011)

Use these commands to fix issues:
- /cco-fix code      # Auto-fix linting, formatting
- /cco-fix security  # Fix security vulnerabilities
- /cco-fix docs      # Update documentation
- /cco-generate tests # Generate missing tests to reach coverage target

All recommendations aligned with project standards in CLAUDE.md and PRINCIPLES.md
============================================================
```

---

## Error Handling

- If **CLAUDE.md not found**: CRITICAL - Stop audit and inform user to run `/cco-init`
- If **PRINCIPLES.md not found**: CRITICAL - Stop audit and inform user to run `/cco-init`
- If **project config not found**: WARNING - Continue with defaults, note in report
- If **category docs not found**: WARNING - Continue with PRINCIPLES.md only, note in report
- If tool not found (e.g., black not installed): Skip tool, note in report
- If audit fails: Show error, continue with other audits
- If project not initialized: Show "/cco-init" message and stop

**Priority**:
1. CLAUDE.md and PRINCIPLES.md are MANDATORY
2. Project config is RECOMMENDED
3. Category docs are OPTIONAL but HIGHLY RECOMMENDED
4. Tools are OPTIONAL (language-specific)

---

## Related Commands

- `/cco-fix code` - Auto-fix code quality issues
- `/cco-fix security` - Fix security vulnerabilities
- `/cco-generate tests` - Generate missing tests
- `/cco-fix docs` - Update documentation
