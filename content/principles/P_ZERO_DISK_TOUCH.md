---
id: P_ZERO_DISK_TOUCH
title: Zero Disk Touch
category: security_privacy
severity: critical
weight: 9
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_ZERO_DISK_TOUCH: Zero Disk Touch 🔴

**Severity**: Critical

Sensitive data never touches filesystem - RAM and secure storage only.

**Why**: Protects user privacy by anonymizing data before collection and storage

**Enforcement**: Skills required - verification_protocol, test_first, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **No Temp Files Sensitive**: No temp files for sensitive data

**❌ Bad**:
```
with open('/tmp/audio.wav', 'wb') as f:  # Disk touch!
```

**✅ Good**:
```
process = subprocess.Popen(['ffmpeg', '-i', 'pipe:0'], stdin=PIPE)  # In-memory
```
