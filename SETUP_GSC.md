# Google Search Console - Configuración para Passas.io

## Estado Actual

✓ **Datos GSC disponibles**: Los datos brutos están almacenados localmente
- `gsc_raw_passas_2026-08-03.json` - Datos completos de la propiedad principal (sc-domain:passas.io)
- `gsc_raw_en_2026-08-04.json` - Análisis específico del locale EN
- Reportes XML con cobertura de indexación

## Pruebas Disponibles

### 1. Validación de Datos Locales
```bash
python test_gsc_validation.py
```
Valida que todos los archivos JSON y XML estén disponibles y con estructura correcta.
**No requiere credenciales de Google.**

### 2. Test de Conexión a GSC API
```bash
python test_gsc_passas_connection.py
```
Verifica:
- Datos locales disponibles ✓
- Posibilidad de conectar a GSC API (requiere credenciales)
- Service account configurado

### 3. Conexión Completa (producción)
```bash
python check_gsc_connection.py
```
Realiza pruebas completas:
- Autenticación con Service Account
- Listado de propiedades verificadas
- Consulta de SearchAnalytics
- Verificación de cobertura

## Configuración Requerida

### Paso 1: Crear Service Account en Google Cloud

1. Accede a [Google Cloud Console](https://console.cloud.google.com/)

2. Selecciona el proyecto **ethereal-mind-493609** (o crea uno nuevo)

3. Habilita la API "Google Search Console API":
   - APIs & Services → Library
   - Busca "Search Console API"
   - Haz clic en "Enable"

4. Crea una Service Account:
   - APIs & Services → Credentials
   - "Create Credentials" → "Service Account"
   - Nombre: `seopassas` (o similar)
   - Asigna rol: "Editor" (o "Webmaster")

5. Genera una clave JSON:
   - En Service Accounts, haz clic en la cuenta creada
   - Pestaña "Keys" → "Add Key" → "Create new key"
   - Tipo: JSON
   - Se descargará automáticamente

### Paso 2: Configurar Credenciales Localmente

Copia el archivo descargado al directorio raíz del proyecto:
```bash
cp ~/Downloads/ethereal-mind-493609-*.json ./service_account.json
```

Crea un archivo `.env`:
```bash
cp .env.example .env
```

Edita `.env` y completa las credenciales:
```ini
GSC_SERVICE_ACCOUNT_FILE=service_account.json
GSC_SITE_URL=sc-domain:passas.io
```

**Alternativa (CI/CD)**: Si usas un pipeline, establece credenciales inline:
```bash
GSC_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
```

### Paso 3: Autorizar Service Account en GSC

1. Accede a [Google Search Console](https://search.google.com/search-console)

2. Para cada propiedad (ej: passas.io):
   - Settings → Users and permissions
   - "Add user"
   - Ingresa el email del Service Account:
     ```
     seopassas@ethereal-mind-493609.iam.gserviceaccount.com
     ```
   - Nivel de permisos: "Full" (lectura/escritura completa)

3. Repite para todas las propiedades a monitorear

### Paso 4: Verificar la Conexión

```bash
# Valida estructura de datos locales
python test_gsc_validation.py

# Comprueba que el setup esté correcto
python test_gsc_passas_connection.py

# Test completo de conexión (requiere credenciales)
python check_gsc_connection.py
```

## Estructura de Datos GSC

### Archivo Principal: `gsc_raw_passas_2026-08-03.json`

```json
{
  "_meta": {
    "propiedad": "sc-domain:passas.io",
    "service_account": "seopassas@ethereal-mind-493609-g5.iam.gserviceaccount.com",
    "generado_utc": "2026-08-03",
    "rangos": {
      "ultimos_7d": {"startDate": "2026-07-27", "endDate": "2026-08-03"},
      "ultimos_28d": {"startDate": "2026-07-06", "endDate": "2026-08-03"}
    }
  },
  "search_analytics": {
    "ultimos_7d": {"rows": [...]},
    "ultimos_28d": {"rows": [...]},
    "ultimos_90d": {"rows": [...]}
  },
  "sitemaps": {
    "body": [...],
    "http_status": [...]
  },
  "sites": {
    "body": [...],
    "http_status": [...]
  },
  "url_inspection": {
    "resultados": [...],
    "total_urls_inspeccionadas": 123
  }
}
```

### Endpoints API Utilizados

- `GET /webmasters/v3/sites` - Listar propiedades
- `GET /webmasters/v3/sites/{site}/sitemaps` - Sitemaps
- `POST /webmasters/v3/sites/{site}/searchAnalytics/query` - Analytics
- `POST /searchconsole.googleapis.com/v1/urlInspection/index:inspect` - Inspección de URLs

## Troubleshooting

### Error: "No hay sitios verificados para esta cuenta"
- **Causa**: El Service Account no tiene acceso a ninguna propiedad en GSC
- **Solución**: Agrega el email del SA como usuario en Settings → Users and permissions

### Error: "HTTP 403 Forbidden"
- **Causa**: Permisos insuficientes o API no habilitada
- **Solución**: 
  1. Verifica que "Search Console API" esté habilitada
  2. Asigna rol "Editor" al Service Account

### Error: "Invalid authentication"
- **Causa**: Credenciales expiradas o inválidas
- **Solución**: Descarga nuevamente la clave JSON desde Google Cloud Console

### "ModuleNotFoundError: No module named 'google'"
- **Causa**: Librerías de Google no instaladas
- **Solución**: 
  ```bash
  pip install -r requirements.txt
  ```

## Scripts Disponibles

| Script | Descripción | Credenciales |
|--------|-------------|-------------|
| `check_gsc_connection.py` | Test completo de conexión API | Requeridas |
| `gsc_raw_dump.py` | Descarga datos brutos de GSC | Requeridas |
| `gsc_full_report.py` | Genera reporte completo | Requeridas |
| `gsc_indexing_audit.py` | Auditoría de indexación | Requeridas |
| `gsc_en_report.py` | Reporte específico EN | Requeridas |
| `test_gsc_validation.py` | Valida datos locales | ✗ No requiere |
| `test_gsc_passas_connection.py` | Test con datos locales | Opcionales |

## Referencias

- [Google Search Console API Docs](https://developers.google.com/webmasters/search-console/guides/access-control)
- [Search Console API Reference](https://developers.google.com/webmasters/search-console/guides/search-analytics)
- [Service Account Setup](https://cloud.google.com/docs/authentication/getting-started)

## Notas Importantes

⚠️ **Latencia de Datos**: Google Search Console publica datos con **2-3 días de retraso**. Los rangos que llegan hasta hoy pueden estar incompletos.

⚠️ **Privacidad**: Nunca commitees el archivo `service_account.json` al repositorio. Está en `.gitignore`.

⚠️ **Permisos**: La Service Account solo puede acceder a propiedades en las que haya sido autorizada como usuario en GSC.
