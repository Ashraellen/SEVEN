# SEVEN — DESCRIPTION CODING INSTRUCTIONS v03

Status: REVIEW CANDIDATE / NOT FROZEN
Protocol: ../SEVEN_ANNOTATION_PROTOCOL_v03.md

This document is for the two independent **description coders**. Description coders must not be the corpus author, must not have written any case, and must not also act as raters in the same round.

## Task

You receive a sheet of short free-text descriptions that raters wrote about hypothetical cases. You do **not** see the cases, the raters' identities, or any intended labels. Items are shuffled.

For each item, map the description to the seven working categories, using the definitions in `CODEBOOK_v03.md`, based only on what the description says.

## Fields

- **PRIMARY_MAPPED** — one of: PRIDE, GREED, LUST, ENVY, GLUTTONY, WRATH, SLOTH_ACEDIA, OTHER, NONE
  - OTHER: the description names a mechanism that is not one of the seven.
  - NONE: the description says nothing motivational, says the behaviour is ordinary, or is empty.
- **SECONDARY_MAPPED** — optional; a second category from the same list if the description clearly names two.
- **COMMENT** — optional, one short line.

## Rules

- Map what the description says, not what you think the underlying case probably was.
- Use the rater's own words and keywords. Do not reinterpret a rater who names a different mechanism as if they meant one of the seven; use OTHER.
- Work independently of the other description coder. Do not discuss until both sheets are returned.
- Disagreements between coders are reported, not adjudicated, unless the protocol says otherwise for a specific analysis.
