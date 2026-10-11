# Tasarım Sistemi: Kadıköy Kahve Dükkânı (tek sayfa)

Dükkân adı: [DOLDUR: dükkân adı]. Logo ve marka rengi gelirse (brief: [DOLDUR: logo/renk]) `--renk-ana` ve `--renk-vurgu` onlara göre değiştirilir; kontrast oranları yeniden kontrol edilir.

## 0. İlham doğrulaması (brief bölüm 6)

Web aramasıyla kontrol edildi. Brief'teki "arama özetine dayanıyor" notu şu şekilde güncellendi:

| Brief'teki iddia | Durum | Not |
|---|---|---|
| Elementary Coffee: koyu katmanlı tek fotoğraf hero | **Doğrulanamadı** | Aramada bu site hiç çıkmadı. Tek kaynak olarak kullanılmadı. Koyu katmanlı hero fikri yine de yaygın ve geçerli bir kalıp; kendi kararımız olarak uygulanıyor. |
| Buzz Coffee: sade yapı, birkaç fotoğraf | **Kısmen doğrulandı** | Başka bir kaynak (alvarotrigo.com) çok sayıda ürün görseli ve açılış-kapanış saatleri olduğunu söylüyor. "Az bölüm, çok boşluk" iddiası doğrulanamadı. ManyPixels listesinde Buzz Coffee girdisini göremedik. |
| Zarla kafe örnekleri: güven, tek net eylem | **Genel olarak doğru** | Zarla'nın örneklerinde Kettle Black (Melbourne) tek "Book a Table" eylemi ve siyah-beyaz fotoğrafla öne çıkıyor. Kaffeine (Londra) açılış saatlerine marka kadar yer veriyor. Dineen Coffee Co. yapışkan menü çubuğu kullanıyor. Üçü de bizim kararlarımızı destekliyor. |
| Kadıköy: Montag, Walter's, Mod Coffee | **Kısmen doğrulandı** | yemek.com'da Walter's Coffee Roastery (Caferağa, Bademaltı Sk.) ve Montag (Kadıköy, Moda şubeleri) geçiyor. **Mod Coffee** aramada çıkmadı, brief'ten çıkarılması veya elle kontrolü önerilir. Venture Coffeeworks ve Story Coffee Moda da anılıyor. |

Tasarıma etkisi: üç ilkeyi ilhamdan değil, hedefe bakarak koruduk. (1) İlk ekranda tek CTA. (2) Açılış saatleri görünür olsun. (3) Gerçek fotoğraf, koyu katmanla okunur metin. Rakip siteler kopyalanmayacak.

## 1. Hava

**Sıcak, samimi, sade.** Krem zemin, espresso kahvesi metin, tek bir kiremit (terracotta) vurgu. Kadıköy'ün mahalle kahvecisi hissi, gösterişsiz.

## 2. Renk paleti

Aydınlık tema varsayılan; koyu tema `prefers-color-scheme: dark` ile otomatik açılır. Oranlar WCAG 2.x göreli parlaklık formülüyle elle hesaplandı (yaklaşık, ±0,1). Yayından önce bir kontrast aracıyla (ör. WebAIM Contrast Checker) doğrulayın.

### Aydınlık tema

| Değişken | Değer | Kullanım | Kontrast |
|---|---|---|---|
| `--arka-plan` | `#FAF6F0` | Sayfa zemini | , |
| `--yuzey` | `#FFFFFF` | Kart, form, menü paneli | , |
| `--metin` | `#2B1D14` | Gövde ve başlık | **15,1:1** arka plan üstünde, 16,3:1 yüzey üstünde |
| `--metin-soluk` | `#6B5A4D` | Alt metin, açıklama, fiyat notu | **6,1:1** arka plan, 6,6:1 yüzey |
| `--renk-ana` | `#5A3825` | Başlık vurgusu, footer zemini, ana renk | **9,6:1** arka plan; beyaz yazı üstünde 10,4:1 |
| `--renk-ikincil` | `#4F6B52` | Etiketler, ikonlar, "şimdi açık" rozeti (adaçayı yeşili) | **5,5:1** arka plan; beyaz yazı üstünde 5,9:1 |
| `--renk-vurgu` | `#A8421F` | Ana CTA düğmesi, bağlantılar (kiremit) | **5,6:1** arka plan; beyaz yazı üstünde **6,1:1** |
| `--kenar` | `#E4D9CB` | Süs çizgileri, kart kenarı (metin değil) | , |
| `--kenar-guclu` | `#8C7B6B` | Form alanı kenarı (arayüz bileşeni, en az 3:1) | 4,1:1 yüzey, 3,8:1 arka plan |

### Koyu tema

| Değişken | Değer | Kontrast |
|---|---|---|
| `--arka-plan` | `#17110D` | , |
| `--yuzey` | `#231A14` | , |
| `--metin` | `#F3EBE1` | **15,9:1** arka plan, 14,5:1 yüzey |
| `--metin-soluk` | `#B9A99A` | **8,2:1** arka plan, 7,5:1 yüzey |
| `--renk-ana` | `#D9B38C` (latte) | **9,6:1** arka plan |
| `--renk-ikincil` | `#9DBB9F` | **8,9:1** arka plan |
| `--renk-vurgu` | `#E07A52` | **6,3:1** arka plan, 5,8:1 yüzey. Düğme yazısı koyu (`#17110D`), 6,3:1 |
| `--kenar` | `#3A2D24` | süs |
| `--kenar-guclu` | `#85766A` | 3,9:1 yüzey |

### Hero katmanı (fotoğraf üstü yazı)

Beyaz yazı için fotoğrafın üstüne en az `rgba(23,17,13,.65)` koyu katman veya aşağıdan yukarı gradyan konur. En açık fotoğraf pikselinde bile yaklaşık 5,5:1 verir. %55 altına inmeyin (yaklaşık 4:1'e düşer). Gerçek fotoğraf gelince ekranda kontrol edin.

## 3. Yazı tipleri

Her iki font da **latin-ext** alt kümesine sahip; Türkçe karakterler (ç ğ ı İ ö ş ü) desteklenir. Aralarında harici bağımlılık tek istek: Google Fonts. `index.html` çift tıklayınca internet varsa yüklenir, yoksa sistem fontuna düşer (sayfa yine okunur ve bozulmaz).

- **Başlık:** Fraunces (yumuşak, sıcak serif), 600
- **Gövde:** Inter, 400/500/600

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap&subset=latin-ext" rel="stylesheet">
```

Not: `display=swap` yazının görünmesini geciktirmez. Çevrimdışı güvence için yedek yığın: `Georgia, 'Times New Roman', serif` ve `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`.

### Boyut ölçeği (akışkan, 360 px ile 1200 px arası)

| Değişken | Değer | Kullanım |
|---|---|---|
| `--fs-xs` | `clamp(0.8125rem, 0.79rem + 0.1vw, 0.875rem)` | Etiket, dipnot |
| `--fs-s` | `clamp(0.9rem, 0.87rem + 0.15vw, 0.975rem)` | Yardımcı metin |
| `--fs-m` | `clamp(1rem, 0.96rem + 0.2vw, 1.125rem)` | Gövde (en az 16 px) |
| `--fs-l` | `clamp(1.2rem, 1.1rem + 0.5vw, 1.5rem)` | Kart başlığı, alt başlık |
| `--fs-xl` | `clamp(1.6rem, 1.3rem + 1.5vw, 2.5rem)` | Bölüm başlığı (h2) |
| `--fs-xxl` | `clamp(2.25rem, 1.6rem + 3.2vw, 4rem)` | Hero başlığı (h1) |

Satır aralığı: gövde 1,6; başlık 1,15. Paragraf uzunluğu en çok `65ch`.

## 4. Boşluk, köşe, gölge

| Değişken | Değer |
|---|---|
| `--bosluk-1` | 4 px |
| `--bosluk-2` | 8 px |
| `--bosluk-3` | 16 px |
| `--bosluk-4` | 24 px |
| `--bosluk-5` | 40 px |
| `--bosluk-6` | 64 px |
| `--bolum-aralik` | `clamp(48px, 8vw, 96px)` (bölümlerin üst-alt boşluğu) |

- Köşe: `--kose-s` 8 px (düğme, form), `--kose-m` 16 px (kart, görsel), `--kose-tam` 999 px (rozet, hap düğme).
- Gölge (yumuşak, sıcak tonlu): `--golge-1: 0 1px 2px rgba(43,29,20,.08)`, `--golge-2: 0 8px 24px rgba(43,29,20,.12)`. Koyu temada gölge yerine `--kenar` çizgisi yeterli.

## 5. Bileşenler

Ortak kural: dokunmatik hedef en az **48x48 px**. Odak halkası her yerde görünür.

**Odak:** `:focus-visible { outline: 3px solid var(--renk-vurgu); outline-offset: 3px; }` (koyu temada da yeterli, vurgu rengi 3:1'in üstünde).

### Buton

| Durum | Stil |
|---|---|
| Ana ("Yol tarifi al") | Zemin `--renk-vurgu`, yazı beyaz (koyu temada `--arka-plan`), 6,1:1. Yükseklik 48 px, yan boşluk 24 px, `--kose-s`, ağırlık 600. Mobilde tam genişlik. |
| İkincil ("Menüyü gör", "Ara") | Saydam zemin, 2 px `--renk-ana` kenar, yazı `--renk-ana`. |
| Hover | Ana: zemin %8 koyulur (`filter: brightness(.92)`), 1 px yukarı kayar. İkincil: zemin `--renk-ana`, yazı `--yuzey`. |
| Focus | Yukarıdaki odak halkası. |
| Active | `transform: translateY(0)`, gölge yok. |
| Hero üstünde | İkincil düğme beyaz kenar ve beyaz yazı kullanır. |

### Kart (menü ürünü, olanak, yorum)

`--yuzey` zemin, 1 px `--kenar`, `--kose-m`, iç boşluk `--bosluk-4`, `--golge-1`; hover'da `--golge-2`. Menü kartı: ad (`--fs-l`, Fraunces) solda, fiyat sağda (`--renk-vurgu`, 600), altta açıklama (`--metin-soluk`). Fiyat noktalı çizgiyle bağlanabilir. Yorum kartı: alıntı italik değil, tırnak işareti büyük ve `--renk-ikincil`; altında isim/baş harf.

### Form alanı

Bu site satış/sipariş yapmıyor; form yalnızca ileride iletişim veya rezervasyon için gerekirse (brief: rezervasyon [DOLDUR: evet/hayır]). Stil hazır dursun: yükseklik 48 px, `--yuzey` zemin, 1 px `--kenar-guclu`, `--kose-s`, yazı 16 px (iOS yakınlaştırmasını önler). Etiket her zaman görünür (`<label>`, placeholder yerine geçmez). Hata: `--renk-vurgu` kenar + metin mesajı (yalnızca renkle belirtme).

### Navigasyon

- Yapışkan (`position: sticky; top: 0`), zemin `--arka-plan` %92 opak + `backdrop-filter: blur(8px)`, altında 1 px `--kenar`. Yükseklik 64 px.
- Sol: logo/ad. Sağ: bağlantılar (#menu, #hakkimizda, #galeri, #iletisim).
- **Mobil (900 px altı):** bağlantılar gizli, 48x48 hamburger düğmesi (`<button aria-expanded aria-controls="nav-menu" aria-label="Menüyü aç">`). Açılınca `--yuzey` tam genişlik panel, bağlantılar alt alta, her biri 56 px yüksek. Esc ve bağlantıya tıklama paneli kapatır.
- **Masaüstü (900 px ve üstü):** satır içi bağlantılar, sağda küçük "Yol tarifi al" düğmesi.
- Aktif bağlantı: altı 2 px `--renk-vurgu` çizgi.
- **Mobil alt çubuk:** ekranın altına sabit, iki düğme ("Yol tarifi" ana, "Ara" ikincil), yükseklik 64 px, `env(safe-area-inset-bottom)` payı, 900 px üstünde gizli. Sayfa sonuna `padding-bottom: 80px` verilir ki footer örtülmesin.

### "Şimdi açık" rozeti

Hap biçimli, `--renk-ikincil` zemin + beyaz yazı (5,9:1). Kapalıysa `--metin-soluk` kenar, saydam zemin. Her zaman yazı içerir ("Şimdi açık" / "Şu an kapalı"), yalnızca renge bağlı değil.

### SSS (`<details>`)

Satır yüksekliği en az 56 px, `summary` sağında artı/eksi ikonu (CSS ile döner), alt çizgi `--kenar`.

### Footer

Zemin `--renk-ana` (koyu temada `--yuzey`), yazı `#FAF6F0` (10,4:1). Üç sütun masaüstünde (ad + slogan, iletişim, sosyal), mobilde tek sütun. Bağlantılar altı çizili, hover'da kalınlaşır. En altta telif satırı (`--fs-xs`).

## 6. Düzen

- **Mobil öncelikli.** Temel stil 360 px içindir; büyük ekranlar `min-width` ile eklenir.
- Maksimum içerik genişliği: **1120 px**, ortalı; yan boşluk `clamp(16px, 5vw, 40px)`. Okuma metni sütunu `65ch`.
- Kırılma noktaları: **600 px** (küçük tablet), **900 px** (menü yatay olur, 2 sütun bölümler), **1200 px** (geniş masaüstü).
- Izgara: `display: grid; gap: var(--bosluk-4);` ve duyarlı sütunlar `repeat(auto-fit, minmax(min(100%, 260px), 1fr))`.
- Bölüm düzeni: Hakkımızda 1 sütun (mobil), 2 sütun metin + fotoğraf (900+). Menü: mobilde sekmeler (yatay kaydırılabilir, `scroll-snap`), masaüstünde 3 kategori yan yana. Olanaklar: mobilde 2 sütun, 600+ 4 sütun. Galeri: mobilde yatay kaydırma (`scroll-snap-type: x mandatory`, kart genişliği %80), 600+ 3 sütun ızgara, 900+ 4 sütun. Yorumlar: mobilde alt alta, 900+ 3 sütun.
- Hero: `min-height: 100svh` (en çok 760 px), içerik sol-altta, katman gradyanı. Hareket: `prefers-reduced-motion` için animasyon ve yumuşak kaydırma kapatılır.

## 7. Görseller

- **Fotoğraf stili:** gerçek mekân, sıcak doğal ışık (pencere ışığı), yakın plan kahve/el/buhar, az insan yüzü (izinli olanlar). Sıcak ton, hafif düşük doygunluk, tutarlı renk düzeltmesi. Yapay zekâ görseli kullanılırsa "örnek görsel" olarak işaretlenir (güven unsuru gerçek fotoğraftır). Yer tutucu: `--kenar` zeminli düz kutu + "[DOLDUR: fotoğraf]" etiketi.
- Oranlar: hero 16:9 (mobilde 4:5 kırpma), galeri 4:3 veya 1:1, hakkımızda 4:5. Her `<img>` için `width`/`height` verilir (kayma olmasın), `loading="lazy"` (hero hariç), WebP/JPG, genişlik en çok 1600 px, hero dışında 800 px.
- **İkonlar:** harici set yerine **inline SVG**, [Lucide](https://lucide.dev) (ISC lisansı, ücretsiz) çizgi stili: 24x24, 1,75 px çizgi, `stroke="currentColor"`, uçlar yuvarlak. Gereken ikonlar: `wifi`, `plug`, `sun` (açık alan), `paw-print`, `credit-card`, `map-pin`, `phone`, `instagram`, `clock`, `menu`, `x`, `coffee`, `chevron-down`. Dekoratif ikonlara `aria-hidden="true"`, tek başına düğme olanlara `aria-label`. Her SVG'yi doğrudan HTML'e gömmek çift tıklayarak açmayı bozmaz (harici dosya gerekmez). Lisans satırını koda yorum olarak ekleyin.
- Logo: metin tabanlı SVG (Fraunces, `--renk-ana`) + küçük fincan işareti. Gerçek logo gelince değişir.

## 8. Kopyala-yapıştır CSS

```css
:root {
  /* Renk: aydınlık tema */
  --renk-ana: #5A3825;       /* 9,6:1 arka plan üstünde */
  --renk-ikincil: #4F6B52;   /* 5,5:1 arka plan üstünde */
  --renk-vurgu: #A8421F;     /* 5,6:1 arka plan, beyaz yazıyla 6,1:1 */
  --arka-plan: #FAF6F0;
  --yuzey: #FFFFFF;
  --metin: #2B1D14;          /* 15,1:1 */
  --metin-soluk: #6B5A4D;    /* 6,1:1 */
  --kenar: #E4D9CB;
  --kenar-guclu: #8C7B6B;    /* form kenarı, 3,8:1+ */
  --on-vurgu: #FFFFFF;       /* vurgu düğmesi üstündeki yazı */
  --hero-katman: rgba(23, 17, 13, .65);

  /* Yazı tipi */
  --font-baslik: 'Fraunces', Georgia, 'Times New Roman', serif;
  --font-govde: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --fs-xs: clamp(0.8125rem, 0.79rem + 0.1vw, 0.875rem);
  --fs-s: clamp(0.9rem, 0.87rem + 0.15vw, 0.975rem);
  --fs-m: clamp(1rem, 0.96rem + 0.2vw, 1.125rem);
  --fs-l: clamp(1.2rem, 1.1rem + 0.5vw, 1.5rem);
  --fs-xl: clamp(1.6rem, 1.3rem + 1.5vw, 2.5rem);
  --fs-xxl: clamp(2.25rem, 1.6rem + 3.2vw, 4rem);

  /* Boşluk */
  --bosluk-1: 4px;
  --bosluk-2: 8px;
  --bosluk-3: 16px;
  --bosluk-4: 24px;
  --bosluk-5: 40px;
  --bosluk-6: 64px;
  --bolum-aralik: clamp(48px, 8vw, 96px);

  /* Köşe ve gölge */
  --kose-s: 8px;
  --kose-m: 16px;
  --kose-tam: 999px;
  --golge-1: 0 1px 2px rgba(43, 29, 20, .08);
  --golge-2: 0 8px 24px rgba(43, 29, 20, .12);

  /* Düzen */
  --maks-genislik: 1120px;
  --yan-bosluk: clamp(16px, 5vw, 40px);
  --okuma-genislik: 65ch;
  --nav-yukseklik: 64px;
  --dokunma: 48px;
  /* Kırılma noktaları (değişken @media içinde çalışmaz, not olarak): 600px, 900px, 1200px */

  color-scheme: light dark;
}

@media (prefers-color-scheme: dark) {
  :root {
    --renk-ana: #D9B38C;
    --renk-ikincil: #9DBB9F;
    --renk-vurgu: #E07A52;   /* 6,3:1 koyu zeminde */
    --arka-plan: #17110D;
    --yuzey: #231A14;
    --metin: #F3EBE1;        /* 15,9:1 */
    --metin-soluk: #B9A99A;  /* 8,2:1 */
    --kenar: #3A2D24;
    --kenar-guclu: #85766A;
    --on-vurgu: #17110D;     /* vurgu düğmesi yazısı 6,3:1 */
    --golge-1: none;
    --golge-2: 0 0 0 1px #3A2D24;
  }
}

/* Temel */
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--arka-plan);
  color: var(--metin);
  font: 400 var(--fs-m) / 1.6 var(--font-govde);
}
h1, h2, h3 { font-family: var(--font-baslik); line-height: 1.15; margin: 0 0 var(--bosluk-3); }
h1 { font-size: var(--fs-xxl); }
h2 { font-size: var(--fs-xl); }
h3 { font-size: var(--fs-l); }
:focus-visible { outline: 3px solid var(--renk-vurgu); outline-offset: 3px; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation: none !important; transition: none !important; }
}

/* Düğme */
.dugme {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--bosluk-2);
  min-height: var(--dokunma); padding: 0 var(--bosluk-4);
  background: var(--renk-vurgu); color: var(--on-vurgu);
  border: 2px solid transparent; border-radius: var(--kose-s);
  font: 600 var(--fs-m) var(--font-govde); text-decoration: none; cursor: pointer;
  transition: filter .15s, transform .15s, background .15s;
}
.dugme:hover { filter: brightness(.92); transform: translateY(-1px); }
.dugme:active { transform: none; }
.dugme--ikincil { background: transparent; color: var(--renk-ana); border-color: var(--renk-ana); }
.dugme--ikincil:hover { background: var(--renk-ana); color: var(--yuzey); filter: none; }

/* Kart */
.kart {
  background: var(--yuzey); border: 1px solid var(--kenar); border-radius: var(--kose-m);
  padding: var(--bosluk-4); box-shadow: var(--golge-1); transition: box-shadow .2s;
}
.kart:hover { box-shadow: var(--golge-2); }

/* Form alanı */
.alan {
  width: 100%; min-height: var(--dokunma); padding: 0 var(--bosluk-3);
  background: var(--yuzey); color: var(--metin);
  border: 1px solid var(--kenar-guclu); border-radius: var(--kose-s);
  font: 400 1rem var(--font-govde);
}

/* Düzen */
.kapsayici { width: 100%; max-width: var(--maks-genislik); margin-inline: auto; padding-inline: var(--yan-bosluk); }
.bolum { padding-block: var(--bolum-aralik); }
.izgara { display: grid; gap: var(--bosluk-4); grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); }
```
