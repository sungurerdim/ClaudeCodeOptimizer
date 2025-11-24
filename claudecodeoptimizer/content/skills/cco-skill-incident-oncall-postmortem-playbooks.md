---
name: incident-response
description: Minimize incident impact through severity classification, automated detection, on-call rotation, incident playbooks, blameless postmortems, and MTTD/MTTR tracking
keywords: [incident response, on-call, postmortem, runbook, playbook, severity, MTTD, MTTR, status page, escalation]
category: observability
related_commands:
  action_types: [audit, generate]
  categories: [observability]
pain_points: [4, 9, 12]
---

# Skill: Incident Response & On-Call Management
**Domain**: Operations & Reliability
**Purpose**: Minimize incident impact through rapid detection, coordinated response, blameless postmortems, and systematic improvement.

> **Standards:** Format defined in [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md)  
> **Discovery:** See [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md#18-command-discovery-protocol)


**Principles**: P_INCIDENT_RESPONSE_READINESS, P_RUNBOOK_OPERATIONAL_DOCS, P_GRACEFUL_SHUTDOWN, P_HEALTH_CHECKS
---

---

## Core Techniques

- **Severity Classification**: P0 (outage, <15min), P1 (degraded, <30min), P2 (partial, <4hr), P3 (minor, <24hr)
- **Automated Detection**: Classify by error rate, response time, affected users, availability
- **On-Call Rotation**: Weekly rotation with multi-tier escalation (primary → secondary → IC → manager)
- **Incident Playbooks**: Template-based response with symptoms, diagnosis, mitigation, rollback
- **Communication Plan**: Status page updates by cadence (P0: 30min, P1: 1hr)
- **Blameless Postmortems**: Timeline, root cause, action items with owners, lessons learned
- **Metrics Tracking**: MTTD (<5min), MTTR (P0: <30min, P1: <2hr), false positive rate (<10%)

---

## Patterns

### ✅ Good - Automated Severity Detection
```python
def determine_severity(error_rate, response_p95, affected_pct, availability):
    if availability < 50 or affected_pct > 80 or error_rate > 50:
        return "P0"  # Complete outage
    if availability < 95 or affected_pct > 20 or error_rate > 10 or response_p95 > 5000:
        return "P1"  # Major degradation
    if error_rate > 5 or response_p95 > 2000 or affected_pct > 5:
        return "P2"  # Partial degradation
    return "P3"
```
**Why**: Consistent classification based on metrics, not guesswork

### ❌ Bad - Manual Severity Guessing
```python
def determine_severity():
    return input("Is it bad? (P0/P1/P2/P3): ")
```
**Why**: Inconsistent, subjective, slow classification

### ✅ Good - Incident Playbook Structure
```markdown
# Playbook: [Incident Type]

## Symptoms
- [Observable symptoms]

## Diagnosis
1. Check [metric/dashboard]
2. Verify [dependency]
3. Review [logs/traces]

## Mitigation
1. Immediate: [stop bleeding]
2. Root cause: [investigate]
3. Permanent: [fix]

## Rollback
kubectl rollout undo deployment/api -n production

## Communication
"Investigating [issue]. Updates every 30min."
"Resolved. Root cause: [brief]. Postmortem in 48h."
```
**Why**: Structured, actionable, repeatable response

### ❌ Bad - Vague Playbook
```markdown
# Try to fix the database
1. Check if it's slow
2. Maybe restart it?
3. Email someone if still broken
```
**Why**: No specific commands, metrics, or escalation path

### ✅ Good - Status Page Integration
```python
def create_incident(name, impact, message):
    return requests.post(
        f'https://api.statuspage.io/v1/pages/{PAGE_ID}/incidents',
        headers={'Authorization': f'OAuth {API_KEY}'},
        json={'incident': {'name': name, 'status': 'investigating', 'impact': impact, 'body': message}}
    )
```
**Why**: Automated, consistent external communication

### ❌ Bad - Manual Email Updates
```python
def notify_customers():
    # Send email to 10,000 customers manually
    for email in customers:
        send_email(email, "We have a problem...")
```
**Why**: Slow, error-prone, no central status tracking

### ✅ Good - Blameless Postmortem
```markdown
# Postmortem: DB Connection Leak

## Timeline
14:05 - Alert triggered
14:20 - Root cause: connection leak in PR #1234
14:25 - Mitigation: increased pool size

## Root Cause
Code change missed db.close() in error path

## Action Items
- [ ] Add connection pool alert >80% (@alice, P0)
- [ ] Implement leak detection (@bob, P0)
- [ ] Update code review checklist (@charlie, P1)

## Lessons
✅ Alert triggered quickly
❌ Code review missed leak
❌ No connection pool monitoring
```
**Why**: Focuses on systems, actionable improvements, no blame

### ❌ Bad - Blame-Oriented Postmortem
```markdown
# Who broke production?

Bob deployed bad code and didn't test it.
Alice should have caught it in code review.
We need to fire someone.
```
**Why**: Blame culture, no system improvements, demotivates team

### ✅ Good - Incident Metrics
```python
mttd = Histogram('incident_mttd_seconds', buckets=[60, 300, 600, 1800, 3600])
mttr = Histogram('incident_mttr_seconds', buckets=[300, 900, 1800, 3600, 7200])
incidents_total = Counter('incidents_total', ['severity'])

def record_incident(severity, detected_at, resolved_at):
    mttd.observe((detected_at - started_at).total_seconds())
    mttr.observe((resolved_at - detected_at).total_seconds())
    incidents_total.labels(severity=severity).inc()
```
**Why**: Quantifiable improvement tracking

### ❌ Bad - No Incident Tracking
```python
# "We had some outages this month, I think?"
# No data on MTTD, MTTR, or trends
```
**Why**: Can't measure improvement, repeat mistakes

---

## Checklist

- [ ] Severity levels defined (P0/P1/P2/P3) with SLAs
- [ ] Automated severity detection based on metrics
- [ ] On-call rotation configured with escalation policy
- [ ] Playbooks created for top 10 incident types
- [ ] Status page integrated with incident system
- [ ] Communication templates tested
- [ ] Postmortem template used for P0/P1
- [ ] Blameless culture maintained
- [ ] Action items tracked with owners and deadlines
- [ ] MTTD and MTTR metrics tracked in dashboard
- [ ] Monthly incident review conducted
- [ ] False positive rate <10%
- [ ] Fire drills conducted quarterly

---

