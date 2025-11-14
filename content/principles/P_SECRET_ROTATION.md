---
id: P_SECRET_ROTATION
title: Secret Management with Rotation
category: security_privacy
severity: critical
weight: 10
applicability:
  project_types: ['all']
  languages: ['all']
---

# P_SECRET_ROTATION: Secret Management with Rotation 🔴

**Severity**: Critical

Use secret managers (Vault, AWS/Azure/GCP), never hardcode. Implement rotation policies and audit logging.

**Why**: Prevents credential leaks and enables rotation without code changes

**Enforcement**: Skills required - verification_protocol, root_cause_analysis

**Project Types**: all
**Languages**: all

**Rules**:
- **No Hardcoded Secrets**: No hardcoded API keys/passwords/tokens
- **Use Secret Manager**: Use secret manager (Vault, AWS Secrets Manager, etc.)
- **Secret Rotation**: Implement secret rotation (30-90 days)
- **Secret Audit Logging**: Audit all secret access
- **No Secrets In Git**: Never commit secrets to git

**❌ Bad**:
```
# Hardcoded secret (CRITICAL violation)
API_KEY = '<hardcoded-api-key-value>'
DB_PASSWORD = '<hardcoded-password-value>'

# Plain env var without rotation
SECRET = os.getenv('SECRET')  # No rotation policy
```

**✅ Good**:
```
# HashiCorp Vault
import hvac
client = hvac.Client(url='https://vault.example.com')
secret = client.secrets.kv.v2.read_secret_version(path='myapp/config')
API_KEY = secret['data']['data']['api_key']

# AWS Secrets Manager with rotation
import boto3
client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='prod/api/key')

# Kubernetes Sealed Secrets
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
name: mysecret
spec:
encryptedData:
password: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
```
