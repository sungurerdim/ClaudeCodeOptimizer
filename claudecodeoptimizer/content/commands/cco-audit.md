---
name: cco-audit
description: Comprehensive codebase audit with full transparency and real-time progress
action_type: audit
parameters:
  security:
    keywords: [security audit, owasp scan, xss check, sqli scan, csrf check, secrets scan, vulnerability scan]
    category: security
    pain_points: [1]
  tech-debt:
    keywords: [tech debt audit, dead code scan, complexity check, duplication scan]
    category: quality
    pain_points: [2]
  ai-security:
    keywords: [ai security audit, prompt injection scan, llm security, ai vulnerability]
    category: security
    pain_points: [3]
  tests:
    keywords: [test audit, coverage check, test quality, test isolation, test pyramid]
    category: testing
    pain_points: [4]
  integration:
    keywords: [integration audit, dependency check, import scan, conflict detection]
    category: infrastructure
    pain_points: [6]
  code-quality:
    keywords: [code quality audit, syntax check, type check, error handling scan]
    category: quality
    pain_points: [2]
  docs:
    keywords: [documentation audit, docstring check, api docs scan, readme check]
    category: docs
    pain_points: [7]
  database:
    keywords: [database audit, n+1 scan, index check, query optimization, db performance]
    category: database
    pain_points: [5]
  observability:
    keywords: [observability audit, logging check, metrics scan, tracing check]
    category: observability
    pain_points: [5]
  monitoring:
    keywords: [monitoring audit, dashboard check, alert scan, prometheus check]
    category: observability
    pain_points: [5]
  cicd:
    keywords: [cicd audit, pipeline check, quality gates scan, deployment audit]
    category: infrastructure
    pain_points: [6]
  containers:
    keywords: [container audit, dockerfile scan, k8s check, container security]
    category: infrastructure
    pain_points: [6]
  supply-chain:
    keywords: [supply chain audit, dependency scan, cve check, sbom scan, license check]
    category: security
    pain_points: [1]
  migrations:
    keywords: [migration audit, schema check, rollback scan, data migration check]
    category: database
    pain_points: [5]
  performance:
    keywords: [performance audit, caching check, bundle scan, response time check]
    category: performance
    pain_points: [5]
  architecture:
    keywords: [architecture audit, coupling check, pattern scan, design review]
    category: architecture
    pain_points: [5]
  git:
    keywords: [git audit, commit quality, branching check, pr process scan]
    category: infrastructure
    pain_points: [5]
  ai-quality:
    keywords: [ai quality audit, ai hallucination scan, api hallucination check, code bloat scan, vibe coding check, copilot quality]
    category: quality
    pain_points: [3, 8, 9]
  ai-debt:
    keywords: [ai debt audit, ai generated debt, ai code quality, ai technical debt]
    category: quality
    pain_points: [2, 3]
  code-review:
    keywords: [code review audit, pr quality check, review quality scan, commit quality check, dora metrics]
    category: quality
    pain_points: [11, 12]
  platform:
    keywords: [platform audit, cicd maturity, test automation check, iac scan, dx audit, ai readiness]
    category: infrastructure
    pain_points: [4, 6, 10]
  ai:
    keywords: [ai audit, complete ai scan, ai security and quality, ai comprehensive check]
    category: meta
    pain_points: [2, 3, 8, 9]
    meta_flags: [ai-quality, ai-debt, ai-security]
  critical:
    keywords: [critical audit, essential checks, must-fix, high priority scan]
    category: meta
    pain_points: [1, 3, 4, 5]
    meta_flags: [security, ai-security, database, tests]
  production-ready:
    keywords: [production ready audit, deploy readiness, pre-deploy check, production checklist]
    category: meta
    pain_points: [1, 4, 5, 7]
    meta_flags: [security, performance, database, tests, docs]
  code-health:
    keywords: [code health audit, quality focus, maintainability check, code cleanliness]
    category: meta
    pain_points: [2, 4, 7]
    meta_flags: [tech-debt, code-quality, tests, docs]
  team-metrics:
    keywords: [team metrics audit, collaboration check, platform maturity, team performance]
    category: meta
    pain_points: [6, 10, 11, 12]
    meta_flags: [code-review, platform, cicd]
---

# CCO Audit Command

**Comprehensive codebase analysis with full transparency, flexible selection, and real-time progress.**
---

## Built-in References

**This command inherits standard behaviors from:**

- **[cco-standards.md](../cco-standards.md)** - Standard structure, execution protocol, file discovery
- **[cco-standards.md](../cco-standards.md)** - UX/DX, efficiency, simplicity, performance standards
- **[cco-patterns.md](../cco-patterns.md)** - Reusable patterns (Step 0, Selection, Accounting, Progress, Error Handling)
- **[cco-standards.md](../cco-standards.md)** - File discovery, model selection, parallel execution
- **model selection** - Haiku for mechanical tasks, let Claude Code decide for complex tasks
- **[cco-tech-detection.md](../cco-tech-detection.md)** - Fast tech detection (<2s), applicability filtering, pre-filtering UI

**See these files for detailed patterns. Only command-specific content is documented below.**

---

## Execution Guarantee

**This command WILL execute fully without requiring user presence during processing.**

**What Happens:**
1. **Step 0**: Introduction and mode selection (user input required)
2. **Step 0.5**: Project context discovery (optional, user choice)
3. **Discovery**: Tech detection and check applicability (automated)
4. **Selection**: Check selection based on mode (automated or user input)
5. **Pre-Flight**: Summary and confirmation (user input required)
6. **Execution**: Run selected checks with real-time progress (fully automated)
7. **Final Report**: Prioritized findings with action plan (automated)

**User Interaction Points:**
- Mode selection (Quick/Category/Full Control)
- Project context discovery (optional)
- Check selection (if Category/Full Control modes)
- Pre-flight confirmation
- Agent error handling (if failures occur)

**Automation:**
- All checks run without interruption
- Streaming results displayed in real-time
- Complete accounting enforced (total issues = reported + verified)
- Agents handle audit execution in parallel

**Time Estimate:**
- Quick Mode: 3-8 minutes
- Category Mode: 5-15 minutes
- Full Control: 10-30 minutes (depends on checks selected)

**Verification:**
- All findings verified (no false positives)
- File-level accounting enforced
- Complete transparency into execution progress

---

## Design Principles

**See:** cco-standards.md
- UX/DX principles (transparency, progressive disclosure, zero surprises)
- Honesty & accurate reporting (no false positives/negatives)
- No hardcoded examples (use placeholders: `{FILE_PATH}`, `{LINE_NUMBER}`)

---

## Execution Flow

```
/cco-audit
    │
    ├─► Step 0: Introduction & Confirmation
    │
    ├─► Mode Selection (Quick/Standard/Full)
    │
    ├─► Project Context (optional, recommended)
    │
    ├─► Discovery Phase (tech detection, applicability, file filtering)
    │
    ├─► Selection (based on mode)
    │
    ├─► Pre-Flight Summary (confirm before run)
    │
    ├─► Execution Dashboard (real-time progress)
    │
    ├─► Streaming Results (findings as discovered)
    │
    └─► Final Report (prioritized, actionable, concise)
```

---


## Step 0: Introduction and Confirmation

**Pattern:** Pattern 1 (Step 0 Introduction)

**Command-Specific Details:**

**Audit Categories:** Security, Quality, Testing, Performance, Infrastructure

**What You'll Be Asked:** Mode selection → Context discovery (optional) → Check selection → Pre-flight

**Time:** Quick 3-8min | Category 5-15min | Full 10-30min

**Output:** Prioritized findings + Action plan (Immediate/Short-term/Long-term)

```python
AskUserQuestion({
  questions: [{
    question: "Ready to start codebase audit?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {label: "Start Audit", description: "Proceed with comprehensive analysis"},
      {label: "Cancel", description: "Exit cco-audit"}
    ]
  }]
})
```

**If Cancel:** Exit with "cco-audit cancelled."
**If Start:** Continue to Mode Selection.

---

## Component 1: Mode Selection

**Always start here. Let user choose control level.**

```python
AskUserQuestion({
  questions: [{
    question: "What level of control do you need?",
    header: "Audit Mode",
    multiSelect: false,
    options: [
      {
        label: "Quick Mode",
        description: "Fast health assessment with scores, ideal comparison, and action plan (~5 min)"
      },
      {
        label: "Quick Presets",
        description: "Use-case based (Pre-commit, Security, etc.) - Fastest start"
      },
      {
        label: "Category Mode",
        description: "Select from 9 category groups - Balanced control"
      },
      {
        label: "Full Control",
        description: "See all {TOTAL_CHECKS} checks, select individually - Maximum control"
      }
    ]
  }]
})
```

### Quick Mode

**When user selects "Quick Mode" or uses `--quick` flag, execute fast health assessment:**

```python
# Quick mode bypasses detailed check selection
# Instead, performs rapid analysis across all 8 areas

def quick_assessment():
    """
    Fast project health assessment with:
    - Score calculation (0-100) for each area
    - Ideal scenario comparison
    - Prioritized action plan
    """

    # Analyze 8 areas (pain-point priority order)
    areas = [
        ("Security", analyze_security_quick),      # Pain #1
        ("Tech Debt", analyze_tech_debt_quick),    # Pain #2
        ("Testing", analyze_testing_quick),        # Pain #4
        ("Documentation", analyze_docs_quick),     # Pain #7
        ("Database", analyze_database_quick),      # Pain #5
        ("CI/CD", analyze_cicd_quick),            # Pain #6
        ("Observability", analyze_observability_quick),  # Pain #5
        ("Tech Stack", analyze_stack_appropriateness),   # Fitness
    ]

    scores = {}
    for area, analyzer in areas:
        scores[area] = analyzer()  # Returns 0-100 score

    # Generate report
    return generate_quick_report(scores)
```

**Quick Mode Output Format:**

```markdown
## Project Health Report

**Stack:** {Detected stack}
**Type:** {Detected project type}
**Overall Score:** {Average}/100 {Emoji}

### Strategic Recommendations

**Platform Maturity:** {Score}/100 {Emoji}
- CI/CD: {Status} ({Details})
- Test Automation: {Coverage}%
- IaC Presence: {Yes/No/Partial}
- Deployment Frequency: {X}/week
➜ Improvement: /cco-audit --platform

**AI Readiness:** {Low/Medium/High} {Emoji}
- Foundation Quality: {Score}/100
- Test Coverage: {Percentage}%
- Platform Stability: {DORA Tier}
- Recommendation: {Action}
➜ {If Low: "Strengthen foundation before AI adoption"}
➜ {If Medium: "Ready for limited AI use with oversight"}
➜ {If High: "AI will amplify your strong foundation"}

**DORA Metrics Overview:**
1. Deployment Frequency: {X}/week ({Elite/High/Medium/Low})
2. Lead Time for Changes: {Hours/Days} ({Tier})
3. MTTR: {Minutes/Hours} ({Tier})
4. Change Failure Rate: {Percentage}% ({Tier})
5. Rework Rate (2025): {Percentage}% ({Tier})
➜ Overall DORA Tier: {Elite/High/Medium/Low}
➜ Deep Dive: /cco-audit --platform

### Scores by Area (Pain-Point Ordered)

{Emoji} #1 AI Quality Crisis: {Score}/100 ({Status})
   - {Key findings}
   ➜ Fix: /cco-audit --ai-quality

{Emoji} #2 AI Tech Debt: {Score}/100 ({Status})
   - {Key findings}
   ➜ Fix: /cco-audit --ai-debt

{Emoji} #3 Security: {Score}/100 ({Status})
   - {Key findings}
   ➜ Fix: /cco-audit --security

[Repeat for all 12 pain points]

### Tech Stack Evaluation

{✅/⚠️/❌} {Framework} - {Assessment}
{Recommendations for improvements}

**AI Code Detection:**
- Estimated AI-generated code: {Percentage}%
- AI signatures found: {ChatGPT/Copilot/Claude patterns}
- Quality score: {AI_Quality_Score}/100
➜ Detailed analysis: /cco-audit --ai

### Ideal Scenario Comparison

For {Project Type}:
- Security: {Current} vs {Target}
- Testing: {Current} vs {Target}
- [Other comparisons]

### Action Plan (Prioritized by Pain-Point Impact)

**Phase 1: {Name} ({Time} - {Impact})**
Command: /cco-audit --{category}
➜ {What it does}
➜ Impact: {Score change}
➜ Addresses Pain #{X}

[Repeat for all phases]

**Projected Score: {Current} → {After}/100 ✅**
```

**After displaying Quick Mode report, ask user:**

```python
AskUserQuestion({
  questions: [{
    question: "Start Phase 1 implementation now?",
    header: "Next Step",
    multiSelect: false,
    options: [
      {
        label: "Start Phase 1",
        description: "Begin implementing highest impact fixes"
      },
      {
        label: "Customize Plan",
        description: "Modify phases or priorities"
      },
      {
        label: "Exit",
        description: "Review report only, no implementation"
      }
    ]
  }]
})
```

**Then proceed to Discovery Phase (same for all modes).**

---

## Component 1.5: Project Context Discovery (Optional)

**Pattern:** Pattern 9 (Context Passing)

**Audit-Specific Usage:**
- Extracted context passed to audit agents for alignment
- Findings filtered based on project architectural decisions
- Recommendations respect discovered conventions

---

## Component 1.6: Tech Stack Detection & Applicability Filtering

**Pattern:** Pattern 10 (Tech Stack Detection & Context Sharing)

**Purpose:** Eliminate irrelevant checks, show only applicable options to user

**Implementation:**

```markdown
### Tech Stack Detection (1-2 seconds)

Detecting project technology stack...

✓ Languages: {DETECTED_LANGUAGES}
✓ Frameworks: {DETECTED_FRAMEWORKS}
✓ DevOps: {DETECTED_DEVOPS}
✓ Testing: {DETECTED_TESTING}
✓ Database: {DETECTED_DATABASE}
✓ Frontend: {DETECTED_FRONTEND}

════════════════════════════════════════════════════════════════
TECH STACK DETECTED (session cache for subsequent commands):

Languages: {DETECTED_LANGUAGES}
Frameworks: {DETECTED_FRAMEWORKS}
Databases: {DETECTED_DATABASES}
DevOps: {DETECTED_DEVOPS}
Frontend: {DETECTED_FRONTEND}
Testing: {DETECTED_TESTING}

Detection time: {DURATION}s
════════════════════════════════════════════════════════════════
```

**Applicability Filtering:**

```python
# Filter checks based on detected tech stack
applicable_checks, filtered_checks = filter_applicable_checks(
    all_checks=ALL_CHECKS,
    tech_stack=detected_tech_stack
)

# Report filtering results
print(f"""
Available checks: {len(applicable_checks)}
Filtered: {len(filtered_checks)} checks not applicable to your project

ℹ️  Filtered categories:
  - {FILTERED_CATEGORY_1} ({REASON_1})
  - {FILTERED_CATEGORY_2} ({REASON_2})
  - {FILTERED_CATEGORY_3} ({REASON_3})

Use --show-all to see filtered checks
""")
```

**User Options After Filtering:**

- See only **applicable checks** (default, recommended)
- Show **all checks** including filtered (--show-all flag)

---

## Component 2: Discovery Phase

**See:** cco-standards.md & cco-patterns.md

**Audit-Specific Discovery:**
1. **File Discovery**: Apply exclusions FIRST, report included/excluded counts
2. **Tech Stack Detection**: Use Glob+Read on filtered files (languages, frameworks, databases, DevOps, testing)
3. **Calculate Applicability**: Filter checks by detected tech stack
4. **Display Summary**: Tech stack, applicable checks count, file scan count

---

## Component 3: Full Checklist

**Only shown in Full Control Mode. Complete list of all available checks.**

### Check Categories

```markdown
## All Available Checks ({TOTAL_CHECKS} total)

### 🔴 CRITICAL IMPACT

#### Security (15 checks)
| Check | Slug | Status |
|-------|------|--------|
| SQL Injection, XSS, CSRF, Secrets, Auth Bypass, Authz Flaws | sec-* | Applicable |
| CVE Scan, SSRF, XXE, Path Traversal, Command Injection | sec-* | Applicable |
| Insecure Deserial, Weak Crypto, Security Headers | sec-* | Applicable |

**[See full checklist: /cco-status --checks]**

Full coverage of 92 critical checks across 9 categories:
- **Security** (15): OWASP Top 10, secrets, CVEs
- **Database** (10): N+1, indexes, optimization
- **Tests** (12): Coverage, isolation, pyramid
- **Code Quality** (15): Complexity, duplication, smells
- **Performance** (10): Slow ops, caching, algorithms
- **CI/CD** (8): Pipeline, gates, deploy
- **Documentation** (8): Docstrings, ADRs, examples
- **Containers** (6): Dockerfile, security, optimization
- **Tech Debt** (8): Deprecated, coupling, refactoring

---

## Component 4: Selection Input

**Pattern:** Pattern 2 (Multi-Select with "All")

**Audit-Specific Selection Modes:**

1. **Quick Presets**: Single-select from presets (Pre-Commit, Security Scan, Pre-Deploy, Full Weekly)
   - Full preset list: `/cco-status --presets` or see frontmatter metadata

2. **Category Mode**: Multi-select by impact level (Critical/High/Medium categories)
   - Groups: 🔴 Critical (Security, Database, Tests), 🟡 High (Quality, Performance, CI/CD), 🟢 Medium (Docs, Containers, Debt)
   - Each group has "All [Group]" option

3. **Full Control**: Two-step selection (categories → individual checks within each)
   - Step 1: Select categories (with "All Categories" option)
   - Step 2: For each category, select specific checks (with "All [Category]" option)

**CLI Syntax (Power Users):**
```bash
/cco-audit --checks="1,2,4,16-25"     # Specific checks
/cco-audit --security --database       # Categories
/cco-audit --all --exclude="3,8,10"    # All except excluded
```

**Selection Parser:** Supports ranges (1-15), categories, presets (@pre-commit), keywords (all, critical), exclusions (-3)

---


---

## Component 5: Pre-Flight Summary

**Show EXACTLY what will happen before execution. No surprises.**

**Display Structure:**
1. **Selection Overview**: Selected checks by category, check numbers, estimated time per category, total time
2. **What's NOT Running**: Not applicable (with reasons), manually excluded, other categories
3. **Execution Plan**: 3 phases (Setup ~30s, Scanning ~X min parallel, Synthesis ~2 min)
4. **Confirmation**: AskUserQuestion with options (Start Audit, Modify Selection, Cancel)

---

## Component 6: State Management & Count Tracking

**Pattern:** Pattern 4 (Complete Accounting)

**Audit-Specific State:**
- Central `AuditState` object maintains: phase, total_findings, severity counts
- Single source for all counts (never derive, always update)
- Use `get_counts_string()` for consistent display formatting

---

## Component 7: Execution Dashboard

**Pattern:** Pattern 3 (Progress Reporting)

**Audit-Specific Phases:**
1. **Setup** (12s): Load skills, discover files, initialize scanners
2. **Scanning** (8-15min): Run checks with real-time progress, streaming findings
3. **Synthesis** (45s): Aggregate findings, calculate scores, generate report

---

## Component 7.5: Agent Execution Strategy

**See:** cco-standards.md & cco-patterns.md
- Model selection (Haiku for patterns, Sonnet for analysis)
- Parallel execution patterns (fan-out for independent categories)
- Error handling with user recovery options (Pattern 5)
- Agent task execution with verification (Pattern 6)

**Audit-Specific Behavior:**
- Independent category checks run in parallel (e.g., `--security --tests --database` → 3 parallel agents)
- Automatic model selection per check type (no configuration needed)

---

## Component 8: Count Consistency Rules

**Pattern:** Pattern 4 (Complete Accounting)

**Audit-Specific Application:**
- All finding counts use single source (state object)
- Any filtering explicitly explained to user
- Formula verified: total = completed + skipped + failed + cannot_do

---

## Component 9: Honesty & Accurate Reporting

**See:** cco-standards.md

**Audit-Specific Application:**
- All findings verified (no false positives/negatives)
- Accurate outcome categorization (fixed/needs_decision/impossible_external)
- Verification required before claiming "fixed"
- Clear distinction between difficulty and impossibility

---

## Component 7: Final Report

**Concise, actionable findings with clear next steps.**

```markdown
═══════════════════════════════════════════════════════════════
                    AUDIT REPORT
═══════════════════════════════════════════════════════════════

## Executive Summary

**Total Findings:** {total_findings}
- Critical: {critical_count}
- High: {high_count}
- Medium: {medium_count}
- Low: {low_count}

**Accounting Verification:** {total_findings} = {critical_count} + {high_count} + {medium_count} + {low_count} ✓

## Findings by Category

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Security | {count} | {count} | {count} | {count} | {total} |
| Database | {count} | {count} | {count} | {count} | {total} |
| Tests | {count} | {count} | {count} | {count} | {total} |

## Top Priority Fixes

### Critical Issues ({critical_count})

{for finding in critical_findings[:10]}
**{finding.category}**: {finding.issue}
- **File**: {finding.file}:{finding.line}
- **Fix**: {finding.recommendation}
{endfor}

{if critical_count > 10}
... and {critical_count - 10} more critical issues (see full report)
{endif}

## Action Plan

### Immediate (Today)
1. Fix {quick_fix_count} critical issues (estimated 1-2 hours)
2. Review {high_priority_count} high-priority security findings

### Short-term (This Week)
1. Address remaining high-priority issues
2. Improve test coverage to {target_coverage}%

### Long-term (Next Month)
1. Refactor {complexity_count} high-complexity modules
2. Implement monitoring for {observability_gaps} areas

═══════════════════════════════════════════════════════════════
```

---
## CLI Usage

**Interactive (Default):** `/cco-audit` - Full UI-guided workflow
**Quick Mode:** `/cco-audit --quick` - Health assessment (~5 min)

**Parametrized (Power Users):**
- **Presets**: `--preset=pre-commit|security|pre-deploy|weekly`
- **Categories**: `--security`, `--security --database --tests`, `--all`
- **Specific**: `--checks="1,2,4,16-25"` or `--checks="sql-injection,n1-queries"`
- **Exclusions**: `--all --exclude="3,8,10"`
- **Context**: `/cco-audit --security "Focus on auth endpoints"` - Optional prompt for focused analysis

---

## Error Handling

**Pattern:** Pattern 5 (Error Handling)

**Audit-Specific Error Types:**
1. **CLI Parameter Errors**: Invalid check numbers, unknown slugs, invalid ranges (CLI only, interactive validates automatically)
2. **Empty Selection**: User options - Select Different Checks, Run All Applicable, Cancel
3. **Long Execution Warning**: User options - Continue, Smaller Selection, Cancel (triggers for >60 min estimates)
4. **Agent Execution Failure**: User options - Retry, Retry with different model, Manual audit, Skip category, Cancel

---

## Success Criteria

- [ ] Mode selection → Discovery → Selection → Pre-flight → Confirmation → Execution → Final report
- [ ] Real-time progress with streaming findings
- [ ] Complete accounting enforced (total issues = reported + verified)
- [ ] Next action commands provided with context

---

## Next Steps: Calling Other Commands (C_COMMAND_CONTEXT_PASSING)

### If Issues Found: Calling /cco-fix or /cco-generate

When audit finds fixable issues or missing components:

**ALWAYS provide context before calling another command:**

#### Calling /cco-fix

```markdown
CONTEXT FOR /cco-fix:
Audit found {COUNT} {SEVERITY} issues across {CATEGORY_COUNT} categories:
- {CATEGORY_1}: {COUNT}x {ISSUE_TYPE} ({FILE_PATHS})
- {CATEGORY_2}: {COUNT}x {ISSUE_TYPE} ({FILE_PATHS})
All issues are {FIXABILITY} with {APPROACH}.

[Then immediately call SlashCommand]
```

**Example:**

```markdown
CONTEXT FOR /cco-fix:
Audit found {COUNT} critical security issues: {COUNT}x SQL injection ({FILE_PATH}:{LINE_NUMBER}), {COUNT}x XSS ({FILE_PATH}:{LINE_NUMBER}), {COUNT}x hardcoded secrets ({FILE_PATH}:{LINE_NUMBER}). All are safe-fixable with parameterized queries, HTML escaping, and environment variables.

SlashCommand({command: "/cco-fix security"})
```

#### Calling /cco-generate

```markdown
CONTEXT FOR /cco-generate:
Audit found {COUNT} missing components:
- {COMPONENT_TYPE}: {COUNT} {ITEMS} ({DETAILS})
- Pattern: {EXISTING_PATTERN_REFERENCE}
- Expected: {EXPECTED_STRUCTURE}

[Then immediately call SlashCommand]
```

**Example:**

```markdown
CONTEXT FOR /cco-generate:
Audit found {COUNT} critical files with zero test coverage: {FILE_PATH_1} (0%), {FILE_PATH_2} (0%), {FILE_PATH_3} (0%), +{REMAINING_COUNT} others. Existing test pattern in {TEST_FILE_PATH} uses {TESTING_FRAMEWORK} with {TEST_PATTERN}. Generate comprehensive test suites for these {COUNT} files following project conventions.

SlashCommand({command: "/cco-generate tests"})
```

**Why This Matters:**
- Called command receives specific issue list, file paths, line numbers
- No duplicate scanning/analysis
- Faster execution
- Consistent findings across commands

**DON'T:**
```markdown
# ❌ BAD: No context
Found some security issues.
SlashCommand({command: "/cco-fix"})
```
