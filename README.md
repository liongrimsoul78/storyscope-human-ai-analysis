# StoryScope Human–AI Analysis — LION LAB Skill v0.2.3

Skill cualitativa, multilingüe y compatible con OpenCode / Agent Skills. La v0.2.3 es una actualización de mantenimiento documental, científico y de validación. Corrige la cita de los valores numéricos (Tabla 15 → Tabla 16), documenta las diferencias entre los gaps publicados y la resta de los valores mostrados, corrige la fila `Reference Explicitness` (`balanced mix`) y amplía el validador a las 30 características. Conserva todas las salvaguardas metodológicas y los valores corregidos en versiones anteriores.

## Base científica y atribución

- **Nombre del proyecto:** StoryScope Human-AI Analysis.
- **Autoría de la Skill:** LION LAB.
- **Base científica:** StoryScope, Russell et al., COLM 2026, arXiv:2604.03136.
- **Implementación independiente:** esta Skill es una implementación y extensión independiente de LION LAB inspirada en el marco de investigación StoryScope.
- **Sin afiliación oficial:** no es el repositorio ni la implementación oficial de los autores de la investigación.
- **Uso responsable:** no debe presentarse como un detector infalible de IA ni como prueba definitiva de autoría humana o de IA. Sus conclusiones son señales analíticas basadas en evidencia, con incertidumbre explícita.

La procedencia, las licencias y los límites de reutilización se detallan en `THIRD_PARTY_NOTICES.md`.

## Contenido

- `SKILL.md`: misión, modos, puerta de adecuación, estados de evidencia, dimensiones, autoauditoría y formato obligatorio.
- `references/research-basis.md`: fuente académica y límites empíricos.
- `references/core-patterns.md`: 30 características centrales en los patrones publicados.
- `references/feature-dimension-map.csv`: mapa de características, dimensiones y valores de las Tablas 14–16.
- `references/evidence-status.md`: taxonomía operativa de cinco estados y regla de ausencia.
- `references/cluster-map.md`: agrupación LION LAB para prevenir doble conteo (no oficial de StoryScope).
- `references/spanish-adaptation.md`: cautelas de español y traducción.
- `references/audit-resolution.md` y `references/audit-second-pass.md`: trazabilidad de auditorías previas.
- `references/data-integrity-v0.2.2.md`: documento histórico de correcciones de datos y fuente tabular; la cita numérica se corrigió a Tabla 16 en v0.2.3.
- `references/numeric-integrity-v0.2.3.md`: transcripción, excepciones de redondeo y alcance de la validación numérica.
- `references/report-template.md`: formato obligatorio de siete secciones.
- `references/worked-examples/01-microrelato-21-palabras.md`: caso de regresión para garantizar “evidencia insuficiente”.
- `validation/validate_feature_map.py`: validador sin dependencias externas de las 30 características, 33 opciones, direcciones y gaps publicados.
- `validation/table16_expected.json`: transcripción canónica de la Tabla 16 usada por el validador.
- `validation/check_source_table16.py` y `validation/source_table16_v6.txt`: verificación independiente por característica y opción contra una extracción literal de la Tabla 16.
- `validation/verify_manifest.py`: verificación SHA-256 del manifiesto.
- `validation/test_acceptance.py`: pruebas positivas y negativas A–G.
- `CHANGELOG.md`: cambios de versión.
- `LICENSE`, `LICENSE-DOCS` y `LICENSE-DATA`: licencias del código, la documentación original y los datos derivados.
- `THIRD_PARTY_NOTICES.md`: atribución y procedencia de material de terceros.
- `.github/workflows/ci.yml`: validación automática en GitHub Actions.

## Instalación desde GitHub

Requisitos: OpenCode (o un agente compatible con Agent Skills) y `git`. La Skill no necesita dependencias Python para su uso normal; los validadores solo usan la biblioteca estándar.

1. Cierra OpenCode.
2. Clona el repositorio dentro del directorio de Skills de OpenCode.

En Windows (PowerShell):

```powershell
$skills = Join-Path $HOME ".config\opencode\skills"
New-Item -ItemType Directory -Force -Path $skills | Out-Null
git clone https://github.com/liongrimsoul78/storyscope-human-ai-analysis.git (Join-Path $skills "storyscope-human-ai-analysis")
```

En macOS o Linux:

```bash
mkdir -p "$HOME/.config/opencode/skills"
git clone https://github.com/liongrimsoul78/storyscope-human-ai-analysis.git \
  "$HOME/.config/opencode/skills/storyscope-human-ai-analysis"
```


La Skill debe quedar en `~/.config/opencode/skills/storyscope-human-ai-analysis/` (en Windows, `$HOME\.config\opencode\skills\storyscope-human-ai-analysis\`), con `SKILL.md` en la raíz de esa carpeta.

3. Verifica la instalación desde el directorio de la Skill:

```bash
cd "$HOME/.config/opencode/skills/storyscope-human-ai-analysis"
python3 validation/verify_manifest.py --strict
```

En Windows, usa `py -3 .\validation\verify_manifest.py --strict` si `python3` no está disponible.

4. Reinicia OpenCode e inicia una sesión nueva para que la Skill se indexe.

Para actualizar una copia existente:

```bash
cd "$HOME/.config/opencode/skills/storyscope-human-ai-analysis"
git pull --ff-only
```

Los respaldos locales, si existen, deben mantenerse fuera del directorio que OpenCode indexa como Skills; por ejemplo, en `~/.config/opencode/skill-backups/` (Windows: `$HOME\.config\opencode\skill-backups\`). No forman parte del repositorio.

## Uso

En un mensaje de OpenCode:

```text
@storyscope-human-ai-analysis
Analiza este texto con StoryScope v0.2.3. Respeta la puerta de longitud/género,
los cinco estados de evidencia, los clústeres y el auto-chequeo obligatorio.
```

## Integridad de los datos

Ejecuta el validador de mantenimiento desde el directorio de la Skill:

```bash
python3 validation/validate_feature_map.py
```

Debe informar 30 características, 33 comprobaciones de opción, 30 nombres únicos y 9 excepciones de redondeo documentadas, sin discrepancias.

En Windows, el comando principal es:

```powershell
py -3 .\validation\validate_feature_map.py
```

Si `python` está disponible en `PATH`, también puede usarse `python .\validation\validate_feature_map.py`. En una instalación de Windows donde `python` apunta al alias de Microsoft Store, ese comando puede fallar con el código 9009; en ese caso usa `py -3`.

Verifica también el manifiesto y la fuente:

```bash
python3 validation/verify_manifest.py --strict
python3 validation/check_source_table16.py
python3 validation/test_acceptance.py
```

La comprobación de fuente compara cada característica y opción por nombre contra la extracción literal de la Tabla 16; no se limita a comparar un conjunto de valores.

## Integración continua

`.github/workflows/ci.yml` ejecuta en cada `push` y `pull request` los cuatro controles anteriores en Ubuntu y Windows con Python 3.12:

- `validation/validate_feature_map.py`
- `validation/check_source_table16.py`
- `validation/verify_manifest.py --strict`
- `validation/test_acceptance.py`

El flujo solo necesita permisos de lectura sobre el repositorio y no realiza llamadas de red desde los validadores.

## Licencias

- **Código original de LION LAB:** MIT. Ver `LICENSE`.
- **Documentación original de LION LAB:** CC BY 4.0. Ver `LICENSE-DOCS`.
- **Datos derivados y transcripciones de material CC0:** CC0 1.0, en el alcance descrito en `LICENSE-DATA`.
- **Material de terceros:** se rige por sus propias licencias y se documenta en `THIRD_PARTY_NOTICES.md`. Las licencias de LION LAB no se aplican a material que pertenece a terceros.

## Importante

- Es una Skill de instrucciones, no un clasificador estadístico.
- No necesita dependencias Python ni llamadas de red para su uso normal. Los validadores incluidos utilizan solo la biblioteca estándar de Python.
- No contiene el corpus Books3, los pesos XGBoost ni el pipeline original.
- Los valores numéricos de las 30 características están en la **Tabla 16**; la **Tabla 15** solo enumera las 13 características human-characterizing y sus opciones de respuesta.
- Los gaps publicados se conservan tal como aparecen en el artículo. Las diferencias aparentes con la resta de los valores mostrados están documentadas en `references/numeric-integrity-v0.2.3.md`; no se alteran los datos para forzar consistencia aritmética ni se infiere la causa de la diferencia.
- El umbral interno de 500 palabras es una salvaguarda LION LAB, no un umbral del artículo.
- La adaptación al español no está validada estadísticamente.
- Esta Skill no requiere ni modifica una instalación local preexistente de LION LAB. Cualquier integración con LION CORE debe decidirse y revisarse por separado.
