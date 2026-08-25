#!/usr/bin/env python3
"""
Cotejo del informe GSC 2026-08-24 y su respuesta contra el estado actual de GSC.
Ejecutado el 2026-08-25. Vuelca JSON crudo para trazabilidad.
"""

import json
import os
import sys
from datetime import date, datetime, timedelta

import requests
import urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC = "https://www.googleapis.com/webmasters/v3"
INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SITE = "sc-domain:passas.io"

OUT = {}


def session():
    sa = os.getenv("GSC_SERVICE_ACCOUNT_FILE")
    creds = service_account.Credentials.from_service_account_file(sa, scopes=SCOPES)
    s = AuthorizedSession(creds)
    s.verify = False
    return s


def sa_query(s, start, end, dimensions=None, row_limit=500, filters=None):
    url = f"{GSC}/sites/{requests.utils.quote(SITE, safe='')}/searchAnalytics/query"
    body = {"startDate": start, "endDate": end, "rowLimit": row_limit}
    if dimensions:
        body["dimensions"] = dimensions
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    r = s.post(url, json=body)
    r.raise_for_status()
    return r.json().get("rows", [])


def totals(rows):
    c = sum(r["clicks"] for r in rows)
    i = sum(r["impressions"] for r in rows)
    ctr = (c / i * 100) if i else 0
    pos = (sum(r["position"] * r["impressions"] for r in rows) / i) if i else 0
    return {"clicks": c, "impressions": i, "ctr": round(ctr, 2), "position": round(pos, 2)}


def main():
    s = session()
    today = date.today()
    print(f"=== COTEJO GSC — ejecutado {today.isoformat()} ===\n")

    # --- 1. Frescura de datos: hasta qué día tiene GSC procesado ---
    print("[1] Frescura de datos GSC")
    daily = sa_query(s, (today - timedelta(days=20)).isoformat(), today.isoformat(), ["date"])
    daily.sort(key=lambda r: r["keys"][0])
    OUT["serie_diaria_reciente"] = [
        {"fecha": r["keys"][0], "clics": r["clicks"], "impresiones": r["impressions"],
         "ctr": round(r["ctr"] * 100, 2), "pos": round(r["position"], 1)}
        for r in daily
    ]
    for d in OUT["serie_diaria_reciente"]:
        print(f"    {d['fecha']}  clics={d['clics']:>3}  impr={d['impresiones']:>4}  "
              f"ctr={d['ctr']:>5}%  pos={d['pos']}")
    ultimo = OUT["serie_diaria_reciente"][-1]["fecha"] if OUT["serie_diaria_reciente"] else None
    print(f"    -> Último día con datos: {ultimo}")

    # --- 2. Ventana del informe (3-24 ago) reconsultada hoy ---
    print("\n[2] Ventana del informe 2026-08-03 a 2026-08-24, reconsultada hoy")
    win = sa_query(s, "2026-08-03", "2026-08-24", ["date"])
    OUT["ventana_informe_recheck"] = totals(win)
    print(f"    {OUT['ventana_informe_recheck']}")
    print(f"    (informe declaraba: clics=35, impresiones=3458, ctr=1.01, pos=8.16)")

    prev = sa_query(s, "2026-07-12", "2026-08-02", ["date"])
    OUT["ventana_previa_recheck"] = totals(prev)
    print(f"    previa: {OUT['ventana_previa_recheck']}")
    print(f"    (informe declaraba: clics=29, impresiones=4104, ctr=0.71, pos=7.73)")

    # --- 3. Semana de la inflexión 16-22 ago ---
    print("\n[3] Semana 2026-08-16 a 2026-08-22 (la inflexión del informe)")
    infl = sa_query(s, "2026-08-16", "2026-08-22", ["date"])
    OUT["semana_inflexion"] = totals(infl)
    print(f"    {OUT['semana_inflexion']}   (informe: 23 clics / 1.277 impr / 1,80%)")

    # --- 4. Semana posterior 23-25 ago: ¿se sostiene? ---
    print("\n[4] Días posteriores al informe (2026-08-23 en adelante)")
    post = sa_query(s, "2026-08-23", today.isoformat(), ["date"])
    post.sort(key=lambda r: r["keys"][0])
    OUT["post_informe"] = [
        {"fecha": r["keys"][0], "clics": r["clicks"], "impresiones": r["impressions"],
         "ctr": round(r["ctr"] * 100, 2), "pos": round(r["position"], 1)}
        for r in post
    ]
    if OUT["post_informe"]:
        for d in OUT["post_informe"]:
            print(f"    {d['fecha']}  clics={d['clics']:>3}  impr={d['impresiones']:>4}  pos={d['pos']}")
        print(f"    agregado: {totals(post)}")
    else:
        print("    Sin datos aún para 23-25 ago (latencia GSC 2-3 días)")

    # --- 5. Páginas de la ventana, recontadas ---
    print("\n[5] Top páginas ventana 03-24 ago (recheck)")
    pages = sa_query(s, "2026-08-03", "2026-08-24", ["page"], row_limit=200)
    pages.sort(key=lambda r: -r["impressions"])
    OUT["paginas_ventana"] = [
        {"pagina": r["keys"][0].replace("https://passas.io", ""), "clics": r["clicks"],
         "impresiones": r["impressions"], "ctr": round(r["ctr"] * 100, 2),
         "pos": round(r["position"], 1)}
        for r in pages
    ]
    for p in OUT["paginas_ventana"][:15]:
        print(f"    {p['clics']:>3}c {p['impresiones']:>5}i  pos={p['pos']:>5}  {p['pagina'][:70]}")

    # --- 6. Concentración burofax ---
    buro = [p for p in OUT["paginas_ventana"] if "burofax" in p["pagina"]]
    tot_w = OUT["ventana_informe_recheck"]
    if buro and tot_w["clicks"]:
        pct = buro[0]["clics"] / tot_w["clicks"] * 100
        OUT["concentracion_burofax"] = {
            "clics_burofax": buro[0]["clics"], "clics_sitio": tot_w["clicks"],
            "pct": round(pct, 1), "pos": buro[0]["pos"], "ctr": buro[0]["ctr"]}
        print(f"\n[6] Concentración burofax: {buro[0]['clics']}/{tot_w['clicks']} "
              f"= {pct:.1f}%  (informe: 60%)")

    # --- 7. Locale EN ---
    print("\n[7] Locale /en — ventana 03-24 ago")
    en_rows = [p for p in OUT["paginas_ventana"] if p["pagina"].startswith("/en")]
    en_tot = {"clics": sum(p["clics"] for p in en_rows),
              "impresiones": sum(p["impresiones"] for p in en_rows),
              "urls_con_impresiones": len(en_rows)}
    OUT["locale_en"] = {"total": en_tot, "paginas": en_rows}
    print(f"    {en_tot}   (informe: 553 impresiones, 1 clic)")
    pct_int = en_tot["impresiones"] / tot_w["impressions"] * 100 if tot_w["impressions"] else 0
    print(f"    /en = {pct_int:.1f}% de las impresiones del sitio")

    # --- 8. Cluster AI Act comercial ---
    print("\n[8] Páginas /servicios/techlaw-* (cluster AI Act comercial)")
    tech = [p for p in OUT["paginas_ventana"] if "techlaw" in p["pagina"]]
    OUT["cluster_aiact"] = tech
    for p in tech:
        print(f"    {p['clics']:>3}c {p['impresiones']:>5}i  pos={p['pos']:>5}  {p['pagina']}")
    print(f"    total impresiones: {sum(p['impresiones'] for p in tech)}  "
          f"clics: {sum(p['clics'] for p in tech)}   (informe: 219 impr / 0 clics / pos 24,1)")

    # --- 9. Asimetría ES/EN en AI Act (punto 3.4 de la respuesta) ---
    print("\n[9] Asimetría ES/EN AI Act (afirmación 3.4 de la respuesta)")
    asim = {}
    for path in ["/servicios/techlaw-ai-act-compliance", "/en/servicios/ai-act-compliance",
                 "/en/servicios/ai-act-high-risk", "/servicios/techlaw-ai-act-alto-riesgo",
                 "/en/blog/digital-omnibus-ai-act-final-text",
                 "/blog/digital-omnibus-ai-act-2026-que-cambia-que-no"]:
        m = [p for p in OUT["paginas_ventana"] if p["pagina"] == path]
        asim[path] = m[0] if m else None
        if m:
            print(f"    pos={m[0]['pos']:>5}  {m[0]['impresiones']:>4}i  {path}")
        else:
            print(f"    (sin impresiones)  {path}")
    OUT["asimetria_es_en"] = asim

    # --- 10. Dispositivo ---
    print("\n[10] Dispositivo")
    dev = sa_query(s, "2026-08-03", "2026-08-24", ["device"])
    OUT["dispositivo"] = [
        {"dispositivo": r["keys"][0], "clics": r["clicks"], "impresiones": r["impressions"],
         "ctr": round(r["ctr"] * 100, 2), "pos": round(r["position"], 1)} for r in dev]
    for d in OUT["dispositivo"]:
        print(f"    {d['dispositivo']:<8} {d['clics']:>3}c {d['impresiones']:>5}i  "
              f"ctr={d['ctr']}%  pos={d['pos']}")

    # --- 11. Marca ---
    print("\n[11] Consultas de marca «passas»")
    brand = sa_query(s, "2026-08-03", "2026-08-24", ["query"], row_limit=500)
    bq = [r for r in brand if "passa" in r["keys"][0].lower()]
    OUT["marca"] = {"total": totals(bq), "consultas": [
        {"q": r["keys"][0], "clics": r["clicks"], "impresiones": r["impressions"],
         "pos": round(r["position"], 1)} for r in bq]}
    print(f"    {OUT['marca']['total']}   (informe: 124 impresiones, 2 clics)")

    # --- 12. Reparto por bloque de negocio (lo que pide la respuesta 3.3) ---
    print("\n[12] Reparto por bloque de negocio (regla 7 de la respuesta)")
    def bloque(path):
        if path.startswith("/en"):
            return "Internacional / locale EN (Perfil C)"
        if "techlaw" in path or "internacional-" in path or "ai-act" in path:
            return "TechLaw ES (Perfil B)"
        if path in ("/", "/servicios", "/blog", "/honorarios") or path.startswith("/team") \
           or path.startswith("/politica") or path.startswith("/aviso") \
           or path.startswith("/terminos") or path.startswith("/autoevaluacion"):
            return "Marca e institucional"
        return "Litigación y consumo ES (Perfil A)"

    agg = {}
    for p in OUT["paginas_ventana"]:
        b = bloque(p["pagina"])
        a = agg.setdefault(b, {"clics": 0, "impresiones": 0, "pos_w": 0.0})
        a["clics"] += p["clics"]
        a["impresiones"] += p["impresiones"]
        a["pos_w"] += p["pos"] * p["impresiones"]
    for b, a in agg.items():
        a["pos_media"] = round(a["pos_w"] / a["impresiones"], 1) if a["impresiones"] else 0
        del a["pos_w"]
    OUT["bloques_negocio"] = agg
    for b, a in sorted(agg.items(), key=lambda x: -x[1]["impresiones"]):
        print(f"    {b:<38} {a['clics']:>3}c {a['impresiones']:>5}i  pos={a['pos_media']}")

    # --- 13. Inspección de URLs clave (indexación) ---
    print("\n[13] Inspección de URLs clave")
    urls = [
        "https://passas.io/blog/responsable-del-despliegue-ai-act-obligaciones-2026",
        "https://passas.io/blog/exito-abogado-preventivo-etica",
        "https://passas.io/blog/la-consulta-juridica-gratuita-y-sus-consecuencias-reales-en-la-abogacia",
        "https://passas.io/en/servicios/commercial-litigation",
        "https://passas.io/en/team/guillermo-passas-varo",
        "https://passas.io/en",
        "https://passas.io/en/blog",
        "https://passas.io/servicios/techlaw-ai-act-compliance",
        "https://passas.io/honorarios",
    ]
    insp = {}
    for u in urls:
        try:
            r = s.post(INSPECT, json={"inspectionUrl": u, "siteUrl": SITE})
            r.raise_for_status()
            res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
            insp[u] = {
                "veredicto": res.get("verdict"),
                "cobertura": res.get("coverageState"),
                "ultimo_rastreo": res.get("lastCrawlTime"),
                "canonica_google": res.get("googleCanonical"),
                "canonica_declarada": res.get("userCanonical"),
                "robots": res.get("robotsTxtState"),
                "indexacion": res.get("indexingState"),
            }
            print(f"    {u.replace('https://passas.io','')}")
            print(f"        veredicto={insp[u]['veredicto']}  cobertura={insp[u]['cobertura']}")
            print(f"        canonica_google={insp[u]['canonica_google']}")
            print(f"        canonica_declarada={insp[u]['canonica_declarada']}")
        except Exception as e:
            insp[u] = {"error": str(e)}
            print(f"    {u}: ERROR {e}")
    OUT["inspeccion_urls"] = insp

    # --- 14. Sitemap ---
    print("\n[14] Sitemap")
    r = s.get(f"{GSC}/sites/{requests.utils.quote(SITE, safe='')}/sitemaps")
    r.raise_for_status()
    OUT["sitemaps"] = r.json()
    for sm in r.json().get("sitemap", []):
        print(f"    {sm.get('path')}  descargado={sm.get('lastDownloaded')}  "
              f"errores={sm.get('errors')}  avisos={sm.get('warnings')}")
        for c in sm.get("contents", []):
            print(f"        tipo={c.get('type')}  enviadas={c.get('submitted')}  "
                  f"indexadas={c.get('indexed')}")

    OUT["_meta"] = {
        "ejecutado": datetime.utcnow().isoformat() + "Z",
        "propiedad": SITE,
        "proposito": "Cotejo del informe 2026-08-24 y su respuesta contra GSC en vivo",
        "ultimo_dia_con_datos": ultimo,
    }

    fn = f"gsc_cotejo_{today.isoformat()}.json"
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(OUT, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Volcado en {fn}")


if __name__ == "__main__":
    main()
