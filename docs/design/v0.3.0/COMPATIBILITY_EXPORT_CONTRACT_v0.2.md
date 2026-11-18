# Contrato de exportación de compatibilidad — v0.2

**Proyecto:** StoryScope Human–AI Analysis
**Fase:** 1.21 — reconciliación de fuentes históricas y cierre de bloqueos contractuales
**Estado:** contrato documental, no implementado
**Fecha:** 2026-11-18
**Origen normativo:** `v0.2.3` (tag anotado `d7221dab…`, commit `a629af7d…`)
**Destino normativo:** rama `feature/storyscope-v0.3.0-design`, `TECHNICAL_SPEC_v0.1.md` y `FEATURE_REGISTRY_v0.1.2-draft.json`
**Predecesor:** `COMPATIBILITY_EXPORT_CONTRACT_v0.1.md` (preservado íntegramente; esta v0.2 es una revisión, no una sobrescritura)

Este documento define **cómo debe comportarse** un futuro exportador de compatibilidad. No contiene código, no crea módulos, clases, servicios, APIs ni CLI, y no modifica ningún contrato científico.

---

## 1. Propósito

Convertir anotaciones cualitativas producidas con StoryScope `v0.2.3` a la representación de evidencia prevista para `v0.3.0`, de modo que:

1. la semántica histórica se conserve o se rechace explícitamente;
2. cada valor de destino pueda rastrearse hasta una fuente, una fila y un fragmento;
3. ninguna conversión pierda información en silencio;
4. el resultado sea idempotente y auditable;
5. el modelo de dominio `v0.3.0` no se contamine con estados de error, cuarentena ni enums nuevos.

El contrato **no** promete que toda anotación histórica sea convertible. Promete que toda anotación histórica tenga un resultado explícito y justificado.

**Principio de esta versión:** es preferible conservar una observación histórica sin convertirla que producir un `EvidenceRecord` formalmente válido pero semánticamente falso.

---

## 2. Alcance y exclusiones

### 2.1 Incluido

- Inventario de los valores históricos realmente documentados en `v0.2.3`.
- Proyección explícita de las dos tablas de la plantilla (`§3` y `§4`) a niveles de ejecución, dimensión y característica.
- Contrato de entrada documental y de salida (`analysis.json` + informe de exportación).
- Reglas de conversión por estado, dirección y tipo de característica.
- Contrato A2 / F-02 ya consolidado.
- Trazabilidad, idempotencia con sublocalizador, reversibilidad y versionado del contrato.
- Diagnósticos y cuarentena externos al modelo de dominio.
- Procedencia histórica frente a atestación de migración.
- Vectores de prueba contractuales (documento aparte).

### 2.2 Excluido

- Implementación del exportador o de cualquier parte del Evidence Engine.
- Modificación de `SKILL.md`, `references/`, `validation/`, `main`, `v0.2.3` o del workflow CI.
- Creación de estados, enums, IDs, campos o esquemas nuevos en el dominio.
- Reinterpretación de datos científicos, conteos o valores de Table 16.
- Conversión de texto libre a etiquetas no documentadas.
- Traducción al español de la nomenclatura del motor.

---

## 3. Autoridad documental

Toda regla de este contrato cita una fuente comprobable. Las fuentes históricas se leen en el tag `v0.2.3`, no en `main`.

| Fuente | Versión | Secciones usadas | Qué establece |
|---|---|---|---|
| `references/evidence-status.md` | `v0.2.3` | tabla «Estados de evidencia»; «Regla de decisión»; «Diferencia entre ausencia y valor categórico “ninguno”»; «Contraevidencia»; «Regla de simetría» | Taxonomía normativa de 5 estados; regla de ausencia; definición de contraevidencia |
| `references/report-template.md` | `v0.2.3` | §1; §3 y su nota «Estados permitidos / Dirección»; §4; §6 | Vocabulario de dirección; estructura de filas; etiqueta global |
| `SKILL.md` | `v0.2.3` | §5 «Direction labels»; §6; §12 | Definición operativa de `mixto`, `neutro`, `no evaluable`; formato de salida |
| `references/feature-dimension-map.csv` | `v0.2.3` | 30 filas | Nombre de característica, tipo de medida, dirección elevada, opciones canónicas |
| `references/core-patterns.md` | `v0.2.3` | listas AI-elevated / human-elevated | Patrones elevados por grupo |
| `references/cluster-map.md` | `v0.2.3` | 8 clústeres operativos | Agrupación y reglas de doble conteo |
| `references/numeric-integrity-v0.2.3.md` | `v0.2.3` | «Excepciones de redondeo documentadas» | Valores publicados; prohibición de recalcular gaps |
| `references/data-integrity-v0.2.2.md` | `v0.2.3` | tabla corregida | Precedente de corrección de valores; `ambivalent/mixed` como opción |
| `references/worked-examples/01-microrelato-21-palabras.md` | `v0.2.3` | «Evaluación obligatoria»; «Observaciones que sí pueden hacerse» | Ejemplo real de `No evaluable` por longitud y de observación local |
| `docs/design/v0.3.0/TECHNICAL_SPEC_v0.1.md` | rama feature | §4.1; §5.1–§5.7; §6.4; §6.5; §10.3 | Contrato de destino, invariantes A2, reglas por tipo |
| `docs/design/v0.3.0/FEATURE_REGISTRY_v0.1.2-draft.json` | rama feature | `feature_records`; `cluster_catalog`; `dimensions`; `counts`; `id_policy` | Fuente única de `historical_reference_pattern_id` |
| `docs/design/v0.3.0/FEATURE_REGISTRY_v0.1.1_draft.json` | rama feature | — | Baseline científico protegido; no se modifica |
| `docs/design/v0.3.0/FEATURE_REGISTRY_REVIEW_NOTES_v0.1.1.md` | rama feature | «Decisiones de Fase 1.4»; «Fase 1.8»; «Consolidación A2 — Fase 1.11» | Historia de F-02 y de la consolidación A2 |
| `docs/design/v0.3.0/PROJECT_CHARTER_v0.1.md` | rama feature | §5 | Modelo de datos inicial |

### 3.1 Ausencias documentales registradas

Se buscaron y **no existen** en `v0.2.3`:

- esquema machine-readable de `EvidenceRecord`, `ClusterSummary` o `AnalysisRun`;
- un corpus de anotaciones reales (el repositorio solo contiene plantilla, guía y un ejemplo de calibración);
- catálogo completo de opciones del instrumento para las características unidireccionales;
- campo de procedencia de la anotación (`observation_origin` histórico);
- offsets de cita normalizados;
- identificador estable de registro.

Estas ausencias **no se suplen por invención**: se convierten en precondiciones del contrato (§5.4) o en bloqueos declarados (§15).

---

## 4. Versiones

Cuatro dimensiones independientes. Confundirlas es un error de contrato.

| Eje | Identificador en este contrato | Valor `v0.2` | Autoridad | Regla de cambio |
|---|---|---|---|---|
| Contrato de exportación | `export_contract_version` | `0.2.0` | este documento | SemVer: en la fase de diseño (0.x) una revisión sustantiva de reglas de conversión, diagnósticos y modelo de procedencia se expresa como incremento *minor* (0.1.0 → 0.2.0). El *major* se reserva para la congelación del contrato al iniciar la implementación. |
| Esquema de origen | `source_format_id` + `source_skill_version` | `storyscope-v0.2.3-qualitative-report` + `0.2.3` | `v0.2.3` | `source_format_id` lo asigna **este contrato**; no es un identificador hallado en `v0.2.3`. `v0.2.3` no tiene esquema machine-readable |
| Esquema de destino | `bundle_schema_version` | `1.0.0` | `TECHNICAL_SPEC` §5.1 | lo fija el proyecto, no el exportador |
| Registro de características | `feature_registry_version` + `feature_registry_schema_version` | `0.1.2-draft` + `1.1.0` | `FEATURE_REGISTRY_v0.1.2-draft.json` | fijado e inmutable por ejecución (`INV-A2-16`) |

Reglas:

- `export_contract_version` **nunca** se escribe dentro de `EvidenceRecord`, `ClusterSummary` ni `AnalysisRun`; vive en el sobre de exportación y en el informe de exportación.
- `feature_registry_version` se escribe en `AnalysisRun` porque el contrato de destino ya lo exige (§5.2) y porque sin él la referencia histórica no es resoluble.
- Cambiar de versión de registro **no** reescribe una exportación anterior: exige una nueva ejecución con revalidación explícita (§5.7, `INV-A2-16`).
- `schema_version` del Feature Registry (`1.1.0`) no se modifica en esta fase.

---

## 5. Contrato de entrada

### 5.1 Naturaleza de la entrada

La entrada es un **informe cualitativo `v0.2.3`**, no un JSON histórico. `v0.2.3` define una plantilla de informe obligatoria (`references/report-template.md` §3–§6) y un formato de salida de siete secciones (`SKILL.md` §12), pero no un esquema de datos.

Por tanto, el exportador consume una **proyección documental** de ese informe. La proyección no inventa campos: cada campo de entrada corresponde a una columna, frase o sección existente en la plantilla.

### 5.2 Campos de ejecución (run-level)

| Campo de entrada | Origen documental | Obligatorio | Destino |
|---|---|---|---|
| `report_language`, `report_variety` | `report-template.md` §1 | sí | `AnalysisRun.context` |
| `genre`, `text_type` | §1 | sí | `AnalysisRun.context` |
| `approx_length`, `counting_method` | §1 | sí | `AnalysisRun.source_metadata` |
| `completeness` (`completo` / `fragmento` / `desconocido`) | §1 | sí | `AnalysisRun.source_metadata` |
| `prompt_task_audience`, `comparison_sample`, `editing_translation_ai` | §1 | no | `AnalysisRun.context` |
| `adequacy_gate` (`no apto` / `exploratorio` / `perfil cualitativo posible`) | §1 | sí | `AnalysisRun.adequacy` (sujeto a §15-B2) |
| `global_label` (`patrón humano` / `patrón IA` / `mixto` / `neutro` / `evidencia insuficiente`) | §6 | sí | nivel de ejecución; ver R-17 y §15-B1 |
| `analysis_quality_confidence` (`baja` / `moderada` / `alta`) | §6 | no | **no** se propaga a registros; ver R-28 y §6.3 |
| `legacy_observation_origin` (`human_annotation` / `external_model` / `independent_tool` / `authorized_experiment`) | **no existe en `v0.2.3`** | sí, declarado por el operador | `EvidenceRecord.observation_origin` |
| `source_text` disponible para verificación de citas | implícito en el análisis | sí | cálculo de `source_spans` |
| `source_document_sha256`, `source_git_tag`, `source_git_commit` | cálculo del exportador | sí | sobre de exportación |
| `feature_registry_version` | `AnalysisRun` de destino | sí | resolución A2 |

### 5.3 Campos de fila (row-level)

`v0.2.3` tiene **dos tablas distintas** y no deben confundirse. La proyección completa está en `COMPATIBILITY_MAPPING_MATRIX_v0.2.md` §1.3.

**Tabla §3 — perfil por dimensiones** (10 filas, una por dimensión):

| Columna histórica | Campo de entrada | Observación |
|---|---|---|
| `Dimensión` | `dimension_name` | nombre bilingüe; resoluble a `dimension_id` |
| `Observación respaldada` | `observation_text` | prosa; no es una cita |
| `Estado de evidencia (5)` | `legacy_state` | taxonomía de 5 estados |
| `Clúster` | `cluster_name` | opcional; resoluble a `cluster_id` |
| `Dirección` | `legacy_direction` | **dirección de la observación** |
| `Fuerza` | `legacy_strength` | sin vocabulario controlado en `v0.2.3` |
| `Por qué / alternativa contextual` | `contextual_alternative` | justificación / explicación alternativa |

**Tabla §4 — indicadores centrales** (solo clústeres relevantes):

| Columna histórica | Campo de entrada | Observación |
|---|---|---|
| `Clúster` | `cluster_name` | resoluble a `cluster_id` |
| `Característica/valor observado` | `feature_name` + `observed_value_text` | resoluble a `feature_id` |
| `Cita o ubicación` | `quotation_or_location` | puede no ser literal ni tener offsets |
| `Dirección del estudio` | **no es un campo de observación** | es la dirección elevada del estudio; se resuelve desde el registro, nunca se copia a `research_alignment` |
| `Contraevidencia real` | `real_counterevidence` | contraevidencia afirmativa citada |
| `Explicación alternativa` | `contextual_alternative` | — |
| `Fuerza` | `legacy_strength` | — |

> **Trampa documentada.** La columna `Dirección del estudio` de §4 describe el hallazgo del paper, no la observación del texto. Un exportador que la copie a `research_alignment` fabricaría alineación. El contrato prohíbe esa copia (R-27).

### 5.4 Requisitos mínimos de la entrada

Una ejecución solo puede iniciarse si se cumplen **todos**:

1. `feature_registry_version` está fijada y la versión existe y es resoluble (§5.7, `INV-A2-16`).
2. `legacy_observation_origin` está declarado explícitamente. `v0.2.3` no lo registra; el exportador no puede inferirlo.
3. El texto analizado está disponible para verificar citas (§5.4). Sin texto no hay `source_spans` verificables y, por la regla 5 de §5.3, no hay `observed` válido.
4. El documento fuente tiene digest SHA-256 calculado.
5. Cada fila declara `legacy_state`; una fila sin estado no es una anotación (`evidence-status.md`: «No se puede asignar dirección a un rasgo hasta registrar su estado»).

Si falla 1, 2, 3 o 4, la ejecución se **rechaza completa**; no se emiten registros parciales. Si falla 5, se rechaza la fila.

### 5.5 Lo que la entrada no puede contener

- Texto completo almacenado en el bundle (§5.2: «No almacenar texto completo»).
- Probabilidades, porcentajes de autoría o scores globales (§5.3, regla 10).
- IDs inventados de característica, opción o patrón.
- Offsets calculados sobre texto normalizado (§5.4: sin normalización Unicode ni conversión de finales de línea).
- Valores numéricos derivados de medias grupales de Table 16 (§4.2).

---

## 6. Contrato de salida

### 6.1 Artefactos

| Artefacto | Contenido | ¿Modelo de dominio? |
|---|---|---|
| `analysis.json` | `schema_version`, `run`, `dimension_profiles`, `evidence_records`, `cluster_summaries`, `audit`, `report_summary` | **sí** |
| `compatibility_export_report.json` | versión del contrato, digests, resultados por fila, diagnósticos, cuarentena, informe de pérdidas, etiquetas run-level, atestaciones de migración | **no** |

El informe de exportación **nunca** se fusiona con `analysis.json`. El bundle puede referenciar su digest desde el sobre de exportación, pero no desde un campo del dominio.

### 6.2 Qué se escribe en el dominio

Solo valores que existen en `TECHNICAL_SPEC_v0.1.md` §5.

| Objeto | Campos que el exportador puede escribir |
|---|---|
| `AnalysisRun` | `analysis_id`, `schema_version`, `methodology_*`, `skill_version`, `feature_registry_version`, `cluster_map_version`, `prompt_pack_version`, `created_at_utc`, `source_metadata`, `context`, `adequacy`, `model_metadata`, `review_status` |
| `EvidenceRecord` | todos los de §5.3, incluidos `reference_pattern_id`, `reference_relation`, `observation_status`, `research_alignment`, `alignment_basis`, `alignment_basis_detail`, `status_reason`, `absence_justification`, `search_scope`, `observation_origin`, `origin_detail`, `observed_option_id`, `observed_value_text`, `source_spans`, `opportunity_status`, `interpretation`, `alternative_explanations`, `counterevidence_record_ids`, `cluster_id`, `shared_evidence_group_id`, `evidence_strength`, `assessment_confidence`, `review_status` |
| `ClusterSummary` | `cluster_id`, `record_ids`, `shared_evidence_group_ids`, `summary`, `alignment`, `double_count_flags` |
| `DimensionProfile` | `dimension_id`, `coverage_status`, `neutral_summary`, `evidence_record_ids`, `limitations` |
| `SourceSpan` | `quote`, `start_char`, `end_char`, `offset_unit` |

### 6.3 Prohibiciones de escritura

1. `mixed` en `EvidenceRecord.research_alignment` o en `alignment_basis` (§5.3, §5.3.3).
2. `historical_reference_pattern_id` dentro de `EvidenceRecord` (§5.3, `INV-A2-01`).
3. Cualquier enum nuevo: estados de exportación, códigos de diagnóstico, etiquetas de cuarentena o de pérdida.
4. Códigos de diagnóstico dentro de `EvidenceRecord`, `ClusterSummary` o `AnalysisRun`.
5. `reference_relation` con valores distintos de `aligned`, `opposed`, `not_assessed` (§5.3).
6. Conversión de ausencia en dirección, o de `not_assessed` en oposición «por conveniencia» (§5.3, regla 4).
7. Offsets aproximados, citas normalizadas o «citas» que no sean subcadena literal (§5.4).
8. **Escribir la etiqueta global `mixto` en `ClusterSummary.alignment` por la simple existencia de dos `record_ids` con alineaciones distintas** (R-17).
9. **Copiar `analysis_quality_confidence` a `EvidenceRecord.assessment_confidence`** (R-28).

### 6.4 Forma del informe de exportación (documental)

```json
{
  "export_contract_version": "0.2.0",
  "source": {
    "format_id": "storyscope-v0.2.3-qualitative-report",
    "skill_version": "0.2.3",
    "git_tag": "v0.2.3",
    "git_commit": "<commit del tag>",
    "document_path": "<ruta relativa>",
    "document_sha256": "<sha256>"
  },
  "target": {
    "bundle_schema_version": "1.0.0",
    "feature_registry_version": "0.1.2-draft",
    "feature_registry_schema_version": "1.1.0",
    "feature_registry_sha256": "<sha256>"
  },
  "counts": {
    "rows_read": 0,
    "records_emitted": 0,
    "records_preserved_without_conversion": 0,
    "rows_quarantined": 0,
    "rows_rejected": 0
  },
  "records": [
    {
      "record_id": "<uuid>",
      "legacy_locator": "<localizador compuesto>",
      "legacy_sublocator": "<localizador de observación>",
      "outcome": "converted | converted_with_flag | preserved | quarantined | rejected",
      "legacy_raw": {
        "state": "<token literal>",
        "direction": "<token literal>",
        "section": "§3 | §4",
        "feature_name": "<texto literal>",
        "cluster_name": "<texto literal>",
        "strength": "<texto literal>"
      },
      "diagnostics": ["CE-000"]
    }
  ],
  "quarantine": [
    {
      "legacy_locator": "<localizador compuesto>",
      "legacy_sublocator": "<localizador de observación>",
      "reason_codes": ["CE-000"],
      "preserved_payload": {}
    }
  ],
  "loss_report": [
    {
      "legacy_locator": "<localizador compuesto>",
      "legacy_sublocator": "<localizador de observación>",
      "field": "<campo histórico>",
      "reason": "<motivo>"
    }
  ],
  "run_level": {
    "legacy_global_label": "<token literal>",
    "legacy_global_label_written_to_domain": false,
    "adequacy_gate": "<token literal>",
    "analysis_quality_confidence": "<token literal>",
    "analysis_quality_confidence_written_to_domain": false,
    "diagnostics": []
  },
  "migration_attestations": [
    {
      "legacy_locator": "<localizador compuesto>",
      "legacy_sublocator": "<localizador de observación>",
      "attested_origin": "human_annotation | external_model | independent_tool | authorized_experiment",
      "attested_by": "<identificador seudonimizado>",
      "attested_at_utc": "<ISO 8601>",
      "basis": "<fundamento textual>",
      "protocol_version": "<versión>",
      "authorization_status": "authorized | not_authorized | not_applicable"
    }
  ]
}
```

`counts` es informativo y debe ser coherente con las listas; el contrato no exige un orden concreto de registros, pero sí que la exportación sea determinista (§11).

---

## 7. Ejes de la anotación histórica

`v0.2.3` usa **tres vocabularios distintos** que no deben colapsarse.

### 7.1 Eje de estado (5 valores)

Fuente: `references/evidence-status.md`, tabla «Estados de evidencia».

| Valor normativo | Significado operativo |
|---|---|
| `Presente–alineado` | valor observado que coincide con la opción/dirección elevada |
| `Presente–opuesto` | valor observado que es el polo alternativo; contraevidencia real |
| `Ausente` | se buscó y no se halló; sin dirección por defecto |
| `No aplicable` | el rasgo no corresponde al género/tarea |
| `No evaluable` | longitud, fragmentariedad, contexto u oportunidad impiden decidir |

**Variante documental:** `neutral` aparece en la «Regla de decisión», paso 3, como tercera opción de estado. No pertenece a la tabla normativa. Se registra como variante (`CE-020`) y se normaliza a observación presente (`observed`) + dirección `neutro`; **no se crea un sexto estado**.

La misma normalización se aplica a la codificación `Presente–alineado` + `neutro`, que es la única forma en que la plantilla histórica puede expresar «presente pero neutro».

### 7.2 Eje de dirección (5 valores)

Fuente: `report-template.md` §3, nota «Estados permitidos / Dirección»; `SKILL.md` §5 «Direction labels».

| Valor | Significado | Puede combinarse con |
|---|---|---|
| `patrón IA` | el valor observado se alinea con una opción/media elevada para IA | `Presente–alineado`, `Presente–opuesto` (solo si la dirección no es la elevada del feature unidireccional) |
| `patrón humano` | se alinea con una opción/media elevada para humanos | `Presente–alineado`, `Presente–opuesto` (solo si la dirección no es la elevada del feature unidireccional) |
| `mixto` | «one canonical feature has relevant observations pointing in both directions or is genuinely ambiguous» | solo agregados; ver R-16 |
| `neutro` | «observed but the study does not establish a meaningful directional pattern» | `Presente` (dos lecturas; ver R-14/R-15) |
| `no evaluable` | el estado no sostiene dirección | `Ausente`, `No aplicable`, `No evaluable` |

`mixto` y `neutro` son **direcciones**, no estados. `no evaluable` es una **dirección** distinta de `No evaluable`, que es un **estado**. La diferencia mayúscula/minúscula es semántica y se conserva.

### 7.3 Eje de etiqueta global (5 valores)

Fuente: `SKILL.md` §12, sección 6; `report-template.md` §6.

`patrón humano` / `patrón IA` / `mixto` / `neutro` / `evidencia insuficiente`.

`evidencia insuficiente` **no es un estado de evidencia**: es la etiqueta global obligatoria cuando falla la puerta de adecuación. No se convierte en `observation_status`.

### 7.4 Normalización de tokens (solo vocabulario)

Para comparar etiquetas se aplica: recorte de espacios, NFC, colapso de espacios internos y unificación de guiones (`-`, `–`, `—`) a `–`. La comparación es insensible a mayúsculas **solo** para el vocabulario.

Esta normalización **nunca** se aplica a `quote`, a `observed_value_text` ni al cálculo de offsets (§5.4). El token literal se conserva siempre en `legacy_raw`.

---

## 8. Proyección de las tablas históricas (Etapa A)

La plantilla `v0.2.3` tiene dos tablas con niveles distintos. **No se hace join automático entre ellas.**

| Campo histórico | Sección | Nivel | Disponibilidad | Destino posible | Condiciones | Pérdidas | Limitaciones |
|---|---|---|---|---|---|---|---|
| `Dimensión` | §3 | dimensión | siempre (10 filas) | `DimensionProfile.dimension_id` | resolución por nombre | ninguna | — |
| `Observación respaldada` | §3 | dimensión | siempre | `DimensionProfile.neutral_summary` / `limitations` | — | no es registro atómico | descriptiva |
| `Estado de evidencia (5)` | §3 | dimensión | siempre | **ninguno** (sin `feature_id`) | — | no convertible a `EvidenceRecord` | dimensión ≠ característica |
| `Clúster` | §3 | dimensión | opcional | agrupación de perfiles | `cluster_id` resoluble | — | — |
| `Dirección` | §3 | dimensión | opcional | **ninguno** | — | no convertible | dimensión ≠ característica |
| `Fuerza` | §3 | dimensión | opcional (texto libre) | **ninguno** | — | preservar en informe | texto libre |
| `Por qué / alternativa contextual` | §3 | dimensión | opcional | `DimensionProfile.limitations` | — | — | — |
| `Clúster` | §4 | característica (clúster) | siempre | `ClusterSummary.cluster_id` / `record.cluster_id` | `cluster_id` resoluble | — | — |
| `Característica/valor observado` | §4 | característica | siempre | `EvidenceRecord.feature_id` + `observed_value_text` | `feature_id` resoluble | — | si no resoluble → rechazo |
| `Cita o ubicación` | §4 | característica | opcional | `SourceSpan` | subcadena literal + offsets | si no literal → cuarentena | sin offsets históricos |
| `Dirección del estudio` | §4 | característica | siempre | **ninguno** (dirección del paper) | resolver desde el registro | nunca copiar a `research_alignment` | — |
| `Contraevidencia real` | §4 | característica | opcional | `counterevidence_record_ids` / `interpretation` | span + justificación | si falta en `Presente–opuesto` → cuarentena | — |
| `Explicación alternativa` | §4 | característica | opcional | `interpretation` / `alternative_explanations` | — | — | — |
| `Fuerza` | §4 | característica | opcional (texto libre) | `evidence_strength` (solo si mapea) | regla documentada | `CE-023` si no mapea | texto libre |
| Campos run-level (§1) | §1 | ejecución | varios | `AnalysisRun` / informe | — | — | — |
| Etiqueta global, `adequacy_gate`, `analysis_quality_confidence` | §6 | ejecución | varios | informe externo (run-level) | — | no escribir en dominio | §15-B1/B2 |

Regla: una fila de §3 no genera `EvidenceRecord`. Una fila de §4 genera como máximo uno o más `EvidenceRecord` según las observaciones que contenga, nunca un registro por dimensión.

---

## 9. Reglas de conversión

Cada fila produce **exactamente un** resultado: `converted`, `converted_with_flag`, `preserved`, `quarantined` o `rejected`. La matriz completa con las 15 columnas exigidas está en `COMPATIBILITY_MAPPING_MATRIX_v0.2.md`.

| ID | Condición | Acción | Destino | Requisitos adicionales | Diagnóstico |
|---|---|---|---|---|---|
| R-01 | `legacy_state` ausente o no reconocido | rechazar fila | — | — | `CE-025`/`CE-001` |
| R-02 | `legacy_direction` ausente o no reconocido | rechazar fila | — | — | `CE-002` |
| R-03 | `Presente–alineado` + dirección = dirección de la referencia histórica | convertir | `observed` + `pattern_ai`/`pattern_human` + `reference_pattern_id` = referencia + `aligned` + `reference_pattern` | span literal; justificación | — |
| R-04 | `Presente–alineado` + dirección opuesta, característica bidireccional | convertir con bandera | `observed` + `pattern_human` + `reference_pattern_id` = patrón humano + `opposed` | span literal; justificación; patrón opuesto registrado | `CE-021` |
| R-05 | `Presente–alineado` + dirección opuesta, característica unidireccional | rechazar fila | — | — | `CE-008` |
| R-06 | `Presente–alineado` + dirección opuesta a la referencia, cualquier tipo | rechazar fila (contradicción interna) | — | — | `CE-007` |
| R-07 | `Presente–opuesto` + bidireccional + `patrón IA` | rechazar fila (contradicción directa) | — | — | `CE-007` |
| R-08 | `Presente–opuesto` + bidireccional + `patrón humano` | **cuarentena** (no resoluble sin asumir referencia AI-first) | — | revisión humana; span y justificación si existen | `CE-035` |
| R-09 | `Presente–opuesto` + unidireccional categórica/binaria/multiselección, valor ≠ patrón de referencia | convertir | `observed` + `not_assessed` + `reference_pattern_id=null` + `opposed` | valor alternativo identificable; span; justificación | `CE-026` si la dirección no está registrada; `CE-022` si la opción no está registrada |
| R-09a | multiselección: `Presente–opuesto` sustentado solo en la ausencia de la opción de referencia | rechazar fila | — | se corrige a `not_observed`/`not_evaluable` según oportunidad | `CE-012` |
| R-09b | unidireccional: `Presente–opuesto` cuyo valor observado es el propio patrón de referencia | rechazar fila | — | — | `CE-007` |
| R-10 | `Presente–opuesto` + escala/ordinal, valor ≠ patrón de referencia | convertir solo con ancla documentada | `observed` + `not_assessed` + `opposed` | ancla o constructo opuesto explícito; span; justificación | `CE-011` si falta el ancla |
| R-11 | `Presente–opuesto` sin span | cuarentena | — | — | `CE-009` |
| R-12 | `Presente–opuesto` sin justificación | cuarentena | — | — | `CE-010` |
| R-13 | `Ausente` + oportunidad suficiente | convertir | `not_observed` + `sufficient` + `not_assessed` + `none` + `status_reason` + `absence_justification` + `search_scope` | `completeness=completo`; búsqueda declarada | — |
| R-14 | `Ausente` + oportunidad limitada/desconocida | convertir con bandera | `not_evaluable` + `limited`/`unknown` + `not_assessed` + `none` + `status_reason` | motivo textual | `CE-013` |
| R-15 | `No aplicable` | convertir | `not_applicable` + `none`/`unknown` + `not_assessed` + `status_reason` | motivo textual | `CE-019` si falta |
| R-16 | `No evaluable` | convertir | `not_evaluable` + `limited`/`none`/`unknown` + `not_assessed` + `status_reason` | motivo textual | `CE-019` si falta |
| R-17 | variante `neutral` (estado) o `Presente–alineado` + `neutro` | convertir con bandera | `observed` + `neutral` (si lectura a) o `not_assessed` (si lectura b) + `reference_pattern_id=null` | `alignment_basis_detail` no nulo para lectura a | `CE-020`; no seleccionar automáticamente entre lecturas |
| R-18 | `neutro` sin lectura seleccionable | rechazar fila | — | — | `CE-027` |
| R-19 | dirección `mixto` a nivel de característica | cuarentena | — | requiere división en ≥2 registros + resumen de clúster | `CE-014` |
| R-20 | etiqueta global `mixto` | **preservar** en informe externo; **no** escribir en `ClusterSummary.alignment` por defecto | `run_level.legacy_global_label` | — | `CE-015`; solo si existe síntesis de clúster explícita con ≥2 `record_ids` con alineaciones distintas se escribe `ClusterSummary.alignment=mixed` |
| R-21 | etiqueta global `evidencia insuficiente` | preservar | `run_level` (informe externo) | — | `CE-028` |
| R-22 | etiqueta global `adequacy_gate` | preservar | `run_level` (informe externo) | — | — |
| R-23 | `analysis_quality_confidence` | preservar | `run_level` (informe externo) | **no** copiar a `EvidenceRecord.assessment_confidence` | — |
| R-24 | opción categórica explícita de ausencia (`no_subplots`, `no_major_withholding`, `no_direct_address`, `no_anachrony`) | convertir | `observed` + `observed_option_id` (si está registrada) + alineación según patrón | span; oportunidad suficiente | `CE-022` si la opción no está en el registro |
| R-25 | fila de dimensión sin `feature_id` (tabla §3) | preservar sin conversión | `DimensionProfile.neutral_summary` / `limitations` | — | `CE-029` informativo |
| R-26 | fila de característica sin `feature_id` resoluble (tabla §4) | rechazar fila | — | — | `CE-003`/`CE-004` |
| R-27 | `feature_id`, `cluster_id` o `dimension_id` inexistente en la versión fijada | rechazar fila | — | — | `CE-006`/`CE-017`/`CE-018` |
| R-28 | falta `status_reason` en estado que lo exige | cuarentena | — | no se sintetiza texto | `CE-019` |
| R-29 | falta `legacy_observation_origin` | rechazar ejecución | — | declaración explícita o atestación de migración | `CE-032` / `CE-036` |
| R-30 | falta texto fuente, o cita no literal | cuarentena | — | `quote == source_text[start:end]` | `CE-033`/`CE-031` |
| R-31 | filas duplicadas idénticas | deduplicar | un registro | misma clave `(digest, sublocator)` | `CE-016` informativo |
| R-32 | `legacy_strength` fuera de `weak`/`moderate`/`strong` | convertir con bandera | `evidence_strength=not_rated` | texto original preservado | `CE-023` |
| R-33 | opción observada no registrada en el Feature Registry | convertir | `observed_option_id=null` + `observed_value_text` | texto literal | `CE-022` |
| R-34 | `feature_registry_version` inexistente o no resoluble | rechazar ejecución | — | — | `CE-005` |
| R-35 | columna `Dirección del estudio` de §4 | no convertir | se resuelve desde el registro | — | — |
| R-36 | sublocalizador no puede distinguir dos observaciones de una misma fila | preservar o revisar; no emitir registro ambiguo | — | — | `CE-037` |
| R-37 | procedencia histórica no demostrable ni atestable | rechazar fila/ejecución según alcance | — | — | `CE-036` |

### 9.1 Precedencia

1. Rechazo de ejecución (R-29, R-34) antes que cualquier fila.
2. Rechazo de fila (R-01, R-02, R-05, R-06, R-07, R-09a, R-09b, R-18, R-26, R-27) antes que cualquier conversión.
3. Cuarentena (R-08, R-11, R-12, R-19, R-28, R-30) antes que emisión.
4. Conversión.
5. Deduplicación (R-31) sobre el conjunto ya convertido.

### 9.2 Regla de simetría

`evidence-status.md`, «Regla de simetría»: la oportunidad se evalúa con el mismo estándar para valores humanos y de IA. El exportador **no** puede aceptar `Ausente` para una característica humana y `No evaluable` para la misma oportunidad en una característica de IA (ni lo contrario). Una ejecución que produzca esa asimetría sin justificación documental emite `CE-034 ASYMMETRIC_OPPORTUNITY` y se revisa manualmente.

### 9.3 Combinaciones estado × dirección (reconciliación)

| Estado | Dirección | Tipo de feature | Lectura | Resultado |
|---|---|---|---|---|
| `Presente–alineado` | `patrón IA` | unidireccional IA | valor = opción elevada | convertir → `aligned` |
| `Presente–alineado` | `patrón humano` | unidireccional humana | valor = opción elevada | convertir → `aligned` |
| `Presente–alineado` | `patrón IA` | bidireccional | valor = polo IA | convertir → `aligned` |
| `Presente–alineado` | `patrón humano` | bidireccional | valor = polo humano | convertir → `opposed` (`CE-021`) |
| `Presente–alineado` | dirección opuesta a la elevada | unidireccional | contradicción | rechazar (`CE-008`/`CE-007`) |
| `Presente–opuesto` | `patrón IA` | unidireccional IA | valor = alternativo, dirección dice IA | rechazar (`CE-007`) |
| `Presente–opuesto` | `patrón humano` | unidireccional IA | valor = alternativo; dirección no registrada | convertir → `not_assessed` + `opposed` (`CE-026`) |
| `Presente–opuesto` | `patrón IA` | bidireccional | contradicción directa | rechazar (`CE-007`) |
| `Presente–opuesto` | `patrón humano` | bidireccional | **no resoluble sin asumir referencia AI-first** | **cuarentena** (`CE-035`) |
| `Presente–opuesto` | `no evaluable` / `neutro` | unidireccional | dirección no registrada | convertir → `not_assessed` + `opposed` (`CE-026`) |
| `Ausente` | `no evaluable` | cualquiera | ausencia sin dirección | convertir según oportunidad |
| `No aplicable` | `no evaluable` | cualquiera | exclusión | convertir |
| `No evaluable` | `no evaluable` | cualquiera | no decidible | convertir |

**Dictamen de TV-03 / R-07 (v0.1):** la conversión `Presente–opuesto` + `patrón humano` + `explicit labels` → `pattern_human` + `opposed` **no es segura**. Requiere asumir que el autor histórico usó el polo IA como referencia, lo que retroactivamente impone la convención AI-first de `v0.3.0` sobre una fuente que no la declara. Por tanto R-07 se reclasifica de «convertir» a «cuarentena» (`CE-035`). El número de casos convertibles se reduce; esto es intencional y se documenta como pérdida de conversión, no como error.

---

## 10. Contrato A2 / F-02

### 10.1 `reference_pattern_id`

- Identifica **exclusivamente** el patrón con el que se alinea el `EvidenceRecord` (§5.3).
- Es `null` cuando `research_alignment` es `neutral` o `not_assessed` (`INV-A2-08`).
- No es la referencia histórica de la característica.
- Si no es nulo, debe pertenecer a la misma característica (`INV-A2-06`) y su dirección debe coincidir con `research_alignment` (`INV-A2-07`).
- Solo se asigna a `observed_option_id` cuando el patrón tiene `pattern_level = response_option`. Los patrones `overall_feature` no son opciones.

### 10.2 `historical_reference_pattern_id`

- Fuente única: `FEATURE_REGISTRY` (`INV-A2-01`).
- Se resuelve con `feature_id` + `AnalysisRun.feature_registry_version`.
- **Nunca** se escribe en `EvidenceRecord` ni se copia al informe como si fuera un campo del registro.
- **Nunca** se infiere del contenido narrativo ni del nombre de la característica.
- Estado del baseline: 30 características con referencia obligatoria, escalar y no nula (`INV-A2-02`); 17 unidireccionales con referencia `pattern_ai`, 10 unidireccionales con referencia `pattern_human` y 3 bidireccionales cuya referencia es el patrón IA (20 con referencia `pattern_ai` en total).

### 10.3 `reference_relation`

Enum cerrado: `aligned`, `opposed`, `not_assessed`. No se añaden valores.

| Relación | Condición estructural | Condición semántica |
|---|---|---|
| `aligned` | `reference_pattern_id = historical_reference_pattern_id` y `research_alignment = dir(referencia)` (`INV-A2-09`) | el span sostiene la alineación |
| `opposed` | bidireccional: patrón opuesto registrado, `research_alignment = dir(patrón opuesto)`, distinto de la referencia (`INV-A2-10`); unidireccional: `reference_pattern_id=null`, `research_alignment=not_assessed`, `observation_status=observed` (`INV-A2-11`) | contraevidencia afirmativa con span y justificación (`INV-A2-15`) |
| `not_assessed` | compatible con `neutral`, ausencia, no aplicabilidad, no evaluabilidad y observación sin patrón | no se asigna relación direccional |

### 10.4 `Presente–opuesto`

`Presente–opuesto` es **contraevidencia afirmativa**: el polo alternativo fue observado realmente (`evidence-status.md`, fila `Presente–opuesto`; «Contraevidencia»).

Prohibido convertirlo en:

- `not_observed` o `Ausente`;
- `neutral`;
- `not_assessed` por conveniencia;
- `opposed` sin span o sin justificación;
- «un patrón distinto» sin declarar cuál.

**Precisión terminológica.** La prohibición afecta a `reference_relation` y a `observation_status`: una contraevidencia nunca se convierte en `reference_relation=not_assessed` ni en `observation_status=not_observed`. En características unidireccionales, `INV-A2-11` exige `research_alignment=not_assessed`; eso **no** significa que la observación no se haya evaluado, porque `observation_status=observed` y `reference_relation=opposed` conservan la contraevidencia. Son campos distintos y no deben confundirse.

Obligatorio:

- `observation_status=observed`;
- `reference_relation=opposed`;
- `source_spans` no vacío y literal;
- justificación tipo-específica (`alignment_basis_detail` o `interpretation` según el caso);
- en bidireccionales, `reference_pattern_id` = patrón opuesto registrado;
- en unidireccionales, `reference_pattern_id=null` y `research_alignment=not_assessed`.

**Ambigüedad del token de dirección en unidireccionales.** Las fuentes no definen si, en `Presente–opuesto`, la columna `Dirección` nombra el polo observado o el polo contra el que se opone. En unidireccionales esa ambigüedad es irreducible: el polo alternativo no tiene patrón registrado. Por eso el contrato **preserva** el token y **no** lo promueve a `research_alignment` (`INV-A2-11`). La única comprobación fiable es que el valor observado no sea el propio patrón de referencia (R-09b); si lo es, la fila se rechaza.

### 10.5 Diferencias según el tipo de característica

Derivadas de §6.5 y del CSV, no de una regla genérica.

| Tipo (`measurement_type_source`) | Nº | Regla de oposición |
|---|---:|---|
| `scale 1–5` | 14 | No se inventan puntos de corte. `opposed` exige ancla o constructo opuesto identificable y justificación cualitativa. Un valor intermedio no es opuesto. |
| `ordinal mean` | 5 | Igual que escala. La distancia a la media grupal no demuestra oposición. |
| `categorical` | 3 | Las tres son bidireccionales con dos opciones elevadas; `opposed` solo cuando el valor observado es el polo opuesto real y verificable. En bidireccionales, `Presente–opuesto` + `patrón humano` no es convertible sin asumir referencia AI-first (R-08). |
| `categorical option` | 4 | Una opción distinta **no** basta salvo complemento documentado. Si no hay complemento, `opposed` es no seguro. |
| `multi-select option` | 3 | La presencia de la opción de referencia implica alineación. La coexistencia con otras opciones **no** produce `opposed`. La ausencia de la referencia **no** demuestra contraevidencia. |
| `binary option` | 1 | Un `no` explícito puede ser `opposed` si es opción canónica observada. La mera ausencia no basta. |

---

## 11. Trazabilidad y procedencia

### 11.1 Identificadores históricos disponibles

`v0.2.3` **no** define `record_id`, ni IDs de fila, ni IDs de anotación. No se inventan.

### 11.2 Localizador compuesto y sublocalizador

Cuando no existe identificador estable se usa:

```text
<source_document_sha256>:<section>:<row_index>:<feature_name_slug>
```

Limitaciones declaradas: si el documento se reordena, `row_index` cambia; el slug mitiga pero no elimina el riesgo; si el nombre de la característica se escribe con variantes, el slug puede divergir; el localizador no identifica una anotación dentro de una misma fila con varias observaciones.

**Sublocalizador (novedad v0.2).** Una fila puede generar más de un `EvidenceRecord` (p. ej., una observación principal y una contraevidencia, o varias opciones observadas). Para distinguirlas se añade:

```text
<legacy_locator>:obs:<n>
```

donde `n` es el índice 1-based de la observación dentro de la fila, ordenado por una regla determinista:

1. observación principal (valor observado) primero;
2. contraevidencia afirmativa a continuación;
3. explicación alternativa / neutralización contextual después;
4. en caso de empate, orden de aparición en el texto fuente.

La clave de unicidad pasa a ser `(source_document_sha256, legacy_sublocator)`. Si dos observaciones de una misma fila no pueden distinguirse de forma determinista, el caso se preserva o se envía a revisión (`CE-037`); no se emite un registro ambiguo.

### 11.3 Registro de procedencia (en el informe de exportación)

Por cada registro emitido se conserva:

| Campo | Fuente |
|---|---|
| `source_document_path`, `source_document_sha256`, `source_git_tag`, `source_git_commit` | cálculo del exportador |
| `legacy_locator`, `legacy_sublocator` | §11.2 |
| `legacy_state_raw`, `legacy_direction_raw`, `legacy_strength_raw` | tokens literales |
| `legacy_feature_name`, `legacy_cluster_name`, `legacy_dimension_name` | texto literal |
| `legacy_observation_text`, `legacy_justification`, `legacy_alternative`, `legacy_counterevidence` | texto literal |
| `legacy_quotation_or_location` | texto literal |
| `source_format_id`, `source_skill_version` | §4 |
| `feature_registry_version`, `feature_registry_sha256` | §4 |
| `export_contract_version` | §4 |
| `record_id` | salida |

El `origin_detail` de cada `EvidenceRecord` **puede** incluir la clave `legacy_locator` como metadato de procedencia, pero la fuente de verdad es el informe. No se añaden campos nuevos a `EvidenceRecord`.

### 11.4 Citas

- `quote` debe ser subcadena literal del texto fuente (§5.4).
- `start_char` / `end_char` se calculan sobre el texto UTF-8 decodificado sin normalización.
- Si la cita aparece una sola vez, el exportador puede resolver offsets; si aparece varias veces, exige desambiguación; si no aparece, la fila va a cuarentena (`CE-031`).
- Una «ubicación» sin cita literal (p. ej. «párrafo 3») no satisface la regla 5 de §5.3 y no permite `observed`.

### 11.5 Procedencia histórica frente a atestación de migración

`v0.2.3` no registra `observation_origin`. El destino lo exige. Se distinguen cuatro situaciones:

1. **Procedencia histórica demostrada** (p. ej., la Skill declara análisis humano cualitativo con protocolo versionado): se establece `observation_origin=human_annotation` y se documenta la base.
2. **Información proporcionada por un tercero** (herramienta independiente, modelo externo autorizado): se establece el valor correspondiente y se registra el método.
3. **Atestación declarada por el operador durante la migración**: se registra en `migration_attestations` del informe externo (responsable seudonimizado, fecha UTC, fundamento textual, versión de protocolo, estado de autorización). El valor de `observation_origin` refleja la atestación, pero la fuente de verdad de la atestación es el informe externo, no el dominio.
4. **Procedencia desconocida**: no se puede demostrar ni atestar válidamente → bloqueo de conversión (R-29/R-37, `CE-032`/`CE-036`).

No se crean nuevos enums en el dominio. La atestación es un mecanismo de procesamiento externo con su propia procedencia, coherente con la cuarentena (§13).

---

## 12. Idempotencia

Condiciones para que dos exportaciones de la misma fuente produzcan el mismo resultado lógico:

1. Mismo `source_document_sha256`.
2. Mismo `export_contract_version`.
3. Mismo `feature_registry_version` (y mismo digest de registro).
4. Mismas opciones de exportación declaradas.
5. Mismo texto fuente disponible para verificación.

Garantías exigidas:

- **Clave de unicidad:** `(source_document_sha256, legacy_sublocator)`. Dos filas con la misma clave no producen dos registros (R-31).
- **`record_id` estable:** el exportador debe producir el mismo `record_id` para la misma clave y versiones, sea por derivación determinista o por mapeo persistido. La elección se documenta en la implementación; el contrato solo exige estabilidad.
- **`analysis_id` estable:** reexportar la misma fuente con los mismos parámetros es la misma ejecución lógica; no se crea una ejecución nueva.
- **Sin acumulación:** la salida es función de la entrada, no del estado previo. Reexportar no añade registros a los anteriores.
- **Orden determinista:** si el formato de salida serializa listas, el orden debe ser estable (p. ej. por `legacy_sublocator`). El contrato no impone un orden concreto, solo su estabilidad.

Una exportación que dependa de la fecha de ejecución, del orden de iteración del sistema de archivos o de un contador global **no cumple** este contrato.

---

## 13. Reversibilidad

Se distinguen cuatro clases. La clasificación se declara por fila en la matriz.

| Clase | Definición | Ejemplo |
|---|---|---|
| **A. Completamente reversible** | el estado histórico se deriva del registro `v0.3.0` + registro de características, sin el informe | `No aplicable`; `No evaluable`; `Ausente` con oportunidad suficiente; `Presente–alineado` unidireccional; `Presente–opuesto` unidireccional |
| **B. Reversible solo con el original preservado** | el registro no basta; hace falta el token literal del informe | `Presente–alineado` + polo humano en bidireccional; variante `neutral`; `Ausente` degradado a `not_evaluable`; dirección no registrada; `Presente–opuesto` bidireccional (cuarentena) |
| **C. Irreversible** | no existe reconstrucción fiel ni con el original | ninguno dentro de este contrato |
| **D. Debe rechazarse** | no se emite registro | contradicciones; agregado en registro atómico; `feature_id` ausente; estado o dirección desconocidos; versión de registro irresoluble |

**Por qué no hay clase C.** Toda fila convertida conserva en el informe sus tokens literales y su texto. Ninguna conversión descarta un valor sin dejarlo registrado. Si una conversión exigiera descartar información y no pudiera preservarla, el contrato la clasifica como D, no como C.

**Demostración de la clase A.** La reconstrucción sin el informe se define por esta tabla:

| Registro `v0.3.0` | `legacy_state` | `legacy_direction` |
|---|---|---|
| `not_applicable` | `No aplicable` | `no evaluable` |
| `not_evaluable` | `No evaluable` | `no evaluable` |
| `not_observed` + `sufficient` | `Ausente` | `no evaluable` |
| `observed` + `pattern_ai` + `aligned` | `Presente–alineado` | `patrón IA` |
| `observed` + `pattern_human` + `aligned` | `Presente–alineado` | `patrón humano` |
| `observed` + `neutral` + `contextual_neutralization` | `neutral` (variante) | `neutro` |

Cualquier otra combinación exige el informe (clase B) o no se emitió (clase D).

**Informe de pérdidas.** Se emite `loss_report` cuando:

- una fila se convierte a un estado distinto del histórico (p. ej. `Ausente` → `not_evaluable`);
- un campo histórico no tiene destino (`Fuerza` libre, `Dirección del estudio` duplicada);
- una etiqueta histórica no se puede afirmar en el dominio (dirección no registrada);
- una fila se preserva sin conversión (dimensión sin `feature_id`);
- una fila se rechaza o se pone en cuarentena.

El informe de pérdidas **no** es un enum del dominio: es una lista de texto y referencias.

---

## 14. Diagnósticos y cuarentena

### 14.1 Espacio separado

Los diagnósticos viven **solo** en `compatibility_export_report.json`. No se escriben en `EvidenceRecord`, `ClusterSummary` ni `AnalysisRun`. No se crea un enum de estados de error en el dominio.

### 14.2 Códigos

| Código | Significado | Acción |
|---|---|---|
| `CE-001` | estado histórico desconocido | rechazar fila |
| `CE-002` | dirección histórica desconocida | rechazar fila |
| `CE-003` | fila de característica sin `feature_id` | rechazar fila |
| `CE-004` | nombre de característica no resoluble | rechazar fila |
| `CE-005` | versión de Feature Registry inexistente | rechazar ejecución |
| `CE-006` | referencia histórica no resoluble | rechazar fila |
| `CE-007` | estado y dirección incompatibles | rechazar fila |
| `CE-008` | `Presente–alineado` contra la referencia en unidireccional | rechazar fila |
| `CE-009` | `Presente–opuesto` sin span | cuarentena |
| `CE-010` | `Presente–opuesto` sin justificación | cuarentena |
| `CE-011` | `Presente–opuesto` en escala sin ancla | cuarentena |
| `CE-012` | ausencia de opción de referencia tratada como oposición en multiselección | rechazar conversión; corregir a `not_observed`/`not_evaluable` |
| `CE-013` | `Ausente` sin oportunidad suficiente | convertir a `not_evaluable` |
| `CE-014` | valor agregado en registro atómico | cuarentena |
| `CE-015` | etiqueta global sin campo de dominio | preservar |
| `CE-016` | duplicado en la fuente | deduplicar o cuarentena |
| `CE-017` | clúster no resoluble | rechazar fila |
| `CE-018` | dimensión no resoluble | rechazar fila |
| `CE-019` | falta `status_reason` | cuarentena |
| `CE-020` | variante `neutral` de estado | convertir con bandera |
| `CE-021` | bidireccional alineada al polo humano | convertir con bandera |
| `CE-022` | opción observada no registrada | `observed_option_id=null` |
| `CE-023` | fuerza no mapeable | `not_rated` |
| `CE-024` | falta digest de la fuente | rechazar ejecución |
| `CE-025` | fila parcial o estado ausente | cuarentena/rechazo |
| `CE-026` | dirección histórica no registrada | convertir con bandera |
| `CE-027` | `neutro` con lectura ambigua | rechazar fila |
| `CE-028` | etiqueta de adecuación sin enum de destino | preservar |
| `CE-029` | fila de dimensión sin característica | preservar |
| `CE-030` | `ambivalent/mixed` leído como dirección `mixto` | corregir; informativo |
| `CE-031` | cita no literal | cuarentena |
| `CE-032` | `legacy_observation_origin` no declarado | rechazar ejecución |
| `CE-033` | texto fuente no disponible | rechazar ejecución |
| `CE-034` | asimetría de oportunidad | revisión manual |
| `CE-035` | `Presente–opuesto` en característica bidireccional no resoluble sin asumir referencia AI-first | cuarentena |
| `CE-036` | procedencia histórica no demostrable ni atestable | rechazar fila/ejecución |
| `CE-037` | sublocalizador incapaz de distinguir observaciones de una misma fila | preservar o revisar |

### 14.3 Contenido de la cuarentena

Cada entrada de cuarentena conserva:

- `legacy_locator`, `legacy_sublocator`;
- `reason_codes`;
- `preserved_payload` con **todos** los campos literales de la fila;
- `source_document_sha256`;
- `feature_registry_version`;
- `export_contract_version`.

La cuarentena es revisable por una persona. No se reintenta automáticamente, no se «arregla» con valores inferidos y no se descarta.

---

## 15. Neutralidad y Fuerza

### 15.1 Neutralidad

Se mantienen **las dos lecturas** identificadas en `v0.1` hasta contar con criterios inequívocos:

- **Lectura a (neutralización contextual):** `observed` + `neutral` + `contextual_neutralization` + `alignment_basis_detail` no nulo.
- **Lectura b (el estudio no establece patrón):** `observed` + `not_assessed` + `none` + `reference_pattern_id=null`.

No se selecciona automáticamente entre R-17 (lectura a) y R-17 (lectura b). La selección exige una regla documentada en la guía de anotación que permita decidir, a partir de la fuente, cuál de las dos lecturas aplica. Hasta entonces, la ambigüedad produce rechazo (`CE-027`).

### 15.2 Fuerza

La fuente histórica utiliza un campo libre (`Fuerza`), no un vocabulario completamente controlado.

- Mapear a `weak` / `moderate` / `strong` **únicamente** cuando exista una regla documentada que vincule el token histórico con el valor controlado.
- En cualquier otro caso: `evidence_strength=not_rated` y conservación del valor literal en `legacy_raw` (`CE-023`).
- **No** confundir `legacy_strength` con `assessment_confidence`. El primero es intensidad cualitativa de la evidencia; el segundo es confianza en la calidad de la lectura. Son campos distintos y no se derivan uno del otro.

### 15.3 Otras opciones

`ambivalent/mixed` sigue siendo una opción de característica (`Moral Polarity Toward Protagonist`), no una dirección global. No confundirlo con `mixed` en agregados (`ClusterSummary`/`AnalysisRun`).

---

## 16. Dependencias metodológicas

Clasificación exigida por la fase: reglas cerradas, decisiones pendientes, guía incompleta y datos faltantes.

### 16.1 Reglas que ya pueden cerrarse

- Vocabulario de 5 estados y 5 direcciones (§7.1, §7.2).
- Ausencia frente a opción categórica explícita (`evidence-status.md`, sección final; §5.3.4).
- Contraevidencia requiere cita y justificación (`evidence-status.md`, «Contraevidencia»).
- Simetría de oportunidad (§9.2).
- Ausencia no tiene dirección (`evidence-status.md`; §5.3, regla 4).
- Resolución A2 y `reference_relation` (§10).
- Reglas por tipo de característica (§10.5).
- Verificación literal de citas y offsets (§5.4).
- `mixed` solo en agregados (§5.3.3).
- Proyección §3 vs §4 sin join automático (§8).

### 16.2 Decisiones metodológicas necesarias

| Decisión | Estado | Efecto si no se cierra |
|---|---|---|
| Confirmar que `Presente–alineado` + polo humano en bidireccional se reexpresa como `opposed` en A2 | adoptada por este contrato; requiere confirmación en la guía | R-04 quedaría en cuarentena |
| Confirmar que la variante `neutral` es dirección `neutro`, no sexto estado | adoptada; requiere confirmación | R-17 quedaría en cuarentena |
| Contenido mínimo de la justificación para `opposed` en escalas | abierta | R-10 no puede aplicarse |
| Contenido mínimo de `status_reason` para `No aplicable` / `No evaluable` | abierta | R-15/R-16 no pueden aplicarse |
| Vocabulario controlado de `Fuerza` | abierta | R-32 emite `not_rated` |
| Existencia y forma del campo de alineación global en `AnalysisRun` | abierta (hueco del contrato de destino) | R-20/R-21 preservan sin escribir |
| Criterio inequívoco para elegir lectura a vs b de `neutro` | abierta | R-17 produce rechazo |
| Procedencia histórica vs atestación de migración | parcialmente resuelta (§11.5) | R-29/R-37 bloquean |

### 16.3 Reglas que requieren completar la guía de anotación

- Selección y delimitación de spans.
- Frontera entre evidencia afirmativa y contraevidencia.
- Resolución de evidencia mixta en el mismo clúster.
- Resolución de múltiples polos en una misma característica.
- Procedimiento de adjudicación de contradicciones.
- Registro de dos observaciones opuestas dentro de una misma característica.
- Criterio de neutralidad contextual (lectura a vs b).
- Vocabulario controlado de `Fuerza`.

### 16.4 Reglas que requieren más datos de origen

- Frecuencia real de cada estado en anotaciones históricas: **no calculable**; el repositorio no contiene corpus.
- Variantes textuales reales de los tokens: solo se conocen las documentadas.
- Catálogo completo de opciones del instrumento: ausente; limita `observed_option_id` a los 33 patrones registrados.
- Existencia de offsets en anotaciones históricas: no consta.

### 16.5 Orden de cierre recomendado

1. Definir el campo de alineación global de `AnalysisRun` y el enum de `adequacy` (bloquea R-20/R-21).
2. Completar la guía en spans, justificación y evidencia mixta (bloquea R-10, R-15, R-16, R-30).
3. Fijar el vocabulario de `Fuerza` (bloquea R-32).
4. Fijar el criterio de neutralidad (bloquea R-17 lectura a/b).
5. Implementar el exportador contra este contrato y los vectores.
6. Abordar la adaptación al español como fase independiente.

Este orden evita rehacer el exportador: los puntos 1–4 son entradas del contrato, no detalles de implementación.

---

## 17. Límites y bloqueos conocidos

### 17.1 Límites del contrato

- No convierte texto libre en etiquetas: solo convierte etiquetas documentadas.
- No valida la calidad científica de la anotación original.
- No reconstruye datos que `v0.2.3` no registró.
- No garantiza round-trip sin el informe de exportación (clase B).
- No sustituye la auditoría semántica de §6.2.
- No autoriza scoring, probabilidad de autoría ni inferencia automática.

### 17.2 Bloqueos del contrato de destino

**B1. `AnalysisRun` no tiene campo de alineación global.** §5.3.3 declara `mixed` válido en `AnalysisRun`, pero §5.2 no enumera ningún campo que lo transporte (`report_summary` aparece en §5.1 sin forma definida). Hasta que se defina, la etiqueta global se preserva en el informe y, si procede, se expresa en `ClusterSummary.alignment`. No se inventa un campo.

**B2. `AnalysisRun.adequacy` no tiene enum documentado.** §5.2 exige «estado, motivos y reglas aplicadas», pero no fija valores. La etiqueta histórica `evidencia insuficiente` y la puerta de adecuación se preservan; no se escriben como valores de enum inventados.

**B3. `observed_option_id` depende del catálogo de opciones.** El Feature Registry contiene 33 patrones de referencia, no el catálogo completo del instrumento. Las opciones no elevadas no tienen ID y se registran como `observed_value_text`.

**B4. `observation_origin` es obligatorio y no tiene fuente histórica.** Requiere declaración explícita del operador o atestación de migración (§11.5). Sin ella, la ejecución se rechaza.

### 17.3 Bloqueos científicos (no resueltos aquí)

- Adaptación al español exploratoria y no validada.
- Sin corpus histórico de anotaciones.
- Sin acceso al corpus original ni a los pesos del paper.

---

## 18. Criterios de conformidad

Una exportación cumple este contrato si y solo si:

1. Cada fila de entrada tiene un resultado explícito de las cinco clases.
2. Todo registro emitido tiene `record_id`, `feature_id`, `dimension_id`, `observation_origin`, `source_spans` y `cluster_id`.
3. Todo `observed` tiene al menos un `source_span` literal verificado.
4. Todo `not_observed` tiene `opportunity_status=sufficient`, `status_reason`, `absence_justification` y `search_scope`.
5. Todo `opposed` tiene span, justificación y cumple `INV-A2-10` o `INV-A2-11`.
6. Ningún `EvidenceRecord` contiene `mixed`, `historical_reference_pattern_id` ni códigos `CE-*`.
7. `reference_relation` solo usa `aligned`, `opposed`, `not_assessed`.
8. La referencia histórica se resuelve desde el registro y no se duplica.
9. Dos exportaciones de la misma fuente con los mismos parámetros producen los mismos `record_id` y el mismo conjunto lógico de registros, con clave `(source_document_sha256, legacy_sublocator)`.
10. El informe de exportación contiene `legacy_raw` de toda fila emitida, preservada, en cuarentena o rechazada.
11. El informe de pérdidas cubre toda conversión que cambie el estado o descarte un campo.
12. No se modificó ningún archivo de `v0.2.3`, del Feature Registry, del Charter ni de la Spec.
13. La etiqueta global y `analysis_quality_confidence` se preservan en el informe externo, sin escritura en el dominio.
14. Toda atestación de migración queda registrada en `migration_attestations`.

Los vectores que demuestran estos criterios están en `COMPATIBILITY_TEST_VECTORS_v0.2.md`.

---

*Predecesor: `COMPATIBILITY_EXPORT_CONTRACT_v0.1.md` (preservado). Cambios sustantivos de v0.1 a v0.2: R-07 reclasificado de conversión a cuarentena (`CE-035`); R-17/R-20 no escriben etiqueta global en `ClusterSummary` por defecto; sublocalizador añadido (§11.2); procedencia por atestación de migración (§11.5); nuevos diagnósticos CE-035/036/037; export_contract_version 0.1.0 → 0.2.0.*
