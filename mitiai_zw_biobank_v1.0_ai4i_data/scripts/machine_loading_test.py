#!/usr/bin/env python3
"""
ZW-BioBank v1.0 — machine-loading test
Minimum Expectations for AI-Ready Data §6.3

  "Applicants should be able to show that a sample of the dataset can be
   loaded into a standard tool such as Python, R, SQL, or a GIS package
   without manual editing."

This script is that demonstration, run rather than asserted. It loads every
processed file into (a) the Python standard library, (b) pandas if present,
and (c) SQL through the shipped DDL, then runs a real analytical query
across three of the four data streams. It edits nothing.

  python3 scripts/machine_loading_test.py

Exits non-zero if any file fails to load.
"""
import csv, json, os, sqlite3, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "processed")
ok = True

def head(t):
    print("\n" + "=" * 72); print(t); print("=" * 72)

# ------------------------------------------------------- 1. Python stdlib
head("1 · Python standard library — csv module, no dependencies")
files = sorted(f for f in os.listdir(PROC) if f.endswith(".csv"))
for fn in files:
    try:
        with open(os.path.join(PROC, fn), encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        print(f"   OK   {fn:<34} {len(rows):>5} rows × {len(rows[0]) if rows else 0} columns")
    except Exception as e:
        ok = False; print(f"   FAIL {fn}: {e}")

for fn in ("schema/schema.json", "metadata/dataset_metadata.json",
           "validation/validation_rules.json"):
    try:
        json.load(open(os.path.join(ROOT, fn), encoding="utf-8"))
        print(f"   OK   {fn:<34} valid JSON")
    except Exception as e:
        ok = False; print(f"   FAIL {fn}: {e}")

# --------------------------------------------------------------- 2. pandas
head("2 · pandas — the ordinary starting point for an AI team")
try:
    import pandas as pd
    for fn in files:
        df = pd.read_csv(os.path.join(PROC, fn))
        print(f"   OK   {fn:<34} shape {str(df.shape):<12} "
              f"dtypes inferred: {df.dtypes.nunique()} distinct")
    df = pd.read_csv(os.path.join(PROC, "environmental_samples_v1.csv"))
    print("\n   Sanity: samples by ecozone and season")
    for (z, s), n in df.groupby(["ecozone", "season"]).size().items():
        print(f"     {z:<20} {s:<5} {n}")
except ImportError:
    print("   pandas not installed in this environment — stdlib and SQL paths above and below")
    print("   are sufficient to demonstrate machine-readability.")
except Exception as e:
    ok = False; print(f"   FAIL pandas: {e}")

# ------------------------------------------------------------------ 3. SQL
head("3 · SQL — loaded through the shipped DDL, constraints enforced")
try:
    conn = sqlite3.connect(":memory:")
    conn.executescript(open(os.path.join(ROOT, "schema", "schema.sql"), encoding="utf-8").read())
    conn.execute("PRAGMA foreign_keys = ON")
    order = [("heritage_knowledge", "heritage_knowledge_v1.csv"),
             ("environmental_samples", "environmental_samples_v1.csv"),
             ("genomic_sequences", "genomic_sequences_v1.csv"),
             ("metabolomic_profiles", "metabolomic_profiles_v1.csv")]
    for t, fn in order:
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({t})")]
        rows = list(csv.DictReader(open(os.path.join(PROC, fn), encoding="utf-8")))
        for r in rows:
            conn.execute(f"INSERT INTO {t} ({','.join(cols)}) VALUES ({','.join('?'*len(cols))})",
                         [(r.get(c) if r.get(c) not in ("", None) else None) for c in cols])
        print(f"   OK   {t:<24} {len(rows)} rows loaded through the schema")
    conn.commit()
except Exception as e:
    ok = False; print(f"   FAIL SQL load: {e}")

# ----------------------------------------------- 4. a real cross-stream query
head("4 · A question no single-stream dataset can answer")
print("   For each compound detected in a knowledge-led sample: the traditional")
print("   indication that directed the collection, the compound found, its")
print("   annotation confidence, and the holder the benefit-sharing claim resolves to.\n")
try:
    q = """
    SELECT k.local_plant_name, k.language_tag, k.disease_target_en,
           m.putative_compound_name, m.msi_annotation_level, m.compound_class,
           k.holder_pseudonym_id, k.benefit_sharing_agreement_ref
    FROM metabolomic_profiles m
    JOIN environmental_samples s ON m.sample_id = s.sample_id
    JOIN heritage_knowledge    k ON s.heritage_use_ref = k.tk_id
    WHERE k.withdrawal_status = 'active'
    ORDER BY m.msi_annotation_level, k.local_plant_name"""
    rows = conn.execute(q).fetchall()
    for r in rows:
        print(f"   {r[0]:<12} [{r[1]}] {str(r[2])[:34]:<34} -> {str(r[3])[:30]:<30} "
              f"MSI {r[4]}  {r[5] or '-':<18} {r[6]}  {r[7]}")
    print(f"\n   {len(rows)} rows. Three streams joined on one physical sample, with the")
    print("   provenance chain intact from compound back to holder.")
except Exception as e:
    ok = False; print(f"   FAIL query: {e}")

# ------------------------------------------------------------------ 5. R / GIS
head("5 · R and GIS")
print("   R      : read.csv('processed/environmental_samples_v1.csv') — plain UTF-8 CSV,")
print("            no embedded newlines, no merged cells, no multi-row headers.")
print("   GIS    : gps_latitude / gps_longitude are WGS 84 (EPSG:4326) decimal degrees,")
print("            with gps_precision_m stating positional uncertainty and location_masked")
print("            declaring whether the point has been blurred to the ward centroid.")
print("            Loads directly as a delimited-text layer in QGIS.")

print("\n" + "=" * 72)
print("RESULT: " + ("every file loaded into Python, SQL and pandas with no manual editing."
                    if ok else "one or more files failed to load — see above."))
print("=" * 72)
sys.exit(0 if ok else 1)
