# SEO Raporu: Kadıköy Kahve Dükkânı

Tek sayfalık site olduğu için tüm kontroller `site/index.html` üzerinde yapıldı.

## 1. Yapılan değişiklikler

| Dosya | Değişiklik |
|---|---|
| `site/index.html` | `meta robots` eklendi. Twitter kartı (`summary`) ve `og:site_name` eklendi. Canonical, `og:url`, `og:image`, `twitter:image` hazır halde yorum içinde bırakıldı. CafeOrCoffeeShop JSON-LD eklendi. |
| `site/robots.txt` | Yeni. Tüm botlara izin verir, sitemap adresini gösterir (`ORNEK-ALANADI.com` yer tutucusu). |
| `site/sitemap.xml` | Yeni. Tek URL (ana sayfa), yer tutucu alan adıyla. |

Sayfa çift tıklayınca açılmaya devam eder. Yeni dosyalar yalnızca head bölümüne eklendi, göreli yollar değişmedi.

## 2. Denetim sonuçları

1. **Title ve description:** Title `[DOLDUR: dükkân adı] | Kadıköy'de Kahve ve Yol Tarifi`. Sabit kısım 43 karakter, dükkân adı en fazla 17 karakter olursa 60 sınırı aşılmaz. Ad uzunsa `[Ad] | Kadıköy Kahve Dükkânı` biçimine geçin. Description yaklaşık 128 karakter (sınır 155), uygun. Sayfa tek olduğu için benzersizlik sorunu yok.
2. **Canonical:** Bilerek yorum satırında. Yer tutucu alan adıyla yayınlanırsa arama motorları yanlış adrese yönlenir. Alan adı belli olunca yorumu açın.
3. **Open Graph ve Twitter:** `og:type`, `og:locale`, `og:site_name`, `og:title`, `og:description` ve Twitter title/description aktif. `og:image` ve `og:url` alan adı ve görsel olmadan geçerli olmadığı için yorumda.
4. **Başlık hiyerarşisi:** Tek `h1` (hero). Bölümler `h2`, alt başlıklar `h3`, atlama yok. İletişimdeki gizli `h3` ("İletişim bilgileri") de `h2` altında, sorun yok. Ek düzeltme gerekmedi.
5. **Yapılandırılmış veri:** `CafeOrCoffeeShop` JSON-LD geçerli JSON olarak eklendi. İçinde yalnızca bilinenler var: ilçe Kadıköy, il İstanbul, ülke TR. `name` değeri `[DOLDUR: dükkân adı]` yer tutucusu olarak duruyor, yayından önce mutlaka değiştirilmeli. Bilinmeyen alanlar (telefon, url, saatler, geo, sameAs, priceRange, görsel) JSON'a konmadı. Hangi satırın nasıl ekleneceği head'deki yorumda yazıyor. FAQPage eklenmedi, çünkü SSS cevapları henüz yer tutucu. Gerçek cevaplar gelince eklenebilir. `aggregateRating` ve `review` uydurulmadı.
6. **Görseller ve bağlantılar:** Logo `alt` metni var. Galeri ve hakkımızda yer tutucuları `role="img"` ile `aria-label` taşıyor. Gerçek fotoğraflar gelince `[DOLDUR]` altları somut açıklamayla değiştirin. Bağlantı metinleri anlamlı ("Yol Tarifi Al", "Menüyü Gör", "Google'da Yorumları Oku"), "buraya tıklayın" yok. `hero.webp`, `hakkimizda.webp` gibi dosya adları zaten betimleyici. Galeri dosyalarını `galeri-N.webp` yerine `kadikoy-kahve-tezgah.webp` gibi adlandırmak daha iyi olur.

## 3. Sizin yapmanız gerekenler (yayından önce)

1. Dükkân adını yazın: title, meta, og/twitter, JSON-LD `name`, logo alt, footer. Title uzunluğunu yeniden sayın.
2. Alan adı belli olunca şunları değiştirin:
   - `robots.txt` ve `sitemap.xml` içindeki `ORNEK-ALANADI.com`.
   - Canonical, `og:url`, `og:image` ve `twitter:image` yorumlarını açıp adresi yazın.
3. 1200x630 boyutunda `img/og-gorsel.jpg` hazırlayın. Ekledikten sonra `twitter:card` değerini `summary_large_image` yapın.
4. JSON-LD'ye telefon, url, `openingHoursSpecification`, `streetAddress`, `postalCode`, `hasMap`, `sameAs`, `priceRange` ve isteğe bağlı `geo` alanlarını ekleyin. Sonra https://validator.schema.org ve Google Rich Results Test ile doğrulayın.
5. Sayfada kalan tüm `[DOLDUR]` ifadelerini değiştirin veya ilgili bölümü silin. Yer tutucu metin indekslenirse arama sonuçlarında görünür.
6. Yayından sonra Google Search Console'a siteyi ekleyin ve `sitemap.xml` gönderin.

## 4. Yerel SEO önerileri

1. **NAP tutarlılığı:** Ad, adres ve telefon; sitede (iletişim, footer, JSON-LD), Google İşletme Profili, Instagram ve diğer dizinlerde birebir aynı yazılmalı (kısaltma, boşluk, "Cad./Caddesi" farkı bile olmamalı). Telefonu `tel:+90...` biçiminde bağlayın.
2. **Google İşletme Profili (en önemli adım):**
   - Profili talep edin ve doğrulayın. Ana kategori "Kafe" veya "Kahve dükkânı".
   - Gün gün saatleri, özel günleri, telefonu, site adresini, olanakları (Wi-Fi, açık alan vb., yalnızca doğruysa) girin.
   - En az 6-8 gerçek fotoğraf yükleyin (dış cephe, iç mekân, menü, ürünler).
   - Site bağlantısını `?utm_source=google&utm_medium=gbp` ile işaretlerseniz tıklamaları ölçebilirsiniz.
   - Müşterilerden yorum isteyin (QR kod veya kısa bağlantı), her yoruma cevap verin. Yorumları satın almayın.
   - Menü ve gönderi (post) bölümünü düzenli güncelleyin.
3. **Google Haritalar yerleştirme:** Haritalar'da dükkânı bulun, Paylaş, Harita yerleştir ile iframe kodunu alın ve `#iletisim` bölümündeki yer tutucunun yerine koyun (kod zaten yorumda hazır, `title` ve `loading="lazy"` içeriyor). "Yol Tarifi Al" düğmelerine aynı profilin paylaşım bağlantısını verin. JSON-LD `hasMap` alanına da aynısını yazın.
4. **İçerik:** Adres satırında mahalleyi yazın (Caferağa, Moda vb., hangisiyse). Ulaşım notuna vapur, metro, durak bilgisi ekleyin. "Kadıköy kahve", "Moda kahve dükkânı" gibi aramalar için metin doğal biçimde bölge adını anmalı, abartılmamalı.
5. **Yerel bağlantılar ve dizinler:** Instagram biyografisine site bağlantısı, Apple Haritalar, Yandex Haritalar ve Bing Places kayıtları, yerel blog ve mahalle yazıları (backlink) için bölge sitelerine başvuru.
6. **Gelecek adım:** Sayfa tek olduğu için çok sayfalı SEO yok. İleride "Menü" veya "Hakkımızda" ayrı sayfa olursa sitemap ve canonical her sayfa için ayrı eklenmeli.
