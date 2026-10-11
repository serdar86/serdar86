# Brief: Kadıköy Kahve Dükkânı Tek Sayfa Sitesi

Dükkân adı: [DOLDUR: dükkân adı]

## 1. Amaç
- Site, dükkânı Kadıköy'de arayan kişilere tanıtmak ve onları dükkâna getirmek için var.
- Tür: tanıtım + yol tarifi (satış yok, online sipariş yok).
- **Tek ana hedef (CTA): "Yol tarifi al"** (Google Haritalar bağlantısı). İkincil CTA: telefon / Instagram.
- Başarı ölçütü: yol tarifi ve telefon tıklamaları.

## 2. Hedef kitle
- Kadıköy/Moda/Caferağa çevresinde yaşayan, çalışan veya gezen 20-45 yaş kahve severler; öğrenciler, uzaktan çalışanlar, çift ve arkadaş grupları. Bölgeye gelen turistler (ikincil).
- Cihaz: ağırlıklı **mobil** (Instagram/Google Haritalar'dan gelir, sokakta arar). Masaüstü ikincil.
- Aradıkları: "yakınımda iyi kahve", menü ve fiyat fikri, çalışma için uygun mu (Wi-Fi, priz), açık mı, nerede.
- Güven unsurları: gerçek mekân fotoğrafları, net adres ve saatler, menü, gerçek müşteri yorumları, Instagram bağlantısı.

## 3. Site haritası
Tek sayfa, tek dosya seti:
| Dosya | Amaç |
|---|---|
| `site/index.html` | Tüm içerik (bölümler aşağıda) |
| `site/css/style.css` | Stil, CSS değişkenleri |
| `site/js/main.js` | Mobil menü, kaydırma, "şimdi açık mı" göstergesi |
| `site/img/` | Görseller ve SVG'ler |

## 4. Bölümler (yukarıdan aşağıya, `index.html`)
1. **Üst menü (header):** Logo/ad + bölüm bağlantıları (#menu, #hakkimizda, #galeri, #iletisim). Mobilde hamburger. Yapışkan (sticky).
2. **Hero:** Tek güçlü başlık, kısa alt metin, tam ekran mekân/kahve fotoğrafı. CTA: "Yol tarifi al" + "Menüyü gör".
3. **Hakkımızda:** Dükkânın hikâyesi, kahve anlayışı, 2-3 vurgu (ör. çekirdek, demleme, atmosfer). Bir fotoğraf.
4. **Menü:** Kategoriler (sıcak, soğuk, tatlı/atıştırmalık). Ürün adı + kısa açıklama + fiyat. Mobilde sekme veya liste.
5. **Neden biz / olanaklar:** Küçük ikonlarla Wi-Fi, priz, açık alan, evcil hayvan dostu vb. (yalnızca doğrulananlar).
6. **Galeri:** 6-8 fotoğraf, mobilde kaydırılabilir ızgara.
7. **Yorumlar:** 2-3 gerçek müşteri yorumu (Google'dan alıntı, izinle).
8. **SSS:** 4-5 soru (açılış saati, Wi-Fi, rezervasyon, evcil hayvan, ödeme). Açılır-kapanır (`<details>`).
9. **İletişim ve konum:** Adres, saatler, telefon, Instagram, gömülü harita, büyük "Yol tarifi al" düğmesi.
10. **Footer:** Ad, telefon, sosyal bağlantılar, telif satırı.

Ek: Mobilde alta sabit "Yol tarifi / Ara" çubuğu.

## 5. İçerik ihtiyacı (kullanıcıdan gelecek, uydurulmayacak)
- Dükkân adı: [DOLDUR: dükkân adı]
- Slogan / tek cümle konumlandırma: [DOLDUR: slogan]
- Açık adres (mahalle, sokak, no): [DOLDUR: adres]
- Google Haritalar bağlantısı ve gömme kodu: [DOLDUR: harita linki]
- Telefon / WhatsApp: [DOLDUR: telefon]
- E-posta (isteğe bağlı): [DOLDUR: e-posta]
- Instagram ve diğer hesaplar: [DOLDUR: sosyal medya]
- Çalışma saatleri (gün gün): [DOLDUR: saatler]
- Hikâye: kuruluş yılı, kurucu, kahve anlayışı: [DOLDUR: hikâye]
- Kahve çekirdeği / kavurmacı bilgisi: [DOLDUR: çekirdek kaynağı]
- Menü ürünleri ve fiyatlar: [DOLDUR: menü ve fiyatlar]
- Olanaklar (Wi-Fi, priz, açık alan, evcil hayvan, ödeme yöntemleri): [DOLDUR: olanaklar]
- Gerçek müşteri yorumları (isim/baş harf ve izin): [DOLDUR: yorumlar]
- Fotoğraflar (mekân, kahve, ekip, en az 6-8): [DOLDUR: fotoğraflar]; yoksa geçici yer tutucu kullanılır ve açıkça işaretlenir.
- Logo ve marka renkleri varsa: [DOLDUR: logo/renk]
- Alan adı tercihi: [DOLDUR: alan adı]
- Rezervasyon alınıyor mu: [DOLDUR: evet/hayır]

## 6. İlham (web'den bulunan kaynaklar)
1. **Elementary Coffee** ([ManyPixels listesi](https://www.manypixels.co/blog/web-design/coffee-shop-websites)): tek özel fotoğraf + koyu katman (overlay) ile hero. Fikir: yazı okunur kalsın, hero tek fotoğrafla atmosfer versin.
2. **Buzz Coffee** (aynı liste): sade yapı, birkaç fotoğrafla mekân havası. Fikir: az bölüm, çok boşluk, net gezinme.
3. **Zarla kafe örnekleri** ([Zarla](https://www.zarla.com/inspiration/cafe)): güveni hızlı kurma, tek net eylem. Fikir: ilk ekranda tek CTA ve gerçek görseller.

Yerel referans (yalnızca sektör bağlamı): Kadıköy'de Moda, Caferağa çevresinde Montag, Walter's, Mod Coffee gibi specialty mekânlar var ([yemek.com](https://yemek.com/kadikoy-kahve-mekanlari/)). Rakip tonunu görmek için incelenebilir; kopya yapılmayacak.

Not: Sıralamayı ve görsel ayrıntıları tasarımcı ajan, bu sitelere bakıp doğrulamalı; arama özetine dayanıyor.

## 7. Teknik karar
- Saf **HTML5 + CSS3 + az JavaScript**. Framework, npm, build adımı yok.
- `site/index.html` çift tıklayınca açılmalı (göreli yollar, harici bağımlılık minimum).
- Mobil öncelikli (mobile-first), duyarlı ızgara (CSS Grid/Flexbox), CSS değişkenleri.
- Görseller: WebP/JPG, `loading="lazy"`, `alt` metinli; ikonlar ve logo SVG.
- Erişilebilirlik: anlamlı etiketler (`header`, `main`, `section`), yeterli kontrast, klavye ile kullanım.
- Yerel SEO: `LocalBusiness` JSON-LD, Kadıköy odaklı title/description (seo-uzmani).
- JS yalnızca: mobil menü, yumuşak kaydırma, "şimdi açık" göstergesi (saatler gelince).
- Yazı tipi: sistem fontu veya en fazla 1-2 yerel/Google font (tasarımcı karar verir).

## 8. Sıradaki adımlar
1. metin-yazari + tasarimci (paralel)
2. gorsel-yonetmen
3. gelistirici
4. seo-uzmani + kalite-kontrol
5. yayinci
