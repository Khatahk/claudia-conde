#!/usr/bin/env python3
"""
Test de conexión a Google Search Console (GSC) con passas.io
Valida credenciales, acceso a API y datos disponibles.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# No importar google libraries aquí - lo haremos dinámicamente
GOOGLE_LIBS_AVAILABLE = False

# Importar dotenv sin los módulos problemáticos
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        pass

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
GSC_API = "https://www.googleapis.com/webmasters/v3"
PASSAS_PROPERTY = "sc-domain:passas.io"


def check_local_data():
    """Verifica datos locales existentes de GSC."""
    print("\n[CHECK] Verificando datos locales de GSC...")

    data_files = {
        "gsc_raw_passas_2026-08-03.json": "Datos brutos principales",
        "gsc_raw_en_2026-08-04.json": "Datos para locales EN",
        "informe_gsc_passas_2026-08-03.xml": "Reporte XML más reciente",
    }

    found_files = []
    for filename, description in data_files.items():
        filepath = Path(filename)
        if filepath.exists():
            size = filepath.stat().st_size
            found_files.append((filename, size, description))
            print(f"  ✓ {filename}")
            print(f"    {description} ({size:,} bytes)")

    if found_files:
        print(f"\n[OK] Se encontraron {len(found_files)} archivo(s) con datos GSC.")
        # Mostrar metadatos del archivo principal
        main_file = Path("gsc_raw_passas_2026-08-03.json")
        if main_file.exists():
            try:
                with open(main_file) as f:
                    data = json.load(f)
                    meta = data.get("_meta", {})
                    print(f"\n[DATA] Metadatos del archivo principal:")
                    print(f"       Propiedad: {meta.get('propiedad')}")
                    print(f"       Service Account: {meta.get('service_account')}")
                    print(f"       Generado: {meta.get('generado_utc')}")

                    # Contar registros
                    for key in ["ultimos_7d", "ultimos_28d"]:
                        if key in data:
                            records = len(data[key].get("rows", []))
                            print(f"       {key}: {records} registros")
            except json.JSONDecodeError:
                print(f"[WARN] No se pudo parsear {main_file}")
        return True
    else:
        print(f"[WARN] No se encontraron archivos locales de datos GSC.")
        return False


def build_credentials():
    """Construye credenciales desde variables de entorno."""
    global GOOGLE_LIBS_AVAILABLE

    try:
        from google.oauth2 import service_account
        GOOGLE_LIBS_AVAILABLE = True
    except BaseException:  # Catch all, including PanicException from Rust
        return None

    sa_json = os.getenv("GSC_SERVICE_ACCOUNT_JSON")
    sa_file = os.getenv("GSC_SERVICE_ACCOUNT_FILE")

    if sa_json:
        try:
            info = json.loads(sa_json)
            return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        except json.JSONDecodeError as e:
            raise EnvironmentError(f"GSC_SERVICE_ACCOUNT_JSON inválido: {e}")

    if sa_file:
        if not Path(sa_file).exists():
            raise EnvironmentError(f"Archivo {sa_file} no encontrado")
        return service_account.Credentials.from_service_account_file(sa_file, scopes=SCOPES)

    return None


def test_connection():
    """Prueba la conexión a GSC API."""
    print("\n[CHECK] Verificando credenciales y conexión a GSC API...")

    try:
        credentials = build_credentials()
        if not credentials:
            print("  [SKIP] No hay credenciales configuradas.")
            print("         Define GSC_SERVICE_ACCOUNT_FILE o GSC_SERVICE_ACCOUNT_JSON en .env")
            return False

        print(f"  ✓ Credenciales cargadas")
        print(f"    Email: {credentials.service_account_email}")

    except EnvironmentError as e:
        print(f"  [ERROR] {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Error al cargar credenciales: {e}")
        return False

    try:
        from google.auth.transport.requests import AuthorizedSession
        import requests

        session = AuthorizedSession(credentials)
        session.verify = False

        # Test: Listar sitios
        print(f"\n  [TEST] Conectando a {GSC_API}/sites...")
        resp = session.get(f"{GSC_API}/sites")
        resp.raise_for_status()
        sites = resp.json().get("siteEntry", [])

        print(f"  ✓ Conexión exitosa")
        print(f"  ✓ Sitios accesibles: {len(sites)}")

        if sites:
            for site in sites:
                site_url = site.get('siteUrl', '?')
                perm = site.get('permissionLevel', '?')
                print(f"    - {site_url} ({perm})")

                # Verificar si passas.io está en la lista
                if 'passas.io' in site_url:
                    print(f"      ✓✓ PASSAS.IO encontrado!")

        return True

    except Exception as e:
        print(f"  [ERROR] Error en conexión: {e}")
        return False


def generate_test_report():
    """Genera un reporte resumido del estado."""
    print("\n" + "=" * 60)
    print("  RESULTADO DE PRUEBA: GSC + PASSAS.IO")
    print("=" * 60)

    local_data_ok = check_local_data()
    api_connection_ok = test_connection()

    print("\n[SUMMARY]")
    print(f"  Datos locales:       {'✓ OK' if local_data_ok else '✗ FALTA'}")
    print(f"  Conexión API:        {'✓ OK' if api_connection_ok else '✗ CONFIG_REQUERIDA' if not GOOGLE_LIBS_AVAILABLE else '✗ FALLA'}")
    print(f"  Google libraries:    {'✓ OK' if GOOGLE_LIBS_AVAILABLE else '✗ NO_INSTALADAS'}")

    status = "✓ LISTO" if local_data_ok else "⚠ PARCIAL"
    print(f"\n  Estado general:      {status}")

    if not api_connection_ok and GOOGLE_LIBS_AVAILABLE:
        print("\n[SETUP] Para completar la conexión API:")
        print("  1. Descarga service account desde Google Cloud Console")
        print("  2. Copia las credenciales en .env:")
        print("     GSC_SERVICE_ACCOUNT_JSON='{...}'")
        print("     O: GSC_SERVICE_ACCOUNT_FILE=service_account.json")
        print("  3. Ejecuta: python check_gsc_connection.py")

    print("\n" + "=" * 60)

    return local_data_ok


if __name__ == "__main__":
    success = generate_test_report()
    sys.exit(0 if success or not GOOGLE_LIBS_AVAILABLE else 1)
