---
titulo: "Informe GSC — sc-domain:passas.io"
fecha: 2026-09-11
fuente: Google Search Console API (searchAnalytics, urlInspection, sitemaps)
ventanas:
  v_actual: 2026-08-25 → 2026-09-08
  v_previa: 2026-08-03 → 2026-08-24
  v_cruce: 2026-08-30 → 2026-09-08
  serie_semanal: 2026-07-27 → 2026-09-08 (lunes–domingo)
dimension_de_referencia: date
ultima_fecha_final: 2026-09-08
cobertura_query: 7,3% de clics, 15,7% de impresiones
fuentes_disponibles:
  - sc-domain:passas.io
---

## 1. Fuentes y límites

- **Propiedad**: `sc-domain:passas.io`. Propiedades accesibles: `sc-domain:passas.io`.
- **Dimensión de referencia**: `date`. Todos los totales del informe salen de ella.
- **Última fecha con dataState `final` (F)**: **2026-09-08**.
- **searchType**: `web`. **rowLimit**: 25000 con paginación por `startRow` hasta agotar filas.
- **Cobertura de query en V_actual**: la dimensión `query` cubre **7,3%** de los clics y **15,7%** de las impresiones del total por `date`. Toda conclusión basada en queries queda limitada a esa cobertura.
- Los totales **cambian según la dimensión consultada**: Google aplica filtros de privacidad y descarta filas por dimensión, de modo que `page` y `query` no suman lo mismo que `date`. Las discrepancias se declaran en cada tabla.
- El campo `indexed` de sitemaps está **deprecado** y siempre vale 0; no se usa.
- La inspección de URL refleja **lo que Google vio en su último rastreo**, no el estado actual del sitio. No se diagnostica canonical, hreflang ni schema por otra vía.
- No se ha realizado ninguna escritura contra la API.

> **Provisional** — hay datos con dataState `all` posteriores a F (3 día(s)). Se reportan aparte en §2 y no entran en ningún total.

## 2. Totales y serie semanal

| Ventana | Clics | Impresiones | CTR | Posición media |
|---|---:|---:|---:|---:|
| V_actual (2026-08-25 → 2026-09-08) | 41 | 4.976 | 0,82% | 8,64 |
| V_previa (2026-08-03 → 2026-08-24) | 39 | 3.906 | 1,00% | 8,20 |
| Delta | +2 | +1.070 | -0,18 pp | +0,44 |

> V_previa está **recalculada hoy contra la API**, no heredada de informes anteriores.

### Serie semanal (lunes–domingo)

| Semana | Clics | Impresiones | CTR | Posición |
|---|---:|---:|---:|---:|
| 2026-07-27 → 2026-08-02 | 7 | 1.753 | 0,40% | 7,73 |
| 2026-08-03 → 2026-08-09 | 5 | 1.227 | 0,41% | 8,58 |
| 2026-08-10 → 2026-08-16 | 8 | 1.065 | 0,75% | 7,49 |
| 2026-08-17 → 2026-08-23 | 22 | 1.330 | 1,65% | 8,26 |
| 2026-08-24 → 2026-08-30 | 13 | 1.841 | 0,71% | 9,12 |
| 2026-08-31 → 2026-09-06 | 20 | 2.346 | 0,85% | 8,81 |
| 2026-09-07 → 2026-09-08 *(parcial)* | 12 | 1.073 | 1,12% | 7,55 |

### Datos provisionales (dataState `all`, posteriores a F)

| Fecha | Clics | Impresiones |
|---|---:|---:|
| 2026-09-09 | 6 | 614 |
| 2026-09-10 | 7 | 522 |
| 2026-09-11 | 0 | 1 |

> Cifras **provisionales**: pueden variar al consolidarse. No se usan en ningún total.

## 3. Por bloque y página

| Bloque | Clics | Impresiones | Δ clics | Δ impresiones |
|---|---:|---:|---:|---:|
| Home | 5 | 73 | +4 | -22 |
| blog ES | 26 | 2.943 | -3 | +679 |
| blog EN | 3 | 1.148 | +3 | +620 |
| servicios ES | 2 | 733 | -3 | -128 |
| servicios EN | 0 | 22 | +0 | -70 |
| herramientas | 0 | 26 | +0 | +26 |
| equipo | 4 | 78 | +1 | +4 |
| estaticas | 1 | 247 | +0 | +18 |
| **Total `page`** | **41** | **5.270** | | |

**Cuadre**: la suma por bloque (41 clics, 5.270 impresiones) es el total de la dimensión `page`. Frente a la referencia `date` (41 clics, 4.976 impresiones) hay +0 clics y +294 impresiones de diferencia: es el efecto conocido de agregación por dimensión en la API (filtrado de privacidad), no un error de extracción.

### Subbloque TechLaw

**Términos declarados** — servicios con prefijo `techlaw-`; artículos cuyo slug contenga: `ai-act`, `inteligencia-artificial`, `digital-omnibus`, `chat-control`, `software`, `rgpd`; y artículos cuyo slug incluya el token `ia` aislado.

> **Nota sobre el término `ia-`**: aplicado como simple subcadena captura `guia-`, `tributaria-`, `andalucia-` o `audiencia-`, lo que arrastraba al bloque artículos sin relación con IA (entre ellos el de burofax, la página con más impresiones del sitio). Se aplica por tanto como **token completo delimitado por guiones**: entran `...-ia-...` y `...-ia` (p. ej. `decision-ia-reclamacion`), y no entra `guia-`.

**Total TechLaw (ES+EN)**: 4 clics, 1.375 impresiones (Δ +2 clics, +337 impresiones).

| URL | Clics | Impresiones | Pos. | Δ clics | Δ impr. |
|---|---:|---:|---:|---:|---:|
| `/en/blog/digital-omnibus-ai-act-final-text` | 0 | 351 | 6,0 | +0 | +17 |
| `/blog/checklist-ai-act-cumplimiento-empresas` | 1 | 202 | 21,6 | +1 | +197 |
| `/en/blog/ai-act-article-5-1a-provider-scope` | 0 | 185 | 5,4 | +0 | -6 |
| `/en/blog/ai-act-article-50-2-marking-deadline` | 1 | 170 | 6,3 | +1 | +170 |
| `/servicios/techlaw-ai-act-compliance` | 0 | 134 | 40,3 | +0 | -57 |
| `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 102 | 7,7 | -1 | -49 |
| `/blog/responsable-del-despliegue-ai-act-obligaciones-2026` | 0 | 42 | 22,2 | +0 | +42 |
| `/autoevaluacion-ai-act` | 1 | 38 | 19,1 | +1 | +36 |
| `/servicios/techlaw-ai-act-alto-riesgo` | 0 | 22 | 6,7 | +0 | -1 |
| `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | 0 | 20 | 11,6 | +0 | -13 |
| `/legal-tools/autoevaluacion-ai-act` | 0 | 18 | 8,2 | +0 | +18 |
| `/blog/administrador-responsabilidad-personal-ia-empresa-lsc-236` | 1 | 16 | 5,4 | +1 | +16 |
| `/servicios/techlaw-founding-pack` | 0 | 14 | 6,3 | -1 | -12 |
| `/en/politica-de-inteligencia-artificial` | 0 | 11 | 4,4 | +0 | +7 |
| `/blog/quien-responde-danos-causados-software-ia-2026` | 0 | 9 | 5,3 | +0 | +9 |
| `/en/servicios/ai-act-provider-compliance` | 0 | 9 | 6,2 | +0 | -12 |
| `/blog/explicar-decision-ia-reclamacion-afectado` | 0 | 7 | 5,9 | +0 | +7 |
| `/blog/estafa-voz-clonada-ia-banco-devolucion-dinero` | 0 | 5 | 26,8 | +0 | +5 |
| `/en/legal-tools/autoevaluacion-ai-act` | 0 | 3 | 8,7 | +0 | +3 |
| `/en/servicios/ai-act-compliance` | 0 | 3 | 4,3 | +0 | -25 |
| `/politica-de-inteligencia-artificial` | 0 | 3 | 6,3 | +0 | +3 |
| `/blog/ai-act-startups-espana-obligaciones-agosto-2026` | 0 | 2 | 6,0 | +0 | -1 |
| `/en/abogados-inteligencia-artificial` | 0 | 2 | 18,0 | +0 | +2 |
| `/en/servicios/ai-act-high-risk` | 0 | 2 | 9,0 | +0 | -22 |
| `/legal-tools/necesito-abogado-ia` | 0 | 2 | 11,0 | +0 | +2 |
| `/servicios/techlaw-ai-compliance-providers` | 0 | 2 | 5,0 | +0 | +2 |
| `/blog/responsable-del-despliegue-ai-act-obligaciones-2026?efe235d7_page=3` | 0 | 1 | 4,0 | +0 | +1 |
| `/en/autoevaluacion-ai-act` | 0 | 0 | 0,0 | +0 | -2 |

### Páginas (top 40 por impresiones)

| URL | Bloque | Clics | Impresiones | Pos. | Δ clics | Δ impr. |
|---|---|---:|---:|---:|---:|---:|
| `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | blog ES | 6 | 1.069 | 7,1 | -18 | -17 |
| `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | blog ES | 11 | 880 | 6,2 | +7 | +165 |
| `/en/blog/digital-omnibus-ai-act-final-text` | blog EN | 0 | 351 | 6,0 | +0 | +17 |
| `/servicios/litigacion-juicio-administrativo` | servicios ES | 1 | 298 | 8,7 | -2 | -149 |
| `/en/blog/unpaid-invoice-spain-debt-recovery-guide` | blog EN | 2 | 261 | 8,0 | +2 | +261 |
| `/blog/checklist-ai-act-cumplimiento-empresas` | blog ES | 1 | 202 | 21,6 | +1 | +197 |
| `/en/blog/ai-act-article-5-1a-provider-scope` | blog EN | 0 | 185 | 5,4 | +0 | -6 |
| `/blog/ayuntamiento-no-paga-factura-intereses-demora-reclamar` | blog ES | 1 | 177 | 7,6 | +1 | +177 |
| `/en/blog/ai-act-article-50-2-marking-deadline` | blog EN | 1 | 170 | 6,3 | +1 | +170 |
| `/en/blog/claiming-unpaid-invoices-spain-pre-action-requirement` | blog EN | 0 | 145 | 4,6 | +0 | +145 |
| `/servicios/techlaw-ai-act-compliance` | servicios ES | 0 | 134 | 40,3 | +0 | -57 |
| `/servicios/internacional-european-data-compliance` | servicios ES | 0 | 107 | 5,9 | +0 | +100 |
| `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | blog ES | 0 | 102 | 7,7 | -1 | -49 |
| `/en` | estaticas | 0 | 91 | 6,3 | -1 | -27 |
| `/blog/gastos-hipoteca-2026-guia-legal-para-reclamar-plazos-y-modelo` | blog ES | 0 | 82 | 7,1 | +0 | -3 |
| `/honorarios` | estaticas | 0 | 79 | 8,1 | +0 | -11 |
| `/` | Home | 5 | 73 | 5,6 | +4 | -22 |
| `/blog/derivacion-responsabilidad-tributaria-administrador-2026` | blog ES | 1 | 70 | 5,0 | +1 | +70 |
| `/blog/cuanto-cuesta-abogado-startup-espana-precios-2026` | blog ES | 2 | 65 | 7,6 | +2 | +9 |
| `/blog/cuando-necesitas-abogado-test-ocho-preguntas` | blog ES | 0 | 49 | 11,1 | +0 | +49 |
| `/servicios/litigacion-juicio-civil` | servicios ES | 0 | 49 | 7,4 | +0 | +22 |
| `/servicios/internacional-due-diligence-tech` | servicios ES | 0 | 48 | 31,1 | +0 | -10 |
| `/team/guillermo-passas-varo` | equipo | 3 | 45 | 5,8 | +1 | +23 |
| `/blog/responsable-del-despliegue-ai-act-obligaciones-2026` | blog ES | 0 | 42 | 22,2 | +0 | +42 |
| `/autoevaluacion-ai-act` | estaticas | 1 | 38 | 19,1 | +1 | +36 |
| `/en/blog/do-you-need-a-lawyer-in-spain-self-check` | blog EN | 0 | 33 | 6,3 | +0 | +33 |
| `/blog/estafa-o-incumplimiento-de-contrato-como-distinguirlo-en-2026` | blog ES | 1 | 31 | 7,7 | +1 | -28 |
| `/team/david-sanchez-lorenzo` | equipo | 1 | 31 | 6,0 | +0 | -21 |
| `/blog/due-diligence-legal-ronda-inversion-startup` | blog ES | 0 | 27 | 9,8 | +0 | +27 |
| `/servicios` | servicios ES | 0 | 26 | 30,2 | -1 | -15 |
| `/servicios/techlaw-ai-act-alto-riesgo` | servicios ES | 0 | 22 | 6,7 | +0 | -1 |
| `/servicios/litigacion-juicio-mercantil` | servicios ES | 0 | 21 | 8,5 | +0 | -3 |
| `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | blog ES | 0 | 20 | 11,6 | +0 | -13 |
| `/legal-tools/autoevaluacion-ai-act` | herramientas | 0 | 18 | 8,2 | +0 | +18 |
| `/blog/administrador-responsabilidad-personal-ia-empresa-lsc-236` | blog ES | 1 | 16 | 5,4 | +1 | +16 |
| `/blog/como-reclamar-una-factura-de-hasta-2000-euros-sin-abogado-guia-2026` | blog ES | 1 | 16 | 6,5 | +1 | -3 |
| `/servicios/techlaw-founding-pack` | servicios ES | 0 | 14 | 6,3 | -1 | -12 |
| `/blog/recurrir-multa-aepd-audiencia-nacional` | blog ES | 0 | 13 | 12,8 | +0 | +13 |
| `/servicios/internacional-spain-entry-pack` | servicios ES | 1 | 12 | 5,7 | +1 | -5 |
| `/en/honorarios` | estaticas | 0 | 12 | 5,7 | +0 | +8 |

## 4. Clusters

> Cobertura: las queries explican 7,3% de los clics y 15,7% de las impresiones. Lo que sigue describe **solo esa porción**.

> Para juzgar posiciones se exige un mínimo de **10 impresiones** por query: por debajo, la API devuelve posiciones extremas (2,0 con una sola impresión) que son cola larga, no presencia real en el top.

### Top queries en V_actual

| Query | Clics | Impresiones | CTR | Pos. |
|---|---:|---:|---:|---:|
| passas | 2 | 106 | 1,9% | 4,7 |
| servicios de verificación otp con cumplimiento rgpd y hosting en la ue | 0 | 97 | 0,0% | 5,9 |
| due diligence tecnológica | 0 | 35 | 0,0% | 39,1 |
| cuanto cuesta un contencioso administrativo | 0 | 24 | 0,0% | 8,0 |
| honorarios abogado recurso contencioso administrativo | 0 | 22 | 0,0% | 8,3 |
| precio abogado contencioso administrativo | 0 | 20 | 0,0% | 12,2 |
| cuanto cuesta un recurso contencioso administrativo | 1 | 19 | 5,3% | 7,3 |
| precio abogado recurso contencioso administrativo | 0 | 19 | 0,0% | 13,7 |
| asesoramiento legal ai act | 0 | 18 | 0,0% | 60,1 |
| chat control 1.0 | 0 | 17 | 0,0% | 8,9 |
| chat control cuando entra en vigor | 0 | 17 | 0,0% | 6,0 |
| honorarios abogado contencioso administrativo | 0 | 17 | 0,0% | 8,0 |
| abogados ai act | 0 | 16 | 0,0% | 32,9 |
| cuanto tarda en llegar un burofax de un abogado | 0 | 15 | 0,0% | 9,3 |
| checklist cumplimiento ai act | 0 | 14 | 0,0% | 18,1 |
| ¿qué tipo de gastos hipotecarios están previstos que cambien de cara a 2026? | 0 | 14 | 0,0% | 7,6 |
| due diligence legal ronda inversión startup | 0 | 13 | 0,0% | 4,9 |
| despliegue de inteligencia artificial | 0 | 12 | 0,0% | 35,7 |
| precio contencioso administrativo | 0 | 12 | 0,0% | 6,8 |
| que hacer si un ayuntamiento no me paga | 0 | 12 | 0,0% | 10,9 |
| recurso contencioso administrativo precio | 0 | 11 | 0,0% | 6,8 |
| intereses de demora ayuntamientos | 0 | 10 | 0,0% | 31,9 |
| abogados documentación técnica | 0 | 8 | 0,0% | 85,9 |
| cuanto tiempo tengo para contestar un burofax | 0 | 8 | 0,0% | 9,6 |
| compliance inteligencia artificial españa | 0 | 7 | 0,0% | 35,6 |

### Contencioso (contencioso, alzada)

Términos: `contencioso`, `alzada`. **Total**: 1 clics, 241 impresiones.

| Query | URL | Clics | Impr. | Pos. |
|---|---|---:|---:|---:|
| cuanto cuesta un contencioso administrativo | `/servicios/litigacion-juicio-administrativo` | 0 | 22 | 8,3 |
| honorarios abogado recurso contencioso administrativo | `/servicios/litigacion-juicio-administrativo` | 0 | 22 | 8,3 |
| cuanto cuesta un recurso contencioso administrativo | `/servicios/litigacion-juicio-administrativo` | 0 | 18 | 10,0 |
| honorarios abogado recurso contencioso administrativo | `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 0 | 18 | 22,7 |
| cuanto cuesta un recurso contencioso administrativo | `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 1 | 17 | 8,5 |
| honorarios abogado contencioso administrativo | `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 0 | 17 | 15,1 |
| honorarios abogado contencioso administrativo | `/servicios/litigacion-juicio-administrativo` | 0 | 16 | 7,9 |
| precio abogado contencioso administrativo | `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 0 | 11 | 10,4 |
| precio contencioso administrativo | `/servicios/litigacion-juicio-administrativo` | 0 | 11 | 9,2 |
| precio abogado recurso contencioso administrativo | `/servicios/litigacion-juicio-administrativo` | 0 | 10 | 8,2 |
| precio contencioso administrativo | `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 0 | 10 | 8,1 |
| precio abogado contencioso administrativo | `/servicios/litigacion-juicio-administrativo` | 0 | 9 | 14,4 |
| precio abogado recurso contencioso administrativo | `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 0 | 9 | 19,9 |
| recurso contencioso administrativo precio | `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 0 | 9 | 8,6 |
| recurso contencioso administrativo precio | `/servicios/litigacion-juicio-administrativo` | 0 | 9 | 9,4 |

**Reparto por URL** (impresiones vs. clics — canibalización):

| URL | Clics | Impresiones |
|---|---:|---:|
| `/servicios/litigacion-juicio-administrativo` | 0 | 123 |
| `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 1 | 118 |

> **Canibalización**: las impresiones se concentran en `/servicios/litigacion-juicio-administrativo` pero los clics los recibe `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026`.

### Burofax

Términos: `burofax`. **Total**: 0 clics, 37 impresiones.

| Query | URL | Clics | Impr. | Pos. |
|---|---|---:|---:|---:|
| cuanto tarda en llegar un burofax de un abogado | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 15 | 9,3 |
| cuanto tiempo tengo para contestar un burofax | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 8 | 9,6 |
| plazo para contestar un burofax | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 6 | 9,5 |
| que significa recibir un burofax | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 3 | 9,0 |
| burofax correos | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 2 | 3,0 |
| consecuencias de recibir un burofax | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 1 | 9,0 |
| jurisprudencia burofax destinatario desconocido | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 1 | 3,0 |
| tipos de burofax | `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 1 | 2,0 |

**Reparto por URL** (impresiones vs. clics — canibalización):

| URL | Clics | Impresiones |
|---|---:|---:|
| `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 0 | 37 |

> Impresiones sin clics en el cluster; no puede evaluarse canibalización.

### AI Act / TechLaw

Términos: `ai act`, `ai-act`, `aiact`, `inteligencia artificial`, `digital omnibus`, `reglamento ia`, `ley de ia`. **Total**: 0 clics, 80 impresiones.

| Query | URL | Clics | Impr. | Pos. |
|---|---|---:|---:|---:|
| asesoramiento legal ai act | `/servicios/techlaw-ai-act-compliance` | 0 | 17 | 61,6 |
| abogados ai act | `/servicios/techlaw-ai-act-compliance` | 0 | 16 | 32,9 |
| checklist cumplimiento ai act | `/blog/checklist-ai-act-cumplimiento-empresas` | 0 | 14 | 18,1 |
| despliegue de inteligencia artificial | `/blog/responsable-del-despliegue-ai-act-obligaciones-2026` | 0 | 12 | 35,7 |
| compliance inteligencia artificial españa | `/servicios/techlaw-ai-act-compliance` | 0 | 7 | 35,6 |
| compliance en inteligencia artificial para empresas | `/servicios/techlaw-ai-act-compliance` | 0 | 2 | 12,0 |
| compliance inteligencia artificial empresas precio | `/servicios/techlaw-ai-act-compliance` | 0 | 2 | 7,0 |
| cómo cumplir el ai act sin contratar una consultora | `/servicios/techlaw-ai-act-compliance` | 0 | 2 | 13,0 |
| "regulation (eu) 2026/1744" ai act article 113 | `/en/blog/digital-omnibus-ai-act-final-text` | 0 | 1 | 10,0 |
| anexo iii ai act | `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | 0 | 1 | 44,0 |
| asesoramiento legal ai act | `/blog/cuanto-cuesta-abogado-startup-espana-precios-2026` | 0 | 1 | 35,0 |
| consultoría ai act | `/servicios/techlaw-ai-act-compliance` | 0 | 1 | 46,0 |
| consultoría para cumplir ley de ia | `/servicios/techlaw-ai-act-compliance` | 0 | 1 | 65,0 |
| gap analysis ai act empresa española | `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | 0 | 1 | 2,0 |
| software para cumplir ai act | `/servicios/techlaw-ai-act-compliance` | 0 | 1 | 30,0 |

**Reparto por URL** (impresiones vs. clics — canibalización):

| URL | Clics | Impresiones |
|---|---:|---:|
| `/servicios/techlaw-ai-act-compliance` | 0 | 49 |
| `/blog/checklist-ai-act-cumplimiento-empresas` | 0 | 14 |
| `/blog/responsable-del-despliegue-ai-act-obligaciones-2026` | 0 | 12 |
| `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | 0 | 2 |
| `/en/blog/digital-omnibus-ai-act-final-text` | 0 | 1 |
| `/blog/cuanto-cuesta-abogado-startup-espana-precios-2026` | 0 | 1 |
| `/autoevaluacion-ai-act` | 0 | 1 |

> Impresiones sin clics en el cluster; no puede evaluarse canibalización.

### Due diligence

Términos: `due diligence`, `due-diligence`. **Total**: 0 clics, 52 impresiones.

| Query | URL | Clics | Impr. | Pos. |
|---|---|---:|---:|---:|
| due diligence tecnológica | `/servicios/internacional-due-diligence-tech` | 0 | 35 | 39,1 |
| due diligence legal ronda inversión startup | `/servicios/internacional-due-diligence-tech` | 0 | 7 | 7,4 |
| due diligence legal ronda inversión startup | `/blog/due-diligence-legal-ronda-inversion-startup` | 0 | 6 | 2,0 |
| due diligence fiscal preventiva para ronda | `/blog/due-diligence-legal-ronda-inversion-startup` | 0 | 2 | 12,5 |
| tech due diligence | `/servicios/internacional-due-diligence-tech` | 0 | 2 | 25,0 |

**Reparto por URL** (impresiones vs. clics — canibalización):

| URL | Clics | Impresiones |
|---|---:|---:|
| `/servicios/internacional-due-diligence-tech` | 0 | 44 |
| `/blog/due-diligence-legal-ronda-inversion-startup` | 0 | 8 |

> Impresiones sin clics en el cluster; no puede evaluarse canibalización.

### Chat control

Términos: `chat control`, `chat-control`. **Total**: 0 clics, 43 impresiones.

| Query | URL | Clics | Impr. | Pos. |
|---|---|---:|---:|---:|
| chat control 1.0 | `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 17 | 8,9 |
| chat control cuando entra en vigor | `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 17 | 6,0 |
| cuando entra en vigor chat control | `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 6 | 8,3 |
| chat control 1 | `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 1 | 10,0 |
| chat control.1.0 | `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 1 | 9,0 |
| cuando entra en vigor el chat control | `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 1 | 7,0 |

**Reparto por URL** (impresiones vs. clics — canibalización):

| URL | Clics | Impresiones |
|---|---:|---:|
| `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 43 |

> Impresiones sin clics en el cluster; no puede evaluarse canibalización.

### Marca (passas)

Términos: `passas`. **Total**: 2 clics, 137 impresiones.

| Query | URL | Clics | Impr. | Pos. |
|---|---|---:|---:|---:|
| passas | `/en` | 0 | 70 | 5,6 |
| passas | `/` | 2 | 36 | 2,9 |
| passas | `/team/guillermo-passas-varo` | 0 | 20 | 6,1 |
| passas | `/servicios` | 0 | 7 | 5,0 |
| passas | `/blog` | 0 | 2 | 9,0 |
| passas | `/honorarios` | 0 | 1 | 2,0 |
| passas | `/servicios/internacional-spain-entry-pack` | 0 | 1 | 6,0 |

**Reparto por URL** (impresiones vs. clics — canibalización):

| URL | Clics | Impresiones |
|---|---:|---:|
| `/en` | 0 | 70 |
| `/` | 2 | 36 |
| `/team/guillermo-passas-varo` | 0 | 20 |
| `/servicios` | 0 | 7 |
| `/blog` | 0 | 2 |
| `/honorarios` | 0 | 1 |
| `/servicios/internacional-spain-entry-pack` | 0 | 1 |

> **Canibalización**: las impresiones se concentran en `/en` pero los clics los recibe `/`.

## 5. Dispositivo y país

| Dispositivo | Clics | Impresiones | CTR | Pos. |
|---|---:|---:|---:|---:|
| DESKTOP | 17 | 2.786 | 0,6% | 10,3 |
| MOBILE | 24 | 2.161 | 1,1% | 6,6 |
| TABLET | 0 | 29 | 0,0% | 5,8 |
| **Total** | **41** | **4.976** | | |

| País | Clics | Impresiones | CTR | Pos. |
|---|---:|---:|---:|---:|
| España | 35 | 3.411 | 1,0% | 9,6 |
| EE. UU. | 0 | 820 | 0,0% | 6,1 |
| gbr | 1 | 187 | 0,5% | 7,2 |
| deu | 0 | 72 | 0,0% | 5,5 |
| nld | 0 | 69 | 0,0% | 5,5 |
| mex | 1 | 36 | 2,8% | 9,9 |
| arg | 0 | 27 | 0,0% | 6,2 |
| col | 0 | 19 | 0,0% | 4,4 |
| can | 0 | 18 | 0,0% | 4,4 |
| ita | 0 | 17 | 0,0% | 4,2 |
| bel | 0 | 15 | 0,0% | 7,9 |
| are | 0 | 14 | 0,0% | 6,3 |
| bra | 0 | 13 | 0,0% | 17,4 |
| per | 0 | 13 | 0,0% | 6,2 |
| pol | 0 | 13 | 0,0% | 5,5 |
| **Total** | **41** | **4.976** | | |

**Cuadre**: device y country suman ambos 41 clics / 4.976 impresiones, **exactamente igual** que la referencia `date`. Ambas tablas suman su total sin pérdida.

### Aspecto en la búsqueda (searchAppearance)

La API no devuelve filas de `searchAppearance` en esta ventana.

## 6. Cruce con Analyze

Ventana V_cruce: 2026-08-30 → 2026-09-08. Analyze (contexto): 30 ago → 11 sep, sesiones con referrer google.com.

> **Las ventanas no son idénticas** (Analyze llega al 11 sep; GSC solo hasta F). La comparación es indicativa, no una conciliación exacta.

### Clics GSC por página en V_cruce

| URL | Clics | Impresiones |
|---|---:|---:|
| `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | 7 | 627 |
| `/` | 5 | 56 |
| `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | 5 | 755 |
| `/team/guillermo-passas-varo` | 3 | 31 |
| `/blog/cuanto-cuesta-abogado-startup-espana-precios-2026` | 2 | 46 |
| `/autoevaluacion-ai-act` | 1 | 28 |
| `/blog/administrador-responsabilidad-personal-ia-empresa-lsc-236` | 1 | 16 |
| `/blog/ayuntamiento-no-paga-factura-intereses-demora-reclamar` | 1 | 177 |
| `/blog/checklist-ai-act-cumplimiento-empresas` | 1 | 189 |
| `/blog/como-reclamar-una-factura-de-hasta-2000-euros-sin-abogado-guia-2026` | 1 | 11 |
| `/blog/derivacion-responsabilidad-tributaria-administrador-2026` | 1 | 70 |
| `/blog/estafa-o-incumplimiento-de-contrato-como-distinguirlo-en-2026` | 1 | 27 |
| `/blog/la-empresa-que-me-debe-dinero-es-insolvente-puedo-reclamar-al-administrador-personalmente-guia-2026` | 1 | 2 |
| `/servicios/internacional-spain-entry-pack` | 1 | 8 |
| `/servicios/litigacion-juicio-administrativo` | 1 | 222 |
| `/team/david-sanchez-lorenzo` | 1 | 22 |
| `/blog` | 0 | 8 |
| `/blog/ai-act-startups-espana-obligaciones-agosto-2026` | 0 | 1 |
| `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | 0 | 85 |
| `/blog/como-salir-de-asnef-en-2026-sin-abogados-guia-paso-a-paso-y-modelo-de-reclamacion-gratuito` | 0 | 3 |
| `/blog/consultar-estado-juicio-andalucia-2026` | 0 | 3 |
| `/blog/cuando-necesitas-abogado-en-un-monitorio-los-tres-momentos-en-que-ir-solo-es-un-error` | 0 | 4 |
| `/blog/cuando-necesitas-abogado-test-ocho-preguntas` | 0 | 49 |
| `/blog/cuando-necesitas-abogado-test-ocho-preguntas?efe235d7_page=3` | 0 | 2 |
| `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | 0 | 15 |

### Aviso: las consultas de dos dimensiones pierden clics

| Consulta | Clics | Impresiones |
|---|---:|---:|
| Sin dimensiones (referencia) | 33 | 3.584 |
| `page` (una dimensión) | 33 | 3.794 |
| `page` × `country` (dos dimensiones) | 3 | 563 |
| `page` × `device` (dos dimensiones) | 3 | 563 |

> **Esta tabla no suma su total, y la razón importa**: al cruzar dos dimensiones Google anonimiza de forma agresiva y aquí se pierde el **91%** de los clics (33 → 3). Por eso **la pregunta clave NO se responde con `page`×`country`**: se responde con consultas de una sola dimensión y filtro de país, que no sufren esa pérdida.

### Pregunta clave: ¿hay clics de EE. UU. en ASNEF, estafa y burofax?

| País (filtro, una dimensión) | Clics | Impresiones |
|---|---:|---:|
| EE. UU. | 0 | 496 |
| España | 30 | 2.520 |
| **Total del sitio** | **33** | **3.584** |

**Verificado**: en V_cruce GSC registra **0 clics desde EE. UU. en todo el sitio** (sobre 496 impresiones). Si no hay ningún clic estadounidense en ninguna página, no puede haberlo en ASNEF, estafa ni burofax. La respuesta es **no**.

De las 8 páginas con impresiones desde EE. UU., 1 pertenece(n) a esos tres temas:

| URL | Clics | Impresiones |
|---|---:|---:|
| `/blog/estafa-voz-clonada-ia-banco-devolucion-dinero` | 0 | 1 |

**Conclusión**: las 10 sesiones de EE. UU. que Analyze atribuye a `google.com` **no son clics de la Búsqueda de Google**. Hipótesis compatibles, no verificadas aquí: tráfico automatizado, `referrer` falsificado, o servicios de Google distintos de la Búsqueda.

### Reparto por dispositivo en V_cruce (top páginas)

| URL | Dispositivo | Clics | Impresiones |
|---|---|---:|---:|
| `/` | DESKTOP | 1 | 4 |
| `/` | MOBILE | 1 | 22 |
| `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | MOBILE | 1 | 25 |
| `/blog` | DESKTOP | 0 | 1 |
| `/blog/ayuntamiento-no-paga-factura-intereses-demora-reclamar` | DESKTOP | 0 | 27 |
| `/blog/ayuntamiento-no-paga-factura-intereses-demora-reclamar` | MOBILE | 0 | 2 |
| `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | DESKTOP | 0 | 2 |
| `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | MOBILE | 0 | 35 |
| `/blog/checklist-ai-act-cumplimiento-empresas` | DESKTOP | 0 | 15 |
| `/blog/checklist-ai-act-cumplimiento-empresas` | MOBILE | 0 | 1 |
| `/blog/cuando-necesitas-abogado-test-ocho-preguntas` | DESKTOP | 0 | 12 |
| `/blog/cuando-necesitas-abogado-test-ocho-preguntas` | MOBILE | 0 | 9 |
| `/blog/cuando-necesitas-abogado-test-ocho-preguntas?efe235d7_page=3` | DESKTOP | 0 | 1 |
| `/blog/cuanto-cuesta-abogado-startup-espana-precios-2026` | DESKTOP | 0 | 7 |
| `/blog/cuanto-cuesta-abogado-startup-espana-precios-2026` | TABLET | 0 | 1 |
| `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | DESKTOP | 0 | 57 |
| `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | DESKTOP | 0 | 3 |
| `/blog/due-diligence-legal-ronda-inversion-startup` | DESKTOP | 0 | 15 |
| `/blog/due-diligence-legal-ronda-inversion-startup` | MOBILE | 0 | 1 |
| `/blog/estafa-o-incumplimiento-de-contrato-como-distinguirlo-en-2026` | MOBILE | 0 | 4 |

### Contraste de magnitud

| Fuente | Medida | Total |
|---|---|---:|
| GSC (V_cruce) | clics | 33 |
| Analyze | sesiones, por página (listadas) | 40 + «resto 1 c/u» |
| Analyze | sesiones, por país | 43 |
| Analyze | sesiones, por dispositivo | 50 |

> **Los totales de Analyze no cuadran entre sí**: 40 (+resto) por página, 43 por país y 50 por dispositivo son tres cifras distintas para la misma ventana. Antes de comparar con GSC conviene resolver esa discrepancia en origen; aquí se reproducen tal como se recibieron.

> Además, **clic ≠ sesión** y las ventanas no coinciden, así que ninguna de estas cifras es directamente conciliable con la otra. Lo comparable es el **reparto relativo** por página, país y dispositivo, no el total.

### Reparto relativo: Analyze frente a GSC

| País | Sesiones Analyze | % Analyze | Clics GSC | % GSC |
|---|---:|---:|---:|---:|
| España | 33 | 76,7% | 3 | 100,0% |
| EE. UU. | 10 | 23,3% | 0 | 0,0% |

## 7. Indexación y sitemap

Origen de la lista de URLs: **inventario_local_webflow (sitemap.xml no accesible)**. Total inspeccionadas: **54**.

> **Límite de cobertura**: no se pudo descargar `passas.io/sitemap.xml` desde el entorno de ejecución, así que la lista procede del inventario local de Webflow (2026-07-27, **anterior a la migración del 9–11 sep**). Google declara **85 URLs enviadas** en el sitemap frente a las 54 inspeccionadas aquí: **la diferencia no está auditada en este informe**. Para cubrirla hay que reejecutar desde una red con acceso a `passas.io`.

| URL | coverageState | indexingState | Último rastreo | pageFetchState | googleCanonical vs userCanonical | Rich results |
|---|---|---|---|---|---|---|
| `/` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-09 | SUCCESSFUL | Google `https://passas.io` ≠ declarada `https://passas.io/` | NONE (—) |
| `/blog` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-19 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-07 | SUCCESSFUL | coinciden | NONE (—) |
| `/honorarios` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-07 | SUCCESSFUL | coinciden | NONE (—) |
| `/autoevaluacion-ai-act` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-26 | SUCCESSFUL | coinciden | NONE (—) |
| `/politica-de-inteligencia-artificial` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-06 | SUCCESSFUL | coinciden | NONE (—) |
| `/politica-de-cookies` | Discovered - currently not indexed ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/politica-de-privacidad` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-30 | SUCCESSFUL | coinciden | NONE (—) |
| `/terminos-y-condiciones` | Discovered - currently not indexed ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/aviso-legal` | Crawled - currently not indexed | INDEXING_STATE_UNSPECIFIED | 2026-09-06 | SUCCESSFUL | — | NONE (—) |
| `/blog/cuanto-cuesta-un-contencioso-administrativo-precios-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-05 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/chat-control-1-0-prorroga-enmiendas-cifrado-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-06 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/checklist-ai-act-cumplimiento-empresas` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-30 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/la-empresa-que-me-debe-dinero-es-insolvente-puedo-reclamar-al-administrador-personalmente-guia-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-29 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/te-reclaman-las-deudas-de-tu-empresa-guia-2026-para-el-administrador-social` | Submitted and indexed | INDEXING_ALLOWED | 2026-07-21 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/responsable-del-despliegue-ai-act-obligaciones-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-02 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/digital-omnibus-ai-act-2026-que-cambia-que-no` | Submitted and indexed | INDEXING_ALLOWED | 2026-07-24 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/el-masc-en-la-practica-que-tienes-que-hacer-antes-de-demandar-en-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-08 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/cuanto-cuesta-abogado-startup-espana-precios-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-06 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/estafa-o-incumplimiento-de-contrato-como-distinguirlo-en-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-06 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/ai-act-startups-espana-obligaciones-agosto-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-26 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/cuando-necesitas-abogado-en-un-monitorio-los-tres-momentos-en-que-ir-solo-es-un-error` | Submitted and indexed | INDEXING_ALLOWED | 2026-06-27 | SUCCESSFUL | Google `/blog/cuando-necesitas-abogado-en-un-monitorio-los-tres-momentos-en-que-ir-solo-es-un-error`; sin canonical declarada | NONE (—) |
| `/blog/consultar-estado-juicio-andalucia-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-07-19 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/me-ha-llegado-un-burofax-guia-de-actuacion-legal-y-pasos-a-seguir-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-05 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/como-reclamar-una-factura-de-hasta-2000-euros-sin-abogado-guia-2026` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-08 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/como-salir-de-asnef-en-2026-sin-abogados-guia-paso-a-paso-y-modelo-de-reclamacion-gratuito` | Submitted and indexed | INDEXING_ALLOWED | 2026-06-19 | SUCCESSFUL | Google `/blog/como-salir-de-asnef-en-2026-sin-abogados-guia-paso-a-paso-y-modelo-de-reclamacion-gratuito`; sin canonical declarada | NONE (—) |
| `/blog/gastos-hipoteca-2026-guia-legal-para-reclamar-plazos-y-modelo` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-27 | SUCCESSFUL | coinciden | NONE (—) |
| `/blog/exito-abogado-preventivo-etica` | Crawled - currently not indexed | INDEXING_ALLOWED | 2026-06-20 | SUCCESSFUL | Google `/blog/exito-abogado-preventivo-etica`; sin canonical declarada | NONE (—) |
| `/blog/la-consulta-juridica-gratuita-y-sus-consecuencias-reales-en-la-abogacia` | Crawled - currently not indexed | INDEXING_ALLOWED | 2026-06-13 | SUCCESSFUL | Google `/blog/la-consulta-juridica-gratuita-y-sus-consecuencias-reales-en-la-abogacia`; sin canonical declarada | NONE (—) |
| `/servicios/techlaw-ai-compliance-providers` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-07 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/internacional-due-diligence-tech` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-18 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/internacional-european-data-compliance` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-07 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/internacional-spain-entry-pack` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-27 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/litigacion-juicio-administrativo` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-11 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/litigacion-juicio-mercantil` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-08 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/litigacion-juicio-civil` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-08 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/techlaw-ai-act-alto-riesgo` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-26 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/techlaw-ai-act-compliance` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-30 | SUCCESSFUL | coinciden | NONE (—) |
| `/servicios/techlaw-founding-pack` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-08 | SUCCESSFUL | coinciden | NONE (—) |
| `/team/david-sanchez-lorenzo` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-26 | SUCCESSFUL | coinciden | NONE (—) |
| `/team/guillermo-passas-varo` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-26 | SUCCESSFUL | coinciden | NONE (—) |
| `/legal` | Crawled - currently not indexed | INDEXING_ALLOWED | 2026-05-30 | SUCCESSFUL | coinciden | NONE (—) |
| `/en/autoevaluacion-ai-act` | Submitted and indexed | INDEXING_ALLOWED | 2026-07-30 | SUCCESSFUL | coinciden | NONE (—) |
| `/legal-tools-tmp` | URL is unknown to Google ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/en/legal-tools/necesito-un-abogado` | Discovered - currently not indexed ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/en/legal-tools/te-compensa-abogado` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-07 | SUCCESSFUL | coinciden | NONE (—) |
| `/en/legal-tools/necesito-abogado-ia` | Discovered - currently not indexed ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/en/legal-tools/autoevaluacion-ai-act` | Submitted and indexed | INDEXING_ALLOWED | 2026-08-31 | SUCCESSFUL | coinciden | NONE (—) |
| `/en/legal-tools/do-i-need-a-lawyer` | URL is unknown to Google ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/en/legal-tools/is-a-lawyer-worth-it` | URL is unknown to Google ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/en/legal-tools/does-my-ai-need-a-lawyer` | URL is unknown to Google ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/en/legal-tools/ai-act-self-assessment` | URL is unknown to Google ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |
| `/en/servicios/commercial-litigation` | Submitted and indexed | INDEXING_ALLOWED | 2026-09-07 | SUCCESSFUL | coinciden | NONE (—) |
| `/en/team/guillermo-passas-varo` | Discovered - currently not indexed ⚠︎3x | INDEXING_STATE_UNSPECIFIED | — | PAGE_FETCH_STATE_UNSPECIFIED | — | NONE (—) |

> ⚠︎3x: 10 de 54 URL(s) devolvieron `unknown`/`discovered` (o estado vacío) en la primera consulta; se consultaron 3 veces y se reporta la **moda**, por ser ruido conocido de la API. El resto se consultó una sola vez.

### Sitemaps

| Sitemap | lastDownloaded | Errores | Avisos | URLs enviadas |
|---|---|---:|---:|---:|
| `https://passas.io/sitemap.xml` | 2026-09-07T10:19:36 | 0 | 0 | 85 |

> El campo `indexed` está deprecado (siempre 0) y se omite deliberadamente.

## 8. Tabla de vigilancia

| Señal | Valor en V_actual | Veredicto |
|---|---|---|
| Clics semanales | 22 / 13 / 20 clics (últimas semanas completas) | **sin dato suficiente** |
| Concentración en burofax | 6/41 clics = 15% | **confirma** |
| Marca «passas» en España | 2 clics, 31 impresiones, CTR 6,45% — consulta homónima, solo dato | **confirma** |
| Cluster contencioso | mejor posición 7,9 entre queries con ≥10 impresiones; 1 clic(s), 241 impr. en el cluster | **preocupa** |
| Servicios /en | 0 clics, 22 impresiones | **confirma** |
| Posición media | 8,64 | **sin dato suficiente** |
| Bloque TechLaw (ES+EN) | 4 clics, 1.375 impresiones (ES+EN) | **confirma** |
| Cobertura de query | 7,3% de clics y 15,7% de impresiones | **confirma** |

## 9. Hallazgos nuevos

_(máximo 5; cada uno marcado como verificado contra la API o como hipótesis)_

1. **[verificado]** **V_previa ha cambiado al recalcularla.** La misma ventana (2026-08-03 → 2026-08-24) da hoy 39 clics y 3.906 impresiones, frente a los 35 clics y 3.622 impresiones que citaba el informe del 25 ago: +4 clics y +284 impresiones. Los datos de GSC siguen consolidándose semanas después, así que **heredar cifras de un informe anterior introduce error**; conviene recalcular siempre.
2. **[verificado]** V_actual (2026-08-25 → 2026-09-08) cierra con 41 clics y 4.976 impresiones (CTR 0,82%, posición 8,64). Frente a V_previa recalculada: +2 clics y +1.070 impresiones, con el CTR cayendo 0,18 pp — más impresiones sin más clics.
3. **[verificado]** **Cero clics desde EE. UU. en todo el sitio** durante V_cruce (0 clics sobre 496 impresiones), medido con filtro de país sobre una sola dimensión. Las 10 sesiones estadounidenses que Analyze atribuye a `google.com` no pueden ser clics de la Búsqueda.
4. **[verificado]** **Las consultas de dos dimensiones no son utilizables para contar clics en esta propiedad.** En V_cruce, `page`×`country` devuelve 3 clics frente a los 33 reales: se pierde el 91% por anonimización. Cualquier reparto cruzado de este informe (y de los anteriores) describe una minoría de los clics; los totales fiables vienen de una sola dimensión.
5. **[hipótesis]** Los cambios de 7–11 sep (canonical v2, migración a `/legal-tools`, slugs EN nuevos con 301 pendientes) caen en el extremo final de la ventana o después de F = 2026-09-08, por lo que su efecto **aún no es medible**. Señal coherente con la hipótesis, no prueba: 5 URLs inspeccionadas siguen siendo «unknown to Google». Queda por confirmar en la próxima extracción.

---

Datos crudos: `gsc_raw_passas_2026-09-11.json` — 103 llamadas a la API, respuestas sin postprocesar.
