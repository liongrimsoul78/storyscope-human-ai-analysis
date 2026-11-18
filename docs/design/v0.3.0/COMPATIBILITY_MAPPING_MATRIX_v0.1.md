# Matriz de compatibilidad histórica — v0.1

**Proyecto:** StoryScope Human–AI Analysis
**Fase:** 1.20
**Estado:** inventario y matriz documental; no implementación
**Fecha:** 2026-11-17
**Contrato asociado:** `COMPATIBILITY_EXPORT_CONTRACT_v0.1.md`
**Vectores asociados:** `COMPATIBILITY_TEST_VECTORS_v0.1.md`

Las fuentes históricas se leen en el tag `v0.2.3` (objeto `d7221dab…`, commit `a629af7d…`). Las fuentes de destino se leen en la rama `feature/storyscope-v0.3.0-design`.

---

## 1. Inventario histórico real

### 1.1 Cómo leer este inventario

Se distinguen cinco estados de conocimiento, y **no se mezclan**:

| Estado de conocimiento | Significado |
|---|---|
| **Normativo** | definido en una tabla o regla obligatoria de `v0.2.3` |
| **Usado en ejemplo** | aparece en un ejemplo de calibración real del repositorio |
| **Mencionado, no observado** | aparece en documentación pero no en ningún registro ni ejemplo |
| **Variante** | token equivalente o inconsistente respecto de la norma |
| **No disponible** | el dato no existe en el repositorio y no se reconstruye |

No hay corpus de anotaciones en el repositorio. Por tanto **ninguna frecuencia de estados es calculable**. Las únicas cifras disponibles son prevalencias del corpus del paper (Table 16), que son otra cosa y se citan como tales.

### 1.2 Estados de evidencia

Fuente: `references/evidence-status.md` (tag `v0.2.3`), tabla «Estados de evidencia» y «Regla de decisión».

| # | Nombre exacto | Campo | Nivel | Definición textual | Significado operativo | Condición de asignación | Evidencia exigida | Fuente que demuestra uso | Frecuencia | Variantes / inconsistencias |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | `Presente–alineado` | `Estado de evidencia (5)` | registro atómico | «Un valor directamente observado coincide con la opción/dirección elevada en el corpus del estudio.» | observación presente y alineada con la dirección elevada | paso 3 de la regla: hay valor afirmativamente observable y coincide | valor concreto + dirección; `report-template.md` §3 exige «Observación respaldada» | tabla normativa; `report-template.md` §3 | no calculable | guion U+2013; puede aparecer con `-` o `—` |
| E2 | `Presente–opuesto` | idem | registro atómico | «Un valor directamente observado es el polo alternativo de una característica que tiene una dirección en el estudio.» | contraevidencia afirmativa | paso 3; el valor observado es el polo alternativo | cita o localización + interpretación alternativa (`evidence-status.md`, «Contraevidencia») | tabla normativa; ejemplo de la propia tabla (`Reference Explicitness`) | no calculable | el ejemplo dice «opción diferente de la que el estudio elevó para el grupo comparado» sin precisar si el polo alternativo es también una opción elevada |
| E3 | `Ausente` | idem | registro atómico | «Se buscó la característica y no se halló; su ausencia no es por sí misma un valor direccional.» | ausencia buscada | paso 4; no aparece y la longitud/completitud sostiene la codificación | búsqueda declarada; longitud suficiente | tabla normativa; `SKILL.md` línea 97 | no calculable | — |
| E4 | `No aplicable` | idem | registro atómico | «El rasgo no corresponde al tipo de texto/género/tarea.» | exclusión por género/tarea | paso 2 | motivo de no aplicabilidad | tabla normativa | no calculable | — |
| E5 | `No evaluable` | idem | registro atómico | «Longitud, fragmentariedad, falta de contexto o falta de oportunidad impide decidir.» | imposibilidad de decidir | paso 1 | motivo de limitación | tabla normativa; `worked-examples/01-microrelato-21-palabras.md` («son **No evaluable** por longitud y forma») | no calculable; **usado en ejemplo real** | — |
| E6 | `neutral` | `Estado de evidencia (5)` (regla) | registro atómico | «decidir `Presente–alineado`, `Presente–opuesto` o `neutral`, según la opción y la tabla publicada» | tercera opción de estado en la regla | paso 3 | no definida | `references/evidence-status.md`, «Regla de decisión», paso 3 | no calculable; **mencionado, no observado** | **inconsistencia**: no figura en la tabla normativa de 5 estados; el mismo documento no lo define; `report-template.md` usa `neutro` como dirección |

**Conclusión del eje de estado:** la taxonomía normativa tiene 5 valores; `neutral` es una variante documental que se normaliza a `Presente` + dirección `neutro` (contrato §7.1, R-14, `CE-020`).

### 1.3 Direcciones

Fuente: `references/report-template.md` §3, nota «Estados permitidos / Dirección»; `SKILL.md` §5 «Direction labels».

| # | Nombre exacto | Campo | Nivel | Definición textual | Significado operativo | Condición de asignación | Evidencia exigida | Fuente que demuestra uso | Frecuencia | Variantes / inconsistencias |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | `patrón IA` | `Dirección` | registro atómico | «observed value aligns with an AI-elevated option/mean in the study» (`SKILL.md` línea 103) | alineación con patrón elevado para IA | valor observado coincide con opción/media IA | valor concreto + referencia | `report-template.md` §3; `SKILL.md` §5 | no calculable | — |
| D2 | `patrón humano` | idem | registro atómico | «observed value aligns with a human-elevated option/mean» (línea 104) | alineación con patrón humano | idem | idem | idem | no calculable | — |
| D3 | `mixto` | idem | **característica o agregado** | «one canonical feature has relevant observations pointing in both directions or is genuinely ambiguous» (línea 105) | coexistencia de direcciones en una característica | observaciones en ambas direcciones o ambigüedad genuina | ≥2 observaciones trazables | `report-template.md` §3; `SKILL.md` §5; `SKILL.md` §12 sección 6 | no calculable | en `v0.3.0` `mixed` solo es válido en `ClusterSummary`/`AnalysisRun` (§5.3.3) |
| D4 | `neutro` | idem | registro atómico | «observed but the study does not establish a meaningful directional pattern» (línea 106) | observación sin patrón direccional | valor observado sin patrón establecido | justificación contextual | idem | no calculable | **dos lecturas**: (a) neutralización contextual; (b) el estudio no establece patrón. El texto no las distingue |
| D5 | `no evaluable` | idem | registro atómico | «evidence state does not support direction» (línea 107) | sin dirección asignable | estado `Ausente`/`No aplicable`/`No evaluable` | motivo | idem | no calculable | homónimo del **estado** `No evaluable`; solo difiere la mayúscula |

### 1.4 Etiquetas globales

Fuente: `SKILL.md` §12 sección 6; `report-template.md` §6.

| # | Nombre exacto | Campo | Nivel | Definición textual | Significado operativo | Condición | Evidencia | Fuente | Frecuencia | Variantes |
|---|---|---|---|---|---|---|---|---|---|---|
| G1 | `patrón humano` | `Etiqueta cualitativa global` | ejecución | una de las cinco etiquetas de §6 | síntesis global | puerta de adecuación superada | registros + resúmenes | `SKILL.md` §12; `report-template.md` §6 | no calculable | — |
| G2 | `patrón IA` | idem | ejecución | idem | idem | idem | idem | idem | no calculable | — |
| G3 | `mixto` | idem | ejecución | idem | síntesis global con direcciones distintas | ≥2 observaciones trazables | `record_ids` | idem | no calculable | homónimo de D3 |
| G4 | `neutro` | idem | ejecución | idem | sin patrón global | puerta superada | justificación | idem | no calculable | homónimo de D4 |
| G5 | `evidencia insuficiente` | idem | ejecución | «If the gate fails, the overall result is `evidencia insuficiente`» (`SKILL.md` línea 72) | puerta de adecuación fallida | <500 palabras o género restringido | gate | `SKILL.md` §12; `report-template.md` §6; `worked-examples/…` | no calculable; **usado en ejemplo real** | no es un estado de evidencia |

### 1.5 Valores de opción citados en las fuentes

| Valor literal | Característica | Tipo | Fuente | Prevalencia del corpus (no frecuencia de anotación) |
|---|---|---|---|---|
| `no_subplots` | Subplot Integration | categorical | `evidence-status.md` sección final; `feature-dimension-map.csv`; `core-patterns.md` | IA 79 %, humano 57 % |
| `thematically parallel` | Subplot Integration | categorical | CSV; registry v0.1.2 | IA 21 %, humano 42 % |
| `embodied` | Dominant Emotional Expression | categorical | CSV; registry | IA 81 %, humano 38 % |
| `explicit labels` | Dominant Emotional Expression | categorical | CSV; registry | IA 8 %, humano 29 % |
| `implicit echoes` | Reference Explicitness | categorical | CSV; registry | IA 72 %, humano 50 % |
| `balanced mix` | Reference Explicitness | categorical | CSV; registry; `numeric-integrity-v0.2.3.md` | IA 16 %, humano 37 % |
| `olfactory` | Dominant Sensory Modalities | multi-select | CSV; registry | IA 82 %, humano 57 % |
| `ambivalent/mixed` | Moral Polarity Toward Protagonist | categorical option | CSV; `data-integrity-v0.2.2.md`; registry | IA 38 %, humano 59 % |
| `no_major_withholding` | (opción de ausencia citada) | — | `evidence-status.md` sección final | no consta |
| `no_direct_address` | (opción de ausencia citada) | — | idem | no consta |
| `no_anachrony` | (opción de ausencia citada) | — | idem | no consta |

> `ambivalent/mixed` es un **valor de opción**, no la dirección `mixto`. Confundirlos es el error más probable de un exportador (contrato R-29, `CE-030`).

### 1.6 Fuentes no disponibles

| Fuente buscada | Resultado |
|---|---|
| Esquema `EvidenceRecord` en `v0.2.3` | no existe |
| Esquema `ClusterSummary` en `v0.2.3` | no existe |
| Esquema `AnalysisRun` en `v0.2.3` | no existe |
| Documentación de importación/exportación en `v0.2.3` | no existe |
| Corpus de anotaciones reales | no existe en el repositorio |
| Catálogo completo de opciones del instrumento | no existe; solo 33 patrones elevados |
| Campo de procedencia de la anotación | no existe |
| Offsets de cita | no existen |
| Identificador estable de registro | no existe |

---

## 2. Matriz de conversión

### 2.1 Cómo leer la matriz

Las 15 columnas exigidas se reparten en dos tablas enlazadas por `row_id`. La tabla A contiene las 7 columnas de identificación y destino; la tabla B, las 8 columnas de requisitos y decisión. Una fila de A y su fila homónima de B forman **una sola fila** de la matriz.

Etiquetas de decisión (clasificación documental, **no** enums de StoryScope):

- `conversión fiel`
- `conversión condicionada`
- `preservación sin conversión`
- `conversión no segura`
- `no evaluable con la evidencia disponible`

### 2.2 Tabla A — identificación y destino

| row_id | legacy_field | legacy_value | legacy_scope | legacy_meaning | target_field | target_value | mapping_conditions |
|---|---|---|---|---|---|---|---|
| M-01 | `Estado de evidencia (5)` + `Dirección` | `Presente–alineado` + `patrón IA` | característica unidireccional IA (17) | valor observado = opción elevada para IA | `EvidenceRecord` | `observed`; `pattern_ai`; `reference_pattern_id`=referencia histórica; `aligned`; `reference_pattern` | dirección = `dir(historical_reference_pattern_id)`; span literal; justificación |
| M-02 | idem | `Presente–alineado` + `patrón humano` | característica unidireccional humana (10) | valor observado = opción elevada para humanos | `EvidenceRecord` | `observed`; `pattern_human`; `reference_pattern_id`=referencia; `aligned`; `reference_pattern` | idem |
| M-03 | idem | `Presente–alineado` + `patrón IA` | bidireccional (3) | valor observado = opción elevada para IA, que es la referencia histórica | `EvidenceRecord` | `observed`; `pattern_ai`; `reference_pattern_id`=referencia; `aligned` | idem |
| M-04 | idem | `Presente–alineado` + `patrón humano` | bidireccional (3) | valor observado = opción elevada para humanos; en A2 no es la referencia | `EvidenceRecord` | `observed`; `pattern_human`; `reference_pattern_id`=patrón humano; `opposed` | patrón humano registrado; span; justificación; etiqueta histórica preservada |
| M-05 | idem | `Presente–alineado` + dirección opuesta a la referencia | unidireccional (27) | alineación declarada imposible: la característica solo tiene una dirección elevada | — | — | rechazo de fila |
| M-06 | idem | `Presente–alineado` + valor observado ≠ patrón de referencia | cualquiera | la etiqueta y el valor se contradicen | — | — | rechazo de fila |
| M-07 | idem | `Presente–opuesto` + `patrón humano` | bidireccional | polo humano observado, opuesto a la referencia IA | `EvidenceRecord` | `observed`; `pattern_human`; `reference_pattern_id`=patrón humano; `opposed` | span; justificación; patrón opuesto registrado |
| M-08 | idem | `Presente–opuesto` + `patrón IA` | bidireccional | oposición declarada contra la propia referencia | — | — | rechazo de fila |
| M-09 | idem | `Presente–opuesto` + dirección y/o opción no registrada, con valor observado ≠ patrón de referencia | unidireccional categórica / binaria / multiselección | polo alternativo observado, sin patrón de grupo registrado | `EvidenceRecord` | `observed`; `not_assessed`; `reference_pattern_id=null`; `opposed` | valor alternativo identificable; span; justificación (`INV-A2-11`) |
| M-10 | idem | `Presente–opuesto` | escala (14) u ordinal (5) | oposición declarada en medida continua | `EvidenceRecord` (solo con ancla) | `observed`; `not_assessed`; `opposed` | ancla o constructo opuesto explícito; sin ancla → cuarentena |
| M-11 | `Cita o ubicación` | ausente o no literal | cualquiera | no hay localización verificable | — | — | cuarentena |
| M-12 | `Por qué / alternativa contextual` | ausente | cualquiera con `Presente–opuesto` | no hay justificación de contraevidencia | — | — | cuarentena |
| M-13 | `Estado de evidencia (5)` | `Ausente` | registro atómico, ejecución completa | se buscó y no se halló | `EvidenceRecord` | `not_observed`; `sufficient`; `not_assessed`; `none`; `status_reason`; `absence_justification`; `search_scope` | `completeness=completo`; búsqueda declarada; motivo |
| M-14 | idem | `Ausente` | fragmento o completitud desconocida | ausencia no sostenible por oportunidad | `EvidenceRecord` | `not_evaluable`; `limited`/`unknown`; `not_assessed`; `none`; `status_reason` | motivo textual; etiqueta histórica preservada |
| M-15 | idem | `No aplicable` | registro atómico | rasgo ajeno al género/tarea | `EvidenceRecord` | `not_applicable`; `none`/`unknown`; `not_assessed`; `status_reason` | motivo textual; sin motivo → cuarentena |
| M-16 | idem | `No evaluable` | registro atómico | longitud/contexto impiden decidir | `EvidenceRecord` | `not_evaluable`; `limited`/`none`/`unknown`; `not_assessed`; `status_reason` | motivo textual; sin motivo → cuarentena |
| M-17 | `Estado de evidencia (5)` (regla) | `neutral` (variante) o `Presente–alineado` + `neutro` | registro atómico | codificación histórica de «presente pero neutro», sin estado normativo propio | `EvidenceRecord` | `observed`; `neutral`; `contextual_neutralization`; `reference_pattern_id=null`; `not_assessed` | `alignment_basis_detail` no nulo; etiqueta preservada |
| M-18 | `Estado` + `Dirección` | `Presente–alineado` + `neutro` (lectura a: neutralización contextual) | registro atómico | observación evaluada sin alineación direccional | `EvidenceRecord` | igual que M-17 | detalle que demuestre evaluación contra referencia aplicable |
| M-19 | `Estado` + `Dirección` | `Presente–alineado` + `neutro` (lectura b: el estudio no establece patrón) | registro atómico | no existe patrón direccional aplicable | `EvidenceRecord` | `observed`; `not_assessed`; `none`; `reference_pattern_id=null`; `not_assessed` | justificación de ausencia de patrón |
| M-20 | `Estado` + `Dirección` | `neutro` sin lectura seleccionable | registro atómico | ambigüedad no resoluble desde la fuente | — | — | rechazo de fila |
| M-21 | `Dirección` | `mixto` | característica | observaciones en ambas direcciones o ambigüedad | — (agregado) | requiere ≥2 `EvidenceRecord` + `ClusterSummary` | división documentada en ≥2 observaciones; no reconstruible desde una fila |
| M-22 | `Etiqueta cualitativa global` | `mixto` | ejecución | síntesis global con direcciones distintas | `ClusterSummary.alignment` | `mixed` | clúster identificado + ≥2 `record_ids` con alineaciones distintas; sin campo de ejecución → preservar |
| M-23 | idem | `evidencia insuficiente` | ejecución | puerta de adecuación fallida | `AnalysisRun.adequacy` (condicionado) | estado + motivos | enum de destino no definido → preservar |
| M-24 | `Característica/valor observado` | `no_subplots` | registro atómico, historia completa | opción categórica explícita de ausencia | `EvidenceRecord` | `observed`; `observed_option_id`=`ssha.pattern.subplot_integration.no_subplots`; `pattern_ai`; `aligned` | span; oportunidad suficiente; no es `not_observed` |
| M-25 | idem | `no_major_withholding`, `no_direct_address`, `no_anachrony` | registro atómico | opciones de ausencia citadas, no registradas | `EvidenceRecord` | `observed`; `observed_option_id=null`; `observed_value_text` literal | span; oportunidad suficiente |
| M-26 | `Dimensión` (tabla §3) | cualquier estado | dimensión sin `feature_id` | observación descriptiva de dimensión | `DimensionProfile` | `neutral_summary`; `limitations`; `coverage_status` | no se convierte en `EvidenceRecord` |
| M-27 | `Característica/valor observado` (tabla §4) | cualquier estado | característica sin `feature_id` resoluble | registro atómico sin referencia canónica | — | — | rechazo de fila |
| M-28 | `Estado de evidencia (5)` o `Dirección` | token no reconocido | cualquiera | vocabulario fuera de las fuentes | — | — | rechazo de fila |
| M-29 | ambos | combinación imposible (p. ej. `Ausente` + `patrón IA`; `Presente–opuesto` con valor = patrón de referencia; `Presente–opuesto` + `neutro`) | cualquiera | estado y dirección se contradicen | — | — | rechazo de fila |
| M-30 | fila completa | duplicado idéntico o conflictivo | cualquiera | dos filas con la misma clave de origen | un registro o cuarentena | deduplicar si idénticas; cuarentena si difieren | misma `(digest, locator)` |
| M-31 | `Dirección del estudio` (tabla §4) | p. ej. `AI` | característica | dirección elevada del paper, no del texto | — | — | nunca se copia a `research_alignment`; se resuelve desde el registro |
| M-32 | `Fuerza` | texto libre | registro atómico | intensidad cualitativa sin vocabulario controlado | `evidence_strength` | `weak`/`moderate`/`strong` si el token coincide; si no, `not_rated` | texto original preservado |
| M-33 | `Característica/valor observado` | `ambivalent/mixed` | Moral Polarity Toward Protagonist | valor de opción elevado para humanos | `EvidenceRecord` | `observed`; `pattern_human`; `reference_pattern_id`=`…ambivalent_mixed`; `aligned` | no interpretar como dirección `mixto` |
| M-34 | ejecución | `feature_registry_version` desconocida | ejecución | no se puede resolver la referencia histórica | — | — | rechazo de ejecución |
| M-35 | `Cita o ubicación` | texto no literal | cualquiera | la cita no es subcadena exacta | — | — | cuarentena |
| M-36 | ejecución | origen no declarado o texto fuente ausente | ejecución | faltan precondiciones de §5.4 | — | — | rechazo de ejecución |
| M-37 | oportunidad | asimetría humano/IA | ejecución | misma oportunidad evaluada con estándares distintos | — | — | revisión manual |
| M-38 | corpus | frecuencia y variantes reales | inventario | no hay corpus histórico | — | — | sin datos |

### 2.3 Tabla B — requisitos, pérdida y decisión

| row_id | evidence_requirements | source_span | rationale | historical_reference | information_loss | reversibility | decision | source_reference |
|---|---|---|---|---|---|---|---|---|
| M-01 | valor observado + justificación | obligatorio, literal | `INV-A2-09`: alineación = referencia | = `historical_reference_pattern_id` (IA) | ninguna | A | conversión fiel | `evidence-status.md` fila 1; `report-template.md` §3; Spec §5.3 tabla; §6.4 |
| M-02 | idem | obligatorio | idem con dirección humana | = referencia (humana) | ninguna | A | conversión fiel | idem |
| M-03 | idem | obligatorio | referencia histórica = patrón IA | = referencia | ninguna | A | conversión fiel | Spec §5.3.5; §6.4 |
| M-04 | idem | obligatorio | A2 exige `opposed` porque la referencia es IA | = patrón IA | la etiqueta histórica no se deriva del registro | B | conversión condicionada | Spec §5.3.5; `INV-A2-10`; Review Notes «Consolidación A2» |
| M-05 | — | — | no existe dirección elevada opuesta en unidireccional | — | fila no convertida | D | conversión no segura | Spec §6.4 `INV-A2-09`; CSV |
| M-06 | — | — | contradicción interna de la fuente | — | fila no convertida | D | conversión no segura | `evidence-status.md` paso 3 |
| M-07 | span + justificación | obligatorio | contraevidencia afirmativa contra referencia IA | = patrón IA | ninguna | A | conversión fiel | `evidence-status.md` fila 2; Spec §5.3.5 |
| M-08 | — | — | oposición contra la referencia no es oposición | — | fila no convertida | D | conversión no segura | `INV-A2-10` |
| M-09 | valor alternativo + span + justificación | obligatorio | `INV-A2-11`: unidireccional `opposed` sin patrón | referencia de la característica | la dirección histórica no se afirma en el dominio | B | conversión condicionada | Spec §6.4 `INV-A2-11`; §6.5; `CE-026`/`CE-022` |
| M-10 | ancla + span + justificación | obligatorio | §6.5: sin umbrales ni anclas inventadas | referencia de la característica | sin ancla, la oposición no es verificable | D | conversión no segura | Spec §6.5; §6.4 `INV-A2-15` |
| M-11 | span | obligatorio | regla 5: `observed` exige span verificable | — | fila no convertida | D | conversión no segura | Spec §5.3 regla 5; §5.4 |
| M-12 | justificación | obligatorio | contraevidencia exige interpretación alternativa | — | fila no convertida | D | conversión no segura | `evidence-status.md` «Contraevidencia» |
| M-13 | búsqueda + completitud | no exigido para ausencia | Spec: `not_observed` exige `sufficient` | referencia no se usa | ninguna | A | conversión fiel | Spec §5.3 tabla; §5.3.2 |
| M-14 | motivo | no exigido | Spec: `Ausente` sin oportunidad = `not_evaluable` | — | el estado cambia; etiqueta preservada | B | conversión condicionada | Spec §5.3 tabla fila `Ausente` |
| M-15 | motivo | no exigido | `INV-A2-13` | — | ninguna si hay motivo | A | conversión fiel | Spec §5.3.2; `INV-A2-13` |
| M-16 | motivo | no exigido | `INV-A2-13` | — | ninguna si hay motivo | A | conversión fiel | idem |
| M-17 | detalle de neutralización | recomendado | `INV-A2-12` | no aplica | token `neutral` solo en procedencia | B | conversión condicionada | Spec §5.3; `INV-A2-12` |
| M-18 | detalle contextual | recomendado | neutralidad evaluada | no aplica | ninguna | B | conversión condicionada | Spec §5.3 (`neutral`); `SKILL.md` línea 106 |
| M-19 | justificación | recomendado | no hay patrón aplicable | no aplica | se pierde la asociación con `neutro` salvo procedencia | B | conversión condicionada | Spec §5.3 caso 3; `SKILL.md` línea 106 |
| M-20 | — | — | dos lecturas incompatibles | — | fila no convertida | D | conversión no segura | `SKILL.md` línea 106 |
| M-21 | ≥2 observaciones | — | `mixed` es propiedad de conjuntos | — | la fila no se convierte; se preserva | D | conversión no segura | Spec §5.3.3; `INV-A2` nota |
| M-22 | `record_ids` | — | `mixed` agregado con trazabilidad | no aplica | sin campo de ejecución, solo clúster | B | preservación sin conversión | Spec §5.3.3; §5.6; §15-B1 del contrato |
| M-23 | gate + motivos | — | etiqueta global, no estado | no aplica | enum de destino indefinido | B | preservación sin conversión | `SKILL.md` §12; Spec §5.2; §15-B2 |
| M-24 | span + oportunidad | obligatorio | §5.3.4: opción explícita de ausencia es observación | = referencia (IA) | ninguna | A | conversión fiel | Spec §5.3.4; `evidence-status.md` sección final |
| M-25 | span + oportunidad | obligatorio | opción no registrada: no se inventa ID | = referencia de la característica | falta `observed_option_id` | B | conversión condicionada | Spec §5.3.4; §5.3 (`observed_option_id` nullable) |
| M-26 | — | — | no hay `feature_id`; el destino es descriptivo | no aplica | no hay registro atómico | A | preservación sin conversión | Spec §5.5; `report-template.md` §3 |
| M-27 | — | — | registro atómico sin `feature_id` | — | fila no convertida | D | conversión no segura | Spec §5.3 (`feature_id` obligatorio) |
| M-28 | — | — | vocabulario no documentado | — | fila no convertida | D | conversión no segura | contrato §7.4 |
| M-29 | — | — | combinación fuera de la taxonomía | — | fila no convertida | D | conversión no segura | `evidence-status.md` columna «¿Puede tener dirección?» |
| M-30 | — | — | idempotencia por clave de origen | — | ninguna si idénticas | A / D | conversión condicionada | contrato §11 |
| M-31 | — | — | campo de referencia, no de observación | se resuelve desde el registro | se evita una alineación fabricada | A | preservación sin conversión | `report-template.md` §4; Spec §5.3.5 |
| M-32 | — | — | `v0.2.3` no define vocabulario de fuerza | no aplica | intensidad original solo en procedencia | B | conversión condicionada | `report-template.md` §3–§4; Spec §5.3 |
| M-33 | span + justificación | obligatorio | opción humana elevada; `mixed` es parte del nombre | = referencia humana | ninguna | A | conversión fiel | CSV fila Moral Polarity; `data-integrity-v0.2.2.md`; registry |
| M-34 | — | — | sin versión fijada no hay resolución A2 | irresoluble | ejecución no convertida | D | conversión no segura | Spec §5.7; `INV-A2-16` |
| M-35 | cita literal | obligatorio | §5.4: sin normalización | — | fila no convertida | D | conversión no segura | Spec §5.4 |
| M-36 | declaración de origen + texto | — | precondiciones de entrada | — | ejecución no convertida | D | conversión no segura | contrato §5.4 |
| M-37 | — | — | `evidence-status.md` «Regla de simetría» | — | revisión manual | D | no evaluable con la evidencia disponible | `evidence-status.md` «Regla de simetría» |
| M-38 | — | — | no hay corpus en el repositorio | — | — | — | no evaluable con la evidencia disponible | inventario §1.1 |

### 2.4 Recuento de decisiones

| Decisión | Filas |
|---|---:|
| conversión fiel | 9 |
| conversión condicionada | 9 |
| preservación sin conversión | 4 |
| conversión no segura | 14 |
| no evaluable con la evidencia disponible | 2 |
| **Total** | **38** |

---

## 3. Casos ambiguos y no convertibles

### 3.1 Ambigüedades de la fuente

**A1. `neutral` como estado y `neutro` como dirección.**
`evidence-status.md` ofrece `neutral` en el paso 3 de la regla de decisión; la tabla normativa no lo incluye y `report-template.md` usa `neutro` como dirección. Además, la taxonomía de 5 estados no tiene un estado «presente neutro», de modo que la plantilla solo puede codificarlo como `Presente–alineado` + `neutro` (o con la variante `neutral`). El contrato no crea un sexto estado: normaliza ambas formas a `observed` + dirección `neutro` y preserva el token. `Presente–opuesto` + `neutro` sigue siendo una contradicción.

**A2. `Presente–alineado` en bidireccional con polo humano.**
La opción humana también está elevada, de modo que «alineado» y «opuesto» son ambos defendibles según la pregunta. A2 fija la referencia en el patrón IA. El contrato convierte a `opposed`, preserva la etiqueta y lo declara (`CE-021`). No lo presenta como error de la fuente.

**A3. `Presente–opuesto` sin polo registrado.**
En características unidireccionales el polo alternativo no tiene patrón. `INV-A2-11` exige `not_assessed`, lo que impide afirmar una dirección. El contrato lo acepta como `opposed` + `not_assessed` y conserva la dirección histórica como dato de procedencia.

**A4. `mixto` en dos niveles.**
Como dirección de característica (D3) y como etiqueta global (G3). El primero es un agregado dentro de un registro atómico y se rechaza; el segundo puede expresarse en `ClusterSummary`. No son intercambiables.

**A5. `ambivalent/mixed` como valor.**
Es una opción de Moral Polarity Toward Protagonist, no una dirección. Se convierte como observación alineada al patrón humano.

**A6. `Dirección del estudio` (§4).**
Describe el paper, no el texto. Copiarla a `research_alignment` fabricaría alineación. Se prohíbe.

### 3.2 Casos no convertibles

| Caso | Motivo | Resultado |
|---|---|---|
| `Presente–alineado` contra la única dirección elevada | contradicción lógica | rechazo |
| `Presente–opuesto` en escala sin ancla | §6.5 prohíbe umbrales inventados | cuarentena |
| `Presente–opuesto` sin span o sin justificación | contraevidencia no demostrada | cuarentena |
| `mixto` a nivel de característica | agregado en registro atómico | cuarentena |
| fila de característica sin `feature_id` | no hay referencia canónica | rechazo |
| estado o dirección desconocidos | vocabulario no documentado | rechazo |
| estado y dirección incompatibles | fuera de la taxonomía | rechazo |
| versión de registro irresoluble | A2 no resoluble | rechazo de ejecución |
| origen no declarado | campo obligatorio sin fuente | rechazo de ejecución |
| texto fuente ausente | spans no verificables | rechazo de ejecución |

### 3.3 Pérdidas potenciales

| Pérdida | Cuándo | Mitigación |
|---|---|---|
| Etiqueta histórica distinta de la relación A2 | M-04 | `legacy_raw` + `CE-021` |
| Estado degradado (`Ausente` → `not_evaluable`) | M-14 | `legacy_raw` + `loss_report` |
| Dirección histórica no afirmable | M-09, M-25 | `legacy_raw` + `CE-026`/`CE-022` |
| Intensidad original | M-32 | `legacy_raw` + `CE-023` |
| Asociación `neutro` ↔ registro | M-18, M-19 | `legacy_raw` + `loss_report` |
| Etiqueta global sin campo | M-22, M-23 | informe de exportación |
| Fila entera | cuarentena/rechazo | `preserved_payload` |

Ninguna pérdida es silenciosa: toda fila emitida, preservada, en cuarentena o rechazada tiene entrada en el informe (contrato §10.3, §12).

---

## 4. Verificación cruzada

| Control | Resultado |
|---|---|
| Todo estado de la matriz existe en `evidence-status.md` | sí (E1–E5); E6 marcado como variante |
| Toda dirección existe en `report-template.md` §3 o `SKILL.md` §5 | sí (D1–D5) |
| Toda etiqueta global existe en `SKILL.md` §12 | sí (G1–G5) |
| Toda opción citada existe en el CSV o en el registro | sí (§1.5); tres opciones de ausencia solo en `evidence-status.md`, marcadas |
| Todo campo de destino existe en la Spec | sí; `AnalysisRun` sin campo de alineación declarado como bloqueo |
| No se introduce ningún enum nuevo | sí; las etiquetas de decisión son clasificación documental |
| No se duplica la referencia histórica | sí; se resuelve desde el registro |
| No se altera `Presente–opuesto` | sí; M-07/M-09/M-10 exigen contraevidencia afirmativa |
| Ausencia ≠ oposición | sí; M-13/M-14 y R-12 |
| Atómico ≠ agregado | sí; M-21/M-22 |
| Reversibilidad declarada por fila | sí |
