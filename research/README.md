# SEVEN Research

This directory is the public methodological entry point for the research layer of **SEVEN**.

SEVEN begins from seven historically persistent labels — pride, greed, lust, envy, gluttony, wrath, and sloth/acedia — but does **not** assume that they are seven natural psychological structures. The research programme asks whether useful human tendencies can become vulnerabilities, how such tendencies interact, and whether the inherited seven-part vocabulary survives explicit attempts to test and falsify it.

## Current research status

**Current instrument: v03 — REVIEW CANDIDATE / NOT FROZEN / NOT YET DEPLOYED TO RATERS.**

v01 and v02 remain in this repository as development history. They were never treated as validated instruments. v03 supersedes them for all current methodological work.

The v03 procedure is deliberately designed so that the seven-category scheme can fail.

Current pre-freeze order:

1. independent corpus audit;
2. pretest with readers who will not become raters;
3. independently selected external stratum;
4. final lint and end-to-end dry run;
5. commitment hashes and external timestamp;
6. freeze;
7. only then, recruitment and rating.

No rating round has started.

## Start here

- [SEVEN_ANNOTATION_PROTOCOL_v03.md](SEVEN_ANNOTATION_PROTOCOL_v03.md) — full v03 protocol, decision rules, claims ladder, limitations, and freeze procedure.
- [annotation/README_DECISIONS_v03.md](annotation/README_DECISIONS_v03.md) — compact record of accepted methodological decisions and current status.
- [annotation/CODEBOOK_v03.md](annotation/CODEBOOK_v03.md) — Round B operational definitions.
- [annotation/ROUND_A_INSTRUCTIONS_v03.md](annotation/ROUND_A_INSTRUCTIONS_v03.md) — label-free first round.
- [annotation/AUDIT_CHECKLIST_v03.md](annotation/AUDIT_CHECKLIST_v03.md) — independent audit procedure for the synthetic corpus.
- [annotation/EXTERNAL_SELECTION_PROCEDURE_v03.md](annotation/EXTERNAL_SELECTION_PROCEDURE_v03.md) — independent selection procedure for the external stratum.
- [annotation/DESCRIPTION_CODING_INSTRUCTIONS_v03.md](annotation/DESCRIPTION_CODING_INSTRUCTIONS_v03.md) — instructions for the two independent coders of Round A descriptions.
- [annotation/RATER_DISCLOSURE_v03.csv](annotation/RATER_DISCLOSURE_v03.csv) — rater disclosure template.
- [annotation/AUDIT_STEP1_TEMPLATE.csv](annotation/AUDIT_STEP1_TEMPLATE.csv) and [annotation/AUDIT_STEP2_TEMPLATE.csv](annotation/AUDIT_STEP2_TEMPLATE.csv) — audit templates.
- [annotation/EXTERNAL_PROVENANCE_v03.csv](annotation/EXTERNAL_PROVENANCE_v03.csv) — provenance template for the external stratum.
- `annotation/build_packets_v03.py` — deterministic packet builder and commitment verifier.
- `annotation/analyze_ratings_v03.py` — reliability analysis and protocol verdict logic.

## What is intentionally not public yet

The following are **not missing documentation**. They are deliberately private before the rating round closes because publishing them would break blinding:

- the v03 master corpus with intended labels and strata;
- `KEY.csv`;
- `ID_MAP.json`;
- `ORDERS.json`;
- the study salt and `ROUND_SECRETS.json`;
- completed audit sheets;
- external-source provenance before disclosure.

The repository-level safeguards for these files are in [research/.gitignore](.gitignore).

At freeze, the public repository will contain commitment hashes. After the round closes, the master corpus, key, maps, orders, raw ratings, free descriptions, and the material required to reproduce the analysis are intended to be disclosed and checked against those commitments.

## Draft corpus status

A private synthetic draft currently contains:

- 28 central cases — 4 per category;
- 16 mixed cases;
- 8 controls;
- 4 cases driven by mechanisms outside the seven;
- 4 practice cases.

The synthetic draft has not passed the independent audit or pretest yet and is therefore **not a frozen research corpus**.

An external stratum of at least 8 units must be selected independently before v03 can support any claim stronger than a result restricted to synthetic material.

## What v03 can and cannot establish

The strongest possible v03 result is limited.

A successful round may show that independent readers can use these operational definitions reproducibly on the tested corpus and that related distinctions appear in their label-free descriptions at the reported rate.

It cannot establish that:

- exactly seven natural psychological structures exist;
- the historical seven are scientifically validated;
- the categories have a particular prevalence in real populations;
- SEVEN's common-root or interaction hypotheses are true;
- the instrument works across languages.

A negative or mixed result is a valid result and requires revision rather than reinterpretation after the fact.

## Language

The canonical public research instrument is **English-only**.

Website pages may be localized, but they should link to the same English research layer. Any future translated rater instrument must be versioned separately and evaluated separately before cross-language results are pooled.

## Historical versions

v01 and v02 are retained for transparency as development history. They should not be distributed to raters and should not be read as the current method.

The current methodological source of truth is v03 plus its accepted decision record.

## Relationship to GREED and the seven-book cycle

GREED is the first active literary and research line inside SEVEN. It is not the end of the project.

The later six lines — envy, pride, wrath, lust, gluttony, and sloth/acedia — remain future research and literary waypoints. Their plots, theses, and conclusions are intentionally not fixed in advance.

The literary work can generate cases, counterexamples, and questions. It is not itself an empirical experiment.
