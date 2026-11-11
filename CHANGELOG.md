# Changelog

## Sin publicar — preparación de publicación

- Migra `README.md` de la instalación mediante ZIP local a `git clone` desde GitHub, con la ubicación de la Skill en OpenCode para Windows, macOS y Linux.
- Generaliza las rutas locales y los respaldos a rutas relativas al entorno (`$HOME`, `~`); elimina referencias a una instalación local concreta.
- Añade `LICENSE` (MIT) para el código original de LION LAB, `LICENSE-DOCS` (CC BY 4.0) para su documentación original y `LICENSE-DATA` (CC0 1.0) para las transcripciones derivadas que correspondan a material CC0.
- Añade `THIRD_PARTY_NOTICES.md` con la cita de Russell et al., la licencia CC0 1.0 del paper, el repositorio oficial y su licencia MIT, y la declaración de que esta Skill no es una implementación oficial.
- Añade `.github/workflows/ci.yml` para ejecutar los validadores y las pruebas de aceptación en Ubuntu y Windows.
- Añade `.gitignore` para artefactos de Python, sistemas operativos, editores, archivos ZIP y respaldos locales.
- Actualiza `MANIFEST_SHA256SUMS.txt` para incluir los archivos nuevos y los hashes modificados.
- Excluye de la distribución pública el informe interno de auditoría y la utilidad local de respaldo; ambos se conservan fuera del árbol del repositorio y no forman parte del manifiesto.
- Ajusta las pruebas de empaquetado en `validation/test_acceptance.py`: la comprobación del README pasa de ZIP a `git clone` y se retira la prueba específica del script local de respaldos, que ya no forma parte de la distribución pública. No se modifica ninguna aserción científica, de datos, de características, opciones, direcciones ni gaps.
- No cambia la lógica científica, las 30 características, los valores Human/AI, los gaps, las 33 opciones, las excepciones de redondeo ni los validadores de datos.

## 0.2.3 — 2026-11-09

- Corrige la referencia científica de los valores numéricos: la **Tabla 15** enumera las 13 características human-characterizing y sus opciones; los valores Human/AI/Gap de las 30 características están en la **Tabla 16**. Se conservan las referencias legítimas a la Tabla 15.
- Corrige la fila `Reference Explicitness` (`balanced mix`): los valores publicados son Human 37% / AI 16% / Gap +21, no 16% / 37%. Es una sexta corrección de datos detectada en la auditoría v0.2.3; los cinco valores corregidos en v0.2.2 permanecen correctos.
- Normaliza la representación de las tres filas compuestas (`Dominant Emotional Expression`, `Subplot Integration`, `Reference Explicitness`) para que los gaps publicados conserven su signo y etiqueta. No se alteran los valores Human/AI salvo la corrección de `Reference Explicitness`.
- Documenta nueve excepciones de redondeo entre los gaps publicados y la resta de los valores ya redondeados. Los datos originales no se modifican para forzar consistencia aritmética.
- Amplía `validation/validate_feature_map.py` para comprobar las 30 características, 33 opciones, nombres, unicidad, valores Human, valores AI, dirección y gaps publicados, con excepciones de redondeo documentadas.
- Añade `validation/check_source_table16.py` y `validation/source_table16_v6.txt`: verificación independiente que compara cada característica y opción por nombre y valor contra la extracción literal de la Tabla 16, no solo un conjunto de triples.
- Añade `validation/table16_expected.json`, `validation/verify_manifest.py` y `validation/test_acceptance.py`.
- Convierte el script local de migración de respaldos en un script solo de copia y verificación: elimina `-Force` y cualquier `Remove-Item`; si el destino existe, verifica sus hashes sin sobrescribirlo ni eliminarlo, y conserva siempre los dos originales.
- Ajusta la documentación de redondeos: los valores y gaps publicados se conservan, pero no se atribuye la diferencia a valores sin redondear porque la Tabla 16 no documenta esa causa.
- Corrige la errata `300/500/1.000-word gates`; los umbrales definidos son menos de 500, 500–999 y 1.000 o más.
- Corrige el metadato de idioma de `SKILL.md` para reflejar instrucciones en inglés y documentación en español.
- Actualiza la revisión de `research-basis.md` y alinea `README.md`, `CHANGELOG.md` y los documentos de integridad.
- Documenta `py -3 .\validation\validate_feature_map.py` como comando principal en Windows y `python` como alternativa cuando esté disponible en `PATH`.
- Prepara el traslado de los respaldos a una carpeta de respaldos fuera del directorio de Skills de OpenCode, sin borrar los originales.
- No modifica el marco metodológico, las reglas de evidencia ni la calibración del microrelato de 21 palabras.

## 0.2.2 — 2026-11-09

- Corrige cinco filas invertidas en `references/feature-dimension-map.csv`: Frequency of Direct Reader Address, Fourth-Wall Permeability, Location Variety Scope, Moral Polarity Toward Protagonist y Nonlinear Framing for Delayed Disclosure.
- Los valores humano/IA ahora coinciden con la Tabla 16 del PDF v6 del artículo; los gaps Human − AI y las direcciones se mantienen coherentes. (La entrada original citaba la Tabla 15; la cita se corrigió en v0.2.3.)
- Añade una nota de trazabilidad de datos y un validador reproducible de integridad para evitar que estas inversiones regresen.
- No modifica el marco metodológico, las reglas de evidencia ni la calibración del microrelato de la v0.2.1.

## 0.2.1 — 2026-11-08

- Reconcilia el corpus: 10.272 historias humanas + 51.336 historias IA = 61.608 historias efectivas. El máximo teórico era 61.632; el artículo indica 24 generaciones rechazadas.
- Precisa la longitud media: 4.753 palabras exactas en la sección 2.1, nota 8; el abstract la redondea a aproximadamente 5.000.
- Prohíbe inferir “español general” u otra variedad cuando no se declara o no hay evidencia suficiente; el informe debe decir `no especificada / no determinable`.
- Añade una segunda resolución de auditoría y amplía la autoauditoría y la plantilla.

## 0.2.0 — 2026-11-08

- Añade una taxonomía obligatoria de cinco estados de evidencia: presente-alineado, presente-opuesto, ausente, no aplicable, no evaluable.
- Prohíbe convertir ausencias en indicadores humanos/IA sin oportunidad suficiente y valor explícito.
- Añade puerta conservadora de longitud/género; umbrales claramente marcados como salvaguardas LION LAB, no resultados del artículo.
- Añade ocho clústeres operativos para evitar doble conteo y aclara que no son clústeres oficiales del paper.
- Añade crosswalk de 30 características únicas con dimensiones publicadas, mediciones y cautelas; aclara las tres variables con opciones que aparecen en ambos listados.
- Separa Style taxonómico de las señales superficiales y prohíbe recontabilizarlas.
- Añade protocolo específico para español y traducción.
- Añade autoauditoría obligatoria y ejemplo de calibración negativa del microrelato de 21 palabras.
- Documenta la resolución de los hallazgos de auditoría en `references/audit-resolution.md`.
- Actualiza la plantilla de salida obligatoria a siete secciones.

## 0.1.0

- Primera versión cualitativa inspirada en StoryScope.
