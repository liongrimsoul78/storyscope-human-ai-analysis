# StoryScope v0.3.0 design pack — review 0.1.1

Este paquete contiene documentos de diseño, no código de motor implementado.

## Contenido
- `PROJECT_CHARTER_v0.1.md`
- `TECHNICAL_SPEC_v0.1.md`
- `FEATURE_REGISTRY_v0.1.1_draft.json`
- `FEATURE_REGISTRY_REVIEW_NOTES_v0.1.1.md`
- `README_IMPORT.md`

## Importación
Copiar la carpeta `docs/design/v0.3.0/` al repositorio de desarrollo `storyscope-human-ai-analysis`.

## Integridad y límites
- No reemplazar `SKILL.md`, `README.md`, `references/` ni `validation/`.
- Los IDs `ssha.*` son identificadores internos de StoryScope Human–AI Analysis; no son IDs oficiales de la investigación original.
- 30 características, 33 patrones/opciones, 10 dimensiones y 8 clústeres se cotejaron con los archivos canónicos del `main` observado.
- AI-elevated patterns citan Table 14 + Table 16; Human-elevated patterns citan Table 15 + Table 16.
- Los 30 nombres, dimensiones, patrones y cautelas se compararon contra el CSV/fixture/cluster map.
- Las comprobaciones estructurales de esta revisión se realizaron ad hoc; incorporar un validador reproducible al repositorio y probarlo en CI será una tarea independiente.
- No crear scores ni probabilidades de autoría. El motor no está implementado.
- La release/tag `v0.2.3` permanece inalterada.
- Los archivos canónicos heredados de `v0.2.3` conservan nomenclatura histórica; se reconocen como procedencia documental, no como dependencia ni identidad del proyecto.
- StoryScope Human–AI Analysis es un proyecto individual, independiente y autónomo.
