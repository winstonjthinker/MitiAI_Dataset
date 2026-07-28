# ZW-BioBank v1.0 — Project Structure & Architecture Specification

**Miti AI Consortium · POTRAZ AI for Impact Challenge 2026 · Track 1: Data (T1)**  
Lead Innovator: **Mutsa M Mutepfa** · Team: **Miti AI Consortium**  
Presenter & Data Engineer: **Winston J Mambongo**  
Primary Steward: **SIRDC (Scientific and Industrial Research and Development Centre)** · Technical Maintainer: **Miti AI**

---

## 1. Executive Overview

**ZW-BioBank v1.0** is a sovereign, controlled-access, multi-modal biological dataset of Zimbabwe. It is structured so that foundation AI models can learn from indigenous natural product metabolomics, metagenomics, and traditional botanical heritage, while ensuring indigenous communities are protected under the Zimbabwe Data Protection Act (DPA Ch. 12:07) and guaranteed benefit-sharing royalties through Prior Informed Consent (PIC) and Benefit-Sharing Agreements (BSA).

### Key Highlights:
- **3 Focal Specimen Pillars**: Medicinal Ginger (*Siphonochilus aethiopicus* & *Zingiber officinale*), Pepper-Bark Tree (*Warburgia salutaris*), and Water Hyacinth (*Eichhornia crassipes*).
- **317 Multi-Modal Records across 5 Tables**: Environmental Samples (T1), Genomic Sequences (T2), Metabolomic Profiles (T3), Heritage Knowledge (T4), and QC Log (T5).
- **400 Applied AI Annotations**: Covering phytochemistry, therapeutic target mapping (ICD-11), metagenomics, and conservation alerts.
- **Zero-Dependency Verification**: Pure Python standard library automated validation engine (`scripts/validate.py`) enforcing 888+ quality checks and 4 structural governance database constraints.

---

## 2. Comprehensive Directory & File Structure

```
mitiai_zw_biobank_v1.0_ai4i_data/
├── README.md                               # Focal pillars, Track 1 evidence mapping, & walkthrough blueprint
├── PROJECT_ARCHITECTURE.md                 # System architecture, ERD diagrams, & file structure reference
├── manifest.csv                            # Cryptographic handover inventory (path, size, SHA-256, version, sensitivity)
├── metadata/                               # Machine-readable metadata cards
│   ├── dataset_metadata.json               # Top-level dataset metadata card (Annex B schema)
│   ├── subset_metadata_environmental.json  # T1 Environmental samples metadata card
│   ├── subset_metadata_genomic.json        # T2 Genomic sequences metadata card
│   ├── subset_metadata_metabolomic.json     # T3 Metabolomic profiles metadata card
│   └── subset_metadata_tk.json             # T4 Heritage knowledge metadata card
├── schema/                                 # Schema definitions, SQL DDL, & ERD diagrams
│   ├── data_dictionary.csv                 # 156-field comprehensive dictionary (Annex A schema)
│   ├── data_dictionary.xlsx                # Formatted Excel dictionary with coverage summary
│   ├── schema.json                         # Machine-readable JSON schema export
│   ├── schema.sql                          # SQLite 3 DDL schema (tables, foreign keys, CHECK constraints, views)
│   └── erd.svg                             # Scalable Vector Graphics entity-relationship diagram
├── processed/                              # Read-only structured production datasets
│   ├── environmental_samples_v1.csv        # T1 Environmental Samples (120 records - physical collection spine)
│   ├── environmental_samples_v1.xlsx       # T1 Excel format
│   ├── genomic_sequences_v1.csv            # T2 Genomic Sequences (55 records - 16S/ITS/Metagenomics)
│   ├── genomic_sequences_v1.xlsx           # T2 Excel format
│   ├── metabolomic_profiles_v1.csv         # T3 Metabolomic Profiles (90 records - LC-MS bioactives & features)
│   ├── metabolomic_profiles_v1.xlsx        # T3 Excel format
│   ├── heritage_knowledge_v1.csv           # T4 Heritage Knowledge (52 records - Traditional Ethnobotany)
│   ├── heritage_knowledge_v1.xlsx          # T4 Excel format
│   ├── qc_log_v1.csv                       # T5 Quality Control Log (Automated validation trace)
│   ├── qc_log_v1.xlsx                      # T5 Excel format
│   └── zw_biobank_v1.0_all_tables.xlsx     # Combined multi-tab workbook of all 5 core tables
├── raw/                                    # Raw collection evidence & registered source manifests
│   ├── zw_src_001_eastern_highlands/       # Source ZW-SRC-001 (Eastern Highlands wild/cultivated flora)
│   ├── zw_src_002_mazowe/                  # Source ZW-SRC-002 (Mazowe Valley agricultural & river catchment)
│   ├── zw_src_003_zvishavane/              # Source ZW-SRC-003 (Zvishavane communal lands)
│   ├── zw_src_004_heritage_knowledge/      # Source ZW-SRC-004 (Traditional knowledge interviews)
│   ├── zw_src_005_national_herbarium/      # Source ZW-SRC-005 (National Herbarium voucher verification)
│   ├── zw_src_006_sirdc_lcms/              # Source ZW-SRC-006 (SIRDC LC-MS core laboratory platform)
│   └── zw_src_007_opportunistic/           # Source ZW-SRC-007 (Opportunistic environmental monitoring)
├── labels/                                 # Machine Learning training labels & annotation guide
│   ├── label_taxonomy.csv                  # 10 formal label classes with positive/negative examples
│   ├── annotation_guide.pdf                # Annotation methodology, verification, & adjudication guide
│   └── annotations_v1.jsonl                # 400 applied machine learning annotation records
├── validation/                             # Automated quality rules & release audit trails
│   ├── validation_rules.json               # 16 quality check rule definitions & thresholds
│   ├── quality_report_v1.pdf               # Generated PDF Quality Report (Annex D compliant)
│   └── error_log.csv                       # Real-time warning/error log from validation engine
├── governance/                             # Legal, ethics, consent, & compliance frameworks
│   ├── source_register.csv                 # Register of 7 physical sources with access terms & fallbacks
│   ├── bias_risk_register.csv              # 8 identified bias/risk metrics with SQL audit queries
│   ├── dpa_compliance_matrix.csv           # Zimbabwe Data Protection Act (Ch. 12:07) compliance matrix
│   ├── consent_log.csv                     # Anonymized registry of Prior Informed Consent (PIC) records
│   ├── consent_template.pdf                # Standardized PIC field interview template
│   ├── access_policy.pdf                   # Open vs Controlled access policy specification
│   ├── anonymization_plan.pdf              # AES-256 identity masking & location blurring protocol
│   ├── budget_refresh_and_handover.csv     # Financial handover & maintenance schedule
│   ├── next_90_days.md                     # Post-challenge implementation roadmap
│   ├── progress_log.csv                    # Project milestone tracking log
│   ├── self_assessment_checklist.csv       # POTRAZ §7 self-assessment checklist
│   ├── target_population_and_sampling.md   # Ecozone & ethnobotanical sampling frame methodology
│   └── license.txt                         # Sovereign controlled-access data license terms
└── scripts/                                # Python automation engine (Standard Library only)
    ├── validate.py                         # Quality control validator & governance refusal demonstration engine
    ├── machine_loading_test.py             # Machine readiness tester (CSV, Pandas, SQLite, QGIS, R)
    ├── generate_reports.py                 # Automated PDF report compiler (Quality & Handover reports)
    └── build_manifest.py                   # Cryptographic SHA-256 manifest generator & integrity verifier
```

---

## 3. Architecture Diagrams

### Diagram 1: Overall End-to-End System & Data Pipeline Architecture

The end-to-end architecture ingests multi-modal raw data from physical collection sources, enforces strict governance gates and location masking, validates data through pure Python rules, structures datasets into SQLite/CSV tiers, and exposes machine-ready data for AI/ML modeling and institutional handover.

```mermaid
flowchart TD
    subgraph SOURCING["1. Physical & Heritage Data Sources"]
        SRC1["ZW-SRC-001: Eastern Highlands"]
        SRC2["ZW-SRC-002: Mazowe Catchment"]
        SRC3["ZW-SRC-003: Zvishavane Lands"]
        SRC4["ZW-SRC-004: Ethnobotanical TK"]
        SRC5["ZW-SRC-005: National Herbarium"]
        SRC6["ZW-SRC-006: SIRDC LC-MS Core"]
        SRC7["ZW-SRC-007: River Sediment"]
    end

    subgraph GOVERNANCE["2. Governance & Consent Control Layer"]
        PIC["Prior Informed Consent (FPIC)"]
        BSA["Benefit-Sharing Agreement (BSA)"]
        AES["AES-256 Encrypted Identity Vault (SIRDC Custody)"]
        MASK["Ward-Centroid Location Masking"]
        SACRED["Sacred Knowledge Exclusion Filter"]
    end

    subgraph PROCESSING["3. Ingestion & Preprocessing Pipeline"]
        PRE_ENV["GPS & Ecozone Normalization"]
        PRE_GEN["Nanopore 16S/ITS Quality Trimming"]
        PRE_MET["LC-MS Feature Extraction & Peak Alignment"]
        PRE_TK["Shona / Ndebele Language Tagging & ICD-11 Mapping"]
    end

    subgraph VALIDATION["4. Validation Engine (scripts/validate.py)"]
        VAL_RULES["validation_rules.json (16 Rule Sets)"]
        VAL_CHECK{"Automated Integrity Check"}
        ERR_LOG["validation/error_log.csv"]
        QC_TABLE["processed/qc_log_v1.csv"]
    end

    subgraph STORAGE["5. Structured Multi-Modal Storage (processed/)"]
        T1["T1: environmental_samples_v1.csv"]
        T2["T2: genomic_sequences_v1.csv"]
        T3["T3: metabolomic_profiles_v1.csv"]
        T4["T4: heritage_knowledge_v1.csv"]
        LABELS["labels/annotations_v1.jsonl (400 Annotations)"]
        SQL_DB["SQLite 3 Database (schema/schema.sql)"]
    end

    subgraph CONSUMPTION["6. Machine Loading & Downstream Handover"]
        LOADER["scripts/machine_loading_test.py"]
        REPORTS["scripts/generate_reports.py"]
        MANIFEST["manifest.csv (SHA-256 Hashes)"]
        AI_MODELS["Foundation AI / ML Training Pipelines"]
    end

    SOURCING --> GOVERNANCE
    GOVERNANCE -->|Consent Approved| PROCESSING
    GOVERNANCE -.->|Sacred / No Consent| REJECT[DB CHECK Refusal / Exclusion]

    PROCESSING --> VALIDATION
    VAL_RULES --> VAL_CHECK
    VAL_CHECK -->|Pass / Warn| STORAGE
    VAL_CHECK -->|Critical Error| ERR_LOG
    VAL_CHECK --> QC_TABLE

    STORAGE --> SQL_DB
    SQL_DB --> LOADER
    SQL_DB --> REPORTS
    SQL_DB --> MANIFEST
    LOADER --> AI_MODELS
```

---

### Diagram 2: Relational Schema & Entity-Relationship Architecture (ERD)

The data architecture is structured around five core tables linked via strict foreign key relationships and traceable provenance.

```mermaid
erDiagram
    heritage_knowledge ||--o{ environmental_samples : "guides collection of"
    source_register ||--o{ heritage_knowledge : "originates from"
    source_register ||--o{ environmental_samples : "collected at"
    environmental_samples ||--o{ genomic_sequences : "derived from (physical sample)"
    environmental_samples ||--o{ metabolomic_profiles : "derived from (physical sample)"
    environmental_samples ||--o{ qc_log : "evaluated in"

    heritage_knowledge {
        string tk_id PK "ZW-TK-YYYY-NNN"
        string source_id FK "ZW-SRC-XXX"
        string holder_pseudonym_id "Encrypted SIRDC Reference"
        string consent_reference "FPIC Reference"
        string knowledge_type "plant-disease | preparation | ecological"
        string local_plant_name "Shona / Ndebele verbatim"
        string disease_target_icd11 "Derived ICD-11 Code"
        string sensitivity_level "public | community-restricted"
        string benefit_sharing_agreement_ref "Signed BSA Reference"
        string withdrawal_status "active | withdrawn"
    }

    environmental_samples {
        string sample_id PK "ZW-SMP-YYYY-NNN"
        string collection_event_id "Event Identifier"
        string source_id FK "ZW-SRC-XXX"
        string ecozone "Eastern Highlands | Mazowe | Zvishavane | Other"
        float gps_latitude "WGS84 (-22.5 to -15.5)"
        float gps_longitude "WGS84 (25.0 to 33.1)"
        int location_masked "0 = Raw, 1 = Ward-Centroid"
        string sample_type "soil | plant_tissue | fungus | water | bark | root"
        string heritage_use_ref FK "ZW-TK-YYYY-NNN (Optional)"
    }

    genomic_sequences {
        string sequence_id PK "ZW-SEQ-YYYY-NNN"
        string sample_id FK "ZW-SMP-YYYY-NNN"
        string target_gene "16S_rRNA | ITS | whole_metagenome"
        string sequencing_platform "Oxford Nanopore MinION / GridION"
        string fastq_sha256 "SHA-256 Checksum"
        float mean_q_score "Quality Metric (> 10.0)"
        string raw_data_path "File URI"
    }

    metabolomic_profiles {
        string metabolite_id PK "ZW-MET-YYYY-NNN"
        string sample_id FK "ZW-SMP-YYYY-NNN"
        string instrument_platform "Thermo Q-Exactive LC-MS"
        string compound_name_putative "Identified Bioactive / Secondary Metabolite"
        float precursor_mz "Mass-to-Charge Ratio"
        float retention_time_min "Chromatographic Retention Time"
        int msi_identification_level "Level 1 to 4 Identification Confidence"
    }

    qc_log {
        string qc_id PK "ZW-QC-YYYY-NNN"
        string entity_type "sample | sequence | profile | tk"
        string entity_id "Target PK Reference"
        string check_code "V01 to V16 Rule Code"
        string check_status "pass | warn | fail"
        string execution_timestamp "ISO 8601 Timestamp"
    }

    source_register {
        string source_id PK "ZW-SRC-001 to 007"
        string source_name "Institutional or Geographic Source"
        string primary_steward "Managing Entity"
        string access_status "lawful_access_verified"
    }
```

---

### Diagram 3: Governance, Legal & Security Architecture

The governance framework enforces legal compliance with the Zimbabwe Data Protection Act (DPA Ch. 12:07), Nagoya Protocol, and National Biotechnology Authority (NBA) guidelines.

```mermaid
flowchart LR
    subgraph DATA_INPUTS["Data Inputs"]
        HOLDER["Community Knowledge Holder"]
        SAMPLE["Botanical / Environmental Sample"]
    end

    subgraph LEGAL_GATES["Database & Enforcement Gates"]
        GATE1{"1. Prior Informed Consent (FPIC)"}
        GATE2{"2. Sacred Knowledge Exclusion"}
        GATE3{"3. NBA Access Permit Gate"}
        GATE4{"4. DPA Identity Masking"}
    end

    subgraph CUSTODY_TIERS["Access Control Tiers"]
        PUBLIC["PUBLIC TIER
        - Ward-Centroid Coordinates
        - Anonymized Metadata
        - Open CSV / JSON Datasets"]
        
        RESTRICTED["COMMUNITY-RESTRICTED TIER
        - Audio Recordings
        - Raw GPS Coordinates
        - Vetted Academic / AI Access"]
        
        SIRDC_VAULT["ENCAPSULATED SIRDC VAULT
        - AES-256 Holder Identity Register
        - Direct Benefit-Sharing Royalty Ledger
        - Zero External Network Access"]
    end

    HOLDER --> GATE1
    SAMPLE --> GATE3
    
    GATE1 -->|Consent Verified| GATE2
    GATE1 -.->|No Consent| BLOCK1[RELEASE BLOCKED]
    
    GATE2 -->|Non-Sacred| GATE4
    GATE2 -.->|Sacred Material| BLOCK2[COLLECTION PROHIBITED]
    
    GATE3 -->|Permit Active| GATE4
    GATE3 -.->|Missing Permit| BLOCK3[PROCESSING BLOCKED]
    
    GATE4 --> PUBLIC
    GATE4 --> RESTRICTED
    GATE4 --> SIRDC_VAULT
```

---

### Diagram 4: Validation Engine Workflow & Proofs Architecture

The automated validation engine (`scripts/validate.py`) executes 888+ checks across 7 quality dimensions and supports interactive refusal demonstrations.

```mermaid
sequenceDiagram
    autonumber
    participant CLI as Operator / CLI Script
    participant VAL as scripts/validate.py
    participant RULES as validation_rules.json
    participant DB as schema/schema.sql (SQLite)
    participant LOG as validation/error_log.csv
    participant REP as scripts/generate_reports.py

    CLI->>VAL: Execute standard validation (python scripts/validate.py)
    VAL->>RULES: Read threshold definitions & 16 check codes (V01-V16)
    VAL->>DB: Load processed dataset tables & execute SQL integrity queries
    
    alt Validation Batch Clean
        DB-->>VAL: 0 Critical Failures, All constraints passed
        VAL->>LOG: Write execution status (STATUS: BATCH CLEAN)
        VAL-->>CLI: Display summary breakdown (888+ checks passed)
    else Validation Violation Detected
        DB-->>VAL: Constraint failure / Invalid coordinate / Unmatched FK
        VAL->>LOG: Log error code, target ID, and action requirement
        VAL-->>CLI: Emit warning / halt release build
    end

    opt Governance Refusal Demonstration Mode
        CLI->>VAL: Run refusal demo (python scripts/validate.py --demo)
        VAL->>DB: Attempt Sacred Knowledge insert -> SQL CHECK Refusal
        VAL->>DB: Attempt Post-dated Consent -> SQL CHECK Refusal
        VAL->>DB: Attempt No-Consent Heritage Sample -> SQL CHECK Refusal
        VAL->>DB: Execute Holder Withdrawal -> Trigger 30-day propagation view
        VAL-->>CLI: Print 4 successfully demonstrated refusal proofs
    end

    opt Report & Manifest Generation
        CLI->>REP: Run report compiler (python scripts/generate_reports.py)
        REP->>LOG: Read QC log & error log
        REP-->>CLI: Render quality_report_v1.pdf & structure summary
    end
```

---

## 4. Technical Specifications & Structural Constraints

### 4.1 The Four Structural Governance Constraints
Governance policies in ZW-BioBank v1.0 are enforced at the database engine level inside [`schema/schema.sql`](file:///C:/Users/HP/Downloads/Miti%20Ai%20BioBank_v1.0/mitiAI_ZW_Biobank%20v1.1_Dataset/mitiai_zw_biobank_v1.0_ai4i_data/schema/schema.sql) and cannot be overridden by application logic:

| Rule | Description | SQL / Validator Constraint |
|---|---|---|
| **1. Consent Gate** | A sample collected via ethnobotanical guidance MUST link to a valid Prior Informed Consent reference. | `CHECK (heritage_use_ref IS NULL OR consent_reference IS NOT NULL)` |
| **2. Sacred Exclusion** | Sacred traditional knowledge is never collected or stored in the database under any condition. | `CHECK (sensitivity_level IN ('public', 'community-restricted'))` |
| **3. Prior Consent** | Consent must be formally granted prior to or on the exact date of the field interview. | `CHECK (consent_date <= interview_date)` |
| **4. Permit Gate** | Physical specimen processing cannot be finalized without an active NBA permit reference. | `nba_permit_ref IS NOT NULL` check during sample processing stage |

---

### 4.2 Focal Specimen Lineages

| Pillar Specimen | Shona / Ndebele Name | Target Organ | Primary Bioactives / Metabolites | Core Application |
|---|---|---|---|---|
| **Medicinal Ginger**<br>*(Siphonochilus aethiopicus* & *Zingiber officinale)* | *Tsangamidzi* (sn)<br>*Isiphepheto* (nd) | Rhizome & Root | Siphonochilone, [6]-Gingerol, [6]-Shogaol, Zerumbone | Respiratory distress, asthma, antimicrobial assays |
| **Pepper-Bark Tree**<br>*(Warburgia salutaris)* | *Muranga* (sn)<br>*Isibhaha* (nd) | Trunk Bark & Leaf | Muzigadial, Polygodial, Warburganal, Verbascoside | Chest infections, malarial fever, COX anti-inflammatory |
| **Water Hyacinth**<br>*(Eichhornia crassipes)* | *Yacinthi Yemumvura* (sn)<br>*Inkazana Yemanzini* (nd) | Aquatic Plant & Sediment | Rhizobiome endophytes (*Streptomyces*), Luteolin, Apigenin | Heavy metal phytoremediation & environmental monitoring |

---

### 4.3 Technical Verification Suite (5 Minimum Proofs)

The repository provides five standalone, zero-dependency Python scripts to demonstrate compliance with the AI for Impact Challenge requirements:

```bash
# PROOF 1: Load Data & Verify Machine Readiness across Python, SQL, GIS
python scripts/machine_loading_test.py

# PROOF 2 & 4: Execute Full Data Provenance Trace & Run Quality Checks
python scripts/validate.py

# PROOF 4: Demonstrate 4 Automated Governance & Refusal Gates
python scripts/validate.py --demo

# PROOF 3 & 5: Generate Structure Summaries & Compliance PDF Reports
python scripts/generate_reports.py

# PROOF 5: Verify Cryptographic SHA-256 Manifest & File Handover Integrity
python scripts/build_manifest.py --verify
```

---
*Miti AI Consortium · Scientific Sovereignty & AI Innovation for Zimbabwe*
