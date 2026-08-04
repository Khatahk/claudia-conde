"""
Informe de indexacion del locale EN (https://passas.io/en/...) -> XML plano.

Lee el volcado gsc_raw_en_<fecha>.json generado por la inspeccion de URLs y
lo cruza con datos de Search Analytics filtrados por /en/.
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from xml.dom import minidom

import requests
import urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SITE     = "sc-domain:passas.io"
SITE_ENC = requests.utils.quote(SITE, safe="")
GSC      = f"https://www.googleapis.com/webmasters/v3/sites/{SITE_ENC}"
TODAY    = date.today()
D90      = (TODAY - timedelta(days=90)).isoformat()

# Estado del locale segun la API de Webflow (data_sites_tool > get_site)
WEBFLOW_LOCALE = {
    "primary_tag": "es-ES", "primary_subdirectory": "", "primary_redirect": True,
    "secondary_tag": "en", "secondary_subdirectory": "en", "secondary_enabled": True,
    "locale_id": "6a633c9c710992687fac04e0",
    "cms_locale_id": "6a633c9c710992687fac04e5",
}


def sub(parent, tag, text=None, **attrs):
    el = ET.SubElement(parent, tag, **{k: str(v) for k, v in attrs.items()})
    if text is not None:
        el.text = str(text)
    return el


def session():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GSC_SERVICE_ACCOUNT_FILE"),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    s = AuthorizedSession(creds)
    s.verify = False
    return s


def query(s, dims, limit=100, filt="/en/"):
    body = {"startDate": D90, "endDate": TODAY.isoformat(),
            "dimensions": dims, "rowLimit": limit}
    if filt:
        body["dimensionFilterGroups"] = [{"filters": [
            {"dimension": "page", "operator": "contains", "expression": filt}]}]
    return s.post(f"{GSC}/searchAnalytics/query", json=body).json().get("rows", [])


def main():
    dump_path = sys.argv[1] if len(sys.argv) > 1 else \
        os.path.join(BASE_DIR, f"gsc_raw_en_{TODAY.isoformat()}.json")
    with open(dump_path) as f:
        dump = json.load(f)

    s = session()
    root = ET.Element("gsc_informe_locale_en", site="passas.io",
                      prefijo="/en", fecha=TODAY.isoformat())

    # ── CONFIGURACION DEL LOCALE EN WEBFLOW ─────────────────────────────────
    cfg = sub(root, "configuracion_webflow")
    sub(cfg, "locale_primario", WEBFLOW_LOCALE["primary_tag"],
        subdirectorio="(raiz)", redirect_automatico=WEBFLOW_LOCALE["primary_redirect"])
    sub(cfg, "locale_secundario", WEBFLOW_LOCALE["secondary_tag"],
        subdirectorio=WEBFLOW_LOCALE["secondary_subdirectory"],
        habilitado=WEBFLOW_LOCALE["secondary_enabled"])
    if WEBFLOW_LOCALE["primary_redirect"]:
        sub(cfg, "alerta",
            "El locale primario tiene redirect automatico por idioma de navegador. "
            "Es la causa probable del Redirect error en /en/.")

    # ── SITEMAP ─────────────────────────────────────────────────────────────
    sm = s.get(f"{GSC}/sitemaps").json().get("sitemap", [])
    sme = sub(root, "sitemap")
    for x in sm:
        enviadas = sum(int(c.get("submitted", 0)) for c in x.get("contents", []))
        sub(sme, "urls_totales_enviadas", enviadas)
        sub(sme, "ultima_descarga", x.get("lastDownloaded", "?"))
        sub(sme, "errores", x.get("errors", "0"))

    # ── ESTADO DE INDEXACION ────────────────────────────────────────────────
    res = dump["resultados"]
    idx = sub(root, "estado_indexacion", total_urls_en=len(res))

    por_estado = {}
    for u, r in res.items():
        st = r["body"].get("inspectionResult", {}).get("indexStatusResult", {})
        por_estado.setdefault(st.get("coverageState", "(sin dato)"), []).append((u, st))

    resumen = sub(idx, "resumen")
    for estado, lista in sorted(por_estado.items(), key=lambda x: -len(x[1])):
        sub(resumen, "estado", len(lista), nombre=estado)
    indexadas = len(por_estado.get("Submitted and indexed", []))
    sub(resumen, "porcentaje_indexado", f"{indexadas/len(res)*100:.1f}%")

    for estado, lista in sorted(por_estado.items(), key=lambda x: -len(x[1])):
        grupo = sub(idx, "grupo", estado=estado, total=len(lista))
        for u, st in sorted(lista):
            e = sub(grupo, "url", u.replace("https://passas.io", ""))
            e.set("rastreada", st.get("lastCrawlTime", "NUNCA"))
            if st.get("robotsTxtState", "").startswith("ROBOTS_TXT_STATE_UNSPEC"):
                e.set("nota", "sin rastrear todavia")

    # ── RENDIMIENTO /en ─────────────────────────────────────────────────────
    rend = sub(root, "rendimiento_en", periodo=f"{D90} a {TODAY.isoformat()}")
    fechas = query(s, ["date"], 200)
    activos = [r for r in fechas if r["impressions"] > 0]
    tot_impr = sum(r["impressions"] for r in fechas)
    tot_clic = sum(r["clicks"] for r in fechas)
    sub(rend, "impresiones_totales", tot_impr)
    sub(rend, "clics_totales", tot_clic)
    sub(rend, "dias_con_impresiones", len(activos))
    if activos:
        sub(rend, "primera_impresion", activos[0]["keys"][0])
        sub(rend, "ultima_impresion", activos[-1]["keys"][0])
    serie = sub(rend, "serie_diaria")
    for r in activos:
        sub(serie, "dia", fecha=r["keys"][0], impresiones=r["impressions"],
            clics=r["clicks"], posicion=f"{r['position']:.1f}")

    pgs = sub(rend, "paginas")
    for r in sorted(query(s, ["page"], 100), key=lambda x: -x["impressions"]):
        sub(pgs, "pagina", r["keys"][0].replace("https://passas.io", ""),
            impresiones=r["impressions"], clics=r["clicks"],
            posicion=f"{r['position']:.1f}")

    qs = sub(rend, "queries")
    for r in sorted(query(s, ["query"], 50), key=lambda x: -x["impressions"]):
        sub(qs, "query", r["keys"][0], impresiones=r["impressions"],
            clics=r["clicks"], posicion=f"{r['position']:.1f}")

    ps = sub(rend, "paises")
    for r in sorted(query(s, ["country"], 30), key=lambda x: -x["impressions"]):
        sub(ps, "pais", r["keys"][0], impresiones=r["impressions"],
            clics=r["clicks"], posicion=f"{r['position']:.1f}")

    # ── DIAGNOSTICO ─────────────────────────────────────────────────────────
    diag = sub(root, "diagnostico")
    problemas = []

    if any(st.get("coverageState") == "Redirect error"
           for _, sts in por_estado.items() for _, st in sts):
        problemas.append(("CRITICO", "home_en_redirect_error",
            "https://passas.io/en/ devuelve Redirect error. Es la pagina raiz del "
            "locale ingles: sin ella no consolida ni recibe el enlazado interno. "
            "Causa probable: el redirect automatico por idioma del locale primario."))

    sin_rastrear = [u for e, l in por_estado.items() for u, st in l
                    if st.get("lastCrawlTime") is None]
    if sin_rastrear:
        problemas.append(("ALTO", "urls_en_sin_rastrear",
            f"{len(sin_rastrear)} URLs EN nunca rastreadas por Google."))

    if tot_clic == 0 and tot_impr > 0:
        problemas.append(("ALTO", "cero_clics_en",
            f"{tot_impr} impresiones y 0 clics en /en. Titles y descriptions "
            "traducidos pero sin captar clic."))

    problemas.append(("INFO", "cobertura_blog_en",
        "Solo 1 de 19 entradas del blog tiene version EN. El blog es el motor "
        "de trafico en ES; sin traducirlo el locale EN no escala."))

    for sev, cod, txt in problemas:
        sub(diag, "problema", txt, severidad=sev, codigo=cod)

    xml = minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")
    out = os.path.join(BASE_DIR, f"informe_gsc_locale_en_{TODAY.isoformat()}.xml")
    with open(out, "w") as f:
        f.write(xml)
    print(xml)
    print(f"\n--> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
