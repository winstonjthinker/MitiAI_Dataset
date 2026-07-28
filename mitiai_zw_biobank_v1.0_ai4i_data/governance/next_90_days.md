# Next 90 days

**ZW-BioBank · Miti AI Consortium · SIRDC custody**

Every milestone below has a named owner and a completion test that someone other than the owner can
run. **None of them requires the grant to land first** — that is the point of listing them this way.

> **Before submission:** replace every `TODO-DATE` in `governance/progress_log.csv` and the anchor
> date below with real dates. Do not invent them. An undisclosed or invented date is an integrity
> problem, not a presentation problem.

**Anchor date:** `TODO-DATE` — all windows below are counted from it.

---

## Days 0–30 · Permission and place

| # | Milestone | Owner | Completion test |
|---|---|---|---|
| 1 | NBA permit issued or application acknowledged in writing | Lead Innovator | Permit reference recorded in `governance/source_register.csv`; the permit gate accepts it |
| 2 | Three community councils engaged, two endorsements issued | Community Liaison Lead | Endorsement references resolve in `governance/consent_log.csv` |
| 3 | Consent instrument reviewed in Shona and in Ndebele by a first-language speaker | Community Liaison Lead | Reviewer signs the instrument; both language versions on file |
| 4 | Field kit and mobile laboratory schedule confirmed with LEC Biotec | Lead Innovator | Dated schedule countersigned by both parties |
| 5 | Tablets enrolled and issued identifier blocks | Miti AI | `manage.py simulate_field_day` runs clean against the live API for each device |

**Gate to the next 30 days:** no collection begins until milestones 1 and 2 are complete. A sample
collected without a permit and a council endorsement is not a sample this project can use.

---

## Days 31–60 · First real collection

| # | Milestone | Owner | Completion test |
|---|---|---|---|
| 6 | First field batch collected and preserved | Field Collection Lead | Median minutes-to-preservation under 30, computed by the app rather than reported |
| 7 | First batch synced from tablets and admitted | Miti AI | 0 failures; every warning carries an owner and a correction action |
| 8 | First bilingual validation pass | Community Liaison Lead | No record leaves `machine_draft`; `translation_status` transitions are attributable |
| 9 | Chain of custody unbroken from field to SIRDC | Field Collection Lead | Custody ledger has no gaps; cold-chain excursions recorded, not absent |
| 10 | First sequencing run in the mobile laboratory | Bioinformatics Lead | `basecalling_model` captured from the run, not typed |

**Gate:** any critical finding holds the batch. The batch does not advance because the calendar says
it should.

---

## Days 61–90 · Prove the chain

| # | Milestone | Owner | Completion test |
|---|---|---|---|
| 11 | First LC-MS run on preserved field extracts | Pharmaceutical Chemist | mzML files admitted with matching checksums |
| 12 | First compound resolved to a holder through `v_provenance_chain` | Miti AI | The query returns a row: compound → sample → tk_id → holder → signed agreement |
| 13 | Community council portal shown to at least one council | Community Liaison Lead | Council can see their own contribution counts and status, unassisted |
| 14 | Coverage board reviewed; next expedition ranked from measured gaps | Field Collection Lead | The Ndebele floor and ecozone quotas are read off the data, not asserted |
| 15 | v1.1 release bundle produced and signed | SIRDC Data Steward | `build_manifest.py --verify` returns intact; release refuses to run with an open critical finding |

**Gate:** milestone 12 is the one that matters. If a compound cannot be walked back to a signed
benefit-sharing agreement, the central claim of this dataset is not yet true.

---

## What would make us stop

Stated here because a plan that has no stopping condition is a wish.

- A community council withdraws endorsement — collection in that district stops that day.
- The NBA permit lapses — processing cannot be marked complete, enforced by the permit gate.
- Preservation latency stays above target for a fortnight — the mobile-lab schedule is wrong and
  metabolomics from that period is not trustworthy.
- A holder identity is found anywhere outside the Holder Identity Register — full stop, and a
  disclosure to the affected council.
