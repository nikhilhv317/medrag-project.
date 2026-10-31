"""FastAPI backend + plain JavaScript UI (static/):  uvicorn api:app --port 8000

The index and models load once at start-up and stay in memory, so only the question's own work runs per request.
Answers stream as NDJSON lines: {"type": "meta", ...sources and facts}, then {"type": "token", "text": ...}, then "done".
New records: POST /api/ingest writes them to the raw stage; `python -m medrag watch` indexes them; a background
thread here loads each new index version and switches to it when ready, so no question waits for a reload.
"""
import json
import secrets
import threading
import time
from contextlib import asynccontextmanager
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from medrag.config import get_settings
from medrag.data import catalog as C
from medrag.index.store import Index
from medrag.providers.llms import get_llm
from medrag.rag.answer import RAG
from medrag.rag.overview import unverified_dates
from medrag.retrieval.retriever import MODES, Retriever
from medrag.security import audit
from medrag.security.access import LOCAL_ADMIN, User, auth_enabled, authenticate

STATIC = Path(__file__).parent / "static"
s = get_settings()
_sessions: dict[str, User] = {}  # sign-in token -> user, in memory: a restart signs everyone out
_search_lock = threading.Lock()  # the retriever's caches and the reranker are shared by every request
_ingest_lock = threading.Lock()  # one addition at a time: each rewrites raw tables
_loaded: dict[str, tuple[str, Retriever]] = {}  # index path -> (built_at, retriever) in use
_load_lock = threading.Lock()
RELOAD_EVERY = 10  # seconds between checks for a new index version


def _indexes() -> list[Path]:
    return sorted(p for p in s.index_dir.glob("*") if (p / "manifest.json").exists()) if s.index_dir.exists() else []


def _manifest(path: Path) -> dict:
    return json.loads((path / "manifest.json").read_text())


def retriever(name: str | None = None) -> Retriever:
    """The loaded retriever for an index. Loaded here only the first time; newer versions are swapped in by
    _reload_loop, so a question never waits for a rebuilt index to load."""
    found = _indexes()
    if not found:
        raise HTTPException(503, "No index found. Build one first: python -m medrag pipeline")
    default = next((p for p in found if p == s.index_path()), found[0])
    path = next((p for p in found if p.name == name), None) if name else default
    if path is None:
        raise HTTPException(404, f"Unknown index {name!r}")
    key = str(path)
    if key not in _loaded:
        with _load_lock:
            if key not in _loaded:
                built = _manifest(path)["built_at"]
                _loaded[key] = (built, Retriever(Index(path)))
    return _loaded[key][1]


def _reload_loop(stop: threading.Event) -> None:
    """Load each new index version (written by `python -m medrag watch`) next to the one in use, then swap.
    Questions in flight finish on the version they started with."""
    while not stop.wait(RELOAD_EVERY):
        for key, (built, _) in list(_loaded.items()):
            try:
                new = _manifest(Path(key))["built_at"]
                if new != built:
                    t0 = time.time()
                    fresh = Retriever(Index(Path(key)))
                    _loaded[key] = (new, fresh)
                    print(f"[{datetime.now():%H:%M:%S}] switched to index built {new} (loaded in {time.time() - t0:.0f}s)")
            except Exception as e:  # a build still being written, or a disk hiccup: keep the version in use
                print(f"[{datetime.now():%H:%M:%S}] index reload skipped: {e}")


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
    stop = threading.Event()
    threading.Thread(target=_reload_loop, args=(stop,), daemon=True, name="index-reload").start()
    yield
    stop.set()


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
        "indexes": [{"name": p.name, **{k: _manifest(p).get(k) for k in ("chunks", "dim", "built_at")},
                     "in_use": _loaded[str(p)][0] if str(p) in _loaded else None} for p in found],
        "default_index": next((p.name for p in found if p == s.index_path()), found[0].name if found else None),
        "llm": f"{s.llm_provider}:{s.llm_model}",
        "modes": list(MODES),
        "top_k": s.top_k,
    }


# ---------------- chat ----------------
class Turn(BaseModel):
    question: str = Field(max_length=2000)
    answer: str = Field(max_length=20000)


class Ask(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    llm: str | None = None
    mode: str = "hybrid+rerank"
    top_k: int | None = Field(None, ge=1, le=20)
    index: str | None = None
    history: list[Turn] = Field(default_factory=list, max_length=10)  # earlier turns, oldest first, for follow-ups


@app.post("/api/ask")
def ask(body: Ask, user: User = Depends(current_user)):
    if body.mode not in MODES:
        raise HTTPException(400, f"mode must be one of {list(MODES)}")
    ret = retriever(body.index)
    try:
        rag = RAG(ret, get_llm(body.llm or f"{s.llm_provider}:{s.llm_model}"))
        with _search_lock:
            r, facts, stream = rag.stream(body.question, body.mode, user=user, k=body.top_k,
                                          history=[t.model_dump() for t in body.history])
    except (ValueError, PermissionError) as e:
        raise HTTPException(400, str(e))

    cols = ["doc_id", "via", "score", "patient_name", "mrn", "study_date", "modality", "body_part", "priority", "text"]
    meta = {"type": "meta", "filters": r.filters.describe(), "notes": r.notes, "facts": facts,
            "sources": _records(r.hits[[c for c in cols if c in r.hits.columns]]), "overview": r.overview}

    def lines():
        yield json.dumps(meta) + "\n"
        text = ""
        try:
            for piece in stream:
                text += piece
                yield json.dumps({"type": "token", "text": piece}) + "\n"
        except Exception as e:  # the LLM failed mid-answer: say so instead of cutting the stream silently
            yield json.dumps({"type": "error", "text": str(e)[:300]}) + "\n"
        if r.overview:  # dates the LLM wrote that match none of the patient's studies or documents
            yield json.dumps({"type": "check", "unverified_dates": unverified_dates(text, r.overview)}) + "\n"
        yield json.dumps({"type": "done"}) + "\n"

    return StreamingResponse(lines(), media_type="application/x-ndjson")


# ---------------- new records ----------------
# Checked here because cleaning would otherwise drop them silently (unknown modality, future date, no text).
class NewPatient(BaseModel):
    mrn: str = Field(pattern=r"^[A-Za-z0-9-]{3,30}$")
    full_name: str = Field(min_length=2, max_length=120)
    gender: str | None = None
    date_of_birth: date | None = None
    blood_group: str | None = None
    city: str | None = None


class NewStudy(BaseModel):
    study_date: datetime
    modality: str
    body_part: str = Field(min_length=2, max_length=40)
    priority: str = "routine"
    indication: str | None = None
    referring_physician: str | None = None
    radiologist: str | None = None
    status: str = "final"
    report_text: str = Field(min_length=20, max_length=20000)

    @field_validator("modality")
    @classmethod
    def known_modality(cls, v: str) -> str:
        if v.strip().lower() not in C.MODALITY_SYNONYMS and v.strip().upper() not in C.MODALITIES:
            raise ValueError(f"unknown modality; use one of {', '.join(C.MODALITIES)}")
        return v.strip()

    @field_validator("study_date")
    @classmethod
    def not_future(cls, v: datetime) -> datetime:
        if v.replace(tzinfo=None) > datetime.now():
            raise ValueError("study_date is in the future")
        return v.replace(tzinfo=None)

    @field_validator("report_text")
    @classmethod
    def has_impression(cls, v: str) -> str:
        if not any(line.upper().startswith("IMPRESSION:") for line in v.splitlines()):
            raise ValueError("report_text needs an 'IMPRESSION:' line (the finding shown in tables and counts)")
        return v


class NewDocument(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    specialty: str | None = None
    doc_date: date
    text: str = Field(max_length=100000)
    description: str | None = None

    @field_validator("text")
    @classmethod
    def long_enough(cls, v: str) -> str:
        if len(v.split()) < 15:
            raise ValueError("document text needs at least 15 words")
        return v


class Ingest(BaseModel):
    patient: NewPatient
    studies: list[NewStudy] = Field(default_factory=list, max_length=50)
    documents: list[NewDocument] = Field(default_factory=list, max_length=20)
    conditions: list[str] = Field(default_factory=list, max_length=20)


@app.post("/api/ingest")
def ingest(body: Ingest, user: User = Depends(current_user)):
    """Add a patient (or more records for an existing MRN). Searchable after the next sync by `python -m medrag watch`."""
    if user.role != "admin":
        raise HTTPException(403, "Only admins can add records.")
    from medrag.ingest.live import add_records

    with _ingest_lock:
        ids = add_records(body.patient.model_dump(), [x.model_dump() for x in body.studies],
                          [x.model_dump() for x in body.documents], body.conditions)
    audit.append("audit", {"user": user.username, "role": user.role, "event": "ingest", "patient_id": ids["patient_id"],
                           "study_ids": ids["study_ids"], "document_ids": ids["document_ids"]})
    return ids | {"next": "Searchable after the next sync: `python -m medrag watch` checks for changes every 30 s."}


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
