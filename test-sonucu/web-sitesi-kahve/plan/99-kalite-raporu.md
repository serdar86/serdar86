# Kalite Kontrol Raporu: Kadıköy Kahve Dükkânı (tek sayfa)

Tarih: 2026-10-11
Kapsam: `site/index.html`, `site/css/style.css`, `site/js/main.js`, `site/img/logo.svg`, `site/robots.txt`, `site/sitemap.xml`; `plan/01`, `02`, `03`, `05` ile karşılaştırma.
Yöntem: Kod incelemesi (statik). Tarayıcıda çalıştırılmadı; "tarayıcıda doğrulayın" notu olan maddeler spesifikasyon ve CSS özgüllük analizine dayanır. Kontrast oranları WCAG formülüyle yeniden hesaplandı. Site dosyalarına dokunulmadı.

## KARAR: ⚠️ Düzeltmeyle hazır

Yapı, erişilebilirlik temeli ve mobil düzen sağlam. Ancak (1) hamburger menü ikonu açılınca kaybolma hatası, (2) koyu temada "Şimdi açık" rozetinin kontrastı, (3) alan adı yer tutucusuyla duran robots/sitemap ve (4) 108 satırlık `[DOLDUR]` listesi yüzünden bugün olduğu gibi yayınlanmamalı. Kod hataları küçük düzeltmelerle giderilir; içerik alanları kullanıcıdan gelmeden yayın yapılmamalı.

---

## 1. Bağlantılar

| Durum | Madde | Referans |
|---|---|---|
| ✅ | `css/style.css`, `js/main.js`, `img/logo.svg` yolları göreli ve dosyalar mevcut; `file://` ile çift tıklayınca açılır | index.html:70-71, 81 |
| ✅ | Tüm `#çapa` hedefleri var: `#icerik` (105), `#menu` (160), `#hakkimizda` (129), `#galeri` (251), `#iletisim` (330) | index.html:75, 90-93, 122, 149 |
| ✅ | Tekrar eden `id` yok (hero-baslik, nav-menu, acik-rozet, sekme-*/panel-*, *-baslik hepsi benzersiz) | index.html geneli |
| ✅ | `aria-controls` / `aria-labelledby` hedefleri mevcut | index.html:85, 167-173 |
| ❌ | Çalışmayan yer tutucu bağlantılar: `#DOLDUR-harita-linki` (101, 118, 199, 295, 396, 422, 431), `#DOLDUR-telefon` (352, 400, 416, 435), `#DOLDUR-instagram` (268, 364, 401, 421), `#DOLDUR-e-posta` (357). Tıklayınca hiçbir şey olmaz; sayfa içi çapa gibi davranır | index.html |
| ⚠️ | `data-harita`, `data-telefon`, `data-instagram` özniteliklerini işleyen JS yok. Bağlantılar tek tek elle değiştirilmeli (16+ yer), tek noktadan yönetilmiyor | index.html, main.js |
| ⚠️ | Favicon yok (yorumda, 62-63). Tarayıcı `/favicon.ico` ister, konsolda 404 görünür | index.html:62-63 |
| ⚠️ | `og:image` yok (28-33 yorumda); paylaşımda görselsiz kart çıkar | index.html:28-33 |

## 2. HTML

| Durum | Madde | Referans |
|---|---|---|
| ✅ | `<!DOCTYPE html>`, `lang="tr"`, `charset`, `viewport` (zoom engellenmemiş) | index.html:1-5 |
| ✅ | Etiketler dengeli; `header/main/footer` düzgün kapanmış; `dl > div > dt/dd` geçerli | index.html geneli |
| ✅ | Başlık sırası: tek `h1`, bölümler `h2`, alt başlıklar `h3`; atlama yok (gizli `h3` 337 dahil) | index.html |
| ✅ | Logo `alt` var; dekoratif SVG ikonlar `aria-hidden="true" focusable="false"` | index.html:81 vd. |
| ✅ | JSON-LD geçerli JSON ve geçerli şema türü (`CafeOrCoffeeShop`) | index.html:48-60 |
| ⚠️ | JSON-LD `name` yer tutucu: `"[DOLDUR: dükkân adı]"` | index.html:52 |
| ⚠️ | Google Fonts URL'sindeki `&subset=latin-ext` CSS2 API'de geçersiz/yok sayılır (zararsız; Türkçe karakterler `unicode-range` ile zaten gelir) | index.html:68 |
| ⚠️ | `theme-color` sabit açık renk; koyu temada tarayıcı çubuğu uyumsuz. İki `meta` + `media="(prefers-color-scheme: ...)"` kullanılabilir | index.html:9 |
| ⚠️ | `<ul class="galeri" tabindex="0">`: 600px üstünde ızgara olduğu için kaydırma yok, ama gereksiz bir Tab durağı kalıyor; ayrıca kaydırılabilir bölge için `role="region"` önerilir | index.html:258 |

## 3. Mobil

| Durum | Madde | Referans |
|---|---|---|
| ✅ | Sabit genişlik yok; `max-width`, `clamp()`, `minmax(min(100%,…))` kullanılmış. Logo 150x40, `viewBox` oranıyla (240x64) uyumlu | style.css, index.html:81 |
| ✅ | Mobil öncelikli; kırılmalar 600/900/1200; gövde yazısı en az 16px (`--fs-m` 1rem) | style.css:26, 362-410 |
| ✅ | Dokunma hedefleri: düğmeler 48px, menü bağlantıları 56px, SSS özetleri 56px, hamburger 48x48 | style.css:52, 214, 315 |
| ✅ | Alt sabit çubuk `safe-area-inset-bottom` payı ve gövde `padding-bottom` ile footer'ı örtmüyor | style.css:88, 350-358 |
| ⚠️ | `body { overflow-x: hidden }` olası yatay taşmayı gizler; gerçek taşma varsa fark edilmez. 320px'de elle test edin | style.css:92 |
| ⚠️ | Metin içi bağlantılar (telefon/e-posta/Instagram `dd` içinde, footer listesi) ve logo bağlantısı 44px'den kısa (yaklaşık 24-40px). Minimum WCAG 2.2 (24px) geçer, 44px hedefi geçmez | index.html:352, 357, 364, 416, 421-422; style.css:191 |
| ⚠️ | İkincil metinler 16px altında: `--fs-s` (14,4px) ürün açıklaması, olanak metni, yorum imzası, ulaşım notu; `--fs-xs` (13px) telif. Okunur ama sınırda | style.css:24-25, 283, 291 |
| ⚠️ | "Şimdi açık" rozeti 900px altında hiç görünmez (`display:none`), oysa hedef kitle ağırlıkla mobil. Saat girilince bu bilgi mobilde kaybolur | style.css:223, 391 |
| ⚠️ | Menü bölümündeki "Yol Tarifi Al" düğmesi mobilde tam genişlik değil (tasarım 03 "mobilde tam genişlik" diyor); hero ve iletişimdeki düğmeler tam genişlik | index.html:199 |

## 4. Erişilebilirlik

| Durum | Madde | Referans |
|---|---|---|
| ✅ | "İçeriğe geç" bağlantısı var ve odakta görünür | index.html:75; style.css:117-123 |
| ✅ | Açık temada tüm renk çiftleri AA geçiyor (vurgu/beyaz 6,06:1; metin-soluk, ikincil, ana yeterli) | style.css:9-18 |
| ✅ | `prefers-reduced-motion` destekleniyor; `:focus-visible` her yerde tanımlı; footer'da beyaz override | style.css:103, 111, 342 |
| ✅ | Klavye ile menü: `aria-expanded`, `aria-controls`, Esc ile kapanma + odağı düğmeye döndürme; sekmelerde ok/Home/End | main.js:36-51, 66-79 |
| ✅ | Form yok (etiket sorunu yok); `.alan` stili ileride için hazır | style.css:158 |
| ✅ | Görünen metin ve `aria-label` uyumu (label-in-name): "Yol Tarifi Al" / "Google Haritalar'da yol tarifi al", "Ara" / "Dükkânı telefonla ara" | index.html:431, 435 |
| ❌ | Koyu temada "Şimdi açık" rozeti: zemin `--renk-ikincil` `#9DBB9F`, yazı `#fff` => yaklaşık 2,1:1 (AA için 4,5:1 gerekir). Tasarım 03 bunu "beyaz yazı 5,9:1" diye yalnızca açık tema için doğruluyor | style.css:65-66, 225 |
| ❌ | Hamburger ikonu hatası (aşağıdaki "Hemen düzeltilmeli" 1. madde): menü açılınca düğme boş görünür | index.html:87; style.css:201-203; main.js:32-33 |
| ⚠️ | Hero'da odak halkası `--renk-vurgu` (`#A8421F`) koyu gradyan üzerinde yaklaşık 2,7:1 (UI bileşeni için 3:1 gerekir); gerçek fotoğrafta daha da kötü olabilir. Hero içi için beyaz halka gerekir | style.css:103, 232-247 |
| ⚠️ | Sabit üst menü ve alt çubuk, Tab ile odaklanan öğeyi örtebilir (WCAG 2.2 "odak örtülmemeli"). `html { scroll-padding-top; scroll-padding-bottom }` yok (yalnızca `section[id]` için `scroll-margin-top`) | style.css:104 |
| ⚠️ | `role="status"` rozeti her dakika aynı metinle `textContent` yeniden yazıyor; bazı ekran okuyucular tekrar duyurabilir. Yalnızca metin değişince güncelleyin | main.js:143-149, 153 |
| ⚠️ | Menü sekmeleri 900px üstünde gizli; `tabpanel` öğeleri `aria-labelledby` ile gizli sekmelere bağlı kalıyor. Panellere `tabindex="0"` de önerilir (WAI-ARIA kalıbı) | index.html:166-189 |
| ⚠️ | SSS "+/−" simgesi CSS `content` olduğu için ekran okuyucuda okunabilir. `content: "+" / ""` biçimi alternatif metin verir | style.css:319, 322 |
| ⚠️ | Hamburger paneli dışarı tıklayınca / odak dışarı çıkınca kapanmıyor (yalnızca Esc, bağlantı tıklaması, boyut değişimi) | main.js:36-51 |
| ⚠️ | `matchMedia(...).addEventListener('change')` çok eski Safari (<14) sürümlerinde yok | main.js:50 |
| ⚠️ | Yer tutucu `role="img"` öğelerinin `aria-label` değerlerinde `[DOLDUR: ...]` metni ekran okuyucuya okunur | index.html:152, 259-264, 388 |

## 5. Performans

| Durum | Madde | Referans |
|---|---|---|
| ✅ | Raster görsel yok (yalnızca küçük SVG logo, `width/height` verilmiş) => yerleşim kayması yok | index.html:81 |
| ✅ | JS `defer`, tek dosya (~6 KB), framework yok; CSS tek dosya | index.html:70-71 |
| ✅ | `preconnect` + `display=swap`; sistem fontu yedeği tanımlı | index.html:66-68; style.css:22-23 |
| ⚠️ | Google Fonts tarama engelleyici (render-blocking) stil dosyası ve üçüncü taraf istek (KVKK/gizlilik açısından da not). Alternatif: fontları yerel `fonts/` altına almak | index.html:68 |
| ⚠️ | `setInterval` saat girilmese de her dakika çalışıyor (maliyeti ihmal edilebilir, ama `tanimli` değilse hiç kurulmayabilir) | main.js:153 |
| ⚠️ | Gerçek fotoğraflar gelince: hero hariç `loading="lazy"`, `width/height`, WebP, hero için `fetchpriority="high"` (hazır yorumda var, 107-111) | index.html:107-111 |
| ⚠️ | `backdrop-filter: blur` hem üst menüde hem alt çubukta; düşük donanımlı telefonlarda kaydırmayı yavaşlatabilir | style.css:187, 356 |

## 6. İçerik ve plan tutarlılığı

| Durum | Madde | Referans |
|---|---|---|
| ✅ | Başlık, meta açıklama, H1, hero alt başlığı, buton etiketleri, bölüm başlıkları, galeri/olanak/SSS metinleri `plan/02-metinler.md` ile birebir | index.html / 02 |
| ✅ | Türkçe karakterler ve yazım doğru (Hikâye, Dükkân, Atıştırmalıklar, Kadıköy'de vb.); tutarsız telefon/adres yok (henüz hiç gerçek veri yok) | index.html |
| ✅ | Meta açıklama yaklaşık 125 karakter (sınır 155) | index.html:8 |
| ⚠️ | SSS: 02 dosyasında 7 soru, sayfada 5 soru var. Nedeni HTML yorumunda belirtilmiş (brief 4-5 diyor); kasıtlı, kabul edilebilir | index.html:299 |
| ⚠️ | Plan belgelerinde title uzunluğu tutarsız: 02 "ad en fazla ~20 karakter", 05 "sabit kısım 43, ad en fazla 17" diyor. Gerçek sabit kısım (` \| Kadıköy'de Kahve ve Yol Tarifi`) 33 karakter => ad en fazla 27 karakter olabilir | 02:16; 05:17 |
| ⚠️ | 02'de "Ana başlık (8 kelime)" yazıyor; başlık 7 kelime (önemsiz belge hatası) | 02:35 |
| ⚠️ | 03-tasarim ile uygulama farkı: Olanaklar "600+ 4 sütun" (uygulama: 2 sütun, 900+ 3 sütun); Galeri "900+ 4 sütun" (uygulama: 3 sütun, 6 öğe için daha uygun). Uygulama mantıklı, belge güncellenmeli | 03:153; style.css:403-405 |
| ⚠️ | Olanaklar bölümünde "Ücretsiz Wi-Fi...", "Bilgisayarınızı şarj ederek..." gibi doğrulanmamış iddialar `[DOLDUR: var/yok]` önekiyle duruyor. Önek silinip satır bırakılırsa yanlış bilgi yayınlanır. Doğrulanmayan `<li>` tamamen silinmeli | index.html:214, 220, 226, 232 |
| ⚠️ | SSS 3. cevap iki alternatifi de görünür metin olarak içeriyor ("Evetse... Hayırsa...") | index.html:315 |
| ❌ | Ziyaretçiye görünen geçici etiketler: hero'da "Geçici görsel" etiketi; logoda "Dükkân Adı" ve "KADIKÖY · KAHVE" yer tutucu metni | index.html:114; logo.svg:38-39 |
| ⚠️ | "Mod Coffee" 03'te doğrulanamadı notu var; brief'te hâlâ geçiyor (site içeriğini etkilemez) | 01:64; 03:14 |

## 7. SEO dosyaları

| Durum | Madde | Referans |
|---|---|---|
| ❌ | `robots.txt` içindeki `Sitemap:` satırı ve `sitemap.xml` içindeki `<loc>` hâlâ `https://ORNEK-ALANADI.com/`. Böyle yayınlanırsa arama motorları var olmayan alan adını görür | robots.txt:5; sitemap.xml:5 |
| ✅ | Canonical bilerek kapalı (yanlış adrese yönlendirmeyi önlemek için); `robots` meta ve OG temel etiketleri aktif | index.html:10-26 |
| ⚠️ | `twitter:card=summary`; `og:image` eklenince `summary_large_image` yapılmalı (05 raporu da söylüyor) | index.html:24 |
| ⚠️ | Sitemap'te `changefreq`/`priority` Google tarafından yok sayılır; `lastmod` eklenebilir (önemsiz) | sitemap.xml:6-7 |

## 8. Güvenlik

| Durum | Madde | Referans |
|---|---|---|
| ✅ | Sayfada `target="_blank"` kullanan dış bağlantı yok => `rel="noopener"` gerekmiyor. Gerçek Instagram/harita bağlantıları eklenirken yeni sekme açılacaksa `rel="noopener noreferrer"` eklenmeli | index.html |
| ✅ | Form yok, hassas veri istenmiyor; satır içi JS / olay işleyici yok; `iframe` hazır kodunda `referrerpolicy` ve `title` var | index.html:386-387 |
| ⚠️ | Üçüncü taraf istek: Google Fonts (IP paylaşımı, gizlilik bildirimi gerekebilir). Yerel font tercih edilirse ortadan kalkar | index.html:66-68 |
| ⚠️ | Statik barındırmada `Content-Security-Policy` / `X-Content-Type-Options` başlıkları yok (Netlify `_headers` ile eklenebilir); zorunlu değil | n/a |

---

## Hemen düzeltilmeli

1. **Hamburger menü ikonu açılınca kayboluyor (❌).**
   Neden: `main.js` 32-33 satırlarında `ikonAc.hidden` / `ikonKapat.hidden` atanıyor ama bunlar SVG öğesi; SVG'de `hidden` IDL özelliği yok, bu atama öznitelik değiştirmez. HTML 87'deki `hidden` özniteliği sabit kalıyor ve `style.css:203` (`.nav__dugme .ikon--kapat[hidden]{display:none}`), 202'deki `display:block` kuralıyla aynı özgüllükte olup sonra geldiği için kazanıyor. Sonuç: menü açılınca iki ikon da gizli, düğme boş görünür (erişilebilir ad `aria-label` ile durur ama görsel kullanıcı için bozuk). Tarayıcıda doğrulayın.
   Çözüm: Ya 32-33'ü `setAttribute('hidden','')` / `removeAttribute('hidden')` ile değiştirin; ya da HTML 87'deki `hidden` özniteliğini ve CSS 203'ü silip yalnızca CSS 201-202'ye güvenin (başlangıçta `.ikon--kapat { display:none }` verin).

2. **Koyu temada rozet kontrastı (❌, style.css:225).**
   Çözüm: `.rozet` yazısını `color: var(--on-vurgu)` yapın (açık temada `#fff`, koyu temada `#17110D` => koyu zemin üzerinde okunur) ya da koyu temada `--renk-ikincil` yerine koyu yeşil bir zemin tanımlayın. Sonrası WebAIM ile ölçün (hedef en az 4,5:1).

3. **`robots.txt` ve `sitemap.xml` yer tutucu alan adı (❌).** Alan adı kesinleşince `ORNEK-ALANADI.com` ifadesini her iki dosyada değiştirin; aynı anda canonical, `og:url`, `og:image` yorumlarını açın. Alan adı yoksa bu iki dosyayı yayından çıkarın.

4. **Yer tutucu bağlantıların çalışır hale getirilmesi (❌).** Telefon (`tel:+90...`), harita (Google Haritalar paylaşım bağlantısı), Instagram, e-posta (`mailto:`) gerçek değerlerle her yerde (bölüm 1'deki satırlar) değiştirilmeli. Öneri: `main.js`'e `data-harita` / `data-telefon` / `data-instagram` özniteliklerini tek bir yapılandırma nesnesinden dolduran küçük bir kod ekleyin (tek yerden yönetim, unutma riski azalır). E-posta bağlantısı (357) `data-` özniteliği taşımıyor; ayrıca ele alın.

5. **Kullanıcıya görünen yer tutucu etiketler (❌).** Hero'daki "Geçici görsel" etiketi (index.html:114), logodaki "Dükkân Adı / KADIKÖY · KAHVE" (logo.svg:38-39), tüm "Geçici görsel" kutuları gerçek içerikle değiştirilmeden yayınlanmamalı.

6. **Doğrulanmamış olanak/SSS cümleleri (⚠️ ama yayın öncesi zorunlu).** Olanaklar kartlarında `[DOLDUR: var/yok]` öneki silinip cümle bırakılırsa yalnızca doğrulananlar kalmalı; doğrulanmayan `<li>` satırı tümüyle silinmeli (index.html:211-245). SSS cevapları (306-323) gerçek bilgiyle yazılmalı, 315'teki "Evetse/Hayırsa" seçeneklerinden yalnızca biri bırakılmalı.

## Önerilir

1. **Odak halkası (hero):** `.hero :focus-visible { outline-color: #fff; }` ekleyin (footer'daki gibi). Fotoğraf gelince tekrar kontrol edin.
2. **Sabit çubuklar ve odak:** `html { scroll-padding-top: calc(var(--nav-yukseklik) + 8px); scroll-padding-bottom: 88px; }` ekleyin ki Tab ile gezerken odaklanan öğe menü/alt çubuk altında kalmasın.
3. **Mobilde "Şimdi açık" bilgisi:** Saatler girildiğinde rozeti mobilde de göstermek için (ör. hero güven satırının yanında ya da menü çubuğunun altında) bir konum belirleyin. Hero'daki "bugünün çalışma saati" (index.html:124) JS ile otomatik doldurulabilir.
4. **Galeri:** `tabindex="0"` ve `aria-label`'ı yalnızca 600px altında (kaydırılabilirken) geçerli yapın veya `role="region"` ekleyin; masaüstünde gereksiz Tab durağını kaldırın.
5. **Rozet güncellemesi:** `rozet.textContent`'i yalnızca değer değiştiğinde atayın (ekran okuyucu tekrar duyurusunu önler); `setInterval`'i yalnızca saatler tanımlıysa kurun.
6. **Fontlar:** Mümkünse Fraunces ve Inter'i `site/fonts/` altına WOFF2 olarak alın (render-blocking üçüncü taraf istek ve gizlilik kaygısı biter; `file://` çalışmaya devam eder). Her halükârda `&subset=latin-ext` parametresini kaldırın.
7. **`theme-color`:** Açık/koyu için iki `meta` ekleyin.
8. **Favicon:** `img/favicon.svg` hazırlayıp 62-63 satırlarındaki yorumu açın. OG görseli (`img/og-gorsel.jpg`, 1200x630) ekleyince `twitter:card` değerini `summary_large_image` yapın.
9. **Dokunma alanı:** Metin içi telefon/e-posta/Instagram bağlantılarına ve footer bağlantılarına `display:inline-block; min-height:44px; padding-block` verin.
10. **Menü bölümü düğmesi** (index.html:199) mobilde tam genişlik olsun (03'e uyum).
11. **Panel ARIA:** Menü `tabpanel` öğelerine `tabindex="0"`; SSS "+/−" için `content: "+" / ""`.
12. **Plan belgelerini güncelleyin:** 02 ve 05'teki title uzunluğu hesabı (gerçek: sabit kısım 33 karakter, ad en fazla 27), 03'teki sütun sayıları, 02'deki "8 kelime".
13. **Gerçek cihaz testi:** 320px genişlik, iOS Safari, Android Chrome; `overflow-x:hidden`'ı geçici kaldırıp gizli taşma var mı bakın. Yayın sonrası PageSpeed Insights, WAVE/axe, schema.org doğrulayıcı ve Google Rich Results Test çalıştırın.
14. **JSON-LD:** Dükkân adı, telefon, `url`, `openingHoursSpecification`, `streetAddress`, `postalCode`, `hasMap`, `sameAs` eklenince yeniden doğrulayın (head'deki yorum rehberi hazır, 35-47).
15. **Gelecekte eklenen dış bağlantılar:** `target="_blank"` kullanılırsa `rel="noopener noreferrer"` ekleyin.

## Kullanıcının doldurması gerekenler

Sitede toplam **108 satırda `[DOLDUR]`** var (index.html 103, logo.svg 2, main.js 1, robots.txt 1, sitemap.xml 1). Benzersiz bilgi listesi:

**Kimlik**
- Dükkân adı: title (7), og:site_name (19), og:title (20), twitter:title (25), JSON-LD `name` (52), logo alt/aria-label (80-81), logo.svg (4, 9, 38), footer (411, 426), harita iframe başlığı (387, 388)
- Slogan (hero 116, footer 412)
- Logo ve marka rengi (varsa)

**İletişim ve konum**
- Açık adres (344), kısa adres (hero 124), mahalle/posta kodu/sokak (JSON-LD için)
- Telefon (+90 biçiminde): 352, 400, 416, 435, SSS 315; JSON-LD `telephone`
- E-posta (isteğe bağlı; yoksa 355-358 satırlarını silin)
- Google Haritalar paylaşım bağlantısı (7 yerde `#DOLDUR-harita-linki`) ve harita gömme kodu (386-391)
- Instagram / sosyal medya bağlantısı ve adı (268, 364, 401, 421)
- Ulaşım notu (382; yoksa silin)
- Alan adı: canonical (14), og:url, og:image, twitter:image (28-33), robots.txt, sitemap.xml
- Çalışma saatleri: gün gün (373-379), SSS 1 (306), `main.js` içindeki `SAATLER` nesnesi (12-20), JSON-LD, hero güven satırı (124)

**İçerik**
- Hikâye: kuruluş yılı, kurucu, açma sebebi (133)
- Çekirdek/kavurmacı bilgisi (138), demleme yöntemleri (142), atmosfer cümlesinin doğrulanması (146)
- Menü: 7 ürün satırı (ad, açıklama, fiyat) (177-193), fiyat güncelleme tarihi (163), alerjen/süt alternatifi notu (198)
- Olanaklar: Wi-Fi, priz, açık alan, evcil hayvan, ödeme yöntemleri, rezervasyon (214, 220, 226, 232, 238, 244); doğrulanmayanları silin
- Yorumlar: 2-3 gerçek ve izinli yorum, isim/baş harf (282-292); Google puanı (yalnızca doğrulanabilirse, 276)
- SSS cevapları: Wi-Fi/priz ve sakin saatler (310), rezervasyon (315), evcil hayvan (319), ödeme (323)

**Görseller**
- Hero fotoğrafı (hero.webp / hero-mobil.webp, 107-111), hakkımızda fotoğrafı (151-152) ve alt metni
- Galeri 6-8 fotoğraf ve her biri için alt metin (256-264)
- OG görseli 1200x630 (28-33), favicon (62-63)

**Teknik**
- JSON-LD ek alanları: `url`, `telephone`, `image`, `hasMap`, `sameAs`, `priceRange`, `geo`, `openingHoursSpecification`, `streetAddress`, `postalCode` (35-47)
- `data-harita`, `data-telefon`, `data-instagram` bağlantılarını gerçek `href` ile eşleştirme

---

## Genel özet

| Alan | Sonuç |
|---|---|
| Bağlantılar / dosya yolları | ✅ yollar ve çapalar doğru; ❌ yer tutucu bağlantılar |
| HTML geçerliliği | ✅ |
| Mobil | ✅ (⚠️ küçük iyileştirmeler) |
| Erişilebilirlik | ⚠️ 2 düzeltme (ikon hatası, koyu tema rozeti) |
| Performans | ✅ (görsel gelince yeniden bakılmalı) |
| İçerik / plan uyumu | ✅ metin uyumu; ❌ yer tutucular yayın engeli |
| Güvenlik | ✅ |
| SEO dosyaları | ❌ yer tutucu alan adı |

**Karar: ⚠️ Düzeltmeyle hazır.** "Hemen düzeltilmeli" 1-3 numaralı kod düzeltmeleri kısa sürer. 4-6 numaralı maddeler ve `[DOLDUR]` listesi tamamlanmadan yayına çıkılmamalı. Hepsi bitince `/site-kontrol` ile yeniden kontrol edin; o zaman karar ✅ Yayına hazır olabilir.
