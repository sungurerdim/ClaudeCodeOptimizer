# Integration Tests

This directory contains comprehensive integration tests for ClaudeCodeOptimizer.

## Test Files

### 1. test_end_to_end_wizard.py
**Purpose**: Test complete wizard workflow from start to finish

**Test Classes** (4 classes, 10 tests):
- `TestEndToEndWizardQuickMode`: Tests quick mode (AI auto-selection)
  - Complete flow from detection to file generation
  - Detection accuracy verification
  - Dry run mode testing
- `TestEndToEndWizardInteractiveMode`: Tests interactive mode with mocked input
  - Mocked user interaction flow
  - Abort/cancellation handling
- `TestEndToEndWizardEdgeCases`: Edge cases and error handling
  - Existing CLAUDE.md preservation
  - Non-git projects
  - Empty projects
- `TestWizardPerformance`: Performance characteristics
  - Execution time validation
  - Idempotency testing

**Key Features**:
- Uses real file operations with temp directories
- Tests both interactive and quick modes
- Verifies complete workflow integration
- Covers happy paths and error scenarios

---

### 2. test_knowledge_setup_integration.py
**Purpose**: Test complete knowledge base setup workflow

**Test Classes** (5 classes, 18 tests):
- `TestGlobalKnowledgeSetup`: Global directory initialization
  - Directory creation
  - Content copying
  - Template deployment
  - Force regeneration
- `TestClaudeHomeSymlinks`: ~/.claude/ symlink creation
  - Symlink creation and validation
  - Cross-platform compatibility
  - Fallback behavior
- `TestKnowledgeDiscoveryFunctions`: Knowledge discovery APIs
  - Principle category discovery
  - Command/guide/agent/skill discovery
- `TestKnowledgeSetupEdgeCases`: Edge cases
  - Corrupted content handling
  - Existing symlinks
  - Concurrent access
- `TestKnowledgeSetupPerformance`: Performance testing
  - Setup completion time
  - File count validation

**Key Features**:
- Tests complete global ~/.claude/ structure setup
- Verifies content copying from package
- Tests cross-platform file operations
- Validates knowledge discovery functions

---

### 3. test_claude_md_generation_integration.py
**Purpose**: Test complete CLAUDE.md generation with real data

**Test Classes** (4 classes, 15 tests):
- `TestClaudeMdGeneration`: New file generation
  - Template-based generation
  - Principle injection
  - Skills injection
  - Agents injection
  - Metadata inclusion
- `TestClaudeMdUpdate`: Updating existing files
  - Custom content preservation
  - Backup creation
  - Backup rotation (keep last 5)
- `TestClaudeMdEdgeCases`: Edge cases
  - Empty preferences
  - No selected skills/agents
  - Invalid principle IDs
  - Files without markers
- `TestClaudeMdPerformance`: Performance testing
  - Generation speed
  - File size validation
  - Large principle set handling

**Key Features**:
- Tests complete CLAUDE.md generation pipeline
- Verifies marker-based content injection
- Tests backup creation and rotation
- Validates content preservation during updates

---

### 4. test_project_analysis_integration.py
**Purpose**: Test full project analysis pipeline with multiple project types

**Test Classes** (9 classes, 25 tests):
- `TestProjectAnalyzerBasic`: Basic analysis functionality
  - Python/FastAPI project analysis
  - JavaScript/React project analysis
  - Polyglot project analysis
- `TestProjectAnalyzerTools`: Tool detection
  - Docker detection
  - CI/CD detection
  - Linter detection
  - Test framework detection
- `TestProjectAnalyzerStatistics`: Statistical analysis
  - File count statistics
  - Extension distribution
  - Detection counts
- `TestProjectAnalyzerStructure`: Structure analysis
  - Directory structure
  - Config file detection
- `TestProjectAnalyzerDependencies`: Dependency detection
  - Python dependencies (pyproject.toml)
  - JavaScript dependencies (package.json)
- `TestProjectAnalyzerRecommendations`: Recommendation engine
  - Command recommendations
  - Project-specific suggestions
- `TestProjectAnalyzerConfidence`: Confidence scoring
  - Overall confidence levels
  - Per-detection confidence scores
- `TestProjectAnalyzerPerformance`: Performance testing
  - Analysis speed
  - Large project handling
- `TestProjectAnalyzerEdgeCases`: Edge cases
  - Empty projects
  - Config-only projects
  - Projects without git
  - Corrupted configs
  - Symlink handling

**Key Features**:
- Creates realistic project fixtures (Python/FastAPI, JS/React, polyglot)
- Tests complete analysis pipeline
- Verifies multi-language detection
- Tests framework hierarchy filtering
- Validates recommendation generation

---

## Test Statistics

- **Total Test Files**: 4
- **Total Test Classes**: 22
- **Total Test Functions**: 68
- **Total Lines of Code**: ~2,800

## Running Integration Tests

### Run all integration tests:
```bash
pytest tests/integration/ -v
```

### Run specific test file:
```bash
pytest tests/integration/test_end_to_end_wizard.py -v
```

### Run with markers:
```bash
# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "integration and not slow"
```

### Run with coverage:
```bash
pytest tests/integration/ --cov=claudecodeoptimizer --cov-report=html
```

## Test Markers

- `@pytest.mark.integration`: Marks test as integration test
- `@pytest.mark.slow`: Marks test as slow (>1s execution time)

## Fixtures

### Common Fixtures (from conftest.py):
- `temp_dir`: Temporary directory for test files
- `project_root`: Project root path
- `content_dir`: Content directory path
- `minimal_preferences`: Minimal valid preferences

### Test-Specific Fixtures:
- `mock_project`: Python FastAPI project fixture
- `mock_global_dir`: Temporary global CCO directory
- `sample_preferences`: Sample preferences dictionary
- `python_api_project`: Full Python API project
- `javascript_frontend_project`: Full JS/React project
- `polyglot_project`: Multi-language project

## Coverage Areas

### Workflows Covered:
1. **End-to-End Wizard Flow**
   - Interactive mode with user input
   - Quick mode with AI auto-selection
   - Detection → Decision → Generation → File Creation

2. **Knowledge Base Setup**
   - Global directory initialization
   - Content deployment
   - Template management
   - Symlink creation (cross-platform)

3. **CLAUDE.md Generation**
   - New file creation
   - Existing file updates
   - Content injection (principles, skills, agents)
   - Backup management

4. **Project Analysis**
   - Multi-language detection
   - Framework detection
   - Tool detection
   - Statistical analysis
   - Recommendation generation

### Edge Cases Covered:
- Empty projects
- Non-git projects
- Corrupted config files
- Existing files/directories
- Cross-platform compatibility
- Performance boundaries
- Error handling

## Best Practices

1. **Use temp_dir fixture**: Always use temporary directories for file operations
2. **Mock external dependencies**: Mock global directories, external tools
3. **Test both happy and error paths**: Cover success and failure scenarios
4. **Verify file contents**: Don't just check existence, verify content
5. **Test cross-platform**: Use platform-specific skips where needed
6. **Performance bounds**: Set reasonable time limits for tests
7. **Cleanup**: Use fixtures that auto-cleanup temporary resources

## Future Enhancements

Potential areas for additional integration tests:

- [ ] CLI integration tests (full command execution)
- [ ] Multi-project workspace testing
- [ ] Concurrent wizard execution
- [ ] Large-scale project analysis (1000+ files)
- [ ] Network-dependent features (if any)
- [ ] Database integration (if applicable)
- [ ] Plugin/extension testing
