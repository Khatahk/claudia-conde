#!/usr/bin/env python3
"""
Sonda de canonical/hreflang vía API de inspección de URL de GSC.
Objetivo: resolver la contradicción entre lo que el informe 2026-08-24 vio con
curl (canonical hardcodeado en /en y /en/blog) y lo que Google registra.
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
INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SITE = "sc-domain:passas.io"

PARES = [
    # (ES, EN) — parejas declaradas como equivalentes por hreflang
    ("https://passas.io/", "https://passas.io/en"),
    ("https://passas.io/blog", "https://passas.io/en/blog"),
    ("https://passas.io/servicios", "https://passas.io/en/servicios"),
    ("https://passas.io/honorarios", "https://passas.io/en/honorarios"),
    ("https://passas.io/servicios/litigacion-juicio-administrativo",
     "https://passas.io/en/servicios/administrative-litigation"),
    ("https://passas.io/servicios/techlaw-ai-act-compliance",
     "https://passas.io/en/servicios/ai-act-compliance"),
    ("https://passas.io/team/guillermo-passas-varo",
     "https://passas.io/en/team/guillermo-passas-varo"),
]


def main():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GSC_SERVICE_ACCOUNT_FILE"), scopes=SCOPES)
    s = AuthorizedSession(creds)
    s.verify = False

    out = {}
    print(f"{'URL':<52} {'veredicto':<9} {'rastreo':<11} {'canon_google':<30} canon_declarada")
    print("-" * 130)

    for es, en in PARES:
        for u in (es, en):
            try:
                r = s.post(INSPECT, json={"inspectionUrl": u, "siteUrl": SITE})
                r.raise_for_status()
                res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
                rec = {
                    "veredicto": res.get("verdict"),
                    "cobertura": res.get("coverageState"),
                    "ultimo_rastreo": res.get("lastCrawlTime"),
                    "canonica_google": res.get("googleCanonical"),
                    "canonica_declarada": res.get("userCanonical"),
                }
                out[u] = rec
                short = u.replace("https://passas.io", "") or "/"
                crawl = (rec["ultimo_rastreo"] or "nunca")[:10]
                cg = (rec["canonica_google"] or "—").replace("https://passas.io", "") or "/"
                cd = (rec["canonica_declarada"] or "— (ausente)").replace("https://passas.io", "")
                print(f"{short:<52} {str(rec['veredicto']):<9} {crawl:<11} {cg:<30} {cd}")
            except Exception as e:
                out[u] = {"error": str(e)}
                print(f"{u}: ERROR {e}")
        print()

    with open("gsc_canonical_probe_2026-08-25.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # Resumen del patrón
    print("\n=== PATRÓN ===")
    con = [u for u, v in out.items() if v.get("canonica_declarada")]
    sin = [u for u, v in out.items() if not v.get("canonica_declarada") and "error" not in v]
    print(f"Con canonical declarada registrada por Google ({len(con)}):")
    for u in con:
        print(f"   {u.replace('https://passas.io','') or '/'}  ->  "
              f"{out[u]['canonica_declarada'].replace('https://passas.io','') or '/'}")
    print(f"\nSin canonical declarada registrada ({len(sin)}):")
    for u in sin:
        print(f"   {u.replace('https://passas.io','') or '/'}  "
              f"(rastreo: {(out[u]['ultimo_rastreo'] or 'nunca')[:10]})")


if __name__ == "__main__":
    main()
