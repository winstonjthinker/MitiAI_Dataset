# ZW-BioBank v1.0

**Miti AI Consortium · POTRAZ AI for Impact Challenge 2026 · Track 1: Data (T1)**  
Lead Innovator: **Mutsa M Mutepfa** · Team: Miti AI Consortium  
Presenter & Data Engineer: **Winston J Mambongo**  
Primary Steward: **SIRDC (Scientific and Industrial Research and Development Centre)** · Technical Maintainer: **Miti AI**  

*Rooted in Zimbabwe, connected by intelligence.*

A sovereign, controlled-access, multi-modal biological dataset of Zimbabwe — structured so that foundation AI models can learn from it, and so that indigenous communities whose traditional knowledge directed the collection are guaranteed benefit-sharing royalties when discoveries are commercialized.

---

## 1. Focal Specimen Pillars

ZW-BioBank v1.0 anchors its multi-modal collection on three primary specimen lineages representing terrestrial flora, traditional pharmacology, medicinal tree bark, and aquatic environmental monitoring in Zimbabwe:

1. **Medicinal Ginger Lineages (*Siphonochilus aethiopicus* & *Zingiber officinale*)**
   * **Local Names**: *Tsangamidzi* (Shona) · *Isiphepheto* (Ndebele)
   * **Tissue / Organ**: Rhizome & Root
   * **Traditional Indication**: Respiratory distress, cough, flu, asthma, and gastric discomfort (ICD-11: CA23 / DD90).
   * **Key Metabolomics & Bioactives**:
     * *Siphonochilus aethiopicus* (African Wild Ginger): Siphonochilone (sesquiterpenoid lactone marker), hydroxy-siphonochilone.
     * *Zingiber officinale* (Common Ginger): Phenolic gingerols ([6]-, [8]-, [10]-gingerol), shogaols ([6]-shogaol), zerumbone.
   * **Conservation & Feasibility**: *S. aethiopicus* is critically endangered in wild Zimbabwean habitats due to over-harvesting; preserved and sampled via smallholder cultivation plots in Eastern Highlands & Mazowe.

2. **Pepper-Bark Tree (*Warburgia salutaris*)**
   * **Local Names**: *Muranga* (Shona) · *Isibhaha* (Ndebele)
   * **Tissue / Organ**: Trunk Bark & Leaf (Sustainable substitute)
   * **Traditional Indication**: Severe chest complaints, malarial fever, abdominal pain, bacterial & fungal infections (ICD-11: CA23 / 1F40).
   * **Key Metabolomics & Bioactives**: Drimane sesquiterpenoids — Muzigadial (potent antimicrobial), Polygodial (antiseptic & peppery taste marker), Warburganal (anti-inflammatory/COX inhibitor), Ugandensidial (cinnamodial), Mukaadial, plus flavonoid glycosides (Verbascoside).
   * **Conservation & Feasibility**: Protected species; bark harvested under sustainable strip-harvesting guidelines or leaf-substitution protocol to prevent tree mortality.

3. **Water Hyacinth (*Eichhornia crassipes* / *Pontederia crassipes*)**
   * **Local Names**: *Yacinthi Yemumvura* (Shona) · *Inkazana Yemanzini* (Ndebele)
   * **Tissue / Organ**: Aquatic Plant Tissue & River/Lake Sediment (Lake Chivero, Manyame Catchment, Mazowe River)
   * **Application**: Phytoremediation monitoring (heavy metal bioaccumulation of Fe, Zn, Cr, Co; phosphate/nitrate stripping) & endophyte metagenomics.
   * **Key Genomics & Bioactives**: 16S/ITS rhizobiome metagenomics (*Streptomyces* spp., Proteobacteria, metal-resistance clusters), Flavonoids (Luteolin, Apigenin), phytosterols.

---

## 2. Core Adjudicator Needs Alignment (Track 1: DATA)

Adjudicators of the **AiZi 2026 AI for Impact Challenge (Track 1: DATA)** evaluate submissions across three foundational pillars specified on Page 2 of the Innovator Preparation Guide:

1. **SOURCE FEASIBILITY**:
   - **Real, Lawful, and Practical Access**: 7 registered sources (`ZW-SRC-001` to `007`) spanning Eastern Highlands, Mazowe, Zvishavane, and SIRDC LC-MS core facilities.
   - **Provenances & Approvals**: Every source record in [`governance/source_register.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/governance/source_register.csv) includes permissions, access statuses, collection tools, and documented fallback sources.

2. **MACHINE READINESS**:
   - **Structured Multi-Modal Datasets**: Read-only datasets in [`processed/`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/processed) covering 317 records across 5 CSV tables plus 400 applied annotations in [`labels/annotations_v1.jsonl`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/labels/annotations_v1.jsonl).
   - **Automated Validation & Loader**: Standard-library Python loader [`scripts/machine_loading_test.py`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/scripts/machine_loading_test.py) and automated validator engine [`scripts/validate.py`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/scripts/validate.py) (`STATUS: BATCH CLEAN`). Zero external network dependencies.

3. **RESPONSIBLE GOVERNANCE**:
   - **Privacy & Data Protection**: Fully aligned with Zimbabwe Data Protection Act (DPA Ch. 12:07) via [`governance/dpa_compliance_matrix.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/governance/dpa_compliance_matrix.csv).
   - **Identity Cryptography**: AES-256 encrypted Holder Identity Register held in SIRDC custody, separated from public datasets.
   - **Benefit-Sharing & Consent**: Prior Informed Consent (PIC) gate and Benefit-Sharing Agreement (BSA) queryable via SQL view `v_provenance_chain`.

---

## 3. Track-Specific Evidence Mapping (Guide Page 2)

This package directly satisfies all 8 evidence areas required by the POTRAZ AI for Impact Challenge 2026:

| Evidence Area | What is Provided & File Location |
|---|---|
| **1. Database or sample data** | Read-only machine-readable datasets in [`processed/`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/processed) (317 multi-modal records across 5 CSV tables) plus 400 applied annotations in [`labels/annotations_v1.jsonl`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/labels/annotations_v1.jsonl). |
| **2. Data architecture** | Source-to-collection-to-validation-to-handover workflow diagram in [`schema/erd.svg`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/erd.svg) and sampling framework in [`governance/target_population_and_sampling.md`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/governance/target_population_and_sampling.md). |
| **3. Source and access evidence** | [`governance/source_register.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/governance/source_register.csv) with all 7 required provenance fields, permission statuses, collection tools, and fallback sources for all registered sources (`ZW-SRC-001` to `007`). |
| **4. Schema and documentation** | SQL DDL [`schema/schema.sql`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/schema.sql), 156-field [`schema/data_dictionary.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/data_dictionary.csv) / [`data_dictionary.xlsx`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/data_dictionary.xlsx), [`schema/schema.json`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/schema.json), and 5 metadata cards in [`metadata/`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/metadata). |
| **5. Representative sample** | Standardized folder structure, WGS 84 GPS coordinates (with ward-centroid precision masking), SHA-256 integrity checksums, and versioned identifiers (`ZW-TK-YYYY-NNN`, `ZW-SMP-YYYY-NNN`, `ZW-SEQ-YYYY-NNN`, `ZW-MET-YYYY-NNN`). |
| **6. Quality and labelling** | 16 rule definitions in [`validation/validation_rules.json`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/validation/validation_rules.json), automated validator [`scripts/validate.py`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/scripts/validate.py), [`validation/error_log.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/validation/error_log.csv), and [`labels/annotation_guide.pdf`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/labels/annotation_guide.pdf). |
| **7. Sampling and representation** | Sampling logic across Eastern Highlands, Mazowe, Zvishavane, and Matobo/Binga; 30% Ndebele language representation floor; bias monitoring queries in [`governance/bias_risk_register.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/governance/bias_risk_register.csv). |
| **8. Governance and future use** | Lawful basis via Data Protection Act (DPA Ch. 12:07) matrix, AES-256 encrypted Holder Identity Register held in SIRDC custody, Prior Informed Consent pack, and 30-day data withdrawal propagation. |

---

## 4. Technical Walkthrough Blueprint (5 Minimum Proofs — Guide Page 3)

Reviewers and adjudicators can execute and verify the recorded technical walkthrough using standard tools (Python standard library only, zero network dependencies):

```bash
python scripts/machine_loading_test.py      # PROOF 1: Load Data & Machine Readiness
python scripts/validate.py                  # PROOF 2 & 4: Trace Provenance & Run Quality Checks
python scripts/validate.py --demo           # PROOF 4: Demonstrate 4 Refusal & Governance Gates
python scripts/generate_reports.py          # PROOF 3 & 5: Generate Structure & Governance PDF Reports
python scripts/build_manifest.py --verify   # PROOF 5: Verify Cryptographic Data Handover & Integrity
```

### Walkthrough Minimum Proofs Breakdown

| What to Show | Minimum Proof | Demonstrated In Submission By |
|---|---|---|
| **1. Load the data** | Open a representative record or file in a standard tool and confirm it is machine-readable. | `python scripts/machine_loading_test.py` loads all processed tables into Python standard `csv`, `pandas`, SQLite SQL engine, QGIS WGS84 GIS layers, and R without manual editing. |
| **2. Trace provenance** | Show where the record came from, who controls the source and how collection/access is managed. | Querying SQLite view `v_provenance_chain` traces any detected compound (e.g., Warburganal or Gingerol) back through the physical sample, traditional knowledge record, holder pseudonym ID, community council endorsement, and signed Benefit-Sharing Agreement (BSA). |
| **3. Explain the structure** | Show the schema, relationships, dictionary, metadata and versioning. | Reviewing SQL DDL [`schema/schema.sql`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/schema.sql), entity-relationship diagram [`schema/erd.svg`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/erd.svg), data dictionary [`schema/data_dictionary.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/data_dictionary.csv), and 5 dataset metadata cards in [`metadata/`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/metadata). |
| **4. Run a quality check** | Demonstrate one rule that passes, warns or blocks release, including a failed example and correction path. | `validate.py` executes 888+ checks across 7 quality dimensions (**`STATUS: BATCH CLEAN`**). Running `python scripts/validate.py --demo` demonstrates automated rejection of 4 governance violations: <br> • Attempting to record knowledge classified `sacred` -> **DB `CHECK` Refusal** <br> • Submitting a sample with no consent reference -> **DB `CHECK` Refusal** <br> • Dating consent *after* interview date -> **DB `CHECK` Refusal** <br> • Leaving a sample active after holder withdrawal -> **Validator `critical` Hold & 30-day propagation view `v_withdrawal_impact`** |
| **5. Show governance** | Explain what is open, controlled or withheld and how the dataset will be handed over and maintained. | Explaining open vs. controlled access tiers, AES-256 holder identity encryption, SIRDC institutional custody, and cryptographic manifest verification ([`manifest.csv`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/manifest.csv)). |

---

## 5. Structure — Annex C

```
mitiai_zw_biobank_v1.0_ai4i_data/
├── README.md                               Focal pillars, Track 1 evidence, walkthrough blueprint
├── manifest.csv                            path · size · SHA-256 · version · sensitivity
├── metadata/
│   ├── dataset_metadata.json               Annex B keys, verbatim and in order
│   └── subset_metadata_{environmental,genomic,metabolomic,tk}.json
├── schema/
│   ├── data_dictionary.csv                 Annex A columns, verbatim and in order — 156 fields
│   ├── data_dictionary.xlsx                same, formatted, with a coverage summary
│   ├── schema.json                         machine-readable schema
│   ├── schema.sql                          SQL DDL, constraints, indexes, three views
│   └── erd.svg                             entity relationship diagram
├── processed/
│   ├── environmental_samples_v1.csv        T1 · Stream D · the spine (120 records)
│   ├── genomic_sequences_v1.csv            T2 · Stream A (55 records)
│   ├── metabolomic_profiles_v1.csv         T3 · Stream B (90 records)
│   ├── heritage_knowledge_v1.csv           T4 · Stream C · targeting layer (52 records)
│   └── qc_log_v1.csv                       T5 · written by validate.py
├── raw/
│   └── zw_src_00{1..7}_*/README.txt        directory naming & access terms per registered source
├── labels/
│   ├── label_taxonomy.csv                  10 labels, each with a negative example
│   ├── annotation_guide.pdf                workflow, review, adjudication
│   └── annotations_v1.jsonl                applied labels with annotator and guide version (400 items)
├── validation/
│   ├── validation_rules.json               thresholds and check definitions — read by the validator
│   ├── quality_report_v1.pdf               Annex D template, generated from the qc log
│   └── error_log.csv                       warnings and failures with owner and action
├── governance/
│   ├── source_register.csv                 7 sources, all 7 required provenance fields
│   ├── bias_risk_register.csv              8 risks, each with a runnable monitoring query
│   ├── dpa_compliance_matrix.csv           Chapter 12:07, with enforcement mechanism per row
│   ├── consent_log.csv · consent_template.pdf
│   ├── anonymization_plan.pdf · access_policy.pdf
│   ├── self_assessment_checklist.csv       §7 checklist, completed
│   └── license.txt
└── scripts/
    ├── validate.py · machine_loading_test.py
    └── generate_reports.py · build_manifest.py
```

---

## 6. The Four Structural Governance Constraints

Governance policies are enforced at the database engine level via [`schema/schema.sql`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/schema.sql):

| Rule | SQL Constraint |
|---|---|
| **Consent Gate** | `CHECK (heritage_use_ref IS NULL OR consent_reference IS NOT NULL)` |
| **Sacred Exclusion** | `CHECK (sensitivity_level IN ('public','community-restricted'))` |
| **Prior Consent** | `CHECK (consent_date <= interview_date)` |
| **Permit Gate** | processing cannot be marked complete without `nba_permit_ref` |

---

## 7. Known Limitations

Disclosed transparently in accordance with Minimum Expectations §4.2:

- Phase I is a 500-sample pilot specification package; it is not a national inventory.
- Untargeted LC-MS confidently identifies a minority of features; most remain MSI level 3–4 (labeled putative).
- Heritage knowledge reflects consenting holders in participating communities and carries selection bias.
- Protected-area access is not secured; Phase I is anchored on communal land habitat.
- Nanopore metagenomics output is reproducible against the recorded basecaller model (`dna_r10.4.1_e8.2_400bps_sup`).

---

*We can discover it — from our soil, our forests, and our heritage.*  
*Miti AI is not just a dataset. It is scientific sovereignty.*
