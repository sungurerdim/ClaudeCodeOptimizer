---
description: Generate code, tests, docs, CI/CD, and more
category: generation
cost: 3
---

# CCO Generate Commands

Generate tests, documentation, CI/CD pipelines, and code from specifications.

**Architecture:** Hybrid Haiku/Sonnet approach for optimal speed + quality
- **Haiku**: Simple generation (tests, docs) - fast data transformation
- **Sonnet**: Complex generation (CI/CD, specs) - reasoning required

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
      {"label": "Tests", "description": "Generate unit tests for untested code (Haiku - fast)"},
      {"label": "Integration Tests", "description": "Generate integration/E2E tests (Sonnet - requires workflow reasoning)"},
      {"label": "Documentation", "description": "Generate API docs, README, docstrings (Haiku - fast)"},
      {"label": "CI/CD Pipeline", "description": "Generate GitHub Actions / GitLab CI config (Sonnet - requires architecture reasoning)"},
      {"label": "From Specs", "description": "Generate code from API specifications (Sonnet - complex)"},
      {"label": "Custom Principles", "description": "Generate project-specific development principles (Sonnet - requires reasoning)"}
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

Use Task tool (Haiku agent - fast pattern-based generation):

```
Task: Generate tests for [file]
Agent: Explore
Model: haiku
Thoroughness: quick

1. Read source file and understand logic
2. Identify:
   - Public functions/methods
   - Edge cases
   - Error paths
3. Generate test file with:
   - Test setup/teardown
   - Happy path tests
   - Edge case tests
   - Error handling tests
4. Use existing test patterns from codebase
```

**Why Haiku:** Unit test generation is pattern-based transformation - analyze function → generate test cases. Fast execution for large codebases.

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

Use Task tool (Sonnet Plan agent - requires workflow reasoning):

```
Task: Generate integration tests
Agent: Plan
Model: sonnet

1. Map user workflows (e.g., signup → login → action)
2. Generate tests for each workflow:
   - Setup: Create test data
   - Execute: Call real APIs
   - Verify: Check database state
   - Cleanup: Remove test data
3. Use appropriate framework (pytest, supertest, etc.)
```

**Why Sonnet:** Integration tests require understanding complex workflows, data dependencies, and service interactions. Needs reasoning about system architecture.

### Output

- Integration test files
- Test fixtures/factories
- Database setup scripts

---

## Generate: Documentation

**Generate API docs, README, and docstrings**

### Generate API Documentation

Use Haiku Explore agent (fast extraction):

```
Task: Generate API documentation
Agent: Explore
Model: haiku
Thoroughness: quick

1. Scan for API routes/endpoints
2. Extract:
   - HTTP method, path
   - Parameters (query, body, headers)
   - Response format
   - Error codes
3. Generate OpenAPI/Swagger spec
4. Generate markdown docs
```

**Why Haiku:** API doc generation is data extraction and formatting. No complex reasoning required.

### Generate README

Use Haiku Explore agent (template filling):

```
Task: Generate README
Agent: Explore
Model: haiku
Thoroughness: medium

Sections:
1. Project name & description (from analysis)
2. Installation instructions (from dependency files)
3. Usage examples (from existing code)
4. API reference (from extracted endpoints)
5. Development setup (from detected tools)
6. Contributing guidelines (standard template)
7. License (detect from LICENSE file)
```

**Why Haiku:** README generation is mostly template filling with project-specific data. Fast and straightforward.

### Generate Docstrings

Use Haiku Explore agent (pattern-based):

```
Task: Generate missing docstrings
Agent: Explore
Model: haiku
Thoroughness: quick

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

**Why Haiku:** Docstring generation is pattern-based code analysis. Can handle hundreds of functions quickly.

---

## Generate: CI/CD Pipeline

**Generate GitHub Actions or GitLab CI configuration**

### Detect Project Needs

- Languages used
- Test commands
- Build process
- Deployment target

### Generate Pipeline

Use Task tool (Sonnet Plan agent - requires architecture reasoning):

```
Task: Generate CI/CD pipeline
Agent: Plan
Model: sonnet

Generate workflow with stages:
1. **Lint**: Run linters/formatters (detect which tools)
2. **Test**: Run unit + integration tests (detect framework)
3. **Build**: Build application/package (detect build tool)
4. **Security**: Run security scans (add appropriate scanners)
5. **Deploy**: Deploy to staging/production (detect deployment target)

Reasoning required:
- Which tools to use for each stage
- Proper job dependencies and ordering
- Cache strategy for dependencies
- Matrix builds for multiple versions
- Environment-specific configurations
- Secrets management approach

Format: GitHub Actions (.github/workflows/ci.yml)
```

**Why Sonnet:** CI/CD pipeline generation requires understanding project architecture, choosing appropriate tools, and designing optimal workflow structure. Needs reasoning about dependencies and deployment strategy.

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

Use Task tool (Sonnet Plan agent - complex architectural decisions):

```
Task: Generate code from spec
Agent: Plan
Model: sonnet

1. Read specification file
2. Generate:
   - API client code
   - Type definitions
   - Request/response models
   - Validation logic
3. Use appropriate code generator (openapi-generator, etc.)
4. Add tests for generated code

Reasoning required:
- Choose appropriate client architecture (REST, GraphQL, gRPC)
- Design error handling strategy
- Implement authentication/authorization
- Handle rate limiting and retries
- Structure generated code for maintainability
- Generate comprehensive tests
```

**Why Sonnet:** Code generation from specs requires architectural decisions about client structure, error handling, auth patterns, and code organization. Complex reasoning required.

### Output

- Generated client/server code
- Type definitions
- Example usage
- Tests

---

## Generate: Custom Principles

**Generate project-specific development principles**

### Process

Use Task tool (Sonnet Plan agent - requires domain reasoning):

```
Task: Generate custom principles
Agent: Plan
Model: sonnet

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

Reasoning required:
- Understand domain-specific requirements (e.g., HIPAA for healthcare)
- Identify patterns in existing code issues
- Design principles that address root causes
- Balance strictness with practicality
- Consider team maturity and adoption challenges
```

**Why Sonnet:** Custom principle generation requires deep understanding of domain constraints, code quality issues, and team dynamics. High-level reasoning essential.

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
✓ Tests:            25 unit tests (+35% coverage) [Haiku - fast]
✓ Integration:      8 E2E tests [Sonnet - reasoning]
✓ Documentation:    README + 50 docstrings [Haiku - fast]
✓ CI/CD:            GitHub Actions pipeline [Sonnet - architecture]
✓ Code from Specs:  API client (OpenAPI) [Sonnet - complex]
✓ Principles:       7 custom principles [Sonnet - reasoning]

Performance:
- Haiku tasks: 2-3x faster than Sonnet
- Sonnet tasks: High quality reasoning
- Total time: ~30-40% faster than all-Sonnet approach

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
