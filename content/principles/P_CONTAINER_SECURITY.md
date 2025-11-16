---
id: P_CONTAINER_SECURITY
title: Container Security
category: security_privacy
severity: high
weight: 9
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_CONTAINER_SECURITY: Container Security 🔴

**Severity**: High

Secure container images and runtime with minimal attack surface

**Why**: Reduces container attack surface through minimal images and runtime restrictions

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **Minimal Base Image**: Use distroless or minimal base images
- **Non Root User**: Run containers as non-root
- **Image Scanning**: Scan images for CVEs

**❌ Bad**:
```
FROM ubuntu:latest
RUN apt-get install...  # Root user, full OS
```

**✅ Good**:
```
FROM gcr.io/distroless/python3
USER 1000:1000  # Non-root, minimal
```

## Autofix Available
