# STORYSCOPE HUMAN–AI ANALYSIS — PROJECT CHARTER

**StoryScope Human–AI Analysis | v0.1 | 12 de noviembre de 2026**  
**Estado:** decisión arquitectónica aprobada para planificación; motor todavía no implementado.  
**Proyecto público de referencia:** https://github.com/liongrimsoul78/storyscope-human-ai-analysis  
**Release estable que debe preservarse:** `v0.2.3` — https://github.com/liongrimsoul78/storyscope-human-ai-analysis/releases/tag/v0.2.3

---

## 1. Decisión ejecutiva

StoryScope Human–AI Analysis desarrollará progresivamente un **StoryScope Evidence Engine**, un motor especializado para analizar narrativa y escritura humano–IA, ampliar la trazabilidad de la evidencia y generar informes reproducibles.

La prioridad no es construir un bot, una web ni una plataforma multiagente. La prioridad es convertir la metodología cualitativa de la Skill `StoryScope Human-AI Analysis` en un flujo de análisis estructurado, auditable, evaluable y extensible.

**Separación arquitectónica obligatoria:**

- **StoryScope Evidence Engine:** autoridad metodológica del dominio narrativo. Define las observaciones, evidencia, interpretación, límites y reportes.
- **Planos de control externos:** si en el futuro existieran, podrían gestionar identidad, autorización, tareas, ejecución, persistencia operacional y auditoría. No deben decidir el significado científico de una característica narrativa.
- **Proveedores de modelos intercambiables:** posibles fuentes de propuestas de extracción en una etapa posterior. Los modelos no son fuentes de verdad ni autoridades metodológicas.
- **Interfaces (OpenCode, CLI, web, bot, MCP):** superficies de acceso reemplazables. Ninguna es necesaria para la primera etapa del motor.

StoryScope no se fusiona con planos de control externos ni introduce una dependencia obligatoria de ellos. Cualquier integración futura será mediante un adaptador con contrato explícito y no alterará la autoridad metodológica del proyecto.

## 2. Situación de partida: hechos confirmados en la continuidad

### 2.1 Skill y repositorio público

- Nombre canónico: **StoryScope Human-AI Analysis**.
- Autoría de la Skill: **proyecto StoryScope Human–AI Analysis**.
- StoryScope Human–AI Analysis es un proyecto individual, independiente y autónomo; no pertenece ni depende de otros proyectos u organizaciones.
- Los identificadores internos `ssha.*` pertenecen a StoryScope Human–AI Analysis; no son identificadores oficiales de la investigación original.
- Repositorio público: `liongrimsoul78/storyscope-human-ai-analysis`.
- Release/tag estable: `v0.2.3`.
- La versión pública es una implementación cualitativa independiente inspirada en el trabajo de Russell et al.; no es la implementación oficial de StoryScope ni tiene afiliación oficial con sus autores.
- La Skill no contiene el dataset original, los pesos, el clasificador XGBoost ni el pipeline oficial de extracción y evaluación.
- Los resultados publicados del clasificador del paper no son resultados de esta Skill ni deben atribuirse al motor de StoryScope.
- La continuidad registra CI aprobado en Ubuntu y Windows, Python 3.12, en el último ciclo de publicación. Estado del repositorio y CI deben verificarse de nuevo antes de una intervención técnica.

### 2.2 Base metodológica actual

- 10 dimensiones narrativas.
- 30 características centrales.
- 33 comprobaciones/opciones a nivel de característica.
- 9 excepciones de redondeo documentadas en la transcripción de la Tabla 16.
- Cinco estados de evidencia: `presente-alineado`, `presente-opuesto`, `ausente`, `no aplicable`, `no evaluable`.
- Etiquetas direccionales: `patrón IA`, `patrón humano`, `mixto`, `neutro`, `no evaluable`.
- Ocho agrupaciones operativas de StoryScope para evitar doble conteo; no son agrupaciones oficiales de la investigación original.
- La ausencia no cuenta como evidencia de autoría. No existe puntuación global por suma o mayoría.
- Las salvaguardas de extensión de texto (por ejemplo, 500/1.000 palabras) son reglas operativas de StoryScope, no umbrales validados por el paper.
- La adaptación al español es exploratoria y no cuenta todavía con una validación equivalente a la del corpus original en inglés.
- El motor v0.3.0 refina estos cinco estados en dos ejes ortogonales (`observation_status` y `research_alignment`) sin modificar el baseline `v0.2.3`. La correspondencia se documenta en la especificación técnica.
- Los archivos canónicos heredados de `v0.2.3` conservan su nomenclatura histórica; se reconocen como procedencia documental, no como dependencia ni identidad del proyecto.
- El contrato de evidencia (`observation_status`, `research_alignment`, `opportunity_status`, `observation_origin`, `status_reason`) y la matriz de combinaciones válidas se definen en la especificación técnica (§ 5.3).
- En v0.3.0, `mixed` no es un valor de `EvidenceRecord.research_alignment`; la mezcla se expresa solo en `ClusterSummary` y `AnalysisRun`.

### 2.3 Estado del motor

**No implementado todavía.** El árbol `engine/` que aparece en esta especificación es una estructura propuesta, no una descripción del repositorio actual. La arquitectura y las versiones de este charter son decisiones de planificación, no entregables ya construidos.

## 3. Objetivo del producto

Producir análisis narrativos que sean:

1. **Trazables:** toda afirmación relevante queda vinculada a evidencia localizable en el texto.
2. **Explicables:** separan observación, interpretación, explicación alternativa y límite.
3. **Reproducibles:** registran versión metodológica, configuración, modelo y condiciones de análisis.
4. **Conservadores:** no transforman patrones de grupo en reglas de autoría individual.
5. **Multilingües con cautela:** permiten ampliar idiomas cuando exista evaluación adecuada para cada idioma.
6. **Privados:** no conservan ni envían textos a servicios externos por defecto.
7. **Extensibles:** permiten incorporar investigación de comprensión narrativa y coautoría sin corromper el núcleo de 30 características.

La finalidad no es prometer la detección infalible de autoría. Es estudiar decisiones narrativas, documentar evidencia y evaluar limitaciones de forma honesta.

## 4. Arquitectura objetivo del StoryScope Evidence Engine

### 4.1 Flujo principal

```text
Texto + contexto autorizado
          |
          v
1. Input & Context Gate
          |
          v
2. Narrative Extractor (interfaz lógica / entrada estructurada)
          |
          v
3. Evidence Ledger
          |
          v
4. Cluster / Double-count Resolver
          |
          v
5. Consistency & Evidence Audit
          |
          v
6. Report Generator
          |
          v
Markdown + JSON + metadatos de ejecución
```

### 4.2 Módulos

**A. Input & Context Gate**
- Identifica idioma/variedad, género, extensión, integridad y tipo de texto.
- Registra condiciones conocidas: prompt disponible, traducción, edición profesional, asistencia de IA declarada, historial de versiones y procedencia aportada.
- Aplica las reglas de adecuación y los límites de interpretación.
- No inventa condiciones desconocidas; usa `unknown`/`not provided`.

**B. Narrative Extractor (componente lógico, no implementado como generador en v0.3.0)**
- Es el punto de integración donde se producen o reciben observaciones narrativas candidatas.
- En v0.3.0 el motor no implementa ni aloja un modelo generativo propio: recibe entradas estructuradas procedentes de anotación humana, modelos externos, herramientas independientes o procesos experimentales autorizados.
- Cada candidato debe incluir la característica, la opción observada, pasajes exactos con posiciones verificables y el origen de la observación.
- El motor valida, estructura, registra, relaciona, audita y reporta; no confunde extracción con interpretación científica.
- No envía textos a servicios externos sin autorización explícita.

**C. Evidence Ledger** — prioridad máxima de v0.3.0
- Registro estructurado de característica, opción observada, estado, dirección, cita literal, offsets, explicación, alternativas, contraevidencia y límites.
- Toda cita debe poder localizarse en el texto analizado. Los validadores deterministas deben detectar citas inexistentes, offsets inválidos y valores no permitidos.
- Diferencia confianza de extracción, fuerza de evidencia y dirección narrativa. Ninguna es una probabilidad de autoría.

**D. Cluster / Double-count Resolver**
- Usa los ocho grupos operativos existentes para detectar relaciones y duplicaciones.
- Una observación compartida puede sustentar varias descripciones relacionadas, pero no generar votos independientes.
- No suma features, estados ni clusters para declarar autoría.

**E. Consistency & Evidence Audit**
- Segunda pasada enfocada en encontrar citas que no respalden la afirmación, omisiones, contraejemplos, contradicciones, doble conteo e incumplimientos de salvaguardas.
- La segunda pasada no se presenta como evaluador estadísticamente independiente si usa el mismo modelo, prompt o fuente.
- Revisión humana será necesaria para construir una referencia de calidad y resolver desacuerdos.

**F. Report Generator**
- Produce informe Markdown y registro JSON versionado.
- Incluye alcance, adecuación, observaciones, evidencia, explicaciones alternativas, contraevidencia, limitaciones y conclusión prudente.
- Nunca emite una probabilidad global de autoría ni un veredicto definitivo.

**G. Run Metadata**
- Registra ID del análisis, versión del esquema, versión de metodología/Skill, modelo y proveedor si se usó, parámetros relevantes, idioma, género, timestamp, estado de revisión y hash opcional del texto.
- No debe almacenar el texto completo en metadatos. El hash no sustituye consentimiento ni garantiza anonimato.

Los siete componentes describen responsabilidades arquitectónicas, no necesariamente siete etapas secuenciales. `Run Metadata` es información transversal de una ejecución, no un paso obligatorio del flujo.

## 5. Modelo de datos inicial

Los esquemas definitivos se diseñarán antes de programar. Como mínimo:

### AnalysisRun
- `analysis_id`
- `schema_version`
- `methodology_version`
- `skill_version`
- `language` / `language_variety`
- `genre`
- `word_count`
- `adequacy_status`
- `source_conditions` (known / unknown / not provided)
- `model_provider` / `model_id` (nullable)
- `created_at`
- `review_status`

### EvidenceRecord
- `record_id`
- `feature_id` (referencia canónica a las 30 características)
- `dimension_id`
- `observed_option`
- `evidence_state` (enum de cinco estados)
- `direction` (enum de etiquetas direccionales)
- `quotation`
- `start_offset` / `end_offset` o localizador equivalente
- `observation`
- `interpretation`
- `alternative_explanations`
- `counterevidence`
- `cluster_id`
- `extraction_confidence` (cualitativa, no calibrada salvo estudio posterior)
- `evidence_strength` (cualitativa y definida por protocolo)
- `reviewer_notes`

No se adoptarán porcentajes ni umbrales de confianza sin un protocolo de calibración y datos de evaluación. El JSON de ejemplo de conversaciones previas es ilustrativo; no es un esquema aprobado.

## 6. Investigaciones externas y cómo incorporarlas

La incorporación se realizará por utilidad y compatibilidad metodológica, no por cantidad de papers o herramientas.

### 6.1 Base principal: StoryScope

Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*, COLM 2026, arXiv:2604.03136v6.  
https://arxiv.org/abs/2604.03136  
Uso: fundamento de las dimensiones/feature patterns y de las limitaciones del enfoque. Mantener atribución exacta y no copiar datasets, pesos ni componentes no licenciados.

### 6.2 Comprensión narrativa: NarraBench

NarraBench, EACL 2026.  
https://aclanthology.org/2026.eacl-long.176/  
Uso: identificar cobertura insuficiente en comprensión narrativa y diseñar pruebas complementarias (estructura, eventos, perspectiva, revelación, relaciones). No convertir las métricas o tareas de NarraBench en señales de autoría.

### 6.3 Escritura mixta humano–IA: HACo-Det

HACo-Det, ACL 2025.  
https://aclanthology.org/2025.acl-long.1069/  
Uso: comprender segmentación/atribución fina en textos mixtos y sus dificultades. Orientar el proyecto hacia evaluación del proceso y procedencia verificable, no hacia una atribución estilística concluyente.

### 6.4 Textos mixtos y robustez: DAMASHA

DAMASHA, Findings of EACL 2026.  
https://aclanthology.org/2026.findings-eacl.326/  
Uso: estudiar segmentación interpretable y evaluación adversarial. No afirmar que el motor obtiene el rendimiento de ese método.

### 6.5 Español y traducción

La adaptación española seguirá siendo experimental hasta contar con corpus autorizado, diversidad de géneros, autores, longitudes y condiciones de edición. Los resultados en inglés no se transferirán automáticamente al español. Toda nueva fuente se verificará, fechará y registrará con idioma, población, tarea y limitaciones.

### 6.6 Regla de actualización de investigación

Antes de añadir una dimensión, feature, detector, modelo o dependencia:
1. Identificar qué problema no resuelto atiende.
2. Buscar literatura reciente y fuentes primarias.
3. Verificar licencia, datos, idioma, dominio, diseño experimental y limitaciones.
4. Distinguir hallazgo publicado, hipótesis de StoryScope y decisión de ingeniería.
5. Diseñar una prueba que pueda demostrar utilidad o permitir descartar la propuesta.
6. Incorporar solo si mejora utilidad, trazabilidad, calidad o reproducibilidad sin quebrantar salvaguardas.

## 7. Estrategia de tecnología

### Adoptar ahora
- OpenCode como entorno/agente principal de desarrollo.
- Agent Skills para conservar la capacidad instalada y portable.
- Python + biblioteca estándar para validadores y componentes iniciales.
- JSON Schema o contrato JSON versionado para intercambiar resultados.
- Markdown/JSON como salidas.
- Pytest o validadores deterministas equivalentes cuando el entorno ya lo permita.
- GitHub Actions para CI siguiendo el patrón probado del repositorio actual.
- Una metodología de pruebas ligera y reproducible, sin necesidad de crear otro framework.
- Documentación curada, por ejemplo con Obsidian.

### Evaluar después, mediante benchmark
- Qwen local/Ollama y llama.cpp como opciones de inferencia.
- Otros modelos cloud/local como adaptadores opcionales y sujetos a privacidad/costo.
- Un selector de proveedores cuando haya al menos más de un proveedor real que necesite selección común.
- MCP cuando exista una necesidad de consumo por más de un cliente o herramienta.

### Posponer o descartar por ahora
- Bot de Telegram, aplicación web, Open WebUI o interfaz visual dedicada.
- Goose, Cline, OpenHands, Hermes y varios frameworks de orquestación simultáneos.
- Hindsight como memoria de historias; las narrativas no se almacenarán por defecto.
- Graphify para analizar contenido narrativo; puede ser útil en análisis del código, no es parte del motor.
- Pipelines de imagen/vídeo/3D y herramientas no relacionadas.
- Clasificador supervisado de autoría antes de contar con datos autorizados y una evaluación válida.

El hardware documentado históricamente es limitado (HP Ryzen 5 5500U con 8 GB de RAM, gráfica integrada). No se debe asumir capacidad para modelos grandes. Confirmar hardware actual antes de decidir runtime o descargas.

## 8. Independencia respecto de sistemas externos

**Decisión: no acoplar ni integrar ahora.**

StoryScope debe poder ejecutarse de forma independiente, sin depender de planos de control, identidades, repositorios o servicios de otros proyectos. Si en el futuro existiera un caso de uso justificado, se diseñará un adaptador periférico con contrato explícito para que un sistema externo administre identidad, autorización, tareas, ejecución, persistencia operacional y auditoría. El motor devolverá resultados versionados y evidencia; el sistema externo no interpretará la semántica narrativa.

Condiciones previas:
- Verificar el estado real del sistema externo y su revisión exacta; no asumir que los informes históricos equivalen al checkout actual.
- Revisar contratos y mecanismos de aislamiento, permisos, idempotencia, trazabilidad y manejo de errores.
- Especificar API/adaptador y pruebas de integración en una propuesta independiente.
- No alterar contratos, esquemas, migraciones, datos ni componentes protegidos de otros proyectos sin autorización específica.

## 9. Hoja de ruta propuesta

### v0.3.0 — Evidence Engine (primera prioridad)
- Definir y versionar esquemas `AnalysisRun` y `EvidenceRecord`.
- Implementar Input & Context Gate.
- Implementar registro de evidencia con citas y offsets validables.
- Incorporar los 30 features actuales sin alterar valores ni dirección publicados.
- Implementar controles de estados, etiquetas, ausencias y doble conteo.
- Añadir segunda pasada de auditoría y pruebas de regresión.
- Generar Markdown/JSON.
- Mantener la Skill v0.2.3 utilizable; el motor no debe ser requisito para cargarla.

### v0.3.1 — Narrative Workbench
- Mejorar comparación de borradores y versiones.
- Añadir comparación de análisis, diferencias y reporte de cambios.
- Añadir metadatos de proceso cuando sean aportados/consentidos.
- No atribuir fragmentos si no existe procedencia verificable.

### v0.4.0 — Research & Evaluation Lab
- Construir protocolo español y piloto autorizado.
- Crear guía de anotación humana y proceso de adjudicación.
- Medir acuerdo interanotador, precisión de citas, consistencia entre corridas, robustez a traducción/edición y fallos por género/extensión.
- Crear test set separado y control de fuga entre autores/prompts/versiones.
- Comparar modelos con tareas idénticas; no confundir benchmark de proveedor con desempeño real del motor.

### v0.5.0 — Adaptador externo (condicional)
- Solo si existe un sistema externo consolidado y un caso real justifica la integración.
- Adaptador desacoplado; interfaz, permisos y auditoría acordados.

### v1.0.0 — plataforma estable (condicional)
- Solo tras evaluación empírica, documentación reproducible, gestión de privacidad, pruebas de regresión y estabilidad de esquemas.
- La numeración es una hoja de ruta, no una promesa de fechas ni una autorización de release.

## 10. Criterios de aceptación iniciales de v0.3.0

v0.3.0 no se considerará aceptada si solo produce texto más largo. Debe demostrar al menos:

1. Cada cita se localiza de manera determinista en la fuente.
2. Todos los estados y etiquetas pertenecen a enumeraciones válidas.
3. Una característica ausente no se usa como prueba de autoría.
4. No se produce puntuación agregada ni probabilidad de autoría.
5. Se conserva la separación de características y opciones.
6. El control de clusters evita el doble conteo.
7. Las interpretaciones incluyen alternativas y contraevidencia cuando corresponde.
8. La auditoría marca afirmaciones sin respaldo o con citas insuficientes.
9. Se puede reconstruir la metodología y configuración de cada corrida.
10. El informe explicita idioma, género, extensión, adecuación y limitaciones.
11. Los fixtures incluyen casos cortos, textos ambiguos, opciones mixtas, traducción/edición declaradas y evidencia insuficiente.
12. La versión publicada v0.2.3 permanece intacta y sus pruebas/regresión siguen aprobadas.

Los valores cuantitativos de aceptación se fijarán solo después de diseñar un piloto y una guía de anotación; no se inventarán objetivos de precisión antes de medir una línea base.

## 11. Privacidad, seguridad y límites de uso

- Analizar únicamente textos proporcionados o autorizados para ese propósito.
- No enviar narrativas a servicios externos sin autorización explícita y aviso del proveedor.
- No conservar el texto completo por defecto; definir borrado y retención antes de crear almacenamiento persistente.
- No usar narrativas privadas para entrenamiento, benchmarking compartido o publicación sin consentimiento y permisos/licencias adecuados.
- Separar datos de texto, identificadores personales y metadatos de análisis.
- No convertir el resultado en prueba pericial, herramienta disciplinaria, selección laboral, juicio legal o decisión de alto impacto.
- No presentar como certeza la autoría o procedencia inferida por estilo.
- No crear modos para evadir detectores.

### 11.1 Falsos positivos y límites de inferencia

- Un texto escrito por una persona puede presentar características asociadas con patrones observados en textos de IA.
- Una característica aislada no permite determinar la autoría.
- La edición profesional, la traducción, la corrección gramatical, las restricciones de género y el estilo pueden modificar las señales observables.
- El sistema no garantiza detectar todos los textos generados por IA.
- El sistema tampoco garantiza evitar clasificar erróneamente textos humanos.
- Los resultados son análisis descriptivos y exploratorios, no pruebas de autoría.
- StoryScope no debe utilizarse como fundamento único de calificación académica, sanción disciplinaria, contratación, decisiones legales ni procedimientos forenses.
- No se inventan tasas de falsos positivos: cualquier estimación requerirá un protocolo de evaluación y datos autorizados.

## 12. Autonomía asistida y autoridad del propietario

El propietario del proyecto puede delegar tareas de investigación, redacción y análisis en herramientas de asistencia. Estas herramientas son instrumentos: la autoridad final sobre el alcance, las decisiones y la publicación corresponde al propietario del proyecto.

La delegación significa que la herramienta de asistencia debe:
- Investigar literatura científica y tecnología vigente cuando una decisión dependa de información reciente o especializada.
- Comparar alternativas y recomendar una decisión, no limitarse a enumerar opciones.
- Rechazar complejidad, herramientas o features que no aporten valor demostrado.
- Priorizar calidad metodológica, trazabilidad, privacidad, reproducibilidad, mantenimiento y coste total.
- Proponer mejoras no solicitadas cuando estén directamente justificadas por evidencia y encajen con el objetivo.
- Mantener un registro de decisiones, versiones, evidencia y temas pendientes.
- Distinguir expresamente hechos verificados, resultados publicados, inferencias, hipótesis y propuestas.

Esta autonomía **no** autoriza automáticamente:
- Commit, push, merge, release, cambios de visibilidad o publicación externa.
- Borrados, migraciones reales, cambios de datos o despliegues.
- Envío de narrativas privadas a servicios externos o uso de datos sin autorización.
- Cambios al tag/release `v0.2.3` o reescritura de su historia.
- Alteraciones de sistemas externos, sus contratos protegidos o sus fases sin autorización de ingeniería separada.
- Gastos, suscripciones, compra de hardware o instalación masiva de herramientas.

Para trabajo futuro, el asistente puede decidir el mejor diseño y priorización dentro del objetivo aprobado, pero debe respetar estas fronteras de seguridad, privacidad y gobierno técnico.

## 13. Próximo paso de continuidad

1. Leer este charter y el registro de continuidad del proyecto.
2. Revalidar en vivo el repositorio público y, cuando se trabaje localmente, el checkout real.
3. Realizar una investigación de brechas de v0.3.0 y convertir el diseño del Evidence Ledger en contratos concretos.
4. Preparar especificación `v0.3.0` antes de modificar código.
5. Implementar en una rama de trabajo aislada, preservando `v0.2.3`.
6. Ejecutar pruebas y reportar hallazgos; no publicar sin instrucción correspondiente.

---

## Fuentes de referencia principales

- Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*, COLM 2026, arXiv:2604.03136v6. https://arxiv.org/abs/2604.03136
- NarraBench, EACL 2026. https://aclanthology.org/2026.eacl-long.176/
- HACo-Det, ACL 2025. https://aclanthology.org/2025.acl-long.1069/
- DAMASHA, Findings of EACL 2026. https://aclanthology.org/2026.findings-eacl.326/
- Repositorio independiente de StoryScope. https://github.com/liongrimsoul78/storyscope-human-ai-analysis
- Release estable `v0.2.3`. https://github.com/liongrimsoul78/storyscope-human-ai-analysis/releases/tag/v0.2.3
