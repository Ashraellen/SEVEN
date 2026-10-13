# SEVEN — ANNOTATION PROTOCOL v02

> **SUPERSEDED BY v03 / HISTORICAL / NOT A CURRENT INSTRUMENT.** This file is kept as development history only. Do not use it for rating, auditing or analysis. Current instrument: [v03 protocol](SEVEN_ANNOTATION_PROTOCOL_v03.md). Explanation: [HISTORICAL_v01_v02.md](annotation/HISTORICAL_v01_v02.md).

Status: SUPERSEDED BY v03 / HISTORICAL / NOT A CURRENT INSTRUMENT (previous status: REVIEW CANDIDATE / NOT FROZEN / DO NOT DEPLOY TO RATERS YET)
Date: 2026-10-13
Project: SEVEN
Author: Nikolay Kostyshev / Ashraellen

## Purpose

This protocol tests whether the seven historical working categories used by SEVEN can be distinguished reproducibly by independent raters.

It does not test whether exactly seven natural psychological structures exist.
It does not validate SEVEN as a psychological theory.
It does not treat fictional or synthetic material as empirical evidence about real people.

## Primary question

When independent raters examine the same behavioural cases without being told their intended construction, do they apply the seven labels with reproducible agreement?

A negative result is informative.

## v02 changes

v02 replaces v01 as the candidate rater package.

Changes:
- neutral case IDs C01–C42;
- no source or stratum information in the rater-facing corpus;
- at least four central cases for each of the seven categories;
- additional mixed-mechanism cases;
- every case is 60–180 words;
- free motive description is collected before category ratings;
- analyst-only provenance and intended construction are separated from the coder packet;
- CSV field count is generated and checked programmatically;
- v02 remains NOT FROZEN until external review is complete.

## Two-stage response per case

Raters must complete Stage A before Stage B.

### Stage A — free description

Write one or two sentences answering:

**What motive, tension, or process seems most important in this case?**

Do not use the seven labels unless they arise naturally in your own description.

### Stage B — structured coding

For each category assign:
- 0 = not supported
- 1 = plausibly present
- 2 = central

Then assign:
- PRIMARY = one category or NONE
- OTHER = YES / NO
- UNCLEAR = YES / NO
- CONFIDENCE = 1–5

Multiple categories may receive 1 or 2.

## Categories

### PRIDE
Self-evaluation, dignity, superiority, status, recognition, humiliation, or protection of a valued self-image becomes central.

### GREED
Acquiring, retaining, accumulating, or recovering resources or advantage becomes central, especially where the boundary of enough shifts or prior loss makes disengagement harder.

### LUST
Sexual or erotic desire, access, pursuit, possession, or gratification becomes central enough to alter judgment, boundaries, or unrelated commitments.

### ENVY
Comparison with another person’s advantage, status, possession, relationship, recognition, or outcome becomes central to dissatisfaction or action.

### GLUTTONY
Consumption, sensory reward, or repeated gratification beyond immediate need becomes disproportionately important. This is broader than food but must not become a generic label for all repetitive pleasure-seeking.

### WRATH
Perceived violation, insult, obstruction, or injustice produces retaliatory, punitive, aggressive, or escalating action beyond ordinary boundary-setting.

### SLOTH / ACEDIA
Disengagement, avoidance, refusal of effort, or resistance to confronting an unwanted reality becomes consequential. Fatigue, illness, disability, ordinary rest, or lack of resources are not sufficient.

## Raters

Minimum pilot: 3 independent raters.
Preferred pilot: 5 independent raters.

Raters must:
- not see the analyst key;
- not see intended primary/secondary labels;
- not see source/provenance notes before ratings are locked;
- not see other raters’ responses;
- use the same English-language packet;
- disclose prior familiarity with SEVEN.

At least one preferred-pilot rater should have no prior involvement with SEVEN.

## Language

v02 is an English-language instrument.

Translations are not interchangeable with this instrument. A translated rater packet requires its own controlled version, translation record, and separate reliability analysis before cross-language pooling is considered.

## Corpus

Candidate corpus: 42 cases.

Composition:
- 28 central single-focus cases: four for each category;
- 14 mixed-mechanism cases;
- all rater-facing IDs are neutral C01–C42;
- all cases are between 60 and 180 words.

The corpus is an instrument-development corpus, not a representative sample of human behaviour.

## Agreement

Primary reliability measure:
**Krippendorff’s alpha**, calculated separately for each of the seven ordinal 0/1/2 variables.

Secondary summaries:
- complete and partial agreement on PRIMARY;
- confusion matrix for PRIMARY;
- multi-label frequency;
- OTHER frequency;
- UNCLEAR frequency;
- confidence distribution;
- qualitative comparison between Stage A free descriptions and Stage B labels.

Interpret alpha cautiously. Values around .800 or above are commonly treated as strong enough for substantive conclusions, while roughly .667–.800 may support tentative interpretation. These are conventions, not proof thresholds.

## Failure / revision signals

Revise the instrument if:
1. one or more categories show persistently weak reliability;
2. the same category pairs are repeatedly confused;
3. OTHER is frequent and independent raters describe a similar missing mechanism;
4. central cases fail to produce expected variation across categories;
5. agreement is high only for obvious single-focus cases and collapses on mixed cases;
6. free descriptions cluster in ways that do not correspond to the seven labels;
7. raters can infer the intended answer from wording or case construction.

## Exploitability

Exploitability is not an eighth category and is not part of the primary reliability score.

A later exploratory phase may ask which promises, pressures, losses, rewards, status cues, or opportunities are most likely to alter a person’s next decision given a coded motivational configuration.

## Dynamic / network extension

A later repeated-context phase may present the same subject across changing situations and test whether the relations among motives change, rather than only their isolated intensity.

This is compatible with network-style thinking about interacting elements, but SEVEN does not claim to be a validated psychological network model.

## Freeze rule

v02 is currently NOT FROZEN.

Before any rater receives the packet:
1. external methodological review must be completed;
2. protocol, codebook, corpus, analyst key, build script, and ratings template must be internally consistent;
3. the final repository commit SHA must be recorded in `research/annotation/FROZEN_MANIFEST_v02.md`;
4. after that SHA is recorded, no file in the frozen packet may change during the rating round.

Any substantive change after freeze requires v03 or a documented amendment followed by a new round.

## v02 outputs

- research/SEVEN_ANNOTATION_PROTOCOL_v02.md
- research/annotation/CORPUS_MASTER_v02.json
- research/annotation/CODER_CORPUS_v02.md
- research/annotation/CORPUS_ANALYST_KEY_v02.md
- research/annotation/CODEBOOK_v02.md
- research/annotation/RATINGS_TEMPLATE_v02.csv
- research/annotation/build_coder_packet.py

After rating:
- RATINGS_v02.csv
- RELIABILITY_REPORT_v02.md
- DISAGREEMENT_REVIEW_v02.md

## v02 / v01 relationship

v01 is retained as development history.
v02 is the candidate package for first real independent rating.
