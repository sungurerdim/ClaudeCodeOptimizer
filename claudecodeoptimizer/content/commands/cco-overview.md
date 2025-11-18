# cco-overview

**Complete project health assessment with ideal scenario comparison.**

---

## Purpose

Analyze project health across all 7 industry pain points (2025 data), compare current state vs ideal, evaluate tech stack appropriateness, and provide prioritized action plan.

---

## Skills Used

All {{SKILL_COUNT}} skills (metadata only for detection - no active loading)

---

## Execution Protocol

### Step 1: Discovery

Scan project structure to detect:
- Programming languages and frameworks
- Database systems
- Testing frameworks
- CI/CD configuration
- Documentation presence
- Containerization
- Logging/monitoring setup

### Step 2: Analysis (Pain-Point Priority Order)

Analyze 8 areas based on 2025 industry pain points:

**#1 Security Posture (Pain #1: 51% top concern)**
- SQL injection risks (grep for string concatenation in queries)
- XSS vulnerabilities (template escaping)
- Hardcoded secrets (API keys, passwords)
- Input validation coverage
- Authentication/authorization implementation
- Dependency vulnerabilities
- AI security (if AI features detected)

**#2 Technical Debt (Pain #2: 23% time waste)**
- Dead code percentage (unused functions, imports)
- Complexity metrics (cyclomatic > 10, functions > 50 lines)
- Duplication (same logic in multiple places)
- TODO/FIXME comments count
- Deprecated API usage

**#3 Testing Quality (Pain #4: Biggest mistake)**
- Test coverage percentage
- Test pyramid compliance (unit >> integration >> e2e)
- Critical functions without tests
- Test isolation (shared state issues)
- Edge case coverage

**#4 Documentation (Pain #7: Knowledge gaps)**
- README completeness
- API documentation (OpenAPI/Swagger)
- Code documentation (docstring coverage)
- Documentation drift (code changed, docs didn't)
- Examples and usage guides

**#5 Database Design (Pain #5: Performance)**
- N+1 query patterns
- Missing indexes
- Unoptimized joins
- Connection pooling
- Query performance

**#6 CI/CD Maturity (Pain #6: Deployment failures)**
- Pipeline presence
- Test automation
- Quality gates (linting, security, tests)
- Deployment strategy (blue/green, canary)

**#7 Observability (Pain #5: Debugging time)**
- Logging strategy (structured logging)
- Monitoring coverage (metrics, alerts)
- Tracing (correlation IDs)
- Health check endpoints

**#8 Tech Stack Appropriateness**
- Framework suitability for project type
- Version currency (outdated = security risk)
- Better alternatives recommendation
- Missing critical components (caching, message queues)

### Step 3: Scoring

Calculate scores (0-100) for each area:
- 0-50: Critical (🔴)
- 51-75: High Priority (🟡)
- 76-90: Medium (🟢)
- 91-100: Good (✅)

### Step 4: Ideal Scenario Comparison

Define ideal scores based on project type:
- MVP/Prototype: Security 80+, Testing 60+, Docs 50+
- Production API: Security 95+, Testing 85+, Docs 90+
- Enterprise: All 90+

### Step 5: Action Plan

Generate prioritized action plan:
1. Critical security fixes (if any)
2. Test coverage improvements (if < 80%)
3. Tech debt cleanup (if high)
4. Documentation gaps (if significant)
5. Performance optimizations (if needed)

For each action:
- Estimated time to complete
- Impact on pain points
- Specific command to run
- Expected score improvement

---

## Output Format

```markdown
## Project Health Report

**Stack:** [Detected stack]
**Type:** [Detected project type]
**Overall Score:** [Average]/100 [Emoji]

### Scores by Area (Pain-Point Ordered)

[Emoji] #1 Security: [Score]/100 ([Status])
   - [Key findings]
   ➜ Fix: [Recommended command]

[Repeat for all 8 areas]

### Tech Stack Evaluation

[✅/⚠️/❌] [Framework] - [Assessment]
[Recommendations for improvements]

### Ideal Scenario (100/100)

For [Project Type]:
- Security: [Target score]
- Testing: [Target score]
- [Other targets]

### Action Plan (Prioritized by Pain-Point Impact)

**Phase 1: [Name] ([Time] - [Impact])**
[Command to run]
➜ [What it does]
➜ Impact: [Score change]
➜ Addresses Pain #[X] ([Description])

[Repeat for all phases]

**Projected Score: [Current] → [After]/100 ✅**
**Time Saved: [Hours]/week (Pain #5)**
**Risk Reduced: [Percentage]% (Pain #1)**

Start Phase 1 now? (yes/no/customize)
```

---

## Implementation Steps

1. **Use TodoWrite** to track analysis phases
2. **Use Grep** extensively for pattern detection:
   - `grep -r "execute.*%|execute.*f\"" .` for SQL injection
   - `grep -r "TODO|FIXME|HACK" .` for technical debt
   - `grep -r "import|from" tests/` for test coverage
3. **Use Read** for configuration files (package.json, pyproject.toml, etc.)
4. **Use Glob** to find files:
   - `**/*.py` for Python files
   - `**/test_*.py` or `**/*_test.py` for tests
   - `**/*.md` for documentation
5. **Analyze git history** if available:
   - Last commit date for each file (documentation drift)
   - Commit frequency (active development)
6. **Calculate metrics**:
   - Coverage: test files / source files ratio
   - Complexity: functions > 50 lines count
   - Documentation: docstring presence
7. **Generate recommendations** based on findings
8. **Present report** with pain-point focus
9. **Ask if user wants to proceed** with Phase 1

---

## Smart Detection

- **No database?** Skip database analysis
- **No tests?** Show as critical gap, recommend /cco-generate --tests
- **No CI/CD?** Recommend /cco-generate --cicd
- **No docs?** Recommend /cco-generate --docs

---

## Pain Points Reference

1. **Security (51%)** - $500M+ cost from vulnerabilities
2. **Tech Debt (23%)** - 23% developer time wasted
3. **AI Reliability (45%)** - Unreliable AI-generated code
4. **Testing (Biggest Mistake)** - Production bugs, delays
5. **Time Waste (69%)** - $2M annually per enterprise
6. **Integration (Failures)** - Deployment delays
7. **Documentation (Gaps)** - Onboarding delays

---

## Success Criteria

- [OK] All 8 areas analyzed
- [OK] Scores calculated and explained
- [OK] Tech stack evaluated with recommendations
- [OK] Action plan generated with time estimates
- [OK] Pain-point impact clearly communicated
- [OK] User presented with clear next steps
