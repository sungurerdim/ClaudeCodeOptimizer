# İyileştirme Fikirleri

Kaynak: Boris Cherny (Claude Code creator) Twitter thread analizi
Tarih: 2026-02-01

## 1. `/cco-techdebt` komutu
Teknik borç odaklı tarama: duplikasyon, dead code, TODO/FIXME/HACK takibi.
Mevcut `cco-agent-analyze`'a `scope=techdebt` eklenerek uygulanabilir.

## 2. `/cco-learn` komutu
Codebase'i tarayıp mimari diagram + modül açıklamaları üreten komut.
Yeni kullanıcılar için onboarding aracı. Mermaid/ASCII output.

## 3. Subagent kullanım rehberliği
Kullanıcıya ne zaman subagent kullanacağını söyleyen ipuçları.
tune çıktısına veya CLAUDE.md'ye eklenebilir.

## 4. CLAUDE.md otomatik güncelleme
optimize/commit sonrası öğrenilen pattern'leri proje CLAUDE.md'ye kaydetme.
Tekrar eden hataları rule olarak kalıcılaştırma.

## 5. MCP entegrasyonu rehberi
tune çıktısına tespit edilen MCP server'ları ve kullanım önerileri ekleme.

## Öncelik (ROI): 4 > 1 > 2 > 3 > 5
