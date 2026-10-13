# SEVEN Research

This directory is the public methodological entry point for the research layer of **SEVEN**. The canonical research files are maintained here in English.\n\nWebsite entry point: [Ashraellen Research](https://www.ashraellen.com/en/research/) (English). **Ashraellen.com is multilingual:** if English is not convenient, open [the main site](https://www.ashraellen.com/) and choose your language; the Research section is available through the site’s language versions. Localized website pages are accessibility and navigation entry points, while this repository remains the methodological source of truth for SEVEN.

SEVEN begins from seven historically persistent labels — pride, greed, lust, envy, gluttony, wrath, and sloth/acedia — but does **not** assume that they are seven natural psychological structures. The research programme asks whether useful human tendencies can become vulnerabilities, how such tendencies interact, and whether the inherited seven-part vocabulary survives explicit attempts to test and falsify it.

## What this study actually does

In plain words, the first empirical step is a **pilot test of whether independent people use the seven categories in the same way**:

1. About 65 short scenes of human behaviour are collected (the "corpus"): 56 invented for the study, plus at least 8 passages chosen from published literature by an independent person.
2. At least five independent readers receive the scenes. In **Round A** they describe in their own words what is going on, without seeing any category names.
3. Only after Round A is locked, in **Round B**, they receive written definitions of the seven categories and rate each scene: 0 (not supported), 1 (plausibly present), 2 (central).
4. Agreement between readers is measured with a pre-specified statistic (Krippendorff's alpha), and the decision rules are written down before any data exist.

If readers do not agree, or keep finding a motive the seven do not cover, the result is a reason to revise the scheme. The procedure is designed so that the scheme can fail.

This is **not** a psychological test of people, not a diagnosis, and not a claim that the scenes show real individuals.

## What the status labels mean

**Current instrument: v03 — REVIEW CANDIDATE / NOT FROZEN / NOT YET DEPLOYED TO RATERS.**

| Label | Meaning |
|---|---|
| REVIEW CANDIDATE | A complete draft, handed over for independent checking. It may still change as a result. |
| NOT FROZEN | No hashes and no external timestamp exist yet, so the files may still be edited. After freeze they cannot change. |
| NOT YET DEPLOYED TO RATERS | No rater has received anything. No rating round has started and there are no data. |
| FROZEN | The files have been fingerprinted (SHA-256), the fingerprints are recorded in a public manifest and with an external timestamp, and nothing may change during the round. |
| SUPERSEDED / HISTORICAL | An older version kept as history. Not to be used. |

## Where to start

Read in this order:

1. **This README** — what the study is, what exists, what is private, how to take part.
2. **[SEVEN_ANNOTATION_PROTOCOL_v03.md](SEVEN_ANNOTATION_PROTOCOL_v03.md)** — the full protocol. If you read only part of it: §1 (purpose), §9 (analysis plan and decision rules) and §10 (what results may and may not claim).
3. **[annotation/CODEBOOK_v03.md](annotation/CODEBOOK_v03.md)** — the seven working definitions and the 0/1/2 scale that raters will use in Round B.

Then, by role:

| If you are… | Read |
|---|---|
| a methodologist or critic | [annotation/README_DECISIONS_v03.md](annotation/README_DECISIONS_v03.md) (accepted decisions and status), then the protocol's limitations (§11) |
| a possible independent auditor | [annotation/AUDIT_CHECKLIST_v03.md](annotation/AUDIT_CHECKLIST_v03.md) |
| a possible external-stratum selector | [annotation/EXTERNAL_SELECTION_PROCEDURE_v03.md](annotation/EXTERNAL_SELECTION_PROCEDURE_v03.md) |
| a possible rater or description coder | not yet: recruitment starts only after freeze. Meanwhile see [annotation/ROUND_A_INSTRUCTIONS_v03.md](annotation/ROUND_A_INSTRUCTIONS_v03.md) and [annotation/DESCRIPTION_CODING_INSTRUCTIONS_v03.md](annotation/DESCRIPTION_CODING_INSTRUCTIONS_v03.md). **If you may become a rater, please do not read the codebook or the protocol before you are asked to: raters who have seen SEVEN materials before their ratings are locked are excluded (protocol §9.1, rule E1).** |
| checking reproducibility | `annotation/build_packets_v03.py` (packet builder and commitment verifier) and `annotation/analyze_ratings_v03.py` (analysis and decision logic) |

## Order of work before the round

Current pre-freeze order:

1. independent corpus audit;
2. pretest with readers who will not become raters;
3. independently selected external stratum;
4. final lint and end-to-end dry run;
5. commitment hashes and external timestamp;
6. freeze;
7. only then, recruitment and rating.

No rating round has started.

## Public files now

- [SEVEN_ANNOTATION_PROTOCOL_v03.md](SEVEN_ANNOTATION_PROTOCOL_v03.md) — protocol, decision rules, claims ladder, limitations, freeze procedure, publication schedule (§14).
- [annotation/README_DECISIONS_v03.md](annotation/README_DECISIONS_v03.md) — compact record of accepted decisions and current status.
- [annotation/CODEBOOK_v03.md](annotation/CODEBOOK_v03.md) — Round B operational definitions.
- [annotation/ROUND_A_INSTRUCTIONS_v03.md](annotation/ROUND_A_INSTRUCTIONS_v03.md) — label-free first round.
- [annotation/DESCRIPTION_CODING_INSTRUCTIONS_v03.md](annotation/DESCRIPTION_CODING_INSTRUCTIONS_v03.md) — for the two independent coders of Round A descriptions.
- [annotation/AUDIT_CHECKLIST_v03.md](annotation/AUDIT_CHECKLIST_v03.md) — independent audit of the synthetic corpus.
- [annotation/EXTERNAL_SELECTION_PROCEDURE_v03.md](annotation/EXTERNAL_SELECTION_PROCEDURE_v03.md) — independent selection of the external stratum.
- Blank templates: [annotation/RATER_DISCLOSURE_TEMPLATE_v03.csv](annotation/RATER_DISCLOSURE_TEMPLATE_v03.csv), [annotation/AUDIT_STEP1_TEMPLATE.csv](annotation/AUDIT_STEP1_TEMPLATE.csv), [annotation/AUDIT_STEP2_TEMPLATE.csv](annotation/AUDIT_STEP2_TEMPLATE.csv), [annotation/EXTERNAL_PROVENANCE_TEMPLATE_v03.csv](annotation/EXTERNAL_PROVENANCE_TEMPLATE_v03.csv). Filled copies are private and ignored by git.
- `annotation/build_packets_v03.py`, `annotation/analyze_ratings_v03.py` — scripts.

## Files that do not exist yet

These appear **only at freeze**, so their absence is expected:

- `COMMITMENT_v03.json` — hashes of the private corpus, key, orders and the instruments;
- `FROZEN_MANIFEST_v03.md` — repository commit SHA and file hashes at freeze, and the dates and outcomes of the audit and pretest;
- the reference of the external timestamp.

## What is intentionally not public yet

The following are **not missing documentation**. They are deliberately private before the rating round closes because publishing them would break blinding:

- the v03 master corpus with intended labels and strata;
- `KEY.csv`;
- `ID_MAP.json`;
- `ORDERS.json`;
- the study salt and `ROUND_SECRETS.json`;
- completed audit sheets and the audit report;
- external-source provenance (filled copy) before disclosure;
- completed rater disclosure forms (never published individually, only as an aggregate).

The repository-level safeguards for these files are in [.gitignore](.gitignore). The full schedule — public now, private until the round closes, published at freeze, published after the round — is in [protocol §14](SEVEN_ANNOTATION_PROTOCOL_v03.md).

At freeze, the public repository will contain commitment hashes. After the round closes, the master corpus, key, maps, orders, raw ratings, free descriptions, and the material required to reproduce the analysis are intended to be disclosed and checked against those commitments.

## Draft corpus status and who wrote it

A private synthetic draft currently contains:

- 28 central cases — 4 per category;
- 16 mixed cases;
- 8 controls;
- 4 cases driven by mechanisms outside the seven;
- 4 practice cases.

**The draft was written by an AI assistant working with the author, with the category definitions in view.** Such cases are likely to be easier to recognise than cases written by someone who did not know the definitions. For that reason the draft is **not** a research corpus yet. It has to pass an independent audit and a pretest, and it has to be complemented by an external stratum chosen by someone who did not write the definitions or the cases. The protocol, instruments and scripts were also drafted with AI assistance under the author's direction; the decision parameters were confirmed by the author.

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

## Glossary

- **Corpus** — the set of short invented scenes that readers rate.
- **Stratum** — a group of scenes with a shared role: *central* (one dominant motive), *mixed* (two plausible motives), *control* (ordinary behaviour, no category should apply), *other* (a mechanism outside the seven), *external* (passages chosen by an independent person from published sources), *practice* (training scenes, not analysed).
- **Rater** — a naive reader who rates scenes. **Description coder** — a person who maps raters' free descriptions to categories.
- **Round A / Round B** — free description without category names / rating with the written definitions.
- **Blind** — raters never see the intended label of a scene, and the first round contains no category names.
- **Key** — the private table of intended labels. It is kept secret until the round closes, so that nobody can rate toward it.
- **Audit** — a check of the corpus by an independent person before any rater sees it. **Pretest** — a trial reading by people who will not become raters.
- **Commitment** — SHA-256 fingerprints of the private files, published before the round, so that nothing can be changed afterwards unnoticed.
- **External timestamp** — a record in an outside service (for example a preregistration) that proves when the commitment existed. Git history alone is under the author's control.
- **Freeze** — the moment after which no instrument file may change.
- **Krippendorff's alpha** — a standard chance-corrected measure of agreement between raters. 1 is perfect agreement, 0 is chance level.
- **Falsification condition** — a pre-specified outcome that counts against the seven-category scheme (protocol §9.4).

## Language

The canonical public research instrument is **English-only**.

Website pages may be localized, but they should link to the same English research layer. Any future translated rater instrument must be versioned separately and evaluated separately before cross-language results are pooled.

## Historical versions

v01 and v02 are retained for transparency as development history, with a **SUPERSEDED / HISTORICAL** banner at the top of each. They should not be distributed to raters and should not be read as the current method. What each old file is, and why the v02 master and key are public on purpose, is explained in [annotation/HISTORICAL_v01_v02.md](annotation/HISTORICAL_v01_v02.md).

The current methodological source of truth is v03 plus its accepted decision record.

## How to contact or take part

Critique of the method is welcome, especially from moral psychology, measurement and reliability, motivation research and the history of ideas.

- To comment on the method, offer to act as an **independent auditor**, an **external-stratum selector** or a **pretest reader**, or to ask about rating later: write to **ashraellen.live@gmail.com** (the same address as on the project page).
- Concrete textual corrections to public files may also be proposed as a pull request.
- Raters and description coders are recruited only after freeze. Independence rules: nobody who wrote the definitions or the cases may be an auditor, a selector, a rater or a description coder; the auditor and the selector are different people and neither may be a rater; pretest readers do not become raters.

## Relationship to GREED and the seven-book cycle

GREED is the first active literary and research line inside SEVEN. It is not the end of the project.

The later six lines — envy, pride, wrath, lust, gluttony, and sloth/acedia — remain future research and literary waypoints. Their plots, theses, and conclusions are intentionally not fixed in advance.

The literary work can generate cases, counterexamples, and questions. It is not itself an empirical experiment. The manuscript and its editorial workspace are described in the [repository README](../README.md).
