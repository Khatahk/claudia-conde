#!/usr/bin/env python3
"""
Cotejo de las afirmaciones cuantitativas de la RESPUESTA al informe
(respuestainformegsc 2026-08-24) contra GSC en vivo.
"""

import json
import os

import requests
import urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC = "https://www.googleapis.com/webmasters/v3"
SITE = "sc-domain:passas.io"
W = ("2026-08-03", "2026-08-24")

OUT = {}


def q(s, dims, row_limit=1000, filters=None):
    url = f"{GSC}/sites/{requests.utils.quote(SITE, safe='')}/searchAnalytics/query"
    body = {"startDate": W[0], "endDate": W[1], "rowLimit": row_limit, "dimensions": dims}
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    r = s.post(url, json=body)
    r.raise_for_status()
    return r.json().get("rows", [])


def main():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GSC_SERVICE_ACCOUNT_FILE"), scopes=SCOPES)
    s = AuthorizedSession(creds)
    s.verify = False

    pages = q(s, ["page"])
    P = {r["keys"][0].replace("https://passas.io", ""): r for r in pages}

    print("=" * 78)
    print("COTEJO DE LA RESPUESTA AL INFORME (afirmaciones cuantitativas)")
    print("=" * 78)

    # --- 3.1 Cluster contencioso: "1.064 impresiones y 7 clics en posiciones 7 a 9" ---
    print("\n[R-3.1] Cluster contencioso: respuesta afirma 1.064 impr / 7 clics / pos 7-9")
    cl = ["/servicios/litigacion-juicio-administrativo",
          "/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026"]
    ci = sum(P[p]["impressions"] for p in cl if p in P)
    cc = sum(P[p]["clicks"] for p in cl if p in P)
    print(f"         GSC hoy: {ci} impresiones, {cc} clics")
    for p in cl:
        if p in P:
            print(f"           {P[p]['clicks']}c {P[p]['impressions']}i  "
                  f"pos={P[p]['position']:.1f}  {p}")
    OUT["cluster_contencioso"] = {"impresiones": ci, "clics": cc,
                                  "afirmado_respuesta": {"impresiones": 1064, "clics": 7}}

    # --- 3.1: "~350 impresiones por ventana de intención de precio" ---
    print("\n[R-3.1b] Intención de precio en el cluster: respuesta/informe afirman ~350 impr")
    queries = q(s, ["query"])
    precio_kw = ("cuanto cuesta", "cuánto cuesta", "precio", "honorarios", "coste", "tarifa",
                 "arancel", "cuanto vale", "cuánto vale", "cuanto cobra", "cuánto cobra")
    conten = [r for r in queries
              if any(k in r["keys"][0].lower() for k in precio_kw)
              and ("contencioso" in r["keys"][0].lower() or "alzada" in r["keys"][0].lower())]
    ti = sum(r["impressions"] for r in conten)
    tc = sum(r["clicks"] for r in conten)
    print(f"         GSC hoy: {ti} impresiones, {tc} clics en {len(conten)} consultas")
    for r in sorted(conten, key=lambda x: -x["impressions"])[:10]:
        print(f"           {r['impressions']:>3}i pos={r['position']:>5.1f}  {r['keys'][0]}")
    OUT["intencion_precio_contencioso"] = {"impresiones": ti, "clics": tc,
                                           "consultas": len(conten), "afirmado": 350}

    # --- 3.3 Reparto por bloque: "De las 20 páginas de servicio, solo una produjo clics" ---
    print("\n[R-3.3] «De las 20 páginas de servicio, solo una produjo clics en la ventana»")
    serv = {p: r for p, r in P.items() if p.startswith("/servicios/") or
            (p.startswith("/en/servicios/"))}
    con_clics = {p: r for p, r in serv.items() if r["clicks"] > 0}
    print(f"         Páginas de servicio con impresiones: {len(serv)}")
    print(f"         Páginas de servicio con clics: {len(con_clics)}")
    for p, r in con_clics.items():
        print(f"           {r['clicks']}c {r['impressions']}i  {p}")
    OUT["paginas_servicio"] = {"con_impresiones": len(serv), "con_clics": len(con_clics),
                               "detalle_con_clics": {p: r["clicks"] for p, r in con_clics.items()}}

    # --- 3.3: "el móvil aporta 25 de los 35 clics totales" ---
    print("\n[R-3.3b] «el móvil aporta 25 de los 35 clics totales»")
    dev = q(s, ["device"])
    for r in dev:
        print(f"         {r['keys'][0]:<8} {r['clicks']}c {r['impressions']}i")
    OUT["dispositivo"] = {r["keys"][0]: {"clics": r["clicks"], "impresiones": r["impressions"]}
                          for r in dev}

    # --- 3.5 Due diligence tech: "pasó de 17 a 53 impresiones"; consulta en pos 9,1 ---
    print("\n[R-3.5] Due diligence tech: respuesta afirma 17 -> 53 impr; "
          "«due diligence legal ronda inversión startup» pos 9,1 / 17 impr")
    dd = P.get("/servicios/internacional-due-diligence-tech")
    if dd:
        print(f"         GSC hoy /servicios/internacional-due-diligence-tech: "
              f"{dd['clicks']}c {dd['impressions']}i pos={dd['position']:.1f}")
    ddq = [r for r in queries if "due diligence" in r["keys"][0].lower()]
    for r in sorted(ddq, key=lambda x: -x["impressions"]):
        print(f"           {r['impressions']:>3}i pos={r['position']:>5.1f}  {r['keys'][0]}")
    OUT["due_diligence"] = {"pagina": {"impresiones": dd["impressions"],
                                       "pos": round(dd["position"], 1)} if dd else None,
                            "consultas": [{"q": r["keys"][0], "impr": r["impressions"],
                                           "pos": round(r["position"], 1)} for r in ddq]}

    # --- 3.6 Marca: "124 impresiones y 2 clics, 3,6% de las impresiones" ---
    print("\n[R-3.6] Marca: respuesta afirma 124 impr / 2 clics / 3,6% de impresiones del sitio")
    bq = [r for r in queries if "passa" in r["keys"][0].lower()]
    bi = sum(r["impressions"] for r in bq)
    bc = sum(r["clicks"] for r in bq)
    tot_impr = sum(r["impressions"] for r in pages)
    print(f"         GSC hoy: {bi} impresiones, {bc} clics "
          f"({bi/tot_impr*100:.1f}% de {tot_impr} impresiones de páginas)")
    OUT["marca"] = {"impresiones": bi, "clics": bc, "pct": round(bi / tot_impr * 100, 1)}

    # --- 3.4 Asimetría ES/EN AI Act ---
    print("\n[R-3.4] Asimetría ES/EN AI Act: respuesta afirma ES pos 29,0 vs EN pos 7,4-7,7")
    for p in ["/servicios/techlaw-ai-act-compliance", "/en/servicios/ai-act-compliance",
              "/en/servicios/ai-act-high-risk"]:
        if p in P:
            print(f"         pos={P[p]['position']:>5.1f}  {P[p]['impressions']:>4}i  {p}")
    OUT["asimetria"] = {p: {"pos": round(P[p]["position"], 1), "impr": P[p]["impressions"]}
                        for p in ["/servicios/techlaw-ai-act-compliance",
                                  "/en/servicios/ai-act-compliance",
                                  "/en/servicios/ai-act-high-risk"] if p in P}

    # --- 2.6 Enlazado: el artículo no indexado ---
    print("\n[R-2.6] responsable-del-despliegue-ai-act-obligaciones-2026: "
          "¿tiene impresiones en la ventana?")
    rd = {p: r for p, r in P.items() if "responsable-del-despliegue" in p}
    print(f"         URLs con ese slug e impresiones: {len(rd)}")
    for p, r in rd.items():
        print(f"           {r['clicks']}c {r['impressions']}i  {p}")
    OUT["responsable_despliegue"] = {p: r["impressions"] for p, r in rd.items()}

    with open("gsc_check_respuesta_2026-08-25.json", "w", encoding="utf-8") as f:
        json.dump(OUT, f, ensure_ascii=False, indent=2)
    print("\n[OK] Volcado en gsc_check_respuesta_2026-08-25.json")


if __name__ == "__main__":
    main()
