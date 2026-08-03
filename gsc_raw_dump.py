"""
Volcado de DATOS BRUTOS de Google Search Console para sc-domain:passas.io.

No interpreta ni diagnostica: devuelve las respuestas JSON tal cual las
entrega la API, mas un indice de las llamadas realizadas.

Salida: JSON por stdout (o al fichero indicado como primer argumento).
"""

import json
import os
import sys
from datetime import date, timedelta

import requests
import urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES   = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC_API  = "https://www.googleapis.com/webmasters/v3"
SC_API   = "https://searchconsole.googleapis.com/v1"
SITE     = "sc-domain:passas.io"
SITE_ENC = requests.utils.quote(SITE, safe="")
INVENTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "webflow_sitemap_inventory.json")

TODAY = date.today()
def ago(n):
    return (TODAY - timedelta(days=n)).isoformat()


def session():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GSC_SERVICE_ACCOUNT_FILE"), scopes=SCOPES)
    s = AuthorizedSession(creds)
    s.verify = False
    return s, creds


def get(s, url):
    r = s.get(url)
    return {"http_status": r.status_code, "body": r.json()}


def post(s, url, body):
    r = s.post(url, json=body)
    return {"http_status": r.status_code, "request_body": body, "body": r.json()}


def query(s, start, end, dims, limit=1000, extra=None):
    body = {"startDate": start, "endDate": end,
            "dimensions": dims, "rowLimit": limit}
    if extra:
        body.update(extra)
    return post(s, f"{GSC_API}/sites/{SITE_ENC}/searchAnalytics/query", body)


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else None
    s, creds = session()

    dump = {
        "_meta": {
            "generado_utc": TODAY.isoformat(),
            "propiedad": SITE,
            "service_account": creds.service_account_email,
            "nota_latencia": "Search Console publica datos con 2-3 dias de retraso; "
                             "los rangos que llegan a hoy pueden estar incompletos.",
            "endpoints": [
                f"GET  {GSC_API}/sites",
                f"GET  {GSC_API}/sites/{{site}}/sitemaps",
                f"POST {GSC_API}/sites/{{site}}/searchAnalytics/query",
                f"POST {SC_API}/urlInspection/index:inspect",
            ],
        }
    }

    # ── 1. Propiedades y permisos ───────────────────────────────────────────
    dump["sites"] = get(s, f"{GSC_API}/sites")

    # ── 2. Sitemaps ─────────────────────────────────────────────────────────
    dump["sitemaps"] = get(s, f"{GSC_API}/sites/{SITE_ENC}/sitemaps")

    # ── 3. Search Analytics: series y desgloses ─────────────────────────────
    rangos = {
        "ultimos_7d":   (ago(7),   TODAY.isoformat()),
        "ultimos_28d":  (ago(28),  TODAY.isoformat()),
        "ultimos_90d":  (ago(90),  TODAY.isoformat()),
        "previo_28d":   (ago(56),  ago(28)),
        "previo_90d":   (ago(180), ago(90)),
    }
    dump["_meta"]["rangos"] = {k: {"startDate": v[0], "endDate": v[1]}
                               for k, v in rangos.items()}

    sa = {}
    for nombre, (ini, fin) in rangos.items():
        sa[nombre] = {
            "totales":   query(s, ini, fin, []),
            "por_fecha": query(s, ini, fin, ["date"]),
            "por_pagina": query(s, ini, fin, ["page"]),
            "por_query": query(s, ini, fin, ["query"]),
            "por_dispositivo": query(s, ini, fin, ["device"]),
            "por_pais":  query(s, ini, fin, ["country"]),
        }
    # Cruces solo en el rango largo (mas caros)
    ini90, fin90 = rangos["ultimos_90d"]
    sa["ultimos_90d"]["pagina_x_query"] = query(s, ini90, fin90, ["page", "query"])
    sa["ultimos_90d"]["por_search_appearance"] = query(s, ini90, fin90, ["searchAppearance"])
    sa["ultimos_90d"]["fecha_x_dispositivo"] = query(s, ini90, fin90, ["date", "device"])
    dump["search_analytics"] = sa

    # ── 4. Inspeccion de URL para todo el inventario del sitemap ────────────
    urls = []
    if os.path.exists(INVENTORY):
        with open(INVENTORY) as f:
            inv = json.load(f)
        base = inv["base_url"]
        for grupo in ("paginas_estaticas", "blog", "servicios", "team"):
            urls += [base + p for p in inv.get(grupo, [])]

    inspecciones = {}
    for u in urls:
        r = s.post(f"{SC_API}/urlInspection/index:inspect",
                   json={"inspectionUrl": u, "siteUrl": SITE})
        inspecciones[u] = {"http_status": r.status_code, "body": r.json()}
    dump["url_inspection"] = {
        "total_urls_inspeccionadas": len(inspecciones),
        "resultados": inspecciones,
    }

    texto = json.dumps(dump, indent=2, ensure_ascii=False)
    if out_path:
        with open(out_path, "w") as f:
            f.write(texto)
        print(f"Volcado escrito en {out_path} ({len(texto):,} caracteres)")
    else:
        print(texto)


if __name__ == "__main__":
    main()
