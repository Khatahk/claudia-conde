"""Informe completo GSC → XML plano. Site: sc-domain:passas.io"""

import json, os, sys, warnings
from datetime import date, timedelta
import requests, urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import xml.etree.ElementTree as ET
from xml.dom import minidom

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES   = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC_API  = "https://www.googleapis.com/webmasters/v3"
SC_API   = "https://searchconsole.googleapis.com/v1"
SITE     = "sc-domain:passas.io"
SITE_ENC = requests.utils.quote(SITE, safe="")
TODAY    = date.today()
D90      = (TODAY - timedelta(days=90)).isoformat()
D60      = (TODAY - timedelta(days=60)).isoformat()
D30      = (TODAY - timedelta(days=30)).isoformat()
D16      = (TODAY - timedelta(days=16)).isoformat()
D7       = (TODAY - timedelta(days=7)).isoformat()
TODAY_S  = TODAY.isoformat()

# ── Auth ────────────────────────────────────────────────────────────────────
def get_session():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GSC_SERVICE_ACCOUNT_FILE"), scopes=SCOPES
    )
    s = AuthorizedSession(creds)
    s.verify = False
    return s, creds

# ── API helpers ──────────────────────────────────────────────────────────────
def gsc_get(s, path):
    r = s.get(f"{GSC_API}/{path}"); r.raise_for_status(); return r.json()

def gsc_post(s, path, body):
    r = s.post(f"{GSC_API}/{path}", json=body); r.raise_for_status(); return r.json()

def analytics(s, start, end, dims, limit=100, filters=None):
    body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": limit}
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    return gsc_post(s, f"sites/{SITE_ENC}/searchAnalytics/query", body).get("rows", [])

def inspect(s, url):
    try:
        r = s.post(f"{SC_API}/urlInspection/index:inspect",
                   json={"inspectionUrl": url, "siteUrl": SITE})
        r.raise_for_status()
        return r.json().get("inspectionResult", {})
    except Exception as e:
        return {"_error": str(e)}

# ── XML helpers ──────────────────────────────────────────────────────────────
def sub(parent, tag, text=None, **attrs):
    el = ET.SubElement(parent, tag, **{k: str(v) for k, v in attrs.items()})
    if text is not None:
        el.text = str(text)
    return el

def pretty(root):
    raw = ET.tostring(root, encoding="unicode")
    return minidom.parseString(raw).toprettyxml(indent="  ", encoding=None)

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    # 1. Conexión
    try:
        session, creds = get_session()
        sites_data = gsc_get(session, "sites")
        sites = sites_data.get("siteEntry", [])
        conn_ok = any(s["siteUrl"] == SITE for s in sites)
    except Exception as e:
        print(f"ERROR_CONEXION: {e}", file=sys.stderr)
        sys.exit(1)

    root = ET.Element("gsc_informe",
                      site="passas.io",
                      fecha=TODAY_S,
                      service_account=creds.service_account_email)

    # ── CONEXION ────────────────────────────────────────────────────────────
    c = sub(root, "conexion")
    sub(c, "estado", "OK" if conn_ok else "SIN_ACCESO")
    sub(c, "permiso", next((s.get("permissionLevel","?") for s in sites if s["siteUrl"]==SITE), "?"))
    sub(c, "sitios_verificados", len(sites))

    if not conn_ok:
        print(pretty(root)); return

    # ── SITEMAPS ────────────────────────────────────────────────────────────
    sm_data = gsc_get(session, f"sites/{SITE_ENC}/sitemaps").get("sitemap", [])
    sms = sub(root, "sitemaps", total=len(sm_data))
    for sm in sm_data:
        contents = sm.get("contents", [])
        submitted = next((c.get("count",0) for c in contents if c.get("type")=="submitted"), 0)
        indexed   = next((c.get("count",0) for c in contents if c.get("type")=="indexed"), 0)
        errors    = next((c.get("count",0) for c in contents if c.get("type")=="indexedError"), 0)
        warns     = next((c.get("count",0) for c in contents if c.get("type")=="indexedWarning"), 0)
        s_el = sub(sms, "sitemap",
                   url=sm.get("path","?"),
                   ultima_descarga=sm.get("lastDownloaded","?"),
                   es_indice=str(sm.get("isSitemapsIndex",False)))
        sub(s_el, "paginas_enviadas", submitted)
        sub(s_el, "paginas_indexadas", indexed)
        sub(s_el, "errores", errors)
        sub(s_el, "avisos", warns)
        tasa = f"{indexed/submitted*100:.1f}%" if submitted else "N/A"
        sub(s_el, "tasa_indexacion", tasa)
        if submitted == 0:
            sub(s_el, "alerta", "CRITICO: sitemap sin URLs enviadas")

    # ── RENDIMIENTO 90d ─────────────────────────────────────────────────────
    rows90 = analytics(session, D90, TODAY_S, ["date"], limit=90)
    rows30 = [r for r in rows90 if r["keys"][0] >= D30]
    rows_prev30 = [r for r in rows90 if D60 <= r["keys"][0] < D30]

    def totals(rows):
        clics = sum(r["clicks"] for r in rows)
        impr  = sum(r["impressions"] for r in rows)
        ctr   = clics/impr*100 if impr else 0
        pos   = sum(r["position"] for r in rows)/len(rows) if rows else 0
        return clics, impr, ctr, pos

    c90, i90, ctr90, pos90 = totals(rows90)
    c30, i30, ctr30, pos30 = totals(rows30)
    cp,  ip,  _,     _     = totals(rows_prev30)

    rend = sub(root, "rendimiento")

    p90 = sub(rend, "periodo_90_dias", desde=D90, hasta=TODAY_S)
    sub(p90, "clics_totales", c90)
    sub(p90, "impresiones_totales", i90)
    sub(p90, "ctr_medio", f"{ctr90:.2f}%")
    sub(p90, "posicion_media", f"{pos90:.1f}")

    p30 = sub(rend, "periodo_30_dias", desde=D30, hasta=TODAY_S)
    sub(p30, "clics", c30)
    sub(p30, "impresiones", i30)
    sub(p30, "ctr_medio", f"{ctr30:.2f}%")
    sub(p30, "posicion_media", f"{pos30:.1f}")

    tend = sub(rend, "tendencia_30_vs_30_anterior")
    sub(tend, "variacion_clics",
        f"{(c30-cp)/cp*100:+.1f}%" if cp else "N/A",
        actual=c30, anterior=cp)
    sub(tend, "variacion_impresiones",
        f"{(i30-ip)/ip*100:+.1f}%" if ip else "N/A",
        actual=i30, anterior=ip)

    # ── TOP PÁGINAS 30d ─────────────────────────────────────────────────────
    pages = analytics(session, D30, TODAY_S, ["page"], limit=25)
    tp = sub(rend, "top_paginas_30_dias", total=len(pages))
    for p in pages:
        pe = sub(tp, "pagina",
                 clics=p["clicks"],
                 impresiones=p["impressions"],
                 ctr=f"{p['ctr']*100:.1f}%",
                 posicion=f"{p['position']:.1f}")
        pe.text = p["keys"][0]
        if p["impressions"] > 50 and p["clicks"] == 0:
            pe.set("alerta", "alto_impresion_cero_clics")
        if p["position"] > 30:
            pe.set("alerta", "posicion_muy_baja")

    # ── TOP QUERIES 30d ─────────────────────────────────────────────────────
    queries = analytics(session, D30, TODAY_S, ["query"], limit=25)
    tq = sub(rend, "top_queries_30_dias", total=len(queries))
    for q in queries:
        qe = sub(tq, "query",
                 clics=q["clicks"],
                 impresiones=q["impressions"],
                 ctr=f"{q['ctr']*100:.1f}%",
                 posicion=f"{q['position']:.1f}")
        qe.text = q["keys"][0]

    # ── QUERIES PÁGINA 2 (oportunidades) ────────────────────────────────────
    all_q = analytics(session, D30, TODAY_S, ["query"], limit=100)
    pag2  = [q for q in all_q if 11 <= q["position"] <= 20 and q["impressions"] >= 5]
    pag2.sort(key=lambda x: x["impressions"], reverse=True)
    op = sub(rend, "oportunidades_pagina2", total=len(pag2))
    for q in pag2[:15]:
        qe = sub(op, "query",
                 impresiones=q["impressions"],
                 clics=q["clicks"],
                 posicion=f"{q['position']:.1f}")
        qe.text = q["keys"][0]

    # ── DISPOSITIVOS ─────────────────────────────────────────────────────────
    devs = analytics(session, D30, TODAY_S, ["device"])
    dv = sub(rend, "desglose_dispositivo_30_dias")
    for d in devs:
        sub(dv, d["keys"][0].lower(),
            clics=d["clicks"],
            impresiones=d["impressions"],
            ctr=f"{d['ctr']*100:.1f}%",
            posicion=f"{d['position']:.1f}")

    # ── PAÍSES ───────────────────────────────────────────────────────────────
    countries = analytics(session, D30, TODAY_S, ["country"], limit=10)
    cv = sub(rend, "top_paises_30_dias")
    for co in countries:
        sub(cv, "pais",
            codigo=co["keys"][0],
            clics=co["clicks"],
            impresiones=co["impressions"],
            posicion=f"{co['position']:.1f}")

    # ── INSPECCIÓN URLs ──────────────────────────────────────────────────────
    urls_inspect = ["https://passas.io/"]
    for p in pages[:6]:
        u = p["keys"][0]
        if u not in urls_inspect:
            urls_inspect.append(u)

    insp_el = sub(root, "inspeccion_urls", total=len(urls_inspect))
    for url in urls_inspect:
        res = inspect(session, url)
        if "_error" in res:
            uel = sub(insp_el, "url", estado="ERROR", href=url)
            sub(uel, "detalle", res["_error"])
            continue
        idx  = res.get("indexStatusResult", {})
        mob  = res.get("mobileUsabilityResult", {})
        verdict  = idx.get("verdict", "?")
        coverage = idx.get("coverageState", "?")
        robots   = idx.get("robotsTxtState", "?")
        idx_st   = idx.get("indexingState", "?")
        crawled  = idx.get("lastCrawlTime", "sin_rastreo")
        as_agent = idx.get("crawledAs", "?")
        canonical= idx.get("googleCanonical", url)
        mob_v    = mob.get("verdict", "?")

        uel = sub(insp_el, "url", estado=verdict, href=url)
        sub(uel, "cobertura", coverage)
        sub(uel, "robots_txt", robots)
        sub(uel, "estado_indexacion", idx_st)
        sub(uel, "ultimo_rastreo", crawled)
        sub(uel, "rastreado_como", as_agent)
        sub(uel, "canonical_google", canonical)
        sub(uel, "usabilidad_movil", mob_v)
        if mob.get("issues"):
            mi = sub(uel, "problemas_movil")
            for issue in mob["issues"]:
                sub(mi, "problema",
                    tipo=issue.get("issueType","?"),
                    mensaje=issue.get("message",""))
        if canonical.rstrip("/") != url.rstrip("/"):
            sub(uel, "alerta", "canonical_difiere_de_url")

    # ── DIAGNÓSTICO CONSOLIDADO ──────────────────────────────────────────────
    diag = sub(root, "diagnostico")

    problems = []
    if sm_data and sm_data[0].get("contents"):
        sub_count = next((c.get("count",0) for c in sm_data[0].get("contents",[])
                          if c.get("type")=="submitted"), 0)
        if sub_count == 0:
            problems.append(("CRITICO", "sitemap_vacio",
                "El sitemap.xml registra 0 URLs enviadas en GSC. "
                "Verificar Webflow Project Settings > SEO > Sitemap habilitado y que "
                "ninguna página tenga 'Exclude from sitemap' activado."))

    if c90 < 100:
        problems.append(("ALTO", "trafico_organico_muy_bajo",
            f"Solo {c90} clics orgánicos en 90 días. El sitio tiene visibilidad mínima. "
            "Priorizar producción de contenido y link building."))

    brand_q = next((q for q in all_q if "passas" in q["keys"][0].lower()), None)
    if brand_q and brand_q["ctr"] < 0.10 and brand_q["position"] < 5:
        problems.append(("ALTO", "ctr_marca_bajo",
            f"Query de marca 'passas' en pos {brand_q['position']:.1f} con CTR "
            f"{brand_q['ctr']*100:.1f}%. Optimizar meta title y description de la homepage."))

    zero_click_pages = [p for p in pages if p["impressions"] > 30 and p["clicks"] == 0]
    if zero_click_pages:
        problems.append(("MEDIO", "paginas_sin_clics_con_impresiones",
            f"{len(zero_click_pages)} página(s) con >30 impresiones y 0 clics. "
            "Revisar y mejorar meta descriptions en Webflow CMS."))

    deep_pages = [p for p in pages if p["position"] > 30]
    if deep_pages:
        problems.append(("MEDIO", "paginas_posicion_profunda",
            f"{len(deep_pages)} página(s) en posición >30. "
            "Revisar calidad de contenido y enlazado interno."))

    if pag2:
        problems.append(("OPORTUNIDAD", "queries_pagina2",
            f"{len(pag2)} queries entre posición 11-20 con potencial de pasar a pág 1. "
            "Optimizar contenido y CTR para estas búsquedas."))

    if c30 > cp * 1.5:
        problems.append(("INFO", "tendencia_positiva",
            f"Crecimiento del {(c30-cp)/cp*100:.0f}% en clics (últ. 30 vs 30 anteriores). "
            "Mantener ritmo de publicación de contenido."))

    for sev, code, desc in problems:
        sub(diag, "problema", severidad=sev, codigo=code).text = desc

    print(pretty(root))

if __name__ == "__main__":
    main()
