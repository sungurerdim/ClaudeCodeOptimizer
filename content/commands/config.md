---
description: CCO configuration management (setup, show)
category: core
subcommands:
  - setup: Interactive configuration wizard
  - show: Display current configuration
---

# CCO Configuration Management

Manage CCO project configuration with interactive setup and status display.

## Usage

```bash
/cco-config setup    # Interactive wizard
/cco-config show     # Show current config
```

---

## Subcommand: setup

**Interactive Configuration Wizard**

Launch the full CCO configuration wizard to customize your project setup.

### Action

```bash
python -m claudecodeoptimizer init --interactive
```

This launches the 5-phase wizard:
1. Project Detection (auto-detect type, languages, frameworks)
2. Principle Selection (choose from available principles: universal + project-specific, see README.md for counts)
3. Command Generation (select commands to enable)
4. Workflow Customization (CI/CD, hooks, scripts)
5. Final Review & Confirmation

### Output

- Configuration saved to `~/.cco/projects/PROJECT_NAME.json`
- Commands generated in `.claude/commands/`
- Principles saved to `.claude/PRINCIPLES.md`

---

## Subcommand: show

**Display Current Configuration**

Show current CCO configuration for this project.

### Action

```python
import json
from pathlib import Path

project_root = Path.cwd()
project_name = project_root.name
config_file = Path.home() / ".cco" / "projects" / f"{project_name}.json"

if not config_file.exists():
    print("❌ Project not initialized")
    exit(0)

config = json.loads(config_file.read_text())
analysis = config.get("analysis", {})

print("=" * 60)
print(f"CCO Configuration: {project_name}")
print("=" * 60)
print(f"\nProject Type: {analysis.get('project_type', 'unknown')}")
print(f"Primary Language: {analysis.get('primary_language', 'unknown')}")
print(f"Framework: {analysis.get('primary_framework', 'none')}")
print(f"\nSelected Principles: {len(analysis.get('selected_principles', []))}")
print(f"Enabled Commands: {len(analysis.get('commands', []))}")
print(f"Features:")
print(f"  - Tests: {'✓' if analysis.get('has_tests') else '✗'}")
print(f"  - Docker: {'✓' if analysis.get('has_docker') else '✗'}")
print(f"  - CI/CD: {'✓' if analysis.get('has_ci_cd') else '✗'}")
print("\n" + "=" * 60)
```

### Output

```
============================================================
CCO Configuration: myproject
============================================================

Project Type: api
Primary Language: python
Framework: fastapi

Selected Principles: 15
Enabled Commands: 8
Features:
  - Tests: ✓
  - Docker: ✓
  - CI/CD: ✓

============================================================
```

---

## Error Handling

**Project Not Initialized:**
```
❌ Project not initialized with CCO
   Run: /cco-init
```

---

## Best Practices

1. **Review After Setup**: Always review config after initial setup with `/cco-config show`
2. **Regular Status Checks**: Use `/cco-status` to monitor project health
3. **Reconfigure When Needed**: Run `/cco-config setup` if project requirements change

---

## Related Commands

- `/cco-init` - Initialize CCO for project
- `/cco-status` - Check CCO status
- `/cco-remove` - Remove CCO from project
