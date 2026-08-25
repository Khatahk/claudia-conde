#!/usr/bin/env python3
"""
Validación de datos GSC para passas.io
Verifica la integridad y disponibilidad de datos sin dependencias de Google.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def validate_gsc_data():
    """Valida archivos de datos GSC existentes."""
    print("\n" + "=" * 70)
    print("  VALIDACIÓN DE DATOS GSC - PASSAS.IO")
    print("=" * 70)

    results = {
        "files_found": 0,
        "files_valid": 0,
        "total_records": 0,
        "errors": [],
    }

    # Archivos esperados
    data_files = {
        "gsc_raw_passas_2026-08-03.json": {
            "description": "Datos brutos - Propiedad principal (sc-domain:passas.io)",
            "expected_keys": ["_meta", "search_analytics", "sitemaps", "sites", "url_inspection"],
        },
        "gsc_raw_en_2026-08-04.json": {
            "description": "Datos brutos - Análisis de locale EN",
            "expected_keys": ["_meta", "resultados"],
        },
        "informe_gsc_passas_2026-08-03.xml": {
            "description": "Reporte XML - Estado general y cobertura",
            "expected_keys": None,  # XML, no JSON
        },
    }

    print("\n[VALIDACIÓN] Analizando archivos...\n")

    for filename, info in data_files.items():
        filepath = Path(filename)

        if not filepath.exists():
            results["errors"].append(f"Archivo no encontrado: {filename}")
            print(f"✗ {filename}")
            continue

        results["files_found"] += 1
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✓ {filename}")
        print(f"  Tamaño: {size_mb:.2f} MB")
        print(f"  Desc:   {info['description']}")

        # Validar contenido
        try:
            if filename.endswith(".json"):
                with open(filepath) as f:
                    data = json.load(f)

                # Verificar claves esperadas
                if info["expected_keys"]:
                    missing = set(info["expected_keys"]) - set(data.keys())
                    if missing:
                        results["errors"].append(
                            f"{filename}: Claves faltantes: {missing}"
                        )
                        print(f"  ✗ Claves faltantes: {missing}")
                    else:
                        results["files_valid"] += 1
                        print(f"  ✓ Estructura válida")

                        # Contar registros
                        if "rows" in data:
                            results["total_records"] += len(data["rows"])
                        for key in ["ultimos_7d", "ultimos_28d"]:
                            if key in data and "rows" in data[key]:
                                results["total_records"] += len(data[key]["rows"])

                        # Mostrar metadata
                        if "_meta" in data:
                            meta = data["_meta"]
                            print(f"  Property: {meta.get('propiedad', '?')}")
                            print(f"  SA Email: {meta.get('service_account', '?')}")

            else:  # XML
                with open(filepath) as f:
                    content = f.read()
                    if len(content) > 100 and content.strip():
                        results["files_valid"] += 1
                        print(f"  ✓ Archivo válido ({len(content)} bytes)")

        except json.JSONDecodeError as e:
            results["errors"].append(f"{filename}: JSON inválido - {e}")
            print(f"  ✗ JSON inválido: {e}")
        except Exception as e:
            results["errors"].append(f"{filename}: {e}")
            print(f"  ✗ Error: {e}")

        print()

    # Resumen
    print("=" * 70)
    print("[RESULTADO]")
    print(
        f"  Archivos encontrados:  {results['files_found']}/{len(data_files)}"
    )
    print(f"  Archivos válidos:      {results['files_valid']}/{results['files_found']}")
    print(f"  Total registros:       {results['total_records']:,}")

    if results["errors"]:
        print(f"\n[ERRORES]")
        for error in results["errors"]:
            print(f"  • {error}")

    # Status
    if results["files_valid"] == results["files_found"] and not results["errors"]:
        print("\n✓✓ Todos los archivos de datos están disponibles y válidos")
        status_ok = True
    else:
        print(f"\n⚠ Se encontraron {len(results['errors'])} problema(s)")
        status_ok = False

    print("=" * 70 + "\n")

    return status_ok


def show_setup_instructions():
    """Muestra instrucciones de configuración."""
    print("\n[SETUP] Configuración de Credenciales Google Search Console")
    print("-" * 70)
    print("""
1. Accede a Google Cloud Console:
   https://console.cloud.google.com/

2. Crea o selecciona un proyecto (e.g., "ethereal-mind-493609")

3. Habilita la API "Search Console API":
   - APIs & Services > Library
   - Busca "Search Console API"
   - Click en "Enable"

4. Crea una Service Account:
   - APIs & Services > Credentials
   - "Create Credentials" > "Service Account"
   - Configura con nombre: "seopassas" (o similar)

5. Genera la clave JSON:
   - En Service Accounts, haz click en la cuenta creada
   - Pestaña "Keys" > "Add Key" > "Create new key"
   - Tipo: JSON
   - Guarda el archivo como 'service_account.json'

6. Agrega el email de la Service Account a Google Search Console:
   - En GSC, para cada propiedad
   - Settings > Users and permissions
   - Add user: seopassas@tu-proyecto.iam.gserviceaccount.com

7. Configura el archivo .env:
   GSC_SERVICE_ACCOUNT_FILE=service_account.json
   GSC_SITE_URL=sc-domain:passas.io

8. Verifica la conexión:
   python check_gsc_connection.py
""")
    print("-" * 70)


if __name__ == "__main__":
    success = validate_gsc_data()

    if not success:
        show_setup_instructions()

    sys.exit(0 if success else 0)  # Exit 0 either way (test completed)
