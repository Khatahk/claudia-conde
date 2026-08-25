# Proyecto passas.io — memoria de trabajo GSC

Repositorio de análisis SEO de **passas.io** contra la API de Google Search Console.
Este archivo es la memoria del proyecto: lo que está verificado, lo que falló, y las
reglas de método que se han ganado a base de errores. Léelo antes de generar un informe.

---

## 1. Conexión a GSC

**Propiedad:** `sc-domain:passas.io` (propiedad de dominio, no de prefijo de URL)
**Service Account:** `seopassas@ethereal-mind-493609-g5.iam.gserviceaccount.com`
**Permiso:** `siteOwner`
**Es el único sitio** al que la cuenta de servicio tiene acceso.

Configuración (`.env`, ignorado por git):

```ini
GSC_SERVICE_ACCOUNT_FILE=service_account.json
GSC_SITE_URL=sc-domain:passas.io
```

`service_account.json` y `.env` están en `.gitignore`. **Nunca los commitees.**

### Gotcha del entorno: las librerías del sistema están rotas

En el contenedor remoto, `python3 -c "from google.oauth2 import service_account"` revienta con
`ModuleNotFoundError: _cffi_backend` + `pyo3_runtime.PanicException`. Es el paquete
`cryptography` de Debian con el binding de Rust incompleto, y **no se puede arreglar con pip**
(`Cannot uninstall cryptography 41.0.7, RECORD file not found`).

Solución verificada: **entorno virtual limpio.**

```bash
python3 -m venv /tmp/gsc_venv
source /tmp/gsc_venv/bin/activate
pip install -r requirements.txt requests
```

Todos los scripts `gsc_*.py` deben ejecutarse dentro de ese venv.

### Endpoints en uso

| Endpoint | Para qué |
|---|---|
| `GET  webmasters/v3/sites` | Listar propiedades |
| `GET  webmasters/v3/sites/{site}/sitemaps` | Estado del sitemap |
| `POST webmasters/v3/sites/{site}/searchAnalytics/query` | Clics / impresiones / CTR / posición |
| `POST searchconsole.googleapis.com/v1/urlInspection/index:inspect` | Cobertura e indexación por URL |

---

## 2. Limitaciones VERIFICADAS de los datos (no son opiniones)

Medidas el 2026-08-25 sobre la ventana 2026-08-03 → 2026-08-24. Reproducibles con
`gsc_verify_20260825.py` y los scripts asociados.

### 2.1 El dimensionado por consulta cubre una fracción mínima del tráfico

| Dimensión | Filas | Clics | Impresiones |
|---|---:|---:|---:|
| `date` | 21 | 35 | 3.622 |
| `page` | 48 | 35 | **3.840** |
| `query` | 112 | **3** | **641** |
| `device` | 3 | 35 | 3.622 |
| `country` | 74 | 35 | 3.622 |

**Las consultas nombradas cubren el 17,7% de las impresiones y solo el 8,6% de los clics.**
El 82,3% de impresiones y el 91,4% de clics quedan anonimizados por Google.
(Ventana previa 12 jul–2 ago: 15,0% de impresiones, 24,1% de clics.)

**Regla:** toda conclusión construida sobre la tabla de consultas describe menos de una quinta
parte del tráfico y menos de una décima de los clics. Hay que declararlo cada vez que se
recomiende algo a partir de consultas. Nunca presentar un agregado de consultas como si fuera
el total del cluster.

### 2.2 Los totales dependen de la dimensión consultada

`page` devuelve 3.840 impresiones; `date`, `device` y `country` devuelven 3.622. **Un 6,0% de
diferencia sobre el mismo periodo.** Es comportamiento estructural de GSC (agregación distinta
por dimensión), no un error de extracción.

**Regla:** fijar la dimensión de referencia al principio del informe y decirlo. Para totales de
ventana usar `date`. No mezclar un total de `date` con un desglose de `page` sin advertirlo.

### 2.3 La API de inspección devuelve veredictos inestables en URLs nunca rastreadas

Probado con 6 llamadas consecutivas por URL (`gsc_inspection_stability.py`):

| URL | Resultado |
|---|---|
| `/blog/responsable-del-despliegue-ai-act-obligaciones-2026` | **INESTABLE** — 4× «Discovered», 2× «URL is unknown to Google» |
| `/en/servicios/commercial-litigation` | **INESTABLE** — 4× «Discovered», 2× «unknown» |
| `/en/team/guillermo-passas-varo` | **INESTABLE** — 4× «Discovered», 2× «unknown» |
| `/blog/exito-abogado-preventivo-etica` (rastreada) | ESTABLE — 6× «Crawled - not indexed» |
| `/honorarios` (indexada) | ESTABLE — 6× «Submitted and indexed» |

**Patrón:** las URLs que Google **nunca ha rastreado** alternan de forma no determinista entre
«Discovered - currently not indexed» y «URL is unknown to Google». Las que sí ha rastreado son
estables.

**Regla:** ante una URL nunca rastreada, consultar varias veces antes de reportar el estado.
La diferencia entre esos dos veredictos **no dice nada sobre la URL** — es ruido de la API.
No construir diagnóstico sobre esa distinción, ni en un sentido ni en el otro.

### 2.4 Latencia y relleno retroactivo

GSC publica con 2–3 días de retraso **y rellena hacia atrás**. La ventana 03–24 ago pasó de
3.458 impresiones (extracción del 24 ago) a 3.622 (recuento del 25 ago), un +4,7%, sin que
cambiara ningún día ya cerrado salvo la entrada del 23 ago.

**Regla:** fechar toda cifra con el día de extracción. Un informe reextraído days después no
dará los mismos números y eso no es un error de nadie.

### 2.5 El campo `indexed` del endpoint de sitemaps es inútil

`GET /sitemaps` devuelve `submitted: 65, indexed: 0`. El campo `indexed` está deprecado y
siempre vale 0. El recuento real de indexación exige recorrer las URLs con el endpoint de
inspección, una por una.

---

## 3. Limitaciones DEL ENTORNO de ejecución (sesión remota)

| Capacidad | Estado | Consecuencia |
|---|---|---|
| API de GSC | ✅ Funciona | Todo el análisis de rendimiento e indexación es verificable |
| **HTML en vivo de passas.io** | ❌ **Bloqueado** | `curl https://passas.io/...` → `CONNECT tunnel failed, 403`. El proxy de egress deniega el host por política de la organización. **No se puede verificar canonical, hreflang, schema ni CTA desde esta sesión.** |
| **MCP de Webflow** | ❌ Desconectado | No se puede leer el CMS, Page Settings ni el Designer |
| Librerías Google del sistema | ⚠️ Rotas | Requiere venv (§1) |

**Consecuencia de método:** desde esta sesión, **cualquier afirmación sobre el HTML publicado
es de segunda mano.** El único sustituto parcial es el endpoint de inspección de URL, que
devuelve `userCanonical` y `googleCanonical` **según el último rastreo de Google**, no según
el estado actual del sitio. Fechas de rastreo observadas el 25 ago: `/en` → 5 ago;
`/en/blog` → 18 ago; `/servicios/techlaw-ai-act-compliance` → 31 jul.

Un informe que necesite verificar el HTML tiene que pedir esa verificación a una sesión con
acceso, o declarar el punto como no verificado. **No inferirlo.**

---

## 4. Reglas de método heredadas (informe 2026-08-24 + su respuesta)

Ganadas a base de errores reales. Se mantienen todas, con dos correcciones.

1. **No afirmar ausencia de datos estructurados a partir de HTML crudo.** `curl` no ejecuta
   JavaScript. Cruzar árbol de elementos, Custom Code, scripts aplicados y campo de Page
   Settings, y cerrar con Rich Results Test o inspección en vivo.
2. **Antes de elevar una incidencia, buscar en el histórico si ya está cerrada.**
3. **Ante una asimetría entre dos plantillas del mismo sitio, asumir configuración ausente**
   antes que fallo de plataforma. La plantilla que funciona enseña cómo arreglar la que no.
4. **No trasladar límites de la API a límites del producto.** `update_page_settings` con
   `jsonLdSchema` devuelve 200 y no guarda; `bulk_update_pages_schema_markup` sí persiste.
   Los placeholders `{{wf ...}}` escritos por API resuelven vacíos: la ficha del Designer es
   un binding registrado, no una cadena de texto.
5. **Separar lo que mueve posición de lo que solo corrige estructura.** Los datos
   estructurados no mueven ranking. Desde agosto de 2023 Google no muestra rich results de
   FAQPage para dominios no institucionales.
6. **Etiquetar la hipótesis como hipótesis** y verificarla antes de convertirla en acción.
7. **Incluir el reparto por bloque de negocio**, no solo por URL.
8. **Cruzar locales** cuando el mismo tema tiene contenido en ambos.
9. **Descontar o advertir del bloque de marca** al leer CTR agregado.
10. **Comprobar que los elementos de conversión apuntan a algún sitio.** Un `href="#"` en el
    botón de reserva pesa más que cualquier incidencia de marcado.

**Corrección a la regla 1 (ampliación).** El mismo escepticismo se aplica a **canonical y
hreflang**, no solo a schema. El informe del 24 ago diagnosticó T1 (canonical roto en `/en` y
`/en/blog`) con `curl` — exactamente el método que la respuesta demolió para T2. La respuesta
no aplicó su propia regla a ese punto. **Cualquier cosa leída del `<head>` con curl hereda la
misma advertencia.**

**Corrección a la regla 6 (nueva, verificada el 25 ago).** La discrepancia entre «Discovered -
currently not indexed» y «URL is unknown to Google» **no es una diferencia de estado que
merezca una nota** (así lo sostuvo la respuesta, §2.6). Es ruido no determinista de la API en
URLs nunca rastreadas — reproducido en §2.3. Ni equipararlas sin más (informe) ni tratarlas
como señal (respuesta): consultar varias veces y reportar la moda.

**Regla nueva 11.** Toda cifra agregada que se presente como reparto de un total **debe sumar
ese total**. La tabla de bloques de negocio de la respuesta (§3.3) suma 3.660 impresiones
declarando repartir 3.458.

**Regla nueva 12.** No heredar cifras del informe anterior sin recontarlas. Las «~350
impresiones de intención de precio» del cluster contencioso pasaron del informe a la respuesta
sin verificación; el recuento real es 183 (cluster) / 198 (sitio entero).

---

## 5. Estado del negocio (contexto fijo, no re-litigar)

- Despacho orientado a calidad, no a volumen. El funnel **filtra** clientes idóneos.
- Ticket mínimo: **2.000 €** judicial / **600 €** extrajudicial. Videoconsulta 90 € IVA incl.
- Objetivo: **6.000 €/mes antes de noviembre de 2026**.
- La caída de CTR cuando crece la visibilidad TOFU **no es un problema** y no se defiende como KPI.
- Perfiles: **A** = litigación y consumo ES · **B** = TechLaw ES · **C** = internacional / locale EN.
- Decisiones cerradas el 3 de julio: no tocar `gastos-hipoteca`; el canal para AI Act es
  LinkedIn + outreach + DM, no SEO a corto plazo.

---

## 6. Scripts del repositorio

| Script | Qué hace | Credenciales |
|---|---|---|
| `check_gsc_connection.py` | Test de conexión y listado de propiedades | Sí |
| `gsc_raw_dump.py` | Volcado de datos brutos | Sí |
| `gsc_full_report.py` | Informe completo | Sí |
| `gsc_indexing_audit.py` | Auditoría de indexación | Sí |
| `gsc_en_report.py` | Informe del locale EN | Sí |
| `gsc_verify_20260825.py` | **Cotejo informe/respuesta vs GSC en vivo** | Sí |
| `gsc_canonical_probe.py` | **Sonda de canonical por parejas ES/EN** | Sí |
| `gsc_inspection_stability.py` | **Prueba de estabilidad de la API de inspección** | Sí |
| `test_gsc_validation.py` | Valida ficheros locales | No |
| `test_gsc_passas_connection.py` | Test con fallbacks | Opcionales |

Volcados de cotejo del 25 ago: `gsc_cotejo_2026-08-25.json`,
`gsc_canonical_probe_2026-08-25.json`, `gsc_inspection_stability_2026-08-25.json`,
`gsc_check_respuesta_2026-08-25.json`.

---

## 7. Informes emitidos

| Fecha | Documento | Nota |
|---|---|---|
| 2026-07-16 / 07-27 / 08-03 | `informe_gsc_passas_*.xml` | Histórico en repo |
| 2026-08-04 | `informe_gsc_locale_en_2026-08-04.xml` | Locale EN |
| 2026-08-24 | `INFORME-GSC-PASSAS-2026-08-24.md` | Informe del piloto (aportado) |
| 2026-08-25 | `respuestainformegsc-2026-08-24.md` | Respuesta correctiva (aportada) |
| **2026-08-25** | **`INFORME-GSC-PASSAS-2026-08-25.md`** | **Cotejo de los dos anteriores contra GSC en vivo** |
