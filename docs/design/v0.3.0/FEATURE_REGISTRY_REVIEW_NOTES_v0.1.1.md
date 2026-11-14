# Feature Registry — notas de revisión v0.1.1

**Proyecto:** StoryScope Human–AI Analysis — Evidence Engine  
**Fecha:** 12 de noviembre de 2026  
**Estado:** borrador revisado mediante comparación automatizada con el checkout público `main` observado durante esta revisión; pendiente de aprobación como registro canónico en el proyecto.

## Resultado de la validación cruzada

| Control | Resultado |
|---|---:|
| Características únicas | 30/30 exactas contra `feature-dimension-map.csv` |
| Características de Table 16 | 30/30 exactas |
| Patrones/opciones de referencia | 33/33 |
| Dimensiones | 10 |
| Clústeres operativos de StoryScope | 8 |
| Códigos y nombres de dimensión | 30/30 coinciden |
| Clúster asignado por característica | 30/30 coinciden con el mapa operativo |
| Cautelas interpretativas | 30/30 coinciden con CSV |
| IDs internos de feature | 30 únicos |
| IDs internos de patrón | 33 únicos |
| JSON | Parseo correcto |

La comparación se hizo contra los archivos canónicos recuperados de `main` del repositorio `liongrimsoul78/storyscope-human-ai-analysis`, usando el mapa CSV, `table16_expected.json` y `cluster-map.md`. Los validadores originales de v0.2.3 continúan siendo la autoridad para la transcripción numérica y no fueron modificados.

## Corrección incorporada en v0.1.1

El borrador v0.1.0 asignaba indiscriminadamente `Table 14`, `Table 15` y `Table 16` a todos los patrones. Esa referencia era demasiado amplia y no reflejaba la organización del artículo.

La procedencia ahora se registra por dirección:
- `pattern_ai`: `Table 14` (rasgo/opción elevada para IA) + `Table 16` (valores humano/IA y gap).
- `pattern_human`: `Table 15` (rasgo/opción elevada para humanos) + `Table 16` (valores humano/IA y gap).
- `Table 16` contiene los valores para las 30 características.

La versión HTML v6 del artículo confirma que Table 14 enumera 20 características AI-characterizing, Table 15 enumera 13 human-characterizing y Table 16 presenta las 30 características con medias/prevalencias y gaps. Fuente primaria: https://arxiv.org/html/2604.03136v6, Appendix I, líneas de tablas 14–16.

## IDs y estado de la taxonomía

- `feature_id`: `ssha.feature.<slug>`.
- `pattern_id`: `ssha.pattern.<feature_slug>.<pattern_slug>`.
- Son identificadores internos de StoryScope Human–AI Analysis, no IDs oficiales de la investigación original.
- No se inventan ni infieren IDs oficiales. Un crosswalk futuro requiere fijar una revisión exacta del `taxonomy.json` oficial y validar cada correspondencia de manera individual.
- Las 33 referencias de patrón representan direcciones/opciones; no son 33 características.
- Los valores numéricos de Table 16 no se duplican en este registro. La fuente canónica sigue siendo `validation/table16_expected.json`.

## Cobertura dimensional

El mapa de 30 características centrales asigna:

| Dimensión | Características |
|---|---:|
| Agents | 2 |
| Social networks | 0 |
| Style | 0 |
| Plot | 4 |
| Setting | 7 |
| Events | 2 |
| Revelation | 3 |
| Situatedness | 6 |
| Temporal structure | 2 |
| Perspective | 4 |

Esto no significa que Social networks o Style estén ausentes del marco científico de diez dimensiones. Significa únicamente que el crosswalk central actual no contiene features con dirección asignadas a esas dos dimensiones. El motor puede describirlas cualitativamente, sin inventar señales direccionales.

## Controles de doble conteo

- Cada característica aparece una sola vez en un clúster operativo de StoryScope.
- `Dominant Emotional Expression`, `Reference Explicitness` y `Subplot Integration` conservan sus valores alternativos dentro de la misma característica.
- Los ocho clústeres son una estructura operativa de StoryScope, no clústeres oficiales de la investigación original.
- El registry incluye `display_name_es` para cada clúster operativo, de modo que la correspondencia bilingüe sea inequívoca.
- Cinco características no disponen de opciones numéricas propias en Table 16 (`Character Introduction`, `Dialogue Function`, `Mode of Resolution`, `Intertextual Strategy Types`, `Moral Polarity Toward Protagonist`). Sus etiquetas direccionales se sustentan en los archivos canónicos de características y en las Tablas 14/15; no se inventan valores numéricos.
- No se suman características, patrones ni clústeres para crear un score o probabilidad de autoría.

## Decisiones de Fase 1.4 (contrato de evidencia)

- `neutral` y `not_assessed` se definen de forma disjunta: `neutral` es neutralidad evaluada; `not_assessed` es ausencia de valoraci?n.
- `opportunity_status` se define operativamente (`sufficient`, `limited`, `none`, `unknown`) y condiciona `not_observed`.
- `observation_origin` registra la procedencia de cada observaci?n (anotaci?n humana, modelo externo, herramienta independiente, experimento autorizado).
- `alignment_basis` se define con sus cuatro valores; `alignment_basis_detail` conserva la justificaci?n contextual auditada.
- Las caracter?sticas bidireccionales (`Dominant Emotional Expression`, `Subplot Integration`, `Reference Explicitness`) se resuelven mediante `reference_pattern_id` y el registro, sin campo adicional.
- `mixed` se restringe a `ClusterSummary` o a registros vinculados; no a registros at?micos aislados.
- Los valores categ?ricos expl?citos de ausencia se registran como `observed` con su opci?n can?nica, no como `not_observed`.
- La matriz de 14 combinaciones v?lidas/inv?lidas se documenta en la especificaci?n (?5.3.6).
- El exportador de compatibilidad hacia los cinco estados hist?ricos sigue pendiente; no se fuerza conversi?n sin equivalencia.

- `mixed` se elimina del enum de `EvidenceRecord.research_alignment` (Fase 1.5.2, Alternativa A); solo `ClusterSummary` y `AnalysisRun`.

## Pendientes antes de congelar el registro

1. Incorporar este borrador a la rama de desarrollo, no a la release estable.
2. Añadir un validador automatizado que reproduzca los controles anteriores usando archivos locales canónicos.
3. Ejecutar el validador y toda la suite actual en CI Windows y Ubuntu.
4. Revisar el contrato de esquema JSON y la política de evolución de IDs.
5. Aceptar el registro solo tras revisión de los diffs y de las pruebas.

Las comprobaciones estructurales de esta revisión se realizaron ad hoc. Su automatización reproducible será una tarea independiente y no se presenta como integrada en CI.

Los archivos canónicos heredados de `v0.2.3` conservan nomenclatura histórica; se reconocen como procedencia documental, no como dependencia ni identidad del proyecto.

**No es una implementación del motor.** El registro continúa en estado `draft_for_review` y no autoriza clasificación, scoring ni inferencia automática de autoría.
