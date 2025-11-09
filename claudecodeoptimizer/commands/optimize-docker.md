---
id: cco-optimize-docker
description: Optimize Dockerfiles for faster builds, smaller images, and better security
category: devops
priority: high
---

# Optimize Docker - Dockerfile Best Practices & Optimization

Analyze and optimize Dockerfiles for **${PROJECT_NAME}** to improve build speed, reduce image size, and enhance security.

**Project Type:** ${PROJECT_TYPE}
**Services:** ${SERVICES_COUNT}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Comprehensive Dockerfile optimization across 7 dimensions:
1. **Multi-Stage Builds** - Reduce final image size by 50-90%
2. **Layer Caching** - Speed up builds by 3-10x
3. **Base Image Security** - Use minimal, secure base images
4. **Layer Consolidation** - Minimize layers for smaller images
5. **Build Context** - Optimize .dockerignore
6. **Security Practices** - Non-root users, secrets management
7. **Size Reduction** - Remove build artifacts, use Alpine variants

**Output:** Optimized Dockerfiles with performance and security improvements.

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast Dockerfile scanning
- Layer analysis and metrics
- Security baseline checks

**Analysis & Reasoning**: Sonnet (Plan agent)
- Multi-stage build optimization
- Security best practices recommendations
- Strategic Docker improvements

**Execution Pattern**:
1. Launch Haiku agents to analyze Dockerfiles (parallel)
2. Calculate image size and layer metrics
3. Use Sonnet for optimization strategy
4. Generate Docker optimization report with before/after comparison

---

## Phase 1: Discover Dockerfiles

Find all Dockerfiles in the project:

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path

project_root = Path(".").resolve()
project_name = project_root.name

print(f"=== Docker Optimization for {project_name} ===\n")

# Find all Dockerfiles
print("Searching for Dockerfiles...\n")
```

**Use Glob to find Dockerfiles:**

```
**/Dockerfile
**/Dockerfile.*
**/*.dockerfile
```

Common locations:
- `./Dockerfile` (root)
- `./services/*/Dockerfile` (microservices)
- `./docker/Dockerfile.*` (variants)

```python
# Example results
dockerfiles = [
    "Dockerfile",
    "services/api/Dockerfile",
    "services/worker/Dockerfile",
    "docker/Dockerfile.dev"
]

print(f"Found {len(dockerfiles)} Dockerfiles:\n")
for df in dockerfiles:
    print(f"  - {df}")
print()
```

---

## Phase 2: Analyze Dockerfiles

Analyze each Dockerfile for optimization opportunities:

```python
print(f"=== Analyzing Dockerfiles ===\n")

# Analysis categories
analysis_results = {
    "multi_stage": [],      # Missing multi-stage builds
    "base_image": [],       # Non-optimal base images
    "layer_cache": [],      # Poor layer ordering
    "layer_count": [],      # Too many layers
    "dockerignore": [],     # Missing .dockerignore
    "security": [],         # Security issues
    "size": []              # Size optimization opportunities
}
```

### 2.1 Multi-Stage Build Detection

**Use Grep to detect multi-stage builds:**

```
Pattern: ^FROM .* AS
Output: files_with_matches
```

If no matches → Single-stage build (not optimal)

```python
# Example analysis
single_stage = [
    "services/api/Dockerfile",
    "services/worker/Dockerfile"
]

multi_stage = [
    "Dockerfile"  # Has "FROM node:18 AS builder"
]

print("Multi-Stage Build Analysis:")
print(f"  Single-stage (needs optimization): {len(single_stage)}")
print(f"  Multi-stage (good): {len(multi_stage)}")
print()

if single_stage:
    analysis_results["multi_stage"] = [
        {
            "file": df,
            "severity": "HIGH",
            "issue": "Single-stage build",
            "impact": "Includes build tools in final image (50-200MB overhead)",
            "recommendation": "Use multi-stage build to separate build and runtime"
        }
        for df in single_stage
    ]
```

### 2.2 Base Image Analysis

**Use Grep to find base images:**

```
Pattern: ^FROM
Output: content
```

Check for:
- **Alpine variants** (smallest) - ✅ GOOD
- **Slim variants** (small) - ✅ ACCEPTABLE
- **Full images** (large) - ⚠️ NEEDS OPTIMIZATION
- **Latest tag** - ❌ SECURITY RISK
- **Outdated versions** - ⚠️ UPDATE NEEDED

```python
base_image_patterns = {
    "alpine": "EXCELLENT",     # node:18-alpine (50MB)
    "slim": "GOOD",            # python:3.11-slim (120MB)
    "bookworm": "ACCEPTABLE",  # python:3.11-bookworm (180MB)
    "full": "POOR",            # python:3.11 (1GB)
    "latest": "CRITICAL"       # python:latest (security risk)
}

print("Base Image Analysis:")

# Example findings
base_images = [
    {
        "file": "services/api/Dockerfile",
        "image": "python:3.11",
        "size_estimate": "1.0 GB",
        "rating": "POOR",
        "recommended": "python:3.11-alpine",
        "savings": "~950 MB"
    },
    {
        "file": "services/worker/Dockerfile",
        "image": "node:latest",
        "size_estimate": "unknown",
        "rating": "CRITICAL",
        "recommended": "node:18-alpine",
        "issue": "Using :latest tag (unpredictable, security risk)"
    }
]

for img in base_images:
    print(f"  {img['file']}:")
    print(f"    Current: {img['image']} ({img.get('size_estimate', 'unknown')})")
    print(f"    Rating: {img['rating']}")
    print(f"    Recommended: {img['recommended']}")
    if 'savings' in img:
        print(f"    Savings: {img['savings']}")
    if 'issue' in img:
        print(f"    Issue: {img['issue']}")
    print()

analysis_results["base_image"] = base_images
```

### 2.3 Layer Caching Analysis

Check if dependency installation is optimized for caching:

**Python Best Practice:**
```dockerfile
# ❌ BAD: Copies everything before installing deps
COPY . /app
RUN pip install -r requirements.txt

# ✅ GOOD: Copies only requirements first
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
```

**Node.js Best Practice:**
```dockerfile
# ❌ BAD
COPY . /app
RUN npm install

# ✅ GOOD
COPY package.json package-lock.json /app/
RUN npm ci
COPY . /app
```

**Use Grep to detect poor caching:**

```
Pattern: COPY \. /app\nRUN (pip install|npm install)
Multiline: true
```

```python
print("Layer Caching Analysis:")

caching_issues = [
    {
        "file": "services/api/Dockerfile",
        "severity": "HIGH",
        "issue": "Copies all files before installing dependencies",
        "impact": "Cache invalidated on every code change (3-5 min rebuild)",
        "fix": "Copy requirements.txt first, install deps, then copy code"
    }
]

for issue in caching_issues:
    print(f"  {issue['file']}:")
    print(f"    Issue: {issue['issue']}")
    print(f"    Impact: {issue['impact']}")
    print(f"    Fix: {issue['fix']}")
    print()

analysis_results["layer_cache"] = caching_issues
```

### 2.4 Layer Count Analysis

**Use Grep to count RUN commands:**

```
Pattern: ^RUN
Output: count
```

Optimal: 5-10 layers (balance between caching and image size)
Too many: >15 layers (consolidate with && chaining)

```python
print("Layer Count Analysis:")

layer_counts = [
    {
        "file": "services/api/Dockerfile",
        "run_count": 18,
        "severity": "MEDIUM",
        "recommendation": "Consolidate RUN commands with && to reduce layers"
    }
]

for lc in layer_counts:
    print(f"  {lc['file']}: {lc['run_count']} RUN commands")
    if lc['run_count'] > 15:
        print(f"    {lc['recommendation']}")
    print()

analysis_results["layer_count"] = layer_counts
```

### 2.5 .dockerignore Detection

Check if .dockerignore exists:

```python
print(".dockerignore Analysis:")

dockerignore_path = project_root / ".dockerignore"

if not dockerignore_path.exists():
    print("  ❌ Missing .dockerignore")
    print("  Impact: Large build context (slow builds, wasted bandwidth)")
    print()

    analysis_results["dockerignore"] = [{
        "severity": "MEDIUM",
        "issue": "No .dockerignore file",
        "impact": "Build context includes unnecessary files (node_modules, .git, __pycache__)",
        "recommendation": "Create .dockerignore with common exclusions"
    }]
else:
    print("  ✅ .dockerignore exists")

    # Check for common patterns
    content = dockerignore_path.read_text()
    missing_patterns = []

    recommended = [
        "node_modules", ".git", "__pycache__", "*.pyc",
        ".pytest_cache", "coverage", ".env", "*.log"
    ]

    for pattern in recommended:
        if pattern not in content:
            missing_patterns.append(pattern)

    if missing_patterns:
        print(f"  ⚠️  Missing recommended patterns: {', '.join(missing_patterns)}")
        analysis_results["dockerignore"] = [{
            "severity": "LOW",
            "issue": f"Incomplete .dockerignore",
            "missing": missing_patterns,
            "recommendation": "Add missing patterns to reduce build context"
        }]
    else:
        print("  ✅ Contains recommended patterns")
    print()
```

### 2.6 Security Analysis

**Use Grep to detect security issues:**

Patterns to check:
1. **Running as root:**
```
Pattern: ^USER root
Or missing: ^USER
```

2. **Hardcoded secrets:**
```
Pattern: (ENV|ARG) .*(PASSWORD|SECRET|TOKEN|KEY)=
```

3. **Unnecessary privileges:**
```
Pattern: --privileged
```

```python
print("Security Analysis:")

security_issues = []

# Example findings
security_issues.append({
    "file": "services/api/Dockerfile",
    "severity": "HIGH",
    "issue": "Running as root user",
    "risk": "Container compromise = root access",
    "fix": "Add USER directive to run as non-root"
})

security_issues.append({
    "file": "services/worker/Dockerfile",
    "severity": "CRITICAL",
    "issue": "Hardcoded API_KEY in ENV",
    "risk": "Secret exposed in image layers",
    "fix": "Use build args or runtime secrets"
})

for issue in security_issues:
    print(f"  [{issue['severity']}] {issue['file']}:")
    print(f"    Issue: {issue['issue']}")
    print(f"    Risk: {issue['risk']}")
    print(f"    Fix: {issue['fix']}")
    print()

analysis_results["security"] = security_issues
```

### 2.7 Size Optimization Analysis

Check for size optimization opportunities:

**Use Grep to detect:**

1. **Missing cleanup after installs:**
```
Pattern: apt-get install.*\n(?!.*rm -rf)
Multiline: true
```

2. **Build artifacts in final image:**
```
Pattern: (gcc|g\+\+|make|build-essential)
```

3. **Development dependencies:**
```
Pattern: pip install.*dev
Pattern: npm install(?!.*--production)
```

```python
print("Size Optimization Analysis:")

size_issues = [
    {
        "file": "services/api/Dockerfile",
        "severity": "MEDIUM",
        "issue": "apt-get without cleanup",
        "waste": "~50-100 MB",
        "fix": "Add: && rm -rf /var/lib/apt/lists/*"
    },
    {
        "file": "services/worker/Dockerfile",
        "severity": "MEDIUM",
        "issue": "Installing dev dependencies in production",
        "waste": "~100-200 MB",
        "fix": "Use: npm ci --production"
    }
]

for issue in size_issues:
    print(f"  {issue['file']}:")
    print(f"    Issue: {issue['issue']}")
    print(f"    Waste: {issue['waste']}")
    print(f"    Fix: {issue['fix']}")
    print()

analysis_results["size"] = size_issues
```

---

## Phase 3: Summarize Findings

Calculate total issues and potential improvements:

```python
print(f"=== Optimization Summary ===\n")

# Count issues by severity
severity_counts = {
    "CRITICAL": 0,
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0
}

total_issues = 0

for category, issues in analysis_results.items():
    for issue in issues:
        severity = issue.get("severity", "MEDIUM")
        severity_counts[severity] += 1
        total_issues += 1

print(f"Total Issues: {total_issues}\n")
print("By Severity:")
for severity, count in severity_counts.items():
    if count > 0:
        print(f"  {severity}: {count}")
print()

# Estimate improvements
print("Potential Improvements:")
print()

# Size savings
total_size_savings = 0
for issue in analysis_results.get("base_image", []):
    if "savings" in issue:
        # Parse "~950 MB" → 950
        savings_str = issue["savings"].replace("~", "").replace("MB", "").strip()
        total_size_savings += int(savings_str)

for issue in analysis_results.get("size", []):
    if "waste" in issue:
        # Parse "~50-100 MB" → 75 (average)
        waste_str = issue["waste"].replace("~", "").replace("MB", "").strip()
        if "-" in waste_str:
            low, high = waste_str.split("-")
            total_size_savings += (int(low) + int(high)) // 2
        else:
            total_size_savings += int(waste_str)

if total_size_savings > 0:
    print(f"  Image Size Reduction: ~{total_size_savings} MB per service")
    print(f"  Total Reduction ({len(dockerfiles)} services): ~{total_size_savings * len(dockerfiles)} MB")
    print()

# Build time savings
cache_issues = len(analysis_results.get("layer_cache", []))
if cache_issues > 0:
    print(f"  Build Time Reduction: 3-5 minutes per rebuild")
    print(f"  (via improved layer caching)")
    print()

# Security improvements
security_count = len(analysis_results.get("security", []))
if security_count > 0:
    print(f"  Security Improvements: {security_count} vulnerabilities fixed")
    print()
```

---

## Phase 4: Generate Optimized Dockerfiles

Show before/after examples for each optimization:

```python
print(f"=== Optimization Examples ===\n")
```

### Example 1: Multi-Stage Build (Python)

```python
print("Example 1: Multi-Stage Build (Python)\n")
print("services/api/Dockerfile\n")
```

**Before (Single-Stage):**
```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "main.py"]
```

**After (Multi-Stage):**
```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-alpine

WORKDIR /app

# Copy only dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Run as non-root
RUN adduser -D appuser
USER appuser

CMD ["python", "main.py"]
```

**Improvements:**
- Image size: 1.0 GB → 150 MB (85% reduction)
- Security: Non-root user
- Base image: Alpine variant

---

### Example 2: Layer Caching (Node.js)

```python
print("\nExample 2: Layer Caching (Node.js)\n")
print("services/worker/Dockerfile\n")
```

**Before (Poor Caching):**
```dockerfile
FROM node:18

WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "index.js"]
```

**After (Optimized Caching):**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Cache dependencies separately
COPY package.json package-lock.json ./
RUN npm ci --production

# Copy application code
COPY . .

# Runtime stage
FROM node:18-alpine

WORKDIR /app

# Copy only node_modules and app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app .

# Run as non-root
USER node

CMD ["node", "index.js"]
```

**Improvements:**
- Build time: 5 min → 30 sec (10x faster on code changes)
- Image size: 900 MB → 120 MB (87% reduction)
- Security: Non-root user
- Caching: Dependencies cached separately

---

### Example 3: Layer Consolidation

```python
print("\nExample 3: Layer Consolidation\n")
```

**Before (Too Many Layers):**
```dockerfile
FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y build-essential
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install setuptools
```

**After (Consolidated):**
```dockerfile
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip wheel setuptools
```

**Improvements:**
- Layers: 7 → 1 (smaller image)
- Size: Cleanup removes ~50 MB
- Best practice: Single RUN for related commands

---

### Example 4: .dockerignore

```python
print("\nExample 4: .dockerignore\n")
```

**Create/Update .dockerignore:**

```dockerignore
# Python
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.coverage
htmlcov/
*.egg-info/
dist/
build/

# Node.js
node_modules/
npm-debug.log
yarn-error.log

# Environment
.env
.env.local
*.env

# Git
.git/
.gitignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Documentation
*.md
docs/

# Tests (if not needed in image)
tests/
*.test.js
*.spec.js

# CI/CD
.github/
.gitlab-ci.yml
```

**Improvements:**
- Build context: ~500 MB → ~50 MB (10x reduction)
- Build speed: Faster file transfer to Docker daemon

---

## Phase 5: Security Hardening

Generate security-hardened Dockerfile template:

```python
print(f"\n=== Security Hardening ===\n")
print("Best Practices Template:\n")
```

```dockerfile
# Use specific version (not :latest)
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache gcc musl-dev

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-alpine

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Create non-root user
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port (documentation)
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
```

**Security Features:**
1. ✅ Specific version tag (not :latest)
2. ✅ Multi-stage build (no build tools in final image)
3. ✅ Minimal base image (Alpine)
4. ✅ Non-root user
5. ✅ No secrets in ENV/ARG
6. ✅ Health check
7. ✅ Minimal attack surface

---

## Phase 6: Apply Optimizations

Offer to apply optimizations automatically:

```python
print(f"\n=== Apply Optimizations ===\n")

print(f"Found {total_issues} optimization opportunities:\n")

# Group by file
files_to_optimize = set()
for category, issues in analysis_results.items():
    for issue in issues:
        if "file" in issue:
            files_to_optimize.add(issue["file"])

print("Files that can be optimized:")
for i, file in enumerate(sorted(files_to_optimize), 1):
    print(f"{i}. {file}")
print()

print("Optimization modes:")
print("1. Generate optimized Dockerfiles (--generate)")
print("2. Show recommendations only (default)")
print("3. Interactive mode (--interactive)")
print()
```

**Use AskUserQuestion for auto-apply:**

```
Question: Apply optimizations automatically?
Options:
1. label: "Generate optimized files"
   description: "Create .optimized versions alongside existing Dockerfiles"

2. label: "Show recommendations only"
   description: "Display optimization guide without modifying files"

3. label: "Interactive mode"
   description: "Review each optimization before applying"
```

If user selects "Generate optimized files":

```python
print("Generating optimized Dockerfiles...\n")

for dockerfile in files_to_optimize:
    optimized_path = dockerfile.replace("Dockerfile", "Dockerfile.optimized")

    print(f"  ✓ {dockerfile} → {optimized_path}")

    # Generate optimized version based on analysis
    # (Implementation would use templates based on language)

print()
print("Review optimized files, then:")
print("1. Test with: docker build -f Dockerfile.optimized .")
print("2. If successful: mv Dockerfile.optimized Dockerfile")
print("3. Commit changes")
```

---

## Phase 7: Validation (Optional)

Offer to validate optimized Dockerfiles:

```python
print(f"\n=== Validation ===\n")

print("To validate optimized Dockerfiles:")
print()
print("# Test build")
print("docker build -f Dockerfile.optimized -t myapp:optimized .")
print()
print("# Compare sizes")
print("docker images | grep myapp")
print()
print("# Test functionality")
print("docker run --rm myapp:optimized")
print()
```

**Metrics to compare:**

```python
print("Compare metrics:\n")

comparison = [
    {
        "metric": "Image Size",
        "before": "1.2 GB",
        "after": "150 MB",
        "improvement": "87% reduction"
    },
    {
        "metric": "Build Time (fresh)",
        "before": "5m 30s",
        "after": "2m 10s",
        "improvement": "60% faster"
    },
    {
        "metric": "Build Time (cached)",
        "before": "5m 00s",
        "after": "15s",
        "improvement": "95% faster"
    },
    {
        "metric": "Layers",
        "before": "18",
        "after": "8",
        "improvement": "56% reduction"
    },
    {
        "metric": "Security Issues",
        "before": "3",
        "after": "0",
        "improvement": "100% fixed"
    }
]

for comp in comparison:
    print(f"{comp['metric']}:")
    print(f"  Before: {comp['before']}")
    print(f"  After:  {comp['after']}")
    print(f"  Improvement: {comp['improvement']}")
    print()
```

---

## Best Practices Summary

```python
print(f"=== Docker Best Practices ===\n")
```

### Multi-Stage Builds
```dockerfile
# Separate build and runtime stages
FROM language:version AS builder
# ... build steps ...

FROM language:version-alpine
COPY --from=builder /app /app
```

### Layer Caching
```dockerfile
# Copy dependency files first
COPY package.json package-lock.json ./
RUN npm ci

# Then copy application code
COPY . .
```

### Base Images
```dockerfile
# Prefer Alpine variants
FROM python:3.11-alpine  # ✅ 50 MB
FROM node:18-alpine      # ✅ 120 MB

# Avoid full images
FROM python:3.11         # ❌ 1 GB
FROM node:18             # ❌ 900 MB
```

### Security
```dockerfile
# Non-root user
RUN adduser -D appuser
USER appuser

# Specific versions
FROM python:3.11-alpine  # ✅
FROM python:latest       # ❌

# No secrets
ARG API_KEY              # ❌ Exposed in history
# Use runtime secrets instead
```

### Size Optimization
```dockerfile
# Clean up in same layer
RUN apt-get update && \
    apt-get install -y pkg && \
    rm -rf /var/lib/apt/lists/*

# Use --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt

# Production dependencies only
RUN npm ci --production
```

### .dockerignore
```dockerignore
node_modules/
__pycache__/
.git/
.env
*.log
tests/
```

---

## Output Example

```
=== Docker Optimization for backend ===

Searching for Dockerfiles...

Found 4 Dockerfiles:
  - Dockerfile
  - services/api/Dockerfile
  - services/worker/Dockerfile
  - docker/Dockerfile.dev

=== Analyzing Dockerfiles ===

Multi-Stage Build Analysis:
  Single-stage (needs optimization): 2
  Multi-stage (good): 2

Base Image Analysis:
  services/api/Dockerfile:
    Current: python:3.11 (1.0 GB)
    Rating: POOR
    Recommended: python:3.11-alpine
    Savings: ~950 MB

  services/worker/Dockerfile:
    Current: node:latest (unknown)
    Rating: CRITICAL
    Recommended: node:18-alpine
    Issue: Using :latest tag (unpredictable, security risk)

Layer Caching Analysis:
  services/api/Dockerfile:
    Issue: Copies all files before installing dependencies
    Impact: Cache invalidated on every code change (3-5 min rebuild)
    Fix: Copy requirements.txt first, install deps, then copy code

Layer Count Analysis:
  services/api/Dockerfile: 18 RUN commands
    Consolidate RUN commands with && to reduce layers

.dockerignore Analysis:
  ❌ Missing .dockerignore
  Impact: Build context includes unnecessary files (node_modules, .git, __pycache__)

Security Analysis:
  [HIGH] services/api/Dockerfile:
    Issue: Running as root user
    Risk: Container compromise = root access
    Fix: Add USER directive to run as non-root

  [CRITICAL] services/worker/Dockerfile:
    Issue: Hardcoded API_KEY in ENV
    Risk: Secret exposed in image layers
    Fix: Use build args or runtime secrets

Size Optimization Analysis:
  services/api/Dockerfile:
    Issue: apt-get without cleanup
    Waste: ~50-100 MB
    Fix: Add: && rm -rf /var/lib/apt/lists/*

=== Optimization Summary ===

Total Issues: 12

By Severity:
  CRITICAL: 2
  HIGH: 4
  MEDIUM: 5
  LOW: 1

Potential Improvements:

  Image Size Reduction: ~1050 MB per service
  Total Reduction (4 services): ~4200 MB

  Build Time Reduction: 3-5 minutes per rebuild
  (via improved layer caching)

  Security Improvements: 6 vulnerabilities fixed

=== Apply Optimizations ===

Found 12 optimization opportunities:

Files that can be optimized:
1. Dockerfile
2. docker/Dockerfile.dev
3. services/api/Dockerfile
4. services/worker/Dockerfile

Optimization modes:
1. Generate optimized Dockerfiles (--generate)
2. Show recommendations only (default)
3. Interactive mode (--interactive)

[User selects "Generate optimized files"]

Generating optimized Dockerfiles...

  ✓ services/api/Dockerfile → services/api/Dockerfile.optimized
  ✓ services/worker/Dockerfile → services/worker/Dockerfile.optimized

Review optimized files, then:
1. Test with: docker build -f Dockerfile.optimized .
2. If successful: mv Dockerfile.optimized Dockerfile
3. Commit changes
```

---

## Quick Optimization Modes

```bash
# Full analysis (default)
/cco-optimize-docker

# Generate optimized Dockerfiles
/cco-optimize-docker --generate

# Interactive mode (review each change)
/cco-optimize-docker --interactive

# Specific service only
/cco-optimize-docker --service=api

# Security audit only
/cco-optimize-docker --security-only

# Size optimization only
/cco-optimize-docker --size-only
```

---

## Integration with Other Commands

```bash
# After optimization, verify security
/cco-optimize-docker --generate
/cco-audit-security

# Complete DevOps workflow
/cco-optimize-docker && /cco-generate-ci && /cco-optimize-deps

# Before deployment
/cco-optimize-docker --security-only
```

---

**Optimization Philosophy:** Small images build fast, deploy fast, run secure. Multi-stage everything!
