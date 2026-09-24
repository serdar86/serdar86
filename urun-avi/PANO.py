# -*- coding: utf-8 -*-
"""PANO.py - dropshipping urun avi panosunu OLCULEN kosudan uretir.

Kullanim:
    python3 PANO.py ham.json pano.html

Baska hicbir sey gerekmez. Kurulum yok, anahtar yok, ikinci dosya yok.
Gorselleri kendi indirir, kucultur ve sayfanin icine gomer; boylece pano
tek basina acilir, tedarikcinin sunucusu kapansa bile bozulmaz.

Panoda hicbir rakam elle yazilmaz. Hepsi ham.json icinden gelir.
ham.json'un tasimasi gereken alanlar icin: asagidaki SOZLESME bolumu.
"""
import base64
import concurrent.futures as cf
import datetime
import html
import io
import json
import re
import statistics
import sys
import urllib.request

# ==================================================================== SOZLESME
# ham.json su ust duzey anahtarlari tasir. Eksik olan varsa script daha ilk
# satirda adiyla soyler, yarim pano uretmez.
#
#   girdi        {nis, tohum[], pazar{ad, location_code, language_code},
#                 satis_bandi[alt, ust], aylik_reklam_butcesi, tedarik, magaza}
#   kazanan      {kelime, hacim, cpc, zorluk, buyume, marj_usd,
#                 aylik[{a, y, h}] (yeniden eskiye, 12 ay),
#                 tedarik{listelenen, eslesen_oran, bantta, medyan, min}}
#   tedarik_urunleri [{baslik, fiyat_usd, gorsel, satildi, renk}]
#   perakende    [{alan, url, medyan, min, max, adet}]
#   rakip_guc    [{alan, organik_trafik, organik_kelime}]
#   videolar     [{baslik, kanal, goruntulenme, link, kapak, sure}]
#   elenenler    [kazanan ile ayni bicim, marj_usd olmadan]
#   gecen        [kazanan ile ayni bicim]
#   cagrilar_asama_c / cagrilar_asama_d  [{uc, http, maliyet_micros, saniye}]
#   bakiye_d     {g0, g1, t0, t1}   kosu oncesi/sonrasi micros bakiye
#   bakiye_onceki_asamalar {genel_fark, gtm_fark}   yoksa sifir sayilir

ZORUNLU = ["girdi", "kazanan", "tedarik_urunleri", "perakende", "rakip_guc",
           "videolar", "elenenler", "gecen", "bakiye_d"]

if len(sys.argv) < 3:
    sys.exit("Kullanim: python3 PANO.py ham.json pano.html")
ham_yol, cikti_yol = sys.argv[1], sys.argv[2]

try:
    D = json.load(open(ham_yol, encoding="utf-8"))
except FileNotFoundError:
    sys.exit(f"HATA: {ham_yol} bulunamadi.")
except json.JSONDecodeError as ex:
    sys.exit(f"HATA: {ham_yol} gecerli JSON degil. {ex}")

eksik = [k for k in ZORUNLU if k not in D]
if eksik:
    sys.exit("HATA: ham.json'da su anahtarlar yok: " + ", ".join(eksik)
             + "\nSozlesme icin bu dosyanin basindaki SOZLESME bolumune bak.")

# ============================================================ gorsel gomme
# Once adresi CDN'in kucuk surumune cevirir, sonra indirir, sonra base64 gomer.
# Pillow varsa ayrica yeniden boyutlandirir; yoksa da calisir.
try:
    from PIL import Image
    PILLOW = True
except ImportError:
    PILLOW = False

TARAYICI = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def kucuk_adres(u, en):
    """Tanidik CDN'lerde kucuk surumu iste. Tanimayinca adresi oldugu gibi birak."""
    if "alicdn" in u or "aliexpress" in u:
        return re.sub(r"_\d+x\d+(q\d+)?", f"_{en}x{en}q75", u, count=1)
    if "ytimg.com" in u:
        return re.sub(r"/[a-z0-9]+default\.jpg.*$", "/mqdefault.jpg", u)
    return u


def adres(u):
    """Gorsel adresi: duz metin ya da {"static": ...} sozlugu kabul edilir."""
    if isinstance(u, dict):
        u = u.get("static") or u.get("url") or ""
    return u or ""


def cek(par):
    u, en = par
    try:
        istek = urllib.request.Request(kucuk_adres(u, en), headers=TARAYICI)
        ham = urllib.request.urlopen(istek, timeout=25).read()
        if PILLOW:
            im = Image.open(io.BytesIO(ham)).convert("RGB")
            if im.width > en:
                im = im.resize((en, round(im.height * en / im.width)), Image.LANCZOS)
            tampon = io.BytesIO()
            im.save(tampon, "JPEG", quality=74, optimize=True, progressive=True)
            ham = tampon.getvalue()
            tur = "jpeg"
        else:
            tur = "avif" if ham[4:12] == b"ftypavif" else ("png" if ham[:4] == b"\x89PNG" else "jpeg")
        if len(ham) > 900_000:          # tek gorsel sayfayi sisirmesin
            return u, None, "cok buyuk"
        return u, f"data:image/{tur};base64," + base64.b64encode(ham).decode(), len(ham)
    except Exception as ex:             # indirilemeyen gorsel panoyu dusurmez
        return u, None, str(ex)[:60]


hedef = [(adres(u["gorsel"]), 300) for u in D["tedarik_urunleri"] if u.get("gorsel")]
hedef += [(adres(v.get("kapak")), 440) for v in D["videolar"][:6] if v.get("kapak")]
hedef = [h for h in hedef if h[0]]

GOMULU, kacan, toplam = {}, 0, 0
if hedef:
    print(f"gorsel indiriliyor: {len(hedef)} adet"
          + ("" if PILLOW else "  (Pillow yok, CDN kucuk surumu kullaniliyor)"))
    with cf.ThreadPoolExecutor(8) as havuz:
        for u, veri, bilgi in havuz.map(cek, hedef):
            if veri:
                GOMULU[u] = veri
                toplam += bilgi
            else:
                kacan += 1
    print(f"gomuldu {len(GOMULU)}/{len(hedef)} | {toplam / 1024:.0f} KB"
          + (f" | {kacan} gorsel indirilemedi, adresi birakildi" if kacan else ""))

# ------------------------------------------------------------------ yardimcilar
def img(u):
    u = adres(u)
    return GOMULU.get(u, u)


def ts(n, ondalik=0):
    """Turkce sayi: binlik nokta, ondalik virgul."""
    if n is None:
        return "-"
    s = f"{n:,.{ondalik}f}"
    tam, _, kus = s.partition(".")
    tam = tam.replace(",", ".")
    return tam + ("," + kus if kus else "")


def e(s):
    return html.escape(str(s if s is not None else ""))


AY = ["Oca", "Sub", "Mar", "Nis", "May", "Haz", "Tem", "Agu", "Eyl", "Eki", "Kas", "Ara"]

# ------------------------------------------------------------------ olculen degerler
G = D["girdi"]
K = D["kazanan"]
ALT, UST = G["satis_bandi"]
ORTA = (ALT + UST) / 2
TED = K["tedarik"]["medyan"]
MARJ = K["marj_usd"]
CPC = K.get("cpc") or 0
TIK = MARJ / CPC if CPC else None                    # basabas icin gereken tiklama
BUTCE_TIK = G["aylik_reklam_butcesi"] / CPC if CPC else None
BUTCE_SATIS = BUTCE_TIK / TIK if (TIK and BUTCE_TIK) else None

AYLIK = list(reversed(K.get("aylik") or []))         # eskiden yeniye
ENB_H = max([m["h"] for m in AYLIK] or [1]) or 1
SON3 = AYLIK[-3:]

URUN = sorted([u for u in D["tedarik_urunleri"] if u.get("gorsel")],
              key=lambda u: -u.get("renk", 0))
PER = sorted(D["perakende"], key=lambda p: p["medyan"])
GUC = {g["alan"]: g for g in D["rakip_guc"]}
ENB_TRF = max([g["organik_trafik"] for g in D["rakip_guc"]] or [1]) or 1
IKINCI = [g for g in D.get("gecen", []) if g["kelime"] != K["kelime"]]
VIDEO = [v for v in D["videolar"] if v.get("kapak")]
CAGRI = D.get("cagrilar_asama_c", []) + D.get("cagrilar_asama_d", [])
B = D["bakiye_d"]
# Kosu tek parca da olcumus olabilir, iki parca da. Her parcanin farki ayri olculur,
# toplam bu olculmus farklarin toplamidir. Hicbir rakam elle yazilmaz.
ONCEKI = D.get("bakiye_onceki_asamalar") or {"genel_fark": 0, "gtm_fark": 0}
BAKIYE_FARK = ((B["g0"] - B["g1"]) + (B["t0"] - B["t1"])
               + ONCEKI.get("genel_fark", 0) + ONCEKI.get("gtm_fark", 0)) / 1e6

# ------------------------------------------------------------------ fiyat merdiveni
MERDIVEN = (
    [("En ucuz tedarikci ilani", K["tedarik"]["min"], "ted"),
     ("Tedarikci medyani", TED, "ted")]
    + [(p["alan"], p["medyan"], "per") for p in PER]
)
MERDIVEN = [m for m in MERDIVEN if m[1] is not None]
OLCEK = (max([v for _, v, _ in MERDIVEN] or [UST]) or 1) * 1.12


def x(v):
    return max(0.0, min(100.0, v / OLCEK * 100))


BANT_ORTA = (x(ALT) + x(UST)) / 2
merdiven_html = "".join(
    f'<div class="mr {sinif}">'
    f'<span class="ad">{e(ad)}</span>'
    f'<span class="cizgi"><i style="width:{x(v)}%"></i></span>'
    f'<span class="dg num">{ts(v, 2)} $</span></div>'
    for ad, v, sinif in MERDIVEN)

# Merdivenin iki ucu: en dusuk ve en yuksek OLCULMUS fiyat. Baslikta bu ikisi yazar.
MERDIVEN_ALT = min([v for _, v, _ in MERDIVEN] or [0])
MERDIVEN_UST = max([v for _, v, _ in MERDIVEN] or [0])

# ------------------------------------------------------------------ elenme gerekcesi (olcumden)
def gerekce(r):
    t = r["tedarik"]
    if t["listelenen"] == 0:
        return "Tedarikcide tek ilan cikmadi", "yok"
    if t["eslesen_oran"] < 0.70:
        return f"Ilanlarin yalnizca yuzde {ts(t['eslesen_oran'] * 100)} kadari gercekten bu urun", "eslesme"
    if t.get("marka_kelimeleri"):
        k = ", ".join(t["marka_kelimeleri"])
        return f"\"{k}\" ilanlarin yuzde 20'sinden azinda geciyor, urun degil marka adi", "marka"
    if t["medyan"] is not None and t["medyan"] >= ORTA:
        return f"Tedarik medyani {ts(t['medyan'], 2)} dolar, satis bandinin ustunde", "marj"
    return "Puani daha dusuk kaldi", "puan"


# ------------------------------------------------------------------ parcalar
kapak_mozaik = "".join(
    f'<div class="kr" style="background-image:url({img(u["gorsel"])})"></div>'
    for u in URUN[:24])

cubuklar = "".join(
    f'<div class="ay{" son" if m in SON3 else ""}">'
    f'<span class="dg num">{ts(m["h"])}</span>'
    f'<div class="cb" style="height:{max(2, round(m["h"] / ENB_H * 100))}%"></div>'
    f'<span class="ad">{AY[m["a"] - 1]}</span></div>'
    for m in AYLIK)


def satici_satiri(p):
    g = GUC.get(p["alan"])
    trf = g["organik_trafik"] if g else 0
    kw = g["organik_kelime"] if g else 0
    return (f'<tr><td class="al">{e(p["alan"])}</td>'
            f'<td class="n">{ts(p["medyan"], 2)} $</td>'
            f'<td class="n">{ts(p["min"], 2)} - {ts(p["max"], 2)} $</td>'
            f'<td class="bar"><span style="width:{max(2, round(trf / ENB_TRF * 100))}%"></span>'
            f'<b class="num">{ts(trf)}</b></td>'
            f'<td class="n">{ts(kw)}</td></tr>')


duvar = "".join(
    f'<figure class="u"><div class="f" style="background-image:url({img(u["gorsel"])})"></div>'
    f'<figcaption><b class="num">{ts(u["fiyat_usd"], 2)} $</b>'
    + (f'<span>{e(u["satildi"])} satildi</span>' if u.get("satildi") else "")
    + '</figcaption></figure>'
    for u in URUN)


def elenen_satiri(r):
    g, sinif = gerekce(r)
    t = r["tedarik"]
    return (f'<tr class="{sinif}"><td class="kw">{e(r["kelime"])}</td>'
            f'<td class="n">x{ts(r["buyume"], 2)}</td>'
            f'<td class="n">{ts(r["hacim"])}</td>'
            f'<td class="n">{ts(t["listelenen"])}</td>'
            f'<td class="n">{ts(t["medyan"], 2) + " $" if t["medyan"] else "-"}</td>'
            f'<td class="g">{g}</td></tr>')


videolar = "".join(
    f'<a class="v" href="{e(v["link"])}" target="_blank" rel="noopener">'
    f'<div class="vk" style="background-image:url({img(v.get("kapak"))})">'
    f'<span class="sure">{e(v["sure"])}</span></div>'
    f'<div class="vb">{e(v["baslik"])}</div>'
    f'<div class="vm">{e(v["kanal"])} &middot; {ts(v["goruntulenme"])} goruntulenme</div></a>'
    for v in VIDEO[:6])

# Bir cagrinin suresi kaydedilmemis olabilir (saniye alani yok ya da None).
# O cagri SAYILIR ama sureye eklenmez; kac tanesi oldugu kunyede yazar.
uc_ozet = {}
SURESIZ = 0
for c in CAGRI:
    d = uc_ozet.setdefault(c["uc"], {"n": 0, "s": 0.0})
    d["n"] += 1
    if c.get("saniye") is None:
        SURESIZ += 1
    else:
        d["s"] += c["saniye"]
kunye = "".join(
    f'<tr><td class="mono">{e(k)}</td><td class="n">{ts(v["n"])}</td>'
    f'<td class="n">{ts(v["s"], 1)} sn</td></tr>'
    for k, v in sorted(uc_ozet.items(), key=lambda i: -i[1]["n"]))
TOPLAM_SN = sum(c["saniye"] for c in CAGRI if c.get("saniye") is not None)
SURESIZ_NOT = (f" ({ts(SURESIZ)} cagrinin suresi kaydedilmedi)" if SURESIZ else "")

ikinci_not = ""
if IKINCI:
    i = IKINCI[0]
    ikinci_not = (f'<p class="ikinci">Ayni taramadan ikinci aday da gecti: '
                  f'<b>{e(i["kelime"])}</b>, tedarik medyani {ts(i["tedarik"]["medyan"], 2)} dolar, '
                  f'ilan eslesmesi yuzde {ts(i["tedarik"]["eslesen_oran"] * 100)}, '
                  f'aylik {ts(i["hacim"])} arama.</p>')

# Bos kalan bolum panoya bos basilmaz, hic basilmaz.
HUKUM = f"Talep son uc ayda {ts(K['buyume'], 2)} katina cikti. Tedarik {ts(TED, 2)} dolar"
HUKUM += (f", pazarin lideri {ts(PER[-1]['medyan'], 2)} dolara satiyor." if PER else ".")

# ------------------------------------------------------------------ bolumler
bolumler = []

if MERDIVEN:
    bolumler.append(f"""
<section><div class="sr">
  <p class="etk">Para nerede duruyor</p>
  <h2>{ts(MERDIVEN_ALT, 2)} dolara aliniyor, {ts(MERDIVEN_UST, 2)} dolara satiliyor</h2>
  <p class="alt">Her cubuk gercek bir fiyat. Yesil olanlar tedarikci tarafi, beyaz olanlar bugun bu
    urunu satan magazalarin medyan fiyati. Turuncu alan senin girdigin satis bandin.</p>
  <div class="merdiven">
    <div class="bantkat">
      <div class="band" style="left:{x(ALT)}%;width:{x(UST) - x(ALT)}%"></div>
      <div class="bandet" style="left:{BANT_ORTA}%">SENIN BANDIN {ts(ALT)}-{ts(UST)} $</div>
    </div>
    {merdiven_html}
  </div>
  <p class="notlar">
    <span>Taramada donen benzersiz ilan <b class="num">{ts(len(URUN))}</b></span>
    <span>Ilan basligi eslesmesi <b class="num">yuzde {ts(K["tedarik"]["eslesen_oran"] * 100)}</b></span>
    <span>Bandin icinde kalan ilan <b class="num">{ts(K["tedarik"]["bantta"])}</b></span>
  </p>
</div></section>""")

if AYLIK:
    bolumler.append(f"""
<section><div class="sr">
  <p class="etk">Talep ne yapiyor</p>
  <h2>{ts(len(AYLIK))} ayin arama egrisi</h2>
  <p class="alt">Her cubuk o ayin arama adedi. Turuncu olanlar son uc ay. Egri mevsimlik, yani stok
    ve reklam takvimi buna gore kurulur.</p>
  <div class="egri">{cubuklar}</div>
</div></section>""")

if TIK:
    bolumler.append(f"""
<section><div class="sr">
  <p class="etk">Reklam matematigi</p>
  <h2>Basabas noktasi {ts(TIK)} tiklama</h2>
  <p class="alt">Uc olculen sayidan cikiyor: tiklama basi maliyet, tedarik medyani ve senin satis
    bandin. Donusum orani hicbir yerde varsayilmadi, bu yuzden burada tahmin yok.</p>
  <div class="kut">
    <div><b class="num">{ts(CPC, 2)} $</b><span>Tiklama basi maliyet</span></div>
    <div><b class="num">{ts(TIK)}</b><span>Bir satisi basabasa getiren tiklama sayisi</span></div>
    <div><b class="num">{ts(BUTCE_TIK)}</b><span>Aylik {ts(G["aylik_reklam_butcesi"])} dolarin aldigi tiklama</span></div>
    <div><b class="num">{ts(BUTCE_SATIS)}</b><span>O butcenin basabas satis adedi</span></div>
  </div>
</div></section>""")

if PER:
    bolumler.append(f"""
<section><div class="sr">
  <p class="etk">Kim satiyor</p>
  <h2>Rafta kim var, ne kadar guclu</h2>
  <p class="alt">Fiyatlar magazalarin kendi koleksiyon sayfalarindan. Organik trafik ve kelime sayisi
    SEMrush ABD veritabanindan.</p>
  <div class="sar"><table>
    <thead><tr><th>Magaza</th><th>Medyan</th><th>Aralik</th><th>Aylik organik trafik</th><th>Kelime</th></tr></thead>
    <tbody>{"".join(satici_satiri(p) for p in PER)}</tbody>
  </table></div>
</div></section>""")

if URUN:
    bolumler.append(f"""
<section style="padding-bottom:0"><div class="sr">
  <p class="etk">Tedarik tarafi</p>
  <h2>Bugun tedarikcide duran {ts(len(URUN))} ilan</h2>
  <p class="alt">Hepsi ayni aramadan geldi. Fiyat ilanin kendi fiyati, satis adedi ilanin kendi
    sayaci. Kargo ve vergi haric.</p>
</div>
<div class="duvar">{duvar}</div></section>""")

if D["elenenler"]:
    bolumler.append(f"""
<section><div class="sr">
  <p class="etk">Elenenler</p>
  <h2>Ayni taramayi gecip tedarikte kalan {ts(len(D["elenenler"]))} aday</h2>
  <p class="alt">Her biri talep kapisini gecti. Gerekce tahmin degil, tedarikci taramasinin
    olcumu.</p>
  {ikinci_not}
  <div class="sar"><table>
    <thead><tr><th>Aday</th><th>Buyume</th><th>Aylik arama</th><th>Ilan</th><th>Tedarik medyani</th><th>Neden elendi</th></tr></thead>
    <tbody>{"".join(elenen_satiri(r) for r in D["elenenler"])}</tbody>
  </table></div>
</div></section>""")

if VIDEO:
    bolumler.append(f"""
<section><div class="sr">
  <p class="etk">Icerik kaniti</p>
  <h2>Bu urunu bugun anlatan videolar</h2>
  <p class="alt">Reklam yaratici fikri icin hazir kaynak. Goruntulenme talebin ikinci kanitidir.</p>
  <div class="vid">{videolar}</div>
</div></section>""")

# ------------------------------------------------------------------ sayfa
HTML = f"""<title>{K["kelime"].title()} Avi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root{{
  --zemin:#0C1420; --panel:#141E2E; --panel2:#1B2739; --cizgi:#28374E;
  --metin:#EDF2F8; --soluk:#8496AE;
  --turuncu:#FF6B35; --yesil:#4FC3A1; --kirmizi:#E5484D;
  --dis:'Bricolage Grotesque',Georgia,serif;
  --gov:'Instrument Sans',system-ui,-apple-system,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,monospace;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--zemin);color:var(--metin);font-family:var(--gov);
  font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}}
.num{{font-variant-numeric:tabular-nums}}
.sr{{max-width:1220px;margin:0 auto;padding:0 28px}}
section{{padding:60px 0;border-top:1px solid var(--cizgi)}}
h2{{font-family:var(--dis);font-weight:600;font-size:clamp(1.55rem,3.1vw,2.15rem);
  margin:0 0 8px;letter-spacing:-.022em;text-wrap:balance}}
.etk{{font-family:var(--mono);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--turuncu);margin:0 0 12px}}
.alt{{color:var(--soluk);font-size:.95rem;margin:0 0 30px;max-width:64ch}}

/* ---- kapak */
header{{position:relative;overflow:hidden}}
.kapakgorsel{{position:relative}}
.mozaik{{display:grid;grid-template-columns:repeat(8,1fr);height:clamp(320px,42vh,440px)}}
.kr{{background-size:cover;background-position:center;filter:saturate(.85) brightness(.62)}}
.perde{{position:absolute;inset:0;background:linear-gradient(180deg,
  rgba(12,20,32,.22) 0%,rgba(12,20,32,.55) 34%,rgba(12,20,32,.88) 68%,var(--zemin) 96%)}}
.kapakic{{position:relative;padding:0 0 44px;margin-top:-176px}}
.rozet{{display:inline-block;font-family:var(--mono);font-size:.72rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--metin);background:rgba(255,107,53,.15);
  border:1px solid var(--turuncu);padding:6px 12px}}
h1{{font-family:var(--dis);font-weight:800;font-size:clamp(2.5rem,7.6vw,5.2rem);line-height:.94;
  letter-spacing:-.036em;margin:18px 0 12px;text-wrap:balance}}
.hukum{{font-size:clamp(1.02rem,2vw,1.32rem);max-width:38ch;margin:0;color:var(--metin)}}
.serit{{display:grid;grid-template-columns:repeat(auto-fit,minmax(196px,1fr));gap:1px;
  background:var(--cizgi);border:1px solid var(--cizgi);margin-top:36px}}
.serit>div{{background:var(--panel);padding:20px 22px}}
.serit b{{display:block;font-family:var(--dis);font-weight:800;
  font-size:clamp(1.85rem,4.2vw,2.7rem);line-height:1;letter-spacing:-.03em}}
.serit span{{display:block;color:var(--soluk);font-size:.83rem;margin-top:9px}}
.serit .ys b{{color:var(--yesil)}} .serit .tr b{{color:var(--turuncu)}}

/* ---- fiyat merdiveni */
.merdiven{{position:relative;display:flex;flex-direction:column;gap:15px;margin:14px 0 22px;
  padding-bottom:26px}}
.bantkat{{position:absolute;top:-12px;bottom:22px;left:206px;right:108px;pointer-events:none}}
.band{{position:absolute;top:0;bottom:0;background:rgba(255,107,53,.10);
  border-left:1px solid var(--turuncu);border-right:1px solid var(--turuncu)}}
.bandet{{position:absolute;bottom:-22px;font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;
  color:var(--turuncu);white-space:nowrap;transform:translateX(-50%)}}
.mr{{display:grid;grid-template-columns:190px 1fr 92px;align-items:center;gap:16px;
  position:relative;z-index:1}}
.mr .ad{{color:var(--soluk);font-size:.88rem;text-align:right}}
.mr .cizgi{{display:block;height:16px;background:rgba(40,55,78,.32)}}
.mr .cizgi i{{display:block;height:100%;background:#41597C}}
.mr.ted .cizgi i{{background:var(--yesil)}}
.mr .dg{{font-family:var(--mono);font-size:.9rem}}
.mr.ted .dg{{color:var(--yesil)}}
.notlar{{display:flex;flex-wrap:wrap;gap:10px 30px;font-size:.92rem;color:var(--soluk);margin:34px 0 0}}
.notlar b{{color:var(--metin);font-family:var(--mono)}}

/* ---- talep egrisi */
.egri{{display:flex;align-items:flex-end;gap:8px;height:250px;margin-top:8px}}
.ay{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%}}
.ay .cb{{width:100%;background:var(--panel2);border-top:2px solid var(--cizgi)}}
.ay.son .cb{{background:rgba(255,107,53,.26);border-top:2px solid var(--turuncu)}}
.ay .ad{{font-family:var(--mono);font-size:.7rem;color:var(--soluk);margin-top:9px}}
.ay .dg{{font-family:var(--mono);font-size:.68rem;color:var(--soluk);margin-bottom:7px}}
.ay.son .ad,.ay.son .dg{{color:var(--turuncu)}}

/* ---- kutular */
.kut{{display:grid;grid-template-columns:repeat(auto-fit,minmax(224px,1fr));gap:1px;
  background:var(--cizgi);border:1px solid var(--cizgi)}}
.kut>div{{background:var(--panel);padding:22px}}
.kut b{{display:block;font-family:var(--dis);font-weight:800;font-size:2rem;line-height:1;
  letter-spacing:-.03em}}
.kut span{{display:block;color:var(--soluk);font-size:.85rem;margin-top:10px}}

/* ---- tablolar */
.sar{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:.93rem;min-width:640px}}
th{{text-align:left;font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--soluk);font-weight:400;padding:0 14px 10px;
  border-bottom:1px solid var(--cizgi);white-space:nowrap}}
td{{padding:13px 14px;border-bottom:1px solid var(--cizgi);vertical-align:middle}}
td.n{{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}}
td.al,td.kw{{font-weight:600}}
td.g{{color:var(--soluk);font-size:.87rem}}
tr.marj td.kw{{color:var(--turuncu)}}
tr.eslesme td.kw,tr.yok td.kw,tr.marka td.kw{{color:var(--soluk);text-decoration:line-through}}
td.bar{{min-width:190px}}
td.bar span{{display:inline-block;height:12px;background:var(--panel2);
  border-right:2px solid var(--turuncu);vertical-align:middle}}
td.bar b{{font-family:var(--mono);font-size:.82rem;color:var(--soluk);margin-left:10px}}
.ikinci{{margin:0 0 26px;padding:14px 18px;background:var(--panel);
  border-left:2px solid var(--yesil);font-size:.92rem;color:var(--soluk)}}
.ikinci b{{color:var(--metin)}}

/* ---- urun duvari */
.duvar{{display:grid;grid-template-columns:repeat(auto-fill,minmax(142px,1fr));gap:1px;
  background:var(--cizgi);border-top:1px solid var(--cizgi);border-bottom:1px solid var(--cizgi)}}
.u{{margin:0;background:var(--panel);position:relative}}
.u .f{{aspect-ratio:1;background-size:cover;background-position:center}}
.u figcaption{{position:absolute;left:0;right:0;bottom:0;padding:8px 10px;display:flex;
  justify-content:space-between;align-items:flex-end;gap:6px;font-family:var(--mono);
  background:linear-gradient(0deg,rgba(12,20,32,.95),rgba(12,20,32,0))}}
.u figcaption b{{font-size:.82rem;font-weight:600}}
.u figcaption span{{font-size:.66rem;color:var(--soluk)}}

/* ---- video */
.vid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:24px}}
.v{{text-decoration:none;color:inherit}}
.vk{{aspect-ratio:16/9;background-size:cover;background-position:center;position:relative;
  border:1px solid var(--cizgi)}}
.vk .sure{{position:absolute;right:7px;bottom:7px;background:rgba(12,20,32,.92);
  font-family:var(--mono);font-size:.7rem;padding:2px 6px}}
.vb{{font-weight:600;font-size:.92rem;margin-top:12px;line-height:1.35}}
.vm{{color:var(--soluk);font-size:.78rem;margin-top:5px;font-family:var(--mono)}}
.v:hover .vb{{color:var(--turuncu)}}

footer{{padding:52px 0 76px;border-top:1px solid var(--cizgi);color:var(--soluk);font-size:.85rem}}
footer p{{max-width:74ch}}
.mono{{font-family:var(--mono);font-size:.84rem}}
@media (max-width:760px){{
  .mozaik{{grid-template-columns:repeat(4,1fr);height:280px}}
  .kapakic{{margin-top:-140px}}
  .egri{{height:172px}} .ay .dg{{display:none}}
  .mr{{grid-template-columns:112px 1fr 74px;gap:10px}}
  .mr .ad{{font-size:.76rem}}
  .bantkat{{left:122px;right:84px}}
}}
</style>

<header>
  <div class="kapakgorsel"><div class="mozaik">{kapak_mozaik}</div><div class="perde"></div></div>
  <div class="sr kapakic">
    <span class="rozet">{e(G["nis"])} &nbsp;&middot;&nbsp; {e(G["pazar"]["ad"])} &nbsp;&middot;&nbsp; {ts(ALT)}-{ts(UST)} $ bandi &nbsp;&middot;&nbsp; {e(G["tedarik"])}</span>
    <h1>{e(K["kelime"])}</h1>
    <p class="hukum">{HUKUM}</p>
    <div class="serit">
      <div class="ys"><b class="num">x{ts(K["buyume"], 2)}</b><span>Son uc ayin ortalamasi, onceki dokuz aya gore</span></div>
      <div><b class="num">{ts(K["hacim"])}</b><span>Aylik arama, {e(G["pazar"]["ad"])}</span></div>
      <div class="tr"><b class="num">{ts(MARJ, 2)} $</b><span>Bandin ortasinda birim basina kalan</span></div>
      <div><b class="num">{ts(K["zorluk"])}</b><span>Arama zorlugu, yuzluk olcek</span></div>
    </div>
  </div>
</header>
{"".join(bolumler)}

<footer><div class="sr">
  <p class="etk" style="color:var(--soluk)">Kunye</p>
  <div class="sar"><table style="min-width:420px">
    <thead><tr><th>Uc</th><th>Cagri</th><th>Sure</th></tr></thead>
    <tbody>{kunye}</tbody>
  </table></div>
  <p style="margin-top:24px">Bu kosuda {ts(len(CAGRI))} cagri yapildi, olculen ag suresi
    {ts(TOPLAM_SN, 1)} saniye{SURESIZ_NOT}. Kosunun bakiyeden dustugu tutar
    {ts(BAKIYE_FARK, 5)} dolar; olcum yontemi kosu oncesi ve sonrasi bakiye farki.</p>
  <p>Pazar {e(G["pazar"]["ad"])}, dil kodu {e(G["pazar"]["language_code"])}, tedarik kaynagi
    {e(G["tedarik"])}, aylik reklam butcesi {ts(G["aylik_reklam_butcesi"])} dolar,
    mevcut magaza {e(G["magaza"])}. Pano uretim tarihi {datetime.date.today().strftime("%d.%m.%Y")}.</p>
  <p>Sinirlar: organik trafik yalnizca ABD veritabanindan gelir. Tedarik fiyatlari kargo ve vergi
    haric ilan fiyatidir. Donusum orani, iade orani ve reklam yaratici performansi hicbir yerde
    varsayilmadi; bu yuzden kar tahmini degil basabas esigi verildi.</p>
</div></footer>
"""

open(cikti_yol, "w", encoding="utf-8").write(HTML)
print(f"yazildi: {cikti_yol}  {len(HTML.encode()) / 1024:.0f} KB")
print(f"bolum {len(bolumler)} | duvar {len(URUN)} gorsel | kapak {len(URUN[:24])} | video {len(VIDEO[:6])}")
print(f"marj {MARJ} | basabas {ts(TIK) if TIK else '-'} tik | bakiye farki {BAKIYE_FARK} usd | cagri {len(CAGRI)}")
