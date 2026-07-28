-- =====================================================================
-- ZW-BioBank v1.0 — Relational Schema (SQL DDL)
-- Miti AI Consortium · POTRAZ AI for Impact Challenge 2026 · Track 1: Data
-- Lead Innovator: Mutsa M Mutepfa
--
-- Dialect: SQLite 3 (portable reference implementation).
-- Satisfies Minimum Expectations §6.1 "schema.json, SQL DDL, or equivalent
-- machine-readable schema". A JSON rendering of the same schema is at
-- schema/schema.json; both are generated from one definition and cannot
-- disagree.
--
-- FIELD NAMES follow the submitted proposal (§3.1, §3.2) exactly:
--   T1 environmental_samples   sample_id       ZW-SMP-YYYY-NNN
--   T2 genomic_sequences       sequence_id     ZW-SEQ-YYYY-NNN
--   T3 metabolomic_profiles    metabolite_id   ZW-MET-YYYY-NNN
--   T4 heritage_knowledge      tk_id           ZW-TK-YYYY-NNN
--   T5 qc_log                  qc_id           ZW-QC-YYYY-NNN
--
-- FOUR RULES ARE STRUCTURAL, not policy. No operator can bypass them:
--   (1) CONSENT GATE     a sample collected because of a holder's knowledge
--                        cannot be written without a consent reference.
--   (2) SACRED EXCLUSION sensitivity_level admits 'public' and
--                        'community-restricted'. 'sacred' is absent by
--                        design. Proposal §3.2 states "Sacred = never
--                        collected"; this is that sentence expressed as a
--                        constraint rather than an intention.
--   (3) PERMIT GATE      processing cannot be marked complete without the
--                        NBA permit reference (proposal §3.2 validation
--                        rule for nba_permit_ref), and protected-area
--                        collection requires an access permit.
--   (4) DEPTH RULE       collection_depth_cm is required when
--                        sample_type = 'soil' (proposal §3.2).
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- T4 · heritage_knowledge  (declared first: referenced by T1)
-- Stream C. The targeting layer, not a cultural addendum.
--
-- Holder identity is NEVER stored here. holder_pseudonym_id resolves to a
-- named individual only through the Holder Identity Register: AES-256
-- encrypted, held in SIRDC institutional custody, distributed at no access
-- tier. That register is what makes benefit-sharing enforceable; keeping it
-- out of this table is what makes the rest of the dataset shareable.
-- Community-level attribution (district, ward) is used by default, with
-- named attribution as an explicit opt-in (DPA Ch.12:07 anonymisation row).
-- ---------------------------------------------------------------------
CREATE TABLE heritage_knowledge (
    tk_id                       TEXT PRIMARY KEY,          -- ZW-TK-YYYY-NNN
    source_id                   TEXT NOT NULL,             -- FK to governance/source_register.csv
    holder_pseudonym_id         TEXT NOT NULL,
    community_council_id        TEXT NOT NULL,
    council_endorsement_ref     TEXT NOT NULL,
    consent_reference           TEXT NOT NULL,             -- FPIC-ZW-YYYY-CNNN
    consent_date                TEXT NOT NULL,             -- ISO 8601
    collection_language         TEXT NOT NULL CHECK (collection_language IN ('sn','nd','en')),
    interview_date              TEXT NOT NULL,
    interviewer_id              TEXT NOT NULL,

    knowledge_type              TEXT NOT NULL CHECK (knowledge_type IN
                                ('plant-disease','preparation','ecological')),
    local_plant_name            TEXT NOT NULL,
    language_tag                TEXT NOT NULL CHECK (language_tag IN ('sn','nd','en')),
    scientific_name             TEXT,                      -- verified post-collection vs Herbarium
    disease_target_local        TEXT NOT NULL,             -- verbatim, never paraphrased
    disease_target_en           TEXT,                      -- derived translation
    translation_status          TEXT NOT NULL DEFAULT 'pending'
                                CHECK (translation_status IN ('pending','machine_draft','human_verified')),
    disease_target_icd11        TEXT,
    preparation_method          TEXT,                      -- verbatim
    preparation_class           TEXT CHECK (preparation_class IN
                                ('decoction','infusion','poultice','powder','maceration',
                                 'smoke_inhalation','topical_oil','chewed_raw','other')),
    plant_part_used             TEXT CHECK (plant_part_used IN
                                ('root','bark','leaf','stem','flower','fruit','seed','whole','na')),
    administration_route        TEXT,
    seasonality_of_use          TEXT CHECK (seasonality_of_use IN ('dry','wet','both','unspecified')),

    province                    TEXT NOT NULL,
    district                    TEXT NOT NULL,             -- community-level attribution unit
    ward                        TEXT,
    named_attribution_opt_in    INTEGER NOT NULL DEFAULT 0 CHECK (named_attribution_opt_in IN (0,1)),

    -- GOVERNANCE ------------------------------------------------------
    -- 'sacred' is deliberately absent. There is no value of this column
    -- that stores sacred knowledge, and therefore no field in this schema
    -- in which it could hide.
    sensitivity_level           TEXT NOT NULL
                                CHECK (sensitivity_level IN ('public','community-restricted')),
    data_sensitivity            TEXT NOT NULL CHECK (data_sensitivity IN
                                ('public','internal','confidential','sensitive','anonymized')),
    benefit_sharing_agreement_ref TEXT NOT NULL,           -- signed BEFORE collection
    withdrawal_status           TEXT NOT NULL DEFAULT 'active'
                                CHECK (withdrawal_status IN ('active','withdrawn')),
    withdrawal_date             TEXT,
    audio_recording_ref         TEXT,                      -- restricted tier only
    bilingual_validation_status TEXT NOT NULL DEFAULT 'pending'
                                CHECK (bilingual_validation_status IN ('pending','passed','failed')),
    validator_id                TEXT,

    created_at                  TEXT NOT NULL,
    record_status               TEXT NOT NULL DEFAULT 'active'
                                CHECK (record_status IN ('active','superseded','redacted')),

    CHECK (withdrawal_status = 'active' OR withdrawal_date IS NOT NULL),
    CHECK (consent_date <= interview_date)                 -- consent is PRIOR, or it is not FPIC
);

-- ---------------------------------------------------------------------
-- T1 · environmental_samples
-- Stream D + the physical collection event. Root provenance of everything
-- downstream: every sequence, metabolite and annotation traces here.
-- ---------------------------------------------------------------------
CREATE TABLE environmental_samples (
    sample_id               TEXT PRIMARY KEY,              -- ZW-SMP-YYYY-NNN
    collection_event_id     TEXT NOT NULL,
    source_id               TEXT NOT NULL,                 -- FK to governance/source_register.csv
    -- 'Other' admits the sites the sampling frame never named: a stand of trees
    -- on a roadside, the bush behind a homestead, anywhere a holder leads the
    -- team outside the three Phase I zones. Only the three named zones carry a
    -- quota; 'Other' is reported out of frame (V22) and never counted into it,
    -- so a quota is never met by relabelling convenience collection.
    ecozone                 TEXT NOT NULL CHECK (ecozone IN
                            ('Eastern Highlands','Mazowe','Zvishavane','Other')),
    province                TEXT NOT NULL,
    district                TEXT NOT NULL,
    ward                    TEXT,
    -- Free text by necessity: the point is that no vocabulary covered the site.
    -- Required when ecozone = 'Other' (see the locality CHECK below).
    locality_description    TEXT,
    land_tenure             TEXT NOT NULL CHECK (land_tenure IN
                            ('communal','resettlement','private','state_protected')),

    -- Coordinate policy: raw GPS at >=4 decimal places is captured in the
    -- field and retained in the restricted tier. Public release carries
    -- ward-centroid coordinates with location_masked = 1 and
    -- gps_precision_m widened accordingly. A public dataset must not
    -- double as a harvest map for a species a community depends on.
    gps_latitude            REAL NOT NULL CHECK (gps_latitude BETWEEN -22.5 AND -15.5),
    gps_longitude           REAL NOT NULL CHECK (gps_longitude BETWEEN 25.0 AND 33.1),
    gps_precision_m         INTEGER NOT NULL,
    location_masked         INTEGER NOT NULL DEFAULT 0 CHECK (location_masked IN (0,1)),
    altitude_m              INTEGER CHECK (altitude_m BETWEEN 0 AND 2600),

    sample_type             TEXT NOT NULL CHECK (sample_type IN
                            ('soil','plant_tissue','fungus','water','bark','root','venom')),
    collection_depth_cm     INTEGER CHECK (collection_depth_cm BETWEEN 0 AND 100),
    local_name              TEXT,
    local_name_language     TEXT CHECK (local_name_language IN ('sn','nd','en')),
    scientific_name         TEXT,
    taxon_confidence        TEXT CHECK (taxon_confidence IN
                            ('field_tentative','herbarium_confirmed','sequence_confirmed')),
    voucher_specimen_ref    TEXT,                          -- National Herbarium accession

    collection_date         TEXT NOT NULL,                 -- ISO 8601, >= 2026-09-01
    season                  TEXT NOT NULL CHECK (season IN ('dry','wet')),
    soil_ph                 REAL CHECK (soil_ph BETWEEN 0 AND 14),
    temperature_celsius     REAL,
    rainfall_prior_30d_mm   REAL CHECK (rainfall_prior_30d_mm >= 0),
    canopy_cover_pct        INTEGER CHECK (canopy_cover_pct BETWEEN 0 AND 100),

    collector_id            TEXT NOT NULL,
    preservation_method     TEXT NOT NULL CHECK (preservation_method IN
                            ('rnalater','silica_gel','flash_frozen','ethanol_70','air_dried')),
    -- Operational metric the mobile laboratory exists to hold down, and a
    -- degradation covariate for metabolomics. Measured, not asserted.
    minutes_to_preservation INTEGER NOT NULL CHECK (minutes_to_preservation >= 0),
    processing_lab          TEXT NOT NULL,
    chain_of_custody_ref    TEXT NOT NULL,

    -- PROVENANCE ------------------------------------------------------
    -- Populated when a holder's knowledge is the reason this sample exists.
    -- NULL means the sample was chosen on ecological criteria alone.
    heritage_use_ref        TEXT REFERENCES heritage_knowledge(tk_id) ON DELETE RESTRICT,
    consent_reference       TEXT,
    nba_permit_ref          TEXT,
    access_permit_ref       TEXT,

    sequencing_status       TEXT NOT NULL DEFAULT 'pending' CHECK (sequencing_status IN
                            ('pending','in_progress','complete','failed')),
    lc_ms_status            TEXT NOT NULL DEFAULT 'pending' CHECK (lc_ms_status IN
                            ('pending','in_progress','complete','failed','not_applicable')),

    data_sensitivity        TEXT NOT NULL DEFAULT 'public' CHECK (data_sensitivity IN
                            ('public','internal','confidential','sensitive','anonymized')),
    created_at              TEXT NOT NULL,
    record_status           TEXT NOT NULL DEFAULT 'active'
                            CHECK (record_status IN ('active','superseded','redacted')),

    -- (1) CONSENT GATE
    CHECK (heritage_use_ref IS NULL OR consent_reference IS NOT NULL),
    -- (3) PERMIT GATE — proposal §3.2: nba_permit_ref must be present
    --     before processing is marked complete.
    CHECK (nba_permit_ref IS NOT NULL
           OR (sequencing_status <> 'complete' AND lc_ms_status <> 'complete')),
    CHECK (land_tenure <> 'state_protected' OR access_permit_ref IS NOT NULL),
    -- (4) DEPTH RULE — proposal §3.2
    CHECK (sample_type <> 'soil' OR collection_depth_cm IS NOT NULL),
    -- A masked record must declare degraded precision.
    CHECK (location_masked = 0 OR gps_precision_m >= 1000),
    -- (5) LOCALITY RULE — 'Other' exists so a real sample is never refused for
    --     being off the sampling frame. It is not a way to skip saying where
    --     you were: with no zone name doing the describing, the description
    --     has to be written down or the site cannot be found again.
    CHECK (ecozone <> 'Other'
           OR (locality_description IS NOT NULL AND locality_description <> ''))
);

-- ---------------------------------------------------------------------
-- T2 · genomic_sequences — Stream A
-- ---------------------------------------------------------------------
CREATE TABLE genomic_sequences (
    sequence_id             TEXT PRIMARY KEY,              -- ZW-SEQ-YYYY-NNN
    sample_id               TEXT NOT NULL REFERENCES environmental_samples(sample_id) ON DELETE RESTRICT,
    platform                TEXT NOT NULL CHECK (platform IN
                            ('ont_minion','ont_gridion','illumina_miseq','illumina_nextseq')),
    library_prep_kit        TEXT,
    flowcell_id             TEXT,
    basecalling_model       TEXT,                          -- reproducibility: ONT output is model-dependent
    run_date                TEXT NOT NULL,
    sequencing_lab          TEXT NOT NULL,
    target_region           TEXT NOT NULL CHECK (target_region IN
                            ('16s_rrna','its','rbcl','matk','shotgun_metagenome','whole_genome')),

    read_count              INTEGER CHECK (read_count >= 0),
    total_bases             INTEGER CHECK (total_bases >= 0),
    mean_read_length_bp     INTEGER CHECK (mean_read_length_bp >= 0),
    read_n50_bp             INTEGER CHECK (read_n50_bp >= 0),
    mean_q_score            REAL CHECK (mean_q_score BETWEEN 0 AND 60),
    assembly_method         TEXT,
    assembly_n50_bp         INTEGER,
    contig_count            INTEGER,

    -- LABELS (see labels/label_taxonomy.csv)
    taxonomic_assignment    TEXT,
    assignment_method       TEXT,                          -- classifier + reference DB version
    organism_novelty        TEXT CHECK (organism_novelty IN
                            ('known','divergent','putative_novel','unassessed')),
    best_blast_accession    TEXT,
    best_blast_pct_identity REAL CHECK (best_blast_pct_identity BETWEEN 0 AND 100),
    predicted_function      TEXT,
    disease_target_relevance REAL CHECK (disease_target_relevance BETWEEN 0 AND 1),
    annotation_confidence   REAL CHECK (annotation_confidence BETWEEN 0 AND 1),
    bgc_count               INTEGER CHECK (bgc_count >= 0),   -- secondary metabolite gene clusters, antiSMASH
    heritage_link           TEXT,                          -- denormalised tk_id for label joins

    file_path_fasta         TEXT NOT NULL,
    file_checksum_sha256    TEXT NOT NULL CHECK (length(file_checksum_sha256) = 64),
    file_size_bytes         INTEGER,
    data_sensitivity        TEXT NOT NULL DEFAULT 'public' CHECK (data_sensitivity IN
                            ('public','internal','confidential','sensitive','anonymized')),
    qc_status               TEXT NOT NULL DEFAULT 'pending'
                            CHECK (qc_status IN ('pending','pass','warning','fail')),
    created_at              TEXT NOT NULL
);

-- ---------------------------------------------------------------------
-- T3 · metabolomic_profiles — Stream B. One row per detected feature.
-- Annotation confidence uses the Metabolomics Standards Initiative (MSI)
-- levels 1–4 rather than a bespoke scale, so an external reviewer can
-- interpret it without our documentation.
-- ---------------------------------------------------------------------
CREATE TABLE metabolomic_profiles (
    metabolite_id           TEXT PRIMARY KEY,              -- ZW-MET-YYYY-NNN
    sample_id               TEXT NOT NULL REFERENCES environmental_samples(sample_id) ON DELETE RESTRICT,
    extract_id              TEXT NOT NULL,
    extraction_solvent      TEXT NOT NULL,
    extraction_date         TEXT NOT NULL,
    instrument              TEXT NOT NULL,
    chromatography_column   TEXT,
    ionization_mode         TEXT NOT NULL CHECK (ionization_mode IN ('positive','negative')),
    collision_energy_ev     REAL,

    retention_time_min      REAL CHECK (retention_time_min >= 0),
    mz_measured             REAL NOT NULL CHECK (mz_measured > 0),
    mz_error_ppm            REAL,
    peak_area               REAL CHECK (peak_area >= 0),
    relative_abundance      REAL CHECK (relative_abundance BETWEEN 0 AND 1),

    putative_compound_name  TEXT,
    molecular_formula       TEXT,
    smiles_canonical        TEXT,                          -- RDKit-canonicalised at ingest
    inchikey                TEXT CHECK (inchikey IS NULL OR length(inchikey) = 27),
    msi_annotation_level    INTEGER CHECK (msi_annotation_level BETWEEN 1 AND 4),
    spectral_library        TEXT,
    library_match_score     REAL CHECK (library_match_score BETWEEN 0 AND 1),
    external_db_hit         TEXT,
    compound_class          TEXT CHECK (compound_class IN
                            ('antimicrobial','anti-parasitic','anti-inflammatory','unknown')),
    compound_novelty        TEXT CHECK (compound_novelty IN
                            ('known','analogue','putative_novel','unassessed')),
    annotation_confidence   REAL CHECK (annotation_confidence BETWEEN 0 AND 1),

    file_path_mzml          TEXT NOT NULL,
    file_checksum_sha256    TEXT NOT NULL CHECK (length(file_checksum_sha256) = 64),
    data_sensitivity        TEXT NOT NULL DEFAULT 'internal' CHECK (data_sensitivity IN
                            ('public','internal','confidential','sensitive','anonymized')),
    qc_status               TEXT NOT NULL DEFAULT 'pending'
                            CHECK (qc_status IN ('pending','pass','warning','fail')),
    created_at              TEXT NOT NULL
);

-- ---------------------------------------------------------------------
-- T5 · qc_log — every validation event, on every record, retained
-- permanently. Minimum Expectations §4.7: pass / warning / fail with an
-- issue log carrying owner, severity, correction action and status.
-- ---------------------------------------------------------------------
CREATE TABLE qc_log (
    qc_id                   TEXT PRIMARY KEY,              -- ZW-QC-YYYY-NNN
    target_table            TEXT NOT NULL CHECK (target_table IN
                            ('environmental_samples','genomic_sequences',
                             'metabolomic_profiles','heritage_knowledge')),
    target_record_id        TEXT NOT NULL,
    check_name              TEXT NOT NULL,
    quality_dimension       TEXT NOT NULL CHECK (quality_dimension IN
                            ('completeness','accuracy','consistency','validity',
                             'uniqueness','timeliness','integrity')),
    check_type              TEXT NOT NULL CHECK (check_type IN
                            ('schema','completeness','controlled_vocab','range',
                             'cross_reference','consent_gate','duplicate','novelty',
                             'checksum','privacy','bias_coverage','machine_readability')),
    check_result            TEXT NOT NULL CHECK (check_result IN ('pass','warning','fail')),
    severity                TEXT NOT NULL CHECK (severity IN ('info','low','medium','high','critical')),
    message                 TEXT NOT NULL,
    checked_by              TEXT NOT NULL CHECK (checked_by IN
                            ('automated','human_audit','bilingual_validator')),
    checked_at              TEXT NOT NULL,
    issue_owner             TEXT,
    correction_action       TEXT,
    corrected_at            TEXT,
    corrected_by            TEXT,
    resolution_status       TEXT NOT NULL DEFAULT 'open'
                            CHECK (resolution_status IN ('open','resolved','waived')),

    -- A critical finding cannot be waived without a recorded action and owner.
    CHECK (NOT (severity = 'critical' AND resolution_status = 'waived'
                AND (correction_action IS NULL OR issue_owner IS NULL)))
);

-- ---------------------------------------------------------------------
-- INDEXES
-- ---------------------------------------------------------------------
CREATE INDEX idx_smp_heritage  ON environmental_samples(heritage_use_ref);
CREATE INDEX idx_smp_ecozone   ON environmental_samples(ecozone, season);
CREATE INDEX idx_smp_source    ON environmental_samples(source_id);
CREATE INDEX idx_seq_sample    ON genomic_sequences(sample_id);
CREATE INDEX idx_met_sample    ON metabolomic_profiles(sample_id);
CREATE INDEX idx_met_inchikey  ON metabolomic_profiles(inchikey);
CREATE INDEX idx_qc_target     ON qc_log(target_table, target_record_id);
CREATE INDEX idx_tk_withdrawal ON heritage_knowledge(withdrawal_status);

-- ---------------------------------------------------------------------
-- VIEW v_provenance_chain
-- The benefit-sharing claim expressed as a query rather than a promise.
-- For any compound: the holder pseudonym, the council that endorsed the
-- interview, and the agreement signed before collection.
-- ---------------------------------------------------------------------
CREATE VIEW v_provenance_chain AS
SELECT  m.metabolite_id,
        m.putative_compound_name,
        m.inchikey,
        m.compound_novelty,
        s.sample_id,
        s.ecozone,
        s.scientific_name,
        s.collection_date,
        k.tk_id,
        k.holder_pseudonym_id,
        k.community_council_id,
        k.council_endorsement_ref,
        k.consent_reference,
        k.benefit_sharing_agreement_ref,
        k.named_attribution_opt_in,
        k.withdrawal_status
FROM metabolomic_profiles  m
JOIN environmental_samples s ON m.sample_id        = s.sample_id
JOIN heritage_knowledge    k ON s.heritage_use_ref = k.tk_id
WHERE k.withdrawal_status = 'active'
  AND s.record_status     = 'active';

-- ---------------------------------------------------------------------
-- VIEW v_withdrawal_impact
-- Run on receipt of a withdrawal. Lists every downstream record that must
-- be pseudonymised or deleted inside the 30-day DPA commitment.
-- ---------------------------------------------------------------------
CREATE VIEW v_withdrawal_impact AS
SELECT  k.tk_id,
        k.withdrawal_date,
        s.sample_id,
        (SELECT COUNT(*) FROM genomic_sequences    g WHERE g.sample_id = s.sample_id) AS genomic_records,
        (SELECT COUNT(*) FROM metabolomic_profiles m WHERE m.sample_id = s.sample_id) AS metabolomic_records
FROM heritage_knowledge k
LEFT JOIN environmental_samples s ON s.heritage_use_ref = k.tk_id
WHERE k.withdrawal_status = 'withdrawn';

-- ---------------------------------------------------------------------
-- VIEW v_bias_coverage
-- Minimum Expectations §4.8. Representativeness is computed from the data,
-- not asserted in prose. Compare against the 200/150/150 ecozone quota and
-- the 30% Ndebele-language floor declared in the proposal.
-- ---------------------------------------------------------------------
CREATE VIEW v_bias_coverage AS
SELECT  s.ecozone,
        s.season,
        COUNT(*)                                                   AS samples,
        SUM(CASE WHEN s.heritage_use_ref IS NOT NULL THEN 1 ELSE 0 END) AS knowledge_led,
        SUM(CASE WHEN k.language_tag = 'nd' THEN 1 ELSE 0 END)      AS ndebele_linked,
        SUM(CASE WHEN k.language_tag = 'sn' THEN 1 ELSE 0 END)      AS shona_linked
FROM environmental_samples s
LEFT JOIN heritage_knowledge k ON s.heritage_use_ref = k.tk_id
WHERE s.record_status = 'active'
GROUP BY s.ecozone, s.season;
