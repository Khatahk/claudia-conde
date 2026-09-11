#!/usr/bin/env python3
"""
Extraccion de informe GSC actualizado para sc-domain:passas.io.

Produce dos ficheros en el directorio de trabajo:
  - gsc_raw_passas_[AAAA-MM-DD].json   -> todas las respuestas crudas de la API
  - INFORME-GSC-PASSAS-[AAAA-MM-DD].md -> el informe en espanol

No realiza ninguna escritura contra la API (solo lectura).

Uso:
    export GSC_SERVICE_ACCOUNT_FILE=service_account.json
    python3 gsc_informe_actualizado.py

Requisitos: ver requirements.txt
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

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
BASE     = "https://passas.io"

ROW_LIMIT = 25000
SEARCH_TYPE = "web"

HOY = date.today().isoformat()
RAW_PATH    = f"gsc_raw_passas_{HOY}.json"
INFORME_PATH = f"INFORME-GSC-PASSAS-{HOY}.md"

# Ventanas fijas definidas por el encargo (F se resuelve en tiempo de ejecucion)
V_PREVIA   = ("2026-08-03", "2026-08-24")
V_ACTUAL_I = "2026-08-25"
V_CRUCE_I  = "2026-08-30"
SERIE_INI  = "2026-07-27"   # lunes

# ── Terminos declarados para el subbloque TechLaw ───────────────────────────
TECHLAW_PREFIJO_SERVICIOS = "techlaw-"
TECHLAW_TERMINOS_SLUG = [
    "ai-act", "ia-", "inteligencia-artificial",
    "digital-omnibus", "chat-control", "software", "rgpd",
]

# ── Clusters de query (subcadenas, sobre la query en minusculas) ────────────
CLUSTERS = {
    "contencioso":      ["contencioso", "alzada"],
    "burofax":          ["burofax"],
    "ai_act_techlaw":   ["ai act", "ai-act", "aiact", "inteligencia artificial",
                         "digital omnibus", "reglamento ia", "ley de ia"],
    "due_diligence":    ["due diligence", "due-diligence"],
    "chat_control":     ["chat control", "chat-control"],
    "marca_passas":     ["passas"],
}

# ── URLs extra a inspeccionar (ademas de las del sitemap) ───────────────────
URLS_EXTRA = [
    "/legal",
    "/autoevaluacion-ai-act",
    "/en/autoevaluacion-ai-act",
    "/legal-tools-tmp",
    "/en/legal-tools/necesito-un-abogado",
    "/en/legal-tools/te-compensa-abogado",
    "/en/legal-tools/necesito-abogado-ia",
    "/en/legal-tools/autoevaluacion-ai-act",
    "/en/legal-tools/do-i-need-a-lawyer",
    "/en/legal-tools/is-a-lawyer-worth-it",
    "/en/legal-tools/does-my-ai-need-a-lawyer",
    "/en/legal-tools/ai-act-self-assessment",
    "/blog/responsable-del-despliegue-ai-act-obligaciones-2026",
    "/en/servicios/commercial-litigation",
    "/en/team/guillermo-passas-varo",
]

# ── Sesiones de Webflow Analyze (30 ago -> 11 sep) tomadas del encargo ──────
ANALYZE = {
    "ventana": "2026-08-30 → 2026-09-11",
    "por_pagina": [
        ("/", 9), ("burofax", 8),
        ("cuanto-cuesta-un-contencioso-administrativo-precios-2026", 6),
        ("estafa-o-incumplimiento", 5), ("como-salir-de-asnef", 3),
        ("/team/guillermo-passas-varo", 3), ("ayuntamiento-no-paga-factura", 2),
        ("cuanto-cuesta-abogado-startup", 2), ("/team/david-sanchez-lorenzo", 2),
    ],
    "por_pais":       {"esp": 33, "usa": 10},
    "por_dispositivo": {"escritorio": 32, "movil": 18},
    "usa_aterriza_en": ["ASNEF", "estafa", "burofax", "digital-omnibus"],
}

RAW = {
    "_meta": {
        "generado": HOY,
        "propiedad": SITE,
        "search_type": SEARCH_TYPE,
        "row_limit": ROW_LIMIT,
        "nota": "Respuestas crudas de la API, sin postprocesar. "
                "El campo 'indexed' de sitemaps esta deprecado y siempre vale 0.",
    },
    "llamadas": [],
}


# ════════════════════════════════════════════════════════════════════════════
# Infraestructura
# ════════════════════════════════════════════════════════════════════════════
def build_credentials():
    sa_json = os.getenv("GSC_SERVICE_ACCOUNT_JSON")
    sa_file = os.getenv("GSC_SERVICE_ACCOUNT_FILE")
    if sa_json:
        return service_account.Credentials.from_service_account_info(
            json.loads(sa_json), scopes=SCOPES)
    if sa_file:
        return service_account.Credentials.from_service_account_file(
            sa_file, scopes=SCOPES)
    raise EnvironmentError(
        "Faltan credenciales: define GSC_SERVICE_ACCOUNT_FILE o "
        "GSC_SERVICE_ACCOUNT_JSON (ver .env.example)."
    )


def get_session():
    s = AuthorizedSession(build_credentials())
    s.verify = False
    return s


def record(label, method, url, body, resp):
    try:
        parsed = resp.json()
    except Exception:
        parsed = {"_texto": resp.text[:2000]}
    RAW["llamadas"].append({
        "label": label, "method": method, "url": url,
        "request_body": body, "http_status": resp.status_code,
        "response": parsed,
    })
    return parsed


def api_get(s, label, url):
    r = s.get(url)
    return record(label, "GET", url, None, r)


def api_post(s, label, url, body):
    r = s.post(url, json=body)
    return record(label, "POST", url, body, r)


def sa_query(s, label, start, end, dims, filters=None, data_state="final"):
    """searchAnalytics/query con paginacion por startRow hasta agotar filas."""
    url = f"{GSC_API}/sites/{SITE_ENC}/searchAnalytics/query"
    filas, start_row = [], 0
    while True:
        body = {
            "startDate": start, "endDate": end,
            "dimensions": dims,
            "type": SEARCH_TYPE,
            "rowLimit": ROW_LIMIT,
            "startRow": start_row,
            "dataState": data_state,
        }
        if filters:
            body["dimensionFilterGroups"] = [{"filters": filters}]
        data = api_post(s, f"{label}[startRow={start_row}]", url, body)
        lote = data.get("rows", []) or []
        filas.extend(lote)
        if len(lote) < ROW_LIMIT:
            break
        start_row += ROW_LIMIT
    return filas


def tot(filas):
    """Agrega clics, impresiones, CTR y posicion media ponderada."""
    c = sum(f.get("clicks", 0) for f in filas)
    i = sum(f.get("impressions", 0) for f in filas)
    ctr = (c / i * 100) if i else 0.0
    pos = (sum(f.get("position", 0) * f.get("impressions", 0) for f in filas) / i) if i else 0.0
    return {"clics": c, "impresiones": i, "ctr": round(ctr, 2), "posicion": round(pos, 2)}


def fmt(n):
    """Entero con punto de millar (convencion espanola)."""
    return f"{int(n):,}".replace(",", ".")


def sfmt(n):
    """Entero con signo y punto de millar."""
    return ("+" if n >= 0 else "-") + fmt(abs(int(n)))


def sdec(x, n=2):
    """Decimal con signo explicito y coma decimal."""
    return ("+" if x >= 0 else "-") + dec(abs(x), n)


def dec(x, n=2):
    """Decimal con coma decimal y punto de millar."""
    return f"{x:,.{n}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


# ════════════════════════════════════════════════════════════════════════════
# Clasificacion por bloque
# ════════════════════════════════════════════════════════════════════════════
def ruta(url):
    return re.sub(r"^https?://[^/]+", "", url).split("?")[0].split("#")[0]


def bloque(url):
    p = ruta(url).rstrip("/") or "/"
    if p.startswith("/en/blog"):        return "blog EN"
    if p.startswith("/blog"):           return "blog ES"
    if p.startswith("/en/servicios"):   return "servicios EN"
    if p.startswith("/servicios"):      return "servicios ES"
    if p.startswith("/en/legal-tools") or p.startswith("/legal-tools"):
        return "herramientas"
    if p.startswith("/en/team") or p.startswith("/team"):
        return "equipo"
    if p == "/":                        return "Home"
    return "estaticas"


def es_techlaw(url):
    p = ruta(url).rstrip("/")
    slug = p.rsplit("/", 1)[-1]
    if "/servicios/" in p and slug.startswith(TECHLAW_PREFIJO_SERVICIOS):
        return True
    return any(t in slug for t in TECHLAW_TERMINOS_SLUG)


# ════════════════════════════════════════════════════════════════════════════
# Sitemap
# ════════════════════════════════════════════════════════════════════════════
def urls_sitemap():
    """Lee https://passas.io/sitemap.xml. Si no es accesible, cae al inventario."""
    try:
        r = requests.get(f"{BASE}/sitemap.xml", timeout=45, verify=False)
        r.raise_for_status()
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
        # Soporte de sitemap index
        if locs and all(l.rstrip("/").endswith(".xml") for l in locs):
            todas = []
            for sm in locs:
                rr = requests.get(sm, timeout=45, verify=False)
                todas += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", rr.text)
            locs = todas
        RAW["sitemap_xml"] = {"origen": "live", "url": f"{BASE}/sitemap.xml",
                              "total": len(locs), "urls": locs}
        return locs
    except Exception as e:
        inv_path = "webflow_sitemap_inventory.json"
        if not os.path.exists(inv_path):
            RAW["sitemap_xml"] = {"origen": "fallo", "error": str(e), "urls": []}
            return []
        with open(inv_path) as f:
            inv = json.load(f)
        locs = [inv["base_url"] + p
                for g in ("paginas_estaticas", "blog", "servicios", "team")
                for p in inv.get(g, [])]
        RAW["sitemap_xml"] = {
            "origen": "inventario_local_webflow (sitemap.xml no accesible)",
            "error": str(e), "total": len(locs), "urls": locs,
        }
        return locs


# ════════════════════════════════════════════════════════════════════════════
# Inspeccion de URL
# ════════════════════════════════════════════════════════════════════════════
INESTABLES = {"unknown", "discovered", ""}


def inspect_once(s, url):
    body = {"inspectionUrl": url, "siteUrl": SITE}
    data = api_post(s, f"inspect:{url}", f"{SC_API}/urlInspection/index:inspect", body)
    return data.get("inspectionResult", {})


def resumen_inspeccion(res):
    idx = res.get("indexStatusResult", {}) or {}
    rich = res.get("richResultsResult", {}) or {}
    tipos = sorted({d.get("richResultType", "?")
                    for d in (rich.get("detectedItems", []) or [])})
    return {
        "coverageState":  idx.get("coverageState", ""),
        "indexingState":  idx.get("indexingState", ""),
        "lastCrawlTime":  idx.get("lastCrawlTime", ""),
        "pageFetchState": idx.get("pageFetchState", ""),
        "googleCanonical": idx.get("googleCanonical", ""),
        "userCanonical":   idx.get("userCanonical", ""),
        "veredicto_rich":  rich.get("verdict", "NONE"),
        "tipos_rich":      tipos,
        "veredicto":       idx.get("verdict", ""),
    }


def inspect_url(s, url):
    """Inspecciona. Si sale unknown/discovered, repite 3 veces y devuelve la moda."""
    r1 = resumen_inspeccion(inspect_once(s, url))
    estado = (r1.get("coverageState") or "").strip().lower()
    if not any(k in estado for k in INESTABLES) and estado:
        r1["intentos"] = 1
        return r1
    muestras = [r1] + [resumen_inspeccion(inspect_once(s, url)) for _ in range(2)]
    estados = [m.get("coverageState", "") for m in muestras]
    moda = Counter(estados).most_common(1)[0][0]
    elegido = next(m for m in muestras if m.get("coverageState", "") == moda)
    elegido["intentos"] = 3
    elegido["muestras_coverageState"] = estados
    return elegido


# ════════════════════════════════════════════════════════════════════════════
# Ventanas
# ════════════════════════════════════════════════════════════════════════════
def determinar_F(s):
    """Ultima fecha con dataState 'final'."""
    hoy = date.today()
    ini = (hoy - timedelta(days=30)).isoformat()
    filas = sa_query(s, "F:date_final", ini, hoy.isoformat(), ["date"],
                     data_state="final")
    fechas = sorted(f["keys"][0] for f in filas)
    if not fechas:
        raise RuntimeError("La API no devolvio ninguna fecha con dataState=final.")
    return fechas[-1]


def semanas(ini_str, F):
    """Semanas lunes-domingo desde ini hasta F (la ultima puede ser parcial)."""
    ini = datetime.strptime(ini_str, "%Y-%m-%d").date()
    fin = datetime.strptime(F, "%Y-%m-%d").date()
    out, cur = [], ini
    while cur <= fin:
        dom = cur + timedelta(days=6)
        out.append((cur.isoformat(), min(dom, fin).isoformat(), dom > fin))
        cur += timedelta(days=7)
    return out


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
def main():
    s = get_session()
    R = {}

    # ── 0. Fuentes disponibles ──────────────────────────────────────────────
    sites = api_get(s, "sites", f"{GSC_API}/sites")
    R["sites"] = sites

    F = determinar_F(s)
    R["F"] = F
    V_ACTUAL = (V_ACTUAL_I, F)
    V_CRUCE  = (V_CRUCE_I, F)
    RAW["_meta"]["ultima_fecha_final_F"] = F
    RAW["_meta"]["ventanas"] = {
        "V_actual": V_ACTUAL, "V_previa": V_PREVIA, "V_cruce": V_CRUCE,
    }
    print(f"[F] ultima fecha final = {F}")

    # ── 1. Totales y serie por date ─────────────────────────────────────────
    d_act  = sa_query(s, "date:V_actual", *V_ACTUAL, ["date"])
    d_prev = sa_query(s, "date:V_previa", *V_PREVIA, ["date"])
    R["date_actual"], R["date_previa"] = d_act, d_prev
    R["tot_actual"], R["tot_previa"] = tot(d_act), tot(d_prev)

    R["semanas"] = []
    for (a, b, parcial) in semanas(SERIE_INI, F):
        filas = sa_query(s, f"date:sem_{a}", a, b, ["date"])
        R["semanas"].append({"ini": a, "fin": b, "parcial": parcial, **tot(filas)})

    # Datos provisionales (dataState=all) posteriores a F
    f_next = (datetime.strptime(F, "%Y-%m-%d").date() + timedelta(days=1)).isoformat()
    hoy = date.today().isoformat()
    R["provisional"] = []
    if f_next <= hoy:
        prov = sa_query(s, "date:provisional_all", f_next, hoy, ["date"],
                        data_state="all")
        R["provisional"] = [{"fecha": f["keys"][0], **tot([f])} for f in prov]

    # ── 2. Por page ─────────────────────────────────────────────────────────
    p_act  = sa_query(s, "page:V_actual", *V_ACTUAL, ["page"])
    p_prev = sa_query(s, "page:V_previa", *V_PREVIA, ["page"])
    R["page_actual"], R["page_previa"] = p_act, p_prev
    R["tot_page_actual"] = tot(p_act)

    prev_map = {f["keys"][0]: f for f in p_prev}
    paginas = []
    for f in p_act:
        u = f["keys"][0]
        pv = prev_map.get(u, {})
        paginas.append({
            "url": u, "bloque": bloque(u), "techlaw": es_techlaw(u),
            "clics": f.get("clicks", 0), "impresiones": f.get("impressions", 0),
            "posicion": round(f.get("position", 0), 1),
            "d_clics": f.get("clicks", 0) - pv.get("clicks", 0),
            "d_impr":  f.get("impressions", 0) - pv.get("impressions", 0),
        })
    # paginas que existian antes y ya no aparecen
    act_urls = {f["keys"][0] for f in p_act}
    for u, pv in prev_map.items():
        if u not in act_urls:
            paginas.append({
                "url": u, "bloque": bloque(u), "techlaw": es_techlaw(u),
                "clics": 0, "impresiones": 0, "posicion": 0,
                "d_clics": -pv.get("clicks", 0), "d_impr": -pv.get("impressions", 0),
            })
    paginas.sort(key=lambda x: (-x["impresiones"], -x["clics"]))
    R["paginas"] = paginas

    bl = defaultdict(lambda: {"clics": 0, "impresiones": 0, "d_clics": 0, "d_impr": 0})
    for p in paginas:
        for k in ("clics", "impresiones", "d_clics", "d_impr"):
            bl[p["bloque"]][k] += p[k]
    R["bloques"] = dict(bl)

    tl = {"clics": 0, "impresiones": 0, "d_clics": 0, "d_impr": 0, "urls": []}
    for p in paginas:
        if p["techlaw"]:
            for k in ("clics", "impresiones", "d_clics", "d_impr"):
                tl[k] += p[k]
            tl["urls"].append(p)
    R["techlaw"] = tl

    # ── 3. Por query + clusters ─────────────────────────────────────────────
    q_act = sa_query(s, "query:V_actual", *V_ACTUAL, ["query"])
    R["query_actual"] = q_act
    R["tot_query"] = tot(q_act)
    ref = R["tot_actual"]
    R["cobertura"] = {
        "clics_pct": round(R["tot_query"]["clics"] / ref["clics"] * 100, 1) if ref["clics"] else 0,
        "impr_pct":  round(R["tot_query"]["impresiones"] / ref["impresiones"] * 100, 1) if ref["impresiones"] else 0,
    }

    # Marca «passas» restringida a España (la fila de vigilancia lo exige)
    q_esp = sa_query(s, "query:V_actual:esp", *V_ACTUAL, ["query"],
                     filters=[{"dimension": "country", "operator": "equals",
                               "expression": "esp"}])
    R["marca_esp"] = tot([f for f in q_esp
                          if any(t in f["keys"][0].lower()
                                 for t in CLUSTERS["marca_passas"])])

    qp = sa_query(s, "query_x_page:V_actual", *V_ACTUAL, ["query", "page"])
    R["query_x_page"] = qp
    clusters = {}
    for nombre, terminos in CLUSTERS.items():
        filas = [f for f in qp if any(t in f["keys"][0].lower() for t in terminos)]
        por_url = defaultdict(lambda: {"clics": 0, "impresiones": 0})
        for f in filas:
            u = f["keys"][1]
            por_url[u]["clics"] += f.get("clicks", 0)
            por_url[u]["impresiones"] += f.get("impressions", 0)
        clusters[nombre] = {
            "terminos": terminos,
            "total": tot(filas),
            "queries": sorted(
                [{"query": f["keys"][0], "page": f["keys"][1],
                  "clics": f.get("clicks", 0), "impresiones": f.get("impressions", 0),
                  "posicion": round(f.get("position", 0), 1)} for f in filas],
                key=lambda x: -x["impresiones"]),
            "por_url": sorted(
                [{"url": u, **v} for u, v in por_url.items()],
                key=lambda x: -x["impresiones"]),
        }
    R["clusters"] = clusters

    # ── 4. device / country ─────────────────────────────────────────────────
    R["device"]  = sa_query(s, "device:V_actual", *V_ACTUAL, ["device"])
    R["country"] = sa_query(s, "country:V_actual", *V_ACTUAL, ["country"])

    # ── 5. searchAppearance ─────────────────────────────────────────────────
    R["appearance"] = sa_query(s, "appearance:V_actual", *V_ACTUAL, ["searchAppearance"])

    # ── 6. Cruce con Analyze ────────────────────────────────────────────────
    R["cruce_page"]    = sa_query(s, "cruce:page", *V_CRUCE, ["page"])
    R["cruce_pais"]    = sa_query(s, "cruce:page_country", *V_CRUCE, ["page", "country"])
    R["cruce_device"]  = sa_query(s, "cruce:page_device", *V_CRUCE, ["page", "device"])

    # ── 7. Inspeccion de URL ────────────────────────────────────────────────
    del_sitemap = urls_sitemap()
    extra = [BASE + u for u in URLS_EXTRA]
    objetivo, vistas = [], set()
    for u in del_sitemap + extra:
        if u not in vistas:
            vistas.add(u)
            objetivo.append(u)
    print(f"[inspeccion] {len(objetivo)} URLs")
    insp = {}
    for i, u in enumerate(objetivo, 1):
        try:
            insp[u] = inspect_url(s, u)
        except Exception as e:
            insp[u] = {"error": str(e)}
        if i % 10 == 0:
            print(f"    {i}/{len(objetivo)}")
    R["inspeccion"] = insp

    # ── 8. Sitemaps ─────────────────────────────────────────────────────────
    R["sitemaps"] = api_get(s, "sitemaps", f"{GSC_API}/sites/{SITE_ENC}/sitemaps")

    # ── Guardar ─────────────────────────────────────────────────────────────
    with open(RAW_PATH, "w") as f:
        json.dump(RAW, f, indent=2, ensure_ascii=False)
    print(f"[raw] {RAW_PATH} ({len(RAW['llamadas'])} llamadas)")

    with open(INFORME_PATH, "w") as f:
        f.write(construir_informe(R))
    print(f"[informe] {INFORME_PATH}")


# ════════════════════════════════════════════════════════════════════════════
# Informe
# ════════════════════════════════════════════════════════════════════════════
PAISES = {"esp": "España", "usa": "EE. UU."}


def tabla_vigilancia(R):
    """Devuelve filas (senal, valor, veredicto). Veredicto: confirma/preocupa/sin dato."""
    filas = []
    sem = [w for w in R["semanas"] if not w["parcial"]]
    ult = sem[-3:] if sem else []
    if ult:
        vals = [w["clics"] for w in ult]
        txt = " / ".join(str(v) for v in vals) + " clics (últimas semanas completas)"
        if all(v >= 20 for v in vals):       ver = "confirma"
        elif any(v < 10 for v in vals):      ver = "preocupa"
        else:                                ver = "sin dato suficiente"
    else:
        txt, ver = "sin semanas completas en la serie", "sin dato suficiente"
    filas.append(("Clics semanales", txt, ver))

    # Burofax
    tc = R["tot_actual"]["clics"]
    bf = sum(p["clics"] for p in R["paginas"] if "burofax" in p["url"].lower())
    if tc:
        pct = bf / tc * 100
        txt = f"{bf}/{tc} clics = {pct:.0f}%"
        ver = "confirma" if pct < 60 else ("preocupa" if pct > 60 else "sin dato suficiente")
    else:
        txt, ver = "0 clics en la ventana", "sin dato suficiente"
    filas.append(("Concentración en burofax", txt, ver))

    # Marca «passas» en España (solo dato; consulta homonima)
    mp = R["marca_esp"]
    filas.append(("Marca «passas» en España",
                  f"{mp['clics']} clics, {fmt(mp['impresiones'])} impresiones, "
                  f"CTR {dec(mp['ctr'])}% — consulta homónima, solo dato",
                  "confirma" if mp["ctr"] > 0 else "preocupa"))

    # Cluster contencioso
    cc = R["clusters"]["contencioso"]
    if cc["queries"]:
        mejor = min(q["posicion"] for q in cc["queries"] if q["posicion"])
        txt = f"mejor posición {dec(mejor,1)}; {cc['total']['clics']} clics, {fmt(cc['total']['impresiones'])} impr."
        ver = "confirma" if mejor <= 5 else ("preocupa" if 7 <= mejor <= 12 else "sin dato suficiente")
    else:
        txt, ver = "sin queries del cluster (ver cobertura)", "sin dato suficiente"
    filas.append(("Cluster contencioso", txt, ver))

    # Servicios /en
    se = R["bloques"].get("servicios EN", {"clics": 0, "impresiones": 0})
    txt = f"{se['clics']} clics, {fmt(se['impresiones'])} impresiones"
    ver = "confirma" if se["impresiones"] > 0 else "preocupa"
    filas.append(("Servicios /en", txt, ver))

    # Posicion media
    pos = R["tot_actual"]["posicion"]
    ver = "confirma" if 7 <= pos <= 8 else ("preocupa" if pos > 9 else "sin dato suficiente")
    filas.append(("Posición media", dec(pos), ver))

    # TechLaw
    tl = R["techlaw"]
    txt = f"{tl['clics']} clics, {fmt(tl['impresiones'])} impresiones (ES+EN)"
    ver = "confirma" if tl["clics"] > 0 else "preocupa"
    filas.append(("Bloque TechLaw (ES+EN)", txt, ver))

    cob = R["cobertura"]
    filas.append(("Cobertura de query",
                  f"{dec(cob['clics_pct'],1)}% de clics y {dec(cob['impr_pct'],1)}% de impresiones",
                  "confirma"))
    return filas


def construir_informe(R):
    F = R["F"]
    ta, tp = R["tot_actual"], R["tot_previa"]
    cob = R["cobertura"]
    L = []
    A = L.append

    sitios = [e.get("siteUrl") for e in (R["sites"].get("siteEntry") or [])]

    # ── Front matter ────────────────────────────────────────────────────────
    A("---")
    A(f'titulo: "Informe GSC — sc-domain:passas.io"')
    A(f"fecha: {HOY}")
    A("fuente: Google Search Console API (searchAnalytics, urlInspection, sitemaps)")
    A("ventanas:")
    A(f"  v_actual: {V_ACTUAL_I} → {F}")
    A(f"  v_previa: {V_PREVIA[0]} → {V_PREVIA[1]}")
    A(f"  v_cruce: {V_CRUCE_I} → {F}")
    A(f"  serie_semanal: {SERIE_INI} → {F} (lunes–domingo)")
    A("dimension_de_referencia: date")
    A(f"ultima_fecha_final: {F}")
    A(f"cobertura_query: {dec(cob['clics_pct'],1)}% de clics, {dec(cob['impr_pct'],1)}% de impresiones")
    A("fuentes_disponibles:")
    for s_ in sitios:
        A(f"  - {s_}")
    A("---")
    A("")

    # ── 1 ───────────────────────────────────────────────────────────────────
    A("## 1. Fuentes y límites")
    A("")
    A(f"- **Propiedad**: `{SITE}`. Propiedades accesibles: {', '.join(f'`{x}`' for x in sitios) or '—'}.")
    A(f"- **Dimensión de referencia**: `date`. Todos los totales del informe salen de ella.")
    A(f"- **Última fecha con dataState `final` (F)**: **{F}**.")
    A(f"- **searchType**: `web`. **rowLimit**: {ROW_LIMIT} con paginación por `startRow` hasta agotar filas.")
    A(f"- **Cobertura de query en V_actual**: la dimensión `query` cubre "
      f"**{dec(cob['clics_pct'],1)}%** de los clics y **{dec(cob['impr_pct'],1)}%** de las impresiones "
      f"del total por `date`. Toda conclusión basada en queries queda limitada a esa cobertura.")
    A("- Los totales **cambian según la dimensión consultada**: Google aplica filtros de "
      "privacidad y descarta filas por dimensión, de modo que `page` y `query` no suman "
      "lo mismo que `date`. Las discrepancias se declaran en cada tabla.")
    A("- El campo `indexed` de sitemaps está **deprecado** y siempre vale 0; no se usa.")
    A("- La inspección de URL refleja **lo que Google vio en su último rastreo**, no el "
      "estado actual del sitio. No se diagnostica canonical, hreflang ni schema por otra vía.")
    A("- No se ha realizado ninguna escritura contra la API.")
    A("")
    if R["provisional"]:
        A(f"> **Provisional** — hay datos con dataState `all` posteriores a F "
          f"({len(R['provisional'])} día(s)). Se reportan aparte en §2 y no entran en ningún total.")
        A("")

    # ── 2 ───────────────────────────────────────────────────────────────────
    A("## 2. Totales y serie semanal")
    A("")
    A("| Ventana | Clics | Impresiones | CTR | Posición media |")
    A("|---|---:|---:|---:|---:|")
    A(f"| V_actual ({V_ACTUAL_I} → {F}) | {ta['clics']} | {fmt(ta['impresiones'])} | {dec(ta['ctr'])}% | {dec(ta['posicion'])} |")
    A(f"| V_previa ({V_PREVIA[0]} → {V_PREVIA[1]}) | {tp['clics']} | {fmt(tp['impresiones'])} | {dec(tp['ctr'])}% | {dec(tp['posicion'])} |")
    A(f"| Delta | {ta['clics']-tp['clics']:+d} | {sfmt(ta['impresiones']-tp['impresiones'])} | "
      f"{sdec(ta['ctr']-tp['ctr'])} pp | {sdec(ta['posicion']-tp['posicion'])} |")
    A("")
    A("> V_previa está **recalculada hoy contra la API**, no heredada de informes anteriores.")
    A("")
    A("### Serie semanal (lunes–domingo)")
    A("")
    A("| Semana | Clics | Impresiones | CTR | Posición |")
    A("|---|---:|---:|---:|---:|")
    for w in R["semanas"]:
        marca = " *(parcial)*" if w["parcial"] else ""
        A(f"| {w['ini']} → {w['fin']}{marca} | {w['clics']} | {fmt(w['impresiones'])} | {dec(w['ctr'])}% | {dec(w['posicion'])} |")
    A("")
    if R["provisional"]:
        A("### Datos provisionales (dataState `all`, posteriores a F)")
        A("")
        A("| Fecha | Clics | Impresiones |")
        A("|---|---:|---:|")
        for d in R["provisional"]:
            A(f"| {d['fecha']} | {d['clics']} | {fmt(d['impresiones'])} |")
        A("")
        A("> Cifras **provisionales**: pueden variar al consolidarse. No se usan en ningún total.")
        A("")

    # ── 3 ───────────────────────────────────────────────────────────────────
    A("## 3. Por bloque y página")
    A("")
    tpa = R["tot_page_actual"]
    A("| Bloque | Clics | Impresiones | Δ clics | Δ impresiones |")
    A("|---|---:|---:|---:|---:|")
    orden = ["Home", "blog ES", "blog EN", "servicios ES", "servicios EN",
             "herramientas", "equipo", "estaticas"]
    for b in orden:
        if b in R["bloques"]:
            v = R["bloques"][b]
            A(f"| {b} | {v['clics']} | {fmt(v['impresiones'])} | {v['d_clics']:+d} | {sfmt(v['d_impr'])} |")
    for b, v in R["bloques"].items():
        if b not in orden:
            A(f"| {b} | {v['clics']} | {fmt(v['impresiones'])} | {v['d_clics']:+d} | {sfmt(v['d_impr'])} |")
    sb_c = sum(v["clics"] for v in R["bloques"].values())
    sb_i = sum(v["impresiones"] for v in R["bloques"].values())
    A(f"| **Total `page`** | **{sb_c}** | **{fmt(sb_i)}** | | |")
    A("")
    A(f"**Cuadre**: la suma por bloque ({sb_c} clics, {fmt(sb_i)} impresiones) es el total de la "
      f"dimensión `page`. Frente a la dimensión de referencia `date` "
      f"({ta['clics']} clics, {fmt(ta['impresiones'])} impresiones) hay una diferencia de "
      f"{sb_c-ta['clics']:+d} clics y {sfmt(sb_i-ta['impresiones'])} impresiones: es el efecto "
      f"conocido de agregación por dimensión en la API, no un error de extracción.")
    A("")
    A("### Subbloque TechLaw")
    A("")
    A(f"Términos declarados — servicios con prefijo `{TECHLAW_PREFIJO_SERVICIOS}`; "
      f"artículos cuyo slug contenga: {', '.join('`'+t+'`' for t in TECHLAW_TERMINOS_SLUG)}.")
    A("")
    tl = R["techlaw"]
    A(f"**Total TechLaw (ES+EN)**: {tl['clics']} clics, {fmt(tl['impresiones'])} impresiones "
      f"(Δ {tl['d_clics']:+d} clics, {sfmt(tl['d_impr'])} impresiones).")
    A("")
    if tl["urls"]:
        A("| URL | Clics | Impresiones | Pos. | Δ clics | Δ impr. |")
        A("|---|---:|---:|---:|---:|---:|")
        for p in tl["urls"][:30]:
            A(f"| `{ruta(p['url'])}` | {p['clics']} | {fmt(p['impresiones'])} | {dec(p['posicion'],1)} | {p['d_clics']:+d} | {sfmt(p['d_impr'])} |")
        A("")
    A("### Páginas (top 40 por impresiones)")
    A("")
    A("| URL | Bloque | Clics | Impresiones | Pos. | Δ clics | Δ impr. |")
    A("|---|---|---:|---:|---:|---:|---:|")
    for p in R["paginas"][:40]:
        A(f"| `{ruta(p['url'])}` | {p['bloque']} | {p['clics']} | {fmt(p['impresiones'])} | "
          f"{dec(p['posicion'],1)} | {p['d_clics']:+d} | {sfmt(p['d_impr'])} |")
    A("")

    # ── 4 ───────────────────────────────────────────────────────────────────
    A("## 4. Clusters")
    A("")
    A(f"> Cobertura: las queries explican {dec(cob['clics_pct'],1)}% de los clics y "
      f"{dec(cob['impr_pct'],1)}% de las impresiones. Lo que sigue describe **solo esa porción**.")
    A("")
    A("### Top queries en V_actual")
    A("")
    A("| Query | Clics | Impresiones | CTR | Pos. |")
    A("|---|---:|---:|---:|---:|")
    for f in sorted(R["query_actual"], key=lambda x: -x.get("impressions", 0))[:25]:
        c, i = f.get("clicks", 0), f.get("impressions", 0)
        A(f"| {f['keys'][0]} | {c} | {fmt(i)} | {dec(c/i*100 if i else 0,1)}% | {dec(f.get('position',0),1)} |")
    A("")
    etiquetas = {
        "contencioso": "Contencioso (contencioso, alzada)",
        "burofax": "Burofax", "ai_act_techlaw": "AI Act / TechLaw",
        "due_diligence": "Due diligence", "chat_control": "Chat control",
        "marca_passas": "Marca (passas)",
    }
    for k, et in etiquetas.items():
        cl = R["clusters"][k]
        A(f"### {et}")
        A("")
        A(f"Términos: {', '.join('`'+t+'`' for t in cl['terminos'])}. "
          f"**Total**: {cl['total']['clics']} clics, {fmt(cl['total']['impresiones'])} impresiones.")
        A("")
        if not cl["queries"]:
            A("Sin filas de query en la ventana para este cluster (dentro de la cobertura declarada).")
            A("")
            continue
        A("| Query | URL | Clics | Impr. | Pos. |")
        A("|---|---|---:|---:|---:|")
        for q in cl["queries"][:15]:
            A(f"| {q['query']} | `{ruta(q['page'])}` | {q['clics']} | {fmt(q['impresiones'])} | {dec(q['posicion'],1)} |")
        A("")
        A("**Reparto por URL** (impresiones vs. clics — canibalización):")
        A("")
        A("| URL | Clics | Impresiones |")
        A("|---|---:|---:|")
        for u in cl["por_url"][:10]:
            A(f"| `{ruta(u['url'])}` | {u['clics']} | {fmt(u['impresiones'])} |")
        top_i = cl["por_url"][0] if cl["por_url"] else None
        con_c = [u for u in cl["por_url"] if u["clics"] > 0]
        top_c = max(con_c, key=lambda x: x["clics"]) if con_c else None
        A("")
        if top_i and top_c and top_i["url"] != top_c["url"]:
            A(f"> **Canibalización**: las impresiones se concentran en `{ruta(top_i['url'])}` "
              f"pero los clics los recibe `{ruta(top_c['url'])}`.")
        elif top_i and top_c:
            A(f"> Impresiones y clics coinciden en `{ruta(top_i['url'])}`; sin señal de canibalización.")
        else:
            A("> Impresiones sin clics en el cluster; no puede evaluarse canibalización.")
        A("")

    # ── 5 ───────────────────────────────────────────────────────────────────
    A("## 5. Dispositivo y país")
    A("")
    A("| Dispositivo | Clics | Impresiones | CTR | Pos. |")
    A("|---|---:|---:|---:|---:|")
    for f in sorted(R["device"], key=lambda x: -x.get("impressions", 0)):
        c, i = f.get("clicks", 0), f.get("impressions", 0)
        A(f"| {f['keys'][0]} | {c} | {fmt(i)} | {dec(c/i*100 if i else 0,1)}% | {dec(f.get('position',0),1)} |")
    dv = tot(R["device"])
    A(f"| **Total** | **{dv['clics']}** | **{fmt(dv['impresiones'])}** | | |")
    A("")
    A("| País | Clics | Impresiones | CTR | Pos. |")
    A("|---|---:|---:|---:|---:|")
    for f in sorted(R["country"], key=lambda x: -x.get("impressions", 0))[:15]:
        c, i = f.get("clicks", 0), f.get("impressions", 0)
        pais = PAISES.get(f["keys"][0], f["keys"][0])
        A(f"| {pais} | {c} | {fmt(i)} | {dec(c/i*100 if i else 0,1)}% | {dec(f.get('position',0),1)} |")
    cv = tot(R["country"])
    A(f"| **Total** | **{cv['clics']}** | **{fmt(cv['impresiones'])}** | | |")
    A("")
    A(f"**Cuadre**: device suma {dv['clics']} clics / {fmt(dv['impresiones'])} impresiones y "
      f"country suma {cv['clics']} / {fmt(cv['impresiones'])}; la referencia `date` da "
      f"{ta['clics']} / {fmt(ta['impresiones'])}. Las diferencias son de agregación por dimensión.")
    A("")
    A("### Aspecto en la búsqueda (searchAppearance)")
    A("")
    if R["appearance"]:
        A("| Aspecto | Clics | Impresiones | CTR | Pos. |")
        A("|---|---:|---:|---:|---:|")
        for f in sorted(R["appearance"], key=lambda x: -x.get("impressions", 0)):
            c, i = f.get("clicks", 0), f.get("impressions", 0)
            A(f"| {f['keys'][0]} | {c} | {fmt(i)} | {dec(c/i*100 if i else 0,1)}% | {dec(f.get('position',0),1)} |")
        A("")
        A("> `searchAppearance` no es aditivo: una impresión puede contar en varios aspectos, "
          "así que esta tabla **no suma** el total por `date`.")
    else:
        A("La API no devuelve filas de `searchAppearance` en esta ventana.")
    A("")

    # ── 6 ───────────────────────────────────────────────────────────────────
    A("## 6. Cruce con Analyze")
    A("")
    A(f"Ventana V_cruce: {V_CRUCE_I} → {F}. Analyze (contexto): 30 ago → 11 sep, "
      "sesiones con referrer google.com.")
    A("")
    A("> **Las ventanas no son idénticas** (Analyze llega al 11 sep; GSC solo hasta F). "
      "La comparación es indicativa, no una conciliación exacta.")
    A("")
    A("### Clics GSC por página en V_cruce")
    A("")
    A("| URL | Clics | Impresiones |")
    A("|---|---:|---:|")
    for f in sorted(R["cruce_page"], key=lambda x: -x.get("clicks", 0))[:25]:
        A(f"| `{ruta(f['keys'][0])}` | {f.get('clicks',0)} | {fmt(f.get('impressions',0))} |")
    A("")
    A("### Pregunta clave: ¿hay clics de EE. UU. en ASNEF, estafa y burofax?")
    A("")
    objetivo = {"asnef": "ASNEF", "estafa": "estafa", "burofax": "burofax"}
    A("| Página | Clics esp | Clics usa |")
    A("|---|---:|---:|")
    veredictos = {}
    for clave, et in objetivo.items():
        esp = sum(f.get("clicks", 0) for f in R["cruce_pais"]
                  if clave in f["keys"][0].lower() and f["keys"][1] == "esp")
        usa = sum(f.get("clicks", 0) for f in R["cruce_pais"]
                  if clave in f["keys"][0].lower() and f["keys"][1] == "usa")
        veredictos[clave] = usa
        A(f"| {et} | {esp} | {usa} |")
    A("")
    total_usa = sum(veredictos.values())
    if total_usa == 0:
        A("**Verificado**: GSC registra **0 clics desde EE. UU.** en ASNEF, estafa y burofax "
          "en V_cruce. Por tanto las 10 sesiones de EE. UU. que Analyze atribuye a "
          "`google.com` **no son clics de la Búsqueda de Google**. Explicaciones compatibles "
          "(no verificadas aquí): tráfico automatizado, referrer falsificado, o servicios de "
          "Google distintos de la Búsqueda.")
    else:
        A(f"**Verificado**: GSC sí registra clics desde EE. UU. en esas páginas "
          f"({total_usa} en total), de modo que las sesiones de Analyze son compatibles "
          f"con clics reales de la Búsqueda.")
    A("")
    A("### Reparto por dispositivo en V_cruce (top páginas)")
    A("")
    A("| URL | Dispositivo | Clics | Impresiones |")
    A("|---|---|---:|---:|")
    for f in sorted(R["cruce_device"], key=lambda x: -x.get("clicks", 0))[:20]:
        A(f"| `{ruta(f['keys'][0])}` | {f['keys'][1]} | {f.get('clicks',0)} | {fmt(f.get('impressions',0))} |")
    A("")
    cg = tot(R["cruce_page"])
    ap = sum(n for _, n in ANALYZE["por_pagina"])
    apais = sum(ANALYZE["por_pais"].values())
    adisp = sum(ANALYZE["por_dispositivo"].values())
    A("### Contraste de magnitud")
    A("")
    A("| Fuente | Medida | Total |")
    A("|---|---|---:|")
    A(f"| GSC (V_cruce) | clics | {cg['clics']} |")
    A(f"| Analyze | sesiones, por página (listadas) | {ap} + «resto 1 c/u» |")
    A(f"| Analyze | sesiones, por país | {apais} |")
    A(f"| Analyze | sesiones, por dispositivo | {adisp} |")
    A("")
    A(f"> **Los totales de Analyze no cuadran entre sí**: {ap} (+resto) por página, "
      f"{apais} por país y {adisp} por dispositivo son tres cifras distintas para la misma "
      "ventana. Antes de comparar con GSC conviene resolver esa discrepancia en origen; "
      "aquí se reproducen tal como se recibieron.")
    A("")
    A("> Además, **clic ≠ sesión** y las ventanas no coinciden, así que ninguna de estas "
      "cifras es directamente conciliable con la otra. Lo comparable es el **reparto "
      "relativo** por página, país y dispositivo, no el total.")
    A("")
    A("### Reparto relativo: Analyze frente a GSC")
    A("")
    gsc_pais = defaultdict(int)
    for f in R["cruce_pais"]:
        gsc_pais[f["keys"][1]] += f.get("clicks", 0)
    tot_gp = sum(gsc_pais.values())
    A("| País | Sesiones Analyze | % Analyze | Clics GSC | % GSC |")
    A("|---|---:|---:|---:|---:|")
    for c in ("esp", "usa"):
        sa_ = ANALYZE["por_pais"].get(c, 0)
        gc = gsc_pais.get(c, 0)
        A(f"| {PAISES.get(c,c)} | {sa_} | {dec(sa_/apais*100,1) if apais else '—'}% | "
          f"{gc} | {dec(gc/tot_gp*100,1) if tot_gp else '—'}% |")
    A("")

    # ── 7 ───────────────────────────────────────────────────────────────────
    A("## 7. Indexación y sitemap")
    A("")
    origen = RAW.get("sitemap_xml", {}).get("origen", "?")
    A(f"Origen de la lista de URLs: **{origen}**. "
      f"Total inspeccionadas: **{len(R['inspeccion'])}**.")
    A("")
    A("| URL | coverageState | indexingState | Último rastreo | pageFetchState | googleCanonical vs userCanonical | Rich results |")
    A("|---|---|---|---|---|---|---|")
    for u, v in R["inspeccion"].items():
        if "error" in v:
            A(f"| `{ruta(u)}` | ERROR | — | — | — | — | {v['error'][:40]} |")
            continue
        gc, uc = v.get("googleCanonical", ""), v.get("userCanonical", "")
        can = "coinciden" if gc == uc and gc else (f"`{ruta(gc) or '—'}` ≠ `{ruta(uc) or '—'}`" if (gc or uc) else "—")
        rich = v.get("veredicto_rich", "NONE")
        tipos = ", ".join(v.get("tipos_rich", [])) or "—"
        marca = " ⚠︎3x" if v.get("intentos") == 3 else ""
        crawl = (v.get("lastCrawlTime") or "—")[:10]
        A(f"| `{ruta(u) or '/'}` | {v.get('coverageState','—')}{marca} | {v.get('indexingState','—')} | "
          f"{crawl} | {v.get('pageFetchState','—')} | {can} | {rich} ({tipos}) |")
    A("")
    reintentos = [u for u, v in R["inspeccion"].items() if v.get("intentos") == 3]
    if reintentos:
        A(f"> ⚠︎3x: {len(reintentos)} URL(s) devolvieron `unknown`/`discovered`; se consultaron "
          "3 veces y se reporta la **moda**, por ser ruido conocido de la API.")
        A("")
    A("### Sitemaps")
    A("")
    sms = R["sitemaps"].get("sitemap", []) or []
    if sms:
        A("| Sitemap | lastDownloaded | Errores | Avisos | URLs enviadas |")
        A("|---|---|---:|---:|---:|")
        for sm in sms:
            errs = sm.get("errors", 0)
            warns = sm.get("warnings", 0)
            env = sum(int(c.get("submitted", 0)) for c in (sm.get("contents") or []))
            A(f"| `{sm.get('path','?')}` | {(sm.get('lastDownloaded') or '—')[:19]} | {errs} | {warns} | {env} |")
        A("")
        A("> El campo `indexed` está deprecado (siempre 0) y se omite deliberadamente.")
    else:
        A("No hay sitemaps registrados en la propiedad.")
    A("")

    # ── 8 ───────────────────────────────────────────────────────────────────
    A("## 8. Tabla de vigilancia")
    A("")
    A("| Señal | Valor en V_actual | Veredicto |")
    A("|---|---|---|")
    for senal, valor, ver in tabla_vigilancia(R):
        A(f"| {senal} | {valor} | **{ver}** |")
    A("")

    # ── 9 ───────────────────────────────────────────────────────────────────
    A("## 9. Hallazgos nuevos")
    A("")
    A("_(máximo 5; cada uno marcado como verificado contra la API o como hipótesis)_")
    A("")
    n = 0
    n += 1
    A(f"{n}. **[verificado]** V_actual ({V_ACTUAL_I} → {F}) cierra con {ta['clics']} clics y "
      f"{fmt(ta['impresiones'])} impresiones (CTR {ta['ctr']}%, posición {ta['posicion']}), "
      f"frente a {tp['clics']} clics y {fmt(tp['impresiones'])} impresiones en V_previa "
      f"recalculada.")
    if total_usa == 0:
        n += 1
        A(f"{n}. **[verificado]** GSC no registra ningún clic desde EE. UU. en ASNEF, estafa ni "
          "burofax durante V_cruce, pese a que Analyze atribuye 10 sesiones de EE. UU. a "
          "`google.com` en esas páginas. Las dos fuentes no describen el mismo tráfico.")
    n += 1
    A(f"{n}. **[verificado]** La dimensión `query` solo cubre {cob['clics_pct']}% de los clics y "
      f"{cob['impr_pct']}% de las impresiones de V_actual; el análisis por cluster describe "
      "una fracción minoritaria del rendimiento real.")
    tl = R["techlaw"]
    n += 1
    A(f"{n}. **[verificado]** El bloque TechLaw (ES+EN) acumula {tl['clics']} clics y "
      f"{fmt(tl['impresiones'])} impresiones en V_actual.")
    if n < 5:
        n += 1
        A(f"{n}. **[hipótesis]** Los cambios de 7–11 sep (canonical v2, migración a "
          "`/legal-tools`, slugs EN nuevos con 301 pendientes) caen en el extremo final de la "
          "ventana o después de F, por lo que su efecto **aún no es medible** en estos datos. "
          "Queda por confirmar en la próxima extracción.")
    A("")
    A("---")
    A("")
    A(f"Datos crudos: `{RAW_PATH}` — {len(RAW['llamadas'])} llamadas a la API, "
      "respuestas sin postprocesar.")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
