# SEVEN — ANNOTATION CODEBOOK v01

Status: PILOT CODER INSTRUCTIONS
Date: 2026-10-13
Protocol: ../SEVEN_ANNOTATION_PROTOCOL_v01.md
Corpus: CORPUS_v01.md

## Instruction to coder

Read each case independently.

Your task is **not** to decide whether a person is good or bad.
Your task is **not** to diagnose anyone.
Your task is **not** to force every case into one of seven labels.

For every case, rate each category:

- 0 = not supported
- 1 = plausibly present
- 2 = central

Then choose:
- PRIMARY = one category, or NONE
- OTHER = YES / NO
- UNCLEAR = YES / NO
- CONFIDENCE = 1–5

If several motives appear important, rate several categories 1 or 2.

Do not infer hidden facts that are not present in the case.

## Categories

### PRIDE
Self-evaluation, dignity, superiority, status, recognition, humiliation, or protection of a valued self-image becomes central to the decision.

Confidence or ordinary self-respect alone is not enough.

### GREED
Acquiring, retaining, accumulating, or recovering resources/advantage becomes central, especially where the boundary of “enough” shifts or loss makes disengagement harder.

Ordinary saving or rational acquisition alone is not enough.

### LUST
Sexual or erotic desire, possession, access, pursuit, or gratification becomes central enough to alter judgment, boundaries, or treatment of another person.

Attraction alone is not enough.

### ENVY
Comparison with another person’s advantage, status, possession, relationship, recognition, or outcome becomes central to dissatisfaction or action.

Admiration or aspiration alone is not enough.

### GLUTTONY
Consumption, sensory reward, or repeated gratification beyond immediate need becomes disproportionately important.

Do not use this as a generic label for every repetitive pleasure-seeking behaviour.

### WRATH
A perceived violation, insult, threat, obstruction, or injustice drives retaliatory, punitive, aggressive, or escalating action.

Ordinary boundary-setting alone is not enough.

### SLOTH / ACEDIA
Disengagement, avoidance, refusal of effort, withdrawal from meaningful action, or resistance to confronting unwanted reality becomes consequential.

Do not code fatigue, illness, disability, lack of resources, or ordinary rest as moral failure.

## OTHER

Mark OTHER = YES when an important mechanism is present but the seven definitions do not represent it well.

Briefly name the missing mechanism in COMMENT.

## UNCLEAR

Mark UNCLEAR = YES when the case does not provide enough information to distinguish plausible explanations.

Uncertainty is a valid result.

## Primary label

PRIMARY is a forced summary only when one category clearly dominates.

Use PRIMARY = NONE when:
- no category fits;
- two or more are inseparable;
- information is insufficient.

Do not choose a primary label merely because the form asks for one.

## Rating template

For each CASE_ID record:

`CASE_ID, PRIDE, GREED, LUST, ENVY, GLUTTONY, WRATH, SLOTH_ACEDIA, PRIMARY, OTHER, UNCLEAR, CONFIDENCE, COMMENT`

Example format only:

`S00,0,1,0,0,0,0,1,NONE,NO,YES,2,"Two explanations remain plausible"`

Do not use this example as a substantive guide.

## Independence rule

Do not discuss ratings with other coders until the dataset is locked.

Do not read SEVEN author commentary about individual corpus cases before completing the round.
