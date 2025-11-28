---
name: cco-context
description: Project context for calibrated recommendations
---

# /cco-context

**Project context** - Gather/update context for calibrated AI recommendations.

Can be run standalone or automatically by context-aware commands (review, audit, optimize, refactor).

## Step 1: Load Context

```bash
cat .claude/cco_context.yaml 2>/dev/null
```

## Step 2: Validate or Gather

### If Context Exists

Show current values and ask:

```
AskUserQuestion:
header: "Context"
question: "Proje context'i bulundu. Güncellemek istediğiniz alanlar:"
multiSelect: true
options:
  - label: "Hepsi geçerli"
    description: "Mevcut context ile devam et"
  - label: "Impact & Scale"
    description: "Kim etkilenir, kaç kişi"
  - label: "Risk & Compliance"
    description: "Veri hassasiyeti, uyumluluk, downtime"
  - label: "Team"
    description: "Takım büyüklüğü, ownership"
  - label: "Operations"
    description: "Rollback, zaman baskısı"
```

- If "Hepsi geçerli" → proceed to Step 3
- If specific sections selected → re-ask only those sections, update file, proceed

### If No Context

Gather with conditional questions:

**Q1 - Impact (always):**
"Bir şeyler ters giderse kim etkilenir?"
→ Sadece ben | Takımım | Müşteriler | Genel halk

**Q2 - Scale (if team+):**
"Kaç kişi etkilenir?"
→ <100 | 100-10K | 10K-1M | 1M+

**Q3 - Data (if customers+):**
"En hassas veri türü?"
→ Public | Internal | PII | Financial/Health

**Q4 - Compliance (if PII+):**
"Hangi uyumluluk gereksinimleri var?" (multiSelect)
→ GDPR/KVKK | SOC2 | HIPAA | PCI-DSS

**Q5 - Downtime (always):**
"Uptime ne kadar kritik?"
→ Downtime OK | Saatler | Dakikalar | Saniyeler

**Q6 - Revenue (if minutes+):**
"Downtime'ın finansal etkisi?"
→ Yok/Dolaylı | Saatlik | Dakikalık

**Q7 - Team (always):**
"Kaç geliştirici çalışıyor?"
→ Solo | 2-5 | 6-15 | 15+

**Q8 - Ownership (if 2+):**
"Kod sahipliği nasıl?"
→ Herkes her yere | Alan sahipliği | Strict CODEOWNERS

**Q9 - Rollback (always):**
"Kötü deploy'u geri almak ne kadar zor?"
→ Git revert | DB migration | User data riski

**Q10 - Pressure (always):**
"Mevcut zaman baskısı?"
→ Rahat | Normal | Deadline var | Acil

After gathering, write to `.claude/cco_context.yaml`:

```yaml
# CCO Project Context - Auto-generated
version: 1
updated: {ISO_DATE}

impact:
  affected: {q1}
  scale: {q2}  # if applicable

risk:
  data_sensitivity: {q3}  # if applicable
  compliance: {q4}  # if applicable
  downtime_tolerance: {q5}
  revenue_impact: {q6}  # if applicable

team:
  size: {q7}
  ownership: {q8}  # if applicable

operations:
  rollback: {q9}
  time_pressure: {q10}

```

## Step 3: Use Context

Context is now available. Commands MUST follow these output requirements:

### Context-Justified Recommendations

Every recommendation/finding MUST include:

1. **What**: The recommendation itself
2. **Why**: Which context field(s) led to this recommendation
3. **Trade-off**: What would be different in another context

Format:
```
[Recommendation]
↳ Context: {field}: {value} → {why this matters}
```

### Examples of Context Justification

```
⚠️ Test coverage %60 - normalde düşük ama kabul edilebilir
↳ Context: time_pressure: urgent, affected: self → hızlı ship öncelikli

❌ SQL injection riski - MUTLAKA düzeltilmeli
↳ Context: data_sensitivity: financial, compliance: pci-dss → güvenlik kritik

ℹ️ Refactoring önerisi - şimdi değil, backlog'a eklenebilir
↳ Context: time_pressure: deadline, rollback: db_migration → riskli değişiklik ertelenebilir
```

### Anti-patterns (YAPMA)

- ❌ Context'e referans vermeden öneri yapmak
- ❌ "Best practice" deyip bağlamı yok saymak
- ❌ Tüm projelere aynı standartları uygulamak
- ❌ Context'i okuyup sonra görmezden gelmek

**Key principle:** AI dynamically evaluates - recommendations without context justification are incomplete.
