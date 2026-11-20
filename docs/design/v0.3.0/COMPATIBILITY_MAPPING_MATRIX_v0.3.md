# Matriz de compatibilidad histórica — v0.3

**Proyecto:** StoryScope Human–AI Analysis
**Fase:** 1.22 — auditoría de coherencia del contrato y cierre de la ruta §4
**Estado:** inventario y matriz documental; no implementación
**Fecha:** 2026-11-19
**Contrato asociado:** `COMPATIBILITY_EXPORT_CONTRACT_v0.3.md`
**Vectores asociados:** `COMPATIBILITY_TEST_VECTORS_v0.3.md`
**Predecesores preservados:** `COMPATIBILITY_MAPPING_MATRIX_v0.1.md`, `COMPATIBILITY_MAPPING_MATRIX_v0.2.md`

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

### 1.2 Niveles de la plantilla histórica

| Tabla | Nivel | Campos de estado/dirección | ¿Genera `EvidenceRecord`? |
|---|---|---|---|
| §3 Perfil por dimensiones | dimensión | sí: `Estado de evidencia (5)`, `Dirección` | **no** |
| §4 Indicadores centrales | característica | **no** | sí, si el valor y el span son resolubles |
| §6 Síntesis | ejecución | etiqueta global | no (run-level) |

Esta separación es la corrección central de v0.3. La v0.2 trataba el estado de §3 como si pudiera alimentar características de §4; eso es un join prohibido.

### 1.3 Estados de evidencia

Fuente: `references/evidence-status.md` (tag `v0.2.3`), tabla «Estados de evidencia» y «Regla de decisión».

| # | Nombre exacto | Campo | Nivel | Definición textual | Significado operativo | Condición de asignación | Evidencia exigida | Fuente que demuestra uso | Frecuencia | Variantes / inconsistencias |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | `Presente–alineado` | `Estado de evidencia (5)` | dimensión (§3); extensión F+ | «Un valor directamente observado coincide con la opción/dirección elevada en el corpus del estudio.» | observación presente y alineada | paso 3 de la regla: hay valor afirmativamente observable y coincide | valor concreto + dirección; `report-template.md` §3 exige «Observación respaldada» | tabla normativa; `report-template.md` §3 | no calculable | guion U+2013; puede aparecer con `-` o `—` |
| E2 | `Presente–opuesto` | idem | dimensión (§3); extensión F+ | «Un valor directamente observado es el polo alternativo de una característica que tiene una dirección en el estudio.» | contraevidencia afirmativa | paso 3; el valor observado es el polo alternativo | cita o localización + interpretación alternativa (`evidence-status.md`, «Contraevidencia») | tabla normativa; ejemplo de la propia tabla (`Reference Explicitness`) | no calculable | en §3 es contraevidencia de dimensión; en §4 estándar no existe este token; la contraevidencia de característica se expresa en `Contraevidencia real` |
| E3 | `Ausente` | idem | dimensión (§3) | «Se buscó la característica y no se halló; su ausencia no es por sí misma un valor direccional.» | ausencia buscada | paso 4; no aparece y la longitud/completitud sostiene la codificación | búsqueda declarada; longitud suficiente | tabla normativa; `SKILL.md` línea 97 | no calculable | **no** se convierte en `not_observed` de característica: no hay `feature_id` |
| E4 | `No aplicable` | idem | dimensión (§3) | «El rasgo no corresponde al tipo de texto/género/tarea.» | exclusión por género/tarea | paso 2 | motivo de no aplicabilidad | tabla normativa | no calculable | se expresa como `DimensionProfile.coverage_status=not_applicable` |
| E5 | `No evaluable` | idem | dimensión (§3) | «Longitud, fragmentariedad, falta de contexto o falta de oportunidad impide decidir.» | imposibilidad de decidir | paso 1 | motivo de limitación | tabla normativa; `worked-examples/01-microrelato-21-palabras.md` | no calculable; **usado en ejemplo real** | se expresa como `DimensionProfile.coverage_status=not_assessable` |
| E6 | `neutral` | `Estado de evidencia (5)` (regla) | dimensión (§3); extensión F+ | «decidir `Presente–alineado`, `Presente–opuesto` o `neutral`, según la opción y la tabla publicada» | tercera opción de estado en la regla | paso 3 | no definida | `references/evidence-status.md`, «Regla de decisión», paso 3 | no calculable; **mencionado, no observado** | **inconsistencia**: no figura en la tabla normativa; `report-template.md` usa `neutro` como dirección |

**Conclusión del eje de estado:** la taxonomía normativa tiene 5 valores; `neutral` es una variante documental que se normaliza a observación presente + dirección `neutro` (contrato §7.1, R-17, `CE-020`). En la ruta D no se crea un sexto estado ni un `EvidenceRecord`.

### 1.4 Direcciones

Fuente: `references/report-template.md` §3, nota «Estados permitidos / Dirección»; `SKILL.md` §5 «Direction labels».

| # | Nombre exacto | Campo | Nivel | Definición textual | Significado operativo | Condición de asignación | Evidencia exigida | Fuente que demuestra uso | Frecuencia | Variantes / inconsistencias |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | `patrón IA` | `Dirección` | dimensión (§3); extensión F+ | «observed value aligns with an AI-elevated option/mean in the study» | alineación con patrón elevado para IA | valor observado coincide con opción/media IA | valor concreto + referencia | `report-template.md` §3; `SKILL.md` §5 | no calculable | — |
| D2 | `patrón humano` | idem | dimensión (§3); extensión F+ | «observed value aligns with a human-elevated option/mean» | alineación con patrón humano | idem | idem | idem | no calculable | — |
| D3 | `mixto` | idem | característica o agregado | «one canonical feature has relevant observations pointing in both directions or is genuinely ambiguous» | coexistencia de direcciones en una característica | observaciones en ambas direcciones o ambigüedad genuina | ≥2 observaciones trazables | `report-template.md` §3; `SKILL.md` §5; `SKILL.md` §12 | no calculable | en `v0.3.0` `mixed` solo es válido en `ClusterSummary`/`AnalysisRun` |
| D4 | `neutro` | idem | dimensión (§3); extensión F+ | «observed but the study does not establish a meaningful directional pattern» | observación sin patrón direccional | valor observado sin patrón establecido | justificación contextual | idem | no calculable | **dos lecturas**: (a) neutralización contextual; (b) el estudio no establece patrón |
| D5 | `no evaluable` | idem | dimensión (§3) | «evidence state does not support direction» | sin dirección asignable | estado `Ausente`/`No aplicable`/`No evaluable` | motivo | idem | no calculable | homónimo del **estado** `No evaluable`; solo difiere la mayúscula |

### 1.5 Etiquetas globales

Fuente: `SKILL.md` §12 sección 6; `report-template.md` §6.

| # | Nombre exacto | Campo | Nivel | Definición textual | Significado operativo | Condición | Evidencia | Fuente | Frecuencia | Variantes |
|---|---|---|---|---|---|---|---|---|---|---|
| G1 | `patrón humano` | `Etiqueta cualitativa global` | ejecución | una de las cinco etiquetas de §6 | síntesis global | puerta de adecuación superada | registros + resúmenes | `SKILL.md` §12; `report-template.md` §6 | no calculable | — |
| G2 | `patrón IA` | idem | ejecución | idem | idem | idem | idem | idem | no calculable | — |
| G3 | `mixto` | idem | ejecución | idem | síntesis global con direcciones distintas | ≥2 observaciones trazables | `record_ids` | idem | no calculable | homónimo de D3 |
| G4 | `neutro` | idem | ejecución | idem | sin patrón global | puerta superada | justificación | idem | no calculable | homónimo de D4 |
| G5 | `evidencia insuficiente` | idem | ejecución | «If the gate fails, the overall result is `evidencia insuficiente`» | puerta de adecuación fallida | <500 palabras o género restringido | gate | `SKILL.md` §12; `report-template.md` §6 | no calculable; **usado en ejemplo real** | no es un estado de evidencia |

**Regla v0.3:** la etiqueta global **no** se escribe en `ClusterSummary.alignment` por defecto, ni se crea un campo nuevo en `AnalysisRun`. Se preserva en `run_level` del informe externo (R-20, R-21, R-22). `ClusterSummary.alignment=mixed` solo cuando existe una síntesis de clúster explícita con ≥2 `record_ids` con alineaciones distintas, independiente de la etiqueta global.

### 1.6 Valores de opción citados en las fuentes

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
| `protagonist choice` | Agency in Resolution | categorical option | CSV; registry | IA 69 %, humano 46 % |
| `internal understanding` | Mode of Resolution | categorical option | CSV; registry | IA 47 %, humano 27 % |
| `no_major_withholding` | (opción de ausencia citada) | — | `evidence-status.md` sección final | no consta |
| `no_direct_address` | (opción de ausencia citada) | — | idem | no consta |
| `no_anachrony` | (opción de ausencia citada) | — | idem | no consta |

> `ambivalent/mixed` es un **valor de opción**, no la dirección `mixto`. Confundirlos es el error más probable de un exportador (contrato §15.3, `CE-030`).
>
> `protagonist choice` pertenece a `Agency in Resolution`, no a `Mode of Resolution`. Un exportador que asigne ese valor a `Mode of Resolution` comete un error de característica (vector TV-04 corregido en v0.3).

### 1.7 Fuentes no disponibles

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
| Estado o dirección a nivel de característica en §4 | no existe |
| Oportunidad de observación a nivel de característica | no existe |

---

## 2. Matriz de conversión

### 2.1 Cómo leer la matriz

Las 15 columnas exigidas se reparten en dos tablas enlazadas por `row_id`. La tabla A contiene las 8 columnas de identificación y destino; la tabla B, las 9 columnas de requisitos y decisión. Una fila de A y su fila homónima de B forman **una sola fila** de la matriz.

Rutas:

- **D** — fila §3 (dimensión). No genera `EvidenceRecord`.
- **F** — fila §4 estándar (sin estado ni dirección). Genera `EvidenceRecord` derivado.
- **F+** — fila de característica que porta explícitamente estado y dirección (extensión no estándar).
- **X** — ejecución o agregado.

Etiquetas de decisión (clasificación documental, **no** enums de StoryScope):

- `conversión fiel`
- `conversión condicionada`
- `preservación sin conversión`
- `conversión no segura`
- `no evaluable con la evidencia disponible`

### 2.2 Tabla A — identificación y destino

| row_id | route | legacy_field | legacy_value | legacy_scope | legacy_meaning | target_field | target_value | mapping_conditions |
|---|---|---|---|---|---|---|---|---|
| M-01 | F+ | `Estado` + `Dirección` | `Presente–alineado` + `patrón IA` | característica unidireccional IA (17) | valor = opción elevada para IA | `EvidenceRecord` | `observed`; `pattern_ai`; `reference_pattern_id`=referencia; `aligned`; `reference_pattern` | dirección = `dir(historical_reference_pattern_id)`; span literal; justificación |
| M-02 | F+ | idem | `Presente–alineado` + `patrón humano` | característica unidireccional humana (10) | valor = opción elevada para humanos | `EvidenceRecord` | `observed`; `pattern_human`; `reference_pattern_id`=referencia; `aligned`; `reference_pattern` | idem |
| M-03 | F+ | idem | `Presente–alineado` + `patrón IA` | bidireccional (3) | valor = polo IA, que es la referencia histórica | `EvidenceRecord` | `observed`; `pattern_ai`; `reference_pattern_id`=referencia; `aligned` | idem |
| M-04 | F+ | idem | `Presente–alineado` + `patrón humano` | bidireccional (3) | valor = polo humano; en A2 no es la referencia | — | **bloqueado** (R-04) | patrón humano registrado; span; justificación; cuarentena `CE-021` |
| M-05 | F+ | idem | `Presente–alineado` + dirección opuesta a la referencia | unidireccional (27) | alineación declarada imposible | — | — | rechazo de fila |
| M-06 | F+ | idem | `Presente–alineado` + valor observado ≠ patrón de referencia | cualquiera | la etiqueta y el valor se contradicen | — | — | rechazo de fila |
| M-07 | F+ | idem | `Presente–opuesto` + `patrón IA` | bidireccional | oposición declarada contra la propia referencia | — | — | rechazo de fila |
| M-08 | F+ | idem | `Presente–opuesto` + `patrón humano` | bidireccional | no resoluble sin asumir referencia AI-first | — | — | cuarentena (`CE-035`) |
| M-09 | F+ | idem | `Presente–opuesto` + dirección y/o opción no registrada, valor ≠ referencia | unidireccional categórica / binaria / multiselección | polo alternativo observado, sin patrón de grupo registrado | `EvidenceRecord` | `observed`; `not_assessed`; `reference_pattern_id=null`; `opposed` | valor alternativo identificable; span; justificación |
| M-10 | F+ | idem | `Presente–opuesto` | escala (14) u ordinal (5) | oposición declarada en medida continua | `EvidenceRecord` (solo con ancla) | `observed`; `not_assessed`; `opposed` | ancla o constructo opuesto explícito; sin ancla → cuarentena |
| M-11 | F+ | `Cita o ubicación` | ausente o no literal | cualquiera | no hay localización verificable | — | — | cuarentena |
| M-12 | F+ | `Por qué / alternativa contextual` | ausente | cualquiera con `Presente–opuesto` | no hay justificación de contraevidencia | — | — | cuarentena |
| M-13 | D | `Estado de evidencia (5)` | `Ausente` | dimensión, ejecución completa | se buscó y no se halló | `DimensionProfile` | `coverage_status=descriptive_assessed`; estado literal en informe | no se emite `not_observed`; búsqueda declarada | 
| M-14 | D | idem | `Ausente` | dimensión, fragmento o completitud desconocida | ausencia no sostenible por oportunidad | `DimensionProfile` | `coverage_status=partially_assessed`/`not_assessable`; estado literal en informe | motivo textual |
| M-15 | D | idem | `No aplicable` | dimensión | rasgo ajeno al género/tarea | `DimensionProfile` | `coverage_status=not_applicable`; estado literal en informe | motivo textual; sin motivo → cuarentena |
| M-16 | D | idem | `No evaluable` | dimensión | longitud/contexto impiden decidir | `DimensionProfile` | `coverage_status=not_assessable`; estado literal en informe | motivo textual; sin motivo → cuarentena |
| M-17 | F+/D | `Estado de evidencia (5)` (regla) | `neutral` (variante) o `Presente–alineado` + `neutro` | característica o dimensión | codificación histórica de «presente pero neutro» | `EvidenceRecord` (F+) o `DimensionProfile` (D) | F+: `observed` + `neutral` (a) o `not_assessed` (b); D: `descriptive_assessed` | `alignment_basis_detail` no nulo para lectura a; ambas lecturas se mantienen |
| M-18 | F+ | `Estado` + `Dirección` | `Presente–alineado` + `neutro` (lectura a) | característica | observación evaluada sin alineación direccional | `EvidenceRecord` | igual que M-17 | detalle que demuestre evaluación contra referencia aplicable |
| M-19 | F+ | `Estado` + `Dirección` | `Presente–alineado` + `neutro` (lectura b) | característica | no existe patrón direccional aplicable | `EvidenceRecord` | `observed`; `not_assessed`; `none`; `reference_pattern_id=null` | justificación de ausencia de patrón |
| M-20 | F+ | `Estado` + `Dirección` | `neutro` sin lectura seleccionable | característica | ambigüedad no resoluble desde la fuente | — | — | rechazo de fila |
| M-21 | F+ | `Dirección` | `mixto` | característica | observaciones en ambas direcciones o ambigüedad | — (agregado) | requiere ≥2 `EvidenceRecord` + `ClusterSummary` | división documentada en ≥2 observaciones |
| M-22 | X | `Etiqueta cualitativa global` | `mixto` | ejecución | síntesis global con direcciones distintas | **ninguno por defecto** | preservar en `run_level.legacy_global_label` | solo con síntesis de clúster explícita → `ClusterSummary.alignment=mixed` |
| M-23 | X | idem | `evidencia insuficiente` | ejecución | puerta de adecuación fallida | `run_level` | estado + motivos | enum de destino no definido → preservar |
| M-24 | X | idem | `adequacy_gate` | ejecución | puerta de adecuación | `run_level` | — | preservar |
| M-25 | X | idem | `analysis_quality_confidence` | ejecución | confianza global en la calidad del análisis | `run_level` | **no** copiar a `EvidenceRecord.assessment_confidence` | preservar |
| M-26 | F | `Característica/valor observado` | `no_subplots` | característica, historia completa | opción categórica explícita de ausencia | `EvidenceRecord` | `observed`; `observed_option_id`=`ssha.pattern.subplot_integration.no_subplots`; `pattern_ai`; `aligned` | span; oportunidad suficiente; no es `not_observed` |
| M-27 | F | idem | `no_major_withholding`, `no_direct_address`, `no_anachrony` | característica | opciones de ausencia citadas, no registradas | `EvidenceRecord` | `observed`; `observed_option_id=null`; `observed_value_text` literal | span; oportunidad suficiente |
| M-28 | D | `Dimensión` (tabla §3) | cualquier estado | dimensión sin `feature_id` | observación descriptiva de dimensión | `DimensionProfile` | `neutral_summary`; `limitations`; `coverage_status` | no se convierte en `EvidenceRecord` |
| M-29 | F | `Característica/valor observado` (tabla §4) | cualquier valor | característica sin `feature_id` resoluble | registro atómico sin referencia canónica | — | — | rechazo de fila |
| M-30 | F+/D | `Estado de evidencia (5)` | token no reconocido | cualquiera | vocabulario fuera de las fuentes (estado) | — | — | rechazo de fila |
| M-31 | F+ | ambos | combinación imposible | cualquiera | estado y dirección se contradicen | — | — | rechazo de fila |
| M-32 | F | fila completa | duplicado en la misma localización fuente | cualquiera | reextracción de la misma fila | un registro o cuarentena | deduplicar si idénticas; cuarentena si difieren | misma `(digest, sublocator)` |
| M-33 | F | `Dirección del estudio` (tabla §4) | p. ej. `AI` | característica | dirección elevada del paper, no del texto | — | — | nunca se copia a `research_alignment`; se resuelve desde el registro |
| M-34 | F+/F | `Fuerza` | texto libre | característica o dimensión | intensidad cualitativa sin vocabulario controlado | `evidence_strength` | `weak`/`moderate`/`strong` si hay regla; si no, `not_rated` | texto original preservado |
| M-35 | F | `Característica/valor observado` | `ambivalent/mixed` | Moral Polarity Toward Protagonist | valor de opción elevado para humanos | `EvidenceRecord` | `observed`; `pattern_human`; `reference_pattern_id`=`…ambivalent_mixed`; `aligned` | no interpretar como dirección `mixto` |
| M-36 | X | ejecución | `feature_registry_version` desconocida | ejecución | no se puede resolver la referencia histórica | — | — | rechazo de ejecución |
| M-37 | F | `Cita o ubicación` | texto no literal | cualquiera | la cita no es subcadena exacta | — | — | cuarentena |
| M-38 | X | ejecución | origen no declarado o texto fuente ausente | ejecución | faltan precondiciones de §5.4 | — | — | rechazo de ejecución |
| M-39 | X | oportunidad | asimetría humano/IA | ejecución | misma oportunidad evaluada con estándares distintos | — | — | revisión manual |
| M-40 | X | corpus | frecuencia y variantes reales | inventario | no hay corpus histórico | — | — | sin datos |
| M-41 | F | fila §4 con múltiples observaciones | dos o más observaciones en una misma fila | característica | colisión de sublocalizador | — | — | preservar o revisar (`CE-037`) |
| M-42 | X | procedencia | origen no demostrable ni atestable | cualquiera | falta de `observation_origin` válido | — | — | bloqueo (`CE-036`) |
| M-43 | F | `Característica/valor observado` + `Cita o ubicación` | valor explícito + span literal | característica §4 | observación afirmativa derivada | `EvidenceRecord` | `observed`; `opportunity_status` según completitud; `assessment_confidence=not_rated` | `feature_id` resoluble; valor explícito; span literal |
| M-44 | F | valor observado | mapea a `historical_reference_pattern_id` | característica §4 | valor = patrón de referencia | `EvidenceRecord` | `aligned`; `research_alignment=dir(referencia)`; `reference_pattern_id`=referencia; `observed_option_id` si `response_option` | span; justificación |
| M-45 | F | valor observado | mapea a otro patrón registrado de la misma característica | bidireccional §4 | valor = polo opuesto registrado | `EvidenceRecord` | `opposed`; `research_alignment=dir(otro)`; `reference_pattern_id`=otro; `observed_option_id`=otro | span; justificación |
| M-46 | F | valor observado | no mapea a ningún patrón registrado | característica §4 | observación sin patrón aplicable | `EvidenceRecord` | `observed`; `not_assessed`; `reference_pattern_id=null`; `observed_option_id=null`; `observed_value_text` | span; valor literal |
| M-47 | F | valor observado | característica `overall_feature` (escala/ordinal) | característica §4 | el valor no basta para alinear | `EvidenceRecord` | `observed`; `not_assessed` por defecto; token direccional explícito opcional | `alignment_basis_detail` si hay token |
| M-48 | F | `Contraevidencia real` | sin span propio o sin justificación propia | característica §4 | contraevidencia no demostrada | — | — | cuarentena (`CE-009`/`CE-010`/`CE-039`) |
| M-49 | F | `Contraevidencia real` | con span y justificación propios | característica §4 | contraevidencia afirmativa | `EvidenceRecord` propio | `observed`; `opposed`; bidireccional con patrón opuesto; unidireccional `not_assessed` + `reference_pattern_id=null` | span y justificación propios |
| M-50 | F | `Característica/valor observado` | ausente o vacío | característica §4 | no hay observación | — | — | rechazo de fila |
| M-51 | F | dos filas distintas | contenido idéntico, localizaciones distintas | característica §4 | posibles duplicados independientes | dos `EvidenceRecord` | preservar ambos; `CE-038` | no deduplicar por contenido |
| M-52 | D | fila §3 | estado presente/opuesto/neutral | dimensión | observación de dimensión | `DimensionProfile` | `coverage_status=descriptive_assessed`; estado/dirección en informe | no se emite `EvidenceRecord` |
| M-53 | D | `Presente–opuesto` | sin observación o sin justificación | dimensión | contraevidencia de dimensión no demostrada | — | — | cuarentena (`CE-009`/`CE-010`) |
| M-54 | F | fila §4 | dos observaciones con spans separados | característica §4 | observaciones independientes | dos `EvidenceRecord` | `:obs:1`, `:obs:2` | sublocalizador determinista |
| M-55 | X | ejecución | origen atestable durante la migración | ejecución | procedencia demostrable por atestación válida del operador | `run_level` | habilita `EvidenceRecord.observation_origin` en las filas completas; no emite registros por sí misma | atestación válida (§11.6) |

### 2.3 Tabla B — requisitos, pérdida y decisión

| row_id | evidence_requirements | source_span | rationale | historical_reference | information_loss | reversibility | decision | source_reference |
|---|---|---|---|---|---|---|---|---|
| M-01 | valor observado + justificación | obligatorio, literal | `INV-A2-09`: alineación = referencia | = `historical_reference_pattern_id` (IA) | ninguna | A | conversión fiel | `evidence-status.md` fila 1; `report-template.md` §3; Spec §5.3 |
| M-02 | idem | obligatorio | idem con dirección humana | = referencia (humana) | ninguna | A | conversión fiel | idem |
| M-03 | idem | obligatorio | referencia histórica = patrón IA | = referencia | ninguna | A | conversión fiel | Spec §5.3.5 |
| M-04 | idem | obligatorio | A2 exigiría `opposed`, pero R-04 está bloqueada | = patrón IA | fila no convertida | — | conversión no segura | Spec §5.3.5; `INV-A2-10`; §16.2 |
| M-05 | — | — | no existe dirección elevada opuesta en unidireccional | — | fila no convertida | D | conversión no segura | Spec §6.4; CSV |
| M-06 | — | — | contradicción interna de la fuente | — | fila no convertida | D | conversión no segura | `evidence-status.md` paso 3 |
| M-07 | — | — | oposición contra la referencia no es oposición | — | fila no convertida | D | conversión no segura | `INV-A2-10` |
| M-08 | span + justificación (si existen) | recomendado | no resoluble sin asumir referencia AI-first | irresoluble | cuarentena | — | conversión no segura | `evidence-status.md` fila 2; Spec §5.3.5 |
| M-09 | valor alternativo + span + justificación | obligatorio | `INV-A2-11`: unidireccional `opposed` sin patrón | referencia de la característica | dirección histórica solo en procedencia | B | conversión condicionada | Spec §6.4; §6.5 |
| M-10 | ancla + span + justificación | obligatorio | §6.5: sin umbrales ni anclas inventadas | referencia de la característica | sin ancla, la oposición no es verificable | B | conversión condicionada | Spec §6.5; `INV-A2-15` |
| M-11 | span | obligatorio | regla 5: `observed` exige span verificable | — | fila no convertida | D | conversión no segura | Spec §5.3 regla 5; §5.4 |
| M-12 | justificación | obligatorio | contraevidencia exige interpretación alternativa | — | fila no convertida | D | conversión no segura | `evidence-status.md` «Contraevidencia» |
| M-13 | búsqueda + completitud | no exigido | ruta D: no hay `feature_id`; no se emite `not_observed` | no aplica | el token `Ausente` solo en informe | B | preservación sin conversión | Spec §5.5; contrato §8.3 |
| M-14 | motivo | no exigido | ruta D: ausencia no sostenible | no aplica | el token `Ausente` solo en informe | B | preservación sin conversión | Spec §5.5; contrato §8.3 |
| M-15 | motivo | no exigido | `coverage_status=not_applicable` | no aplica | ninguna si hay motivo | A | preservación sin conversión | Spec §5.5; `INV-A2-13` |
| M-16 | motivo | no exigido | `coverage_status=not_assessable` | no aplica | ninguna si hay motivo | A | preservación sin conversión | Spec §5.5; `INV-A2-13` |
| M-17 | detalle de neutralización | recomendado | `INV-A2-12`; dos lecturas | no aplica | token `neutral` solo en procedencia | B | conversión condicionada | Spec §5.3; contrato §15.1 |
| M-18 | detalle contextual | recomendado | neutralidad evaluada | no aplica | ninguna | B | conversión condicionada | Spec §5.3; `SKILL.md` línea 106 |
| M-19 | justificación | recomendado | no hay patrón aplicable | no aplica | asociación con `neutro` solo en procedencia | B | conversión condicionada | Spec §5.3; `SKILL.md` línea 106 |
| M-20 | — | — | dos lecturas incompatibles | — | fila no convertida | D | conversión no segura | `SKILL.md` línea 106 |
| M-21 | ≥2 observaciones | — | `mixed` es propiedad de conjuntos | — | fila no convertida | D | conversión no segura | Spec §5.3.3 |
| M-22 | `record_ids` | — | `mixed` agregado con trazabilidad | no aplica | sin campo de ejecución, solo clúster | B | preservación sin conversión | Spec §5.3.3; contrato §17-B1 |
| M-23 | gate + motivos | — | etiqueta global, no estado | no aplica | enum de destino indefinido | B | preservación sin conversión | `SKILL.md` §12; contrato §17-B2 |
| M-24 | — | — | puerta de adecuación | no aplica | preservar | B | preservación sin conversión | `SKILL.md` §12; contrato §17-B2 |
| M-25 | — | — | confianza global | no aplica | no copiar a `assessment_confidence` | B | preservación sin conversión | `report-template.md` §6; Spec §5.3 |
| M-26 | span + oportunidad | obligatorio | §5.3.4: opción explícita de ausencia es observación | = referencia (IA) | ninguna | A | conversión fiel | Spec §5.3.4 |
| M-27 | span + oportunidad | obligatorio | opción no registrada: no se inventa ID | = referencia de la característica | falta `observed_option_id` | B | conversión condicionada | Spec §5.3.4; `observed_option_id` nullable |
| M-28 | — | — | no hay `feature_id`; destino descriptivo | no aplica | no hay registro atómico | B | preservación sin conversión | Spec §5.5; `report-template.md` §3 |
| M-29 | — | — | registro atómico sin `feature_id` | — | fila no convertida | D | conversión no segura | Spec §5.3 |
| M-30 | — | — | vocabulario no documentado | — | fila no convertida | D | conversión no segura | contrato §7.4 |
| M-31 | — | — | combinación fuera de la taxonomía | — | fila no convertida | D | conversión no segura | `evidence-status.md` |
| M-32 | — | — | idempotencia por localización fuente | — | ninguna si idénticas | A/D | conversión condicionada | contrato §11.3, §12 |
| M-33 | — | — | campo de referencia, no de observación | se resuelve desde el registro | se evita una alineación fabricada | A | preservación sin conversión | `report-template.md` §4; Spec §5.3.5 |
| M-34 | — | — | `v0.2.3` no define vocabulario de fuerza | no aplica | intensidad original solo en procedencia | B | conversión condicionada | `report-template.md` §3–§4; Spec §5.3 |
| M-35 | span + justificación | obligatorio | opción humana elevada; `mixed` es parte del nombre | = referencia humana | ninguna | A | conversión fiel | CSV; `data-integrity-v0.2.2.md`; registry |
| M-36 | — | — | sin versión fijada no hay resolución A2 | irresoluble | ejecución no convertida | D | conversión no segura | Spec §5.7; `INV-A2-16` |
| M-37 | cita literal | obligatorio | §5.4: sin normalización | — | fila no convertida | D | conversión no segura | Spec §5.4 |
| M-38 | declaración de origen + texto | — | precondiciones de entrada | — | ejecución no convertida | D | conversión no segura | contrato §5.4 |
| M-39 | — | — | `evidence-status.md` «Regla de simetría» | — | revisión manual | D | no evaluable con la evidencia disponible | `evidence-status.md` |
| M-40 | — | — | no hay corpus en el repositorio | — | — | — | no evaluable con la evidencia disponible | inventario §1.1 |
| M-41 | — | — | dos observaciones en una fila | — | no se emite registro ambiguo | D | conversión no segura | contrato §11.2; `CE-037` |
| M-42 | — | — | procedencia no demostrable ni atestable | — | bloqueo | D | conversión no segura | contrato §11.6; `CE-036` |
| M-43 | valor explícito + span literal | obligatorio | ruta F: el valor y el span bastan para `observed` | se resuelve desde el registro | ninguna si el valor mapea | A | conversión condicionada | contrato §9.4; Spec §5.3 regla 5 |
| M-44 | valor + span + justificación | obligatorio | `INV-A2-09`: valor = referencia | = referencia | ninguna | A | conversión fiel | contrato §9.4; Spec §5.3.5 |
| M-45 | valor + span + justificación | obligatorio | `INV-A2-10`: valor = polo opuesto registrado | = patrón opuesto | ninguna | A | conversión fiel | contrato §9.4; Spec §5.3.5 |
| M-46 | valor + span | obligatorio | opción no registrada; no se inventa ID | = referencia de la característica | falta `observed_option_id` | A | conversión condicionada | contrato §9.4; Spec §5.3.4 |
| M-47 | valor + span | obligatorio | escala/ordinal sin umbral por historia | = `overall_feature` | alineación no afirmada | A | conversión condicionada | contrato §9.4; Spec §6.5 |
| M-48 | span propio + justificación propia | obligatorio | contraevidencia no demostrada | — | fila no convertida | D | conversión no segura | contrato §11.5; `CE-039` |
| M-49 | span propio + justificación propia | obligatorio | contraevidencia afirmativa | referencia de la característica | dirección histórica solo en procedencia | A | conversión condicionada | contrato §9.4; `INV-A2-11` |
| M-50 | — | — | no hay observación | — | fila no convertida | D | conversión no segura | contrato §9.4; `CE-025` |
| M-51 | — | — | dos filas distintas con texto idéntico | — | ninguna; se preservan ambas | A | conversión condicionada | contrato §11.3; `CE-038` |
| M-52 | — | — | ruta D: estado de dimensión | no aplica | estado/dirección solo en informe | B | preservación sin conversión | contrato §8.1, §9.2 |
| M-53 | — | — | `Presente–opuesto` de dimensión sin justificación | — | fila no convertida | D | conversión no segura | contrato §9.2; `CE-010` |
| M-54 | dos spans separados | obligatorio | sublocalizador determinista | — | ninguna | A | conversión condicionada | contrato §11.2 |
| M-55 | atestación válida (`migration_attestations`) | — | §11.6: atestación de migración permite la conversión | no aplica | ninguna | B | conversión condicionada | contrato §11.6 |

### 2.4 Recuento de decisiones

| Decisión | Filas | Total |
|---|---|---:|
| conversión fiel | M-01, M-02, M-03, M-26, M-35, M-44, M-45 | 7 |
| conversión condicionada | M-09, M-10, M-17, M-18, M-19, M-27, M-32, M-34, M-43, M-46, M-47, M-49, M-51, M-54, M-55 | 15 |
| preservación sin conversión | M-13, M-14, M-15, M-16, M-22, M-23, M-24, M-25, M-28, M-33, M-52 | 11 |
| conversión no segura | M-04, M-05, M-06, M-07, M-08, M-11, M-12, M-20, M-21, M-29, M-30, M-31, M-36, M-37, M-38, M-41, M-42, M-48, M-50, M-53 | 20 |
| no evaluable con la evidencia disponible | M-39, M-40 | 2 |
| **Total** | | **55** |

*Nota:* M-04 pasó de «conversión condicionada» (v0.1) a «conversión no segura» (v0.2) y se mantiene bloqueada en v0.3. M-08 se mantiene en cuarentena. M-13…M-16 se reclasificaron a preservación porque §3 no genera `EvidenceRecord`. M-43…M-55 son nuevas filas de la ruta F.

---

## 3. Casos ambiguos y no convertibles

### 3.1 Ambigüedades de la fuente

**A1. `neutral` como estado y `neutro` como dirección.**
`evidence-status.md` ofrece `neutral` en el paso 3 de la regla de decisión; la tabla normativa no lo incluye y `report-template.md` usa `neutro` como dirección. La taxonomía de 5 estados no tiene un estado «presente neutro», de modo que la plantilla solo puede codificarlo como `Presente–alineado` + `neutro` (o con la variante `neutral`). En ruta D se preserva como `coverage_status=descriptive_assessed`; en ruta F+ se normaliza a `observed` + dirección `neutro` y se mantienen las dos lecturas. `Presente–opuesto` + `neutro` sigue siendo una contradicción.

**A2. `Presente–opuesto` en bidireccional con polo humano (F+).**
Dictamen v0.3: **no convertible sin asumir referencia AI-first.** La fuente histórica no declara qué polo es la referencia para una característica bidireccional; ambos polos están elevados. Cuarentena (`CE-035`).

**A3. `Presente–opuesto` en §3 (ruta D).**
Es contraevidencia de dimensión. No se convierte en `opposed` de característica porque no hay `feature_id`. Se preserva en el informe y se exige observación/justificación no vacías. Si se desea contraevidencia de característica, debe constar en §4 `Contraevidencia real` con span propio.

**A4. `mixto` en dos niveles.**
Como dirección de característica (D3) y como etiqueta global (G3). El primero es un agregado dentro de un registro atómico y se rechaza; el segundo se preserva en el informe externo y solo se expresa en `ClusterSummary` con síntesis explícita. No son intercambiables.

**A5. `ambivalent/mixed` como valor.**
Es una opción de Moral Polarity Toward Protagonist, no una dirección. Se convierte como observación alineada al patrón humano.

**A6. `Dirección del estudio` (§4).**
Describe el paper, no el texto. Copiarla a `research_alignment` fabricaría alineación. Se prohíbe.

**A7. Proyección §3 vs §4.**
No existe join automático. Una fila de §3 no genera `EvidenceRecord`. Una fila de §4 no hereda estado ni dirección de §3.

**A8. Escalas sin umbral.**
El registro no contiene umbrales por historia. Un valor «alto» o «4/5» no basta para afirmar alineación. La ruta F usa `not_assessed` salvo token direccional explícito.

### 3.2 Casos no convertibles

| Caso | Motivo | Resultado |
|---|---|---|
| `Presente–alineado` contra la única dirección elevada (F+) | contradicción lógica | rechazo |
| `Presente–alineado` + polo humano en bidireccional (F+) | R-04 bloqueada | cuarentena (`CE-021`) |
| `Presente–opuesto` en escala sin ancla (F+) | §6.5 prohíbe umbrales inventados | cuarentena |
| `Presente–opuesto` sin span o sin justificación (F+) | contraevidencia no demostrada | cuarentena |
| `Presente–opuesto` en bidireccional (F+) | no resoluble sin asumir referencia AI-first | cuarentena (`CE-035`) |
| `mixto` a nivel de característica | agregado en registro atómico | cuarentena |
| fila de característica sin `feature_id` | no hay referencia canónica | rechazo |
| estado o dirección desconocidos | vocabulario no documentado | rechazo |
| estado y dirección incompatibles | fuera de la taxonomía | rechazo |
| versión de registro irresoluble | A2 no resoluble | rechazo de ejecución |
| origen no declarado ni atestable | campo obligatorio sin fuente | rechazo de ejecución |
| texto fuente ausente | spans no verificables | rechazo de ejecución |
| dos observaciones indistinguibles en una fila | sublocalizador ambiguo | preservar o revisar (`CE-037`) |
| contraevidencia sin span/justificación propios | no se puede emitir | cuarentena (`CE-009`/`CE-010`/`CE-039`) |

**Nota sobre la dirección en la ruta D.** En la ruta D, `legacy_direction` es opcional. Su ausencia o su no normalización **no** convierten la fila en no convertible ni activan rechazo (R-D07); el token se conserva literalmente y no se usa para producir `research_alignment`. La única exigencia de la ruta D es un `legacy_state` válido (R-01, R-D01). Por eso M-13…M-16 y M-28/M-52 preservan filas sin depender de una dirección. R-02 se aplica únicamente a entradas F+.

**Nota sobre M-55.** M-55 es una condición de procedencia **a nivel de ejecución**, no una fila de característica. No genera `EvidenceRecord` por sí misma: habilita el establecimiento de `EvidenceRecord.observation_origin` en las filas completas que ya cumplen los demás requisitos. La atestación externa se conserva en `migration_attestations`, que sigue siendo la fuente de verdad de la atestación; el dominio solo refleja el valor. Sin atestación válida, la conversión no se habilita (R-29/R-37, `CE-032`/`CE-036`).

### 3.3 Pérdidas potenciales

| Pérdida | Cuándo | Mitigación |
|---|---|---|
| Etiqueta histórica distinta de la relación A2 | M-04 (bloqueada) | `legacy_raw` + `CE-021` |
| Estado de dimensión no representado en el dominio | M-13…M-16, M-28, M-52 | `legacy_raw` + `loss_report` |
| Dirección histórica no afirmable | M-09, M-27 | `legacy_raw` + `CE-026`/`CE-022` |
| Intensidad original | M-34 | `legacy_raw` + `CE-023` |
| Asociación `neutro` ↔ registro | M-18, M-19 | `legacy_raw` + `loss_report` |
| Etiqueta global sin campo | M-22…M-25 | informe de exportación |
| Conversión de `Presente–opuesto` bidireccional (F+) | M-08 | cuarentena + `CE-035` |
| Contraevidencia sin span propio | M-48 | cuarentena + `CE-039` |
| Fila entera | cuarentena/rechazo | `preserved_payload` |

Ninguna pérdida es silenciosa: toda fila emitida, preservada, en cuarentena o rechazada tiene entrada en el informe (contrato §11.4, §13).

---

## 4. Verificación cruzada

| Control | Resultado |
|---|---|
| Todo estado de la matriz existe en `evidence-status.md` | sí (E1–E5); E6 marcado como variante |
| Toda dirección existe en `report-template.md` §3 o `SKILL.md` §5 | sí (D1–D5) |
| Toda etiqueta global existe en `SKILL.md` §12 | sí (G1–G5) |
| Toda opción citada existe en el CSV o en el registro | sí (§1.6); tres opciones de ausencia solo en `evidence-status.md`, marcadas |
| Todo campo de destino existe en la Spec | sí; `AnalysisRun` sin campo de alineación declarado como bloqueo |
| No se introduce ningún enum nuevo | sí; las etiquetas de decisión son clasificación documental |
| No se duplica la referencia histórica | sí; se resuelve desde el registro |
| No se altera `Presente–opuesto` | sí; M-07/M-09/M-10/M-49 exigen contraevidencia afirmativa |
| Ausencia ≠ oposición | sí; M-13/M-14 y M-48 |
| Atómico ≠ agregado | sí; M-21/M-22 |
| Etiqueta global ≠ `ClusterSummary.alignment` por defecto | sí (M-22) |
| §3 no genera `EvidenceRecord` | sí (M-13…M-16, M-28, M-52) |
| §4 no hereda estado/dirección de §3 | sí (M-43…M-47) |
| Contraevidencia con span propio | sí (M-48/M-49) |
| Idempotencia por localización, no por contenido | sí (M-32/M-51) |
| R-04 bloqueada | sí (M-04) |
| Reversibilidad declarada por fila | sí |
