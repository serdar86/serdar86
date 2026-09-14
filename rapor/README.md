# Hangi Uygulama Tutar — reklam ömrü analizi

Instagram/Facebook reklam verisinden hareketle, solo bir geliştiricinin reklamla
kâr edebileceği uygulama nişlerinin sıralaması.

**Rapor:** [`index.html`](index.html) — yayımlanmış hali:
<https://claude.ai/artifact/GK4rWi2Svxj93jp9b2fNku> *(özel bağlantı, yalnızca hesap sahibi açabilir)*

**Tarama aracı:** [`../adscan/`](../adscan/)

## Yöntemin özeti

Temel varsayım: reklamveren para kaybettiren reklamı aylarca ödemez, dolayısıyla
**reklam ömrü kârlılığın dolaylı göstergesidir.** 2026 için iki düzeltme gerekiyor:

1. **Eski reklam tek başına kanıt değil.** Cost-cap ve Advantage+ ile çalışan hesaplar
   kazanmayan reklamı kapatmadan bırakabiliyor. Ömrü her zaman **yenileme temposuyla
   birlikte** okuyun — eski reklam + sıfır yeni kreatif = unutulmuş hesap.
2. **Kreatif ömrü kısaldı.** Meta'nın Andromeda sıralaması kreatif sinyallerine daha sert
   ağırlık veriyor; eskiden altı hafta dayanan konsept artık iki-üç haftada kitlesini yakıyor.

## En kritik kısıt

Meta durdurulmuş reklamları **yalnızca AB ve İngiltere için** saklıyor (~1 yıl geriye).
ABD veya Türkiye hedefli bir reklam kapatıldığında Ad Library'den tamamen kayboluyor.
Aynı kısıt API'de de var: `ad_type=ALL` ticari reklamları yalnızca AB/UK sorgularında
döndürüyor.

**Sonuç:** "reklam ne zaman kapandı" analizi sadece AB üzerinden yapılabilir. Bu yüzden
`adscan` varsayılan olarak Almanya/Hollanda/Fransa sorguluyor.

## Sonuç sıralaması

| Kademe | Niş | Neden |
|---|---|---|
| **A** | Uyku & horlama kaydı | Teknik bar düşük, kreatif kendini satıyor, yerleşik dev yok |
| **A** | Vücut tarama & ilerleme fotoğrafı | Önce/sonra formatı evergreen — en uzun ömürlü reklamlar burada |
| **A** | Dikey kalori takibi | Cal AI kanıtı güçlü ama genel kategori doymuş; sadece dar kama |
| **A** | Astroloji & manifestasyon | Teknik barı en düşük, kanca malzemesi sonsuz, CPI düşük |
| **B** | AI fotoğraf / portre | Kanıtlı ama kreatif yanması ve CPI acımasız |
| **B** | AI companion | Kategori kazanıyor, ama Meta'da değil — Reddit'e kaymış |
| **B** | Yüzsüz video araçları | Gerçek talep, ama web SaaS kalıbı; mobil abonelik işi değil |
| **C** | Genel tarayıcı / meditasyon / kalori | CPI yerleşiklerce ezilmiş |

## Dürüstlük notu

Rapor hazırlanırken bulunduğum ortamda `facebook.com` ağ politikasıyla engelliydi,
bu yüzden **Ad Library'ye canlı bağlanılamadı.** Rapordaki rakamlar yayımlanmış
kaynaklardan geliyor; ömür imzaları ise yöntemin kendisinden. Canlı doğrulamayı
`adscan` ile kendi makinenizde yapın — araç tam da bunun için yazıldı.
