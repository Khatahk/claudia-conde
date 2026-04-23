"""
Verifica la conexión a Google Search Console (GSC) API.

Soporta dos métodos de autenticación:
  1. Service Account (variable de entorno GSC_SERVICE_ACCOUNT_FILE o GSC_SERVICE_ACCOUNT_JSON)
  2. OAuth2 (variable de entorno GSC_CREDENTIALS_FILE, por defecto credentials.json)

Variables de entorno:
  GSC_SERVICE_ACCOUNT_FILE  - Ruta al archivo JSON de service account
  GSC_SERVICE_ACCOUNT_JSON  - Contenido JSON del service account (inline)
  GSC_CREDENTIALS_FILE      - Ruta al archivo credentials.json de OAuth2
  GSC_SITE_URL              - URL del sitio a verificar (opcional)
"""

import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def build_service_with_service_account():
    import google.auth
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    sa_file = os.getenv("GSC_SERVICE_ACCOUNT_FILE")
    sa_json = os.getenv("GSC_SERVICE_ACCOUNT_JSON")

    if sa_json:
        info = json.loads(sa_json)
        credentials = service_account.Credentials.from_service_account_info(
            info, scopes=SCOPES
        )
    elif sa_file:
        credentials = service_account.Credentials.from_service_account_file(
            sa_file, scopes=SCOPES
        )
    else:
        return None

    return build("searchconsole", "v1", credentials=credentials)


def build_service_with_oauth2():
    import pickle

    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds_file = os.getenv("GSC_CREDENTIALS_FILE", "credentials.json")
    token_file = "token.pickle"
    creds = None

    if os.path.exists(token_file):
        with open(token_file, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_file):
                raise FileNotFoundError(
                    f"No se encontró el archivo de credenciales: {creds_file}\n"
                    "Configura GSC_SERVICE_ACCOUNT_FILE, GSC_SERVICE_ACCOUNT_JSON "
                    f"o proporciona {creds_file}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "wb") as f:
            pickle.dump(creds, f)

    return build("searchconsole", "v1", credentials=creds)


def get_service():
    service = build_service_with_service_account()
    if service:
        print("[AUTH] Usando Service Account")
        return service
    print("[AUTH] Usando OAuth2")
    return build_service_with_oauth2()


def check_connection(service):
    print("\n[CHECK] Listando sitios verificados en GSC...")
    result = service.sites().list().execute()
    sites = result.get("siteEntry", [])

    if not sites:
        print("[WARN]  No se encontraron sitios verificados en esta cuenta.")
        return []

    print(f"[OK]    Se encontraron {len(sites)} sitio(s):")
    for site in sites:
        print(f"         - {site['siteUrl']}  (permiso: {site.get('permissionLevel', 'desconocido')})")
    return sites


def check_site_data(service, site_url):
    """Realiza una consulta de prueba de datos de rendimiento para confirmar acceso de lectura."""
    print(f"\n[CHECK] Consultando datos de rendimiento para: {site_url}")
    body = {
        "startDate": "2025-01-01",
        "endDate": "2025-01-07",
        "dimensions": ["query"],
        "rowLimit": 3,
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = response.get("rows", [])
    if rows:
        print(f"[OK]    Datos recibidos ({len(rows)} fila(s) de muestra).")
    else:
        print("[OK]    Conexión correcta pero sin datos en el rango de fechas de prueba.")
    return rows


def main():
    print("=" * 55)
    print("  Verificación de conexión a Google Search Console")
    print("=" * 55)

    try:
        service = get_service()
    except Exception as e:
        print(f"\n[ERROR] Autenticación fallida: {e}")
        sys.exit(1)

    try:
        sites = check_connection(service)
    except Exception as e:
        print(f"\n[ERROR] No se pudo listar los sitios: {e}")
        sys.exit(1)

    site_url = os.getenv("GSC_SITE_URL")
    if not site_url and sites:
        site_url = sites[0]["siteUrl"]
        print(f"\n[INFO]  GSC_SITE_URL no definido; usando el primer sitio: {site_url}")

    if site_url:
        try:
            check_site_data(service, site_url)
        except Exception as e:
            print(f"\n[ERROR] No se pudo consultar datos del sitio: {e}")
            sys.exit(1)

    print("\n[RESULT] Conexión a GSC verificada correctamente.")


if __name__ == "__main__":
    main()
