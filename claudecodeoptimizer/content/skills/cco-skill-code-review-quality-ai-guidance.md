---
name: code-review-quality-ai-guidance
description: Assess and improve code review quality through commit analysis, PR metrics, review depth scoring, and AI-specific review guidance to combat the 2025 review decline (-27% comments despite +20% PRs)
keywords: [code review, PR quality, review depth, commit quality, review metrics, AI code review, LGTM, substantive review, reviewer diversity]
category: quality
related_commands:
  action_types: [audit, generate]
  categories: [code-review, git]
pain_points: [11, 12]
---

# Code Review Quality & AI Review Guidance

Assess and improve code review quality + AI-specific review patterns.
---

## Standard Structure

**This skill follows [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md):**

- **Standard sections** - Domain, Purpose, Core Techniques, Anti-Patterns, Checklist
- **Code example format** - Bad/Good pattern with specific examples
- **Detection pattern format** - Python functions with Finding objects
- **Checklist format** - Specific, verifiable items

**See STANDARDS_SKILLS.md for format details. Only skill-specific content is documented below.**

---

## Domain

Development teams using Pull Requests, code review processes, Git workflows.

---

## Purpose

**2025 Crisis:** Code review quality is declining despite increased velocity:
- Comments on commits: **-27%** (down)
- Pull requests: **+20%** (up)
- Commits: **+25%** (up to 1 billion in 2025)

**Problem:** AI accelerates development velocity, but review quality suffers. More PRs, less meaningful review = technical debt and bugs slip through.

**This skill helps:** Measure review quality, identify shallow reviews, generate AI-specific review checklists.

---

## Core Techniques

### 1. Commit Message Quality Analysis

**Substantive vs LGTM:**

```python
def analyze_commit_message_quality() -> dict:
    """Measure commit message depth"""
    commits = subprocess.check_output(
        'git log --since="30 days ago" --format="%H|%s|%b"',
        shell=True
    ).decode().strip().split('\n\n')

    substantive = 0
    trivial = 0
    lengths = []

    TRIVIAL_PATTERNS = [
        r'^(lgtm|looks good|approved|✅|👍|ok|fine|good)$',
        r'^wip$',
        r'^fix$',
        r'^update$',
        r'^typo$'
    ]

    for commit in commits:
        if not commit:
            continue

        parts = commit.split('|', 2)
        if len(parts) < 2:
            continue

        subject = parts[1].lower().strip()
        body = parts[2] if len(parts) > 2 else ''

        # Check if trivial
        is_trivial = any(re.match(pattern, subject, re.I) for pattern in TRIVIAL_PATTERNS)

        if is_trivial and not body:
            trivial += 1
        else:
            substantive += 1
            lengths.append(len(subject) + len(body))

    avg_length = sum(lengths) / len(lengths) if lengths else 0

    return {
        'substantive_commits': substantive,
        'trivial_commits': trivial,
        'trivial_percentage': (trivial / (substantive + trivial)) * 100 if (substantive + trivial) > 0 else 0,
        'avg_message_length': avg_length,
        'quality_score': 100 - ((trivial / (substantive + trivial)) * 100) if (substantive + trivial) > 0 else 0
    }
```

---

### 2. Review Time Distribution

**Too fast = shallow, too slow = bottleneck:**

```python
def analyze_review_time() -> dict:
    """Measure PR merge speed (git log based)"""
    # Get merge commits
    merges = subprocess.check_output(
        'git log --merges --since="30 days ago" --format="%H|%ct|%s"',
        shell=True
    ).decode().strip().split('\n')

    review_times = []
    for merge in merges:
        if not merge:
            continue

        parts = merge.split('|')
        if len(parts) < 3:
            continue

        merge_hash, merge_time, subject = parts

        # Find first commit in this PR (simplified: parent commit)
        try:
            parent_hash = subprocess.check_output(
                f'git log -1 --format=%P {merge_hash}',
                shell=True
            ).decode().strip().split()[1]  # Second parent = feature branch

            first_commit_time = subprocess.check_output(
                f'git log -1 --format=%ct {parent_hash}',
                shell=True
            ).decode().strip()

            review_time_hours = (int(merge_time) - int(first_commit_time)) / 3600
            review_times.append(review_time_hours)
        except:
            continue  # Skip malformed merges

    if not review_times:
        return {'avg_review_time_hours': 0, 'reviews': 0}

    avg_review_time = sum(review_times) / len(review_times)

    # Classify
    too_fast = [t for t in review_times if t < 1]  # < 1 hour
    optimal = [t for t in review_times if 1 <= t <= 24]  # 1-24 hours
    too_slow = [t for t in review_times if t > 48]  # > 2 days

    return {
        'avg_review_time_hours': avg_review_time,
        'total_reviews': len(review_times),
        'too_fast': len(too_fast),
        'optimal': len(optimal),
        'too_slow': len(too_slow),
        'too_fast_percentage': (len(too_fast) / len(review_times)) * 100,
        'quality_risk': 'HIGH' if len(too_fast) > len(review_times) * 0.3 else 'LOW'
    }
```

---

### 3. Reviewer Diversity

**Echo chamber detection:**

```python
def analyze_reviewer_diversity() -> dict:
    """Check if same people always review"""
    # Get commit authors and committers (reviewers merge = commit)
    commits = subprocess.check_output(
        'git log --since="30 days ago" --format="%an|%cn"',
        shell=True
    ).decode().strip().split('\n')

    authors = set()
    committers = set()  # Usually reviewers who merge
    pairs = []

    for commit in commits:
        if not commit:
            continue
        parts = commit.split('|')
        if len(parts) < 2:
            continue

        author, committer = parts
        authors.add(author)
        committers.add(committer)

        if author != committer:  # Different person = review happened
            pairs.append((author, committer))

    # Calculate diversity
    unique_pairs = len(set(pairs))
    total_reviews = len(pairs)

    # Check for echo chamber (same reviewer always)
    from collections import Counter
    reviewer_counts = Counter(p[1] for p in pairs)
    most_common_reviewer_pct = (reviewer_counts.most_common(1)[0][1] / total_reviews * 100) if reviewer_counts else 0

    return {
        'total_authors': len(authors),
        'total_reviewers': len(committers),
        'unique_review_pairs': unique_pairs,
        'total_reviews': total_reviews,
        'diversity_score': (unique_pairs / total_reviews * 100) if total_reviews > 0 else 0,
        'most_common_reviewer_percentage': most_common_reviewer_pct,
        'echo_chamber_risk': 'HIGH' if most_common_reviewer_pct > 50 else 'LOW'
    }
```

---

### 4. Comment Density

**Lines changed vs discussion:**

```python
def analyze_comment_density() -> dict:
    """Ratio of discussion to code changes"""
    # Get commits with stats
    commits = subprocess.check_output(
        'git log --since="30 days ago" --shortstat --format="%H"',
        shell=True
    ).decode().strip().split('\n')

    total_insertions = 0
    total_deletions = 0
    commit_count = 0

    for line in commits:
        if 'insertion' in line or 'deletion' in line:
            match = re.search(r'(\d+) insertion', line)
            if match:
                total_insertions += int(match.group(1))
            match = re.search(r'(\d+) deletion', line)
            if match:
                total_deletions += int(match.group(1))
        elif line.strip():  # Commit hash
            commit_count += 1

    total_changes = total_insertions + total_deletions

    # Get commit message lengths (proxy for discussion)
    message_lengths = subprocess.check_output(
        'git log --since="30 days ago" --format="%s%n%b"',
        shell=True
    ).decode()

    total_message_chars = len(message_lengths)

    # Comment density = discussion per 100 lines changed
    comment_density = (total_message_chars / total_changes * 100) if total_changes > 0 else 0

    return {
        'total_changes': total_changes,
        'total_message_chars': total_message_chars,
        'comment_density': comment_density,  # Chars per 100 LOC
        'commits': commit_count,
        'quality': (
            'HIGH' if comment_density > 50 else
            'MEDIUM' if comment_density > 20 else
            'LOW'
        )
    }
```

---

### 5. AI Code Review Patterns

**Specific guidance for AI-generated code:**

```python
def generate_ai_review_checklist(file_changes: List[str]) -> dict:
    """Dynamic checklist for AI code review"""
    checklist = {
        'general': [
            'Does code match actual API signatures?',
            'Are all imported functions real (not hallucinated)?',
            'Is error handling comprehensive, not just try/pass?',
            'Are type hints accurate and complete?'
        ],
        'ai_specific': [],
        'context_specific': []
    }

    # Detect AI signatures in diff
    has_ai_patterns = any(
        re.search(r'(Here\'s how|You can use|Co-authored.*Copilot)', change)
        for change in file_changes
    )

    if has_ai_patterns:
        checklist['ai_specific'].extend([
            'Is this code copy/pasted from elsewhere? (Check for duplicates)',
            'Does complexity match purpose? (Bloat check)',
            'Are comments explaining WHY, not WHAT?',
            'Is logic sound? (Check for off-by-one, infinite loops)'
        ])

    # Context-specific checks
    if any('async' in change for change in file_changes):
        checklist['context_specific'].append('Are all awaits necessary? No blocking calls in async?')

    if any('open(' in change for change in file_changes):
        checklist['context_specific'].append('File operations in try/finally? Resource cleanup?')

    if any('password' in change.lower() for change in file_changes):
        checklist['context_specific'].append('Passwords hashed (bcrypt/argon2)? Never plaintext in logs?')

    return checklist
```

---

## Patterns

### Complete Review Quality Report

```python
def generate_review_quality_report() -> dict:
    """Comprehensive code review quality assessment"""
    return {
        'commit_message_quality': analyze_commit_message_quality(),
        'review_time': analyze_review_time(),
        'reviewer_diversity': analyze_reviewer_diversity(),
        'comment_density': analyze_comment_density(),
        'overall_score': calculate_overall_review_score(),
        'recommendations': generate_recommendations()
    }

def calculate_overall_review_score() -> dict:
    """Weighted score: 0-100"""
    msg_quality = analyze_commit_message_quality()
    review_time = analyze_review_time()
    diversity = analyze_reviewer_diversity()
    density = analyze_comment_density()

    # Weights
    score = (
        msg_quality['quality_score'] * 0.25 +
        (100 - review_time['too_fast_percentage']) * 0.25 +
        diversity['diversity_score'] * 0.25 +
        (min(density['comment_density'], 100)) * 0.25
    )

    return {
        'score': score,
        'grade': (
            'A' if score >= 80 else
            'B' if score >= 60 else
            'C' if score >= 40 else
            'D'
        )
    }

def generate_recommendations() -> List[str]:
    """Actionable improvements"""
    report = generate_review_quality_report()
    recommendations = []

    if report['commit_message_quality']['trivial_percentage'] > 30:
        recommendations.append(
            'Encourage substantive commit messages. Avoid "LGTM", "fix", "wip".'
        )

    if report['review_time']['too_fast_percentage'] > 30:
        recommendations.append(
            'Many PRs merged < 1 hour. Implement minimum review time policy.'
        )

    if report['reviewer_diversity']['echo_chamber_risk'] == 'HIGH':
        recommendations.append(
            'Reviewer diversity low. Rotate reviewers to avoid echo chamber.'
        )

    if report['comment_density']['quality'] == 'LOW':
        recommendations.append(
            'Low discussion density. Encourage more PR comments and questions.'
        )

    return recommendations
```

---

## Checklist

### Review Quality Metrics
- [ ] Commit message quality scored
- [ ] Review time distribution analyzed
- [ ] Reviewer diversity measured
- [ ] Comment density calculated
- [ ] Overall score computed

### Red Flags
- [ ] Trivial commits > 30%
- [ ] PRs merged < 1 hour > 30%
- [ ] Single reviewer dominance > 50%
- [ ] Comment density < 20 chars/100 LOC
- [ ] Overall score < 60

### AI Code Review
- [ ] AI-generated code detected
- [ ] AI-specific checklist generated
- [ ] Hallucination check included
- [ ] Bloat check included
- [ ] Logic bug patterns checked

### Improvements
- [ ] Minimum review time policy
- [ ] Reviewer rotation schedule
- [ ] Review checklist template
- [ ] AI code review guidelines
- [ ] Monthly review quality reports

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for code review domain
action_types: [audit, generate]
keywords: [code review, PR quality, review depth, commit quality]
category: quality
pain_points: [11, 12]  # Review Quality Decline, Context Loss in Reviews
```

---

## References

- [GitHub Octoverse 2025: Review Quality Decline](https://octoverse.github.com/)
- [Best Practices for Code Review (Google)](https://google.github.io/eng-practices/review/)
- [Code Review Best Practices (Microsoft)](https://learn.microsoft.com/en-us/azure/devops/repos/git/pull-requests)
