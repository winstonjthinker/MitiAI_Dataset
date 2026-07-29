# ZW-BioBank — Zimbabwe Multi-Modal Indigenous Biology Dataset

**Miti AI Consortium · POTRAZ AI for Impact Challenge 2026 · Track 1: Data (T1)**

Lead Innovator: **Mutsa M Mutepfa** · Presenter & Data Engineer: **Winston J Mambongo**
Primary Steward: **SIRDC** (institutional custody) · Technical Maintainer: **Miti AI Consortium**

*Rooted in Zimbabwe, connected by intelligence.*

A sovereign, controlled-access, multi-modal biological dataset of Zimbabwe — structured so
foundation models can learn from it, and so the indigenous communities whose traditional
knowledge directed the collection are guaranteed benefit-sharing when discoveries are
commercialised.

---

## What is in this repository

| Path | Contents |
|---|---|
| [`mitiai_zw_biobank_v1.0_ai4i_data/`](mitiai_zw_biobank_v1.0_ai4i_data) | The complete dataset package — schema, data, labels, validation, governance, scripts |
| [`PROJECT_ARCHITECTURE.md`](PROJECT_ARCHITECTURE.md) | Source → collection → validation → handover architecture |
| [`mitiai_zw_biobank_v1.0_ai4i_data/README.md`](mitiai_zw_biobank_v1.0_ai4i_data/README.md) | **Full package documentation** — focal specimens, evidence mapping, walkthrough blueprint |

---

## Reproduce every claim in five minutes

Python 3 standard library plus `reportlab` for the PDF reports. **No network access, no
database server, no manual editing.** Run in this order from inside the package directory:

```bash
cd mitiai_zw_biobank_v1.0_ai4i_data

python scripts/machine_loading_test.py      # PROOF 1  Load the data
python scripts/validate.py                  # PROOF 2  Trace provenance + quality checks
python scripts/validate.py --demo           # PROOF 4  Four governance refusals
python scripts/validate.py                  #          Re-run clean: restores BATCH CLEAN
python scripts/generate_reports.py          # PROOF 3  Structure + governance PDFs
python scripts/build_manifest.py            #          Re-seal after the logs are rewritten
python scripts/build_manifest.py --verify   # PROOF 5  Cryptographic integrity
```

Order matters. `validate.py` writes a fresh `checked_at` timestamp into every row of the QC
and error logs, so those two files legitimately carry a new SHA-256 after each run;
`build_manifest.py` re-seals the manifest over them. Verifying before re-sealing reports
them as `ALTERED`, which is the manifest working correctly, not a fault.

### What you should see

| Command | Expected result |
|---|---|
| `machine_loading_test.py` | Every file loads into Python `csv`, pandas, SQLite and QGIS with no manual editing |
| `validate.py` | `317/317 records admitted` · 888 checks · **`STATUS: BATCH CLEAN`** · 0 failures |
| `validate.py --demo` | `4 attempted, 4 refused` · **`STATUS: BATCH HELD`** |
| `build_manifest.py --verify` | `verify: OK — package intact, every checksum matches` |

---

## The five minimum proofs

| # | Show | Where it is proven |
|---|---|---|
| **1** | **Load the data** | `scripts/machine_loading_test.py` — 317 records across 5 tables open in standard tools; plain UTF-8 CSV, no merged cells, no multi-row headers. Excel copies ship alongside every CSV. |
| **2** | **Trace provenance** | SQLite view `v_provenance_chain` walks a detected compound back through physical sample → traditional knowledge record → holder pseudonym → community council endorsement → signed benefit-sharing agreement. 88 compounds resolve to a named holder. |
| **3** | **Explain the structure** | `schema/schema.sql` (DDL, constraints, indexes, 3 views), `schema/schema.json`, `schema/erd.svg`, a 156-field `schema/data_dictionary.csv`, and 5 metadata cards in `metadata/`. |
| **4** | **Run a quality check** | 16 rules in `validation/validation_rules.json` drive 888 checks across all 7 quality dimensions. `--demo` attempts four governance violations and all four are refused — three by database `CHECK` constraints, one by a validator hold. |
| **5** | **Show governance** | Tiered access below, `manifest.csv` SHA-256 over all 69 files, and the registers in `governance/`. |

### Governance enforced by the database, not by prose

Four constraints in `schema/schema.sql` make policy a condition of a row existing:

| Rule | Constraint |
|---|---|
| Consent gate | `CHECK (heritage_use_ref IS NULL OR consent_reference IS NOT NULL)` |
| Sacred exclusion | `CHECK (sensitivity_level IN ('public','community-restricted'))` |
| Prior consent | `CHECK (consent_date <= interview_date)` |
| Permit gate | Processing cannot complete without `nba_permit_ref` |

Holder withdrawal is caught by the validator, which surfaces every downstream record through
`v_withdrawal_impact` and holds the batch until each is actioned inside the 30-day commitment.

---

## What is open, controlled and withheld

**This repository is the public tier.** It is deliberately open, and that is consistent with
the controlled-access model rather than an exception to it:

| Tier | Contents | Access |
|---|---|---|
| **Public** — this repo | Schema, data dictionary, metadata, validation code, aggregate statistics, and a representative pilot sample | Open |
| **Research** | Full record-level data | Data access agreement with SIRDC |
| **Restricted** | Community-restricted knowledge | SIRDC **plus** community council concurrence |
| **Commercial** | Any commercial application | Gated behind an executed benefit-sharing agreement — no exceptions |

**Withheld entirely.** The Holder Identity Register is AES-256 encrypted and held in SIRDC
custody, never in this repository. Every identifier you see here is a pseudonym (`HLD-EH-007`,
`INT-002`, `LIA-EH-01`). GPS coordinates in the public release are masked to ward centroids at
a stated 5,000 m precision, declared per row via `location_masked`. Knowledge classified as
sacred is refused at the database level and cannot enter the bank at all.

**Licence.** Code (`scripts/`, `schema/schema.sql`, `validation/validation_rules.json`) is MIT.
The data is **not** under an open data licence — it is sovereign controlled access, tiered as
above. See [`governance/license.txt`](mitiai_zw_biobank_v1.0_ai4i_data/governance/license.txt).

---

## Coverage

- **Geography** — Eastern Highlands (Chimanimani, Mutare, Nyanga), Mazowe, Zvishavane, and the
  SIRDC LC-MS core facility, across 7 registered sources `ZW-SRC-001`–`007`
- **Languages** — Shona (`sn`), Ndebele (`nd`), English (`en`), with a 30% Ndebele
  representation floor monitored in `governance/bias_risk_register.csv`
- **Modalities** — environmental samples, genomic sequences, metabolomic profiles, and
  traditional heritage knowledge, joined on one physical sample

### Known limitations, stated plainly

Phase I is a 500-sample pilot specification, not a national inventory. Untargeted LC-MS
confidently identifies only a minority of features — most remain MSI level 3–4 and are labelled
putative. Heritage knowledge reflects consenting holders in participating communities and
carries selection bias. Protected-area access is not yet secured, so Phase I is anchored on
communal land. Full detail in `governance/target_population_and_sampling.md` and
`governance/bias_risk_register.csv`.

---

## Integrity when you clone

`.gitattributes` pins `* -text` so Git performs no line-ending translation on checkout. Without
it, CRLF conversion would rewrite file bytes and every checksum in `manifest.csv` would fail on
a fresh clone. If `build_manifest.py --verify` reports `OK` after cloning, the package you hold
is byte-identical to the one that was sealed.

---

*We can discover it — from our soil, our forests, and our heritage.*
*Miti AI is not just a dataset. It is scientific sovereignty.*
