# CCO Interactive Wizard

Production-ready wizard for initializing CCO in any project.

## Features

- **100% Pure Python stdlib** - No external dependencies (no rich, questionary, etc.)
- **Universal** - Works with any programming language, framework, or project type
- **5-Phase Flow** - Detection → Questions → Commands → Preview → Apply
- **58 Questions** - Comprehensive configuration across 9 categories
- **AI-Powered Hints** - Context-aware recommendations based on project detection
- **Dry-Run Mode** - Preview changes without modifying files

## Quick Start

```bash
# Run wizard in current directory
python .cco/wizard/cli.py

# Preview without making changes
python .cco/wizard/cli.py --dry-run

# Run in specific directory
python .cco/wizard/cli.py --project /path/to/project
```

## Architecture

### 4 Core Files

1. **cli.py** (651 lines)
   - Main wizard orchestrator
   - 5-phase flow implementation
   - State management
   - File generation

2. **questions.py** (883 lines)
   - 58 questions across 9 categories
   - AI hint generators
   - Default value generators
   - Question validation

3. **checkpoints.py** (451 lines)
   - Confirmation screens
   - Preview displays
   - Detection results viewer
   - Completion summary

4. **renderer.py** (456 lines)
   - CLI rendering utilities
   - ANSI color support (optional)
   - Input helpers
   - Table/list formatting

**Total:** 2,464 lines of production-ready Python

## 5-Phase Wizard Flow

### Phase 1: Detection

```
1. Scan project files
2. Detect languages, frameworks, tools
3. Analyze codebase patterns
4. Display detection results
5. Confirm or edit
```

### Phase 2: Questions

```
58 questions across 9 categories:
├── Project Identity (12)
├── Development Style (8)
├── Code Quality (10)
├── Documentation (8)
├── Testing Strategy (7)
├── Security Posture (6)
├── Performance (5)
├── Collaboration (4)
└── DevOps (6)

Each question shows:
- AI recommendation
- Default value (from detection)
- Multiple choice or text input
```

### Phase 3: Command Selection

```
1. Generate command recommendations
2. Show core/recommended/optional
3. Allow customization
4. Display selection summary
5. Confirm
```

### Phase 4: Preview

```
Display all changes:
├── Files to create
├── Files to modify
├── Commands to install
├── Permissions to configure
└── Principles to enforce

User confirms before applying
```

### Phase 5: Apply

```
1. Create directories
2. Write preferences.json
3. Generate command files
4. Configure permissions
5. Generate PRINCIPLES.md
6. Show completion summary
```

## Question Categories

### 1. Project Identity (12 questions)

- name
- types (api, backend, frontend, etc.)
- primary_language
- secondary_languages
- frameworks
- deployment_target
- expected_scale
- business_domain
- compliance_requirements
- project_maturity
- team_trajectory
- license_model

### 2. Development Style (8 questions)

- code_philosophy
- development_pace
- tdd_adherence
- refactoring_frequency
- breaking_changes_policy
- code_review_strictness
- pair_programming
- feature_flags

### 3. Code Quality Standards (10 questions)

- linting_strictness
- type_coverage_target
- cyclomatic_complexity_limit
- function_length_limit
- dry_enforcement
- code_comment_density
- naming_convention_strictness
- magic_number_tolerance
- import_organization
- line_length_limit

### 4. Documentation Preferences (7 questions)

- verbosity
- target_audience
- documentation_style
- inline_documentation
- architecture_diagrams
- api_documentation
- readme_length

### 5. Testing Strategy (7 questions)

- coverage_target
- test_pyramid_ratio
- mutation_testing
- property_based_testing
- test_isolation
- test_naming
- mocking_philosophy

### 6. Security Posture (6 questions)

- security_stance
- secret_management
- encryption_scope
- audit_logging
- input_validation
- dependency_scanning

### 7. Performance vs Maintainability (5 questions)

- optimization_priority
- caching_strategy
- database_queries
- premature_optimization
- duplication_for_performance

### 8. Team Collaboration (4 questions)

- git_workflow
- commit_convention
- pr_size_limit
- code_ownership

### 9. DevOps Automation (6 questions)

- ci_cd_trigger
- deployment_frequency
- rollback_strategy
- infrastructure
- monitoring
- environment_count

## AI Hint System

Each question can have an AI hint generator that uses detection results:

```python
def get_deployment_hint(report: Dict[str, Any]) -> str:
    """Generate AI hint for deployment target"""
    tools = [t["detected_value"] for t in report.get("tools", [])]
    if "docker" in tools or "kubernetes" in tools:
        return "Detected Docker/K8s - likely cloud deployment"
    return "Inferred from tooling"
```

## Default Value System

Default values are computed from detection results:

```python
def default_primary_language(report: Dict[str, Any]) -> str:
    """Get default primary language from detection"""
    languages = report.get("languages", [])
    return languages[0]["detected_value"] if languages else "python"
```

## Usage Examples

### Basic Usage

```bash
python .cco/wizard/cli.py
```

### Dry Run (Preview Only)

```bash
python .cco/wizard/cli.py --dry-run
```

### Custom Project Path

```bash
python .cco/wizard/cli.py --project /path/to/project
```

### Programmatic Usage

```python
from wizard.cli import CCOWizard

wizard = CCOWizard("/path/to/project", dry_run=False)
success = wizard.run()

if success:
    print("CCO initialized successfully!")
```

## File Structure After Initialization

```
project/
├── .cco/
│   ├── config/
│   │   ├── preferences.json      # All 58 answers
│   │   └── project.json          # Project metadata
│   └── state/                    # Runtime state
├── .claude/
│   ├── commands/
│   │   ├── cco-help.md
│   │   ├── cco-status.md
│   │   └── ...                   # 8-20 commands
│   └── settings.json             # Permissions
└── PRINCIPLES.md                 # Development principles
```

## Integration with CCO System

The wizard integrates with:

1. **Detection Engine** (`.cco/ai/detection.py`)
   - Auto-detects languages, frameworks, tools
   - Analyzes codebase patterns

2. **Recommendation Engine** (`.cco/ai/recommendations.py`)
   - Generates AI recommendations
   - Domain/scale-based logic

3. **Command Recommender** (`.cco/ai/command_selection.py`)
   - Recommends CCO commands
   - Rule-based selection

4. **Preference Schema** (`.cco/schemas/preferences.py`)
   - Validates all 58 answers
   - Type-safe configuration

## Terminal Support

### Color Support

Colors are automatically detected and disabled if:
- Terminal doesn't support ANSI codes
- `TERM=dumb` environment variable
- Non-TTY output (piped)

### Keyboard Shortcuts

- `Ctrl+C` - Cancel wizard at any point
- `Enter` - Accept default value
- `1-9` - Select choice by number

## Error Handling

The wizard handles:
- Invalid input (retries)
- Detection failures (graceful degradation)
- File write errors (rollback)
- Keyboard interrupts (clean exit)

## Testing

```bash
# Syntax check
python -m py_compile .cco/wizard/*.py

# Dry run (no file writes)
python .cco/wizard/cli.py --dry-run

# Test detection only
python .cco/ai/detection.py /path/to/project
```

## Dependencies

**Zero external dependencies!** Uses only Python stdlib:
- `os`, `sys`, `json`, `time`
- `pathlib`, `argparse`
- `typing`, `datetime`

No need for:
- ❌ rich
- ❌ questionary
- ❌ click
- ❌ prompt_toolkit

## Development

### Adding New Questions

1. Add question to `questions.py`:

```python
{
    "category": "code_quality",
    "field": "new_setting",
    "type": "choice",
    "prompt": "What is your preference?",
    "choices": ["option1", "option2", "option3"],
    "ai_hint": lambda report: "AI recommendation",
    "default": lambda report: "option1",
}
```

2. Update schema in `.cco/schemas/preferences.py`
3. Update template rendering to use new field

### Adding New Categories

1. Add category to `preferences.py` schema
2. Add questions to `questions.py`
3. Update `cli.py` categories dict
4. Update documentation

## Future Enhancements

- [ ] Interactive command selection (checkbox UI)
- [ ] Edit detection results before questions
- [ ] Save/load wizard state (resume later)
- [ ] Export configuration to share with team
- [ ] Template preview before generation
- [ ] Rollback mechanism for failed installations

## License

Part of ClaudeCodeOptimizer. Same license as parent project.

---

**Total Lines:** 2,464
**Files:** 4 core + 1 init
**Dependencies:** 0 external
**Questions:** 58 across 9 categories
**Status:** Production-ready
