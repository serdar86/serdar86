# adscan — Meta Ad Library reklam ömrü tarayıcısı

Instagram/Facebook reklamlarının **ne zaman açıldığını ve ne zaman kapatıldığını**
çeker, reklamveren bazında ömür dağılımı çıkarır ve "bu hesap para basıyor mu?"
sorusuna skor verir.

## Neden bu araç?

Ad Library arayüzünde tek tek reklama bakıp "şu tarihten beri yayında" yazısını
okumak 20 reklamda işe yarar, 2000 reklamda yaramaz. Bu araç aynı veriyi API'den
toplu çekip **ömür istatistiğine** çevirir.

## Kritik kısıt — önce bunu okuyun

Meta'nın kuralı (aracın sınırı değil):

| Ne istiyorsunuz | ABD/Türkiye | AB + UK |
|---|---|---|
| Aktif ticari reklamlar | ✅ (sadece web arayüzü) | ✅ API + web |
| **Kapatılmış reklamlar / kapanma tarihi** | ❌ yok | ✅ ~1 yıl geriye |
| API ile `ad_type=ALL` | ❌ boş döner | ✅ çalışır |

Yani **"reklam ne zaman kapandı" analizi yalnızca AB hedefli reklamlarda
mümkün.** Varsayılan ülkeler bu yüzden AB. ABD pazarını ölçmek istiyorsanız:
o uygulamalar AB'de de reklam veriyorsa oradan okuyun — kreatif ve ömür
davranışı büyük ölçüde aynıdır.

## Kurulum

Bağımlılık yok, sadece Python 3.10+.

```bash
python3 adscan/adscan.py --selftest   # ağ gerekmez, mantığı doğrular
```

### Token alma

1. `facebook.com/ID` üzerinden kimlik doğrulaması yapın (1–3 iş günü).
2. `developers.facebook.com` → yeni uygulama → **Ad Library API** ürününü ekleyin.
3. Access token üretin.

```bash
export META_AD_LIBRARY_TOKEN="EAAB..."
```

## Kullanım

```bash
# Niş taraması
python3 adscan/adscan.py --query "calorie tracker" --countries DE,NL,FR

# Belirli rakipler (Page ID ile, en fazla 10)
python3 adscan/adscan.py --pages 1234567890,9876543210

# Tam döküm
python3 adscan/adscan.py --query "sleep tracker" \
    --csv ozet.csv --ads-csv reklamlar.csv
```

## Çıktıyı okuma

```
REKLAMVEREN                   SKOR AKTIF  EN ESKI   90G+  YENI30  KARAR
Acme Sleep                    78.4    12     412g    34%       6  PARA BASIYOR
```

| Kolon | Anlamı |
|---|---|
| `EN ESKI` | Hâlâ yayında olan en eski reklamın gün sayısı |
| `90G+` | Ömrü 90 günü geçmiş reklamların oranı (kalıcı kreatif) |
| `YENI30` | Son 30 günde açılan yeni reklam sayısı (canlılık) |
| `median_life_of_killed_ads` | Kapatılan reklamların medyan ömrü — **testi ne kadar hızlı kesiyorlar** |
| `infant_mortality_14d` | Kapatılanların 14 günde ölme oranı — yüksekse hâlâ arıyorlar |

### Kararlar

- **PARA BASIYOR** — 90 gün+ ayakta reklam **ve** son 30 günde ≥3 yeni kreatif.
  Kopyalanacak hesap budur.
- **ÖLÇEKLENİYOR** — çok yeni reklam, henüz 90 günü dolan yok. Yeni bir kazanan
  doğuyor olabilir; en erken sinyal burası.
- **UNUTULMUŞ** — eski reklam var ama sıfır yenileme. **Tuzak:** 2026'da
  cost-cap/Advantage+ ile reklamı kapatmayı unutmak yaygın. Eski reklam tek
  başına kanıt değildir, skoru yarıya düşürülür.
- **TEST EDİYOR** — reklamların çoğu 14 günde ölmüş. Niş henüz çözülmemiş.

## Yöntemin sınırı

Ad Library harcama göstermez (siyasi reklamlar hariç). Ömür, harcamanın
**dolaylı** göstergesidir. Bir hesabın 400 günlük reklamı olması, o reklamın
bugün kârlı olduğunu değil, kapatılmadığını söyler — bu yüzden skor, ömrü
tek başına değil **yenileme temposuyla birlikte** değerlendirir.
