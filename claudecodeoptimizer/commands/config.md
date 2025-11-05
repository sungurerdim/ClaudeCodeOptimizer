---
description: CCO configuration management (setup, export, import)
category: core
subcommands:
  - setup: Interactive configuration wizard
  - export: Export configuration to file
  - import: Import configuration from file
  - show: Display current configuration
---

# CCO Configuration Management

Manage CCO project configuration with interactive setup, export/import capabilities.

## Usage

```bash
/cco-config setup    # Interactive wizard
/cco-config export   # Export to cco-config.json
/cco-config import   # Import from file
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
2. Principle Selection (choose from 52 principles)
3. Command Generation (select commands to enable)
4. Workflow Customization (CI/CD, hooks, scripts)
5. Final Review & Confirmation

### Output

- Configuration saved to `~/.cco/projects/PROJECT_NAME.json`
- Commands generated in `.claude/commands/`
- Principles saved to `.claude/PRINCIPLES.md`

---

## Subcommand: export

**Export Configuration to File**

Export current CCO configuration to a portable JSON file.

### Action

Use the Task tool with Explore agent:

```
Task: Export CCO configuration
Agent: Explore
Thoroughness: quick
```

### Steps

1. **Load Configuration**
```python
import json
from pathlib import Path

# Load project config
project_root = Path.cwd()
project_name = project_root.name
config_file = Path.home() / ".cco" / "projects" / f"{project_name}.json"

if not config_file.exists():
    print("❌ Project not initialized. Run /cco-init first.")
    exit(1)

config = json.loads(config_file.read_text())
```

2. **Create Export File**
```python
# Export to project root
export_file = project_root / "cco-config.json"

# Add metadata
export_data = {
    "version": "1.0.0",
    "exported_at": str(datetime.now()),
    "project_name": project_name,
    "config": config
}

export_file.write_text(json.dumps(export_data, indent=2))
print(f"✓ Configuration exported to: {export_file}")
```

3. **Verify Export**
```bash
cat cco-config.json | head -20
```

### Output

- `cco-config.json` file in project root
- Contains: project settings, selected principles, enabled commands
- Can be committed to version control
- Portable across team members

---

## Subcommand: import

**Import Configuration from File**

Import CCO configuration from an exported JSON file.

### Action

Use the Task tool with Explore agent:

```
Task: Import CCO configuration
Agent: Explore
Thoroughness: quick
```

### Steps

1. **Locate Import File**
```python
import json
from pathlib import Path

project_root = Path.cwd()
import_file = project_root / "cco-config.json"

if not import_file.exists():
    print("❌ No cco-config.json found in project root")
    print("   Run /cco-config export first")
    exit(1)

import_data = json.loads(import_file.read_text())
config = import_data["config"]
```

2. **Validate Configuration**
```python
# Check required fields
required = ["project_type", "primary_language", "selected_principles"]
missing = [f for f in required if f not in config.get("analysis", {})]

if missing:
    print(f"❌ Invalid config file. Missing: {missing}")
    exit(1)

print(f"✓ Configuration valid")
print(f"  Project: {import_data['project_name']}")
print(f"  Exported: {import_data['exported_at']}")
```

3. **Apply Configuration**
```python
# Save to global registry
project_name = project_root.name
config_file = Path.home() / ".cco" / "projects" / f"{project_name}.json"
config_file.parent.mkdir(parents=True, exist_ok=True)
config_file.write_text(json.dumps(config, indent=2))

print(f"✓ Configuration imported successfully")
```

4. **Regenerate Commands**
```bash
python -m claudecodeoptimizer init
```

This regenerates `.claude/commands/` based on imported config.

### Output

- Configuration applied to current project
- Commands regenerated in `.claude/commands/`
- Principles synchronized

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

**Invalid Config File:**
```
❌ Invalid configuration file
   Missing required fields: [...]
```

**Import Failed:**
```
❌ Import failed: [error message]
   Check file format and try again
```

---

## Best Practices

1. **Export After Setup**: Always export config after initial setup
2. **Version Control**: Commit `cco-config.json` to share team settings
3. **Regular Sync**: Re-import config when pulling team changes
4. **Backup**: Keep exported configs for reference

---

## Related Commands

- `/cco-init` - Initialize CCO for project
- `/cco-status` - Check CCO status
- `/cco-remove` - Remove CCO from project
