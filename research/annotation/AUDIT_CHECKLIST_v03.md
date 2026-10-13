# SEVEN — INDEPENDENT CORPUS AUDIT CHECKLIST v03

Status: REVIEW CANDIDATE / NOT FROZEN
Protocol: ../SEVEN_ANNOTATION_PROTOCOL_v03.md (sections 3, 11, 12)
Order of work: AUDIT (this document) -> PRETEST -> EXTERNAL STRATUM (separate selector) -> final check -> commitment and timestamp -> freeze.

## 0. Who may audit
A person who did not write the codebook definitions, any synthetic case, or any part of the draft corpus (the author and the AI assistant that drafted them do not qualify). The auditor may not be a rater in the study and must not be the external-stratum selector. The auditor does not need to be a domain expert, but must be able to read English fluently and to apply a written rubric.

Declaration (auditor): I did not write or edit the definitions or the cases. I will not rate in the study, and I will not disclose the contents of this corpus before disclosure.
Name / date:

## 1. What the auditor receives, in this order
1. CODEBOOK_v03.md and the protocol sections 3 and 11 (Step 1 below uses only the codebook).
2. The Round B `CASES.md` from a throwaway build (`build --raters AUD --salt <throwaway>`, never the study salt). It contains the 56 analysis cases and 4 practice cases in neutral random order with no strata and no keys.
3. Only after Step 1 is saved and returned: the throwaway build's `private/KEY.csv` (strata and intended labels), the practice feedback text, and the lint report, for Steps 2 to 4. The throwaway build is destroyed after the audit; the study build uses its own salt.

## 2. Step 1: blind pass (about 90 minutes)
For each case, without reading ahead and without seeing any key:
- A1. Write one sentence on what the person is trying to get, avoid, or protect.
- A2. Rate the seven categories 0/1/2 as in the codebook, and give PRIMARY, OTHER, UNCLEAR.
- A3. Giveaway flag: YES if you could name the intended category from wording alone (a signature word, a stock phrase, a narrator cue) without reading the situation. Quote the words.
- A4. Narration flag: YES if any sentence tells the reader what the behaviour means instead of showing it (a thesis, a verdict, "this is about", a word naming an inner state the person would not have named).
- A5. Realism flag (1 to 3): 1 = implausible or cartoonish, 3 = plausible.
- A6. Harm flag: YES if the case contains content that should not go to raters (self-harm, abuse of a minor, identifiable real persons, graphic sexual content, stereotypes of a group).
Save as AUDIT_STEP1.csv (columns in section 7) and send it back before reading anything else.

## 3. Step 2: unblinded checks (about 60 minutes)
Now with the key, strata and lint report:
- B1. For every central case, does the key label match your PRIMARY? List the mismatches. Mismatches are information, not errors to be fixed by the auditor.
- B2. For every central case, apply the counterfactual test in writing: if the key motive were removed, would the behaviour still occur? If yes, the case is not central.
- B3. For every mixed case, is the intended secondary genuinely plausible from the facts? Is the ambiguity in the facts, not in the narrator's hedging? Can you build a reading in which the intended secondary is the primary?
- B4. For every control, is there a plausible reading that makes a category central? If so, the control is contaminated.
- B5. For every "other" case, is the mechanism really outside the seven definitions? Could a careful rater justify a 2 for any category?
- B6. For every practice case, does the feedback text teach the scale without revealing the intended label of any analysis case?
- B7. Duplicate or near-duplicate structure across cases (same setting, same sentence skeleton, same escalation pattern). List clusters of 3 or more.
- B8. Form cues: does length, sentence count, tense or genre correlate with stratum or category? Name any cue you noticed.
- B9. Character names, places, jobs: does any recur in a way that identifies a stratum?

## 4. Step 3: category coverage (about 20 minutes)
- C1. For each category, list the facets covered by the central cases (for example, for GREED: retention, accumulation, recovery). Name facets not covered.
- C2. Which of the eight required mixed pairs feel most forced?
- C3. Which kinds of human motive that raters will plausibly meet in daily life are missing from controls and "other" cases?

## 5. Step 4: verdict per case
Every case gets one of:
- OK: no flags.
- REWRITE: giveaway, narration, unrealistic, or counterfactual failure. The reason is written in one line.
- REPLACE: structurally unsuited (control contaminated, mixed not ambiguous in facts, "other" is in fact a category, harm flag).
- DROP: cannot be repaired in the existing stratum.

## 6. Pass criteria for the corpus
The corpus passes the audit when all of the following hold after the rewrites and a second, partial audit (Step 1 only, on rewritten cases, by the same auditor):
- No hard flags: no harm flag, no giveaway quoted by the auditor, no narration flag, and no control with a plausible central reading.
- Auditor PRIMARY agrees with the key on at least 21 of 28 central cases (75 percent). Reason: below that, either the cases are unclear or the definitions are. Above 26 of 28 is a warning for giveaways, not a goal. Report the number either way.
- Every central case passes the counterfactual test (B2).
- Every one of the 8 required mixed pairs appears, and for each mixed case the auditor can construct a plausible reading with the intended secondary as primary.
- No cluster in B7 of 3 or more cases, or the cluster is rewritten.
- Realism: median at least 2.5, and no case below 2.

If the corpus does not pass, the analyst rewrites or replaces the cases, increments the corpus version, and the auditor repeats Step 1 on the changed cases. Rewrites are made by someone who is neither the auditor nor an eventual rater. All changes are logged in AUDIT_CHANGELOG_v03.md with before/after text hashes. The key is not changed to fit a rater's reading unless the audit finds that the key itself is wrong, and then the case is rewritten, not relabelled.

## 7. Files
- AUDIT_STEP1_TEMPLATE.csv — columns: CASE_ID, A1_SENTENCE, PRIDE, GREED, LUST, ENVY, GLUTTONY, WRATH, SLOTH_ACEDIA, PRIMARY, OTHER, UNCLEAR, A3_GIVEAWAY, A3_QUOTE, A4_NARRATION, A4_QUOTE, A5_REALISM, A6_HARM, COMMENT
- AUDIT_STEP2_TEMPLATE.csv — columns: CASE_ID, STRATUM, KEY_PRIMARY, KEY_SECONDARY, B1_MATCH, B2_COUNTERFACTUAL_OK, B3_PLAUSIBLE_ALT, B4_CONTAMINATED, B5_REALLY_OTHER, B7_CLUSTER, VERDICT, REASON
- AUDIT_REPORT_v03.md — free-text summary: pass or fail by criterion, the numbers in section 6, coverage gaps (section 4), cases by verdict.
- AUDIT_CHANGELOG_v03.md — edits made afterwards.

## 8. After the audit
The audited corpus (with its text hashes) is the input to the pretest. The pretest and the external stratum must not change the audited cases. If the pretest finds a problem, the case is replaced and re-audited. The freeze is made only on a corpus whose every case has passed the audit and the pretest.

## 9. Auditor's independence note
The auditor's blind ratings are not rater data and are never pooled into the study. They are reported alongside the study as a corpus-quality check.
