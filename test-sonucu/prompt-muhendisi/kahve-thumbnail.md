# Kahve Videosu Thumbnail Promptları

## 1) Thumbnail promptu (hedef: Midjourney v7)

Neden Midjourney: Sinematik ışık, doku ve yüksek kontrastta güçlüdür; `--ar 16:9` desteği vardır. Görsel modeller İngilizce ile daha iyi çalıştığı için prompt İngilizcedir. Metin yapay zekâya yazdırılmaz (harfleri bozar); boş alan bırakılır, yazı Canva/Photoshop'ta eklenir.

```
Extreme close-up of a steaming black coffee in a white ceramic cup on a dark wooden table, dramatic rim lighting, thick rising steam lit from behind, glossy crema with a perfect swirl, scattered roasted coffee beans in the foreground, shallow depth of field, shot on 85mm f/1.8 lens, warm orange and deep teal color contrast, rich saturated colors, high contrast, cinematic, hyper-detailed, subject placed on the right third of the frame, large clean empty dark space on the left third for title text, dark blurred background with soft bokeh, no text, no letters, no watermark, no logo, no people, no clutter --ar 16:9 --style raw --v 7
```

### Neden böyle yazıldı
- Tek net odak (fincan) var; küçük ekranda bile okunur.
- Turuncu-turkuaz zıtlığı ve rim light, akış içinde dikkat çeker.
- "Sol üçte bir boş" kuralı yazı için alan bırakır.
- Negatif ifadeler (`no text`, `no logo`) bozuk yazı ve marka logosunu engeller.
- `--style raw` aşırı "yapay güzelleştirmeyi" azaltır.

### Doldurulacak / ayarlanacak noktalar
- Kahve türü: `black coffee` yerine `latte art`, `espresso shot`, `Turkish coffee in a copper cezve` vb.
- Yazı alanı yönü: video yazınız sağdaysa `left` ile `right` yer değiştirin.
- Yüz eklemek isterseniz: kendi fotoğrafınızı sonradan montajlayın (gerçek kişi taklidi önerilmez).

### Alternatif
**Kısa versiyon:**
```
Close-up steaming black coffee cup, dramatic backlight, dark background, orange and teal, high contrast, empty space on left for text, no text --ar 16:9 --v 7
```
**Daha yaratıcı versiyon:**
```
A giant coffee cup like a volcano erupting with glowing steam over a tiny miniature landscape, surreal, cinematic lighting, vivid orange and teal, high contrast, dark moody background, empty space on the left third for text, no text, no watermark --ar 16:9 --v 7
```

ChatGPT/DALL-E için: aynı promptun başına "Create a 16:9 YouTube thumbnail image:" ekleyin ve `--` parametrelerini silin.

---

## 2) Mevcut prompt değerlendirmesi

Mevcut prompt: `güzel bir kahve resmi yap`

**Puan: 12/100**

| Ölçüt | Puan | Not |
|---|---|---|
| Netlik | 3/10 | "Güzel" öznel; ne tür kahve belli değil |
| Bağlam | 1/10 | Kullanım amacı (thumbnail, afiş?) yok |
| Format | 0/10 | Oran, çözünürlük yok |
| Stil / ışık / kamera | 0/10 | Hiçbiri belirtilmemiş |
| Kısıtlar | 0/10 | Negatif ifade yok (yazı, logo vb.) |

**En büyük 3 sorun**
1. Konu belirsiz: fincan mı, çekirdek mi, kafe mi? Model rastgele seçer.
2. Stil, ışık ve kompozisyon yok; sonuç sıradan stok görsel olur.
3. Oran ve kullanım amacı yok; 16:9 çıkmaz, yazı alanı bırakılmaz.

**İyileştirilmiş hâli (Midjourney v7)**
```
Cozy cup of latte with detailed heart-shaped latte art on a rustic wooden table, soft warm morning window light from the left, rising steam, coffee beans and a cinnamon stick beside the cup, shallow depth of field, 50mm lens, warm brown and cream color palette, photorealistic, high detail, no text, no watermark --ar 16:9 --style raw --v 7
```

**Önce / sonra**

| | Önce | Sonra |
|---|---|---|
| Konu | "kahve" | Latte art, ahşap masa, tarçın, çekirdek |
| Işık | Yok | Soldan sıcak pencere ışığı |
| Kamera | Yok | 50mm, sığ alan derinliği |
| Renk | Yok | Kahve-krem paleti |
| Format | Yok | `--ar 16:9`, `--v 7` |
| Kısıt | Yok | Yazı ve filigran yok |
