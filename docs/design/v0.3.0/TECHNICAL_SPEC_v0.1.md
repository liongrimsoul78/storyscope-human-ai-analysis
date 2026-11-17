# StoryScope Evidence Engine — Technical Specification v0.1

**Proyecto:** StoryScope Human–AI Analysis  
**Versión objetivo del motor:** `0.3.0`  
**Versión de esta especificación:** `0.1`  
**Fecha:** 12 de noviembre de 2026  
**Estado:** diseño técnico propuesto para implementación; no describe código ya implementado.  
**Baseline que se preserva:** Skill `v0.2.3`, release/tag público `v0.2.3`.

---

## 0. Decisión ejecutiva

La primera versión del motor será un **motor determinista de estructuración, validación, auditoría y representación de evidencia narrativa**. El modelo lingüístico propone observaciones; el registro de características, los validadores y las reglas metodológicas controlan qué puede entrar en un informe.

El sistema no será un clasificador de autoría, no intentará reproducir el clasificador oficial de StoryScope y no calculará probabilidades de procedencia humana o IA.

La salida primaria será un expediente JSON versionado, complementado por un informe Markdown. Cada observación importante deberá poder rastrearse hasta una característica del registro metodológico y a uno o más fragmentos exactos del texto original.

### Decisiones aprobadas para el diseño

1. Mantener la Skill pública `v0.2.3` intacta como baseline.
2. Incorporar el motor en el repositorio actual bajo un límite explícito `engine/`; no crear todavía un segundo repositorio.
3. Mantener StoryScope independiente de planos de control y proyectos externos. La integración futura, si se justifica, será un adaptador periférico.
4. Empezar con Python y biblioteca estándar para el runtime del motor.
5. Usar contratos JSON versionados y JSON Schema Draft 2020-12 para interoperabilidad; la validación de relaciones y citas exige además verificaciones semánticas propias.
6. Mantener el análisis narrativo descriptivo de las diez dimensiones separado de las 30 características centrales y de sus 33 comprobaciones de opción.
7. Separar el estado de observación de la alineación investigativa. Esto corrige una ambigüedad del modelo conceptual heredado sin reescribir la Skill `v0.2.3`.
8. La segunda pasada será una auditoría de calidad, no un juez independiente ni una prueba de verdad. La revisión humana sigue siendo el ancla de evaluación.
9. El modelo A2 adopta `reference_pattern_id`, `historical_reference_pattern_id` (exclusivo del registro) y `reference_relation` (`aligned`, `opposed`, `not_assessed`) para conservar Presente–opuesto sin duplicar la referencia histórica en `EvidenceRecord`.
9. No persistir el texto completo, no transmitirlo a servicios externos y no guardar su hash por defecto.
11. No incorporar todavía bot, aplicación web, base vectorial, framework multiagente, proveedor LLM obligatorio ni integración con planos de control externos.

## 1. Estado de partida y límites del conocimiento

### 1.1 Baseline de la Skill

La release pública `v0.2.3` contiene una metodología cualitativa independiente inspirada en la investigación StoryScope. Incluye:

- diez dimensiones narrativas como marco de organización;
- treinta características centrales en el mapa de StoryScope;
- treinta y tres comprobaciones/opciones a nivel de característica;
- ocho clústeres operativos propios de StoryScope para evitar doble conteo;
- cinco estados heredados de evidencia;
- etiquetas direccionales cualitativas;
- salvaguardas para textos breves, géneros no comparables, adaptación al español, ausencia como evidencia, privacidad y no atribución concluyente.

La Skill no contiene la taxonomía oficial completa de 304 características, el corpus original, pesos, el clasificador XGBoost ni el pipeline de extracción oficial. Los resultados publicados por el clasificador del artículo no son métricas del motor de StoryScope.

### 1.2 Precisión relevante sobre las 30 características

Las 30 características de `feature-dimension-map.csv` no son una implementación de las 304 características de la taxonomía original. El mapa actual asigna las características centrales a los códigos de dimensión presentes en el CSV. No debe suponerse que las 30 cubren por igual las diez dimensiones.

En particular, la capa descriptiva puede perfilar las diez dimensiones; la capa de patrones centrales solo puede aplicar las características y opciones realmente presentes en el registro de 30/33. Las dimensiones sin una característica central mapeada no reciben señales direccionales inventadas.

### 1.3 Niveles de evidencia

En los documentos y el producto deberán distinguirse siempre:

- **Hecho de fuente:** publicado en el artículo o contenido de la release estable.
- **Dato del baseline:** transcrito y validado por StoryScope contra la fuente publicada.
- **Decisión de ingeniería:** contrato elegido para hacer implementable el motor.
- **Hipótesis experimental:** idea que todavía requiere medición.
- **Resultado medido:** salida de una prueba ejecutada, con versión, datos y condiciones registrados.

Una especificación o un árbol propuesto no deben describirse como implementados.

### 1.4 Falsos positivos y límites de inferencia

- Un texto escrito por una persona puede presentar características asociadas con patrones observados en textos de IA.
- Una característica aislada no permite determinar la autoría.
- La edición profesional, la traducción, la corrección gramatical, las restricciones de género y el estilo pueden modificar las señales observables.
- El sistema no garantiza detectar todos los textos generados por IA.
- El sistema tampoco garantiza evitar clasificar erróneamente textos humanos.
- Los resultados son análisis descriptivos y exploratorios, no pruebas de autoría.
- StoryScope no debe utilizarse como fundamento único de calificación académica, sanción disciplinaria, contratación, decisiones legales ni procedimientos forenses.
- No se fijan tasas de falsos positivos sin un protocolo de evaluación y datos autorizados.

## 2. Objetivo funcional de v0.3.0

Dado un texto suministrado o autorizado y un paquete de observaciones estructuradas, el motor debe:

1. evaluar la adecuación de la entrada;
2. registrar contexto y condiciones conocidas sin completar datos desconocidos;
3. aceptar observaciones ligadas al registro canónico de características;
4. comprobar que cada cita coincide exactamente con el texto fuente;
5. impedir estados, opciones, dimensiones y clústeres inválidos;
6. impedir que una ausencia se convierta en dirección de autoría;
7. agrupar observaciones relacionadas sin sumar votos;
8. auditar afirmaciones no sustentadas y contraevidencia omitida;
9. producir un informe legible y un expediente JSON reproducible en cuanto a método y configuración.

El motor debe seguir siendo útil sin una conexión de red y sin un proveedor de modelos instalado. En v0.3.0, OpenCode puede actuar como entorno que solicita la extracción al modelo; el motor recibe el resultado estructurado y lo valida. El paquete Python no necesitará un SDK de OpenAI, Ollama u otro proveedor.

### 2.1 Narrative Extractor: componente lógico e implementación externa

La arquitectura distingue dos planos:

- **Narrative Extractor como componente lógico:** representa el punto donde se producen o reciben observaciones narrativas candidatas. Permanece en la arquitectura como interfaz o punto de integración.
- **Implementación concreta de la extracción:** en v0.3.0 el motor no implementa ni aloja un modelo generativo propio. Las observaciones pueden proceder de anotación humana, un modelo externo, herramientas de análisis independientes o procesos experimentales autorizados.

La responsabilidad del motor es validar, estructurar, registrar, relacionar, auditar y reportar esas observaciones. El origen de cada observación debe quedar registrado en sus metadatos. La extracción de observaciones y la interpretación científica permanecen separadas. No se envían textos a servicios externos sin autorización explícita.

## 3. Alcance y exclusiones

### Incluido en v0.3.0

- Input & Context Gate.
- Narrative Extractor como interfaz lógica y contrato de entrada estructurada; no como generador implementado.
- Registro canónico de 30 características y 33 patrones/opciones publicados en el baseline.
- Perfil descriptivo de las diez dimensiones, marcando explícitamente cobertura descriptiva y cobertura de patrones.
- Evidence Ledger con referencias textuales exactas.
- Validador de citas y offsets.
- Control de estados, opciones, dirección, oportunidad de observación y clústeres.
- Detección de candidatos a doble conteo.
- Auditoría determinista y auditoría semántica asistida por modelo, claramente diferenciadas.
- Renderizado de Markdown y exportación JSON.
- CLI local mínima para validar, auditar y renderizar.
- Fixtures de regresión y CI para Windows y Ubuntu siguiendo el patrón compatible con el repo.

### Excluido de v0.3.0

- Clasificador supervisado de autoría.
- Probabilidad, puntuación global, umbral de IA/humano o mayoría de votos.
- Reimplementación de los 304 features oficiales.
- Entrenamiento o fine-tuning de modelos.
- Implementación de un modelo generativo propio dentro del motor.
- Servicio web, API de red, Telegram, bot, interfaz gráfica o cuenta multiusuario.
- Base de datos operacional, vector database, memoria persistente de historias o almacenamiento de corpus.
- MCP obligatorio.
- Integración directa con planos de control o servicios de otros proyectos.
- Atribución de fragmentos humano/IA sin procedencia documental.
- Validación científica equivalente al inglés para español u otros idiomas.

## 4. Arquitectura de ejecución

```text
Texto autorizado (memoria de proceso; no se persiste por defecto)
                 |
                 v
        1. Input & Context Gate
                 |
                 v
  2. Extraction Contract (propuesta del modelo
     o anotación humana; JSON estructurado)
                 |
                 v
  3. Evidence Ledger + Feature Registry
                 |
                 v
  4. Deterministic Validation
     - esquema y enums
     - registro y opciones
     - citas exactas y offsets
     - oportunidad de observación
     - límites y política de ausencia
                 |
                 v
  5. Cluster / Double-count Resolver
                 |
                 v
  6. Semantic Evidence Audit (flags; no auto-corrección)
                 |
                 v
  7. Report Renderer
                 |
        +--------+--------+
        |                 |
        v                 v
  analysis.json       report.md
```

Los siete pasos del diagrama son responsabilidades de procesamiento, no necesariamente etapas secuenciales rígidas. `Run Metadata` es información transversal de la ejecución (§5.2), no un paso independiente.

### 4.1 Input & Context Gate

Registra, como mínimo:

- idioma mediante código BCP-47 cuando se conozca;
- variedad declarada o `not_specified` / `not_determinable`;
- género y tipo de texto: narrativa, no ficción, híbrido, formato restringido u otro;
- longitud aproximada y método de conteo;
- estado del documento: completo, fragmento o desconocido;
- disponibilidad de consigna, prompt, audiencia y propósito;
- condiciones de producción declaradas: traducción, edición, dictado, plantilla, asistencia de IA y coautoría;
- estado de adecuación y razones.

Cada condición debe distinguir `yes`, `no`, `unknown` y `not_provided`. `not_provided` significa que el usuario no entregó ese dato; `unknown` significa que el dato fue considerado pero no se pudo determinar. No inferir variedad de idioma a partir de la ubicación del usuario ni de la ausencia de regionalismos.

#### Conteo reproducible

En v0.3.0 se usará `whitespace_tokens_v1`: número de elementos obtenidos mediante `text.split()`. Es un conteo operativo reproducible, no un tokenizador lingüístico ni un conteo morfológico. El informe lo denominará `recuento aproximado de palabras`.

Se conserva el guardrail vigente de StoryScope: menos de 500 palabras no permite etiqueta global direccional; los rangos 500–999 y 1.000+ se mantienen como reglas operativas, no como umbrales científicos del paper. Géneros breves o muy restringidos pueden seguir siendo inadecuados independientemente de la longitud.

### 4.2 Extraction Contract

El extractor propone observaciones; no escribe directamente la conclusión final. El contrato es una entrada estructurada: no implica que el motor implemente un extractor generativo propio. Para cada observación deberá proponer:

- `feature_id` canónico;
- `dimension_id`;
- `reference_pattern_id` cuando exista correspondencia con una de las 33 comprobaciones del registro;
- `observed_option_id` cuando exista una opción observable definida;
- descripción neutral de lo observado;
- estado de observación;
- alineación investigativa propuesta y su fundamento;
- citas/localizadores;
- oportunidad de observación;
- origen de la observacion (`observation_origin`) y metadatos de procedencia;
- explicación alternativa;
- contraevidencia pertinente;
- clúster y posible relación de doble conteo.

El extractor no debe inventar valores numéricos 1–5 para una historia comparándola con medias de grupo. Las medias, prevalencias y gaps de la Tabla 16 son estadísticas grupales y no umbrales individuales.

### 4.3 Feature Registry

El registro será la fuente canónica para IDs y metadatos de características. Se generará/curará a partir de los archivos publicados de referencia y se validará contra el CSV y `table16_expected.json` existentes.

Campos mínimos por característica:

- ID interno estable `ssha.feature.<slug>`;
- nombre canónico inglés y etiqueta de presentación española;
- código y nombre de dimensión del paper;
- ID de clúster operativo de StoryScope;
- tipo de medición del baseline;
- una o más referencias de patrón publicadas;
- opciones destacadas con ID estable cuando corresponda;
- cautela interpretativa y condiciones de aplicabilidad.

Reglas:

1. IDs internos inmutables una vez publicados; las etiquetas pueden evolucionar sin cambiar IDs.
2. No renombrar ni corregir valores científicos en el motor por intuición.
3. Preservar los 30 nombres, 33 opciones y nueve excepciones de redondeo comprobadas por v0.2.3.
4. Distinguir un `feature` de una `reference_pattern`/opción: dos opciones direccionales de una característica no son dos características independientes.
5. No presentar los ocho clústeres operativos de StoryScope como clústeres oficiales de la investigación original.

## 5. Contrato conceptual de datos

### 5.1 Analysis Bundle

El archivo canónico `analysis.json` contendrá:

```json
{
  "schema_version": "1.0.0",
  "run": {},
  "dimension_profiles": [],
  "evidence_records": [],
  "cluster_summaries": [],
  "audit": {},
  "report_summary": {}
}
```

El texto original no forma parte de este bundle. La fuente se proporciona al validador cuando se necesita verificar citas.

### 5.2 AnalysisRun

Campos obligatorios:

- `analysis_id`: UUID.
- `engine_name`, `engine_version`.
- `schema_version`.
- `methodology_name`, `methodology_version`.
- `skill_version`.
- `feature_registry_version`, `cluster_map_version`, `prompt_pack_version`.
- `created_at_utc` en ISO 8601 UTC.
- `source_metadata`: recuento de caracteres, recuento aproximado, método, completitud y hash opcional.
- `context`: idioma, variedad, género, tipo de texto y condiciones de producción declaradas.
- `adequacy`: estado, motivos y reglas aplicadas.
- `model_metadata`: nullable; proveedor, modelo, revisión y parámetros no sensibles, si se usó un LLM.
- `review_status`: `not_reviewed`, `machine_audited`, `human_reviewed`, `adjudicated`.

No almacenar:

- texto completo;
- ruta local del archivo fuente;
- nombre real, correo o identificador personal del autor salvo necesidad expresamente autorizada;
- API keys, tokens, cabeceras o secretos;
- prompts privados completos en metadatos públicos.

`source_sha256` será opt-in. Por defecto `null`/omitido. Un hash no anonimiza un texto y puede permitir confirmar textos conocidos.

### 5.3 EvidenceRecord: decisión central del modelo de evidencia

Un `EvidenceRecord` es un hallazgo atómico sobre una característica/opción y una evidencia textual. Una característica puede tener varios registros cuando hay opciones, pasajes o direcciones diferentes. Los registros relacionados deben vincularse para no inflar la evidencia.

Campos:

- `record_id`: UUID estable dentro del bundle.
- `feature_id`: ID del Feature Registry.
- `dimension_id`: código de dimensión.
- `reference_pattern_id`: nullable; patrón específico en el registro de 33. Identifica exclusivamente el patrón con el que se alinea el registro.
- `reference_relation`: enum `aligned`, `opposed`, `not_assessed`. Relación de la observación con la referencia histórica de la característica. Se sitúa junto a `research_alignment` porque ambos responden a preguntas distintas:
  - `research_alignment` responde si la observación se alinea con un patrón IA o humano registrado;
  - `reference_relation` responde si la observación está en el polo de referencia histórica, en el polo opuesto o sin relación direccional asignada.
- `observed_option_id`: nullable; opción identificada por el registro.
- `observation_status`:
  - `observed`: hay un valor/decisión afirmativamente observable;
  - `not_observed`: se buscó y no se encontró, con oportunidad suficiente;
  - `not_applicable`: la característica no corresponde al género/tarea;
  - `not_evaluable`: la extensión, fragmento o contexto no permite decidir.
- `research_alignment`:
  - `pattern_ai`: la observación se alinea con un patrón elevado para IA en el registro;
  - `pattern_human`: la observación se alinea con un patrón elevado para humanos en el registro;
  - `neutral`: la observación fue evaluada respecto de una referencia aplicable y no muestra alineación direccional con los patrones humanos ni de IA considerados (neutralidad evaluada; no sustituye a una referencia no disponible);
  - `not_assessed`: no se realizó ni puede justificarse una evaluación de alineación con un patrón de referencia (ausencia, no aplicable, no evaluable u observación sin patrón aplicable).

Nota: `mixed` no es un valor válido de `research_alignment` en `EvidenceRecord`. La mezcla de direcciones se expresa únicamente en `ClusterSummary` y `AnalysisRun` (ver § 5.3.3 y § 5.6).
- `alignment_basis`:
  - `reference_pattern`: la alineación se funda en un `reference_pattern_id` del registro;
  - `contextual_neutralization`: la alineación se evalua como neutral por neutralización contextual documentada;
  - `none`: no hay fundamento de alineación.

Nota: `mixed_observations` no es un valor válido de `alignment_basis` en `EvidenceRecord`. En un registro individual la alineación se funda en `reference_pattern`, `contextual_neutralization` o `none`. La mezcla se documenta en los niveles agregados, no en el registro atómico.
- `status_reason`: motivo obligatorio para `not_observed`, `not_applicable` y `not_evaluable`; `null` para `observed`.
- `absence_justification`: texto que documenta el alcance de la búsqueda y la razón de la ausencia cuando `observation_status=not_observed`; `null` en los demás casos.
- `search_scope`: alcance de la búsqueda realizada para establecer ausencia (`full_text`, `declared_span`, `relevant_sections`, `not_applicable`); `null` si no aplica.
- `observation_origin`: procedencia de la observación (ver 5.3.1); obligatorio.
- `origin_detail`: metadatos de procedencia (método o herramienta, modelo y versión, identificador seudonimizado del anotador, fecha o identificador de ejecución, versión del protocolo, estado de autorización del procesamiento externo); `null` cuando no corresponda.
- `alignment_basis_detail`: justificación auditada cuando `alignment_basis=contextual_neutralization` o cuando `pattern_ai`/`pattern_human` se fundamente en algo distinto de un `reference_pattern_id`; `null` en los demás casos.
- `observed_value_text`: descripción neutral, sin score numérico inventado.
- `source_spans`: una o más citas exactas con offsets.
- `opportunity_status`: `sufficient`, `limited`, `none`, `unknown`.
- `interpretation`: lectura del hallazgo separada de la observación.
- `alternative_explanations`: lista de explicaciones contextuales plausibles.
- `counterevidence_record_ids`: referencias a otros hallazgos que contradicen o matizan este.
- `cluster_id`: clúster operativo del Feature Registry.
- `shared_evidence_group_id`: nullable; enlaza varios registros originados en la misma decisión narrativa.
- `evidence_strength`: `weak`, `moderate`, `strong`, `not_rated`.
- `assessment_confidence`: `low`, `moderate`, `high`, `not_rated`; expresa confianza en la calidad de esta lectura, nunca probabilidad de autoría.
- `review_status`: `unreviewed`, `accepted`, `revised`, `rejected`.

#### Resolución de la referencia histórica (`historical_reference_pattern_id`)

`historical_reference_pattern_id` es una propiedad del `FEATURE_REGISTRY`, no un campo duplicado de `EvidenceRecord`.

Reglas:
- El registro almacena un único `historical_reference_pattern_id` por `feature_record`.
- `EvidenceRecord` resuelve la referencia mediante `feature_id` + `AnalysisRun.feature_registry_version`.
- No se duplica `historical_reference_pattern_id` en `EvidenceRecord`.
- La versión del registro debe quedar fijada en el bundle y ser reproducible.
- La resolución requiere que el patrón exista en la versión fijada y pertenezca a la misma característica.
- Si el bundle se exporta fuera de su contexto, el sobre de exportación debe conservar `feature_registry_version` (y, si el formato lo contempla, el digest del registro).
- No se reinterpreta un análisis histórico con una versión posterior del registro sin revalidación explícita.

#### Por qué se separan observation_status y research_alignment

El esquema heredado usa cinco estados que combinan en sus etiquetas presencia y alineación (`Presente–alineado`, `Presente–opuesto`, `Ausente`, `No aplicable`, `No evaluable`). Sin embargo, el informe también necesita representar un hallazgo presente pero neutral en contexto. Dos ejes ortogonales lo expresan mejor:

- `observation_status` responde: ¿se observó, no se observó, no aplica o no es evaluable?
- `research_alignment` responde: ¿la observación se alinea con patrones IA, patrones humanos, ambos, ninguno o no puede valorarse?

No se modificará el baseline `v0.2.3`. El motor `v0.3.0` usará este esquema versionado nuevo. Un exportador de compatibilidad podrá producir el estado heredado cuando exista equivalencia inequívoca; ante una observación neutral, no fabricará una conversión engañosa.

#### Correspondencia con los cinco estados históricos

La tabla siguiente documenta la relación con los estados de `v0.2.3` (`references/evidence-status.md`). No sustituye el modelo histórico ni se aplica automáticamente: cada fila exige que la dirección específica de la característica esté respaldada por el registro.

| Estado histórico | `observation_status` | `research_alignment` | Traducción exacta |
|---|---|---|---|
| Presente–alineado | `observed` | `pattern_ai` o `pattern_human`, según la dirección elevada de la característica | Condicional: requiere `reference_pattern_id` o fundamento contextual auditado |
| Presente–opuesto | `observed` | La dirección opuesta a la elevada cuando existe patrón registrado; `not_assessed` cuando no existe patrón opuesto registrado | Condicional; exige `reference_relation=opposed`, `source_spans` no vacío y justificación; nunca se representa como `neutral` ni como mera ausencia |
| Ausente | `not_observed` con `opportunity_status=sufficient` | `not_assessed` | Exacta solo si la oportunidad es suficiente; en caso contrario corresponde a `not_evaluable` |
| No aplicable | `not_applicable` | `not_assessed` | Exacta |
| No evaluable | `not_evaluable` | `not_assessed` | Exacta |
| Presente neutral (sin estado histórico separado) | `observed` | `neutral` | Sin equivalente exacto en el enum histórico |

Aclaraciones:

- `not_assessed` pertenece a `research_alignment` y significa que no se propone alineación investigativa; `not_evaluable` pertenece a `observation_status` y significa que no puede decidirse si el rasgo está presente. No son equivalentes.
- La ausencia de una observación no constituye evidencia direccional por sí misma.
- La alineación con patrones de investigación no equivale a una decisión de autoría.
- El exportador de compatibilidad no puede preservar el significado en todos los casos. Las combinaciones sin traducción exacta quedan pendientes de especificación; no se forzará una conversión que pierda información.

#### 5.3.1 Procedencia de la observación (`observation_origin`)

Toda observación debe registrar su origen en `observation_origin` (obligatorio), con `origin_detail` cuando corresponda:

- `human_annotation`: anotación realizada por una persona siguiendo un protocolo versionado.
- `external_model`: salida de un modelo externo (LLM u otro) autorizado para procesar el texto.
- `independent_tool`: resultado de una herramienta de análisis independiente (no generativa).
- `authorized_experiment`: proceso experimental autorizado (piloto, benchmark, evaluación humana).

Metadatos mínimos cuando apliquen:
- método o herramienta y su versión;
- modelo y versión (solo si `external_model`);
- identificador seudonimizado del anotador o del ejecutor;
- fecha o identificador de ejecución;
- versión del protocolo de anotación;
- estado de autorización del procesamiento externo (`authorized`, `not_authorized`, `not_applicable`).

Reglas:
- No enviar textos a servicios externos sin autorización explícita; registrar el estado de autorización.
- No almacenar credenciales, tokens ni datos personales innecesarios; usar identificadores seudonimizados.
- La procedencia es trazabilidad, no validación científica: una observación generada por un modelo no se considera validada por el solo hecho de proceder de él.

#### 5.3.2 Definición operativa de `opportunity_status`

- `sufficient`: el texto y su contexto ofrecen oportunidad suficiente para detectar o descartar la característica; permite establecer `observed` o `not_observed`.
- `limited`: existe alguna oportunidad, pero insuficiente para una conclusión firme; fuerza `not_evaluable` para ausencias y limita la fuerza de la evidencia.
- `none`: no existe oportunidad alguna (p. ej., característica no aplicable al texto o género); corresponde a `not_applicable` o `not_evaluable`.
- `unknown`: no se pudo determinar la oportunidad (p. ej., fragmento sin metadatos de completitud); tratar como `not_evaluable` hasta que se resuelva.

Relación con `observation_status`:
- `not_observed` exige `opportunity_status=sufficient` (regla 1).
- `not_evaluable` suele acompañarse de `limited`, `none` o `unknown`.
- `not_applicable` suele acompañarse de `none`.
- `observed` requiere `sufficient` o `limited` según la extensión del pasaje.

Qué permite concluir: con `sufficient` se puede afirmar presencia o ausencia documentada. Qué no permite concluir: con `limited`/`none`/`unknown` no se puede establecer ausencia real ni alineación direccional.

#### 5.3.3 Evidencia mixta (`mixed`)

`mixed` describe la coexistencia de señales en direcciones distintas dentro de un conjunto de observaciones vinculadas. Es una propiedad de un conjunto, nunca de una observación individual.

`mixed` no es un valor válido de `research_alignment` en `EvidenceRecord`. Un registro individual conserva siempre su alineación individual (`pattern_ai`, `pattern_human`, `neutral` o `not_assessed`).

Niveles donde `mixed` es válido:
- `ClusterSummary.alignment`: síntesis cualitativa de las observaciones del clúster.
- `AnalysisRun`: perfil global del expediente, respaldado por registros y resúmenes trazables.

Condiciones para declarar `mixed`:
1. Dos o más observaciones trazables.
2. Registros individuales con alineaciones distintas.
3. Referencias a los registros que justifican la síntesis (`record_ids`).
4. Ausencia de una operación de votación por mayoría.
5. Ausencia de porcentajes o puntuaciones de autoría.

Prohibido: convertir `mixed` en un promedio numérico, en una votación por mayoría o en un porcentaje de autoría; inferir `mixed` únicamente por incertidumbre, falta de datos o ausencia de evaluación; confundir `mixed` con `neutral` o con `not_assessed`.

Cuando dos observaciones presenten direcciones distintas:
- Crear dos `EvidenceRecord` individuales con sus alineaciones correspondientes.
- Vincularlos mediante `shared_evidence_group_id` cuando proceda.
- No sobrescribir las alineaciones individuales con `mixed`.
- Expresar la mezcla en el `ClusterSummary` o en el `AnalysisRun` correspondiente.

#### 5.3.4 Valores categóricos explícitos de ausencia

Una opción explícita de una característica que describe la ausencia de un elemento narrativo (p. ej., `no_subplots`, `no_major_withholding`, `no_direct_address`, `no_anachrony`) constituye una observación, no una ausencia superficial.

Regla: si el texto presenta esa condición y el registro lo respalda con cita u oportunidad suficiente, se registra como:
- `observation_status=observed`;
- `observed_option_id` = la opción canónica correspondiente;
- `research_alignment` según el patrón aplicable, o `not_assessed` si no existe patrón.

No confundir con `not_observed`, que se reserva para "característica no detectada tras oportunidad suficiente de búsqueda". Las opciones categóricas de ausencia se verifican contra el registro canónico antes de emplearlas; no se inventan identificadores de opción.

#### 5.3.5 Resolución de características bidireccionales

Las tres características con patrones en ambas direcciones son `Dominant Emotional Expression`, `Subplot Integration` y `Reference Explicitness`.

Regla de resolución: no inferir la dirección a partir del nombre de la característica. La dirección se resuelve mediante `reference_pattern_id` y el registro versionado (`research_direction_or_option_source`), que ya codifica qué opción se eleva para IA y cuál para humanos.

Decisión: no se añade un campo `reference_direction` independiente; el patrón seleccionado desambigua la dirección. Si el patrón seleccionado no permite determinar la dirección (p. ej., observación sin patrón aplicable), `research_alignment=not_assessed`.

Para el exportador de compatibilidad, la dirección de referencia histórica de estas características se resuelve mediante `historical_reference_pattern_id` del registro versionado. En las tres bidireccionales actuales esa referencia es el patrón IA. Esta es una convención histórica de compatibilidad para comparar contra el corpus del estudio; no implica una jerarquía de calidad entre escritura humana e IA.

Ejemplo de registro válido para una observación del polo humano:
- `research_alignment=pattern_human`
- `reference_pattern_id`=patrón humano
- `reference_relation=opposed`
- `historical_reference_pattern_id`=patrón IA (resuelto desde el registro)

No hay contradicción: `reference_pattern_id` identifica el patrón con el que se alinea la observación; `historical_reference_pattern_id` identifica la referencia histórica de la característica. En una bidireccional ambos pueden ser patrones distintos.

#### 5.3.6 Matriz de combinaciones válidas e inválidas

Combinaciones por caso (estructura válida, restricciones, interpretación permitida/prohibida):

1. Observación presente alineada con patrón IA: `observed` + `pattern_ai` + `reference_pattern` + `reference_pattern_id` no nulo + `source_spans` no vacío + `opportunity_status` sufficient/limited. Permitido: describir alineación con el patrón. Prohibido: convertir en probabilidad de autoría.
2. Observación presente alineada con patrón humano: análogo con `pattern_human`.
3. Observación presente sin patrón aplicable: `observed` + `not_assessed` + `none` + `reference_pattern_id` null. Permitido: registrar la observación sin atribuir dirección. Prohibido: asignar `pattern_ai`/`pattern_human` por intuición.
4. Observación evaluada como neutral: `observed` + `neutral` + `contextual_neutralization` + `alignment_basis_detail` no nulo. Permitido: documentar la neutralización contextual. Prohibido: usar `neutral` como sustituto de una referencia no disponible.
5. Ausencia real con oportunidad suficiente: `not_observed` + `not_assessed` + `none` + `opportunity_status=sufficient` + `status_reason` no nulo + `absence_justification` no nulo + `search_scope` no nulo + `observed_option_id` null. Permitido: registrar ausencia como estado. Prohibido: interpretar la ausencia como evidencia direccional.
6. Ausencia no determinable por oportunidad limitada: `not_evaluable` + `not_assessed` + `none` + `opportunity_status` en {limited, none, unknown} + `status_reason` no nulo. Permitido: marcar no evaluable. Prohibido: afirmar presencia o ausencia.
7. Característica no aplicable: `not_applicable` + `not_assessed` + `none` + `status_reason` no nulo + `opportunity_status` en {none, unknown}. Permitido: excluir del análisis por género/tarea. Prohibido: tratar como evidencia.
8. Característica no evaluable: igual que 6, con motivo de limitación contextual.
9. Característica bidireccional: `observed` + `pattern_ai`/`pattern_human` + `reference_pattern` + `reference_pattern_id` no nulo que corresponda a una de las dos direcciones del feature; si no hay patrón aplicable, `not_assessed`. Permitido: alineación con la dirección del patrón seleccionado. Prohibido: inferir la dirección del nombre de la característica.
10. Evidencia mixta agregada: `mixed` válido solo en `ClusterSummary` o en `AnalysisRun`, respaldado por `record_ids` con alineaciones distintas. Prohibido: `mixed` en `EvidenceRecord` (no es valor válido de su enum), votación por mayoría o porcentaje.
11. Opción categórica explícita de ausencia: `observed` + `observed_option_id` = opción canónica + `research_alignment` según patrón o `not_assessed`. Prohibido: registrar como `not_observed`.
12. Observación de anotación humana: `observation_origin=human_annotation` + `origin_detail` con protocolo y anotador seudonimizado.
13. Observación de modelo externo: `observation_origin=external_model` + `origin_detail` con modelo, versión y estado de autorización; requiere autorización explícita.
14. Conflicto entre dirección y patrón de referencia: si `reference_pattern_id` no coincide con la dirección reclamada, `research_alignment=not_assessed` + `alignment_basis=none` + flag `INVALID_STATE_ALIGNMENT_COMBINATION`.
15. Consistencia con la referencia histórica:
   - `aligned` exige `reference_pattern_id = historical_reference_pattern_id` resuelto y `research_alignment = dir(historical_reference_pattern_id)`.
   - `opposed` exige evidencia afirmativa y, en características bidireccionales, `reference_pattern_id` = patrón opuesto registrado.
   - `not_assessed` no asigna una relación direccional y es compatible con `neutral`, con ausencia, con no aplicabilidad, con no evaluabilidad y con observaciones sin patrón aplicable.
   - El referente histórico se resuelve desde `FEATURE_REGISTRY` mediante `feature_id + AnalysisRun.feature_registry_version`; no se duplica en `EvidenceRecord`.
16. Relación entre registros: `counterevidence_record_ids` enlaza hallazgos que contradicen o matizan otro; no sustituye a `reference_relation`, que expresa la relación de una observación con la referencia histórica de su característica.

#### 5.3.7 Alternativas para conservar Presente–opuesto (pendiente de decisión del propietario)

`references/evidence-status.md` define Presente–opuesto como un valor directamente observado que representa el polo alternativo de una característica direccional: es contraevidencia real, no ausencia. El esquema v0.3.0 de dos ejes no conserva por sí solo esa distinción, porque `research_alignment` codifica el grupo del patrón (IA o humano), no la relación con una dirección de referencia. Se presentan tres alternativas; ninguna se adopta en esta fase.

**Alternativa A — Campo tipado separado `reference_relation`.**
- Añadir a `EvidenceRecord` un campo `reference_relation` con valores `aligned`, `opposed`, `not_assessed`.
- Compatibilidad con 30 features y 33 patrones: total, no altera el registro.
- Conservación del significado histórico: alta; `opposed` codifica contraevidencia explícitamente.
- Efecto sobre la matriz de estados: añade un tercer eje para la exportación histórica; la matriz actual de dos ejes se mantiene para el análisis descriptivo.
- Efecto sobre el exportador: puede producir Presente–opuesto cuando `reference_relation=opposed` y `observation_status=observed`.
- Facilidad de validación: alta (enum + consistencia con `reference_pattern_id`).
- Riesgo: un implementador puede confundir `reference_relation` con `research_alignment`; requiere documentación estricta.

**Alternativa B — Representación explícita de contraevidencia.**
- Añadir un campo o registro de contraevidencia con referencia a la característica y al patrón/polo de comparación (p. ej., `counterevidence=true` con `comparison_pole`).
- Compatibilidad: total.
- Conservación del significado: alta; la contraevidencia queda tipada.
- Efecto sobre la matriz: Presente–opuesto se modela como observación presente con marca de contraevidencia, no como estado separado.
- Efecto sobre el exportador: más claro que A, pero requiere reglas adicionales.
- Facilidad de validación: media (más campos, más invariantes).
- Riesgo: proliferación de esquema y duplicación con `counterevidence_record_ids`.

**Alternativa C — Derivar la relación del patrón seleccionado y del registro.**
- No añadir campos. La relación se deriva comparando el grupo del `reference_pattern_id` seleccionado con la dirección elevada de la característica en `research_direction_or_option_source` del registro.
- Compatibilidad: total.
- Conservación del significado: media-alta para features unidireccionales (27 de 30); para las tres bidireccionales (`Dominant Emotional Expression`, `Subplot Integration`, `Reference Explicitness`) la dirección elevada es ambigua y exige declarar una dirección de referencia.
- Efecto sobre la matriz: no añade ejes; la exportación es determinista dado el registro y la dirección de referencia declarada.
- Efecto sobre el exportador: determinista, pero depende de fijar la versión del registro.
- Facilidad de validación: media (requiere pinning de la revisión del registro y resolución de bidireccionales).
- Riesgo: lógica implícita, más difícil de auditar; la ambigüedad bidireccional persiste.

**Estado:** decisión adoptada en la consolidación documental v0.3.0: se selecciona la Alternativa A refinada como modelo A2.

Modelo A2 adoptado:
- `reference_pattern_id`: patrón de alineación del `EvidenceRecord`.
- `historical_reference_pattern_id`: referencia histórica almacenada exclusivamente en `FEATURE_REGISTRY`.
- `reference_relation`: `aligned`, `opposed`, `not_assessed`.

No se adoptan B ni C como solución principal:
- B añadiría una estructura paralela de contraevidencia y duplicaría responsabilidades con `counterevidence_record_ids`.
- C dejaría la relación implícita y no resolvería de forma auditable las características bidireccionales.

La Alternativa A se refina con la separación de identificadores: `reference_pattern_id` y `historical_reference_pattern_id` tienen funciones distintas y no se fusionan. El exportador de compatibilidad sigue pendiente para los casos sin equivalencia exacta.

#### Reglas lógicas mínimas

1. `not_observed` exige `opportunity_status=sufficient`; de lo contrario debe ser `not_evaluable`.
2. `not_applicable` requiere motivo y `research_alignment=not_assessed`.
3. `not_evaluable` requiere motivo y `research_alignment=not_assessed`.
4. `not_observed` no recibe `pattern_ai` ni `pattern_human` por defecto.
5. `observed` exige al menos un `source_span` verificable.
6. `observed` con `research_alignment=not_assessed` es admisible cuando no existe correspondencia investigativa clara.
7. `research_alignment=pattern_ai` o `pattern_human` exige `reference_pattern_id` o fundamento contextual auditado; no basta una etiqueta libre del modelo.
8. `mixed` no es un valor de `EvidenceRecord.research_alignment`; en `ClusterSummary` y `AnalysisRun` requiere dos o más observaciones trazables con alineaciones distintas; no es un promedio numérico ni una votación.
9. `EvidenceRecord.research_alignment` no admite `mixed`; la mezcla se expresa solo en `ClusterSummary` y `AnalysisRun`.
10. Ningún campo contiene probabilidad de autoría, porcentaje de humano/IA o puntuación global.
11. Un mismo suceso narrativo observado en varias características debe usar `shared_evidence_group_id` cuando proceda y no puede sumar votos independientes.

### 5.4 SourceSpan y verificación textual

Cada pasaje contendrá:

- `quote`: fragmento literal;
- `start_char`: índice de inicio, base cero;
- `end_char`: índice final exclusivo;
- `offset_unit`: `unicode_codepoint`.

Los offsets se calculan sobre el texto UTF-8 decodificado exactamente, sin normalización Unicode ni conversión de finales de línea. `quote` debe ser igual a `source_text[start_char:end_char]`.

Si el extractor entrega una cita sin offsets:

- el verificador puede resolverla automáticamente si aparece exactamente una vez;
- si aparece varias veces, exige desambiguación mediante offsets/contexto;
- si no aparece exactamente, la cita queda rechazada y el registro no puede respaldar conclusiones.

La normalización de espacios, puntuación o Unicode no se aplicará antes de comprobar coincidencia. Esto evita “citas aproximadas” que parecen literales y no lo son.

### 5.5 DimensionProfile

Habrá diez perfiles descriptivos, uno por dimensión del marco. Cada perfil incluirá:

- `dimension_id`;
- `coverage_status`: `descriptive_assessed`, `partially_assessed`, `not_assessable`, `not_applicable`;
- `neutral_summary`;
- `evidence_record_ids`;
- `limitations`.

No todas las dimensiones tienen que contener una característica del conjunto central 30. Un perfil descriptivo de una dimensión no mapeada no puede convertirse automáticamente en señal direccional de autoría.

### 5.6 ClusterSummary

Los ocho clústeres operativos serán identificadores estables. Cada resumen contiene:

- `cluster_id`;
- `record_ids`;
- `shared_evidence_group_ids`;
- `summary` neutral;
- `alignment`: `pattern_ai`, `pattern_human`, `mixed`, `neutral`, `not_assessed`; `mixed` requiere `record_ids` que acrediten ambas direcciones.
- `double_count_flags`.

No usar recuento de registros ni mayoría de features para asignar alineación al clúster. La síntesis es cualitativa y debe explicar si varias features reflejan una sola decisión narrativa.

### 5.7 Fuente de verdad, versionado y resolución

- `FEATURE_REGISTRY` es la fuente única de `historical_reference_pattern_id`.
- `AnalysisRun.feature_registry_version` fija la versión del registro usada por el bundle.
- `schema_version` identifica el esquema del bundle; en el registro, la adición de `historical_reference_pattern_id` se refleja como `schema_version` 1.1.0 frente a 1.0.0 de la versión 0.1.1-draft.
- El digest SHA-256 del registro puede incluirse en el paquete exportado cuando el formato ya lo contemple.
- No se reinterpreta un análisis histórico con una versión posterior del registro sin revalidación explícita.

## 6. Auditoría en dos capas

### 6.1 Capa A — determinista

No depende de un LLM. Debe validar:

- JSON Schema y tipos;
- campos obligatorios, enums y claves desconocidas;
- referencias a feature, dimensión, patrón, opción y clúster existentes;
- citas y offsets exactos;
- coherencia entre estado de observación y oportunidad;
- que las ausencias no tengan dirección;
- que la dirección investigativa tenga fundamento;
- que una característica/opción no se confunda con dos características;
- que no haya score o probabilidad prohibida;
- que los IDs referenciados existan;
- que el informe solo cite `record_id` válidos.

### 6.2 Capa B — auditoría semántica asistida por modelo

Una segunda pasada inspecciona el Evidence Ledger para encontrar:

- interpretación que no se desprende de la cita;
- cita que es literal pero no respalda la afirmación;
- alternativa contextual ausente;
- contraevidencia ignorada;
- uso de rasgos ausentes como señal;
- afirmaciones generales basadas en un único indicio;
- doble conteo potencial;
- generalización injustificada entre inglés, español y no ficción;
- incumplimiento de los guardrails de extensión y género.

La auditoría devuelve **flags** con severidad, registro afectado, motivo y acción sugerida. No reescribe ni corrige automáticamente el Evidence Ledger. Un revisor debe aceptar, modificar o rechazar los cambios.

### 6.3 Independencia y límites

Dos pasadas del mismo modelo, o dos modelos de una familia similar, no constituyen validación estadísticamente independiente. El acuerdo entre LLMs no es sustituto de concordancia con anotadores humanos. La evidencia reciente sobre LLM-as-judge advierte que los modelos pueden coincidir entre sí y aun así alejarse de los juicios humanos, especialmente en criterios subjetivos y multilingües.

Por ello:

- la auditoría automática mide cumplimiento estructural y encuentra riesgos;
- la auditoría semántica propone objeciones;
- la evaluación de calidad se ancla en anotaciones humanas documentadas y adjudicadas;
- ningún resultado de la segunda pasada se presenta como veredicto independiente.

### 6.4 Invariantes del modelo A2

Los invariantes `INV-A2-01` a `INV-A2-17` se definen en la Fase 1.10-T y se adoptan aquí. En esta especificación se resumen sus reglas operativas:

1. `INV-A2-01`: `historical_reference_pattern_id` se almacena solo en `FEATURE_REGISTRY`; `EvidenceRecord` lo resuelve mediante `feature_id + AnalysisRun.feature_registry_version`.
2. `INV-A2-02`: en las 30 características actuales, `historical_reference_pattern_id` es obligatorio, escalar y no nulo.
3. `INV-A2-03`: `historical_reference_pattern_id` debe pertenecer a la misma característica.
4. `INV-A2-04`: la selección es AI-first: patrón IA si existe; en caso contrario, patrón humano.
5. `INV-A2-05`: los valores de `historical_reference_pattern_id` son únicos entre características.
6. `INV-A2-06`: `reference_pattern_id`, si no es nulo, debe pertenecer a la misma característica.
7. `INV-A2-07`: `pattern_direction(reference_pattern_id) = research_alignment`.
8. `INV-A2-08`: `research_alignment ∈ {pattern_ai, pattern_human}` ⇔ `reference_pattern_id` no nulo.
9. `INV-A2-09`: `aligned` exige `reference_pattern_id = historical_reference_pattern_id` resuelto y `research_alignment = dir(historical_reference_pattern_id)`.
10. `INV-A2-10`: en bidireccionales, `opposed` exige `reference_pattern_id` = patrón opuesto registrado, `research_alignment = dir(reference_pattern_id)` y `reference_pattern_id ≠ historical_reference_pattern_id`.
11. `INV-A2-11`: en unidireccionales, `opposed` exige `reference_pattern_id=null`, `research_alignment=not_assessed`, `observation_status=observed`, evidencia y justificación.
12. `INV-A2-12`: `neutral` exige `observed`, `reference_pattern_id=null`, `reference_relation=not_assessed`, `alignment_basis=contextual_neutralization` y `alignment_basis_detail` no nulo.
13. `INV-A2-13`: ausencia, no aplicabilidad y no evaluabilidad exigen `research_alignment=not_assessed`, `reference_pattern_id=null` y `reference_relation=not_assessed`, con sus requisitos de oportunidad y motivo.
14. `INV-A2-14`: `reference_relation ∈ {aligned, opposed}` exige `observation_status=observed`.
15. `INV-A2-15`: `opposed` exige evidencia afirmativa y justificación tipo-específica; en escalas y ordinales no se inventan puntos de corte; en multi-select la coexistencia o ausencia de la opción de referencia no bastan; en categóricas/binarias una opción distinta no basta salvo complemento documentado.
16. `INV-A2-16`: la resolución exige `AnalysisRun.feature_registry_version` fijada e inmutable; no se reinterpreta un análisis con una versión posterior sin revalidación explícita.
17. `INV-A2-17`: las futuras características sin patrón histórico usan `historical_reference_pattern_id=null` y solo admiten `research_alignment=not_assessed`, `reference_pattern_id=null`, `reference_relation=not_assessed`.

La validación estructural automatizable puede comprobar identificadores, enums, pertenencia, dirección, cardinalidad, spans y justificación no nula. La validación semántica requiere auditoría para decidir si un valor constituye realmente un polo opuesto, si una cita sostiene una interpretación o si una opción diferente es un complemento documentado.

### 6.5 Validación estructural vs. semántica para `opposed`

- **Bidireccionales:** estructuralmente verificable por IDs y direcciones; semánticamente requiere confirmar que el texto sostiene el patrón alternativo.
- **Categóricas unidireccionales:** una opción diferente no basta; requiere complemento opuesto documentado por el instrumento o la metodología.
- **Binarias:** un `no` explícito puede ser `opposed` cuando es una opción canónica observada; la mera ausencia no basta.
- **Multi-select:** la presencia de la opción de referencia implica alineación con esa referencia; su coexistencia con otras opciones no produce automáticamente `opposed`; la ausencia de la opción de referencia no demuestra contraevidencia.
- **Escalas y ordinales:** no se crean umbrales numéricos; `opposed` requiere un ancla o constructo opuesto identificable y justificación cualitativa. Un valor intermedio o una media no se vuelve opuesto automáticamente.

### 6.4 Formato de AuditFinding

Campos mínimos:

- `finding_id`;
- `rule_id`;
- `severity`: `error`, `warning`, `info`;
- `record_ids`;
- `description`;
- `suggested_action`;
- `origin`: `deterministic` o `model_assisted`;
- `review_status`: `open`, `accepted`, `dismissed`, `resolved`.

Códigos de regla iniciales sugeridos:

- `QUOTE_NOT_FOUND`;
- `SPAN_OUT_OF_BOUNDS`;
- `QUOTE_OFFSET_MISMATCH`;
- `UNKNOWN_FEATURE_ID`;
- `UNKNOWN_PATTERN_OPTION`;
- `INVALID_STATE_ALIGNMENT_COMBINATION`;
- `ABSENCE_AS_DIRECTION`;
- `DIRECTION_WITHOUT_BASIS`;
- `UNSUPPORTED_INTERPRETATION`;
- `MISSING_ALTERNATIVE_EXPLANATION`;
- `COUNTEREVIDENCE_OMITTED`;
- `POTENTIAL_DOUBLE_COUNT`;
- `GLOBAL_ALIGNMENT_GUARDRAIL`;
- `LANGUAGE_TRANSFER_OVERCLAIM`;
- `AUTHORSHIP_PROBABILITY_FORBIDDEN`;
- `PRIVACY_POLICY_VIOLATION`.

## 7. Salidas

### 7.1 `analysis.json`

Expediente canónico versionado con run, perfiles, registros, resúmenes de clúster y auditoría.

### 7.2 `report.md`

Conservará los siete apartados de la plantilla v0.2.3, con estos ajustes:

1. Alcance, contexto y adecuación.
2. Resumen estructural neutral.
3. Perfil descriptivo de las diez dimensiones.
4. Evidencias centrales agrupadas por clúster, con citas y contraevidencia.
5. Lenguaje superficial, separado de narrativa.
6. Síntesis prudente y limitaciones.
7. Recomendaciones, solo cuando procedan.

El informe no contendrá puntuación ni probabilidad global. Toda afirmación analítica sustantiva debe poder rastrearse a uno o más `record_id` del expediente.

### 7.3 Estados de auditoría

- `passed`: validaciones deterministas sin errores ni warnings relevantes.
- `passed_with_warnings`: sin errores bloqueantes, pero hay alertas abiertas.
- `requires_human_review`: hay cuestiones semánticas o metodológicas que requieren juicio humano.
- `failed`: errores estructurales, referencias rotas, citas no verificables o violaciones de reglas obligatorias.

Un informe con `failed` no puede presentarse como análisis final aceptado. Un informe con `requires_human_review` puede exportarse solo indicando claramente que está pendiente.

## 8. Contratos y dependencias

### Runtime

- Python 3.12 como baseline inicial por compatibilidad con el CI actual; comprobar versiones reales al implementar.
- Biblioteca estándar para lectura, JSON, UUID, fechas, hashing opcional, CLI y validación de reglas de dominio.
- Sin dependencias de red, base de datos, vector store o SDK de modelos.

### Esquemas

- JSON Schema Draft 2020-12 para contratos interoperables.
- Dependencia `jsonschema` limitada al entorno de desarrollo/CI para probar los esquemas; no requerida por el runtime de análisis.
- Los invariantes que dependen del texto fuente o de referencias cruzadas se verifican con código propio; JSON Schema por sí solo no valida una cita contra el texto original.

### CLI mínima

Comandos propuestos:

```powershell
py -3 -m storyscope_evidence_engine validate --analysis .\analysis.json --source .\story.txt
py -3 -m storyscope_evidence_engine audit --analysis .\analysis.json --source .\story.txt
py -3 -m storyscope_evidence_engine render --analysis .\analysis.json --output .\report.md
```

En v0.3.0, CLI no llama a proveedores ni envía el texto a la nube. La creación de candidatos estructurados la realiza OpenCode/modelo autorizado o un anotador humano; el motor valida, audita, agrupa y renderiza.

### Contrato de proveedor futuro

No implementar todavía Model Hub. Cuando exista más de un proveedor real, definir una interfaz neutral para `extract(text, context, registry) -> EvidenceProposal[]`. Los proveedores nunca podrán modificar el registro canónico ni saltarse los validadores.

## 9. Privacidad y seguridad de datos

- El texto se lee localmente y se procesa en memoria.
- No guardar texto completo ni fragmentos innecesarios dentro del expediente.
- Los informes contienen citas breves y estrictamente necesarias para justificar observaciones.
- El hash de la fuente está desactivado por defecto y requiere solicitud explícita.
- No se transmiten textos a APIs ni a detectores online en v0.3.0.
- Los fixtures de prueba usan textos originales sintéticos o materiales con permisos claros; no se incorporan narrativas privadas del usuario.
- No persistir prompts ni salidas sensibles en logs.
- Limitar el tamaño de entrada, informar errores y evitar procesar archivos binarios o codificaciones no soportadas silenciosamente.

## 10. Estrategia de pruebas

### 10.1 Unitarias y de contrato

- Bundle válido e inválido.
- Enums fuera de lista, campos ausentes y claves desconocidas.
- Feature, dimensión, patrón, opción y clúster inexistentes.
- Las 30 características y 33 patrones permanecen trazables a los datos de v0.2.3.
- No se altera la transcripción de Tabla 16, las nueve excepciones de redondeo ni los valores validados.

### 10.2 Citas y offsets

- Cita exacta única.
- Cita repetida con offsets que identifican una ocurrencia.
- Cita inexistente.
- Offset negativo, fin fuera de rango e inicio mayor que fin.
- Tildes, caracteres combinados, signos tipográficos y emojis.
- CRLF y LF preservados; no normalizar antes de verificar.
- Cita truncada o con espacios distintos debe fallar hasta corregirse.

### 10.3 Semántica y oportunidad

- Microtexto de 21 palabras: no produce alineación global.
- Texto menor de 500 palabras: etiqueta global `evidencia insuficiente`.
- Fragmento que empieza a mitad de una escena: la apertura del relato completo es `not_evaluable`.
- Ausencia de subtramas en fragmento breve: `not_evaluable`, no opción `no_subplots`.
- Historia completa con oportunidad suficiente y valor categórico explícito `no_subplots`: `observed` como opción, no ausencia superficial.
- Ausencia de un rasgo jamás recibe `pattern_ai` ni `pattern_human` por defecto.
- Género no aplicable separado de información insuficiente.
- No ficción marcada como adaptación exploratoria.

### 10.4 Opciones y doble conteo

- `Dominant Emotional Expression`, `Reference Explicitness` y `Subplot Integration` permiten opciones distintas sin duplicar el feature.
- La presencia de varias observaciones vinculadas a un mismo pasaje no crea votos.
- Un grupo de evidencia compartida debe aparecer una sola vez en la síntesis de clúster.
- La agregación nunca cuenta registros, direcciones o features como puntos.

### 10.5 Auditoría y reportes

- Auditoría determinista bloquea citas inválidas.
- Auditoría semántica solo crea flags; no modifica registros.
- Reporte solo referencia IDs existentes.
- Ningún informe puede contener porcentaje o probabilidad de autoría.
- Los resultados que requieren revisión quedan etiquetados.
- Repetir renderizado del mismo bundle produce el mismo Markdown salvo campos explícitamente variables (p. ej., timestamp de generación, que deberá aislarse).

### 10.6 Evaluación humana posterior

Antes de afirmar calidad científica, preparar un piloto con:

- guía de anotación versionada;
- dos anotadores humanos independientes en una primera fase;
- adjudicación documentada de desacuerdos;
- acuerdo interanotador apropiado al tipo de variable (por ejemplo, kappa para pares de anotadores o alfa de Krippendorff cuando corresponda a número de anotadores/datos faltantes/escala);
- conjunto de desarrollo y test separado;
- partición por autor y prompt para reducir fuga de información;
- estratificación por idioma, variedad, género, longitud, edición y condición de asistencia;
- intervalos de confianza y prevalencia por etiqueta cuando existan muestras suficientes.

No se fijarán objetivos arbitrarios de precisión antes del piloto y la línea base. Las métricas automáticas de exactitud de cita y validez de esquema se reportan separadas de juicios narrativos subjetivos.

## 11. Estructura de archivos propuesta

```text
storyscope-human-ai-analysis/
├── SKILL.md                         # baseline v0.2.3 preservado al inicio
├── references/
│   ├── feature-dimension-map.csv    # no alterar valores científicos
│   ├── cluster-map.md
│   ├── evidence-status.md           # baseline histórico
│   └── ...
├── engine/
│   └── storyscope_evidence_engine/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── input_gate.py
│       ├── registry.py
│       ├── bundle.py
│       ├── quote_verifier.py
│       ├── evidence_validator.py
│       ├── cluster_resolver.py
│       ├── audit.py
│       └── report.py
├── schemas/
│   ├── analysis-bundle.schema.json
│   ├── analysis-run.schema.json
│   ├── evidence-record.schema.json
│   └── audit-report.schema.json
├── validation/
│   ├── build_feature_registry.py
│   └── validate_feature_registry.py
├── tests/
│   ├── fixtures/
│   ├── test_schemas.py
│   ├── test_quote_verifier.py
│   ├── test_evidence_rules.py
│   ├── test_cluster_resolver.py
│   ├── test_audit.py
│   └── test_report.py
└── docs/
    └── design/
        └── v0.3.0/
            ├── TECHNICAL_SPEC_v0.1.md
            └── EVIDENCE_ANNOTATION_GUIDE.md   # propuesta futura
```

Este árbol es una propuesta. Antes de crearlo, inspeccionar el estado real del repositorio y no sobrescribir archivos existentes.

## 12. Plan de implementación recomendado

### Fase 0 — preflight, solo lectura

1. Verificar repo, rama, HEAD, tag `v0.2.3`, status, diff-check y CI actual.
2. Identificar si el checkout local tiene modificaciones no publicadas.
3. Comparar versión local con `main` remoto sin asumir que son iguales.
4. Crear respaldo antes de cualquier escritura.
5. Detenerse ante diferencias no comprendidas.

### Fase 1 — contratos y registro

1. Definir `analysis-bundle.schema.json` y subesquemas.
2. Definir Feature Registry con 30 IDs internos estables y 33 referencias de patrón.
3. Validar cobertura y valores contra archivos canónicos existentes.
4. Añadir pruebas de compatibilidad con la transcripción Tabla 16.

### Fase 2 — validación determinista

1. Implementar Input Gate y conteo reproducible.
2. Implementar lector UTF-8 con preservación de saltos de línea.
3. Implementar verificador exacto de citas/offsets.
4. Implementar reglas de estado, alineación y oportunidad.
5. Implementar validación de referencias cruzadas.

### Fase 3 — agrupación y auditoría

1. Implementar los ocho clústeres como catálogo versionado.
2. Implementar grupos de evidencia compartida y flags de doble conteo.
3. Implementar auditoría determinista.
4. Definir contrato de salida para la auditoría semántica; no autoescritura.

### Fase 4 — reportes y CI

1. Renderizar `analysis.json` y `report.md`.
2. Añadir fixtures positivos/negativos.
3. Ejecutar pruebas en serie en Windows y Ubuntu.
4. Verificar que los tests de v0.2.3 siguen pasando sin alteración.
5. Documentar límites, dependencias y resultados.

No hacer commit, push, merge ni publicar una release sin una autorización explícita y un informe de aceptación.

## 13. Criterios de aceptación v0.3.0

La versión no se considera lista si falla cualquiera de estos requisitos:

1. Preserva el baseline metodológico y numérico de v0.2.3.
2. Registra y valida 30 features y 33 referencias de patrón sin duplicar las opciones.
3. Representa diez perfiles dimensionales y distingue perfiles descriptivos de patrones centrales.
4. Cada observación direccional tiene base de patrón explícita.
5. Cada observación `observed` cuenta con citas localizables exactamente.
6. Los estados `not_observed`, `not_applicable` y `not_evaluable` no reciben alineación de autoría.
7. Los valores categóricos explícitos como `no_subplots` se distinguen de una ausencia superficial.
8. No permite score agregado ni probabilidad de autoría.
9. El resolver de clústeres impide el doble conteo como votos.
10. La auditoría determinista y la semántica se distinguen; la segunda no altera datos automáticamente.
11. Se puede reconstruir metodología, versiones y parámetros disponibles de cada corrida.
12. No se almacena texto completo ni se transmite a servicios externos por defecto.
13. El informe declara idioma, variedad, género, longitud, completitud, adecuación y limitaciones.
14. Los fixtures cubren Unicode, fragmentos, género, ausencia, opciones duales y evidencia insuficiente.
15. La Skill `v0.2.3` y sus validadores permanecen intactos y aprobados.
16. CI pasa en Windows y Ubuntu usando la matriz ya probada.

## 14. Investigación que influye en esta especificación

### Fuentes científicas

1. Russell, Jenna et al. *StoryScope: Investigating idiosyncrasies in AI fiction*. COLM 2026; arXiv:2604.03136v6. https://arxiv.org/abs/2604.03136
   - Fuente principal del marco narrativo y las 30 características centrales; sus métricas son del clasificador/corpus del estudio, no del motor de StoryScope.
2. Hamilton, Sil; Wilkens, Matthew; Piper, Andrew. *NarraBench: A Comprehensive Framework for Narrative Benchmarking*. EACL 2026. https://aclanthology.org/2026.eacl-long.176/
   - Justifica evaluar comprensión narrativa en dimensiones subjetivas y tareas poco cubiertas; no constituye un detector de autoría.
3. *HACo-Det*. ACL 2025. https://aclanthology.org/2025.acl-long.1069/
   - Referencia para estudiar textos mixtos y dificultades de atribución por segmentos.
4. *DAMASHA*. Findings of EACL 2026. https://aclanthology.org/2026.findings-eacl.326/
   - Referencia para segmentación interpretable y análisis de textos mixtos; no se importa como clasificador.
5. Mukherjee et al. *The Geometry of LLM-as-Judge: Why Inter-LLM Consensus Is Not Human Alignment*. Findings of EMNLP 2026. https://aclanthology.org/2026.findings-emnlp.1696/
   - Motiva que la segunda pasada sea una auditoría y no un sustituto de anotadores humanos; el acuerdo entre modelos puede no reflejar alineación humana.
6. Fu & Liu. *How Reliable is Multilingual LLM-as-a-Judge?* Findings of EMNLP 2025. https://aclanthology.org/2025.findings-emnlp.587/
   - Advierte sobre consistencia variable entre idiomas. No permite inferir una tasa específica para español sin evaluación específica.

### Fuentes de estándares

- JSON Schema, especificación vigente Draft 2020-12: https://json-schema.org/specification
- JSON Schema Validation 2020-12: https://json-schema.org/draft/2020-12/json-schema-validation

## 15. Próxima decisión técnica

Tras aprobar esta especificación, la siguiente tarea será **preflight de solo lectura del repositorio local y diseño/creación del Feature Registry**. No implementar extracción LLM hasta que los contratos, IDs, citas y reglas de estado pasen sus pruebas deterministas.

**Estado final de esta especificación:** arquitectura y contratos propuestos; motor todavía no implementado; release `v0.2.3` preservada.
