#!/usr/bin/env python3
"""
adscan - Meta Ad Library reklam omru tarayicisi.

Amac: Bir nis veya reklamveren icin Instagram/Facebook reklamlarinin
NE ZAMAN ACILDIGINI ve NE ZAMAN KAPATILDIGINI cekip, hangi reklamlarin
uzun sure ayakta kaldigini olcmek. Uzun yasayan reklam = para kazandiran
reklam varsayimini, 2026 kosullarina gore duzeltilmis bir skorla test eder.

ONEMLI KISIT (Meta'nin kurali, aracin degil):
  Ticari (siyasi olmayan) reklamlar API'den SADECE ad_reached_countries
  bir AB/AEA ulkesi veya UK oldugunda doner. Ayrica DURDURULMUS reklamlarin
  gecmisi de yalnizca AB'de ~1 yil saklanir. Bu yuzden varsayilan ulkeler
  AB'dir: ABD'yi sorgularsaniz "kapanma tarihi" verisi gelmez.

Kullanim:
  export META_AD_LIBRARY_TOKEN=...
  python3 adscan.py --query "calorie tracker" --countries DE,NL,FR
  python3 adscan.py --pages 1234567890,9876543210 --csv cikti.csv
  python3 adscan.py --selftest
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

API_VERSION = "v21.0"
API_HOST = "https://graph.facebook.com"

# ad_type=ALL yalnizca bu ulkeler icin ticari reklam dondurur.
EU_DEFAULT = ["DE", "NL", "FR", "ES", "IT", "PL", "SE", "IE"]

FIELDS = [
    "id",
    "page_id",
    "page_name",
    "ad_creation_time",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "ad_creative_bodies",
    "ad_creative_link_titles",
    "ad_creative_link_captions",
    "ad_snapshot_url",
    "publisher_platforms",
    "eu_total_reach",
    "target_locations",
]


# --------------------------------------------------------------------------
# Veri modeli
# --------------------------------------------------------------------------

@dataclass
class Ad:
    ad_id: str
    page_id: str
    page_name: str
    start: date
    stop: date | None          # None => hala yayinda
    body: str = ""
    platforms: list[str] = field(default_factory=list)
    reach: int | None = None
    snapshot_url: str = ""

    @property
    def is_active(self) -> bool:
        return self.stop is None

    def days_running(self, today: date) -> int:
        """Reklamin toplam yasam suresi (gun). Aktifse bugune kadar."""
        end = self.stop if self.stop is not None else today
        return max((end - self.start).days, 0)

    def on_instagram(self) -> bool:
        return any("instagram" in p.lower() for p in self.platforms)


@dataclass
class AdvertiserStats:
    page_id: str
    page_name: str
    n_ads: int
    n_active: int
    n_stopped: int
    max_days_active: int          # hala yayinda olan en eski reklam
    max_days_any: int
    median_life_stopped: float    # kapatilmis reklamlarin medyan omru
    survivor_ratio: float         # omru >= 90 gun olan reklam orani
    infant_mortality: float       # kapatilanlarin <=14 gunde olme orani
    refresh_30d: int              # son 30 gunde acilan yeni reklam sayisi
    instagram_share: float
    verdict: str
    score: float

    def as_row(self) -> dict:
        return {
            "page_name": self.page_name,
            "page_id": self.page_id,
            "verdict": self.verdict,
            "score": round(self.score, 1),
            "ads_total": self.n_ads,
            "ads_active": self.n_active,
            "ads_stopped": self.n_stopped,
            "oldest_active_days": self.max_days_active,
            "oldest_any_days": self.max_days_any,
            "median_life_of_killed_ads": round(self.median_life_stopped, 1),
            "survivor_ratio_90d": round(self.survivor_ratio, 3),
            "infant_mortality_14d": round(self.infant_mortality, 3),
            "new_ads_last_30d": self.refresh_30d,
            "instagram_share": round(self.instagram_share, 3),
        }


# --------------------------------------------------------------------------
# Skorlama - saf fonksiyon, testi asagida
# --------------------------------------------------------------------------

SURVIVOR_DAYS = 90      # "kanitlanmis" kabul edilen omur esigi
INFANT_DAYS = 14        # bu surede kapatilan reklam = basarisiz test


def score_advertiser(ads: list[Ad], today: date) -> AdvertiserStats:
    """Bir reklamverenin reklam omur dagilimindan saglik skoru cikarir.

    2026 duzeltmesi: tek basina "eski reklam" kaniti degildir. Cost-cap /
    Advantage+ ile calisan hesaplar kazanmayan reklami da acik birakabiliyor.
    Gercek sinyal, eski reklamin YANINDA surekli yeni kreatif acilmasidir -
    yani hesap hala para basiyor ve kreatif yeniliyor. Eski reklam + sifir
    yenileme = unutulmus hesap, kazanan degil.
    """
    if not ads:
        raise ValueError("bos reklam listesi")

    lives = [a.days_running(today) for a in ads]
    active = [a for a in ads if a.is_active]
    stopped = [a for a in ads if not a.is_active]

    stopped_lives = [a.days_running(today) for a in stopped]
    median_life_stopped = statistics.median(stopped_lives) if stopped_lives else 0.0

    max_days_active = max((a.days_running(today) for a in active), default=0)
    max_days_any = max(lives)

    survivor_ratio = sum(1 for d in lives if d >= SURVIVOR_DAYS) / len(lives)
    infant_mortality = (
        sum(1 for d in stopped_lives if d <= INFANT_DAYS) / len(stopped_lives)
        if stopped_lives
        else 0.0
    )
    refresh_30d = sum(1 for a in ads if (today - a.start).days <= 30)
    ig_share = sum(1 for a in ads if a.on_instagram()) / len(ads)

    # --- skor: 0-100 ---
    s = 0.0
    s += min(max_days_active / 365.0, 1.0) * 30       # ayakta kalan en eski reklam
    s += min(survivor_ratio / 0.35, 1.0) * 25          # kalici kreatif orani
    s += min(refresh_30d / 8.0, 1.0) * 25              # canli yenileme temposu
    s += min(len(active) / 15.0, 1.0) * 10             # es zamanli olcek
    s += (1.0 - min(infant_mortality, 1.0)) * 10       # test israfinin azligi

    # --- karar ---
    if max_days_active >= SURVIVOR_DAYS and refresh_30d >= 3 and survivor_ratio >= 0.20:
        verdict = "PARA BASIYOR"
    elif refresh_30d >= 6 and max_days_active < SURVIVOR_DAYS:
        verdict = "OLCEKLENIYOR"
    elif max_days_active >= SURVIVOR_DAYS and refresh_30d == 0:
        verdict = "UNUTULMUS (eski ama olu hesap)"
        s *= 0.5
    elif stopped and infant_mortality >= 0.6:
        verdict = "TEST EDIYOR (henuz tutturamamis)"
    else:
        verdict = "BELIRSIZ"

    return AdvertiserStats(
        page_id=ads[0].page_id,
        page_name=ads[0].page_name,
        n_ads=len(ads),
        n_active=len(active),
        n_stopped=len(stopped),
        max_days_active=max_days_active,
        max_days_any=max_days_any,
        median_life_stopped=median_life_stopped,
        survivor_ratio=survivor_ratio,
        infant_mortality=infant_mortality,
        refresh_30d=refresh_30d,
        instagram_share=ig_share,
        verdict=verdict,
        score=s,
    )


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------

def _parse_date(raw: str | None) -> date | None:
    if not raw:
        return None
    raw = raw.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    # ISO fallback
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def ad_from_api(row: dict) -> Ad | None:
    start = _parse_date(row.get("ad_delivery_start_time"))
    if start is None:
        return None
    bodies = row.get("ad_creative_bodies") or []
    reach = row.get("eu_total_reach")
    return Ad(
        ad_id=str(row.get("id", "")),
        page_id=str(row.get("page_id", "")),
        page_name=row.get("page_name", "(bilinmiyor)"),
        start=start,
        stop=_parse_date(row.get("ad_delivery_stop_time")),
        body=(bodies[0] if bodies else "")[:400],
        platforms=row.get("publisher_platforms") or [],
        reach=int(reach) if isinstance(reach, (int, str)) and str(reach).isdigit() else None,
        snapshot_url=row.get("ad_snapshot_url", ""),
    )


def fetch_ads(
    token: str,
    countries: list[str],
    query: str | None = None,
    page_ids: list[str] | None = None,
    limit: int = 500,
    max_pages: int = 20,
) -> list[Ad]:
    """ads_archive'i sayfalayarak ceker. ad_type=ALL + AB ulkeleri sart."""
    params = {
        "access_token": token,
        "ad_type": "ALL",
        "ad_active_status": "ALL",   # hem aktif hem kapatilmis -> omur analizi
        "ad_reached_countries": json.dumps(countries),
        "fields": ",".join(FIELDS),
        "limit": str(min(limit, 500)),
    }
    if page_ids:
        params["search_page_ids"] = json.dumps(page_ids[:10])
    elif query:
        params["search_terms"] = query
    else:
        raise ValueError("--query ya da --pages vermelisiniz")

    url = f"{API_HOST}/{API_VERSION}/ads_archive?" + urllib.parse.urlencode(params)
    ads: list[Ad] = []

    for _ in range(max_pages):
        req = urllib.request.Request(url, headers={"User-Agent": "adscan/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise SystemExit(
                f"API hatasi {exc.code}: {detail}\n\n"
                "Ipucu: ad_type=ALL ticari reklamlari yalnizca AB/UK icin dondurur. "
                "ABD sorguladiysaniz bos/hatali doner."
            ) from exc
        except urllib.error.URLError as exc:
            raise SystemExit(
                f"Aga ulasilamadi: {exc.reason}\n"
                "graph.facebook.com erisilebilir bir agdan calistirin."
            ) from exc

        for row in payload.get("data", []):
            ad = ad_from_api(row)
            if ad:
                ads.append(ad)

        nxt = (payload.get("paging") or {}).get("next")
        if not nxt:
            break
        url = nxt

    return ads


# --------------------------------------------------------------------------
# Rapor
# --------------------------------------------------------------------------

def group_and_score(ads: list[Ad], today: date, min_ads: int = 2) -> list[AdvertiserStats]:
    buckets: dict[str, list[Ad]] = {}
    for ad in ads:
        buckets.setdefault(ad.page_id or ad.page_name, []).append(ad)
    stats = [
        score_advertiser(group, today)
        for group in buckets.values()
        if len(group) >= min_ads
    ]
    return sorted(stats, key=lambda s: s.score, reverse=True)


def print_table(stats: list[AdvertiserStats], top: int = 25) -> None:
    if not stats:
        print("Sonuc yok. Farkli anahtar kelime veya ulke deneyin.")
        return
    hdr = f"{'REKLAMVEREN':<28} {'SKOR':>5} {'AKTIF':>5} {'EN ESKI':>8} {'90G+':>6} {'YENI30':>7}  KARAR"
    print(hdr)
    print("-" * len(hdr))
    for s in stats[:top]:
        print(
            f"{s.page_name[:27]:<28} {s.score:>5.1f} {s.n_active:>5} "
            f"{s.max_days_active:>7}g {s.survivor_ratio*100:>5.0f}% {s.refresh_30d:>7}  {s.verdict}"
        )
    print()
    print(f"Toplam {len(stats)} reklamveren. 'EN ESKI' = hala yayinda olan en eski reklamin gun sayisi.")


def write_csv(path: str, stats: list[AdvertiserStats]) -> None:
    if not stats:
        return
    rows = [s.as_row() for s in stats]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV yazildi: {path}")


def write_ads_csv(path: str, ads: list[Ad], today: date) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            ["page_name", "ad_id", "acilis", "kapanis", "gun", "aktif", "instagram", "metin", "snapshot"]
        )
        for a in sorted(ads, key=lambda x: x.days_running(today), reverse=True):
            writer.writerow(
                [
                    a.page_name,
                    a.ad_id,
                    a.start.isoformat(),
                    a.stop.isoformat() if a.stop else "",
                    a.days_running(today),
                    "evet" if a.is_active else "hayir",
                    "evet" if a.on_instagram() else "hayir",
                    a.body.replace("\n", " ")[:300],
                    a.snapshot_url,
                ]
            )
    print(f"Reklam detay CSV yazildi: {path}")


# --------------------------------------------------------------------------
# Selftest
# --------------------------------------------------------------------------

def _selftest() -> int:
    today = date(2026, 9, 14)

    def mk(start: str, stop: str | None, name="Acme", pid="1", ig=True) -> Ad:
        return Ad(
            ad_id=f"{name}-{start}-{stop}",
            page_id=pid,
            page_name=name,
            start=date.fromisoformat(start),
            stop=date.fromisoformat(stop) if stop else None,
            platforms=["instagram", "facebook"] if ig else ["facebook"],
        )

    failures = []

    def check(label, got, want):
        if got != want:
            failures.append(f"  {label}: beklenen {want}, gelen {got}")

    # omur hesabi
    check("aktif omru", mk("2026-01-01", None).days_running(today), 256)
    check("kapali omru", mk("2026-01-01", "2026-03-02").days_running(today), 60)
    check("negatif yok", mk("2026-12-01", None).days_running(today), 0)

    # PARA BASIYOR: eski aktif reklam + canli yenileme
    winner = (
        [mk("2025-06-01", None)] * 1
        + [mk("2025-08-01", None) for _ in range(3)]
        + [mk("2026-09-01", None) for _ in range(4)]
        + [mk("2026-02-01", "2026-02-10") for _ in range(2)]
    )
    w = score_advertiser(winner, today)
    check("winner verdict", w.verdict, "PARA BASIYOR")

    # UNUTULMUS: eski reklam ama 30 gunde sifir yeni
    stale = [mk("2025-01-01", None), mk("2025-01-05", None), mk("2025-02-01", "2025-03-01")]
    st = score_advertiser(stale, today)
    check("stale verdict", st.verdict, "UNUTULMUS (eski ama olu hesap)")
    if not st.score < w.score:
        failures.append("  unutulmus hesap skoru kazanandan dusuk olmali")

    # TEST EDIYOR: cogu reklam 14 gunde olmus
    testing = [mk(f"2026-0{m}-01", f"2026-0{m}-08") for m in range(1, 8)]
    t = score_advertiser(testing, today)
    check("testing verdict", t.verdict, "TEST EDIYOR (henuz tutturamamis)")
    check("infant mortality", round(t.infant_mortality, 2), 1.0)

    # OLCEKLENIYOR: cok yeni reklam, henuz 90 gunu dolan yok
    scaling = [mk("2026-08-20", None) for _ in range(8)]
    sc = score_advertiser(scaling, today)
    check("scaling verdict", sc.verdict, "OLCEKLENIYOR")

    # tarih ayristirma
    check("iso z", _parse_date("2026-01-02T00:00:00+0000"), date(2026, 1, 2))
    check("plain", _parse_date("2026-01-02"), date(2026, 1, 2))
    check("bos", _parse_date(None), None)

    # api satiri -> Ad
    ad = ad_from_api(
        {
            "id": "9",
            "page_id": "7",
            "page_name": "Test",
            "ad_delivery_start_time": "2026-01-01",
            "ad_delivery_stop_time": "",
            "publisher_platforms": ["instagram"],
            "ad_creative_bodies": ["merhaba"],
        }
    )
    check("api aktif", ad.is_active, True)
    check("api ig", ad.on_instagram(), True)

    # gruplama sirali mi
    mixed = winner + [mk("2025-01-01", None, name="Stale", pid="2")] * 3
    ranked = group_and_score(mixed, today)
    check("siralama", ranked[0].page_name, "Acme")

    if failures:
        print("SELFTEST BASARISIZ:")
        print("\n".join(failures))
        return 1
    print("selftest: tum kontroller gecti")
    return 0


# --------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Meta Ad Library reklam omru tarayicisi")
    p.add_argument("--query", help="anahtar kelime, orn: 'calorie tracker'")
    p.add_argument("--pages", help="virgullu Facebook Page ID listesi (en fazla 10)")
    p.add_argument("--countries", default=",".join(EU_DEFAULT),
                   help=f"virgullu ulke kodlari (varsayilan AB: {','.join(EU_DEFAULT)})")
    p.add_argument("--token", default=os.environ.get("META_AD_LIBRARY_TOKEN", ""))
    p.add_argument("--csv", help="reklamveren ozeti icin cikti dosyasi")
    p.add_argument("--ads-csv", help="tek tek reklamlar icin cikti dosyasi")
    p.add_argument("--min-ads", type=int, default=2, help="reklamveren basina asgari reklam sayisi")
    p.add_argument("--top", type=int, default=25)
    p.add_argument("--selftest", action="store_true", help="skorlama mantigini test et (ag gerekmez)")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    if not args.token:
        print("HATA: META_AD_LIBRARY_TOKEN yok. developers.facebook.com'da "
              "Ad Library API urununu ekleyip token alin.", file=sys.stderr)
        return 2
    if not args.query and not args.pages:
        p.error("--query veya --pages gerekli")

    countries = [c.strip().upper() for c in args.countries.split(",") if c.strip()]
    non_eu = [c for c in countries if c not in set(EU_DEFAULT) | {
        "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "GR", "HU",
        "LV", "LT", "LU", "MT", "PT", "RO", "SK", "SI", "GB", "IS", "LI", "NO"}]
    if non_eu:
        print(f"UYARI: {', '.join(non_eu)} AB/UK disinda. Meta bu ulkeler icin "
              "ticari reklam ve kapanma tarihi dondurmez.", file=sys.stderr)

    page_ids = [x.strip() for x in args.pages.split(",")] if args.pages else None
    ads = fetch_ads(args.token, countries, query=args.query, page_ids=page_ids)
    today = datetime.now(timezone.utc).date()

    print(f"\n{len(ads)} reklam cekildi ({'aktif+kapali' if ads else '-'}).\n")
    stats = group_and_score(ads, today, min_ads=args.min_ads)
    print_table(stats, top=args.top)

    if args.csv:
        write_csv(args.csv, stats)
    if args.ads_csv:
        write_ads_csv(args.ads_csv, ads, today)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
