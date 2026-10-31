"""FastAPI backend (api.py): every endpoint on the small offline dataset, with a fake LLM."""
import gc
import json

import pytest
from fastapi.testclient import TestClient

from medrag.providers.llms import LLM


class FakeLLM(LLM):
    provider = "ollama"

    def __init__(self):
        super().__init__("fake")

    def stream(self, system, user, max_tokens=1500):
        yield "The records show "
        yield "a finding [S1]."


@pytest.fixture(scope="module")
def client(env, built):
    import api

    mp = pytest.MonkeyPatch()
    mp.setattr(api, "s", env)
    mp.setattr(api, "get_llm", lambda spec: FakeLLM())
    with TestClient(api.app) as c:
        yield c
    mp.undo()
    api._retriever.cache_clear()  # release the memory-mapped index: Windows cannot delete an open file in later tests
    gc.collect()


def _events(res):
    return [json.loads(line) for line in res.text.splitlines() if line]


def test_info_and_home_page(client):
    info = client.get("/api/info").json()
    assert info["user"]["role"] == "admin" and not info["auth"] and info["indexes"] and "hybrid+rerank" in info["modes"]
    assert "<title>MedRAG</title>" in client.get("/").text and client.get("/static/app.js").status_code == 200


def test_ask_streams_sources_then_answer(client):
    res = client.post("/api/ask", json={"question": "How many CT studies were done?", "top_k": 4})
    events = _events(res)
    meta, tokens = events[0], [e["text"] for e in events if e["type"] == "token"]
    assert meta["type"] == "meta" and 0 < len(meta["sources"]) <= 6 and "Matching studies" in meta["facts"]
    assert "".join(tokens) == "The records show a finding [S1]." and events[-1]["type"] == "done"
    assert client.post("/api/ask", json={"question": "x", "mode": "nonsense"}).status_code == 400
    assert client.post("/api/ask", json={"question": ""}).status_code == 422


def test_patients_search_and_detail(client, built):
    _, cleaned, *_ = built
    pt = cleaned["patients"].iloc[0]
    found = client.get("/api/patients", params={"q": pt["mrn"]}).json()
    assert found["total"] == 1 and found["patients"][0]["patient_id"] == pt["patient_id"]
    detail = client.get(f"/api/patients/{pt['patient_id']}").json()
    assert detail["mrn"] == pt["mrn"] and "PATIENT PROFILE" in detail["profile"] and isinstance(detail["studies"], list)
    assert client.get("/api/patients/999999").status_code == 404


def test_quality_evals_and_audit(client):
    q = client.get("/api/quality").json()
    assert q["patients"] > 0 and q["studies"] > 0
    assert client.get("/api/evals").json() == [] and client.get("/api/evals/eval_..%2F..%2Fsecret").status_code == 404
    a = client.get("/api/audit").json()
    assert a["total"] >= 1 and "Requests" in a["metrics"]  # the question above was logged


def test_sign_in_is_required_when_users_are_configured(client, tmp_path, monkeypatch):
    from medrag.config import get_settings
    from medrag.security import access

    monkeypatch.setenv("USERS_FILE", str(tmp_path / "users.json"))
    get_settings.cache_clear()
    try:
        access.save_user("res", "a long enough password", "researcher")
        assert client.get("/api/info").status_code == 401
        assert client.post("/api/login", json={"username": "res", "password": "wrong"}).status_code == 401
        token = client.post("/api/login", json={"username": "res", "password": "a long enough password"}).json()["token"]
        h = {"Authorization": f"Bearer {token}"}
        assert client.get("/api/info", headers=h).json()["user"]["role"] == "researcher"
        assert client.get("/api/patients", params={"q": "a"}, headers=h).status_code == 403
        assert client.get("/api/audit", headers=h).status_code == 403
        client.post("/api/logout", headers=h)
        assert client.get("/api/info", headers=h).status_code == 401
    finally:
        monkeypatch.delenv("USERS_FILE")
        get_settings.cache_clear()
