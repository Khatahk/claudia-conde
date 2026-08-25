#!/usr/bin/env python3
"""
Prueba de estabilidad de la API de inspección de URL de GSC.

Contexto: el informe 2026-08-24 (T4) registró que la API devolvió dos veredictos
distintos para la misma URL y los trató como equivalentes. La respuesta al informe
sostuvo que son "estados distintos" y que la discrepancia merecía una nota.

Esta prueba llama N veces a la misma URL para determinar si la discrepancia
procede de la URL o de la API.
"""

import json
import os
import time
from collections import Counter

import urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SITE = "sc-domain:passas.io"
N = 6

# Mezcla deliberada: nunca rastreadas, rastreadas-sin-indexar, e indexadas (control)
URLS = [
    "https://passas.io/blog/responsable-del-despliegue-ai-act-obligaciones-2026",
    "https://passas.io/en/servicios/commercial-litigation",
    "https://passas.io/en/team/guillermo-passas-varo",
    "https://passas.io/blog/exito-abogado-preventivo-etica",
    "https://passas.io/honorarios",  # control: indexada y estable
]


def main():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GSC_SERVICE_ACCOUNT_FILE"), scopes=SCOPES)
    s = AuthorizedSession(creds)
    s.verify = False

    resultados = {}
    for u in URLS:
        short = u.replace("https://passas.io", "")
        print(f"\n=== {short} ===")
        obs = []
        for i in range(N):
            try:
                r = s.post(INSPECT, json={"inspectionUrl": u, "siteUrl": SITE})
                r.raise_for_status()
                res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
                estado = res.get("coverageState")
                obs.append(estado)
                print(f"  llamada {i+1}: {estado}")
            except Exception as e:
                obs.append(f"ERROR: {e}")
                print(f"  llamada {i+1}: ERROR {e}")
            time.sleep(1.5)

        cnt = Counter(obs)
        estable = len(cnt) == 1
        resultados[u] = {
            "observaciones": obs,
            "distintos": len(cnt),
            "estable": estable,
            "reparto": dict(cnt),
        }
        print(f"  -> {'ESTABLE' if estable else '*** INESTABLE ***'}: {dict(cnt)}")

    print("\n\n=== CONCLUSIÓN ===")
    inestables = [u for u, v in resultados.items() if not v["estable"]]
    if inestables:
        print(f"{len(inestables)} de {len(URLS)} URLs devuelven cobertura inestable "
              f"en {N} llamadas consecutivas:")
        for u in inestables:
            print(f"   {u.replace('https://passas.io','')}: {resultados[u]['reparto']}")
        print("\nLa discrepancia de veredictos procede de la API, no del estado de la URL.")
    else:
        print("Todas las URLs devuelven cobertura estable.")

    with open("gsc_inspection_stability_2026-08-25.json", "w", encoding="utf-8") as f:
        json.dump({"llamadas_por_url": N, "resultados": resultados}, f,
                  ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
