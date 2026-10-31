"""FastAPI backend + plain JavaScript UI (static/):  uvicorn api:app --port 8000

The index and models load once at start-up and stay in memory, so only the question's own work runs per request.
Answers stream as NDJSON lines: {"type": "meta", ...sources and facts}, then {"type": "token", "text": ...}, then "done".
"""
import json
import secrets
import threading
from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path

import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from medrag.config import get_settings
from medrag.data import catalog as C
from medrag.index.store import Index
from medrag.providers.llms import get_llm
from medrag.rag.answer import RAG
from medrag.retrieval.retriever import MODES, Retriever
from medrag.security import audit
from medrag.security.access import LOCAL_ADMIN, User, auth_enabled, authenticate

STATIC = Path(__file__).parent / "static"
s = get_settings()
_sessions: dict[str, User] = {}  # sign-in token -> user, in memory: a restart signs everyone out
_search_lock = threading.Lock()  # the retriever's caches and the reranker are shared by every request


def _indexes() -> list[Path]:
    return sorted(p for p in s.index_dir.glob("*") if (p / "manifest.json").exists()) if s.index_dir.exists() else []


def _manifest(path: Path) -> dict:
    return json.loads((path / "manifest.json").read_text())


@lru_cache(maxsize=2)
def _retriever(path: str, built_at: str) -> Retriever:  # built_at in the key: a rebuilt index is loaded again
    return Retriever(Index(Path(path)))


def retriever(name: str | None = None) -> Retriever:
    found = _indexes()
    if not found:
        raise HTTPException(503, "No index found. Build one first: python -m medrag pipeline")
    default = next((p for p in found if p == s.index_path()), found[0])
    path = next((p for p in found if p.name == name), None) if name else default
    if path is None:
        raise HTTPException(404, f"Unknown index {name!r}")
    return _retriever(str(path), _manifest(path)["built_at"])


def current_user(authorization: str | None = Header(None)) -> User:
    if not auth_enabled():
        return LOCAL_ADMIN
    token = (authorization or "").removeprefix("Bearer ").strip()
    if token not in _sessions:
        raise HTTPException(401, "Sign in first")
    return _sessions[token]


def _records(df: pd.DataFrame) -> list[dict]:
    """DataFrame -> JSON-safe rows (dates as ISO text, NaN as null)."""
    return json.loads(df.to_json(orient="records", date_format="iso"))


@asynccontextmanager
async def lifespan(_app):
    if _indexes():
        retriever()  # load the default index before the first question, not during it
    yield


app = FastAPI(title="MedRAG", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC / "index.html")


# ---------------- session and settings ----------------
class Login(BaseModel):
    username: str
    password: str


@app.post("/api/login")
def login(body: Login):
    u = authenticate(body.username, body.password)
    if u is None:
        audit.append("audit", {"user": body.username, "event": "failed sign-in"})
        raise HTTPException(401, "Wrong user name or password.")
    token = secrets.token_urlsafe(32)
    _sessions[token] = u
    audit.append("audit", {"user": u.username, "role": u.role, "event": "sign-in"})
    return {"token": token, "username": u.username, "role": u.role}


@app.post("/api/logout")
def logout(authorization: str | None = Header(None)):
    _sessions.pop((authorization or "").removeprefix("Bearer ").strip(), None)
    return {"ok": True}


@app.get("/api/info")
def info(user: User = Depends(current_user)):
    found = _indexes()
    return {
        "user": {"username": user.username, "role": user.role, "sees_records": user.sees_records},
        "auth": auth_enabled(),
        "indexes": [{"name": p.name, **{k: _manifest(p).get(k) for k in ("chunks", "dim", "built_at")}} for p in found],
        "default_index": next((p.name for p in found if p == s.index_path()), found[0].name if found else None),
        "llm": f"{s.llm_provider}:{s.llm_model}",
        "modes": list(MODES),
        "top_k": s.top_k,
    }


# ---------------- chat ----------------
class Ask(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    llm: str | None = None
    mode: str = "hybrid+rerank"
    top_k: int | None = Field(None, ge=1, le=20)
    index: str | None = None


@app.post("/api/ask")
def ask(body: Ask, user: User = Depends(current_user)):
    if body.mode not in MODES:
        raise HTTPException(400, f"mode must be one of {list(MODES)}")
    ret = retriever(body.index)
    try:
        rag = RAG(ret, get_llm(body.llm or f"{s.llm_provider}:{s.llm_model}"))
        with _search_lock:
            r, facts, stream = rag.stream(body.question, body.mode, user=user, k=body.top_k)
    except (ValueError, PermissionError) as e:
        raise HTTPException(400, str(e))

    cols = ["doc_id", "via", "score", "patient_name", "mrn", "study_date", "modality", "body_part", "priority", "text"]
    meta = {"type": "meta", "filters": r.filters.describe(), "notes": r.notes, "facts": facts,
            "sources": _records(r.hits[[c for c in cols if c in r.hits.columns]])}

    def lines():
        yield json.dumps(meta) + "\n"
        try:
            for piece in stream:
                yield json.dumps({"type": "token", "text": piece}) + "\n"
        except Exception as e:  # the LLM failed mid-answer: say so instead of cutting the stream silently
            yield json.dumps({"type": "error", "text": str(e)[:300]}) + "\n"
        yield json.dumps({"type": "done"}) + "\n"

    return StreamingResponse(lines(), media_type="application/x-ndjson")


# ---------------- patients ----------------
def _visible(user: User, index: str | None) -> pd.DataFrame:
    if not user.sees_records:
        raise HTTPException(403, f"Your role ({user.role}) does not give access to individual patient records.")
    meta = retriever(index).meta
    allowed = user.allowed_mask(meta)
    return meta if allowed is None else meta[allowed]


@app.get("/api/patients")
def patients(q: str, index: str | None = None, user: User = Depends(current_user)):
    meta = _visible(user, index)
    people = meta[meta["doc_type"] == "patient"].drop_duplicates("patient_id")
    ql = q.strip().lower()
    found = people[people["patient_name"].str.lower().str.contains(ql, regex=False) | (people["mrn"].str.lower() == ql)
                   | (people["patient_id"].astype(str) == ql)]
    return {"total": len(found), "patients": _records(found.head(20)[["patient_id", "patient_name", "mrn"]])}


@app.get("/api/patients/{patient_id}")
def patient(patient_id: int, index: str | None = None, user: User = Depends(current_user)):
    meta = _visible(user, index)
    mine = meta[meta["patient_id"] == patient_id]
    profile = mine[mine["doc_id"] == f"patient:{patient_id}"].sort_values("part")
    if profile.empty:
        raise HTTPException(404, "No such patient, or not one you may see")
    studies = mine[(mine["doc_type"] == "study") & (mine["part"] == 0)].sort_values("study_date", ascending=False)
    studies = studies.assign(modality=studies["modality"].map(C.MODALITY_NAMES))
    docs = mine[mine["doc_type"] == "document"].sort_values(["study_date", "part"])
    documents = [{"doc_id": doc_id, "date": f"{g.iloc[0].study_date:%Y-%m-%d}", "title": g.iloc[0].title,
                  "specialty": g.iloc[0].specialty, "source": g.iloc[0].source, "text": "\n\n".join(g["text"])}
                 for doc_id, g in docs.groupby("doc_id", sort=False)]
    first = profile.iloc[0]
    return {"patient_id": patient_id, "name": first.patient_name, "mrn": first.mrn, "profile": "\n".join(profile["text"]),
            "studies": _records(studies[["study_id", "study_date", "modality", "body_part", "priority", "impression",
                                         "ai_label", "ai_confidence"]]),
            "documents": documents}


# ---------------- data quality, evaluation, audit ----------------
@app.get("/api/quality")
def quality(index: str | None = None, _user: User = Depends(current_user)):
    meta = retriever(index).meta
    files = {n: (s.reports_dir / n).read_text(encoding="utf-8")
             for n in ("cleaning_log.md", "quality_raw.md", "quality_clean.md") if (s.reports_dir / n).exists()}
    return {"patients": int(meta["patient_id"].nunique()),
            "studies": int(meta.loc[meta["doc_type"] == "study", "study_id"].nunique()),
            "chunks": len(meta), "reports": files}


@app.get("/api/evals")
def evals(_user: User = Depends(current_user)):
    runs = sorted(s.reports_dir.glob("eval_*/summary.md"), reverse=True) if s.reports_dir.exists() else []
    return [p.parent.name for p in runs]


@app.get("/api/evals/{run}")
def eval_run(run: str, _user: User = Depends(current_user)):
    folder = s.reports_dir / run
    if not run.startswith("eval_") or folder.parent != s.reports_dir or not (folder / "summary.md").exists():
        raise HTTPException(404, "No such evaluation run")
    gen = folder / "generation.csv"
    return {"summary": (folder / "summary.md").read_text(encoding="utf-8"),
            "answers": _records(pd.read_csv(gen)) if gen.exists() else []}


@app.get("/api/audit")
def audit_log(user: User = Depends(current_user)):
    if user.role not in ("admin", "auditor"):
        raise HTTPException(403, "Only admins and auditors can read the audit log.")
    log = audit.read("audit")
    return {"total": len(log), "events": _records(log.sort_values("ts", ascending=False).head(500)) if len(log) else [],
            "metrics": audit.metrics_summary()}
