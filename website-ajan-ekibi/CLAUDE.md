# Web Sitesi Ajan Ekibi

Bu klasör bir web sitesi stüdyosudur. Her zaman **Türkçe** konuş ve yaz.

## Ekip (`.claude/agents/`)
| Ajan | Görev |
|---|---|
| proje-planlayici | İsteği site planına çevirir: amaç, kitle, sayfalar, bölümler |
| metin-yazari | Başlıklar, slogan, bölüm metinleri, SSS, meta açıklamalar |
| tasarimci | Renk paleti, fontlar, boşluklar, bileşenler (CSS değişkenleri) |
| gorsel-yonetmen | Görsel listesi, yapay zekâ görsel promptları, SVG logo ve ikonlar |
| gelistirici | HTML/CSS/JS ile siteyi kodlar |
| seo-uzmani | Meta, JSON-LD, sitemap, robots, yerel SEO |
| kalite-kontrol | Bağlantı, mobil, erişilebilirlik, performans, yazım kontrolü |
| yayinci | Netlify / Cloudflare / GitHub Pages yayın rehberi, alan adı |
| prompt-muhendisi | Güçlü prompt yazar/iyileştirir (Claude, görsel, video), yeni ajan tasarlar |

## Çalışma kuralları
- Bağımsız ajanları **paralel** çalıştır (metin + tasarım; SEO + yayın rehberi).
- Bağımlı adımları sırayla çalıştır: plan → metin/tasarım → görsel → kod → SEO/kontrol.
- Planlar `plan/`, site dosyaları `site/` klasöründe durur.
- Saf HTML + CSS + az JavaScript kullan; framework, npm veya build adımı yok. Site, `site/index.html` dosyasına çift tıklayınca açılmalı.
- Gerçek bilgileri (telefon, adres, fiyat, yorum) uydurma; `[DOLDUR: ...]` ile işaretle.
- Site bitince her zaman `kalite-kontrol` ile kontrol et.

## Kısayol komutları
- `/site-yap <açıklama>`: tüm ekiple sıfırdan site
- `/sayfa-ekle <sayfa/bölüm>`: mevcut siteye ekleme
- `/tasarim-degistir <istek>`: renk/font/hava değişikliği
- `/site-kontrol`: kalite + SEO kontrolü ve düzeltme
- `/yayinla`: internete koyma rehberi
- `/prompt <istek veya prompt>`: prompt yaz / iyileştir
