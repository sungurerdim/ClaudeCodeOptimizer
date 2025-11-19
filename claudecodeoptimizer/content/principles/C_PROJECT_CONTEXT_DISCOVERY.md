# C_PROJECT_CONTEXT_DISCOVERY: Project Context Discovery via Sub-Agent

**Severity**: High

Use Haiku sub-agent to extract project context from documentation before analysis/fix operations. This ensures work aligns with project goals, conventions, and architecture without consuming main context tokens.

---

## Why

- **Alignment**: Findings/fixes match project goals and conventions
- **Efficiency**: No wasted effort on irrelevant issues
- **Quality**: Architectural decisions respected
- **Token Optimization**: Sub-agent uses separate context, main context stays clean

---

## Documentation Files (Priority Order)

```python
PROJECT_DOC_FILES = [
    # Priority 1: Primary Documentation (Root)
    "README.md",
    "README.rst",
    "README.txt",
    "README",
    "CONTRIBUTING.md",

    # Priority 2: Project Architecture
    "ARCHITECTURE.md",
    "DESIGN.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "GOVERNANCE.md",

    # Priority 3: Community & Standards
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "AUTHORS.md",
    "CONTRIBUTORS.md",

    # Priority 4: docs/ Directory
    "docs/README.md",
    "docs/index.md",
    "docs/getting-started.md",
    "docs/architecture.md",
    "docs/design.md",

    # Priority 5: Alternative Locations
    ".github/CONTRIBUTING.md",
    ".github/SECURITY.md",
    "docs/ADR/*.md",  # Architecture Decision Records
    "doc/README.md",
    "wiki/Home.md"
]

# NOT included: CLAUDE.md (already in main context)
```

---

## User Prompt

Ask user before running analysis:

```python
{
    question: "Proje dokümantasyonundan context çıkarılsın mı?",
    header: "Project Context",
    multiSelect: false,
    options: [
        {
            label: "Evet (önerilen)",
            description: "README/CONTRIBUTING'den proje amacı ve konvansiyonları çıkar, analizler hedefe uygun olur"
        },
        {
            label: "Hayır",
            description: "Sadece kod analizi yap (daha hızlı, dokümantasyondan bağımsız)"
        }
    ]
}
```

---

## Sub-Agent Implementation

### Phase 0: Project Context Discovery

```python
# Only if user selected "Evet"
if user_wants_context:
    context_result = Task({
        subagent_type: "Explore",
        model: "haiku",
        prompt: """
        Extract project context summary (MAX 200 tokens).

        Search for and read these files in priority order (stop after finding 3-4 relevant ones):
        - README.md, README.rst, README.txt, README
        - CONTRIBUTING.md, .github/CONTRIBUTING.md
        - ARCHITECTURE.md, DESIGN.md, docs/architecture.md
        - docs/ADR/*.md (Architecture Decision Records)
        - ROADMAP.md, CHANGELOG.md

        Return structured summary:

        ## Project Context

        **Purpose**: {1-2 sentences describing what the project does}

        **Goals**:
        - {Primary goal}
        - {Secondary goal}
        - {Tertiary goal if exists}

        **Tech Stack**: {languages, frameworks, databases}

        **Conventions**:
        - Naming: {snake_case/camelCase/PascalCase}
        - Testing: {pytest/jest/unittest/etc}
        - Formatting: {black/prettier/etc}
        - Linting: {ruff/eslint/etc}

        **Architecture Notes**:
        - {Key architectural decision 1}
        - {Key architectural decision 2}

        If a file doesn't exist, skip that section.
        If no documentation found, return: "No project documentation found."
        """
    })
```

### Using Context in Analysis

```python
# Pass context to analysis agents
if context_result and context_result != "No project documentation found.":
    analysis_prompt = f"""
    {context_result}

    ---

    Analyze the codebase with the above project context in mind.
    Ensure findings align with project goals and conventions.
    Filter out issues that contradict architectural decisions.
    """
```

---

## When to Use

| Command | Context Benefit | Recommendation |
|---------|-----------------|----------------|
| **audit** | Align findings with project goals | Optional (recommended) |
| **fix** | Match fixes to project conventions | Optional (recommended) |
| **generate** | Follow project style in generated code | Optional (recommended) |
| **implement** | Respect architectural decisions | Optional (recommended) |

---

## Cost/Benefit Analysis

| Metric | Without Context | With Context |
|--------|-----------------|--------------|
| Main context tokens | 0 | 0 (sub-agent separate) |
| Sub-agent cost | $0 | ~$0.02-0.05 |
| Latency | 0 | ~10-15 seconds |
| Relevance of findings | Medium | High |
| Convention compliance | Low | High |

**Trade-off**: Small cost/latency increase for significantly better alignment.

---

## Self-Enforcement

This principle applies to:
1. **CCO commands** - audit, fix, generate, implement must offer context discovery
2. **Runtime execution** - Sub-agent extracts fresh context each run
3. **Generated outputs** - All results respect discovered conventions

### Verification

```python
# Commands must include context question
def verify_context_question(command_content):
    required_patterns = [
        r"Project Context",
        r"dokümantasyon.*context",
        r"Evet.*önerilen",
    ]
    for pattern in required_patterns:
        if not re.search(pattern, command_content, re.IGNORECASE):
            raise ValueError(f"Missing context discovery question: {pattern}")
```

---

## Checklist

- [ ] User asked about context discovery (not forced)
- [ ] "Evet (önerilen)" label guides user
- [ ] Haiku model used for cost efficiency
- [ ] MAX 200 token summary enforced
- [ ] Priority order followed for file discovery
- [ ] CLAUDE.md excluded (already in context)
- [ ] Context passed to analysis agents when available
- [ ] "No documentation found" handled gracefully
