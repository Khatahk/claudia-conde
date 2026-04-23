"""
Verifica la conexión a Google Search Console (GSC) API.

Variables de entorno:
  GSC_SERVICE_ACCOUNT_FILE  - Ruta al archivo JSON de service account
  GSC_SERVICE_ACCOUNT_JSON  - Contenido JSON del service account (inline)
  GSC_SITE_URL              - URL del sitio a verificar (opcional)
"""

import json
import os
import sys
import warnings

import requests
import urllib3
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC_API = "https://www.googleapis.com/webmasters/v3"


def build_credentials():
    sa_json = os.getenv("GSC_SERVICE_ACCOUNT_JSON")
    sa_file = os.getenv("GSC_SERVICE_ACCOUNT_FILE")

    if sa_json:
        info = json.loads(sa_json)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    if sa_file:
        return service_account.Credentials.from_service_account_file(sa_file, scopes=SCOPES)

    raise EnvironmentError(
        "Define GSC_SERVICE_ACCOUNT_FILE o GSC_SERVICE_ACCOUNT_JSON en el .env"
    )


def get_session(credentials):
    session = AuthorizedSession(credentials)
    session.verify = False  # permite proxies con certificados autofirmados
    return session


def list_sites(session):
    url = f"{GSC_API}/sites"
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json().get("siteEntry", [])


def query_search_analytics(session, site_url):
    url = f"{GSC_API}/sites/{requests.utils.quote(site_url, safe='')}/searchAnalytics/query"
    body = {
        "startDate": "2025-01-01",
        "endDate": "2025-01-07",
        "dimensions": ["query"],
        "rowLimit": 3,
    }
    resp = session.post(url, json=body)
    resp.raise_for_status()
    return resp.json().get("rows", [])


def main():
    print("=" * 55)
    print("  Verificación de conexión a Google Search Console")
    print("=" * 55)

    try:
        credentials = build_credentials()
        print("[AUTH]   Service Account cargado correctamente")
        print(f"         Proyecto : {credentials.service_account_email.split('@')[1]}")
        print(f"         Email SA : {credentials.service_account_email}")
    except Exception as e:
        print(f"\n[ERROR] Credenciales inválidas: {e}")
        sys.exit(1)

    try:
        session = get_session(credentials)
    except Exception as e:
        print(f"\n[ERROR] No se pudo crear la sesión autenticada: {e}")
        sys.exit(1)

    try:
        print("\n[CHECK]  Listando sitios verificados en GSC...")
        sites = list_sites(session)
    except requests.HTTPError as e:
        print(f"\n[ERROR] HTTP {e.response.status_code}: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] No se pudo conectar con GSC: {e}")
        sys.exit(1)

    if not sites:
        print("[WARN]   No hay sitios verificados para esta cuenta de servicio.")
        print("         Asegúrate de haber añadido el email del SA como usuario en GSC.")
    else:
        print(f"[OK]     Se encontraron {len(sites)} sitio(s):")
        for s in sites:
            print(f"          - {s['siteUrl']}  (permiso: {s.get('permissionLevel', '?')})")

    site_url = os.getenv("GSC_SITE_URL") or (sites[0]["siteUrl"] if sites else None)
    if not site_url:
        print("\n[INFO]   Sin sitios disponibles para consulta de datos.")
    else:
        if not os.getenv("GSC_SITE_URL"):
            print(f"\n[INFO]   GSC_SITE_URL no definido; usando: {site_url}")
        try:
            print(f"[CHECK]  Consultando SearchAnalytics para {site_url}...")
            rows = query_search_analytics(session, site_url)
            if rows:
                print(f"[OK]     Datos recibidos ({len(rows)} fila(s) de muestra).")
            else:
                print("[OK]     Conexión correcta (sin datos en el rango de fechas de prueba).")
        except requests.HTTPError as e:
            print(f"\n[ERROR] HTTP {e.response.status_code}: {e.response.text}")
            sys.exit(1)
        except Exception as e:
            print(f"\n[ERROR] Error al consultar datos: {e}")
            sys.exit(1)

    print("\n[RESULT] Conexión a GSC verificada correctamente.\n")


if __name__ == "__main__":
    main()
