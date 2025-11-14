---
id: cco-setup-cicd
description: Generate GitHub Actions, GitLab CI configs
category: devops
priority: normal
principles:
  - 'P_CI_GATES'
  - 'C_PRODUCTION_GRADE'
  - 'P_SUPPLY_CHAIN_SECURITY'
  - 'C_FOLLOW_PATTERNS'
  - 'U_TEST_FIRST'
---

# Setup CI/CD

Generate CI/CD pipeline configurations for **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Create complete CI/CD pipelines:
1. Detect platform (GitHub Actions, GitLab CI, etc.)
2. Generate appropriate configuration
3. Include testing, linting, building
4. Add deployment stages
5. Security scanning

**Output:** Production-ready CI/CD configuration.

---

## Architecture & Model Selection

**Generation**: Haiku (template-based)
**Execution Pattern**: Sequential generation

---

## When to Use

**Use this command:**
- New projects without CI/CD
- Migrating platforms
- Improving existing pipelines
- Adding new stages

---

## Phase 1: Detect Platform

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path

project_root = Path(".").resolve()

print(f"=== Platform Detection ===\n")

platforms = {
    'GitHub Actions': (project_root / '.github').exists(),
    'GitLab CI': (project_root / '.gitlab-ci.yml').exists(),
    'CircleCI': (project_root / '.circleci').exists(),
}

detected = [name for name, exists in platforms.items() if exists]

if detected:
    print(f"Detected: {', '.join(detected)}")
else:
    print("No existing CI/CD detected")
    print("Will generate GitHub Actions (default)")

print()
```

---

## Phase 2: Generate GitHub Actions

```python
print(f"=== GitHub Actions Generation ===\n")

github_actions = '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --statistics

    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml --cov-report=html

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Run security scan
      run: |
        pip install safety bandit
        safety check
        bandit -r src/

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Build package
      run: |
        python -m pip install build
        python -m build

    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3

    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: |
        pip install twine
        twine upload dist/*
'''

workflow_path = project_root / '.github' / 'workflows' / 'ci.yml'
workflow_path.parent.mkdir(parents=True, exist_ok=True)

print("Generated GitHub Actions workflow:")
print("  - test: Run tests on Python 3.9-3.11")
print("  - security: Security scanning")
print("  - build: Build package")
print("  - deploy: Publish to PyPI (main branch)")
print()
print(f"File: {workflow_path.relative_to(project_root)}")
print()
```

---

## Phase 3: Generate GitLab CI

```python
print(f"=== GitLab CI Generation ===\n")

gitlab_ci = '''stages:
  - test
  - security
  - build
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -V
  - pip install virtualenv
  - virtualenv venv
  - source venv/bin/activate
  - pip install -e ".[dev]"

test:
  stage: test
  script:
    - pytest --cov=src --cov-report=xml --cov-report=html
    - flake8 .
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

security:
  stage: security
  script:
    - pip install safety bandit
    - safety check
    - bandit -r src/
  allow_failure: true

build:
  stage: build
  script:
    - python -m pip install build
    - python -m build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  script:
    - pip install twine
    - twine upload dist/*
  only:
    - main
  when: manual
'''

print("Generated GitLab CI configuration:")
print("  - test: Run tests with coverage")
print("  - security: Security scanning")
print("  - build: Build artifacts")
print("  - deploy: Manual deployment")
print()
```

---

## Phase 4: Generate CircleCI

```python
print(f"=== CircleCI Generation ===\n")

circleci = '''version: 2.1

orbs:
  python: circleci/python@2.1.1

workflows:
  test-and-deploy:
    jobs:
      - test
      - build:
          requires:
            - test
      - deploy:
          requires:
            - build
          filters:
            branches:
              only: main

jobs:
  test:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
      - run:
          name: Run tests
          command: pytest --cov=src
      - run:
          name: Lint
          command: flake8 .

  build:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Build package
          command: |
            python -m pip install build
            python -m build
      - persist_to_workspace:
          root: .
          paths:
            - dist

  deploy:
    docker:
      - image: cimg/python:3.11
    steps:
      - attach_workspace:
          at: .
      - run:
          name: Deploy to PyPI
          command: |
            pip install twine
            twine upload dist/*
'''

print("Generated CircleCI configuration:")
print("  - Orb-based Python setup")
print("  - Parallel test execution")
print("  - Workspace for artifacts")
print()
```

---

## Phase 5: Add Pre-commit Hooks

```python
print(f"=== Pre-commit Hooks ===\n")

precommit = '''repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
'''

print("Generated pre-commit configuration:")
print("  - Code formatting (black)")
print("  - Import sorting (isort)")
print("  - Linting (flake8)")
print("  - Type checking (mypy)")
print()
```

---

## Phase 6: Summary

```python
print(f"=== Setup Summary ===\n")

print("Generated CI/CD Configurations:")
print("  ✓ GitHub Actions (.github/workflows/ci.yml)")
print("  ✓ GitLab CI (.gitlab-ci.yml)")
print("  ✓ CircleCI (.circleci/config.yml)")
print("  ✓ Pre-commit hooks (.pre-commit-config.yaml)")
print()

print("Pipeline Stages:")
print("  1. Test: Run tests on multiple Python versions")
print("  2. Security: Scan for vulnerabilities")
print("  3. Build: Create distribution packages")
print("  4. Deploy: Publish to PyPI (production only)")
print()

print("Next Steps:")
print("  1. Review generated configurations")
print("  2. Add secrets (PYPI_TOKEN) to CI platform")
print("  3. Enable CI/CD in repository settings")
print("  4. Push to trigger first run")
print()
```

---

## Output Example

```
=== Platform Detection ===

No existing CI/CD detected
Will generate GitHub Actions (default)

=== GitHub Actions Generation ===

Generated GitHub Actions workflow:
  - test: Run tests on Python 3.9-3.11
  - security: Security scanning
  - build: Build package
  - deploy: Publish to PyPI (main branch)

File: .github/workflows/ci.yml

=== GitLab CI Generation ===

Generated GitLab CI configuration:
  - test: Run tests with coverage
  - security: Security scanning
  - build: Build artifacts
  - deploy: Manual deployment

=== Pre-commit Hooks ===

Generated pre-commit configuration:
  - Code formatting (black)
  - Import sorting (isort)
  - Linting (flake8)
  - Type checking (mypy)

=== Setup Summary ===

Generated CI/CD Configurations:
  ✓ GitHub Actions (.github/workflows/ci.yml)
  ✓ GitLab CI (.gitlab-ci.yml)
  ✓ CircleCI (.circleci/config.yml)
  ✓ Pre-commit hooks (.pre-commit-config.yaml)

Pipeline Stages:
  1. Test: Run tests on multiple Python versions
  2. Security: Scan for vulnerabilities
  3. Build: Create distribution packages
  4. Deploy: Publish to PyPI (production only)

Next Steps:
  1. Review generated configurations
  2. Add secrets (PYPI_TOKEN) to CI platform
  3. Enable CI/CD in repository settings
  4. Push to trigger first run
```

---

**CI/CD Philosophy:** Automate everything you can. If it's worth doing, it's worth automating.
