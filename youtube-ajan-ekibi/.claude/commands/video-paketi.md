---
description: Bir konu için tüm ajanlarla eksiksiz video paketi hazırlar (araştırma, senaryo, kanca, SEO, thumbnail, Shorts, topluluk, kalite kontrol)
argument-hint: <video konusu>
---
Konu: **$ARGUMENTS**

Bu konu için eksiksiz bir YouTube video paketi hazırla. Klasör adı olarak konunun kısa, Türkçe karaktersiz, tireli halini kullan (ör. `cikti/evde-kahve-yapimi/`). Klasörü ayrıca oluşturmana gerek yok; Write aracı dosyayı yazarken klasörü otomatik oluşturur. Her ajana dosyayı kendisinin Write ile kaydetmesini söyle. Ajanları şu sırayla çalıştır:

**Aşama 1: Araştırma (paralel çalıştır)**
- `trend-arastirmaci` → `01-arastirma.md`
- `rakip-analisti` → `02-rakip-analizi.md`

**Aşama 2: Senaryo** (Aşama 1 bitince)
- `senarist` → araştırma dosyalarını okuyup `03-senaryo.md`

**Aşama 3: Paketleme (paralel çalıştır)** (senaryo bitince)
- `kanca-uzmani` → `04-kancalar.md`
- `seo-uzmani` → `05-seo.md`
- `thumbnail-tasarimci` → `06-thumbnail.md`
- `shorts-uzmani` → `07-shorts.md`
- `topluluk-yoneticisi` → `08-topluluk.md`

**Aşama 4: Kalite kontrol**
- `elestirmen` → tüm dosyaları okuyup `99-kalite-kontrol.md`

**Aşama 5: Düzeltme ve özet**
- Eleştirmenin "en kritik 5 düzeltme" maddesini ilgili dosyalara uygula.
- `00-OZET.md` dosyası oluştur: seçilen başlık, thumbnail konsepti, kanca, tahmini süre, yayın kontrol listesi.
- Bana Türkçe kısa bir özet ver ve dosyaların listesini göster.
