# Kadıköy Kahve Dükkânı Sitesi — Özet

## Site
Tek sayfalık, mobil öncelikli, saf HTML + CSS + az JavaScript. Framework, npm, build yok.
Ana hedef: ziyaretçiyi dükkâna getirmek ("Yol Tarifi Al"); ikincil: telefon ve Instagram.

**Bölümler:** üst menü, hero, hakkımızda, menü (sekmeli), olanaklar, galeri, yorumlar, SSS, iletişim ve harita, footer. Mobilde alta sabit "Yol Tarifi Al / Ara" çubuğu.

## Renkler ve fontlar
- Krem zemin `#FAF6F0`, espresso kahvesi metin `#5A3825`, kiremit vurgu `#A8421F`, adaçayı yeşili `#4F6B52`. Koyu tema otomatik (`prefers-color-scheme`).
- Fontlar: Fraunces (başlık), Inter (gövde). Google Fonts'tan yüklenir; internet yoksa sistem fontuna düşer.

## Dosyalar
- `site/index.html`, `site/css/style.css`, `site/js/main.js`, `site/img/logo.svg`, `site/robots.txt`, `site/sitemap.xml`
- Plan dosyaları: `01-brief`, `02-metinler`, `03-tasarim`, `04-gorseller`, `05-seo-raporu`, `06-yayinlama`, `99-kalite-raporu`

## Sizin doldurmanız gerekenler ([DOLDUR])
Tam satır listesi: `99-kalite-raporu.md`. Ana gruplar:
1. **Kimlik:** dükkân adı (title, logo, footer, JSON-LD), logo/renk tercihi.
2. **İletişim ve konum:** adres, telefon (`tel:`), e-posta, Google Haritalar bağlantısı ve iframe, Instagram bağlantısı. `index.html` içinde `#DOLDUR-harita-linki`, `#DOLDUR-telefon`, `#DOLDUR-instagram`, `#DOLDUR-e-posta` ile aranır.
3. **Saatler:** `js/main.js` içindeki `SAATLER` nesnesi (dolunca "Şimdi açık" göstergesi çalışır).
4. **Menü:** ürün adları ve fiyatlar.
5. **Olanaklar:** Wi-Fi, priz, açık alan, evcil hayvan, ödeme, rezervasyon. Doğru olan cümle HTML yorumunda hazır; yanlış olan kartı silin.
6. **Yorumlar ve SSS cevapları:** gerçek müşteri yorumları (uydurmayın).
7. **Görseller:** gerçek fotoğraflar (`04-gorseller.md`), "Geçici görsel" etiketlerini kaldırın; `favicon.svg` ve `og-gorsel.jpg` ekleyin.
8. **Alan adı:** `robots.txt` ve `sitemap.xml` içindeki `ORNEK-ALANADI.com`; `index.html` içindeki canonical/OG yorumlarını açın.
9. **JSON-LD:** telefon, saatler, adres ayrıntısı, `hasMap`, `sameAs`.

## Siteyi açma
`site/index.html` dosyasına çift tıklayın.

## Yayınlama (kısa)
1. Yukarıdaki `[DOLDUR]` alanlarını doldurun (aksi halde müşteri yer tutucuları görür).
2. Netlify Drop'a `site/` klasörünü sürükleyin (ayrıntı ve alternatifler: `06-yayinlama.md`).
3. İsterseniz alan adı bağlayın, ardından Google İşletme Profili ve Search Console'u kurun (`05-seo-raporu.md`).

## Notlar
- Site tarayıcıda açılıp denenmedi; kontroller kod okuyarak yapıldı. İlk açılışta özellikle mobil menü ikonunu ve alt çubuğu gözle kontrol edin.
- Rehberdeki bazı fiyat/limit bilgileri doğrulanamadı; yayından önce ilgili sitelerde teyit edin.
- Kalite raporundaki bazı "Önerilir" maddeleri (mobilde "Şimdi açık" rozeti, favicon, og:image, plan belgelerindeki küçük tutarsızlıklar) yapılmadı.
