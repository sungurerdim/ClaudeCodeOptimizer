# CCO Kapsamli Yeniden Yapilandirma Plani

## Ozet

CCO'nun iki temel sorunu var:

1. **Format:** Komutlar ve agentlar prosedural pseudocode olarak yazilmis. Deklaratif stile donusturulmeli.
2. **Kural kalitesi:** Mevcut kurallar token verimli degil ve bazi kritik eksikler var. Kurallarin benim (Opus 4.5) en iyi isledigim formata donusturulmesi, etkisiz kurallarin cikarilmasi ve eksik kurallarin eklenmesi gerekiyor.

**Mevcut:** ~8,200 satir (komutlar + agentlar + core rules) + 18K token SessionStart hook
**Hedef:** ~2,500 satir + ~5K token SessionStart hook

---

## Kural Etkinlik Analizi (Model Perspektifi)

Bu bolum, hook'taki her kuralin benim uzerimde gercekte ne kadar etkili oldugunu, hangi formatin en iyi isledigini ve nelerin eksik oldugunu degerlendiriyor.

### Etki Siniflandirmasi

| Kural | Etki | Neden |
|-------|------|-------|
| **Change Scope [BLOCKER]** | YUKSEK | 1 numarali basarisizlik modum: kullanicinin istemedigini "iyilestirmek". Bu kural dogrudan bunu engelliyor |
| **Read-Before-Edit [BLOCKER]** | YUKSEK | Okumadan duzenleme hatalarina karsi somut bariyer |
| **Complexity Limits [BLOCKER]** | YUKSEK | Tablo formati mukemmel — taranabilir, somut sayilar, belirsizlik yok |
| **Anti-Overengineering Guard** | YUKSEK | 3 soru formati false-positive bulmalarimi ciddi olcude azaltiyor |
| **No Deferrals [BLOCKER]** | YUKSEK | Auto modda erteleme egilimimi dogrudan engelliyor |
| **Task Completion [BLOCKER]** | YUKSEK | Context uzayinca durma egilimime karsi etkili |
| **Uncertainty Protocol [BLOCKER]** | YUKSEK | Sessizce varsayim yapma egilimimi engelliyor |
| **Agent Delegation [CHECK]** | YUKSEK | CCO'ya ozel, dogru agent secimi icin kritik |
| **Model Strategy** | YUKSEK | CCO'ya ozel, dogru model secimi icin gerekli |
| **Accounting [BLOCKER]** | ORTA | Formul basit ve faydali ama 15+ yerde tekrar gereksiz |
| **File Creation [BLOCKER]** | ORTA | Etkili ama tek cumlede yeterli, ornek blogu gereksiz |
| **Severity Levels [CHECK]** | ORTA | Referans tablosu iyi, ama zaten bildigim bir sey |
| **Security Violations [BLOCKER]** | ORTA | Tablo formati iyi, ama cogu pattern zaten bildigim seyler |
| **Refactoring Safety [CHECK]** | ORTA | Checklist formati iyi, gercek hatalari onluyor |
| **Validation Boundaries [CHECK]** | DUSUK | Sadece public API yazarken gerekli, her oturumda yuklenmesi gereksiz agirlik |
| **Success Criteria [CHECK]** | DUSUK | Bu sablonu gercekte kullanmiyorum. Basit isler icin overhead, karmasik isler icin zaten dogal olarak planliyorum |
| **Output Format / Output Standards** | DUSUK | Cikti formati baglama gore degismeli, katı sablon uygulanmasi ters etki yapiyor |
| **Confidence Scoring (agirliklar)** | DUSUK | %40/%30/%20/%10 gibi sayisal agirliklar hesaplamiyorum — butunsel yargi kullaniyorum. Esikler (>=90 auto-fix vb.) daha faydali |
| **Enforcement (Safety altinda)** | SIFIR | "Ihlali duzelt" zaten [BLOCKER] etiketinin anlami. Tamamen gereksiz tekrar |
| **Security Lookup tablosu** | DUSUK | Bunlari zaten biliyorum. Sadece edge case'lerde faydali |

### En Iyi Isledigim Format

| Format | Etkinlik | Ornek |
|--------|----------|-------|
| **Tek cumle imperatif kural** | EN YUKSEK | "Okunmamis dosyayi duzenleme" |
| **Tablo (lookup/referans)** | EN YUKSEK | Complexity limits tablosu |
| **[BLOCKER] oncelik etiketi** | EN YUKSEK | Net onceliklendirme sinyali |
| **Somut esikler (sayi)** | EN YUKSEK | "≤ 15", "≤ 50 satir" |
| **3-maddelik kontrol sorusu** | YUKSEK | Anti-Overengineering Guard |
| **Karar agaci (tek seviye)** | YUKSEK | Agent Delegation |
| Paragraf aciklama | DUSUK | Okumak yerine atliyorum |
| ASCII agac diyagrami | DUSUK | Tek cumle ile ayni bilgi |
| ✓/✗ ornek bloklari | DUSUK | Kural ifadesinden zaten anliyorum |
| Cok seviyeli ic ice format | DUSUK | Tarama zorlugu |

### Eksik Kurallar (Gercek Zaaflarima Yonelik)

Bu kurallarin eklenmesi somut iyilestirme saglayacak:

| Eksik Kural | Zaaf | Onerilen Format |
|-------------|------|-----------------|
| **Incremental Verification** | Edit sonrasi dogrulama atlamak — birikimli hatalar | "Her edit sonrasi: degisikligin beklenen etkisini dogrula (lint/test/manual). Sonraki edite gecme" [BLOCKER] |
| **Context Staleness** | Uzun oturumlarda eski okumalara guvenip guncel olmayan bilgiyle hareket etmek | "Dosya 20+ adimdır okunmadiysa, edit oncesi yeniden oku" [BLOCKER] |
| **Error Recovery** | Tool call basarisiz olunca koru korune tekrar denemek | "Tool hatasi → once teshis (neden?), sonra strateji degistir. Ayni komutu 2x tekrarlama" [BLOCKER] |
| **Scope Creep Detection** | Analiz sirasinda bulgu sayisi beklentinin cok ustune cikinca kontrolsuz buyume | "Bulgu sayisi baslangic tahmininin 2x'ini astiysa dur, kullaniciya bildir, kapsam daralt" [CHECK] |
| **Partial Output Guard** | Buyuk islemlerde yarim cikti uretip "tamamlandi" demek | "Ciktida eksik bolum veya placeholder varsa tamamlanmamistir" [BLOCKER] |

### Kaldirilabilecek / Birlestirilebilecek Icerik

| Mevcut | Oneri | Token Tasarrufu |
|--------|-------|-----------------|
| Tum ✓/✗ ornek bloklari (6 adet) | Kaldir — kural ifadesi yeterli | ~800 token |
| ASCII agac diyagramlari (3 adet) | Tek cumleli kurala donustur | ~400 token |
| Enforcement bolumu (Safety) | Kaldir — [BLOCKER] etiketi ayni isi yapıyor | ~200 token |
| Success Criteria sablonu | Kaldir — doğal planlama daha etkili | ~300 token |
| Output Format + Output Standards | Tek satirda birlesik: "Progress, summary, error format" | ~300 token |
| Security Lookup tablosu | Kucult: sadece yanlis yapilabilecek edge case'ler | ~200 token |
| Confidence Scoring agirlik detayi | Agirlik formulunu kaldir, sadece esikleri tut | ~300 token |
| Tool Rules: CCO-ozel 3 kural (Profile Validation, Mode Detection, Output Envelope) | Komut dosyalarina tasi, hook'tan cikar | ~1,500 token |

### Stack/Dil/Framework/Operations Kurallari Analizi (44 dosya)

3 kategori, 44 dosya: `rules/languages/` (22), `rules/frameworks/` (8), `rules/operations/` (11)

**Genel Degerlendirme:** Bu kurallar `/cco:tune` tarafindan proje stack'ine gore secilip `.claude/rules/` altina kopyalaniyor. Dolayisiyla sadece ilgili projede yukleniyor — token israfi global hook kadar kritik degil. Ancak kalite tutarsiz.

#### Format Etkinlik Siralamasi (en iyiden en kotuye)

| Format | Etkinlik | Ornek |
|--------|----------|-------|
| **"Gotcha" formati** | EN YUKSEK | Frontend: "React keys — array index breaks reconciliation" |
| **Somut parametreler** | EN YUKSEK | Security: "Argon2id: memory 19456 KiB, iterations 2" |
| **Threshold tablolari** | YUKSEK | Testing coverage, Observability alert thresholds |
| **Kisa kural + ornek** | YUKSEK | Python: "`str \| None` not `Optional[str]`" |
| **Catalog/liste formati** | DUSUK | ORM: Her framework icin "Use X, Configure Y" — zaten bildigim seyler |
| **"Label-Prefix" stili** | DUSUK | Rust: "Ownership-Clear", "Borrow-Prefer" — etiketler token israfi |

#### Dosya Bazinda Degerlendirme

**ALTIN STANDART (degisiklik gereksiz):**
- `cco-python.md` — 28 satir, sadece modern syntax (bilmedigim/karistirabilecegim seyler)
- `cco-go.md` — 23 satir, minimal, dogru odak
- `cco-frontend.md` — Gotcha formati, framework-bazli tuzaklar
- `cco-security.md` — Somut parametreler (Argon2id, JWT TTL, rate limits)
- `cco-observability.md` — Spesifik threshold'lar ve alert yapilandirmasi
- `cco-database.md` — Somut gereksinimler tablosu

**IYILESTIRME GEREKEN:**
- `cco-typescript.md` — Iyi ama "Runtime Validation" bolumu tek satirda zod'u anlatip bitiyor, zod schema ornegi eklenmeli
- `cco-backend.md` — Universal Patterns tablosu iyi, ama "Operations Checklist" zaten bilinen seyler
- `cco-testing.md` — Coverage tablolari iyi, ama Naming Convention bolumu cok temel

**BUYUK REVIZYON GEREKEN:**
- `cco-rust.md` — "Label-Prefix" formatini kaldir (Ownership-Clear → dogrudan kural yaz). Gotcha eklenmeli: borrow checker tuzaklari, lifetime sorunlari, async footguns
- `cco-cicd.md` — Cok genel. "Cache dependencies", "Use secrets" gibi bariz seyler. Gotcha formatina donustur: her CI platformunun bilinen tuzaklari
- `cco-orm.md` — Katalog formati. Her ORM icin temel best practice listelemek yerine, N+1, migration tuzaklari, connection pool hatalari gibi GOTCHA'lara odaklan

**BIRLESTIRME ADAYLARI:**
- `cco-cicd.md` + `cco-build.md` → tek dosya (zaten cok kisa ve genel)

#### Eksikler

| Eksik | Etki |
|-------|------|
| **Versiyon-ozel tuzaklar** | Python 3.12+ degisiklikleri, Node 22 degisiklikleri vb. — yeni pattern'leri yanlis kullanabiliyorum |
| **Cross-cutting gotchas** | Monorepo tuzaklari, workspace yapilandirmasi — bunlar ne language ne framework'e sığıyor |
| **"Bunu YAPMA" listesi** | Her dil icin en sik yapilan 3-5 hata (anti-pattern focus) |

#### Onerilen Ilke: "Gotcha-First" Kurali

Tum stack kurallarinda su filtre uygulanmali:

> **"Bu kurali bilmesem ne olurdu?"**
> - Yanlis kod yazardim → KALIR (gotcha)
> - Suboptimal ama calisan kod yazardim → KUCULT (tek satir hatirlatma)
> - Zaten dogru yazardim → KALDIR (token israfi)

Bu filtre uygulandiginda cogu dosya %20-40 kuculur ve etki artar.

---

### Tool Rules Bolumu: Hook'ta Kal, Tekrarlari Sil

Hook'taki Tool Rules 8 kuraldan olusuyor. Analiz:

**Genel faydali (hook'ta kalir, sadelestir):**
- Execution Flow (analyze→plan→apply paterni) — her turlu cok adimli islem icin faydali
- Plan Review ("Bulgulari goster, SONRA sor") — evrensel iyi pratik
- Needs-Approval Flow — mimari kararlar icin onay paterni
- Confidence Scoring — agirlik formulunu kaldir, sadece esik tablosu
- Skip Patterns — her kod analizinde gecerli

**CCO-ozel (komut dosyalarina tasi, hook'tan cikar):**
- Profile Validation — CCO profile sistemi
- Mode Detection (--auto/--preview) — CCO flag'leri
- Output Envelope (JSON schema) — CCO cikti formati

**Kritik kural: Hook'taki kurallarin command/agent dosyalarinda kopyasi olmamali.**

Mevcut durumda 6 kural hook'ta tanimlanip komutlarda tekrar ediliyor (bkz. Tekrar Analizi).
Hedef: Hook tek kaynaktir. Komut/agent dosyalari hook kurallarini tekrar etmez, gerektiginde "Hook kurallarina uygun olarak..." seklinde referans verir.

Bu ilke Faz 4'te uygulanir ve ~2,000+ token tasarruf saglar (komut dosyalarindaki tekrarlar).

---

## Faz 1: SessionStart Hook Sadelestir + rules/core/ Temizle

**Mimari:** `hooks/core-rules.json` global kurallar tasiyor ve HER oturumda yuklenmeli. Bu kurallar proje-bagimsiz, evrensel kisitlamalar (guvenlik, complexity limitleri, workflow). `rules/core/` dosyalari ise ayni kurallarin dokumante edilmis hali.

**Sorun:** Hook icerigi ~18K token. Icerik dogru ama format sismis ve bazi kurallar etkisiz veya yanlis yerde.

**Degisiklik (hook'taki TUM icerige uygulanir — Foundation, Safety, Workflow ve Tool Rules dahil):**

1. **Format sadelestirme** (yukaridaki analiz tablosuna gore):
   - Ornek bloklari (`✓`/`✗`) kaldir — tek cumle kural yeterli
   - ASCII agac diyagramlari → tek satirlik kurala donustur
   - Enforcement bolumu kaldir (BLOCKER etiketi ayni isi yapiyor)
   - Success Criteria sablonu kaldir
   - Output Format + Output Standards → tek satir

2. **Etkisiz kurallari cikar veya kucult:**
   - Security Lookup → sadece edge case'ler (pickle, eval, yaml.load)
   - Confidence Scoring → agirlik formulunu kaldir, sadece esik tablosu
   - Validation Boundaries → kucult (tek satirlik hatirlatma)

3. **Tool Rules:**
   - CCO-ozel 3 kurali (Profile Validation, Mode Detection, Output Envelope) komut dosyalarina tasi, hook'tan cikar
   - Genel faydali 5 kural hook'ta kalir (ayni format sadelestirmesi bunlara da uygulanir)

4. **Eksik kurallari ekle** (5 adet, yukaridaki "Eksik Kurallar" tablosundan):
   - Incremental Verification [BLOCKER]
   - Context Staleness [BLOCKER]
   - Error Recovery [BLOCKER]
   - Scope Creep Detection [CHECK]
   - Partial Output Guard [BLOCKER]

5. **Anti-Overengineering Guard'i [BLOCKER]'a yukselrt** — etkisi yuksek, mevcut [CHECK] seviyesi yetersiz

**Hedef:** 18K → ~5K token (%72 azalma)

**Dosyalar:** `hooks/core-rules.json`

**Risk:** Dusuk — kurallar korunuyor, format ve yapi degisiyor. Her kural oncesi/sonrasi diff ile dogrulama.

---

## Faz 2: Analyze Agent (En Buyuk Tekil Dosya)

**Sorun:** `cco-agent-analyze.md` 1,615 satir. 105+ hardcoded regex pattern, platform filtreleme pseudocode'u, confidence scoring algoritmalari iceriyor.

**Degisiklik (1,615 → ~400 satir, %75 azalma):**
- **105 regex pattern kaldir.** Yerine scope adi + dogal dil aciklamasi koy
- **Platform filtreleme pseudocode'u (~70 satir) kaldir.** Yerine tek satirlik talimat
- **Confidence scoring algoritmasi (~60 satir) kaldir.** Yerine kisa kural
- **Output validation pseudocode kaldir.** JSON schema ornegi yeterli
- **Criticality rating, type quality scoring, comment quality pillar tablolari kaldir**
- **"When to Use" ve "Advantages" tablolari kaldir**
- **Scope tanimlarini tek tabloya daralt**

**Dosya:** `agents/cco-agent-analyze.md`

---

## Faz 3: Komutlari Pseudocode'dan Deklaratif Stile Donustur

### Donusum Deseni (tum komutlarda ayni):

**ONCE (prosedural):**
```javascript
const files = Bash("git diff --name-only HEAD").split('\n')
const codeFiles = files.filter(f => f.match(/\.(py|js|ts)$/))
if (codeFiles.length > 0) {
  lintTask = Bash("{lint_command}", { run_in_background: true })
}
```

**SONRA (deklaratif):**
```
## Quality Gates
Profilden format, lint, type, test komutlarini tum projede calistir.
Sadece docs/config degismisse testleri atla.
Gate basarisiz olursa kullaniciya sor: once duzelt (onerilen) veya yine de commit yap.
```

### 3a: optimize.md (888 → ~250 satir, %72)
### 3b: commit.md (484 → ~150 satir, %69)
### 3c: align.md (944 → ~250 satir, %74)
### 3d: tune.md (589 → ~200 satir, %66)
### 3e: preflight.md (810 → ~200 satir, %75)
### 3f: research.md (408 → ~150 satir, %63)
### 3g: docs.md (831 → ~200 satir, %76)

Her komutta: tum JavaScript pseudocode bloklari kaldirilip, yerine deklaratif talimatlar ve kisitlamalar konacak.

---

## Faz 4: Tekrarlari Ortadan Kaldir

**Temel ilke: Hook tek kaynaktir. Hook'taki kurallarin command/agent dosyalarinda kopyasi olmamali.**

Komut/agent dosyalarinda hook kurallari tekrar edilmeyecek. Gerektiginde hook kuralina referans verilecek.

### Silinecek tekrarlar (komut/agent dosyalarindan):

| Tekrarlanan Kural | Tekrar Yerleri | Silinecek Yer |
|-------------------|----------------|---------------|
| **Accounting formulu** | 5 dosya, ~15 mention | Tumu — hook yeterli |
| **Severity levels** | 4 dosya, ~8 mention | Tumu — hook yeterli |
| **Model strategy** | 4 dosya, ~4 mention | Tumu — hook yeterli |
| **Skip patterns** | 3 dosya, ~3 mention | Tumu — hook yeterli |
| **Confidence scoring** | 3 dosya, ~4 mention | Tumu — hook yeterli |
| **Output envelope** | 4 dosya, ~4 mention | Tumu — hook yeterli |

### Diger tekrar temizligi:
- **Optimize/Align scope overlap** (30+ cakisan check) → Analyze agent sahiplenir
- **CCO-ozel Tool Rules** (Profile Validation, Mode Detection, Output Envelope) → Hook'tan cikar, ilgili komut dosyalarina tasi (bu 3 kural sadece komut calistiginda gerekli)

### rules/core/ dosyalari:
Dokumantasyon olarak korunur. Hook'un okunabilir referansidir, runtime'da yuklenmez.

**Tahmini tasarruf:** Komut/agent dosyalarindan ~2,000+ token tekrar silimi

---

## Faz 5: Core Rules, Apply Agent ve Stack Kurallari Sadelestir

### 5a: Core + Agents
- **cco-thresholds.md** (321 → ~80 satir, %75)
- **cco-agent-apply.md** (722 → ~250 satir, %65)
- **cco-agent-research.md** (328 → ~180 satir, %45)

### 5b: Stack Kurallarini "Gotcha-First" Filtresinden Gecir
Tum `rules/languages/`, `rules/frameworks/`, `rules/operations/` dosyalarina "Bu kurali bilmesem ne olurdu?" filtresi uygula:

- **Buyuk revizyon:** `cco-rust.md`, `cco-cicd.md`, `cco-orm.md` — Label-Prefix kaldir, gotcha formatina donustur
- **Kucuk iyilestirme:** `cco-typescript.md`, `cco-backend.md`, `cco-testing.md`
- **Birlestirme:** `cco-cicd.md` + `cco-build.md`
- **Dokunma:** `cco-python.md`, `cco-go.md`, `cco-frontend.md`, `cco-security.md`, `cco-observability.md`, `cco-database.md` (zaten iyi)

---

## Hedef Ozet Tablosu

| Dosya | Mevcut | Hedef | Azalma |
|-------|--------|-------|--------|
| SessionStart hook | ~18K token | ~5K token | %72 |
| agents/cco-agent-analyze.md | 1,615 | 400 | %75 |
| agents/cco-agent-apply.md | 722 | 250 | %65 |
| agents/cco-agent-research.md | 328 | 180 | %45 |
| commands/optimize.md | 888 | 250 | %72 |
| commands/commit.md | 484 | 150 | %69 |
| commands/align.md | 944 | 250 | %74 |
| commands/tune.md | 589 | 200 | %66 |
| commands/preflight.md | 810 | 200 | %75 |
| commands/research.md | 408 | 150 | %63 |
| commands/docs.md | 831 | 200 | %76 |
| rules/core/cco-thresholds.md | 321 | 80 | %75 |
| **TOPLAM** | **~8,200 + 18K** | **~2,500 + 5K** | **~71%** |

---

## Uygulama Sirasi

1. **Faz 1** → Dusuk risk, hook icerigi sadelestirme (kurallar korunur)
2. **Faz 2** → En buyuk tekil dosya, Faz 3'ten once gerekli
3. **Faz 3a-3g** → Birer birer, her biri bagimsiz test edilebilir
4. **Faz 4** → Komutlar yeniden yazildiktan sonra temizlik
5. **Faz 5** → Son polish

---

## Dogrulama (Her faz sonrasi)

1. `pytest tests/` - mevcut testler gecmeli
2. Degisiklik yapilan komutu test et
3. Token sayimi dogrula
4. Redundancy check: "Bu bilgi baska dosyada tekrarlaniyor mu?"
5. Declarative check: "Bu satir NASIL mi yoksa NE mi soyluyor?"
