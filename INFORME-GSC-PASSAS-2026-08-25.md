---
title: "Cotejo e informe actualizado — passas.io — 25 de agosto de 2026"
fecha: "25 de agosto de 2026"
tipo: "Cotejo de dos documentos previos contra GSC en vivo + informe actualizado"
documentos_cotejados:
  - "INFORME-GSC-PASSAS-2026-08-24.md (informe del piloto)"
  - "respuestainformegsc-2026-08-24.md (respuesta correctiva)"
  - "DATOS-GSC-PASSAS-2026-08-03_2026-08-24.md (datos brutos)"
fuente: "API de Google Search Console, propiedad sc-domain:passas.io, consultada el 2026-08-25"
ventana: "2026-08-03 a 2026-08-24"
dimension_de_referencia: "date (salvo indicación expresa)"
cobertura_de_datos: "GSC tiene procesado hasta 2026-08-23"
---

# Cotejo e informe actualizado — passas.io — 25 de agosto de 2026

Este documento hace tres cosas: coteja el informe del 24 de agosto y su respuesta contra los
datos que la API de Search Console devuelve **hoy**, corrige lo que no se sostiene, y deja
registradas las limitaciones del proceso que hemos ido encontrando.

Todo lo que se afirma aquí procede de una consulta ejecutada el 25 de agosto de 2026 contra
`sc-domain:passas.io`. Los volcados JSON están en el repositorio. Donde no he podido verificar,
lo digo y explico por qué.

---

## 1. Lo primero: qué he podido comprobar y qué no

Antes de cualquier cifra conviene decir con qué he trabajado, porque condiciona todo lo demás.

| Fuente | Estado | Alcance |
|---|---|---|
| **API de Search Console** | ✅ Operativa | Rendimiento, indexación, sitemap — todo verificable |
| **HTML publicado de passas.io** | ❌ **Inaccesible** | El proxy de egress deniega el host (`CONNECT tunnel failed, 403`) |
| **MCP de Webflow** | ❌ Desconectado | Sin acceso a CMS, Page Settings ni Designer |

**Consecuencia directa:** las incidencias que dependen del HTML —T1 (canonical/hreflang), T2
(schema de servicios), T3 (FAQPage escapado), el CTA `href="#"`, el `hola@passas.io` del
footer— **no las he podido verificar en vivo**. Lo que sí he podido hacer es interrogar el
endpoint de inspección de URL, que devuelve lo que Google vio **en su último rastreo**. No es
lo mismo que el estado actual del sitio, y en §4 se ve por qué eso importa.

El resto del informe distingue explícitamente entre *verificado contra GSC*, *no verificable
desde esta sesión* y *pendiente de comprobación en vivo*.

---

## 2. Veredicto del cotejo, en una tabla

| # | Afirmación | Origen | Veredicto |
|---|---|---|---|
| 1 | Ventana previa: 29 clics / 4.104 impr / 0,71% / pos 7,73 | Informe | ✅ **Exacto** |
| 2 | Ventana actual: 35 clics | Informe | ✅ **Exacto** |
| 3 | Semana 16–22 ago: 23 clics / 1.277 impr / 1,80% | Informe | ✅ **Exacto** |
| 4 | Burofax = 60% de los clics del sitio | Informe | ✅ **Exacto** (21/35 = 60,0%) |
| 5 | Móvil 25 clics vs escritorio 9 | Informe | ✅ **Exacto** |
| 6 | Asimetría AI Act: ES pos 29 vs EN pos 7,4–7,7 | Respuesta §3.4 | ✅ **Confirmado** (29,1 vs 7,4 y 7,8) |
| 7 | Solo 1 de las páginas de servicio produjo clics | Respuesta §3.3 | ✅ **Confirmado** |
| 8 | Due diligence: consulta en pos 9,1 con 17 impr | Respuesta §3.5 | ✅ **Confirmado** |
| 9 | Cluster contencioso: 1.064 impr / 7 clics | Respuesta §3.1 | ✅ **Confirmado** (hoy 1.090 / 7) |
| 10 | Marca: 124 impr / 2 clics / 3,6% | Respuesta §3.6 | ✅ **Confirmado** (hoy 133 / 2 / 3,5%) |
| 11 | Ventana actual: 3.458 impresiones | Informe | ⚠️ **Desactualizado** → 3.622 |
| 12 | Locale EN: 553 impresiones | Informe | ⚠️ **Desactualizado** → 631 |
| 13 | «28% de las impresiones del sitio son internacionales» | Informe §1.5 | ⚠️ **Cambio de métrica a media frase** |
| 14 | «~350 impresiones/ventana de intención de precio» | Informe §4.2 → Respuesta §3.1 | ❌ **Sobrestimado ~90%** → 183 |
| 15 | Bloque TechLaw: 1 clic | Respuesta §3.3 | ❌ **Falso** → 0 clics |
| 16 | Tabla de bloques de negocio | Respuesta §3.3 | ❌ **No cuadra**: suma 3.660 sobre 3.458 |
| 17 | «Son estados distintos y merecía una nota» (T4) | Respuesta §2.6 | ❌ **Refutado**: es ruido de la API |

Cuatro cosas nuevas que ninguno de los dos documentos tenía aparecen en §5.

---

## 3. Lo que se sostiene

Conviene decirlo antes de las correcciones, porque es la mayor parte.

**El armazón cuantitativo del informe es sólido.** Clics de ventana (35), ventana previa
completa (29 / 4.104 / 0,71% / 7,73), la semana de la inflexión (23 clics / 1.277 impresiones
/ 1,80%), el reparto por dispositivo y la concentración del burofax en el 60% de los clics
reproducen **exactos** contra la API un día después. Quien extrajo esos datos lo hizo bien.

**Las cuatro lecturas que la respuesta salvó, se salvan.** El burofax como motor y no
escaparate, la entrada del locale inglés como cambio estructural del mes, la demanda de AI Act
que aparece después del 2 de agosto y no decae, y la asimetría móvil/escritorio por tercera
ventana. Las cuatro siguen en pie.

**Y la mejor aportación de la respuesta también se sostiene, con datos frescos.** La asimetría
ES/EN del AI Act (§3.4) era el hallazgo más accionable de aquel documento y hoy es más nítido:

| Página | Posición | Impresiones |
|---|---:|---:|
| `/servicios/techlaw-ai-act-compliance` (ES) | **29,1** | 180 |
| `/en/servicios/ai-act-compliance` (EN) | **7,8** | 28 |
| `/en/servicios/ai-act-high-risk` (EN) | **7,4** | 23 |

Veintiuna posiciones de diferencia sobre contenido equivalente. El volumen inglés sigue siendo
pequeño y parte viene de marca contaminada, así que la lectura es indicativa —como decía la
respuesta— pero la magnitud no es ruido. **La inversión SEO en AI Act rinde antes en inglés.**

Igual de firme: de las 20 páginas de servicio, **solo una produjo clics** en la ventana
(`/servicios/litigacion-juicio-administrativo`, 3 clics). Y solo 14 de las 20 recibieron
siquiera una impresión.

---

## 4. Lo que hay que corregir

### 4.1 Las impresiones de la ventana han subido, y eso cambia un porcentaje

El informe declaró 3.458 impresiones advirtiendo que el 22 de agosto estaba incompleto y que
el 23 y el 24 no existían. Hoy GSC tiene procesado hasta el **23 de agosto**:

| Medición | Clics | Impresiones | CTR |
|---|---:|---:|---:|
| Informe (extracción 24 ago) | 35 | 3.458 | 1,01% |
| Recuento hoy (25 ago) | 35 | **3.622** | 0,97% |

El 23 de agosto aportó 164 impresiones y **0 clics**. No es un error del informe: es la
latencia haciendo su trabajo. Pero obliga a fechar las cifras (§6.4).

**Lo que sí conviene corregir es un cambio de métrica.** El punto 5 del resumen ejecutivo dice
que la versión inglesa «ya suma 553 impresiones en la ventana (**28% de las impresiones del
sitio son ya internacionales**, frente al 17,6% de la ventana previa)». El paréntesis cambia de
métrica a media frase: 553 impresiones son las de las **páginas `/en`**; el 28% es la cuota de
impresiones **desde fuera de España**, que incluye tráfico a páginas españolas. Son dos cosas
distintas y la frase las encadena como si fueran la misma.

Los números correctos, hoy:

- Páginas `/en`: **631 impresiones = 17,4%** de las impresiones del sitio.
- Impresiones desde fuera de España: 28% (esa cifra sí era correcta, en §4.4).

El locale inglés es un sexto del sitio, no un cuarto.

### 4.2 Las «~350 impresiones de intención de precio» no existen

Es el error con más recorrido, porque **pasó del informe a la respuesta sin que nadie lo
recontara**. El informe lo usa en §4.2 para declarar el cluster contencioso «la oportunidad
nº 1 del sitio»; la respuesta lo discute estratégicamente en §3.1 —y hace bien— pero **acepta
la cifra**.

Recuento sobre la tabla de consultas, con un filtro deliberadamente generoso (*cuánto cuesta,
precio, honorarios, coste, tarifa, arancel, cuánto vale, cuánto cobra*):

| Ámbito | Impresiones | Clics | Consultas |
|---|---:|---:|---:|
| Cluster contencioso | **183** | 0 | 14 |
| Sitio entero | 198 | 0 | 25 |

**183, no ~350.** La cifra del informe casi duplica lo observable. Y hay un matiz que la
agrava y que desarrollo en §5.1: la tabla de consultas solo cubre el 17,7% de las impresiones
del sitio, así que ni 183 ni 350 son «el volumen de intención de precio del cluster» — son *lo
que se puede ver de él*.

Esto no destruye el argumento de la respuesta en §3.1; lo refuerza. Si la respuesta sostenía
que mejorar posición en intención de precio puede no traducirse en encargos por encima de
10.000 €, con la mitad de volumen visible el caso es más fuerte todavía.

### 4.3 El bloque TechLaw tiene cero clics, y la tabla de bloques no cuadra

La respuesta §3.3 introduce el reparto por bloque de negocio —una regla excelente, que asumo—
pero su tabla tiene dos problemas.

**Problema 1: suma más que el total que dice repartir.**

> «Repartiendo las 3.458 impresiones de la ventana:»
> 2.280 + 630 + 450 + 300 = **3.660**

Doscientas dos impresiones de más sobre el total que declara distribuir.

**Problema 2: atribuye 1 clic a TechLaw.** No lo hay. Los 35 clics de la ventana están
íntegramente atribuidos, y ninguno cae en una página TechLaw ni de AI Act:

| Página | Clics | Bloque |
|---|---:|---|
| `/blog/me-ha-llegado-un-burofax-...` | 21 | Perfil A |
| `/blog/cuanto-cuesta-un-contencioso-...` | 4 | Perfil A |
| `/servicios/litigacion-juicio-administrativo` | 3 | Perfil A |
| `/team/guillermo-passas-varo` | 2 | Marca |
| `/blog/chat-control-1-0-...` | 1 | Perfil A |
| `/` | 1 | Marca |
| `/servicios` | 1 | Marca |
| `/team/david-sanchez-lorenzo` | 1 | Marca |
| `/en` | 1 | Perfil C |
| **Total** | **35** | |

Las 16 páginas de TechLaw y AI Act (ES y EN) suman **830 impresiones y 0 clics**.

**Reparto corregido** (dimensión `page`, total 3.840, suma cuadrada):

| Bloque | Impresiones | Clics | Pos. media |
|---|---:|---:|---:|
| Litigación y consumo ES (Perfil A) | 2.554 | **29** | 6,7 |
| Internacional / locale EN (Perfil C) | 631 | 1 | 7,3 |
| TechLaw ES (Perfil B) | 346 | **0** | 20,7 |
| Marca e institucional | 309 | 5 | 9,2 |
| **Total** | **3.840** | **35** | |

La conclusión estratégica de la respuesta no solo aguanta: sale reforzada. **El 82,9% de los
clics del sitio (29 de 35) salen del bloque de litigación de consumo, y el bloque TechLaw no
ha producido un solo clic en 830 impresiones.** En búsqueda orgánica, passas.io es hoy un sitio
de litigación de consumo en móvil con un catálogo TechLaw adosado sin visibilidad comercial.

### 4.4 T4: los dos veredictos no son «estados distintos». Es ruido de la API

Aquí la respuesta corrigió al informe y **se equivocó en la corrección**.

El informe registró que la API devolvió dos veredictos para la misma URL («Descubierta:
actualmente sin indexar» y «Google no reconoce esta URL») y los trató como equivalentes. La
respuesta §2.6 objetó: *«Son estados distintos y la discrepancia merecía una nota, no una
equiparación.»*

Lo he probado. Seis llamadas consecutivas por URL, con URLs de control:

| URL | 6 llamadas | Resultado |
|---|---|---|
| `/blog/responsable-del-despliegue-ai-act-obligaciones-2026` | 4× «Discovered» · 2× «unknown» | **INESTABLE** |
| `/en/servicios/commercial-litigation` | 4× «Discovered» · 2× «unknown» | **INESTABLE** |
| `/en/team/guillermo-passas-varo` | 4× «Discovered» · 2× «unknown» | **INESTABLE** |
| `/blog/exito-abogado-preventivo-etica` *(rastreada)* | 6× «Crawled - not indexed» | ESTABLE |
| `/honorarios` *(indexada)* | 6× «Submitted and indexed» | ESTABLE |

El patrón es limpio: **las URLs que Google nunca ha rastreado alternan de forma no
determinista entre los dos veredictos; las rastreadas son perfectamente estables.**

La discrepancia procede de la API, no de la URL. El informe acertó operativamente al
equipararlas (ambas significan «fuera del índice, nunca rastreada») aunque no supiera por qué;
la respuesta convirtió ruido en señal. **La regla correcta es consultar varias veces y reportar
la moda.**

Estado real hoy, por moda de 6 llamadas: `responsable-del-despliegue-ai-act-obligaciones-2026`
y `/en/team/guillermo-passas-varo` están en **«Discovered - currently not indexed»**, nunca
rastreadas. `/en/servicios/commercial-litigation`, igual. Sin cambios desde el informe: las
peticiones de indexación siguen pendientes.

### 4.5 T1 (canonical): el diagnóstico probablemente acierta, el método no lo demuestra

Este punto merece cuidado, porque es donde la respuesta no aplicó su propia regla.

La respuesta demolió —con razón— el uso de `curl` para diagnosticar schema (§2.1): contar
bloques `ld+json` en HTML sin ejecutar JavaScript no mide el schema de un sitio. Pero **T1 se
diagnosticó exactamente con el mismo método**: leyendo `<link rel="canonical">` y los bloques
`hreflang` del `<head>` servido por `curl`. La respuesta no lo señaló.

Lo que Google registra, en su último rastreo de cada URL:

| URL | Último rastreo | Canónica de Google | Canónica declarada |
|---|---|---|---|
| `/` | 25 ago | `/` | `/` |
| **`/en`** | **5 ago** | `/en` | **— ausente —** |
| `/blog` | 7 ago | `/blog` | `/blog` |
| **`/en/blog`** | **18 ago** | `/en/blog` | **— ausente —** |
| `/servicios` | 6 ago | `/servicios` | `/servicios` |
| `/en/servicios` | 9 ago | `/en/servicios` | `/en/servicios` |
| `/honorarios` | 31 jul | `/honorarios` | `/honorarios` |
| `/en/honorarios` | 9 ago | `/en/honorarios` | `/en/honorarios` |
| `/servicios/litigacion-juicio-administrativo` | 17 jul | (self) | (self) |
| `/en/servicios/administrative-litigation` | 9 ago | (self) | (self) |
| `/servicios/techlaw-ai-act-compliance` | 31 jul | (self) | (self) |
| `/en/servicios/ai-act-compliance` | 9 ago | (self) | (self) |
| `/team/guillermo-passas-varo` | 5 ago | (self) | (self) |

**Dos lecturas, y las dos importan.**

La primera **corrobora al informe**: de trece URLs, **exactamente dos se comportan distinto, y
son precisamente las dos que el informe señaló**. Todas las demás —españolas e inglesas—
declaran canónica propia y correcta. Que la anomalía esté localizada con esa precisión en
`/en` y `/en/blog` es la huella exacta de un canonical hardcodeado en Page Settings de Home y
de Blog. El diagnóstico y el arreglo propuesto (vaciar el campo, dejar actuar el Global
Canonical Tag) son casi con seguridad correctos.

La segunda **desmiente la descripción**. El informe afirma que `/en` declara
`<link href="https://passas.io" rel="canonical"/>` —la home española como canónica de la
inglesa—. Google no registra eso: registra **ausencia** de canónica declarada. No es lo mismo
un canonical mal apuntado que un canonical ausente.

¿Se contradicen? No necesariamente, y esta es la parte incómoda: **las dos fuentes miran
momentos distintos.** Google rastreó `/en` el 5 de agosto y `/en/blog` el 18; el informe hizo
`curl` el 24. Si algo cambió entre medias, ambas observaciones pueden ser ciertas y ninguna
describe hoy.

**No puedo cerrarlo desde esta sesión** porque el HTML en vivo está bloqueado (§1). Lo que sí
puedo afirmar con datos:

- `/en` y `/en/blog` están **indexadas, con veredicto PASS y canónica propia**. El riesgo que
  el informe calificó de «latente» sigue latente: no se ha materializado.
- La anomalía existe y está donde el informe dijo.
- **El arreglo propuesto es correcto y barato** (10 minutos). Hacerlo no requiere resolver esta
  discrepancia. Lo que sí requiere verificación en vivo es *cerrar* la incidencia después.

### 4.6 T2, T3 y los pendientes de la respuesta: no verificables desde aquí

La respuesta afirma haber resuelto el schema de la plantilla Services el 25 de agosto,
replicando el mecanismo de la plantilla Blog Posts, y haber arreglado el CTA `href="#"` de las
20 páginas de servicio. **No puedo confirmarlo ni desmentirlo**: exige leer el HTML publicado o
el CMS, y ambos están fuera de alcance (§1).

Tampoco puedo verificar lo que la respuesta deja abierto: el `hola@passas.io` del footer con
`href="#"`, el HtmlEmbed heredado que sirve JSON escapado como texto oculto en 19 artículos, ni
el estado del campo `faq` por servicio.

Queda **pendiente de verificación en vivo**, no resuelto. Y como el CTA del hero era —según la
propia respuesta— un enlace muerto en el único punto de conversión de las páginas que
monetizan, esa comprobación es la más urgente de todas.

---

## 5. Lo que ninguno de los dos documentos tenía

Cuatro hallazgos del cotejo. Los dos primeros afectan a cómo hay que leer cualquier informe
futuro.

### 5.1 La tabla de consultas cubre el 17,7% de las impresiones y el 8,6% de los clics

Los datos brutos advertían que «Google anonimiza las consultas de bajo volumen». Nadie lo
cuantificó. Consultando cada dimensión por separado, paginando hasta agotar filas:

| Dimensión | Filas | Clics | Impresiones |
|---|---:|---:|---:|
| `date` | 21 | 35 | 3.622 |
| `page` | 48 | 35 | 3.840 |
| **`query`** | 112 | **3** | **641** |
| `device` | 3 | 35 | 3.622 |
| `country` | 74 | 35 | 3.622 |

**El 82,3% de las impresiones y el 91,4% de los clics no tienen consulta asociada.** En la
ventana previa: 85,0% y 75,9%.

Esto reencuadra buena parte del análisis de ambos documentos. Las tablas de consultas de AI
Act, la contaminación de marca, la intención de precio del cluster: todo se construye sobre
menos de una quinta parte de las impresiones y **menos de una décima de los clics**. El
artículo del burofax se llevó 21 clics; la tabla de consultas atribuye a «burofax» exactamente
1.

No invalida las lecturas —una muestra sesgada hacia consultas de volumen sigue diciendo algo—
pero sí obliga a dos cosas: **declarar la cobertura cada vez** que se recomiende algo a partir
de consultas, y **no presentar un agregado de consultas como si fuera el total del cluster**,
que es justo lo que hizo la cifra de las ~350 impresiones.

### 5.2 Los totales cambian según la dimensión que consultes

`page` devuelve **3.840** impresiones; `date`, `device` y `country` devuelven **3.622**. Un
6,0% de diferencia sobre el mismo periodo y la misma propiedad.

Es comportamiento estructural de GSC, no un error de extracción. Pero significa que «la ventana
tuvo 3.458 impresiones» es una frase incompleta sin decir por qué dimensión se preguntó. Los
informes deben **fijar la dimensión de referencia** y declararla.

### 5.3 El campo `indexed` del endpoint de sitemaps es inútil

`GET /sitemaps` devuelve `submitted: 65, indexed: 0`. El campo está deprecado y siempre vale 0.
El «56 de 65 indexadas» del informe salió de recorrer las URLs una a una con el endpoint de
inspección, que es la única forma correcta —y conviene dejar constancia de que la vía rápida no
existe.

Sitemap al día: descargado por Google el **23 ago a las 18:33 UTC**, 65 URLs, **0 errores, 0
avisos**.

### 5.4 El 23 de agosto entró con 0 clics

Primer día completo posterior al informe: **164 impresiones, 0 clics, posición media 7,8**. Un
solo día no dice nada, y el 23 de agosto fue domingo. Pero es el primer dato de la ventana que
el informe fijó para vigilar (§8: «clics semanales ≥ 20 sostenido tras el retorno de
vacaciones») y conviene no perderlo de vista.

---

## 6. Reglas de método actualizadas

Las diez de la respuesta se mantienen. Añado dos correcciones y tres reglas nuevas, todas
nacidas de este cotejo.

**Corrección a la regla 1.** El escepticismo sobre `curl` sin JavaScript **se aplica también a
canonical y hreflang**, no solo a schema. Cualquier lectura del `<head>` por HTML crudo hereda
la advertencia. (§4.5)

**Corrección a la regla 6.** La diferencia entre «Discovered - currently not indexed» y «URL is
unknown to Google» **no es señal**: es ruido no determinista de la API en URLs nunca rastreadas.
Consultar varias veces y reportar la moda. (§4.4)

**Regla 11 — toda tabla de reparto debe sumar su total.** (§4.3)

**Regla 12 — no heredar cifras sin recontarlas.** Un número que pasa de un documento a otro sin
verificación se fosiliza. Las «~350 impresiones» sobrevivieron a una revisión crítica completa
porque el revisor discutió la conclusión sin auditar el dato. (§4.2)

**Regla 13 — declarar siempre la cobertura de la dimensión que se usa,** y fijar la dimensión de
referencia del informe. (§5.1, §5.2)

**Regla 14 — declarar qué fuentes estaban disponibles al generar el informe.** Un informe hecho
sin acceso al HTML no es un informe con menos hallazgos: es un informe cuyos hallazgos técnicos
son de segunda mano. Debe decirlo en la primera página. (§1)

---

## 7. Plan de acción

Reordenado según lo que este cotejo cambia. Lo que no cambia, no lo repito: el plan del informe
del 24 y las correcciones de la respuesta siguen vigentes en todo lo demás.

### Inmediato — verificación, no análisis

1. **Comprobar en vivo el CTA del hero de las 20 páginas de servicio.** La respuesta dice
   haberlo arreglado; es el único punto de conversión de las páginas que monetizan y era
   `href="#"`. Cinco minutos con acceso al sitio. **Es la comprobación más rentable del
   documento.**
2. **Comprobar el `hola@passas.io` del footer** (`href="#"` en todo el sitio según la
   respuesta, no detectado por el informe).
3. **Vaciar el canonical hardcodeado de Page Settings de Home y de Blog** (T1). El arreglo es
   correcto aunque la discrepancia de §4.5 no esté cerrada, y cuesta 10 minutos. Verificar
   después que `/en` emite canónica a `/en`.
4. **Solicitar indexación** de `responsable-del-despliegue-ai-act-obligaciones-2026`,
   `/en/servicios/commercial-litigation` y `/en/team/guillermo-passas-varo`. Siguen fuera del
   índice y nunca rastreadas.

### Donde está el dinero — sin cambios de fondo

5. **AI Act: empezar por el locale inglés.** Es la mejor lectura de la respuesta y hoy es más
   nítida (§3): 21 posiciones de diferencia sobre contenido equivalente. Antes de invertir en
   posicionar `/servicios/techlaw-ai-act-compliance` desde la posición 29, dar contenido de
   apoyo en inglés a las páginas EN que ya rondan la posición 7.
6. **Replicar el patrón burofax** con artículos de urgencia inmediata. El bloque de litigación
   de consumo produce el 82,9% de los clics del sitio; es el único formato con CTR demostrado
   por encima del 2% en este dominio.
7. **Cluster contencioso: rebajar la prioridad, no abandonarlo.** Con 183 impresiones visibles
   de intención de precio en lugar de ~350, y con la reserva de §5.1 sobre cobertura, el caso
   de la respuesta (§3.1) para desplazar el esfuerzo hacia intención de urgencia gana peso.
   Resolver la canibalización sigue siendo correcto; declararlo «la oportunidad nº 1 del sitio»
   ya no.
8. **Due diligence tech**, tal como propuso la respuesta (§3.5): confirmado en posición 9,1 con
   17 impresiones, Perfil B, ticket de 5.000 €. Más cerca de página 1 que cualquier consulta de
   AI Act en español.

### No hacer

- No perseguir el CTR global.
- No tocar `gastos-hipoteca`.
- No replantear las decisiones estratégicas del 3 de julio.
- **No volver a presentar cifras de consultas sin declarar su cobertura.**

---

## 8. Qué vigilar en la próxima ventana (revisión ~14 sep)

La tabla del informe del 24 sigue siendo buena. Le añado tres filas y corrijo un umbral.

| Señal | Confirma | Preocupa |
|---|---|---|
| Clics semanales | ≥ 20/semana sostenido | Vuelta a < 10 |
| Concentración en burofax | Baja del 60% porque suben otros | Sube del 60% |
| Marca «passas» en España | CTR > 0 tras arreglar T1 | Otra ventana con 0 clics |
| Cluster contencioso | Alguna URL entra en top 5 | Sigue en 7-12 una 3.ª ventana |
| Páginas de servicio con schema | Rich Results Test en verde | Sigue sin JSON-LD |
| Servicios `/en` | Empiezan a recibir impresiones | Sigue siendo solo blog + home |
| Posición media | Se estabiliza en 7-8 | Sube de 9 |
| **Bloque TechLaw (ES+EN)** | **Primer clic en 830+ impresiones** | **Otra ventana con 0 clics** |
| **CTA de servicios** | **Verificado apuntando al calendario** | **Sigue sin verificar** |
| **Cobertura de la dimensión `query`** | **Se declara en el informe** | **Vuelve a omitirse** |

---

## 9. Nota final sobre el proceso

Los tres documentos —informe, respuesta y este cotejo— dibujan un patrón que conviene nombrar.

El informe hizo bien la extracción y mal la verificación técnica: usó `curl` sin JavaScript
para diagnosticar el `<head>` y el schema, y elevó a incidencia alta cosas ya cerradas.

La respuesta corrigió con acierto casi todo eso, e introdujo la mejor idea de la serie —el
reparto por bloque de negocio, la asimetría entre locales—. Pero cometió el mismo tipo de error
que denunciaba: no aplicó su regla del `curl` a T1, aceptó sin recontar la cifra de las ~350
impresiones, y su tabla de bloques no suma. Corregir un método con el rigor del método
corregido es más difícil de lo que parece.

Este cotejo tampoco está a salvo. Se ha hecho **sin acceso al HTML publicado ni al CMS**, así
que todo lo que dice sobre el estado técnico del sitio depende de lo que Google rastreó hace
entre siete y treinta y nueve días. Lo he declarado en §1 y lo repito aquí porque es
exactamente el tipo de limitación que, no declarada, se convierte en el error de la siguiente
iteración.

La conclusión operativa es simple: **cada informe debe abrir diciendo con qué fuentes se hizo,
y cerrar diciendo qué quedó sin verificar.**
