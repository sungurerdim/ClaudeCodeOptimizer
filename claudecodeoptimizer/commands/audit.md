---
description: Comprehensive audit (code, security, tests, docs, principles, all)
category: audit
cost: 3
---

# CCO Audit Commands

Run comprehensive audits on your codebase: code quality, security, tests, documentation, and principle compliance.

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

**Runtime tool detection** - automatically detect and run available tools.

### Detect Available Tools

- **Python**: black, ruff, mypy, pylint, flake8, pytest
- **JavaScript/TypeScript**: prettier, eslint, tslint, tsc, jest, vitest
- **Go**: gofmt, goimports, golint, staticcheck, go test
- **Rust**: rustfmt, clippy, cargo test
- **Other**: Language-specific formatters, linters, type checkers

### Run Checks

Use Task tool (Explore agent, medium thoroughness):

```bash
# Python example
black --check .
ruff check .
mypy .

# Report results
```

### Output

- Formatting issues found
- Lint violations
- Type errors
- Recommendations for fixes

**Next Step**: Use `/cco-fix code` to auto-fix issues.

---

## Audit: Security

**7 Critical Security & Privacy Principles**

Audit against:
- P019: Privacy-First Design
- P020: TTL Enforcement
- P021: Zero-Disk Policy
- P022: Defense-in-Depth
- P024: Secure Configuration
- P025: Key Derivation
- P026: Secret Scanning

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

Checks:
- P019: Privacy-First Design
- P021: Zero-Disk Policy
- P026: Secret Scanning
- Scan for unencrypted sensitive data
- Detect hardcoded secrets (API keys, passwords, tokens)
- Check .env, config files
- Verify .gitignore for secrets
```

**Agent 2: Security Architecture** (Haiku, quick):
```
Task(Explore, "Audit security architecture and config", model="haiku", thoroughness="quick")

Checks:
- P020: TTL Enforcement
- P022: Defense-in-Depth
- P024: Secure Configuration
- P025: Key Derivation
- Validate security headers
- Check HTTPS enforcement
- Verify data expiration
- Check input validation
```

### Aggregation

Use Sonnet Plan agent for intelligent risk assessment:
```
Task(Plan, "Analyze security audit findings", model="sonnet", prompt="""
Analyze security findings from 2 parallel security audits.

Tasks:
1. Merge all security findings
2. Assess actual risk level (not just theoretical)
3. Identify attack vectors and exploit scenarios
4. Prioritize by: exploitability × impact
5. Provide specific remediation steps
6. Estimate security debt and fix effort
7. Recommend immediate actions vs long-term hardening

Focus on practical, actionable security improvements.
""")
```

Why Sonnet here:
- Risk assessment requires reasoning (not just data)
- Attack vector analysis needs intelligence
- Prioritization by real-world exploitability
- Context-aware remediation recommendations

---

## Audit: Tests

**Test Coverage & Quality Analysis**

### Metrics

1. **Coverage**: Line, branch, function coverage
2. **Quality**: Assertion quality, test isolation
3. **Flaky Tests**: Detect non-deterministic tests
4. **Speed**: Identify slow tests

### Run Analysis

```bash
# Python
pytest --cov --cov-report=term-missing
pytest --durations=10

# JavaScript
jest --coverage
npm test -- --verbose
```

### Output

- Coverage percentage (target: >80%)
- Uncovered files/lines
- Flaky test detection
- Slow tests (>5s)

**Next Step**: Use `/cco-generate tests` for missing coverage.

---

## Audit: Documentation

**Documentation Completeness & Accuracy**

### Check

1. **API Docs**: All public APIs documented
2. **README**: Up-to-date setup instructions
3. **Inline Comments**: Complex logic explained
4. **Sync**: Docs match actual code behavior
5. **Examples**: Working code examples

### Run Audit

Use Task tool (Explore agent):

```
1. Check README exists and is current
2. Verify API documentation coverage
3. Scan for outdated docs (deprecated APIs, old examples)
4. Check docstring coverage (Python) or JSDoc (JS)
```

### Output

- Missing documentation
- Outdated documentation
- Documentation quality score

**Next Step**: Use `/cco-fix docs` to update documentation.

---

## Audit: Principles

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
- Code Quality principles
- Architecture principles
- Focus: Static code analysis

**Agent 2 - Security & Operations** (Haiku, quick):
- Security & Privacy principles
- Operational Excellence principles
- Focus: Runtime & config analysis

**Agent 3 - Process & Performance** (Haiku, quick):
- Testing principles
- Git Workflow principles
- Performance principles
- API Design principles
- Focus: Process & optimization

Each agent:
```
Task(Explore, "Audit {categories} principles", model="haiku", thoroughness="quick")
```

**Aggregate Results**

Use Sonnet Plan agent (intelligent analysis):
```
Task(Plan, "Analyze principle audit results", model="sonnet", prompt="""
Merge results from 3 parallel audits and provide intelligent analysis.

Tasks:
1. Merge all category results
2. Calculate overall compliance score
3. Identify patterns and trends across violations
4. Prioritize issues by impact (not just severity)
5. Provide root cause analysis for common failures
6. Generate actionable, specific recommendations
7. Estimate effort for each recommendation

Output should be clear, prioritized, and actionable.
""")
```

Why Sonnet here:
- Deep pattern analysis across categories
- Intelligent prioritization (impact > severity)
- Root cause reasoning
- Context-aware recommendations

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

If user selected "All", run all audit types:

1. Code Quality Audit
2. Security Audit
3. Test Audit
4. Documentation Audit
5. Principles Audit

Generate combined report with all findings.

---

## Final Report

After all selected audits complete, generate summary:

```
============================================================
COMPREHENSIVE AUDIT REPORT
Project: ${PROJECT_NAME}
Date: ${DATE}
============================================================

Audits Run: [selected audits]

Summary:
✓ Code Quality:    [score]
⚠ Security:        [score]
✓ Tests:           [score]
⚠ Documentation:   [score]
✓ Principles:      [score]

Critical Issues: [count]
Warnings: [count]
Passed: [count]

Next Steps:
1. Fix critical security issues
2. Increase test coverage
3. Update outdated documentation
4. Refactor code duplication

Use these commands to fix issues:
- /cco-fix code
- /cco-fix security
- /cco-fix docs
- /cco-generate tests
============================================================
```

---

## Error Handling

- If tool not found (e.g., black not installed), skip and note in report
- If audit fails, show error and continue with other audits
- If project not initialized, show "/cco-init" message

---

## Related Commands

- `/cco-fix code` - Auto-fix code quality issues
- `/cco-fix security` - Fix security vulnerabilities
- `/cco-generate tests` - Generate missing tests
- `/cco-fix docs` - Update documentation
