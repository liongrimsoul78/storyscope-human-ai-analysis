# Vectores de prueba contractuales — v0.1

**Proyecto:** StoryScope Human–AI Analysis
**Fase:** 1.20
**Estado:** casos documentales; **no** es una suite ejecutable
**Fecha:** 2026-11-17
**Contrato:** `COMPATIBILITY_EXPORT_CONTRACT_v0.1.md`
**Matriz:** `COMPATIBILITY_MAPPING_MATRIX_v0.1.md`

Estos vectores fijan el comportamiento esperado **antes** de implementar el exportador. No contienen código, no se ejecutan y no sustituyen a las pruebas del motor.

---

## 1. Convenciones

- **Tipo de caso:** `real` cuando el valor, la característica o el ejemplo proviene de una fuente de `v0.2.3`; `sintético` cuando la fila se construye para el vector. Todo dato sintético se marca. Ningún dato sintético se presenta como observación real.
- **Versión del Registry:** salvo indicación contraria, `0.1.2-draft` (esquema `1.1.0`).
- **Origen:** salvo indicación contraria, `legacy_observation_origin` está declarado y el texto fuente está disponible.
- **Reversibilidad:** clases A/B/C/D del contrato §12.
- **Resultado:** `converted`, `converted_with_flag`, `preserved`, `quarantined`, `rejected`, o rechazo de ejecución.

---

## 2. Vectores

### TV-01 — Conversión fiel, unidireccional IA

| Campo | Valor |
|---|---|
| Tipo | característica y opción reales; fila sintética |
| Fuente y estado de entrada | `Thematic Explicitness and Moralizing` (escala 1–5, referencia `pattern_ai`); estado `Presente–alineado`; dirección `patrón IA` |
| Campos disponibles | observación, estado, dirección, cita literal, justificación, clúster `thematic_framing`, ejecución completa |
| Campos ausentes | `Fuerza`; explicación alternativa |
| Tipo de característica | `scale 1–5`; `pattern_level=overall_feature` |
| Evidencia y localización | cita literal única en el texto; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `pattern_ai`; `reference_pattern_id=ssha.pattern.thematic_explicitness_and_moralizing.overall`; `aligned`; `reference_pattern`; `observed_option_id=null`; `source_spans` no vacío; `opportunity_status=sufficient` |
| Justificación | `INV-A2-09`: dirección = dirección de la referencia; `observed_option_id` no aplica a patrones `overall_feature` |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-01 |

### TV-02 — Conversión fiel, unidireccional humana

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Fuente y estado de entrada | `Frequency of Direct Reader Address` (`ordinal mean`, referencia `pattern_human`); `Presente–alineado` + `patrón humano` |
| Campos disponibles | observación, estado, dirección, cita literal, justificación, ejecución completa |
| Campos ausentes | `Fuerza` |
| Tipo de característica | `ordinal mean`; `overall_feature` |
| Evidencia y localización | cita literal de segunda persona dirigida al lector |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `pattern_human`; `reference_pattern_id=ssha.pattern.frequency_of_direct_reader_address.overall`; `aligned` |
| Justificación | referencia histórica humana; no se compara numéricamente con la media |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-02 |

### TV-03 — `Presente–opuesto` con evidencia suficiente, bidireccional

| Campo | Valor |
|---|---|
| Tipo | característica y opciones reales; fila sintética |
| Fuente y estado de entrada | `Dominant Emotional Expression` (`categorical`); `Presente–opuesto` + `patrón humano`; valor observado `explicit labels` |
| Campos disponibles | cita con etiqueta emocional explícita, justificación, clúster `emotional_sensory_expression` |
| Campos ausentes | `Fuerza` |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `pattern_human`; `reference_pattern_id=ssha.pattern.dominant_emotional_expression.explicit_labels`; `opposed`; `observed_option_id` = ese patrón (`response_option`) |
| Justificación | `INV-A2-10`: patrón opuesto registrado; la referencia histórica es el patrón IA |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-07 |

### TV-04 — `Presente–opuesto` unidireccional con evidencia

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Fuente y estado de entrada | `Mode of Resolution` (`categorical option`, referencia IA `internal understanding`); `Presente–opuesto` + `patrón IA`; valor observado «protagonist choice» |
| Campos disponibles | cita literal de resolución por elección del protagonista, justificación |
| Campos ausentes | `observed_option_id` para la opción alternativa (no registrada); `Fuerza` |
| Tipo de característica | `categorical option` unidireccional |
| Evidencia y localización | cita literal; offsets resolubles |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `not_assessed`; `reference_pattern_id=null`; `opposed`; `observed_option_id=null`; `observed_value_text="protagonist choice"`; `CE-022` |
| Justificación | `INV-A2-11`: en unidireccional, `opposed` no admite patrón; la opción alternativa no está registrada y la dirección histórica solo se preserva |
| Pérdida esperada | la dirección histórica `patrón IA` solo queda en `legacy_raw` |
| Reversibilidad | B |
| Matriz | M-09 |

### TV-05 — `Presente–opuesto` sin span

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Reference Explicitness`; `Presente–opuesto` + `patrón humano`; «Cita o ubicación» vacía |
| Campos disponibles | estado, dirección, justificación |
| Campos ausentes | cita literal, offsets |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | ninguna |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-009`; payload literal preservado |
| Justificación | regla 5 de §5.3 y §9.4 del contrato: `observed` exige span verificable |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-11 |

### TV-06 — `Presente–opuesto` sin justificación

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Subplot Integration`; `Presente–opuesto` + `patrón humano`; cita literal de subtrama temáticamente paralela |
| Campos disponibles | cita, estado, dirección |
| Campos ausentes | «Por qué / alternativa contextual» |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal válida |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-010` |
| Justificación | `evidence-status.md` «Contraevidencia» exige interpretación alternativa |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-12 |

### TV-07 — `Presente–opuesto` en escala sin ancla

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Thematic Unity` (`scale 1–5`); `Presente–opuesto` + `patrón humano` |
| Campos disponibles | estado, dirección, cita, justificación genérica («el tema está poco integrado») |
| Campos ausentes | ancla o constructo opuesto explícito |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-011` |
| Justificación | §6.5: no se inventan puntos de corte; una media grupal no es umbral |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-10 |

### TV-08 — `Ausente` con oportunidad suficiente

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Dominant Sensory Modalities`; `Ausente` + `no evaluable`; ejecución `completo`; búsqueda declarada |
| Campos disponibles | motivo, alcance de búsqueda, longitud suficiente |
| Campos ausentes | cita (no procede) |
| Tipo de característica | `multi-select option` |
| Evidencia y localización | `search_scope=full_text`; `absence_justification` |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `not_observed`; `sufficient`; `not_assessed`; `none`; `status_reason`; `absence_justification`; `search_scope=full_text`; `observed_option_id=null` |
| Justificación | correspondencia exacta de `Ausente` en §5.3 |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-13 |

### TV-09 — `Ausente` con oportunidad insuficiente

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | misma característica que TV-08; `Ausente`; ejecución `fragmento` |
| Campos disponibles | estado, motivo |
| Campos ausentes | completitud; búsqueda declarada |
| Tipo de característica | `multi-select option` |
| Evidencia y localización | ninguna |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `not_evaluable`; `limited`; `not_assessed`; `none`; `status_reason`; `CE-013` |
| Justificación | §5.3: `Ausente` solo es exacta con `sufficient` |
| Pérdida esperada | el estado cambia; etiqueta histórica preservada |
| Reversibilidad | B |
| Matriz | M-14 |

### TV-10 — `No aplicable` (ejemplo real de la fuente)

| Campo | Valor |
|---|---|
| Tipo | real (`evidence-status.md`, fila `No aplicable`: «Subtramas en una etiqueta de producto o un formulario») |
| Fuente y estado de entrada | `Subplot Integration`; `No aplicable` + `no evaluable`; género «etiqueta de producto» |
| Campos disponibles | motivo de no aplicabilidad |
| Campos ausentes | cita |
| Tipo de característica | `categorical` |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `not_applicable`; `none`; `not_assessed`; `status_reason` |
| Justificación | correspondencia exacta; `INV-A2-13` |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-15 |

### TV-11 — `No evaluable` (ejemplo real de la fuente)

| Campo | Valor |
|---|---|
| Tipo | real (`worked-examples/01-microrelato-21-palabras.md`: «son **No evaluable** por longitud y forma») |
| Fuente y estado de entrada | microrelato de 21 palabras; `Subplot Integration`; `No evaluable` + `no evaluable` |
| Campos disponibles | motivo (longitud), longitud, género |
| Campos ausentes | cita |
| Tipo de característica | `categorical` |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `not_evaluable`; `limited`; `not_assessed`; `none`; `status_reason` |
| Justificación | correspondencia exacta; el ejemplo prohíbe tratar la falta como evidencia |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-16 |

### TV-12 — Variante `neutral` de estado

| Campo | Valor |
|---|---|
| Tipo | real (`evidence-status.md`, regla de decisión paso 3); fila sintética |
| Fuente y estado de entrada | `Dialogue Function`; `Presente–alineado` + `neutro` (codificación histórica de presente neutro); justificación de neutralización contextual. La variante de estado `neutral` produce el mismo resultado |
| Campos disponibles | estado, dirección, detalle contextual, cita |
| Campos ausentes | — |
| Tipo de característica | `multi-select option` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `neutral`; `contextual_neutralization`; `reference_pattern_id=null`; `not_assessed`; `alignment_basis_detail` no nulo; `CE-020` |
| Justificación | `INV-A2-12`; no se crea un sexto estado; la taxonomía histórica carece de estado «presente neutro» |
| Pérdida esperada | los tokens `Presente–alineado` y `neutro` solo en procedencia |
| Reversibilidad | B |
| Matriz | M-17 / M-18 |

### TV-13 — `neutro` con lectura ambigua

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

### TV-14 — Etiqueta global `evidencia insuficiente`

| Campo | Valor |
|---|---|
| Tipo | real (`worked-examples/01-microrelato-21-palabras.md`) |
| Fuente y estado de entrada | microrelato de 21 palabras; puerta «no apto»; etiqueta global `evidencia insuficiente` |
| Campos disponibles | longitud, género, puerta, etiqueta |
| Campos ausentes | enum de `adequacy` en el destino |
| Tipo de característica | ejecución |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `CE-028`; etiqueta en `run_level.legacy_global_label`; `written_to_domain=false` |
| Justificación | `evidencia insuficiente` no es un estado de evidencia; el enum de `adequacy` no está definido (contrato §15-B2) |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-23 |

### TV-15 — `mixed` en agregado

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | clúster `causal_plot_architecture` con dos registros: uno `pattern_ai`, otro `pattern_human`; etiqueta de clúster `mixto` |
| Campos disponibles | dos `record_id`, alineaciones distintas, resumen cualitativo |
| Campos ausentes | — |
| Tipo de característica | agregado de clúster |
| Evidencia y localización | `record_ids` trazables |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `ClusterSummary.alignment=mixed`; `record_ids` con ambas direcciones; sin votación ni porcentaje |
| Justificación | §5.3.3: `mixed` válido en `ClusterSummary` con ≥2 observaciones y alineaciones distintas |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-22 |

### TV-16 — `mixto` en registro atómico (intento inválido)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Depth of Interior Access`; dirección `mixto`; una sola fila, sin observaciones desglosadas |
| Campos disponibles | estado, dirección `mixto`, observación |
| Campos ausentes | las dos observaciones que sustentarían la mezcla |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | una cita |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined`; `CE-014`; **nunca** `mixed` en `EvidenceRecord` |
| Justificación | §5.3.3 y `INV-A2` nota: `mixed` es propiedad de conjuntos |
| Pérdida esperada | fila no convertida hasta desglose |
| Reversibilidad | D |
| Matriz | M-21 |

### TV-17 — Bidireccional alineada al polo humano

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Fuente y estado de entrada | `Reference Explicitness`; `Presente–alineado` + `patrón humano`; valor `balanced mix` |
| Campos disponibles | cita literal, justificación |
| Campos ausentes | `Fuerza` |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `pattern_human`; `reference_pattern_id=ssha.pattern.reference_explicitness.balanced_mix`; `opposed`; `CE-021`; etiqueta histórica preservada |
| Justificación | la opción humana está elevada (histórico) pero la referencia A2 es IA |
| Pérdida esperada | la etiqueta `Presente–alineado` no se deriva del registro |
| Reversibilidad | B |
| Matriz | M-04 |

### TV-18 — Unidireccional binaria con opción alternativa

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Fuente y estado de entrada | `Narratorial Thematic Commentary` (`binary option`, referencia IA `yes`); `Presente–opuesto` + `patrón humano`; valor `no` explícito |
| Campos disponibles | cita literal del comentario ausente de forma canónica, justificación |
| Campos ausentes | patrón registrado para `no`; patrón humano registrado para la característica |
| Tipo de característica | `binary option` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `not_assessed`; `reference_pattern_id=null`; `opposed`; `observed_value_text="no"`; `CE-026`; `CE-022` |
| Justificación | §6.5: un `no` explícito puede ser `opposed`; la mera ausencia no basta |
| Pérdida esperada | dirección histórica solo en procedencia |
| Reversibilidad | B |
| Matriz | M-09 |

### TV-19 — Multiselección con coexistencia

| Campo | Valor |
|---|---|
| Tipo | característica real; fila sintética |
| Fuente y estado de entrada | `Dominant Sensory Modalities`; `Presente–alineado` + `patrón IA`; modalidades `olfactory` y `visual` coexistentes |
| Campos disponibles | cita con ambas modalidades, justificación |
| Campos ausentes | — |
| Tipo de característica | `multi-select option` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `pattern_ai`; `reference_pattern_id=ssha.pattern.dominant_sensory_modalities.olfactory`; `aligned`; **sin** `opposed` |
| Justificación | §6.5: la coexistencia no produce oposición |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-01 |

### TV-20 — Multiselección sin la opción de referencia

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Dialogue Function`; `Presente–opuesto` + `patrón IA`; el texto no contiene diálogo |
| Campos disponibles | estado, dirección, observación |
| Campos ausentes | opción alternativa observada; cita de diálogo |
| Tipo de característica | `multi-select option` |
| Evidencia y localización | ninguna cita de diálogo |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `CE-012`; se corrige a `not_observed`/`not_evaluable` según oportunidad |
| Justificación | §6.5: la ausencia de la opción de referencia no demuestra contraevidencia |
| Pérdida esperada | fila no convertida como oposición |
| Reversibilidad | D |
| Matriz | M-29 |

### TV-21 — Registro sin `feature_id` (nivel característica)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | fila de §4 con «Característica/valor observado» genérico («uso del tiempo»), sin nombre canónico |
| Campos disponibles | estado, dirección, cita |
| Campos ausentes | `feature_id` resoluble |
| Tipo de característica | desconocido |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `CE-003`/`CE-004` |
| Justificación | `feature_id` es obligatorio en `EvidenceRecord`; no se adivina la característica |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-27 |

### TV-22 — Fila de dimensión sin `feature_id`

| Campo | Valor |
|---|---|
| Tipo | real (estructura de `report-template.md` §3) |
| Fuente y estado de entrada | dimensión `Social networks`; estado `Presente–alineado`; dirección `patrón humano` |
| Campos disponibles | dimensión, observación, estado, dirección |
| Campos ausentes | `feature_id` (la dimensión no tiene características en el mapa central) |
| Tipo de característica | no aplica |
| Evidencia y localización | observación descriptiva |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `DimensionProfile.neutral_summary`; `limitations`; `coverage_status`; `CE-029` |
| Justificación | §5.5: un perfil descriptivo no se convierte en señal direccional |
| Pérdida esperada | no hay registro atómico |
| Reversibilidad | A |
| Matriz | M-26 |

### TV-23 — Versión de Registry desconocida

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | ejecución con `feature_registry_version="0.0.9"` |
| Campos disponibles | todo salvo versión válida |
| Campos ausentes | versión existente |
| Tipo de característica | ejecución |
| Evidencia y localización | no procede |
| Versión del Registry | inexistente |
| Resultado esperado | rechazo de ejecución; `CE-005`; **ningún** registro emitido |
| Justificación | `INV-A2-16`: la versión debe estar fijada y ser resoluble |
| Pérdida esperada | ejecución no convertida |
| Reversibilidad | D |
| Matriz | M-34 |

### TV-24 — Registro duplicado idéntico

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | dos filas idénticas para `Thematic Unity`, misma cita, mismo estado, misma sección |
| Campos disponibles | ambas completas |
| Campos ausentes | — |
| Tipo de característica | `scale 1–5` |
| Evidencia y localización | misma cita |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | un único registro; `CE-016` informativo; mismo `record_id` |
| Justificación | clave de unicidad `(digest, locator)`; idempotencia |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-30 |

### TV-25 — Registro duplicado conflictivo

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
| Matriz | M-30 |

### TV-26 — Registro inconsistente (estado y dirección)

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | `Ausente` + `patrón IA` |
| Campos disponibles | estado, dirección |
| Campos ausentes | dirección coherente (`no evaluable`) |
| Tipo de característica | cualquiera |
| Evidencia y localización | no procede |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `rejected`; `CE-007` |
| Justificación | `evidence-status.md`: ausencia no tiene dirección por defecto |
| Pérdida esperada | fila no convertida |
| Reversibilidad | D |
| Matriz | M-29 |

### TV-27 — Cita no literal

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
| Matriz | M-35 |

### TV-28 — Exportación repetida (idempotencia)

| Campo | Valor |
|---|---|
| Tipo | sintético (ejecución completa) |
| Fuente y estado de entrada | misma fuente, mismo contrato, mismo registry, mismas opciones; dos ejecuciones |
| Campos disponibles | conjunto de filas de TV-01 a TV-27 |
| Campos ausentes | — |
| Tipo de característica | conjunto |
| Evidencia y localización | idénticas |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | mismo `analysis_id`; mismos `record_id`; mismo conjunto lógico de registros; sin duplicados; mismo orden serializado |
| Justificación | contrato §11 |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-30 |

### TV-29 — Reconstrucción del original

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | (a) registro de TV-01; (b) registro de TV-04 con su informe de exportación |
| Campos disponibles | (a) solo registro + registry; (b) registro + `legacy_raw` |
| Campos ausentes | (a) ninguno; (b) nada, el informe está disponible |
| Tipo de característica | escala unidireccional / categórica unidireccional |
| Evidencia y localización | — |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | (a) `Presente–alineado` + `patrón IA` sin el informe; (b) `Presente–opuesto` + `patrón IA` desde `legacy_raw` |
| Justificación | clases A y B del contrato §12 |
| Pérdida esperada | ninguna con el informe; en (b) sin informe no hay reconstrucción |
| Reversibilidad | A / B |
| Matriz | M-01 / M-09 |

### TV-30 — `ambivalent/mixed` como opción, no como dirección

| Campo | Valor |
|---|---|
| Tipo | real (valor de opción en CSV y registry); fila sintética |
| Fuente y estado de entrada | `Moral Polarity Toward Protagonist`; `Presente–alineado` + `patrón humano`; valor `ambivalent/mixed` |
| Campos disponibles | cita literal de ambivalencia moral, justificación |
| Campos ausentes | — |
| Tipo de característica | `categorical option` |
| Evidencia y localización | cita literal |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `pattern_human`; `reference_pattern_id=ssha.pattern.moral_polarity_toward_protagonist.ambivalent_mixed`; `aligned`; **sin** `mixed` en `research_alignment`; `CE-030` informativo si el texto es ambiguo |
| Justificación | `ambivalent/mixed` es una opción; `mixed` es una dirección agregada |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-33 |

### TV-31 — Opción categórica explícita de ausencia

| Campo | Valor |
|---|---|
| Tipo | real (`no_subplots`; `evidence-status.md`; CSV; registry); fila sintética |
| Fuente y estado de entrada | `Subplot Integration`; `Presente–alineado` + `patrón IA`; historia completa con una sola línea argumental |
| Campos disponibles | cita, justificación, completitud |
| Campos ausentes | — |
| Tipo de característica | `categorical` bidireccional |
| Evidencia y localización | cita literal; oportunidad suficiente |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `observed`; `observed_option_id=ssha.pattern.subplot_integration.no_subplots`; `pattern_ai`; `aligned`; **no** `not_observed` |
| Justificación | §5.3.4: la opción explícita de ausencia es una observación |
| Pérdida esperada | ninguna |
| Reversibilidad | A |
| Matriz | M-24 |

### TV-32 — Origen no declarado y texto ausente

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | ejecución sin `legacy_observation_origin` y sin texto fuente |
| Campos disponibles | filas completas |
| Campos ausentes | origen, texto |
| Tipo de característica | ejecución |
| Evidencia y localización | no verificable |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | rechazo de ejecución; `CE-032` y `CE-033`; **ningún** registro emitido |
| Justificación | `observation_origin` es obligatorio y no tiene fuente histórica; `observed` exige span verificable |
| Pérdida esperada | ejecución no convertida |
| Reversibilidad | D |
| Matriz | M-36 |

### TV-33 — `mixto` global sin campo de dominio

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | etiqueta global `mixto`; dos registros en clústeres distintos |
| Campos disponibles | etiqueta, registros |
| Campos ausentes | clúster único que justifique la síntesis; campo de alineación en `AnalysisRun` |
| Tipo de característica | ejecución |
| Evidencia y localización | `record_ids` |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `preserved`; `CE-015`; etiqueta en `run_level`; sin escritura en `AnalysisRun` |
| Justificación | contrato §15-B1: §5.2 no define campo de alineación global |
| Pérdida esperada | ninguna; se preserva |
| Reversibilidad | B |
| Matriz | M-22 |

### TV-34 — Asimetría de oportunidad

| Campo | Valor |
|---|---|
| Tipo | sintético |
| Fuente y estado de entrada | misma longitud y género; `Dominant Sensory Modalities` = `Ausente` (suficiente) y `Frequency of Direct Reader Address` = `No evaluable` (limitada) |
| Campos disponibles | ambas filas, misma ejecución |
| Campos ausentes | justificación de la diferencia |
| Tipo de característica | dos características |
| Evidencia y localización | misma oportunidad textual |
| Versión del Registry | `0.1.2-draft` |
| Resultado esperado | `quarantined` para revisión manual; `CE-034`; no se emite ninguna de las dos filas hasta resolver la asimetría |
| Justificación | `evidence-status.md` «Regla de simetría» |
| Pérdida esperada | ninguna si se corrige la asimetría |
| Reversibilidad | D |
| Matriz | M-37 |

---

## 3. Cobertura exigida

| Categoría exigida por la fase | Vectores |
|---|---|
| Conversión histórica fiel | TV-01, TV-02, TV-03, TV-10, TV-11, TV-19, TV-31 |
| `Presente–opuesto` con evidencia suficiente | TV-03, TV-04, TV-18 |
| `Presente–opuesto` sin evidencia suficiente | TV-05, TV-06, TV-07 |
| Ausencia | TV-08, TV-09 |
| `not_observed` | TV-08 |
| `neutral` | TV-12 |
| `not_assessed` | TV-19 (observación sin patrón), TV-04 (oposición unidireccional), TV-22 (perfil) |
| `mixed` en agregado | TV-15 |
| Intento inválido de `mixed` en `EvidenceRecord` | TV-16 |
| Bidireccional con polo humano observado | TV-03, TV-17 |
| Unidireccional con opción alternativa | TV-04, TV-18 |
| Multiselección con coexistencia | TV-19, TV-20 |
| Registro sin `feature_id` | TV-21, TV-22 |
| Registry version desconocida | TV-23 |
| Registro duplicado | TV-24, TV-25 |
| Registro inconsistente | TV-26 |
| Registro con evidencia insuficiente | TV-05, TV-06, TV-27 |
| Exportación repetida (idempotencia) | TV-28 |
| Reconstrucción del original | TV-29 |
| Categórica explícita de ausencia | TV-31 |
| Valor de opción homónimo de `mixed` | TV-30 |
| Etiqueta global sin campo | TV-14, TV-33 |
| Precondiciones de ejecución | TV-32 |
| Simetría | TV-34 |

**Total: 34 vectores.** Casos negativos: TV-05, TV-06, TV-07, TV-13, TV-16, TV-20, TV-21, TV-23, TV-25, TV-26, TV-27, TV-32, TV-34 (13). Casos ambiguos: TV-09, TV-13, TV-17, TV-20, TV-25, TV-33. Casos sin conversión: TV-16, TV-21, TV-23, TV-25, TV-26, TV-27, TV-32.

---

## 4. Criterios de aceptación de los vectores

Un futuro exportador se considera conforme a estos vectores si:

1. produce el `outcome` esperado para los 34 casos;
2. emite el código de diagnóstico esperado (o ninguno cuando la tabla dice «ninguno»);
3. no emite `mixed`, `historical_reference_pattern_id` ni códigos `CE-*` dentro de `EvidenceRecord`, `ClusterSummary` o `AnalysisRun`;
4. conserva `legacy_raw` en todos los casos, incluidos los rechazados;
5. reproduce el mismo resultado en dos ejecuciones consecutivas (TV-28);
6. reconstruye el estado histórico en los casos de clase A sin el informe y en los de clase B con él (TV-29).

No se implementa aquí ninguna suite ejecutable: los vectores son contractuales y se ejecutarán cuando exista autorización para implementar el exportador.
