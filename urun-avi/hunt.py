# -*- coding: utf-8 -*-
"""hunt.py - AIsa uzerinden dropshipping urun avi (STEP 0 - STEP 9).

Kullanim:
    AISA_API_KEY=... python3 hunt.py [config.json]

- Girdi config.json'dan okunur (SECTION 1).
- Her ham yanit raw/ altina yazilir. Dosya varsa cagri TEKRAR YAPILMAZ;
  siralamayi degistirmek icin scripti yeniden calistirmak bedavadir.
- Her ucretli adimdan once bakiye okunur; adim harcama tavanini asacaksa
  script durur ve kullaniciya sorulmasini ister.
- Sonunda measurement.json yazilir ve PANO.py ile board.html uretilir.
Yalnizca standart kutuphane kullanir.
"""
import json
import math
import os
import re
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.environ.get("AISA_ROOT", "https://api.aisa.one").rstrip("/")
DATA = ROOT + "/apis/v1"
ACCOUNT = ROOT + "/v1"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
CALLS = os.path.join(RAW, "_calls.json")

STOP = {"for", "the", "and", "a", "an", "of", "with", "to", "in", "my", "best", "near", "me"}
# Olculen fiyatlar (prompt). Bilinmeyen uclar icin temkinli tahmin; ilk cagridan
# sonra header'daki gercek fiyat kullanilir.
KW_IDEAS_COST = {500: 0.144, 600: 0.168, 700: 0.192, 1000: 0.264}
EST = {"firecrawl/scrape": 0.005, "semrush/domain-overview": 0.003,
       "tavily/search": 0.01, "youtube/search": 0.01}


def die(msg):
    sys.exit(msg)


# ------------------------------------------------------------------ HTTP + kayit
KEY = os.environ.get("AISA_API_KEY", "").strip()
os.makedirs(RAW, exist_ok=True)
calls = json.load(open(CALLS)) if os.path.exists(CALLS) else []


def save_calls():
    json.dump(calls, open(CALLS, "w"), indent=1)


def http(method, url, body=None):
    if not KEY:
        die("HATA: AISA_API_KEY ortam degiskeni yok. AIsa baglantisi bu ortamda tanimli degil.")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
        "Accept": "application/json, text/csv, */*"})
    t = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=180)
        code, hdr, text = r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as ex:
        code, hdr, text = ex.code, dict(ex.headers), ex.read().decode("utf-8", "replace")
    sec = round(time.time() - t, 2)
    cost = 0
    for k, v in hdr.items():
        if k.lower() == "x-aisa-customer-cost-micros-usd":
            try:
                cost = int(float(v))
            except ValueError:
                pass
    return code, cost, sec, text


def call(tag, uc, method, url, body=None, asama="d"):
    """Once diskteki ham yaniti dener. Yoksa cagirir, kaydeder, maliyetini yazar."""
    path = os.path.join(RAW, tag + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    code, cost, sec, text = http(method, url, body)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = text
    rec = {"uc": uc, "http": code, "maliyet_micros": cost, "saniye": sec, "asama": asama, "tag": tag}
    calls.append(rec)
    save_calls()
    out = {"http": code, "cost": cost, "body": payload}
    if 200 <= code < 300:           # basarisiz yanit diske yazilmaz; tekrar denemek bedava
        json.dump(out, open(path, "w"), ensure_ascii=False)
    else:
        print(f"  ! {uc} HTTP {code}: {str(text)[:200]}")
    return out


def balance(tag=None):
    code, cost, sec, text = http("GET", ACCOUNT + "/credits/balance")
    if code != 200:
        die(f"HATA: bakiye okunamadi, HTTP {code}: {text[:300]}")
    b = json.loads(text)
    g = int(b.get("available_balance_micros_usd") or 0)
    t = int((b.get("gtm") or {}).get("balance_micros_usd") or 0)
    calls.append({"uc": "credits/balance", "http": code, "maliyet_micros": cost,
                  "saniye": sec, "asama": "d", "tag": tag or "balance"})
    save_calls()
    return g, t


# ------------------------------------------------------------------ girdi
CFG = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "config.json"),
                    encoding="utf-8"))
ALT, UST = CFG["satis_bandi"]
ORTA = (ALT + UST) / 2
CEIL = int(CFG["harcama_tavani_usd"] * 1e6)
LOC, LANG = CFG["pazar"]["location_code"], CFG["pazar"]["language_code"]
US = LOC == 2840


def words(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP]


def stem(w):
    """Tekil/cogul farkini kapatir: mattresses->mattress, beds->bed, covers->cover."""
    for suf, rep in (("sses", "ss"), ("ies", "y"), ("es", "e"), ("s", "")):
        if w.endswith(suf) and len(w) > len(suf) + 2 and not w.endswith("ss"):
            return w[: -len(suf)] + rep
    return w


def stems(s):
    return {stem(w) for w in words(s)}


# ------------------------------------------------------------------ STEP 0
B0 = os.path.join(RAW, "balance_0.json")
if os.path.exists(B0):
    g0, t0 = json.load(open(B0))
else:
    g0, t0 = balance("balance_0")
    json.dump([g0, t0], open(B0, "w"))
print(f"STEP 0  bakiye genel {g0/1e6:.4f}  gtm {t0/1e6:.4f}  tavan {CEIL/1e6:.2f} USD")


def guard(step, est_usd, tags=()):
    """Adim tavani asacaksa dur ve sor. Adimin tum yanitlari diskteyse cagri yok, kontrol de yok."""
    if tags and all(os.path.exists(os.path.join(RAW, t + ".json")) for t in tags):
        return None
    g, t = balance(f"guard_{step}")
    spent = (g0 - g) + (t0 - t)
    if spent + est_usd * 1e6 > CEIL:
        die(f"DUR ({step}): simdiye kadar {spent/1e6:.4f} USD harcandi, bu adim ~{est_usd:.4f} USD "
            f"daha ekler, tavan {CEIL/1e6:.2f} USD. Devam icin kullaniciya sor, "
            f"onay gelirse config.json'da harcama_tavani_usd'yi yukselt ve tekrar calistir.")
    return spent


def est(uc):
    seen = [c["maliyet_micros"] for c in calls if c["uc"] == uc and c["maliyet_micros"]]
    return (max(seen) / 1e6) if seen else EST[uc]


# ------------------------------------------------------------------ STEP 1
limit = CFG.get("keyword_ideas_limit", 500)
guard("keyword_ideas", KW_IDEAS_COST.get(limit, 0.264), ["keyword_ideas"])
r = call("keyword_ideas", "dataforseo/keyword_ideas", "POST",
         DATA + "/dataforseo/dataforseo_labs/google/keyword_ideas/live",
         [{"keywords": CFG["tohum"], "location_code": LOC, "language_code": LANG, "limit": limit,
           "filters": [["keyword_info.search_volume", ">", 1500], "and",
                       ["keyword_properties.keyword_difficulty", "<", 40]],
           "order_by": ["keyword_info.search_volume,desc"]}], asama="c")
if r["http"] != 200:
    die("HATA: keyword_ideas basarisiz.")
task = (r["body"].get("tasks") or [{}])[0]
if task.get("status_code") != 20000:
    die(f"HATA: DataForSEO status {task.get('status_code')} {task.get('status_message')}")
items = ((task.get("result") or [{}])[0] or {}).get("items") or []
print(f"STEP 1  keyword_ideas {len(items)} satir")

# ------------------------------------------------------------------ STEP 2
seed_sets = [stems(s) for s in CFG["tohum"]]
need = math.ceil(len(seed_sets) / 2)
ANCHOR = {w for w in set().union(*seed_sets) if sum(w in s for s in seed_sets) >= need}
if not ANCHOR:
    die("DUR: tohum kelimeler ortak bir nis tarif etmiyor (nis capasi bulunamadi). Tohumlari duzelt.")
print(f"STEP 2  nis capasi {sorted(ANCHOR)}")


def monthly(it):
    ms = [m for m in (it.get("keyword_info") or {}).get("monthly_searches") or []
          if m.get("search_volume") is not None]
    ms.sort(key=lambda m: (m["year"], m["month"]), reverse=True)
    return ms[:12]


def growth(ms):
    if len(ms) < 12:
        return None
    last3 = statistics.mean(m["search_volume"] for m in ms[:3])
    prev9 = statistics.mean(m["search_volume"] for m in ms[3:12])
    return last3 / prev9 if prev9 else None


cnt = {"intent": 0, "anchor": 0, "advertiser": 0, "growth": 0}
survivors = []
for it in items:
    kw = it.get("keyword") or ""
    ki = it.get("keyword_info") or {}
    if ((it.get("search_intent_info") or {}).get("main_intent")) not in ("commercial", "transactional"):
        cnt["intent"] += 1; continue
    if not (stems(kw) & ANCHOR):
        cnt["anchor"] += 1; continue
    if (ki.get("competition") or 0) < 0.50:
        cnt["advertiser"] += 1; continue
    ms = monthly(it)
    gr = growth(ms)
    if gr is None or gr < 1.15:
        cnt["growth"] += 1; continue
    vol = ki.get("search_volume") or 0
    survivors.append({
        "kelime": kw, "hacim": vol, "cpc": ki.get("cpc"),
        "zorluk": (it.get("keyword_properties") or {}).get("keyword_difficulty"),
        "rekabet": ki.get("competition"), "buyume": round(gr, 4),
        "skor": gr * math.sqrt(vol),
        "aylik": [{"a": m["month"], "y": m["year"], "h": m["search_volume"]} for m in ms]})
survivors.sort(key=lambda s: -s["skor"])
top = survivors[:10]
print(f"        elenen: niyet {cnt['intent']}, capa {cnt['anchor']}, reklamci {cnt['advertiser']}, "
      f"buyume {cnt['growth']} | kalan {len(survivors)} | tedarike giren {len(top)}")
for s in top:
    print(f"          {s['skor']:8.1f}  x{s['buyume']:.2f}  {s['hacim']:>7}  {s['kelime']}")
if not top:
    die("DUR: hicbir aday talep kapilarini gecemedi. Tohumlar cok dar ya da nis buyumuyor degil; "
        "farkli urunlerden 3-5 tohum dene.")

# ------------------------------------------------------------------ STEP 3
CARD = re.compile(r"\*\*(?P<title>[^*]{12,200})\*\*(?:\s|\\)*\$(?P<price>[\d.,]+)")
IMG = re.compile(r"!\[[^\]]*\]\((https://ae-pic[^)\s]+_480x480[^)\s]*)\)")
SOLD = re.compile(r"([\d.,]+\+?)\s*sold", re.I)


def num(s):
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def listings(md):
    out, seen = [], set()
    for m in CARD.finditer(md):
        title, price = m.group("title").strip(), num(m.group("price"))
        if price is None or (title, price) in seen:
            continue
        seen.add((title, price))
        imgs = IMG.findall(md[max(0, m.start() - 4500): m.start()])
        sold = SOLD.search(md[m.end(): m.end() + 1200])
        out.append({"baslik": title, "fiyat_usd": price, "gorsel": imgs[-1] if imgs else None,
                     "satildi": sold.group(1) if sold else None})
    return out


def scrape(tag, url):
    r = call(tag, "firecrawl/scrape", "POST", DATA + "/firecrawl/scrape",
             {"url": url, "formats": ["markdown"], "proxy": "basic"})
    md = ((r.get("body") or {}).get("data") or {}).get("markdown") or "" if isinstance(r.get("body"), dict) else ""
    return md


def slug(kw):
    return "-".join(re.findall(r"[a-z0-9]+", kw.lower()))


guard("supplier", len(top) * est("firecrawl/scrape"), ["ali_" + slug(s["kelime"]) for s in top])
passed, failed = [], []
for s in top:
    md = scrape("ali_" + slug(s["kelime"]),
                f"https://www.aliexpress.com/w/wholesale-{slug(s['kelime'])}.html")
    L = listings(md)
    s["_listings"] = L
    cw = sorted(stems(s["kelime"]))
    need_w = min(len(cw), max(2, len(cw) - 1))
    tset = [stems(l["baslik"]) for l in L]
    matched = [l for l, ts_ in zip(L, tset) if sum(w in ts_ for w in cw) >= need_w]
    share = {w: (sum(w in ts_ for ts_ in tset) / len(L) if L else 0) for w in cw}
    prices = [l["fiyat_usd"] for l in matched]
    med = round(statistics.median(prices), 2) if prices else None
    s["tedarik"] = {
        "listelenen": len(L), "eslesen_oran": round(len(matched) / len(L), 4) if L else 0,
        "bantta": sum(ALT <= p <= UST for p in prices), "medyan": med,
        "min": min(prices) if prices else None,
        "kelime_payi": {w: round(v, 3) for w, v in share.items()},
        "marka_kelimeleri": [w for w, v in share.items() if v < 0.20],
        "markdown_uzunluk": len(md)}
    t = s["tedarik"]
    if not L or t["eslesen_oran"] < 0.70 or t["marka_kelimeleri"] or med is None or med > ORTA:
        failed.append(s)
    else:
        s["marj_usd"] = round(ORTA - med, 2)
        s["kazanan_skor"] = s["skor"] * (s["marj_usd"] / ORTA)
        passed.append(s)
    print(f"STEP 3  {s['kelime']:<40} ilan {t['listelenen']:>3}  eslesme {t['eslesen_oran']:.2f}  "
          f"medyan {med}  marka {t['marka_kelimeleri'] or '-'}  md {len(md)}")

passed.sort(key=lambda s: -s["kazanan_skor"])
if not passed:
    json.dump({"elenenler": failed}, open(os.path.join(HERE, "elenenler_only.json"), "w"),
              ensure_ascii=False, indent=1, default=str)
    die("DUR: ilk on adayin hicbiri tedarik kapilarini (eslesme, marka, marj) gecemedi. "
        "Olcumler elenenler_only.json'da. Tohumlari ya da satis bandini gozden gecir.")
W = passed[0]
print(f"        KAZANAN {W['kelime']}  marj {W['marj_usd']}  "
      + (f"| ikinci {passed[1]['kelime']}" if len(passed) > 1 else ""))

# Kazanan icin duvari genisletmek uzere 2. sayfa (bir cagri daha).
guard("supplier_p2", est("firecrawl/scrape"), ["ali_" + slug(W["kelime"]) + "_p2"])
md2 = scrape("ali_" + slug(W["kelime"]) + "_p2",
             f"https://www.aliexpress.com/w/wholesale-{slug(W['kelime'])}.html?page=2")
seen = {(l["baslik"], l["fiyat_usd"]) for l in W["_listings"]}
W["_listings"] += [l for l in listings(md2) if (l["baslik"], l["fiyat_usd"]) not in seen]

# ------------------------------------------------------------------ renk (olculen)
def colorfulness(url):
    """Hasler-Susstrunk renklilik olcusu. Pillow yoksa olculemez -> None."""
    try:
        from PIL import Image
        import io
        u = re.sub(r"_\d+x\d+(q\d+)?", "_120x120q75", url, count=1)
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=20).read())).convert("RGB")
        im.thumbnail((80, 80))
        rg, yb = [], []
        for r_, g_, b_ in im.getdata():
            rg.append(r_ - g_); yb.append(0.5 * (r_ + g_) - b_)
        return round(math.hypot(statistics.pstdev(rg), statistics.pstdev(yb))
                     + 0.3 * math.hypot(statistics.mean(rg), statistics.mean(yb)), 2)
    except Exception:
        return None


urunler = []
for l in W["_listings"]:
    if not l["gorsel"]:
        continue
    c = colorfulness(l["gorsel"])
    urunler.append({**l, "renk": c if c is not None else 0})
if urunler and all(u["renk"] == 0 for u in urunler):
    print("        uyari: renk olculemedi (Pillow yok ya da gorsel indirilemedi); siralama yok")

# ------------------------------------------------------------------ STEP 4
guard("tavily", est("tavily/search"), ["tavily_" + slug(W["kelime"])])
r = call("tavily_" + slug(W["kelime"]), "tavily/search", "POST", DATA + "/tavily/search",
         {"query": f"{W['kelime']} buy online price shop", "max_results": 10})
res = (r.get("body") or {}).get("results") or [] if isinstance(r.get("body"), dict) else []
doms, pages = [], []
for x in res:
    u = x.get("url") or ""
    d = urllib.parse.urlparse(u).netloc.lower().removeprefix("www.")
    if not d or any(b in d for b in ("reddit.", "youtube.", "youtu.be")) or d in doms:
        continue
    doms.append(d); pages.append(u)
doms, pages = doms[:3], pages[:3]
PRICE = re.compile(r"\$\s?(\d{1,3}(?:,\d{3})?(?:\.\d{2})?)")
perakende = []
guard("retail", len(pages) * est("firecrawl/scrape"), ["retail_" + slug(d) for d in doms])
for d, u in zip(doms, pages):
    md = scrape("retail_" + slug(d), u)
    ps = []
    for frag in PRICE.findall(md):
        v = num(frag)
        if v is not None and 5 <= v <= 400:
            ps.append(v)
    print(f"STEP 4  {d:<32} fiyat {len(ps)}  md {len(md)}")
    if ps:
        perakende.append({"alan": d, "url": u, "medyan": round(statistics.median(ps), 2),
                          "min": min(ps), "max": max(ps), "adet": len(ps)})

# ------------------------------------------------------------------ STEP 5
rakip = []
if US and perakende:
    guard("semrush", len(perakende) * est("semrush/domain-overview"),
          ["semrush_" + slug(p["alan"]) for p in perakende])
    for p in perakende:
        r = call("semrush_" + slug(p["alan"]), "semrush/domain-overview", "GET",
                 DATA + "/semrush/domain-overview?" + urllib.parse.urlencode({"domain": p["alan"]}))
        body = r.get("body")
        text = body if isinstance(body, str) else (body.get("data") if isinstance(body, dict) else "") or ""
        if not isinstance(text, str) or "ERROR" in text or ";" not in text:
            print(f"STEP 5  {p['alan']}: veri yok ({str(text)[:80]})"); continue
        rows = [ln.split(";") for ln in text.strip().splitlines()]
        h, v = rows[0], rows[1] if len(rows) > 1 else []
        rec = dict(zip(h, v))
        try:
            rakip.append({"alan": p["alan"], "organik_trafik": int(rec["Organic Traffic"]),
                          "organik_kelime": int(rec["Organic Keywords"])})
            print(f"STEP 5  {p['alan']:<32} trafik {rec['Organic Traffic']}  kelime {rec['Organic Keywords']}")
        except (KeyError, ValueError):
            print(f"STEP 5  {p['alan']}: beklenmeyen bicim")

# ------------------------------------------------------------------ STEP 6
guard("youtube", est("youtube/search"), ["youtube_" + slug(W["kelime"])])
r = call("youtube_" + slug(W["kelime"]), "youtube/search", "GET",
         DATA + "/youtube/search?" + urllib.parse.urlencode({"q": W["kelime"]}))
vids = (r.get("body") or {}).get("videos") or [] if isinstance(r.get("body"), dict) else []
videolar = [{"baslik": v.get("title"), "kanal": (v.get("channel") or {}).get("title"),
             "goruntulenme": v.get("views") or 0, "link": v.get("link"),
             "kapak": (v.get("thumbnail") or {}).get("static"), "sure": v.get("length"),
             "yayin": v.get("published_time")} for v in vids[:8]]
print(f"STEP 6  video {len(videolar)}")

# ------------------------------------------------------------------ STEP 7
calls[:] = [c for c in calls if c.get("tag") != "balance_1"]   # yeniden kosuda tekrar sayilmasin
g1, t1 = balance("balance_1")
diff = (g0 - g1) + (t0 - t1)
hdr = sum(c["maliyet_micros"] for c in calls)
print(f"STEP 7  bakiye farki {diff/1e6:.4f} USD | header toplami {hdr/1e6:.4f} USD")
if diff != hdr:
    print("        UYARI: header toplami bakiye farkina esit degil; kaydedilmemis bir cagri var "
          "(ya da raw/ onceki bir kosudan geldi). Panoya bakiye farki yazilir.")

# ------------------------------------------------------------------ STEP 8
def shape(s, with_margin):
    o = {k: s[k] for k in ("kelime", "hacim", "cpc", "zorluk", "buyume", "aylik", "tedarik")}
    if with_margin:
        o["marj_usd"] = s["marj_usd"]
    return o


def rec(c):
    return {k: c[k] for k in ("uc", "http", "maliyet_micros", "saniye")}


M = {
    "girdi": {k: CFG[k] for k in ("nis", "tohum", "pazar", "satis_bandi",
                                  "aylik_reklam_butcesi", "tedarik", "magaza")},
    "kazanan": shape(W, True),
    "tedarik_urunleri": urunler,
    "perakende": perakende,
    "rakip_guc": rakip,
    "videolar": videolar,
    "elenenler": [shape(s, False) for s in failed],
    "gecen": [shape(s, True) for s in passed],
    "cagrilar_asama_c": [rec(c) for c in calls if c["asama"] == "c"],
    "cagrilar_asama_d": [rec(c) for c in calls if c["asama"] == "d"],
    "bakiye_d": {"g0": g0, "g1": g1, "t0": t0, "t1": t1},
    "nis_capasi": sorted(ANCHOR),
    "adim2_elenen": cnt,
}
json.dump(M, open(os.path.join(HERE, "measurement.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("STEP 8  measurement.json yazildi")

# ------------------------------------------------------------------ STEP 9
subprocess.run([sys.executable, os.path.join(HERE, "PANO.py"),
                os.path.join(HERE, "measurement.json"), os.path.join(HERE, "board.html")], check=True)
