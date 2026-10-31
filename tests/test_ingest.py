"""New records while the app runs: POST /api/ingest -> one `watch` sync -> the app swaps in the new index.
Uses its own small dataset, so it cannot disturb the session dataset of the other tests."""
import argparse
import gc
import json
import time

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from medrag.providers.llms import LLM

REPORT = "TECHNIQUE: Non-contrast CT of the chest.\nFINDINGS: Small right pleural effusion.\nIMPRESSION: Small right pleural effusion.\nRECOMMENDATION: Clinical correlation."
NOTE = "Cardiology consult. The patient reports exertional chest tightness for two weeks. Echo shows preserved function. Plan: stress test."


class FakeLLM(LLM):
    provider = "ollama"

    def __init__(self):
        super().__init__("fake")

    def stream(self, system, user, max_tokens=1500):
        yield "Small right pleural effusion on 2026-01-10."


@pytest.fixture()
def live(tmp_path, monkeypatch):
    from medrag.config import get_settings
    from medrag.data import store
    from medrag.data.generate import generate

    for k, v in {"DATA_BACKEND": "parquet", "DATA_DIR": str(tmp_path / "data"), "INDEX_DIR": str(tmp_path / "idx"),
                 "REPORTS_DIR": str(tmp_path / "reports"), "EMBED_PROVIDER": "hash", "EMBED_MODEL": "bow",
                 "RERANK_MODEL": "none", "USERS_FILE": "", "LLM_PROVIDER": "ollama"}.items():
        monkeypatch.setenv(k, v)
    get_settings.cache_clear()
    store.write_all("raw", generate(n_patients=60, mean_studies=3, dirty_rate=0.0, seed=5))
    import api
    from medrag.__main__ import sync

    args = argparse.Namespace(max_words=220, embed_provider=None, embed_model=None)
    sync(args)  # the first build
    monkeypatch.setattr(api, "s", get_settings())
    monkeypatch.setattr(api, "get_llm", lambda spec: FakeLLM())
    monkeypatch.setattr(api, "RELOAD_EVERY", 0.2)
    api._loaded.clear()
    with TestClient(api.app) as c:
        yield c, args, sync
    api._loaded.clear()
    gc.collect()
    get_settings.cache_clear()


def test_new_patient_is_searchable_after_one_sync(live):
    client, args, sync = live
    body = {"patient": {"mrn": "MRN-NEW-001", "full_name": "Zara Quintero", "gender": "female", "date_of_birth": "1970-05-01"},
            "studies": [{"study_date": "2026-01-10T09:00:00", "modality": "ct scan", "body_part": "chest", "priority": "urgent",
                         "report_text": REPORT}],
            "documents": [{"title": "Cardiology consult", "specialty": "Cardiology", "doc_date": "2026-01-12", "text": NOTE}],
            "conditions": ["Hypertension"]}
    ids = client.post("/api/ingest", json=body).json()
    assert ids["new_patient"] and len(ids["study_ids"]) == 1 and ids["document_ids"][0] > 1_000_000

    before = client.get("/api/info").json()["indexes"][0]["in_use"]
    q = {"question": "tell me about zara quintero"}
    assert json.loads(client.post("/api/ask", json=q).text.splitlines()[0])["overview"] is None  # not indexed yet

    time.sleep(1.1)  # a new built_at (second resolution)
    sync(args)
    for _ in range(100):  # the app loads the new version in the background, then switches
        if client.get("/api/info").json()["indexes"][0]["in_use"] != before:
            break
        time.sleep(0.1)
    meta = json.loads(client.post("/api/ask", json=q).text.splitlines()[0])
    (o,) = meta["overview"]
    assert o["mrn"] == "MRN-NEW-001" and o["conditions"] == "Hypertension"
    assert [(s["date"], s["modality"], s["finding"]) for s in o["studies"]] == [("2026-01-10", "CT", "Small right pleural effusion.")]
    assert [d["title"] for d in o["documents"]] == ["Cardiology consult"]

    # more for the same MRN: the same patient, nothing duplicated
    again = client.post("/api/ingest", json={"patient": body["patient"], "studies": [body["studies"][0] | {"study_date": "2026-02-01T10:00:00"}]}).json()
    assert again["patient_id"] == ids["patient_id"] and not again["new_patient"]


def test_ingested_documents_keep_their_patient_and_never_move_others(live):
    from medrag.data import store
    from medrag.ingest.live import add_records, sync_documents

    client, args, sync = live
    old = pd.DataFrame([{"document_id": 7, "patient_id": 3, "source": "mtsamples", "source_id": "M7", "title": "Old note",
                         "specialty": "Surgery", "doc_date": pd.Timestamp("2022-01-01"), "text": NOTE, "labels": None, "description": None}])
    store.write_table("clean", "documents", old)
    pid = add_records({"mrn": "MRN0000010", "full_name": "x"}, documents=[{"title": "New", "doc_date": "2026-01-01", "text": NOTE}])["patient_id"]
    sync_documents()
    docs = store.read_table("clean", "documents").set_index("document_id")
    assert docs.loc[7, "patient_id"] == 3 and docs.loc[7, "title"] == "Old note"  # untouched
    assert (docs.loc[docs.index > 1_000_000, "patient_id"] == pid).all()  # kept the patient it arrived with
    sync_documents()
    assert len(store.read_table("clean", "documents")) == len(docs)  # running again adds nothing twice


def test_ingest_rejects_what_cleaning_would_drop(live):
    client, *_ = live
    p = {"mrn": "MRN-NEW-002", "full_name": "Test Person"}
    study = {"study_date": "2025-01-01T00:00:00", "modality": "CT", "body_part": "chest", "report_text": REPORT}
    assert client.post("/api/ingest", json={"patient": p, "studies": [study | {"modality": "laser scan"}]}).status_code == 422
    assert client.post("/api/ingest", json={"patient": p, "studies": [study | {"report_text": "Findings: none at all here."}]}).status_code == 422
    assert client.post("/api/ingest", json={"patient": p, "studies": [study | {"study_date": "2099-01-01T00:00:00"}]}).status_code == 422
    short = {"title": "Note", "doc_date": "2025-01-01", "text": "too short"}
    assert client.post("/api/ingest", json={"patient": p, "documents": [short]}).status_code == 422
