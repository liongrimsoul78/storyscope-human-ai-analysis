# Vectores de prueba contractuales — v0.3

**Proyecto:** StoryScope Human–AI Analysis
**Fase:** 1.22 — auditoría de coherencia del contrato y cierre de la ruta §4
**Estado:** casos documentales; **no** es una suite ejecutable
**Fecha:** 2026-11-19
**Contrato:** `COMPATIBILITY_EXPORT_CONTRACT_v0.3.md`
**Matriz:** `COMPATIBILITY_MAPPING_MATRIX_v0.3.md`
**Predecesores preservados:** `COMPATIBILITY_TEST_VECTORS_v0.1.md`, `COMPATIBILITY_TEST_VECTORS_v0.2.md`

Estos vectores fijan el comportamiento esperado **antes** de implementar el exportador. No contienen código, no se ejecutan y no sustituyen a las pruebas del motor.

---

## 1. Convenciones

- **Tipo de caso:** `real` cuando el valor, la característica o el ejemplo proviene de una fuente de `v0.2.3`; `sintético` cuando la fila se construye para el vector. Todo dato sintético se marca. Ningún dato sintético se presenta como observación real.
- **Versión del Registry:** salvo indicación contraria, `0.1.2-draft` (esquema `1.1.0`).
- **Origen:** salvo indicación contraria, `legacy_observation_origin` está declarado y el texto fuente está disponible.
- **Rutas:** `D` (§3 dimensión), `F` (§4 estándar), `F+` (característica con estado/dirección explícitos, extensión no estándar), `X` (ejecución/agregado).
- **Reversibilidad:** clases A/B/C/D del contrato §13.
- **Resultado:** `converted`, `converted_with_flag`, `preserved`, `quarantined`, `rejected`, o rechazo de ejecución.

**Resolución de definiciones.** El conjunto completo es de 70 vectores, distribuidos en la cadena de predecesores: **TV-01…TV-34** están definidos en `COMPATIBILITY_TEST_VECTORS_v0.1.md`; **TV-35…TV-56** en `COMPATIBILITY_TEST_VECTORS_v0.2.md`; **TV-57…TV-70** son nuevos de v0.3. Esta v0.3 redefine los casos que cambian de semántica (TV-03, TV-04, TV-08…TV-11, TV-17, TV-29, TV-40) y reproduce completos TV-35…TV-56. Cuando una definición aparece en más de un documento, **prevalece la de v0.3**. Un vector heredado sin redefinición conserva la definición de su documento de origen.

---

## 2. Vectores heredados revisados (TV-01…TV-34)

Los vectores TV-01 a TV-34 se conservan desde `COMPATIBILITY_TEST_VECTORS_v0.1.md`. La mayoría son casos de **ruta F+** (fila de característica que porta explícitamente estado y dirección). Esa ruta **no es la estándar** de `v0.2.3`; se mantiene para informes que hayan añadido esas columnas y para fijar las reglas de estado/dirección. Los cambios de v0.3 son:

- **TV-03** se mantiene `quarantined` (`CE-035`). Se corrige su presencia en la tabla de cobertura: ya no figura en «Conversión histórica fiel» ni en «`Presente–opuesto` con evidencia suficiente».
- **TV-04** se corrige: `Presente–opuesto` + `patrón IA` en unidireccional IA es una contradicción (R-07/§9.7); el vector pasa a `Presente–opuesto` + `patrón humano` con valor alternativo sintético no registrado. Se elimina el uso erróneo de `protagonist choice` bajo `Mode of Resolution`.
- **TV-08, TV-09, TV-10, TV-11** se reclasifican a **ruta D**: `Ausente`, `No aplicable` y `No evaluable` son estados de dimensión y no generan `EvidenceRecord`.
- **TV-17** se revisa: `Presente–alineado` + polo humano en bidireccional es R-04, que está **bloqueada**; el resultado pasa de `converted` a `quarantined` (`CE-021`).
- **TV-29** se revisa: `Presente–opuesto` unidireccional es **clase B**, no A, porque el token de dirección solo vive en `legacy_raw`.
- **TV-40** se revisa por la misma razón que TV-17: cuarentena (`CE-021`).
- **TV-14, TV-33** se mantienen: la etiqueta global y `analysis_quality_confidence` se preservan en `run_level`, sin escritura en el dominio.

### TV-03 — `Presente–opuesto` en bidireccional (cuarentena)

| Campo | Valor |
|---|---|
| Tipo | característica y opciones reales; fila sintética |
| Ruta | F+ |
| Fuente y estado de entrada | `Dominant Emotional Expression` (`categorical`); `Presente–opuesto` + `patrón humano`; valor observado `explicit labels` |
| Campos disponibles | cita con etiqueta emocional explícita, justificación, clúster `emotional_sensory_expression` |
| Campos ausentes | `Fuerza` |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-035`; payload literal preservado; **no** se emite `EvidenceRecord` |
| Justificación | dictamen v0.3: `Presente–opuesto` + `patrón humano` en bidireccional no es resoluble sin asumir referencia AI-first; la fuente histórica no declara qué polo es la referencia. La ruta F estándar (TV-58) sí puede convertir el mismo valor porque no interpreta un estado histórico. |
| Pérdida esperada | fila no convertida; revisión humana requerida |
| Reversibilidad | B |
| Matriz | M-08 |

### TV-04 — `Presente–opuesto` unidireccional con evidencia (corregido)

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética; valor alternativo sintético no registrado |
| Ruta | F+ |
| Fuente y estado de entrada | `Mode of Resolution` (`categorical option`, referencia IA `internal understanding`); `Presente–opuesto` + `patrón humano`; valor observado «external event» (alternativa sintética, no registrada) |
| Campos disponibles | cita literal de resolución por un evento externo, justificación |
| Campos ausentes | `observed_option_id` para la opción alternativa (no registrada); `Fuerza` |
| Tipo de característica | `categorical option` unidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `not_assessed`; `reference_pattern_id=null`; `opposed`; `observed_option_id=null`; `observed_value_text="external event"`; `CE-022`/`CE-026` |
| Justificación | `INV-A2-11`: en unidireccional, `opposed` no admite patrón; la opción alternativa no está registrada y la dirección histórica solo se preserva. `Presente–opuesto` + `patrón IA` habría sido una contradicción (R-07). |
| Pérdida esperada | la dirección histórica `patrón humano` solo queda en `legacy_raw` |
| Reversibilidad | B |
| Matriz | M-09 |

### TV-08 — `Ausente` de dimensión con oportunidad suficiente (ruta D)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | D |
| Fuente y estado de entrada | dimensión `Setting`; `Ausente`; ejecución `completo`; búsqueda declarada |
| Campos disponibles | motivo, alcance de búsqueda, longitud suficiente |
| Campos ausentes | `feature_id` (no aplica en §3) |
| Tipo de característica | no aplica (dimensión) |
| Evidencia y localización | `search_scope=full_text`; motivo |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.coverage_status=descriptive_assessed`; estado literal en informe; `CE-040`; **no** se emite `not_observed` |
| Justificación | ruta D: §3 no tiene `feature_id`; `Ausente` no se convierte en `not_observed` sin inventar una característica |
| Pérdida esperada | el token `Ausente` solo en el informe |
| Reversibilidad | B |
| Matriz | M-13 |

### TV-09 — `Ausente` de dimensión con oportunidad insuficiente (ruta D)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | D |
| Fuente y estado de entrada | misma dimensión que TV-08; `Ausente`; ejecución `fragmento` |
| Campos disponibles | estado, motivo |
| Campos ausentes | completitud |
| Tipo de característica | no aplica (dimensión) |
| Evidencia y localización | ninguna |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.coverage_status=partially_assessed`; estado literal en informe; `CE-013`; **no** se emite `not_evaluable` |
| Justificación | ruta D: la ausencia no sostenible no se convierte en estado atómico |
| Pérdida esperada | el token `Ausente` solo en el informe |
| Reversibilidad | B |
| Matriz | M-14 |

### TV-10 — `No aplicable` de dimensión (ruta D)

| Campo | Valor |
|---|---|
| Tipo | real (`evidence-status.md`, fila `No aplicable`: «Subtramas en una etiqueta de producto o un formulario») |
| Ruta | D |
| Fuente y estado de entrada | dimensión `Plot`; `No aplicable`; género «etiqueta de producto» |
| Campos disponibles | motivo de no aplicabilidad |
| Campos ausentes | cita de característica |
| Tipo de característica | no aplica (dimensión) |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.coverage_status=not_applicable`; estado literal en informe; **no** se emite `EvidenceRecord` |
| Justificación | ruta D; `coverage_status=not_applicable` es la representación exacta |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-15 |

### TV-11 — `No evaluable` de dimensión (ruta D)

| Campo | Valor |
|---|---|
| Tipo | real (`worked-examples/01-microrelato-21-palabras.md`: «son **No evaluable** por longitud y forma») |
| Ruta | D |
| Fuente y estado de entrada | microrelato de 21 palabras; dimensión `Plot`; `No evaluable` |
| Campos disponibles | motivo (longitud), longitud, género |
| Campos ausentes | cita de característica |
| Tipo de característica | no aplica (dimensión) |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.coverage_status=not_assessable`; estado literal en informe; **no** se emite `EvidenceRecord` |
| Justificación | ruta D; el ejemplo prohíbe tratar la falta como evidencia |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-16 |

### TV-17 — Bidireccional con polo humano observado (R-04 bloqueada)

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Ruta | F+ |
| Fuente y estado de entrada | `Reference Explicitness`; `Presente–alineado` + `patrón humano`; valor `balanced mix` |
| Campos disponibles | cita literal, justificación |
| Campos ausentes | `Fuerza` |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-021`; payload literal preservado; **no** se emite `EvidenceRecord` |
| Justificación | R-04 está bloqueada: la reexpresión como `opposed` bajo AI-first no está justificada por la guía de anotación. La ruta F estándar (TV-58) no interpreta el estado histórico y sí puede convertir el valor. |
| Pérdida esperada | fila no convertida |
| Reversibilidad | B |
| Matriz | M-04 |

### TV-29 — Reconstrucción del original (revisado)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F+ |
| Fuente y estado de entrada | (a) registro de TV-01; (b) registro de TV-04 con su informe de exportación |
| Campos disponibles | (a) solo registro + registry; (b) registro + `legacy_raw` |
| Campos ausentes | (a) ninguno; (b) nada, el informe está disponible |
| Tipo de característica | escala unidireccional / categórica unidireccional |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | (a) `Presente–alineado` + `patrón IA` sin el informe (clase A); (b) `Presente–opuesto` + `patrón humano` desde `legacy_raw` (clase B) |
| Justificación | clases A y B del contrato §13; `Presente–opuesto` unidireccional es B porque la dirección no está en el dominio |
| Pérdida esperada | ninguna con el informe; en (b) sin informe no hay reconstrucción de la dirección |
| Reversibilidad | A / B |
| Matriz | M-01 / M-09 |

### TV-40 — `Presente–alineado` + `patrón humano` en bidireccional (R-04 bloqueada)

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Ruta | F+ |
| Fuente y estado de entrada | `Reference Explicitness`; `Presente–alineado` + `patrón humano`; valor `balanced mix` |
| Campos disponibles | cita literal, justificación |
| Campos ausentes | — |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-021`; **no** se emite `EvidenceRecord` |
| Justificación | R-04 bloqueada (§16.2); no se adopta la reexpresión `Presente–alineado` + polo humano → `opposed` sin justificación de la guía |
| Pérdida esperada | fila no convertida |
| Reversibilidad | B |
| Matriz | M-04 |

---

## 3. Vectores de proyección y ejecución (TV-35…TV-56, revisados)

### TV-35 — Fila §3 de dimensión sin `feature_id`

| Campo | Valor |
|---|---|
| Tipo | real (estructura de `report-template.md` §3) |
| Ruta | D |
| Fuente y estado de entrada | dimensión `Social networks`; estado `Presente–alineado`; dirección `patrón humano`; sin `feature_id` |
| Campos disponibles | dimensión, observación, estado, dirección |
| Campos ausentes | `feature_id` (la dimensión no tiene características en el mapa central) |
| Tipo de característica | no aplica |
| Evidencia y localización | observación descriptiva |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.neutral_summary`; `limitations`; `coverage_status=descriptive_assessed`; `CE-029`; **no** se emite `EvidenceRecord` |
| Justificación | §8.1: un perfil descriptivo no se convierte en señal direccional; no se hace join con §4 |
| Pérdida esperada | no hay registro atómico |
| Reversibilidad | B |
| Matriz | M-28 / M-52 |

### TV-36 — Fila §4 de característica sin estado histórico explícito (corregido)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | fila de §4 con `Característica/valor observado` y cita, **sin** `Estado de evidencia` ni `Dirección` |
| Campos disponibles | característica, valor, cita, clúster |
| Campos ausentes | `legacy_state`, `legacy_direction` |
| Tipo de característica | `categorical` (ejemplo: `Dominant Emotional Expression`) |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `converted`; `observed`; alineación derivada del valor; **no** se rechaza por falta de estado; **no** se hereda estado de §3 |
| Justificación | §9.4: la ruta F deriva `observed` del valor explícito y el span; §4 no tiene estado y no se le exige |
| Pérdida esperada | ninguna si el valor mapea; si no, `not_assessed` |
| Reversibilidad | A |
| Matriz | M-43 / M-44 |

### TV-37 — Intento inválido de unir estados de §3 a features de §4

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | D/F |
| Fuente y estado de entrada | ejecución que intenta copiar el estado de la dimensión `Plot` a las features `Subplot Integration` y `Mode of Resolution` |
| Campos disponibles | estado de dimensión, features de §4 |
| Campos ausentes | — |
| Tipo de característica | varias |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected` para cada intento de join; `CE-029`/`CE-007`; no se emiten registros por dimensión |
| Justificación | §8: no existe join automático entre §3 y §4; §4 no hereda estado |
| Pérdida esperada | ninguna fila convertida por join |
| Reversibilidad | D |
| Matriz | M-28 / M-29 / M-52 |

### TV-38 — `Dirección del estudio` confundida con alineación observada

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | fila de §4 con `Dirección del estudio=AI`; el exportador intenta copiarla a `research_alignment` |
| Campos disponibles | valor, dirección del estudio, cita |
| Campos ausentes | dirección observada |
| Tipo de característica | cualquiera |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected` para la copia; `research_alignment` se resuelve desde el valor y el registro, no desde `Dirección del estudio`; `CE-006`/`CE-026` si no hay mapeo |
| Justificación | R-35; `report-template.md` §4 |
| Pérdida esperada | la dirección del estudio solo en `legacy_raw` |
| Reversibilidad | A |
| Matriz | M-33 |

### TV-39 — `Presente–opuesto` + `patrón humano` en bidireccional (F+)

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Ruta | F+ |
| Fuente y estado de entrada | `Reference Explicitness`; `Presente–opuesto` + `patrón humano`; valor `balanced mix` |
| Campos disponibles | cita literal, justificación, clúster `intertextuality` |
| Campos ausentes | — |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-035`; payload literal preservado |
| Justificación | dictamen v0.3: no resoluble sin asumir referencia AI-first |
| Pérdida esperada | fila no convertida |
| Reversibilidad | B |
| Matriz | M-08 |

### TV-41 — `Presente–opuesto` + `patrón IA` en bidireccional

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F+ |
| Fuente y estado de entrada | `Dominant Emotional Expression`; `Presente–opuesto` + `patrón IA`; valor `embodied` |
| Campos disponibles | cita literal, justificación |
| Campos ausentes | — |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `CE-007` |
| Justificación | contradicción directa: el valor se alinea con IA pero el estado dice polo alternativo |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-07 |

### TV-42 — Combinaciones contradictorias estado/dirección

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F+ |
| Fuente y estado de entrada | `Thematic Unity`; `Presente–alineado` + `patrón humano` (característica unidireccional IA) |
| Campos disponibles | estado, dirección |
| Campos ausentes | dirección coherente |
| Tipo de característica | `scale 1–5` unidireccional IA |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `CE-008` |
| Justificación | alineación declarada imposible para unidireccional |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-05 |

### TV-43 — `mixto` global sin campo run-level

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | X |
| Fuente y estado de entrada | etiqueta global `mixto`; dos registros en clústeres distintos; sin campo de alineación en `AnalysisRun` |
| Campos disponibles | etiqueta, registros |
| Campos ausentes | clúster único que justifique la síntesis; campo de alineación en `AnalysisRun` |
| Tipo de característica | ejecución |
| Evidencia y localización | `record_ids` |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `CE-015`; etiqueta en `run_level.legacy_global_label`; `written_to_domain=false` |
| Justificación | R-20; §17-B1: no se inventa campo |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-22 |

### TV-44 — Intento de transferir `mixto` global a `ClusterSummary`

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | X |
| Fuente y estado de entrada | etiqueta global `mixto`; exportador intenta escribir `ClusterSummary.alignment=mixed` por la simple existencia de dos `record_ids` con alineaciones distintas |
| Campos disponibles | etiqueta, registros |
| Campos ausentes | síntesis de clúster explícita |
| Tipo de característica | ejecución + clúster |
| Evidencia y localización | `record_ids` |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected` para esa escritura; `CE-015`; `ClusterSummary.alignment` solo se escribe con síntesis explícita |
| Justificación | R-20; `mixed` es propiedad de conjuntos con síntesis documentada |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-22 |

### TV-45 — Preservación de `analysis_quality_confidence`

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | X |
| Fuente y estado de entrada | ejecución con `analysis_quality_confidence=alta` y registros con `evidence_strength` variado |
| Campos disponibles | etiqueta, registros |
| Campos ausentes | — |
| Tipo de característica | ejecución |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `run_level.analysis_quality_confidence=alta`; **no** copia a `EvidenceRecord.assessment_confidence`; `assessment_confidence=not_rated`; R-23 |
| Justificación | `report-template.md` §6; Spec §5.3 |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-25 |

### TV-46 — `adequacy` no definido

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | X |
| Fuente y estado de entrada | ejecución con puerta `no apto` y etiqueta `evidencia insuficiente` |
| Campos disponibles | puerta, etiqueta |
| Campos ausentes | enum de `adequacy` en el destino |
| Tipo de característica | ejecución |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `CE-028`; etiqueta en `run_level.legacy_global_label`; `written_to_domain=false` |
| Justificación | §17-B2: no se inventa enum |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-23 |

### TV-47 — Dos observaciones distintas dentro de una fila

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | fila de §4 con valor observado principal + contraevidencia en la misma fila, con spans separados |
| Campos disponibles | valor, cita principal, contraevidencia con cita propia, justificación propia |
| Campos ausentes | — |
| Tipo de característica | `categorical` |
| Evidencia y localización | dos citas literales distintas |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | dos `EvidenceRecord` con `legacy_sublocator` `:obs:1` y `:obs:2`; clave de unicidad `(digest, sublocator)` |
| Justificación | §11.2: sublocalizador distingue observaciones |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-54 |

### TV-48 — Colisión de localizador

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | fila con dos observaciones que no pueden distinguirse por la regla determinista |
| Campos disponibles | ambas |
| Campos ausentes | criterio de desempate |
| Tipo de característica | cualquiera |
| Evidencia y localización | ambigua |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved` o revisión; `CE-037`; no se emite registro ambiguo |
| Justificación | §11.2: sin identidad estable, preservar o revisar |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-41 |

### TV-49 — Repetición de la misma localización fuente

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | la misma fila de §4 extraída dos veces (misma sección, mismo `row_index`, misma feature) |
| Campos disponibles | ambas completas |
| Campos ausentes | — |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | misma cita |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | un único registro; `CE-016` informativo; mismo `record_id`; clave `(digest, sublocator)` |
| Justificación | idempotencia por localización fuente |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-32 |

### TV-50 — Duplicados conflictivos en la misma localización

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | misma localización fuente, una extracción con valor `Presente–alineado` + `patrón IA` y otra con `Ausente` |
| Campos disponibles | ambas |
| Campos ausentes | resolución de la contradicción |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | la primera con cita; la segunda sin cita |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | ambas `quarantined`; `CE-016`; no se elige una |
| Justificación | el exportador no adjudica contradicciones de la fuente |
| Pérdida esperada | ninguna fila convertida |
| Reversibilidad | D |
| Matriz | M-32 |

### TV-51 — Origen histórico no documentado

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | X |
| Fuente y estado de entrada | ejecución sin `legacy_observation_origin` y sin atestación válida |
| Campos disponibles | filas completas |
| Campos ausentes | origen, atestación |
| Tipo de característica | ejecución |
| Evidencia y localización | no verificable |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | rechazo de ejecución; `CE-032`/`CE-036`; **ningún** registro emitido |
| Justificación | `observation_origin` obligatorio; procedencia no demostrable ni atestable |
| Pérdida esperada | ejecución no convertida |
| Reversibilidad | D |
| Matriz | M-38 / M-42 |

### TV-52 — Atestación de procedencia durante la migración

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | X |
| Fuente y estado de entrada | ejecución sin origen histórico, pero con atestación válida del operador |
| Campos disponibles | filas completas, atestación |
| Campos ausentes | origen histórico demostrado |
| Tipo de característica | ejecución |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | conversión permitida; `observation_origin` refleja la atestación; `migration_attestations` registra responsable, fecha, fundamento, versión de protocolo y autorización; `origin_detail` puede referenciar la atestación |
| Justificación | §11.6: atestación de migración es mecanismo externo con su propia procedencia |
| Pérdida esperada | ninguna |
| Reversibilidad | B |
| Matriz | M-38 |

### TV-53 — Neutralidad con dos lecturas posibles

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F+ |
| Fuente y estado de entrada | `Sensory Density`; `Presente–alineado` + `neutro`; justificación «no destaca» |
| Campos disponibles | estado, dirección, texto ambiguo |
| Campos ausentes | indicación de si hubo neutralización contextual o ausencia de patrón |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `CE-027` |
| Justificación | las dos lecturas de `neutro` producen destinos distintos; no se elige por defecto |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-20 |

### TV-54 — `Fuerza` fuera del vocabulario controlado

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | `Thematic Unity`; valor «4/5»; `Fuerza` = «muy fuerte» |
| Campos disponibles | valor, fuerza libre |
| Campos ausentes | regla documentada que vincule «muy fuerte» con `strong` |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `converted`; `evidence_strength=not_rated`; `CE-023`; valor literal preservado en `legacy_raw` |
| Justificación | §15.2: sin regla documentada, no se mapea |
| Pérdida esperada | intensidad original solo en procedencia |
| Reversibilidad | B |
| Matriz | M-34 |

### TV-55 — Evidencia sin span literal

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | `Sensory Density`; valor «alta»; «cita» parafraseada |
| Campos disponibles | paráfrasis, offsets aproximados |
| Campos ausentes | subcadena literal |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | no verificable |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-031` |
| Justificación | §5.4: sin normalización; la cita debe ser igual a `source_text[start:end]` |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-37 |

### TV-56 — Opción alternativa sin catálogo completo (F+)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F+ |
| Fuente y estado de entrada | `Agency in Resolution` (`categorical option`, referencia IA `protagonist choice`); `Presente–opuesto` + `patrón humano`; valor «external agency» (alternativa sintética, no registrada) |
| Campos disponibles | cita literal, justificación |
| Campos ausentes | `observed_option_id` para la opción alternativa; `Fuerza` |
| Tipo de característica | `categorical option` unidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `not_assessed`; `reference_pattern_id=null`; `opposed`; `observed_option_id=null`; `observed_value_text="external agency"`; `CE-022`/`CE-026` |
| Justificación | §9.3/R-09: en unidireccional, `Presente–opuesto` con valor alternativo no registrado se convierte sin patrón; la dirección histórica `patrón humano` solo se preserva en `legacy_raw` |
| Pérdida esperada | dirección histórica solo en procedencia |
| Reversibilidad | B |
| Matriz | M-09 |

---

## 4. Vectores nuevos de la ruta F estándar (TV-57…TV-70)

### TV-57 — §4 con valor que mapea al patrón de referencia (alineado)

| Campo | Valor |
|---|---|
| Tipo | característica y opción reales; fila sintética |
| Ruta | F |
| Fuente y estado de entrada | `Dominant Emotional Expression`; valor observado `embodied`; cita literal; sin estado histórico |
| Campos disponibles | valor, cita, justificación, clúster `emotional_sensory_expression` |
| Campos ausentes | `Fuerza`; `legacy_state` (no existe en §4) |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `converted`; `observed`; `pattern_ai`; `reference_pattern_id=ssha.pattern.dominant_emotional_expression.embodied`; `observed_option_id`=ese patrón; `aligned`; `reference_pattern`; `opportunity_status=sufficient`; `assessment_confidence=not_rated` |
| Justificación | §9.4: el valor mapea al patrón de referencia; no se usa `Dirección del estudio` |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-43 / M-44 |

### TV-58 — §4 con valor que mapea al polo humano registrado (opuesto)

| Campo | Valor |
|---|---|
| Tipo | característica y opción reales; fila sintética |
| Ruta | F |
| Fuente y estado de entrada | `Reference Explicitness`; valor observado `balanced mix`; cita literal; sin estado histórico |
| Campos disponibles | valor, cita, justificación |
| Campos ausentes | `legacy_state` |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `converted`; `observed`; `pattern_human`; `reference_pattern_id=ssha.pattern.reference_explicitness.balanced_mix`; `observed_option_id`=ese patrón; `opposed`; `reference_pattern` |
| Justificación | §9.4: el valor mapea a un patrón registrado distinto de la referencia; la referencia histórica es el patrón IA (Spec §5.3.5). **No** es R-04: no hay estado `Presente–alineado`; el valor es explícito. |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-45 |

### TV-59 — §4 con valor no registrado

| Campo | Valor |
|---|---|
| Tipo | característica real; valor sintético no registrado |
| Ruta | F |
| Fuente y estado de entrada | `Mode of Resolution`; valor observado «external event»; cita literal |
| Campos disponibles | valor, cita, justificación |
| Campos ausentes | patrón registrado para «external event» |
| Tipo de característica | `categorical option` unidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `converted`; `observed`; `not_assessed`; `reference_pattern_id=null`; `observed_option_id=null`; `observed_value_text="external event"`; `alignment_basis=none`; `CE-022` |
| Justificación | §9.4: opción no registrada no inventa ID |
| Pérdida esperada | falta `observed_option_id` |
| Reversibilidad | A |
| Matriz | M-46 |

### TV-60 — §4 de escala sin token direccional

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Ruta | F |
| Fuente y estado de entrada | `Thematic Unity`; valor observado «4/5»; cita literal; sin token direccional |
| Campos disponibles | valor, cita |
| Campos ausentes | token direccional; umbral por historia |
| Tipo de característica | `scale 1–5`; `overall_feature` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `converted`; `observed`; `not_assessed`; `reference_pattern_id=null`; `observed_option_id=null`; `observed_value_text="4/5"`; `CE-041` |
| Justificación | §9.4/R-42: el valor de escala no basta para afirmar alineación; no se comparan medias grupales |
| Pérdida esperada | alineación no afirmada |
| Reversibilidad | A |
| Matriz | M-47 |

### TV-61 — §4 de escala con token direccional explícito

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Ruta | F |
| Fuente y estado de entrada | `Thematic Unity`; valor observado «alto, patrón IA»; cita literal |
| Campos disponibles | valor con token explícito, cita |
| Campos ausentes | — |
| Tipo de característica | `scale 1–5`; `overall_feature` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `converted`; `observed`; `pattern_ai`; `reference_pattern_id=ssha.pattern.thematic_unity.overall`; `aligned`; `alignment_basis=reference_pattern`; `alignment_basis_detail` cita el token explícito |
| Justificación | §9.4/R-42: la alineación solo se afirma con token direccional explícito en la fila |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-44 / M-47 |

### TV-62 — §4 con contraevidencia sin span propio

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | `Subplot Integration`; valor `no_subplots`; `Contraevidencia real` = «hay una subtrama paralela», sin cita propia |
| Campos disponibles | valor, cita principal, texto de contraevidencia |
| Campos ausentes | span propio de la contraevidencia |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita principal; contraevidencia sin cita |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined` para la contraevidencia; `CE-009`; la observación principal puede convertirse por separado si su span es válido |
| Justificación | §11.5: la contraevidencia no reutiliza la cita principal por defecto |
| Pérdida esperada | contraevidencia no emitida |
| Reversibilidad | D |
| Matriz | M-48 |

### TV-63 — §4 con contraevidencia con span y justificación propios

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | `Subplot Integration`; valor `no_subplots`; `Contraevidencia real` = «una subtrama paralela» con cita propia y justificación |
| Campos disponibles | valor, cita principal, cita de contraevidencia, justificación |
| Campos ausentes | — |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | dos citas literales distintas |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | dos `EvidenceRecord`: principal `observed` + `pattern_ai` + `aligned` (`no_subplots`); contraevidencia `observed` + `pattern_human` + `reference_pattern_id=thematically_parallel` + `opposed`; `:obs:1`/`:obs:2`; `counterevidence_record_ids` enlaza ambos |
| Justificación | §9.4/R-F08: contraevidencia afirmativa con span y justificación propios |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-49 / M-54 |

### TV-64 — §4 con contraevidencia que reutiliza la cita principal

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | `Subplot Integration`; `Contraevidencia real` cita exactamente la misma frase que la observación principal, sin justificación independiente |
| Campos disponibles | valor, cita principal, texto de contraevidencia |
| Campos ausentes | justificación independiente |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | una sola cita reutilizada |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined` para la contraevidencia; `CE-039` |
| Justificación | §11.5: no se reutiliza la cita principal por defecto |
| Pérdida esperada | contraevidencia no emitida |
| Reversibilidad | D |
| Matriz | M-48 |

### TV-65 — §3 `Ausente` (ruta D)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | D |
| Fuente y estado de entrada | dimensión `Setting`; `Ausente`; ejecución completa; búsqueda declarada |
| Campos disponibles | motivo, búsqueda |
| Campos ausentes | `feature_id` |
| Tipo de característica | no aplica |
| Evidencia y localización | `search_scope=full_text` |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.coverage_status=descriptive_assessed`; `CE-040`; **no** `not_observed` |
| Justificación | §8.3: §3 no emite `not_observed` |
| Pérdida esperada | token `Ausente` solo en informe |
| Reversibilidad | B |
| Matriz | M-13 |

### TV-66 — §3 `No aplicable` (ruta D)

| Campo | Valor |
|---|---|
| Tipo | real (`evidence-status.md`) |
| Ruta | D |
| Fuente y estado de entrada | dimensión `Plot`; `No aplicable`; género «etiqueta de producto» |
| Campos disponibles | motivo |
| Campos ausentes | cita de característica |
| Tipo de característica | no aplica |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.coverage_status=not_applicable`; **no** `EvidenceRecord` |
| Justificación | §9.2/R-15 |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-15 |

### TV-67 — §3 `No evaluable` (ruta D)

| Campo | Valor |
|---|---|
| Tipo | real (`worked-examples/01-microrelato-21-palabras.md`) |
| Ruta | D |
| Fuente y estado de entrada | microrelato de 21 palabras; dimensión `Plot`; `No evaluable` |
| Campos disponibles | motivo |
| Campos ausentes | cita de característica |
| Tipo de característica | no aplica |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.coverage_status=not_assessable`; **no** `EvidenceRecord` |
| Justificación | §9.2/R-16 |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-16 |

### TV-68 — Filas distintas con contenido idéntico

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | dos filas de §4 para `Thematic Unity`, mismo valor y misma cita, pero `row_index` distinto |
| Campos disponibles | ambas completas |
| Campos ausentes | — |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | misma cita, localizaciones distintas |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | **dos** `EvidenceRecord`; `CE-038` informativo; no se deduplican; `record_id` distintos |
| Justificación | §11.3: dos filas físicamente distintas son observaciones distintas; no se deduplica por contenido |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-51 |

### TV-69 — Reextracción de la misma localización fuente

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F |
| Fuente y estado de entrada | la misma fila de §4 extraída dos veces (misma sección, `row_index` y feature) |
| Campos disponibles | ambas completas |
| Campos ausentes | — |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | misma cita |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | **un** `EvidenceRecord`; `CE-016`; mismo `record_id` |
| Justificación | §11.3/§12: se deduplica solo la repetición de la misma localización fuente |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-32 |

### TV-70 — Reversibilidad de `Presente–opuesto` unidireccional (F+)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Ruta | F+ |
| Fuente y estado de entrada | `Mode of Resolution`; `Presente–opuesto` + `patrón humano`; valor «external event» |
| Campos disponibles | registro + informe |
| Campos ausentes | token de dirección en el dominio |
| Tipo de característica | `categorical option` unidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | registro `observed` + `not_assessed` + `opposed` + `reference_pattern_id=null`; **reversibilidad B**; la dirección `patrón humano` solo se reconstruye desde `legacy_raw` |
| Justificación | §13: la tabla anterior de v0.2 declaraba A, pero el token de dirección no está en el dominio |
| Pérdida esperada | dirección histórica solo en el informe |
| Reversibilidad | B |
| Matriz | M-09 |

---

## 5. Cobertura exigida

| Categoría | Vectores |
|---|---|
| Conversión fiel (F+) | TV-01, TV-02, TV-19, TV-31 |
| Conversión condicionada (F+) | TV-04, TV-12, TV-18, TV-56 |
| Conversión fiel (ruta F) | TV-57, TV-58 |
| Conversión condicionada (ruta F) | TV-36, TV-59, TV-60, TV-61, TV-63, TV-68, TV-69 |
| Preservación sin conversión (ruta D) | TV-22, TV-35, TV-65, TV-66, TV-67 |
| Cuarentena | TV-03, TV-05, TV-06, TV-07, TV-13, TV-16, TV-17, TV-20, TV-25, TV-27, TV-39, TV-40, TV-48, TV-53, TV-62, TV-64 |
| Rechazo | TV-21, TV-23, TV-26, TV-32, TV-37, TV-38, TV-41, TV-42, TV-50, TV-51 |
| Etiqueta global / run-level | TV-14, TV-33, TV-43, TV-44, TV-45, TV-46 |
| Agregado `mixed` con `record_ids` | TV-15 |
| Valor de opción ≠ dirección | TV-30 |
| Idempotencia | TV-24, TV-28, TV-47, TV-49, TV-68, TV-69 |
| Reversibilidad | TV-29, TV-70 |
| Ausencia / no aplicable / no evaluable | TV-08, TV-09, TV-10, TV-11, TV-65, TV-66, TV-67 |
| Contraevidencia | TV-62, TV-63, TV-64 |
| Proyección §3 vs §4 | TV-35, TV-36, TV-37, TV-38 |
| `Dirección del estudio` vs alineación | TV-38 |
| Neutralidad con dos lecturas | TV-53 |
| `Fuerza` fuera de vocabulario | TV-54 |
| Evidencia sin span | TV-55 |
| Opción alternativa sin catálogo | TV-56, TV-59 |
| Procedencia / atestación | TV-51, TV-52 |
| Simetría de oportunidad | TV-34 |
| `analysis_quality_confidence` | TV-45 |

**Total: 70 vectores** (34 heredados de v0.1, revisados donde cambia la ruta + 22 de proyección/ejecución TV-35…TV-56 + 14 nuevos de ruta F TV-57…TV-70).

**Corrección de cobertura respecto de v0.2.** TV-03 **no** figura en «Conversión histórica fiel» ni en «`Presente–opuesto` con evidencia suficiente»; figura solo en «Cuarentena» (`CE-035`). TV-17 y TV-40 tampoco figuran como conversión: R-04 está bloqueada y ambos son cuarentena (`CE-021`).

Casos negativos: TV-03, TV-05, TV-06, TV-07, TV-13, TV-16, TV-17, TV-20, TV-21, TV-23, TV-25, TV-26, TV-32, TV-37, TV-38, TV-39, TV-40, TV-41, TV-42, TV-48, TV-50, TV-51, TV-53, TV-55, TV-62, TV-64.

Casos ambiguos: TV-09, TV-13, TV-20, TV-25, TV-33, TV-48, TV-53, TV-60.

Casos sin conversión: TV-03, TV-16, TV-17, TV-21, TV-23, TV-25, TV-26, TV-32, TV-35, TV-37, TV-38, TV-39, TV-40, TV-41, TV-42, TV-48, TV-50, TV-51, TV-53, TV-55, TV-62, TV-64, TV-65, TV-66, TV-67.

---

## 6. Criterios de aceptación de los vectores

Un futuro exportador se considera conforme a estos vectores si:

1. produce el `outcome` esperado para los 70 casos;
2. emite el código de diagnóstico esperado (o ninguno cuando la tabla dice «ninguno»);
3. no emite `mixed`, `historical_reference_pattern_id` ni códigos `CE-*` dentro de `EvidenceRecord`, `ClusterSummary` o `AnalysisRun`;
4. conserva `legacy_raw` en todos los casos, incluidos los rechazados;
5. reproduce el mismo resultado en dos ejecuciones consecutivas (TV-28, TV-47, TV-49, TV-68, TV-69);
6. reconstruye el estado histórico en los casos de clase A sin el informe y en los de clase B con él (TV-29, TV-70);
7. no emite `EvidenceRecord` desde una fila §3 (TV-08…TV-11, TV-35, TV-65…TV-67);
8. no rechaza una fila §4 por falta de estado (TV-36);
9. no deduplica filas distintas con contenido idéntico (TV-68);
10. no reutiliza la cita principal para la contraevidencia (TV-62, TV-64).

No se implementa aquí ninguna suite ejecutable: los vectores son contractuales y se ejecutarán cuando exista autorización para implementar el exportador.
