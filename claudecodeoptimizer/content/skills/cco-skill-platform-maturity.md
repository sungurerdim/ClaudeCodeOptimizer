---
name: cco-skill-platform-maturity
description: Assess platform engineering maturity through CI/CD automation, test coverage, IaC presence, deployment capabilities, and developer experience scoring to determine AI readiness and amplification potential
keywords: [platform engineering, CI/CD maturity, test automation, IaC, Infrastructure as Code, deployment automation, developer experience, DX, AI readiness, platform maturity, DevOps]
category: platform
related_commands:
  action_types: [audit]
  categories: [platform, cicd, tests]
pain_points: [4, 6, 10]
---

# Platform Engineering, Maturity & Developer Experience

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


Assess platform maturity + CI/CD automation + test coverage + IaC + DX + AI readiness.
---

---

## Domain

Platform teams, DevOps, infrastructure, CI/CD pipelines, developer experience optimization.

---

## Purpose

**DORA 2025 Finding:** 90% of organizations have platform engineering, but quality varies dramatically.

**Critical Insight:** Platform quality directly correlates with AI benefit amplification:
- **High-quality platform + AI = Benefits amplified**
- **Low-quality platform + AI = Problems amplified (or no benefit)**

**Why Platform Matters:**
Companies struggling with AI adoption skipped fundamentals:
- No automated testing
- Manual deployments
- Accumulated technical debt
- Poor developer experience

**This skill assesses:** Platform maturity, foundation strength, AI readiness.

---

## Core Techniques

### 1. CI/CD Maturity Assessment

**Detect and score CI/CD completeness:**

```python
def assess_cicd_maturity() -> dict:
    """Check for CI/CD files and completeness"""
    cicd_files = {
        'github_actions': glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml'),
        'gitlab_ci': glob.glob('.gitlab-ci.yml'),
        'jenkins': glob.glob('Jenkinsfile') + glob.glob('Jenkinsfile.*'),
        'circleci': glob.glob('.circleci/config.yml'),
        'azure_pipelines': glob.glob('azure-pipelines.yml'),
        'travis': glob.glob('.travis.yml'),
        'drone': glob.glob('.drone.yml')
    }

    detected = {k: v for k, v in cicd_files.items() if v}

    if not detected:
        return {'maturity': 'NONE', 'score': 0, 'detected': None}

    # Analyze pipeline completeness
    stages = analyze_pipeline_stages(list(detected.values())[0][0])

    return {
        'maturity': calculate_cicd_maturity(stages),
        'score': calculate_cicd_score(stages),
        'detected': list(detected.keys())[0],
        'files': list(detected.values())[0],
        'stages': stages
    }

def analyze_pipeline_stages(file_path: str) -> dict:
    """Check what stages are present"""
    with open(file_path) as f:
        content = f.read().lower()

    return {
        'build': any(keyword in content for keyword in ['build', 'compile', 'bundle']),
        'test': any(keyword in content for keyword in ['test', 'pytest', 'jest', 'unittest']),
        'lint': any(keyword in content for keyword in ['lint', 'ruff', 'eslint', 'flake8']),
        'security_scan': any(keyword in content for keyword in ['security', 'sast', 'snyk', 'trivy', 'bandit']),
        'deploy': any(keyword in content for keyword in ['deploy', 'release', 'publish']),
        'quality_gates': any(keyword in content for keyword in ['coverage', 'sonar', 'quality']),
        'rollback': any(keyword in content for keyword in ['rollback', 'revert', 'previous']),
        'notifications': any(keyword in content for keyword in ['notify', 'slack', 'email', 'teams'])
    }

def calculate_cicd_maturity(stages: dict) -> str:
    """Maturity level based on stages"""
    stage_count = sum(stages.values())

    if stage_count >= 7:
        return 'ADVANCED'  # Full pipeline with quality gates + rollback
    elif stage_count >= 5:
        return 'MATURE'  # Build, test, security, deploy
    elif stage_count >= 3:
        return 'BASIC'  # Build, test, deploy
    elif stage_count >= 1:
        return 'MINIMAL'  # At least something
    else:
        return 'NONE'

def calculate_cicd_score(stages: dict) -> int:
    """Score 0-100"""
    weights = {
        'build': 10,
        'test': 20,
        'lint': 10,
        'security_scan': 20,
        'deploy': 15,
        'quality_gates': 15,
        'rollback': 5,
        'notifications': 5
    }

    score = sum(weights[k] for k, v in stages.items() if v)
    return score
```

---

### 2. Test Automation Coverage

**How automated is testing?**

```python
def assess_test_automation() -> dict:
    """Measure test automation maturity"""
    # Detect test framework
    test_configs = {
        'pytest': glob.glob('pytest.ini') + glob.glob('pyproject.toml'),
        'jest': glob.glob('jest.config.*'),
        'unittest': glob.glob('setup.py'),  # Often uses unittest
        'mocha': glob.glob('.mocharc.*'),
        'rspec': glob.glob('.rspec')
    }

    framework = next((k for k, v in test_configs.items() if v), None)

    if not framework:
        return {'maturity': 'NONE', 'score': 0}

    # Count test files
    test_patterns = {
        'pytest': ['**/test_*.py', '**/*_test.py'],
        'jest': ['**/*.test.js', '**/*.test.ts', '**/*.spec.js'],
        'unittest': ['**/test_*.py'],
        'mocha': ['**/test/*.js', '**/*.test.js'],
        'rspec': ['**/spec/**/*_spec.rb']
    }

    test_files = []
    for pattern in test_patterns.get(framework, []):
        test_files.extend(glob.glob(pattern, recursive=True))

    # Count source files
    source_patterns = {
        'pytest': ['**/*.py'],
        'jest': ['**/*.js', '**/*.ts'],
        'unittest': ['**/*.py'],
        'mocha': ['**/*.js'],
        'rspec': ['**/*.rb']
    }

    source_files = []
    for pattern in source_patterns.get(framework, []):
        files = glob.glob(pattern, recursive=True)
        # Exclude tests, node_modules, venv
        source_files.extend([
            f for f in files
            if not any(exclude in f for exclude in ['test', 'node_modules', 'venv', '.venv'])
        ])

    # Calculate ratios
    test_ratio = len(test_files) / len(source_files) if source_files else 0

    return {
        'framework': framework,
        'test_files': len(test_files),
        'source_files': len(source_files),
        'test_ratio': test_ratio,
        'maturity': (
            'EXCELLENT' if test_ratio > 0.5 else
            'GOOD' if test_ratio > 0.3 else
            'BASIC' if test_ratio > 0.1 else
            'POOR'
        ),
        'score': min(100, int(test_ratio * 200))  # 50% ratio = 100 score
    }
```

---

### 3. Infrastructure as Code (IaC) Detection

**Is infrastructure version controlled?**

```python
def assess_iac_presence() -> dict:
    """Detect Infrastructure as Code usage"""
    iac_files = {
        'terraform': glob.glob('**/*.tf', recursive=True) + glob.glob('**/*.tfvars', recursive=True),
        'cloudformation': glob.glob('**/cloudformation/**/*.yaml', recursive=True) + glob.glob('**/*.template', recursive=True),
        'ansible': glob.glob('**/ansible/**/*.yml', recursive=True) + glob.glob('**/playbooks/**/*.yml', recursive=True),
        'pulumi': glob.glob('Pulumi.*.yaml') + glob.glob('**/pulumi/**', recursive=True),
        'cdk': glob.glob('cdk.json') + glob.glob('**/cdk/**', recursive=True),
        'helm': glob.glob('**/charts/**', recursive=True) + glob.glob('Chart.yaml'),
        'kubernetes': glob.glob('**/k8s/**/*.yaml', recursive=True) + glob.glob('**/kubernetes/**/*.yaml', recursive=True)
    }

    detected = {k: v for k, v in iac_files.items() if v}

    if not detected:
        return {'maturity': 'NONE', 'score': 0}

    # Calculate completeness
    categories_covered = len(detected)

    return {
        'tools': list(detected.keys()),
        'file_count': sum(len(files) for files in detected.values()),
        'maturity': (
            'COMPLETE' if categories_covered >= 3 else  # Multiple tools
            'GOOD' if categories_covered >= 2 else
            'BASIC' if categories_covered == 1 else
            'NONE'
        ),
        'score': min(100, categories_covered * 33)  # 3 categories = 100
    }
```

---

### 4. Deployment Automation Assessment

**Can you deploy with one command?**

```python
def assess_deployment_automation() -> dict:
    """Check deployment automation"""
    deployment_indicators = {
        'docker': glob.glob('Dockerfile') + glob.glob('docker-compose.yml'),
        'kubernetes': glob.glob('**/k8s/**', recursive=True),
        'scripts': glob.glob('deploy.sh') + glob.glob('scripts/deploy.*'),
        'makefile': glob.glob('Makefile'),
        'package_json_scripts': check_npm_deploy_script(),
        'github_actions_deploy': check_cicd_deploy_stage('.github/workflows/*.yml'),
        'gitlab_ci_deploy': check_cicd_deploy_stage('.gitlab-ci.yml')
    }

    detected = {k: v for k, v in deployment_indicators.items() if v}

    automation_level = (
        'FULL' if len(detected) >= 3 else  # Container + orchestration + CI/CD
        'PARTIAL' if len(detected) >= 2 else
        'MANUAL' if len(detected) == 1 else
        'NONE'
    )

    return {
        'automation_level': automation_level,
        'methods': list(detected.keys()),
        'score': min(100, len(detected) * 25),  # 4 methods = 100
        'one_command_deploy': automation_level in ['FULL', 'PARTIAL']
    }

def check_npm_deploy_script() -> bool:
    """Check if package.json has deploy script"""
    if not os.path.exists('package.json'):
        return False
    with open('package.json') as f:
        content = json.load(f)
    return 'deploy' in content.get('scripts', {})

def check_cicd_deploy_stage(pattern: str) -> bool:
    """Check if CI/CD config has deploy stage"""
    files = glob.glob(pattern)
    if not files:
        return False
    with open(files[0]) as f:
        content = f.read().lower()
    return 'deploy' in content
```

---

### 5. Developer Experience (DX) Scoring

**How easy is it to develop?**

```python
def assess_developer_experience() -> dict:
    """Score developer experience"""
    dx_indicators = {
        'readme': os.path.exists('README.md'),
        'contributing': os.path.exists('CONTRIBUTING.md'),
        'setup_script': any(os.path.exists(f) for f in ['setup.sh', 'setup.py', 'Makefile']),
        'pre_commit': os.path.exists('.pre-commit-config.yaml'),
        'editorconfig': os.path.exists('.editorconfig'),
        'gitignore': os.path.exists('.gitignore'),
        'env_example': os.path.exists('.env.example') or os.path.exists('.env.template'),
        'docker_dev': os.path.exists('docker-compose.dev.yml'),
        'linting': any(os.path.exists(f) for f in ['.eslintrc', '.ruff.toml', 'pyproject.toml']),
        'formatting': any(os.path.exists(f) for f in ['.prettierrc', 'pyproject.toml'])
    }

    present = sum(dx_indicators.values())

    return {
        'indicators_present': present,
        'indicators_total': len(dx_indicators),
        'coverage': (present / len(dx_indicators)) * 100,
        'dx_score': (present / len(dx_indicators)) * 100,
        'maturity': (
            'EXCELLENT' if present >= 8 else
            'GOOD' if present >= 6 else
            'BASIC' if present >= 4 else
            'POOR'
        ),
        'missing': [k for k, v in dx_indicators.items() if not v]
    }
```

---

### 6. AI Readiness Assessment

**Is foundation strong enough for AI?**

```python
def assess_ai_readiness() -> dict:
    """Combine all metrics to determine AI readiness"""
    cicd = assess_cicd_maturity()
    tests = assess_test_automation()
    iac = assess_iac_presence()
    deploy = assess_deployment_automation()
    dx = assess_developer_experience()

    # Weighted score
    ai_readiness_score = (
        cicd['score'] * 0.25 +
        tests['score'] * 0.30 +  # Testing most important
        iac['score'] * 0.15 +
        deploy['score'] * 0.15 +
        dx['dx_score'] * 0.15
    )

    return {
        'ai_readiness_score': ai_readiness_score,
        'readiness_level': (
            'HIGH' if ai_readiness_score >= 75 else
            'MEDIUM' if ai_readiness_score >= 50 else
            'LOW'
        ),
        'verdict': (
            'Strong foundation - AI will amplify benefits' if ai_readiness_score >= 75 else
            'Weak foundation - Improve fundamentals before AI' if ai_readiness_score < 50 else
            'Moderate foundation - Some benefits, some risks'
        ),
        'priority_improvements': generate_priority_improvements(cicd, tests, iac, deploy, dx)
    }

def generate_priority_improvements(cicd, tests, iac, deploy, dx) -> List[str]:
    """What to improve first"""
    improvements = []

    if tests['score'] < 50:
        improvements.append('CRITICAL: Improve test automation (score: {})'.format(tests['score']))

    if cicd['score'] < 60:
        improvements.append('HIGH: Enhance CI/CD pipeline (score: {})'.format(cicd['score']))

    if deploy['automation_level'] in ['MANUAL', 'NONE']:
        improvements.append('HIGH: Automate deployments')

    if dx['dx_score'] < 60:
        improvements.append('MEDIUM: Improve developer experience (score: {})'.format(dx['dx_score']))

    if iac['maturity'] == 'NONE':
        improvements.append('LOW: Add Infrastructure as Code')

    return improvements
```

---

## Patterns

### Complete Platform Maturity Report

```python
def generate_platform_maturity_report() -> dict:
    """Full platform engineering assessment"""
    return {
        'cicd_maturity': assess_cicd_maturity(),
        'test_automation': assess_test_automation(),
        'infrastructure_as_code': assess_iac_presence(),
        'deployment_automation': assess_deployment_automation(),
        'developer_experience': assess_developer_experience(),
        'ai_readiness': assess_ai_readiness(),
        'overall_maturity': calculate_overall_platform_maturity()
    }

def calculate_overall_platform_maturity() -> dict:
    """Overall platform score"""
    cicd = assess_cicd_maturity()
    tests = assess_test_automation()
    iac = assess_iac_presence()
    deploy = assess_deployment_automation()
    dx = assess_developer_experience()

    overall_score = (
        cicd['score'] * 0.25 +
        tests['score'] * 0.25 +
        iac['score'] * 0.15 +
        deploy['score'] * 0.20 +
        dx['dx_score'] * 0.15
    )

    return {
        'overall_score': overall_score,
        'tier': (
            'ELITE' if overall_score >= 80 else
            'HIGH' if overall_score >= 60 else
            'MEDIUM' if overall_score >= 40 else
            'LOW'
        ),
        'dora_correlation': (
            'High performers' if overall_score >= 80 else
            'Medium performers' if overall_score >= 60 else
            'Low performers'
        )
    }
```

---

## Checklist

### CI/CD Maturity
- [ ] CI/CD tool detected
- [ ] Build stage present
- [ ] Test stage present
- [ ] Security scan present
- [ ] Deployment stage present
- [ ] Quality gates configured
- [ ] Rollback capability exists

### Test Automation
- [ ] Test framework configured
- [ ] Test files exist
- [ ] Test-to-source ratio > 0.3
- [ ] Tests run in CI/CD
- [ ] Coverage tracked

### Infrastructure as Code
- [ ] IaC tool detected (Terraform, CloudFormation, etc.)
- [ ] Infrastructure version controlled
- [ ] Multiple environments defined

### Deployment Automation
- [ ] One-command deploy possible
- [ ] Container-based deployment
- [ ] Orchestration configured (K8s, Docker Compose)

### Developer Experience
- [ ] README exists
- [ ] Setup instructions clear
- [ ] Pre-commit hooks configured
- [ ] Linting configured
- [ ] Formatting configured
- [ ] Environment template provided

### AI Readiness
- [ ] Overall score > 75 (high readiness)
- [ ] Test automation strong (> 50)
- [ ] CI/CD mature (> 60)
- [ ] Foundation strong for AI amplification

---

---

## References

- [DORA State of DevOps 2025: Platform Quality & AI Amplification](https://dora.dev/)
- [Team Topologies: Platform Engineering](https://teamtopologies.com/)
- [The DevEx Index: Measuring Developer Experience](https://getdx.com/)
