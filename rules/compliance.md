# Compliance Rules
*Regulatory compliance requirements by framework*

**Trigger:** Compliance != None (multi-select, cumulative)

## Base Compliance (Any)
- **Data-Classification**: Classify data by sensitivity level
- **Access-Control**: Role-based access with least privilege
- **Incident-Response**: Documented incident response plan

## SOC2
- **SOC2-Audit-Trail**: Complete audit trail for all data access
- **SOC2-Change-Mgmt**: Documented change management process
- **SOC2-Access-Review**: Quarterly access reviews

## HIPAA
- **HIPAA-PHI-Encrypt**: Encrypt PHI at rest and in transit
- **HIPAA-BAA**: Business Associate Agreements for vendors
- **HIPAA-Access-Log**: Log all PHI access with user, time, purpose
- **HIPAA-Minimum**: Minimum necessary access to PHI

## PCI-DSS
- **PCI-Card-Mask**: Mask PAN (show only last 4 digits)
- **PCI-No-Storage**: Store only masked payment data, exclude CVV/CVC
- **PCI-Network-Seg**: Network segmentation for cardholder data
- **PCI-Key-Mgmt**: Cryptographic key management procedures

## GDPR
- **GDPR-Consent**: Explicit consent with purpose specification
- **GDPR-Right-Access**: Implement data subject access requests
- **GDPR-Right-Delete**: Implement right to erasure
- **GDPR-Data-Portability**: Export user data in portable format
- **GDPR-Breach-Notify**: 72-hour breach notification procedure

## CCPA
- **CCPA-Opt-Out**: "Do Not Sell" opt-out mechanism
- **CCPA-Disclosure**: Disclose categories of data collected
- **CCPA-Delete**: Honor deletion requests within 45 days

## ISO27001
- **ISO-Risk-Assess**: Regular risk assessments
- **ISO-Asset-Inventory**: Maintain information asset inventory
- **ISO-Policy-Docs**: Documented security policies

## FedRAMP
- **FedRAMP-Boundary**: Documented system boundary
- **FedRAMP-Continuous**: Continuous monitoring implementation
- **FedRAMP-FIPS**: FIPS 140-2 validated cryptography

## DORA (EU Financial)
- **DORA-ICT-Risk**: ICT risk management framework
- **DORA-Incident**: Major ICT incident reporting
- **DORA-Resilience**: Digital operational resilience testing

## HITRUST
- **HITRUST-CSF**: Align with HITRUST CSF controls
- **HITRUST-Inherit**: Leverage inherited controls from providers
