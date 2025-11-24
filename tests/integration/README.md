# Integration Tests

This directory contains integration tests for ClaudeCodeOptimizer that verify end-to-end command workflows.

## Test Files

### test_command_flows.py
**Purpose**: Test CCO command execution flows and file operations

**Test Classes**:
- `TestCCOStatusCommand`: Tests installation health check (`cco-status`)
  - Clean installation verification
  - Missing directories detection
  - No installation handling

- `TestCCOHelpCommand`: Tests command reference display (`cco-help`)
  - Command list display
  - Command file discovery

- `TestCCOGenerateCommand`: Tests file generation workflows (`cco-generate`)
  - Missing test file generation
  - Documentation creation (ADRs, runbooks)
  - PR template generation

- `TestCCOUpdateCommand`: Tests update workflows (`cco-update`)
  - Version tracking with VersionManager
  - Backup creation before updates

- `TestMetadataTracking`: Tests installation metadata
  - Metadata file structure
  - Missing metadata handling

- `TestKnowledgeSetup`: Tests CCO directory setup
  - Directory structure creation
  - Existing file preservation

- `TestErrorHandling`: Tests error scenarios
  - Permission errors
  - Missing dependencies
  - Path validation

- `TestFileGeneration`: Tests file creation
  - Correct file structure
  - Valid markdown generation
  - UTF-8 encoding preservation

**Key Features**:
- Uses `tmp_path` pytest fixture for isolated testing
- Real file operations (no mocking)
- Tests both success and error paths
- Verifies file content correctness

## Running Tests

### Run all integration tests:
```bash
pytest tests/integration/ -v
```

### Run specific test file:
```bash
pytest tests/integration/test_command_flows.py -v
```

### Run specific test class:
```bash
pytest tests/integration/test_command_flows.py::TestCCOStatusCommand -v
```

### Run with coverage:
```bash
pytest tests/integration/ --cov=claudecodeoptimizer --cov-report=html
```

## Test Patterns

### Temporary Directory Usage
All tests use `tmp_path` fixture for isolation:
```python
def test_example(self, tmp_path: Path) -> None:
    # tmp_path is automatically created and cleaned up
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    # ... test logic ...
```

### File Operations
```python
# Create files
(tmp_path / "file.txt").write_text("content")

# Verify files exist
assert (tmp_path / "file.txt").exists()

# Read and verify content
content = (tmp_path / "file.txt").read_text()
assert "expected" in content
```

### Directory Structure Setup
```python
# Setup CCO structure
claude_dir = tmp_path / ".claude"
(claude_dir / "commands").mkdir(parents=True)
(claude_dir / "principles").mkdir()
(claude_dir / "skills").mkdir()
(claude_dir / "agents").mkdir()
```

## Coverage Goals

Current integration test coverage focuses on:
- ✅ Command execution workflows
- ✅ File generation and validation
- ✅ Directory structure setup
- ✅ Error handling
- ✅ Metadata tracking

## Future Test Additions

Planned integration tests:
- [ ] Full cco-audit command workflow
- [ ] Full cco-fix command workflow
- [ ] CLAUDE.md marker system integration
- [ ] Multi-command sequential execution
- [ ] Cross-platform path handling
