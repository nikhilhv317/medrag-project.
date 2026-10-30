#!/bin/sh
set -e
# A -> B -> C on the CPU, one after another (sharing 4 cores would slow every job down).
cd /d/LLM/medrag
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
$PY -m medrag bench embed --models medcpt:ncbi/MedCPT,sentence-transformers:BAAI/bge-base-en-v1.5,sentence-transformers:intfloat/e5-base-v2,sentence-transformers:NeuML/pubmedbert-base-embeddings,ollama:nomic-embed-text > reports/bench_embed_all.log 2>&1
echo "embed done $?"
$PY -m medrag bench chunk > reports/bench_chunk_all.log 2>&1
echo "chunk done $?"
$PY -m medrag bench tune > reports/bench_tune_all.log 2>&1
echo "tune done $?"
