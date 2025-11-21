# Pull Request

## Description

<!-- Provide a clear and concise description of your changes -->
<!-- Include motivation and context for why this change is needed -->

**Type of Change:**
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test coverage improvement

**Related Issues:**
<!-- Link to related issues: Fixes #123, Relates to #456 -->

---

## Changes Made

<!-- List the specific changes in this PR -->
-
-
-

---

## Checklist

### General Code Quality

- [ ] Code follows project naming conventions (snake_case for Python)
- [ ] No hardcoded values or magic numbers (use named constants)
- [ ] Error handling is appropriate and informative
- [ ] No commented-out code left in the codebase
- [ ] Logging is appropriate (not using print statements)
- [ ] Type hints added for all function parameters and returns
- [ ] Docstrings added for all public functions and classes
- [ ] Code is DRY (no unnecessary duplication)
- [ ] Functions are single-purpose and focused
- [ ] File/module organization follows existing patterns

**Principles Applied:**
<!-- Check which CCO principles this PR follows -->
- [ ] U_CHANGE_VERIFICATION - All changes verified before claiming completion
- [ ] U_CROSS_PLATFORM_COMPATIBILITY - Commands work on Windows, macOS, Linux
- [ ] U_DRY - No unnecessary duplication
- [ ] U_EVIDENCE_BASED_ANALYSIS - Claims backed by evidence, complete accounting
- [ ] U_FOLLOW_PATTERNS - Follows existing codebase patterns
- [ ] U_MINIMAL_TOUCH - Only required files edited
- [ ] U_NO_HARDCODED_EXAMPLES - No hardcoded example data in templates
- [ ] U_NO_OVERENGINEERING - Simplest solution chosen

---

### AI-Generated Code Checks

**Critical: Review for AI hallucinations and anti-patterns**

- [ ] **No Hallucinated Functions**: All functions actually exist in dependencies
- [ ] **No Hallucinated Modules**: All imports are real and available
- [ ] **No Hallucinated APIs**: All API endpoints/methods actually exist
- [ ] **No Placeholder Code**: No TODOs, FIXMEs, or stub implementations
- [ ] **No Over-Engineering**: Solution is appropriately scoped (not gold-plated)
- [ ] **No Unnecessary Abstractions**: No premature generalization
- [ ] **No Bloat**: Implementation is concise and focused
- [ ] **No Copy-Paste Errors**: Variable names match context
- [ ] **No Broken Imports**: All imports verified to work
- [ ] **No Type Mismatches**: Types are correct and consistent

**Context-Specific Checks:**
- [ ] **Async Patterns**: Correct use of async/await (if applicable)
- [ ] **Resource Cleanup**: Proper cleanup in try/finally or context managers
- [ ] **Path Handling**: Uses Path objects, forward slashes, platform-independent
- [ ] **Error Messages**: Clear, actionable error messages
- [ ] **Configuration**: No hardcoded paths or environment assumptions

**Principles Applied:**
- [ ] C_NO_UNSOLICITED_FILE_CREATION - No unnecessary file creation
- [ ] C_NATIVE_TOOL_INTERACTIONS - Uses native Claude Code tools

---

### Testing & Coverage

- [ ] **Unit tests added** for new functionality
- [ ] **Integration tests added** if cross-module functionality changed
- [ ] **All tests pass** locally (`pytest tests/ -v`)
- [ ] **Coverage maintained or improved** (check with `pytest --cov`)
- [ ] **Edge cases tested** (empty inputs, None values, errors)
- [ ] **Test names are descriptive** (explain what is being tested)
- [ ] **Tests use tmp_path fixture** (no hardcoded /tmp or system paths)
- [ ] **Tests are isolated** (no dependencies between tests)
- [ ] **Assertions are specific** (not just `assert result`)

**Coverage Target:** 80%+ for new code

**Test Evidence:**
```
# Paste test output here showing all tests pass
```

**Principles Applied:**
- [ ] U_EVIDENCE_BASED_ANALYSIS - Test results prove functionality works

---

### Security

- [ ] **No secrets committed** (API keys, passwords, tokens)
- [ ] **No hardcoded credentials** (use environment variables)
- [ ] **Input validation** added for user-supplied data
- [ ] **No SQL injection** vulnerabilities (parameterized queries)
- [ ] **No path traversal** vulnerabilities (path validation)
- [ ] **Dependencies scanned** (no known vulnerabilities)
- [ ] **Sensitive data logged appropriately** (not in plaintext)
- [ ] **File permissions set correctly** (not world-writable)

**Security Scan Results:**
```
# If applicable, paste security scan output
```

---

### Documentation

- [ ] **README updated** if public API changed
- [ ] **Docstrings added** for all new public functions/classes
- [ ] **Inline comments** explain "why" for non-obvious code
- [ ] **ADR created** if architectural decision made
- [ ] **Runbook updated** if operational procedures changed
- [ ] **CHANGELOG updated** with user-facing changes
- [ ] **Type hints complete** for all new functions
- [ ] **Examples provided** in docstrings for complex functions

**Documentation Locations:**
<!-- List where documentation was updated -->
-
-

---

### Performance

- [ ] **No unnecessary loops** or O(n²) algorithms
- [ ] **Database queries optimized** (no N+1 queries)
- [ ] **Large files handled efficiently** (streaming, chunking)
- [ ] **Caching used appropriately** (not premature optimization)
- [ ] **Resource usage reasonable** (memory, CPU)
- [ ] **Async where beneficial** (I/O-bound operations)

**Performance Impact:**
<!-- Describe performance characteristics if relevant -->
- Benchmark results (if applicable):
- Expected load:

---

### Breaking Changes

<!-- If this is a breaking change, fill out this section -->

**Breaking Change Checklist:**
- [ ] **Migration guide provided** in PR description or docs
- [ ] **Deprecation warnings added** (if gradual migration)
- [ ] **CHANGELOG clearly marks breaking change** with "BREAKING:"
- [ ] **Version bump planned** (major version for breaking changes)
- [ ] **Backward compatibility considered** (can it be avoided?)
- [ ] **Communication plan** (how will users be informed?)

**Migration Instructions:**
<!-- If breaking change, provide step-by-step migration guide -->
```
1.
2.
3.
```

**Breaking Changes Guideline:**
- Breaking changes require explicit user approval before implementation
- Document migration path and alternatives considered

---

## Reviewer Notes

<!-- Add any notes for reviewers, areas of concern, or questions -->

**Review Focus Areas:**
-
-

**Known Limitations:**
-
-

**Future Improvements:**
-
-

---

## Review Quality Metrics

**For Reviewers:**
- [ ] Reviewed all changed files (not just summary)
- [ ] Tested changes locally
- [ ] Verified tests pass
- [ ] Checked for AI hallucinations/anti-patterns
- [ ] Considered edge cases and error scenarios
- [ ] Reviewed documentation changes
- [ ] Checked backward compatibility

**Comment Density Target:** At least one substantive comment per 50 lines of changed code

---

## Pre-Merge Checklist

**Before merging, ensure:**
- [ ] All CI/CD checks pass (tests, linting, type checking)
- [ ] At least one approval from code owner
- [ ] All review comments addressed or discussed
- [ ] Branch is up to date with main
- [ ] Commit messages follow conventional commits format
- [ ] No merge conflicts
- [ ] Squash commits if needed (clean history)

---

## Post-Merge Actions

**After merging:**
- [ ] Monitor for issues in production/usage
- [ ] Update related issues (close or link)
- [ ] Notify stakeholders if breaking change
- [ ] Update documentation site (if applicable)
- [ ] Create follow-up issues for future improvements

---

**Additional Notes:**
<!-- Any other information relevant to this PR -->
