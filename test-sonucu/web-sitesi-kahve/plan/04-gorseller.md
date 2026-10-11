# Görsel Planı: Kadıköy Kahve Dükkânı (tek sayfa)

Dükkân adı: [DOLDUR: dükkân adı]

Kaynaklar: `plan/01-brief.md`, `plan/02-metinler.md`, `plan/03-tasarim.md`. Palet ve oranlar tasarım dosyasından alındı.

## 0. Temel kurallar

- **Güven unsuru gerçek fotoğraftır.** Yapay zekâ görselleri yalnızca geçici doldurma içindir. Sitede kullanılırsa görselin yanında veya `alt` içinde "örnek görsel" belirtilir. Gerçek fotoğraf gelince aynı dosya adıyla değiştirilir, HTML'e dokunmak gerekmez.
- **Telifli görsel, stok sitelerden kopya, başka kafelerin fotoğrafı veya marka logosu kullanılmaz.** Yapay zekâ promptlarında marka, kafe ya da kişi adı geçmez.
- **Gerçek olmayan bilgi gösterilmez.** Yapay zekâ görselinde okunabilir yazı, tabela, menü, fiyat veya logo bulunmamalıdır (promptlarda `no text` var).
- Biçim: WebP (kalite 78-82), yedek olarak JPG gerekmez (tüm güncel tarayıcılar WebP açar). Hero dışında hepsi `loading="lazy"`, hepsi `width`/`height` ile.
- Ton: sıcak doğal ışık, hafif düşük doygunluk, krem/espresso/kiremit ağırlıklı. Tüm görseller aynı renk düzeltmesiyle teslim edilir.
- Hedef dosya boyutu: hero en çok 220 KB, diğerleri en çok 120 KB.

### Renk referansı (promptlara yazılacak)

| Ad | Hex | Promptta karşılığı |
|---|---|---|
| Krem | `#FAF6F0` | warm cream |
| Espresso | `#2B1D14` / `#5A3825` | deep espresso brown |
| Kiremit | `#A8421F` | terracotta |
| Adaçayı | `#4F6B52` | muted sage green |
| Latte | `#D9B38C` | latte beige |

---

## 1. Görsel listesi

| # | Dosya | Nerede kullanılır | Ölçü (px) | Oran | Alt metin (Türkçe) |
|---|---|---|---|---|---|
| 1 | `site/img/hero.webp` | Hero arka planı (masaüstü, 600 px üstü) | 1600 x 900 | 16:9 | Pencere kenarında buharı tüten bir fincan kahve ve ahşap masa |
| 2 | `site/img/hero-mobil.webp` | Hero arka planı (mobil, `<picture>` ile 600 px altı) | 900 x 1125 | 4:5 | Pencere kenarında buharı tüten bir fincan kahve ve ahşap masa |
| 3 | `site/img/hakkimizda.webp` | Hakkımızda bölümü fotoğrafı | 800 x 1000 | 4:5 | Barista tezgâhta filtre kahve hazırlıyor (gerçek fotoğrafla: dükkânın içi, [DOLDUR: fotoğraf açıklaması]) |
| 4 | `site/img/galeri-1.webp` | Galeri: mekân genel görünümü | 800 x 600 | 4:3 | Dükkânın içinden genel görünüm: ahşap masalar ve pencere ışığı |
| 5 | `site/img/galeri-2.webp` | Galeri: tezgâh / bar | 800 x 600 | 4:3 | Kahve tezgâhı, espresso makinesi ve fincanlar |
| 6 | `site/img/galeri-3.webp` | Galeri: kahve fincanı | 800 x 800 | 1:1 | Latte sanatı yapılmış bir fincanın üstten görünümü |
| 7 | `site/img/galeri-4.webp` | Galeri: oturma alanı | 800 x 600 | 4:3 | Pencere önündeki rahat oturma köşesi |
| 8 | `site/img/galeri-5.webp` | Galeri: tatlı / atıştırmalık | 800 x 800 | 1:1 | Tabakta dilimlenmiş tatlı ve yanında kahve |
| 9 | `site/img/galeri-6.webp` | Galeri: ekip / barista (mutlaka gerçek) | 800 x 600 | 4:3 | Baristanın elleri kahveyi demliyor (gerçek: ekipten [DOLDUR: kişi, izinle]) |
| 10 | `site/img/galeri-7.webp` | Galeri: demleme yakın plan (isteğe bağlı) | 800 x 600 | 4:3 | Filtre kahve süzme anının yakın çekimi |
| 11 | `site/img/galeri-8.webp` | Galeri: dış cephe / giriş (isteğe bağlı, mutlaka gerçek) | 800 x 600 | 4:3 | Dükkânın Kadıköy'deki giriş kapısı ve sokak görünümü |
| 12 | `site/img/og-gorsel.jpg` | Sosyal paylaşım (Open Graph / Twitter kartı) | 1200 x 630 | 1.91:1 | (alt gerekmez, meta etikette `og:image:alt`: "[DOLDUR: dükkân adı], Kadıköy'de kahve dükkânı") |
| 13 | `site/img/logo.svg` | Header ve footer | 240 x 64 (vektör) | 15:4 | `alt="[DOLDUR: dükkân adı]"` (görsel ad yerine geçiyorsa) |
| 14 | `site/img/favicon.svg` | Sekme simgesi | 32 x 32 (vektör) | 1:1 | (dekoratif) |

Notlar:
- Galeri brief'te 6-8 fotoğraf. 1-6 zorunlu, 7-8 isteğe bağlı. Dosya adları sıralıdır; sıra değişirse yalnızca HTML sırası değişir.
- Hero için `<picture>` örneği:

```html
<picture>
  <source media="(max-width: 599px)" srcset="img/hero-mobil.webp" width="900" height="1125">
  <img src="img/hero.webp" width="1600" height="900" alt="Pencere kenarında buharı tüten bir fincan kahve ve ahşap masa" fetchpriority="high">
</picture>
```
- Alt metinler yer tutucu görseller içindir. Gerçek fotoğrafta içerikle birebir güncellenir; "fotoğraf" veya "görsel" kelimesiyle başlanmaz.
- Hero metni sol altta olduğundan, kompozisyonda sol alt üçte bir boş/sakin bırakılır. Hero üstüne `rgba(23,17,13,.65)` katman gelir.
- `og-gorsel.jpg` için hero görselinden 1200x630 kırpma + logo üstüne yerleştirilir (Canva veya Figma ile, yazı: dükkân adı).

---

## 2. Yapay zekâ promptları (geçici doldurma)

Midjourney, DALL-E ve Higgsfield için ortak İngilizce prompt. Her promptun sonuna ortak ek eklenir.

**Ortak ek (hepsinin sonuna):**
`natural window light, warm muted color grading, slightly desaturated, cream #FAF6F0, deep espresso brown #5A3825 and terracotta #A8421F accents, subtle sage green #4F6B52, soft film grain, realistic documentary photography, no text, no logos, no signage, no watermark, no brand names, no people's faces`

**Midjourney parametreleri:** `--style raw --v 7 --no text, logo, watermark, brand, neon, oversaturated` ve oran için aşağıdaki `--ar`.
**DALL-E:** Oranı cümle olarak yaz (ör. "wide 16:9") ve sonra ölçüye kırp.
**Higgsfield:** Aynı prompt, oranı arayüzden seçin.

### 1-2. Hero (`hero.webp` ve `hero-mobil.webp`)

```
A single ceramic cup of freshly brewed coffee with gentle steam rising, placed on a worn light oak table beside a large cafe window, soft morning side light, blurred cozy neighborhood cafe interior in the background with plants and wooden shelves, shallow depth of field, the left lower third of the frame calm and uncluttered for text overlay, inviting and quiet mood, [ortak ek] --ar 16:9 --style raw --v 7
```
Mobil için aynı prompt, `--ar 4:5` ve "subject centered slightly right, lower third calm" eklenerek ayrı üretilir. Dikey görseli yatay görselden kırpmak fincanı kesebilir.

### 3. Hakkımızda (`hakkimizda.webp`)

```
Over-the-shoulder view of a barista's hands pouring hot water over ground coffee in a pour-over dripper on a wooden counter, a gooseneck kettle, warm cafe interior softly blurred behind, face not visible, hands and equipment as focus, intimate craft atmosphere, [ortak ek] --ar 4:5 --style raw --v 7
```

### 4. Galeri 1, mekân genel görünümü (`galeri-1.webp`)

```
Interior of a small neighborhood coffee shop, light oak tables and simple chairs, large windows with daylight, hanging plants, terracotta pots, plaster wall in warm cream, empty and tidy, welcoming atmosphere, wide-angle but natural perspective, [ortak ek] --ar 4:3 --style raw --v 7
```

### 5. Galeri 2, tezgâh / bar (`galeri-2.webp`)

```
Coffee bar counter with a compact espresso machine, stacked ceramic cups, a grinder and a small plant, wooden counter top, warm side light from a window, shallow depth of field, no people, [ortak ek] --ar 4:3 --style raw --v 7
```

### 6. Galeri 3, kahve fincanı (`galeri-3.webp`)

```
Top-down view of a latte with simple leaf latte art in a matte cream ceramic cup and saucer on a dark espresso-brown wooden table, a small spoon beside, soft diffused light, minimal composition, [ortak ek] --ar 1:1 --style raw --v 7
```

### 7. Galeri 4, oturma alanı (`galeri-4.webp`)

```
Cozy corner seat by a window in a cafe, a small round wooden table, a worn terracotta-colored cushion on a bench, a book and a coffee cup on the table, a plant on the windowsill, golden afternoon light, calm and unhurried mood, [ortak ek] --ar 4:3 --style raw --v 7
```

### 8. Galeri 5, tatlı / atıştırmalık (`galeri-5.webp`)

```
A slice of simple homemade cake on a small ceramic plate beside a cup of black coffee, rustic light oak table, a linen napkin in sage green, close-up at a three-quarter angle, soft window light, appetizing but understated, no packaging, [ortak ek] --ar 1:1 --style raw --v 7
```

### 9. Galeri 6, ekip / barista (`galeri-6.webp`)

Mutlaka gerçek çekilmeli (bölüm 3). Geçici yer tutucu için:
```
Close-up of a barista's hands holding a portafilter and tamping ground espresso, apron in muted terracotta, wooden counter, face out of frame, warm window light, [ortak ek] --ar 4:3 --style raw --v 7
```
Yapay zekâ ile insan yüzü üretilmez. Ekip varmış gibi gösteren sahte görsel kullanılmaz.

### 10. Galeri 7, demleme yakın plan (`galeri-7.webp`)

```
Macro close-up of coffee dripping through a paper filter into a glass server, steam, dark rich coffee against warm blurred background, droplets in focus, [ortak ek] --ar 4:3 --style raw --v 7
```

### 11. Galeri 8, dış cephe (`galeri-8.webp`)

Gerçek çekilmesi şart: gerçek adres ve sokakla eşleşmek zorunda, yapay zekâ ile üretilmemeli. Geçici yer tutucu için bu görsel hiç kullanılmaz (galeri 7 görselle yeterli olur).

### 12. Sosyal paylaşım (`og-gorsel.jpg`)

Hero görselinin (gerçek ya da geçici) 1200x630 kırpması. Ayrı prompt gerekmez.

---

## 3. Mutlaka gerçek fotoğraf olması gerekenler

| Görsel | Neden | Çekim ipuçları |
|---|---|---|
| **Dış cephe / giriş** (`galeri-8`) | Ziyaretçi dükkânı sokakta tanımalı, yanlış beklenti güveni kırar | Gün ışığında, kapı net, tabela okunur; hem yakın hem sokaktan geniş kare. Yoldan geçen yüzler görünmesin veya bulanıklaştırılsın |
| **Ekip / barista** (`galeri-6`, `hakkimizda`) | Güven ve samimiyet; yapay zekâ ile sahte ekip yanıltıcıdır | Kişilerden yazılı/sözlü izin al. Yüz göstermek istemeyenler için eller ve fincan çekimi. Çalışırken, doğal anda çek |
| **Mekân iç görünüm** (`galeri-1`, `galeri-4`) | Wi-Fi/priz/oturma düzeni gibi kararları etkiler; "gerçekte nasıl" sorusunun cevabı | Pencere ışığı varken, kalabalık olmayan saatte, masalar düzenli. Telefon geniş açı lensi kullanılabilir ama çarpıtmayı düzelt |
| **Ürün: kahve ve tatlı** (`galeri-3`, `galeri-5`, `hero`) | Menüdeki ürünle birebir uyuşmalı | Pencere kenarında, üstten (flat lay) ve 45 derece olmak üzere iki açı. Buhar için taze demlenen kahve kullan. Fincanı ve zemini temizle |
| **Tezgâh / bar** (`galeri-2`) | Dükkânın karakterini ve ekipmanını gösterir | Tezgâh toplanmış, ekipman parlak; makine ve öğütücü kadrajda |

Genel çekim ipuçları:
1. **Işık:** Flaşı kapat. Pencere yan ışığı en iyisidir. En güzel saat sabah erken veya öğleden sonra.
2. **Telefon yeterli:** Lensi sil, HDR açık, ızgara açık. Yatay çek (hero 16:9 için), ayrıca dikey bir set çek (mobil hero 4:5).
3. **Hero için:** Sol alt üçte birini sakin bırak, metin oraya gelecek.
4. **Tutarlılık:** Aynı gün, benzer ışıkta çek. Düzenlemede aynı hazır ayarı (preset) uygula: sıcak, hafif düşük doygunluk.
5. **Her sahne için en az 5 kare** çek, en keskin olanı seç.
6. **Dosya hazırlığı:** Boyutlandır, WebP'ye çevir (Squoosh gibi bir araç), dosya adlarını bu plandakiyle eşleştir. EXIF konum bilgisini sil.
7. **İzin:** Müşteri yüzü görünen kare yayınlanmaz veya izin alınır.

---

## 4. Logo

### Üç fikir

1. **Fincan + buhar (seçilen):** Çizgi stilinde, yan görünüşlü fincan, üstünde iki kıvrık buhar çizgisi (kiremit), gövde espresso kahvesi; yanında Fraunces serif ad ve ince "KADIKÖY · KAHVE" alt satırı. Sıcak, mahalle kahvecisi havası; küçük boyutta (favicon) tek fincan işareti olarak da çalışır.
2. **Monogram damga:** Dükkân adının baş harfi daire içinde, daire kenarında "KADIKÖY" yazısı; mühür/kaşe hissi, el yapımı vurgusu. Ad belli olunca yapılabilir.
3. **Vapur + fincan:** Kadıköy iskelesini çağrıştıran basit vapur siluetinin bacasından çıkan buhar, fincan haline dönüşür. Yerel kimlik güçlü ama çizimi detaylı; küçük boyutta okunurluğu zayıf, bu yüzden ikinci planda.

### Seçilen: `site/img/logo.svg`

- Tek dosya, harici bağımlılık yok. Renkler: ana `#5A3825`, vurgu `#A8421F`; koyu temada `prefers-color-scheme` ile `#D9B38C` ve `#E07A52`.
- Ad metni yer tutucudur: "Dükkân Adı". `[DOLDUR: dükkân adı]` notu dosyada yorum olarak durur. Ad belli olunca `<text class="yazi">` içeriği değiştirilir; uzun adlarda `font-size` küçültülür ve `viewBox` genişliği artırılır.
- Önemli: `<img src="img/logo.svg">` olarak kullanıldığında SVG içindeki Fraunces yazı tipi yüklenmez (harici dosya/font erişimi yok), Georgia yedeği devreye girer. Ad kesinleşince metni yola (outline) çevirmek veya logoyu `<svg>` olarak HTML'e gömmek en güvenlisidir.
- Header'da yükseklik 40 px (`height="40"`), footer'da koyu zeminde (`#5A3825`) kullanılacaksa ayrı açık renkli sürüm gerekir: `.ana` ve `.vurgu` renkleri `#FAF6F0` yapılır.
- `favicon.svg` için sadece fincan işareti (32x32) çıkarılır: logo dosyasındaki `<g>` grubu `viewBox="0 0 44 52"` ile yeniden kullanılır.

---

## 5. İkonlar (inline SVG)

Stil: 24x24, `stroke="currentColor"`, çizgi 1,75, yuvarlak uçlar, `fill="none"`. Çizimler Lucide (ISC lisansı) tarzındadır. Lisans satırını koda yorum olarak ekleyin: `<!-- İkonlar: Lucide, ISC lisansı -->`.

Dekoratif ikonlara `aria-hidden="true"`; tek başına düğme olanlara düğmede `aria-label` verilir.

**Sık kullanılan SVG kabuğu:**
```html
<svg class="ikon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"> ... </svg>
```
Aşağıda yalnızca içerik verilir; kabuğun içine yerleştirin.

| Ad | Kullanım yeri | İçerik |
|---|---|---|
| `wifi` | Olanaklar: Wi-Fi | `<path d="M12 20h.01"/><path d="M2 8.82a15 15 0 0 1 20 0"/><path d="M5 12.859a10 10 0 0 1 14 0"/><path d="M8.5 16.429a5 5 0 0 1 7 0"/>` |
| `plug` | Olanaklar: priz | `<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>` |
| `sun` | Olanaklar: açık alan | `<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>` |
| `paw-print` | Olanaklar: evcil hayvan | `<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z"/>` |
| `credit-card` | Olanaklar: ödeme | `<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>` |
| `map-pin` | Adres, iletişim | `<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>` |
| `navigation` | "Yol tarifi al" düğmesi | `<polygon points="3 11 22 2 13 21 11 13 3 11"/>` |
| `phone` | "Ara" düğmesi, telefon | `<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>` |
| `camera` | Instagram bağlantısı (marka simgesi yerine genel kamera) | `<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>` |
| `clock` | Çalışma saatleri, "şimdi açık" | `<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>` |
| `menu` | Mobil menü açma | `<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>` |
| `x` | Mobil menü kapatma | `<path d="M18 6 6 18"/><path d="m6 6 12 12"/>` |
| `coffee` | Menü başlığı, hakkımızda vurgusu, geçici görsel | `<path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/>` |
| `chevron-down` | SSS (CSS ile döndürülür) | `<path d="m6 9 6 6 6-6"/>` |

Notlar:
- Instagram'ın kendi marka simgesi yerine `camera` önerildi: marka logosu kullanma kuralıyla çakışmamak için. Bağlantı metni "Instagram" açıkça yazılır.
- İkon yanında her zaman görünür metin olsun (yalnızca ikonla anlam taşıma).
- Menü ve kapat ikonları aynı düğmede JS ile `hidden` değiştirerek gösterilir.

---

## 6. Gerçek fotoğraf yoksa: CSS/SVG yer tutucu

Boş kutu yerine, sıcak tonlu, açıkça "geçici" etiketli bir yer tutucu kullanılır. Görsel dosyası olmayan her `<img>` yerine `<div class="yer-tutucu">` konur; dosya gelince `<img>` ile değiştirilir.

```html
<div class="yer-tutucu yer-tutucu--4-3" role="img" aria-label="Geçici görsel: dükkânın içi">
  <svg class="ikon" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
    <path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/>
  </svg>
  <span>Geçici görsel</span>
</div>
```

```css
.yer-tutucu {
  display: grid; place-content: center; justify-items: center; gap: var(--bosluk-2);
  width: 100%;
  background:
    radial-gradient(circle at 25% 20%, rgba(168, 66, 31, .14), transparent 55%),
    radial-gradient(circle at 80% 85%, rgba(79, 107, 82, .16), transparent 50%),
    linear-gradient(135deg, var(--kenar), var(--arka-plan));
  color: var(--metin-soluk);              /* 6,1:1 */
  border: 1px dashed var(--kenar-guclu);
  border-radius: var(--kose-m);
  font-size: var(--fs-s); font-weight: 500; text-align: center;
}
.yer-tutucu--4-3  { aspect-ratio: 4 / 3; }
.yer-tutucu--1-1  { aspect-ratio: 1 / 1; }
.yer-tutucu--4-5  { aspect-ratio: 4 / 5; }
.yer-tutucu--16-9 { aspect-ratio: 16 / 9; }

/* Hero yer tutucusu: fotoğraf yokken de koyu katman ve beyaz yazı çalışsın */
.hero--yer-tutucu {
  background:
    radial-gradient(circle at 70% 30%, rgba(168, 66, 31, .45), transparent 55%),
    linear-gradient(160deg, #5A3825, #2B1D14 70%, #17110D);
}
```

Kurallar:
- Her yer tutucuda görünür "Geçici görsel" etiketi bulunur; yayından önce hepsi gerçek fotoğrafla değiştirilmelidir (kalite-kontrol listesine ekle).
- Hero yer tutucusunda beyaz yazı koyu gradyan üstünde 10:1 üzerinde kontrast verir.
- Koyu temada değişkenler otomatik uyar (`--kenar`, `--arka-plan` koyu tonlara döner).
- Daha zengin bir alternatif: bölüm 2'deki yapay zekâ görselleri, "örnek görsel" etiketiyle.

---

## 7. Yapılacaklar listesi

1. Kullanıcıdan gerçek fotoğraflar istenir ([DOLDUR: fotoğraflar]); en az: dış cephe, iç mekân, tezgâh, 2 ürün, ekip (izinli).
2. Gelene kadar CSS yer tutucu (bölüm 6) veya "örnek görsel" etiketli yapay zekâ görselleri kullanılır.
3. Dükkân adı belli olunca `logo.svg` metni güncellenir, `favicon.svg` ve `og-gorsel.jpg` üretilir.
4. Kalite-kontrol: tüm `alt` metinleri, boyutlar, `width`/`height`, dosya boyutları, "Geçici görsel" etiketlerinin kalkması.
