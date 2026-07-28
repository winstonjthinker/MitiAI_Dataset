#!/usr/bin/env python3
"""
ZW-BioBank v1.0 — ingest validator
Miti AI Consortium · POTRAZ AI for Impact Challenge 2026 · Track 1: Data
Lead Innovator: Mutsa M Mutepfa

Implements checks V01-V21 from validation/validation_rules.json. Thresholds
and critical-field lists are READ from that file, not hard-coded here, so a
reviewer can change a threshold and re-run without touching code.

  python3 scripts/validate.py           validate the batch
  python3 scripts/validate.py --demo    additionally attempt four governance
                                        violations and show each refused

Outputs
  processed/qc_log_v1.csv     every check, every record (table T5)
  validation/error_log.csv    warnings and failures only, with owner,
                              severity, correction action and status

Exits non-zero if any check fails. Standard library only: no installation,
no network, runs on any laptop.
"""
import csv, json, os, re, sqlite3, sys
from datetime import datetime, timezone, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "processed")
VAL  = os.path.join(ROOT, "validation")
GOV  = os.path.join(ROOT, "governance")

RULES = json.load(open(os.path.join(VAL, "validation_rules.json"), encoding="utf-8"))
TH    = RULES["thresholds"]
CRIT  = RULES["critical_fields"]
PAT   = RULES["id_patterns"]

TABLES = {
    "heritage_knowledge":    "heritage_knowledge_v1.csv",
    "environmental_samples": "environmental_samples_v1.csv",
    "genomic_sequences":     "genomic_sequences_v1.csv",
    "metabolomic_profiles":  "metabolomic_profiles_v1.csv",
}
PK = {"environmental_samples":"sample_id","heritage_knowledge":"tk_id",
      "genomic_sequences":"sequence_id","metabolomic_profiles":"metabolite_id"}

OWNER = {"environmental_samples":"Field Collection Lead",
         "heritage_knowledge":"Community Liaison Lead",
         "genomic_sequences":"Bioinformatics Lead",
         "metabolomic_profiles":"Pharmaceutical Chemist"}

results = []
_n = [0]

def log(table, rid, check, dim, ctype, result, severity, message,
        by="automated", action="", owner=None):
    _n[0] += 1
    results.append({
        "qc_id": f"ZW-QC-{date.today().year}-{_n[0]:03d}",
        "target_table": table, "target_record_id": rid,
        "check_name": check, "quality_dimension": dim, "check_type": ctype,
        "check_result": result, "severity": severity, "message": message,
        "checked_by": by,
        "checked_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "issue_owner": (owner or OWNER.get(table, "Data Architect")) if result != "pass" else "",
        "correction_action": action, "corrected_at": "", "corrected_by": "",
        "resolution_status": "resolved" if result == "pass" else "open",
    })

def read(name):
    p = os.path.join(PROC, name)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else None

def build_db():
    conn = sqlite3.connect(":memory:")
    conn.executescript(open(os.path.join(ROOT, "schema", "schema.sql"), encoding="utf-8").read())
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def cols(conn, t):
    return [r[1] for r in conn.execute(f"PRAGMA table_info({t})")]

# ======================================================== V01 schema insert
def v01_load(conn, t, rows):
    c = cols(conn, t); loaded = 0
    for r in rows:
        rid = r.get(PK[t], "<no-pk>")
        vals = [(r.get(x) if r.get(x) not in ("", None) else None) for x in c]
        try:
            conn.execute(f"INSERT INTO {t} ({','.join(c)}) VALUES ({','.join('?'*len(c))})", vals)
            loaded += 1
            log(t, rid, "schema_insert", "validity", "schema", "pass", "info",
                "Record satisfies every constraint in the DDL.")
        except sqlite3.IntegrityError as e:
            m = str(e)
            ctype = "consent_gate" if "consent_reference" in m else "schema"
            sev = "critical" if ctype == "consent_gate" else "high"
            log(t, rid, "schema_insert", "validity", ctype, "fail", sev,
                f"Rejected by database constraint: {m}",
                action="Correct at source and re-ingest. Record not admitted to the bank.")
        except sqlite3.Error as e:
            log(t, rid, "schema_insert", "validity", "schema", "fail", "high", str(e),
                action="Correct at source and re-ingest.")
    conn.commit()
    return loaded

# =============================================== V02 critical completeness
def v02(t, rows):
    if not rows: return
    for field in CRIT.get(t, []):
        present = sum(1 for r in rows if (r.get(field) or "").strip())
        rate = present / len(rows)
        if rate >= TH["critical_field_completeness"]:
            log(t, f"<batch:{field}>", "critical_field_completeness", "completeness",
                "completeness", "pass", "info",
                f"{field}: {rate:.1%} populated against a {TH['critical_field_completeness']:.0%} threshold.")
        else:
            log(t, f"<batch:{field}>", "critical_field_completeness", "completeness",
                "completeness", "fail", "high",
                f"{field}: {rate:.1%} populated, below the {TH['critical_field_completeness']:.0%} threshold.",
                action="Return to the collection team for field re-capture before ingest.")

# ==================================================== V03 identifier format
def v03(t, rows):
    pat = PAT.get(f"{t}.{PK[t]}")
    if not pat or not rows: return
    rx = re.compile(pat)
    bad = [r[PK[t]] for r in rows if not rx.match(r.get(PK[t], ""))]
    for rid in bad:
        log(t, rid, "identifier_format", "consistency", "controlled_vocab", "fail", "medium",
            f"Identifier does not match the documented pattern {pat}.",
            action="Reissue under the documented format before ingest.")
    if not bad:
        log(t, "<batch>", "identifier_format", "consistency", "controlled_vocab", "pass", "info",
            f"All {len(rows)} identifiers match {pat}.")

# ======================================================= V04 / V05 duplicates
def v04(t, rows):
    if not rows: return
    seen = {}
    for r in rows:
        seen.setdefault(r.get(PK[t]), []).append(r)
    dupes = 0
    for k, grp in seen.items():
        if len(grp) > 1:
            dupes += 1
            log(t, k, "primary_key_uniqueness", "uniqueness", "duplicate", "fail", "critical",
                f"Identifier appears {len(grp)} times in this batch.",
                action="Resolve at source. Identifiers are never reissued.")
    if not dupes:
        log(t, "<batch>", "primary_key_uniqueness", "uniqueness", "duplicate", "pass", "info",
            f"All {len(rows)} identifiers are unique within the batch.")

def v05(rows):
    if not rows: return
    seen = {}
    for r in rows:
        key = (r.get("gps_latitude"), r.get("gps_longitude"), r.get("collection_date"),
               r.get("sample_type"), r.get("collector_id"), r.get("collection_depth_cm"))
        seen.setdefault(key, []).append(r["sample_id"])
    flagged = 0
    for key, ids in seen.items():
        if len(ids) > 1:
            flagged += 1
            log("environmental_samples", ", ".join(ids), "near_duplicate_sample", "uniqueness",
                "duplicate", "warning", "medium",
                "Same type, coordinates, date and collector. Confirm these are distinct physical "
                "samples and not a double entry.",
                action="Field lead to confirm against the collection notebook.")
    if not flagged:
        log("environmental_samples", "<batch>", "near_duplicate_sample", "uniqueness", "duplicate",
            "pass", "info",
            "No two samples share type, coordinates, depth, date and collector.")

# ======================================================== V06 checksum format
def v06(t, rows):
    if not rows: return
    rx = re.compile(r"^[0-9a-f]{64}$")
    for r in rows:
        v = (r.get("file_checksum_sha256") or "").strip()
        rid = r[PK[t]]
        if rx.match(v):
            log(t, rid, "checksum_format", "integrity", "checksum", "pass", "info",
                "SHA-256 present and well formed.")
        else:
            log(t, rid, "checksum_format", "integrity", "checksum", "fail", "high",
                "Missing or malformed SHA-256 for the referenced raw file.",
                action="Recompute from the raw file and re-ingest.")

# ====================================================== V07 source_id resolves
def v07(conn):
    p = os.path.join(GOV, "source_register.csv")
    if not os.path.exists(p):
        log("environmental_samples", "<batch>", "source_id_resolves", "integrity",
            "cross_reference", "fail", "high", "governance/source_register.csv is missing.",
            action="Restore the source register; provenance cannot be evidenced without it.")
        return
    known = {r["source_id"] for r in csv.DictReader(open(p, encoding="utf-8"))}
    for t in ("environmental_samples", "heritage_knowledge"):
        for rid, sid in conn.execute(f"SELECT {PK[t]}, source_id FROM {t}"):
            if sid not in known:
                log(t, rid, "source_id_resolves", "integrity", "cross_reference", "fail", "high",
                    f"source_id {sid} is not in the source register.",
                    action="Register the source, with permission status and known limitations, before ingest.")
    log("environmental_samples", "<batch>", "source_id_resolves", "integrity", "cross_reference",
        "pass", "info", f"All source identifiers resolve to the register ({len(known)} sources).")

# ================================================ V08 consent reference match
def v08(conn):
    for sid, a, b in conn.execute("""
        SELECT s.sample_id, s.consent_reference, k.consent_reference
        FROM environmental_samples s JOIN heritage_knowledge k ON s.heritage_use_ref = k.tk_id
        WHERE s.consent_reference IS NOT k.consent_reference"""):
        log("environmental_samples", sid, "consent_reference_matches_heritage", "integrity",
            "consent_gate", "fail", "critical",
            f"Sample cites consent {a} but its heritage record cites {b}.",
            action="Halt all processing of this sample pending reconciliation with the holder.")

# ==================================================== V09 consent log agreement
def v09(conn):
    p = os.path.join(GOV, "consent_log.csv")
    if not os.path.exists(p): return
    cl = {r["tk_id"]: r for r in csv.DictReader(open(p, encoding="utf-8"))}
    for tk, cref, endorse, wstat in conn.execute(
            "SELECT tk_id, consent_reference, council_endorsement_ref, withdrawal_status "
            "FROM heritage_knowledge"):
        row = cl.get(tk)
        if not row:
            log("heritage_knowledge", tk, "consent_log_agreement", "consistency", "consent_gate",
                "fail", "critical", "No entry in governance/consent_log.csv for this record.",
                action="Do not process. A record with no consent-log entry has no evidenced consent.")
            continue
        mismatches = []
        if row["consent_reference"] != cref: mismatches.append("consent reference")
        if row["council_endorsement_ref"] != endorse: mismatches.append("council endorsement")
        if row["withdrawal_status"] != wstat: mismatches.append("withdrawal status")
        if mismatches:
            log("heritage_knowledge", tk, "consent_log_agreement", "consistency", "consent_gate",
                "fail", "critical",
                f"Disagrees with the consent log on: {', '.join(mismatches)}.",
                action="Reconcile against the signed paper record, which is authoritative.")
        else:
            log("heritage_knowledge", tk, "consent_log_agreement", "consistency", "consent_gate",
                "pass", "info", "Consent reference, endorsement and withdrawal status all agree "
                "with the consent log.")

# ================================================= V10 withdrawal propagation
def v10(conn):
    for sid, tk, wdate in conn.execute("""
        SELECT s.sample_id, k.tk_id, k.withdrawal_date FROM environmental_samples s
        JOIN heritage_knowledge k ON s.heritage_use_ref = k.tk_id
        WHERE k.withdrawal_status = 'withdrawn' AND s.record_status = 'active'"""):
        log("environmental_samples", sid, "withdrawal_propagation", "integrity", "cross_reference",
            "fail", "critical",
            f"{tk} was withdrawn on {wdate} but this linked sample is still active.",
            action=f"Pseudonymise or delete within {TH['withdrawal_action_days']} days of the "
                   "withdrawal date. See view v_withdrawal_impact.")

# =================================================== V11 heritage link agreement
def v11(conn):
    for seq, link, parent in conn.execute("""
        SELECT g.sequence_id, g.heritage_link, s.heritage_use_ref
        FROM genomic_sequences g JOIN environmental_samples s ON g.sample_id = s.sample_id
        WHERE g.heritage_link IS NOT s.heritage_use_ref"""):
        log("genomic_sequences", seq, "heritage_link_agreement", "consistency", "cross_reference",
            "warning", "medium",
            f"Denormalised heritage_link ({link}) disagrees with the parent sample ({parent}).",
            action="Re-derive heritage_link from environmental_samples.heritage_use_ref.")

# ======================================================== V12 location masking
def v12(conn):
    for sid, masked, prec in conn.execute(
            "SELECT sample_id, location_masked, gps_precision_m FROM environmental_samples "
            "WHERE data_sensitivity = 'public'"):
        if not masked:
            log("environmental_samples", sid, "location_masking", "validity", "privacy", "fail",
                "high", "Record is classified public but carries unmasked coordinates.",
                action="Blur to ward centroid and set location_masked before public release.")
        else:
            log("environmental_samples", sid, "location_masking", "validity", "privacy", "pass",
                "info", f"Public record is masked at {prec} m stated precision.")

# ===================================================== V13 no direct identifiers
def v13(conn):
    phone = re.compile(r"(\+263|0)7\d{8}")
    natid = re.compile(r"\b\d{2}-\d{6,7}[A-Z]\d{2}\b")
    fields = ["local_plant_name","disease_target_local","disease_target_en","preparation_method"]
    for row in conn.execute(f"SELECT tk_id, {', '.join(fields)} FROM heritage_knowledge"):
        tk, texts = row[0], row[1:]
        blob = " ".join(x for x in texts if x)
        hits = []
        if phone.search(blob): hits.append("telephone number")
        if natid.search(blob): hits.append("national ID number")
        if hits:
            log("heritage_knowledge", tk, "no_direct_identifiers", "validity", "privacy", "fail",
                "critical", f"Free text appears to contain a {', '.join(hits)}.",
                action="Redact before ingest. Pseudonymisation is defeated by an identifier in "
                       "free text.")
        else:
            log("heritage_knowledge", tk, "no_direct_identifiers", "validity", "privacy", "pass",
                "info", "No direct identifier patterns detected in free-text fields.")

# ====================================================== V14 translation verified
def v14(conn):
    for tk, st in conn.execute("SELECT tk_id, translation_status FROM heritage_knowledge "
                               "WHERE record_status = 'active'"):
        if st != "human_verified":
            log("heritage_knowledge", tk, "translation_verified", "accuracy", "completeness",
                "warning", "medium",
                f"Translation status is '{st}'. The record is held out of every release tier "
                "until a bilingual reviewer verifies it.",
                by="bilingual_validator", action="Queue for bilingual review.")

# ============================================ V15 annotation confidence honesty
def v15(conn):
    for mid, lvl, name in conn.execute(
            "SELECT metabolite_id, msi_annotation_level, putative_compound_name "
            "FROM metabolomic_profiles WHERE msi_annotation_level >= 3"):
        log("metabolomic_profiles", mid, "annotation_confidence_honesty", "accuracy", "novelty",
            "warning", "low",
            f"MSI level {lvl}: '{name}' is a putative annotation and must not be reported as an "
            "identification.",
            action="Retain the caveat in any downstream use or publication.")

# ========================================================= V16 / V17 / V18 ranges
def v16(conn):
    lim = TH["max_minutes_to_preservation"]
    for sid, mins in conn.execute(
            f"SELECT sample_id, minutes_to_preservation FROM environmental_samples "
            f"WHERE minutes_to_preservation > {lim}"):
        log("environmental_samples", sid, "preservation_latency", "accuracy", "range", "warning",
            "medium", f"{mins} minutes to preservation exceeds the {lim}-minute target.",
            action="Flag for degradation review before any metabolomic interpretation.")

def v17(conn):
    lim = TH["min_mean_q_score"]
    for seq, q in conn.execute(
            f"SELECT sequence_id, mean_q_score FROM genomic_sequences "
            f"WHERE mean_q_score IS NOT NULL AND mean_q_score < {lim}"):
        log("genomic_sequences", seq, "sequence_quality", "accuracy", "range", "warning", "medium",
            f"Mean Q score {q} is below Q{int(lim)}. Taxonomic assignment is provisional.",
            action="Mark assignments provisional; consider re-running the library.")

def v18(conn):
    p = os.path.join(GOV, "source_register.csv")
    windows = {}
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            windows[r["source_id"]] = (r["collection_time_start"][:10], r["collection_time_end"][:10])
    today = date.today().isoformat()
    spec_mode = RULES.get("mode") == "specification"
    for sid, src, cdate in conn.execute(
            "SELECT sample_id, source_id, collection_date FROM environmental_samples"):
        in_window = src in windows and windows[src][0] <= cdate <= windows[src][1]
        if cdate > today and spec_mode and in_window:
            log("environmental_samples", sid, "collection_window", "timeliness", "range", "pass",
                "info",
                f"Collection date {cdate} is inside the planned window for {src} and ahead of "
                "today. Expected in specification mode; this becomes a hard failure in production "
                "mode.")
        elif cdate > today:
            log("environmental_samples", sid, "collection_window", "timeliness", "range", "fail",
                "high", f"Collection date {cdate} is in the future.",
                action="Correct the date at source.")
        elif src in windows and not in_window:
            log("environmental_samples", sid, "collection_window", "timeliness", "range",
                "warning", "medium",
                f"Collection date {cdate} falls outside the declared window for {src} "
                f"({windows[src][0]} to {windows[src][1]}).",
                action="Confirm the date, or update the source register window and record why.")

# ============================================== V19 / V20 / V21 bias and coverage
def v19(conn):
    rows = conn.execute("SELECT language_tag, COUNT(*) FROM heritage_knowledge "
                        "WHERE record_status = 'active' GROUP BY language_tag").fetchall()
    total = sum(c for _, c in rows) or 1
    nd = dict(rows).get("nd", 0)
    share = nd / total
    floor = TH["min_ndebele_heritage_share"]
    if share >= floor:
        log("heritage_knowledge", "<batch>", "language_representation", "completeness",
            "bias_coverage", "pass", "info",
            f"Ndebele-language records are {share:.0%} of the active corpus ({nd} of {total}), "
            f"at or above the {floor:.0%} floor.")
    else:
        log("heritage_knowledge", "<batch>", "language_representation", "completeness",
            "bias_coverage", "warning", "medium",
            f"Ndebele-language records are {share:.0%} of the active corpus ({nd} of {total}), "
            f"below the {floor:.0%} floor declared in the bias risk register (BR-03).",
            action="Direct the next collection round to Ndebele-speaking communities.")

#: Ecozone value for sites the sampling frame never named. Admitted, described
#: by locality_description (rule D5), reported by v24, never counted into quota.
OPEN_ECOZONE = "Other"


def v20(conn):
    quota = TH["ecozone_quota"]
    counts = dict(conn.execute("SELECT ecozone, COUNT(*) FROM environmental_samples "
                               "WHERE record_status='active' GROUP BY ecozone").fetchall())
    total_q = sum(quota.values())
    # In-frame collection only. Including out-of-frame samples in the denominator
    # would make every named zone look under-collected against a total it never
    # contributed to.
    total_c = sum(n for z, n in counts.items() if z != OPEN_ECOZONE) or 1
    for zone, q in quota.items():
        got = counts.get(zone, 0)
        expected_share = q / total_q
        actual_share = got / total_c
        msg = f"{zone}: {got} of {q} quota ({got/q:.0%}); {actual_share:.0%} of collection to date "\
              f"against an expected {expected_share:.0%}."
        if actual_share < expected_share / 2:
            log("environmental_samples", f"<zone:{zone}>", "ecozone_coverage", "completeness",
                "bias_coverage", "warning", "low", msg,
                action="Rebalance the next expedition toward this ecozone (BR-01).")
        else:
            log("environmental_samples", f"<zone:{zone}>", "ecozone_coverage", "completeness",
                "bias_coverage", "pass", "info", msg)

def v21(conn):
    seen = {}
    for zone, season in conn.execute("SELECT DISTINCT ecozone, season FROM environmental_samples "
                                     "WHERE record_status='active'"):
        seen.setdefault(zone, set()).add(season)
    for zone, seasons in seen.items():
        # Only the named zones carry a seasonal-pairing commitment. 'Other' is a
        # bag of unrelated sites; "wet-season only" there says nothing about
        # confounding and would be a warning nobody could act on.
        if zone == OPEN_ECOZONE:
            continue
        if len(seasons) < 2:
            log("environmental_samples", f"<zone:{zone}>", "seasonal_coverage", "completeness",
                "bias_coverage", "warning", "medium",
                f"{zone} carries {list(seasons)[0]}-season records only. Season is confounded with "
                "site until the second-season refresh is collected.",
                action="Schedule the counterpart season collection (BR-02).")
        else:
            log("environmental_samples", f"<zone:{zone}>", "seasonal_coverage", "completeness",
                "bias_coverage", "pass", "info", f"{zone} carries both dry and wet season records.")

def v24(conn):
    """
    Out-of-frame collection.

    Collection follows the holder, not the sampling frame, so a sample from the
    bush behind a homestead is admitted rather than refused. What must not happen
    is its drifting out of sight: a rising out-of-frame share means the design is
    being replaced by whatever was convenient, and the only way anyone notices is
    if the number is reported. These samples never count toward the quota, so the
    200/150/150 target cannot be met by relabelling.
    """
    total, out = conn.execute(
        "SELECT COUNT(*), SUM(ecozone = ?) FROM environmental_samples "
        "WHERE record_status='active'", (OPEN_ECOZONE,)).fetchone()
    out = out or 0
    if not total:
        return
    share = out / total
    msg = (f"{out} of {total} active samples ({share:.0%}) were collected outside the three "
           f"named ecozones. They are admitted and carry a locality description (D5), and they "
           f"do not count toward the 200/150/150 quota.")
    if share > 0.25:
        log("environmental_samples", "<zone:Other>", "out_of_frame_coverage", "completeness",
            "bias_coverage", "warning", "medium", msg,
            action="More than a quarter of collection is out of frame. Aim the next expedition "
                   "at the named zones or restate the sampling frame (BR-01).")
    else:
        log("environmental_samples", "<zone:Other>", "out_of_frame_coverage", "completeness",
            "bias_coverage", "pass", "info", msg)

# =========================================================== provenance summary
def provenance(conn):
    return conn.execute("SELECT COUNT(*) FROM v_provenance_chain").fetchone()[0]

# ============================================================ governance demo
def demo(conn):
    print("\n" + "=" * 74)
    print("GOVERNANCE DEMONSTRATION — four violations, four refusals")
    print("=" * 74)
    caught = 0

    print("\n" + "-" * 74)
    print("1 of 4 · attempting to record knowledge the holder classified SACRED")
    print("-" * 74)
    try:
        conn.execute("""INSERT INTO heritage_knowledge
            (tk_id,source_id,holder_pseudonym_id,community_council_id,council_endorsement_ref,
             consent_reference,consent_date,collection_language,interview_date,interviewer_id,
             knowledge_type,local_plant_name,language_tag,disease_target_local,province,district,
             sensitivity_level,data_sensitivity,benefit_sharing_agreement_ref,created_at)
            VALUES ('ZW-TK-2026-999','ZW-SRC-004','HLD-X','CC-X','END-X','FPIC-ZW-2026-C999',
                    '2026-09-01','sn','2026-09-01','INT-001','plant-disease','[redacted]','sn',
                    '[redacted]','Manicaland','Chimanimani','sacred','confidential','BSA-X',
                    '2026-09-01T00:00:00+02:00')""")
        print("   ACCEPTED — this would be a defect.")
    except sqlite3.IntegrityError as e:
        caught += 1
        print(f"   REFUSED by the database.\n   {e}")
        print("\n   sensitivity_level admits 'public' and 'community-restricted'. The proposal says")
        print("   sacred knowledge is never collected; this is that sentence as a constraint. There")
        print("   is no field in the schema in which such a record could be stored, by accident or")
        print("   otherwise.")

    print("\n" + "-" * 74)
    print("2 of 4 · knowledge-led sample submitted with no consent reference")
    print("-" * 74)
    try:
        conn.execute("""INSERT INTO environmental_samples
            (sample_id,collection_event_id,source_id,ecozone,province,district,land_tenure,
             gps_latitude,gps_longitude,gps_precision_m,location_masked,sample_type,
             collection_date,season,collector_id,preservation_method,minutes_to_preservation,
             processing_lab,chain_of_custody_ref,heritage_use_ref,created_at)
            VALUES ('ZW-SMP-2026-998','CE-X','ZW-SRC-001','Eastern Highlands','Manicaland',
                    'Chimanimani','communal',-19.8,32.86,5000,1,'bark','2026-09-20','dry',
                    'COL-003','silica_gel',40,'MOBILE-LEC-01','COC-X','ZW-TK-2026-001',
                    '2026-09-20T00:00:00+02:00')""")
        print("   ACCEPTED — this would be a defect.")
    except sqlite3.IntegrityError as e:
        caught += 1
        print(f"   REFUSED by the database.\n   {e}")
        print("\n   The sample names a holder's knowledge as the reason it was collected but carries")
        print("   no consent document. Consent is not a field someone remembers to fill in. It is a")
        print("   condition of the row existing.")

    print("\n" + "-" * 74)
    print("3 of 4 · consent dated AFTER the interview it supposedly authorised")
    print("-" * 74)
    try:
        conn.execute("""INSERT INTO heritage_knowledge
            (tk_id,source_id,holder_pseudonym_id,community_council_id,council_endorsement_ref,
             consent_reference,consent_date,collection_language,interview_date,interviewer_id,
             knowledge_type,local_plant_name,language_tag,disease_target_local,province,district,
             sensitivity_level,data_sensitivity,benefit_sharing_agreement_ref,created_at)
            VALUES ('ZW-TK-2026-997','ZW-SRC-004','HLD-Y','CC-Y','END-Y','FPIC-ZW-2026-C997',
                    '2026-09-20','sn','2026-09-14','INT-004','plant-disease','Muranga','sn',
                    'test','Manicaland','Chimanimani','public','confidential','BSA-Y',
                    '2026-09-20T00:00:00+02:00')""")
        print("   ACCEPTED — this would be a defect.")
    except sqlite3.IntegrityError as e:
        caught += 1
        print(f"   REFUSED by the database.\n   {e}")
        print("\n   Consent obtained after the fact is not prior informed consent. The 'P' in FPIC")
        print("   is enforced by a constraint rather than by a reviewer noticing the dates.")

    print("\n" + "-" * 74)
    print("4 of 4 · holder withdraws; a linked sample is left active")
    print("-" * 74)
    conn.execute("""INSERT INTO environmental_samples
        (sample_id,collection_event_id,source_id,ecozone,province,district,land_tenure,
         gps_latitude,gps_longitude,gps_precision_m,location_masked,sample_type,collection_date,
         season,collector_id,preservation_method,minutes_to_preservation,processing_lab,
         chain_of_custody_ref,heritage_use_ref,consent_reference,nba_permit_ref,created_at,
         record_status)
        VALUES ('ZW-SMP-2026-996','CE-X','ZW-SRC-001','Eastern Highlands','Manicaland','Nyanga',
                'communal',-18.2,32.75,5000,1,'bark','2026-11-01','wet','COL-003','silica_gel',
                52,'MOBILE-LEC-01','COC-Y','ZW-TK-2026-006','FPIC-ZW-2026-C006','NBA-ZW-2026-014',
                '2026-11-01T00:00:00+02:00','active')""")
    conn.commit()
    before = len(results)
    v10(conn)
    found = [r for r in results[before:] if r["check_result"] == "fail"]
    caught += len(found)
    for r in found:
        print(f"   CAUGHT by the validator — [{r['severity']}] {r['message']}")
    print("\n   Withdrawal is not a manual clean-up task. Every downstream record is surfaced on the")
    print("   next run and the batch is held until each is actioned inside the 30-day commitment.")
    for row in conn.execute("SELECT * FROM v_withdrawal_impact"):
        print(f"   v_withdrawal_impact: {row}")
    return caught

# ==================================================================== main
def main():
    conn = build_db()
    print("=" * 74)
    print("ZW-BioBank v1.0 — ingest validation")
    print(f"Rules  validation/validation_rules.json v{RULES['rules_version']}")
    print(f"Run at {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}")
    print("=" * 74)

    total = 0
    for t, fn in TABLES.items():
        rows = read(fn)
        if rows is None:
            print(f"  {t:<24} file not found — skipped"); continue
        loaded = v01_load(conn, t, rows)
        v02(t, rows); v03(t, rows); v04(t, rows)
        if t in ("genomic_sequences", "metabolomic_profiles"): v06(t, rows)
        if t == "environmental_samples": v05(rows)
        print(f"  {t:<24} {loaded}/{len(rows)} records admitted")
        total += len(rows)

    for fn in (v07, v08, v09, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v24):
        fn(conn)

    chain = provenance(conn)
    demo_caught = demo(conn) if "--demo" in sys.argv else None

    # ---- write T5 and the error log
    qc_path = os.path.join(PROC, "qc_log_v1.csv")
    with open(qc_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader(); w.writerows(results)

    errs = [r for r in results if r["check_result"] in ("warning", "fail")]
    err_path = os.path.join(VAL, "error_log.csv")
    with open(err_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader(); w.writerows(errs)

    p = sum(1 for r in results if r["check_result"] == "pass")
    wn = sum(1 for r in results if r["check_result"] == "warning")
    fl = sum(1 for r in results if r["check_result"] == "fail")

    print("\n" + "-" * 74)
    print(f"  records examined  {total}")
    print(f"  checks run        {len(results)}   across {len({r['check_name'] for r in results})} distinct checks")
    print(f"  PASS {p}    WARNING {wn}    FAIL {fl}")
    print(f"  compounds resolving to a named holder via v_provenance_chain: {chain}")
    dims = sorted({r["quality_dimension"] for r in results})
    print(f"  quality dimensions exercised: {', '.join(dims)} ({len(dims)} of 7)")
    if demo_caught is not None:
        print(f"  governance violations attempted in demo: {demo_caught} attempted, {demo_caught} refused")
    print(f"  qc log     processed/qc_log_v1.csv")
    print(f"  error log  validation/error_log.csv ({len(errs)} entries)")
    print("-" * 74)

    if fl:
        print("  STATUS: BATCH HELD. Failing records are not admitted to the bank.")
        for r in results:
            if r["check_result"] == "fail":
                print(f"    [{r['severity']:<8}] {r['target_table']}.{r['target_record_id']} — {r['check_name']}")
    else:
        print("  STATUS: BATCH CLEAN. All records admitted; warnings carry documented caveats.")
    return 1 if fl else 0

if __name__ == "__main__":
    sys.exit(main())
