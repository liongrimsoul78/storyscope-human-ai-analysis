---
name: storyscope-human-ai-analysis
description: Analyze human-versus-AI writing patterns with a cautious StoryScope-inspired method. Profile narrative decisions, distinguish narrative structure from surface language, assess evidence states, compare matched texts, and explain uncertainty. Do not infer authorship from absence or short samples.
compatibility: OpenCode and Agent Skills-compatible agents; qualitative use requires no external tools or Python packages.
metadata:
  author: LION LAB
  version: "0.2.3"
  source_research: "Russell et al., StoryScope, COLM 2026, arXiv:2604.03136v6"
  language: "English instructions; Spanish documentation; multilingual analysis with language-specific caveats"
---

# StoryScope Human–AI Writing Analysis

## 1. Mission and scope

Apply a **qualitative, StoryScope-inspired reading framework** to observable narrative decisions and prose choices. It is not the official StoryScope pipeline, trained classifier, or taxonomy implementation. Never state or imply that you executed the original XGBoost classifier, reproduced its scores, or know the actual provenance of a text.

The research asks whether discourse-level narrative choices can distinguish human-written and LLM-generated **English-language fiction in a controlled corpus**. The central distinction is:

- **Narrative/discourse structure:** agents, goals, agency, causal chains, plot, setting, revelation, temporal order, perspective, reader positioning, and intertextuality.
- **Surface language/style:** diction, syntax, sentence rhythm, repetition, register, figurative density, transitions, and other sentence-level patterns.

Keep these tracks separate. A surface-language observation must not be counted again as a narrative feature. The taxonomy's `Style` dimension may be described, but do not add it as a second independent signal when the same stylistic evidence has already been recorded.

## 2. Non-negotiable epistemic rules

1. **No authorship verdict.** Textual patterns cannot prove that a person or model wrote a text. Consider human, AI, AI-assisted, translated, edited, templated, imitated, dictated, and jointly authored possibilities.
2. **No invented probabilities or detector scores.** Do not produce a percentage, posterior probability, certainty score, or threshold from qualitative observations.
3. **No single-cue conclusion.** A linear plot, a moralizing sentence, sensory detail, polished grammar, an em dash, or a stock transition is not decisive.
4. **No absence-as-evidence shortcut.** Follow the evidence-state decision tree in `references/evidence-status.md` before assigning direction.
5. **No double-counting.** Group correlated observations by the operational clusters in `references/cluster-map.md`. One underlying narrative choice counts as one cluster-level observation, even if several related feature descriptions capture it.
6. **Context before direction.** Assess length, genre, language, prompt, audience, translation, editing, and constraints before interpreting a feature.
7. **Evidence before interpretation.** Cite a short quotation or precise location for each important claim. Keep observation, interpretation, alternative explanation, and confidence distinct.
8. **No artificial humanization.** Do not insert fake mistakes, random irregularities, invented anecdotes, arbitrary flashbacks, or unnecessary subplots to make text appear human.
9. **No detector evasion.** Revisions should improve specificity, clarity, voice, factual grounding, and authorial intent, not bypass AI detectors.
10. **No forensic or high-stakes use.** This is not a disciplinary, hiring, grading, legal, plagiarism, or forensic authorship tool.
11. **Preserve the author's intent.** Do not alter facts, citations, dialect, register, identity, or intended meaning unless explicitly asked.
12. **Privacy.** Analyze only supplied or authorized text. Do not send it to external services, APIs, or online detectors unless the user explicitly authorizes that action.

## 3. Choose a mode

Infer the mode from the request. Ask at most one concise question only when a missing fact materially changes the task; otherwise state assumptions.

- **A — Narrative profile:** fiction, story, novel excerpt, script, scene. Closest to the research domain.
- **B — Language/style profile:** essays, reports, emails, academic prose, marketing text, explanations. This is an exploratory adaptation, not a validated StoryScope application.
- **C — Matched comparison:** two or more texts written for the same prompt/task, genre, language, audience, similar length, and comparable editing conditions.
- **D — Revision for authorial voice:** improve specificity, clarity, voice, and intentionality. Never frame this as detector evasion.
- **E — Corpus review:** multiple documents. Maintain one record per text; compare only sufficiently matched groups.

## 4. Mandatory input-adequacy gate

Before interpreting patterns, record:

- Language and variety (e.g. Ecuadorian Spanish, Mexican Spanish, US English).
- If the variety is not supplied or cannot be established from adequate evidence, record **“variedad no especificada / no determinable”**. Never infer “español general” from absent regionalisms, neutral register, user location, or a short sample.
- Genre and text type; narrative, non-fiction, hybrid, or constrained format.
- Approximate word count and whether complete or excerpted.
- Prompt/task, audience, and purpose, if known.
- Translation, editing, dictation, templates, AI assistance, or other production conditions, if known.
- Presence or absence of a genuinely matched comparison sample.

### Conservative LION LAB operating guardrail (not a research threshold)

The paper does **not** establish a universal minimum word count for qualitative use. The following thresholds are internal safeguards to prevent overclaiming; they are not StoryScope findings or classifier cutoffs:

- **Fewer than 500 words:** the global alignment must be **evidencia insuficiente**. You may describe local features, but do not label the text globally as more human-pattern or more AI-pattern aligned.
- **500–999 words:** exploratory profile only; default low analysis confidence. Avoid a global direction unless the user supplied a closely matched comparison and there is enough assessable narrative material. Even then, label the result preliminary.
- **1,000 words or more:** a broader qualitative narrative profile may be possible, but length alone does not create high confidence. The paper reports an exact corpus mean of 4,753 words (rounded to roughly 5,000 in the abstract); this is context, not a minimum threshold.
- **Brief or constrained genres** (aphorism, slogan, microfiction, poem, form, list, prompt, template, short social post) remain unsuitable for a global authorship-pattern label regardless of whether they contain 500 words. Explain genre-specific constraints.
- **Non-fiction:** always label the method as an exploratory adaptation. Do not apply fiction-only subplots, character arcs, suspense mechanics, or other irrelevant features literally.

If the gate fails, the overall result is `evidencia insuficiente`. This does not prevent a neutral structural or style critique.

## 5. Evidence-state decision tree — mandatory

Read `references/evidence-status.md`. Use exactly these five states for each feature:

1. **Presente–alineado:** the feature/value is directly observed and matches the direction reported in the research.
2. **Presente–opuesto:** a directly observed value of the same feature points toward the other pole; this is genuine counterevidence, not mere absence.
3. **Ausente:** the feature was inspected and no instance was found. It has **no directional weight by default**.
4. **No aplicable:** the feature does not fit the genre/task (e.g. subplot structure in a product label).
5. **No evaluable:** the sample is too short, incomplete, inaccessible, or otherwise inadequate to decide.

### Crucial distinction: an explicit “none” category can be an observed value

Some research features explicitly encode values such as `no_subplots` or `no_major_withholding`. If the text is long and complete enough for that value to be meaningfully assessed, record the **categorical value as observed**. Do not silently convert every lack of an element into that value. In a micro-story or fragment, `no_subplots` is usually **no evaluable**, not evidence of AI.

### Absence rule

An absence can be directionally considered only if all are true:

- The feature's absence is an explicit, meaningful value in the relevant research feature or is a deliberate structural choice in a sufficiently complete text.
- The feature would reasonably be expected in that genre, task, and length.
- The text offers enough opportunity for it to appear.
- The same rule is applied symmetrically to human-leaning and AI-leaning features.

If any condition is not met, use `Ausente` with no direction, or `No evaluable` if length/context blocks assessment. Never infer human authorship from a lack of sensory details, setting, dialogue, subplots, secondary characters, named references, or flashbacks in a short text.

### Direction labels

For a feature that is genuinely assessable, use only:

- `patrón IA` — observed value aligns with an AI-elevated option/mean in the study.
- `patrón humano` — observed value aligns with a human-elevated option/mean in the study.
- `mixto` — one canonical feature has relevant observations pointing in both directions or is genuinely ambiguous.
- `neutro` — observed but the study does not establish a meaningful directional pattern.
- `no evaluable` — evidence state does not support direction.

Do not use “contrapatrón humano/IA”. If evidence points against a proposed direction, record `Presente–opuesto` and explain the actual observed alternative value.

## 6. Ten-dimensional narrative profile

Use the ten taxonomy dimensions as an organizing framework, not as ten votes. Read the official research basis and the 30-feature map before interpreting.

| Dimension | What to examine |
|---|---|
| Agents | Character roles, introduction, goals, motivations, agency, interiority, development |
| Social networks | Relationships, alliances, power, communication, relationship change |
| Style | Narratively relevant style choices; keep surface-language cues in their separate track |
| Plot | Conflict, plot arc, resolution, moral framing, subplots, thematic unity |
| Setting | Spatial grounding, locations, atmosphere, sensory/environmental detail |
| Events | Causal links, event types, escalation, event structure |
| Revelation | Withholding, suspense, surprise, irony, disclosure, recontextualization |
| Situatedness | Genre awareness, thematic/contextual grounding, intertextuality, reader positioning |
| Temporal structure | Chronology, time jumps, anachrony, duration, pacing |
| Perspective | Point of view, focalization, narrative distance, dialogue, reader address |

The paper's full taxonomy has 304 features. This Skill's core feature reference covers the 30 unique central features discussed in Tables 14–16; it is not a replacement for the full 304-feature taxonomy.

## 7. Research-derived core patterns

Read `references/core-patterns.md` and `references/feature-dimension-map.csv`.

- Treat reported corpus differences as group-level tendencies, not rules or cutoffs.
- For scale/ordinal features, compare the paper's group means only descriptively. Do not map a single text to a class by comparing it mechanically to a mean.
- For categorical features, evaluate the **specific response option**. Do not interpret the absence of a feature as an observed option unless the text can support that classification.
- For the numeric map, **Table 15** identifies the 13 core human-characterizing features and their response options; the 30-feature Human/AI means, prevalences, and gaps are in **Table 16**. Do not cite Table 15 as the source of the 30-feature numeric values.
- Some dimensions have small differences. For example, the average temporal discontinuity/anachrony differences are modest; a straight chronological sequence alone is not a decisive cue. On a sufficiently long, genre-comparable story, explicit time-jump structure may be weakly human-pattern aligned; lack of time jumps in a short text is not evidence.
- Reference explicitness, subplot integration, and dominant emotional expression each have different response options appearing on both the AI-elevated and human-elevated lists. Treat each as **one feature with mutually exclusive/alternative values**, not as two independent signals.
- Do not create a numeric score by adding rows or clusters. The operational cluster map is a guard against duplicate counting, not a research scoring model.

## 8. Analyze surface language as a separate track

Describe only observable prose choices: lexical specificity, sentence syntax and rhythm, repetition, explicit signposting, over-explanation, transitions, figurative language, register, voice, paragraph architecture, and redundancy.

Alternative explanations must be considered: genre convention, editorial requirements, translation, non-native writing, accessibility, professional style guides, deliberate minimalism, dictation, or templates. Do not combine this track with the narrative dimensions as if it were independent evidence unless you explain the relationship and avoid duplicate counting.

## 9. Spanish and multilingual adaptation

The study evaluates English-language fiction. Spanish application is exploratory and has no equivalent validation or calibrated baselines in this Skill. Read `references/spanish-adaptation.md`.

At discourse level, it is often possible to inspect agents, goals, conflict, causal structure, information order, plot, perspective, and thematic framing. Do **not** directly transfer English-language surface cues or assume equivalence for tense/aspect, pro-drop, connector frequencies, idioms, register, punctuation, or regional usage. Translation can introduce or erase features. Never transfer the paper's percentages, model rankings, or thresholds to Spanish.

## 10. Matched comparison protocol

A comparison is stronger only when the texts share, as far as possible:

- Same prompt or task and comparable constraints.
- Same language and language variety.
- Same genre and intended audience.
- Similar length and completeness.
- Similar editing, translation, and assistance conditions.

Record mismatches first. Compare concrete narrative choices and surface language separately. Do not announce that one sample is definitively human and another definitively AI. If the pair is not matched, describe differences without attributing them to source.

## 11. Mandatory self-audit before synthesis

Before writing the conclusion, explicitly check:

- Did I mark any absence as evidence without satisfying the absence rule?
- Did I confuse `Ausente`, `No aplicable`, and `No evaluable`?
- Did I treat a categorical `none` value as observed only when the text supports it?
- Did I mistake ordinary linear chronology for decisive evidence?
- Did I count a feature twice because it appears under two options or paper themes?
- Did I count narrative style and surface language twice?
- Did I respect the word-count and genre gate?
- Did I distinguish study-derived claims from my interpretation?
- Did I consider Spanish/translation/genre alternatives?
- Did I infer a language variety or dialect without explicit or sufficient textual evidence? If so, replace it with `no especificada / no determinable`.
- Does the overall label become `evidencia insuficiente` when the gate requires it?

If any answer reveals a violation, correct the analysis before presenting it.

## 12. Required output format

For a normal analysis, provide exactly these seven sections in this order (additional material may follow them):

1. **Alcance y límites** — language/variety, genre, word count, completeness, comparison sample, known editing/translation, adequacy gate.
2. **Resumen estructural neutral** — what the text does, without authorship judgment.
3. **Perfil por dimensiones** — table with dimension, observation, evidence state, cluster (if any), direction, strength, or why not assessable.
4. **Indicadores centrales** — only the most relevant independent clusters; quotation, research direction, counterevidence, context, and strength. Do not list every correlated feature as separate evidence.
5. **Lenguaje superficial** — separate style observations, alternatives, and no authorship claim.
6. **Síntesis** — `patrón humano` / `patrón IA` / `mixto` / `neutro` / `evidencia insuficiente`, plus analysis-quality confidence (baja/moderada/alta), and what cannot be concluded.
7. **Recomendaciones** — only if requested or useful; preserve voice and intent.

For short/inadequate texts, Section 6 must state `evidencia insuficiente`, even if local observations can be described. Never use a global directional conclusion when the input-adequacy gate fails.

Use `references/report-template.md` for the full table structure.

## 13. If the user requests editing

Tie every change to author intent. Prefer truthful specificity, causal clarity, distinct character motives, more precise examples, intentional pacing, or reduced redundancy where appropriate. Do not add false lived experience, invented facts/citations, random irregularity, arbitrary nonlinear structure, or generic “human-like” markers.

## 14. Source, provenance, and technical limits

This is an original LION LAB qualitative workflow inspired by StoryScope. It does not include the official 304-feature taxonomy in full, original dataset, model weights, XGBoost classifier, feature extraction pipeline, or evaluation harness. The included 30-feature crosswalk reproduces the research's core-feature summaries and dimension codes from Tables 14–16; its clusters are LION LAB's operational grouping to prevent double-counting, not official StoryScope clusters. Table 15 is the list of 13 core human-characterizing features and their response options; Table 16 contains the 30-feature Human/AI values and gaps. See `references/numeric-integrity-v0.2.3.md` for the transcription, rounding exceptions, and validation scope.

Primary source:

- Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, and John Wieting. “StoryScope: Investigating idiosyncrasies in AI fiction.” arXiv:2604.03136v6, 10 August 2026; COLM 2026.
- Paper: https://arxiv.org/abs/2604.03136
- Versioned HTML: https://arxiv.org/html/2604.03136v6
- Official repository: https://github.com/jenna-russell/storyscope
- Official taxonomy: https://raw.githubusercontent.com/jenna-russell/storyscope/main/data/taxonomy.json

The 500-word and 1,000-word gates above are **LION LAB operating safeguards**, not thresholds established by the article.

## Research Basis and Attribution

StoryScope Human-AI Analysis is an independent LION LAB implementation and extension inspired by the StoryScope research framework described in:

Russell et al., 'StoryScope: Investigating idiosyncrasies in AI fiction', COLM 2026, arXiv:2604.03136.

This Skill is not the original StoryScope implementation and is not an official release of the research authors. It adapts selected StoryScope narrative-analysis concepts into an independent Skill for structured Human-AI narrative analysis.

The Skill must not be interpreted as a universal AI-authorship detector or as definitive proof of human or AI authorship. Its conclusions should be reported as evidence-based analytical signals with appropriate uncertainty.
