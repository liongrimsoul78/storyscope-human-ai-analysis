# Contrato de exportación de compatibilidad — v0.3

**Proyecto:** StoryScope Human–AI Analysis
**Fase:** 1.22 — auditoría de coherencia del contrato y cierre de la ruta §4
**Estado:** contrato documental, no implementado
**Fecha:** 2026-11-19
**Origen normativo:** `v0.2.3` (tag anotado `d7221dab…`, commit `a629af7d…`)
**Destino normativo:** rama `feature/storyscope-v0.3.0-design`, `TECHNICAL_SPEC_v0.1.md` y `FEATURE_REGISTRY_v0.1.2-draft.json`
**Predecesores preservados:** `COMPATIBILITY_EXPORT_CONTRACT_v0.1.md`, `COMPATIBILITY_EXPORT_CONTRACT_v0.2.md`

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

**Corrección estructural de v0.3.** La plantilla histórica tiene dos tablas de niveles distintos:

- **§3 — Perfil por dimensiones:** filas de dimensión con `Estado de evidencia (5)` y `Dirección`. No tienen `feature_id`.
- **§4 — Indicadores centrales:** filas de característica con valor observado y cita. **No tienen `Estado de evidencia` ni `Dirección`.**

La v0.2 trataba el estado de §3 como si pudiera alimentar características de §4. Eso es un join prohibido. La v0.3 define **dos rutas de ingestión independientes** (§8 y §9): la ruta D (§3) no genera `EvidenceRecord`; la ruta F (§4) deriva `observation_status` del valor explícito y del span literal, sin heredar estado ni dirección de §3.

---

## 2. Alcance y exclusiones

### 2.1 Incluido

- Inventario de los valores históricos realmente documentados en `v0.2.3`.
- Proyección explícita de las dos tablas de la plantilla (`§3` y `§4`) a niveles de ejecución, dimensión y característica.
- Contrato de entrada documental y de salida (`analysis.json` + informe de exportación).
- Reglas de conversión por ruta: dimensión (§3) y característica (§4).
- Reglas de estado/dirección para filas que portan estado explícito.
- Contrato A2 / F-02 ya consolidado.
- Trazabilidad, idempotencia con sublocalizador, reversibilidad y versionado del contrato.
- Diagnósticos y cuarentena externos al modelo de dominio.
- Procedencia histórica frente a atestación de migración.
- Vectores de prueba contractuales (documento aparte).
- Validador documental cruzado (regla ↔ matriz ↔ vectores ↔ cobertura ↔ reversibilidad).

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
| `references/report-template.md` | `v0.2.3` | §1; §3 y su nota «Estados permitidos / Dirección»; §4; §6 | Vocabulario de dirección; estructura de filas; etiqueta global; **§4 sin estado ni dirección** |
| `SKILL.md` | `v0.2.3` | §5 «Direction labels»; §6; §12 | Definición operativa de `mixto`, `neutro`, `no evaluable`; formato de salida |
| `references/feature-dimension-map.csv` | `v0.2.3` | 30 filas | Nombre de característica, tipo de medida, dirección elevada, opciones canónicas |
| `references/core-patterns.md` | `v0.2.3` | listas AI-elevated / human-elevated | Patrones elevados por grupo |
| `references/cluster-map.md` | `v0.2.3` | 8 clústeres operativos | Agrupación y reglas de doble conteo |
| `references/numeric-integrity-v0.2.3.md` | `v0.2.3` | «Excepciones de redondeo documentadas» | Valores publicados; prohibición de recalcular gaps |
| `references/data-integrity-v0.2.2.md` | `v0.2.3` | tabla corregida | Precedente de corrección de valores; `ambivalent/mixed` como opción |
| `references/worked-examples/01-microrelato-21-palabras.md` | `v0.2.3` | «Evaluación obligatoria»; «Observaciones que sí pueden hacerse» | Ejemplo real de `No evaluable` por longitud y de observación local |
| `docs/design/v0.3.0/TECHNICAL_SPEC_v0.1.md` | rama feature | §4.1; §5.1–§5.7; §6.4; §6.5; §10.3 | Contrato de destino, invariantes A2, reglas por tipo |
| `docs/design/v0.3.0/FEATURE_REGISTRY_v0.1.2-draft.json` | rama feature | `feature_records`; `cluster_catalog`; `dimensions`; `counts`; `id_policy` | Fuente única de `historical_reference_pattern_id`; 30 features, 33 patrones |
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
- identificador estable de registro;
- **estado o dirección a nivel de característica en §4**;
- **oportunidad de observación a nivel de característica**.

Estas ausencias **no se suplen por invención**: se convierten en precondiciones del contrato (§5.4) o en bloqueos declarados (§17).

---

## 4. Versiones

Cuatro dimensiones independientes. Confundirlas es un error de contrato.

| Eje | Identificador en este contrato | Valor `v0.3` | Autoridad | Regla de cambio |
|---|---|---|---|---|
| Contrato de exportación | `export_contract_version` | `0.3.0` | este documento | SemVer: en la fase de diseño (0.x) una revisión sustantiva de rutas de ingestión, reglas de conversión, idempotencia y reversibilidad se expresa como incremento *minor* (0.2.0 → 0.3.0). El *major* se reserva para la congelación del contrato al iniciar la implementación. |
| Esquema de origen | `source_format_id` + `source_skill_version` | `storyscope-v0.2.3-qualitative-report` + `0.2.3` | `v0.2.3` | `source_format_id` lo asigna **este contrato**; no es un identificador hallado en `v0.2.3`. `v0.2.3` no tiene esquema machine-readable |
| Esquema de destino | `bundle_schema_version` | `1.0.0` | `TECHNICAL_SPEC` §5.1 | lo fija el proyecto, no el exportador |
| Registro de características | `feature_registry_version` + `feature_registry_schema_version` | `0.1.2-draft` + `1.1.0` | `FEATURE_REGISTRY_v0.1.2-draft.json` | fijado e inmutable por ejecución (`INV-A2-16`) |

Reglas:

- `export_contract_version` **nunca** se escribe dentro de `EvidenceRecord`, `ClusterSummary` ni `AnalysisRun`; vive en el sobre de exportación y en el informe de exportación.
- `feature_registry_version` se escribe en `AnalysisRun` porque el contrato de destino ya lo exige (§5.2) y porque sin él la referencia histórica no es resoluble.
- Cambiar de versión de registro **no** reescribe una exportación anterior: exige una nueva ejecución con revalidación explícita (§5.7, `INV-A2-16`).
- `schema_version` del Feature Registry (`1.1.0`) no se modifica en esta fase.

**Justificación del incremento 0.2.0 → 0.3.0.** La v0.3 separa las rutas §3 y §4, redefine la identidad de idempotencia y corrige la clase de reversibilidad de `Presente–opuesto` unidireccional. Son cambios de reglas de conversión, no erratas editoriales; por tanto, incremento *minor* en fase 0.x.

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
| `adequacy_gate` (`no apto` / `exploratorio` / `perfil cualitativo posible`) | §1 | sí | `AnalysisRun.adequacy` (sujeto a §17-B2) |
| `global_label` (`patrón humano` / `patrón IA` / `mixto` / `neutro` / `evidencia insuficiente`) | §6 | sí | nivel de ejecución; ver R-20/R-21 y §17-B1 |
| `analysis_quality_confidence` (`baja` / `moderada` / `alta`) | §6 | no | **no** se propaga a registros; ver R-23 y §15.3 |
| `legacy_observation_origin` (`human_annotation` / `external_model` / `independent_tool` / `authorized_experiment`) | **no existe en `v0.2.3`** | sí, por **una de dos vías**: declaración explícita del operador (este campo) o atestación de migración válida (§11.6, M-55) | `EvidenceRecord.observation_origin` |
| `migration_attestations` | informe externo (§11.6) | condicional: obligatorio si la procedencia se aporta por atestación; prohibido inferirlo | informe de exportación; fuente de verdad de la atestación |
| `source_text` disponible para verificación de citas | implícito en el análisis | sí | cálculo de `source_spans` |
| `source_document_sha256`, `source_git_tag`, `source_git_commit` | cálculo del exportador | sí | sobre de exportación |
| `feature_registry_version` | `AnalysisRun` de destino | sí | resolución A2 |

### 5.3 Campos de fila (row-level)

`v0.2.3` tiene **dos tablas distintas y de niveles distintos**. La proyección completa está en §8.

**Tabla §3 — perfil por dimensiones** (10 filas, una por dimensión):

| Columna histórica | Campo de entrada | Observación |
|---|---|---|
| `Dimensión` | `dimension_name` | nombre bilingüe; resoluble a `dimension_id` |
| `Observación respaldada` | `observation_text` | prosa; no es una cita de característica |
| `Estado de evidencia (5)` | `legacy_state` | taxonomía de 5 estados; **nivel dimensión** |
| `Clúster` | `cluster_name` | opcional; resoluble a `cluster_id` |
| `Dirección` | `legacy_direction` | **dirección de la observación de dimensión**, no de una característica |
| `Fuerza` | `legacy_strength` | sin vocabulario controlado en `v0.2.3` |
| `Por qué / alternativa contextual` | `contextual_alternative` | justificación / explicación alternativa |

**Tabla §4 — indicadores centrales** (solo clústeres relevantes):

| Columna histórica | Campo de entrada | Observación |
|---|---|---|
| `Clúster` | `cluster_name` | resoluble a `cluster_id` |
| `Característica/valor observado` | `feature_name` + `observed_value_text` | resoluble a `feature_id`; el valor es explícito |
| `Cita o ubicación` | `quotation_or_location` | puede no ser literal ni tener offsets |
| `Dirección del estudio` | **no es un campo de observación** | es la dirección elevada del estudio; se resuelve desde el registro, nunca se copia a `research_alignment` |
| `Contraevidencia real` | `real_counterevidence` | contraevidencia afirmativa citada; exige span y justificación propios |
| `Explicación alternativa` | `contextual_alternative` | — |
| `Fuerza` | `legacy_strength` | — |

> **Trampa documentada 1.** La columna `Dirección del estudio` de §4 describe el hallazgo del paper, no la observación del texto. Un exportador que la copie a `research_alignment` fabricaría alineación. El contrato prohíbe esa copia (R-35).
>
> **Trampa documentada 2.** §4 **no tiene** `Estado de evidencia` ni `Dirección`. Un exportador que exija esos campos a una fila §4 rechazaría todas las filas válidas. La ruta F (§9.4) no los exige y no los hereda de §3.

### 5.4 Requisitos mínimos de la entrada

Una ejecución solo puede iniciarse si se cumplen **todos**:

1. `feature_registry_version` está fijada y la versión existe y es resoluble (§5.7, `INV-A2-16`).
2. `legacy_observation_origin` **o** una atestación de migración válida. `v0.2.3` no registra `observation_origin`; el exportador no puede inferirlo. Se admiten dos vías, mutuamente verificables:
   - **Vía directa:** el operador declara `legacy_observation_origin` con uno de los cuatro valores permitidos.
   - **Vía atestada:** existe al menos una entrada válida en `migration_attestations` con `attested_origin` igual a uno de los cuatro valores permitidos (M-55).
   Si coexisten ambas, sus valores deben coincidir; una discrepancia es rechazo, no se resuelve silenciosamente. Si ninguna vía aporta procedencia válida, la ejecución se rechaza (R-29/R-37, `CE-032`/`CE-036`).
3. El texto analizado está disponible para verificar citas (§5.4). Sin texto no hay `source_spans` verificables y, por la regla 5 de §5.3, no hay `observed` válido.
4. El documento fuente tiene digest SHA-256 calculado.
5. **Para cada fila §3:** declara `legacy_state`. Una fila §3 sin estado no es una anotación (`evidence-status.md`: «No se puede asignar dirección a un rasgo hasta registrar su estado»).
6. **Para cada fila §4:** declara un valor observado explícito y una cita o ubicación. No se exige `legacy_state` ni `legacy_direction`.

Si falla 1, 2, 3 o 4, la ejecución se **rechaza completa**; no se emiten registros parciales. Si falla 5, se rechaza la fila §3. Si falla 6, se rechaza la fila §4.

### 5.5 Lo que la entrada no puede contener

- Texto completo almacenado en el bundle (§5.2: «No almacenar texto completo»).
- Probabilidades, porcentajes de autoría o scores globales (§5.3, regla 10).
- IDs inventados de característica, opción o patrón.
- Offsets calculados sobre texto normalizado (§5.4: sin normalización Unicode ni conversión de finales de línea).
- Valores numéricos derivados de medias grupales de Table 16 (§4.2).
- Un `legacy_state` de §3 copiado a una fila §4.

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
8. **Escribir la etiqueta global `mixto` en `ClusterSummary.alignment` por la simple existencia de dos `record_ids` con alineaciones distintas** (R-20).
9. **Copiar `analysis_quality_confidence` a `EvidenceRecord.assessment_confidence`** (R-23).
10. **Escribir `legacy_state` o `legacy_direction` de una fila §3 en un `EvidenceRecord` de una característica §4** (R-38, R-39).
11. **Escribir un `EvidenceRecord` con `observation_status=not_observed`, `not_applicable` o `not_evaluable` a partir de una fila §3.** La ruta D no emite registros atómicos; esos estados pertenecen a `DimensionProfile.coverage_status` y al informe externo.

### 6.4 Forma del informe de exportación (documental)

```json
{
  "export_contract_version": "0.3.0",
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
    "dimension_rows_read": 0,
    "feature_rows_read": 0,
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
      "route": "D | F | F+",
      "outcome": "converted | converted_with_flag | preserved | quarantined | rejected",
      "legacy_raw": {
        "state": "<token literal o null>",
        "direction": "<token literal o null>",
        "section": "§3 | §4",
        "feature_name": "<texto literal>",
        "cluster_name": "<texto literal>",
        "strength": "<texto literal>",
        "study_direction": "<texto literal>",
        "counterevidence": "<texto literal>"
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

`counts` es informativo y debe ser coherente con las listas; el contrato no exige un orden concreto de registros, pero sí que la exportación sea determinista (§12).

---

## 7. Ejes de la anotación histórica

`v0.2.3` usa **tres vocabularios distintos** que no deben colapsarse.

### 7.1 Eje de estado (5 valores)

Fuente: `references/evidence-status.md`, tabla «Estados de evidencia».

| Valor normativo | Significado operativo | Nivel histórico |
|---|---|---|
| `Presente–alineado` | valor observado que coincide con la opción/dirección elevada | §3 (dimensión); extensión F+ |
| `Presente–opuesto` | valor observado que es el polo alternativo; contraevidencia real | §3 (dimensión); extensión F+ |
| `Ausente` | se buscó y no se halló; sin dirección por defecto | §3 (dimensión) |
| `No aplicable` | el rasgo no corresponde al género/tarea | §3 (dimensión) |
| `No evaluable` | longitud, fragmentariedad, contexto u oportunidad impiden decidir | §3 (dimensión) |

**Variante documental:** `neutral` aparece en la «Regla de decisión», paso 3, como tercera opción de estado. No pertenece a la tabla normativa. Se registra como variante (`CE-020`) y se normaliza a observación presente + dirección `neutro`; **no se crea un sexto estado**.

### 7.2 Eje de dirección (5 valores)

Fuente: `report-template.md` §3, nota «Estados permitidos / Dirección»; `SKILL.md` §5 «Direction labels».

| Valor | Significado | Puede combinarse con |
|---|---|---|
| `patrón IA` | el valor observado se alinea con una opción/media elevada para IA | `Presente–alineado`, `Presente–opuesto` (solo si la dirección no es la elevada del feature unidireccional) |
| `patrón humano` | se alinea con una opción/media elevada para humanos | `Presente–alineado`, `Presente–opuesto` (solo si la dirección no es la elevada del feature unidireccional) |
| `mixto` | «one canonical feature has relevant observations pointing in both directions or is genuinely ambiguous» | solo agregados; ver R-19/R-20 |
| `neutro` | «observed but the study does not establish a meaningful directional pattern» | `Presente` (dos lecturas; ver R-17) |
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

La plantilla `v0.2.3` tiene dos tablas de niveles distintos. **No se hace join automático entre ellas.** Se definen dos rutas independientes.

### 8.1 Ruta D — §3, nivel dimensión

| Campo histórico | Sección | Nivel | Disponibilidad | Destino posible | Condiciones | Pérdidas | Limitaciones |
|---|---|---|---|---|---|---|---|
| `Dimensión` | §3 | dimensión | siempre (10 filas) | `DimensionProfile.dimension_id` | resolución por nombre | ninguna | — |
| `Observación respaldada` | §3 | dimensión | siempre | `DimensionProfile.neutral_summary` | — | no es registro atómico | descriptiva |
| `Estado de evidencia (5)` | §3 | dimensión | siempre | `DimensionProfile.coverage_status` (derivado) | regla R-13…R-16 | el token literal solo en el informe | dimensión ≠ característica |
| `Clúster` | §3 | dimensión | opcional | agrupación de perfiles | `cluster_id` resoluble | — | — |
| `Dirección` | §3 | dimensión | opcional | **ninguno** | opcional; si existe se conserva literalmente; su ausencia no rechaza la fila (R-D07) | no convertible a `research_alignment` | dimensión ≠ característica |
| `Fuerza` | §3 | dimensión | opcional (texto libre) | **ninguno** | — | preservar en informe | texto libre |
| `Por qué / alternativa contextual` | §3 | dimensión | opcional | `DimensionProfile.limitations` | — | — | — |

**Regla D:** una fila de §3 **nunca** genera `EvidenceRecord`. El estado y la dirección de dimensión no se replican en características.

**Nota sobre `legacy_direction` en ruta D.** `legacy_direction` es **opcional**. Su ausencia o su no normalización **no** rechazan la fila: el token se conserva literalmente en `legacy_raw` y no se usa para producir `research_alignment` (R-D07). La dirección de dimensión nunca se replica en características (R-D06). La única exigencia de ruta D es `legacy_state` válido (R-01, R-D01).

### 8.2 Ruta F — §4, nivel característica

| Campo histórico | Sección | Nivel | Disponibilidad | Destino posible | Condiciones | Pérdidas | Limitaciones |
|---|---|---|---|---|---|---|---|
| `Clúster` | §4 | característica (clúster) | siempre | `ClusterSummary.cluster_id` / `record.cluster_id` | `cluster_id` resoluble | — | — |
| `Característica/valor observado` | §4 | característica | siempre | `EvidenceRecord.feature_id` + `observed_value_text` | `feature_id` resoluble; valor explícito | — | si no resoluble → rechazo |
| `Cita o ubicación` | §4 | característica | opcional | `SourceSpan` | subcadena literal + offsets | si no literal → cuarentena | sin offsets históricos |
| `Dirección del estudio` | §4 | característica | siempre | **ninguno** (dirección del paper) | resolver desde el registro | nunca copiar a `research_alignment` | — |
| `Contraevidencia real` | §4 | característica | opcional | `counterevidence_record_ids` + registro propio | span y justificación propios | si falta span/justificación → cuarentena | no reutiliza la cita principal |
| `Explicación alternativa` | §4 | característica | opcional | `interpretation` / `alternative_explanations` | — | — | — |
| `Fuerza` | §4 | característica | opcional (texto libre) | `evidence_strength` (solo si mapea) | regla documentada | `CE-023` si no mapea | texto libre |
| Campos run-level (§1) | §1 | ejecución | varios | `AnalysisRun` / informe | — | — | — |
| Etiqueta global, `adequacy_gate`, `analysis_quality_confidence` | §6 | ejecución | varios | informe externo (run-level) | — | no escribir en dominio | §17-B1/B2 |

**Regla F:** una fila de §4 genera **cero o más** `EvidenceRecord`, uno por observación independiente y localizable. Nunca genera un registro por dimensión. La alineación se asigna solo cuando el valor observado mapea inequívocamente a un patrón registrado o cuando la propia fila declara una dirección explícita (extensión F+).

### 8.3 Lo que no se emite desde `v0.2.3`

La ruta D no emite `not_observed`, `not_applicable` ni `not_evaluable` como `EvidenceRecord`. La ruta F solo emite `observed` (incluidas las opciones categóricas explícitas de ausencia, que son observaciones). Por tanto:

- `not_observed` **no** se produce a partir de `Ausente` de §3: no hay `feature_id` y no se hace join.
- `not_applicable` **no** se produce a partir de `No aplicable` de §3: se expresa como `DimensionProfile.coverage_status=not_applicable`.
- `not_evaluable` **no** se produce a partir de `No evaluable` de §3: se expresa como `DimensionProfile.coverage_status=not_assessable`.

Estos estados siguen siendo válidos para análisis nuevos de `v0.3.0`; simplemente no son producibles por el exportador de compatibilidad sin inventar un `feature_id` que la fuente no contiene.

---

## 9. Reglas de conversión

Cada fila produce **exactamente un** resultado: `converted`, `converted_with_flag`, `preserved`, `quarantined` o `rejected`. La matriz completa está en `COMPATIBILITY_MAPPING_MATRIX_v0.3.md`.

**Rutas:**

- **D** — fila §3 (dimensión). No genera `EvidenceRecord`.
- **F** — fila §4 estándar (sin estado ni dirección). Genera `EvidenceRecord` derivado del valor y el span.
- **F+** — fila de característica que **porta explícitamente** `legacy_state` y `legacy_direction` (extensión no estándar). Usa las reglas de estado/dirección; el estado debe ser propio de la fila, nunca heredado de §3.

### 9.1 Reglas de ejecución

| ID | Condición | Acción | Destino | Diagnóstico |
|---|---|---|---|---|
| R-29 | procedencia ausente: ni declaración directa válida ni atestación válida (M-55) | rechazar ejecución | — | `CE-032` |
| R-29a | declaración directa y atestación válidas pero con valores distintos | rechazar ejecución | — | `CE-032` |
| R-34 | `feature_registry_version` inexistente o no resoluble | rechazar ejecución | — | `CE-005` |
| R-30e | falta texto fuente o digest | rechazar ejecución | — | `CE-033`/`CE-024` |
| R-20 | etiqueta global `mixto` | preservar en informe externo; **no** escribir en `ClusterSummary.alignment` por defecto | `run_level.legacy_global_label` | `CE-015` |
| R-21 | etiqueta global `evidencia insuficiente` | preservar | `run_level` | `CE-028` |
| R-22 | `adequacy_gate` | preservar | `run_level` | — |
| R-23 | `analysis_quality_confidence` | preservar | `run_level`; **no** copiar a `assessment_confidence` | — |
| R-37 | procedencia histórica no demostrable ni atestable | rechazar fila/ejecución según alcance | — | `CE-036` |

**Precisión sobre R-29 y M-55.** R-29 no exige un campo literal `legacy_observation_origin` cuando la procedencia se aporta por atestación. Las dos vías son equivalentes y excluyentes en valor: una declaración directa válida o una atestación válida satisfacen el requisito; ambas juntas solo si coinciden. M-55 (ruta X) es la condición de procedencia a nivel de ejecución que habilita el establecimiento de `observation_origin` a partir de una atestación válida; no genera `EvidenceRecord` por sí misma y no sustituye la fuente de verdad, que sigue siendo `migration_attestations`.

### 9.2 Ruta D — reglas de dimensión (§3)

| ID | Condición | Acción | Destino | Diagnóstico |
|---|---|---|---|---|
| R-01 | fila §3 sin `legacy_state` | rechazar fila | — | `CE-025` |
| R-D01 | `legacy_state` no reconocido | rechazar fila | — | `CE-001` |
| R-D07 | `legacy_direction` ausente o no reconocido en ruta D | preservar; conservar el token literal en `legacy_raw`; **no** rechazar la fila; **no** producir `research_alignment` | `DimensionProfile` | `CE-002` informativo |
| R-D02 | `dimension_name` no resoluble | rechazar fila | — | `CE-018` |
| R-D03 | `cluster_name` no resoluble | convertir con bandera; `cluster_id=null` | `DimensionProfile` | `CE-017` |
| R-13 | `Ausente` + `completeness=completo` | preservar; `coverage_status=descriptive_assessed` | `DimensionProfile` | `CE-040` informativo |
| R-14 | `Ausente` + `fragmento`/`desconocido` | preservar; `coverage_status=partially_assessed`/`not_assessable` | `DimensionProfile` | `CE-013` |
| R-15 | `No aplicable` | preservar; `coverage_status=not_applicable` | `DimensionProfile` | `CE-019` si falta motivo |
| R-16 | `No evaluable` | preservar; `coverage_status=not_assessable` | `DimensionProfile` | `CE-019` si falta motivo |
| R-25 | fila §3 con estado presente/opuesto/neutral | preservar; `coverage_status=descriptive_assessed` | `DimensionProfile` | `CE-029` informativo |
| R-D04 | `Presente–opuesto` sin texto de observación o sin justificación | cuarentena | — | `CE-009`/`CE-010` |
| R-D05 | `legacy_strength` presente | preservar literal; no mapear en ruta D | informe | `CE-023` si se intenta mapear |
| R-D06 | fila §3 intenta aportar `feature_id` o alimentar §4 | ignorar el join; preservar | `DimensionProfile` | `CE-029` |

**Nota sobre `Presente–opuesto` en ruta D.** En §3, `Presente–opuesto` es una contraevidencia **de dimensión**. Se preserva como nota descriptiva y no se promueve a `reference_relation=opposed`, porque no existe una característica atómica a la que vincularla. Si se desea contraevidencia a nivel de característica, debe constar en la columna `Contraevidencia real` de §4 con su propio span y justificación (R-F08).

### 9.3 Ruta F+ — reglas de estado/dirección (extensión no estándar)

Estas reglas solo se aplican cuando una fila de característica porta **explícitamente** `legacy_state` y `legacy_direction`. No se aplican a §3 (que no tiene `feature_id`) ni a §4 estándar (que no tiene estado). Se conservan para informes históricos que hayan añadido esas columnas y para los vectores TV-01…TV-34.

| ID | Condición | Acción | Destino | Diagnóstico |
|---|---|---|---|---|
| R-02 | `legacy_direction` ausente o no reconocido en F+ | rechazar fila | — | `CE-002` |
| R-03 | `Presente–alineado` + dirección = dirección de la referencia histórica | convertir | `observed` + `pattern_ai`/`pattern_human` + `reference_pattern_id`=referencia + `aligned` | span; justificación |
| R-04 | `Presente–alineado` + polo humano en bidireccional | **BLOQUEADA**: no convertir hasta que la guía de anotación justifique la reexpresión como `opposed` | — | `CE-021` (bloqueo) |
| R-05 | `Presente–alineado` + dirección opuesta, unidireccional | rechazar fila | — | `CE-008` |
| R-06 | `Presente–alineado` + dirección opuesta a la referencia, cualquier tipo | rechazar fila | — | `CE-007` |
| R-07 | `Presente–opuesto` + bidireccional + `patrón IA` | rechazar fila (contradicción directa) | — | `CE-007` |
| R-08 | `Presente–opuesto` + bidireccional + `patrón humano` | **cuarentena** (no resoluble sin asumir referencia AI-first) | — | `CE-035` |
| R-09 | `Presente–opuesto` + unidireccional categórica/binaria/multiselección, valor ≠ referencia | convertir | `observed` + `not_assessed` + `reference_pattern_id=null` + `opposed` | `CE-026`/`CE-022` |
| R-09a | multiselección: `Presente–opuesto` sustentado solo en ausencia de la referencia | rechazar fila | — | `CE-012` |
| R-09b | unidireccional: `Presente–opuesto` cuyo valor es el propio patrón de referencia | rechazar fila | — | `CE-007` |
| R-10 | `Presente–opuesto` + escala/ordinal, valor ≠ referencia | convertir solo con ancla documentada | `observed` + `not_assessed` + `opposed` | `CE-011` si falta ancla |
| R-11 | `Presente–opuesto` sin span | cuarentena | — | `CE-009` |
| R-12 | `Presente–opuesto` sin justificación | cuarentena | — | `CE-010` |
| R-17 | variante `neutral` o `Presente–alineado` + `neutro` | convertir con bandera | `observed` + `neutral` (lectura a) o `not_assessed` (lectura b) | `CE-020`/`CE-027` |
| R-18 | `neutro` sin lectura seleccionable | rechazar fila | — | `CE-027` |
| R-19 | dirección `mixto` a nivel de característica | cuarentena | — | `CE-014` |

**Estado de R-04.** R-04 **no está adoptada**. La §16.2 la mantiene bloqueada. Ningún vector puede declararla convertida. Si un informe F+ presenta `Presente–alineado` + polo humano en bidireccional, el resultado es `quarantined` con `CE-021` hasta que la guía de anotación aporte la justificación semántica.

### 9.4 Ruta F — reglas de característica (§4 estándar)

| ID | Condición | Acción | Destino | Diagnóstico |
|---|---|---|---|---|
| R-38 | §4 con `feature_id` resoluble + valor explícito + span literal | convertir: `observed` derivado; `opportunity_status` según completitud; `assessment_confidence=not_rated` | `EvidenceRecord` | — |
| R-39 | valor observado mapea a `historical_reference_pattern_id` | `aligned`; `research_alignment=dir(referencia)`; `reference_pattern_id`=referencia; `observed_option_id`=referencia si `response_option` | `EvidenceRecord` | — |
| R-40 | valor observado mapea a otro patrón registrado de la misma característica (solo bidireccional) | `opposed`; `research_alignment=dir(otro)`; `reference_pattern_id`=otro; `observed_option_id`=otro | `EvidenceRecord` | — |
| R-41 | valor observado no mapea a ningún patrón registrado | `observed` + `not_assessed` + `reference_pattern_id=null` + `observed_option_id=null`; `observed_value_text` literal | `EvidenceRecord` | `CE-022` |
| R-42 | característica con patrón `overall_feature` (escala/ordinal) | `observed` + `not_assessed` por defecto; alineación solo con token direccional explícito en la fila y `alignment_basis_detail` | `EvidenceRecord` | `CE-026` si el token no está registrado |
| R-F01 | §4 sin `feature_id` resoluble | rechazar fila | — | `CE-003`/`CE-004` |
| R-F02 | §4 sin valor observado explícito | rechazar fila | — | `CE-025` |
| R-F03 | valor presente pero sin span literal | cuarentena | — | `CE-031` |
| R-F04 | `Contraevidencia real` sin span propio | cuarentena | — | `CE-009` |
| R-F05 | `Contraevidencia real` sin justificación propia | cuarentena | — | `CE-010` |
| R-F06 | `Contraevidencia real` reutiliza la cita principal sin justificación independiente | cuarentena | — | `CE-039` |
| R-F07 | `Contraevidencia real` en escala/ordinal sin ancla | cuarentena | — | `CE-011` |
| R-F08 | `Contraevidencia real` válida | registro propio: `observed` + `opposed`; bidireccional con patrón opuesto; unidireccional `not_assessed` + `reference_pattern_id=null` | `EvidenceRecord` | — |
| R-F09 | múltiples valores en una celda sin spans separados | un registro principal con el conjunto; no dividir automáticamente | `EvidenceRecord` | `CE-037` si hay colisión |
| R-F10 | dos observaciones con spans separados en la misma fila | dos registros con `:obs:1`, `:obs:2` | `EvidenceRecord` | — |
| R-31 | repetición exacta de la **misma localización fuente** | deduplicar | un registro | `CE-016` informativo |
| R-31b | filas físicamente distintas con contenido idéntico | **no deduplicar**; preservar ambas; marcar posible duplicado | dos registros | `CE-038` informativo |
| R-31c | duplicados conflictivos en la misma localización fuente | cuarentena de ambas | — | `CE-016` |
| R-35 | columna `Dirección del estudio` de §4 | no convertir; resolver desde el registro | — | — |
| R-36 | sublocalizador incapaz de distinguir dos observaciones | preservar o revisar; no emitir registro ambiguo | — | `CE-037` |
| R-32 | `legacy_strength` fuera de `weak`/`moderate`/`strong` | convertir con bandera; `evidence_strength=not_rated` | `EvidenceRecord` | `CE-023` |

**Precisión sobre R-38 y `opportunity_status`.** `v0.2.3` no registra oportunidad por característica. El exportador la deriva de `completeness` de §1:

- `completo` → `sufficient`;
- `fragmento` → `limited`;
- `desconocido` → `unknown`.

La derivación se registra en el informe. No se inventa una evaluación de oportunidad que la fuente no contiene.

**Precisión sobre R-42.** Para escalas y medias ordinales, el registro solo tiene un patrón `overall_feature`; no hay umbral por historia. El valor observado («alto», «4/5», «escaso») no basta para afirmar alineación. Por eso el resultado por defecto es `observed` + `not_assessed`. Solo un token direccional explícito en la propia fila (`patrón IA`, `patrón humano`, `neutro`) permite alineación, y siempre con `alignment_basis_detail`. Esto evita fabricar alineación a partir de medias grupales.

### 9.5 Precedencia

1. Rechazo de ejecución (R-29, R-34, R-30e) antes que cualquier fila.
2. Rechazo de fila (R-01, R-D01, R-D02, R-05, R-06, R-07, R-09a, R-09b, R-18, R-F01, R-F02; R-02 solo en F+) antes que cualquier conversión.
3. Cuarentena (R-04, R-08, R-11, R-12, R-15, R-16, R-19, R-F03…R-F07, R-31c, R-36) antes que emisión.
4. Conversión.
5. Deduplicación (R-31) sobre el conjunto ya convertido; R-31b no deduplica.

### 9.6 Regla de simetría

`evidence-status.md`, «Regla de simetría»: la oportunidad se evalúa con el mismo estándar para valores humanos y de IA. El exportador **no** puede aceptar `Ausente` para una característica humana y `No evaluable` para la misma oportunidad en una característica de IA (ni lo contrario). Una ejecución que produzca esa asimetría sin justificación documental emite `CE-034 ASYMMETRIC_OPPORTUNITY` y se revisa manualmente.

### 9.7 Combinaciones estado × dirección (solo F+)

| Estado | Dirección | Tipo de feature | Lectura | Resultado |
|---|---|---|---|---|
| `Presente–alineado` | `patrón IA` | unidireccional IA | valor = opción elevada | convertir → `aligned` |
| `Presente–alineado` | `patrón humano` | unidireccional humana | valor = opción elevada | convertir → `aligned` |
| `Presente–alineado` | `patrón IA` | bidireccional | valor = polo IA | convertir → `aligned` |
| `Presente–alineado` | `patrón humano` | bidireccional | valor = polo humano | **bloqueado** (R-04) → cuarentena `CE-021` |
| `Presente–alineado` | dirección opuesta a la elevada | unidireccional | contradicción | rechazar (`CE-008`/`CE-007`) |
| `Presente–opuesto` | `patrón IA` | unidireccional IA | valor = alternativo, dirección dice IA | rechazar (`CE-007`) |
| `Presente–opuesto` | `patrón humano` | unidireccional IA | valor = alternativo; dirección no registrada | convertir → `not_assessed` + `opposed` (`CE-026`) |
| `Presente–opuesto` | `patrón IA` | bidireccional | contradicción directa | rechazar (`CE-007`) |
| `Presente–opuesto` | `patrón humano` | bidireccional | **no resoluble sin asumir referencia AI-first** | **cuarentena** (`CE-035`) |
| `Presente–opuesto` | `no evaluable` / `neutro` | unidireccional | dirección no registrada | convertir → `not_assessed` + `opposed` (`CE-026`) |
| `Ausente` | `no evaluable` | cualquiera | ausencia sin dirección | ruta D: preservar (`coverage_status`) |
| `No aplicable` | `no evaluable` | cualquiera | exclusión | ruta D: `not_applicable` |
| `No evaluable` | `no evaluable` | cualquiera | no decidible | ruta D: `not_assessable` |

**Dictamen de TV-03 / R-08 (mantenido).** La conversión `Presente–opuesto` + `patrón humano` + `explicit labels` → `pattern_human` + `opposed` **no es segura**. Requiere asumir que el autor histórico usó el polo IA como referencia, lo que retroactivamente impone la convención AI-first de `v0.3.0` sobre una fuente que no la declara. R-08 mantiene la cuarentena (`CE-035`). En la ruta F estándar, el caso equivalente se expresa con `Contraevidencia real` y un span propio; si el valor es el polo humano registrado, se convierte como `opposed` con `reference_pattern_id`=patrón humano y sin diagnóstico de bloqueo, sin depender de un estado histórico. **`CE-021` queda reservado exclusivamente a la cuarentena de R-04**; la conversión de R-40 no lo emite.

### 9.8 Ruta F estándar: tabla de decisión por tipo

| Tipo (`measurement_type_source`) | Nº | Valor → patrón | Alineación por defecto | Contraevidencia |
|---|---:|---|---|---|
| `scale 1–5` | 14 | no hay mapeo de opción; patrón `overall_feature` | `not_assessed` salvo token direccional explícito | solo con ancla; si no, cuarentena |
| `ordinal mean` | 5 | idem | idem | idem |
| `categorical` | 3 | mapeo por etiqueta de opción | `aligned`/`opposed` según patrón | patrón opuesto registrado |
| `categorical option` | 4 | mapeo por etiqueta de opción | `aligned` si es la referencia; si no, `not_assessed` | `opposed` con valor alternativo explícito |
| `multi-select option` | 3 | presencia de la opción de referencia | `aligned` si está presente; coexistencia no es oposición | no se deriva de la ausencia |
| `binary option` | 1 | `yes`/`no` explícito | `aligned` si es la referencia; `no` puede ser `opposed` | `no` explícito con span y justificación |

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

**Ruta D vs ruta F.** En ruta D, `Presente–opuesto` se preserva como contraevidencia de dimensión y no se convierte. En ruta F, la contraevidencia se expresa con `Contraevidencia real` y un registro propio. En ruta F+, se aplican R-07/R-08/R-09/R-10.

### 10.5 Diferencias según el tipo de característica

Derivadas de §6.5 y del CSV, no de una regla genérica.

| Tipo (`measurement_type_source`) | Nº | Regla de oposición |
|---|---:|---|
| `scale 1–5` | 14 | No se inventan puntos de corte. `opposed` exige ancla o constructo opuesto identificable y justificación cualitativa. Un valor intermedio no es opuesto. |
| `ordinal mean` | 5 | Igual que escala. La distancia a la media grupal no demuestra oposición. |
| `categorical` | 3 | Las tres son bidireccionales con dos opciones elevadas; `opposed` solo cuando el valor observado es el polo opuesto real y verificable. En F+, `Presente–opuesto` + `patrón humano` no es convertible sin asumir referencia AI-first (R-08). |
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

**Sublocalizador.** Una fila puede generar más de un `EvidenceRecord` (p. ej., una observación principal y una contraevidencia, o varias opciones observadas con spans separados). Para distinguirlas se añade:

```text
<legacy_locator>:obs:<n>
```

donde `n` es el índice 1-based de la observación dentro de la fila, ordenado por una regla determinista:

1. observación principal (valor observado) primero;
2. contraevidencia afirmativa a continuación;
3. explicaciones alternativas u observaciones adicionales después;
4. en caso de empate, orden de aparición en el texto fuente.

La clave de unicidad es `(source_document_sha256, legacy_sublocator)`. Si dos observaciones de una misma fila no pueden distinguirse de forma determinista, el caso se preserva o se envía a revisión (`CE-037`); no se emite un registro ambiguo.

### 11.3 Identidad frente a contenido

- El localizador incluye `row_index`. Por tanto, **dos filas físicamente distintas con texto idéntico tienen localizadores distintos** y son observaciones distintas.
- **No se deduplica por contenido.** Dos observaciones idénticas pueden ser independientes (p. ej., el mismo rasgo descrito en dos escenas distintas).
- Se deduplica solo la **repetición exacta de la misma localización fuente** (mismo `section`, `row_index`, `feature_name_slug` y `sublocator`), que indica una reextracción de la misma fila, no dos filas.
- Las filas distintas con contenido idéntico se preservan ambas y se marcan con `CE-038` como posible duplicado, sin eliminarlas.
- Si dos filas comparten localización pero difieren en contenido, ambas van a cuarentena (`CE-016`); el exportador no adjudica la contradicción.

### 11.4 Registro de procedencia (en el informe de exportación)

Por cada registro emitido se conserva:

| Campo | Fuente |
|---|---|
| `source_document_path`, `source_document_sha256`, `source_git_tag`, `source_git_commit` | cálculo del exportador |
| `legacy_locator`, `legacy_sublocator` | §11.2 |
| `legacy_state_raw`, `legacy_direction_raw`, `legacy_strength_raw` | tokens literales |
| `legacy_feature_name`, `legacy_cluster_name`, `legacy_dimension_name` | texto literal |
| `legacy_observation_text`, `legacy_justification`, `legacy_alternative`, `legacy_counterevidence`, `legacy_study_direction` | texto literal |
| `legacy_quotation_or_location` | texto literal |
| `source_format_id`, `source_skill_version` | §4 |
| `feature_registry_version`, `feature_registry_sha256` | §4 |
| `export_contract_version` | §4 |
| `record_id` | salida |

El `origin_detail` de cada `EvidenceRecord` **puede** incluir la clave `legacy_locator` como metadato de procedencia, pero la fuente de verdad es el informe. No se añaden campos nuevos a `EvidenceRecord`.

### 11.5 Citas

- `quote` debe ser subcadena literal del texto fuente (§5.4).
- `start_char` / `end_char` se calculan sobre el texto UTF-8 decodificado sin normalización.
- Si la cita aparece una sola vez, el exportador puede resolver offsets; si aparece varias veces, exige desambiguación; si no aparece, la fila va a cuarentena (`CE-031`).
- Una «ubicación» sin cita literal (p. ej. «párrafo 3») no satisface la regla 5 de §5.3 y no permite `observed`.
- **La contraevidencia no reutiliza la cita de la observación principal por defecto.** Debe tener su propio span literal y su propia justificación. Si el informe solo repite la cita principal, se cuarentena (`CE-039`).

### 11.6 Procedencia histórica frente a atestación de migración

`v0.2.3` no registra `observation_origin`. El destino lo exige. Se distinguen cuatro situaciones:

1. **Procedencia histórica demostrada** (p. ej., la Skill declara análisis humano cualitativo con protocolo versionado): se establece `observation_origin=human_annotation` y se documenta la base.
2. **Información proporcionada por un tercero** (herramienta independiente, modelo externo autorizado): se establece el valor correspondiente y se registra el método.
3. **Atestación declarada por el operador durante la migración**: se registra en `migration_attestations` del informe externo (responsable seudonimizado, fecha UTC, fundamento textual, versión de protocolo, estado de autorización). El valor de `observation_origin` refleja la atestación, pero la fuente de verdad de la atestación es el informe externo, no el dominio.
4. **Procedencia desconocida**: no se puede demostrar ni atestar válidamente → bloqueo de conversión (R-29/R-37, `CE-032`/`CE-036`).

No se crean nuevos enums en el dominio. La atestación es un mecanismo de procesamiento externo con su propia procedencia, coherente con la cuarentena (§14).

**Validez de la atestación.** Una entrada de `migration_attestations` es válida solo si cumple todos los siguientes:

| Campo | Condición |
|---|---|
| `legacy_locator` | no vacío y coincidente con el localizador compuesto de la observación migrada (§11.2) |
| `legacy_sublocator` | no vacío y coincidente con el sublocalizador de la observación migrada |
| `attested_origin` | uno de `human_annotation`, `external_model`, `independent_tool`, `authorized_experiment` |
| `attested_by` | identificador seudonimizado no vacío |
| `attested_at_utc` | fecha/hora ISO 8601 en UTC |
| `basis` | fundamento textual no vacío |
| `protocol_version` | versión no vacía |
| `authorization_status` | `authorized` para habilitar M-55; `not_authorized` invalida la entrada; `not_applicable` carece de criterio documentado y se conserva como decisión pendiente (no se infiere autorización) |

`migration_attestations` es la fuente externa de verdad de la atestación. El dominio solo refleja `attested_origin` en `EvidenceRecord.observation_origin`; no lo sustituye.

**Concordancia entre vías.** Si coexisten declaración directa y atestación válida, sus valores de procedencia deben coincidir. Una discrepancia no se resuelve silenciosamente: se rechaza la ejecución (`CE-032`). Si solo una vía está presente y es válida, se acepta. Si ninguna está presente o es válida, se rechaza (R-29/R-37).

**Correspondencia por observación.** Una atestación solo autoriza la observación a la que apuntan sus localizadores:

1. El localizador compuesto esperado se determina según §11.2 a partir de `(source_document_sha256, section, row_index, feature_name_slug)`.
2. El sublocalizador esperado se determina añadiendo `:obs:<n>` según la regla determinista de §11.2.
3. La coincidencia se comprueba por igualdad exacta de `legacy_locator` y `legacy_sublocator` con los valores esperados de la observación.
4. Si una atestación apunta a otra observación, no habilita la actual: se ignora para R-29 de esta observación (no se produce autorización cruzada).
5. Si existen varias atestaciones en la misma ejecución, cada una solo autoriza la observación cuyos localizadores coinciden.
6. Una atestación válida correspondiente a una fila no autoriza automáticamente otras filas, aunque compartan contenido.

M-55 sigue siendo condición run-level; la autorización efectiva de procedencia se evalúa por observación. No se convierte en fila de característica ni genera `EvidenceRecord`.

**M-55 no genera `EvidenceRecord` por sí misma.** Es una condición de procedencia **a nivel de ejecución**: habilita el establecimiento de `EvidenceRecord.observation_origin` en las filas completas que ya cumplen los demás requisitos (estado, valor explícito, span, versión de Registry). `migration_attestations` conserva la atestación externa y sigue siendo su fuente de verdad; el dominio solo refleja el valor, no lo sustituye. Sin atestación válida, M-55 no habilita la conversión y se aplican R-29/R-37 (`CE-032`/`CE-036`).

---

## 12. Idempotencia

Condiciones para que dos exportaciones de la misma fuente produzcan el mismo resultado lógico:

1. Mismo `source_document_sha256`.
2. Mismo `export_contract_version`.
3. Mismo `feature_registry_version` (y mismo digest de registro).
4. Mismas opciones de exportación declaradas.
5. Mismo texto fuente disponible para verificación.

Garantías exigidas:

- **Clave de unicidad:** `(source_document_sha256, legacy_sublocator)`. Dos extracciones de la **misma localización fuente** no producen dos registros (R-31). Dos filas distintas con el mismo texto **sí** producen dos registros (R-31b).
- **`record_id` estable:** el exportador debe producir el mismo `record_id` para la misma clave y versiones, sea por derivación determinista o por mapeo persistido. La elección se documenta en la implementación; el contrato solo exige estabilidad.
- **`analysis_id` estable:** reexportar la misma fuente con los mismos parámetros es la misma ejecución lógica; no se crea una ejecución nueva.
- **Sin acumulación:** la salida es función de la entrada, no del estado previo. Reexportar no añade registros a los anteriores.
- **Orden determinista:** si el formato de salida serializa listas, el orden debe ser estable (p. ej. por `legacy_sublocator`). El contrato no impone un orden concreto, solo su estabilidad.
- **Independencia del sistema de archivos:** el resultado no depende del orden de iteración, de la fecha de ejecución ni de un contador global.

**Demostración de no colisión.** Para una fila con dos observaciones independientes, la clave es `(digest, locator:obs:1)` y `(digest, locator:obs:2)`; son distintas. Para dos filas distintas con el mismo texto, los locators difieren en `row_index`; las claves son distintas y no se deduplican. Para una reextracción de la misma fila, la clave es idéntica y se deduplica. Los vectores TV-47…TV-50 y TV-57…TV-60 fijan estos casos.

Una exportación que dependa de la fecha de ejecución, del orden de iteración del sistema de archivos o de un contador global **no cumple** este contrato.

---

## 13. Reversibilidad

Se distinguen cuatro clases, más `—` cuando no existe registro convertido. La clasificación se declara por fila en la matriz.

| Clase | Definición | Ejemplo |
|---|---|---|
| **A. Completamente reversible** | el estado o la observación se deriva del registro `v0.3.0` + registro de características, sin el informe | §4 con valor explícito y span; `observed` + `pattern_ai`/`pattern_human` + `aligned`; §4 con valor no registrado (`not_assessed`); `No aplicable`/`No evaluable` de §3 como `coverage_status` exacto |
| **B. Reversible solo con el original preservado** | el registro no basta; hace falta el token literal o el texto del informe | §3 con `Presente–alineado`/`Presente–opuesto`/`neutral`/`Ausente` (el `coverage_status` es más grueso que el estado); `Presente–opuesto` unidireccional en F+ (la dirección solo está en `legacy_raw`); `Fuerza` libre; contraevidencia preservada sin registro |
| **C. Irreversible** | no existe reconstrucción fiel ni con el original | ninguno dentro de este contrato |
| **D. Debe rechazarse** | no se emite registro | contradicciones; `feature_id` ausente; estado o dirección desconocidos; versión de registro irresoluble; procedencia no demostrable |
| **`—`. No aplica** | no existe registro convertido (cuarentena o bloqueo sin emisión; la reversibilidad de un registro inexistente no se evalúa) | M-04 (R-04 bloqueada); M-08 (`Presente–opuesto` bidireccional en cuarentena) |

**Por qué no hay clase C.** Toda fila convertida conserva en el informe sus tokens literales y su texto. Ninguna conversión descarta un valor sin dejarlo registrado. Si una conversión exigiera descartar información y no pudiera preservarla, el contrato la clasifica como D, no como C.

**Demostración de la clase A para §4.**

| Registro `v0.3.0` | Reconstrucción desde el dominio + registro |
|---|---|
| `observed` + `pattern_ai` + `aligned` + `reference_pattern_id`=referencia IA | valor = etiqueta del patrón; `Dirección del estudio` = AI; sin estado histórico (no existía en §4) |
| `observed` + `pattern_human` + `aligned` + `reference_pattern_id`=referencia humana | valor = etiqueta del patrón; `Dirección del estudio` = Human |
| `observed` + `pattern_human` + `opposed` + `reference_pattern_id`=patrón humano (bidireccional) | valor = etiqueta del patrón humano; `Dirección del estudio` = AI/Human; estado histórico no aplica en §4 estándar |
| `observed` + `not_assessed` + `reference_pattern_id=null` + `observed_value_text` | valor literal preservado; sin dirección |
| `observed` + `not_assessed` + `reference_pattern_id=null` + `observed_option_id=null` (opción no registrada) | valor literal preservado; `CE-022` |

**Demostración de la clase A para §3.**

| `coverage_status` | `legacy_state` reconstruible |
|---|---|
| `not_applicable` | `No aplicable` |
| `not_assessable` | `No evaluable` |
| `descriptive_assessed` | `Ausente` (si `completeness=completo`) o `Presente–alineado`/`Presente–opuesto`/`neutral` — **no distinguible sin el informe** |

Por eso `descriptive_assessed` es clase B cuando el estado original era `Ausente` o una variante de presente: el `coverage_status` no conserva el token. Solo `not_applicable` y `not_assessable` son clase A exactas.

**Corrección respecto de v0.2.** `Presente–opuesto` unidireccional en F+ es **clase B**, no A: el registro (`observed` + `not_assessed` + `opposed` + `reference_pattern_id=null`) reconstruye el estado, pero no el token de dirección (`patrón IA`/`patrón humano`), que solo vive en `legacy_raw`. La tabla anterior de v0.2 lo declaraba A sin incluirlo en la reconstrucción; la v0.3 lo corrige.

**Informe de pérdidas.** Se emite `loss_report` cuando:

- una fila se convierte a un estado distinto del histórico;
- un campo histórico no tiene destino (`Fuerza` libre, `Dirección del estudio` duplicada, estado/dirección de §3);
- una etiqueta histórica no se puede afirmar en el dominio (dirección no registrada);
- una fila se preserva sin conversión (dimensión sin `feature_id`);
- una fila se rechaza o se pone en cuarentena;
- una contraevidencia no puede emitirse por falta de span o justificación propios.

El informe de pérdidas **no** es un enum del dominio: es una lista de texto y referencias.

---

## 14. Diagnósticos y cuarentena

### 14.1 Espacio separado

Los diagnósticos viven **solo** en `compatibility_export_report.json`. No se escriben en `EvidenceRecord`, `ClusterSummary` ni `AnalysisRun`. No se crea un enum de estados de error en el dominio.

### 14.2 Códigos

| Código | Significado | Acción |
|---|---|---|
| `CE-001` | estado histórico desconocido | rechazar fila |
| `CE-002` | dirección histórica desconocida | rechazar fila (solo F+); en ruta D se preserva (`CE-002` informativo) |
| `CE-003` | fila de característica sin `feature_id` | rechazar fila |
| `CE-004` | nombre de característica no resoluble | rechazar fila |
| `CE-005` | versión de Feature Registry inexistente | rechazar ejecución |
| `CE-006` | referencia histórica no resoluble | rechazar fila |
| `CE-007` | estado y dirección incompatibles | rechazar fila |
| `CE-008` | `Presente–alineado` contra la referencia en unidireccional | rechazar fila |
| `CE-009` | `Presente–opuesto` o contraevidencia sin span | cuarentena |
| `CE-010` | `Presente–opuesto` o contraevidencia sin justificación | cuarentena |
| `CE-011` | oposición en escala sin ancla | cuarentena |
| `CE-012` | ausencia de opción de referencia tratada como oposición en multiselección | rechazar conversión |
| `CE-013` | `Ausente` sin oportunidad suficiente | ruta D: `partially_assessed`/`not_assessable` |
| `CE-014` | valor agregado en registro atómico | cuarentena |
| `CE-015` | etiqueta global sin campo de dominio | preservar |
| `CE-016` | duplicado en la misma localización fuente | deduplicar o cuarentena |
| `CE-017` | clúster no resoluble | `cluster_id=null` |
| `CE-018` | dimensión no resoluble | rechazar fila |
| `CE-019` | falta `status_reason` o motivo de dimensión | cuarentena |
| `CE-020` | variante `neutral` de estado | convertir con bandera |
| `CE-021` | bidireccional alineada al polo humano (R-04) | **bloqueo**: cuarentena |
| `CE-022` | opción observada no registrada | `observed_option_id=null` |
| `CE-023` | fuerza no mapeable | `not_rated` |
| `CE-024` | falta digest de la fuente | rechazar ejecución |
| `CE-025` | fila parcial o estado/valor ausente | rechazar fila |
| `CE-026` | dirección histórica no registrada | convertir con bandera |
| `CE-027` | `neutro` con lectura ambigua | rechazar fila |
| `CE-028` | etiqueta de adecuación sin enum de destino | preservar |
| `CE-029` | fila de dimensión sin característica | preservar |
| `CE-030` | `ambivalent/mixed` leído como dirección `mixto` | corregir; informativo |
| `CE-031` | cita no literal | cuarentena |
| `CE-032` | procedencia ausente: ni declaración directa válida ni atestación válida (o discrepancia entre ambas) | rechazar ejecución |
| `CE-033` | texto fuente no disponible | rechazar ejecución |
| `CE-034` | asimetría de oportunidad | revisión manual |
| `CE-035` | `Presente–opuesto` en bidireccional no resoluble sin asumir referencia AI-first | cuarentena |
| `CE-036` | procedencia histórica no demostrable ni atestable | rechazar fila/ejecución |
| `CE-037` | sublocalizador incapaz de distinguir observaciones de una misma fila | preservar o revisar |
| `CE-038` | filas distintas con contenido idéntico (posible duplicado) | preservar ambas; informativo |
| `CE-039` | contraevidencia reutiliza la cita principal sin justificación independiente | cuarentena |
| `CE-040` | `Ausente` preservado como `coverage_status` (sin `not_observed`) | informativo |
| `CE-041` | valor de escala sin token direccional explícito | `not_assessed`; informativo |

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

**En ruta F estándar**, la ausencia de dirección no es `neutral`: es `not_assessed`. `neutral` exige una neutralización contextual explícita, que §4 no registra. Por eso R-42 usa `not_assessed` por defecto y no `neutral`.

### 15.2 Fuerza

La fuente histórica utiliza un campo libre (`Fuerza`), no un vocabulario completamente controlado.

- Mapear a `weak` / `moderate` / `strong` **únicamente** cuando exista una regla documentada que vincule el token histórico con el valor controlado.
- En cualquier otro caso: `evidence_strength=not_rated` y conservación del valor literal en `legacy_raw` (`CE-023`).
- **No** confundir `legacy_strength` con `assessment_confidence`. El primero es intensidad cualitativa de la evidencia; el segundo es confianza en la calidad de la lectura. Son campos distintos y no se derivan uno del otro.
- `assessment_confidence` se escribe `not_rated` por defecto en la exportación de compatibilidad; nunca se copia `analysis_quality_confidence`.

### 15.3 Otras opciones

`ambivalent/mixed` sigue siendo una opción de característica (`Moral Polarity Toward Protagonist`), no una dirección global. No confundirlo con `mixed` en agregados (`ClusterSummary`/`AnalysisRun`).

---

## 16. Dependencias metodológicas

Clasificación exigida por la fase: reglas cerradas, decisiones pendientes, guía incompleta y datos faltantes.

### 16.1 Reglas que ya pueden cerrarse

- Vocabulario de 5 estados y 5 direcciones (§7.1, §7.2).
- Separación de rutas §3/§4 y prohibición de join (§8).
- Ruta F derivada de valor + span (§9.4).
- Ausencia frente a opción categórica explícita (`evidence-status.md`, sección final; §5.3.4).
- Contraevidencia requiere cita y justificación propias (`evidence-status.md`, «Contraevidencia»; §11.5).
- Simetría de oportunidad (§9.6).
- Ausencia no tiene dirección (`evidence-status.md`; §5.3, regla 4).
- Resolución A2 y `reference_relation` (§10).
- Reglas por tipo de característica (§9.8, §10.5).
- Verificación literal de citas y offsets (§5.4).
- `mixed` solo en agregados (§5.3.3).
- Identidad por localización fuente y no por contenido (§11.3, §12).

### 16.2 Decisiones metodológicas necesarias

| Decisión | Estado | Efecto si no se cierra |
|---|---|---|
| Confirmar que `Presente–alineado` + polo humano en bidireccional se reexpresa como `opposed` en A2 | **BLOQUEADA**; R-04 no se adopta | R-04 queda en cuarentena (`CE-021`) |
| Confirmar que la variante `neutral` es dirección `neutro`, no sexto estado | adoptada; requiere confirmación | R-17 quedaría en cuarentena |
| Contenido mínimo de la justificación para `opposed` en escalas | abierta | R-10/R-F07 no pueden aplicarse |
| Contenido mínimo de `status_reason` para `No aplicable` / `No evaluable` | abierta | R-15/R-16 no pueden aplicarse |
| Vocabulario controlado de `Fuerza` | abierta | R-32 emite `not_rated` |
| Existencia y forma del campo de alineación global en `AnalysisRun` | abierta (hueco del contrato de destino) | R-20/R-21 preservan sin escribir |
| Criterio inequívoco para elegir lectura a vs b de `neutro` | abierta | R-17 produce rechazo |
| Procedencia histórica vs atestación de migración | parcialmente resuelta (§11.6) | R-29/R-37 bloquean |
| Alineación derivable de valores `overall_feature` sin token explícito | **cerrada en negativo**: no se deriva | R-42 usa `not_assessed` |

### 16.3 Reglas que requieren completar la guía de anotación

- Selección y delimitación de spans.
- Frontera entre evidencia afirmativa y contraevidencia.
- Resolución de evidencia mixta en el mismo clúster.
- Resolución de múltiples polos en una misma característica.
- Procedimiento de adjudicación de contradicciones.
- Registro de dos observaciones opuestas dentro de una misma característica.
- Criterio de neutralidad contextual (lectura a vs b).
- Vocabulario controlado de `Fuerza`.
- Justificación semántica de R-04.

### 16.4 Reglas que requieren más datos de origen

- Frecuencia real de cada estado en anotaciones históricas: **no calculable**; el repositorio no contiene corpus.
- Variantes textuales reales de los tokens: solo se conocen las documentadas.
- Catálogo completo de opciones del instrumento: ausente; limita `observed_option_id` a los 33 patrones registrados.
- Existencia de offsets en anotaciones históricas: no consta.

### 16.5 Orden de cierre recomendado

1. Definir el campo de alineación global de `AnalysisRun` y el enum de `adequacy` (bloquea R-20/R-21).
2. Completar la guía en spans, justificación y evidencia mixta (bloquea R-10, R-15, R-16, R-F03, R-F07).
3. Fijar el vocabulario de `Fuerza` (bloquea R-32).
4. Fijar el criterio de neutralidad (bloquea R-17 lectura a/b).
5. Justificar o descartar R-04 (bloquea `CE-021`).
6. Implementar el exportador contra este contrato y los vectores.
7. Abordar la adaptación al español como fase independiente.

---

## 17. Límites y bloqueos conocidos

### 17.1 Límites del contrato

- No convierte texto libre en etiquetas: solo convierte etiquetas documentadas.
- No valida la calidad científica de la anotación original.
- No reconstruye datos que `v0.2.3` no registró.
- No garantiza round-trip sin el informe de exportación (clase B).
- No sustituye la auditoría semántica de §6.2.
- No autoriza scoring, probabilidad de autoría ni inferencia automática.
- No produce `not_observed`, `not_applicable` ni `not_evaluable` desde §3 (§8.3).

### 17.2 Bloqueos del contrato de destino

**B1. `AnalysisRun` no tiene campo de alineación global.** §5.3.3 declara `mixed` válido en `AnalysisRun`, pero §5.2 no enumera ningún campo que lo transporte (`report_summary` aparece en §5.1 sin forma definida). Hasta que se defina, la etiqueta global se preserva en el informe y, si procede, se expresa en `ClusterSummary.alignment` solo con síntesis explícita.

**B2. `AnalysisRun.adequacy` no tiene enum documentado.** §5.2 exige «estado, motivos y reglas aplicadas», pero no fija valores. La etiqueta histórica `evidencia insuficiente` y la puerta de adecuación se preservan; no se escriben como valores de enum inventados.

**B3. `observed_option_id` depende del catálogo de opciones.** El Feature Registry contiene 33 patrones de referencia, no el catálogo completo del instrumento. Las opciones no elevadas no tienen ID y se registran como `observed_value_text`.

**B4. `observation_origin` es obligatorio y no tiene fuente histórica.** Requiere declaración explícita del operador o atestación de migración (§11.6). Sin ella, la ejecución se rechaza.

**B5. `review_status` tiene enums distintos en §5.2 y §5.3.** `AnalysisRun` usa `not_reviewed`/`machine_audited`/`human_reviewed`/`adjudicated`; `EvidenceRecord` usa `unreviewed`/`accepted`/`revised`/`rejected`. El exportador usa el enum correspondiente a cada objeto y no los mezcla. La divergencia se registra como hueco del contrato de destino, no se corrige aquí.

### 17.3 Bloqueos científicos (no resueltos aquí)

- Adaptación al español exploratoria y no validada.
- Sin corpus histórico de anotaciones.
- Sin acceso al corpus original ni a los pesos del paper.

---

## 18. Criterios de conformidad

Una exportación cumple este contrato si y solo si:

1. Cada fila de entrada tiene un resultado explícito de las cinco clases y una ruta declarada (`D`, `F` o `F+`).
2. Ninguna fila §3 genera `EvidenceRecord`.
3. Ningún `EvidenceRecord` de §4 hereda `legacy_state` o `legacy_direction` de §3.
4. Todo registro emitido tiene `record_id`, `feature_id`, `dimension_id`, `observation_origin`, `source_spans` y `cluster_id`.
5. Todo `observed` tiene al menos un `source_span` literal verificado.
6. Toda contraevidencia tiene su propio span y su propia justificación; no reutiliza la cita principal.
7. Todo `opposed` cumple `INV-A2-10` o `INV-A2-11`.
8. Ningún `EvidenceRecord` contiene `mixed`, `historical_reference_pattern_id` ni códigos `CE-*`.
9. `reference_relation` solo usa `aligned`, `opposed`, `not_assessed`.
10. La referencia histórica se resuelve desde el registro y no se duplica.
11. Dos exportaciones de la misma fuente con los mismos parámetros producen los mismos `record_id` y el mismo conjunto lógico de registros, con clave `(source_document_sha256, legacy_sublocator)`.
12. Las filas distintas con contenido idéntico se preservan ambas y se marcan con `CE-038`; no se deduplican.
13. El informe de exportación contiene `legacy_raw` de toda fila emitida, preservada, en cuarentena o rechazada.
14. El informe de pérdidas cubre toda conversión que cambie el estado o descarte un campo.
15. No se modificó ningún archivo de `v0.2.3`, del Feature Registry, del Charter ni de la Spec.
16. La etiqueta global y `analysis_quality_confidence` se preservan en el informe externo, sin escritura en el dominio.
17. Toda atestación de migración queda registrada en `migration_attestations`.
18. R-04 no se aplica como conversión: cualquier caso se cuarentena (`CE-021`).

Los vectores que demuestran estos criterios están en `COMPATIBILITY_TEST_VECTORS_v0.3.md`.

---

*Predecesores preservados: `COMPATIBILITY_EXPORT_CONTRACT_v0.1.md` y `COMPATIBILITY_EXPORT_CONTRACT_v0.2.md`. Cambios sustantivos de v0.2 a v0.3: rutas D/F/F+ separadas (§8, §9); §4 no exige ni hereda estado/dirección; `not_observed`/`not_applicable`/`not_evaluable` no se emiten desde §3; idempotencia por localización fuente y no por contenido (§11.3, §12); `Presente–opuesto` unidireccional reclasificado a clase B (§13); R-04 bloqueada (§9.3, §16.2); nuevos diagnósticos CE-038/CE-039/CE-040/CE-041; export_contract_version 0.2.0 → 0.3.0.*
