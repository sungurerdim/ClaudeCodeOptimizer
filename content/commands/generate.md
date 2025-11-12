---
description: Generate code, tests, docs, CI/CD, and more
category: generation
cost: 5
principles: ['U001', 'U002', 'U011', 'P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010', 'P011']
---

# CCO Generate Commands

Generate tests, documentation, CI/CD pipelines, and code from specifications.

## Prerequisites: Load Required Context

```python
from pathlib import Path

print("📚 Loading CCO Context for Generation...\n")

# Load CLAUDE.md and PRINCIPLES.md
for doc_name in ["CLAUDE.md", "PRINCIPLES.md"]:
    doc_path = Path(doc_name)
    if doc_path.exists():
        tokens = len(doc_path.read_text(encoding="utf-8")) // 4
        print(f"✓ Loaded {doc_name} (~{tokens:,} tokens)")

print()
```

---

## Architecture & Model Selection

**Code Generation**: Haiku (fast, cost-effective)
- Unit test generation
- Docstring generation
- Simple code scaffolding
- Boilerplate code

**Complex Generation**: Sonnet (higher quality)
- Integration test generation
- API documentation
- CI/CD pipeline configuration
- Complex code from specs

**Execution Pattern**:
1. Use Haiku for repetitive, pattern-based generation (tests, docs)
2. Use Sonnet for complex logic and architecture decisions (CI/CD, specs)
3. Always verify generated code with existing test suite

**Implementation**:
```python
# Simple generation (Haiku)
Task("generate unit tests", model="haiku", subagent_type="Plan")
Task("generate docstrings", model="haiku", subagent_type="Plan")

# Complex generation (Sonnet)
Task("generate CI/CD pipeline", model="sonnet", subagent_type="Plan")
Task("generate code from specifications", model="sonnet", subagent_type="Plan")
```

---

## Step 1: Select What to Generate

**Use AskUserQuestion tool**:

```json
{
  "questions": [{
    "question": "What would you like to generate?",
    "header": "Generate",
    "multiSelect": true,
    "options": [
      {"label": "Tests", "description": "Generate unit tests for untested code"},
      {"label": "Integration Tests", "description": "Generate integration/E2E tests"},
      {"label": "Documentation", "description": "Generate API docs, README, docstrings"},
      {"label": "CI/CD Pipeline", "description": "Generate GitHub Actions / GitLab CI config"},
      {"label": "From Specs", "description": "Generate code from API specifications (OpenAPI, etc.)"},
      {"label": "Custom Principles", "description": "Generate project-specific development principles"}
    ]
  }]
}
```

---

## Generate: Tests

**Generate unit tests for untested code**

### Step 1: Find Untested Code

```bash
# Run coverage
pytest --cov --cov-report=term-missing

# Identify files with <80% coverage
```

### Step 2: Generate Tests

**Use Task tool with explicit model:**

**Test Generation Agent:**
```
Subagent Type: Plan
Model: sonnet
Description: Generate comprehensive tests

MUST LOAD FIRST:
1. @CLAUDE.md (Test-First Development section)
2. @~/.cco/principles/testing.md
3. Print: "✓ Loaded 2 docs (~1,900 tokens)"

Task: Generate tests for [file]

Steps:
1. Read source file and understand:
   - What the code does (business logic)
   - Input/output contracts
   - Error conditions
   - Dependencies

2. Identify test cases:
   - Public functions/methods (API surface)
   - Happy path scenarios
   - Edge cases (empty inputs, boundary values)
   - Error paths (exceptions, invalid inputs)
   - Integration points (if applicable)

3. Generate test file following project patterns:
   - Use existing test framework (pytest, jest, etc.)
   - Match naming conventions
   - Include setup/teardown if needed
   - Add descriptive docstrings
   - Group related tests in classes

4. Test categories to generate:
   - Unit tests (isolated, fast)
   - Integration tests (if function interacts with external systems)
   - Property-based tests (for complex logic)

Why Sonnet:
- Requires understanding of code logic
- Must design comprehensive test coverage
- Needs to match existing patterns
- Quality test generation needs reasoning
```

### Output

- Test files created in appropriate test directory
- Coverage improvement estimate
- Test framework used (pytest, jest, etc.)

---

## Generate: Integration Tests

**Generate integration/E2E tests**

### Step 1: Identify Integration Points

- API endpoints
- Database operations
- External service calls
- User workflows

### Step 2: Generate Tests

Use Task tool (Plan agent):

```
Task: Generate integration tests
Agent: Plan

1. Map user workflows (e.g., signup → login → action)
2. Generate tests for each workflow:
   - Setup: Create test data
   - Execute: Call real APIs
   - Verify: Check database state
   - Cleanup: Remove test data
3. Use appropriate framework (pytest, supertest, etc.)
```

### Output

- Integration test files
- Test fixtures/factories
- Database setup scripts

---

## Generate: Documentation

**Generate API docs, README, and docstrings**

### Generate API Documentation

```
Task: Generate API documentation
Agent: Plan

1. Scan for API routes/endpoints
2. Extract:
   - HTTP method, path
   - Parameters (query, body, headers)
   - Response format
   - Error codes
3. Generate OpenAPI/Swagger spec
4. Generate markdown docs
```

### Generate README

```
Task: Generate README
Agent: Plan

Sections:
1. Project name & description
2. Installation instructions
3. Usage examples
4. API reference
5. Development setup
6. Contributing guidelines
7. License
```

### Generate Docstrings

```
Task: Generate missing docstrings
Agent: Explore

For each undocumented function/class:
1. Analyze code to understand purpose
2. Generate docstring:
   - Description
   - Parameters (types, description)
   - Return value
   - Raises (exceptions)
   - Examples
3. Use language conventions (Google-style for Python, JSDoc for JS)
```

---

## Generate: CI/CD Pipeline

**Generate GitHub Actions or GitLab CI configuration**

### Detect Project Needs

- Languages used
- Test commands
- Build process
- Deployment target

### Generate Pipeline

Use Task tool (Plan agent):

```
Task: Generate CI/CD pipeline
Agent: Plan

Generate workflow with stages:
1. **Lint**: Run linters/formatters
2. **Test**: Run unit + integration tests
3. **Build**: Build application/package
4. **Security**: Run security scans
5. **Deploy**: Deploy to staging/production (optional)

Format: GitHub Actions (.github/workflows/ci.yml)
```

### Output

- `.github/workflows/ci.yml` or `.gitlab-ci.yml`
- Configured for detected languages/frameworks
- Includes caching, parallelization
- Badge URLs for README

---

## Generate: From Specs

**Generate code from API specifications**

### Supported Specs

- OpenAPI / Swagger
- GraphQL schema
- Protocol Buffers
- JSON Schema

### Generation Process

```
Task: Generate code from spec
Agent: Plan

1. Read specification file
2. Generate:
   - API client code
   - Type definitions
   - Request/response models
   - Validation logic
3. Use appropriate code generator (openapi-generator, etc.)
4. Add tests for generated code
```

### Output

- Generated client/server code
- Type definitions
- Example usage
- Tests

---

## Generate: Custom Principles

**Generate project-specific development principles**

### Process

```
Task: Generate custom principles
Agent: Plan

1. Analyze project:
   - Domain (fintech, healthcare, etc.)
   - Team size
   - Tech stack
   - Existing issues from audits
2. Generate 5-10 custom principles:
   - Based on project domain requirements
   - Address common issues found
   - Aligned with team practices
3. Format as principle definition:
   - ID, title, description
   - Applicability rules
   - Good/bad examples
   - Auto-fix availability
```

### Output

- `custom-principles.json` in project root
- Formatted for CCO principle system
- Can be imported to CCO

---

## Step 3: Review Generated Content

After generation:

```
============================================================
GENERATION SUMMARY
============================================================

Generated:
✓ Tests:            25 unit tests (+35% coverage)
✓ Integration:      8 E2E tests
✓ Documentation:    README + 50 docstrings
✓ CI/CD:            GitHub Actions pipeline
✓ Code from Specs:  API client (OpenAPI)
✓ Principles:       7 custom principles

Next Steps:
1. Review generated code
2. Run tests: pytest
3. Commit changes: git add . && git commit
4. Enable CI/CD: Push to trigger pipeline
============================================================
```

---

## Error Handling

- **No spec file found**: Ask user to provide path
- **Generation failed**: Show error, offer manual creation
- **Tests don't pass**: Mark as draft, needs manual review

---

## Related Commands

- `/cco-audit tests` - Check test coverage
- `/cco-audit docs` - Check doc completeness
- `/cco-fix` - Fix issues in generated code
