---
description: Tüm ekiple sıfırdan eksiksiz web sitesi yapar (plan, metin, tasarım, görsel, kod, SEO, kalite kontrol, yayın rehberi)
argument-hint: <site açıklaması, ör. "Kadıköy'de bir kahve dükkânı için tek sayfalık site">
---
İstek: **$ARGUMENTS**

Bu istek için eksiksiz bir web sitesi yap. Planlar `plan/`, site dosyaları `site/` klasörüne gider. Klasörleri ayrıca oluşturmana gerek yok; Write aracı dosyayı yazarken klasörü otomatik oluşturur. Her ajana dosyasını kendisinin Write ile kaydetmesini söyle. Ajanları şu sırayla çalıştır:

**Aşama 1: Plan**
- `proje-planlayici` → `plan/01-brief.md`

**Aşama 2: İçerik ve tasarım (paralel çalıştır)** (brief bitince)
- `metin-yazari` → `plan/02-metinler.md`
- `tasarimci` → `plan/03-tasarim.md`

**Aşama 3: Görseller** (tasarım bitince)
- `gorsel-yonetmen` → `plan/04-gorseller.md` ve `site/img/logo.svg`

**Aşama 4: Kodlama**
- `gelistirici` → `site/` altındaki tüm dosyalar

**Aşama 5: Optimizasyon ve kontrol (paralel çalıştır)**
- `seo-uzmani` → SEO düzeltmeleri + `plan/05-seo-raporu.md`
- `yayinci` → `plan/06-yayinlama.md`

**Aşama 6: Kalite kontrol**
- `kalite-kontrol` → `plan/99-kalite-raporu.md`

**Aşama 7: Düzeltme ve özet**
- Kalite raporundaki "hemen düzeltilmeli" maddelerini `gelistirici` ile düzelttir.
- `plan/00-OZET.md` yaz: sitenin özeti, sayfalar, renkler/fontlar, kullanıcının doldurması gereken `[DOLDUR]` listesi, siteyi açma ve yayınlama adımları.
- Bana Türkçe kısa bir özet ver ve siteyi açmak için `site/index.html` dosyasına çift tıklamamı söyle.
