"""New records while the app is in use: add them to the raw stage, and `sync` makes them searchable.

    add_records()  -> raw tables (POST /api/ingest)
    python -m medrag watch -> on a change: clean -> sync_documents -> incremental index -> the app swaps it in

Raw tables are rewritten whole, so a watcher can catch the middle of an addition (a patient without its
study yet); the next cycle completes it. Ingested documents keep the patient they arrive with.
"""
from datetime import datetime

import pandas as pd

from medrag.data import store
from medrag.documents import prepare

INGESTED_ID_BASE = 1_000_000  # ingested document ids, apart from the bulk Open-i / MTSamples ids (1..n)


def _read(name: str) -> pd.DataFrame:
    try:
        return store.read_table("raw", name)
    except FileNotFoundError:
        return pd.DataFrame(columns=list(store.COLUMNS[name]))


def _next_id(df: pd.DataFrame, col: str, floor: int = 0) -> int:
    top = pd.to_numeric(df[col], errors="coerce").max() if len(df) else None
    return max(int(top) if pd.notna(top) else 0, floor) + 1


def _append(name: str, df: pd.DataFrame, rows: list[dict]) -> None:
    if rows:
        store.write_table("raw", name, pd.concat([df, pd.DataFrame(rows)], ignore_index=True))


def add_records(patient: dict, studies: list[dict] = (), documents: list[dict] = (), conditions: list[str] = ()) -> dict:
    """Add a patient (or find them by MRN) with new studies + reports, documents and conditions.
    Returns the ids given. Dependent rows are written before the patient, so a half-seen addition is only ever
    a set of orphans that cleaning drops until the next cycle."""
    now = pd.Timestamp(datetime.now())
    patients = _read("patients")
    known = patients[patients["mrn"].astype(str).str.upper() == patient["mrn"].upper()]
    pid = int(pd.to_numeric(known["patient_id"]).min()) if len(known) else _next_id(patients, "patient_id")

    st, rep = _read("studies"), _read("reports")
    sid, rid = _next_id(st, "study_id"), _next_id(rep, "report_id")
    new_studies, new_reports = [], []
    for i, x in enumerate(studies):
        new_studies.append({"study_id": sid + i, "patient_id": pid, "accession": x.get("accession") or f"ACC{sid + i:09d}",
                            "study_date": pd.Timestamp(x["study_date"]), "modality": x["modality"], "body_part": x["body_part"],
                            "indication": x.get("indication"), "priority": x.get("priority") or "routine",
                            "referring_physician": x.get("referring_physician")})
        new_reports.append({"report_id": rid + i, "study_id": sid + i, "radiologist": x.get("radiologist"),
                            "report_text": x["report_text"], "status": x.get("status") or "final", "signed_at": now})

    docs = _read("documents_ingested")
    did = _next_id(docs, "document_id", INGESTED_ID_BASE)
    new_docs = [{"document_id": did + i, "patient_id": pid, "source": "ingest", "source_id": d.get("source_id") or f"ING{did + i}",
                 "title": d["title"], "specialty": d.get("specialty") or "", "doc_date": pd.Timestamp(d["doc_date"]),
                 "text": d["text"], "labels": d.get("labels"), "description": d.get("description")} for i, d in enumerate(documents)]

    _append("reports", rep, new_reports)
    _append("studies", st, new_studies)
    _append("conditions", _read("conditions"), [{"patient_id": pid, "condition": c, "diagnosed_on": pd.NaT} for c in conditions])
    _append("documents_ingested", docs, new_docs)
    if not len(known):
        _append("patients", patients, [{"patient_id": pid, "mrn": patient["mrn"], "full_name": patient["full_name"],
                                        "gender": patient.get("gender"), "date_of_birth": pd.to_datetime(patient.get("date_of_birth")),
                                        "blood_group": patient.get("blood_group"), "city": patient.get("city")}])
    return {"patient_id": pid, "new_patient": not len(known), "study_ids": [s["study_id"] for s in new_studies],
            "document_ids": [d["document_id"] for d in new_docs]}


def sync_documents() -> list[str]:
    """Add ingested documents to the clean stage (cleaned like the rest, patient kept). Documents already there,
    including every bulk-loaded one, are left exactly as they are."""
    new = _read("documents_ingested")
    if new.empty:
        return []
    try:
        clean_docs = store.read_table("clean", "documents")
    except FileNotFoundError:
        clean_docs = pd.DataFrame(columns=list(store.COLUMNS["documents"]))
    patients = set(store.read_table("clean", "patients")["patient_id"])
    new = new[~new["document_id"].isin(set(clean_docs["document_id"])) & new["patient_id"].isin(patients)]
    if new.empty:
        return []
    cleaned, log = prepare.clean(new)
    store.write_table("clean", "documents", pd.concat([clean_docs, cleaned], ignore_index=True))
    return log + [f"documents: added {len(cleaned):,} ingested documents to the clean stage"]
