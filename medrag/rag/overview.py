"""Patient overviews built straight from the index: every study, finding, recommendation and document is exact.

For "tell me about <patient>" the user sees these tables, and the LLM writes only a short summary on top
(rag/answer.py). Small LLMs that rewrote the whole history mixed up patients, dates and recommendations.
"""
import re

import pandas as pd
from rapidfuzz import fuzz

from medrag.data import catalog as C
from medrag.retrieval.query_parser import Filters
from medrag.retrieval.retriever import Retriever

# Words that ask for a patient's overall picture rather than something specific about them.
OVERVIEW_WORDS = set("""tell me about summary summarise summarize summarised summarized summarizing overview history
imaging show give patient patients details detail info information the of for on a an in to lines line two three short
brief briefly please now and what who is everything all records record profile describe explain his her their s
case quick quickly can you i want know more""".split())
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def is_overview(question: str, f: Filters) -> bool:
    """A question that names a patient and asks for nothing narrower ("daniellie chang", "summary about X")."""
    if not f.patient_ids or f.unresolved_patient:
        return False
    if (f.modality or f.body_part or f.priority or f.date_from is not None or f.date_to is not None or f.findings
            or f.documents or f.aggregate or f.abnormal_only or f.latest):
        return False
    name_words = {w for n in f.patient_names for w in n.lower().split()}
    for w in re.findall(r"[a-z]+", question.lower()):
        if w in OVERVIEW_WORDS or w in name_words:
            continue
        if any(fuzz.ratio(w, n) >= 75 for n in name_words):  # a misspelt name word ("daniellie")
            continue
        return False
    return True


def _recommendation(text: str) -> str:
    m = re.search(r"RECOMMENDATION:\s*(.+)", text or "")
    return m.group(1).strip() if m else ""


def patient_overview(retriever: Retriever, patient_id: int, scope: pd.Series | None = None) -> dict:
    """Everything the index holds about one patient, newest first. scope: rows the user may see."""
    meta = retriever.meta if scope is None else retriever.meta[scope]
    mine = meta[meta["patient_id"] == patient_id]
    profile = mine[mine["doc_type"] == "patient"].sort_values("part")
    head = profile["text"].iloc[0] if len(profile) else ""
    sex_age = re.search(r"\|\s*(\w+), age (\d+)", head)
    cond = re.search(r"Chronic conditions:\s*(.+?)\.?\s*$", head, re.M)
    st = mine[(mine["doc_type"] == "study") & (mine["part"] == 0)].sort_values("study_date", ascending=False)
    studies = [{
        "date": f"{x.study_date:%Y-%m-%d}", "study_id": int(x.study_id), "modality": C.MODALITY_NAMES.get(x.modality, x.modality),
        "body_part": x.body_part, "priority": x.priority, "finding": x.impression or "(no report)",
        "abnormal": bool(retriever._abnormal[x.Index]), "recommendation": _recommendation(x.text),
    } for x in st.itertuples()]
    docs = mine[(mine["doc_type"] == "document") & (mine["part"] == 0)].sort_values("study_date", ascending=False)
    documents = []
    for x in docs.itertuples():
        summary = re.search(r"^Summary:\s*(.+)$", x.text, re.M)
        documents.append({"date": f"{x.study_date:%Y-%m-%d}", "doc_id": x.doc_id, "title": x.title, "specialty": x.specialty,
                          "source": x.source, "conclusion": (x.impression if isinstance(x.impression, str) and x.impression
                                                             else summary.group(1).strip() if summary else "")})
    first = mine.iloc[0] if len(mine) else None
    return {
        "patient_id": int(patient_id), "name": first.patient_name if first is not None else "",
        "mrn": first.mrn if first is not None else "",
        "gender": sex_age.group(1) if sex_age else None, "age": int(sex_age.group(2)) if sex_age else None,
        "conditions": cond.group(1) if cond and "none recorded" not in cond.group(1).lower() else "",
        "studies": studies, "abnormal": sum(s["abnormal"] for s in studies), "documents": documents,
    }


def _words(s: str) -> set[str]:
    return {w[:6] for w in re.findall(r"[a-z]{5,}", s.lower())}


def _dated_words(o: dict) -> dict[str, set[str]]:
    by_date: dict[str, set[str]] = {}
    for s in o["studies"]:
        by_date.setdefault(s["date"], set()).update(_words(f"{s['modality']} {s['body_part']} {s['finding']}"))
    for d in o["documents"]:
        by_date.setdefault(d["date"], set()).update(_words(f"{d['title']} {d['specialty']} {d['conclusion']}"))
    return by_date


def unverified_dates(text: str, overviews: list[dict]) -> list[str]:
    """Problems with the dates in an answer: a date with no study or document of the patient, a date that belongs
    to another patient of the same name (each date is checked against the last MRN written before it), or a
    sentence whose finding shares no word with the record for that date. Empty when everything checks out."""
    per_mrn = {o["mrn"].upper(): _dated_words(o) for o in overviews}
    pooled: dict[str, set[str]] = {}
    for by_date in per_mrn.values():
        for date, words in by_date.items():
            pooled.setdefault(date, set()).update(words)
    problems, mrn = {}, None
    for sentence in re.split(r"(?<=[.!?])\s+|\n", text):
        for m in re.finditer(r"\bMRN\d+\b|\b\d{4}-\d{2}-\d{2}\b", sentence, re.I):
            token = m.group(0)
            if token.upper().startswith("MRN"):
                mrn = token.upper() if token.upper() in per_mrn else mrn
                continue
            records = per_mrn[mrn] if mrn and len(per_mrn) > 1 else pooled
            if token not in records:
                other = next((k for k, v in per_mrn.items() if token in v), None)
                problems[token] = (f"{token} (belongs to the other patient, {other})" if other
                                   else f"{token} (no such study or document)")
            elif not (_words(DATE_RE.sub("", sentence)) & records[token]):
                problems.setdefault(token, f"{token} (does not match the record for that date)")
    return sorted(problems.values())
