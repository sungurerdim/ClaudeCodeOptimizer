---
title: Modern Python Packaging Skill
category: infrastructure
description: pyproject.toml, poetry, uv, packaging
metadata:
  name: "Modern Python Packaging"
  activation_keywords: ["package", "pyproject", "uv", "poetry", "publish"]
  category: "language-python"
  language: "python"
principles: ['U_DEPENDENCY_MANAGEMENT', 'P_SUPPLY_CHAIN_SECURITY', 'P_SEMANTIC_VERSIONING', 'P_VERSION_MANAGEMENT']
use_cases:
  project_purpose: [library, cli, backend]
  project_maturity: [active-dev, production]
---

# Modern Python Packaging

Master modern Python packaging with pyproject.toml, UV, and best practices for distribution.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Modern Packaging Standards:**
- `pyproject.toml` replaces setup.py (PEP 517, 518, 621)
- Build backend: `hatchling`, `setuptools`, or `pdm-backend`
- Dependency management: UV (fastest), Poetry, or pip-tools
- Version control: `setuptools-scm` or `hatch-vcs` for git-based versioning
- Distribution: Build wheels (.whl) and source distributions (.tar.gz)

**Key Patterns:**
1. Use `pyproject.toml` as single source of configuration
2. Specify dependencies with version constraints (^, ~, >=)
3. Separate production and development dependencies
4. Use `src/` layout for packages (prevents import confusion)
5. Include metadata: description, license, classifiers

**Publishing Workflow:**
1. Update version in pyproject.toml
2. Build: `python -m build`
3. Test: `twine check dist/*`
4. Upload: `twine upload dist/*` (PyPI) or use UV/Poetry

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Complete pyproject.toml (UV):**
```toml
[project]
name = "mypackage"
version = "0.1.0"
description = "A modern Python package"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["example", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.4.0",
]

[project.urls]
Homepage = "https://github.com/username/mypackage"
Documentation = "https://mypackage.readthedocs.io"
Repository = "https://github.com/username/mypackage"
Issues = "https://github.com/username/mypackage/issues"

[project.scripts]
myapp = "mypackage.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
```

**Project Structure (src layout):**
```
myproject/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
└── docs/
    └── index.md
```

**UV Workflow:**
```bash
# Install UV (fastest Python package installer)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init myproject
cd myproject

# Add dependencies
uv add requests pydantic

# Add dev dependencies
uv add --dev pytest pytest-cov ruff mypy

# Install project in editable mode
uv pip install -e .

# Run commands in UV environment
uv run pytest
uv run mypy src/

# Update dependencies
uv lock
uv sync
```

**Poetry Alternative:**
```bash
# Initialize project
poetry new myproject
cd myproject

# Add dependencies
poetry add requests pydantic

# Add dev dependencies
poetry add --group dev pytest pytest-cov ruff mypy

# Install
poetry install

# Run commands
poetry run pytest
poetry shell  # Activate virtualenv

# Publish
poetry build
poetry publish
```

**Dynamic Versioning (setuptools-scm):**
```toml
[build-system]
requires = ["setuptools>=64", "setuptools-scm>=8"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
dynamic = ["version"]

[tool.setuptools_scm]
version_file = "src/mypackage/_version.py"
```

**Entry Points and CLI:**
```toml
[project.scripts]
myapp = "mypackage.cli:main"
admin = "mypackage.admin:run"

[project.gui-scripts]
myapp-gui = "mypackage.gui:main"
```

```python
# src/mypackage/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="My CLI app")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    print("Running myapp...")

if __name__ == "__main__":
    main()
```

**Building and Publishing:**
```bash
# Install build tools
uv pip install build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel and sdist
python -m build

# Check package
twine check dist/*

# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ mypackage

# Upload to PyPI
twine upload dist/*
```

**Dependency Version Constraints:**
```toml
dependencies = [
    "requests>=2.31.0,<3.0.0",  # Specific range
    "pydantic~=2.4.0",          # Compatible release (~= 2.4.0 means >=2.4.0, <2.5.0)
    "click>=8.0",               # Minimum version
    "numpy==1.24.0",            # Exact version (avoid unless necessary)
]
```

**Including Data Files:**
```toml
[tool.hatch.build]
include = [
    "src/mypackage/**/*.py",
    "src/mypackage/data/*.json",
    "README.md",
    "LICENSE",
]
exclude = [
    "tests/",
    "docs/",
    "*.pyc",
]
```

**Manifest.in (if using setuptools):**
```
include README.md
include LICENSE
recursive-include src/mypackage/data *.json
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

**Package Metadata Best Practices:**
```toml
[project]
# Use semantic versioning: MAJOR.MINOR.PATCH
version = "1.2.3"

# Comprehensive classifiers
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Typing :: Typed",
]

# Specify Python version range
requires-python = ">=3.11,<4.0"
```

**GitHub Actions for Publishing:**
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

**Anti-Patterns to Avoid:**
```toml
# ✗ Don't pin exact versions in libraries
dependencies = ["requests==2.31.0"]  # Too restrictive

# ✓ Use ranges for compatibility
dependencies = ["requests>=2.31.0,<3.0.0"]

# ✗ Don't commit build artifacts
# dist/, build/, *.egg-info should be in .gitignore

# ✗ Don't use setup.py for modern projects
# Use pyproject.toml instead
```
