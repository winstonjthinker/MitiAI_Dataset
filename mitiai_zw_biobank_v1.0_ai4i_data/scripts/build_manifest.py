#!/usr/bin/env python3
"""
Write manifest.csv: every file with path, size, SHA-256 checksum, version and
sensitivity level, as required by Minimum Expectations §6.1.

  python3 scripts/build_manifest.py            build or rebuild
  python3 scripts/build_manifest.py --verify   confirm nothing has been altered

Run this AFTER validate.py, which rewrites the qc log and error log.
"""
import csv, hashlib, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "manifest.csv")
VERSION = "v1.0.0"

# role, sensitivity, description
ROLE = {
 "README.md": ("documentation","public","Package overview, how to run everything, and what is specification versus illustrative"),
 "manifest.csv": ("integrity","public","This file. Excluded from its own checksum list."),

 "metadata/dataset_metadata.json": ("metadata","public","Dataset metadata card — Annex B keys verbatim"),
 "metadata/subset_metadata_environmental.json": ("metadata","public","Subset card — T1 environmental samples"),
 "metadata/subset_metadata_genomic.json": ("metadata","public","Subset card — T2 genomic sequences"),
 "metadata/subset_metadata_metabolomic.json": ("metadata","public","Subset card — T3 metabolomic profiles"),
 "metadata/subset_metadata_tk.json": ("metadata","public","Subset card — T4 heritage knowledge"),

 "schema/data_dictionary.csv": ("schema","public","156 documented fields — Annex A columns verbatim"),
 "schema/data_dictionary.xlsx": ("schema","public","Data dictionary formatted for presentation, with a coverage summary"),
 "schema/schema.json": ("schema","public","Machine-readable schema generated from the DDL"),
 "schema/schema.sql": ("schema","public","SQL DDL: tables, constraints, indexes and three governance views"),
 "schema/erd.svg": ("schema","public","Entity relationship diagram"),

 "processed/environmental_samples_v1.csv": ("data","public","T1 · Stream D (ILLUSTRATIVE)"),
 "processed/environmental_samples_v1.xlsx": ("data","public","T1 · Stream D Excel spreadsheet (ILLUSTRATIVE)"),
 "processed/genomic_sequences_v1.csv": ("data","public","T2 · Stream A (ILLUSTRATIVE)"),
 "processed/genomic_sequences_v1.xlsx": ("data","public","T2 · Stream A Excel spreadsheet (ILLUSTRATIVE)"),
 "processed/metabolomic_profiles_v1.csv": ("data","internal","T3 · Stream B (ILLUSTRATIVE)"),
 "processed/metabolomic_profiles_v1.xlsx": ("data","internal","T3 · Stream B Excel spreadsheet (ILLUSTRATIVE)"),
 "processed/heritage_knowledge_v1.csv": ("data","confidential","T4 · Stream C (ILLUSTRATIVE)"),
 "processed/heritage_knowledge_v1.xlsx": ("data","confidential","T4 · Stream C Excel spreadsheet (ILLUSTRATIVE)"),
 "processed/qc_log_v1.csv": ("quality","public","T5 · every validation event, written by validate.py"),
 "processed/qc_log_v1.xlsx": ("quality","public","T5 · every validation event Excel spreadsheet"),
 "processed/zw_biobank_v1.0_all_tables.xlsx": ("data","public","All-in-one Excel workbook containing all data streams as sheets"),

 "labels/label_taxonomy.csv": ("labels","public","Ten labels with definitions and positive/negative examples"),
 "labels/annotation_guide.pdf": ("labels","public","Annotator workflow, review and adjudication"),
 "labels/annotations_v1.jsonl": ("labels","public","Applied labels with annotator, guide version and review status"),

 "validation/validation_rules.json": ("validation","public","Machine-readable rules; the validator reads thresholds from here"),
 "validation/quality_report_v1.pdf": ("validation","public","Annex D quality report, generated from the qc log"),
 "validation/error_log.csv": ("validation","public","Warnings and failures with owner, severity, action and status"),

 "governance/source_register.csv": ("governance","public","Six sources with all seven required provenance fields"),
 "governance/bias_risk_register.csv": ("governance","public","Eight bias risks with runnable monitoring queries"),
 "governance/dpa_compliance_matrix.csv": ("governance","public","Data Protection Act [Chapter 12:07] compliance matrix"),
 "governance/consent_log.csv": ("governance","confidential","FPIC record per heritage knowledge holder"),
 "governance/consent_template.pdf": ("governance","public","FPIC template, English reference version"),
 "governance/anonymization_plan.pdf": ("governance","public","Structural controls, location masking, re-identification risk"),
 "governance/access_policy.pdf": ("governance","public","Tiers, roles, security, retention, prohibited uses"),
 "governance/self_assessment_checklist.csv": ("governance","public","Minimum Expectations §7 checklist, completed with evidence locations"),
 "governance/license.txt": ("governance","public","MIT for code; sovereign controlled access for data"),

 "scripts/validate.py": ("code","public","Ingest validator, checks V01–V21"),
 "scripts/build_manifest.py": ("code","public","This generator"),
 "scripts/machine_loading_test.py": ("code","public","Minimum Expectations §6.3 machine-loading demonstration"),
 "scripts/generate_reports.py": ("code","public","Generates the five PDF deliverables"),
}
for d, label in (("zw_src_001_eastern_highlands","ZW-SRC-001 Eastern Highlands"),
                 ("zw_src_002_mazowe","ZW-SRC-002 Mazowe"),
                 ("zw_src_003_zvishavane","ZW-SRC-003 Zvishavane"),
                 ("zw_src_004_heritage_knowledge","ZW-SRC-004 Heritage knowledge"),
                 ("zw_src_005_national_herbarium","ZW-SRC-005 National Herbarium"),
                 ("zw_src_006_sirdc_lcms","ZW-SRC-006 SIRDC LC-MS"),
                 ("zw_src_007_opportunistic","ZW-SRC-007 Opportunistic Sites")):
    tier = "confidential" if "heritage" in d else "public"
    ROLE[f"raw/{d}/README.md"] = ("documentation", tier, f"Raw directory convention and access terms — {label}")

 # Governance documents
ROLE["governance/budget_refresh_and_handover.csv"] = ("governance","public","Budget refresh and handover timeline")
ROLE["governance/next_90_days.md"] = ("governance","public","Next 90 days implementation plan")
ROLE["governance/progress_log.csv"] = ("governance","public","Implementation progress log")
ROLE["governance/target_population_and_sampling.md"] = ("governance","public","Target population and sampling strategy")

# Raw feed files
ROLE["raw/zw_src_001_eastern_highlands/raw_field_collection_eastern_highlands.csv"] = ("data","public","Raw field collection log — Eastern Highlands")
ROLE["raw/zw_src_001_eastern_highlands/raw_field_collection_eastern_highlands.xlsx"] = ("data","public","Raw field collection log Excel — Eastern Highlands")
ROLE["raw/zw_src_002_mazowe/raw_field_collection_mazowe.csv"] = ("data","public","Raw field collection log — Mazowe")
ROLE["raw/zw_src_002_mazowe/raw_field_collection_mazowe.xlsx"] = ("data","public","Raw field collection log Excel — Mazowe")
ROLE["raw/zw_src_003_zvishavane/raw_field_collection_zvishavane.csv"] = ("data","public","Raw field collection log — Zvishavane")
ROLE["raw/zw_src_003_zvishavane/raw_field_collection_zvishavane.xlsx"] = ("data","public","Raw field collection log Excel — Zvishavane")
ROLE["raw/zw_src_004_heritage_knowledge/raw_heritage_transcripts_feed.csv"] = ("data","confidential","Raw heritage transcripts feed")
ROLE["raw/zw_src_004_heritage_knowledge/raw_heritage_transcripts_feed.xlsx"] = ("data","confidential","Raw heritage transcripts feed Excel")
ROLE["raw/zw_src_005_national_herbarium/raw_herbarium_accessions_catalog.csv"] = ("data","public","Raw herbarium accessions catalog")
ROLE["raw/zw_src_005_national_herbarium/raw_herbarium_accessions_catalog.xlsx"] = ("data","public","Raw herbarium accessions catalog Excel")
ROLE["raw/zw_src_006_sirdc_lcms/raw_lcms_spectral_features.csv"] = ("data","internal","Raw LC-MS spectral features matrix")
ROLE["raw/zw_src_006_sirdc_lcms/raw_lcms_spectral_features.xlsx"] = ("data","internal","Raw LC-MS spectral features matrix Excel")
ROLE["raw/zw_src_007_opportunistic/raw_opportunistic_field_log.csv"] = ("data","public","Raw opportunistic field log")
ROLE["raw/zw_src_007_opportunistic/raw_opportunistic_field_log.xlsx"] = ("data","public","Raw opportunistic field log Excel")

# Scratch scripts
ROLE["scratch/export_excel.py"] = ("code","internal","Utility to export CSV files to Excel workbooks")
ROLE["scratch/generate_expanded_dataset.py"] = ("code","internal","Utility generator script")


def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(buf), b""):
            h.update(chunk)
    return h.hexdigest()

def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".git", ".ipynb_checkpoints"}]
        for fn in sorted(filenames):
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
            if rel != "manifest.csv":
                yield rel

def build():
    rows = []
    for rel in sorted(walk()):
        full = os.path.join(ROOT, rel)
        role, tier, desc = ROLE.get(rel, ("unclassified", "public", ""))
        rows.append({"relative_path": rel, "sha256": sha256(full),
                     "size_bytes": os.path.getsize(full), "version": VERSION,
                     "role": role, "sensitivity_level": tier, "description": desc})
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    total = sum(r["size_bytes"] for r in rows)
    print(f"manifest.csv written: {len(rows)} files, {total:,} bytes")
    unc = [r["relative_path"] for r in rows if r["role"] == "unclassified"]
    if unc:
        print("  unclassified (add to ROLE in this script):")
        for u in unc: print("   ", u)
    return 0

def verify():
    if not os.path.exists(MANIFEST):
        print("no manifest.csv found"); return 1
    listed, bad, missing, extra = set(), 0, 0, 0
    for row in csv.DictReader(open(MANIFEST, encoding="utf-8")):
        listed.add(row["relative_path"])
        full = os.path.join(ROOT, row["relative_path"])
        if not os.path.exists(full):
            print(f"  MISSING  {row['relative_path']}"); missing += 1; continue
        if sha256(full) != row["sha256"]:
            print(f"  ALTERED  {row['relative_path']}"); bad += 1
    for rel in walk():
        if rel not in listed:
            print(f"  UNLISTED {rel}"); extra += 1
    n = bad + missing + extra
    print(f"verify: {'OK — package intact, every checksum matches' if not n else f'{n} discrepancies'}")
    return 1 if n else 0

if __name__ == "__main__":
    sys.exit(verify() if "--verify" in sys.argv else build())
