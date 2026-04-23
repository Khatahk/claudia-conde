"""Auditoría de indexación GSC para sc-domain:passas.io"""

import json
import os
import sys
import warnings
from datetime import date, timedelta

import requests
import urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC_API   = "https://www.googleapis.com/webmasters/v3"
SC_API    = "https://searchconsole.googleapis.com/v1"
SITE      = "sc-domain:passas.io"
SITE_ENC  = requests.utils.quote(SITE, safe="")
TODAY     = date.today()
D90       = (TODAY - timedelta(days=90)).isoformat()
D30       = (TODAY - timedelta(days=30)).isoformat()
D7        = (TODAY - timedelta(days=7)).isoformat()
TODAY_S   = TODAY.isoformat()

def get_session():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GSC_SERVICE_ACCOUNT_FILE"), scopes=SCOPES
    )
    s = AuthorizedSession(creds)
    s.verify = False
    return s

def gsc_get(session, path):
    r = session.get(f"{GSC_API}/{path}")
    r.raise_for_status()
    return r.json()

def gsc_post(session, path, body):
    r = session.post(f"{GSC_API}/{path}", json=body)
    r.raise_for_status()
    return r.json()

def sc_post(session, path, body):
    r = session.post(f"{SC_API}/{path}", json=body)
    r.raise_for_status()
    return r.json()

# ─── 1. SITEMAPS ────────────────────────────────────────────────────────────
def audit_sitemaps(session):
    data = gsc_get(session, f"sites/{SITE_ENC}/sitemaps")
    sitemaps = data.get("sitemap", [])
    results = []
    for sm in sitemaps:
        errors   = sum(c.get("count", 0) for c in sm.get("contents", []) if c.get("type") == "indexedError")
        warnings = sum(c.get("count", 0) for c in sm.get("contents", []) if c.get("type") == "indexedWarning")
        indexed  = sum(c.get("count", 0) for c in sm.get("contents", []) if c.get("type") == "indexed")
        submitted= next((c.get("count",0) for c in sm.get("contents",[]) if c.get("type")=="submitted"),0)
        results.append({
            "url":       sm.get("path"),
            "last_downloaded": sm.get("lastDownloaded", "?"),
            "submitted": submitted,
            "indexed":   indexed,
            "errors":    errors,
            "warnings":  warnings,
            "is_sitemapIndex": sm.get("isSitemapsIndex", False),
        })
    return results

# ─── 2. SEARCH ANALYTICS ────────────────────────────────────────────────────
def analytics_query(session, start, end, dimensions, row_limit=25, filters=None):
    body = {
        "startDate": start, "endDate": end,
        "dimensions": dimensions, "rowLimit": row_limit,
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    return gsc_post(session, f"sites/{SITE_ENC}/searchAnalytics/query", body).get("rows", [])

# ─── 3. URL INSPECTION ──────────────────────────────────────────────────────
def inspect_url(session, page_url):
    body = {"inspectionUrl": page_url, "siteUrl": SITE}
    try:
        r = session.post(f"{SC_API}/urlInspection/index:inspect", json=body)
        r.raise_for_status()
        return r.json().get("inspectionResult", {})
    except Exception as e:
        return {"error": str(e)}

# ────────────────────────────────────────────────────────────────────────────
def main():
    session = get_session()

    # ── SITEMAPS ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  1. SITEMAPS                                     ║")
    print("╚══════════════════════════════════════════════════╝")
    sitemaps = audit_sitemaps(session)
    if not sitemaps:
        print("  ⚠  No hay sitemaps registrados en GSC.")
    for sm in sitemaps:
        idx_rate = f"{sm['indexed']/sm['submitted']*100:.1f}%" if sm['submitted'] else "N/A"
        print(f"\n  URL        : {sm['url']}")
        print(f"  Descargado : {sm['last_downloaded']}")
        print(f"  Enviadas   : {sm['submitted']}  |  Indexadas: {sm['indexed']}  ({idx_rate})")
        print(f"  Errores    : {sm['errors']}  |  Avisos: {sm['warnings']}")

    # ── RENDIMIENTO GENERAL 90 días ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  2. RENDIMIENTO GLOBAL (últimos 90 días)         ║")
    print("╚══════════════════════════════════════════════════╝")
    rows90 = analytics_query(session, D90, TODAY_S, ["date"], row_limit=90)
    if rows90:
        total_clicks = sum(r["clicks"] for r in rows90)
        total_impr   = sum(r["impressions"] for r in rows90)
        avg_ctr      = total_clicks / total_impr * 100 if total_impr else 0
        avg_pos      = sum(r["position"] for r in rows90) / len(rows90)
        print(f"  Clics totales    : {total_clicks:,}")
        print(f"  Impresiones      : {total_impr:,}")
        print(f"  CTR medio        : {avg_ctr:.2f}%")
        print(f"  Posición media   : {avg_pos:.1f}")

        # Tendencia: últimos 30 vs anteriores 30
        recent = [r for r in rows90 if r["keys"][0] >= D30]
        prev   = [r for r in rows90 if r["keys"][0] < D30 and r["keys"][0] >= (TODAY - timedelta(days=60)).isoformat()]
        if recent and prev:
            rc = sum(r["clicks"] for r in recent)
            pc = sum(r["clicks"] for r in prev)
            ri = sum(r["impressions"] for r in recent)
            pi = sum(r["impressions"] for r in prev)
            trend_c = (rc-pc)/pc*100 if pc else 0
            trend_i = (ri-pi)/pi*100 if pi else 0
            print(f"\n  Tendencia (últ.30 vs 30 ant.):")
            print(f"    Clics       : {rc:,} vs {pc:,}  ({trend_c:+.1f}%)")
            print(f"    Impresiones : {ri:,} vs {pi:,}  ({trend_i:+.1f}%)")
    else:
        print("  Sin datos de rendimiento.")

    # ── TOP PÁGINAS ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  3. TOP PÁGINAS (últimos 30 días)                ║")
    print("╚══════════════════════════════════════════════════╝")
    pages = analytics_query(session, D30, TODAY_S, ["page"], row_limit=20)
    if pages:
        print(f"  {'Clics':>6}  {'Impr':>7}  {'CTR':>6}  {'Pos':>6}  URL")
        print(f"  {'─'*6}  {'─'*7}  {'─'*6}  {'─'*6}  {'─'*40}")
        for p in pages:
            print(f"  {p['clicks']:>6,}  {p['impressions']:>7,}  {p['ctr']*100:>5.1f}%  {p['position']:>6.1f}  {p['keys'][0]}")
    else:
        print("  Sin datos.")

    # ── PÁGINAS SIN CLICS (alta impresión, CTR bajo) ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  4. PÁGINAS CON BAJO CTR (>100 impr, 0 clics)   ║")
    print("╚══════════════════════════════════════════════════╝")
    low_ctr = [p for p in pages if p["impressions"] > 100 and p["clicks"] == 0]
    if low_ctr:
        for p in low_ctr:
            print(f"  Impr={p['impressions']:,}  Pos={p['position']:.1f}  {p['keys'][0]}")
    else:
        print("  No se detectan páginas con este patrón.")

    # ── TOP QUERIES ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  5. TOP QUERIES (últimos 30 días)                ║")
    print("╚══════════════════════════════════════════════════╝")
    queries = analytics_query(session, D30, TODAY_S, ["query"], row_limit=20)
    if queries:
        print(f"  {'Clics':>6}  {'Impr':>7}  {'CTR':>6}  {'Pos':>6}  Query")
        print(f"  {'─'*6}  {'─'*7}  {'─'*6}  {'─'*6}  {'─'*40}")
        for q in queries:
            print(f"  {q['clicks']:>6,}  {q['impressions']:>7,}  {q['ctr']*100:>5.1f}%  {q['position']:>6.1f}  {q['keys'][0]}")
    else:
        print("  Sin datos.")

    # ── QUERIES EN POSICIÓN 11-20 (page 2) ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  6. QUERIES EN PÁGINA 2 (pos 11-20, oportunidad)║")
    print("╚══════════════════════════════════════════════════╝")
    queries_all = analytics_query(session, D30, TODAY_S, ["query"], row_limit=100)
    page2 = [q for q in queries_all if 11 <= q["position"] <= 20 and q["impressions"] > 10]
    page2.sort(key=lambda x: x["impressions"], reverse=True)
    if page2:
        print(f"  {'Clics':>6}  {'Impr':>7}  {'Pos':>6}  Query")
        for q in page2[:15]:
            print(f"  {q['clicks']:>6,}  {q['impressions']:>7,}  {q['position']:>6.1f}  {q['keys'][0]}")
    else:
        print("  No hay queries en página 2 con suficientes impresiones.")

    # ── DISPOSITIVOS ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  7. DESGLOSE POR DISPOSITIVO (últimos 30 días)  ║")
    print("╚══════════════════════════════════════════════════╝")
    devices = analytics_query(session, D30, TODAY_S, ["device"], row_limit=10)
    for d in devices:
        print(f"  {d['keys'][0]:12s}  Clics={d['clicks']:,}  Impr={d['impressions']:,}  "
              f"CTR={d['ctr']*100:.1f}%  Pos={d['position']:.1f}")

    # ── INSPECCIÓN DE URLS PRINCIPALES ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  8. INSPECCIÓN DE URLs PRINCIPALES               ║")
    print("╚══════════════════════════════════════════════════╝")
    # Inspecciona homepage + top páginas (máx 5)
    urls_to_check = ["https://passas.io/"]
    if pages:
        for p in pages[:4]:
            u = p["keys"][0]
            if u not in urls_to_check:
                urls_to_check.append(u)

    for url in urls_to_check:
        result = inspect_url(session, url)
        if "error" in result:
            print(f"\n  URL: {url}\n  ⚠  {result['error']}")
            continue
        idx  = result.get("indexStatusResult", {})
        mob  = result.get("mobileUsabilityResult", {})
        rich = result.get("richResultsResult", {})

        verdict      = idx.get("verdict", "?")
        coverage     = idx.get("coverageState", "?")
        robots       = idx.get("robotsTxtState", "?")
        indexing_st  = idx.get("indexingState", "?")
        last_crawled = idx.get("lastCrawlTime", "sin rastreo")
        crawled_as   = idx.get("crawledAs", "?")
        canonical    = idx.get("googleCanonical", url)
        mob_verdict  = mob.get("verdict", "?")

        icon = "✅" if verdict == "PASS" else "❌" if verdict == "FAIL" else "⚠ "
        print(f"\n  {icon} {url}")
        print(f"     Indexada        : {verdict}  ({coverage})")
        print(f"     Robots.txt      : {robots}")
        print(f"     Estado indexado : {indexing_st}")
        print(f"     Último rastreo  : {last_crawled}  (como: {crawled_as})")
        print(f"     Canonical GSC   : {canonical}")
        print(f"     Usabilidad móvil: {mob_verdict}")
        if mob.get("issues"):
            for issue in mob["issues"]:
                print(f"       - {issue.get('issueType','?')}: {issue.get('message','')}")

    print("\n" + "═"*55 + "\n")

if __name__ == "__main__":
    main()
