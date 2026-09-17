"""Auditoría completa de GSC para sc-domain:passas.io.

Extrae en una sola pasada todo lo necesario para auditar las dos dimensiones
del sitio y vuelca un JSON con los datos brutos:

  1. Técnica   -> URL Inspection API sobre todas las URLs con impresiones:
                  estado de cobertura, canónica declarada vs. elegida por
                  Google, robots.txt, último rastreo y sitemaps referenciantes.
  2. Contenido -> Search Analytics API por fecha, consulta, página, país,
                  dispositivo y sus cruces, con ventanas de 28/90/480 días.

Uso:
    python gsc_auditoria_completa.py [--dias-fin 2]

La opción --dias-fin marca el desfase de datos de GSC (por defecto 2 días).
"""

import argparse
import json
import os
import sys
import time
from datetime import date, timedelta

import urllib3
from dotenv import load_dotenv
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC_API = "https://www.googleapis.com/webmasters/v3"
SC_API = "https://searchconsole.googleapis.com/v1"
SITE = "sc-domain:passas.io"
ROW_LIMIT = 25000


def get_session():
    ruta = os.getenv("GSC_SERVICE_ACCOUNT_FILE")
    if not ruta or not os.path.exists(ruta):
        sys.exit("Falta GSC_SERVICE_ACCOUNT_FILE (ver .env.example)")
    creds = service_account.Credentials.from_service_account_file(ruta, scopes=SCOPES)
    s = AuthorizedSession(creds)
    s.verify = False
    return s


def search_analytics(session, inicio, fin, dimensiones):
    """Consulta Search Analytics paginando hasta agotar las filas."""
    filas, start_row = [], 0
    while True:
        cuerpo = {
            "startDate": inicio,
            "endDate": fin,
            "dimensions": dimensiones,
            "rowLimit": ROW_LIMIT,
            "startRow": start_row,
            "type": "web",
        }
        r = session.post(
            f"{GSC_API}/sites/{SITE.replace(':', '%3A')}/searchAnalytics/query",
            json=cuerpo,
        )
        r.raise_for_status()
        lote = r.json().get("rows", [])
        filas += lote
        if len(lote) < ROW_LIMIT:
            return filas
        start_row += ROW_LIMIT


def inspeccionar(session, url, reintentos=4):
    """URL Inspection API con reintento exponencial ante 429/5xx."""
    for intento in range(reintentos):
        r = session.post(
            f"{SC_API}/urlInspection/index:inspect",
            json={"inspectionUrl": url, "siteUrl": SITE, "languageCode": "es"},
        )
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 503):
            time.sleep(2**intento)
            continue
        return {"error": f"{r.status_code}: {r.text[:200]}"}
    return {"error": "agotados los reintentos"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias-fin", type=int, default=2)
    ap.add_argument("--sin-inspeccion", action="store_true",
                    help="omite la URL Inspection API (más rápido)")
    args = ap.parse_args()

    s = get_session()
    hoy = date.today()
    fin = (hoy - timedelta(days=args.dias_fin)).isoformat()

    def desde(dias):
        return (hoy - timedelta(days=dias)).isoformat()

    ventanas = {
        "fecha_historico": (desde(480), fin, ["date"]),
        "consulta_90d": (desde(92), fin, ["query"]),
        "pagina_90d": (desde(92), fin, ["page"]),
        "consulta_28d": (desde(30), fin, ["query"]),
        "pagina_28d": (desde(30), fin, ["page"]),
        "consulta_28d_previos": (desde(58), desde(31), ["query"]),
        "pagina_28d_previos": (desde(58), desde(31), ["page"]),
        "pais_90d": (desde(92), fin, ["country"]),
        "dispositivo_90d": (desde(92), fin, ["device"]),
        "pagina_consulta_90d": (desde(92), fin, ["page", "query"]),
        "fecha_pagina_90d": (desde(92), fin, ["date", "page"]),
        "pagina_historico": (desde(480), fin, ["page"]),
    }

    salida = {"sitio": SITE, "generado": hoy.isoformat(), "search_analytics": {}}

    for nombre, (ini, f, dims) in ventanas.items():
        filas = search_analytics(s, ini, f, dims)
        salida["search_analytics"][nombre] = {
            "inicio": ini, "fin": f, "dimensiones": dims, "filas": filas
        }
        print(f"{nombre:<24} {ini} → {f}  {len(filas)} filas", flush=True)

    r = s.get(f"{GSC_API}/sites/{SITE.replace(':', '%3A')}/sitemaps")
    r.raise_for_status()
    salida["sitemaps"] = r.json()
    print(f"sitemaps                 {len(salida['sitemaps'].get('sitemap', []))}")

    if not args.sin_inspeccion:
        urls = sorted(
            {f["keys"][0]
             for f in salida["search_analytics"]["pagina_historico"]["filas"]}
        )
        salida["inspeccion"] = {}
        for i, url in enumerate(urls, 1):
            salida["inspeccion"][url] = inspeccionar(s, url)
            if i % 20 == 0:
                print(f"  inspeccionadas {i}/{len(urls)}", flush=True)
        print(f"inspeccion               {len(salida['inspeccion'])} URLs")

    destino = f"gsc_raw_auditoria_{hoy.isoformat()}.json"
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False)
    print(f"\nVolcado en {destino}")


if __name__ == "__main__":
    main()
