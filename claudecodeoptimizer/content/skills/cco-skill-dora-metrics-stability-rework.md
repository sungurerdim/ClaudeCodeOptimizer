---
name: dora-metrics-stability-rework
description: Measure and improve software delivery performance through 5 DORA metrics (deployment frequency, lead time, MTTR, change failure rate, rework rate) with stability trend analysis and AI impact assessment
keywords: [DORA metrics, deployment frequency, lead time, MTTR, change failure rate, rework rate, stability, delivery performance, DevOps metrics, CI/CD metrics, AI impact]
category: platform
related_commands:
  action_types: [audit]
  categories: [platform, cicd, git]
pain_points: [4, 6]
---

# DORA Metrics, Stability & Rework Tracking

> **Standards:** Format defined in [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md)  
> **Discovery:** See [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md#18-command-discovery-protocol)


Measure software delivery performance through 5 DORA metrics + stability trends + AI impact.
---

---

## Domain

DevOps teams, CI/CD pipelines, platform engineering, delivery performance measurement.

---

## Purpose

**DORA 2025 Finding:** AI amplifies what exists - strong foundations improve, weak foundations worsen.

**The 5 DORA Metrics (2025):**
1. Deployment Frequency
2. Lead Time for Changes
3. Mean Time to Restore (MTTR)
4. Change Failure Rate
5. **Rework Rate** (NEW in 2025)

**Why Rework Rate Matters:**
- Quantifies unplanned fixes/patches
- Indicates stability trends
- Measures AI's true impact (individual productivity vs organizational stability)

---

## Core Techniques

### 1. Deployment Frequency

**Measure from git tags or CI/CD logs:**

```python
def calculate_deployment_frequency(days: int = 30) -> dict:
    """How often do you deploy to production?"""
    # From git tags
    tags = subprocess.check_output(
        f"git tag --sort=-creatordate --merged main | head -20",
        shell=True
    ).decode().strip().split('\n')

    # Filter production tags (v1.0.0, release-*, etc.)
    prod_tags = [t for t in tags if re.match(r'v\d+\.\d+\.\d+|release-', t)]

    # Get dates
    dates = []
    for tag in prod_tags:
        date_str = subprocess.check_output(
            f"git log -1 --format=%ai {tag}",
            shell=True
        ).decode().strip()
        dates.append(datetime.fromisoformat(date_str.split()[0]))

    # Calculate frequency
    recent_deploys = [d for d in dates if (datetime.now() - d).days <= days]

    return {
        'deployments_per_month': len(recent_deploys) * (30 / days),
        'deployments_last_30_days': len(recent_deploys),
        'elite': len(recent_deploys) >= 30,  # Multiple per day
        'high': 7 <= len(recent_deploys) < 30,  # Weekly+
        'medium': 1 <= len(recent_deploys) < 7,  # Monthly+
        'low': len(recent_deploys) < 1
    }
```

---

### 2. Lead Time for Changes

**Time from commit to production:**

```python
def calculate_lead_time() -> dict:
    """Average time from commit to deploy"""
    # Get last 10 deployments
    tags = subprocess.check_output(
        "git tag --sort=-creatordate | head -10",
        shell=True
    ).decode().strip().split('\n')

    lead_times = []
    for i in range(len(tags) - 1):
        current_tag = tags[i]
        previous_tag = tags[i + 1]

        # Commits between tags
        commits = subprocess.check_output(
            f"git log {previous_tag}..{current_tag} --format=%H",
            shell=True
        ).decode().strip().split('\n')

        # First commit time
        first_commit_time = subprocess.check_output(
            f"git log -1 --format=%ct {commits[-1]}",
            shell=True
        ).decode().strip()

        # Tag time (deploy time)
        tag_time = subprocess.check_output(
            f"git log -1 --format=%ct {current_tag}",
            shell=True
        ).decode().strip()

        lead_time_hours = (int(tag_time) - int(first_commit_time)) / 3600
        lead_times.append(lead_time_hours)

    avg_lead_time = sum(lead_times) / len(lead_times) if lead_times else 0

    return {
        'avg_lead_time_hours': avg_lead_time,
        'elite': avg_lead_time < 24,  # < 1 day
        'high': 24 <= avg_lead_time < 168,  # 1-7 days
        'medium': 168 <= avg_lead_time < 720,  # 1 week - 1 month
        'low': avg_lead_time >= 720
    }
```

---

### 3. Mean Time to Restore (MTTR)

**Time to recover from failure:**

```python
def calculate_mttr() -> dict:
    """Average time to recover from incidents"""
    # Look for hotfix/revert commits
    hotfixes = subprocess.check_output(
        'git log --all --grep="hotfix\\|revert\\|urgent" --since="90 days ago" --format="%H|%ct"',
        shell=True
    ).decode().strip().split('\n')

    if not hotfixes or hotfixes == ['']:
        return {'mttr_hours': 0, 'incidents': 0}

    recovery_times = []
    for hotfix in hotfixes:
        if not hotfix:
            continue
        commit_hash, timestamp = hotfix.split('|')

        # Find previous deploy (tag before this hotfix)
        previous_tag = subprocess.check_output(
            f"git describe --tags --abbrev=0 {commit_hash}^",
            shell=True
        ).decode().strip()

        previous_tag_time = subprocess.check_output(
            f"git log -1 --format=%ct {previous_tag}",
            shell=True
        ).decode().strip()

        recovery_time_hours = (int(timestamp) - int(previous_tag_time)) / 3600
        recovery_times.append(recovery_time_hours)

    avg_mttr = sum(recovery_times) / len(recovery_times) if recovery_times else 0

    return {
        'mttr_hours': avg_mttr,
        'incidents': len(recovery_times),
        'elite': avg_mttr < 1,  # < 1 hour
        'high': 1 <= avg_mttr < 24,  # < 1 day
        'medium': 24 <= avg_mttr < 168,  # < 1 week
        'low': avg_mttr >= 168
    }
```

---

### 4. Change Failure Rate

**% of deployments causing failures:**

```python
def calculate_change_failure_rate() -> dict:
    """% of deploys requiring hotfix"""
    # Get all production tags
    tags = subprocess.check_output(
        "git tag --sort=-creatordate | head -20",
        shell=True
    ).decode().strip().split('\n')

    failures = 0
    for i in range(len(tags) - 1):
        current_tag = tags[i]
        next_tag = tags[i + 1]

        # Check for hotfix commits between tags
        hotfix_commits = subprocess.check_output(
            f'git log {next_tag}..{current_tag} --grep="hotfix\\|urgent\\|fix.*bug" --oneline',
            shell=True
        ).decode().strip()

        if hotfix_commits:
            failures += 1

    change_failure_rate = (failures / len(tags)) * 100 if tags else 0

    return {
        'change_failure_rate': change_failure_rate,
        'failed_deployments': failures,
        'total_deployments': len(tags),
        'elite': change_failure_rate < 15,
        'high': 15 <= change_failure_rate < 30,
        'medium': 30 <= change_failure_rate < 45,
        'low': change_failure_rate >= 45
    }
```

---

### 5. Rework Rate (NEW 2025 Metric)

**Unplanned fixes after deployment:**

```python
def calculate_rework_rate() -> dict:
    """% of work that is rework (NEW DORA metric 2025)"""
    # Get commits in last 30 days
    all_commits = subprocess.check_output(
        'git log --since="30 days ago" --format="%H"',
        shell=True
    ).decode().strip().split('\n')

    # Identify rework commits
    rework_patterns = [
        r'fix.*bug',
        r'hotfix',
        r'patch',
        r'urgent',
        r'revert',
        r'rollback',
        r'critical.*fix'
    ]

    rework_commits = subprocess.check_output(
        f'git log --since="30 days ago" --grep="{"\\|".join(rework_patterns)}" --format="%H"',
        shell=True
    ).decode().strip().split('\n')

    rework_commits = [c for c in rework_commits if c]  # Remove empty

    rework_rate = (len(rework_commits) / len(all_commits)) * 100 if all_commits else 0

    return {
        'rework_rate': rework_rate,
        'rework_commits': len(rework_commits),
        'total_commits': len(all_commits),
        'elite': rework_rate < 10,
        'high': 10 <= rework_rate < 20,
        'medium': 20 <= rework_rate < 30,
        'low': rework_rate >= 30
    }
```

---

### 6. Stability Trend Analysis

**Are things getting better or worse?**

```python
def analyze_stability_trend() -> dict:
    """Compare last 30 days vs previous 30 days"""
    current_period = calculate_all_metrics(days=30)
    previous_period = calculate_all_metrics(days=60, offset=30)

    return {
        'deployment_frequency': {
            'current': current_period['deploy_freq'],
            'previous': previous_period['deploy_freq'],
            'trend': 'improving' if current_period['deploy_freq'] > previous_period['deploy_freq'] else 'declining'
        },
        'rework_rate': {
            'current': current_period['rework_rate'],
            'previous': previous_period['rework_rate'],
            'trend': 'improving' if current_period['rework_rate'] < previous_period['rework_rate'] else 'declining'
        },
        'change_failure_rate': {
            'current': current_period['cfr'],
            'previous': previous_period['cfr'],
            'trend': 'improving' if current_period['cfr'] < previous_period['cfr'] else 'declining'
        }
    }
```

---

### 7. AI Impact Assessment

**How is AI affecting delivery?**

```python
def assess_ai_impact() -> dict:
    """Correlate AI adoption with DORA metrics"""
    # Detect AI-generated commits (simplified)
    ai_commits = subprocess.check_output(
        'git log --since="90 days ago" --all -S"AI-generated\\|Co-authored-by.*Copilot" --format="%H"',
        shell=True
    ).decode().strip().split('\n')

    total_commits = subprocess.check_output(
        'git log --since="90 days ago" --format="%H"',
        shell=True
    ).decode().strip().split('\n')

    ai_percentage = (len(ai_commits) / len(total_commits)) * 100 if total_commits else 0

    # Get DORA metrics
    metrics = calculate_all_metrics()

    return {
        'ai_adoption_percentage': ai_percentage,
        'individual_productivity': 'high' if metrics['deploy_freq'] > 10 else 'medium',
        'organizational_stability': 'high' if metrics['rework_rate'] < 15 else 'low',
        'amplification_effect': determine_amplification(metrics, ai_percentage),
        'verdict': (
            'AI amplifying benefits' if metrics['rework_rate'] < 15 else
            'AI amplifying problems - strengthen foundation'
        )
    }

def determine_amplification(metrics: dict, ai_pct: float) -> str:
    """DORA 2025: AI amplifies existing patterns"""
    if ai_pct > 30:  # Heavy AI usage
        if metrics['rework_rate'] < 15 and metrics['cfr'] < 20:
            return 'POSITIVE - Strong foundation + AI = Benefits'
        else:
            return 'NEGATIVE - Weak foundation + AI = Problems'
    return 'LOW AI USAGE - Insufficient data'
```

---

## Patterns

### Complete DORA Dashboard

```python
def generate_dora_report() -> dict:
    """Full DORA metrics report"""
    return {
        'deployment_frequency': calculate_deployment_frequency(),
        'lead_time': calculate_lead_time(),
        'mttr': calculate_mttr(),
        'change_failure_rate': calculate_change_failure_rate(),
        'rework_rate': calculate_rework_rate(),  # NEW 2025
        'stability_trend': analyze_stability_trend(),
        'ai_impact': assess_ai_impact(),
        'overall_performance': classify_performance()
    }

def classify_performance() -> str:
    """DORA performance classification"""
    metrics = calculate_all_metrics()

    elite_count = sum([
        metrics['deploy_freq'] >= 30,
        metrics['lead_time'] < 24,
        metrics['mttr'] < 1,
        metrics['cfr'] < 15,
        metrics['rework_rate'] < 10
    ])

    if elite_count >= 4:
        return 'ELITE'
    elif elite_count >= 3:
        return 'HIGH'
    elif elite_count >= 2:
        return 'MEDIUM'
    else:
        return 'LOW'
```

---

## Checklist

### Metrics Collection
- [ ] Deployment frequency measured
- [ ] Lead time calculated
- [ ] MTTR tracked
- [ ] Change failure rate determined
- [ ] Rework rate calculated (2025 metric)

### Trend Analysis
- [ ] Current vs previous period compared
- [ ] Stability trend identified (improving/declining)
- [ ] Root causes investigated

### AI Impact
- [ ] AI adoption percentage measured
- [ ] Individual productivity assessed
- [ ] Organizational stability assessed
- [ ] Amplification effect determined

### Performance Classification
- [ ] DORA tier identified (Elite/High/Medium/Low)
- [ ] Action plan created for improvement

---

---

## References

- [DORA State of DevOps 2025](https://dora.dev/)
- [Google Cloud: DORA Metrics](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
- [Accelerate (Book): Building and Scaling High-Performing Technology Organizations](https://itrevolution.com/product/accelerate/)
