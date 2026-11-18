# Vectores de prueba contractuales — v0.2

**Proyecto:** StoryScope Human–AI Analysis
**Fase:** 1.21
**Estado:** casos documentales; **no** es una suite ejecutable
**Fecha:** 2026-11-18
**Contrato:** `COMPATIBILITY_EXPORT_CONTRACT_v0.2.md`
**Matriz:** `COMPATIBILITY_MAPPING_MATRIX_v0.2.md`
**Predecesor:** `COMPATIBILITY_TEST_VECTORS_v0.1.md` (preservado)

Estos vectores fijan el comportamiento esperado **antes** de implementar el exportador. No contienen código, no se ejecutan y no sustituyen a las pruebas del motor.

---

## 1. Convenciones

- **Tipo de caso:** `real` cuando el valor, la característica o el ejemplo proviene de una fuente de `v0.2.3`; `sintético` cuando la fila se construye para el vector. Todo dato sintético se marca. Ningún dato sintético se presenta como observación real.
- **Versión del Registry:** salvo indicación contraria, `0.1.2-draft` (esquema `1.1.0`).
- **Origen:** salvo indicación contraria, `legacy_observation_origin` está declarado y el texto fuente está disponible.
- **Reversibilidad:** clases A/B/C/D del contrato §13.
- **Resultado:** `converted`, `converted_with_flag`, `preserved`, `quarantined`, `rejected`, o rechazo de ejecución.

---

## 2. Vectores heredados de v0.1 (revisados)

Los vectores TV-01 a TV-34 se conservan con los mismos campos. Los cambios de v0.1 a v0.2 son:

- **TV-03** se reclasifica: resultado esperado pasa de `converted` a `quarantined` (`CE-035`), por el dictamen de R-07 (no resoluble sin asumir referencia AI-first).
- **TV-17** se mantiene como conversión condicionada, pero se añade la nota de que la etiqueta histórica `Presente–alineado` no se deriva del registro (clase B).
- **TV-14, TV-33** se ajustan: la etiqueta global y `analysis_quality_confidence` se preservan en `run_level` del informe externo, sin escritura en el dominio.

El resto de los 34 vectores conserva su resultado esperado de v0.1.

### TV-03 — `Presente–opuesto` en bidireccional (revisado)

| Campo | Valor |
|---|---|
| Tipo | característica y opciones reales; fila sintética |
| Fuente y estado de entrada | `Dominant Emotional Expression` (`categorical`); `Presente–opuesto` + `patrón humano`; valor observado `explicit labels` |
| Campos disponibles | cita con etiqueta emocional explícita, justificación, clúster `emotional_sensory_expression` |
| Campos ausentes | `Fuerza` |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-035`; payload literal preservado; **no** se emite `EvidenceRecord` |
| Justificación | dictamen v0.2: `Presente–opuesto` + `patrón humano` en bidireccional no es resoluble sin asumir referencia AI-first; la fuente histórica no declara qué polo es la referencia |
| Pérdida esperada | fila no convertida; revisión humana requerida |
| Reversibilidad | B |
| Matriz | M-08 |

---

## 3. Vectores nuevos (TV-35…TV-56)

### TV-35 — Fila §3 de dimensión sin `feature_id`

| Campo | Valor |
|---|---|
| Tipo | real (estructura de `report-template.md` §3) |
| Fuente y estado de entrada | dimensión `Social networks`; estado `Presente–alineado`; dirección `patrón humano`; sin `feature_id` |
| Campos disponibles | dimensión, observación, estado, dirección |
| Campos ausentes | `feature_id` (la dimensión no tiene características en el mapa central) |
| Tipo de característica | no aplica |
| Evidencia y localización | observación descriptiva |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.neutral_summary`; `limitations`; `coverage_status`; `CE-029` |
| Justificación | §5.5: un perfil descriptivo no se convierte en señal direccional; no se hace join con §4 |
| Pérdida esperada | no hay registro atómico |
| Reversibilidad | A |
| Matriz | M-28 |

### TV-36 — Fila §4 de característica sin estado histórico explícito

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | fila de §4 con `Característica/valor observado` y cita, pero sin `Estado de evidencia (5)` |
| Campos disponibles | característica, cita, clúster |
| Campos ausentes | `legacy_state` |
| Tipo de característica | cualquiera |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `CE-001`/`CE-025` |
| Justificación | `evidence-status.md`: «No se puede asignar dirección a un rasgo hasta registrar su estado» |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-30 |

### TV-37 — Intento inválido de unir estados de §3 a features de §4

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | ejecución que intenta copiar el estado de la dimensión `Plot` a las features `Subplot Integration` y `Mode of Resolution` |
| Campos disponibles | estado de dimensión, features de §4 |
| Campos ausentes | — |
| Tipo de característica | varias |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected` para cada intento de join; `CE-007` o `CE-029`; no se emiten registros por dimensión |
| Justificación | §8 del contrato: no existe join automático entre §3 y §4 |
| Pérdida esperada | ninguna fila convertida por join |
| Reversibilidad | D |
| Matriz | M-28, M-29 |

### TV-38 — `Dirección del estudio` confundida con alineación observada

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | fila de §4 con `Dirección del estudio=AI`; el exportador intenta copiarla a `research_alignment` |
| Campos disponibles | estado, dirección del estudio, cita |
| Campos ausentes | dirección observada |
| Tipo de característica | cualquiera |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `research_alignment` se resuelve desde el registro, no desde `Dirección del estudio` |
| Justificación | R-35; `report-template.md` §4 |
| Pérdida esperada | fila no convertida si no hay dirección observada |
| Reversibilidad | D |
| Matriz | M-33 |

### TV-39 — `Presente–opuesto` + `patrón humano` en bidireccional

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Fuente y estado de entrada | `Reference Explicitness`; `Presente–opuesto` + `patrón humano`; valor `balanced mix` |
| Campos disponibles | cita literal, justificación, clúster `Intertextuality` |
| Campos ausentes | — |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-035`; payload literal preservado |
| Justificación | dictamen v0.2: no resoluble sin asumir referencia AI-first |
| Pérdida esperada | fila no convertida |
| Reversibilidad | B |
| Matriz | M-08 |

### TV-40 — `Presente–alineado` + `patrón humano` en bidireccional

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Fuente y estado de entrada | `Reference Explicitness`; `Presente–alineado` + `patrón humano`; valor `balanced mix` |
| Campos disponibles | cita literal, justificación |
| Campos ausentes | — |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `pattern_human`; `reference_pattern_id`=patrón humano; `opposed`; `CE-021` |
| Justificación | opción humana elevada; referencia histórica es IA |
| Pérdida esperada | etiqueta histórica no se deriva del registro |
| Reversibilidad | B |
| Matriz | M-04 |

### TV-41 — `Presente–opuesto` + `patrón IA` en bidireccional

| Campo | Valor |
|---|---|
| Tipo | sintético |
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
| Fuente y estado de entrada | etiqueta global `mixto`; dos registros en clústeres distintos; sin campo de alineación en `AnalysisRun` |
| Campos disponibles | etiqueta, registros |
| Campos ausentes | clúster único que justifique la síntesis; campo de alineación en `AnalysisRun` |
| Tipo de característica | ejecución |
| Evidencia y localización | `record_ids` |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `CE-015`; etiqueta en `run_level.legacy_global_label`; `written_to_domain=false` |
| Justificación | R-20; §15-B1: no se inventa campo |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-22 |

### TV-44 — Intento de transferir `mixto` global a `ClusterSummary`

| Campo | Valor |
|---|---|
| Tipo | sintético |
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
| Fuente y estado de entrada | ejecución con `analysis_quality_confidence=alta` y registros con `evidence_strength` variado |
| Campos disponibles | etiqueta, registros |
| Campos ausentes | — |
| Tipo de característica | ejecución |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `run_level.analysis_quality_confidence=alta`; **no** copia a `EvidenceRecord.assessment_confidence`; R-23 |
| Justificación | `report-template.md` §6; Spec §5.3 |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | A |
| Matriz | M-25 |

### TV-46 — `adequacy` no definido

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | ejecución con puerta `no apto` y etiqueta `evidencia insuficiente` |
| Campos disponibles | puerta, etiqueta |
| Campos ausentes | enum de `adequacy` en el destino |
| Tipo de característica | ejecución |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `CE-028`; etiqueta en `run_level.legacy_global_label`; `written_to_domain=false` |
| Justificación | §15-B2: no se inventa enum |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-23 |

### TV-47 — Dos observaciones distintas dentro de una fila

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | fila de §4 con valor observado principal + contraevidencia en la misma fila |
| Campos disponibles | estado, dirección, cita principal, contraevidencia |
| Campos ausentes | — |
| Tipo de característica | `categorical` |
| Evidencia y localización | dos citas literales |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | dos `EvidenceRecord` con `legacy_sublocator` `:obs:1` y `:obs:2`; clave de unicidad `(digest, sublocator)` |
| Justificación | §11.2: sublocalizador distingue observaciones |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-41 (no aplica; caso válido) |

### TV-48 — Colisión de localizador

| Campo | Valor |
|---|---|
| Tipo | sintético |
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

### TV-49 — Duplicados idénticos

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | dos filas idénticas para `Thematic Unity`, misma cita, mismo estado, misma sección |
| Campos disponibles | ambas completas |
| Campos ausentes | — |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | misma cita |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | un único registro; `CE-016` informativo; mismo `record_id`; clave `(digest, sublocator)` |
| Justificación | idempotencia por clave de origen |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-32 |

### TV-50 — Duplicados conflictivos

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | misma clave de origen, una fila `Presente–alineado` + `patrón IA` y otra `Ausente` |
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
| Matriz | M-38, M-42 |

### TV-52 — Atestación de procedencia durante la migración

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | ejecución sin origen histórico, pero con atestación válida del operador |
| Campos disponibles | filas completas, atestación |
| Campos ausentes | origen histórico demostrado |
| Tipo de característica | ejecución |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | conversión permitida; `observation_origin` refleja la atestación; `migration_attestations` registra responsable, fecha, fundamento, versión de protocolo y autorización; `origin_detail` puede referenciar la atestación |
| Justificación | §11.5: atestación de migración es mecanismo externo con su propia procedencia |
| Pérdida esperada | ninguna |
| Reversibilidad | B |
| Matriz | M-38 |

### TV-53 — Neutralidad con dos lecturas posibles

| Campo | Valor |
|---|---|
| Tipo | sintético |
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
| Fuente y estado de entrada | `Thematic Unity`; `Presente–alineado` + `patrón IA`; `Fuerza` = «muy fuerte» |
| Campos disponibles | estado, dirección, fuerza libre |
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
| Fuente y estado de entrada | `Sensory Density`; `Presente–alineado` + `patrón IA`; «cita» parafraseada |
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

### TV-56 — Opción alternativa sin catálogo completo

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Mode of Resolution`; `Presente–opuesto` + `patrón IA`; valor «protagonist choice» (no registrado) |
| Campos disponibles | cita literal, justificación |
| Campos ausentes | `observed_option_id` para la opción alternativa |
| Tipo de característica | `categorical option` unidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `not_assessed`; `reference_pattern_id=null`; `opposed`; `observed_option_id=null`; `observed_value_text="protagonist choice"`; `CE-022`/`CE-026` |
| Justificación | §5.3.4 y §5.3: opción no registrada no inventa ID; dirección no registrada |
| Pérdida esperada | dirección histórica solo en procedencia |
| Reversibilidad | B |
| Matriz | M-09, M-27 |

---

## 4. Cobertura exigida

| Categoría exigida por la fase | Vectores |
|---|---|
| Conversión histórica fiel | TV-01, TV-02, TV-03(v0.1, revisado), TV-10, TV-11, TV-19, TV-31, TV-40 |
| `Presente–opuesto` con evidencia suficiente | TV-03(v0.1), TV-04, TV-18, TV-39, TV-41 |
| `Presente–opuesto` sin evidencia suficiente | TV-05, TV-06, TV-07 |
| Ausencia | TV-08, TV-09 |
| `not_observed` | TV-08 |
| `neutral` | TV-12, TV-13, TV-53 |
| `not_assessed` | TV-04, TV-19, TV-22, TV-56 |
| `mixed` en agregado | TV-15 |
| Intento inválido de `mixed` en `EvidenceRecord` | TV-16 |
| Bidireccional con polo humano observado | TV-03(v0.1), TV-17, TV-39, TV-40, TV-41 |
| Unidireccional con opción alternativa | TV-04, TV-18, TV-56 |
| Multiselección con coexistencia | TV-19, TV-20 |
| Registro sin `feature_id` | TV-21, TV-22, TV-35, TV-37 |
| Registry version desconocida | TV-23 |
| Registro duplicado | TV-24, TV-25, TV-49, TV-50 |
| Registro inconsistente | TV-26, TV-42 |
| Registro con evidencia insuficiente | TV-05, TV-06, TV-27, TV-55 |
| Exportación repetida (idempotencia) | TV-28, TV-47, TV-48 |
| Reconstrucción del original | TV-29 |
| Categórica explícita de ausencia | TV-31 |
| Valor de opción homónimo de `mixed` | TV-30 |
| Etiqueta global sin campo | TV-14, TV-33, TV-43, TV-44, TV-46 |
| Precondiciones de ejecución | TV-32, TV-51, TV-52 |
| Simetría | TV-34 |
| Proyección §3 vs §4 | TV-35, TV-36, TV-37, TV-38 |
| `Dirección del estudio` vs alineación | TV-38 |
| Neutralidad con dos lecturas | TV-53 |
| `Fuerza` fuera de vocabulario | TV-54 |
| Evidencia sin span | TV-55 |
| Opción alternativa sin catálogo | TV-56 |
| Procedencia / atestación | TV-51, TV-52 |
| `analysis_quality_confidence` | TV-45 |

**Total: 56 vectores** (34 heredados revisados + 22 nuevos). Casos negativos: los de v0.1 más TV-36, TV-37, TV-38, TV-39, TV-41, TV-42, TV-48, TV-50, TV-51, TV-53, TV-55. Casos ambiguos: TV-09, TV-13, TV-17, TV-20, TV-25, TV-33, TV-48, TV-53. Casos sin conversión: TV-16, TV-21, TV-23, TV-25, TV-26, TV-27, TV-32, TV-36, TV-37, TV-38, TV-39, TV-41, TV-42, TV-48, TV-50, TV-51, TV-55.

---

## 5. Criterios de aceptación de los vectores

Un futuro exportador se considera conforme a estos vectores si:

1. produce el `outcome` esperado para los 56 casos;
2. emite el código de diagnóstico esperado (o ninguno cuando la tabla dice «ninguno»);
3. no emite `mixed`, `historical_reference_pattern_id` ni códigos `CE-*` dentro de `EvidenceRecord`, `ClusterSummary` o `AnalysisRun`;
4. conserva `legacy_raw` en todos los casos, incluidos los rechazados;
5. reproduce el mismo resultado en dos ejecuciones consecutivas (TV-28, TV-47, TV-48);
6. reconstruye el estado histórico en los casos de clase A sin el informe y en los de clase B con él (TV-29).

No se implementa aquí ninguna suite ejecutable: los vectores son contractuales y se ejecutarán cuando exista autorización para implementar el exportador.
